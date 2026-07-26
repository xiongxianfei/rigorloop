# Boundary-First Proof Modeling Spec Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: Codex spec-review skill with context-separated reviewer
Target: commit `6093b03b` against `67a3cab2`
Reviewed artifact: specs/rigorloop-workflow.md; specs/skill-contract.md
Status: changes-requested
Review status: changes-requested
Material findings: none new; BFP-SR3-1, BFP-SR3-2, BFP-SR3-3 remain open
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R4 spec diff; R3 findings; approved architecture and ADR; matching test specs
Manifest owner: workflow orchestrator

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: none new; BFP-SR3-1, BFP-SR3-2, BFP-SR3-3 remain open
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r4.md`
- Review log: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md`
- Review resolution: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md#spec-review-r4`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: implementation remains blocked

## Prior-Finding Reconciliation

| Finding | Result | Remaining gap |
| --- | --- | --- |
| BFP-SR3-1 | partially-resolved | Seeded inputs may have zero or multiple triggers, contrasts need not be clean, and substituted identity is undefined. |
| BFP-SR3-2 | partially-resolved | Blocked grammar, roles/cardinality, immutable candidates, observed outcomes, and inventory-based metrics remain open. |
| BFP-SR3-3 | partially-resolved | Caller-authored same-row receipts and canned fixture evidence can still support production claims. |

## Required Corrections

- Incident derivation must accept exactly one field/value trigger, require a
  zero-trigger valid contrast, and reject zero/multiple-trigger seeded states.
- Simple-change proof must separate immutable candidate inputs, structural gate
  results, independently observed stage outcomes, and before/after artifact
  inventory.
- Canonical capability evidence must be freshly recomputed by the closed
  operation registry and sole report writer; caller-authored receipts cannot be
  the production trust anchor.
- M1 may prove schemas, contrasts, and synthetic aggregation, but it must not
  claim published-skill workflow behavior that first exists in M2/M3.

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | pass |
| observability | block |
| security/privacy | block |
| non-goals | pass |
| acceptance criteria | block |

## Architecture Assessment

Architecture assessment: architecture-required

The accepted component split remains useful, but a bounded amendment must
assign fresh operation execution, receipt serialization, canonical versus test
evidence, and immutable candidate ownership.
