# Code Review R2: Requirement-Fidelity Gate M2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2 implementation diff
Reviewed artifact: M2 implementation diff at commit 9681a032
Reviewed commit: 9681a032 M2: validate requirement-fidelity review evidence
Reviewed milestone: M2. Applicability, receipt, and autoprogression validators
Review date: 2026-06-26
Recording status: recorded
Status: changes-requested
Autoprogression profile: implementation-through-verify
Material findings: RFG-M2-CR1
Review status: changes-requested
Immediate next stage: review-resolution
Implementation handoff: not-allowed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r2.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md; docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md; docs/plan.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFG-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r2.md
- Review log: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md
- Review resolution: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md#code-review-r2
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: RFG-M2-CR1
- Verify readiness: not-claimed

## Review Inputs

- Implementation diff: commit `9681a032`
- Approved spec: specs/requirement-fidelity-gate.md
- Test spec: specs/requirement-fidelity-gate.test.md
- Active plan: docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md
- Prior milestone review: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r1.md
- Validation evidence recorded in change metadata and plan validation notes

## Diff Summary

M2 adds requirement-fidelity closed vocabularies and review-artifact checks, lifecycle route checks for fidelity receipt validity when applicability is `applicable`, optional change-metadata validation for `review.requirement_fidelity`, and implementation-profile gating for approved recorded `test-spec-review` evidence.

The implementation also adds focused and full-suite tests for the new validation paths.

## Requirement-Property Decomposition

| Spec clause | Requirement property | Required surfaces | Verified? | Evidence |
| --- | --- | --- | --- | --- |
| `R3` | Workflow-managed continuation requires both independent-review and requirement-fidelity receipts when both apply. | lifecycle route and lifecycle tests | no | `scripts/lifecycle_state_sync.py:503`; `scripts/test-artifact-lifecycle-validator.py:1585` |
| `R4`-`R8` | Applicability must be computed/recorded before comparison and unknown or unjustified override values fail closed. | review-artifact validator, lifecycle route, change-metadata validator | partial | Review-artifact and metadata validators check supplied fields, but lifecycle route treats missing applicability as no failure. |
| `R30`-`R34` | Applicable clean automated reviews require receipt evidence and must block missing decomposition or validator/spec comparison. | review-artifact validator and lifecycle route | partial | The implementation blocks invalid supplied receipt fields, but omits a lifecycle requirement that an applicability result exist before clean handoff. |
| `R46`, `R50` | Independent-review behavior and historical records are preserved. | existing validator suites and historical compatibility tests | yes | Full `test-review-artifact-validator.py`, `test-artifact-lifecycle-validator.py`, and `test-change-metadata-validator.py` are recorded as passing. |

## Findings

### RFG-M2-CR1 - Clean automated handoff can omit the fidelity applicability result entirely

Finding ID: RFG-M2-CR1
Severity: blocker
Location: scripts/lifecycle_state_sync.py:503
Evidence: `_requirement_fidelity_failure_reason` returns `None` when `requirement_fidelity_applicability` is absent. That means `_clean_review_gate_failure_reason` treats missing fidelity applicability as no failure and can advance a workflow-managed clean `code-review` with only the independent-review receipt. I confirmed this directly by evaluating `evaluate_automated_review_gate_route` with a workflow-managed clean review fixture containing valid independent-review gates and no requirement-fidelity fields; the result was `ImplementationAutoprogressionRoute(profile_state='active', next_stage='advance', stop_reason=None)`. The test fixture default at `scripts/test-artifact-lifecycle-validator.py:1585` also lacks `requirement_fidelity_applicability`, so the positive clean-advance tests exercise the bypass path by default.
Required outcome: Workflow-managed automated clean handoff must require a deterministic requirement-fidelity applicability result before advance. If the result is `applicable`, a valid fidelity receipt must be required; if the result is `not-applicable`, a closed not-applicable reason must be required. Add negative tests proving omission of the applicability result blocks clean handoff, and keep direct/profile-off or historical compatibility behavior explicitly covered.
Safe resolution path: Change `_requirement_fidelity_failure_reason` or its caller so workflow-managed automated clean reviews fail with a stable stop reason when `requirement_fidelity_applicability` is missing. Update the lifecycle fixture defaults and tests so clean advance requires either `applicable` plus `requirement_fidelity_receipt_valid=True` or `not-applicable` plus a closed reason. Add a review-artifact validator negative test for automated review records that omit the requirement-fidelity applicability manifest where the automated fidelity gate is in force.
auto_fix_class: none

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R3`, `R4`, `R5`, `R30`, and `R34` require applicable automated handoff to be gated by fidelity applicability/receipt evidence; omission currently advances. |
| Test coverage | concern | Added tests cover invalid supplied values, but no lifecycle test covers missing applicability on a clean workflow-managed review. |
| Edge cases | block | The core bypass edge case, independent-review receipt alone with no fidelity applicability result, is not rejected. |
| Error handling | concern | Unknown fidelity values fail closed, but absent fidelity applicability is treated as no-op. |
| Architecture boundaries | pass | The implementation stays inside repo-owned validators and lifecycle helpers. |
| Compatibility | pass | Existing full validator suites pass and historical/direct behavior is not broadly migrated. |
| Security/privacy | pass | No secret, auth, network, or private-corpus behavior is introduced. |
| Derived artifact currency | pass | No generated skill or adapter output is touched in M2. |
| Unrelated changes | pass | The diff is scoped to M2 validators, tests, plan state, and change metadata. |
| Validation evidence | concern | Recorded validation commands are relevant, but they do not exercise the missing-applicability bypass. |

## No-Finding Rationale

Not applicable. One material finding is recorded.

## Milestone Handoff

M2 remains open and moves to `resolution-needed`. The next stage is `review-resolution` for `RFG-M2-CR1`. M3 through M5 remain open, and final closeout is not ready.
