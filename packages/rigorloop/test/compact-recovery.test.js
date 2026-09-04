import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { chmodSync, existsSync, mkdirSync, readFileSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { evaluateCompactCandidate, inspectCompactTransaction, recoverCompactTransaction, runCompactTransaction } from "../dist/lib/compact-transaction.js";

const hash = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;
const rev = (letter) => `sha256:${letter.repeat(64)}`;

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-recovery-"));
  const paths = ["docs/changes/example/change.yaml", "docs/changes/example/evidence.yaml"];
  for (const path of paths) mkdirSync(join(root, path, ".."), { recursive: true });
  writeFileSync(join(root, paths[0]), "prior change\n");
  writeFileSync(join(root, paths[1]), "prior evidence\n");
  const currentFiles = Object.fromEntries(paths.map((path) => [path, readFileSync(join(root, path))]));
  const contents = { [paths[0]]: "candidate change\n", [paths[1]]: "candidate evidence\n" };
  const request = {
    schema: "compact-operation-v1", operation: "advance-stage", change_id: "example", expected_lifecycle_revision: rev("a"),
    expected_files: Object.fromEntries(paths.map((path) => [path, { path, state: "present", identity: hash(currentFiles[path]) }])),
    payload: { from_stage: "proposal", to_stage: "proposal-review" },
  };
  const candidateFiles = Object.fromEntries(paths.map((path) => [path, { path, action: "replace", identity: hash(contents[path]), source: "inline", content: contents[path], source_path: null }]));
  const candidate = evaluateCompactCandidate({ request, currentFiles, candidateFiles, candidateLifecycleRevision: rev("b"), validateCandidateSet: () => true });
  const readCompleteSet = () => Object.fromEntries(paths.map((path) => [path, readFileSync(join(root, path))]));
  return { root, paths, candidate, readCompleteSet };
}

test("mixed interrupted replacement blocks readers and restores the exact prior set", async () => {
  const item = await fixture();
  const crashed = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === `after-replace:${item.paths[0]}` ? "crash" : null });
  assert.equal(crashed.status, "recovery-required");
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  assert.equal(inspection.status, "recovery-required");
  const lock = join(item.root, ".rigorloop/transactions/example/lock");
  unlinkSync(lock);
  const recovered = recoverCompactTransaction({ root: item.root, changeId: "example", action: "restore-prior", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(recovered.status, "success");
  assert.equal(readFileSync(join(item.root, item.paths[0]), "utf8"), "prior change\n");
  assert.equal(readFileSync(join(item.root, item.paths[1]), "utf8"), "prior evidence\n");
});

test("persisted interrupted candidate can be accepted only after complete validation", async () => {
  const item = await fixture();
  const crashed = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === "after-persisted-readback" ? "crash" : null });
  assert.equal(crashed.status, "recovery-required");
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  unlinkSync(join(item.root, ".rigorloop/transactions/example/lock"));
  const accepted = recoverCompactTransaction({ root: item.root, changeId: "example", action: "accept-candidate", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(accepted.status, "success");
  assert.equal(readFileSync(join(item.root, item.paths[0]), "utf8"), "candidate change\n");
  assert.equal(existsSync(join(item.root, ".rigorloop/transactions/example")), false);
});

test("tampered recovery content fails closed without exposing private bytes", async () => {
  const item = await fixture();
  const crashed = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === "after-recovery-prepared" ? "crash" : null });
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  unlinkSync(join(item.root, ".rigorloop/transactions/example/lock"));
  writeFileSync(join(item.root, ".rigorloop/transactions/example/prior/0000"), "tampered secret\n");
  const result = recoverCompactTransaction({ root: item.root, changeId: "example", action: "restore-prior", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(result.status, "recovery-required");
  assert.equal(JSON.stringify(result).includes("tampered secret"), false);
});

test("transaction-private state is owner-only and weak preexisting state rejects", async () => {
  const item = await fixture();
  const observed = {};
  const crashed = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => {
    if (point === "after-recovery-prepared") {
      const tx = join(item.root, ".rigorloop/transactions/example");
      observed.directory = statSync(tx).mode & 0o777;
      observed.lock = statSync(join(tx, "lock")).mode & 0o777;
      observed.recovery = statSync(join(tx, "recovery.yaml")).mode & 0o777;
      return "crash";
    }
    return null;
  } });
  assert.equal(crashed.status, "recovery-required");
  assert.deepEqual(observed, { directory: 0o700, lock: 0o600, recovery: 0o600 });

  const other = await fixture();
  const tx = join(other.root, ".rigorloop/transactions/example");
  mkdirSync(tx, { recursive: true, mode: 0o755 });
  chmodSync(tx, 0o755);
  const rejected = runCompactTransaction({ root: other.root, candidate: other.candidate, validateCandidateSet: () => true });
  assert.equal(rejected.status, "rejected");
  assert.equal(rejected.errors[0].code, "RL_UNSAFE_PATH");
});

test("unsafe recovery lock and unsupported durability fail before replacement", async () => {
  const item = await fixture();
  const unsupported = runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, durabilityProbe: () => false });
  assert.equal(unsupported.status, "rejected");
  assert.equal(unsupported.errors[0].code, "RL_UNSUPPORTED_DURABILITY");
  assert.equal(readFileSync(join(item.root, item.paths[0]), "utf8"), "prior change\n");

  const other = await fixture();
  const tx = join(other.root, ".rigorloop/transactions/example");
  mkdirSync(tx, { recursive: true, mode: 0o700 });
  writeFileSync(join(tx, "outside"), "not a lock\n");
  const { symlinkSync } = await import("node:fs");
  symlinkSync("outside", join(tx, "lock"));
  const unsafe = runCompactTransaction({ root: other.root, candidate: other.candidate, validateCandidateSet: () => true });
  assert.equal(unsafe.status, "rejected");
  assert.equal(unsafe.errors[0].code, "RL_UNSAFE_PATH");
});

test("a rejected recovery action releases its lock and permits exact prior restoration", async () => {
  const item = await fixture();
  runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === "after-recovery-prepared" ? "crash" : null });
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  unlinkSync(join(item.root, ".rigorloop/transactions/example/lock"));
  const premature = recoverCompactTransaction({ root: item.root, changeId: "example", action: "accept-candidate", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(premature.status, "recovery-required");
  assert.equal(existsSync(join(item.root, ".rigorloop/transactions/example/lock")), false);
  const restored = recoverCompactTransaction({ root: item.root, changeId: "example", action: "restore-prior", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(restored.status, "success");
});

test("prepared recovery discards staging without rewriting an untouched prior set", async () => {
  const item = await fixture();
  runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === "after-recovery-prepared" ? "crash" : null });
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  unlinkSync(join(item.root, ".rigorloop/transactions/example/lock"));
  const restored = recoverCompactTransaction({ root: item.root, changeId: "example", action: "restore-prior", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(restored.status, "success");
  assert.equal(restored.bytes_changed, false);
  assert.deepEqual(restored.affected_paths, []);
});

test("recovery refuses an authoritative file outside both recorded identities", async () => {
  const item = await fixture();
  runCompactTransaction({ root: item.root, candidate: item.candidate, validateCandidateSet: () => true, fault: (point) => point === `after-replace:${item.paths[0]}` ? "crash" : null });
  const inspection = inspectCompactTransaction({ root: item.root, changeId: "example" });
  unlinkSync(join(item.root, ".rigorloop/transactions/example/lock"));
  writeFileSync(join(item.root, item.paths[0]), "unrelated authoritative bytes\n");
  const refused = recoverCompactTransaction({ root: item.root, changeId: "example", action: "restore-prior", expectedRecoveryIdentity: inspection.recovery_identity, readCompleteSet: item.readCompleteSet, validateCandidateSet: () => true });
  assert.equal(refused.status, "recovery-required");
  assert.equal(readFileSync(join(item.root, item.paths[0]), "utf8"), "unrelated authoritative bytes\n");
});
