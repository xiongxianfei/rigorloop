import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml, serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import {
  changeBytes,
  lifecycleRevision,
  packageContext,
  packageRepository,
  setWorkflowStage,
  writePackageReview,
  writeRequest,
} from "./helpers/lifecycle-package-fixture.js";

function advance(root, source, destination, name = `${source}-to-${destination}`) {
  const request = writeRequest(root, name, {
    schema_version: 1,
    operation: "advance-stage",
    change_id: "example",
    expected_lifecycle_revision: lifecycleRevision(root),
    source_stage: source,
    destination_stage: destination,
    stage_authority: "workflow",
  });
  return executeLifecycleCli(["advance-stage", "--request", request, "--format", "json"], { cwd: root });
}

function approvePackage(root, kind) {
  const stage = `${kind}-review`;
  setWorkflowStage(root, stage);
  const context = packageContext(root, stage);
  const review = writePackageReview(root, context, { kind });
  const record = writeRequest(root, `record-${kind}`, {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: lifecycleRevision(root),
    package_kind: kind,
    review_id: review.reviewId,
    upstream_review_id: review.packageFacts.upstream_review_id,
    members: review.packageFacts.members,
    evidence_path: review.reviewPath,
    stage_authority: stage,
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", record], { cwd: root }).exitCode, 0);
  const settle = writeRequest(root, `settle-${kind}`, {
    schema_version: 1,
    operation: "settle-review-package",
    change_id: "example",
    expected_lifecycle_revision: lifecycleRevision(root),
    package_kind: kind,
    review_id: review.reviewId,
    stage_authority: stage,
  });
  assert.equal(executeLifecycleCli(["settle-review-package", "--request", settle], { cwd: root }).exitCode, 0);
  return review;
}

test("consolidated authoring stages advance only across adjacent edges", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "proposal-review" });
  for (const [source, destination] of [["proposal-review", "architecture"], ["architecture", "spec"], ["spec", "design-review"]]) {
    setWorkflowStage(root, source);
    const status = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
    assert.equal(status.permitted_operations.includes("advance-stage"), true, source);
    const execution = advance(root, source, destination);
    assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  }
  const recorded = parseLifecycleYaml(readFileSync(join(changeRoot, "change.yaml"), "utf8"));
  assert.equal(recorded.workflow_state.current_stage, "design-review");
  assert.equal(recorded.workflow_state.next_stage, "design-review");
});

test("approved package authority advances design and delivery gates", async () => {
  const { root } = await packageRepository();
  approvePackage(root, "design");
  const designAdvance = advance(root, "design-review", "plan");
  assert.equal(designAdvance.exitCode, 0, JSON.stringify(designAdvance.result));

  approvePackage(root, "delivery");
  const deliveryAdvance = advance(root, "delivery-review", "implement");
  assert.equal(deliveryAdvance.exitCode, 0, JSON.stringify(deliveryAdvance.result));
});

test("package settlement remains isolated until workflow advances", async () => {
  const { root } = await packageRepository();
  approvePackage(root, "design");
  const settled = parseLifecycleYaml(changeBytes(root));
  assert.equal(settled.review_packages.design.status, "approved");
  assert.equal(settled.workflow_state.current_stage, "design-review");
  assert.equal(settled.workflow_state.next_stage, "design-review");
});

test("retired and skipped progression edges fail without mutation", async () => {
  const { root } = await packageRepository({ stage: "spec-review" });
  const before = changeBytes(root);
  for (const [source, destination] of [["spec-review", "architecture"], ["spec", "plan"], ["design-review", "implement"]]) {
    setWorkflowStage(root, source);
    const stable = changeBytes(root);
    const execution = advance(root, source, destination, `reject-${source}-${destination}`);
    assert.equal(execution.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
    assert.equal(changeBytes(root), stable);
  }
  assert.notEqual(before.length, 0);
});

test("design review cannot advance without current approved package authority", async () => {
  const { root } = await packageRepository({ stage: "design-review" });
  const before = changeBytes(root);
  const status = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
  assert.equal(status.permitted_operations.includes("advance-stage"), false);
  const execution = advance(root, "design-review", "plan");
  assert.equal(execution.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.equal(changeBytes(root), before);
});

test("advance-stage synchronizes active automation and rejects contradiction", async () => {
  const { root, changeRoot } = await packageRepository({ stage: "architecture" });
  const path = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow.automation = { current_stage: "architecture", mechanism: "bounded-review-fix", status: "active" };
  writeFileSync(path, serializeLifecycleYaml(change), "utf8");

  const execution = advance(root, "architecture", "spec", "automation-sync");
  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.equal(parseLifecycleYaml(changeBytes(root)).workflow.automation.current_stage, "spec");

  setWorkflowStage(root, "architecture");
  const contradictory = parseLifecycleYaml(changeBytes(root));
  contradictory.workflow.automation.current_stage = "proposal-review";
  writeFileSync(path, serializeLifecycleYaml(contradictory), "utf8");
  const before = changeBytes(root);
  const rejected = advance(root, "architecture", "spec", "automation-contradiction");
  assert.equal(rejected.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.equal(changeBytes(root), before);
});

test("downstream status rejects stale and mixed package authority", async () => {
  const stale = await packageRepository();
  approvePackage(stale.root, "design");
  const delivery = approvePackage(stale.root, "delivery");
  setWorkflowStage(stale.root, "verify");
  assert.equal(executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: stale.root }).exitCode, 0);
  writeFileSync(join(stale.root, delivery.reviewPath), `${readFileSync(join(stale.root, delivery.reviewPath), "utf8")}\nchanged\n`, "utf8");
  const staleStatus = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: stale.root });
  assert.equal(staleStatus.exitCode, 2);
  assert.equal(staleStatus.result.blockers.some((item) => item.code === "RL_STALE_EVIDENCE"), true);
  assert.equal(staleStatus.result.effective_state.downstream_package_authority.packages.delivery.state, "stale");

  const mixed = await packageRepository();
  approvePackage(mixed.root, "design");
  approvePackage(mixed.root, "delivery");
  setWorkflowStage(mixed.root, "code-review");
  const mixedPath = join(mixed.changeRoot, "change.yaml");
  const mixedChange = parseLifecycleYaml(changeBytes(mixed.root));
  mixedChange.review_packages.delivery.upstream_review_id = "design-review-other";
  writeFileSync(mixedPath, serializeLifecycleYaml(mixedChange), "utf8");
  const mixedStatus = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: mixed.root });
  assert.equal(mixedStatus.exitCode, 2);
  assert.equal(mixedStatus.result.effective_state.review_packages.delivery.status, "review-required");
  assert.equal(mixedStatus.result.effective_state.review_packages.delivery.authority, "withheld");
  assert.equal(mixedStatus.result.effective_state.downstream_package_authority.packages.delivery.state, "mixed");
});
