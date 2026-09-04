import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { evaluateCompactCandidate, runCompactTransaction } from "../dist/lib/compact-transaction.js";

const hash = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;
const rev = (letter) => `sha256:${letter.repeat(64)}`;

async function fixture(candidateText = "candidate\n") {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-race-"));
  const path = "docs/changes/example/change.yaml";
  mkdirSync(join(root, "docs/changes/example"), { recursive: true });
  writeFileSync(join(root, path), "prior\n");
  const prior = Buffer.from("prior\n");
  const request = {
    schema: "compact-operation-v1", operation: "advance-stage", change_id: "example", expected_lifecycle_revision: rev("a"),
    expected_files: { [path]: { path, state: "present", identity: hash(prior) } },
    payload: { from_stage: "proposal", to_stage: "proposal-review" },
  };
  const candidateFiles = { [path]: { path, action: "replace", identity: hash(candidateText), source: "inline", content: candidateText, source_path: null } };
  return { root, path, candidate: evaluateCompactCandidate({ request, currentFiles: { [path]: prior }, candidateFiles, candidateLifecycleRevision: rev("b"), validateCandidateSet: () => true }) };
}

test("a live competing writer is busy and only the lock owner changes bytes", async () => {
  const item = await fixture();
  let competing;
  const owner = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => {
    if (point === "after-lock") competing = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true });
    return null;
  } });
  assert.equal(owner.status, "success");
  assert.equal(competing.status, "busy");
  assert.equal(readFileSync(join(item.root, item.path), "utf8"), "candidate\n");
});

test("identical uncertain retry is already-applied and conflicting replay is stale", async () => {
  const item = await fixture();
  assert.equal(runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true }).status, "success");
  const identical = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true });
  assert.equal(identical.status, "already-applied");
  assert.equal(identical.bytes_changed, false);

  const conflicting = await fixture("different\n");
  writeFileSync(join(conflicting.root, conflicting.path), "somebody else\n");
  const rejected = runCompactTransaction({ root: conflicting.root, candidate: conflicting.candidate, validateCandidateSet: () => true });
  assert.equal(rejected.status, "rejected");
  assert.equal(rejected.errors[0].code, "RL_STALE_OPERATION");
  assert.equal(readFileSync(join(conflicting.root, conflicting.path), "utf8"), "somebody else\n");
});

test("compact recovery implementation has no Git, PR, network, process, or log dependency", () => {
  const source = readFileSync(new URL("../dist/lib/compact-transaction.js", import.meta.url), "utf8");
  assert.doesNotMatch(source, /child_process|https?:|\.git\b|pull.request|diagnostic.log|local.log/i);
});
