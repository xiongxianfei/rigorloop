# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Contributor code-review
Target: commit `389fe43` (`M3: validate v2 token benchmark coverage metadata`)
Status: changes-requested

## Review inputs

- Diff: `git show --name-only --format=fuller HEAD`
- Commit: `389fe43`
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Test spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md`
- Plan: `docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- Validation evidence in plan: M3 targeted v2 validator tests, full token-cost report validation tests, v1 report compatibility validation, py_compile, change metadata validation, artifact lifecycle validation, and diff checks.

## Diff summary

M3 adds `validate_token_cost_report(...)`, CLI `--required-benchmark-context`, required benchmark context validation, `skill-token-runtime-v2` benchmark coverage validation, per-run `result_quality` validation, required benchmark presence gates, role-scoped result-quality waiver checks, claimed optional coverage gates, and optional warning-code checks.

The tests add generated v2 metadata/context fixtures and cover CLI context loading, in-process context loading, required result-quality failures, waiver role checks, claimed optional failures, unclaimed optional warnings, and changed-skill-required optional benchmarks.

## Findings

### EDTF-CR1 - Optional run result-quality can be hidden by mismatched coverage metadata

Finding ID: EDTF-CR1
Severity: major

Evidence:

- `scripts/validate-token-cost-report.py` builds `optional_statuses` from `benchmark_coverage.optional_run[*].result_quality_status` in `validate_benchmark_coverage(...)`.
- `scripts/validate-token-cost-report.py` then calls `validate_result_quality(...)` for optional dynamic runs, but for non-required runs it validates only schema and does not compare the run's `result_quality.status` against the coverage entry for that benchmark.
- `validate_optional_warning_coverage(...)` decides whether an unclaimed optional benchmark requires `optional-benchmark-failed` or `optional-benchmark-inconclusive` from `optional_statuses`, not from the actual dynamic run.
- Direct proof: a report whose `architecture-review` dynamic run has `result_quality.status: fail`, but whose coverage entry says `result_quality_status: pass`, currently validates successfully:

```text
0
/tmp/tmp8rql3ynm.yaml: valid token-cost report metadata
```

Problem:

This violates the optional benchmark warning contract. R8h says optional extended benchmarks with `fail` or `inconclusive` must warn when they are not required and not claimed as release coverage. R15a-R15b define the warning codes, and R15d requires benchmark identity in separate fields. With the current implementation, the metadata can hide the failed optional run by marking the coverage summary as `pass`, so release evidence can advertise clean optional behavior while the actual run says otherwise.

Required outcome:

The validator must reject or otherwise block inconsistent v2 metadata where `benchmark_coverage.optional_run[*].result_quality_status` does not match the corresponding dynamic run's `result_quality.status`.

Safe resolution:

Track each dynamic run's `result_quality.status` by `dynamic_runtime.runs[*].id` during v2 validation, compare it against `benchmark_coverage.optional_run[*].result_quality_status`, and validate optional warning requirements from the reconciled actual run status. Add focused tests for:

- optional unclaimed run `fail` with coverage `pass` must fail;
- optional unclaimed run `inconclusive` with coverage `pass` must fail;
- optional unclaimed run `fail` with matching coverage `fail` and `optional-benchmark-failed` warning passes;
- optional unclaimed run `inconclusive` with matching coverage `inconclusive` and `optional-benchmark-inconclusive` warning passes.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | EDTF-CR1 violates R8h and R15 warning behavior because optional dynamic run quality can be hidden by mismatched coverage metadata. |
| Test coverage | block | Existing tests set `optional_quality_status` and coverage `result_quality_status` to the same value, so they do not cover mismatched summary-vs-run metadata. |
| Edge cases | block | The named optional warning edge case is incomplete when coverage and dynamic run status disagree. |
| Error handling | pass | CLI context file loading and parse failures have clear error handling; no separate error-path finding found. |
| Architecture boundaries | pass | M3 keeps changed-surface detection in release validation scope and only validates supplied context/report metadata. |
| Compatibility | pass | Existing v1 report validation still passes, and v2 checks are gated by suite id or explicit context. |
| Security/privacy | pass | No secret material, maintainer-local path exposure, or network validation dependency added. |
| Derived artifact currency | pass | No generated `.codex/skills/` or `dist/adapters/` output is touched. |
| Unrelated changes | pass | Diff is scoped to validator, validator tests, and workflow evidence for M3. |
| Validation evidence | concern | Recorded validation is relevant, but it does not include the mismatched optional coverage/run-status case identified in EDTF-CR1. |

## Outcome

Review status: changes-requested

Reviewed milestone: M3. Token-cost validator v2 metadata and context support

Milestone closeout: resolution-needed

Required review-resolution: EDTF-CR1

Recommended next stage: review-resolution for EDTF-CR1, then implement the accepted M3 fix and rerun code-review M3.
