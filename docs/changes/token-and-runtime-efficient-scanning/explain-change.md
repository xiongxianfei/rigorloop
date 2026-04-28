# Token and Runtime Efficient Scanning Explain Change

## Summary

M1 adds the bounded extraction guidance required by the approved token and runtime efficient scanning spec. M2 shapes the first named script output, `python scripts/build-adapters.py --version <version> --check`, so normal adapter drift output is summary-first and bounded while `--verbose` keeps complete diagnostics available. M3 makes adapter drift collection inspect `dist/adapters/manifest.yaml` before filesystem confirmation and reports manifest contract problems as `manifest-error`. M4 closes the implementation slice by regenerating derived outputs, running selected validation, release validation, lifecycle validation, and broad smoke. The first-pass `code-review` returned `clean-with-notes`, `verify` passed with verdict `ready`, and PR-stage CI repair routes `scripts/test-adapter-distribution.py` through deterministic adapter checks.

## Problem

RigorLoop agents and contributors repeatedly inspect large files, generated artifacts, validation logs, and review evidence. Before this change, the repository did not give enough explicit guidance or script behavior for starting from bounded evidence, reusing parsed state inside a command, and avoiding high-volume normal output. The result was higher token usage, slower repeated scans, and harder-to-review transcripts even when the underlying validation was correct.

The selected proposal direction was bounded extraction plus lightweight scan reuse: keep reviewability and full detail available, but make concise, ID-based, failure-focused evidence the default first path.

## Decision trail

- Proposal: `docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md`
- Proposal option selected: Option 4, standardize bounded extraction plus lightweight scan reuse.
- Spec: `specs/token-and-runtime-efficient-scanning.md`
- Test spec: `specs/token-and-runtime-efficient-scanning.test.md`
- Architecture/ADR decision: no separate architecture artifact was required because the helper work stays in-process, adapter-family scoped, dependency-free, and non-persistent.
- Plan: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
- Milestones completed: M1, add bounded extraction and skill guidance; M2, shape adapter drift check output; M3, add manifest-first adapter inspection; M4, align generated output, lifecycle artifacts, and final validation
- Requirements covered through M4: `R1`-`R37`. First-pass `code-review`, `verify`, and `explain-change` are complete; PR handoff remains a separate workflow stage.

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
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Classifies `scripts/test-adapter-distribution.py` as adapter-owned and adds selector regression coverage for explicit and PR-mode routing. | Hosted PR CI runs `scripts/ci.sh --mode pr`; changed adapter regression scripts must select deterministic adapter checks instead of blocking on manual routing. | `python scripts/test-select-validation.py`, `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` |
| Change-local and plan artifacts | Records M4 generated-output alignment, selector proof, release validation, lifecycle validation, and broad-smoke evidence. | Satisfies `T16`, `AC9`, and `AC11` without changing runtime behavior after M3. | M4 pass-gate commands and `bash scripts/ci.sh --mode broad-smoke` |

## Aligned-surface audit

| Surface | Decision | Rationale |
| --- | --- | --- |
| `AGENTS.md` | unaffected with rationale | It already points to `CONSTITUTION.md`, specs, active plans, and workflow docs; M1 updates those lower-level workflow surfaces without changing repository instruction precedence. |
| `CONSTITUTION.md` | unaffected with rationale | M1 changes operational evidence-collection guidance, not the repository's source-of-truth order, lifecycle policy, or governing principles. |
| `specs/rigorloop-workflow.md` | unaffected with rationale | The approved M1 scope names contributor workflow guidance and scan-sensitive skills; durable workflow-spec changes are not required for this first milestone. |
| Manifest-first adapter inspection | implemented | M3 reads and validates `dist/adapters/manifest.yaml` before generated-file traversal and keeps canonical expected files plus filesystem comparison in the proof path. |
| Generated `.codex/skills/` and `dist/adapters/` | synchronized through generators | M4 reran `python scripts/build-skills.py` and `python scripts/build-adapters.py --version 0.1.1`; no generated diff remained. |
| Release metadata | validated | M4 changed no release metadata content, but `python scripts/validate-release.py --version v0.1.1` passed as the release validation proof. |

## Review and verification outcomes

- First-pass `code-review`
  - Status: `clean-with-notes`
  - Result: no blocking or required-change findings.
  - Durable location: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
  - Recommended next stage: `verify`
- `verify`
  - Verdict: `ready`
  - Result: no blockers, no stale lifecycle drift, no generated-output drift, and no missing validation evidence.
  - Broad smoke: passed with unrelated baseline warnings for older draft proposal files outside this change.
  - Durable location: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
  - Recommended next stage: `explain-change`
- `explain-change`
  - Status: complete.
  - Result: this durable artifact links the proposal, requirements, implementation areas, tests, validation, review, verification, alternatives, scope limits, and PR handoff readiness.
  - Recommended next stage: `pr`

## Review Resolution Summary

No material review findings exist for this slice. The first-pass `code-review` result was `clean-with-notes` with zero unresolved items, so no `review-resolution.md` closeout artifact is required.

## Alternatives Rejected

- Broad output and repeated full-file reads as the default: rejected in the proposal because it keeps token and runtime costs high and buries relevant evidence.
- Chat-discipline-only guidance: rejected because it is inconsistent, hard to test, and does not improve repository-owned scripts.
- Persistent indexing or caching in the first slice: rejected because the approved first slice defers persistent cache behavior until measurement justifies the complexity.
- Changing validation semantics, selected check coverage, or command exit behavior while shaping output: rejected by the proposal and spec non-goals.
- Hand-editing generated `.codex/skills/` or `dist/adapters/`: rejected because generated outputs must remain reproducible from canonical sources and existing generator commands.
- Creating a top-level `docs/explain/` artifact: rejected because this ordinary non-trivial change already has the required change-local explanation surface.

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
- `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py` originally produced the expected selector blocked/manual-routing result for `scripts/test-adapter-distribution.py`; the direct manual route passed.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_drift_entries_classify_generated_output_failures AdapterDistributionTests.test_manifest_first_inspection_precedes_filesystem_confirmation AdapterDistributionTests.test_manifest_errors_are_structured_and_displayed_completely` failed before implementation because the M3 manifest-first helper and manifest-error drift entries were not implemented.
- `python scripts/test-adapter-distribution.py` passed with 56 tests after M3.
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/build-adapters.py --version 0.1.1 --check --verbose`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/build-skills.py`
- `python scripts/build-adapters.py --version 0.1.1`
- `python scripts/select-validation.py --mode explicit` with the M4 concrete path set originally selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, and `selector.regression`; it blocked only on the expected manual route for `scripts/test-adapter-distribution.py`.
- `bash scripts/ci.sh --mode explicit` with the supported M4 path set executed the selected checks successfully.
- `python scripts/validate-release.py --version v0.1.1`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md`
- `bash scripts/ci.sh --mode broad-smoke`
- `python scripts/select-validation.py --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
- `bash scripts/ci.sh --mode explicit --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/plan.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
- `python scripts/select-validation.py --mode explicit --path scripts/build-adapters.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py --path scripts/validation_selection.py` passed after PR-stage CI repair, selecting `adapters.regression`, `adapters.drift`, `adapters.validate`, and `selector.regression` with no blocking results.
- `bash scripts/ci.sh --mode explicit --path scripts/test-adapter-distribution.py`
- `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`

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
- M4 performs generated-output, release, artifact-lifecycle, selector, and broad-smoke validation without adding runtime behavior.
- Generated `.codex/skills/` and `dist/adapters/` were produced through existing generator commands.
- No new external dependency, parser boundary, or persistent cache is introduced. PR-mode CI behavior changes only through repository-owned selector routing for an adapter-owned script path.

## Risks and Follow-ups

- Persistent cache behavior remains deferred until a later measurement-backed proposal updates or supersedes the spec.
- Broader parser helpers outside the adapter drift family remain out of scope and require architecture review before adoption.
- Hosted CI is the remaining external confirmation after push; local repo-owned PR-mode validation now passes instead of relying on a manual-routing exception.
- PR body preparation and PR opening remain owned by the `pr` stage.

## Readiness

M1-M4 implementation, first-pass `code-review`, `verify`, and `explain-change` are complete. The branch is `branch-ready`, and this explanation is ready for PR handoff. The next stage is `pr`; direct `$explain-change` execution stops before opening or preparing the PR.
