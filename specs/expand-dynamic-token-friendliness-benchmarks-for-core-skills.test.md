# Expand Dynamic Token-Friendliness Benchmarks for Core Skills Test Spec

## Status

- active

## Related spec and plan

- Spec: [Expand Dynamic Token-Friendliness Benchmarks for Core Skills](expand-dynamic-token-friendliness-benchmarks-for-core-skills.md), approved.
- Existing benchmark spec: [Release Token-Friendliness Benchmark for Skills](release-token-friendliness-benchmark-for-skills.md), approved.
- Existing benchmark test spec: [Release Token-Friendliness Benchmark for Skills Test Spec](release-token-friendliness-benchmark-for-skills.test.md), active.
- Architecture: [Canonical system architecture](../docs/architecture/system/architecture.md), updated for v2 benchmark coverage, required benchmark context, result quality, and claimed optional coverage gates.
- Plan: [Expand Dynamic Token-Friendliness Benchmarks for Core Skills](../docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md), approved by plan-review R2.
- Change metadata: [change.yaml](../docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml).
- Review records:
  - `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/proposal-review-r2.md`
  - `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/plan-review-r2.md`

## Testing strategy

- Use manifest and fixture contract tests for `benchmarks/token-cost/manifest.yaml`, required core prompt files, transition carryover prompts, optional extended benchmark declarations, and scenario fixture shape.
- Use runner dry-run integration tests for v2 manifest group loading and benchmark enumeration without requiring the Codex CLI.
- Use standalone token-cost validator tests for v2 coverage metadata, per-run result-quality schema, required benchmark context, claimed optional coverage gates, waiver roles, warning codes, v1 compatibility, and report evidence references.
- Use release-validation integration tests for changed public skill detection, generated adapter traceback, required benchmark context generation, in-process delegation to token-cost validation, and invalid governed metadata blocking.
- Use report metadata fixture tests for the first v2 baseline, preserved pre-transition v1 evidence, overlap-comparison metadata, and Markdown coverage table requirements.
- Use manual review only for live Codex output correctness and result-quality decisions in the first v2 implementation. Manual result-quality evidence must still be structured in YAML.
- Do not add structured expected-output automation in this slice. The test spec records where manual result-quality review is required and where later automation may attach.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
|---|---|---|
| `R1`, `R1a`-`R1d` | `T1`, `T11`, `T16` | Suite id, v1/v2 comparison metadata, and v2 baseline behavior. |
| `R2`, `R2a`-`R2d` | `T2`, `T3`, `T18` | Required core benchmark ids, skill mapping, prompt paths, and no-edit prompt policy. |
| `R3`, `R3a`-`R3b` | `T1`, `T4`, `T11`, `T16` | Transition carryover required status and later optional move as metadata behavior. |
| `R4`, `R4a`-`R4b` | `T1`, `T5`, `T7`, `T8`, `T12` | Optional extended set, optional missing behavior, warning-only optional runs, and claimed coverage gates. |
| `R5`, `R5a`-`R5e` | `T5`, `T6`, `T18` | First optional `architecture-review` prompt and scenario fixture behavior. |
| `R6`, `R6a`-`R6c` | `T6`, `T19` | Self-contained scenario fixture and overlay trigger policy. |
| `R7`, `R7a`-`R7c` | `T7`, `T11`, `T16`, `T18` | YAML coverage metadata and Markdown coverage table. |
| `R8`, `R8a`-`R8l` | `T7`, `T8`, `T9`, `T12`, `T18` | Per-run result-quality schema, required benchmark gates, optional warning behavior, and claimed optional gates. |
| `R9`, `R9a`-`R9f` | `T9`, `T18` | Role-scoped result-quality waivers and approver identity validation. |
| `R10`, `R10a`-`R10e` | `T13`, `T14`, `T18` | Release validation changed-surface ownership and generated adapter trace behavior. |
| `R11`, `R11a`-`R11b` | `T13`, `T15`, `T18` | Optional benchmarks required by changed public skills and missing benchmark follow-up warnings. |
| `R12`, `R12a`-`R12e` | `T10`, `T12`, `T15`, `T18` | Required benchmark context schema, effective required-set calculation, and in-process validation. |
| `R13`, `R13a`-`R13d` | `T10`, `T15`, `T18` | CLI context YAML loading, transient default behavior, and tracked evidence path. |
| `R14`, `R14a`-`R14e` | `T11`, `T16`, `T18` | Pre-transition v1 preservation and first v2 report identity. |
| `R15`, `R15a`-`R15e` | `T8`, `T12`, `T18` | Optional warning codes and required blocker code distinction. |
| `R16`, `R16a` | `T17` | Claude Code and opencode dynamic benchmarks remain optional. |
| `R17`, `R17a` | `T12`, `T16` | Token thresholds remain warning-only unless evidence, portability, or required result quality fails. |

## Example coverage map

| Example | Test IDs | Notes |
|---|---|---|
| `E1` | `T1`, `T2`, `T4`, `T7`, `T11`, `T16` | Final v2 release requires core and transition carryover evidence with result quality or valid waivers. |
| `E2` | `T11`, `T16` | Existing v1 `v0.1.1` evidence is preserved and referenced by the v2 report. |
| `E3` | `T8`, `T12` | Optional `architecture-review` failure warns when unclaimed and not required. |
| `E4` | `T13`, `T15` | Public `architecture-review` skill change makes the benchmark required. |
| `E5` | `T14`, `T15` | Generated adapter path traces to the canonical owning skill. |
| `E6` | `T10`, `T15` | Required benchmark context works in process and through CLI YAML. |
| `E7` | `T5`, `T6`, `T18` | `architecture-review` scenario reviews canonical architecture directly and does not demand a change-local delta. |

## Edge case coverage

- First v2 report has no comparable v2 predecessor: `T11`, `T16`.
- Existing `v0.1.1` v1 report path collides with the first v2 report: `T11`, `T16`.
- `v0.1.1` is already finalized before v2 lands: `T11`, manual release-version check.
- Required benchmark run is missing: `T12`.
- Required benchmark result quality is `not-reviewed`: `T7`, `T12`.
- Required benchmark result quality is `fail` or `inconclusive`: `T8`, `T9`, `T12`.
- Optional benchmark is run and fails but is unclaimed and not required: `T8`, `T12`.
- Optional benchmark is claimed as release coverage and fails: `T8`, `T12`.
- Optional benchmark becomes required because its public skill changed: `T13`, `T15`.
- Public skill changes but no benchmark exists: `T13`, `T15`.
- Generated adapter output changes without canonical skill changes: `T14`, `T15`.
- Required benchmark context YAML is generated for debugging only: `T10`, `T15`.
- Required benchmark context is tracked as release evidence: `T10`, `T16`.
- Waiver role is vague or unsupported: `T9`.
- Waiver approver identity is empty: `T9`.
- `architecture-review` output requires a change-local architecture delta: `T5`, manual result-quality review.
- Three scenario fixtures duplicate the same base files: `T19`.
- Token thresholds are exceeded without missing evidence: `T12`, `T16`.

## Test cases

### T1. V2 manifest declares suite groups and comparison identity

- Covers: `R1`, `R1a`-`R1d`, `R3`, `R4`, `R7`, `E1`
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/manifest.yaml`.
- Steps:
  - Parse the manifest through the runner or measurement test helper.
  - Assert the suite id is `skill-token-runtime-v2`.
  - Assert `previous_suite_id: skill-token-runtime-v1` or equivalent v2 comparison metadata is present where the manifest owns suite identity.
  - Assert the manifest separates required core, transition carryover, and optional extended benchmark groups.
  - Assert v1/v2 totals are not marked directly comparable.
- Expected result:
  - The manifest gives the runner and validator enough structure to distinguish required, carryover, and optional benchmark groups.
- Failure proves:
  - The suite identity or group model is ambiguous and release validation cannot apply v2 gates.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T2. Required core benchmarks and skill mappings are complete

- Covers: `R2`, `R2a`, `E1`
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/manifest.yaml`.
- Steps:
  - Assert required core benchmark ids are exactly `workflow-route`, `proposal-short`, `plan-handoff`, `implement-handoff`, `code-review-small`, `explain-change-summary`, `verify-final-pack`, and `pr-handoff`.
  - Assert each id maps to the expected public skill: `workflow`, `proposal`, `plan`, `implement`, `code-review`, `explain-change`, `verify`, and `pr`.
  - Assert each required core benchmark uses `tool: codex` and points to a prompt fixture under `benchmarks/token-cost/prompts/`.
- Expected result:
  - The required core suite covers the standard delivery path.
- Failure proves:
  - A core workflow skill can ship without release-required dynamic benchmark coverage.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T3. Required core prompt fixtures are output-bounded and no-edit

- Covers: `R2b`-`R2d`
- Level: integration
- Fixture/setup:
  - Required core prompt files under `benchmarks/token-cost/prompts/`.
- Steps:
  - Assert every required core prompt file exists.
  - Assert each prompt names a focused skill task or expected skill route.
  - Assert each prompt includes `Do not edit files` or stricter no-write wording.
  - Assert each prompt includes an `Output only:` block or equivalent bounded output instruction.
- Expected result:
  - Prompt fixtures remain short, fixture-backed, single-skill focused, and safe for dry-run or live execution.
- Failure proves:
  - Dynamic benchmarks may measure accidental editing or unbounded output instead of skill runtime behavior.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T4. Transition carryover benchmarks remain required for first v2 release

- Covers: `R3`, `R3a`, `R3b`, `E1`
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/manifest.yaml`.
  - Valid v2 report fixture.
- Steps:
  - Assert `architecture-no-impact` and `learn-no-durable-lesson` appear in the transition carryover required group.
  - Validate a report fixture missing either carryover benchmark and assert failure unless a valid waiver exists.
  - Validate report metadata that records transition carryover status.
- Expected result:
  - The first v2 transition release preserves continuity with v1 baseline prompts.
- Failure proves:
  - Baseline prompts can be removed silently and comparability evidence is lost.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - `scripts/test-token-cost-report-validation.py`

### T5. Architecture-review optional benchmark prompt checks canonical-review behavior

- Covers: `R5`, `R5d`, `R5e`, `E7`
- Level: integration and manual
- Fixture/setup:
  - `benchmarks/token-cost/prompts/architecture-review.md`.
  - `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`.
- Steps:
  - Assert the prompt forbids file edits.
  - Assert the prompt bounds output to review surface, review status, findings, whether a change-local architecture delta is required, and next stage or required action.
  - During manual result-quality review of a live run, fail the run if output requires a change-local architecture delta before reviewing the canonical architecture update.
- Expected result:
  - The benchmark directly tests the simplified architecture-review contract.
- Failure proves:
  - The optional benchmark may pass while preserving the old rejected change-local-delta requirement.
- Automation location:
  - Prompt contract in `scripts/test-token-cost-measurement.py`.
  - Manual result-quality evidence in release report YAML.

### T6. Architecture-review scenario fixture is separate and self-contained

- Covers: `R5a`-`R5c`, `R6`, `R6a`-`R6c`, `E7`
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`.
- Steps:
  - Assert the fixture path exists and is not the generic `minimal-public-project` fixture.
  - Assert it includes `AGENTS.md`, `VISION.md`, `README.md`, `docs/workflows.md`, canonical architecture files, ADR-not-required note, change metadata, explain-change evidence, a spec, and a tiny source file.
  - Assert no change-local architecture delta file is required by the fixture.
  - Assert no shared overlay mechanism is required before the three-scenario duplication trigger.
- Expected result:
  - The first architecture-review scenario is isolated, downstream-shaped, and reviewable without hidden fixture composition.
- Failure proves:
  - The benchmark can pollute the base fixture or depend on unapproved overlay complexity.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T7. Result-quality schema is required for each dynamic v2 run

- Covers: `R7`, `R8`, `R8a`-`R8e`
- Level: unit
- Fixture/setup:
  - Valid v2 report fixture under `tests/fixtures/token-cost/reports/`.
  - Negative fixtures omitting result-quality fields.
- Steps:
  - Validate the fixture with `scripts/validate-token-cost-report.py`.
  - Assert every dynamic run includes `result_quality.status`, `reviewed_by`, `review_surface`, `reviewed_at`, `criteria`, `notes`, and `blockers`.
  - Assert every criterion includes `id`, `expectation`, `result`, and `notes`.
  - Assert invalid status or criterion result enums fail.
  - Assert required benchmark `not-reviewed` fails.
- Expected result:
  - Manual quality review is structured enough to gate release evidence.
- Failure proves:
  - Token-cost reports can claim low cost without proving benchmark correctness.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T8. Required, optional, and claimed optional result-quality gates differ correctly

- Covers: `R4a`, `R8f`-`R8l`, `R15`, `R15a`-`R15e`, `E3`
- Level: unit
- Fixture/setup:
  - V2 report fixtures for required benchmark `pass`, `fail`, `inconclusive`, and `not-reviewed`.
  - Optional unclaimed benchmark fixtures for `fail` and `inconclusive`.
  - Claimed optional benchmark fixtures for missing, failed, inconclusive, not-reviewed, and valid pass states.
- Steps:
  - Assert required final-release `fail` and `inconclusive` fail without valid waiver.
  - Assert optional unclaimed `fail` emits `optional-benchmark-failed` warning and does not block.
  - Assert optional unclaimed `inconclusive` emits `optional-benchmark-inconclusive` warning and does not block.
  - Assert claimed optional coverage is treated like required coverage.
  - Assert claimed optional failures do not use optional warning codes.
- Expected result:
  - Optional benchmark problems remain visible without becoming blockers unless the report claims coverage or changed-skill policy requires them.
- Failure proves:
  - Reports can either over-block optional evidence or advertise failed coverage as passing.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T9. Required benchmark result-quality waivers are role-scoped

- Covers: `R8g`, `R9`, `R9a`-`R9f`
- Level: unit
- Fixture/setup:
  - V2 final release fixture with a required benchmark `fail` or `inconclusive`.
  - Waiver variants for approved and invalid roles.
- Steps:
  - Assert valid waiver roles are exactly `release-owner`, `release-manager`, and `repository-maintainer`.
  - Assert empty `approved_by`, empty `approval_surface`, empty `approved_at`, empty `reason`, and missing evidence fail.
  - Assert vague roles such as `owner`, `admin`, `maintainer`, and `approved` fail.
  - Assert first-slice validation does not require GitHub collaborator lookup.
- Expected result:
  - Required benchmark exceptions are explicit, review-visible, and role-scoped.
- Failure proves:
  - Release-required benchmark failures can pass with ambiguous or unauditable approvals.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T10. Required benchmark context validates by object and CLI YAML

- Covers: `R12`, `R12a`-`R12e`, `R13`, `R13a`-`R13d`, `E6`
- Level: unit and integration
- Fixture/setup:
  - Required benchmark context object fixture.
  - Equivalent YAML context fixture.
  - V2 report fixture satisfying the context.
- Steps:
  - Validate report metadata through the validator API with `required_benchmark_context`.
  - Validate the same report through CLI using `--required-benchmark-context <yaml>`.
  - Assert the effective required set is computed from `core + transition_carryover + required_due_to_changes[*].benchmark`.
  - Assert a duplicated precomputed effective required set is not required.
  - Assert tracked context evidence, when present, uses `docs/reports/token-cost/releases/<release-version>.required-benchmarks.yaml`.
- Expected result:
  - Release validation can call the validator in process, while maintainers can debug the same contract by YAML.
- Failure proves:
  - Required benchmark decisions can drift between release validation and standalone validation.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T11. V2 report preserves pre-transition v1 evidence

- Covers: `R1b`-`R1d`, `R3`, `R14`, `R14a`-`R14e`, `E2`
- Level: integration
- Fixture/setup:
  - Existing or fixture `docs/reports/token-cost/releases/v0.1.1.yaml` with `skill-token-runtime-v1`.
  - Expected preserved paths:
    - `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md`
    - `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml`
  - V2 report fixture for `v0.1.1`.
- Steps:
  - Assert pre-transition v1 evidence is preserved before the canonical v2 report takes `v0.1.1` paths.
  - Assert v2 comparison metadata references the preserved v1 YAML path.
  - Assert Markdown report includes an overlap-comparison note.
  - Assert suite totals are marked non-comparable while overlapping prompts may be informational.
- Expected result:
  - Historical v1 evidence is not overwritten or confused with the v2 baseline.
- Failure proves:
  - Release evidence identity is ambiguous and comparability claims are unsafe.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`
  - `scripts/test-token-cost-measurement.py` if report fixtures live with measurement evidence.

### T12. Token-cost validator blocks missing required evidence but keeps thresholds warning-only

- Covers: `R7`, `R8`, `R15`, `R17`, `R17a`
- Level: unit
- Fixture/setup:
  - V2 report fixtures with complete evidence.
  - Negative fixtures for missing analyzer summary, missing run evidence, missing result quality, and missing required benchmark.
  - Warning fixtures for input-token, command-output, static skill-size, full-file-read, and repeated-read threshold warnings.
- Steps:
  - Validate each fixture.
  - Assert missing or invalid required evidence fails.
  - Assert token threshold warnings do not fail when evidence is complete and required result quality passes.
  - Assert portability failure remains a blocker through existing v1 validator behavior.
- Expected result:
  - Release gates focus on evidence integrity, portability, and required result correctness, not hard token regression thresholds.
- Failure proves:
  - The validator either misses release-blocking evidence gaps or turns warning-only thresholds into hard gates.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T13. Canonical public skill changes require existing optional benchmarks

- Covers: `R10`, `R10a`, `R10b`, `R11`, `R11a`, `R11b`, `E4`
- Level: integration
- Fixture/setup:
  - Release validation changed-path fixture containing `skills/architecture-review/SKILL.md`.
  - Benchmark manifest containing `architecture-review`.
  - Changed-path fixture for a public skill with no benchmark.
- Steps:
  - Run release-validation changed-surface helper or focused integration test.
  - Assert `architecture-review` appears in `required_benchmarks.required_due_to_changes`.
  - Assert public skill changes with no benchmark record warning/follow-up evidence and do not block unless full coverage is claimed.
- Expected result:
  - Optional benchmark status becomes release-required when the corresponding public skill changes and a benchmark exists.
- Failure proves:
  - Public skill changes can ship without available dynamic coverage, or missing benchmark gaps can over-block release.
- Automation location:
  - Focused release-validation integration test, likely `scripts/test-adapter-distribution.py` or a new release-validation test file selected in M4.

### T14. Generated adapter changes trace to owning canonical skills

- Covers: `R10c`-`R10e`, `E5`
- Level: integration
- Fixture/setup:
  - Changed-path fixture containing `dist/adapters/codex/.agents/skills/architecture-review/SKILL.md`.
  - Optional variants for Claude Code and opencode adapter paths.
  - Canonical changed and canonical unchanged cases.
- Steps:
  - Run release-validation changed-surface helper or focused integration test.
  - Assert generated adapter path maps to `skills/architecture-review/SKILL.md`.
  - Assert generated adapter changes do not independently define benchmark ownership.
  - Assert generated output changes without canonical changes route to adapter drift or regeneration evidence unless a benchmark reason is recorded.
- Expected result:
  - Release validation uses canonical skill ownership and does not invent benchmark ownership from generated output alone.
- Failure proves:
  - Release validation can require the wrong benchmark or miss adapter drift.
- Automation location:
  - Focused release-validation integration test, likely `scripts/test-adapter-distribution.py` or a new release-validation test file selected in M4.

### T15. Release validation passes required benchmark context and propagates token-cost failures

- Covers: `R10a`, `R11`, `R12`, `R13`, `R15`, `E4`, `E5`, `E6`
- Level: integration
- Fixture/setup:
  - Otherwise-valid release fixture.
  - Invalid governed v2 token-cost metadata fixture.
  - Required benchmark context with core, transition carryover, and changed-skill-required entries.
- Steps:
  - Run `validate_release_output(...)` or the focused release-validation integration test.
  - Assert release validation constructs or passes `required_benchmark_context`.
  - Assert invalid token-cost metadata causes release validation failure through token-cost validator delegation.
  - Assert CLI/debug context YAML is transient by default and tracked only when explicitly cited as release evidence.
- Expected result:
  - Release validation decides what is required, token-cost validation checks the report, and release validation propagates failures.
- Failure proves:
  - Release validation can find token-cost metadata without enforcing the v2 gate contract.
- Automation location:
  - Focused release-validation integration test, likely `scripts/test-adapter-distribution.py` or a new release-validation test file selected in M4.

### T16. V2 final report metadata and Markdown coverage table validate

- Covers: `R1`, `R7`, `R7a`-`R7c`, `R8`, `R14`, `R17`, `E1`, `E2`
- Level: integration and manual
- Fixture/setup:
  - `docs/reports/token-cost/releases/v0.1.1.yaml`.
  - `docs/reports/token-cost/releases/v0.1.1.md`.
  - Preserved pre-transition v1 report files when applicable.
- Steps:
  - Validate v2 YAML with `scripts/validate-token-cost-report.py`.
  - Assert Markdown names or links the YAML metadata file.
  - Assert Markdown includes a benchmark coverage table.
  - Assert YAML records coverage groups, run evidence, analyzer evidence, manual result quality, warnings, blockers, and comparison metadata.
  - Assert live benchmark result-quality decisions are manually reviewed and recorded.
- Expected result:
  - The release report is both human-readable and machine-checkable.
- Failure proves:
  - Reviewers cannot connect the Markdown report to the YAML gate evidence or trust claimed coverage.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - Manual Markdown review during M5.

### T17. Non-Codex dynamic benchmarks remain optional

- Covers: `R16`, `R16a`
- Level: unit
- Fixture/setup:
  - V2 report fixture with Codex runs only.
  - Optional metadata fixture mentioning Claude Code or opencode dynamic sections.
- Steps:
  - Validate a Codex-only v2 report and assert it passes when other required evidence is complete.
  - Validate optional Claude Code or opencode sections and assert they do not become required.
- Expected result:
  - The v2 release gate does not require unsupported dynamic runners.
- Failure proves:
  - The expansion accidentally broadens release-blocking runtime requirements beyond Codex.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T18. Runner dry-run enumerates v2 benchmarks and report commands remain scoped

- Covers: `R2`, `R5`, `R7`, `R8`, `R9`, `R10`-`R15`, `E1`, `E7`
- Level: smoke
- Fixture/setup:
  - Updated manifest and prompt fixtures.
  - Token-cost validator and release-validation scripts.
- Steps:
  - Run `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`.
  - Assert dry-run output includes required core, transition carryover, and optional benchmark ids without executing Codex.
  - Run `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/validate-token-cost-report.py scripts/validate-release.py`.
  - Run the milestone-specific validator and release-validation tests.
- Expected result:
  - The benchmark suite can be inspected and validated without live Codex execution.
- Failure proves:
  - The release benchmark cannot be reliably reviewed before expensive or environment-dependent runs.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - Milestone validation commands in the active plan.

### T19. Fixture duplication trigger remains visible but not implemented early

- Covers: `R6a`-`R6c`
- Level: manual and integration
- Fixture/setup:
  - Existing `minimal-public-project` fixture.
  - `minimal-public-project-architecture-review` fixture.
  - Any future `minimal-public-project-proposal-review` fixture.
- Steps:
  - During M2, assert only two duplicated scenario-style fixtures exist and no overlay mechanism is required.
  - If a third duplicated scenario fixture is added, assert the implementation records a follow-up proposal or review-visible decision for shared base-fixture or overlay work.
- Expected result:
  - Fixture duplication stays simple until duplication itself becomes a maintenance risk.
- Failure proves:
  - The implementation either adds overlay complexity too early or ignores the agreed duplication trigger.
- Automation location:
  - `scripts/test-token-cost-measurement.py` for current fixture count checks if practical.
  - Manual plan/review check for future trigger.

## Fixtures and data

- `benchmarks/token-cost/manifest.yaml`: v2 suite manifest with required core, transition carryover, and optional extended groups.
- `benchmarks/token-cost/prompts/plan-handoff.md`: required core prompt fixture.
- `benchmarks/token-cost/prompts/explain-change-summary.md`: required core prompt fixture.
- `benchmarks/token-cost/prompts/pr-handoff.md`: required core prompt fixture.
- `benchmarks/token-cost/prompts/architecture-review.md`: optional extended prompt fixture.
- `benchmarks/token-cost/fixtures/minimal-public-project/`: existing generic downstream fixture.
- `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`: separate scenario fixture for canonical architecture review without a change-local delta.
- `tests/fixtures/token-cost/reports/`: report metadata fixtures for valid v2, invalid required evidence, optional warning evidence, claimed optional coverage, waivers, and preserved v1 report behavior.
- Required benchmark context fixtures may live under `tests/fixtures/token-cost/contexts/` unless implementation chooses a narrower existing fixture location.
- Release-validation changed-surface fixtures may live with the selected release validation test file.

## Mocking/stubbing policy

- Do not require live Codex execution in ordinary automated tests.
- Use `--dry-run` for runner enumeration and command construction.
- Use small synthetic JSONL or YAML fixtures for analyzer and validator behavior.
- Stub changed-path inputs for release-validation context tests instead of depending on a specific local git history.
- Do not mock the token-cost validator in release validation propagation tests; the integration test must prove real delegation or real imported validation logic.
- Do not mock filesystem existence for report evidence when a small tracked fixture can prove path checks.

## Migration or compatibility tests

- Validate that existing `skill-token-runtime-v1` report fixtures still pass the v1 validator path after v2 support is added.
- Validate that v2 reports use a new baseline and do not compute strict v1-to-v2 suite total deltas.
- Validate preservation of pre-transition v1 `v0.1.1` evidence when v2 becomes canonical for the same release path.
- Validate that existing raw-or-sanitized analyzer evidence behavior remains unchanged.
- Validate that `.codex/skills/` remains rejected as the public benchmark skill source through the existing v1 runner metadata rule.

## Observability verification

- Validator errors must name field paths, benchmark ids, skill ids, report paths, and waiver fields where applicable.
- Release-validation integration tests must assert the error includes either `token-cost report validation failed` or the propagated token-cost validator error.
- Dry-run output must show enough benchmark ids and output paths for maintainers to see required versus optional coverage.
- Release metadata must expose coverage groups, result-quality status, warning codes, blocker codes, and optional benchmark warning details.

## Security/privacy verification

- Required benchmark context must use repo-relative public paths when tracked as evidence.
- Context YAML must be transient by default in CLI and CI flows unless a release owner cites it as evidence.
- Result-quality notes must summarize review findings and must not require private raw model output.
- Scenario fixtures must avoid private repository-specific data and local machine paths.
- Existing raw JSONL omission tests remain authoritative for sanitized evidence behavior.

## Performance checks

- Runner tests use dry-run by default, so automated validation stays fast and does not consume Codex tokens.
- Live Codex benchmarks are manual or release-preparation evidence in M5, not ordinary unit tests.
- Token thresholds remain warning-only in v2 validation unless evidence is missing, invalid, structurally blocked, portability fails, or required result quality fails without waiver.
- Required benchmark context generation should use changed-path inputs and avoid broad repository scans beyond release validation's existing surface analysis.

## Manual QA checklist

- Review the `architecture-review` live output, if run, and confirm it reviews the canonical architecture update directly.
- Confirm no live benchmark output edited files when prompts forbid edits.
- Confirm required benchmark `result_quality.criteria` matches the prompt's requested output shape and skill ownership.
- Confirm optional benchmark failures are not summarized as coverage pass.
- Confirm the Markdown report coverage table matches YAML coverage metadata.
- Confirm preserved v1 report paths remain linked from v2 comparison metadata when v2 targets `v0.1.1`.
- Confirm any waiver is specific, review-visible, role-scoped, and evidence-backed.

## What not to test

- Do not automate semantic expected-output checks in the first v2 implementation; manual result-quality review is the approved first-slice mechanism.
- Do not require live Claude Code or opencode dynamic benchmark runs.
- Do not test skill text optimization or token reduction; this change expands coverage and evidence contracts.
- Do not test a shared base-fixture overlay implementation before the duplication trigger is reached.
- Do not validate waiver approver identity against GitHub collaborators, CODEOWNERS, or maintainer registries in this slice.
- Do not add hard token regression gates.

## Uncovered gaps

- None that block implementation.
- Structured expected-output automation remains a deliberate follow-up after manual result-quality criteria stabilize.
- Shared base-fixture or overlay work remains a deliberate follow-up after three duplicated scenario fixtures or a duplication-related review finding.

## Next artifacts

- implement

## Follow-on artifacts

None yet.

## Readiness

Active for implementation.

This test spec defines the proof surface for M1-M5. Implementation may begin with M1 after this artifact is committed with the active plan state.
