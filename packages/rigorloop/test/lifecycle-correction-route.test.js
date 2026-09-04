import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { evaluateLifecycleOperation } from "../dist/lib/lifecycle-operations.js";
import { packageContext, packageRepository, setWorkflowStage, writeActiveV3Manifests, writePackageReview } from "./helpers/lifecycle-package-fixture.js";

const sha = (value) => createHash("sha256").update(value).digest("hex");

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-correction-route-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  writeActiveV3Manifests(root);
  const spec = "# Example spec\n\nVersion one.\n";
  writeFileSync(join(root, "specs", "example.md"), spec, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), "Review ID: code-review-r1\nMaterial findings: F-CODE\nOpen findings: F-CODE\n", "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v3
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

function activateContract(root, changeRoot, contract) {
  const active = { schema_version: 1, state: "active", activating_source_revision: "a".repeat(40), changes: [] };
  const preactivation = { schema_version: 1, state: "preactivation", activating_source_revision: null, changes: [] };
  writeFileSync(join(root, "specs/lifecycle-contract-activation.yaml"), `${JSON.stringify(contract === "stage-owned-change-local-v1" ? preactivation : active, null, 2)}\n`, "utf8");
  writeFileSync(join(root, "specs/final-verification-contract-activation.yaml"), `${JSON.stringify(contract === "stage-owned-change-local-v3" ? active : preactivation, null, 2)}\n`, "utf8");
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.lifecycle_contract = contract;
  if (contract === "stage-owned-change-local-v3") {
    change.workflow_state.planned_work.current_milestone = "none";
    change.workflow_state.planned_work.remaining_implementation_milestones = [];
    change.workflow_state.planned_work.milestones.M2.state = "closed";
  }
  writeFileSync(changePath, `${JSON.stringify(change, null, 2)}\n`, "utf8");
}

function addV3CorrectionArtifacts(root, changeRoot) {
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  for (const [id, kind, path] of [
    ["architecture", "architecture", "docs/architecture/example.md"],
    ["plan", "plan", "docs/plans/example.md"],
  ]) {
    mkdirSync(join(root, ...path.split("/").slice(0, -1)), { recursive: true });
    const content = `# ${kind}\n`;
    writeFileSync(join(root, path), content, "utf8");
    change.artifact_states[id] = { kind, path, role: "primary", lifecycle_state: kind === "plan" ? "active" : "approved" };
    change.lifecycle_cli.artifacts[id] = { artifact_kind: kind, artifact_role: "primary", artifact_path: path, artifact_sha256: sha(content), stage_authority: kind };
  }
  writeFileSync(changePath, `${JSON.stringify(change, null, 2)}\n`, "utf8");
}

test("package finding routes each required owner before package rereview", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "design-review" });
  const review = writePackageReview(root, packageContext(root), {
    outcome: "changes-requested",
    findings: [{ id: "PKG-CROSS", scope: "cross-artifact", affected: ["architecture", "spec"], owners: ["architecture", "spec"] }],
    correctionTargets: ["architecture", "spec"],
  });
  const recorded = execute(root, "record-package-review", {
    schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: review.reviewId, upstream_review_id: review.packageFacts.upstream_review_id,
    members: review.packageFacts.members, evidence_path: review.reviewPath, stage_authority: "design-review",
  });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));
  const settled = execute(root, "settle-review-package", {
    schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: review.reviewId, stage_authority: "design-review",
  });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.deepEqual(status(root).permitted_operations, ["route-correction"]);

  const routeRevision = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/package-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: design-review\nDestination artifact: architecture\nReason: upstream-contract-gap\nFinding IDs: PKG-CROSS\nReturn stage: design-review\nLifecycle revision: ${routeRevision}\n`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: routeRevision,
    source_stage: "design-review", destination_stage: "architecture", destination_artifact_id: "architecture",
    reason: "upstream-contract-gap", evidence_path: routeEvidence, finding_ids: ["PKG-CROSS"], return_stage: "design-review", stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));

  let change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const prior = change.lifecycle_cli.artifacts.architecture.artifact_sha256;
  const revisedArchitecture = "# Architecture\n\nReconciled boundary.\n";
  writeFileSync(join(root, "docs/architecture/example.md"), revisedArchitecture, "utf8");
  const authoringEvidence = "docs/changes/example/evidence/architecture-revision.md";
  writeFileSync(join(root, authoringEvidence), `Artifact path: docs/architecture/example.md\nArtifact identity: sha256:${sha(revisedArchitecture)}\nAuthoring result: complete\n`, "utf8");
  const revised = execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "architecture", artifact_kind: "architecture", artifact_role: "primary", artifact_path: "docs/architecture/example.md",
    evidence_path: authoringEvidence, prior_artifact_sha256: prior, stage_authority: "architecture",
  });
  assert.equal(revised.exitCode, 0, JSON.stringify(revised.result));
  assert.deepEqual(status(root).permitted_operations, ["return-correction"]);

  change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const route = change.lifecycle_cli.active_correction;
  const registration = change.lifecycle_cli.artifacts.architecture;
  const returnRevision = status(root).lifecycle_revision;
  const returnEvidence = "docs/changes/example/evidence/package-return.md";
  writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${route.route_id}\nLifecycle revision: ${returnRevision}\nDestination artifact: architecture\nArtifact path: docs/architecture/example.md\nArtifact identity: sha256:${registration.artifact_sha256}\nAuthoring evidence path: ${registration.authoring_evidence_path}\nAuthoring evidence identity: sha256:${registration.authoring_evidence_sha256}\n`, "utf8");
  const returned = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
    route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });
  assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
  assert.equal(status(root).effective_state.current_stage, "design-review");
  assert.equal(status(root).effective_state.review_packages.design.status, "review-required");
  assert.deepEqual(status(root).permitted_operations, ["route-correction"]);

  const repeatRevision = status(root).lifecycle_revision;
  const repeatEvidence = "docs/changes/example/evidence/package-route-repeat.md";
  writeFileSync(join(root, repeatEvidence), `Change ID: example\nSource stage: design-review\nDestination artifact: architecture\nReason: upstream-contract-gap\nFinding IDs: PKG-CROSS\nReturn stage: design-review\nLifecycle revision: ${repeatRevision}\n`, "utf8");
  const repeated = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: repeatRevision,
    source_stage: "design-review", destination_stage: "architecture", destination_artifact_id: "architecture",
    reason: "upstream-contract-gap", evidence_path: repeatEvidence, finding_ids: ["PKG-CROSS"], return_stage: "design-review", stage_authority: "workflow",
  });
  assert.equal(repeated.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
});

test("delivery upstream-direction and blocked findings route through the design package owner", async () => {
  for (const outcome of ["changes-requested", "blocked"]) {
    const { root, changeRoot } = await packageRepository({ stage: "design-review" });
    const design = writePackageReview(root, packageContext(root), { outcome: "approved" });
    assert.equal(execute(root, "record-package-review", {
      schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "design", review_id: design.reviewId, upstream_review_id: design.packageFacts.upstream_review_id,
      members: design.packageFacts.members, evidence_path: design.reviewPath, stage_authority: "design-review",
    }).exitCode, 0);
    assert.equal(execute(root, "settle-review-package", {
      schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "design", review_id: design.reviewId, stage_authority: "design-review",
    }).exitCode, 0);
    setWorkflowStage(root, "delivery-review");

    const delivery = writePackageReview(root, packageContext(root, "delivery-review"), {
      kind: "delivery", outcome,
      findings: [{ id: `PKG-UPSTREAM-${outcome}`, scope: "upstream-direction", affected: ["design"], owners: ["design-review"] }],
      correctionTargets: ["design"],
    });
    assert.equal(execute(root, "record-package-review", {
      schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "delivery", review_id: delivery.reviewId, upstream_review_id: delivery.packageFacts.upstream_review_id,
      members: delivery.packageFacts.members, evidence_path: delivery.reviewPath, stage_authority: "delivery-review",
    }).exitCode, 0);
    assert.equal(execute(root, "settle-review-package", {
      schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "delivery", review_id: delivery.reviewId, stage_authority: "delivery-review",
    }).exitCode, 0);
    assert.deepEqual(status(root).permitted_operations, ["route-correction"]);

    const priorBytes = readFileSync(join(changeRoot, "change.yaml"), "utf8");
    const rejectedRevision = status(root).lifecycle_revision;
    const rejectedEvidence = "docs/changes/example/evidence/package-route-wrong-stage.md";
    writeFileSync(join(root, rejectedEvidence), `Change ID: example\nSource stage: delivery-review\nDestination artifact: design\nReason: upstream-contract-gap\nFinding IDs: PKG-UPSTREAM-${outcome}\nReturn stage: delivery-review\nLifecycle revision: ${rejectedRevision}\n`, "utf8");
    const rejected = execute(root, "route-correction", {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: rejectedRevision,
      source_stage: "delivery-review", destination_stage: "spec", destination_artifact_id: "design",
      reason: "upstream-contract-gap", evidence_path: rejectedEvidence, finding_ids: [`PKG-UPSTREAM-${outcome}`], return_stage: "delivery-review", stage_authority: "workflow",
    });
    assert.notEqual(rejected.exitCode, 0);
    assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), priorBytes);

    const routeRevision = status(root).lifecycle_revision;
    const routeEvidence = "docs/changes/example/evidence/package-route-design.md";
    writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: delivery-review\nDestination artifact: design\nReason: upstream-contract-gap\nFinding IDs: PKG-UPSTREAM-${outcome}\nReturn stage: delivery-review\nLifecycle revision: ${routeRevision}\n`, "utf8");
    const routed = execute(root, "route-correction", {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: routeRevision,
      source_stage: "delivery-review", destination_stage: "design-review", destination_artifact_id: "design",
      reason: "upstream-contract-gap", evidence_path: routeEvidence, finding_ids: [`PKG-UPSTREAM-${outcome}`], return_stage: "delivery-review", stage_authority: "workflow",
    });
    assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
    assert.deepEqual(status(root).permitted_operations, ["record-package-review"]);

    const revisedDesign = writePackageReview(root, packageContext(root), { outcome: "approved", round: "r2" });
    const recordedDesign = execute(root, "record-package-review", {
      schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "design", review_id: revisedDesign.reviewId, upstream_review_id: revisedDesign.packageFacts.upstream_review_id,
      members: revisedDesign.packageFacts.members, evidence_path: revisedDesign.reviewPath, stage_authority: "design-review",
    });
    assert.equal(recordedDesign.exitCode, 0, JSON.stringify(recordedDesign.result));
    assert.equal(execute(root, "settle-review-package", {
      schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      package_kind: "design", review_id: revisedDesign.reviewId, stage_authority: "design-review",
    }).exitCode, 0);
    assert.deepEqual(status(root).permitted_operations, ["return-correction"]);

    const change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
    const route = change.lifecycle_cli.active_correction;
    const returnRevision = status(root).lifecycle_revision;
    const returnEvidence = "docs/changes/example/evidence/package-return-design.md";
    writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${route.route_id}\nLifecycle revision: ${returnRevision}\nDestination package: design\nReview ID: ${revisedDesign.reviewId}\nReview evidence path: ${revisedDesign.reviewPath}\n`, "utf8");
    const returned = execute(root, "return-correction", {
      schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
      route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
    });
    assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
    assert.equal(status(root).effective_state.current_stage, "delivery-review");
    assert.equal(status(root).effective_state.review_packages.delivery.status, "review-required");
  }
});

test("delivery verification findings route to plan and cannot route to retired test-spec", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "design-review" });
  const design = writePackageReview(root, packageContext(root), { outcome: "approved" });
  assert.equal(execute(root, "record-package-review", {
    schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: design.reviewId, upstream_review_id: design.packageFacts.upstream_review_id,
    members: design.packageFacts.members, evidence_path: design.reviewPath, stage_authority: "design-review",
  }).exitCode, 0);
  assert.equal(execute(root, "settle-review-package", {
    schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: design.reviewId, stage_authority: "design-review",
  }).exitCode, 0);
  setWorkflowStage(root, "delivery-review");
  const delivery = writePackageReview(root, packageContext(root, "delivery-review"), {
    kind: "delivery", outcome: "changes-requested",
    findings: [{ id: "V2-PLAN-GAP", scope: "artifact-local", affected: ["plan"], owners: ["plan"] }],
    correctionTargets: ["plan"],
  });
  assert.equal(execute(root, "record-package-review", {
    schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "delivery", review_id: delivery.reviewId, upstream_review_id: delivery.packageFacts.upstream_review_id,
    members: delivery.packageFacts.members, evidence_path: delivery.reviewPath, stage_authority: "delivery-review",
  }).exitCode, 0);
  assert.equal(execute(root, "settle-review-package", {
    schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "delivery", review_id: delivery.reviewId, stage_authority: "delivery-review",
  }).exitCode, 0);

  const revision = status(root).lifecycle_revision;
  const evidence = "docs/changes/example/evidence/v2-plan-route.md";
  writeFileSync(join(root, evidence), `Change ID: example\nSource stage: delivery-review\nDestination artifact: plan\nReason: upstream-planning-gap\nFinding IDs: V2-PLAN-GAP\nReturn stage: delivery-review\nLifecycle revision: ${revision}\n`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: revision,
    source_stage: "delivery-review", destination_stage: "plan", destination_artifact_id: "plan",
    reason: "upstream-planning-gap", evidence_path: evidence, finding_ids: ["V2-PLAN-GAP"], return_stage: "delivery-review", stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
  assert.equal(status(root).effective_state.current_stage, "plan");

  const path = join(changeRoot, "change.yaml");
  const before = readFileSync(path, "utf8");
  const rejected = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    source_stage: "delivery-review", destination_stage: "test-spec", destination_artifact_id: "test-spec",
    reason: "upstream-proof-gap", evidence_path: evidence, finding_ids: ["V2-PLAN-GAP"], return_stage: "delivery-review", stage_authority: "workflow",
  });
  assert.notEqual(rejected.exitCode, 0);
  assert.equal(readFileSync(path, "utf8"), before);
});

test.skip("historical individual-review correction flow", async () => {
  const { root, changeRoot } = await fixture();
  const initialRevision = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/correction-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: upstream-proof-gap
Finding IDs: F-CODE
Return stage: design-review
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
    return_stage: "design-review",
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

test.skip("historical changes-requested artifact-review correction flow", async () => {
  const { root, changeRoot } = await fixture();
  const initialRevision = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/correction-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: upstream-proof-gap
Finding IDs: F-CODE
Return stage: design-review
Lifecycle revision: ${initialRevision}
`, "utf8");
  assert.equal(execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: initialRevision,
    source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "upstream-proof-gap",
    evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "verify", milestone_id: "M2", stage_authority: "workflow",
  }).exitCode, 0);

  let change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const firstRevision = "# Example spec\n\nVersion two.\n";
  writeFileSync(join(root, "specs", "example.md"), firstRevision, "utf8");
  const firstEvidence = "docs/changes/example/evidence/spec-revision-1.md";
  writeFileSync(join(root, firstEvidence), `Artifact path: specs/example.md\nArtifact identity: sha256:${sha(firstRevision)}\nAuthoring result: complete\n`, "utf8");
  assert.equal(execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: firstEvidence,
    prior_artifact_sha256: change.lifecycle_cli.artifacts.spec.artifact_sha256, stage_authority: "spec",
  }).exitCode, 0);

  const reviewPath = "docs/changes/example/reviews/spec-review-r2.md";
  writeFileSync(join(root, reviewPath), `Review ID: spec-review-r2
Stage: spec-review
Round: r2
Status: changes-requested
Reviewed artifact path: specs/example.md
Reviewed artifact identity: sha256:${sha(firstRevision)}
Material findings: F-SPEC
`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `${readFileSync(join(changeRoot, "review-log.md"), "utf8")}\nReview ID: spec-review-r2\nMaterial findings: F-SPEC\nOpen findings: F-SPEC\n`, "utf8");
  assert.equal(execute(root, "record-review", {
    schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", evidence_path: reviewPath, stage_authority: "spec-review",
  }).exitCode, 0);
  assert.equal(execute(root, "settle-artifact", {
    schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", stage_authority: "spec-review",
  }).exitCode, 0);

  change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const secondRevision = "# Example spec\n\nVersion three resolves review.\n";
  writeFileSync(join(root, "specs", "example.md"), secondRevision, "utf8");
  const secondEvidence = "docs/changes/example/evidence/spec-revision-2.md";
  writeFileSync(join(root, secondEvidence), `Artifact path: specs/example.md\nArtifact identity: sha256:${sha(secondRevision)}\nAuthoring result: complete\n`, "utf8");
  const revised = execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: secondEvidence,
    prior_artifact_sha256: change.lifecycle_cli.artifacts.spec.artifact_sha256, stage_authority: "spec",
  });
  assert.equal(revised.exitCode, 0, JSON.stringify(revised.result));
  assert.equal(status(root).effective_state.current_stage, "spec-review");
  assert.deepEqual(status(root).permitted_operations, ["record-review"]);
});

test("settled Proposal correction can return after its exact approved review", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "design-review" });
  const changePath = join(changeRoot, "change.yaml");
  const proposalPath = "docs/proposals/example.md";
  const originalProposal = readFileSync(join(root, proposalPath), "utf8");

  const designReview = writePackageReview(root, packageContext(root), { outcome: "approved" });
  assert.equal(execute(root, "record-package-review", {
    schema_version: 1, operation: "record-package-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: designReview.reviewId, upstream_review_id: designReview.packageFacts.upstream_review_id,
    members: designReview.packageFacts.members, evidence_path: designReview.reviewPath, stage_authority: "design-review",
  }).exitCode, 0);
  assert.equal(execute(root, "settle-review-package", {
    schema_version: 1, operation: "settle-review-package", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    package_kind: "design", review_id: designReview.reviewId, stage_authority: "design-review",
  }).exitCode, 0);

  let change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow_state = {
    lifecycle_state: "active", current_stage: "implement", next_stage: "code-review", blocker: null, evidence: [],
    planned_work: {
      current_milestone: "M2", remaining_implementation_milestones: ["M2"],
      milestones: { M2: { kind: "implementation", state: "implementing" } },
    },
  };
  writeFileSync(changePath, `${JSON.stringify(change, null, 2)}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `${readFileSync(join(changeRoot, "review-log.md"), "utf8")}\nReview ID: code-review-r1\nMaterial findings: F-CODE\nOpen findings: F-CODE\n`, "utf8");

  const routeRevision = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/proposal-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: implement\nDestination artifact: proposal\nReason: upstream-contract-gap\nFinding IDs: F-CODE\nReturn stage: implement\nLifecycle revision: ${routeRevision}\n`, "utf8");
  assert.equal(execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: routeRevision,
    source_stage: "implement", destination_stage: "proposal", destination_artifact_id: "proposal", reason: "upstream-contract-gap",
    evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "implement", milestone_id: "M2", stage_authority: "workflow",
  }).exitCode, 0);

  const revisedProposal = "# Proposal\n\nCorrected direction.\n";
  writeFileSync(join(root, proposalPath), revisedProposal, "utf8");
  const authoringEvidence = "docs/changes/example/evidence/proposal-revision.md";
  writeFileSync(join(root, authoringEvidence), `Artifact path: ${proposalPath}\nArtifact identity: sha256:${sha(revisedProposal)}\nAuthoring result: complete\n`, "utf8");
  assert.equal(execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "proposal", artifact_kind: "proposal", artifact_role: "primary", artifact_path: proposalPath,
    evidence_path: authoringEvidence, prior_artifact_sha256: sha(originalProposal), stage_authority: "proposal",
  }).exitCode, 0);

  const reviewPath = "docs/changes/example/reviews/proposal-review-r2.md";
  const review = `Review ID: proposal-review-r2\nStage: proposal-review\nRound: r2\nStatus: approved\nReviewed artifact path: ${proposalPath}\nReviewed artifact identity: sha256:${sha(revisedProposal)}\nMaterial findings: none\n`;
  writeFileSync(join(root, reviewPath), review, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `${readFileSync(join(changeRoot, "review-log.md"), "utf8")}\n### Review entry\n\nReview ID: proposal-review-r2\nMaterial findings: none\nOpen findings: none\n`, "utf8");
  assert.equal(execute(root, "record-review", {
    schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "proposal", evidence_path: reviewPath, stage_authority: "proposal-review",
  }).exitCode, 0);
  assert.equal(execute(root, "settle-artifact", {
    schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "proposal", stage_authority: "proposal-review",
  }).exitCode, 0);
  assert.equal(parseLifecycleYaml(readFileSync(changePath, "utf8")).review_packages.design.status, "review-required");

  change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  const activeRoute = change.lifecycle_cli.active_correction;
  const registration = change.lifecycle_cli.artifacts.proposal;
  const returnRevision = status(root).lifecycle_revision;
  const returnEvidence = "docs/changes/example/evidence/proposal-return.md";
  writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${activeRoute.route_id}\nLifecycle revision: ${returnRevision}\nDestination artifact: proposal\nArtifact path: ${proposalPath}\nArtifact identity: sha256:${sha(revisedProposal)}\nAuthoring evidence path: ${registration.authoring_evidence_path}\nAuthoring evidence identity: sha256:${registration.authoring_evidence_sha256}\n`, "utf8");
  const returned = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
    route_id: activeRoute.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });

  assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
  assert.equal(returned.result.operation_result.restored_stage, "design-review");
  assert.equal(parseLifecycleYaml(readFileSync(changePath, "utf8")).lifecycle_cli.active_correction, undefined);

  writeFileSync(join(root, "specs/example.md"), "# Specification\n\nUnregistered Design refinement.\n", "utf8");
  const rerouteStatus = status(root);
  const rerouteRevision = rerouteStatus.lifecycle_revision;
  assert.equal(rerouteStatus.permitted_operations.includes("route-correction"), true, JSON.stringify(rerouteStatus));
  const rerouteEvidence = "docs/changes/example/evidence/proposal-reroute.md";
  writeFileSync(join(root, rerouteEvidence), `Change ID: example\nSource stage: design-review\nDestination artifact: proposal\nReason: upstream-contract-gap\nFinding IDs: F-CODE\nReturn stage: design-review\nLifecycle revision: ${rerouteRevision}\n`, "utf8");
  const rerouted = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: rerouteRevision,
    source_stage: "design-review", destination_stage: "proposal", destination_artifact_id: "proposal", reason: "upstream-contract-gap",
    evidence_path: rerouteEvidence, finding_ids: ["F-CODE"], return_stage: "design-review", milestone_id: "M2", stage_authority: "workflow",
  });
  assert.equal(rerouted.exitCode, 0, JSON.stringify(rerouted.result));
  assert.equal(status(root).effective_state.current_stage, "proposal");
});

test("workflow can route and register an already-authored upstream correction", async () => {
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
Reason: system-requirement-gap
Finding IDs: none
Return stage: design-review
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
    reason: "system-requirement-gap",
    evidence_path: emptyFindingEvidence,
    finding_ids: [],
    return_stage: "design-review",
    milestone_id: "M2",
    stage_authority: "workflow",
  });
  assert.equal(rejected.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), beforeRejectedRoute);

  const routeEvidence = "docs/changes/example/evidence/stale-correction-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example
Source stage: verify
Destination artifact: spec
Reason: system-requirement-gap
Finding IDs: F-CODE
Return stage: design-review
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
    reason: "system-requirement-gap",
    evidence_path: routeEvidence,
    finding_ids: ["F-CODE"],
    return_stage: "design-review",
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

test("implementation can route a finding to a current approved design-package member", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "implement" });
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow_state.planned_work = {
    plan_artifact_id: "plan",
    current_milestone: "M1",
    remaining_implementation_milestones: ["M1"],
    milestones: { M1: { kind: "implementation", state: "implementing" } },
    latest_review: {},
    final_closeout: { readiness: "not-ready", reasons: ["implementation-milestones-open"], evidence: [] },
    initialization_basis: { review_id: "delivery-review-r1", review_round: "r1", review_record: "docs/changes/example/reviews/delivery-review-r1.md", reviewed_artifact_path: "docs/plans/example.md" },
  };
  change.review_packages = {
    design: { package_kind: "design", review_id: "design-review-r1", upstream_review_id: "proposal-review-r1", members: { architecture: "docs/architecture/example.md", spec: "specs/example.md", "adr-cache": "docs/adr/ADR-cache.md" }, findings: [], correction_targets: [], outcome: "approved", status: "approved", authority: "granted", review_round: "r1" },
  };
  const designReviewPath = "docs/changes/example/reviews/design-review-r1.md";
  const designReview = "Review ID: design-review-r1\nStage: design-review\nRound: r1\nReviewer authority: design-review\nPackage kind: design\nPackage members: architecture=docs/architecture/example.md, spec=specs/example.md, adr-cache=docs/adr/ADR-cache.md\nUpstream review ID: proposal-review-r1\nStatus: approved\nMaterial findings: none\nCorrection targets: none\nRecording status: recorded\n";
  const reviewLog = "Review ID: design-review-r1\nStage: design-review\nStatus: approved\nMaterial findings: none\nOpen findings: none\nRecording status: recorded\n\nReview ID: code-review-m1-r1\nMaterial findings: F-SPEC\nOpen findings: F-SPEC\n";
  writeFileSync(join(root, designReviewPath), designReview, "utf8");
  change.lifecycle_cli.package_reviews.design = { package_kind: "design", review_id: "design-review-r1", upstream_review_id: "proposal-review-r1", members: { architecture: "docs/architecture/example.md", spec: "specs/example.md", "adr-cache": "docs/adr/ADR-cache.md" }, findings: [], correction_targets: [], outcome: "approved", round: "r1", evidence_path: designReviewPath, evidence_sha256: sha(designReview), review_log_path: "docs/changes/example/review-log.md", review_log_sha256: sha(reviewLog.trimEnd()), stage_authority: "design-review" };
  writeFileSync(changePath, `${JSON.stringify(change, null, 2)}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), reviewLog, "utf8");

  const revision = status(root).lifecycle_revision;
  const evidencePath = "docs/changes/example/evidence/implementation-spec-route.md";
  writeFileSync(join(root, evidencePath), `Change ID: example\nSource stage: implement\nDestination artifact: spec\nReason: upstream-contract-gap\nFinding IDs: F-SPEC\nReturn stage: design-review\nLifecycle revision: ${revision}\n`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: revision,
    source_stage: "implement", destination_stage: "spec", destination_artifact_id: "spec", reason: "upstream-contract-gap",
    evidence_path: evidencePath, finding_ids: ["F-SPEC"], return_stage: "design-review", milestone_id: "M1", stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
  assert.equal(status(root).effective_state.current_stage, "spec");

  const correctedSpec = "# Specification\n\nCorrected projection contract.\n";
  writeFileSync(join(root, "specs", "example.md"), correctedSpec, "utf8");
  const authoringEvidence = "docs/changes/example/evidence/implementation-spec-authoring.md";
  writeFileSync(join(root, authoringEvidence), `Artifact path: specs/example.md\nArtifact identity: sha256:${sha(correctedSpec)}\nAuthoring result: complete\n`, "utf8");
  const recorded = execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: authoringEvidence,
    prior_artifact_sha256: change.lifecycle_cli.artifacts.spec.artifact_sha256, stage_authority: "spec",
  });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));
  const activeRoute = parseLifecycleYaml(readFileSync(changePath, "utf8")).lifecycle_cli.active_correction;
  const returnRevision = status(root).lifecycle_revision;
  const returnEvidence = "docs/changes/example/evidence/implementation-spec-return.md";
  writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${activeRoute.route_id}\nLifecycle revision: ${returnRevision}\nDestination artifact: spec\nArtifact path: specs/example.md\nArtifact identity: sha256:${sha(correctedSpec)}\nAuthoring evidence path: ${authoringEvidence}\nAuthoring evidence identity: sha256:${sha(readFileSync(join(root, authoringEvidence)))}\n`, "utf8");
  const returned = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
    route_id: activeRoute.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });
  assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
  const afterReturn = status(root);
  assert.equal(afterReturn.effective_state.current_stage, "design-review");
  assert.deepEqual(afterReturn.permitted_operations, ["record-package-review"], JSON.stringify(afterReturn));
});

test("artifact revision is rejected outside its current authoring stage without a correction route", async () => {
  const { root, changeRoot } = await fixture();
  const original = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  const revisedSpec = "# Example spec\n\nUnauthorized downstream revision.\n";
  writeFileSync(join(root, "specs", "example.md"), revisedSpec, "utf8");
  const evidencePath = "docs/changes/example/evidence/unrouted-spec-revision.md";
  writeFileSync(join(root, evidencePath), `Artifact path: specs/example.md\nArtifact identity: sha256:${sha(revisedSpec)}\nAuthoring result: complete\n`, "utf8");
  const priorChange = readFileSync(join(changeRoot, "change.yaml"), "utf8");

  const revised = execute(root, "record-artifact-revision", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
    artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: evidencePath,
    prior_artifact_sha256: original.lifecycle_cli.artifacts.spec.artifact_sha256, stage_authority: "spec",
  });

  assert.notEqual(revised.exitCode, 0);
  assert.equal(revised.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), priorChange);
});

test("route rejects lateral, missing-milestone, conflicting, and stale requests without mutation", async () => {
  for (const scenario of ["lateral", "missing-milestone", "conflicting", "stale"]) {
    const { root, changeRoot } = await fixture();
    const initial = status(root).lifecycle_revision;
    const routeEvidence = "docs/changes/example/evidence/correction-route.md";
    const destinationStage = scenario === "lateral" ? "verify" : "spec";
    writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: system-requirement-gap\nFinding IDs: F-CODE\nReturn stage: design-review\nLifecycle revision: ${initial}\n`, "utf8");
    const body = {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: scenario === "stale" ? `sha256:${"0".repeat(64)}` : initial,
      source_stage: "verify", destination_stage: destinationStage, destination_artifact_id: "spec", reason: "system-requirement-gap",
      evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "design-review", ...(scenario === "missing-milestone" ? {} : { milestone_id: "M2" }), stage_authority: "workflow",
    };
    const before = readFileSync(join(changeRoot, "change.yaml"));
    const first = execute(root, "route-correction", body);
    if (scenario === "conflicting") {
      assert.equal(first.exitCode, 0, JSON.stringify(first.result));
      const routedBytes = readFileSync(join(changeRoot, "change.yaml"));
      const conflictEvidence = "docs/changes/example/evidence/conflicting-route.md";
      writeFileSync(join(root, conflictEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: technical-realization-gap\nFinding IDs: F-CODE\nReturn stage: architecture\nLifecycle revision: ${status(root).lifecycle_revision}\n`, "utf8");
      const conflict = execute(root, "route-correction", { ...body, expected_lifecycle_revision: status(root).lifecycle_revision, reason: "technical-realization-gap", evidence_path: conflictEvidence });
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
  writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: system-requirement-gap\nFinding IDs: NOT-OPEN\nReturn stage: design-review\nLifecycle revision: ${current}\n`, "utf8");
  const rejected = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: current,
    source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "system-requirement-gap",
    evidence_path: routeEvidence, finding_ids: ["NOT-OPEN"], return_stage: "design-review", milestone_id: "M2", stage_authority: "workflow",
  });
  assert.equal(rejected.result.errors[0].code, "RL_CORRECTION_ROUTE_INVALID");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});

test("code review correction routes through implementation and returns to rereview", async () => {
  const { root, changeRoot } = await fixture();
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow_state.current_stage = "code-review";
  change.workflow_state.next_stage = "code-review";
  change.workflow_state.planned_work.milestones.M2.state = "review-requested";
  writeFileSync(changePath, `${JSON.stringify(change, null, 2)}\n`, "utf8");
  const current = status(root).lifecycle_revision;
  const routeEvidence = "docs/changes/example/evidence/implementation-route.md";
  writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: code-review\nDestination artifact: implement\nReason: upstream-proof-gap\nFinding IDs: F-CODE\nReturn stage: code-review\nLifecycle revision: ${current}\n`, "utf8");
  const routed = execute(root, "route-correction", {
    schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: current,
    source_stage: "code-review", destination_stage: "implement", destination_artifact_id: "implement", reason: "upstream-proof-gap",
    evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: "code-review", milestone_id: "M2", stage_authority: "workflow",
  });
  assert.equal(routed.exitCode, 0, JSON.stringify(routed.result));
  assert.equal(status(root).effective_state.current_stage, "implement");
  assert.deepEqual(status(root).permitted_operations, ["return-correction"]);

  const route = parseLifecycleYaml(readFileSync(changePath, "utf8")).lifecycle_cli.active_correction;
  const returnRevision = status(root).lifecycle_revision;
  const returnEvidence = "docs/changes/example/evidence/implementation-return.md";
  writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${route.route_id}\nLifecycle revision: ${returnRevision}\nDestination stage: implement\nCorrection result: complete\nRequired next stage: code-review\n`, "utf8");
  const returned = execute(root, "return-correction", {
    schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: returnRevision,
    route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
  });
  assert.equal(returned.exitCode, 0, JSON.stringify(returned.result));
  assert.equal(status(root).effective_state.current_stage, "code-review");
  const after = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  assert.equal(after.workflow_state.planned_work.milestones.M2.state, "review-requested");
  assert.equal(after.lifecycle_cli.correction_history[route.route_id].status, "returned");
});

test("v3 verify correction transaction enforces every exact owner and rereview boundary", async () => {
  const { root, changeRoot } = await fixture();
  const change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  change.lifecycle_contract = "stage-owned-change-local-v3";
  change.workflow_state.planned_work.current_milestone = "none";
  change.workflow_state.planned_work.remaining_implementation_milestones = [];
  change.workflow_state.planned_work.milestones.M2.state = "closed";
  for (const [id, kind, path] of [
    ["architecture", "architecture", "docs/architecture/example.md"],
    ["plan", "plan", "docs/plans/example.md"],
  ]) {
    mkdirSync(join(root, ...path.split("/").slice(0, -1)), { recursive: true });
    const content = `# ${kind}\n`;
    writeFileSync(join(root, path), content, "utf8");
    change.artifact_states[id] = { kind, path, role: "primary", lifecycle_state: kind === "plan" ? "active" : "approved" };
    change.lifecycle_cli.artifacts[id] = { artifact_kind: kind, artifact_role: "primary", artifact_path: path, artifact_sha256: sha(content), stage_authority: kind };
  }
  const routes = {
    "system-requirement-gap": ["spec", "design-review"],
    "technical-realization-gap": ["architecture", "design-review"],
    "verification-allocation-gap": ["plan", "delivery-review"],
    "implementation-defect": ["implement", "code-review"],
    "stale-or-incomplete-review": ["code-review", "code-review"],
    "ci-or-environment-gap": ["ci-maintenance", "verify"],
    "external-evidence-gap": ["external-evidence-acquisition", "verify"],
  };
  for (const [reason, [owner, returnStage]] of Object.entries(routes)) {
    const revision = `sha256:${"a".repeat(64)}`;
    const evidencePath = `docs/changes/example/evidence/v3-${reason}.md`;
    writeFileSync(join(root, evidencePath), `Change ID: example\nSource stage: verify\nDestination artifact: ${owner}\nReason: ${reason}\nFinding IDs: F-CODE\nReturn stage: ${returnStage}\nLifecycle revision: ${revision}\n`, "utf8");
    const requestBody = {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: revision,
      source_stage: "verify", destination_stage: owner, destination_artifact_id: owner, reason,
      evidence_path: evidencePath, finding_ids: ["F-CODE"], return_stage: returnStage, stage_authority: "workflow",
    };
    const result = evaluateLifecycleOperation({ root, change, request: requestBody });
    assert.equal(result.status, "routed", reason);
    assert.equal(result.candidate.workflow_state.current_stage, owner, reason);
    assert.equal(result.candidate.lifecycle_cli.active_correction.destination_kind, ["implement", "code-review", "ci-maintenance", "external-evidence-acquisition"].includes(owner) ? "stage" : undefined, reason);
    assert.throws(
      () => evaluateLifecycleOperation({ root, change, request: { ...requestBody, destination_stage: "verify", destination_artifact_id: "verify" } }),
      /unknown_value|exact owner/,
      reason,
    );
  }
  const unknownEvidence = "docs/changes/example/evidence/v3-unknown.md";
  writeFileSync(join(root, unknownEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: future-gap\nFinding IDs: F-CODE\nReturn stage: design-review\nLifecycle revision: sha256:${"a".repeat(64)}\n`, "utf8");
  assert.throws(
    () => evaluateLifecycleOperation({ root, change, request: {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
      source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "future-gap",
      evidence_path: unknownEvidence, finding_ids: ["F-CODE"], return_stage: "design-review", stage_authority: "workflow",
    } }),
    /unknown_value future-gap/,
  );
});

test("public v3 correction routes all seven Verify finding kinds to their exact return boundary", async () => {
  const routes = {
    "system-requirement-gap": ["spec", "design-review"],
    "technical-realization-gap": ["architecture", "design-review"],
    "verification-allocation-gap": ["plan", "delivery-review"],
    "implementation-defect": ["implement", "code-review"],
    "stale-or-incomplete-review": ["code-review", "code-review"],
    "ci-or-environment-gap": ["ci-maintenance", "verify"],
    "external-evidence-gap": ["external-evidence-acquisition", "verify"],
  };
  for (const [reason, [owner, returnStage]] of Object.entries(routes)) {
    const { root, changeRoot } = await fixture();
    activateContract(root, changeRoot, "stage-owned-change-local-v3");
    addV3CorrectionArtifacts(root, changeRoot);
    const routeRevision = status(root).lifecycle_revision;
    const routeEvidence = `docs/changes/example/evidence/public-v3-${reason}-route.md`;
    writeFileSync(join(root, routeEvidence), `Change ID: example\nSource stage: verify\nDestination artifact: ${owner}\nReason: ${reason}\nFinding IDs: F-CODE\nReturn stage: ${returnStage}\nLifecycle revision: ${routeRevision}\n`, "utf8");
    const routed = execute(root, "route-correction", {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: routeRevision,
      source_stage: "verify", destination_stage: owner, destination_artifact_id: owner, reason,
      evidence_path: routeEvidence, finding_ids: ["F-CODE"], return_stage: returnStage, stage_authority: "workflow",
    });
    assert.equal(routed.exitCode, 0, `${reason}: ${JSON.stringify(routed.result)}`);
    assert.equal(status(root).effective_state.current_stage, owner, reason);

    let change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
    const route = change.lifecycle_cli.active_correction;
    let returnEvidence;
    if (["spec", "architecture", "plan"].includes(owner)) {
      const destination = change.artifact_states[owner];
      const prior = change.lifecycle_cli.artifacts[owner].artifact_sha256;
      const revisedContent = `# ${owner}\n\nCorrected for ${reason}.\n`;
      writeFileSync(join(root, destination.path), revisedContent, "utf8");
      const authoringEvidence = `docs/changes/example/evidence/public-v3-${reason}-authoring.md`;
      writeFileSync(join(root, authoringEvidence), `Artifact path: ${destination.path}\nArtifact identity: sha256:${sha(revisedContent)}\nAuthoring result: complete\n`, "utf8");
      const revised = execute(root, "record-artifact-revision", {
        schema_version: 1, operation: "record-artifact-revision", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
        artifact_id: owner, artifact_kind: destination.kind, artifact_role: "primary", artifact_path: destination.path,
        evidence_path: authoringEvidence, prior_artifact_sha256: prior, stage_authority: owner,
      });
      assert.equal(revised.exitCode, 0, `${reason}: ${JSON.stringify(revised.result)}`);
      change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
      const registration = change.lifecycle_cli.artifacts[owner];
      returnEvidence = `docs/changes/example/evidence/public-v3-${reason}-return.md`;
      writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${route.route_id}\nLifecycle revision: ${status(root).lifecycle_revision}\nDestination artifact: ${owner}\nArtifact path: ${destination.path}\nArtifact identity: sha256:${registration.artifact_sha256}\nAuthoring evidence path: ${registration.authoring_evidence_path}\nAuthoring evidence identity: sha256:${registration.authoring_evidence_sha256}\n`, "utf8");
    } else {
      returnEvidence = `docs/changes/example/evidence/public-v3-${reason}-return.md`;
      writeFileSync(join(root, returnEvidence), `Change ID: example\nRoute ID: ${route.route_id}\nLifecycle revision: ${status(root).lifecycle_revision}\nDestination stage: ${owner}\nCorrection result: complete\nRequired next stage: ${returnStage}\n`, "utf8");
    }
    const returned = execute(root, "return-correction", {
      schema_version: 1, operation: "return-correction", change_id: "example", expected_lifecycle_revision: status(root).lifecycle_revision,
      route_id: route.route_id, evidence_path: returnEvidence, stage_authority: "workflow",
    });
    assert.equal(returned.exitCode, 0, `${reason}: ${JSON.stringify(returned.result)}`);
    assert.equal(status(root).effective_state.current_stage, returnStage, reason);
    assert.equal(parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8")).workflow_state.blocker, null, reason);
    if (["spec", "architecture", "plan", "implement"].includes(owner)) assert.notEqual(status(root).effective_state.current_stage, "verify", reason);
  }
});

test("public v1 and v2 correction requests reject every v3-only Verify finding kind without mutation", async () => {
  const reasons = ["system-requirement-gap", "technical-realization-gap", "verification-allocation-gap", "implementation-defect", "stale-or-incomplete-review", "ci-or-environment-gap", "external-evidence-gap"];
  for (const contract of ["stage-owned-change-local-v1", "stage-owned-change-local-v2"]) {
    for (const reason of reasons) {
      const { root, changeRoot } = await fixture();
      activateContract(root, changeRoot, contract);
      const revision = status(root).lifecycle_revision;
      const evidencePath = `docs/changes/example/evidence/${contract}-${reason}.md`;
      writeFileSync(join(root, evidencePath), `Change ID: example\nSource stage: verify\nDestination artifact: spec\nReason: ${reason}\nFinding IDs: F-CODE\nReturn stage: verify\nLifecycle revision: ${revision}\n`, "utf8");
      const before = readFileSync(join(changeRoot, "change.yaml"));
      const rejected = execute(root, "route-correction", {
        schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: revision,
        source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason,
        evidence_path: evidencePath, finding_ids: ["F-CODE"], return_stage: "verify", milestone_id: "M2", stage_authority: "workflow",
      });
      assert.equal(rejected.result.errors[0].code, "RL_INCOMPATIBLE_VERSION", `${contract}: ${reason}`);
      assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before, `${contract}: ${reason}`);
    }
  }
});

test("public v3 correction requests reject unknown, wrong, and Verify owners without mutation", async () => {
  const attempts = [
    ["future-gap", "spec", "design-review"],
    ["implementation-defect", "spec", "code-review"],
    ["implementation-defect", "verify", "code-review"],
  ];
  for (const [reason, owner, returnStage] of attempts) {
    const { root, changeRoot } = await fixture();
    activateContract(root, changeRoot, "stage-owned-change-local-v3");
    const revision = status(root).lifecycle_revision;
    const evidencePath = `docs/changes/example/evidence/rejected-${reason}-${owner}.md`;
    writeFileSync(join(root, evidencePath), `Change ID: example\nSource stage: verify\nDestination artifact: ${owner}\nReason: ${reason}\nFinding IDs: F-CODE\nReturn stage: ${returnStage}\nLifecycle revision: ${revision}\n`, "utf8");
    const before = readFileSync(join(changeRoot, "change.yaml"));
    const rejected = execute(root, "route-correction", {
      schema_version: 1, operation: "route-correction", change_id: "example", expected_lifecycle_revision: revision,
      source_stage: "verify", destination_stage: owner, destination_artifact_id: owner, reason,
      evidence_path: evidencePath, finding_ids: ["F-CODE"], return_stage: returnStage, stage_authority: "workflow",
    });
    assert.notEqual(rejected.exitCode, 0, `${reason}: ${owner}`);
    assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before, `${reason}: ${owner}`);
  }
});
