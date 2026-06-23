# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/single-source-of-workflow-state.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: WSS-SR1, WSS-SR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-log.md`
- Review resolution: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`
- Open blockers: WSS-SR1, WSS-SR2
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Resolve WSS-SR1 and WSS-SR2 before architecture, plan, test-spec, or implementation reliance.

`Immediate next stage` is the routing field; allowed values exclude `test-spec`.
Use `Eventual test-spec readiness` to assess whether test-spec authoring will
be possible after required routing stages.

## Findings

## Finding WSS-SR1

Finding ID: WSS-SR1
Severity: blocking
Location: `specs/single-source-of-workflow-state.md` R43, R47, R49, R50; lines 188, 196-202.
Evidence: R43 requires exact parseable `Current Handoff Summary` fields. R47 says `Review status` must use a "spec-defined enum-like value" but only says it must distinguish "at least" six states. R49 says final-closeout reason must start with a "spec-defined reason code", and R50 again lists only "at least" seven categories. The spec does not define the closed syntax or allowed values that validators and tests must accept or reject.
Required outcome: Define exact allowed values and parseable syntax for `Review status` and final-closeout reason codes, including how review stage and round are represented when present.
Safe resolution path: Add a normative table or requirements that enumerate the closed `Review status` statuses, allowed review-stage values, allowed round token shape or `none`, and the closed final-closeout reason-code vocabulary. Update examples and acceptance criteria so valid and invalid bounded owner-field fixtures are deterministic.
needs-decision rationale: none

## Finding WSS-SR2

Finding ID: WSS-SR2
Severity: major
Location: `specs/single-source-of-workflow-state.md` R53-R55, Inputs and outputs, Acceptance criteria; lines 208-212, 282-303, 456.
Evidence: R53 requires `docs/plan.md` projection columns `Plan`, `State`, `Next stage`, and `Change ID`. R55 requires those rows to match the active plan owner for lifecycle state, next stage, and change ID. The spec defines `Current Handoff Summary` as the owner for next stage but does not identify the owner or parse source for `Change ID`, and "lifecycle state" can mean the active/blocked index section, the active plan `Plan lifecycle state`, or another plan-body status field.
Required outcome: Define the authoritative source for each `docs/plan.md` projection cell, especially `State` and `Change ID`.
Safe resolution path: Add a projection-source table that maps `Plan` to the plan path/title, `State` to the plan body's `Plan lifecycle state` or the index section value, `Next stage` to `Current Handoff Summary`, and `Change ID` to an exact plan-body field, source artifact entry, or change metadata path. Update R53-R55 and acceptance criteria so validators do not infer these sources.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | Parser-critical enum fields and `docs/plan.md` projection sources are underspecified. |
| normative language | concern | The new requirements are mostly testable, but R47/R49/R50 use `MUST` around values the spec does not actually define. |
| completeness | concern | The spec covers the proposal direction but leaves two deterministic validation inputs unresolved. |
| testability | block | Tests would have to guess accepted owner-field enum values and projection sources for `State` and `Change ID`. |
| examples | concern | Examples cover important state-sync flows but do not show valid `Review status`, final-closeout reason-code, or full plan-index table rows. |
| compatibility | pass | Historical plans, ledgers, reopened archived plans, and existing workflow-stage order are handled. |
| observability | pass | Required diagnostics include paths, owner values, projection mismatches, and stale-token details. |
| security/privacy | pass | The contract does not introduce secrets, hosted state, or external service dependencies. |
| non-goals | pass | Non-goals preserve workflow order, verify/PR ownership, historical records, and no hosted control plane. |
| acceptance criteria | concern | Acceptance criteria include the major behaviors but need exact enum and projection-source checks after revision. |

## Eventual test-spec readiness

not-ready

The amended spec is close, but test-spec authoring would need to guess closed owner-field values and projection source ownership.

## Stop condition

Material findings WSS-SR1 and WSS-SR2 require spec revision before architecture, plan, test-spec, or implementation reliance.

## Recommended spec edits

- Add exact enum/syntax tables for `Review status` and final-closeout reason codes.
- Add a `docs/plan.md` projection-source table for `Plan`, `State`, `Next stage`, and `Change ID`.
- Add examples or acceptance criteria that exercise valid and invalid owner-field enum values and plan-index projection cells.

## No-finding statement

Not applicable. This review recorded material findings.
