import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";

async function fixture(m2State = "planned", reviewStatus = "not-started") {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-milestone-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  writeFileSync(join(changeRoot, "evidence", "m2.md"), "Milestone: M2\nValidation result: passed\n", "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states: {}
workflow_state:
  lifecycle_state: active
  current_stage: implement
  next_stage: implement
  blocker: null
  evidence: []
  planned_work:
    current_milestone: M2
    milestones:
      M1:
        kind: implementation
        state: closed
      M2:
        kind: implementation
        state: ${m2State}
      M3:
        kind: implementation
        state: planned
    remaining_implementation_milestones:
      - M2
      - M3
    latest_review:
      status: ${reviewStatus}
      stage: code-review
      round: r1
      artifact_id: plan
      occurrence: milestone
      milestone_id: M2
      evidence: []
    final_closeout:
      readiness: not-ready
      reasons:
        - lifecycle-gates-open
      evidence: []
`, "utf8");
  return { root, changeRoot };
}

function revision(root) { return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision; }
function request(root, name, body) { const path = `requests/${name}.json`; writeFileSync(join(root, path), JSON.stringify(body), "utf8"); return path; }

test("start milestone enforces current selection and predecessor order", async () => {
  const { root, changeRoot } = await fixture();
  const path = request(root, "start", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["start-milestone", "--request", path], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /M2:\n\s+kind: implementation\n\s+state: implementing/);
  const wrong = request(root, "wrong", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M3", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["start-milestone", "--request", wrong], { cwd: root }).result.errors[0].code, "RL_MILESTONE_ORDER");
});

test("complete milestone requires matching review and proof", async () => {
  const { root, changeRoot } = await fixture("review-requested", "approved");
  const path = request(root, "complete", { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", evidence_path: "docs/changes/example/evidence/m2.md", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root }).exitCode, 0);
  const changed = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(changed, /M2:\n\s+kind: implementation\n\s+state: closed/);
  assert.doesNotMatch(changed, /remaining_implementation_milestones:\n\s+- M2/);
  assert.match(changed, /current_milestone: M3/);
  assert.match(changed, /current_stage: implement/);
});
