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

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-correction-route-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  const spec = "# Example spec\n\nVersion one.\n";
  writeFileSync(join(root, "specs", "example.md"), spec, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), "Review ID: code-review-r1\nMaterial findings: F-CODE\nOpen findings: F-CODE\n", "utf8");
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
workflow_state:
  lifecycle_state: active
  current_stage: verify
  next_stage: verify
  blocker: proof gap in the test specification
  evidence: []
  planned_work:
    current_milestone: M2
    remaining_implementation_milestones:
      - M2
    milestones:
      M2:
        kind: implementation
        state: implementing
lifecycle_cli:
  schema_version: 2
  artifacts:
    spec:
      artifact_kind: spec
      artifact_role: primary
      artifact_path: specs/example.md
      artifact_sha256: ${sha(spec)}
      stage_authority: spec
  reviews: {}
  validations: {}
  resolutions: {}
  milestones: {}
  correction_history: {}
  withdrawals: {}
`, "utf8");
  return { root, changeRoot };
}

function status(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
}

function request(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

function execute(root, operation, body) {
  const path = request(root, operation, body);
  return executeLifecycleCli([operation, "--request", path, "--format", "json"], { cwd: root });
}

test("workflow routes one exact upstream correction and returns after exact settlement", async () => {
  const { root, changeRoot } = await fixture();
  const initialRevision = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/correction-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: upstream-proof-gap
Finding IDs: F-CODE
Return stage: verify
Lifecycle revision: ${initialRevision}
`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1,
    operation: "route-correction",
    change_id: "example",
    expected_lifecycle_revision: initialRevision,
    source_stage: "verify",
    destination_stage: "spec",
    destination_artifact_id: "spec",
    reason: "upstream-proof-gap",
    evidence_path: routeEvidence,
    finding_ids: ["F-CODE"],
    return_stage: "verify",
    milestone_id: "M2",
    stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
  assert.match(routed.result.operation_result.route_id, /^route-[a-f0-9]{64}$/);
  assert.equal(routed.result.operation_result.source_snapshot.milestone_id, "M2");
  assert.equal(routed.result.operation_result.source_snapshot.blocker, "proof gap in the test specification");
  let change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(change.workflow_state.current_stage, "spec");
  assert.equal(change.workflow_state.blocker, null);
  assert.equal(change.workflow_state.planned_work.milestones.M2.state, "implementing");
  assert.equal(change.lifecycle_cli.active_correction.source_snapshot.blocker, "proof gap in the test specification");
  assert.equal(status(root).effective_state.active_correction.destination_artifact_id, "spec");
  assert.equal(status(root).effective_state.active_correction.milestone_id, "M2");
  assert.equal(status(root).effective_state.active_correction.milestone_state, "implementing");

  const currentRevision = status(root).lifecycle_revision;
  const replay = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: currentRevision,
    source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "upstream-proof-gap",
    evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "verify", milestone_id: "M2", stage_authority: "workflow",
  });
  assert.equal(replay.result.status, "already-recorded");

  const priorIdentity = change.lifecycle_cli.artifacts.spec.artifact_sha256;
  const revisedSpec = "# Example spec\n\nVersion two with corrected proof.\n";
  writeFileSync(join(root, "specs", "example.md"), revisedSpec, "utf8");
  const authoringEvidence = "docs/changes/example/evidence/spec-revision.md";
  writeFileSync(join(root, authoringEvidence), `Artifact path: specs/example.md\nArtifact identity: sha256:${sha(revisedSpec)}\nAuthoring result: complete\n`, "utf8");
  const revised = execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: authoringEvidence,
    prior_artifact_sha256: priorIdentity, stage_authority: "spec",
  });
  assert.equal(revised.exitCode, 0, JSON.stringify(revised.result));
  assert.equal(status(root).effective_state.current_stage, "spec-review");
  assert.deepEqual(status(root).permitted_operations, ["record-review"]);

  const reviewPath = "docs/changes/example/reviews/spec-review-r2.md";
  const reviewText = `Review ID: spec-review-r2
Stage: spec-review
Round: r2
Status: approved
Reviewed artifact path: specs/example.md
Reviewed artifact identity: sha256:${sha(revisedSpec)}
Material findings: none
`;
  writeFileSync(join(root, reviewPath), reviewText, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `${readFileSync(join(changeRoot, "review-log.md"), "utf8")}\n### Review entry\n\nReview ID: spec-review-r2\nMaterial findings: none\nOpen findings: none\n`, "utf8");
  const reviewed = execute(root, "record-review", {
    schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", evidence_path: reviewPath, stage_authority: "spec-review",
  });
  assert.equal(reviewed.exitCode, 0, JSON.stringify(reviewed.result));
  const settled = execute(root, "settle-artifact", {
    schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", stage_authority: "spec-review",
  });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.deepEqual(status(root).permitted_operations, ["return-correction"]);
  assert.deepEqual(status(root).effective_state.unresolved_findings, ["F-CODE"]);

  change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const route = change.lifecycle_cli.active_correction;
  const review = change.lifecycle_cli.reviews.spec;
  const returnRevision = status(root).lifecycle_revision;
  const returnEvidence = "docs/changes/example/evidence/correction-return.md";
  writeFileSync(join(root, returnEvidence), `Change ID: example
Route ID: ${route.route_id}
Lifecycle revision: ${returnRevision}
Destination artifact: spec
Artifact path: specs/example.md
Artifact identity: sha256:${sha(revisedSpec)}
Review ID: ${review.review_id}
Review round: ${review.round}
Review authority: ${review.stage_authority}
Review outcome: ${review.outcome}
Review evidence path: ${review.evidence_path}
Review evidence identity: sha256:${review.evidence_sha256}
`, "utf8");
  const returned = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
    route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });
  assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
  assert.equal(returned.result.operation_result.restored_stage, "verify");
  change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(change.workflow_state.current_stage, "verify");
  assert.equal(change.workflow_state.next_stage, "verify");
  assert.equal(change.workflow_state.blocker, "proof gap in the test specification");
  assert.equal(change.workflow_state.planned_work.current_milestone, "M2");
  assert.equal(change.workflow_state.planned_work.milestones.M2.state, "implementing");
  assert.equal(change.lifecycle_cli.active_correction, undefined);
  assert.equal(change.lifecycle_cli.correction_history[route.route_id].status, "returned");

  const returnReplay = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });
  assert.equal(returnReplay.result.status, "already-recorded", JSON.stringify(returnReplay.result));
});

test("workflow can route and register an already-authored stale upstream correction", async () => {
  const { root, changeRoot } = await fixture();
  const original = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const priorIdentity = original.lifecycle_cli.artifacts.spec.artifact_sha256;
  const revisedSpec = "# Example spec\n\nAlready-authored correction.\n";
  writeFileSync(join(root, "specs", "example.md"), revisedSpec, "utf8");

  const beforeRoute = status(root);
  assert.deepEqual(beforeRoute.effective_state.stale_evidence, ["spec"]);
  assert.equal(beforeRoute.permitted_operations.includes("route-correction"), true);
  const context = executeLifecycleCli(["context", "spec", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(context.result.errors.at(-1).code, "RL_WORKFLOW_ROUTE_REQUIRED");
  assert.equal(context.result.context.permitted_registration_operation, null);
  assert.equal(context.result.context.available_after_workflow_route, "record-artifact-revision");

  const beforeRejectedRoute = readFileSync(join(changeRoot, "change.yaml"));
  const emptyFindingEvidence = "docs/changes/example/evidence/stale-correction-without-finding.md";
  writeFileSync(join(root, emptyFindingEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: upstream-stale-input
Finding IDs: none
Return stage: verify
Lifecycle revision: ${beforeRoute.lifecycle_revision}
`, "utf8");
  const rejected = execute(root, "route-correction", {
    schema_version: 1,
    operation: "route-correction",
    change_id: "example",
    expected_lifecycle_revision: beforeRoute.lifecycle_revision,
    source_stage: "verify",
    destination_stage: "spec",
    destination_artifact_id: "spec",
    reason: "upstream-stale-input",
    evidence_path: emptyFindingEvidence,
    finding_ids: [],
    return_stage: "verify",
    milestone_id: "M2",
    stage_authority: "workflow",
  });
  assert.equal(rejected.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), beforeRejectedRoute);

  const routeEvidence = "docs/changes/example/evidence/stale-correction-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: upstream-stale-input
Finding IDs: F-CODE
Return stage: verify
Lifecycle revision: ${beforeRoute.lifecycle_revision}
`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1,
    operation: "route-correction",
    change_id: "example",
    expected_lifecycle_revision: beforeRoute.lifecycle_revision,
    source_stage: "verify",
    destination_stage: "spec",
    destination_artifact_id: "spec",
    reason: "upstream-stale-input",
    evidence_path: routeEvidence,
    finding_ids: ["F-CODE"],
    return_stage: "verify",
    milestone_id: "M2",
    stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
  let change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(change.lifecycle_cli.active_correction.prior_artifact_sha256, priorIdentity);

  const authoringEvidence = "docs/changes/example/evidence/stale-spec-revision.md";
  writeFileSync(join(root, authoringEvidence), `Artifact path: specs/example.md
Artifact identity: sha256:${sha(revisedSpec)}
Authoring result: complete
`, "utf8");
  const revised = execute(root, "record-artifact-revision", {
    schema_version: 1,
    operation: "record-artifact-revision",
    change_id: "example",
    expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec",
    artifact_kind: "spec",
    artifact_role: "primary",
    artifact_path: "specs/example.md",
    evidence_path: authoringEvidence,
    prior_artifact_sha256: priorIdentity,
    stage_authority: "spec",
  });
  assert.equal(revised.exitCode, 0, JSON.stringify(revised.result));
  change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(change.lifecycle_cli.artifacts.spec.artifact_sha256, sha(revisedSpec));
  assert.equal(change.artifact_states.spec.lifecycle_state, "review-required");
});

test("route rejects lateral, missing-milestone, conflicting, and stale requests without mutation", async () => {
  for (const scenario of ["lateral", "missing-milestone", "conflicting", "stale"]) {
    const { root, changeRoot } = await fixture();
    const initial = status(root).lifecycle_revision;
    const routeEvidence = "docs/changes/example/evidence/correction-route.md";
    const destinationStage = scenario === "lateral" ? "verify" : "spec";
    writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: upstream-proof-gap\nFinding IDs: F-CODE\nReturn stage: verify\nLifecycle revision: ${initial}\n`, "utf8");
    const body = {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: scenario === "stale" ? `sha256:${"0".repeat(64)}` : initial,
      source_stage: "verify", destination_stage: destinationStage, destination_artifact_id: "spec", reason: "upstream-proof-gap",
      evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "verify", ...(scenario === "missing-milestone" ? {} : { milestone_id: "M2" }), stage_authority: "workflow",
    };
    const before = readFileSync(join(changeRoot, "change.yaml"));
    const first = execute(root, "route-correction", body);
    if (scenario === "conflicting") {
      assert.equal(first.exitCode, 0, JSON.stringify(first.result));
      const routedBytes = readFileSync(join(changeRoot, "change.yaml"));
      const conflictEvidence = "docs/changes/example/evidence/conflicting-route.md";
      writeFileSync(join(root, conflictEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: upstream-contract-gap\nFinding IDs: F-CODE\nReturn stage: verify\nLifecycle revision: ${status(root).lifecycle_revision}\n`, "utf8");
      const conflict = execute(root, "route-correction", { ...body, expected_lifecycle_revision: status(root).lifecycle_revision, reason: "upstream-contract-gap", evidence_path: conflictEvidence });
      assert.equal(conflict.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
      assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), routedBytes);
      continue;
    }
    assert.equal(first.result.errors[0].code, scenario === "stale" ? "RL_STALE_OPERATION" : scenario === "lateral" ? "RL_INVALID_REQUEST" : "RL_CORRECTION_ROUTE_INVALID");
    assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
  }
});

test("route rejects unknown findings and non-destination revision without mutation", async () => {
  const { root, changeRoot } = await fixture();
  const before = readFileSync(join(changeRoot, "change.yaml"));
  const current = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/bad-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: upstream-proof-gap\nFinding IDs: NOT-OPEN\nReturn stage: verify\nLifecycle revision: ${current}\n`, "utf8");
  const rejected = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: current,
    source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "upstream-proof-gap",
    evidence_path: routeEvidence, finding_ids: ["NOT-OPEN"], return_stage: "verify", milestone_id: "M2", stage_authority: "workflow",
  });
  assert.equal(rejected.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});
