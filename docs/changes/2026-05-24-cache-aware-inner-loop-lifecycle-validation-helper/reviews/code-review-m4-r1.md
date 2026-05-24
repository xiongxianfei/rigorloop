# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M4 measurement schema and selector routing
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-log.md`
- Review resolution: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/review-resolution.md`
- Reviewed milestone: M4
- Milestone closeout: closed
- Remaining implementation milestones: M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed
- Next stage: implement M5

## Review Inputs

- Reviewed implementation commit: `8a15661` (`M4: add helper measurement and routing`)
- Plan: `docs/plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Test spec: `specs/validation-idempotency-and-cache-hit-safety.test.md`
- Implementation files: `scripts/validate-change-metadata.py`
- Test files and fixtures: `scripts/test-change-metadata-validator.py`, `tests/fixtures/change-metadata/measurement-*`
- Evidence files: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
- Selector proof: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-evidence.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml`
- Validation evidence: M4 validation notes in the active plan and `change.yaml`

## Diff Summary

M4 updates validation-cache measurement metadata validation from the older first-slice count model to the helper-specific model from the approved spec. The validator now requires helper invocations, actual-run fallbacks, closeout actual runs, per-validator command family, and helper count consistency rules. The test fixtures cover required fields, negative counts, helper/fallback drift, cache-hit-rate drift, closeout cache skips, unsafe values, Workstream B state validation, and the first-slice measurement evidence file. Selector routing was already registered; M4 records direct selector proof that cache evidence and measurement paths route without manual debt.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R117-R130 and R157-R159 are enforced by helper-specific measurement fields, count consistency checks, `closeout_cache_skips: 0`, safe-value validation, and `defer` Workstream B recommendation evidence. R152-R154 are covered by selector output for both cache evidence files. |
| Test coverage | pass | `scripts/test-change-metadata-validator.py` now includes fixtures for missing helper fields, helper/fallback count drift, cache-hit-rate drift, cache-hit-as-closeout impossible counts, and existing unsafe value/state cases. |
| Edge cases | pass | The old `eligible_commands = cache_hits + cache_misses + cache_disabled` behavior was replaced with `helper_invocations = cache_hits + actual_run_fallbacks`, `actual_run_fallbacks = cache_misses + cache_disabled`, and actual-run/closeout separation checks. |
| Error handling | pass | Missing, negative, and inconsistent fields fail closed with explicit field-level errors. |
| Architecture boundaries | pass | The implementation stays in change-metadata validation and fixtures; it does not expand cache eligibility or add a wrapper/helper surface. |
| Compatibility | pass | Existing selector registrations are preserved, and direct lifecycle closeout remains actual-run validation. |
| Security/privacy | pass | Measurement safe-value validation remains active, and the new measurement evidence uses repository-relative paths and no host/user/secret data. |
| Derived artifact currency | pass | No generated artifacts are touched. |
| Unrelated changes | pass | The diff is scoped to M4 measurement validation, fixtures, measurement evidence, and lifecycle state updates. |
| Validation evidence | pass | `python scripts/test-validation-cache.py`, `python scripts/test-change-metadata-validator.py`, `python scripts/test-select-validation.py`, selector explicit routing, measurement validation, change metadata validation, review artifact validation, artifact lifecycle validation, and `git diff --check --` are recorded as passing. |

## No-Finding Rationale

The reviewed implementation makes the helper measurement fields normative in the validator, proves invalid count relationships with focused fixtures, records first-slice measurement evidence with expansion deferred, and demonstrates deterministic selector routes for both cache evidence files without changing cache eligibility or closeout semantics.

## Residual Risks

Repository-local guidance and behavior-preservation evidence remain open in M5. Final closeout remains blocked until M5, M6, explain-change, verify, and PR handoff complete.
