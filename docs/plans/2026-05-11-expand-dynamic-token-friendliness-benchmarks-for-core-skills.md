# Expand Dynamic Token-Friendliness Benchmarks for Core Skills

- Status: active
- Owner: maintainer
- Start date: 2026-05-11
- Last updated: 2026-05-11
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement `skill-token-runtime-v2` so public release Token-Friendliness evidence covers the core delivery workflow, preserves v1 transition evidence, records manual result quality, and distinguishes required, claimed optional, changed-skill-required, and warning-only optional benchmark coverage.

## Why now

The first release Token-Friendliness benchmark proved dynamic measurement is necessary: runtime evidence showed confirmed skill-file reads and an input-token warning that static skill size alone could not explain. The existing `skill-token-runtime-v1` suite is intentionally small and misses core delivery skills such as `plan`, `explain-change`, and `pr`.

## Source artifacts

- Proposal: `docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Existing release benchmark spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Existing release benchmark test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Spec review: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/spec-review-r2.md`
- Architecture review: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/reviews/architecture-review-r1.md`
- Change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`

## Context and orientation

Current v1 benchmark surfaces:

- `benchmarks/token-cost/manifest.yaml`
- `benchmarks/token-cost/prompts/`
- `benchmarks/token-cost/fixtures/minimal-public-project/`
- `scripts/run-token-cost-benchmarks.py`
- `scripts/analyze-codex-jsonl.py`
- `scripts/validate-token-cost-report.py`
- `scripts/validate-release.py`
- `scripts/test-token-cost-measurement.py`
- `scripts/test-token-cost-report-validation.py`

The v2 change is release-process and evidence-shape work. It must not hand-edit generated output under `.codex/skills/` or `dist/adapters/`. Adapter output changes are only relevant when canonical source or generator contracts change.

`docs/plan.md` is the plan index. This file is the plan body and owns the current milestone handoff state for this initiative.

## Scope

### In scope

- Add or update a test spec for `skill-token-runtime-v2` coverage and validator behavior.
- Update the benchmark manifest shape to represent `skill-token-runtime-v2`, required core benchmarks, transition carryover benchmarks, and optional extended benchmarks.
- Add required core prompt fixtures for `plan-handoff`, `explain-change-summary`, and `pr-handoff`.
- Keep `architecture-no-impact` and `learn-no-durable-lesson` required for one transition release.
- Add the first optional `architecture-review` prompt and separate scenario fixture.
- Add or update runner dry-run behavior only where needed to understand v2 manifest groups and scenario fixtures.
- Add validator support for coverage metadata, per-run result quality, required benchmark context, claimed optional coverage gates, and allowed waiver roles.
- Add release validation required-benchmark context generation and delegation.
- Preserve existing pre-transition v1 report evidence if v2 also targets `v0.1.1`.
- Update sample or baseline metadata/report evidence needed to prove the v2 contract.

### Out of scope

- Benchmark every RigorLoop skill.
- Add hard total-token regression gates.
- Require Claude Code or opencode dynamic benchmarks.
- Add hosted telemetry.
- Add structured expected-output automation beyond recorded manual result-quality metadata.
- Optimize skill text to reduce token cost.
- Introduce shared fixture overlays before the duplication trigger is reached.
- Validate waiver approver identity against GitHub collaborators.

## Constraints

- Follow `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`.
- Keep `skill-token-runtime-v1` reports as historical evidence.
- Treat `skill-token-runtime-v2` totals as a new baseline.
- Release validation owns changed public skill detection; token-cost validation validates the required benchmark context and report metadata.
- YAML metadata gates; Markdown explains.
- Claimed optional coverage is gated coverage.
- Unclaimed optional failures and inconclusive results remain warning-only.
- The runner must continue installing public Codex skills from `dist/adapters/codex/.agents/skills/` into temp fixtures.
- Do not mutate source fixtures during benchmark runs.

## Current Handoff Summary

- Current stage: code-review
- Current milestone: M4. Release validation required benchmark context integration
- Current milestone state: implemented and committed; awaiting code-review
- Last reviewed milestone: M3. Token-cost validator v2 metadata and context support
- Review status: M4 implementation complete; code-review M4 not yet run
- Next stage after plan-review: test-spec
- Test-spec artifact: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md`
- Test-spec status: active
- Implementation may start after: test-spec is authored and accepted for use; complete
- Remaining in-scope implementation milestones: M4 review, M5
- Next stage: code-review M4
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M4 still needs code-review, M5 remains open, and final explain-change, verify, and PR handoff are not complete.

## Requirements covered

| Requirement IDs | Planned coverage |
|---|---|
| `R1`, `R1a`-`R1d` | test-spec gate, M1, M3, M4, M5 |
| `R2`, `R2a`-`R2d` | test-spec gate, M1 |
| `R3`, `R3a`-`R3b` | test-spec gate, M1, M3 |
| `R4`, `R4a`-`R4b` | test-spec gate, M1, M2, M3 |
| `R5`, `R5a`-`R5e` | test-spec gate, M2 |
| `R6`, `R6a`-`R6c` | test-spec gate, M2 |
| `R7`, `R7a`-`R7c` | test-spec gate, M3, M4, M5 |
| `R8`, `R8a`-`R8l` | test-spec gate, M3, M4, M5 |
| `R9`, `R9a`-`R9f` | test-spec gate, M3, M4, M5 |
| `R10`, `R10a`-`R10e` | test-spec gate, M4 |
| `R11`, `R11a`-`R11b` | test-spec gate, M4 |
| `R12`, `R12a`-`R12e` | test-spec gate, M3, M4 |
| `R13`, `R13a`-`R13d` | test-spec gate, M3, M4 |
| `R14`, `R14a`-`R14e` | test-spec gate, M5 |
| `R15`, `R15a`-`R15e` | test-spec gate, M3, M4 |
| `R16`, `R16a` | test-spec gate, M3 |
| `R17`, `R17a` | test-spec gate, M3, M5 |

## Pre-implementation gate: test-spec

Before M1 implementation begins, create or update:

```text
specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md
```

The test spec must define proof for:

- required core benchmark coverage;
- transition carryover behavior;
- optional benchmark result-quality semantics;
- claimed optional coverage gates;
- required benchmark context validation;
- changed public skill benchmark requirements;
- architecture-review optional extended benchmark fixture;
- pre-transition v1 report preservation.

Implementation must not start until this test spec is authored and accepted for use.

Suggested validation for the test-spec stage:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md --path specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `git diff --check -- specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`

## Milestones

### M1. Manifest and required core prompt fixtures

- Milestone state: closed
- Goal: Expand the manifest and prompt fixtures to declare the v2 required core suite plus transition carryover.
- Requirements: `R1`-`R3`, `R7`.
- Files/components likely touched:
  - `benchmarks/token-cost/manifest.yaml`
  - `benchmarks/token-cost/prompts/plan-handoff.md`
  - `benchmarks/token-cost/prompts/explain-change-summary.md`
  - `benchmarks/token-cost/prompts/pr-handoff.md`
  - `scripts/test-token-cost-measurement.py`
- Dependencies: active v2 test spec.
- Tests to add/update:
  - Manifest suite id and group coverage tests.
  - Prompt existence and no-edit instruction tests.
  - Transition carryover required status tests.
- Implementation steps:
  - Update the manifest to `skill-token-runtime-v2`.
  - Represent required core prompts and transition carryover prompts distinctly.
  - Add the three new required core prompt fixtures.
  - Preserve existing prompt ids for overlap comparison where possible.
  - Update measurement tests to validate v2 manifest groups and prompt files.
- Validation commands:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
  - `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`
- Expected observable result: The manifest declares the required v2 suite and dry-run can enumerate all required benchmark prompts without Codex execution.
- Commit message: `M1: expand token benchmark manifest and core prompts`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
  - [x] code-review passed
- Risks:
  - Manifest shape changes may break the runner if the loader assumes the v1 flat prompt list.
- Rollback/recovery:
  - Revert manifest and prompt fixture changes together if runner compatibility fails.

### M2. Architecture-review optional scenario fixture

- Milestone state: closed
- Goal: Add the first optional extended benchmark, using a separate architecture-review fixture that tests canonical architecture review without a change-local delta.
- Requirements: `R4`-`R6`, `R8`.
- Files/components likely touched:
  - `benchmarks/token-cost/manifest.yaml`
  - `benchmarks/token-cost/prompts/architecture-review.md`
  - `benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/`
  - `scripts/test-token-cost-measurement.py`
- Dependencies: M1 manifest group support.
- Tests to add/update:
  - Scenario fixture self-contained shape.
  - Optional extended benchmark declaration.
  - No shared overlay requirement until duplication trigger.
- Implementation steps:
  - Add the `architecture-review` optional prompt.
  - Add the separate scenario fixture with canonical architecture package, ADR-not-required note, change metadata, explain-change, and tiny source file.
  - Add fixture tests that ensure no change-local architecture delta is required.
  - Ensure the manifest marks `architecture-review` optional unless changed-skill or claimed-coverage policy requires it later.
- Validation commands:
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`
  - `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py`
- Expected observable result: The optional `architecture-review` benchmark exists and remains separate from the minimal public fixture.
- Commit message: `M2: add architecture-review benchmark fixture`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
  - [x] code-review passed
- Risks:
  - The scenario fixture can grow enough to distort token cost for unrelated prompts if accidentally reused.
- Rollback/recovery:
  - Remove only the optional prompt, fixture, and manifest entry.

### M3. Token-cost validator v2 metadata and context support

- Milestone state: closed
- Goal: Teach standalone token-cost validation to enforce v2 coverage metadata, result quality, waiver roles, claimed optional gates, and required benchmark context.
- Requirements: `R7`-`R9`, `R12`-`R16`, `R17`.
- Files/components likely touched:
  - `scripts/validate-token-cost-report.py`
  - `scripts/test-token-cost-report-validation.py`
  - `tests/fixtures/token-cost/`
  - sample report metadata under `docs/reports/token-cost/releases/` if needed for fixtures
- Dependencies: active v2 test spec.
- Tests to add/update:
  - Valid v2 metadata with required core, transition carryover, and result quality.
  - Missing required benchmark failure.
  - Claimed optional `pass`, `fail`, `inconclusive`, `not-reviewed`, and missing evidence behavior.
  - Unclaimed optional warning-only behavior.
  - Allowed and rejected `approved_role` values.
  - CLI `--required-benchmark-context` loading.
  - In-process validation object coverage if the validator exposes an importable API.
- Implementation steps:
  - Add v2 coverage metadata validation without breaking v1 report validation.
  - Add required benchmark context parsing and validation.
  - Add result-quality schema checks.
  - Add claimed optional coverage gates.
  - Add role enum validation for result-quality waivers.
  - Preserve raw-or-sanitized evidence behavior from v1.
- Validation commands:
  - `python scripts/test-token-cost-report-validation.py`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py`
  - `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases`
- Expected observable result: Standalone validator accepts valid v2 metadata/context and rejects invalid required or claimed coverage cases.
- Commit message: `M3: validate v2 token benchmark coverage metadata`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
  - [x] code-review passed
- Risks:
  - Adding v2 validation can regress v1 release report validation.
- Rollback/recovery:
  - Keep v2 rules gated by suite id and restore v1 fixture validation before proceeding.

### M4. Release validation required benchmark context integration

- Milestone state: implemented and committed; awaiting code-review
- Goal: Generate release-specific required benchmark context from changed surfaces and pass it to token-cost validation.
- Requirements: `R10`-`R13`, `R15`.
- Files/components likely touched:
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`, only if it needs a command-path adjustment
  - release validation tests or fixtures
  - `scripts/test-token-cost-report-validation.py`, if release integration coverage is colocated
- Dependencies: M3 validator API and context support.
- Tests to add/update:
  - Canonical skill change requires benchmark when one exists.
  - Generated adapter skill path traces back to canonical skill.
  - Generated drift without canonical change routes to adapter validation unless a benchmark reason is recorded.
  - Public skill change with no benchmark records warning/follow-up.
  - Invalid governed v2 metadata blocks through release validation delegation.
- Implementation steps:
  - Add required benchmark context construction in release validation.
  - Support in-memory object transport to token-cost validation.
  - Support transient YAML only for CLI/debug paths.
  - Ensure release validation does not track context YAML by default.
  - Add integration test proving invalid governed metadata blocks release validation.
- Validation commands:
  - `python scripts/test-token-cost-report-validation.py`
  - focused release-validation integration test command, added or selected by this milestone
  - `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py`
  - `git diff --check -- scripts/validate-release.py scripts/release-verify.sh scripts/test-token-cost-report-validation.py tests`
- Expected observable result: Focused tests prove release validation decides which benchmarks are required, delegates to token-cost validation, and blocks invalid governed metadata without depending on final `v0.1.1` v2 report evidence.
- Commit message: `M4: integrate required benchmark context into release validation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Git diff range ambiguity can make changed-skill detection brittle.
  - Accidentally running final release validation here can create a false dependency on report metadata intentionally created later.
- Rollback/recovery:
  - Fall back to explicit required benchmark context fixtures until release diff detection is corrected.

### M5. V2 transition report evidence and lifecycle closeout

- Milestone state: planned
- Goal: Preserve pre-transition v1 evidence, add v2 transition report metadata/report evidence, and prepare the initiative for final review gates.
- Requirements: `R1`, `R3`, `R7`-`R9`, `R14`-`R17`.
- Files/components likely touched:
  - `docs/reports/token-cost/releases/v0.1.1.md`
  - `docs/reports/token-cost/releases/v0.1.1.yaml`
  - `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md`
  - `docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml`
  - `docs/reports/token-cost/runs/v0.1.1/`
  - `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/`
  - `docs/plan.md`
  - this plan file
- Dependencies: M1-M4 closed; live Codex run may be waived only according to approved release policy.
- Tests to add/update:
  - Report metadata fixture validation for v2 baseline.
  - Preservation path validation for pre-transition v1 report when applicable.
- Implementation steps:
  - Move or preserve existing v1 report evidence under the pre-transition path when v2 targets `v0.1.1`.
  - Generate or update v2 release metadata with coverage and result-quality fields.
  - Record overlap comparison as informational only.
  - Run the benchmark suite when Codex is available, or record valid waiver/non-final evidence according to release stage.
  - Update change-local validation evidence.
  - Prepare for final code-review, explain-change, verify, and PR handoff after all milestones close.
- Validation commands:
  - `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/test-token-cost-report-validation.py`
  - `python scripts/validate-release.py --version v0.1.1`
  - `bash scripts/ci.sh --mode explicit --path benchmarks/token-cost --path scripts/validate-token-cost-report.py --path scripts/validate-release.py --path docs/reports/token-cost/releases/v0.1.1.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
  - `git diff --check -- benchmarks/token-cost scripts docs/reports/token-cost docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Expected observable result: v2 transition evidence validates, pre-transition v1 evidence remains preserved, and the plan is ready for final implementation review sequence.
- Commit message: `M5: add v2 token benchmark transition report evidence`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Live Codex availability or token variability can affect dynamic evidence.
  - Existing `v0.1.1` report identity can be mishandled if preservation is not done atomically.
- Rollback/recovery:
  - Restore v1 report paths and keep v2 report under an RC or next-release path until validated.

## Validation plan

Plan-stage validation:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/plan.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `git diff --check -- docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`

Implementation-stage validation is listed per milestone. Prefer the smallest relevant command first, then broaden through `bash scripts/ci.sh --mode explicit --path ...` before final closeout.

## Risks and recovery

| Risk | Recovery |
|---|---|
| v2 manifest shape breaks v1 runner assumptions | Add compatibility handling in the runner and keep tests for v1 fixture shape. |
| Required benchmark context generation is ambiguous from git state | Allow explicit YAML context for debugging and tests; keep generated context transient unless cited as release evidence. |
| Claimed optional coverage is accidentally summarized as passing optional evidence | Validator blocks claimed optional failures and requires unclaimed warning evidence if coverage is not claimed. |
| Pre-transition v1 report is overwritten | Preserve v1 under the pretransition path before writing canonical v2 report. |
| Codex is unavailable for live dynamic runs | Use dry-run and validator evidence during implementation; final release uses pass or a valid waiver only. |
| Fixture duplication grows too quickly | Keep separate fixtures until three scenario fixtures duplicate base files or review flags drift. |

## Dependencies

- Approved v2 spec and architecture update.
- Clean architecture-review R1.
- Plan-review approval before test-spec and implementation.
- Test spec before implementation.
- Existing v1 validator, runner, analyzer, and release-validation scripts.
- Public Codex adapter output generated under `dist/adapters/codex/.agents/skills/` for live benchmark runs.

## Progress

- 2026-05-11: Plan created after approved spec, canonical architecture update, and clean architecture-review R1.
- 2026-05-11: Plan-review R2 approved the revised plan after EDTF-PL1 and EDTF-PL2 resolution.
- 2026-05-11: Test spec created and marked active; next stage is M1 implementation.
- 2026-05-11: M1 implementation updated the manifest to `skill-token-runtime-v2`, added required core prompts for `plan-handoff`, `explain-change-summary`, and `pr-handoff`, kept transition carryover prompts in the executable list, and updated prompt fixture tests.
- 2026-05-11: Code-review M1 R1 found no material findings and closed M1; next stage is M2 implementation.
- 2026-05-11: M2 implementation added the optional `architecture-review` prompt declaration, prompt fixture, and separate `minimal-public-project-architecture-review` scenario fixture with canonical architecture package, ADR-not-required note, change metadata, explain-change evidence, spec, diagrams, and tiny source file.
- 2026-05-11: Code-review M2 R1 found no material findings and closed M2; next stage is M3 implementation.
- 2026-05-11: M3 implementation added standalone validator support for v2 benchmark coverage metadata, per-run manual `result_quality`, required benchmark context via in-process API and `--required-benchmark-context`, role-scoped result-quality waivers, claimed optional gates, changed-skill-required benchmark enforcement, and unclaimed optional warning behavior.
- 2026-05-11: Code-review M3 R1 found EDTF-CR1, a major validator gap where optional dynamic run `result_quality.status` can be hidden by mismatched `benchmark_coverage.optional_run[*].result_quality_status`; M3 is in `resolution-needed`.
- 2026-05-11: EDTF-CR1 was accepted and fixed by reconciling optional coverage result-quality status with actual dynamic run result-quality status and adding focused mismatch tests; M3 is ready for code-review rerun.
- 2026-05-11: Code-review M3 R2 found no material findings and closed M3; next stage is M4 implementation.
- 2026-05-11: M4 implementation added release-side required benchmark context generation, generated adapter path tracing, changed-skill missing-benchmark warning metadata, and in-process token-cost validator delegation for v2 reports; next stage is code-review M4.

## Decision log

- 2026-05-11: Use five implementation milestones plus a pre-implementation test-spec gate rather than one broad implementation slice -> the work spans manifest/prompt fixtures, scenario fixture, standalone validation, release validation integration, and report evidence.
- 2026-05-11: Keep test-spec outside the implementation milestone loop -> `test-spec` is the next workflow stage after plan-review, and implementation must not start until proof design is active.
- 2026-05-11: Keep validator support and release validation integration separate -> token-cost report schema validation and release changed-surface detection have different ownership.
- 2026-05-11: Keep real `validate-release.py --version v0.1.1` in M5 -> final release validation depends on v2 report evidence created in the report-evidence milestone.
- 2026-05-11: Keep the runner executable manifest as a flat `prompts:` list in M1 while adding v2 grouping metadata beside it -> the current runner can enumerate all required prompts without a loader refactor, and validator/report grouping work remains scoped to later milestones.
- 2026-05-11: Add `architecture-review` under `optional_prompts` rather than the flat executable `prompts` list -> M2 makes the optional benchmark discoverable and fixture-backed without making it part of the release-required dry-run set before runner/validator optional-suite handling lands.
- 2026-05-11: Gate v2-only validation by `skill-token-runtime-v2` suite id or an explicit required benchmark context -> the historical v1 report fixture keeps its existing schema while v2 reports receive the new coverage and result-quality checks.
- 2026-05-11: Keep required benchmark context validation in the token-cost validator but leave changed-surface detection for M4 release validation -> M3 proves the context contract without moving release diff analysis into the standalone validator.
- 2026-05-11: Keep the tracked `v0.1.1` v1 report on the existing release validation path until M5 creates v2 evidence -> M4 only passes required benchmark context when the governed token-cost report declares `skill-token-runtime-v2`, preserving pre-transition validation.

## Surprises and discoveries

- none yet

## Validation notes

- 2026-05-11: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed with `reviews=7`, `findings=6`, `log_entries=7`, and `resolution_entries=6`.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ... plan-review-r2.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md ...` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.test.md docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed.
- 2026-05-11: `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_manifest_lists_v2_prompt_groups_and_fixtures` failed before implementation because the manifest still declared `skill-token-runtime-v1`; it passed after the v2 manifest and prompt fixture updates.
- 2026-05-11: `python scripts/test-token-cost-measurement.py` passed.
- 2026-05-11: `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex` passed and enumerated the ten required core plus transition carryover benchmarks.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after M1 implementation.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ... explain-change.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed.
- 2026-05-11: Code-review M1 R1 reviewer reran `python scripts/test-token-cost-measurement.py`; passed 23 tests.
- 2026-05-11: Code-review M1 R1 reviewer reran `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; passed.
- 2026-05-11: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed after M1 code-review closeout with `reviews=8`, `findings=6`, `log_entries=8`, and `resolution_entries=6`.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ... code-review-m1-r1.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_architecture_review_optional_prompt_and_fixture_are_self_contained` failed before M2 implementation because `optional_prompts` and the scenario fixture were missing; it passed after the optional prompt and fixture were added.
- 2026-05-11: `python scripts/test-token-cost-measurement.py` passed with 24 tests after M2 implementation.
- 2026-05-11: `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex` passed after M2 implementation; the optional prompt declaration did not change the current required/carryover dry-run execution list.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after M2 implementation.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ... explain-change.md` passed after M2 implementation with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/plan.md` passed.
- 2026-05-11: Code-review M2 R1 reviewer reran `python scripts/test-token-cost-measurement.py`; passed 24 tests.
- 2026-05-11: Code-review M2 R1 reviewer reran `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; passed.
- 2026-05-11: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed after M2 code-review closeout with `reviews=9`, `findings=6`, `log_entries=9`, and `resolution_entries=6`.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ... code-review-m2-r1.md` passed with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_result_quality_and_required_context_are_enforced_by_cli TokenCostReportValidatorTests.test_v2_required_benchmark_context_is_supported_in_process TokenCostReportValidatorTests.test_v2_required_benchmark_result_quality_waiver_roles_are_enforced TokenCostReportValidatorTests.test_v2_claimed_optional_coverage_is_gated_and_unclaimed_optional_warns TokenCostReportValidatorTests.test_v2_changed_skill_required_context_requires_optional_benchmark` failed before M3 implementation because the validator lacked `--required-benchmark-context` parsing and the `validate_token_cost_report` in-process API; it passed after M3 implementation.
- 2026-05-11: `python scripts/test-token-cost-report-validation.py` passed with 15 tests after M3 implementation.
- 2026-05-11: `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml` passed after M3 implementation, confirming v1 report validation remains compatible.
- 2026-05-11: `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py` passed after M3 implementation.
- 2026-05-11: `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases` passed after M3 implementation.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after M3 handoff artifact updates.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/plan.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/explain-change.md` passed after M3 with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/plan.md` passed after M3 handoff artifact updates.
- 2026-05-11: `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_optional_coverage_result_quality_must_match_dynamic_run` failed before the EDTF-CR1 fix because mismatched optional coverage/run status passed; it passed after the validator reconciliation fix.
- 2026-05-11: `python scripts/test-token-cost-report-validation.py` passed with 16 tests after the EDTF-CR1 fix.
- 2026-05-11: `python -m py_compile scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py` passed after the EDTF-CR1 fix.
- 2026-05-11: `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml` passed after the EDTF-CR1 fix.
- 2026-05-11: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed after EDTF-CR1 resolution with `reviews=10`, `findings=7`, `log_entries=10`, and `resolution_entries=7`.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after EDTF-CR1 resolution.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-resolution.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/review-log.md --path docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/plan.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after EDTF-CR1 resolution with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests docs/reports/token-cost/releases docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/plan.md` passed after EDTF-CR1 resolution.
- 2026-05-11: Code-review M3 R2 reviewer reran `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_v2_optional_coverage_result_quality_must_match_dynamic_run`; passed.
- 2026-05-11: Code-review M3 R2 reviewer reran `python scripts/test-token-cost-report-validation.py`; passed with 16 tests.
- 2026-05-11: Code-review M3 R2 reviewer reran `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`; passed with `reviews=10`, `findings=7`, `log_entries=10`, and `resolution_entries=7`.
- 2026-05-11: Code-review M3 R2 reviewer reran `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`; passed.
- 2026-05-11: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_required_benchmark_context_requires_changed_skill_benchmark AdapterDistributionTests.test_required_benchmark_context_traces_generated_adapter_paths AdapterDistributionTests.test_generated_only_adapter_change_does_not_require_dynamic_benchmark AdapterDistributionTests.test_changed_public_skill_without_benchmark_records_warning_follow_up` failed before M4 implementation because release validation did not expose required benchmark context construction; it passed after the context builder and generated adapter path tracing were added.
- 2026-05-11: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_release_validation_passes_required_context_to_token_cost_validation` passed after M4 implementation, proving v2 release validation delegates to token-cost validation with generated required benchmark context.
- 2026-05-11: `python scripts/test-token-cost-report-validation.py` passed with 16 tests after M4 implementation.
- 2026-05-11: `python scripts/test-adapter-distribution.py` passed with 64 tests after M4 implementation.
- 2026-05-11: `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py` passed after M4 implementation.
- 2026-05-11: `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml` passed after M4 implementation.
- 2026-05-11: `python scripts/validate-release.py --version v0.1.1` passed after M4 implementation, confirming the v1 pre-transition report still validates before M5 creates v2 report evidence.
- 2026-05-11: `git diff --check -- scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py scripts/test-token-cost-report-validation.py tests docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md` passed after M4 implementation.
- 2026-05-11: `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml` passed after M4 artifact updates.
- 2026-05-11: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md --path docs/plan.md --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml --path docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/explain-change.md` passed after M4 artifact updates with the existing unrelated `docs/plan.md` lifecycle-language warning.
- 2026-05-11: `git diff --check -- scripts/validate-release.py scripts/adapter_distribution.py scripts/test-adapter-distribution.py scripts/test-token-cost-report-validation.py tests docs/plan.md docs/plans/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills` passed after M4 artifact updates.

## Outcome and retrospective

- Pending. This initiative is not done until all in-scope implementation milestones are closed and downstream review, explain-change, verify, and PR handoff are complete.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- Consider a later shared fixture overlay proposal after the third duplicated scenario fixture or a duplication-related review finding.
- Consider structured expected-output checks only after manual result-quality review patterns stabilize.
