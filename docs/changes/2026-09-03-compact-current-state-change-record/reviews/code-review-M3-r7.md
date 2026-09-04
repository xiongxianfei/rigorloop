# Code Review M3 R7: Typed pending-milestone selection

Review ID: code-review-m3-r7
Stage: code-review
Round: r7
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation and bounded CLI implementation against Design Review R11 and Delivery Review R8
Reviewed milestone: M3
Review date: 2026-09-04
Status: approved
Review status: approved
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: none at the M3 review layer
- Next stage: milestone settlement through Workflow
- Review status: approved
- Material findings: none
- Recording status: recorded
- Review record: `reviews/code-review-M3-r7.md`
- Reviewed milestone: M3
- Milestone closeout: pending lifecycle settlement
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review judgment

The SR-46 delta is coherent across the executable contract, published JSON Schema, eligibility derivation, pure evaluator, and focused tests. `RemainingWork.kind` distinguishes selectable milestones from tasks. With no active work, only an exact pending entry owned by `implement` may take the `null` to `planned` transition; the evaluator removes that entry and constructs the active milestone itself. Existing active milestones retain only the approved adjacent transitions, and closure clears active work rather than persisting a closed active record.

The new tests prove exact selection among multiple pending milestones, missing, blocked, wrong-kind, and wrong-owner rejection without mutation, stale replay rejection, and reviewed closure. The normal request path still validates the complete expected authoritative set before semantic evaluation, and all public transports continue to use the same evaluator and transaction adapter.

No caller permission claim, Git or pull-request dependency, plan-prose parsing, additional writer path, or compatibility migration was introduced.

## Checklist

| Area | Result | Evidence |
| --- | --- | --- |
| R6 correction | pass | The first or next milestone is selected from typed current `remaining_work` through an exact bounded operation. |
| Schema and vocabulary | pass | JavaScript and JSON Schema require `kind`, allow only the reviewed nullable activation input, and reject closed active milestone state. |
| State mutation | pass | Selection removes exactly one entry and derives active work; invalid requests leave the input set unchanged; closure clears active work. |
| Retry and ambiguity | pass | The milestone ID selects one exact mapping entry, multiple pending entries remain independently selectable, and replay against the changed revision is stale. |
| Validation | pass | 32 focused tests and 455 package tests pass; lifecycle, result-measurement, governed-validation, package, and diff checks pass. |

## No-Finding Statement

Clean formal Code Review completed with no material findings against the exact M3 R7 implementation and evidence.

## Independence statement

This review did not edit implementation, tests, schemas, plan, Design artifacts, implementation evidence, or workflow routing state.
