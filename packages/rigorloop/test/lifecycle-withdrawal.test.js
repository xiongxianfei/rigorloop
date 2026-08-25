import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml } from "../dist/lib/lifecycle-contract.js";

const sha = (value) => createHash("sha256").update(value).digest("hex");

async function fixture(currentStage = "verify") {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-withdrawal-"));
  const canonicalRoot = join(root, "docs", "changes", "canonical");
  const duplicateRoot = join(root, "docs", "changes", "duplicate");
  mkdirSync(canonicalRoot, { recursive: true });
  mkdirSync(join(duplicateRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "docs", "architecture"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  const artifactPath = "docs/architecture/shared.md";
  const artifact = "# Shared architecture\n\n## Owning change record\n\n`docs/changes/canonical/change.yaml`\n";
  writeFileSync(join(root, artifactPath), artifact, "utf8");
  const change = (id, stage) => `change_id: ${id}
title: ${id}
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  architecture:
    kind: architecture
    path: ${artifactPath}
    role: primary
    lifecycle_state: approved
workflow_state:
  lifecycle_state: ${id === "canonical" ? "complete" : "active"}
  current_stage: ${stage}
  next_stage: ${stage}
  blocker: null
lifecycle_cli:
  schema_version: 2
  artifacts:
    architecture:
      artifact_kind: architecture
      artifact_role: primary
      artifact_path: ${artifactPath}
      artifact_sha256: ${sha(artifact)}
      stage_authority: architecture
  reviews: {}
  validations: {}
  resolutions: {}
  milestones: {}
  correction_history: {}
  withdrawals: {}
`;
  writeFileSync(join(canonicalRoot, "change.yaml"), change("canonical", "complete"), "utf8");
  writeFileSync(join(duplicateRoot, "change.yaml"), change("duplicate", currentStage), "utf8");
  writeFileSync(join(duplicateRoot, "review-log.md"), "Review ID: architecture-review-r1\nOpen findings: none\n", "utf8");
  return { root, canonicalRoot, duplicateRoot, artifactPath };
}

function revision(root) {
  return executeLifecycleCli(["status", "--change", "duplicate", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

function request(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

test("workflow withdraws only a proved duplicate architecture registration", async () => {
  const { root, canonicalRoot, duplicateRoot, artifactPath } = await fixture();
  const artifactBefore = readFileSync(join(root, artifactPath));
  const canonicalBefore = readFileSync(join(canonicalRoot, "change.yaml"));
  const logBefore = readFileSync(join(duplicateRoot, "review-log.md"));
  const current = revision(root);
  const evidencePath = "docs/changes/duplicate/evidence/withdrawal.md";
  writeFileSync(join(root, evidencePath), `Change ID: duplicate
Artifact ID: architecture
Artifact path: ${artifactPath}
Canonical owner: canonical
Reason: duplicate-registration
Lifecycle revision: ${current}
`, "utf8");
  const body = {
    schema_version: 1, operation: "withdraw-artifact-registration", change_id: "duplicate", expected_lifecycle_revision: current,
    artifact_id: "architecture", artifact_path: artifactPath, canonical_owner_change_id: "canonical", reason: "duplicate-registration",
    evidence_path: evidencePath, stage_authority: "workflow",
  };
  const path = request(root, "withdraw", body);
  const execution = executeLifecycleCli(["withdraw-artifact-registration", "--request", path, "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.equal(execution.result.operation_result.canonical_owner_change_id, "canonical");
  assert.equal(execution.result.operation_result.receipt_status, "withdrawn");
  assert.match(execution.human, /docs\/architecture\/shared\.md; withdrawn; canonical owner canonical/);
  const changed = parseLifecycleYaml(readFileSync(join(duplicateRoot, "change.yaml"), "utf8"));
  assert.equal(changed.artifact_states.architecture, undefined);
  assert.equal(changed.lifecycle_cli.artifacts.architecture, undefined);
  const [receipt] = Object.values(changed.lifecycle_cli.withdrawals);
  assert.equal(receipt.status, "withdrawn");
  assert.equal(receipt.canonical_owner_change_id, "canonical");
  assert.equal(receipt.prior_lifecycle_revision, current);
  assert.equal(receipt.resulting_lifecycle_revision, undefined);
  assert.deepEqual(readFileSync(join(root, artifactPath)), artifactBefore);
  assert.deepEqual(readFileSync(join(canonicalRoot, "change.yaml")), canonicalBefore);
  assert.deepEqual(readFileSync(join(duplicateRoot, "review-log.md")), logBefore);

  const replay = request(root, "withdraw-replay", { ...body, expected_lifecycle_revision: revision(root) });
  const replayed = executeLifecycleCli(["withdraw-artifact-registration", "--request", replay, "--format", "json"], { cwd: root });
  assert.equal(replayed.result.status, "already-recorded", JSON.stringify(replayed.result));
});

test("withdrawal refuses an active artifact and ownership-pointer mismatch without mutation", async () => {
  const active = await fixture("architecture");
  const activePath = join(active.duplicateRoot, "change.yaml");
  const activeBefore = readFileSync(activePath);
  let current = revision(active.root);
  let evidencePath = "docs/changes/duplicate/evidence/withdrawal.md";
  writeFileSync(join(active.root, evidencePath), `Change ID: duplicate\nArtifact ID: architecture\nArtifact path: ${active.artifactPath}\nCanonical owner: canonical\nReason: duplicate-registration\nLifecycle revision: ${current}\n`, "utf8");
  let path = request(active.root, "active", { schema_version: 1, operation: "withdraw-artifact-registration", change_id: "duplicate", expected_lifecycle_revision: current, artifact_id: "architecture", artifact_path: active.artifactPath, canonical_owner_change_id: "canonical", reason: "duplicate-registration", evidence_path: evidencePath, stage_authority: "workflow" });
  let result = executeLifecycleCli(["withdraw-artifact-registration", "--request", path, "--format", "json"], { cwd: active.root });
  assert.equal(result.result.errors[0].code, "RL_WITHDRAWAL_UNSAFE");
  assert.deepEqual(readFileSync(activePath), activeBefore);

  const mismatch = await fixture();
  writeFileSync(join(mismatch.root, mismatch.artifactPath), "# Shared architecture\n\n## Owning change record\n\n`docs/changes/another/change.yaml`\n", "utf8");
  current = revision(mismatch.root);
  evidencePath = "docs/changes/duplicate/evidence/withdrawal.md";
  writeFileSync(join(mismatch.root, evidencePath), `Change ID: duplicate\nArtifact ID: architecture\nArtifact path: ${mismatch.artifactPath}\nCanonical owner: canonical\nReason: duplicate-registration\nLifecycle revision: ${current}\n`, "utf8");
  path = request(mismatch.root, "mismatch", { schema_version: 1, operation: "withdraw-artifact-registration", change_id: "duplicate", expected_lifecycle_revision: current, artifact_id: "architecture", artifact_path: mismatch.artifactPath, canonical_owner_change_id: "canonical", reason: "duplicate-registration", evidence_path: evidencePath, stage_authority: "workflow" });
  result = executeLifecycleCli(["withdraw-artifact-registration", "--request", path, "--format", "json"], { cwd: mismatch.root });
  assert.equal(result.result.errors[0].code, "RL_WITHDRAWAL_UNSAFE");
});

test("withdrawal rejects wrong kind, wrong path, unknown reason, and stale revision without mutation", async () => {
  for (const scenario of ["wrong-kind", "wrong-path", "unknown-reason", "stale"]) {
    const state = await fixture();
    const selectedPath = join(state.duplicateRoot, "change.yaml");
    if (scenario === "wrong-kind") writeFileSync(selectedPath, readFileSync(selectedPath, "utf8").replaceAll("kind: architecture", "kind: spec").replaceAll("artifact_kind: architecture", "artifact_kind: spec"), "utf8");
    const current = revision(state.root);
    const evidencePath = "docs/changes/duplicate/evidence/withdrawal.md";
    writeFileSync(join(state.root, evidencePath), `Change ID: duplicate\nArtifact ID: architecture\nArtifact path: ${state.artifactPath}\nCanonical owner: canonical\nReason: duplicate-registration\nLifecycle revision: ${current}\n`, "utf8");
    const before = readFileSync(selectedPath);
    const body = {
      schema_version: 1, operation: "withdraw-artifact-registration", change_id: "duplicate", expected_lifecycle_revision: scenario === "stale" ? `sha256:${"0".repeat(64)}` : current,
      artifact_id: "architecture", artifact_path: scenario === "wrong-path" ? "docs/architecture/other.md" : state.artifactPath,
      canonical_owner_change_id: "canonical", reason: scenario === "unknown-reason" ? "cleanup" : "duplicate-registration",
      evidence_path: evidencePath, stage_authority: "workflow",
    };
    const path = request(state.root, scenario, body);
    const execution = executeLifecycleCli(["withdraw-artifact-registration", "--request", path, "--format", "json"], { cwd: state.root });
    assert.equal(execution.result.errors[0].code, scenario === "stale" ? "RL_STALE_OPERATION" : "RL_WITHDRAWAL_UNSAFE", scenario);
    assert.deepEqual(readFileSync(selectedPath), before, scenario);
  }
});
