# Code Review M3 R6: Multi-milestone lifecycle completeness

Review ID: code-review-m3-r6
Stage: code-review
Round: r6
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 compact semantic-operation and bounded CLI implementation against Design Review R9 and Delivery Review R6
Reviewed artifact: M3 compact semantic-operation and bounded CLI implementation against Design Review R9 and Delivery Review R6
Reviewed milestone: M3
Review date: 2026-09-04
Status: changes-requested
Review status: changes-requested
Material findings: CCSR-M3-CR7
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: CCSR-M3-CR7
- Next stage: review-resolution and specification correction
- Review status: changes-requested
- Material findings: CCSR-M3-CR7
- Recording status: recorded
- Review record: `reviews/code-review-M3-r6.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CCSR-M3-CR7
- Verify readiness: not-claimed

## Finding CCSR-M3-CR7

Finding ID: CCSR-M3-CR7
- Severity: major
- Location: `specs/compact-current-state-change-record.md:215`, `specs/compact-current-state-change-record.md:220`, `specs/compact-current-state-change-record.md:253`, `specs/compact-current-state-change-record.md:274`, and `packages/rigorloop/dist/lib/compact-operations.js` milestone handling
- Evidence: The approved schema represents at most one active milestone, and `advance-milestone` requires that exact milestone already be active. Closing it sets `active_work` to null. `RemainingWork` has no milestone kind or activation semantics, and no operation can select the first or next planned milestone from current state. A multi-milestone change therefore cannot progress after closure without an undeclared caller-constructed coordinator or implementation-specific plan parsing. This is not safely repairable inside M3 because Design R9 does not define the semantic input, eligibility predicate, remaining-work update, or resulting current stage.
- Required outcome: Define one bounded current-state operation that selects an exact pending implementation milestone when no work is active, derives an `ActiveMilestone`, and prevents ambiguous, blocked, missing, or non-implementation work from being selected. Define how the selected item leaves `remaining_work`, how closure exposes the next selection or downstream gate, and how retry/identity semantics remain exact without Git, PR, logs, or plan-prose reconstruction.
- Safe resolution path: Route to Specification, adopt a minimal activation branch within `advance-milestone` or another explicitly reviewed operation, align schemas and architecture, obtain fresh Design and Delivery Review, then implement test-first and repeat holistic M3 review.
- needs-decision rationale: The owning Design stage must choose the exact activation schema and state transition; current approved requirements do not imply one interoperable encoding.

## Checklist

| Area | Result | Evidence |
| --- | --- | --- |
| R5 correction | pass | Exact gate, correction, decision, evidence, stable-path, artifact-settlement, and Verify predicates now have direct positive and negative proof. |
| Multi-milestone behavior | block | No approved current-state transition can create the first or next `ActiveMilestone`. |
| Failure safety | pass | Unsupported selection currently fails closed instead of inventing state. |
| Compatibility and trust boundary | pass | No Git, PR, network, log, or caller-permission dependency exists. |
| Validation evidence | pass-with-scope-limit | 29 focused tests and 452 package tests pass, but none can prove an operation absent from the approved contract. |

## Handoff

Route CCSR-M3-CR7 to Specification as a technical-realization gap. M3 must remain open until the corrected Design and Delivery packages are approved and the exact activation transition is implemented and rereviewed.
