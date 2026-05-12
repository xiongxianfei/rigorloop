# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit fab8b95
Reviewed artifact: docs/plans/2026-05-12-record-every-formal-review.md#M2
Review date: 2026-05-12
Status: changes-requested
Recording status: recorded

## Review inputs

- Diff/review surface: `fab8b95` (`M2: validate clean formal review receipts`)
- Governing spec: `specs/formal-review-recording.md`
- Test spec: `specs/formal-review-recording.test.md`
- Active plan: `docs/plans/2026-05-12-record-every-formal-review.md`
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence: M2 validation notes in the active plan plus temporary negative metadata checks run during review.

## Diff summary

M2 extends the review artifact validator to parse clean receipt review-log table entries, reject clean roots with empty `review-resolution.md`, validate clean receipt review-file metadata, add change metadata shape checks for optional receipt pointers, and record M2 handoff metadata.

## Findings

### CR-M2-001: Clean receipt root metadata can omit required review fields

Finding ID: CR-M2-001
Severity: major
Location: `scripts/validate-change-metadata.py` `validate_metadata_semantics`; `scripts/review_artifact_validation.py` clean receipt root validation
Evidence: A temporary copy of `tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml` with `review.reviewed_artifact` removed still passed both `python scripts/validate-change-metadata.py <copy>/change.yaml` and `python scripts/validate-review-artifacts.py --mode structure <copy>`. A second copy with `review.unresolved_items: 1` also passed both commands.
Required outcome: Clean receipt root validation must reject minimal clean-receipt roots whose `change.yaml.review` does not identify reviewed artifact, review-log path, review status, and unresolved item count `0`.
Safe resolution path: Add focused negative tests for missing `review.reviewed_artifact`, missing `review.review_log`, and nonzero `review.unresolved_items` on a clean receipt root. Implement validation in the review artifact validator, change metadata validator, or a shared helper so the clean receipt root fixture still passes and malformed roots fail.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `R4l` requires the minimal clean-receipt root `change.yaml` to identify reviewed artifact, review-log path, review status, and unresolved item count `0`; malformed temporary roots still pass. |
| Test coverage | block | M2 tests cover pointer type errors but not missing required clean-root metadata or nonzero unresolved items. |
| Edge cases | block | The named `T27` edge case for `change.yaml.review` metadata is only proved by the positive fixture, not by negative enforcement. |
| Error handling | pass | Clean receipt table row, receipt metadata, and empty-resolution failure paths are covered. |
| Architecture boundaries | pass | The implementation extends existing validators and fixtures rather than introducing a second parser model. |
| Compatibility | concern | The new clean-root validation should stay scoped to clean receipt roots so legacy non-clean metadata remains compatible. |
| Security/privacy | pass | Reviewed diff and validation output contain no secrets or sensitive runtime values. |
| Derived artifact currency | pass | No generated adapter output was expected for M2; the one canonical skill wording fix is scheduled for generated-output refresh in M4. |
| Unrelated changes | pass | The workflow skill wording update resolves an existing contract-alignment test failure and is recorded in the plan. |
| Validation evidence | concern | The recorded validation commands are relevant, but they did not include negative proof for the required minimal `change.yaml.review` fields. |

## No-finding rationale

Not applicable; material finding `CR-M2-001` requires a fix before M2 can close.

## Residual risks

Keep the fix narrowly scoped to clean receipt roots. The general change metadata schema still intentionally allows broader project vocabulary and optional fields outside this clean-root contract.
