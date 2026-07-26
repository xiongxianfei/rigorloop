# Boundary-First Proof Modeling Spec Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: Codex spec-review skill with context-separated reviewer
Target: commit `67a3cab2` against `5aba328c`
Reviewed artifact: specs/rigorloop-workflow.md; specs/skill-contract.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR3-1, BFP-SR3-2, BFP-SR3-3
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact two-spec diff; accepted proposal; prior approved boundary clauses; M1 code-review findings; approved architecture; matching test specs
Manifest owner: workflow orchestrator

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: BFP-SR3-1, BFP-SR3-2, BFP-SR3-3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r3.md`
- Review log: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md`
- Review resolution: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md#spec-review-r3`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: implementation remains blocked until all three contracts are deterministic and spec-review approves them

## Findings

### BFP-SR3-1: Incident replay is not independently derivable

Finding ID: BFP-SR3-1
- Severity: blocking
- Location: `specs/rigorloop-workflow.md` R28x; `specs/skill-contract.md` R56o
- Evidence: The fixture has no contrast identity, omission prose is not mapped to one triggering field/value, and diagnostic families have no closed vocabulary or equality rule. The evaluator must invent the mappings it is required to derive.
- Required outcome: Freeze each omission's triggering field/value, valid contrast, first detecting stage, and diagnostic family.
- Safe resolution path: Add an exact rule table, contrast linkage, single triggering values, closed diagnostic IDs, and tests proving expected labels cannot control derived results.
- needs-decision rationale: none

### BFP-SR3-2: Simple-change observations are not computable

Finding ID: BFP-SR3-2
- Severity: blocking
- Location: `specs/rigorloop-workflow.md` R28y; `specs/skill-contract.md` R56p
- Evidence: The amendment names trace properties but does not close the trace fields, identity/linkage invariants, outcomes, correction semantics, repository inventory, or metric formulas.
- Required outcome: Define one closed four-stage trace and deterministic derivation rules for every reported observation.
- Safe resolution path: Specify exact records, ordered linkage, outcome and diagnostic vocabularies, correction events, output inventory, formulas, and malformed/substituted/multi-correction contrasts.
- needs-decision rationale: none

### BFP-SR3-3: Current hashes can authenticate unrelated evidence

Finding ID: BFP-SR3-3
- Severity: blocking
- Location: `specs/rigorloop-workflow.md` R28y
- Evidence: Any current tracked or change-local regular file can satisfy any row because the reference is not bound to the evaluated check/fixture, result, or diagnostic.
- Required outcome: Every pass/fail evidence record must bind the cited bytes to the exact evaluated operation and outcome.
- Safe resolution path: Define a validated row-scoped receipt with operation identity, result, diagnostic, artifact reference, and receipt identity; reject arbitrary-file and cross-row substitution.
- needs-decision rationale: none

## Review Dimensions

| Dimension | Verdict | Evidence |
| --- | --- | --- |
| requirement clarity | block | Three executable mappings remain implicit. |
| normative language | pass | New obligations consistently use testable normative terms. |
| completeness | block | Rule, trace, metric, and row-evidence bindings are incomplete. |
| testability | block | T45, T46, T51, and T55 still require implementation guesses. |
| examples | concern | Shapes are illustrative but not yet complete contracts. |
| compatibility | pass | Draft pre-activation amendment does not invalidate released artifacts. |
| observability | block | Diagnostics, trace linkage, and metric inputs are not closed. |
| security/privacy | concern | Filesystem safety is defined, but semantically unrelated evidence remains acceptable. |
| non-goals | pass | Semantic review remains reviewer-owned. |
| acceptance criteria | block | Substitution and computation contrasts are incomplete. |

## Architecture Assessment

Architecture assessment: architecture-not-required

The existing architecture already assigns pure fixture and capability
evaluation to the typed model and report serialization to the validator.
After spec approval, perform a bounded coherence check for finalized trace and
receipt terminology; no new component or ADR is required.
