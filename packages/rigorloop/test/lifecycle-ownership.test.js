import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";

const sha = (value) => createHash("sha256").update(value).digest("hex");

async function repository() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-ownership-"));
  mkdirSync(join(root, "docs", "changes", "canonical"), { recursive: true });
  mkdirSync(join(root, "docs", "changes", "example", "evidence"), { recursive: true });
  mkdirSync(join(root, "docs", "architecture"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  const artifact = "# Shared architecture\n";
  writeFileSync(join(root, "docs", "architecture", "shared.md"), artifact, "utf8");
  writeFileSync(join(root, "docs", "changes", "canonical", "change.yaml"), `change_id: canonical
title: Canonical
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  architecture:
    kind: architecture
    path: docs/architecture/shared.md
    role: primary
    lifecycle_state: approved
workflow_state:
  lifecycle_state: complete
  current_stage: complete
  next_stage: none
  blocker: null
lifecycle_cli:
  schema_version: 2
  artifacts:
    architecture:
      artifact_kind: architecture
      artifact_role: primary
      artifact_path: docs/architecture/shared.md
      artifact_sha256: ${sha(artifact)}
      stage_authority: architecture
  reviews: {}
  validations: {}
  resolutions: {}
  milestones: {}
  correction_history: {}
  withdrawals: {}
`, "utf8");
  writeFileSync(join(root, "docs", "changes", "example", "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states: {}
workflow_state:
  lifecycle_state: active
  current_stage: architecture
  next_stage: architecture-review
  blocker: null
lifecycle_cli:
  schema_version: 2
  artifacts: {}
  reviews: {}
  validations: {}
  resolutions: {}
  milestones: {}
  correction_history: {}
  withdrawals: {}
`, "utf8");
  const evidencePath = "docs/changes/example/evidence/architecture-authoring.md";
  writeFileSync(join(root, evidencePath), `Artifact path: docs/architecture/shared.md\nArtifact identity: sha256:${sha(artifact)}\nAuthoring result: complete\n`, "utf8");
  return { root, evidencePath };
}

function revision(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

function request(root, body) {
  const path = "requests/register.json";
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

test("new artifact registration rejects a path owned by another governed change", async () => {
  const { root, evidencePath } = await repository();
  const changePath = join(root, "docs", "changes", "example", "change.yaml");
  const before = readFileSync(changePath);
  const path = request(root, {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: revision(root),
    artifact_id: "architecture", artifact_kind: "architecture", artifact_role: "primary", artifact_path: "docs/architecture/shared.md",
    evidence_path: evidencePath, stage_authority: "architecture",
  });
  const execution = executeLifecycleCli(["record-artifact-revision", "--request", path, "--format", "json"], { cwd: root });
  assert.equal(execution.result.errors[0].code, "RL_ARTIFACT_PATH_OWNED");
  assert.deepEqual(readFileSync(changePath), before);
});

test("ownership discovery ignores legacy records without the governed lifecycle contract", async () => {
  const { root, evidencePath } = await repository();
  mkdirSync(join(root, "docs", "changes", "legacy"), { recursive: true });
  writeFileSync(join(root, "docs", "changes", "legacy", "change.yaml"), `change_id: legacy
validation:
  - command: bash -c "echo value: other"
    result: pass
`, "utf8");
  const path = request(root, {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: revision(root),
    artifact_id: "architecture", artifact_kind: "architecture", artifact_role: "primary", artifact_path: "docs/architecture/shared.md",
    evidence_path: evidencePath, stage_authority: "architecture",
  });

  const execution = executeLifecycleCli(["record-artifact-revision", "--request", path, "--format", "json"], { cwd: root });

  assert.equal(execution.result.errors[0].code, "RL_ARTIFACT_PATH_OWNED");
  assert.match(execution.result.errors[0].summary, /already owned/);
  assert.deepEqual(execution.result.errors[0].relevant_identities, ["docs/architecture/shared.md", "canonical"]);
});

test("ownership discovery fails closed on contradictory or unreadable governed records", async () => {
  const { root, evidencePath } = await repository();
  const canonicalPath = join(root, "docs", "changes", "canonical", "change.yaml");
  writeFileSync(canonicalPath, readFileSync(canonicalPath, "utf8").replace("artifact_role: primary", "artifact_role: supporting"), "utf8");
  const path = request(root, {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: revision(root),
    artifact_id: "architecture", artifact_kind: "architecture", artifact_role: "primary", artifact_path: "docs/architecture/shared.md",
    evidence_path: evidencePath, stage_authority: "architecture",
  });
  const contradictory = executeLifecycleCli(["record-artifact-revision", "--request", path, "--format", "json"], { cwd: root });
  assert.equal(contradictory.result.errors[0].code, "RL_ARTIFACT_PATH_OWNED");
  assert.match(contradictory.result.errors[0].summary, /contradictory/);

  writeFileSync(canonicalPath, "change_id: canonical\nchange_id: duplicate\nlifecycle_contract: stage-owned-change-local-v1\n", "utf8");
  const unreadable = executeLifecycleCli(["record-artifact-revision", "--request", path, "--format", "json"], { cwd: root });
  assert.equal(unreadable.result.errors[0].code, "RL_ARTIFACT_PATH_OWNED");
  assert.match(unreadable.result.errors[0].summary, /cannot be determined/);
});
