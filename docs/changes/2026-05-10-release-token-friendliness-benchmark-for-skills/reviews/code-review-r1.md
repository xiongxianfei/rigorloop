# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1 metadata schema and validator
Status: changes-requested
Date: 2026-05-11

## Review Inputs

- Diff range: `ed5d21d`
- Review surface: committed M1 implementation and tracked governing artifacts.
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Plan milestone: `docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md`, M1.
- Architecture: `docs/architecture/system/architecture.md`
- Validation evidence recorded in M1 commit and active plan.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Diff Summary

M1 adds a standalone token-cost metadata validator at `scripts/validate-token-cost-report.py`, fixture-backed validator tests at `scripts/test-token-cost-report-validation.py`, valid report fixtures under `tests/fixtures/token-cost/reports/`, and lifecycle artifacts for the accepted proposal, spec, architecture update, plan, and test spec. The active plan marks M1 as `review-requested`.

## Findings

### RTF-CR1 - RC reuse metadata is not validated

Finding ID: RTF-CR1
Severity: major
Dimension: spec alignment, test coverage, edge cases

Evidence:

- The approved spec requires `rc_reuse` when a final release reuses or refers to an RC benchmark: `R2c` in `specs/release-token-friendliness-benchmark-for-skills.md`.
- The approved spec requires RC reuse metadata to include `reused_from`, `benchmark_relevant_changes_since_rc`, `checked_by`, `checked_surface`, and `rationale`: `R22a` in `specs/release-token-friendliness-benchmark-for-skills.md`.
- The test spec assigns RC reuse coverage to M1's validator test surface: `T15` in `specs/release-token-friendliness-benchmark-for-skills.test.md`.
- `scripts/validate-token-cost-report.py` only checks the base top-level sections in `validate_report` and does not mention `rc_reuse`.
- `scripts/test-token-cost-report-validation.py` accepts a final waiver whose reason says there were no benchmark-relevant changes since a passing RC run, but the fixture contains no `rc_reuse` metadata.

Problem:

A final release waiver can pass with an RC-based rationale but without the required RC reuse decision surface. That means the validator does not enforce who checked benchmark-relevant changes, what surfaces were checked, or whether rerun/waiver rules were applied.

Required outcome:

The standalone validator and tests must enforce RC reuse metadata when final-release metadata reuses, refers to, or waives based on RC benchmark evidence.

Safe resolution:

Add validator coverage for `rc_reuse`:

- require `rc_reuse` when a final `dynamic_runtime.status: waived` uses RC/no-benchmark-relevant-change evidence or when metadata explicitly references RC reuse;
- validate `reused_from`, `benchmark_relevant_changes_since_rc`, `checked_by`, `checked_surface`, and `rationale`;
- when `benchmark_relevant_changes_since_rc: false`, require the rationale or checked-surface field to name the specified surfaces from `R22c`;
- when `benchmark_relevant_changes_since_rc: true`, require either rerun evidence or a valid waiver path;
- add passing and failing fixture tests for both true and false cases.

Owner: implementer
Owning stage: implement M1

### RTF-CR2 - Markdown report link/name requirement is not validated

Finding ID: RTF-CR2
Severity: major
Dimension: spec alignment, test coverage, validation evidence

Evidence:

- `R1c` requires the Markdown report to link to or name the YAML metadata file.
- `R24a` says `scripts/validate-token-cost-report.py` owns report links.
- The implementation checks only that `report.report_markdown` exists; `validate_report` calls `require_existing_repo_path(report.get("report_markdown"), "report.report_markdown", errors)` and does not inspect the Markdown file content.
- `scripts/test-token-cost-report-validation.py` has no negative fixture proving that a Markdown report missing the YAML metadata name fails.

Problem:

A release can pass standalone token-cost validation with Markdown that exists but does not identify the structured YAML gate metadata. That violates the human/report and machine/gate pairing required by the spec.

Required outcome:

The standalone validator must verify that the Markdown report names or links the YAML metadata file.

Safe resolution:

After resolving `report.report_markdown`, read the Markdown report and require it to contain the metadata file basename or repo-relative metadata path. Add a negative test that removes the YAML reference from the Markdown fixture and asserts the validator fails with a clear `report.report_markdown` error.

Owner: implementer
Owning stage: implement M1

## Checklist Coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | M1 misses RC reuse validation and Markdown link validation required by `R2c`, `R22`, and `R1c`. |
| Test coverage | block | Validator tests do not include RC reuse true/false fixtures or Markdown-without-YAML-link failure. |
| Edge cases | block | RC reuse and benchmark-relevant-change edge cases from the test spec are not directly proved. |
| Error handling | concern | Current field-path errors are useful, but missing RC reuse/report-link branches mean invalid states are accepted. |
| Architecture boundaries | pass | The implementation keeps validation standalone and avoids `validate-release.py`/`release-verify.sh`, matching the M1/M5 boundary. |
| Compatibility | pass | Existing token-cost measurement tests still pass, and historical release validation was not wired in M1. |
| Security/privacy | pass | Raw JSONL omission and sanitized evidence paths are validated without requiring private raw JSONL. |
| Derived artifact currency | pass | No generated adapter output was edited for M1. |
| Unrelated changes | pass | The implementation stays within the lifecycle artifacts and M1 validator/test surface. |
| Validation evidence | concern | Reported commands passed, but they do not cover the missing RC reuse and Markdown link requirements. |

## Review Status

changes-requested

## Recommended Next Stage

Review-resolution for M1, then implement fixes for RTF-CR1 and RTF-CR2 before rerunning code-review.

This was a direct code-review request. There is no automatic downstream handoff beyond recording the required review state.
