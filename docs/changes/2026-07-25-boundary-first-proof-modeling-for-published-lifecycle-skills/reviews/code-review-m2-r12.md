# Code Review M2 R12

Review ID: code-review-m2-r12

Stage: code-review

Round: 12

Reviewer: Codex code-review skill

Target: M2 R11 resolution through `b849b9fe`

Reviewed artifact: implementation diff `77f182a4..b849b9fe`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-19

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-temporal-history-r12

Reviewer context ID: boundary-m2-review-r12-reset

Context separation mechanism: blind-first changed-validator inspection before
validation summaries and prior-finding reconciliation

Risk tier: elevated

Risk-tier triggers: untrusted immutable evidence, closed-schema validation,
correction history, and fail-closed error handling

Risk-tier classifier: governing-spec, generated-evidence, validation, and
recovery triggers

Governing artifacts: `specs/rigorloop-workflow.md` R28y;
`specs/rigorloop-workflow.test.md` T52;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M2

Formal criteria: exact prior finding set, open/closed resolution progression,
record-byte recomputation, malformed-value rejection, and controlled
fail-closed diagnostics

Initial packet inventory: specs/rigorloop-workflow.md@b849b9fe#sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819; specs/rigorloop-workflow.test.md@b849b9fe#sha256:431e30ef05ff2720e77a589b48ac2794d79d76878f17c8dbe6be335d165d8f87; scripts/boundary_proof_behavior.py@b849b9fe#sha256:810c72c93791ea3a768101ed4cc8d9cc8bbd5072dc1a23a9749d8bd4b168d977; scripts/boundary_proof_model.py@b849b9fe#sha256:d88fd733abbd81fcd0190debaafb3b6d29f5e79494f1f47582bd3e982f154525; scripts/test-boundary-proof.py@b849b9fe#sha256:b8f398d39f1907c6a3a53f4c5e53ab5ecf09f4f55783f05ddf8747a863c6f7ad; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/current.json@b849b9fe#sha256:fdb30a97998a53349e9ac09356f6f677a69eaa9e1be9cf8845cc4e9a02379b18

Prompt template version: code-review-template-v1

Initial packet hash: sha256:9f899573ea31406cb69500749f1a3831747fe34673096c01462c3fae7689d5c6

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: correction-bundle byte revalidation and malformed immutable
evidence handling.

Highest-impact failure modes: malformed evidence escapes the controlled
fail-closed diagnostic as a raw runtime exception; a caller cannot distinguish
invalid evidence from a harness defect.

Changed boundaries: raw JSON values versus typed bundle identities; malformed
finding arrays versus closed finding vocabularies.

Evidence expected: exact temporal-history positives plus missing, changed,
reused, unhashable reviewed-ID, and non-string finding-member negatives.

Areas requiring direct inspection: `_validate_review_bundle_payloads`, its call
order before the pure evaluator, and direct mutation tests.

Areas intentionally out of scope: M3, M4, final holistic review, verify, PR,
and release activation.

Risk classes considered: validation=applicable; generated evidence=applicable;
recovery=applicable; authorization=not-changed; external deployment=not-applicable

Falsifiable review questions: Can every JSON value at `reviewed_snapshot_id`
and `material_finding_ids[]` produce only a controlled fail-closed result? Can
the validator still accept the exact temporal-history positive?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, change metadata, and plan handoff
- Open blockers: BFP-CR-M2-19
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-19
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r12.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-19
- Verify readiness: not-claimed

## Findings

## Finding BFP-CR-M2-19

Finding ID: BFP-CR-M2-19

Prior finding reconciliation: partially-resolved

Severity: blocker

Auto-fix class: declared-safe

Location: `scripts/boundary_proof_behavior.py:3450-3456`,
`scripts/boundary_proof_behavior.py:3515-3522`

Evidence: The assembler and pure evaluator now enforce the correct open,
prior-finding, closed-resolution sequence. However,
`_validate_review_bundle_payloads` evaluates
`reviewed_snapshot_id not in output_snapshots` before proving the value is a
string. JSON arrays and objects therefore raise raw `TypeError: unhashable
type` instead of `runtime-identity-unstable`. The same helper iterates
`material_finding_ids` in string containment checks without first proving every
member is a string. Because this helper runs before the pure closed-schema
evaluator, malformed immutable evidence can escape controlled fail-closed
handling.

Required outcome: Validate `reviewed_snapshot_id` as a string and
`material_finding_ids` as a stable-ID-sorted unique string list before
membership or content operations; convert every malformed contrast to the
closed runtime diagnostic.

Safe resolution path: Add early exact type/shape guards inside
`_validate_review_bundle_payloads`, followed by direct table-driven tests for
array, object, null, scalar, non-string finding members, duplicate/unsorted
findings, and the valid temporal-history control.

needs-decision rationale: none

Auto-fix recipe: harden only the new review-bundle byte validator and its
focused tests; retain the approved temporal-history and public-skill behavior.

Required validation: `python scripts/test-boundary-proof.py`; immutable
current-run validation; code-review-m2-r13.

## Prior finding reconciliation

- BFP-CR-M2-14 through BFP-CR-M2-17: resolved.
- BFP-CR-M2-18: resolved; temporal identity and resolution progression are
  enforced.
- BFP-CR-M2-19: new-finding; malformed value handling remains open.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Valid temporal history conforms; malformed values do not fail through the closed diagnostic. |
| Test coverage | block | Direct unhashable and non-string contrasts are absent. |
| Edge cases | block | JSON list/object reviewed IDs raise raw `TypeError`. |
| Error handling | block | Closed validation is bypassed by raw runtime exceptions. |
| Architecture boundaries | pass | No ownership or mutation boundary changed. |
| Compatibility | pass | Public skills and adapters are unchanged. |
| Security/privacy | pass | No authority widened. |
| Derived artifact currency | pass | `run-9538fe0…` validates for valid zero-correction evidence. |
| Unrelated changes | pass | Diff remains M2-scoped. |
| Validation evidence | concern | Positive evidence passes; malformed-value proof is incomplete. |

## Handoff

M2 remains `resolution-needed`. Apply the declared-safe type-guard correction
and rerun code review; downstream milestones remain blocked.
