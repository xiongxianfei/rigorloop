# Code Review M2 R11

Review ID: code-review-m2-r11

Stage: code-review

Round: 11

Reviewer: Codex code-review skill

Target: M2 R10 resolution through `df414a58`

Reviewed artifact: implementation diff `2f269d67..df414a58`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-18

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-r10-resolution

Reviewer context ID: boundary-m2-review-r11-reset

Context separation mechanism: blind-first diff and governing-clause pass before
validation summaries and prior findings

Risk tier: elevated

Risk-tier triggers: correction authority, temporal review evidence, immutable
publication, and recovery

Risk-tier classifier: governing-spec, mutation-authority, recovery, and
generated-evidence triggers

Governing artifacts: `specs/rigorloop-workflow.md` R28y;
`specs/rigorloop-workflow.test.md` T52;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M2

Formal criteria: exact finding projection, correction eligibility, temporal
review-resolution binding, approving-rereview prior-finding identity, durable
owner-decision stop, request-only child input, and post-observation expectation
comparison

Initial packet inventory: specs/rigorloop-workflow.md@df414a58#sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819; specs/rigorloop-workflow.test.md@df414a58#sha256:431e30ef05ff2720e77a589b48ac2794d79d76878f17c8dbe6be335d165d8f87; docs/plans/2026-07-25-boundary-first-proof-modeling.md@df414a58#sha256:2d5b03b18a350565c560a84ced4a8cfd793b2f07c49a5e909387ae60960d56a8; scripts/boundary_proof_behavior.py@df414a58#sha256:23dce971a42c8b3063ab43a55372eec53aebffd941eaacc710951fb723483ca2; scripts/boundary_proof_model.py@df414a58#sha256:9b6aa376beda3241724a0ded8ed16fd461d93e1ac5f938ff47010c4aa0d241ef; scripts/test-boundary-proof.py@df414a58#sha256:6e3ac8f4ca19daa787bb1a9e2e13312b6e5d1d686d5beb166965c9de05d26721; current.json@df414a58#sha256:bce347a2e25d65436411448241f5a8a64894f168de314139761781fc105de8ca

Prompt template version: code-review-template-v1

Initial packet hash: sha256:99d33675b8ab15ccda9a6e33557c5a2ba1435257696f068679198134899facf2

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: correction review-bundle assembly, correction-trace
validation, immutable publication, owner-decision stop recovery, and scenario
comparison.

Highest-impact failure modes: a changes-requested event is retroactively bound
to a closed resolution; an approving rereview loses the exact finding set it
settled; invalid correction evidence passes immutable validation.

Changed boundaries: open versus closed review resolution; initial review versus
rereview; review-record projection versus bundle-carried historical finding
identity.

Evidence expected: exact first-review open resolution, exact approving-rereview
closed resolution, exact prior finding set on rereview, mutation contrasts for
all three, and both correction-role assemblers.

Areas requiring direct inspection: `_correction_review_bundle`,
`_assemble_feature_spec_correction_run`,
`_assemble_test_spec_correction_run`, `evaluate_simple_change_trace`, and the
correction-assembler tests.

Areas intentionally out of scope: M3, M4, final holistic review, final verify,
PR, and release activation.

Risk classes considered: authorization=applicable; recovery=applicable;
generated evidence=applicable; requirement fidelity=applicable; temporal
review evidence=applicable; external deployment=not-applicable

Falsifiable review questions: Does each correction bundle preserve the exact
resolution state that existed at that occurrence? Can an approving rereview
erase or substitute the prior finding set and still pass validation?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, change metadata, and plan handoff
- Open blockers: BFP-CR-M2-18
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-18
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r11.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-18
- Verify readiness: not-claimed

## Findings

## Finding BFP-CR-M2-18

Finding ID: BFP-CR-M2-18

Prior finding reconciliation: new

Severity: blocker

Auto-fix class: declared-safe

Location: `scripts/boundary_proof_behavior.py:3534-3551`,
`scripts/boundary_proof_behavior.py:3851-3868`,
`scripts/boundary_proof_model.py:1989-2000`,
`scripts/test-boundary-proof.py:1985-2003`

Evidence: Both correction assemblers attach `corrected_resolution` to the
attempt-1 `changes-requested` bundle, then build the attempt-2 approving
rereview from a payload whose `material_finding_ids` is empty and pass no
resolution. The result reverses R28y's temporal evidence contract: the first
review should bind its open resolution, while the approving rereview must bind
the closed resolution and carry the exact prior finding set. The pure
evaluator accepts the invalid empty rereview set because it does not compare
the approving bundle with the pending correction's finding IDs. The assembler
test constructs and approves that invalid shape. The current zero-correction
canonical run cannot exercise this branch.

Required outcome: Bind the changes-requested bundle to the exact initial open
resolution; bind the approving-rereview bundle to the exact corrected closed
resolution and exact prior finding set; require the evaluator and immutable
validator to reject missing, changed, empty, or substituted rereview finding
sets and resolution references.

Safe resolution path: Extend the correction bundle builder with explicit
historical-finding and resolution inputs whose legal combinations are
outcome/attempt checked. Track the pending finding tuple in the pure evaluator
and require exact equality on approving rereview. Correct both assemblers and
replace the permissive assembler fixture with positive and mutation tests for
feature-spec and test-spec corrections.

needs-decision rationale: none

Auto-fix recipe: implement the exact approved R28y temporal bundle contract in
the behavior assembler, pure evaluator, and focused tests; do not change the
public skills, scenario expectation contract, M3, or M4.

Required validation: `python scripts/test-boundary-proof.py`;
controlled one-correction assembler validation for both roles; immutable
validation of the current zero-correction run.

## Prior finding reconciliation

- BFP-CR-M2-14: resolved by identity-bound correction eligibility and the
  owner-decision branch.
- BFP-CR-M2-15: resolved by post-observation scenario comparison.
- BFP-CR-M2-16: resolved by the complete durable correction-stop package and
  discard recovery proof.
- BFP-CR-M2-17: resolved by the direct T52 contrast matrix.
- BFP-CR-M2-18: new-finding.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Correction rereview bundle violates the exact R28y temporal contract. |
| Test coverage | block | The assembler test encodes the invalid empty rereview finding set. |
| Edge cases | block | Missing/substituted rereview findings and resolution are accepted. |
| Error handling | concern | Immutable validation cannot distinguish the invalid correction history. |
| Architecture boundaries | pass | Parent-only materialization and child input separation remain intact. |
| Compatibility | pass | Public skills and adapters are unchanged. |
| Security/privacy | pass | No credential, network, or mutation authority is widened. |
| Derived artifact currency | pass | `run-5820520…` validates for the zero-correction branch. |
| Unrelated changes | pass | The reviewed implementation remains scoped to M2. |
| Validation evidence | concern | Passing zero-correction evidence does not prove the correction branch. |

## Requirement-fidelity receipt

Requirement fidelity is applicable and does not pass. The produced correction
bundle loses the approved contract's temporal and historical identity, and the
validator accepts that loss.

## Handoff

M2 moves to `resolution-needed`. The finding is deterministic and within the
approved scope, so workflow-managed review-resolution may apply the declared
safe recipe and must rerun code review. M3 and final closeout remain blocked.
