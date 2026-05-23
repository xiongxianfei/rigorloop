# Code Review M2 R2 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M2 post-resolution commit `3cbbf36`
Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence
Reviewed artifact: scripts/validation_cache.py; scripts/validate-artifact-lifecycle.py
Review date: 2026-05-23
Recording status: recorded
Status: approved

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence
- Milestone closeout: closed
- Remaining implementation milestones: M3 and M4 planned
- Required review-resolution: no
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `3cbbf36` against `a638ad8`, with focus on the `VIC-CR-M2-R1-F1` and `VIC-CR-M2-R1-F2` resolution in `scripts/validation_cache.py`, `scripts/validate-artifact-lifecycle.py`, and `scripts/test-validation-cache.py`.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, review log, review-resolution, M1 reviews, and M2 R1 review are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected and rerun: `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, and `python scripts/test-select-validation.py` passed during this review rerun.

## Diff Summary

The M2 review-resolution diff makes local cache records and contexts carry mandatory `cache_key`, `validator_id`, and `command_family` fields. Local cache-hit eligibility now rejects missing, malformed, unsupported, or mismatched identity fields before considering component hashes. The formal cache-hit evidence writer now reads and validates an existing `validation-cache-evidence.yaml`, preserves unrelated cache-hit records, replaces only a matching stable cache-hit ID, appends new IDs, and rejects malformed or duplicate-ID evidence.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The resolved M2 implementation preserves Workstream A scope, keeps cache use opt-in for explicit-path lifecycle validation, and now fails closed when required cache identity fields are missing or malformed. |
| Test coverage | pass | `scripts/test-validation-cache.py` directly covers missing and mismatched cache keys, missing and unsupported validator IDs, command-family mismatches, valid matching records, merge-preserving evidence writes, same-ID replacement, malformed evidence, and duplicate IDs. |
| Edge cases | pass | The named M2 review edge cases from `VIC-CR-M2-R1-F1` and `VIC-CR-M2-R1-F2` have direct regression coverage. |
| Error handling | pass | Malformed local cache records are ignored as cache misses, while malformed tracked formal evidence fails closed with stable cache identity errors. |
| Architecture boundaries | pass | Cache execution remains in the lifecycle CLI/helper layer and actual lifecycle validation semantics remain unchanged when the validator runs. |
| Compatibility | pass | Cache use remains opt-in, first-slice validator support remains limited to `artifact-lifecycle`, and unsupported cache records do not fail validation commands. |
| Security/privacy | pass | Formal evidence writing continues to use repository-relative references and does not write local worktree paths into tracked cache-hit evidence. |
| Derived artifact currency | pass | No generated artifacts are changed. |
| Unrelated changes | pass | The resolution diff is scoped to M2 cache safety findings, tests, and lifecycle state recording. |
| Validation evidence | pass | Reviewer-run validation passed for cache regression, artifact lifecycle regression, and selector regression. Recorded implementation validation also includes metadata validation, artifact lifecycle validation, selected CI, review-artifact validation, and whitespace checks after M2 review-resolution. |

## No-Finding Rationale

The two M2 R1 findings are resolved. Local cache hit eligibility now requires an exact stored full cache key, supported validator ID, and supported command family, and it treats missing or malformed local cache records as misses. Formal cache-hit evidence is no longer overwritten on each write; unrelated cache-hit records remain reviewable, same-ID replacement is bounded, and malformed tracked evidence fails closed.

## Residual Risks

- M2 does not implement compact metadata closeout enforcement or Workstream A measurement; those remain planned for M3 and M4.
- Cache-hit evidence reference validation remains bounded to the M2 formal evidence writer. Full compact `change.yaml` evidence-kind enforcement is intentionally deferred to M3.

## Milestone Handoff

- Reviewed milestone: M2. Explicit-path lifecycle cache integration and cache-hit evidence.
- Review status: clean-with-notes.
- Milestone state after review: closed.
- Required review-resolution: no.
- Remaining in-scope implementation milestones: M3 and M4 remain planned.
- Next stage: implement M3.
- Final closeout readiness: not ready; M3 and M4 are not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.
