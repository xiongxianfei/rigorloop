# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commits fab8b95..493981a
Reviewed artifact: docs/plans/2026-05-12-record-every-formal-review.md#M2
Review date: 2026-05-12
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: M2 implementation and accepted `CR-M2-001` fix through commit `493981a`.
- Governing spec: `specs/formal-review-recording.md`
- Test spec: `specs/formal-review-recording.test.md`
- Active plan: `docs/plans/2026-05-12-record-every-formal-review.md`
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence: M2 validation notes in the active plan plus temporary status-mutation proof run during review.

## Diff summary

M2 now parses clean receipt review-log table entries, validates clean receipt file metadata, rejects empty `review-resolution.md` in clean roots, and adds shared `change.yaml.review` semantic checks for clean receipt roots.

## Findings

### CR-M2-002: Clean receipt root accepts non-clean review status

Finding ID: CR-M2-002
Severity: major
Location: `scripts/change_metadata_semantics.py` `validate_clean_receipt_root_review_metadata`; `scripts/review_artifact_validation.py` clean receipt root metadata validation
Evidence: A temporary copy of `tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` with `review.status: approved` instead of `review.status: clean` still passed both `python scripts/validate-review-artifacts.py --mode structure <copy>` and `python scripts/validate-change-metadata.py <copy>/change.yaml`.
Required outcome: Clean receipt root validation must reject a clean receipt root whose `change.yaml.review.status` does not identify the root as clean.
Safe resolution path: Require `review.status: clean` for clean receipt roots when strict clean-root validation is active, and add negative tests proving both metadata validation and review-artifact validation reject another status such as `approved`.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `R4l` requires the minimal clean-receipt root to identify review status, and the accepted fix specified `review.status: clean`; `approved` still passes. |
| Test coverage | block | Current tests cover missing status but not an invalid non-clean status. |
| Edge cases | block | The named `T27` clean-root metadata edge case still lacks direct invalid-status proof. |
| Error handling | pass | Missing reviewed artifact, missing review-log path, missing/nonzero unresolved items, and empty resolution failures are covered. |
| Architecture boundaries | pass | The shared helper keeps metadata semantics centralized across both validators. |
| Compatibility | concern | The fix should remain scoped to declared or validator-identified clean receipt roots, not all historical change metadata. |
| Security/privacy | pass | Reviewed diff and validation output contain no secrets or sensitive runtime values. |
| Derived artifact currency | pass | No generated adapter output was expected for M2; generated output refresh remains M4. |
| Unrelated changes | pass | The rerun diff is tied to accepted `CR-M2-001` and its validation evidence. |
| Validation evidence | concern | Existing M2 validation passed, but it did not include invalid-status negative proof. |

## No-finding rationale

Not applicable; material finding `CR-M2-002` requires a fix before M2 can close.

## Residual risks

Keep strict `status: clean` enforcement limited to clean receipt roots so ordinary non-clean change metadata continues using the existing project vocabulary.
