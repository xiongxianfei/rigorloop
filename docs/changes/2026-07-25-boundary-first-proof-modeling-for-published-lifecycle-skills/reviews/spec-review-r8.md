# Boundary-First Proof Modeling Spec Review R8

Review ID: spec-review-r8
Stage: spec-review
Round: 8
Reviewer: Codex spec-review skill with context-separated reviewer
Target: commit `64f53570` against `c23b185b`
Reviewed artifact: specs/rigorloop-workflow.md; specs/skill-contract.md
Status: changes-requested
Review status: changes-requested
Material findings: none new; BFP-SR3-2 and BFP-SR3-3 remain open
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: exact R8 spec diff; R7 review; R28x-R28y; R56o-R56p; formal-review contract; accepted architecture; matching test specs
Manifest owner: workflow orchestrator

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: none new; BFP-SR3-2 and BFP-SR3-3 remain open
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r8.md`
- Review log: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md`
- Review resolution: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md#spec-review-r8`
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: implementation remains blocked

## Prior-Finding Reconciliation

| Finding | Result | Evidence |
| --- | --- | --- |
| BFP-SR3-1 | resolved | Incident derivation remains closed. |
| BFP-SR3-2 | nearly-resolved | Oracle, bundle, baseline, classifier, and trace semantics pass; exact review evidence union and portable run publication remain open. |
| BFP-SR3-3 | nearly-resolved | Manifest and typed identity ownership pass; filesystem inputs and typed dependencies still conflict. |

## Required Corrections

- Define review-event evidence as the deduplicated union of input snapshots,
  bundle snapshot, and bundle members; use the same set in artifact counting.
- Publish immutable run directories through an atomically replaced small
  current pointer.
- Define `input_refs` as filesystem-selector evidence and
  `dependency_results` as typed-result-selector evidence.

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | pass |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | block |
| observability | block |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | block |

Architecture assessment: architecture-required
