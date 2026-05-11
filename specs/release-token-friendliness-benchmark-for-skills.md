# Release Token-Friendliness Benchmark for Skills

## Status

approved

## Related proposal

- [Release Token-Friendliness Benchmark for Skills](../docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md)

## Goal and context

This spec defines the release contract for measuring and recording skill token-friendliness before public RigorLoop releases.

RigorLoop skills are distributed for use in downstream projects. Their cost is not limited to static `SKILL.md` size: skill guidance can also cause broad searches, large file reads, generated-output scans, repeated reads, and verbose command output. Public releases therefore need evidence that shipped skills remain usable within a reasonable context budget.

The first implementation establishes a report-required release gate, not a score-required gate. It requires human-readable Markdown, structured YAML metadata, fixture-backed Codex runtime benchmarks, analyzer summaries, public skill portability results, and release-over-release comparison. It keeps total-token regression thresholds warning-only until the repository has comparable report history.

This spec does not change workflow stage order, runtime architecture, or the public skill contract outside release measurement and validation.

## Glossary

- `Token-Friendliness`: the release evidence that RigorLoop skills are concise, portable, and efficient during agent use.
- `public release`: a tagged RigorLoop release intended for downstream users.
- `release report`: the human-readable Markdown report stored under `docs/reports/token-cost/releases/`.
- `release metadata`: the structured YAML file stored beside the Markdown report and used by release validation.
- `dynamic benchmark`: a noninteractive runtime benchmark that runs prompt fixtures with an agent tool and records usage evidence.
- `Codex dynamic benchmark`: the first required dynamic benchmark, executed with `codex exec --json --ephemeral`.
- `analyzer summary`: a per-run machine-readable summary produced from a Codex JSONL run.
- `public Codex adapter skills`: generated public Codex skills under `dist/adapters/codex/.agents/skills/`.
- `repository-local Codex mirror`: generated local Codex runtime output under `.codex/skills/`.
- `clean fixture`: a minimal downstream-style project fixture that does not contain installed generated skills.
- `temporary fixture`: a disposable copy of the clean fixture used for a benchmark run.
- `raw JSONL`: the original JSONL event stream emitted by Codex.
- `sanitized summary`: tracked evidence that replaces raw JSONL when raw JSONL is too large or contains sensitive local data.
- `valid waiver`: an approved, evidence-backed reason that a final public release may proceed without a completed final-release dynamic benchmark.
- `benchmark-relevant change`: a change that can affect skill loading, public skill text, adapter output, workflow guidance, benchmark prompts, analyzer scripts, portability checks, model/tool behavior, fixture behavior, or release packaging.
- `warning`: a non-blocking release concern.
- `high-warning`: a non-blocking release concern that needs stronger visibility than an ordinary warning.
- `blocker`: a release condition that prevents release readiness unless corrected or explicitly waived where waivers are allowed.

## Examples first

### Example E1: final release with complete benchmark evidence

Given a maintainer prepares public release `v0.1.1`
When the maintainer runs static skill measurement, runs the Codex benchmark suite, tracks JSONL and analyzer summaries, writes `v0.1.1.md`, and writes `v0.1.1.yaml`
Then release validation passes when the metadata is parseable, required fields exist, portability passes, runner metadata agrees with run evidence, and `dynamic_runtime.status` is `pass`.

### Example E2: final release waiver after a passing RC run

Given `v0.1.1-rc.1` has a passing dynamic benchmark
And no benchmark-relevant changes occurred after the RC benchmark
When Codex is unavailable for the final release runner
Then `v0.1.1.yaml` may set `dynamic_runtime.status: waived` only when waiver approval, reason, evidence, approval surface, and RC reuse decision metadata are present.

### Example E3: missing raw JSONL is not automatically an error

Given a benchmark run produced raw JSONL containing sensitive local paths
When the release tracks an analyzer summary and sanitized summary instead of raw JSONL
Then the run evidence is valid only when `raw_jsonl_tracked: false`, `jsonl: ""`, `raw_omission_reason` is non-empty, and tracked summary evidence exists.

### Example E3a: analyzer summary does not preserve omitted raw JSONL

Given raw JSONL is omitted from durable release artifacts
When the analyzer summary is written
Then `run.raw_jsonl_tracked` is `false`, `run.jsonl` is empty, and `run.sanitized_source`, `run.sanitized_summary`, and `run.raw_omission_reason` identify the summarized evidence without requiring a private local raw JSONL path.

### Example E4: prose-only report fails release validation

Given `docs/reports/token-cost/releases/v0.1.1.md` exists
And `docs/reports/token-cost/releases/v0.1.1.yaml` is missing
When release validation runs for `v0.1.1`
Then release validation blocks because reviewers have prose evidence but the release gate has no structured metadata.

### Example E5: runner installs public adapter skills into a temp fixture

Given a clean fixture under `benchmarks/token-cost/fixtures/minimal-public-project/`
When the Codex benchmark runner starts
Then it copies the clean fixture to an isolated temp directory and installs skills from `dist/adapters/codex/.agents/skills/` into `<temp-fixture>/.agents/skills/`.

### Example E6: repository-local Codex mirror is rejected as benchmark source

Given a runner configuration points the skill source at `.codex/skills/`
When release token-cost metadata is validated
Then validation blocks because the release benchmark must measure the public adapter output, not the repository-local generated mirror.

### Example E7: high token growth warns but does not block in v1

Given a benchmark report shows median input tokens increased above the initial warning threshold
When all required evidence is present, parseable, and portable
Then release validation reports a `warning` or `high-warning`, but it does not block the release in the first implementation slice.

### Example E8: confirmed unbounded command output is recorded

Given a per-run analyzer summary detects one shell output over 20,000 estimated tokens
And the run has no justification
When release metadata is reviewed
Then v1 records the issue as release evidence and warning or high-warning; later gates may treat the same unbounded output as a blocker after comparable report history exists.

### Example E9: first release report declares itself the baseline

Given no prior public release token-friendliness report exists
When `v0.1.1` creates the first release metadata
Then `comparison.baseline` is `true`, previous release and report fields are null, `comparison.comparable` is `false`, `comparison.deltas` is null, and the rationale explains that no prior comparable report exists.

## Requirements

R1. Every public release MUST include a Token-Friendliness release report with both Markdown and YAML metadata.

R1a. The Markdown report MUST be stored at `docs/reports/token-cost/releases/<release-version>.md`.

R1b. The YAML metadata MUST be stored at `docs/reports/token-cost/releases/<release-version>.yaml`.

R1c. The Markdown report MUST link to or name the YAML metadata file.

R1d. Release validation MUST NOT depend on parsing Markdown prose as the only source of release-gate evidence.

R2. The release metadata MUST use `schema_version: 1` for the first schema.

R2a. The release metadata MUST contain the top-level sections `report`, `benchmark_suite`, `environment`, `runner`, `static_skill_size`, `dynamic_runtime`, `summary`, `portability`, `comparison`, `waiver`, and `release_gate`.

R2b. The release metadata MUST contain `optional_dynamic` when optional Claude Code or opencode results are recorded.

R2c. The release metadata MUST contain `rc_reuse` when a final release reuses or refers to an RC benchmark.

R2d. Release validation MUST require at least these fields: `schema_version`, `report.release`, `report.report_date`, `report.commit`, `report.report_markdown`, `benchmark_suite.id`, `benchmark_suite.manifest`, `runner.command`, `runner.suite`, `runner.fixture`, `runner.skill_source`, `runner.output_dir`, `static_skill_size.status`, `dynamic_runtime.status`, `summary`, `portability.status`, and `release_gate.result`.

R3. Release metadata status fields MUST use the approved enum values.

R3a. Generic status values MUST be limited to `pass`, `warning`, `blocked`, `not-run`, `waived`, and `fail` where those values are allowed by the field.

R3b. `release_gate.result` MUST be limited to `pass`, `warning`, `blocked`, and `waived`.

R3c. Warning severity labels MUST use `warning` and `high-warning`; the phrase `hard warning` MUST NOT be used as a release-gate severity.

R4. The Markdown release report MUST summarize static skill size, dynamic runtime benchmarks, command-output amplification, public skill portability, previous-release comparison, top cost drivers, and the release decision.

R5. Static skill measurement MUST be included in every public release report.

R5a. Static measurement evidence MUST identify the measurement command, number of skills measured, total estimated tokens, largest skill, and any warning entries.

R5b. The default static measurement command MUST be `python scripts/measure-skill-tokens.py` unless a later approved spec changes the command.

R6. Codex dynamic runtime measurement MUST be included for every final public release unless a valid waiver is recorded.

R6a. For final public releases, `dynamic_runtime.status` MUST be `pass` or `waived`.

R6b. For early adoption and RC preparation, `dynamic_runtime.status` MAY be `blocked` or `not-run` only when metadata records a reason, owner, environment, follow-up, and whether release may proceed.

R6c. Release validation MUST block when the dynamic benchmark suite was not run and no valid waiver exists.

R6d. Release validation MUST block when the report omits dynamic runtime measurement and no valid waiver exists.

R6e. `blocked` and `not-run` dynamic runtime statuses MUST be valid only for non-final release preparation, RC work, or draft reports.

R6f. When non-final `dynamic_runtime.status` is `blocked` or `not-run`, metadata MUST include `dynamic_runtime.incomplete`.

R6g. `dynamic_runtime.incomplete` MUST include `reason`, `owner`, `environment`, `follow_up`, and `release_may_proceed`.

R6h. `dynamic_runtime.incomplete.release_may_proceed` MUST be a boolean value.

R7. A valid final-release dynamic benchmark waiver MUST be explicit, approved, and evidence-backed.

R7a. If `dynamic_runtime.status` is `waived`, metadata MUST set `waiver.status: approved`.

R7b. A waiver MUST include `waiver.reason`, `waiver.approved_by`, `waiver.approval_surface`, and `waiver.evidence`.

R7c. A waiver MUST name the release owner, maintainer-of-record, or approving maintainer.

R7d. A waiver MUST include either a statement that no benchmark-relevant change occurred since the last passing run or another approved waiver reason.

R7e. Valid waiver reasons MUST be limited to Codex unavailability with no benchmark-relevant changes since a passing RC run, emergency security or critical fix release with maintainer-approved deferral, or benchmark tooling failure with tracked follow-up and passing static and portability checks.

R7f. Forgetting to run the benchmark, lack of time, inconvenience, and unexplained dynamic regressions MUST NOT be accepted as waiver reasons.

R8. Benchmark prompts MUST be tracked as executable fixtures under `benchmarks/token-cost/`.

R8a. The first benchmark suite manifest MUST be `benchmarks/token-cost/manifest.yaml`.

R8b. The first benchmark suite id MUST be `skill-token-runtime-v1`.

R8c. The first suite MUST include prompt fixtures for `workflow-route`, `proposal-short`, `implement-handoff`, `code-review-small`, `verify-final-pack`, `architecture-no-impact`, and `learn-no-durable-lesson`.

R8d. Each manifest entry MUST identify the benchmark id, prompt path, tool, fixture, expected skill, expected result, and tags or equivalent classification.

R8e. Each first-suite prompt MUST forbid file edits unless the benchmark is later changed to explicitly test edits.

R9. The first runtime fixture MUST be a minimal downstream public project fixture.

R9a. The clean fixture MUST live under `benchmarks/token-cost/fixtures/minimal-public-project/` unless a later approved change replaces the path.

R9b. The clean fixture MUST include enough downstream-project structure for public skills to operate, including `AGENTS.md`, `VISION.md`, `README.md`, `docs/workflows.md`, `docs/changes/.gitkeep`, and a tiny sample change surface such as `src/example.txt`.

R9c. The clean fixture MUST NOT contain repository-internal generated skill mirrors as benchmark inputs.

R9d. The clean fixture MUST remain small enough that broad reads and large command outputs are visible in the analyzer evidence.

R10. The Codex benchmark runner MUST install current public Codex adapter skills into a temporary fixture copy before execution.

R10a. The runner MUST copy skills from `dist/adapters/codex/.agents/skills/`.

R10b. The runner MUST install those skills into `<temp-fixture>/.agents/skills/`.

R10c. The runner MUST NOT use `.codex/skills/` as the source for release benchmark skills.

R10d. The runner MUST NOT mutate the clean source fixture.

R11. The first implementation MUST include a small benchmark runner script at `scripts/run-token-cost-benchmarks.py`.

R11a. The runner MUST accept a release version, benchmark suite path, tool selection, optional fixture path, optional temp root, optional output directory, and debug retention flags.

R11b. The runner MUST read the manifest, copy the configured clean fixture into a fresh temporary directory, install public skills, run each prompt, write run outputs, and report the written paths.

R11c. The runner MUST NOT generate the final Markdown report in the first implementation.

R12. Benchmark temporary directories MUST be isolated and disposable.

R12a. The runner MUST create temporary run directories outside the repository working tree.

R12b. For local runs, the default temp root MUST be the system temp directory, using `$TMPDIR` when available and `/tmp` or platform equivalent as fallback.

R12c. For CI runs, the default temp root MUST be `$RUNNER_TEMP` when available and the system temp directory as fallback.

R12d. The runner MUST delete the temp directory after successful completion unless `--keep-temp` is set.

R12e. On failure, the runner MAY preserve the temp directory only when `--keep-failed-temp` or an equivalent debug mode is set.

R12f. Release metadata MUST record fixture source, skill source, output directory, and temp policy, but MUST NOT rely on unstable local temp paths as release-critical evidence.

R13. The Codex benchmark runner MUST execute prompt fixtures with `codex exec --json --ephemeral` or an equivalent normalized invocation recorded in metadata.

R13a. Raw Codex JSONL runs, when tracked, MUST be written under `docs/reports/token-cost/runs/<release-version>/`.

R13b. Run filenames MUST include the benchmark id and run number or another stable per-run identifier.

R13c. The runner MUST call `scripts/analyze-codex-jsonl.py` automatically for each JSONL run.

R13d. The runner MUST write an analyzer summary next to each JSONL run.

R13e. The runner SHOULD print the equivalent analyzer command for debugging.

R14. Per-run dynamic evidence MUST explicitly distinguish tracked raw JSONL from sanitized-summary evidence.

R14a. Each dynamic run metadata entry MUST include `evidence.raw_jsonl_tracked`, `evidence.jsonl`, `evidence.analysis`, `evidence.sanitized_summary`, and `evidence.raw_omission_reason`.

R14b. When `raw_jsonl_tracked` is true, `evidence.jsonl` MUST point to a tracked JSONL run or an intentionally retained release artifact.

R14c. When `raw_jsonl_tracked` is false, `evidence.jsonl` MUST be empty, `evidence.raw_omission_reason` MUST be non-empty, and `evidence.analysis` or `evidence.sanitized_summary` MUST point to tracked sanitized evidence.

R14d. Release validation MUST treat missing raw JSONL as a blocker only when the sanitized evidence contract is not satisfied.

R15. Analyzer summary files MUST use a minimal stable schema.

R15a. Each analyzer summary MUST include `schema_version: 1`.

R15b. Each analyzer summary MUST include `run.id`, `run.raw_jsonl_tracked`, `run.jsonl`, `run.sanitized_source`, `run.sanitized_summary`, and `run.raw_omission_reason`.

R15c. Each analyzer summary MUST include `usage.input_tokens`, `usage.cached_input_tokens`, `usage.output_tokens`, and `usage.reasoning_output_tokens`.

R15d. Each analyzer summary MUST include `tool_output.total_estimated_tokens` and `tool_output.largest_event`.

R15e. `tool_output.largest_event` MUST include `kind`, `command`, `path`, `lines`, and `estimated_tokens`.

R15f. Each analyzer summary MUST include signal counts for full-file reads, broad searches, generated-output reads, and repeated file reads.

R15g. Each analyzer summary MUST include `verdict.result`, `verdict.warnings`, and `verdict.blockers`.

R15h. `verdict.result` MUST be limited to `pass`, `warning`, and `blocked`.

R15i. `run.jsonl` MUST be required only when `run.raw_jsonl_tracked` is true.

R15j. When `run.raw_jsonl_tracked` is false, `run.jsonl` MUST be empty and the analyzer summary MUST include non-empty `run.sanitized_source`, `run.sanitized_summary`, and `run.raw_omission_reason`.

R15k. Analyzer summaries MUST NOT require private local raw JSONL paths as durable release evidence when raw JSONL is intentionally omitted.

R16. Dynamic runtime metadata MUST include enough summary data for release comparison.

R16a. Each dynamic run MUST record benchmark id, prompt path, fixture path, result, evidence, usage, tool output, analyzer signals, and full-file-read classification or reference an analyzer summary that contains those values.

R16b. The release-level `summary` section MUST record median input tokens, median cached input tokens, median output tokens, median reasoning output tokens, max single tool-output estimated tokens, full-file-read count, broad-search count, and generated-output-read count.

R17. Command-output amplification MUST be measured from Codex JSONL analyzer evidence in the first implementation.

R17a. Reports MUST identify the largest command or output source, line count, estimated tokens, and notes or justification when relevant.

R17b. A separate live command-output wrapper MUST NOT be required for the first implementation.

R18. Full-file read detection MUST use compound analyzer signals.

R18a. Analyzer and report evidence SHOULD consider command shape, large leading line ranges, output-to-file-size ratio when available, high-volume single-file output, repeated same-file reads, and generated-output reads.

R18b. Full-file read classification MUST use `none`, `suspected`, `confirmed`, or `justified`.

R18c. A single weak signal MUST NOT be enough to hard-block a release.

R18d. Analyzer and validator behavior MUST avoid false positives for files at or under 80 lines, explicitly requested whole-file review targets, path-list output, capped small excerpts, and justified generated-output validation.

R19. Public skill portability results MUST be included in every public release report.

R19a. Portability metadata MUST include counts for public skill internal path leaks, generated-output internals in public skills, and local examples in public skills.

R19b. Release validation MUST block when `portability.status` is `fail`.

R20. Release metadata MUST record runner invocation evidence.

R20a. `runner.command` MUST contain the runner command or a normalized equivalent invocation.

R20b. `runner.tool` MUST be `codex` for the first required dynamic benchmark.

R20c. `runner.suite` MUST match `benchmark_suite.manifest`.

R20d. `runner.fixture` MUST match `benchmark_suite.fixture`.

R20e. `runner.skill_source` MUST be `dist/adapters/codex/.agents/skills/` for the required Codex benchmark.

R20f. `runner.output_dir` MUST identify the run output directory for the release.

R20g. Release validation MUST verify that runner metadata, benchmark suite metadata, and listed run evidence agree.

R21. Release reports MUST compare against the most recent prior public release report when one exists.

R21a. If no prior report exists, the first report MUST declare itself the baseline.

R21b. Comparison metadata MUST include `baseline`, `previous_release`, `previous_report`, `comparable`, `deltas`, and `rationale`.

R21c. If no prior report exists, comparison metadata MUST set `baseline: true`, `previous_release: null`, `previous_report: null`, `comparable: false`, and `deltas: null`.

R21d. If no prior report exists, comparison metadata MUST include a rationale explaining that the report is the first release token-friendliness baseline.

R21e. Numeric deltas MUST be required only when `comparison.baseline` is false, `comparison.comparable` is true, and `comparison.previous_report` exists.

R21f. When numeric deltas are required, they MUST include static total estimated tokens, median input tokens, median output tokens, and max single tool-output estimated tokens.

R22. RC reuse decisions MUST be recorded when a final release reuses an RC benchmark report or waives a final rerun based on RC evidence.

R22a. RC reuse metadata MUST include `reused_from`, `benchmark_relevant_changes_since_rc`, `checked_by`, `checked_surface`, and `rationale`.

R22b. If `benchmark_relevant_changes_since_rc` is true, the final release MUST rerun affected benchmarks, rerun the full suite, or record a valid waiver.

R22c. If `benchmark_relevant_changes_since_rc` is false, the rationale MUST state the checked surfaces, including public skills, adapter output, workflow guide, benchmark prompts, analyzer, fixture, model or tool version when known, and release packaging.

R23. Benchmark-relevant changes MUST include changes that can affect skill loading, public skill text, adapter output, workflow guidance, benchmark prompts, analyzer scripts, portability checks, workflow order, handoff behavior, skill frontmatter or descriptions, result format, evidence-reading guidance, tool-output guidance, benchmark fixture behavior, Codex version, model, or adapter release packaging.

R23a. Unrelated product docs, internal-only plan changes, review-resolution text, change-local artifacts, typo fixes outside public skills or guides, and historical report edits SHOULD NOT be treated as benchmark-relevant unless the release owner records why they are relevant.

R24. Release validation MUST be split between a token-cost-specific validator and release-level validation.

R24a. `scripts/validate-token-cost-report.py` MUST own token-cost YAML schema validation, required fields, enums, report links, run references, waiver fields, runner metadata checks, and raw-or-sanitized evidence checks.

R24b. `scripts/validate-release.py` MUST own release readiness and delegate token-cost report validation when public release policy requires a Token-Friendliness report.

R24c. The token-cost validator MUST be runnable standalone against a draft report.

R25. The first token-cost validator SHOULD use existing lightweight parser conventions if they can safely parse schema version 1.

R25a. A dedicated YAML parser dependency MAY be added only if the implementation plan records why the lightweight parser cannot safely handle the required nested maps, lists, scalars, enums, and references.

R26. Release validation MUST block on structural and evidence failures.

R26a. Blocking conditions MUST include missing Markdown report, missing YAML metadata, unparsable metadata, missing benchmark suite declaration, missing static measurement, missing dynamic measurement without waiver, dynamic suite not run without waiver, missing required evidence without sanitized substitute, uninterpretable raw or summarized results, inconsistent runner or suite metadata, and public portability failure.

R26b. Initial token regression thresholds MUST NOT be hard release blockers.

R26c. Token growth, command-output amplification growth, new full-file reads, and warning-threshold breaches MUST be reported as `warning` or `high-warning` unless another requirement classifies them as blockers.

R27. Initial warning thresholds MUST be recorded as warning guidance, not blockers.

R27a. A public skill over 4,000 estimated tokens SHOULD be reported as `warning`.

R27b. A public skill over 5,000 estimated tokens SHOULD be reported as `high-warning`.

R27c. A short dynamic benchmark over 75,000 input tokens SHOULD be reported as `warning`.

R27d. A short dynamic benchmark over 100,000 input tokens SHOULD be reported as `high-warning`.

R27e. A single command or output over 8,000 estimated tokens SHOULD be reported as `warning`.

R27f. A single command or output over 20,000 estimated tokens SHOULD be reported as `high-warning` in the first implementation.

R27g. A broad search output over 80 lines SHOULD be reported as `warning`.

R28. Future hard gates MAY be introduced only after comparable release report history exists.

R28a. After at least three comparable release reports, hard gates MAY be added first for structural reliability, portability failures, omitted benchmarks without waiver, severe command-output amplification without justification, and unbounded full-file reads without justification.

R28b. Static total token regression and median dynamic input-token regression SHOULD remain warning-only until at least five or six comparable reports exist and a maintainer override path is defined.

R29. Claude Code and opencode dynamic benchmarks MUST be optional in the first implementation.

R29a. Optional dynamic sections MAY record `not-run` with a reason such as `optional in v1`.

R29b. Claude Code or opencode benchmarks MUST NOT become required until each tool has a stable noninteractive benchmark path, parseable output, consistent prompts, maintainer-operable runners, and comparable reports across releases.

R30. The first implementation MUST NOT add a full Markdown report generator.

R30a. Maintainers MUST write the first Markdown reports manually using analyzer-backed evidence.

R30b. A report-generator proposal SHOULD be triggered after repeated manual-report errors or after three comparable stable reports, whichever comes first.

R31. Implementation planning for this feature MUST split the work into reviewable milestones.

R31a. The plan MUST include at least these milestone boundaries unless it records an equivalent or narrower split: metadata schema and validator, benchmark fixture and prompt suite, runner and analyzer-summary integration, first baseline report, and release validation integration.

R32. Release notes for a public release MUST link to the Token-Friendliness release report.

R33. Generated adapter output MUST NOT be hand-edited to improve measured token-friendliness.

R33a. If public adapter output needs to change, the canonical source or generator contract MUST change instead.

## Inputs and outputs

Inputs:

- release version, such as `v0.1.1` or `v0.1.1-rc.1`;
- current commit SHA;
- static skill measurement output;
- benchmark suite manifest at `benchmarks/token-cost/manifest.yaml`;
- prompt fixtures under `benchmarks/token-cost/prompts/`;
- clean fixture under `benchmarks/token-cost/fixtures/minimal-public-project/`;
- public Codex adapter skills under `dist/adapters/codex/.agents/skills/`;
- Codex JSONL runs when raw data is tracked;
- analyzer summaries or sanitized summaries when raw JSONL is omitted;
- previous release metadata when available;
- waiver approval evidence when a waiver is used.

Outputs:

- Markdown release report at `docs/reports/token-cost/releases/<release-version>.md`;
- YAML release metadata at `docs/reports/token-cost/releases/<release-version>.yaml`;
- raw JSONL runs under `docs/reports/token-cost/runs/<release-version>/` when tracked;
- per-run analyzer summaries beside raw or summarized run evidence;
- release validation result from `scripts/validate-release.py --version <release-version>` or equivalent release command;
- standalone token-cost validation result from `scripts/validate-token-cost-report.py <metadata-path>`.

## State and invariants

- Markdown explains the report; YAML gates the release.
- Prompt fixtures define benchmark intent; runner metadata defines how the run is reproduced.
- The clean fixture represents a downstream public project and remains unmutated.
- The temporary fixture is disposable and must not become durable release evidence.
- The required Codex benchmark measures public adapter output, not the repository-local Codex mirror.
- Raw JSONL is useful evidence but is not mandatory when tracked sanitized evidence satisfies the evidence contract.
- Waivers are exceptional, explicit, approved, and evidence-backed.
- Warning and high-warning token thresholds do not block first-slice releases.
- Safety-critical skill guidance and claim boundaries must not be removed solely to lower token counts.

## Error and boundary behavior

- Missing Markdown report blocks release validation.
- Missing YAML metadata blocks release validation.
- Unparseable YAML metadata blocks release validation.
- Missing required schema fields blocks release validation.
- Unknown enum values block release validation.
- Missing static measurement blocks release validation.
- Missing dynamic measurement blocks release validation unless a valid waiver exists.
- A final public release with `dynamic_runtime.status: blocked` or `not-run` blocks release validation.
- A final public release with `dynamic_runtime.status: waived` blocks release validation unless waiver fields are complete and approved.
- Missing raw JSONL does not block when sanitized evidence is explicitly recorded and parseable.
- Missing raw JSONL blocks when the run claims `raw_jsonl_tracked: true`.
- Runner metadata that points to `.codex/skills/` blocks release validation.
- Runner metadata that disagrees with suite or run evidence blocks release validation.
- Public portability failure blocks release validation.
- Optional Claude Code or opencode `not-run` status does not block v1 release validation.
- Codex command failure during benchmark execution must produce a non-success runner result and preserve debug evidence only when configured.
- The validator must report enough path and field context for maintainers to correct metadata without reading validator source.
- Non-final `blocked` or `not-run` dynamic runtime metadata without `dynamic_runtime.incomplete` blocks validation.
- Final public release metadata with `dynamic_runtime.status: blocked` or `not-run` blocks validation.
- First-baseline metadata must not fabricate previous release fields or numeric deltas.

## Compatibility and migration

- Existing baseline reports under `docs/reports/token-cost/` remain historical evidence and do not need to be rewritten into release-report format.
- The first public release using this policy may declare itself the release baseline when no prior release metadata exists.
- The new release metadata format is additive to existing adapter release validation.
- Existing `scripts/measure-skill-tokens.py` and `scripts/analyze-codex-jsonl.py` remain the measurement base unless changed by the implementation.
- Existing release verification can continue to run adapter checks; token-cost report validation is an additional release-readiness gate.
- Raw JSONL retention policy is compatible with sanitized summaries so releases can avoid tracking sensitive local data.
- A later report generator must consume or emit the same structured metadata contract unless a later spec version supersedes it.

## Observability

- The runner must print or record each benchmark id, prompt path, temporary fixture policy, JSONL path, analyzer summary path, and final runner result.
- The token-cost validator must report blocking and warning findings with field paths or file paths.
- Release metadata must record environment details including primary tool, Codex availability, Codex version when known, model when known, OS when known, and runner type.
- Release metadata must record largest tool-output sources and analyzer signals so reviewers can identify cost drivers.
- Release reports must include top cost drivers and suggested actions.

## Security and privacy

- Raw JSONL may contain local paths, command output, or sensitive project data. Maintainers may omit raw JSONL only through the explicit sanitized-evidence contract.
- Release metadata should record stable repo-relative paths and must not rely on unstable local temp paths as release evidence.
- The runner must not copy secrets or untracked local files from the repository into release artifacts.
- The fixture must avoid private repository-specific examples that would leak into public skill behavior.
- Waiver approval metadata must identify an approval surface without embedding private discussion content when a public summary is enough.

## Accessibility and UX

This feature has no graphical UI.

Command-line output should be concise, path-oriented, and actionable. Validation errors should name the invalid field or missing file. Markdown reports should be readable as plain Markdown without requiring rendered diagrams or external assets.

## Performance expectations

- The first benchmark suite must remain small enough to run during release preparation without requiring every supported agent tool.
- The runner must avoid broad repository scans outside the configured fixture, public skill source, suite manifest, prompt files, and output directory.
- Analyzer summaries should keep release metadata and Markdown reports compact by referencing per-run evidence instead of duplicating raw JSONL.
- Temporary directories should be deleted by default so repeated benchmark runs do not accumulate local artifacts.

## Edge cases

1. No previous public release report exists: the current report declares itself the baseline.
2. No previous public release report exists: comparison metadata uses null previous fields and null deltas.
3. Previous release metadata exists but is not comparable: comparison records `baseline: false`, `comparable: false`, and explains why.
4. RC benchmark passed and no benchmark-relevant changes occurred: final release may reuse RC evidence with `rc_reuse` metadata.
5. RC benchmark passed but benchmark-relevant changes occurred: final release reruns affected benchmarks, reruns the full suite, or records a valid waiver.
6. Codex is unavailable on a maintainer machine: RC metadata may record `blocked` or `not-run`; final metadata must be `pass` or `waived`.
7. Codex version or model changed after RC: the release owner treats it as benchmark-relevant unless a rationale says it cannot affect the report.
8. Raw JSONL is too large: raw JSONL may be omitted only when analyzer or sanitized summary evidence is tracked.
9. Raw JSONL contains sensitive local paths: sanitized evidence may replace it with an omission reason.
10. Raw JSONL is omitted from durable artifacts: analyzer summary identity fields use sanitized source and summary paths rather than private local raw JSONL paths.
11. Analyzer cannot determine file length: file-size-ratio signals are omitted rather than guessed.
12. A file under 80 lines is read in full: full-file-read detection does not automatically treat it as unbounded.
13. A whole file is the explicit review target: full-file-read classification may be `justified`.
14. A generated adapter path is read while validating adapter output: generated-output read may be justified.
15. A benchmark prompt accidentally allows edits: prompt review or manifest validation must catch the mismatch before release reliance.
16. Runner fails after creating a temp directory: temp is deleted unless failed-temp retention is enabled for debugging.
17. Optional Claude Code or opencode benchmark data exists: metadata may include it without making those tools required.
18. Static token totals increase but portability and structure pass: release records warning evidence, not a v1 blocker.
19. Public portability fails while token metrics improve: release validation blocks because portability is a release-surface requirement.
20. Metadata and Markdown disagree: YAML remains the release gate, and reviewers must correct the inconsistency before release.

## Non-goals

- Do not make token score the only release-quality measure.
- Do not define hard total-token regression blockers in the first implementation.
- Do not add hosted telemetry infrastructure.
- Do not require contributors to install every supported agent tool locally.
- Do not make Claude Code or opencode dynamic benchmarks required in v1.
- Do not add a full Markdown report generator in v1.
- Do not optimize every skill as part of this release-process change.
- Do not remove safety-critical skill guidance solely to reduce token counts.
- Do not hand-edit generated adapter output to reduce measured size.
- Do not replace existing adapter validation, release notes, or release verification contracts except where this spec adds token-cost evidence.

## Acceptance criteria

- A draft or approved spec exists for the release Token-Friendliness benchmark contract.
- The proposal is accepted before implementation planning relies on this spec.
- A schema version 1 YAML metadata contract is defined and testable.
- A Markdown release report path and YAML metadata path are defined.
- A dedicated token-cost validator ownership boundary is defined.
- Release validation delegation to token-cost validation is defined.
- The first benchmark suite includes seven fixture-backed prompts.
- The clean minimal downstream fixture contract is defined.
- The runner install source is the public Codex adapter skill path.
- The runner explicitly avoids `.codex/skills/` as public release benchmark source.
- Temporary directory behavior is defined.
- Automatic analyzer invocation and analyzer summary schema are defined.
- Analyzer summary examples cover both tracked raw JSONL and omitted raw JSONL.
- Validation accepts `run.jsonl` only when `run.raw_jsonl_tracked: true`.
- Validation requires sanitized evidence fields when `run.raw_jsonl_tracked: false`.
- Raw JSONL and sanitized-summary evidence behavior is defined.
- Waiver and RC reuse metadata behavior are defined.
- Validation requires `dynamic_runtime.incomplete` when non-final status is `blocked` or `not-run`.
- Validation rejects final public release metadata with `dynamic_runtime.status: blocked` or `not-run`.
- First baseline metadata uses `comparison.baseline: true` and does not require previous release, previous report, or numeric deltas.
- Numeric comparison deltas are required only when a previous comparable report exists.
- Warning, high-warning, and blocker semantics are defined.
- First-slice release gates block structural, evidence, waiver, and portability failures, not warning-only token regressions.
- Future hard-gate progression is constrained by comparable report history.
- The follow-on implementation plan is required to split work into reviewable milestones.

## Open questions

None currently.

## Next artifacts

- architecture or no-architecture decision
- execution plan
- test spec
- benchmark prompt definitions
- release report template
- first release Token-Friendliness baseline report
- release validation update

## Follow-on artifacts

- Spec-review R2 approved this spec with no material findings.
- Canonical architecture update: `docs/architecture/system/architecture.md`.

## Readiness

Approved after spec-review. Downstream architecture, planning, and test-spec artifacts may rely on this contract.
