import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml } from "../dist/lib/lifecycle-contract.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-stage-advance-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  writeFileSync(join(root, "specs", "example.md"), "# Approved spec\n", "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  spec:
    kind: spec
    path: specs/example.md
    role: primary
    lifecycle_state: approved
    review:
      artifact_id: spec
      id: spec-review-r1
      outcome: approved
      record: docs/changes/example/reviews/spec-review-r1.md
      round: r1
workflow_state:
  lifecycle_state: active
  current_stage: spec-review
  next_stage: spec-review
  blocker: null
  evidence: []
workflow: {}
`, "utf8");
  return { root, changeRoot };
}

function revision(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

function request(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

test("advance-stage moves a completed review to the next allowed stage", async () => {
  const { root, changeRoot } = await fixture();
  const before = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
  assert.equal(before.effective_state.current_stage, "spec-review");
  assert.equal(before.permitted_operations.includes("advance-stage"), true);

  const advance = request(root, "advance-to-architecture", {
    schema_version: 1,
    operation: "advance-stage",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    source_stage: "spec-review",
    destination_stage: "architecture",
    stage_authority: "workflow",
  });
  const execution = executeLifecycleCli(["advance-stage", "--request", advance, "--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.equal(execution.result.effective_state.current_stage, "architecture");
  const recorded = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(recorded.workflow_state.current_stage, "architecture");
  assert.equal(recorded.workflow_state.next_stage, "architecture");
});

test("advance-stage rejects a skipped stage without changing lifecycle bytes", async () => {
  const { root, changeRoot } = await fixture();
  const before = readFileSync(join(changeRoot, "change.yaml"));
  const advance = request(root, "skip-architecture", {
    schema_version: 1,
    operation: "advance-stage",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    source_stage: "spec-review",
    destination_stage: "architecture-review",
    stage_authority: "workflow",
  });
  const execution = executeLifecycleCli(["advance-stage", "--request", advance, "--format", "json"], { cwd: root });

  assert.equal(execution.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});

test("advance-stage rejects an incomplete current stage without changing lifecycle bytes", async () => {
  const { root, changeRoot } = await fixture();
  const changePath = join(changeRoot, "change.yaml");
  const incomplete = readFileSync(changePath, "utf8")
    .replace("lifecycle_state: approved", "lifecycle_state: review-required")
    .replace(/    review:\n(?:      .+\n)+/, "");
  writeFileSync(changePath, incomplete, "utf8");
  const before = readFileSync(changePath);
  const status = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
  assert.equal(status.permitted_operations.includes("advance-stage"), false);
  const advance = request(root, "advance-incomplete", {
    schema_version: 1,
    operation: "advance-stage",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    source_stage: "spec-review",
    destination_stage: "architecture",
    stage_authority: "workflow",
  });
  const execution = executeLifecycleCli(["advance-stage", "--request", advance, "--format", "json"], { cwd: root });

  assert.equal(execution.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.deepEqual(readFileSync(changePath), before);
});
