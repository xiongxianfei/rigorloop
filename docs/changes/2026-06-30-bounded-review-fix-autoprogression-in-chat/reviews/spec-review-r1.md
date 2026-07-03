# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/review-fix-autoprogression.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SR-RFA-1, SR-RFA-2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r1.md
- Review log: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-log.md
- Review resolution: docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/review-resolution.md
- Open blockers: SR-RFA-1, SR-RFA-2
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: material spec findings require revision before architecture, planning, or test-spec reliance

## Findings

## Finding SR-RFA-1

Finding ID: SR-RFA-1
Severity: major
Location: specs/review-fix-autoprogression.md, requirements R4-R11 and R39-R40
Evidence: R4 says review-fix authorization is persisted under `workflow.autoprogression.review_fix`, R6 defines profile statuses, R9 lists state fields, and R10 preserves direct review isolation. The spec does not define the activation gate for `$workflow auto: <target-stage>` beyond Example E2's non-normative phrase "proposal gate is clean." Existing workflow contracts define activation gates explicitly: `authoring-through-plan-review` activates only when the profile is armed and the proposal gate passes, and proposal gate readiness is separate from user authorization.
Required outcome: Add normative activation and persistence requirements for review-fix autoprogression. The spec must say when `$workflow auto: <target-stage>` may create armed state, when armed state may become active, what proposal/spec/review evidence is required before the first downstream stage, how direct review invocations interact with already armed state, and how `off`, `paused`, `completed`, and `cancelled` are represented or cleared.
Safe resolution path: Add requirements after R9 along these lines: review-fix activation requires durable user authorization plus a clean current gate for the current stage; proposal-start activation requires accepted proposal and approved recorded proposal-review with no open findings; direct review invocations do not activate or resume the profile even when state exists; unknown or contradictory persisted state pauses; cancellation/off/completed transitions update `workflow.autoprogression.review_fix` deterministically in `change.yaml` or the approved fallback policy surface.
needs-decision rationale: none

## Finding SR-RFA-2

Finding ID: SR-RFA-2
Severity: major
Location: specs/review-fix-autoprogression.md, requirements R11, R14-R15, R20-R22, R39, and edge case EC5
Evidence: R11 includes `architecture when required -> architecture-review when required`, but no requirement records how that decision is made. R14 says preflight resolves the next transition, but does not require the recorded architecture assessment used by the existing workflow contract. EC5 says `architecture` as target stage may be "not reached because the architecture assessment did not require it," but R21 says the driver stops when the target stage is reached and R22 says it cannot continue past the target stage. That leaves target-stage behavior ambiguous when a conditional target is not applicable.
Required outcome: Define recorded architecture assessment and conditional-target behavior normatively. The spec must require an architecture assessment after approved `spec-review` before routing to `architecture`, `architecture-review`, or `plan`; define the closed assessment values; define that `architecture-ambiguous` stops; and define what happens when the requested target stage is conditional and the assessment says it is not required.
Safe resolution path: Add requirements stating that after approved recorded `spec-review`, the driver records exactly one architecture assessment value: `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`. `architecture-required` routes through `architecture` and `architecture-review`; `architecture-not-required` skips those conditional stages and continues toward the next applicable target only if doing so does not exceed the user's target intent; if the requested target is the skipped conditional stage, stop with a `target-not-applicable` terminal or paused reason rather than claiming the target was reached. `architecture-ambiguous` stops for owner decision.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most requirements are testable, but activation and conditional architecture routing need explicit normative behavior. |
| normative language | concern | Important gate behavior appears only in examples or is implied by existing workflow contracts. |
| completeness | concern | The spec covers command, state, budgets, and auto-safe rules, but misses precise activation and architecture-assessment routing. |
| testability | concern | Tests can cover most rules, but cannot deterministically assert conditional target handling without the missing contract. |
| examples | pass | Examples cover isolation, arming, safe fix, owner stop, budget stop, and stale review. |
| compatibility | pass | Existing profile behavior is explicitly preserved. |
| observability | pass | Chat and durable evidence outputs are named. |
| security/privacy | pass | Network, publication, release, destructive, credential, and external-state operations are excluded. |
| non-goals | pass | The no-dry-run and no-implementation boundaries match the accepted proposal. |
| acceptance criteria | concern | Acceptance criteria should add activation-gate and architecture-assessment checks after the spec revision. |

## Exact Suggested Spec Edits

- Add requirements for review-fix activation gate and state transitions after R9.
- Add requirements for recorded architecture assessment after approved `spec-review`.
- Add a closed stop reason for conditional targets that are not applicable, such as `target-not-applicable`.
- Add acceptance criteria covering activation gate, direct-review-with-armed-state isolation, architecture-required routing, architecture-not-required routing, architecture-ambiguous stop, and conditional target not applicable.

## Recommendation

Recommendation: changes-requested. Revise the spec for SR-RFA-1 and SR-RFA-2, then rerun spec-review. This direct spec-review is isolated and does not automatically continue into architecture or plan.
