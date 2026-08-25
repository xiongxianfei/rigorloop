import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";

async function fixture(openFindings = "none") {
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
  writeFileSync(join(changeRoot, "reviews", "spec-review-r1.md"), `Review ID: spec-review-r1\nStage: spec-review\nRound: r1\nStatus: approved\nReviewed artifact path: specs/example.md\nReviewed artifact identity: sha256:${specIdentity}\nMaterial findings: none\n`, "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), `Review ID: earlier-review\nMaterial findings: OLD-1\nOpen findings: none\n\n### Review entry\n\nReview ID: spec-review-r1\nFinding ID: F-1\nMaterial findings: none\nOpen findings: ${openFindings}\n`, "utf8");
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
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /lifecycle_state: approved/);
});

test("stale request and unresolved findings block without changing bytes", async () => {
  const { root, changeRoot } = await fixture("F-1");
  const oldRevision = revision(root);
  const reviewPath = request(root, "review", { schema_version: 1, operation: "record-review", change_id: "example", expected_lifecycle_revision: oldRevision, artifact_id: "spec", evidence_path: "docs/changes/example/reviews/spec-review-r1.md", stage_authority: "spec-review" });
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).exitCode, 0);
  const before = readFileSync(join(changeRoot, "change.yaml"));
  assert.equal(executeLifecycleCli(["record-review", "--request", reviewPath], { cwd: root }).result.errors[0].code, "RL_STALE_OPERATION");
  const settlePath = request(root, "settle", { schema_version: 1, operation: "settle-artifact", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", stage_authority: "spec-review" });
  const blocked = executeLifecycleCli(["settle-artifact", "--request", settlePath], { cwd: root });
  assert.equal(blocked.result.errors[0].code, "RL_UNRESOLVED_MATERIAL_FINDING");
  assert.deepEqual(readFileSync(join(changeRoot, "change.yaml")), before);
});

test("validation and finding resolution register existing exact evidence only", async () => {
  const { root } = await fixture();
  const validationPath = request(root, "validation", { schema_version: 1, operation: "record-validation", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/evidence/validation.md", subject_path: "specs/example.md", stage_authority: "verify" });
  assert.equal(executeLifecycleCli(["record-validation", "--request", validationPath], { cwd: root }).exitCode, 0);
  const resolutionPath = request(root, "resolution", { schema_version: 1, operation: "record-finding-resolution", change_id: "example", expected_lifecycle_revision: revision(root), artifact_id: "spec", evidence_path: "docs/changes/example/review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" });
  assert.equal(executeLifecycleCli(["record-finding-resolution", "--request", resolutionPath], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8"), /resolutions:/);
});
