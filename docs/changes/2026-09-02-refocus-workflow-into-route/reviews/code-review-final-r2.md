# Final Holistic Code Review R2: Refocus Workflow into Route

Review ID: code-review-final-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: correction range 7609dd9f..60049128 and complete branch
Reviewed artifact: final-review lifecycle correction through 600491280ae861f01d3af8d85124dc9345febe10
Reviewed milestone: final holistic cross-milestone review
Reviewed occurrence: final
Reviewed revision: 600491280ae861f01d3af8d85124dc9345febe10
Review date: 2026-09-03
Status: changes-requested
Review status: changes-requested
Material findings: RFR-FINAL-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r2.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`
- Open blockers: RFR-FINAL-CR2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-FINAL-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r2.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: final
- Milestone closeout: all implementation milestones closed; final review correction required
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: RFR-FINAL-CR2
- Verify readiness: not-claimed

## Review inputs

- Actual correction diff: `7609dd9f..60049128`, plus the complete branch for interaction checks.
- Approved Design and Delivery packages: `design-review-r1` and `delivery-review-r1` remain current.
- Final review correction evidence: `evidence/final-r1-lifecycle-correction.md`.
- Validation evidence: 93 focused lifecycle tests, 371 package tests with 2 historical skips, 107 metadata-validator tests, 111 review-artifact-validator tests, explicit lifecycle validation, and `git diff --check` passed.

## Resolution of R1

RFR-FINAL-CR1 is resolved. The implementation adds an identity-bound `record-final-review` operation, consumes its current evidence and log hashes for `code-review -> verify`, supports idempotent replay, rejects stale or non-clean evidence, and permits a final implementation correction without fabricating a milestone.

## Finding RFR-FINAL-CR2

Finding ID: RFR-FINAL-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-operations.js:401`; `packages/rigorloop/dist/lib/lifecycle-operations.js:533`; `packages/rigorloop/dist/lib/lifecycle-operations.js:560`; `packages/rigorloop/dist/lib/lifecycle-stage-routing.js:29`
Evidence: `record-final-review` validates only its selected review-log occurrence, so a clean occurrence can be registered while the log's global `Open findings` set still names another unresolved material finding. The final correction exemption is also selected by source stage plus `current_milestone: none`; an ordinary correction reason can therefore reach `implement` without a milestone, and the evaluator does not require all implementation milestones to be closed with an empty remaining projection. These are direct mutation paths, so read-side permitted-operation filtering is not an authority boundary.
Required outcome: Reject final-review registration and final-stage advancement while any review-log finding remains globally open. Permit a milestone-free final Code Review correction only for `implementation-defect -> implement -> code-review` when every implementation milestone is closed and the remaining implementation projection is empty. Add direct negative regression tests for an unrelated open finding, an ordinary correction reason without a milestone, and contradictory remaining-work state.
Safe resolution path: Add one shared fail-closed open-finding check for final receipt/advance and narrow the existing final correction predicate; do not introduce another operation, artifact, or lifecycle state.
needs-decision rationale: none; this only enforces the authority boundary already approved for RFR-FINAL-CR1.

## Review conclusion

The original deadlock is fixed, but the direct mutation evaluator needs the two narrow fail-closed checks above before final review authority is safe. Verify remains blocked pending R3.
