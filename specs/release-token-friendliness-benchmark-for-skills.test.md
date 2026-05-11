# Release Token-Friendliness Benchmark for Skills Test Spec

## Status

- active

## Related spec and plan

- Spec: [Release Token-Friendliness Benchmark for Skills](release-token-friendliness-benchmark-for-skills.md), approved.
- Proposal: [Release Token-Friendliness Benchmark for Skills](../docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md), accepted.
- Architecture: [Canonical system architecture](../docs/architecture/system/architecture.md), updated for token-cost report validation, benchmark runner, analyzer summaries, and release validation integration.
- Plan: [Release Token-Friendliness Benchmark for Skills](../docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md), active and approved by plan-review R2.
- Change metadata: [change.yaml](../docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml).
- Review records:
  - `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/proposal-review-r2.md`
  - `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/plan-review-r2.md`

## Testing strategy

- Use focused unit tests for the standalone token-cost metadata validator, including schema version, required fields, enums, waiver states, incomplete non-final states, raw-or-sanitized evidence, comparison metadata, runner metadata, portability failures, and warning-only thresholds.
- Use fixture and contract tests for `benchmarks/token-cost/manifest.yaml`, prompt fixtures, and the minimal downstream fixture.
- Use runner unit or dry-run integration tests for temporary directory policy, public Codex adapter skill installation, output path construction, Codex command construction, analyzer invocation, and cleanup behavior without requiring the Codex CLI in ordinary test runs.
- Use analyzer unit tests for schema version 1 summary output, tracked raw JSONL identity, omitted raw JSONL identity, usage fields, command-output amplification, full-file-read signal classification, and false-positive avoidance.
- Use release report metadata fixtures for baseline, comparable previous release, RC reuse, waiver, optional non-Codex dynamic sections, warning-only regressions, and structural blockers.
- Use release validation integration tests only after M5 wires `scripts/validate-release.py` and `scripts/release-verify.sh`; M1 tests must stay standalone.
- Use manual checks only for live Codex benchmark execution and human-readable Markdown report quality because local contributors may not have Codex installed and exact token counts vary.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R4` | `T1`, `T2`, `T12`, `T16` | Report paths, Markdown/YAML pairing, schema version, required sections, enums, and Markdown summary shape. |
| `R5` | `T12`, `T18` | Static measurement evidence and default command in release metadata/report. |
| `R6`-`R7` | `T3`, `T4`, `T15`, `T16` | Final dynamic pass-or-waived rule, non-final incomplete metadata, and valid waiver reasons. |
| `R8`-`R9` | `T6`, `T7` | Benchmark manifest, seven prompts, no-edit prompt policy, and clean minimal downstream fixture. |
| `R10`-`R13` | `T8`, `T9`, `T10`, `T18` | Runner CLI, temp policy, public Codex skill source, JSONL output, analyzer invocation, and no Markdown generation. |
| `R14`-`R16` | `T5`, `T11`, `T12`, `T18` | Raw-or-sanitized run evidence, analyzer summary schema, run metadata, and release-level summary metrics. |
| `R17`-`R18` | `T11`, `T12`, `T13` | Command-output amplification and compound full-file-read signal classification. |
| `R19` | `T14`, `T16` | Public skill portability metadata and failure blocker. |
| `R20` | `T9`, `T16` | Runner invocation metadata and agreement with suite/run evidence. |
| `R21` | `T15` | First baseline, comparable previous release, and numeric delta rules. |
| `R22`-`R23` | `T15`, `T16`, `T18` | RC reuse metadata and benchmark-relevant change classification. |
| `R24`-`R26` | `T1`-`T5`, `T14`, `T16`, `T17` | Standalone validator ownership, release validation delegation, and structural/evidence blockers. |
| `R27`-`R28` | `T14`, `T16`, `T18` | Warning/high-warning thresholds and future hard-gate boundaries. |
| `R29` | `T16` | Optional Claude Code and opencode dynamic sections remain non-blocking in v1. |
| `R30` | `T10`, `T12` | No full Markdown report generator in the first implementation. |
| `R31` | `T17` | Plan milestone split remains reviewable and lifecycle-valid. |
| `R32` | `T12`, `T16` | Release notes link to the Token-Friendliness report. |
| `R33` | `T8`, `T17` | Public adapter output is used as benchmark input but never hand-edited. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T12`, `T16`, `T18` | Final release with complete static, dynamic, report, and metadata evidence. |
| `E2` | `T4`, `T15`, `T16` | Final waiver based on passing RC evidence and no benchmark-relevant changes. |
| `E3` | `T5`, `T11`, `T16` | Missing raw JSONL is valid only with sanitized evidence. |
| `E3a` | `T11` | Analyzer summary identity fields avoid private raw JSONL paths. |
| `E4` | `T1`, `T16` | Prose-only Markdown report fails release validation. |
| `E5` | `T8`, `T9` | Runner installs public adapter skills into a temporary fixture. |
| `E6` | `T8`, `T16` | `.codex/skills/` is rejected as the benchmark skill source. |
| `E7` | `T14`, `T16` | Token growth produces warning/high-warning, not v1 blockers. |
| `E8` | `T13`, `T14` | Large unbounded command output is recorded as warning/high-warning in v1. |
| `E9` | `T15` | First release metadata declares itself the baseline without fake deltas. |

## Edge case coverage

- No prior release report exists: `T15`.
- Prior report exists but is not comparable: `T15`.
- RC benchmark exists and no benchmark-relevant change occurred: `T15`.
- RC benchmark exists but benchmark-relevant change occurred: `T15`, `T16`.
- Codex unavailable for non-final work: `T3`.
- Final release attempts `blocked` or `not-run`: `T3`, `T16`.
- Raw JSONL too large or sensitive: `T5`, `T11`.
- Raw JSONL claimed tracked but missing: `T5`, `T16`.
- Analyzer cannot determine file length: `T13`.
- File at or under 80 lines is fully read: `T13`.
- Explicit whole-file review target or generated-output validation is justified: `T13`.
- Prompt accidentally allows edits: `T6`.
- Runner fails after temp creation: `T10`.
- Optional Claude Code or opencode data exists: `T16`.
- Static token totals increase while structure passes: `T14`, `T16`.
- Public portability fails while metrics improve: `T14`, `T16`.
- Markdown and YAML disagree: `T16`, manual report review.

## Test cases

### T1. Standalone token-cost metadata validator accepts the minimal valid schema

- Covers: `R1`, `R1a`-`R1d`, `R2`, `R2a`, `R2d`, `R3`, `R24`, `R24a`, `R24c`, `R26`
- Level: unit
- Fixture/setup:
  - Valid final-release YAML fixture under `tests/fixtures/token-cost/reports/valid-final-pass/`.
  - Matching Markdown report, manifest path, run evidence, analyzer summary, and release notes fixture paths where required.
- Steps:
  - Run `python scripts/validate-token-cost-report.py <valid-yaml>`.
  - Assert the command exits zero.
  - Assert the validator reports the release version and no blockers.
- Expected result:
  - A complete schema version 1 report passes standalone validation without invoking release validation.
- Failure proves:
  - The YAML gate cannot validate the primary release evidence contract.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T2. Metadata schema rejects missing required fields and invalid enums

- Covers: `R2a`-`R2d`, `R3a`-`R3c`, `R26a`
- Level: unit
- Fixture/setup:
  - Negative YAML fixtures missing each required top-level section or required field.
  - Negative YAML fixtures with invalid `dynamic_runtime.status`, `release_gate.result`, `verdict.result`, and `hard warning` severity.
- Steps:
  - Run the validator against each negative fixture.
  - Assert non-zero exit.
  - Assert the error includes the missing or invalid field path.
- Expected result:
  - Structural and enum errors fail clearly and point to the field to fix.
- Failure proves:
  - Release validation could accept unparsable, incomplete, or ambiguous gate metadata.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T3. Dynamic runtime status rules distinguish final and non-final releases

- Covers: `R6`, `R6a`-`R6h`, `R26a`
- Level: unit
- Fixture/setup:
  - Final release metadata with `dynamic_runtime.status: pass`.
  - Final release metadata with `blocked` and `not-run`.
  - Non-final or draft metadata with `blocked` or `not-run`, with and without `dynamic_runtime.incomplete`.
- Steps:
  - Validate each fixture.
  - Assert final `pass` succeeds when other evidence is complete.
  - Assert final `blocked` and `not-run` fail.
  - Assert non-final `blocked` and `not-run` pass only when `reason`, `owner`, `environment`, `follow_up`, and boolean `release_may_proceed` are present.
- Expected result:
  - Draft/RC incomplete states are reviewable, while final public releases require `pass` or valid `waived`.
- Failure proves:
  - The gate cannot enforce final-release dynamic benchmark requirements.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T4. Waiver metadata accepts only approved evidence-backed final waivers

- Covers: `R7`, `R7a`-`R7f`, `R22`, `E2`
- Level: unit
- Fixture/setup:
  - Valid waiver fixture with approved status, approving maintainer, approval surface, evidence, and RC no-benchmark-relevant-change rationale.
  - Invalid fixtures for missing approval, invalid reason, missing evidence, missing maintainer, and unexplained dynamic regression.
- Steps:
  - Run the token-cost validator against each fixture.
  - Assert valid waiver passes.
  - Assert invalid waivers fail with field-specific errors.
- Expected result:
  - Waivers are exceptional, explicit, approved, and evidence-backed.
- Failure proves:
  - Final release could silently skip required dynamic measurement.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T5. Raw JSONL and sanitized evidence contract is enforced

- Covers: `R14`, `R14a`-`R14d`, `R15i`-`R15k`, `E3`
- Level: unit
- Fixture/setup:
  - Run metadata fixture with tracked raw JSONL and analyzer summary.
  - Run metadata fixture with omitted raw JSONL, analyzer summary, sanitized summary, and omission reason.
  - Negative fixtures for missing JSONL when tracked, non-empty JSONL when omitted, missing omission reason, and missing sanitized evidence.
- Steps:
  - Validate each fixture.
  - Assert tracked raw JSONL requires a valid `evidence.jsonl`.
  - Assert omitted raw JSONL requires empty `evidence.jsonl`, non-empty reason, and tracked sanitized evidence.
- Expected result:
  - Missing raw JSONL is a blocker only when the sanitized evidence contract is not satisfied.
- Failure proves:
  - Release evidence is either too privacy-hostile or too easy to omit.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T6. Benchmark manifest and prompt fixtures satisfy first-suite contract

- Covers: `R8`, `R8a`-`R8e`, `R31`, edge case 15
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/manifest.yaml`.
  - `benchmarks/token-cost/prompts/*.md`.
- Steps:
  - Parse the manifest with repository lightweight YAML conventions or the runner manifest loader.
  - Assert suite id is `skill-token-runtime-v1`.
  - Assert the seven required benchmark ids exist.
  - Assert each entry has prompt path, tool, fixture, expected skill, expected result, and tags or equivalent classification.
  - Assert every prompt file exists and contains a no-edit instruction.
- Expected result:
  - The first benchmark suite is executable, reviewable, and edit-safe.
- Failure proves:
  - Dynamic benchmarks can drift from the approved release evidence contract.
- Automation location:
  - `scripts/test-token-cost-measurement.py` or `scripts/test-token-cost-report-validation.py`

### T7. Minimal public fixture remains clean and downstream-shaped

- Covers: `R9`, `R9a`-`R9d`
- Level: integration
- Fixture/setup:
  - `benchmarks/token-cost/fixtures/minimal-public-project/`.
- Steps:
  - Assert required files exist: `AGENTS.md`, `VISION.md`, `README.md`, `docs/workflows.md`, `docs/changes/.gitkeep`, and `src/example.txt`.
  - Assert fixture does not contain `.codex/skills/`, `.agents/skills/`, or generated adapter output.
  - Assert fixture file count and sample files remain small enough to make broad reads visible.
- Expected result:
  - The clean fixture represents a downstream project and remains unmutated/generated-output-free.
- Failure proves:
  - Benchmarks could measure repository internals or stale installed skills instead of user-like behavior.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T8. Runner installs public Codex skills and rejects repository-local mirror

- Covers: `R10`, `R10a`-`R10d`, `R20e`, `R33`, `E5`, `E6`
- Level: integration
- Fixture/setup:
  - Clean fixture.
  - Temporary output directory.
  - Public skill source path `dist/adapters/codex/.agents/skills/`.
  - Negative source path `.codex/skills/`.
- Steps:
  - Run runner dry-run or fixture-preparation mode.
  - Assert public skills are copied into `<temp-fixture>/.agents/skills/`.
  - Assert source fixture remains unchanged.
  - Assert `.codex/skills/` as source is rejected by runner config or metadata validation.
- Expected result:
  - Runtime benchmark setup measures public adapter output, not the repository-local Codex mirror.
- Failure proves:
  - Release benchmarks can measure the wrong skill surface or mutate tracked fixtures.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - `scripts/run-token-cost-benchmarks.py --dry-run` if implemented

### T9. Runner CLI and output paths are reproducible

- Covers: `R11`, `R11a`-`R11c`, `R13`, `R13a`-`R13e`, `R20`, `R20a`-`R20g`
- Level: integration
- Fixture/setup:
  - Manifest fixture.
  - Clean project fixture.
  - Temporary output root or `docs/reports/token-cost/runs/<release>/` test fixture.
  - Stubbed command executor for Codex.
- Steps:
  - Run runner command-construction tests with `--release`, `--suite`, `--tool codex`, `--fixture`, `--temp-root`, `--output-dir`, and retention flags.
  - Assert generated Codex command uses `codex exec --json --ephemeral` or normalized equivalent.
  - Assert output paths include release version, benchmark id, and run number.
  - Assert analyzer command is invoked or queued for every run.
  - Assert runner metadata fields agree with suite and output paths.
- Expected result:
  - A maintainer can reproduce dynamic benchmark execution from recorded metadata.
- Failure proves:
  - JSONL files exist without enough evidence to repeat or validate how they were produced.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T10. Runner temp directory policy is isolated and cleanup-safe

- Covers: `R12`, `R12a`-`R12f`, `R11b`, edge case 16
- Level: integration
- Fixture/setup:
  - Temporary repo-external root.
  - Environment variants for `$TMPDIR` and `$RUNNER_TEMP`.
  - Stubbed success and failure benchmark execution.
- Steps:
  - Run fixture-preparation mode locally with default temp policy.
  - Run with CI-style `$RUNNER_TEMP`.
  - Assert temp directories are outside the repo working tree.
  - Assert success deletes temp unless `--keep-temp` is set.
  - Assert failure preserves temp only with `--keep-failed-temp`.
  - Assert release metadata records fixture source, skill source, output directory, and temp policy, not unstable local temp paths.
- Expected result:
  - Benchmark temp state is disposable and does not pollute the repository.
- Failure proves:
  - Repeated release benchmark runs can mutate durable fixtures or leak unstable local paths into evidence.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T11. Analyzer emits schema version 1 summaries for tracked and omitted raw JSONL

- Covers: `R15`, `R15a`-`R15k`, `E3a`
- Level: unit
- Fixture/setup:
  - Existing sample Codex JSONL fixture.
  - Sanitized-summary fixture.
  - Analyzer CLI options for summary output and raw omission, when implemented.
- Steps:
  - Run analyzer to write a summary for tracked raw JSONL.
  - Assert `schema_version: 1`, run identity, usage, tool output, signals, and verdict fields exist.
  - Run analyzer summary mode for omitted raw JSONL.
  - Assert `run.raw_jsonl_tracked: false`, empty `run.jsonl`, non-empty `run.sanitized_source`, `run.sanitized_summary`, and `run.raw_omission_reason`.
- Expected result:
  - Analyzer summaries are stable, machine-readable release evidence whether raw JSONL is tracked or omitted.
- Failure proves:
  - Release metadata cannot safely reference per-run analysis evidence.
- Automation location:
  - `scripts/test-token-cost-measurement.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`

### T12. Baseline release report and metadata are valid and linked

- Covers: `R1`, `R1a`-`R1c`, `R4`, `R5`, `R16`, `R17`, `R30`, `R30a`, `R32`, `E1`
- Level: integration, manual
- Fixture/setup:
  - First release Markdown report and YAML metadata under `docs/reports/token-cost/releases/<release-version>.md/.yaml`.
  - Analyzer summaries or sanitized evidence under `docs/reports/token-cost/runs/<release-version>/`.
  - Release notes under `docs/releases/<release-version>/release-notes.md`.
- Steps:
  - Validate the YAML metadata with `scripts/validate-token-cost-report.py`.
  - Inspect Markdown report headings for static size, dynamic benchmarks, command-output amplification, portability, comparison, cost drivers, and release decision.
  - Assert Markdown names or links the YAML file.
  - Assert release notes link the report.
  - Assert no full Markdown report generator was added or required for this report.
- Expected result:
  - The first baseline report is human-readable, machine-checkable, and release-note-linked.
- Failure proves:
  - The release report is not durable enough for public release review.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`
  - manual review during M4

### T13. Compound full-file-read and command-output signal tests avoid weak blockers

- Covers: `R17`, `R17a`, `R17b`, `R18`, `R18a`-`R18d`, `E8`
- Level: unit
- Fixture/setup:
  - JSONL fixtures for `cat file`, large leading `sed` range, high-volume output, repeated same-file reads, generated-output reads, path-list output, small file reads, and justified whole-file target metadata when available.
- Steps:
  - Run analyzer summary mode on each fixture.
  - Assert confirmed/suspected/justified/none classification follows compound signals.
  - Assert files at or under 80 lines, path lists, capped excerpts, and justified generated-output validation are not unbounded blockers.
  - Assert high-volume command output records largest event lines and estimated tokens.
- Expected result:
  - Analyzer evidence catches major cost drivers without hard-blocking on weak single-signal guesses.
- Failure proves:
  - Release evidence will either miss runtime amplification or over-report false positives.
- Automation location:
  - `scripts/test-token-cost-measurement.py`

### T14. Warning and high-warning thresholds are non-blocking in v1

- Covers: `R19b`, `R26b`, `R26c`, `R27`, `R27a`-`R27g`, `R28`, `R28a`, `R28b`, `E7`, `E8`
- Level: unit
- Fixture/setup:
  - Metadata fixtures with static skill token warnings, dynamic input-token warnings, command-output warnings, broad-search warnings, and portability fail.
- Steps:
  - Validate warning-only fixtures.
  - Assert `warning` and `high-warning` can produce `release_gate.result: warning` but do not block when required evidence and portability pass.
  - Assert `portability.status: fail` blocks even if token metrics improve.
- Expected result:
  - First-slice release gates distinguish warning evidence from structural blockers.
- Failure proves:
  - The implementation prematurely hard-gates token regressions or ignores portability failures.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T15. Comparison, first-baseline, and RC reuse metadata follow exact contracts

- Covers: `R21`, `R21a`-`R21f`, `R22`, `R22a`-`R22c`, `R23`, `R23a`, `E2`, `E9`
- Level: unit
- Fixture/setup:
  - First-baseline metadata fixture.
  - Comparable previous-release fixture with numeric deltas.
  - Non-comparable previous-report fixture.
  - RC reuse fixtures with benchmark-relevant changes true and false.
- Steps:
  - Validate the first-baseline fixture and assert previous fields and deltas are null.
  - Validate comparable fixture and assert required numeric deltas exist.
  - Validate non-comparable fixture and assert rationale is required.
  - Validate RC reuse false fixture and assert checked surfaces are named.
  - Validate RC reuse true fixture and assert rerun evidence or waiver is required.
- Expected result:
  - Release-over-release comparison and RC reuse decisions are explicit and testable.
- Failure proves:
  - Baselines can fabricate deltas or RC reuse can hide benchmark-relevant changes.
- Automation location:
  - `scripts/test-token-cost-report-validation.py`

### T16. Release validation delegates token-cost validation only for governed releases

- Covers: `R1d`, `R6c`, `R6d`, `R19`, `R20g`, `R24b`, `R26`, `R26a`-`R26c`, `R29`, `R29a`, `R29b`, `R32`, examples `E1`-`E7`
- Level: integration
- Fixture/setup:
  - Governed release metadata and release notes fixture.
  - Historical release fixture outside the token-cost policy scope.
  - Invalid governed release fixtures for missing report, missing metadata, invalid waiver, missing evidence, inconsistent runner metadata, and optional non-Codex not-run.
- Steps:
  - Run `python scripts/validate-release.py --version <governed-version>`.
  - Assert it delegates to `scripts/validate-token-cost-report.py`.
  - Assert governed missing/invalid token-cost evidence blocks.
  - Assert governed token-cost metadata that exists but fails standalone token-cost report validation also fails release validation through delegated validator failure propagation.
  - Assert historical releases are not accidentally broken unless policy scope requires it.
  - Assert optional Claude Code/opencode `not-run` sections do not block v1.
- Expected result:
  - Release readiness includes token-cost evidence for governed public releases without broadening v1 tool requirements.
- Failure proves:
  - Token-cost release evidence is either not enforced or enforced too broadly.
- Automation location:
  - Release validation tests added or extended in M5.
  - `python scripts/validate-release.py --version <release-version>`

### T17. Lifecycle and generated-output boundaries remain valid

- Covers: `R24`, `R31`, `R31a`, `R33`, `R33a`
- Level: integration, smoke
- Fixture/setup:
  - Plan, spec, test spec, review artifacts, and change metadata.
  - Existing adapter generation/validation commands when canonical skills or public adapter output change.
- Steps:
  - Run lifecycle validation for the spec, test spec, plan, plan index, change metadata, review log, and review resolution.
  - Run review artifact and change metadata validators.
  - If canonical skills or adapter output change, run adapter generation check and adapter validation.
  - Assert generated adapter output is not hand-edited as part of token-friendliness measurement.
- Expected result:
  - Lifecycle artifacts stay coherent and generated output remains derived.
- Failure proves:
  - The implementation can pass local tests while violating repository governance.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `python scripts/validate-review-artifacts.py --mode closeout ...`
  - `python scripts/validate-change-metadata.py ...`
  - `python scripts/build-adapters.py --check`
  - `python scripts/validate-adapters.py`

### T18. End-to-end release benchmark dry run produces inspectable evidence

- Covers: `R5`, `R10`-`R18`, `R20`, `R22`, `R23`, `R27`, `R32`, `E1`
- Level: smoke, manual
- Fixture/setup:
  - Built public Codex adapter output.
  - Benchmark manifest and minimal fixture.
  - Codex CLI available for live release-runner validation, or runner dry-run/stub mode for ordinary contributor validation.
- Steps:
  - Run `python scripts/measure-skill-tokens.py`.
  - Run `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release <release-version> --tool codex` when Codex is available.
  - Confirm JSONL and analyzer summaries are written under `docs/reports/token-cost/runs/<release-version>/` or sanitized evidence is recorded.
  - Validate release metadata.
  - Manually inspect top cost drivers and release decision in the Markdown report.
- Expected result:
  - Maintainers can produce a complete, inspectable release Token-Friendliness evidence pack.
- Failure proves:
  - The release benchmark is not repeatable enough for public release use.
- Automation location:
  - `scripts/run-token-cost-benchmarks.py`
  - `scripts/validate-token-cost-report.py`
  - manual release preparation checklist

## Fixtures and data

- `tests/fixtures/token-cost/reports/` should contain valid and invalid release metadata/report cases for M1 and M5.
- `tests/fixtures/token-cost/sample-codex-session.jsonl` remains the base analyzer fixture and should be extended or accompanied by focused JSONL fixtures for summary output, full-file-read signals, and sanitized raw omission.
- `benchmarks/token-cost/manifest.yaml` owns benchmark suite identity.
- `benchmarks/token-cost/prompts/*.md` owns executable benchmark prompts.
- `benchmarks/token-cost/fixtures/minimal-public-project/` owns the clean downstream project fixture.
- `docs/reports/token-cost/releases/<release-version>.md/.yaml` and `docs/reports/token-cost/runs/<release-version>/` become release evidence fixtures or real baseline artifacts in M4.

## Mocking/stubbing policy

- Unit tests must not require Codex CLI, network access, secrets, or non-standard services.
- Runner tests should use dry-run mode, command construction, or an injected/stubbed command executor for ordinary validation.
- Live `codex exec --json --ephemeral` is release-run or manual smoke evidence, not a required unit-test dependency.
- File-system tests should use temporary directories outside the repo for runner temp policy, while durable outputs under `docs/reports/token-cost/` are created only by release-report milestones.
- Analyzer tests should use deterministic JSONL fixtures rather than live model output.

## Migration or compatibility tests

- Existing historical baseline reports under `docs/reports/token-cost/` must remain valid historical evidence and are not rewritten into release report format.
- Existing release validation must not block historical releases unless the governed release scope explicitly includes them.
- Existing `scripts/measure-skill-tokens.py` and `scripts/analyze-codex-jsonl.py` behavior remains compatible unless tests are updated to cover the approved summary extensions.
- Existing adapter validation remains separate; token-cost release validation adds evidence beside adapter release validation.

## Observability verification

- Runner output records benchmark id, prompt path, temp policy, JSONL path, analyzer summary path, and final result.
- Token-cost validator errors include field paths or file paths.
- Analyzer summaries include usage, largest tool-output source, signal counts, and verdict.
- Release metadata records environment details, runner invocation, top summary metrics, portability counts, and gate result.
- Markdown reports include top cost drivers and suggested actions.

## Security/privacy verification

- Raw JSONL omission tests verify private local raw paths are not required as durable release evidence.
- Runner temp-path tests verify metadata records stable repo-relative sources and output paths, not unstable local temp directories.
- Fixture tests verify the minimal public fixture avoids repository-internal generated skill mirrors and private examples.
- Release evidence tests verify sanitized summaries include omission reasons without embedding private discussion content.

## Performance checks

- Runner tests verify configured fixture, suite, public skill source, and output directory are the only required filesystem surfaces.
- Fixture tests keep the first benchmark suite small and reviewable.
- Analyzer summary tests verify metadata can reference compact summaries rather than duplicating raw JSONL.
- Warning-threshold tests verify high token usage is visible without making v1 total-token regressions hard blockers.

## Manual QA checklist

- Run live Codex benchmark once in a release-capable environment before a final public release unless a valid waiver applies.
- Inspect the Markdown report for readable summary, command-output amplification, portability, comparison, top cost drivers, and release decision.
- Inspect sanitized evidence when raw JSONL is omitted.
- Confirm release notes link the report.
- Confirm no generated adapter output was hand-edited to improve measured token-friendliness.

## What not to test

- Do not require Claude Code or opencode dynamic benchmark execution in v1; optional metadata coverage is enough.
- Do not test a hosted telemetry service; none is in scope.
- Do not require a full Markdown report generator; the first reports are manual.
- Do not assert exact live token counts from Codex runs; assert schema, evidence, summaries, warnings, and gate behavior.
- Do not make total token regression a hard blocker in v1.

## Uncovered gaps

None. Live Codex execution remains manual or release-run evidence by design, with automated coverage for deterministic runner setup and metadata validation.

## Next artifacts

- implement M1: metadata schema and standalone validator
- code-review M1
- repeat implementation and review for M2 through M5

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for M1. The test spec covers the approved contract and plan; M1 should begin with standalone token-cost metadata validator tests before production code.
