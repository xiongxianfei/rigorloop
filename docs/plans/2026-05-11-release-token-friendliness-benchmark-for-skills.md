# Release Token-Friendliness Benchmark for Skills

- Status: active
- Owner: maintainer
- Start date: 2026-05-11
- Last updated: 2026-05-11
- Related issue or PR: none yet
- Supersedes: none

## Purpose / Big Picture

This plan turns the approved release Token-Friendliness benchmark contract into reviewable implementation slices.

The implementation adds a release evidence surface that proves public skills remain token-friendly during real agent use. It must keep Markdown reports human-readable, YAML metadata machine-checkable, benchmark prompts fixture-backed, Codex runtime evidence reproducible, raw JSONL privacy-safe, and release validation waiver-aware.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- Spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Architecture: `docs/architecture/system/architecture.md`
- Architecture diagram: `docs/architecture/system/diagrams/container.mmd`
- Review records: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/`
- Review resolution: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md`
- Test spec: `specs/release-token-friendliness-benchmark-for-skills.test.md`

## Context and Orientation

Relevant existing surfaces:

- `scripts/measure-skill-tokens.py` already measures static skill size.
- `scripts/analyze-codex-jsonl.py` already reads Codex JSONL and reports token usage plus command-output amplification.
- `scripts/validate-release.py` validates `docs/releases/<version>/release.yaml` and release notes through adapter distribution helpers.
- `scripts/release-verify.sh` is the release-owned gate for known public release versions.
- `docs/reports/token-cost/2026-05-10-baseline.md` is historical baseline evidence, not the new per-release report format.
- `dist/adapters/codex/.agents/skills/` is the public Codex adapter skill source for release benchmarks.
- `.codex/skills/` is a repository-local generated mirror and must not be used as the public release benchmark source.

No `benchmarks/` directory exists yet. This plan creates the first `benchmarks/token-cost/` fixture surface.

## Non-goals

- Do not make token score the only release-quality measure.
- Do not introduce hard total-token regression blockers in this first implementation.
- Do not add hosted telemetry infrastructure.
- Do not require contributors to install Claude Code or opencode for v1.
- Do not add a full Markdown report generator.
- Do not optimize every skill in this change.
- Do not hand-edit generated adapter output.
- Do not replace existing adapter validation or release metadata; add token-cost evidence beside it.

## Requirements Covered

- `R1`-`R4`: release Markdown plus YAML report paths, schema identity, enums, and Markdown summary shape.
- `R5`: static skill measurement evidence.
- `R6`-`R7`: final dynamic benchmark requirement and waiver semantics.
- `R8`-`R10`: benchmark manifest, prompt fixtures, minimal fixture, and public Codex skill installation.
- `R11`-`R13`: benchmark runner, temp policy, Codex execution, JSONL output, and automatic analyzer invocation.
- `R14`-`R18`: raw or sanitized evidence, analyzer summary schema, dynamic summary, command-output amplification, and full-file-read signal reporting.
- `R19`: public skill portability results.
- `R20`-`R23`: runner invocation metadata, previous-release comparison, RC reuse, and benchmark-relevant change classification.
- `R24`-`R26`: token-cost validator ownership, release validation delegation, and blocking conditions.
- `R27`-`R28`: warning and future hard-gate semantics.
- `R29`-`R30`: optional non-Codex dynamic benchmarks and deferred report generator.
- `R31`: reviewable implementation milestones.
- `R32`: release notes link requirement.
- `R33`: generated adapter output remains derived.

## Current Handoff Summary

- Current milestone: M5. Release validation integration and documentation
- Current milestone state: closed
- Last reviewed milestone: M5 code-review R10 clean-with-notes
- Review status: M5 closed with no material findings after RTF-CR8 resolution.
- Remaining in-scope implementation milestones: none
- Next stage: explain-change
- Final closeout readiness: ready to start final closeout
- Reason final closeout is or is not ready: All in-scope implementation milestones are closed and review-resolution is closed; explain-change, verify, and PR handoff remain.

## Milestones

### M1. Metadata schema and validator

- Milestone state: closed
- Goal: Add the structured token-cost release metadata contract and standalone validator.
- Requirements: `R1`-`R7`, `R14`-`R16`, `R19`-`R28`, `R29`, `R30`
- Files/components likely touched:
  - `scripts/validate-token-cost-report.py`
  - `tests/fixtures/` for token-cost metadata cases
  - `scripts/test-token-cost-report-validation.py` or existing focused test harness
- Dependencies: approved spec and architecture; no benchmark runner dependency for schema tests.
- Tests to add/update:
  - valid final pass metadata;
  - final `waived` metadata with complete waiver;
  - final `blocked` or `not-run` rejected;
  - non-final `blocked` or `not-run` requires `dynamic_runtime.incomplete`;
  - raw JSONL tracked evidence path validation;
  - omitted raw JSONL requires analyzer or sanitized summary evidence;
  - first baseline comparison shape;
  - comparable prior-release deltas;
  - public portability failure blocks;
  - runner metadata path/source mismatch blocks.
- Implementation steps:
  1. Define the validator command surface.
  2. Parse the schema version 1 metadata with existing lightweight conventions when safe.
  3. Validate required sections, required fields, enums, waiver fields, incomplete dynamic fields, evidence references, comparison shape, and runner metadata.
  4. Add fixtures and negative tests for standalone token-cost metadata validation.
  5. Leave `scripts/validate-release.py`, `scripts/release-verify.sh`, governed-release scope, and release-level delegation to M5.
- Validation commands:
  - `python scripts/validate-token-cost-report.py <sample-metadata>`
  - `python -m py_compile scripts/validate-token-cost-report.py`
  - `python scripts/test-token-cost-report-validation.py`
  - `git diff --check -- scripts/validate-token-cost-report.py tests/fixtures`
- Expected observable result: Token-cost release metadata can be validated standalone without changing release-level validation.
- Commit message: `M1: add token-cost release metadata validation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M1
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - lightweight YAML parsing may be too weak for nested lists and maps;
  - standalone schema tests could drift from later release-level integration expectations.
- Rollback/recovery:
  - keep standalone validator fixtures to preserve schema lessons;
  - if lightweight parsing is unsafe, record the reason and add a scoped YAML parser dependency in this milestone before proceeding.
  - if schema assumptions conflict with M5 release integration, revise standalone fixtures before wiring the release gate.

### M2. Benchmark fixture and prompt suite

- Milestone state: closed
- Goal: Add the first executable benchmark suite and clean downstream project fixture.
- Requirements: `R8`-`R10`, `R31`
- Files/components likely touched:
  - `benchmarks/token-cost/manifest.yaml`
  - `benchmarks/token-cost/prompts/*.md`
  - `benchmarks/token-cost/fixtures/minimal-public-project/`
  - focused fixture validation tests if needed
- Dependencies: M1 not strictly required, but manifest shape should match validator expectations.
- Tests to add/update:
  - manifest includes all seven benchmark ids;
  - prompt paths exist;
  - fixture path exists and contains required downstream-project files;
  - fixture does not include installed `.codex/skills/` or `.agents/skills/` generated skill copies.
- Implementation steps:
  1. Create `benchmarks/token-cost/manifest.yaml` with suite id `skill-token-runtime-v1`.
  2. Add seven prompt fixtures: `workflow-route`, `proposal-short`, `implement-handoff`, `code-review-small`, `verify-final-pack`, `architecture-no-impact`, and `learn-no-durable-lesson`.
  3. Add the minimal public project fixture with `AGENTS.md`, `VISION.md`, `README.md`, `docs/workflows.md`, `docs/changes/.gitkeep`, and `src/example.txt`.
  4. Keep fixture content small and free of RigorLoop repository internals.
- Validation commands:
  - `test -f benchmarks/token-cost/manifest.yaml`
  - `find benchmarks/token-cost -maxdepth 4 -type f | sort`
  - `git diff --check -- benchmarks/token-cost`
- Expected observable result: The benchmark suite can be reviewed as tracked fixtures before any runtime runner exists.
- Commit message: `M2: add token-cost benchmark fixtures`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M2
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - fixture may become too repository-specific;
  - prompts may accidentally ask for edits.
- Rollback/recovery:
  - remove or revise prompts independently;
  - fixture is authored test data and can be adjusted without generated-output migration.

### M3. Runner and analyzer-summary integration

- Milestone state: closed
- Goal: Add repeatable Codex benchmark execution and analyzer summary output.
- Requirements: `R11`-`R18`, `R20`, `R25`, `R29`, `R33`
- Files/components likely touched:
  - `scripts/run-token-cost-benchmarks.py`
  - `scripts/analyze-codex-jsonl.py`
  - `scripts/test-token-cost-measurement.py`
  - `tests/fixtures/token-cost/`
- Dependencies: M2 fixtures; public Codex adapter output generated by existing adapter generation before real release runs.
- Tests to add/update:
  - runner dry-run or command-construction test;
  - temp fixture copy does not mutate source fixture;
  - public skill source must be `dist/adapters/codex/.agents/skills/`;
  - `.codex/skills/` source is rejected;
  - output paths land under `docs/reports/token-cost/runs/<release>/`;
  - analyzer can emit schema version 1 summary for tracked raw JSONL;
  - analyzer can emit schema version 1 summary for omitted raw JSONL/sanitized summary;
  - command-output amplification and signal counts are preserved.
- Implementation steps:
  1. Add runner CLI with `--release`, `--suite`, `--tool codex`, `--fixture`, `--temp-root`, `--keep-temp`, `--keep-failed-temp`, and `--output-dir`.
  2. Implement temp-root policy for local and CI.
  3. Copy the clean fixture into temp, then copy public Codex skills into `<temp-fixture>/.agents/skills/`.
  4. Execute prompt fixtures with `codex exec --json --ephemeral` when not in dry-run/test mode.
  5. Save JSONL and invoke `scripts/analyze-codex-jsonl.py` automatically.
  6. Extend the analyzer to write machine-readable summary files matching `R15`.
  7. Keep report generation out of this milestone.
- Validation commands:
  - `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py`
  - `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`
  - `python scripts/test-token-cost-measurement.py`
  - `git diff --check -- scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py tests/fixtures/token-cost`
- Expected observable result: Maintainers can run one command to prepare temp fixture runs and analyzer summaries; tests can verify runner behavior without requiring Codex availability.
- Commit message: `M3: add token-cost benchmark runner`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M3
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Codex may be unavailable in local or CI validation;
  - temp cleanup mistakes can leave local artifacts;
  - analyzer summary format could drift from release metadata expectations.
- Rollback/recovery:
  - keep analyzer summary extension independent from live runner execution;
  - provide dry-run or test mode for unit-style validation;
  - if Codex is unavailable, validate command construction and fixture preparation while recording dynamic run as blocked only in release metadata, not in tests.

### M4. First baseline report and release report template

- Milestone state: closed
- Goal: Add the first release Token-Friendliness report format and baseline metadata without adding a full report generator.
- Requirements: `R1`-`R7`, `R14`-`R23`, `R27`-`R30`, `R32`
- Files/components likely touched:
  - `docs/reports/token-cost/releases/<release-version>.md`
  - `docs/reports/token-cost/releases/<release-version>.yaml`
  - `docs/reports/token-cost/runs/<release-version>/` for tracked sample or real run summaries
  - `docs/releases/<release-version>/release-notes.md`
  - report template documentation if needed
- Dependencies: M1 validator; M2 fixtures; M3 runner/analyzer.
- Tests to add/update:
  - validator accepts first-baseline metadata;
  - Markdown report names YAML metadata;
  - release notes link to the token-friendliness report;
  - raw JSONL omitted case is accepted when sanitized summary exists.
- Implementation steps:
  1. Choose the first policy release version from the active release context.
  2. Run static measurement.
  3. Run dynamic benchmarks when Codex is available, or record a valid non-final blocked/not-run state if still pre-final.
  4. Write the Markdown report manually.
  5. Write YAML metadata with `comparison.baseline: true` if no previous release report exists.
  6. Validate the report and update release notes with a report link.
- Validation commands:
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release <release-version> --tool codex`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/<release-version>.yaml`
  - `git diff --check -- docs/reports/token-cost docs/releases`
- Expected observable result: The first release Token-Friendliness report exists as Markdown plus YAML and can be validated.
- Commit message: `M4: add token-friendliness baseline report`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M4
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - raw JSONL may contain local data and require sanitized summaries;
  - Codex may be unavailable for the release runner;
  - first baseline could be confused with older non-release baseline reports.
- Rollback/recovery:
  - remove release-gate requirement if benchmark tooling proves unreliable;
  - keep historical report as evidence;
  - use waiver or non-final incomplete metadata only when allowed by the spec.

### M5. Release validation integration and documentation

- Milestone state: closed
- Goal: Wire token-friendliness validation into release readiness and contributor-facing release guidance.
- Requirements: `R24`-`R33`
- Files/components likely touched:
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`
  - `docs/workflows.md`
  - `AGENTS.md` only if concise root guidance needs release pointer changes
  - release validation tests/fixtures
- Dependencies: M1 validator and at least one valid report fixture; M4 report if final release validation requires real evidence.
- Tests to add/update:
  - release validation calls token-cost validator for governed versions;
  - historical releases are not accidentally broken unless policy requires them;
  - missing token-cost report blocks governed public release;
  - valid waiver passes final release only when complete;
  - portability failure blocks;
  - warning-only token regression does not block.
- Implementation steps:
  1. Decide the release-version scope that first requires token-cost report validation.
  2. Delegate from release validation to the token-cost report validator.
  3. Update release verification script to include the new gate when applicable.
  4. Update workflow/release guidance to name the benchmark/report process and command sequence.
  5. Keep Claude Code and opencode dynamic measurements optional.
  6. Ensure release notes link behavior is documented.
- Validation commands:
  - `python scripts/validate-release.py --version <release-version>`
  - `bash scripts/release-verify.sh <release-version>`
  - `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py`
  - `git diff --check -- scripts/validate-release.py scripts/release-verify.sh docs/workflows.md AGENTS.md`
- Expected observable result: Public release validation fails missing or invalid token-cost evidence for governed releases and remains warning-only for token regressions.
- Commit message: `M5: gate releases on token-friendliness evidence`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] hand off to code-review for M5
  - [x] code-review completed
  - [x] material findings resolved or explicitly dispositioned
  - [x] progress updated
  - [ ] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - release verifier scope may be too broad for historical releases;
  - release notes and token-cost reports may drift;
  - contributors may confuse warnings with blockers.
- Rollback/recovery:
  - keep standalone validator while removing release-level delegation;
  - document any waiver or temporary blocked state in release metadata;
  - preserve warning-only token thresholds until a later accepted hard-gate proposal.

## Validation Plan

Milestone validation starts narrow and expands only when the changed surface requires it.

Baseline checks for plan artifacts:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml
python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml
git diff --check -- docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml
```

Implementation validation will include:

```bash
python scripts/measure-skill-tokens.py
python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/<release-version>.yaml
python scripts/validate-release.py --version <release-version>
python -m py_compile scripts/measure-skill-tokens.py scripts/analyze-codex-jsonl.py scripts/run-token-cost-benchmarks.py scripts/validate-token-cost-report.py scripts/validate-release.py
git diff --check --
```

When the release changes canonical skills or public adapter output:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

When final release verification is in scope:

```bash
bash scripts/release-verify.sh <release-version>
```

## Risks and Recovery

- Schema/validator overreach: keep validator standalone first, add release delegation only after fixtures prove the schema.
- YAML parser limitation: use existing lightweight conventions first, but add a scoped dependency only with recorded rationale.
- Codex unavailable: tests should validate dry-run behavior and metadata states; final release still requires `pass` or valid `waived`.
- Sensitive raw JSONL: use sanitized summaries and omission reasons rather than committing raw local data.
- Wrong skill source: hard-code or validate the public source `dist/adapters/codex/.agents/skills/` and reject `.codex/skills/`.
- Historical release breakage: scope release-token validation to governed release versions.
- Report generator temptation: keep Markdown manual in this plan; defer generator to a later proposal after repeated manual errors or three comparable reports.

## Dependencies

- Approved spec and canonical architecture update are complete.
- Plan-review must approve this plan before implementation.
- Test-spec should be created after plan-review and before implementation.
- M2 depends on no generated output.
- M3 depends on M2 fixtures.
- M4 depends on M1 validator and M3 runner/analyzer for real report evidence.
- M5 depends on M1 validator and ideally M4 baseline report evidence.

## Progress

- 2026-05-11: Created plan after approved proposal, spec, and architecture-review.
- 2026-05-11: Revised M1 after plan-review R1 to keep standalone token-cost metadata validation separate from M5 release validation integration.
- 2026-05-11: Plan-review R2 approved the revised plan for test-spec handoff.
- 2026-05-11: Created active test spec and moved the handoff to implement M1.
- 2026-05-11: Implemented M1 standalone token-cost report metadata validator, fixture-backed tests, and valid report evidence cases; M1 is ready for code-review.
- 2026-05-11: Code-review R1 requested M1 fixes for RC reuse metadata validation and Markdown report metadata-link validation.
- 2026-05-11: Resolved code-review R1 findings with RC reuse validation, Markdown/YAML pairing validation, and focused tests; M1 is ready for code-review rerun.
- 2026-05-11: Code-review R2 requested an M1 fix for partial RC reuse checked-surface validation; RTF-CR3 is open.
- 2026-05-11: Resolved RTF-CR3 by requiring all RC reuse checked-surface categories and adding per-category negative tests; M1 is ready for code-review rerun.
- 2026-05-11: Code-review R3 found no material findings for M1; M1 is closed and the plan is ready for implement M2.
- 2026-05-11: Started M2 implementation for benchmark manifest, prompt fixtures, clean minimal fixture, and focused fixture validation.
- 2026-05-11: Added fixture-first tests for benchmark manifest, seven prompt fixtures, clean minimal fixture contents, absence of installed skills, and absence of generated-surface references.
- 2026-05-11: Added `benchmarks/token-cost/manifest.yaml`, seven no-edit prompt fixtures, and the clean minimal public project fixture; M2 is ready for code-review.
- 2026-05-11: Code-review R4 found no material findings for M2; M2 is closed and the plan is ready for implement M3.
- 2026-05-11: Started M3 implementation for the benchmark runner, analyzer schema-versioned summaries, and dry-run/test-mode proof surfaces.
- 2026-05-11: Added failing M3 tests for analyzer tracked and omitted raw JSONL summaries, runner dry-run installation, public skill source rejection, temp-root isolation, cleanup behavior, analyzer invocation, and no Markdown generation.
- 2026-05-11: Implemented `scripts/run-token-cost-benchmarks.py` and extended `scripts/analyze-codex-jsonl.py` to write schema version 1 summaries beside JSONL runs; M3 is ready for code-review.
- 2026-05-11: Code-review R5 requested M3 fixes for analyzer summary path stability, repeated same-file read signals, and justified full-file-read classification.
- 2026-05-11: Resolved RTF-CR4, RTF-CR5, and RTF-CR6 with repo-relative analyzer summary paths, repeated capped read signals, justified read classification, and focused tests; M3 is ready for code-review rerun.
- 2026-05-11: Code-review R6 found no material findings for M3; M3 is closed and the plan is ready for implement M4.
- 2026-05-11: Started M4 implementation for the first Token-Friendliness baseline report, release metadata, sanitized analyzer summaries, and release-notes link.
- 2026-05-11: Live Codex benchmark execution first failed in the disposable temp fixture because Codex requires `--skip-git-repo-check` outside trusted repositories; added runner/test coverage for the normalized command and reran successfully.
- 2026-05-11: Added the `v0.1.1` Token-Friendliness Markdown report, YAML metadata, sanitized per-run analyzer summaries, and release-notes link; M4 is ready for code-review.
- 2026-05-11: Code-review R7 requested an M4 fix for analyzer parsing of current Codex `command_execution` `aggregated_output` events; RTF-CR7 is open.
- 2026-05-11: Resolved RTF-CR7 by parsing current Codex `command_execution` `aggregated_output` events, adding focused analyzer coverage, rerunning the v0.1.1 benchmark, regenerating sanitized summaries, and correcting the Markdown/YAML baseline report; M4 is ready for code-review rerun.
- 2026-05-11: Code-review R8 found no material findings for M4 after RTF-CR7 resolution; M4 is closed and the plan is ready for implement M5.
- 2026-05-11: Started M5 implementation for release validation integration and documentation.
- 2026-05-11: Added release-level token-cost report validation for governed `v0.1.1`, added release verifier invocation, updated release metadata/workflow guidance, and added regression tests for missing token-cost evidence and historical release scope; M5 is ready for code-review.
- 2026-05-11: Code-review R9 requested an M5 test fix for invalid governed token-cost metadata propagation through release validation; RTF-CR8 is open.
- 2026-05-11: Resolved RTF-CR8 by adding a release-level integration test that points governed `v0.1.1` release validation at invalid token-cost metadata, asserting the token-cost validator failure is propagated, and clarifying T16 test-spec language; M5 is ready for code-review rerun.
- 2026-05-11: Code-review R10 found no material findings after RTF-CR8 resolution; M5 is closed and the plan is ready for final closeout via explain-change.

## Decision Log

- 2026-05-11: Use five implementation milestones matching the proposal/spec slicing: schema and validator, fixtures, runner/analyzer, first report, and release integration. This keeps each review loop focused on one durable responsibility.
- 2026-05-11: Keep report generation out of scope. The approved spec defers a generator until repeated manual-report errors or three comparable stable reports.
- 2026-05-11: Treat live Codex execution as release-run evidence, not a unit-test prerequisite. Runner tests should cover deterministic setup and command construction without requiring every contributor to have Codex installed.
- 2026-05-11: M1 uses the repository's lightweight YAML parsing style with local schema/semantic checks rather than adding a YAML dependency. The schema version 1 metadata shape used in M1 is covered by standalone fixtures.
- 2026-05-11: M3 runner uses a `--dry-run` test mode that prepares the temp fixture, installs public Codex skills, writes synthetic JSONL, and invokes the real analyzer without requiring local Codex availability.

## Surprises and Discoveries

- No `benchmarks/` directory exists yet; M2 creates the benchmark fixture root.
- M1 can validate runner metadata shape before the runner exists by using test fixture paths and checking the required public skill source string.
- Code-review R1 found that RC reuse and Markdown/YAML pairing were part of the M1 validator contract, not later release integration. Both are now covered by standalone tests.
- Code-review R2 found that RC reuse checked-surface validation must reject partial surface coverage, not only no-surface coverage.
- RTF-CR3 resolution keeps model/tool version mandatory as an addressed category, including unknown/unchanged wording through accepted synonyms, so final-release RC reuse decisions have a consistent review surface.
- Code-review R3 closed M1 without new material findings and handed the plan to M2.
- M2 fixture validation deliberately checks the clean source fixture only. Public skill installation remains M3 runner scope.
- The plan's `find benchmarks/token-cost -maxdepth 4 -type f | sort` command does not list the deeper `docs/changes/.gitkeep` fixture file, but the focused test checks it directly.
- Code-review R4 closed M2 without new material findings and confirmed public skill installation remains M3 runner scope.
- M3 reuses the existing lightweight YAML parser from `scripts/validate-token-cost-report.py` for the benchmark manifest instead of adding a dependency.
- M3 keeps live Codex execution available for release runs, but contributor tests use `--dry-run` so Codex installation is not required for ordinary validation.
- Analyzer full-file read evidence now uses event context, so small capped excerpts are not counted as full-file reads solely because the command starts at line 1.
- Code-review R5 found that M3 still needs explicit proof and implementation for stable repo-relative summary paths, repeated capped same-file read signals, and justified full-file-read classification.
- RTF-CR4 resolution keeps absolute paths only for JSONL outside the repository; repository output paths now become stable repo-relative summary evidence.
- RTF-CR5 resolution counts repeated file-read-like paths independently from full-file classification and reports repeated files rather than extra reads.
- RTF-CR6 resolution adds a small `--justified-read` plus `--justification` analyzer interface for explicit whole-file or generated-output validation cases.
- Code-review R6 closed M3 with no new material findings after the R5 resolution.
- M4 records raw JSONL as omitted for the baseline report because live Codex JSONL contained disposable local temp fixture paths and full command output. The tracked analyzer summaries are the sanitized release evidence.
- M4 adjusted the runner Codex invocation to include `--skip-git-repo-check` because the benchmark fixture intentionally runs outside the repository working tree.
- Code-review R7 found that the analyzer does not parse current Codex command output stored in `aggregated_output`, so the M4 command-output amplification evidence must be regenerated after analyzer coverage is fixed.
- RTF-CR7 resolution found current Codex `command_execution` events expose command output through nested `item.aggregated_output`. Corrected analyzer summaries now show non-zero command-output amplification and confirmed skill-file reads for the v0.1.1 baseline.
- M5 scopes the first required token-cost release gate to `v0.1.1`; earlier release targets remain validated by the existing adapter/release checks without requiring backfilled token-cost metadata.
- `python scripts/validate-release.py --version v0.1.0` fails against the current repository-generated `dist/adapters/manifest.yaml` because the working tree holds `0.1.1` adapter output. The historical-scope behavior is covered through fixture-backed release validation and `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.0`.
- Code-review R9 found that M5 release validation integration still needs direct proof that invalid governed token-cost metadata blocks through validator delegation, not only missing-report and valid-report proof.
- RTF-CR8 resolution uses an invalid copy of the existing valid token-cost fixture with `report.report_markdown` removed. This keeps release-level coverage narrow while proving validator-delegation failure propagation.

## Validation Notes

- `python scripts/test-token-cost-report-validation.py` passed.
- `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml` passed.
- `python -m py_compile scripts/validate-token-cost-report.py` passed.
- `python scripts/test-token-cost-measurement.py` passed as a regression check for existing token-cost measurement scripts.
- `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py tests/fixtures/token-cost` passed.
- Code-review R1 resolution: `python scripts/test-token-cost-report-validation.py` passed 9 tests; `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`, `python -m py_compile scripts/validate-token-cost-report.py`, `python scripts/test-token-cost-measurement.py`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r1.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- Code-review R2 resolution: `python scripts/test-token-cost-report-validation.py` passed 10 tests; `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`, `python -m py_compile scripts/validate-token-cost-report.py`, `python scripts/test-token-cost-measurement.py`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r2.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- Code-review R3 validation rerun: `python scripts/test-token-cost-report-validation.py` passed 10 tests; `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`, `python -m py_compile scripts/validate-token-cost-report.py`, `python scripts/test-token-cost-measurement.py`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and `git diff --check -- scripts/validate-token-cost-report.py scripts/test-token-cost-report-validation.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r2.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- M2 test-first proof: `python scripts/test-token-cost-measurement.py` failed before fixture creation with missing `benchmarks/token-cost/manifest.yaml` and missing fixture `AGENTS.md`.
- M2 validation: `python scripts/test-token-cost-measurement.py` passed 10 tests; `test -f benchmarks/token-cost/manifest.yaml` passed; `find benchmarks/token-cost -maxdepth 4 -type f | sort` listed the manifest, seven prompt files, and top-level fixture files; `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` passed; `rg -n "dist/adapters|\\.codex/skills|\\.agents/skills" benchmarks/token-cost` returned no matches.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- Code-review R4 validation rerun: `python scripts/test-token-cost-measurement.py` passed 10 tests; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- M3 test-first proof: `python scripts/test-token-cost-measurement.py` failed before implementation with missing analyzer summary output support and missing `scripts/run-token-cost-benchmarks.py`.
- M3 validation: `python scripts/test-token-cost-measurement.py` passed 17 tests; `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py` passed; `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl` passed; `python scripts/test-token-cost-report-validation.py` passed 10 tests; `git diff --check -- scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py scripts/test-token-cost-measurement.py tests/fixtures/token-cost` passed.
- Code-review R5 recording validation: `python scripts/validate-review-artifacts.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, and `git diff --check -- docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r5.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- Code-review R5 resolution validation: `python scripts/test-token-cost-measurement.py` passed 22 tests; `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py` passed; `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl` passed; `python scripts/test-token-cost-report-validation.py` passed 10 tests; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills` passed; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` passed; `git diff --check -- scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py scripts/test-token-cost-measurement.py tests/fixtures/token-cost docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r5.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- Code-review R6 validation rerun: `python scripts/test-token-cost-measurement.py` passed 22 tests; `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py` passed; `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl` passed; `python scripts/test-token-cost-report-validation.py` passed 10 tests; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills` passed after review recording with 11 reviews, 16 findings, 11 log entries, and 16 resolution entries; `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` passed; `git diff --check -- docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md docs/plan.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/reviews/code-review-r6.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- M4 test-first proof: `python scripts/test-token-cost-measurement.py` failed after adding the expected `--skip-git-repo-check` runner command assertion and before the runner command was updated.
- M4 validation: `python scripts/measure-skill-tokens.py` passed and reported 23 skills with 54,294 estimated tokens; `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex` passed after the runner command fix; `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml` passed; `python scripts/test-token-cost-measurement.py` passed 22 tests; `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py` passed; `python scripts/test-token-cost-report-validation.py` passed 10 tests; `git diff --check -- docs/reports/token-cost docs/releases/v0.1.1/release-notes.md scripts/run-token-cost-benchmarks.py scripts/test-token-cost-measurement.py` passed.
- M4 lifecycle validation: `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/release-token-friendliness-benchmark-for-skills.md --path specs/release-token-friendliness-benchmark-for-skills.test.md --path docs/plans/2026-05-11-release-token-friendliness-benchmark-for-skills.md --path docs/plan.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-log.md --path docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/review-resolution.md --path docs/reports/token-cost/releases/v0.1.1.md --path docs/reports/token-cost/releases/v0.1.1.yaml --path docs/releases/v0.1.1/release-notes.md` passed with the existing `docs/plan.md` lifecycle-language warning.
- RTF-CR7 test-first proof: `python scripts/test-token-cost-measurement.py` failed before the analyzer fix because current Codex `item.completed` / `command_execution` / `aggregated_output` events reported `tool_calls: 0` and `unknown_records: 1`.
- RTF-CR7 resolution validation: `python scripts/test-token-cost-measurement.py` passed 23 tests; `python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex` passed and regenerated seven run summaries; raw JSONL was omitted after sanitized analyzer summaries were regenerated; additional M4 validation is recorded in the change metadata.
- RTF-CR7 final validation: `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`, `python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py`, `python scripts/test-token-cost-report-validation.py`, `python scripts/analyze-codex-jsonl.py tests/fixtures/token-cost/sample-codex-session.jsonl`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and scoped `git diff --check -- ...` passed. Artifact lifecycle validation passed with the existing `docs/plan.md` lifecycle-language warning.
- M5 test-first proof: `python scripts/test-adapter-distribution.py` failed before implementation because `validate_release_output` did not accept token-cost report validation parameters, governed `v0.1.1` did not block missing token-cost metadata, and `release-verify.sh v0.1.1` did not invoke `scripts/validate-token-cost-report.py`.
- M5 validation: `python scripts/test-adapter-distribution.py` passed 58 tests; `bash scripts/release-verify.sh v0.1.1` passed; `python scripts/validate-release.py --version v0.1.1` passed; `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.0` passed; `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`, `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py scripts/adapter_distribution.py`, and `python scripts/test-token-cost-report-validation.py` passed.
- RTF-CR8 focused proof: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_1_1_release_validation_blocks_invalid_token_cost_report` passed.
- RTF-CR8 resolution validation: `python scripts/test-adapter-distribution.py` passed 59 tests; `python scripts/test-token-cost-report-validation.py`, `python scripts/validate-release.py --version v0.1.1`, `python -m py_compile scripts/validate-release.py scripts/validate-token-cost-report.py scripts/adapter_distribution.py`, `bash scripts/release-verify.sh v0.1.1`, `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, and `git diff --check --` passed. Artifact lifecycle validation passed with the existing `docs/plan.md` and `docs/workflows.md` lifecycle-language warnings.
- Code-review R10 validation rerun: `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_1_1_release_validation_blocks_invalid_token_cost_report`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills`, `python scripts/validate-change-metadata.py docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`, and `git diff --check --` passed.

## Outcome and Retrospective

- To be completed after implementation, review, explain-change, verify, and PR handoff.

## Readiness

- See `Current Handoff Summary`.

## Risks and Follow-ups

- Future hard token gates require a later proposal/spec after comparable report history exists.
- Claude Code and opencode dynamic benchmarks remain optional until stable comparable runners exist.
