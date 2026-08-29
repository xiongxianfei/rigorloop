import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml, serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-plan-initialization-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "docs", "plans"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });

  const planPath = "docs/plans/example.md";
  const reviewPath = "docs/changes/example/reviews/plan-review-r1.md";
  const plan = `# Example plan

## Owning change record

\`docs/changes/example/change.yaml\`

## Milestones

### M1. Implement behavior

- Milestone kind: implementation

### M2. Close lifecycle

- Milestone kind: lifecycle-closeout
`;
  const planSha = createHash("sha256").update(plan).digest("hex");
  const authoringEvidence = `Artifact path: ${planPath}\nArtifact identity: sha256:${planSha}\nAuthoring result: complete\n`;
  const authoringEvidenceSha = createHash("sha256").update(authoringEvidence).digest("hex");
  writeFileSync(join(root, planPath), plan, "utf8");
  writeFileSync(join(changeRoot, "evidence", "plan.md"), authoringEvidence, "utf8");
  writeFileSync(join(root, reviewPath), `Review ID: plan-review-r1\nStage: plan-review\nRound: r1\nStatus: approved\nReviewed artifact path: ${planPath}\nReviewed artifact identity: sha256:${planSha}\nMaterial findings: none\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `Review ID: plan-review-r1\nStage: plan-review\nRound: r1\nRecord: ${reviewPath}\nStatus: approved\nMaterial findings: none\nOpen findings: none\nRecording status: recorded\n`, "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  plan:
    authoring_evidence: docs/changes/example/evidence/plan.md
    kind: plan
    lifecycle_state: review-required
    path: ${planPath}
    role: primary
workflow_state:
  blocker: null
  current_stage: plan-review
  evidence: []
  lifecycle_state: active
  next_stage: plan-review
workflow: {}
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  status: not-reviewed
  unresolved_items: 0
lifecycle_cli:
  schema_version: 2
  artifacts:
    plan:
      artifact_kind: plan
      artifact_path: ${planPath}
      artifact_role: primary
      artifact_sha256: ${planSha}
      authoring_evidence_path: docs/changes/example/evidence/plan.md
      authoring_evidence_sha256: ${authoringEvidenceSha}
      stage_authority: plan
  reviews: {}
  validations: {}
  resolutions: {}
  milestones: {}
  correction_history: {}
  withdrawals: {}
`, "utf8");
  return { root, changeRoot, planPath, reviewPath, planSha };
}

function revision(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

function request(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

test("initialize-approved-plan creates reviewed milestone state once before settlement", async () => {
  const { root, changeRoot, planPath, reviewPath, planSha } = await fixture();
  const reviewRequest = request(root, "review", {
    schema_version: 1,
    operation: "record-review",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "plan",
    evidence_path: reviewPath,
    stage_authority: "plan-review",
  });
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewRequest], { cwd: root }).exitCode, 0);
  assert.deepEqual(executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.permitted_operations, ["initialize-approved-plan"]);

  const initializeRequest = request(root, "initialize", {
    schema_version: 1,
    operation: "initialize-approved-plan",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "plan",
    stage_authority: "plan",
  });
  const initialized = executeLifecycleCli(["initialize-approved-plan", "--request", initializeRequest, "--format", "json"], { cwd: root });
  assert.equal(initialized.exitCode, 0, JSON.stringify(initialized.result));
  assert.equal(initialized.result.operation_result.next_operation, "settle-artifact");

  const change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.deepEqual(change.workflow_state.planned_work, {
    plan_artifact_id: "plan",
    current_milestone: "M1",
    milestones: {
      M1: { kind: "implementation", state: "planned" },
      M2: { kind: "lifecycle-closeout", state: "planned" },
    },
    remaining_implementation_milestones: ["M1"],
    latest_review: {
      artifact_id: "none",
      evidence: [],
      milestone_id: "none",
      occurrence: "none",
      round: "none",
      stage: "none",
      status: "not-started",
    },
    final_closeout: {
      readiness: "not-ready",
      reasons: ["implementation-milestones-open"],
      evidence: [],
    },
    initialization_basis: {
      review_id: "plan-review-r1",
      review_round: "r1",
      review_record: reviewPath,
      reviewed_artifact_path: planPath,
      reviewed_revision: planSha,
    },
  });
  assert.deepEqual(initialized.result.permitted_operations, ["settle-artifact"]);

  const retryRequest = request(root, "initialize-retry", {
    schema_version: 1,
    operation: "initialize-approved-plan",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "plan",
    stage_authority: "plan",
  });
  const retry = executeLifecycleCli(["initialize-approved-plan", "--request", retryRequest, "--format", "json"], { cwd: root });
  assert.equal(retry.exitCode, 0, JSON.stringify(retry.result));
  assert.equal(retry.result.status, "already-recorded");

  const conflicting = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  conflicting.workflow_state.planned_work.milestones.M1.state = "implementing";
  writeFileSync(join(changeRoot, "change.yaml"), serializeLifecycleYaml(conflicting), "utf8");
  const conflictRequest = request(root, "initialize-conflict", {
    schema_version: 1,
    operation: "initialize-approved-plan",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "plan",
    stage_authority: "plan",
  });
  const conflict = executeLifecycleCli(["initialize-approved-plan", "--request", conflictRequest, "--format", "json"], { cwd: root });
  assert.equal(conflict.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
});

test("initialize-approved-plan rejects an unreviewed plan", async () => {
  const { root, changeRoot } = await fixture();
  const unreviewedRequest = request(root, "unreviewed", {
    schema_version: 1,
    operation: "initialize-approved-plan",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "plan",
    stage_authority: "plan",
  });
  const unreviewed = executeLifecycleCli(["initialize-approved-plan", "--request", unreviewedRequest, "--format", "json"], { cwd: root });
  assert.equal(unreviewed.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");

  const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before);
});
