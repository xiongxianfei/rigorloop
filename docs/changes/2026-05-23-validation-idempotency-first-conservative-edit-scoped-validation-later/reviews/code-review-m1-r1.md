# Code Review M1 R1 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 commit `aeb81bd`
Reviewed milestone: M1. Cache identity primitives and local cache contract
Reviewed artifact: scripts/validation_cache.py
Review date: 2026-05-23
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: VIC-CR-M1-R1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md#code-review-m1-r1`
- Reviewed milestone: M1. Cache identity primitives and local cache contract
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 pending review-resolution; M2, M3, and M4 planned
- Required review-resolution: yes
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `aeb81bd` against its parent, with focus on `scripts/validation_cache.py`, `scripts/test-validation-cache.py`, selector registration changes, and M1 lifecycle artifacts.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, review log, and review-resolution are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected: M1 plan validation notes and commit message evidence for `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, change metadata validation, artifact lifecycle validation, `git diff --check --`, and explicit selected CI.

## Diff Summary

M1 adds `scripts/validation_cache.py` with first-slice cache identity primitives for explicit-path lifecycle validation, adds `scripts/test-validation-cache.py`, registers a `validation_cache.regression` selector route for the new helper and test, and records lifecycle artifacts through M1 review-requested handoff. The implementation does not integrate runtime cache skipping into the lifecycle validator.

## Findings

### VIC-CR-M1-R1-F1: Unresolved implementation manifests are not disabled or directly tested

Finding ID: VIC-CR-M1-R1-F1
Severity: major
Location: `scripts/validation_cache.py:207`, `scripts/validation_cache.py:300`, `scripts/test-validation-cache.py:187`

Evidence: The approved test spec `VIC-T008` requires invalid cases where imports cannot be resolved deterministically, with the expected result that an unresolved manifest disables caching. The implementation manifest builder silently skips missing or unreadable files: `build_implementation_manifest` continues when a pending file is not present, `_repository_imports` returns an empty tuple on parse/read failures, and `_resolve_module` returns an empty set when an import cannot be resolved. The M1 test only proves the happy path for resolved local imports and standard-library exclusion; it does not cover a missing entrypoint, unreadable/invalid helper, or unresolved helper import.

Required outcome: The cache identity layer must expose unresolved implementation-manifest state as cache-ineligible, and M1 tests must directly prove the named unresolved-manifest edge case from `VIC-T008` / spec `R26`.

Safe resolution path: Add an explicit manifest eligibility/status result or raise `CacheIdentityError` for deterministic-manifest failures that would otherwise produce an incomplete implementation identity. Add focused tests for at least a missing entrypoint or unresolved repository-local helper import and for unreadable or unparsable repository-local helper input if supported by the chosen API. Preserve standard-library and third-party exclusion behavior, then rerun the M1 validation set and selected CI.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | M1 covers most cache identity primitives, but unresolved implementation manifests do not satisfy spec `R26` or test spec `VIC-T008`. |
| Test coverage | concern | `scripts/test-validation-cache.py` covers resolved implementation manifests, path normalization, input-surface hashes, policy manifests, local cache key matching, and selector routing, but misses the required unresolved-manifest case. |
| Edge cases | concern | Named edge case `EC23`/`VIC-T008` is not directly proven. |
| Error handling | concern | Missing or unparseable manifest inputs currently collapse to omitted imports or missing markers instead of cache-disabled state. |
| Architecture boundaries | pass | The cache helper remains separate from lifecycle execution, and M1 does not add validator cache skipping. |
| Compatibility | pass | Selector registration is narrow to the new validation-cache surface and explicit selected CI proves deterministic routing. |
| Security/privacy | pass | Path normalization rejects absolute, home, URL, hostname-like, credential-bearing, env-like, glob, and escaping paths; tracked evidence avoids local cache contents. |
| Derived artifact currency | pass | No generated outputs are changed. |
| Unrelated changes | pass | The implementation diff is scoped to the validation-idempotency artifacts, cache helper/tests, and selector route needed by the new script surface. |
| Validation evidence | concern | Recorded validation is relevant and credible for covered behavior, but it cannot prove the missing unresolved-manifest edge case. |

## No-Finding Rationale

Not applicable. One material finding requires review-resolution before M1 can close.

## Milestone Handoff

- Reviewed milestone: M1. Cache identity primitives and local cache contract.
- Review status: changes-requested.
- Milestone state after review: resolution-needed.
- Required review-resolution: yes, for `VIC-CR-M1-R1-F1`.
- Remaining in-scope implementation milestones: M1 pending review-resolution; M2, M3, and M4 remain planned.
- Next stage: review-resolution for M1.
- Final closeout readiness: not ready; M1 is unresolved, M2 through M4 are not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.
