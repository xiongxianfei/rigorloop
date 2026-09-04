import assert from "node:assert/strict";
import { test } from "node:test";

import { projectCompactSnapshot } from "../dist/lib/compact-projection.js";

const d = `sha256:${"a".repeat(64)}`;
const snapshot = {
  change_id: "example",
  lifecycle_contract: "compact-current-state-v1",
  lifecycle_revision: d,
  current_stage: "code-review",
  artifacts: { spec: { artifact_id: "spec", kind: "spec", role: "primary", path: "specs/example.md", identity: d, owner: "spec", status: "approved" } },
  reviews: { M1: { target_id: "M1", path: "docs/changes/example/reviews/code-review-M1.md", identity: d, review_id: "review-2", outcome: "changes-requested", reviewer_authority: "code-review", status: "current" } },
  active_work: null,
  open_findings: { F1: { finding_id: "F1", review_target_id: "M1", review_path: "docs/changes/example/reviews/code-review-M1.md", review_identity: d, owner: "implement", severity: "major", blocking_effect: "blocks-progression" } },
  material_decisions: {},
  evidence: {},
  blockers: [],
  remaining_work: { W1: { work_id: "W1", kind: "task", owner: "implement", required_action: "Fix F1", status: "pending" } },
};

test("bounded views retain exact shape and empty unrelated categories", () => {
  const projection = projectCompactSnapshot(snapshot, "open-findings");
  assert.equal(projection.view, "open-findings");
  assert.equal(projection.change_id, "example");
  assert.equal(projection.lifecycle_contract, "compact-current-state-v1");
  assert.equal(projection.lifecycle_revision, d);
  assert.equal(projection.progression_status, "blocked");
  assert.deepEqual(Object.keys(projection.open_findings), ["F1"]);
  assert.deepEqual(projection.artifacts, {});
  assert.deepEqual(projection.reviews, {});
  assert.deepEqual(projection.remaining_work, {});
});

test("skill context includes only selected current identities and exact required paths", () => {
  const projection = projectCompactSnapshot(snapshot, "skill-context", {
    artifactIds: ["spec"],
    reviewTargetIds: ["M1"],
    findingIds: ["F1"],
    remainingWorkIds: ["W1"],
    requiredPaths: ["specs/example.md", "docs/changes/example/reviews/code-review-M1.md"],
    requestedOperation: "route-correction",
    request: { payload: { correction: { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Focused proof passes", expected_review_target: "M1" } } },
  });
  assert.deepEqual(Object.keys(projection.artifacts), ["spec"]);
  assert.deepEqual(Object.keys(projection.reviews), ["M1"]);
  assert.deepEqual(Object.keys(projection.open_findings), ["F1"]);
  assert.deepEqual(Object.keys(projection.remaining_work), ["W1"]);
  assert.deepEqual(projection.required_paths, ["docs/changes/example/reviews/code-review-M1.md", "specs/example.md"]);
  assert.equal(projection.progression_status, "blocked");
  assert.equal(projection.operation_eligibility.status, "permitted");
  assert.ok(projection.permitted_operations.includes("route-correction"));
});

test("omitting an exact requested operation yields null eligibility fields", () => {
  const projection = projectCompactSnapshot(snapshot, "summary");
  assert.equal(projection.requested_operation, null);
  assert.equal(projection.operation_eligibility, null);
});

test("procedural history cannot change an equal current-state projection", () => {
  const left = { ...snapshot, procedural_history: Array.from({ length: 2 }, (_, i) => ({ i })) };
  const right = { ...snapshot, procedural_history: Array.from({ length: 2000 }, (_, i) => ({ i })) };
  assert.deepEqual(projectCompactSnapshot(left, "summary"), projectCompactSnapshot(right, "summary"));
});

test("unknown projection views fail closed", () => {
  assert.throws(() => projectCompactSnapshot(snapshot, "history"), /ProjectionView: unknown_value history/);
});

test("projection identities fail closed when missing or invalid", () => {
  assert.throws(() => projectCompactSnapshot({ ...snapshot, change_id: undefined }, "summary"), /change_id must be an Id/);
  assert.throws(() => projectCompactSnapshot({ ...snapshot, lifecycle_contract: "history-v1" }, "summary"), /lifecycle_contract: unknown_value/);
  assert.throws(() => projectCompactSnapshot({ ...snapshot, lifecycle_revision: "latest" }, "summary"), /lifecycle_revision must be a Digest/);
});
