# Code Review M4 R2

Review ID: code-review-m4-r2
Stage: code-review
Round: 2
Reviewer: Contributor code-review
Target: commit `3f91722` (`M4: pass changed surfaces through release validation CLI`)
Status: clean-with-notes

## Review inputs

- Diff: `git show --stat --oneline HEAD`
- Commit: `3f91722`
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Test spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md`
- Plan: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Prior review: `reviews/code-review-m4-r1.md`
- Review resolution: `review-resolution.md#code-review-m4-r1`
- Change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- Reviewer-rerun validation: focused EDTF-CR2 release validation CLI/API tests.

## Diff summary

The M4 rerun target resolves EDTF-CR2 by adding maintainer-facing changed-surface inputs to `scripts/validate-release.py` through repeated `--changed-path` values and a line-based `--changed-paths-file`.

Release validation now distinguishes omitted changed-surface input from an explicitly empty changed-path set, blocks final `skill-token-runtime-v2` validation when changed-surface input is missing, and passes normalized changed paths into required benchmark context generation. The context builder also records generated-only adapter skill changes as benchmark-required when a benchmark exists, while preserving generated trace metadata.

The test suite adds direct coverage for the release CLI forwarding changed paths, final v2 validation blocking when no changed-surface input is provided, generated adapter changed paths requiring the matching benchmark through release validation, and a complete changed-skill v2 metadata path passing.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | The rerun target satisfies R10-R12 by keeping changed-surface ownership in release validation and passing required benchmark context into token-cost validation. |
| Test coverage | pass | Focused tests prove CLI changed-path forwarding, v2 final no-input blocking, generated adapter path enforcement, and the valid changed-skill metadata pass path. |
| Edge cases | pass | The prior EDTF-CR2 edge cases are directly covered for canonical and generated changed-surface inputs. |
| Error handling | pass | Final v2 release validation now emits a clear blocker when changed-surface input is omitted. |
| Architecture boundaries | pass | Token-cost validation still validates supplied report metadata and required context; release validation owns changed-surface context construction. |
| Compatibility | pass | The v1 pre-transition report path remains compatible because v2-only required-context behavior is gated by suite id. |
| Security/privacy | pass | The change introduces local path inputs only and does not add network collaborator lookup, credentials, or secret handling. |
| Derived artifact currency | pass | No generated `.codex/skills/` or `dist/adapters/` output was edited. |
| Unrelated changes | pass | The diff is scoped to release validation CLI/context behavior, tests, and M4 workflow evidence. |
| Validation evidence | pass | Reviewer reran the focused EDTF-CR2 release validation tests; all passed. The implementation record also cites full adapter distribution, token-cost validator, py_compile, and artifact validations. |

## No-finding rationale

No blocking findings were found because the accepted EDTF-CR2 finding is resolved on the real `validate-release.py` entry point, the release validation API still receives the changed paths, missing changed-skill benchmarks now fail through token-cost delegation, and the focused rerun directly proves the named failure and pass paths.

## Residual risks

- Automatic release diff-range discovery remains a later improvement; the first slice intentionally uses explicit changed-path input.
- Final v2 report evidence and preserved v1 transition report handling remain M5 scope.

## Outcome

Review status: clean-with-notes

Reviewed milestone: M4. Release validation required benchmark context integration

Milestone closeout: close M4

Required review-resolution: none

Recommended next stage: implement M5
