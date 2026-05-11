# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Contributor code-review
Target: commit `0acd3c6` (`M4: integrate required benchmark context into release validation`)
Status: changes-requested

## Review inputs

- Diff: `git show --name-only --format=fuller HEAD`
- Commit: `0acd3c6`
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Test spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md`
- Plan: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Architecture: `docs/architecture/system/architecture.md`
- Change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- Validation evidence in plan: focused required benchmark context tests, full adapter distribution tests, full token-cost report validator tests, release validation command, py_compile, change metadata validation, artifact lifecycle validation, and diff checks.

## Diff summary

M4 adds release-side required benchmark context helpers to `scripts/adapter_distribution.py`, including canonical skill path detection, generated adapter skill path ownership tracing, manifest-backed skill-to-benchmark mapping, missing-benchmark follow-up metadata, and in-process token-cost validator invocation for v2 reports.

The tests add focused coverage for canonical `architecture-review` changes, generated adapter path tracebacks, generated-only adapter drift metadata, missing benchmark follow-up metadata, and v2 token-cost failure propagation when `validate_release_output(...)` is called with explicit `changed_paths`.

## Findings

### EDTF-CR2 - Real release-validation command does not analyze changed surfaces

Finding ID: EDTF-CR2
Severity: major

Evidence:

- `scripts/validate-release.py` still invokes `validate_release_output(args.version)` without a changed-path input or any release diff range.
- `scripts/adapter_distribution.py` defines `validate_release_output(..., changed_paths=())`, so the default release-validation path supplies an empty changed-path set.
- `_validate_token_cost_report(...)` only passes changed surfaces to `build_required_benchmark_context(...)` through that `changed_paths` argument.
- `build_required_benchmark_context(...)` only detects canonical public skill changes and generated adapter skill tracebacks by iterating over the provided `changed_paths`.
- The M4 integration test proves delegation only for an explicit API call that passes `changed_paths=("skills/architecture-review/SKILL.md",)`.

Problem:

The approved contract says release validation owns changed public skill detection. R10b requires release validation to detect changed canonical public skill files, R10c requires generated adapter skill path tracebacks, R11a requires adding an existing benchmark to `required_benchmarks.required_due_to_changes`, and R12 requires release validation to pass the required benchmark context to token-cost validation.

With the current implementation, the actual release command planned for real validation, `python scripts/validate-release.py --version v0.1.1`, cannot detect changed canonical or generated skill paths because it neither computes nor accepts those paths. A v2 release report validated through the CLI can therefore omit a changed-skill-required optional benchmark unless some non-CLI caller manually passes `changed_paths`.

Required outcome:

The release-validation path used by maintainers and CI must provide release changed-surface data to required benchmark context generation before token-cost validation runs.

Safe resolution:

Add an explicit release changed-surface source to the release validation path. Acceptable first-slice options are:

- add a CLI/debug flag such as `--changed-paths-file` or `--changed-path` and require it for v2 final validation when changed-skill decisions are needed;
- or implement a small release change-surface helper that derives changed paths from the approved release diff range and passes them into `validate_release_output(...)`.

Then add focused proof that the real release-validation entry point, not only a direct helper call, constructs a required benchmark context from changed canonical and generated skill paths and propagates the required benchmark failure when the changed-skill benchmark is missing.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | EDTF-CR2 violates R10b, R10c, R11a, and R12 on the actual release-validation command path. |
| Test coverage | block | The M4 tests cover helper/API calls with explicit `changed_paths`, but not the real `validate-release.py` entry point or a required changed-surface source. |
| Edge cases | block | The named changed public skill and generated adapter traceback edge cases are not enforced through the maintainer-facing release command. |
| Error handling | concern | There is no error or warning when v2 release validation runs without changed-surface input. |
| Architecture boundaries | pass | The implementation keeps changed-surface ownership in release validation and leaves token-cost metadata validation in the token-cost validator. |
| Compatibility | pass | The v1 pre-transition report path still validates and v2-specific context is gated by suite id. |
| Security/privacy | pass | No network identity lookup, secret handling, or credential exposure was introduced. |
| Derived artifact currency | pass | No generated `.codex/skills/` or `dist/adapters/` output was edited. |
| Unrelated changes | pass | The diff is scoped to release validation helpers, release validation tests, and M4 workflow evidence. |
| Validation evidence | concern | Recorded tests are relevant but do not prove the real release command path receives changed-surface data. |

## Outcome

Review status: changes-requested

Reviewed milestone: M4. Release validation required benchmark context integration

Milestone closeout: resolution-needed

Required review-resolution: EDTF-CR2

Recommended next stage: review-resolution for EDTF-CR2, then implement the accepted M4 fix and rerun code-review M4.
