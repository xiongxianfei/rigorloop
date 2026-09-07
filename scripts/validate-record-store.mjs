// Repository metadata validation reuses the recorder's read-only, bounded checks.
import { basename, dirname, resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { executeRecordStore } from "../packages/rigorloop/dist/lib/record-store.js";
import { parseRecordStore, validateRecordStoreSet } from "../packages/rigorloop/dist/lib/record-store-contract.js";

import { parseV2Record, validateV2Set } from "../packages/rigorloop/dist/lib/record-format-v2.js";

function snapshotFiles(root, changeId, revision, v2) {
  if (!/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(revision)) throw new Error();
  const git = args => execFileSync("git", ["-C", root, ...args],
    {maxBuffer: 1024 * 1024 + 1, timeout: 10000, stdio: ["ignore", "pipe", "pipe"]});
  const commit = git(["rev-parse", "--verify", `${revision}^{commit}`]).toString().trim();
  if (commit !== revision) throw new Error();
  let total = 0;
  const read = path => {
    const entry = git(["ls-tree", "-z", commit, "--", `:(literal)${path}`]).toString();
    const match = /^(100644|100755) blob ([a-f0-9]+)\t([^\0]+)\0$/.exec(entry);
    if (!match || match[3] !== path) throw new Error();
    const bytes = git(["cat-file", "blob", match[2]]);
    total += bytes.length;
    if (total > 65 * 1024 * 1024) throw new Error();
    return bytes;
  };
  const prefix=`docs/changes/${changeId}/`;
  if(git(["ls-tree", "-z", commit, "--", `:(literal)${prefix}${v2?"change.yaml":"change.json"}`]).length) throw new Error();
  const manifest = prefix+(v2?"change.json":"change.yaml");
  const files = {[manifest]: read(manifest)};
  const change = (v2?parseV2Record:parseRecordStore)("change", files[manifest]);
  if (change.change_id !== changeId) throw new Error();
  // Parsing validates the bounded registry before any supporting blob is read.
  for (const record of change.records) files[record.path] = read(record.path);
  return files;
}

try {
  const snapshot = process.argv.length === 5 && process.argv[3] === "--revision";
  if (process.argv.length !== 3 && !snapshot) throw new Error();
  const path = resolve(process.argv[2]), changeDirectory = dirname(path);
  const changes = dirname(changeDirectory), docs = dirname(changes);
  const v2=basename(path)==="change.json";
  if ((!v2 && basename(path) !== "change.yaml") || basename(changes) !== "changes" || basename(docs) !== "docs") throw new Error();
  const changeId = basename(changeDirectory);
  let files;
  if (snapshot) files = snapshotFiles(dirname(docs), changeId, process.argv[4], v2);
  else {
    const result = executeRecordStore({ root: dirname(docs), changeId, operation: "inspect" });
    if (result.status !== "inspected" || result.revision === null || !result.files.some(file=>file.path===`docs/changes/${changeId}/${basename(path)}`)) throw new Error();
    files = Object.fromEntries(result.snapshot.records.map(record => [record.path, record.content]));
  }
  (v2?validateV2Set:validateRecordStoreSet)(changeId, files);
  process.stdout.write("Explicit recording structure and references valid; no readiness judgment.\n");
} catch {
  process.stderr.write("Invalid or unavailable explicit recording set.\n");
  process.exitCode = 1;
}
