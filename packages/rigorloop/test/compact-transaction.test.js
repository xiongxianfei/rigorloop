import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { evaluateCompactCandidate, runCompactTransaction } from "../dist/lib/compact-transaction.js";

const hash = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;
const revision = (letter) => `sha256:${letter.repeat(64)}`;

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-tx-"));
  const changePath = "docs/changes/example/change.yaml";
  const reviewPath = "docs/changes/example/reviews/proposal-review.md";
  const untouchedPath = "docs/proposals/example.md";
  mkdirSync(join(root, "docs/changes/example/reviews"), { recursive: true });
  mkdirSync(join(root, "docs/proposals"), { recursive: true });
  writeFileSync(join(root, changePath), "prior change\n");
  writeFileSync(join(root, reviewPath), "prior review\n");
  writeFileSync(join(root, untouchedPath), "untouched\n");
  return { root, changePath, reviewPath, untouchedPath };
}

function envelope(item, overrides = {}) {
  const currentFiles = {
    [item.changePath]: Buffer.from("prior change\n"),
    [item.reviewPath]: Buffer.from("prior review\n"),
  };
  const candidateFiles = {
    [item.changePath]: Buffer.from("candidate change\n"),
    [item.reviewPath]: Buffer.from("candidate review\n"),
  };
  const request = {
    schema: "compact-operation-v1",
    operation: "advance-stage",
    change_id: "example",
    expected_lifecycle_revision: revision("a"),
    expected_files: Object.fromEntries(Object.entries(currentFiles).map(([path, bytes]) => [path, { path, state: "present", identity: hash(bytes) }])),
    payload: {
      from_stage: "proposal",
      to_stage: "proposal-review",
    },
  };
  const derivedCandidateFiles = Object.fromEntries(Object.entries(candidateFiles).map(([path, bytes]) => [path, { path, action: "replace", identity: hash(bytes), source: "inline", content: bytes.toString("utf8"), source_path: null }]));
  return evaluateCompactCandidate({ request, currentFiles, candidateFiles: derivedCandidateFiles, candidateLifecycleRevision: revision("b"), validateCandidateSet: () => true, ...overrides });
}

test("pure evaluator binds every expected and affected file without filesystem I/O", async () => {
  const item = await fixture();
  const candidate = envelope(item);
  assert.deepEqual(candidate.affectedPaths, [item.changePath, item.reviewPath]);
  assert.equal(candidate.files[item.changePath].priorIdentity, hash("prior change\n"));
  assert.equal(candidate.files[item.reviewPath].candidateIdentity, hash("candidate review\n"));

  const missing = envelope(item);
  delete missing.request.expected_files[item.reviewPath];
  assert.throws(() => evaluateCompactCandidate({ request: missing.request, currentFiles: missing.currentFiles, candidateFiles: {}, candidateLifecycleRevision: revision("b"), validateCandidateSet: () => true }), { code: "RL_STALE_OPERATION" });
});

test("multi-file transaction publishes one validated set and preserves unrelated bytes", async () => {
  const item = await fixture();
  const untouched = readFileSync(join(item.root, item.untouchedPath));
  const result = runCompactTransaction({ root: item.root, candidate: envelope(item), validateCandidateSet: () => true });
  assert.equal(result.status, "success");
  assert.equal(result.bytes_changed, true);
  assert.deepEqual(result.affected_paths, [item.changePath, item.reviewPath]);
  assert.equal(readFileSync(join(item.root, item.changePath), "utf8"), "candidate change\n");
  assert.equal(readFileSync(join(item.root, item.reviewPath), "utf8"), "candidate review\n");
  assert.deepEqual(readFileSync(join(item.root, item.untouchedPath)), untouched);
  assert.equal(existsSync(join(item.root, ".rigorloop/transactions/example")), false);
});

test("recoverable adapter fault restores every prior byte before unlocking", async () => {
  const item = await fixture();
  const result = runCompactTransaction({
    root: item.root,
    candidate: envelope(item),
    validateCandidateSet: () => true,
    fault: (point) => point === `after-replace:${item.changePath}` ? "error" : null,
  });
  assert.equal(result.status, "rejected");
  assert.equal(result.errors[0].code, "RL_TRANSACTION_FAILED");
  assert.equal(readFileSync(join(item.root, item.changePath), "utf8"), "prior change\n");
  assert.equal(readFileSync(join(item.root, item.reviewPath), "utf8"), "prior review\n");
  assert.equal(existsSync(join(item.root, ".rigorloop/transactions/example")), false);
});

test("transaction limits reject before authoritative replacement", async () => {
  const item = await fixture();
  const oversized = envelope(item);
  oversized.requestBytes = 1024 * 1024 + 1;
  const result = runCompactTransaction({ root: item.root, candidate: oversized, validateCandidateSet: () => true });
  assert.equal(result.status, "rejected");
  assert.equal(result.errors[0].code, "RL_LIMIT_EXCEEDED");
  assert.equal(readFileSync(join(item.root, item.changePath), "utf8"), "prior change\n");

  const combined = envelope(item);
  combined.requestBytes = 1;
  const chunk = Buffer.alloc(8 * 1024 * 1024);
  for (let index = 0; index < 5; index += 1) {
    const path = `docs/changes/example/reviews/large-${index}.md`;
    combined.currentFiles[path] = chunk;
    combined.candidateSet[path] = chunk;
    combined.files[path] = { path, priorBytes: chunk, priorIdentity: hash(chunk), candidateBytes: chunk, candidateIdentity: hash(chunk) };
    combined.affectedPaths.push(path);
  }
  const tooLarge = runCompactTransaction({ root: item.root, candidate: combined, validateCandidateSet: () => true });
  assert.equal(tooLarge.status, "rejected");
  assert.equal(tooLarge.errors[0].code, "RL_LIMIT_EXCEEDED");
});

test("every ordinary fault boundary restores the complete prior set", async () => {
  for (const point of ["after-lock", "after-recovery-prepared", "after-phase-replacing", "after-replace:docs/changes/example/change.yaml", "after-replace:docs/changes/example/reviews/proposal-review.md", "during-cleanup"]) {
    const item = await fixture();
    const outcome = runCompactTransaction({ root: item.root, candidate: envelope(item), validateCandidateSet: () => true, fault: (observed) => observed === point ? "error" : null });
    assert.equal(outcome.status, "rejected", point);
    assert.equal(readFileSync(join(item.root, item.changePath), "utf8"), "prior change\n", point);
    assert.equal(readFileSync(join(item.root, item.reviewPath), "utf8"), "prior review\n", point);
    assert.equal(existsSync(join(item.root, ".rigorloop/transactions/example")), false, point);
  }
});
