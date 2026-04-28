# Token and Runtime Efficient Scanning Explain Change

## Summary

M1 adds the bounded extraction guidance required by the approved token and runtime efficient scanning spec. M2 shapes the first named script output, `python scripts/build-adapters.py --version <version> --check`, so normal adapter drift output is summary-first and bounded while `--verbose` keeps complete diagnostics available. M3 makes adapter drift collection inspect `dist/adapters/manifest.yaml` before filesystem confirmation and reports manifest contract problems as `manifest-error`.

## Decision trail

- Proposal: `docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md`
- Spec: `specs/token-and-runtime-efficient-scanning.md`
- Test spec: `specs/token-and-runtime-efficient-scanning.test.md`
- Plan: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
- Milestones completed: M1, add bounded extraction and skill guidance; M2, shape adapter drift check output; M3, add manifest-first adapter inspection
- Requirements covered through M3: `R1`-`R37`. Final M4 repository-wide alignment and broad-smoke validation remain open.

## Diff rationale by area

| Area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `docs/workflows.md` | Adds bounded extraction, normal output budgets, verbose expansion, and full-file read escalation guidance. | Satisfies `R1`-`R4`, `R10`-`R15`, and `R34` for contributor-visible workflow guidance. | `T1`, `python scripts/test-skill-validator.py` |
| `skills/` | Adds concise summary and stable-ID first evidence guidance plus full-file read rules to the 19 scan-sensitive canonical skills. | Satisfies `R5`, `R6`, and `R35` without changing stage order or skill trigger behavior. | `T2`, `python scripts/test-skill-validator.py` |
| `.codex/skills/` | Regenerated from canonical `skills/`. | Keeps the local Codex runtime mirror derived instead of hand-edited. | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `dist/adapters/` | Regenerated from canonical skills and adapter templates. | Keeps public adapter packages aligned after canonical skill wording changed. | `python scripts/build-adapters.py --version 0.1.1`, `python scripts/build-adapters.py --version 0.1.1 --check` |
| `scripts/test-skill-validator.py` | Adds focused M1 contract tests. | Proves workflow and first-slice skill guidance carry the required efficiency rules. | Initial failing run, then passing targeted test |
| `scripts/adapter_distribution.py` | Adds structured `AdapterDriftEntry` records, generated-output and canonical-source categories, normal and verbose formatters, and a string-returning compatibility bridge for `collect_adapter_drift`. | Satisfies M2 output shaping and taxonomy requirements without changing drift detection semantics or adding a persistent cache. | `T5`, `T6`, `T8`, `T9`, `T10`, `T13`, `python scripts/test-adapter-distribution.py` |
| `scripts/build-adapters.py` | Routes `--check` through the shaped formatter and accepts `--check --verbose`; rejects `--verbose` without `--check`. | Gives the selected first script a default concise mode plus an explicit complete-detail escape hatch while keeping existing check identity. | `T4`, `T7`, `T14`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/build-adapters.py --version 0.1.1 --check --verbose` |
| `scripts/test-adapter-distribution.py` | Adds M2 coverage for clean output, bounded drift output, verbose determinism, generated-output categories, canonical-source categories, no persistent cache writes, output-size evidence, and CLI compatibility. | Proves the display change preserves actionable detail, complete verbose diagnostics, and command compatibility. | `python scripts/test-adapter-distribution.py` |
| `scripts/adapter_distribution.py` | Adds in-process manifest inspection before generated-file traversal and converts missing, malformed, inconsistent, version-mismatched, or stale manifest contract evidence into `manifest-error` drift entries. | Satisfies M3 manifest-first and manifest-error behavior while preserving filesystem drift confirmation for non-manifest files. | `T11`, `T12`, `python scripts/test-adapter-distribution.py` |
| `scripts/test-adapter-distribution.py` | Adds M3 coverage for manifest-before-filesystem call order, manifest-error normal and verbose display, and continued non-manifest missing/stale/unexpected detection. | Proves manifest evidence is used first but is not treated as authoritative over canonical sources or filesystem state. | Initial failing M3 targeted test run, then passing adapter regression suite |

## Aligned-surface audit

| Surface | Decision | Rationale |
| --- | --- | --- |
| `AGENTS.md` | unaffected with rationale | It already points to `CONSTITUTION.md`, specs, active plans, and workflow docs; M1 updates those lower-level workflow surfaces without changing repository instruction precedence. |
| `CONSTITUTION.md` | unaffected with rationale | M1 changes operational evidence-collection guidance, not the repository's source-of-truth order, lifecycle policy, or governing principles. |
| `specs/rigorloop-workflow.md` | unaffected with rationale | The approved M1 scope names contributor workflow guidance and scan-sensitive skills; durable workflow-spec changes are not required for this first milestone. |
| Manifest-first adapter inspection | implemented | M3 reads and validates `dist/adapters/manifest.yaml` before generated-file traversal and keeps canonical expected files plus filesystem comparison in the proof path. |
| Generated `.codex/skills/` and `dist/adapters/` | unaffected with rationale | M3 changes adapter drift inspection code and tests only; no canonical skill or adapter template changed, so generated output was checked but not regenerated. |

## Tests added or changed

- `scripts/test-skill-validator.py`
  - `test_workflow_guidance_defines_bounded_extraction_and_output_budgets`
  - `test_scan_sensitive_skills_include_summary_id_reasoning_and_full_file_rules`
- `scripts/test-adapter-distribution.py`
  - `test_adapter_drift_entries_classify_generated_output_failures`
  - `test_canonical_source_failures_are_structured_adapter_drift_entries`
  - `test_adapter_drift_collection_does_not_write_persistent_cache`
  - `test_clean_adapter_check_normal_output_is_summary_first`
  - `test_normal_adapter_drift_output_is_bounded_and_actionable`
  - `test_verbose_adapter_drift_output_includes_every_entry_deterministically`
  - `test_adapter_drift_normal_output_reports_over_budget_warning`
  - `test_adapter_drift_output_size_evidence_records_before_after_counts`
  - `test_build_adapters_cli_supports_verbose_check_only`
  - `test_manifest_first_inspection_precedes_filesystem_confirmation`
  - `test_manifest_errors_are_structured_and_displayed_completely`

## Validation evidence

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py`
- `python scripts/build-adapters.py --version 0.1.1`
- `python scripts/test-select-validation.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`
- `python scripts/select-validation.py --mode explicit` with the M1 authored path set selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; broad smoke was not required.
- `bash scripts/ci.sh --mode explicit` with the same M1 authored path set executed the selected checks successfully.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
- `git diff --check -- .`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
- `python scripts/build-adapters.py --version 0.1.1 --verbose` failed as expected with exit code 2 and a clear `--check` requirement.
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/test-select-validation.py`
- `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py` produced the expected selector blocked/manual-routing result for `scripts/test-adapter-distribution.py`; the direct manual route passed.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_drift_entries_classify_generated_output_failures AdapterDistributionTests.test_manifest_first_inspection_precedes_filesystem_confirmation AdapterDistributionTests.test_manifest_errors_are_structured_and_displayed_completely` failed before implementation because the M3 manifest-first helper and manifest-error drift entries were not implemented.
- `python scripts/test-adapter-distribution.py` passed with 56 tests after M3.
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
- `python scripts/validate-adapters.py --version 0.1.1`

M2 output-size evidence:

| Case | Legacy normal lines | Shaped normal lines |
| --- | ---: | ---: |
| clean adapter output | 1 | 4 |
| representative many-drift output | 35 | 26 |

Additional validation results are recorded in the active plan.

## Scope control

- M1 did not change adapter drift output, `--verbose` support, failure taxonomy, manifest-first collection, selected check coverage, or command exit behavior.
- M2 changes only adapter drift check output shape and structured reporting; it does not change selected check coverage, generated adapter validation semantics, or sync behavior.
- M3 implements manifest-first collection and `manifest-error` regression coverage.
- M3 does not perform final M4 generated-output, release, artifact-lifecycle, broad-smoke, or PR-readiness validation.
- Generated `.codex/skills/` and `dist/adapters/` were produced through existing generator commands.
- No new external dependency, parser boundary, persistent cache, or hosted CI behavior change is introduced.

## Readiness

M1-M3 are complete and ready for `code-review` as reviewable milestone slices. M4 remains open for the full initiative, so final `verify`, `explain-change`, and `pr` are not ready yet.
