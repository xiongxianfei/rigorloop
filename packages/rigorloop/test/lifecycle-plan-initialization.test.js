import assert from "node:assert/strict";
import { test } from "node:test";

import { validateLifecycleRequest } from "../dist/lib/lifecycle-contract.js";

test("retired plan-review cannot initialize planned work", () => {
  const review = validateLifecycleRequest({
    schema_version: 1,
    operation: "record-review",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    artifact_id: "plan",
    evidence_path: "docs/changes/example/reviews/plan-review-r1.md",
    stage_authority: "plan-review",
  });

  assert.equal(review.ok, false);
  assert.equal(review.errors[0].code, "RL_INVALID_REQUEST");
  assert.match(review.errors[0].summary, /stage_authority/);
});
