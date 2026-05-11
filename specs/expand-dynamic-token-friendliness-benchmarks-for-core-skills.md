# Expand Dynamic Token-Friendliness Benchmarks for Core Skills

## Status

approved

## Related proposal

- [Expand Dynamic Token-Friendliness Benchmarks for Core Skills](../docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md)
- Existing approved contract: [Release Token-Friendliness Benchmark for Skills](release-token-friendliness-benchmark-for-skills.md)

## Goal and context

This spec defines the `skill-token-runtime-v2` expansion of RigorLoop's release Token-Friendliness benchmark.

The existing `skill-token-runtime-v1` release benchmark proves static size, dynamic runtime cost, command-output amplification, public skill portability, and release metadata. The v1 suite is intentionally small, but it does not cover enough of the standard delivery path. This v2 expansion adds required dynamic coverage for the core workflow skills users rely on during normal delivery while preserving a manageable release benchmark.

This spec is additive to the approved release Token-Friendliness benchmark contract. It does not replace static skill measurement, adapter validation, public portability checks, sanitized evidence rules, waiver rules, or the existing Markdown plus YAML release report model.

## Glossary

- `skill-token-runtime-v2`: the expanded Codex dynamic benchmark suite and metadata shape defined by this spec.
- `required core benchmark`: a release-required benchmark for a core standard workflow skill.
- `transition carryover benchmark`: a v1 benchmark that remains required for one v2 transition release to preserve continuity.
- `optional extended benchmark`: a benchmark for an important skill that is not required for every release unless another rule makes it required.
- `changed-skill-required benchmark`: an optional benchmark that becomes required for a release because the corresponding public skill changed and a benchmark exists.
- `required benchmark context`: structured release-validation input that tells token-cost validation which benchmarks are required for a specific release.
- `result quality`: manual or future automated evidence that a benchmark output followed the prompt and made correct handoff or readiness claims.
- `pre-transition v1 report`: a tracked `skill-token-runtime-v1` report for a release version that is preserved when the same release version becomes the canonical v2 report.

## Examples first

### Example E1: v2 final release runs required core and carryover benchmarks

Given `v0.1.1` is the first public release using `skill-token-runtime-v2`
When release validation checks token-friendliness metadata
Then the report passes only when all required core benchmarks and transition carryover benchmarks have run evidence, analyzer evidence, and passing result-quality evidence or valid waivers.

### Example E2: pre-transition v1 evidence is preserved

Given `docs/reports/token-cost/releases/v0.1.1.yaml` already exists as a `skill-token-runtime-v1` pre-release report
When `v0.1.1` becomes the first canonical `skill-token-runtime-v2` release report
Then the v1 report is preserved as `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml`
And the v2 report references that path as overlap-comparison evidence.

### Example E3: optional benchmark failure warns

Given the optional `architecture-review` benchmark is run for extra visibility
And it is not required by changed-skill policy and is not claimed as release coverage
When result quality is `fail`
Then release metadata records `optional-benchmark-failed` as a warning and the release is not blocked by that optional failure.

### Example E4: changed public skill makes an optional benchmark required

Given `skills/architecture-review/SKILL.md` changed
And an `architecture-review` benchmark exists
When release validation builds required benchmark context
Then `architecture-review` appears under `required_benchmarks.required_due_to_changes`
And a missing, failed, not-reviewed, or unwaived inconclusive result blocks final release.

### Example E5: generated adapter change traces to canonical skill

Given `dist/adapters/codex/.agents/skills/architecture-review/SKILL.md` changed
When release validation analyzes changed surfaces
Then it traces the generated path to `skills/architecture-review/SKILL.md`
And applies the benchmark requirement for the owning canonical skill when the canonical skill changed or generated output is part of the same skill change.

### Example E6: required benchmark context is available in process and by CLI

Given release validation determines that core, transition carryover, and one changed-skill benchmark are required
When it calls token-cost validation in process
Then it passes the `required_benchmark_context` object directly.

Given a maintainer debugs the same release gate
When they run the standalone token-cost validator
Then they may pass the same context shape as YAML with `--required-benchmark-context`.

### Example E7: architecture-review benchmark checks canonical architecture review behavior

Given the `minimal-public-project-architecture-review` fixture contains a canonical architecture update and no change-local architecture delta
When the `architecture-review` optional benchmark runs
Then passing result quality requires the output to review the canonical update directly and not demand a change-local architecture delta.

## Requirements

R1. The expanded dynamic benchmark suite MUST use suite id `skill-token-runtime-v2`.

R1a. `skill-token-runtime-v2` metadata MUST identify `previous_suite_id: skill-token-runtime-v1` when comparing with v1 evidence.

R1b. The first `skill-token-runtime-v2` release report MUST be treated as a new suite baseline.

R1c. Suite totals from `skill-token-runtime-v1` and `skill-token-runtime-v2` MUST NOT be treated as directly comparable.

R1d. Overlapping prompts between v1 and v2 MAY be compared as continuity evidence when metadata marks the comparison as informational.

R2. The release-required core suite MUST include these benchmarks:

- `workflow-route`
- `proposal-short`
- `plan-handoff`
- `implement-handoff`
- `code-review-small`
- `explain-change-summary`
- `verify-final-pack`
- `pr-handoff`

R2a. Required core benchmarks MUST map to these public skills: `workflow`, `proposal`, `plan`, `implement`, `code-review`, `explain-change`, `verify`, and `pr`.

R2b. Required core prompt fixtures MUST live under `benchmarks/token-cost/prompts/`.

R2c. Required core prompts MUST be fixture-backed, single-skill focused, output-bounded, and explicit about whether file edits are allowed.

R2d. Required core prompts in the first v2 implementation MUST forbid file edits.

R3. The first `skill-token-runtime-v2` transition release MUST keep `architecture-no-impact` and `learn-no-durable-lesson` as transition carryover required benchmarks.

R3a. Transition carryover benchmarks MUST remain required for exactly one comparable v2 transition release unless a later approved spec changes the transition.

R3b. After the transition release, `architecture-no-impact` and `learn-no-durable-lesson` MUST move to optional extended coverage unless their corresponding public skills change and changed-skill policy makes them required.

R4. The optional extended benchmark set MUST include, at minimum, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `learn`, `research`, `explore`, `vision`, and `project-map`.

R4a. Missing optional extended benchmarks MUST NOT block a public release unless the release claims coverage for the optional benchmark or changed-skill policy makes the benchmark required.

R4b. Optional extended benchmarks SHOULD run before major releases, before large skill refactors, when touched skills are in the extended set, or when a maintainer requests broader coverage.

R5. The first optional extended benchmark added after core expansion MUST be `architecture-review`.

R5a. The `architecture-review` benchmark MUST use a separate scenario fixture directory for the first implementation.

R5b. The first `architecture-review` fixture path MUST be `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`.

R5c. The fixture MUST represent a tiny downstream-style project with a canonical architecture update, no change-local architecture delta, and an ADR-not-required note.

R5d. The benchmark prompt MUST forbid file edits and bound output to review surface, review status, findings, whether a change-local architecture delta is required, and next stage or required action.

R5e. Manual result-quality review MUST fail the `architecture-review` benchmark when output requires a change-local architecture delta before reviewing the canonical architecture update.

R6. Fixture directories SHOULD remain self-contained in the first implementation.

R6a. A shared base-fixture or overlay proposal SHOULD be triggered when three or more scenario fixtures duplicate the same base files.

R6b. A shared base-fixture or overlay proposal SHOULD also be triggered when duplicate fixture drift causes a review finding or implementation error.

R6c. If `minimal-public-project-proposal-review` is added after `minimal-public-project-architecture-review` and duplicates the same base files, it SHOULD count as the third duplicated scenario fixture trigger.

R7. Release metadata MUST include benchmark coverage metadata for `skill-token-runtime-v2`.

R7a. Coverage metadata MUST identify `suite_id`, required core benchmarks, required core status, transition carryover benchmarks, transition carryover status, optional extended benchmarks, optional benchmarks run, changed-skill benchmark status, missing required benchmarks, and missing optional benchmarks.

R7b. Markdown release reports MUST include a human-readable benchmark coverage table.

R7c. YAML metadata MUST remain the release gate; Markdown coverage tables are reviewer-facing summaries.

R8. Each dynamic run in `skill-token-runtime-v2` MUST include `result_quality`.

R8a. `result_quality.status` MUST be one of `pass`, `fail`, `inconclusive`, or `not-reviewed`.

R8b. `result_quality` MUST include `reviewed_by`, `review_surface`, `reviewed_at`, `criteria`, `notes`, and `blockers`.

R8c. Each `result_quality.criteria` entry MUST include `id`, `expectation`, `result`, and `notes`.

R8d. Criteria result values MUST be `pass`, `fail`, or `inconclusive`.

R8e. For required benchmarks, `result_quality.status` MUST NOT be `not-reviewed`.

R8f. For final public releases, required benchmarks MUST have `result_quality.status: pass` unless a valid waiver exists.

R8g. For final public releases, required benchmarks with `fail` or `inconclusive` MUST block unless a valid required-benchmark result-quality waiver exists.

R8h. Optional extended benchmarks with `fail` or `inconclusive` MUST warn with notes and follow-up when they are not required and not claimed as release coverage.

R8i. Structured expected-output checks MUST NOT be required in the first v2 implementation.

R8j. When a release report explicitly claims an optional benchmark as release coverage, that benchmark MUST be treated as release-required for evidence and result-quality purposes.

R8k. For final public releases, claimed optional benchmark coverage MUST block when the claimed benchmark is missing, invalid, not reviewed, failed, inconclusive without a valid waiver, or missing required analyzer or result-quality evidence.

R8l. A report MAY avoid claimed optional coverage gates only by removing the release-coverage claim and recording the benchmark as optional warning evidence instead.

R9. Result-quality waivers MUST be explicit, review-visible, and role-scoped.

R9a. Valid waiver approval roles MUST be limited to `release-owner`, `release-manager`, and `repository-maintainer`.

R9b. Waiver metadata MUST include non-empty `approved_by`, allowed `approved_role`, `approval_surface`, `approved_at`, `reason`, and evidence when the waiver affects a required benchmark.

R9c. The first implementation MUST validate `approved_by` as a non-empty review-visible string and MUST NOT require GitHub collaborator, CODEOWNERS, or maintainer-registry lookup.

R9d. A valid required-benchmark result-quality waiver MUST include `waiver.status: approved`, `waiver.approved_by`, `waiver.approved_role`, `waiver.approval_surface`, `waiver.reason`, and `waiver.evidence`.

R9e. Required-benchmark result-quality waiver approval roles MUST use the R9a allowed role enum.

R9f. A required-benchmark result-quality waiver MUST be review-visible and specific to the affected benchmark.

R10. Release validation MUST own changed public skill detection.

R10a. Token-cost validation MUST validate the metadata and required benchmark context that release validation provides.

R10b. Release validation MUST detect changed canonical public skill files under `skills/<name>/SKILL.md`.

R10c. Release validation MUST trace generated adapter skill paths back to the owning canonical skill when generated adapter skill output changes.

R10d. Generated adapter changes MUST NOT independently define benchmark ownership.

R10e. If generated output changes without a corresponding canonical skill change, release validation MUST treat it as adapter drift or regeneration evidence unless another release-validation rule records why dynamic skill benchmarking is required.

R11. Optional extended benchmarks MUST become conditionally required when the corresponding public skill changes and a benchmark exists.

R11a. If a public skill changes and a benchmark exists for that skill, release validation MUST add the benchmark to `required_benchmarks.required_due_to_changes`.

R11b. If a public skill changes and no benchmark exists for that skill, release validation MUST record the missing benchmark and follow-up as warning evidence unless the release claims complete coverage for that skill.

R12. Release validation MUST pass required benchmark context to token-cost validation.

R12a. The in-process object name SHOULD be `required_benchmark_context`.

R12b. Required benchmark context MUST include `schema_version`, `context_source`, `release`, `benchmark_suite`, `required_benchmarks`, `optional_benchmarks`, and `waiver_policy`.

R12c. `required_benchmarks` MUST include `core`, `transition_carryover`, and `required_due_to_changes`.

R12d. Token-cost validation MUST compute the effective required set as `core + transition_carryover + required_due_to_changes[*].benchmark`.

R12e. The required benchmark context MUST NOT require a duplicate precomputed effective required set unless a later implementation proves it useful and a spec revision adds it.

R13. The standalone token-cost validator CLI MUST support a YAML required benchmark context file.

R13a. The CLI flag SHOULD be `--required-benchmark-context`.

R13b. CI and local release validation SHOULD generate the context YAML transiently by default.

R13c. The context YAML MUST be tracked only when it becomes release decision evidence, waiver evidence, surprising required-benchmark evidence, or explicit debug evidence cited by a release owner.

R13d. When tracked as release evidence, the preferred path MUST be `docs/reports/token-cost/releases/<release-version>.required-benchmarks.yaml`.

R14. `skill-token-runtime-v2` release reports MUST preserve pre-transition v1 evidence when the same release version already has a tracked v1 report.

R14a. The canonical final v2 report for `v0.1.1` MUST use `docs/reports/token-cost/releases/v0.1.1.md` and `docs/reports/token-cost/releases/v0.1.1.yaml`.

R14b. If the existing pre-release v1 report is superseded by the v2 final report, the v1 report MUST be preserved as `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md` and `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml`.

R14c. The v2 report MUST reference the preserved pre-transition v1 report in comparison metadata.

R14d. The v2 Markdown report MUST include an overlap-comparison note that suite totals are not directly comparable and overlapping prompts are continuity evidence only.

R14e. If `v0.1.1` is finalized before v2 lands, the first v2 transition report MUST move to the next release line or RC path instead of replacing finalized evidence.

R15. Optional benchmark result-quality warnings MUST use stable generic warning codes.

R15a. Optional benchmark failure warning code MUST be `optional-benchmark-failed`.

R15b. Optional benchmark inconclusive warning code MUST be `optional-benchmark-inconclusive`.

R15c. Required benchmark blocking codes SHOULD include `required-benchmark-failed`, `required-benchmark-inconclusive`, and `required-benchmark-missing`.

R15d. Benchmark and skill identity MUST be recorded in separate metadata fields rather than encoded into warning or blocker codes.

R15e. Claimed optional benchmark coverage MUST NOT use optional warning codes when it fails release-required evidence or result-quality gates.

R16. `skill-token-runtime-v2` MUST NOT require Claude Code or opencode dynamic benchmarks.

R16a. Claude Code and opencode dynamic reports MAY remain optional until stable comparable runners exist.

R17. `skill-token-runtime-v2` MUST keep token thresholds warning-only unless evidence is missing, invalid, structurally blocked, portability fails, or required result quality fails without waiver.

R17a. Token regression thresholds MUST NOT become hard gates in this expansion.

## Inputs and outputs

Inputs:

- accepted proposal for expanding dynamic token-friendliness benchmarks;
- existing `skill-token-runtime-v1` release metadata and reports;
- benchmark suite manifest;
- prompt fixtures;
- minimal public project fixtures;
- changed release surfaces from release validation;
- dynamic benchmark run evidence;
- analyzer summaries;
- manual result-quality review evidence;
- optional waiver evidence.

Outputs:

- updated benchmark manifest declaring `skill-token-runtime-v2`, required core, transition carryover, and optional extended benchmarks;
- new required core prompt fixtures for `plan-handoff`, `explain-change-summary`, and `pr-handoff`;
- required benchmark context object or YAML evidence when needed;
- release metadata with coverage and result-quality fields;
- Markdown report coverage table;
- preserved pre-transition v1 report when v2 supersedes a pre-release v1 report for the same release version.

## State and invariants

- Release validation decides what benchmarks are required.
- Token-cost validation proves the report satisfies the required benchmark context.
- Required benchmarks block final public release when evidence is missing, invalid, failed, not reviewed, or inconclusive without waiver.
- Optional benchmark problems are visible warnings unless they are required by changed-skill policy or claimed as release coverage.
- Claimed optional coverage is gated coverage.
- One canonical final token-friendliness report exists per release version.
- Historical pre-transition evidence is preserved separately and linked.
- Fixtures stay simple and self-contained until duplication becomes a maintenance risk.
- Manual result-quality review is structured evidence until expected-output checks become stable enough for automation.

## Error and boundary behavior

- Missing required core benchmark evidence blocks final release.
- Missing transition carryover evidence blocks the v2 transition release unless waived.
- Missing changed-skill-required benchmark evidence blocks final release unless waived.
- Required benchmark `result_quality.status: fail` blocks final release unless waived.
- Required benchmark `result_quality.status: inconclusive` blocks final release unless waived.
- Required benchmark `result_quality.status: not-reviewed` blocks final release.
- Claimed optional benchmark coverage follows required-benchmark evidence and result-quality gates.
- Claimed optional benchmark coverage blocks final release when missing, invalid, failed, not reviewed, inconclusive without waiver, or missing analyzer or result-quality evidence.
- Optional benchmark `fail` warns when the optional benchmark is not required and not claimed as release coverage.
- Optional benchmark `inconclusive` warns when the optional benchmark is not required and not claimed as release coverage.
- Optional benchmark `fail` or `inconclusive` may remain warning-only only when `claimed_as_release_coverage` is false and the benchmark is not otherwise required.
- Optional benchmark failure or inconclusive status must not be summarized as coverage pass.
- Unknown waiver approval roles block required-benchmark waiver validation.
- Empty waiver approver identity blocks required-benchmark waiver validation.
- Generated adapter changes without canonical skill changes route to adapter validation unless release validation records a benchmark reason.
- Existing v1 report path collision blocks v2 report finalization unless the v1 report is preserved separately or a non-colliding release path is chosen.

## Compatibility and migration

- Existing `skill-token-runtime-v1` reports remain historical evidence.
- The first `skill-token-runtime-v2` report becomes a new comparable baseline for v2 suite totals.
- Overlapping v1 and v2 prompts may be compared only as continuity evidence.
- The existing approved release Token-Friendliness benchmark spec remains valid for v1 behavior unless superseded by this v2 expansion.
- Existing static measurement and command-output amplification evidence remain required release evidence.
- Existing sanitized raw JSONL behavior remains unchanged.
- Existing adapter validation remains separate from changed public skill benchmark detection.
- Existing generated output must not be hand-edited to satisfy benchmark requirements.

## Observability

- Release metadata must show coverage groups and statuses for required core, transition carryover, changed-skill-required, optional run, missing required, and missing optional benchmarks.
- Release metadata must show result-quality status and criteria per run.
- Release metadata must show optional benchmark warnings with stable warning codes, benchmark id, skill id, severity, message, and follow-up.
- Release validation should expose the required benchmark context through logs, debug output, or a transient YAML file when useful.
- If required benchmark context is tracked as release evidence, the release report must link or reference it.

## Security and privacy

- Required benchmark context must not include private local paths unless it is tracked intentionally as release decision evidence and the paths are safe to publish.
- Waiver approval surfaces should be review-visible but should not copy private discussion content when a public summary is enough.
- Result-quality notes should summarize correctness evidence without embedding sensitive raw model output.
- Scenario fixtures must avoid private repository-specific examples and local machine details.

## Accessibility and UX

This feature has no graphical UI.

Command output and validator errors should name benchmark ids, skill ids, report paths, field paths, and waiver fields clearly enough for maintainers to fix metadata without reading validator source.

## Performance expectations

- The required v2 suite should remain small enough for release preparation.
- Adding `plan-handoff`, `explain-change-summary`, and `pr-handoff` should not make every optional skill part of every release.
- Required benchmark context generation should use changed-path analysis and should not require broad repository scans beyond release validation's existing changed-surface inputs.
- Scenario fixture duplication should remain simple until the three-fixture or review-finding trigger justifies overlay complexity.

## Edge cases

1. `v0.1.1` already has a tracked pre-release v1 report and v2 also targets `v0.1.1`: preserve v1 under the pretransition path and make v2 canonical for final release.
2. `v0.1.1` is finalized before v2 lands: v2 targets the next release or RC path.
3. An optional benchmark is run and fails but is not required: release records `optional-benchmark-failed` warning.
4. An optional benchmark is run and inconclusive but is not required: release records `optional-benchmark-inconclusive` warning.
5. An optional benchmark is run and passes but is not required: report may record it as optional evidence.
5a. An optional benchmark is claimed as release coverage and fails: release blocks unless a valid waiver exists or the claim is removed and the run is recorded as optional warning evidence.
6. A public skill changes and its optional benchmark exists: benchmark becomes required.
7. A public skill changes and no benchmark exists: release records a warning and follow-up unless full coverage is claimed.
8. Generated adapter output changes without canonical skill change: adapter validation handles drift unless release validation records a benchmark reason.
9. Required benchmark context is needed only for debugging: generate transient YAML and do not track it.
10. Required benchmark context supports a waiver decision: track or cite it as release evidence.
11. `architecture-review` output demands a change-local architecture delta for the scenario fixture: result quality fails.
12. Three scenario fixtures duplicate the same base files: create a follow-up base-fixture or overlay proposal.
13. Result-quality reviewer identity is present but role is invalid: waiver validation blocks.
14. Required benchmark result is inconclusive during RC preparation: warning may be recorded with follow-up; final release requires pass or waiver.

## Non-goals

- Do not benchmark every RigorLoop skill in this expansion.
- Do not make total token regression a hard gate.
- Do not require Claude Code or opencode dynamic benchmarks.
- Do not add hosted telemetry.
- Do not add structured expected-output automation in the first v2 implementation.
- Do not optimize skill text in this benchmark-coverage change.
- Do not introduce shared fixture overlays before duplication triggers justify them.
- Do not validate waiver approver identity against GitHub collaborators in the first implementation.

## Acceptance criteria

- The proposal is accepted before this spec is used for planning.
- The v2 suite id and comparison behavior are defined.
- Required core benchmarks are listed and mapped to core public skills.
- Transition carryover benchmarks are defined for one v2 transition release.
- Optional extended benchmark behavior is defined.
- The first optional `architecture-review` benchmark fixture contract is defined.
- Benchmark coverage metadata is defined.
- Manual result-quality metadata is defined.
- Required benchmark result-quality blockers are defined.
- Optional benchmark warning behavior and warning codes are defined.
- Claimed optional benchmark coverage follows required-benchmark gates.
- Required benchmark result-quality waivers use the allowed waiver role enum.
- Changed public skill benchmark requirements are defined.
- Required benchmark context schema and transport forms are defined.
- Pre-transition v1 report preservation behavior is defined.
- Compatibility with v1 reports and existing release evidence is defined.
- Claude Code and opencode remain optional.

## Open questions

None.

## Next artifacts

- architecture or no-architecture decision
- execution plan
- test spec

## Follow-on artifacts

- Spec-review R2 approved this spec with no material findings.

## Readiness

Approved for architecture or no-architecture decision before execution planning.

This approved spec defines the v2 expansion contract for architecture, planning, and implementation.
