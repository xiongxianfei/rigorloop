# Code Review M4 R1 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M4 commit `f68d83d`
Reviewed milestone: M4. Measurement evidence and selected validation routing
Reviewed artifact: scripts/validate-change-metadata.py; scripts/validation_selection.py
Review date: 2026-05-23
Recording status: recorded
Status: approved

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M4. Measurement evidence and selected validation routing
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `f68d83d` against `ff3cc29`, with focus on `scripts/validate-change-metadata.py`, `scripts/validation_selection.py`, M4 tests, measurement fixtures, `validation-cache-measurement.yaml`, `behavior-preservation.md`, and lifecycle state updates.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, review log, review-resolution, M1 through M3 code-review records, and M4 implementation commit are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected and rerun: targeted M4 reviewer checks for measurement fixtures, cache evidence selector routing, direct measurement validation, and explicit selector output for validation cache evidence files.

## Diff Summary

M4 adds validation for `validation-cache-measurement.yaml`, including required top-level fields, summary counts, non-negative numeric fields, Workstream B recommendation state, closeout cache-skip rejection, and recursive unsafe-value checks. It registers `validation-cache-evidence.yaml` and `validation-cache-measurement.yaml` as deterministic change-local evidence classes in the selector. It also adds measurement fixtures, selector routing tests, this change's Workstream A measurement artifact, behavior-preservation evidence, and plan/change state updates.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The implementation addresses R75, R117-R130, and AC17/AC29-AC32 by recording and validating Workstream A measurement evidence while keeping Workstream B as a deferred recommendation only. |
| Test coverage | pass | `test_measurement_valid_fixture_passes`, `test_measurement_invalid_fixtures_fail`, and `test_validation_cache_evidence_files_route_without_manual_debt` cover the M4 measurement and routing paths. |
| Edge cases | pass | Direct proof covers missing fields, negative counts, inconsistent counts, nonzero `closeout_cache_skips`, invalid Workstream B state, missing rationale, unsafe values, and selector routing without manual debt. |
| Error handling | pass | Invalid measurement files produce stable field-specific diagnostics and do not fall back to legacy change metadata validation. |
| Architecture boundaries | pass | Measurement validation stays in change metadata validation; selector routing remains registration-based and does not add edit-scoped validator narrowing. |
| Compatibility | pass | Existing change metadata validation remains intact; only files named `validation-cache-measurement.yaml` use the new measurement contract. |
| Security/privacy | pass | Measurement evidence rejects unsafe paths, hostnames, credential-bearing values, secret-like values, and machine-local values through the existing safe-value helper. |
| Derived artifact currency | pass | No generated artifacts are changed. |
| Unrelated changes | pass | The diff is scoped to M4 validators, selector routing, fixtures, measurement evidence, behavior-preservation evidence, and lifecycle state updates. |
| Validation evidence | pass | Implementation and reviewer-run checks include targeted measurement tests, targeted selector routing, measurement validation, local selector proof, local selected CI, review artifact validation, lifecycle validation, and whitespace checks. |

## No-Finding Rationale

The M4 implementation satisfies the approved measurement and routing contract without adding Workstream B changed-path or edit-class validation narrowing. The validator rejects the named unsafe and impossible measurement states, the selector routes the new deterministic evidence files through bounded checks without manual-routing debt, and the recorded measurement evidence keeps `closeout_cache_skips: 0`.

## Residual Risks

- The measurement numbers are review evidence for deciding whether follow-up work is worthwhile; they are not a performance guarantee or authorization for Workstream B.
- Final closeout still requires explain-change, verify, and PR handoff after this clean final implementation milestone review.

## Milestone Handoff

- Reviewed milestone: M4. Measurement evidence and selected validation routing.
- Review status: clean-with-notes.
- Milestone state after review: closed.
- Required review-resolution: no.
- Remaining in-scope implementation milestones: none.
- Next stage: explain-change.
- Final closeout readiness: not ready; explain-change and verify are not recorded, and PR handoff is not prepared.
