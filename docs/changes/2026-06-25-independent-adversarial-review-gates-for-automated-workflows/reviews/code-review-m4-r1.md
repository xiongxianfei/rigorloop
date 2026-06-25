# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M4 calibration fixtures and measurement evidence implementation diff at commit `690309e8`
Reviewed artifact: M4 implementation diff at commit `690309e8`
Review date: 2026-06-25
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m4-r1.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`, `docs/plans/2026-06-25-independent-adversarial-review-gates.md`, `docs/plan.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Open blockers: CR5-F1, CR5-F2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR5-F1, CR5-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m4-r1.md
- Review log: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md
- Review resolution: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md
- Reviewed milestone: M4. Calibration fixtures and measurement evidence
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution, M5
- Required review-resolution: yes
- Finding IDs: CR5-F1, CR5-F2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `690309e8`, especially `scripts/lifecycle_state_sync.py`, `scripts/review_artifact_validation.py`, `scripts/test-artifact-lifecycle-validator.py`, `scripts/test-review-artifact-validator.py`, `tests/fixtures/review-artifacts/valid-calibration-public-defect-class/`, `behavior-preservation.md`, active plan state, plan index, and change metadata updates.
- Tracked governing branch state: branch `proposal/independent-adversarial-review-gates`; M4 implementation commit is tracked at `690309e8`. One unrelated untracked learn-session file exists and was excluded from the implementation review surface.
- Governing artifacts: `specs/review-independence-and-criticality.md` R14-R17 and AC10-AC14; `specs/review-independence-and-criticality.test.md` T10-T12 and T19; `docs/plans/2026-06-25-independent-adversarial-review-gates.md` M4.
- Validation evidence reviewed: focused `python scripts/test-review-artifact-validator.py -k calibration`, focused `python scripts/test-artifact-lifecycle-validator.py -k sampling_floors`, full `python scripts/test-review-artifact-validator.py`, full `python scripts/test-artifact-lifecycle-validator.py`, review artifact closeout validation, change metadata validation, lifecycle explicit-path validation, `git diff --check`, and whitespace scan.

## Diff summary

M4 adds calibration record validation to review artifact parsing, adds lifecycle routing checks for standard-risk rollout sampling floors, adds review-artifact and lifecycle tests for sampling, second-review disagreement, elevated-risk second review, downstream escape record fields, and metric separation, adds a public defect-class calibration fixture, records M4 behavior-preservation evidence, and updates lifecycle state to request M4 code-review.

## Findings

### CR5-F1 - Critical-risk clean reviews still advance without explicit L3 or human authority evidence

Finding ID: CR5-F1
Severity: major
Location: `scripts/lifecycle_state_sync.py:459`-`481`; `scripts/test-artifact-lifecycle-validator.py:1835`-`1882`; `scripts/review_artifact_validation.py:1194`-`1268`
Evidence: `specs/review-independence-and-criticality.md` R14d requires critical-risk reviews to satisfy their configured `L3` or human authority gate. T10 also names "critical-risk reviews satisfy L3 or human authority gate" as a required assertion. M4 adds standard sampling and elevated second-review cases, but the new lifecycle test table has no `critical-internal` or `irreversible-external-action` case. Direct probe: `evaluate_automated_review_gate_route` returned `ImplementationAutoprogressionRoute(profile_state='active', next_stage='advance', stop_reason=None)` for `risk_tier: critical-internal` and `risk_tier: irreversible-external-action` when `risk_tier_satisfied` was set to `True` without any explicit L3 or human authority evidence. Direct review-artifact probe: a copied valid calibration fixture changed to `Risk tier: critical-internal`, `Independence level: L1`, and `Context separation mechanism: fresh-context-same-model` passed `python scripts/validate-review-artifacts.py --mode structure` with zero findings.
Required outcome: M4 must add explicit critical-risk authority evidence and tests so critical internal clean reviews cannot advance without configured L3 evidence, and irreversible external action reviews cannot advance without the required human authority evidence.
Safe resolution path: Add closed fields to lifecycle route inputs and calibration/review records for critical authority evidence, such as `critical_authority_required`, `critical_authority_satisfied`, and a human-authority marker for irreversible external actions. Validate `critical-internal` against L3-or-human evidence and `irreversible-external-action` against human authority. Add lifecycle tests for critical internal without L3/human, critical internal with L3, irreversible external with L3-only rejected, and irreversible external with human authority accepted. Add review-artifact fixture tests proving a critical internal L1 calibration record fails and a valid L3/human record passes. Rerun M4 review-artifact, lifecycle, closeout, metadata, and state-sync validation.
needs-decision rationale: none
auto_fix_class: none

### CR5-F2 - Calibration yes/no fields accept unsupported values and can hide ambiguous evidence

Finding ID: CR5-F2
Severity: major
Location: `scripts/review_artifact_validation.py:1221`-`1268`; `scripts/test-review-artifact-validator.py:1123`-`1176`
Evidence: M4 introduces calibration fields that operate as closed yes/no controls: `Sample-rate reduction requested`, `Second review required`, and `Automatic continuation`. The validator only checks literal `yes` in branch conditions and never rejects unsupported values. Direct probe: replacing those three fields with `banana` in `tests/fixtures/review-artifacts/valid-calibration-public-defect-class/reviews/code-review-r1.md` produced `()` from `validate_change_root(...).blocking_findings`, and the CLI structure validator also passed. This violates the R17a record-shape intent to prefer closed vocabulary fields and weakens T10/T11 proof because ambiguous values can bypass reduction and continuation checks.
Required outcome: Calibration boolean-like control fields must reject unsupported values instead of treating unknown values as false or not-required.
Safe resolution path: Add a shared closed vocabulary for calibration yes/no fields and validate `Sample-rate reduction requested`, `Second review required`, and `Automatic continuation` against it before using them in branch logic. Add regression tests that set each field to an unsupported value and assert fail-closed errors. Rerun M4 review-artifact validation and full validator tests.
needs-decision rationale: none
auto_fix_class: none

## Checklist coverage

1. Spec alignment: block. CR5-F1 leaves R14d/T10 critical authority enforcement incomplete; CR5-F2 leaves calibration control fields outside the closed-vocabulary discipline expected by R17a/T11.
2. Test coverage: block. M4 tests cover standard sampling, early reduction, elevated second review, and disagreement, but omit the named critical-risk T10 cases and unsupported yes/no calibration values.
3. Edge cases: block. Critical internal and irreversible external action reviews are named edge cases; direct probes show both can advance without explicit L3/human evidence when `risk_tier_satisfied` is asserted. Ambiguous boolean-like calibration values also pass.
4. Error handling: concern. The new validators fail closed for some fields, but they treat unsupported control values as false/not-required rather than invalid evidence.
5. Architecture boundaries: pass. The implementation stays in existing validators, lifecycle helpers, fixtures, and change-local evidence; no service, persistence, generated public adapter source, or external dependency was added.
6. Compatibility: pass. Existing non-calibration automated review fixtures still pass after the narrowed calibration trigger, and the M4 behavior-preservation file records manual/profile-off compatibility.
7. Security/privacy: concern. No secrets or private reasoning are exposed, but CR5-F1 affects the critical/security authority boundary by allowing high-risk review handoff without explicit L3/human proof.
8. Derived artifact currency: pass. M4 does not touch canonical skills or generated adapter output.
9. Unrelated changes: pass. The reviewed commit contains M4 validator, test, fixture, behavior-preservation, plan, index, and change metadata updates. The unrelated untracked learn file is outside the review surface.
10. Validation evidence: concern. The recorded commands passed, but the targeted test set is missing the critical-risk authority cases and unsupported control-value regressions reproduced above.

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
- Reason final closeout is or is not ready: implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — M4 has open code-review findings; M5 remains incomplete.
