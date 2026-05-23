# Code Review M1 R2 - Validation Idempotency and Cache-Hit Safety

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1 post-resolution commit `b831913`
Reviewed milestone: M1. Cache identity primitives and local cache contract
Reviewed artifact: scripts/validation_cache.py
Review date: 2026-05-23
Recording status: recorded
Status: approved

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M1. Cache identity primitives and local cache contract
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3, and M4 planned
- Required review-resolution: no
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commits `aeb81bd` and `b831913`, with focus on the M1 cache identity implementation and the `VIC-CR-M1-R1-F1` resolution.
- Tracked governing branch state: proposal, approved spec, ADR, active plan, test spec, review log, review-resolution, and M1 review records are present in the branch.
- Governing artifacts: `specs/validation-idempotency-and-cache-hit-safety.md`, `specs/validation-idempotency-and-cache-hit-safety.test.md`, `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`, and `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md`.
- Validation evidence inspected: `python scripts/test-validation-cache.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/test-select-validation.py`, change metadata validation, artifact lifecycle validation, selected CI for the validation cache surface, review artifact closeout, and whitespace validation recorded in the active plan and change metadata.

## Diff Summary

M1 adds `scripts/validation_cache.py`, direct cache identity tests, and a narrow selector route for the validation-cache helper/test surface. The post-resolution diff makes implementation-manifest construction fail closed for missing entrypoints, unresolved repository-local imports, unparseable repository-local helpers, and unresolved manifest-generator identity. It adds direct tests for those unresolved-manifest cases while preserving standard-library and third-party exclusion. M1 still does not integrate runtime cache skipping into the lifecycle validator.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | M1 implements cache identity primitives and local cache eligibility only; no runtime cache skip or Workstream B behavior is introduced. |
| Test coverage | pass | `scripts/test-validation-cache.py` covers command family, command/path normalization, duplicate path rejection, input-surface markers, implementation and policy manifests, local cache matching, and unresolved implementation-manifest failures. |
| Edge cases | pass | The previously missing `VIC-T008` / spec `R26` edge case is directly covered by missing-entrypoint, unresolved `scripts.*` import, and unparseable helper tests. |
| Error handling | pass | Implementation-manifest failures raise stable `CacheIdentityError.code` values and include explicit cache-ineligibility diagnostics. |
| Architecture boundaries | pass | Cache identity remains isolated in `scripts/validation_cache.py`; lifecycle validator execution behavior is unchanged in M1. |
| Compatibility | pass | Standard-library and third-party imports remain excluded, and selector routing is bounded to `validation_cache.regression`. |
| Security/privacy | pass | Path normalization rejects unsafe local/remote/credential-bearing values, and this milestone records no local cache contents as lifecycle evidence. |
| Derived artifact currency | pass | No generated outputs are changed. |
| Unrelated changes | pass | The implementation and review-resolution diff is scoped to validation idempotency artifacts, cache helper/tests, and selector routing needed for the new cache surface. |
| Validation evidence | pass | Recorded and reviewer-run validation includes cache regression, lifecycle regression, selector regression, change metadata validation, artifact lifecycle validation, review artifact closeout, selected CI for validation-cache paths, and whitespace checks. |

## No-Finding Rationale

The M1 implementation now satisfies the approved first-slice contract for deterministic cache identity primitives. The only M1 code-review finding, `VIC-CR-M1-R1-F1`, is resolved by failing closed when implementation identity cannot be resolved and by adding direct tests for the previously missing unresolved-manifest edge case. The remaining work is intentionally deferred to M2 through M4.

## Residual Risks

- M1 does not prove runtime cache-hit behavior, formal cache-hit evidence writing, closeout metadata enforcement, or Workstream A measurement; those are planned for M2 through M4.
- Import discovery remains a conservative first-slice implementation surface and should be re-reviewed when runtime cache skipping is integrated in M2.

## Milestone Handoff

- Reviewed milestone: M1. Cache identity primitives and local cache contract.
- Review status: clean-with-notes.
- Milestone state after review: closed.
- Required review-resolution: no.
- Remaining in-scope implementation milestones: M2, M3, and M4 remain planned.
- Next stage: implement M2.
- Final closeout readiness: not ready; M2 through M4 are not implemented or reviewed, final validation has not run, explain-change and verify are not recorded, and PR handoff is not prepared.
