import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";
import { createHash } from "node:crypto";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-artifact-revision-"));
  mkdirSync(join(root, "docs", "changes", "example", "evidence"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  writeFileSync(join(root, "docs", "changes", "example", "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states: {}
workflow_state:
  lifecycle_state: active
  current_stage: spec
  next_stage: spec-review
  blocker: null
  evidence: []
`, "utf8");
  return root;
}

function revision(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

function request(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

function evidence(root, name, artifactPath, content) {
  const digest = createHash("sha256").update(content).digest("hex");
  const path = `docs/changes/example/evidence/${name}.md`;
  writeFileSync(join(root, path), `Artifact path: ${artifactPath}\nArtifact identity: sha256:${digest}\nAuthoring result: complete\n`, "utf8");
  return path;
}

test("record-artifact-revision creates and revises only its exact artifact entry", async () => {
  const root = await fixture();
  writeFileSync(join(root, "specs", "example.md"), "# Version one\n", "utf8");
  const firstEvidence = evidence(root, "spec-authoring", "specs/example.md", "# Version one\n");
  const create = request(root, "create", {
    schema_version: 1,
    operation: "record-artifact-revision",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    artifact_kind: "spec",
    artifact_role: "primary",
    artifact_path: "specs/example.md",
    evidence_path: firstEvidence,
    stage_authority: "spec",
  });
  const created = executeLifecycleCli(["record-artifact-revision", "--request", create, "--format", "json"], { cwd: root });
  assert.equal(created.exitCode, 0, JSON.stringify(created.result));
  const afterCreate = readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8");
  assert.match(afterCreate, /lifecycle_state: review-required/);
  assert.match(afterCreate, /artifact_sha256:/);
  assert.match(afterCreate, /next_stage: spec-review/);

  const beforeContext = executeLifecycleCli(["context", "spec", "--change", "example", "--format", "json"], { cwd: root }).result;
  const prior = beforeContext.context.target_artifact.sha256;
  writeFileSync(join(root, "specs", "example.md"), "# Version two\n", "utf8");
  const revisionEvidence = evidence(root, "spec-revision", "specs/example.md", "# Version two\n");
  const revise = request(root, "revise", {
    schema_version: 1,
    operation: "record-artifact-revision",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    artifact_kind: "spec",
    artifact_role: "primary",
    artifact_path: "specs/example.md",
    evidence_path: revisionEvidence,
    prior_artifact_sha256: prior,
    stage_authority: "spec",
  });
  const revised = executeLifecycleCli(["record-artifact-revision", "--request", revise, "--format", "json"], { cwd: root });
  assert.equal(revised.exitCode, 0, JSON.stringify(revised.result));
  assert.notEqual(revised.result.lifecycle_revision, created.result.lifecycle_revision);
  assert.match(readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8"), /spec-revision\.md/);
});

test("record-artifact-revision rejects wrong authority, stale prior identity, and route mutation", async () => {
  const root = await fixture();
  writeFileSync(join(root, "specs", "example.md"), "# Spec\n", "utf8");
  const badEvidence = evidence(root, "spec", "specs/example.md", "# Spec\n");
  const before = readFileSync(join(root, "docs", "changes", "example", "change.yaml"));
  const bad = request(root, "bad", {
    schema_version: 1,
    operation: "record-artifact-revision",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    artifact_kind: "spec",
    artifact_role: "primary",
    artifact_path: "specs/example.md",
    evidence_path: badEvidence,
    stage_authority: "plan",
  });
  const result = executeLifecycleCli(["record-artifact-revision", "--request", bad, "--format", "json"], { cwd: root });
  assert.equal(result.result.errors[0].code, "RL_AUTHORITY_BOUNDARY");
  assert.deepEqual(readFileSync(join(root, "docs", "changes", "example", "change.yaml")), before);

  writeFileSync(join(root, "docs", "changes", "example", "evidence", "wrong.md"), `Artifact path: specs/example.md\nArtifact identity: sha256:${"0".repeat(64)}\nAuthoring result: complete\n`, "utf8");
  const wrongEvidence = request(root, "wrong-evidence", {
    schema_version: 1,
    operation: "record-artifact-revision",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    artifact_kind: "spec",
    artifact_role: "primary",
    artifact_path: "specs/example.md",
    evidence_path: "docs/changes/example/evidence/wrong.md",
    stage_authority: "spec",
  });
  const stale = executeLifecycleCli(["record-artifact-revision", "--request", wrongEvidence, "--format", "json"], { cwd: root });
  assert.equal(stale.result.errors[0].code, "RL_STALE_EVIDENCE");
  assert.deepEqual(readFileSync(join(root, "docs", "changes", "example", "change.yaml")), before);
});
