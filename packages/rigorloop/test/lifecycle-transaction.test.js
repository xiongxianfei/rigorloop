import assert from "node:assert/strict";
import { chmodSync, existsSync, mkdirSync, readFileSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { inspectLifecycleLock, inspectLifecycleRecovery, lifecycleTransactionPaths, reconcileInterruptedTransaction, runLifecycleTransaction } from "../dist/lib/lifecycle-transaction.js";
import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { changeBytes, lifecycleRevision, packageContext, packageRepository, writePackageReview, writeRequest } from "./helpers/lifecycle-package-fixture.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-tx-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(changeRoot, { recursive: true });
  const changePath = join(changeRoot, "change.yaml");
  writeFileSync(changePath, "change_id: example\nvalue: prior\n", "utf8");
  return { root, changePath, prior: readFileSync(changePath), paths: lifecycleTransactionPaths(changePath) };
}

const valid = (bytes) => bytes.includes(Buffer.from("change_id: example"));

test("transaction replaces change.yaml and cleans fixed transient siblings", async () => {
  const item = await fixture();
  const result = runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "r1", currentRevision: "r1", candidateBytes: "change_id: example\nvalue: candidate\n", candidateRevision: "r2", validateCandidate: valid });
  assert.equal(result.status, "success");
  assert.match(readFileSync(item.changePath, "utf8"), /candidate/);
  assert.equal(existsSync(item.paths.lock), false);
  assert.equal(existsSync(item.paths.recovery), false);
  assert.equal(statSync(item.changePath).mode & 0o777, 0o644);
});

test("stale and busy operations do not change repository bytes", async () => {
  const item = await fixture();
  assert.throws(() => runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "old", currentRevision: "new", candidateBytes: "changed", candidateRevision: "r2", validateCandidate: valid }), { code: "RL_STALE_OPERATION" });
  assert.deepEqual(readFileSync(item.changePath), item.prior);
  assert.equal(statSync(item.changePath).mode & 0o777, 0o644);
  writeFileSync(item.paths.lock, JSON.stringify({ pid: process.pid }), { mode: 0o600 });
  assert.equal(inspectLifecycleLock(item.changePath).state, "live");
  assert.throws(() => runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "r1", currentRevision: "r1", candidateBytes: "changed", candidateRevision: "r2", validateCandidate: valid }), { code: "RL_OPERATION_BUSY" });
  assert.deepEqual(readFileSync(item.changePath), item.prior);
});

test("post-validation failure restores prior bytes", async () => {
  const item = await fixture();
  assert.throws(() => runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "r1", currentRevision: "r1", candidateBytes: "change_id: example\nvalue: bad\n", candidateRevision: "r2", validateCandidate: () => false }), { code: "RL_POST_VALIDATION_FAILED" });
  assert.deepEqual(readFileSync(item.changePath), item.prior);
  assert.equal(existsSync(item.paths.recovery), false);
  assert.equal(existsSync(item.paths.lock), false);
});

test("interruption before replacement leaves prior bytes and private recovery state", async () => {
  const item = await fixture();
  assert.throws(() => runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "r1", currentRevision: "r1", candidateBytes: "change_id: example\nvalue: next\n", candidateRevision: "r2", validateCandidate: valid, fault: (point) => point === "after-recovery-prepared" ? "crash" : null }), { code: "RL_POST_VALIDATION_FAILED" });
  assert.deepEqual(readFileSync(item.changePath), item.prior);
  const recovery = inspectLifecycleRecovery(item.changePath);
  assert.equal(recovery.observed, "prior");
  const abandonedCandidate = join(item.paths.recovery, "..", recovery.bundle.candidate_file);
  assert.equal(statSync(item.paths.lock).mode & 0o777, 0o600);
  assert.equal(statSync(item.paths.recovery).mode & 0o777, 0o600);
  unlinkSync(item.paths.lock);
  assert.deepEqual(reconcileInterruptedTransaction({ changePath: item.changePath, changeId: "example", validateCandidate: valid }), { status: "abandoned-prepared" });
  assert.equal(existsSync(abandonedCandidate), false);
});

test("interruption after replacement reconciles candidate identity", async () => {
  const item = await fixture();
  assert.throws(() => runLifecycleTransaction({ changePath: item.changePath, changeId: "example", expectedRevision: "r1", currentRevision: "r1", candidateBytes: "change_id: example\nvalue: next\n", candidateRevision: "r2", validateCandidate: valid, fault: (point) => point === "after-replace-before-phase" ? "crash" : null }), { code: "RL_POST_VALIDATION_FAILED" });
  assert.equal(inspectLifecycleRecovery(item.changePath).observed, "candidate");
  unlinkSync(item.paths.lock);
  assert.deepEqual(reconcileInterruptedTransaction({ changePath: item.changePath, changeId: "example", validateCandidate: valid }), { status: "committed-candidate" });
  assert.match(readFileSync(item.changePath, "utf8"), /next/);
});

test("package review post-validation failure restores the complete prior authority", async () => {
  const { root } = await packageRepository();
  const context = packageContext(root);
  const review = writePackageReview(root, context);
  const request = writeRequest(root, "package-post-validation", {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: lifecycleRevision(root),
    package_kind: "design",
    package_revision: review.packageFacts.aggregate_revision,
    upstream_binding: review.packageFacts.upstream_binding,
    member_artifact_ids: review.packageFacts.member_artifact_ids,
    evidence_path: review.reviewPath,
    stage_authority: "design-review",
  });
  const before = changeBytes(root);
  const execution = executeLifecycleCli(["record-package-review", "--request", request, "--format", "json"], {
    cwd: root,
    runLifecycleTransaction: (options) => runLifecycleTransaction({ ...options, validateCandidate: () => false }),
  });
  assert.equal(execution.result.errors[0].code, "RL_POST_VALIDATION_FAILED");
  assert.equal(changeBytes(root), before);
  assert.equal(inspectLifecycleRecovery(join(root, "docs", "changes", "example", "change.yaml")).state, "absent");
});
