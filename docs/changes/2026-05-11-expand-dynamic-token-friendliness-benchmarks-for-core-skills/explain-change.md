# Explain Change

## Summary

This change expands the token-cost benchmark suite from `skill-token-runtime-v1` through the M3 slice of `skill-token-runtime-v2`.

M1 adds the required core benchmark fixtures for `plan`, `explain-change`, and `pr`, keeps the v1 `architecture` and `learn` prompts as transition carryover benchmarks, and records the optional extended benchmark set in the manifest without implementing optional prompt fixtures yet.

M2 adds the first optional extended benchmark, `architecture-review`, using a separate scenario fixture that reviews a canonical architecture update directly and intentionally does not include a change-local architecture delta.

M3 teaches the standalone token-cost report validator to understand v2 release metadata: coverage groups, manual result-quality review, required benchmark context, role-scoped result-quality waivers, claimed optional gates, changed-skill-required benchmarks, and warning-only optional failures.

## Changed surfaces

- `benchmarks/token-cost/manifest.yaml`: declares `skill-token-runtime-v2`, v1 comparison metadata, required core benchmarks, transition carryover benchmarks, optional extended benchmark names, and the flat executable prompt list used by the current runner.
- `benchmarks/token-cost/prompts/plan-handoff.md`: adds the required core plan handoff prompt.
- `benchmarks/token-cost/prompts/explain-change-summary.md`: adds the required core explain-change summary prompt.
- `benchmarks/token-cost/prompts/pr-handoff.md`: adds the required core PR handoff prompt.
- `benchmarks/token-cost/prompts/workflow-route.md`: changes the existing prompt to use the same explicit `Output only:` shape enforced by the M1 prompt test.
- `benchmarks/token-cost/prompts/architecture-review.md`: adds the optional extended architecture-review prompt with bounded no-edit output.
- `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`: adds the separate downstream-style architecture-review scenario fixture with canonical architecture package, ADR-not-required note, change metadata, explain-change evidence, spec, diagrams, and tiny source file.
- `scripts/test-token-cost-measurement.py`: updates the manifest and prompt fixture contract test to enforce v2 suite identity, required core groups, transition carryover, optional extended declarations, prompt existence, no-edit instructions, and bounded output.
- `scripts/validate-token-cost-report.py`: adds the `validate_token_cost_report(...)` in-process API, `--required-benchmark-context` CLI flag, v2 benchmark coverage validation, per-run `result_quality` validation, required benchmark presence checks, required-benchmark waiver role validation, claimed optional gating, and optional warning-code checks while preserving v1 report compatibility.
- `scripts/test-token-cost-report-validation.py`: adds validator tests for v2 context loading by CLI and API, required benchmark result quality, allowed and rejected waiver roles, claimed optional blocking, changed-skill-required benchmarks, and unclaimed optional warning-only behavior.

## Validation

- `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_manifest_lists_v2_prompt_groups_and_fixtures`
- `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_architecture_review_optional_prompt_and_fixture_are_self_contained`
- `python scripts/test-token-cost-measurement.py`
- `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`
- `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_result_quality_and_required_context_are_enforced_by_cli TokenCostReportValidatorTests.test_v2_required_benchmark_context_is_supported_in_process TokenCostReportValidatorTests.test_v2_required_benchmark_result_quality_waiver_roles_are_enforced TokenCostReportValidatorTests.test_v2_claimed_optional_coverage_is_gated_and_unclaimed_optional_warns TokenCostReportValidatorTests.test_v2_changed_skill_required_context_requires_optional_benchmark`
- `python scripts/test-token-cost-report-validation.py`
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
- `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`
- `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases`

## Notes

The dry-run command wrote synthetic output under `docs/reports/token-cost/runs/test/`; those generated validation files were removed after each dry-run command completed so they are not committed as release evidence.
