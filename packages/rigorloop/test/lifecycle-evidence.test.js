import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import {
  changeBytes,
  lifecycleRevision as packageLifecycleRevision,
  packageContext,
  packageRepository,
  setWorkflowStage,
  writePackageReview,
  writeRequest as writePackageRequest,
} from "./helpers/lifecycle-package-fixture.js";

async function fixture(openFindings = "none", reviewOutcome = "approved") {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-evidence-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  const spec = "# Example spec\n";
  writeFileSync(join(root, "specs", "example.md"), spec, "utf8");
  const { createHash } = await import("node:crypto");
  const specIdentity = createHash("sha256").update(spec).digest("hex");
  writeFileSync(join(changeRoot, "reviews", "spec-review-r1.md"), `Review ID: spec-review-r1\nStage: spec-review\nRound: r1\nStatus: ${reviewOutcome}\nReviewed artifact path: specs/example.md\nReviewed artifact identity: sha256:${specIdentity}\nMaterial findings: ${openFindings}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `Review ID: earlier-review\nMaterial findings: OLD-1\nOpen findings: none\n\n### Review entry\n\nReview ID: spec-review-r1\nFinding ID: F-1\nMaterial findings: ${openFindings}\nOpen findings: ${openFindings}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-resolution.md"), "Finding ID: F-1\nDisposition: accepted\nOwner: spec\nStatus: resolved\nValidation evidence: focused test\n", "utf8");
  writeFileSync(join(changeRoot, "evidence", "validation.md"), `Subject path: specs/example.md\nSubject identity: sha256:${specIdentity}\nValidation result: passed\n`, "utf8");
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
    lifecycle_state: review-required
    authoring_evidence: docs/changes/example/evidence/validation.md
workflow_state:
  lifecycle_state: active
  current_stage: spec-review
  next_stage: spec-review
  blocker: null
  evidence: []
review:
  status: not-reviewed
  unresolved_items: ${openFindings === "none" ? 0 : 1}
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

test("review registration binds exact evidence and settlement derives state", async () => {
  const { root, changeRoot } = await fixture();
  const reviewRequest = request(root, "review", {
    schema_version: 1,
    operation: "record-review",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    evidence_path: "docs/changes/example/reviews/spec-review-r1.md",
    stage_authority: "spec-review",
  });
  const dryRun = executeLifecycleCli(["record-review", "--request", reviewRequest, "--dry-run", "--format", "json"], { cwd: root });
  assert.equal(dryRun.exitCode, 0);
  assert.equal(dryRun.result.mutation.status, "planned");
  assert.doesNotMatch(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /lifecycle_cli/);
  const recorded = executeLifecycleCli(["record-review", "--request", reviewRequest, "--format", "json"], { cwd: root });
  assert.equal(recorded.exitCode, 0);
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /artifact_sha256/);

  const settleRequest = request(root, "settle", {
    schema_version: 1,
    operation: "settle-artifact",
    change_id: "example",
    expected_lifecycle_revision: revision(root),
    artifact_id: "spec",
    stage_authority: "spec-review",
  });
  const settled = executeLifecycleCli(["settle-artifact", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  const settledChange = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(settledChange, /lifecycle_state: approved/);
  assert.match(settledChange, /review:\n  latest_review: docs\/changes\/example\/reviews\/spec-review-r1\.md\n  review_log: docs\/changes\/example\/review-log\.md\n  reviewed_artifact: specs\/example\.md\n  status: clean\n  unresolved_items: 0/);
});

test("stale request and unresolved findings block without changing bytes", async () => {
  const { root, changeRoot } = await fixture("F-1");
  const oldRevision = revision(root);
  const reviewPath = request(root, "review", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: oldRevision, artifact_id: "spec", evidence_path: "docs/changes/example/reviews/spec-review-r1.md", stage_authority: "spec-review" });
  const recorded = executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));
  const before = readFileSync(join(changeRoot, "change.yaml"));
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).result.errors[0].code, "RL_STALE_OPERATION");
  const settlePath = request(root, "settle", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", stage_authority: "spec-review" });
  const blocked = executeLifecycleCli(["settle-artifact", "--request", settlePath], { cwd: root });
  assert.equal(blocked.result.errors[0].code, "RL_UNRESOLVED_MATERIAL_FINDING");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});

test("changes-requested settlement hands an artifact back despite its open findings", async () => {
  const { root, changeRoot } = await fixture("F-1", "changes-requested");
  const reviewPath = request(root, "review", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/reviews/spec-review-r1.md", stage_authority: "spec-review" });
  const recorded = executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));

  const settlePath = request(root, "settle", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", stage_authority: "spec-review" });
  const settled = executeLifecycleCli(["settle-artifact", "--request", settlePath, "--format", "json"], { cwd: root });

  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  const change = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(change, /lifecycle_state: revision-required/);
  assert.match(change, /review:\n(?:  .+\n)*  status: changes-requested\n  unresolved_items: 1/);
  assert.doesNotMatch(change, /\n    authoring_evidence:/);
  assert.deepEqual(settled.result.permitted_operations, ["record-artifact-revision"]);
});

test("validation and finding resolution register existing exact evidence only", async () => {
  const { root } = await fixture();
  const validationPath = request(root, "validation", { schema_version: 1, operation: "record-validation", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/evidence/validation.md", subject_path: "specs/example.md", stage_authority: "verify" });
  assert.equal(executeLifecycleCli(["record-validation", "--request", validationPath], { cwd: root }).exitCode, 0);
  const resolutionPath = request(root, "resolution", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  assert.equal(executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8"), /resolutions:/);
});

test("settlement subtracts resolutions for the exact target review occurrence", async () => {
  const { root, changeRoot } = await fixture("F-1", "approved");
  const reviewPath = request(root, "review-resolved", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/reviews/spec-review-r1.md", stage_authority: "spec-review" });
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).exitCode, 0);
  const resolutionPath = request(root, "resolution-before-settlement", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  assert.equal(executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath], { cwd: root }).exitCode, 0);
  const settlePath = request(root, "settle-resolved", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", stage_authority: "spec-review" });
  const settled = executeLifecycleCli(["settle-artifact", "--request", settlePath, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /lifecycle_state: approved/);
});

test("package review recording and approved settlement are atomic and compact", async () => {
  const { root } = await packageRepository();
  const context = packageContext(root);
  const review = writePackageReview(root, context);
  const recordRequest = writePackageRequest(root, "record-package", {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root),
    package_kind: "design",
    package_revision: review.packageFacts.aggregate_revision,
    upstream_binding: review.packageFacts.upstream_binding,
    member_artifact_ids: review.packageFacts.member_artifact_ids,
    evidence_path: review.reviewPath,
    stage_authority: "design-review",
  });
  const before = changeBytes(root);
  const dryRun = executeLifecycleCli(["record-package-review", "--request", recordRequest, "--dry-run", "--format", "json"], { cwd: root });
  assert.equal(dryRun.exitCode, 0, JSON.stringify(dryRun.result));
  assert.equal(changeBytes(root), before);
  const recorded = executeLifecycleCli(["record-package-review", "--request", recordRequest, "--format", "json"], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));

  const settleRequest = writePackageRequest(root, "settle-package", {
    schema_version: 1,
    operation: "settle-review-package",
    change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root),
    package_kind: "design",
    package_revision: review.packageFacts.aggregate_revision,
    stage_authority: "design-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  const change = changeBytes(root);
  const compactProjection = change.slice(change.indexOf("review_packages:"), change.indexOf("workflow_state:"));
  assert.match(change, /review_packages:\n  design:\n    aggregate_revision: sha256:/);
  assert.match(change, /authority: granted/);
  assert.doesNotMatch(compactProjection, /member_sha256/);
  assert.doesNotMatch(compactProjection, /artifact_sha256/);

  const replay = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(replay.exitCode, 0, JSON.stringify(replay.result));
  assert.equal(replay.result.status, "already-recorded");
  assert.equal(replay.result.state_changed, false);
});

test("non-approved package outcomes remain visible and grant no authority", async () => {
  const { root } = await packageRepository();
  const context = packageContext(root);
  const review = writePackageReview(root, context, {
    outcome: "changes-requested",
    findings: [{ id: "PKG-1", scope: "cross-artifact", affected: ["architecture", "spec"], owners: ["architecture", "spec"] }],
    correctionTargets: ["architecture", "spec"],
  });
  const recordRequest = writePackageRequest(root, "record-package-findings", {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root),
    package_kind: "design",
    package_revision: review.packageFacts.aggregate_revision,
    upstream_binding: review.packageFacts.upstream_binding,
    member_artifact_ids: review.packageFacts.member_artifact_ids,
    evidence_path: review.reviewPath,
    stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordRequest], { cwd: root }).exitCode, 0);
  const settleRequest = writePackageRequest(root, "settle-package-findings", {
    schema_version: 1,
    operation: "settle-review-package",
    change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root),
    package_kind: "design",
    package_revision: review.packageFacts.aggregate_revision,
    stage_authority: "design-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(changeBytes(root), /authority: withheld/);
  assert.match(changeBytes(root), /state: changes-requested/);
  assert.match(changeBytes(root), /affected_artifact_ids:\n\s+- architecture\n\s+- spec/);
});

test("every non-approved package outcome settles visibly without granting authority", async () => {
  for (const outcome of ["changes-requested", "blocked", "inconclusive"]) {
    const { root } = await packageRepository();
    const context = packageContext(root);
    const review = writePackageReview(root, context, outcome === "changes-requested" ? {
      outcome,
      findings: [{ id: "PKG-MATRIX", scope: "artifact-local", affected: ["spec"], owners: ["spec"] }],
      correctionTargets: ["spec"],
    } : { outcome });
    const recordRequest = writePackageRequest(root, `record-${outcome}`, {
      schema_version: 1, operation: "record-package-review", change_id: "example",
      expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
      package_revision: review.packageFacts.aggregate_revision, upstream_binding: review.packageFacts.upstream_binding,
      member_artifact_ids: review.packageFacts.member_artifact_ids, evidence_path: review.reviewPath, stage_authority: "design-review",
    });
    assert.equal(executeLifecycleCli(["record-package-review", "--request", recordRequest], { cwd: root }).exitCode, 0, outcome);
    const settleRequest = writePackageRequest(root, `settle-${outcome}`, {
      schema_version: 1, operation: "settle-review-package", change_id: "example",
      expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
      package_revision: review.packageFacts.aggregate_revision, stage_authority: "design-review",
    });
    const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
    assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
    assert.match(changeBytes(root), new RegExp(`state: ${outcome}`));
    assert.match(changeBytes(root), /authority: withheld/);
  }
});

test("delivery package binds the approved design revision and settles independently", async () => {
  const { root } = await packageRepository();
  const designContext = packageContext(root);
  const designReview = writePackageReview(root, designContext);
  const designRecord = writePackageRequest(root, "delivery-setup-design-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    package_revision: designReview.packageFacts.aggregate_revision, upstream_binding: designReview.packageFacts.upstream_binding,
    member_artifact_ids: designReview.packageFacts.member_artifact_ids, evidence_path: designReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", designRecord], { cwd: root }).exitCode, 0);
  const designSettle = writePackageRequest(root, "delivery-setup-design-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    package_revision: designReview.packageFacts.aggregate_revision, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", designSettle], { cwd: root }).exitCode, 0);

  setWorkflowStage(root, "delivery-review");
  const deliveryContext = packageContext(root, "delivery-review");
  assert.equal(deliveryContext.exitCode, 0, JSON.stringify(deliveryContext.result));
  assert.deepEqual(deliveryContext.result.context.review_package.member_artifact_ids, ["plan", "test-spec"]);
  assert.equal(deliveryContext.result.context.review_package.upstream_binding, designReview.packageFacts.aggregate_revision);
  const deliveryReview = writePackageReview(root, deliveryContext, { kind: "delivery" });
  const deliveryRecord = writePackageRequest(root, "delivery-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "delivery",
    package_revision: deliveryReview.packageFacts.aggregate_revision, upstream_binding: deliveryReview.packageFacts.upstream_binding,
    member_artifact_ids: deliveryReview.packageFacts.member_artifact_ids, evidence_path: deliveryReview.reviewPath, stage_authority: "delivery-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", deliveryRecord], { cwd: root }).exitCode, 0);
  const deliverySettle = writePackageRequest(root, "delivery-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "delivery",
    package_revision: deliveryReview.packageFacts.aggregate_revision, stage_authority: "delivery-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", deliverySettle, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(changeBytes(root), /review_packages:[\s\S]*delivery:[\s\S]*authority: granted/);
});

test("package review rejects unknown finding scope and stale member settlement unchanged", async () => {
  const unknown = await packageRepository();
  const unknownContext = packageContext(unknown.root);
  const unknownReview = writePackageReview(unknown.root, unknownContext, {
    outcome: "changes-requested",
    findings: [{ id: "PKG-UNKNOWN", scope: "mixed", affected: ["architecture", "spec"], owners: ["architecture", "spec"] }],
    correctionTargets: ["architecture", "spec"],
  });
  const unknownRequest = writePackageRequest(unknown.root, "unknown-scope", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(unknown.root), package_kind: "design",
    package_revision: unknownReview.packageFacts.aggregate_revision, upstream_binding: unknownReview.packageFacts.upstream_binding,
    member_artifact_ids: unknownReview.packageFacts.member_artifact_ids, evidence_path: unknownReview.reviewPath, stage_authority: "design-review",
  });
  const rejected = executeLifecycleCli(["record-package-review", "--request", unknownRequest, "--format", "json"], { cwd: unknown.root });
  assert.equal(rejected.result.errors[0].code, "RL_INVALID_REQUEST");
  assert.match(rejected.result.errors[0].summary, /finding scope/);

  const stale = await packageRepository();
  const staleContext = packageContext(stale.root);
  const staleReview = writePackageReview(stale.root, staleContext);
  const recordRequest = writePackageRequest(stale.root, "stale-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(stale.root), package_kind: "design",
    package_revision: staleReview.packageFacts.aggregate_revision, upstream_binding: staleReview.packageFacts.upstream_binding,
    member_artifact_ids: staleReview.packageFacts.member_artifact_ids, evidence_path: staleReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordRequest], { cwd: stale.root }).exitCode, 0);
  writeFileSync(join(stale.root, stale.sources.spec[0]), "# Changed after review\n", "utf8");
  const beforeStaleSettle = changeBytes(stale.root);
  const settleRequest = writePackageRequest(stale.root, "stale-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(stale.root), package_kind: "design",
    package_revision: staleReview.packageFacts.aggregate_revision, stage_authority: "design-review",
  });
  const staleResult = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: stale.root });
  assert.equal(staleResult.result.errors[0].code, "RL_STALE_EVIDENCE");
  assert.equal(changeBytes(stale.root), beforeStaleSettle);
});
