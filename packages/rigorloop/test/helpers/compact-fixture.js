import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

import { compactLifecycleRevision } from "../../dist/lib/compact-contract.js";
import { serializeLifecycleYaml } from "../../dist/lib/lifecycle-contract.js";

export const compactHash = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;

export function writeCompactFixture(root, changeId = "example") {
  const changePath = `docs/changes/${changeId}/change.yaml`;
  const reviewPath = `docs/changes/${changeId}/reviews/code-review-M1.md`;
  const finding = { finding_id: "F1", affected_surfaces: ["implementation"], severity: "major", blocking_effect: "blocks-progression", owner: "implement", required_next_action: "Correct it", disposition: "open", evidence: "Focused failure" };
  const reviewRecord = { schema: "compact-review-v1", review_id: "review-1", target: { target_id: "M1", target_kind: "milestone" }, round: 1, subjects: {}, reviewer_authority: "code-review", outcome: "changes-requested", recording_status: "recorded", open_findings: { F1: finding }, material_decisions: [], limitations: [], recorded_at: "2026-09-04T00:00:00Z" };
  const review = `---\n${serializeLifecycleYaml(reviewRecord)}---\n\n# Current review\n`;
  const change = { schema: "compact-change-v1", change_id: changeId, title: "Example", lifecycle_contract: "compact-current-state-v1", lifecycle_revision: `sha256:${"0".repeat(64)}`, current_stage: "code-review", artifacts: {}, reviews: { M1: { target_id: "M1", path: reviewPath, identity: compactHash(review), review_id: "review-1", outcome: "changes-requested", reviewer_authority: "code-review", status: "current" } }, active_work: null, open_findings: { F1: { finding_id: "F1", review_target_id: "M1", review_path: reviewPath, review_identity: compactHash(review), owner: "implement", severity: "major", blocking_effect: "blocks-progression" } }, material_decisions: {}, evidence: {}, blockers: [], remaining_work: {}, readiness: "blocked" };
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(change), files: { [reviewPath]: review } }).revision;
  mkdirSync(join(root, `docs/changes/${changeId}/reviews`), { recursive: true });
  writeFileSync(join(root, reviewPath), review);
  writeFileSync(join(root, changePath), serializeLifecycleYaml(change));
  return { change, changePath, reviewPath, files: { [changePath]: Buffer.from(serializeLifecycleYaml(change)), [reviewPath]: Buffer.from(review) } };
}

export function correctionRequest(fixture) {
  return { schema: "compact-operation-v1", operation: "route-correction", change_id: fixture.change.change_id, expected_lifecycle_revision: fixture.change.lifecycle_revision, expected_files: Object.fromEntries(Object.entries(fixture.files).sort(([a], [b]) => a.localeCompare(b)).map(([path, bytes]) => [path, { path, state: "present", identity: compactHash(bytes) }])), payload: { correction: { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Focused proof passes", expected_review_target: "M1" } } };
}
