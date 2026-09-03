# Final Holistic Code Review R3: Refocus Workflow into Route

Review ID: code-review-final-r3
Stage: code-review
Round: r3
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: correction range a7168698..3613ef03 and complete branch
Reviewed artifact: final-review mutation guard correction through 3613ef038bce333d798cd20faf5b34686d0fc932
Reviewed milestone: final holistic cross-milestone review
Reviewed occurrence: final
Reviewed revision: 3613ef038bce333d798cd20faf5b34686d0fc932
Review date: 2026-09-03
Status: changes-requested
Review status: changes-requested
Material findings: RFR-FINAL-CR3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r3.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`
- Open blockers: RFR-FINAL-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-FINAL-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-final-r3.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: final
- Milestone closeout: all implementation milestones closed; final review correction required
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: RFR-FINAL-CR3
- Verify readiness: not-claimed

## Review inputs

- Actual correction diff: `a7168698..3613ef03`, plus the complete branch for interaction checks.
- Approved Design and Delivery packages: `design-review-r1` and `delivery-review-r1` remain current.
- Correction evidence: `evidence/final-r2-mutation-guard-correction.md`.
- Validation evidence: 95 focused lifecycle tests; 373 package tests with 2 historical skips; 107 change-metadata tests; 111 review-artifact-validator tests; `git diff --check`.

## Findings

### Finding RFR-FINAL-CR3

Finding ID: RFR-FINAL-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-read.js:153`; `packages/rigorloop/dist/lib/lifecycle-read.js:298`
Evidence: The planned-work sentinel is the string `none`, but `activeMilestone()` returns it unchanged. The final-review advertisement checks `!milestone`, which is false for that truthy string. Live exact-change context therefore reports no blockers but offers only `route-correction`; it omits the implemented `record-final-review` operation that route needs to progress this first v3 change.
Required outcome: Normalize `current_milestone: none` to no active milestone in the read model and directly prove that a closed final implementation set advertises `record-final-review` before receipt registration.
Safe resolution path: Change only the existing `activeMilestone()` helper and add one focused assertion to the final-review lifecycle test.
needs-decision rationale: none; the operation and advertisement behavior were already approved by RFR-FINAL-CR1.

## Resolution of R2

RFR-FINAL-CR2 is resolved. `record-final-review` now rejects the complete review log when any occurrence reports an open finding, and final stage completion repeats that check against the identity-bound log. The milestone-free exception now requires the exact implementation-defect route, every implementation milestone closed, and an empty remaining-work projection. Direct negative tests prove unrelated open findings, ordinary reasons, and contradictory remaining work cannot mutate lifecycle state.

## Review conclusion

The mutation guards are correct, but route cannot discover the final-review registration operation because the read model does not normalize its existing `none` sentinel. Verify remains blocked pending the narrow correction and R4.
