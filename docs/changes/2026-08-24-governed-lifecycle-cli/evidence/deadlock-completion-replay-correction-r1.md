# Milestone Completion and Replay Correction Evidence

Change ID: 2026-08-24-governed-lifecycle-cli
Implementation scope: isolated post-close correction for `RLCLI-DEADLOCK-CR1` and `RLCLI-DEADLOCK-CR2`
Implementation status: complete

## Delivered

- `complete-milestone` now closes only the reviewed milestone, advances the planned-work cursor, resets `latest_review`, and reports structural continuation eligibility without changing workflow-stage projections.
- A separate workflow-authorized `start-milestone` marks the selected successor implementing and atomically synchronizes `workflow_state.current_stage`, `workflow_state.next_stage`, and an active `workflow.automation.current_stage`.
- Contradictory active automation state fails without lifecycle mutation.
- Direct review consumption stores a versioned normalized completion record and fingerprint covering milestone proof, review receipt, canonical review-log occurrence, complete packet inventory, normalized review facts, milestone identity, and workflow authority.
- Closed replay rereads every recorded constituent. Omitted review evidence, receipt drift, canonical-entry drift, milestone-proof drift, non-proof packet drift, and authority conflicts return `RL_STALE_EVIDENCE` without lifecycle mutation.
- Pre-projected reviews are reconstructed from their exact referenced review record and stored with the same complete normalized evidence identity as directly supplied reviews.
- Canonical review-log lookup requires exactly one matching prose or table occurrence; duplicate authorizing occurrences reject before mutation.
- Milestone start and completion validate the exact remaining-implementation projection, and completion accepts only the legal `review-requested -> closed` source transition.
- Matching legacy completion registrations upgrade deterministically without changing routing; subsequent exact replay returns `already-recorded`.

## Changed implementation

- `packages/rigorloop/dist/lib/lifecycle-operations.js`
- `packages/rigorloop/test/lifecycle-milestone.test.js`

## Validation

- `node --test packages/rigorloop/test/lifecycle-milestone.test.js`: passed, 13 tests.
- `node --test packages/rigorloop/test/lifecycle-*.test.js`: passed, 74 tests.
- `npm test --prefix packages/rigorloop`: passed, 256 tests.
- `git diff --check`: passed.
- Cross-milestone C09 was attempted before finding closeout. Its artifact-lifecycle portion ran 170 tests and reported six failures caused by the expected temporary mismatch between the two still-open review findings and `review.unresolved_items`; the focused implementation behavior did not fail. C09 must be rerun after resolution evidence closes the findings.

## Recovery and compatibility

All new failure paths are evaluated before transaction persistence, so rejected requests retain byte-identical lifecycle state. Existing closed registrations without the new fingerprint can be upgraded only by re-presenting matching current proof and, where originally recorded, the matching review receipt. The upgrade changes evidence registration only and never repairs or selects workflow routing implicitly.
