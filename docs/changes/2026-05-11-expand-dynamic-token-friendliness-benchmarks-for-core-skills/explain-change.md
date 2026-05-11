# Explain Change

## Summary

This change expands the token-cost benchmark suite from `skill-token-runtime-v1` through the M5 transition-report slice of `skill-token-runtime-v2`.

M1 adds the required core benchmark fixtures for `plan`, `explain-change`, and `pr`, keeps the v1 `architecture` and `learn` prompts as transition carryover benchmarks, and records the optional extended benchmark set in the manifest without implementing optional prompt fixtures yet.

M2 adds the first optional extended benchmark, `architecture-review`, using a separate scenario fixture that reviews a canonical architecture update directly and intentionally does not include a change-local architecture delta.

M3 teaches the standalone token-cost report validator to understand v2 release metadata: coverage groups, manual result-quality review, required benchmark context, role-scoped result-quality waivers, claimed optional gates, changed-skill-required benchmarks, and warning-only optional failures.

M4 integrates the required benchmark context into release validation. Release validation now builds the context from changed canonical skill paths and generated adapter skill paths, passes it to the token-cost validator in process for v2 reports, and preserves the existing v1 pre-transition report validation path until M5 creates the final v2 evidence. The EDTF-CR2 review fix adds maintainer-facing changed-surface input to `validate-release.py` so the real release command can pass those changed paths.

M5 preserves the earlier `v0.1.1` `skill-token-runtime-v1` report as pre-transition evidence, creates the canonical `v0.1.1` `skill-token-runtime-v2` YAML and Markdown report, records manual result-quality review for the ten required core and transition carryover runs, and stores sanitized analyzer summaries as durable evidence while leaving raw JSONL outside the repository.

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
- `scripts/adapter_distribution.py`: adds release-side required benchmark context construction, canonical skill change detection, generated adapter skill path ownership tracing, generated-only adapter drift metadata, missing-benchmark follow-up metadata, and in-process token-cost report validation for v2 report metadata.
- `scripts/test-adapter-distribution.py`: adds release-validation integration coverage for changed public skills, generated adapter tracebacks, generated-only adapter drift, missing optional benchmark follow-up metadata, and v2 token-cost validation failure propagation.
- `scripts/validate-release.py`: adds repeated `--changed-path` and line-based `--changed-paths-file` arguments, normalizes and deduplicates changed paths, and passes them into release validation.
- `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.{md,yaml}`: preserves the previous v1 release-token report as historical continuity evidence.
- `docs/reports/token-cost/releases/v0.1.1.{md,yaml}`: replaces the canonical release report with the first v2 transition report, including coverage metadata, result-quality evidence, overlap comparison, and warning-only token-cost signals.
- `docs/reports/token-cost/runs/v0.1.1/*-run1.analysis.yaml`: stores sanitized analyzer summaries for all ten required v2 transition runs.

## Validation

- `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_manifest_lists_v2_prompt_groups_and_fixtures`
- `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_architecture_review_optional_prompt_and_fixture_are_self_contained`
- `python scripts/test-token-cost-measurement.py`
- `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`
- `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_result_quality_and_required_context_are_enforced_by_cli TokenCostReportValidatorTests.test_v2_required_benchmark_context_is_supported_in_process TokenCostReportValidatorTests.test_v2_required_benchmark_result_quality_waiver_roles_are_enforced TokenCostReportValidatorTests.test_v2_claimed_optional_coverage_is_gated_and_unclaimed_optional_warns TokenCostReportValidatorTests.test_v2_changed_skill_required_context_requires_optional_benchmark`
- `python scripts/test-token-cost-report-validation.py`
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
- `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_required_benchmark_context_requires_changed_skill_benchmark AdapterDistributionTests.test_required_benchmark_context_traces_generated_adapter_paths AdapterDistributionTests.test_generated_only_adapter_change_traces_to_required_dynamic_benchmark AdapterDistributionTests.test_changed_public_skill_without_benchmark_records_warning_follow_up`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_validation_passes_required_context_to_token_cost_validation`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_v2_final_release_validation_requires_changed_surface_input AdapterDistributionTests.test_generated_only_adapter_change_traces_to_required_dynamic_benchmark AdapterDistributionTests.test_generated_adapter_changed_path_requires_missing_benchmark_through_release_validation AdapterDistributionTests.test_release_validation_passes_required_context_to_token_cost_validation AdapterDistributionTests.test_changed_skill_with_complete_v2_metadata_passes_release_validation`
- `python scripts/test-adapter-distribution.py`
- `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py`
- `python scripts/validate-release.py --version v0.1.1`
- `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-v2-runs-v0.1.1`
- `python scripts/measure-skill-tokens.py`
- `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-v2-dry-run-v0.1.1`
- `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py scripts/validate-token-cost-report.py scripts/validate-release.py scripts/adapter_distribution.py`
- `python scripts/validate-release.py --version v0.1.1 --changed-paths-file /tmp/rigorloop-empty-changed-paths.txt`
- `bash scripts/ci.sh --mode explicit --path docs/reports/token-cost/releases/v0.1.1.yaml --path docs/reports/token-cost/releases/v0.1.1.md --path docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml --path docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md --path docs/reports/token-cost/runs/v0.1.1/workflow-route-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/plan-handoff-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/implement-handoff-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/code-review-small-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/explain-change-summary-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/verify-final-pack-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/pr-handoff-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/architecture-no-impact-run1.analysis.yaml --path docs/reports/token-cost/runs/v0.1.1/learn-no-durable-lesson-run1.analysis.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`
- `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases`
- `git diff --check -- scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py scripts/test-token-cost-report-validation.py tests docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`

## Notes

The dry-run command wrote synthetic output under `docs/reports/token-cost/runs/test/`; those generated validation files were removed after each dry-run command completed so they are not committed as release evidence.

The M5 live run kept raw JSONL under `/tmp/rigorloop-token-v2-runs-v0.1.1` and tracked only sanitized analyzer summaries. The report records `implement-handoff` command-output amplification as a `high-warning` because R17 keeps token thresholds warning-only for this expansion.
