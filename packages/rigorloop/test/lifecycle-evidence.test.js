import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
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
  mkdirSync(join(root, "docs", "proposals"), { recursive: true });
  const proposal = "# Example proposal\n";
  writeFileSync(join(root, "docs", "proposals", "example.md"), proposal, "utf8");
  const { createHash } = await import("node:crypto");
  const proposalIdentity = createHash("sha256").update(proposal).digest("hex");
  writeFileSync(join(changeRoot, "reviews", "proposal-review-r1.md"), `Review ID: proposal-review-r1\nStage: proposal-review\nRound: r1\nStatus: ${reviewOutcome}\nReviewed artifact path: docs/proposals/example.md\nReviewed artifact identity: sha256:${proposalIdentity}\nMaterial findings: ${openFindings}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `Review ID: earlier-review\nMaterial findings: OLD-1\nOpen findings: none\n\n### Review entry\n\nReview ID: proposal-review-r1\nFinding ID: F-1\nMaterial findings: ${openFindings}\nOpen findings: ${openFindings}\n`, "utf8");
  writeFileSync(join(changeRoot, "review-resolution.md"), "Finding ID: F-1\nDisposition: accepted\nOwner: proposal\nStatus: resolved\nValidation evidence: focused test\n", "utf8");
  writeFileSync(join(changeRoot, "evidence", "validation.md"), `Subject path: docs/proposals/example.md\nSubject identity: sha256:${proposalIdentity}\nValidation result: passed\n`, "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  proposal:
    kind: proposal
    path: docs/proposals/example.md
    role: primary
    lifecycle_state: review-required
    authoring_evidence: docs/changes/example/evidence/validation.md
workflow_state:
  lifecycle_state: active
  current_stage: proposal-review
  next_stage: proposal-review
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
    artifact_id: "proposal",
    evidence_path: "docs/changes/example/reviews/proposal-review-r1.md",
    stage_authority: "proposal-review",
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
    artifact_id: "proposal",
    stage_authority: "proposal-review",
  });
  const settled = executeLifecycleCli(["settle-artifact", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  const settledChange = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(settledChange, /lifecycle_state: accepted/);
  assert.match(settledChange, /review:\n  latest_review: docs\/changes\/example\/reviews\/proposal-review-r1\.md\n  review_log: docs\/changes\/example\/review-log\.md\n  reviewed_artifact: docs\/proposals\/example\.md\n  status: clean\n  unresolved_items: 0/);
});

test("stale request and unresolved findings block without changing bytes", async () => {
  const { root, changeRoot } = await fixture("F-1");
  const oldRevision = revision(root);
  const reviewPath = request(root, "review", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: oldRevision, artifact_id: "proposal", evidence_path: "docs/changes/example/reviews/proposal-review-r1.md", stage_authority: "proposal-review" });
  const recorded = executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));
  const before = readFileSync(join(changeRoot, "change.yaml"));
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).result.errors[0].code, "RL_STALE_OPERATION");
  const settlePath = request(root, "settle", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", stage_authority: "proposal-review" });
  const blocked = executeLifecycleCli(["settle-artifact", "--request", settlePath], { cwd: root });
  assert.equal(blocked.result.errors[0].code, "RL_UNRESOLVED_MATERIAL_FINDING");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});

test("changes-requested settlement hands an artifact back despite its open findings", async () => {
  const { root, changeRoot } = await fixture("F-1", "changes-requested");
  const reviewPath = request(root, "review", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/reviews/proposal-review-r1.md", stage_authority: "proposal-review" });
  const recorded = executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));

  const settlePath = request(root, "settle", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", stage_authority: "proposal-review" });
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
  const validationPath = request(root, "validation", { schema_version: 1, operation: "record-validation", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/evidence/validation.md", subject_path: "docs/proposals/example.md", stage_authority: "verify" });
  assert.equal(executeLifecycleCli(["record-validation", "--request", validationPath], { cwd: root }).exitCode, 0);
  const resolutionPath = request(root, "resolution", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  assert.equal(executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8"), /resolutions:/);
});

test("finding resolution reads fields from the requested finding section", async () => {
  const { root, changeRoot } = await fixture();
  writeFileSync(join(changeRoot, "review-resolution.md"), `# Resolution\n\nFinding ID: OTHER-1\nDisposition: accepted\nOwner: other\nStatus: resolved\nValidation evidence: other proof\n\nFinding ID: F-1\nDisposition: partially-accepted\nOwner: spec\nStatus: resolved\nValidation evidence: focused proof\n`, "utf8");
  const resolutionPath = request(root, "scoped-resolution", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  const execution = executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath, "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  const change = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(change.lifecycle_cli.resolutions["F-1"].disposition, "partially-accepted");
  assert.equal(change.lifecycle_cli.resolutions["F-1"].owner, "spec");
});

test("settlement subtracts resolutions for the exact target review occurrence", async () => {
  const { root, changeRoot } = await fixture("F-1", "approved");
  const reviewPath = request(root, "review-resolved", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/reviews/proposal-review-r1.md", stage_authority: "proposal-review" });
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).exitCode, 0);
  const resolutionPath = request(root, "resolution-before-settlement", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  assert.equal(executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath], { cwd: root }).exitCode, 0);
  const settlePath = request(root, "settle-resolved", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "proposal", stage_authority: "proposal-review" });
  const settled = executeLifecycleCli(["settle-artifact", "--request", settlePath, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /lifecycle_state: accepted/);
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
    review_id: review.reviewId,
    upstream_review_id: review.packageFacts.upstream_review_id,
    members: review.packageFacts.members,
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
    review_id: review.reviewId,
    stage_authority: "design-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  const change = changeBytes(root);
  const compactProjection = change.slice(change.indexOf("review_packages:"), change.indexOf("workflow_state:"));
  assert.match(change, /review_packages:\n  design:\n    authority: granted/);
  assert.match(change, /members:\n(?:      .+\n)*      architecture: docs\/architecture\/example\.md/);
  assert.match(change, /upstream_review_id: proposal-review-r1/);
  assert.doesNotMatch(compactProjection, /aggregate_revision|package_revision/);
  assert.match(change, /authority: granted/);
  assert.doesNotMatch(compactProjection, /member_sha256/);
  assert.doesNotMatch(compactProjection, /artifact_sha256/);

  const replay = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(replay.exitCode, 0, JSON.stringify(replay.result));
  assert.equal(replay.result.status, "already-recorded");
  assert.equal(replay.result.state_changed, false);

  writeFileSync(join(root, review.reviewPath), `${readFileSync(join(root, review.reviewPath), "utf8")}\nChanged after settlement.\n`, "utf8");
  const staleReplay = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(staleReplay.result.errors[0].code, "RL_STALE_EVIDENCE");
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
    review_id: review.reviewId,
    upstream_review_id: review.packageFacts.upstream_review_id,
    members: review.packageFacts.members,
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
    review_id: review.reviewId,
    stage_authority: "design-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(changeBytes(root), /authority: withheld/);
  assert.match(changeBytes(root), /status: changes-requested/);
  assert.match(changeBytes(root), /affected_artifact_ids:\n\s+- architecture\n\s+- spec/);
});

test("governed member revision invalidates approved package without package hashes", async () => {
  const { root } = await packageRepository();
  const review = writePackageReview(root, packageContext(root));
  const record = writePackageRequest(root, "invalidation-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design", review_id: review.reviewId,
    members: review.packageFacts.members, upstream_review_id: review.packageFacts.upstream_review_id,
    evidence_path: review.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", record], { cwd: root }).exitCode, 0);
  const settle = writePackageRequest(root, "invalidation-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design", review_id: review.reviewId, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", settle], { cwd: root }).exitCode, 0);

  const revised = "# Revised specification\n";
  writeFileSync(join(root, "specs/example.md"), revised, "utf8");
  const evidencePath = "docs/changes/example/evidence/spec-revision.md";
  writeFileSync(join(root, evidencePath), `Artifact path: specs/example.md\nArtifact identity: sha256:${createHash("sha256").update(revised).digest("hex")}\nAuthoring result: complete\n`, "utf8");
  const prior = parseLifecycleYaml(changeBytes(root)).lifecycle_cli.artifacts.spec.artifact_sha256;
  const revise = writePackageRequest(root, "invalidate-member", {
    schema_version: 1, operation: "record-artifact-revision", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary",
    artifact_path: "specs/example.md", evidence_path: evidencePath, prior_artifact_sha256: prior, stage_authority: "spec",
  });
  const result = executeLifecycleCli(["record-artifact-revision", "--request", revise, "--format", "json"], { cwd: root });
  assert.equal(result.exitCode, 0, JSON.stringify(result.result));
  const changed = parseLifecycleYaml(changeBytes(root));
  assert.equal(changed.review_packages.design.status, "review-required");
  assert.equal(changed.review_packages.design.authority, "withheld");
  assert.equal(changed.review_packages.design.review_id, review.reviewId);
  assert.equal(JSON.stringify(changed.review_packages.design).includes("sha256"), false);
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
      review_id: review.reviewId, upstream_review_id: review.packageFacts.upstream_review_id,
      members: review.packageFacts.members, evidence_path: review.reviewPath, stage_authority: "design-review",
    });
    assert.equal(executeLifecycleCli(["record-package-review", "--request", recordRequest], { cwd: root }).exitCode, 0, outcome);
    const settleRequest = writePackageRequest(root, `settle-${outcome}`, {
      schema_version: 1, operation: "settle-review-package", change_id: "example",
      expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
      review_id: review.reviewId, stage_authority: "design-review",
    });
    const settled = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: root });
    assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
    assert.match(changeBytes(root), new RegExp(`status: ${outcome}`));
    assert.match(changeBytes(root), /authority: withheld/);
    const status = packageContext(root).result.context.review_package;
    assert.equal(status.next_permitted_operation, { "changes-requested": "route-correction", blocked: "record-package-review", inconclusive: "record-package-review" }[outcome]);
  }
});

test("blocked package review without correction targets permits an unchanged clean rereview", async () => {
  const { root } = await packageRepository();
  const initialContext = packageContext(root);
  const blockedReview = writePackageReview(root, initialContext, { outcome: "blocked" });
  const recordBlocked = writePackageRequest(root, "record-blocked-r1", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: blockedReview.reviewId, upstream_review_id: blockedReview.packageFacts.upstream_review_id,
    members: blockedReview.packageFacts.members, evidence_path: blockedReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordBlocked], { cwd: root }).exitCode, 0);
  const settleBlocked = writePackageRequest(root, "settle-blocked-r1", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: blockedReview.reviewId, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", settleBlocked], { cwd: root }).exitCode, 0);

  const blockedContext = packageContext(root).result.context.review_package;
  assert.equal(blockedContext.next_permitted_operation, "record-package-review");

  const approvedReview = writePackageReview(root, packageContext(root), { outcome: "approved", round: "r2" });
  const recordApproved = writePackageRequest(root, "record-approved-r2", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: approvedReview.reviewId, upstream_review_id: approvedReview.packageFacts.upstream_review_id,
    members: approvedReview.packageFacts.members, evidence_path: approvedReview.reviewPath, stage_authority: "design-review",
  });
  const recorded = executeLifecycleCli(["record-package-review", "--request", recordApproved, "--format", "json"], { cwd: root });
  assert.equal(recorded.exitCode, 0, JSON.stringify(recorded.result));
  const settleApproved = writePackageRequest(root, "settle-approved-r2", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: approvedReview.reviewId, stage_authority: "design-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", settleApproved, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.equal(packageContext(root).result.context.review_package.authority, "granted");
});

test("blocked package rereview rejects modified prior review evidence", async () => {
  const { root } = await packageRepository();
  const blockedReview = writePackageReview(root, packageContext(root), { outcome: "blocked" });
  const recordBlocked = writePackageRequest(root, "record-blocked-before-stale", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: blockedReview.reviewId, upstream_review_id: blockedReview.packageFacts.upstream_review_id,
    members: blockedReview.packageFacts.members, evidence_path: blockedReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordBlocked], { cwd: root }).exitCode, 0);
  const settleBlocked = writePackageRequest(root, "settle-blocked-before-stale", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: blockedReview.reviewId, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", settleBlocked], { cwd: root }).exitCode, 0);

  const currentContext = packageContext(root);
  const priorEvidence = join(root, blockedReview.reviewPath);
  writeFileSync(priorEvidence, `${readFileSync(priorEvidence, "utf8")}\nModified after settlement.\n`, "utf8");
  const staleContext = packageContext(root).result.context.review_package;
  assert.equal(staleContext.status, "incomplete");
  assert.equal(staleContext.next_permitted_operation, null);
  assert.equal(staleContext.errors[0].code, "RL_STALE_EVIDENCE");
  const approvedReview = writePackageReview(root, currentContext, { outcome: "approved", round: "r2" });
  const recordApproved = writePackageRequest(root, "record-approved-after-stale", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: approvedReview.reviewId, upstream_review_id: approvedReview.packageFacts.upstream_review_id,
    members: approvedReview.packageFacts.members, evidence_path: approvedReview.reviewPath, stage_authority: "design-review",
  });
  const before = changeBytes(root);
  const rejected = executeLifecycleCli(["record-package-review", "--request", recordApproved, "--format", "json"], { cwd: root });
  assert.notEqual(rejected.exitCode, 0);
  assert.equal(rejected.result.errors[0].code, "RL_STALE_EVIDENCE");
  assert.equal(changeBytes(root), before);
});

test("replacement Proposal Review invalidates approved design authority", async () => {
  const { root } = await packageRepository();
  const designReview = writePackageReview(root, packageContext(root));
  const recordDesign = writePackageRequest(root, "proposal-replacement-design-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design", review_id: designReview.reviewId,
    members: designReview.packageFacts.members, upstream_review_id: designReview.packageFacts.upstream_review_id,
    evidence_path: designReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordDesign], { cwd: root }).exitCode, 0);
  const settleDesign = writePackageRequest(root, "proposal-replacement-design-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design", review_id: designReview.reviewId, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", settleDesign], { cwd: root }).exitCode, 0);

  setWorkflowStage(root, "proposal-review");
  const proposalBytes = readFileSync(join(root, "docs/proposals/example.md"));
  const proposalIdentity = createHash("sha256").update(proposalBytes).digest("hex");
  const reviewPath = "docs/changes/example/reviews/proposal-review-r2.md";
  writeFileSync(join(root, reviewPath), `Review ID: proposal-review-r2\nStage: proposal-review\nRound: r2\nStatus: approved\nReviewed artifact path: docs/proposals/example.md\nReviewed artifact identity: sha256:${proposalIdentity}\nMaterial findings: none\n`, "utf8");
  writeFileSync(join(root, "docs/changes/example/review-log.md"), `### Review entry\n\nReview ID: proposal-review-r2\nStage: proposal-review\nRound: r2\nStatus: approved\nMaterial findings: none\nOpen findings: none\n`, "utf8");
  const recordProposal = writePackageRequest(root, "proposal-replacement-record", {
    schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: packageLifecycleRevision(root),
    artifact_id: "proposal", evidence_path: reviewPath, stage_authority: "proposal-review",
  });
  assert.equal(executeLifecycleCli(["record-review", "--request", recordProposal], { cwd: root }).exitCode, 0);
  const settleProposal = writePackageRequest(root, "proposal-replacement-settle", {
    schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: packageLifecycleRevision(root),
    artifact_id: "proposal", stage_authority: "proposal-review",
  });
  const result = executeLifecycleCli(["settle-artifact", "--request", settleProposal, "--format", "json"], { cwd: root });
  assert.equal(result.exitCode, 0, JSON.stringify(result.result));
  const changed = parseLifecycleYaml(changeBytes(root));
  assert.equal(changed.review_packages.design.status, "review-required");
  assert.equal(changed.review_packages.design.authority, "withheld");
  assert.equal(changed.review_packages.design.review_id, designReview.reviewId);
});

test("delivery package binds the approved design revision and settles independently", async () => {
  const { root } = await packageRepository();
  const designContext = packageContext(root);
  const designReview = writePackageReview(root, designContext);
  const designRecord = writePackageRequest(root, "delivery-setup-design-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: designReview.reviewId, upstream_review_id: designReview.packageFacts.upstream_review_id,
    members: designReview.packageFacts.members, evidence_path: designReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", designRecord], { cwd: root }).exitCode, 0);
  const designSettle = writePackageRequest(root, "delivery-setup-design-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "design",
    review_id: designReview.reviewId, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", designSettle], { cwd: root }).exitCode, 0);

  setWorkflowStage(root, "delivery-review");
  const deliveryContext = packageContext(root, "delivery-review");
  assert.equal(deliveryContext.exitCode, 0, JSON.stringify(deliveryContext.result));
  assert.deepEqual(deliveryContext.result.context.review_package.members, { plan: "docs/plans/example.md", "test-spec": "specs/example.test.md" });
  assert.equal(deliveryContext.result.context.review_package.upstream_review_id, designReview.reviewId);
  const deliveryReview = writePackageReview(root, deliveryContext, { kind: "delivery" });
  const deliveryRecord = writePackageRequest(root, "delivery-record", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "delivery",
    review_id: deliveryReview.reviewId, upstream_review_id: deliveryReview.packageFacts.upstream_review_id,
    members: deliveryReview.packageFacts.members, evidence_path: deliveryReview.reviewPath, stage_authority: "delivery-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", deliveryRecord], { cwd: root }).exitCode, 0);
  const deliverySettle = writePackageRequest(root, "delivery-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(root), package_kind: "delivery",
    review_id: deliveryReview.reviewId, stage_authority: "delivery-review",
  });
  const settled = executeLifecycleCli(["settle-review-package", "--request", deliverySettle, "--format", "json"], { cwd: root });
  assert.equal(settled.exitCode, 0, JSON.stringify(settled.result));
  assert.match(changeBytes(root), /review_packages:[\s\S]*delivery:[\s\S]*authority: granted/);
});

test("package review rejects unknown finding scope and ignores ungoverned direct edits", async () => {
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
    review_id: unknownReview.reviewId, upstream_review_id: unknownReview.packageFacts.upstream_review_id,
    members: unknownReview.packageFacts.members, evidence_path: unknownReview.reviewPath, stage_authority: "design-review",
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
    review_id: staleReview.reviewId, upstream_review_id: staleReview.packageFacts.upstream_review_id,
    members: staleReview.packageFacts.members, evidence_path: staleReview.reviewPath, stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", recordRequest], { cwd: stale.root }).exitCode, 0);
  writeFileSync(join(stale.root, stale.sources.spec[0]), "# Changed after review\n", "utf8");
  const beforeStaleSettle = changeBytes(stale.root);
  const settleRequest = writePackageRequest(stale.root, "stale-settle", {
    schema_version: 1, operation: "settle-review-package", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(stale.root), package_kind: "design",
    review_id: staleReview.reviewId, stage_authority: "design-review",
  });
  const staleResult = executeLifecycleCli(["settle-review-package", "--request", settleRequest, "--format", "json"], { cwd: stale.root });
  assert.equal(staleResult.exitCode, 0, JSON.stringify(staleResult.result));
  assert.notEqual(changeBytes(stale.root), beforeStaleSettle);
});

test("package review rejects contradictory finding owner and correction target mappings", async () => {
  const wrongOwner = await packageRepository();
  const ownerReview = writePackageReview(wrongOwner.root, packageContext(wrongOwner.root), {
    outcome: "changes-requested",
    findings: [{ id: "PKG-OWNER", scope: "artifact-local", affected: ["spec"], owners: ["plan"] }],
    correctionTargets: ["spec"],
  });
  const ownerRequest = writePackageRequest(wrongOwner.root, "wrong-owner", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(wrongOwner.root), package_kind: "design", review_id: ownerReview.reviewId,
    members: ownerReview.packageFacts.members, upstream_review_id: ownerReview.packageFacts.upstream_review_id,
    evidence_path: ownerReview.reviewPath, stage_authority: "design-review",
  });
  const ownerResult = executeLifecycleCli(["record-package-review", "--request", ownerRequest, "--format", "json"], { cwd: wrongOwner.root });
  assert.equal(ownerResult.result.errors[0].code, "RL_AUTHORITY_BOUNDARY");

  const wrongTarget = await packageRepository();
  const targetReview = writePackageReview(wrongTarget.root, packageContext(wrongTarget.root), {
    outcome: "changes-requested",
    findings: [{ id: "PKG-TARGET", scope: "artifact-local", affected: ["spec"], owners: ["spec"] }],
    correctionTargets: ["architecture"],
  });
  const targetRequest = writePackageRequest(wrongTarget.root, "wrong-target", {
    schema_version: 1, operation: "record-package-review", change_id: "example",
    expected_lifecycle_revision: packageLifecycleRevision(wrongTarget.root), package_kind: "design", review_id: targetReview.reviewId,
    members: targetReview.packageFacts.members, upstream_review_id: targetReview.packageFacts.upstream_review_id,
    evidence_path: targetReview.reviewPath, stage_authority: "design-review",
  });
  const targetResult = executeLifecycleCli(["record-package-review", "--request", targetRequest, "--format", "json"], { cwd: wrongTarget.root });
  assert.equal(targetResult.result.errors[0].code, "RL_AUTHORITY_BOUNDARY");
});
