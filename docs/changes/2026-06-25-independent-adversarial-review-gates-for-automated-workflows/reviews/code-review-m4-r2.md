# Code Review M4 R2

Review ID: code-review-m4-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M4 review-resolution for calibration fixtures and measurement evidence
Reviewed artifact: Uncommitted M4 review-resolution diff after `code-review-m4-r1`
Review date: 2026-06-25
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m4-r2.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`, `docs/plans/2026-06-25-independent-adversarial-review-gates.md`, `docs/plan.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Open blockers: CR6-F1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR6-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m4-r2.md
- Review log: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md
- Review resolution: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md
- Reviewed milestone: M4. Calibration fixtures and measurement evidence
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution, M5
- Required review-resolution: yes
- Finding IDs: CR6-F1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: uncommitted M4 review-resolution diff after `code-review-m4-r1`, especially `scripts/lifecycle_state_sync.py`, `scripts/review_artifact_validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-review-artifact-validator.py`, new calibration authority fixtures, spec/test-spec deltas, active plan state, plan index, review-resolution, review log, behavior-preservation evidence, and change metadata.
- Tracked governing branch state: branch `proposal/independent-adversarial-review-gates`; governing spec, test spec, architecture, plan, and prior review records are tracked. The reviewed M4 resolution changes are uncommitted. One unrelated untracked learn-session file exists and is outside the review surface.
- Governing artifacts: `specs/review-independence-and-criticality.md` R14d and R17a; `specs/review-independence-and-criticality.test.md` T10c-T10g and T11d-T11f; `docs/plans/2026-06-25-independent-adversarial-review-gates.md` M4; `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md#code-review-m4-r1`.
- Validation evidence reviewed: focused `python scripts/test-review-artifact-validator.py -k calibration`, `python scripts/test-artifact-lifecycle-validator.py -k sampling_floors`, `python scripts/test-artifact-lifecycle-validator.py -k critical_authority`, `python scripts/test-review-artifact-validator.py -k authority`, `python scripts/test-review-artifact-validator.py -k boolean`, full `python scripts/test-review-artifact-validator.py`, full `python scripts/test-artifact-lifecycle-validator.py`, review-artifact structure and closeout validation, change metadata validation, lifecycle explicit-path validation, direct negative fixture probes, direct unsupported-value probe, `git diff --check`, and whitespace scan.

## Diff summary

The M4 review-resolution adds critical authority fields and validators, fail-closed calibration yes/no parsing, lifecycle routing cases for critical-internal and irreversible-external-action review gates, review-artifact tests for authority and boolean control fields, positive and negative calibration authority fixtures, spec/test-spec clarifications, behavior-preservation notes, and lifecycle state updates returning M4 to code-review.

## Findings

### CR6-F1 - Unsupported critical authority kinds are masked by outcome mismatch when `advance` is supplied

Finding ID: CR6-F1
Severity: major
Location: `scripts/lifecycle_state_sync.py:454`-`494`, `scripts/lifecycle_state_sync.py:527`-`535`, `scripts/test-artifact-lifecycle-validator.py:1931`-`1940`
Evidence: `specs/review-independence-and-criticality.test.md` T10g requires unsupported critical-authority kinds to fail closed before route branching, and the M4 R1 resolution policy says closed vocabulary control fields must be parsed separately from branch consumers. `_critical_authority_failure_reason` correctly returns `critical-authority-kind-invalid` for an unsupported `critical_authority_kind`, but `evaluate_automated_review_gate_route` checks the supplied `review_gate_outcome` against the gate-derived expected outcome before returning the underlying failure reason. Direct probe with `native_review_status: clean-with-notes`, `review_gate_outcome: advance`, `risk_tier: critical-internal`, `risk_tier_satisfied: True`, `critical_authority_kind: banana`, and `critical_authority_satisfied: True` returned `ImplementationAutoprogressionRoute(profile_state='paused', next_stage=None, stop_reason='review-gate-outcome-mismatch-given-gate-state')`, not `critical-authority-kind-invalid`. The added test only covers the invalid kind when the supplied outcome is already `inconclusive`, so the parser-order case that T10g names remains unproved.
Required outcome: Unsupported critical authority kinds must surface as the explicit closed-vocabulary failure regardless of the supplied `review_gate_outcome`, and a regression test must cover the `advance` probe.
Safe resolution path: In `evaluate_automated_review_gate_route`, split clean native-status evaluation so closed-vocabulary/parser failures such as `critical-authority-kind-invalid` are returned before the supplied outcome consistency check, or add a route-input parse step before clean gate derivation. Add a lifecycle regression test using the direct probe above and expecting `critical-authority-kind-invalid`. Keep the existing mismatch behavior for non-parser gate failures where appropriate, then rerun the M4 targeted and full validation commands.
needs-decision rationale: none
auto_fix_class: none

## Checklist coverage

1. Spec alignment: block. R14d authority enforcement blocks advancement, but T10g's closed-vocabulary parser-order expectation is not met for `advance` inputs.
2. Test coverage: block. The new tests cover invalid authority kind only when `review_gate_outcome` is already `inconclusive`; they miss the malformed `advance` input that currently masks the parser failure.
3. Edge cases: block. Unsupported critical authority kind plus supplied `advance` is a named closed-vocabulary edge case and direct probe shows the wrong stop reason.
4. Error handling: concern. The route still pauses, but it reports a generic outcome mismatch instead of the actionable unsupported authority kind.
5. Architecture boundaries: pass. The resolution stays in existing lifecycle validators, review artifact validators, fixtures, specs, and change-local evidence.
6. Compatibility: pass. Standard/elevated behavior and existing calibration fixture shape remain compatible in the reviewed diff.
7. Security/privacy: concern. No secrets or private reasoning are exposed, but critical authority errors need precise fail-closed diagnostics so high-risk handoff evidence cannot be misclassified.
8. Derived artifact currency: pass. The reviewed diff does not touch canonical skills or generated adapter output.
9. Unrelated changes: pass. The reviewed diff is scoped to M4 review-resolution artifacts and validators; the unrelated untracked learn-session file is excluded.
10. Validation evidence: concern. Full suites passed, but the direct parser-order probe above is not represented in the targeted tests.

## Residual risks

M5 remains open. This review does not assess final generated/doc proof, final holistic review evidence, explain-change, verify, or PR readiness.

## Milestone handoff state

- Reviewed milestone: M4. Calibration fixtures and measurement evidence
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M4 resolution, M5
- Next stage: review-resolution
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — M4 has an open code-review finding; M5 remains incomplete.
