# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Target: specs/single-bounded-review-fix-workflow-automation.md
Reviewed artifact: specs/single-bounded-review-fix-workflow-automation.md
Review date: 2026-07-21
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `BRF-SR6`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r2.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: the cross-spec disposition ledger cannot identify every source requirement uniquely and still uses an open-ended default
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: repair the source identifier collision, make every disposition explicit, and record an approving same-stage rereview before architecture relies on the contract

## Review Invocation Manifest

- Manifest owner: workflow orchestrator
- Review ID: `spec-review-r2`
- Review stage: `spec-review`
- Review target: `specs/single-bounded-review-fix-workflow-automation.md@sha256:9337a03f4446eeb8f785fcd096d3add353d0efdd6997b26a230e4670d29e9126`
- Context separation mechanism: tracked-artifact and governing-source reset
- Reviewer context ID: `/root/spec-review-r2`
- Risk tier: elevated
- Risk-tier triggers: cross-spec precedence, durable authorization, migration compatibility, and long-lived workflow state
- Formal criteria: spec-review dimensions and `BRF-SR1` through `BRF-SR5`
- Initial packet inventory: accepted proposal, revised spec, spec-review R1, four affected legacy specs, `CONSTITUTION.md`, and `docs/workflows.md`, each read from the tracked workspace and content-hashed before review
- Prompt template version: `spec-review-result-skeleton-v1`
- Phase receipts: tracked artifact reset; R1 finding recheck; closed-contract audit; verdict recorded

## Review Inputs

- Spec: `specs/single-bounded-review-fix-workflow-automation.md`
- Accepted proposal: `docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md`
- Prior review: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r1.md`
- Governing contracts: `CONSTITUTION.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/review-fix-autoprogression.md`, `specs/review-finding-resolution-contract.md`
- Operating context: `docs/workflows.md`, `AGENTS.md`

## Findings

## Finding BRF-SR6

Finding ID: BRF-SR6
Severity: major
Location: `Compatibility and migration / Cross-spec disposition contract`; `specs/workflow-stage-autoprogression.md` requirements at lines 278 and 425
Evidence: The revised spec promises exact, machine-testable one-requirement/one-disposition precedence, but `specs/workflow-stage-autoprogression.md` contains two different requirements with the same stable ID `R2ba`: one says standard execution-flow autoprogression begins at `implement` and continues through `pr`, while the other defines durable test-spec settlement identities. The disposition ledger has no way to identify those source requirements separately. It also says unlisted requirements are `preserved-unchanged`, even though the contract states that open-ended prose cannot establish precedence. A static check therefore cannot prove that every affected requirement has exactly one disposition or determine whether an omitted requirement was intentionally preserved.
Required outcome: Every source requirement and acceptance surface covered by the cross-spec amendment has a unique stable selector and exactly one explicit disposition, with no wildcard or unlisted-item default serving as normative precedence.
Safe resolution path: Assign one of the duplicate `R2ba` requirements a new repository-valid stable ID and update every reference to it. Replace the unlisted-requirement default with an explicit inventory of the remaining preserved-unchanged requirement IDs and exact non-requirement selectors for all four affected specs, or narrow the normative ledger to an explicitly enumerated affected-selector registry whose completeness is statically checkable. Add source-selector uniqueness to `BRF-R098e` and the required proof matrix.
needs-decision rationale: none; unique source identifiers and explicit dispositions are prerequisites of the already selected machine-checkable precedence design.

## R1 Finding Rereview

| Finding | Result | Evidence |
| --- | --- | --- |
| `BRF-SR1` | resolved | `BRF-R017a` through `BRF-R017f` define one occurrence kind per public target, unique active-plan milestone binding before persistence, exact failure behavior, and no rebinding on resume. |
| `BRF-SR2` | resolved | `BRF-R008a` through `BRF-R008j` define separate closed run, parent, capability, and capability-kind vocabularies plus legal transitions, terminality, and single-use authority. |
| `BRF-SR3` | resolved | `BRF-R043a` through `BRF-R043e` permit an early final target but prohibit future-contingent verification authorization and require a boundary pause. |
| `BRF-SR4` | resolved | `BRF-R005` and `BRF-R098a` through `BRF-R098d` make migration-window aliases mandatory and map plan-review, verify, status, off, and unknown forms without legacy writes. |
| `BRF-SR5` | not resolved | The revision adds substantial exact mappings and conditional legacy-spec amendments, but duplicate source ID `R2ba` and the open-ended unlisted-item default prevent exhaustive machine-checkable precedence. |

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | Target binding, state ownership, authorization timing, cancellation, and adapter behavior are now explicit. |
| normative language | concern | The unlisted-requirement default conflicts with the adjacent prohibition on open-ended precedence. |
| completeness | block | Cross-spec precedence cannot uniquely address both source requirements named `R2ba`. |
| testability | block | A uniqueness/completeness validator cannot distinguish the duplicate source IDs or prove that default-preserved requirements were intentionally classified. |
| examples | pass | New examples cover repeated-stage binding, cancellation, early verify target selection, and the legacy verify adapter. |
| compatibility | block | The compatibility direction is correct, but its same-rank precedence ledger is not yet mechanically exhaustive. |
| observability | pass | Run, authority, capability, receipt, gate, pause, and next-action reporting are observable. |
| security/privacy | pass | Risk classes remain separate, future-contingent verification consent is forbidden, and external actions remain prohibited. |
| non-goals | pass | The revision remains scoped to the single mechanism and does not expand external or background authority. |
| acceptance criteria | concern | The new criteria are comprehensive, but `AC-BRF-SR5-1` and `AC-BRF-SR5-4` cannot pass until source selectors are unique and exhaustive. |

## Recommendation

The revised contract resolves `BRF-SR1` through `BRF-SR4` and materially improves `BRF-SR5`, but it is not ready for architecture. Repair the exact-selector contract, then run `spec-review-r3`. No downstream handoff occurs from this changes-requested review.
