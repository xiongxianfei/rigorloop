// Repository metadata validation reuses the recorder's read-only, bounded checks.
import { basename, dirname, resolve } from "node:path";
import { executeRecordStore } from "../packages/rigorloop/dist/lib/record-store.js";
import { validateRecordStoreSet } from "../packages/rigorloop/dist/lib/record-store-contract.js";

try {
  if (process.argv.length !== 3) throw new Error();
  const path = resolve(process.argv[2]), changeDirectory = dirname(path);
  const changes = dirname(changeDirectory), docs = dirname(changes);
  if (basename(path) !== "change.yaml" || basename(changes) !== "changes" || basename(docs) !== "docs") throw new Error();
  const changeId = basename(changeDirectory);
  const result = executeRecordStore({ root: dirname(docs), changeId, operation: "inspect" });
  if (result.status !== "inspected" || result.revision === null) throw new Error();
  validateRecordStoreSet(changeId, Object.fromEntries(result.snapshot.records.map(record => [record.path, record.content])));
  process.stdout.write("Explicit recording structure and references valid; no readiness judgment.\n");
} catch {
  process.stderr.write("Invalid or unavailable explicit recording set.\n");
  process.exitCode = 1;
}
