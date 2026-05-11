# Release Token-Friendliness Benchmark for Skills

## Status

accepted

## Problem

RigorLoop publishes skills for use in other projects. A skill is not only a text file; it affects what files an agent reads, how much context it loads, whether it uses broad searches, whether command output is noisy, whether it scans generated artifacts unnecessarily, and whether its final handoff stays concise.

The repository now has static skill-size measurement and an initial token-cost baseline, but static size alone does not answer the main user-facing release question:

```text
How token-friendly are RigorLoop skills during real agent use?
```

Without a release benchmark, skill-token regressions can ship unnoticed, public skills can become more verbose over time, runtime context cost can grow even when static skill files look acceptable, contributors cannot compare releases, and optimization decisions rely too much on intuition.

## Goals

- Require every public release to include a Token-Friendliness benchmark report.
- Record benchmark results in a durable release report.
- Compare each release against the previous public release report or establish the first baseline when no prior report exists.
- Measure static skill size and dynamic runtime cost.
- Include command-output amplification and public skill portability checks.
- Identify the largest cost drivers before further skill optimization.
- Keep the first release benchmark lightweight and repeatable.
- Use report-required release gating first, with warning-only token thresholds until enough baseline history exists.
- Make the report useful to RigorLoop maintainers and downstream users.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Require every public release to run a Token-Friendliness benchmark. | in scope | Goals; Recommended direction; Release benchmark rule |
| Record benchmark results in a durable report. | in scope | Goals; Required release report |
| Compare each release against a previous release or baseline. | in scope | Goals; Versioning and comparison |
| Measure static skill size. | in scope | Measurement model; Acceptance criteria |
| Measure dynamic runtime token usage. | in scope | Measurement model; Benchmark suite |
| Measure command-output amplification. | in scope | Measurement model; Command-output amplification |
| Include public skill portability checks. | in scope | Required release report; Release gate semantics |
| Identify largest cost drivers. | in scope | Required release report; Top cost drivers |
| Keep first benchmark lightweight and repeatable. | in scope | Benchmark suite; Rollout |
| Avoid hard token-cost release blockers until history exists. | in scope | Release gate semantics; Decision log |
| Do not add hosted telemetry infrastructure. | out of scope | Non-goals |
| Do not require contributors to install every supported agent tool locally. | out of scope | Non-goals; Risks and mitigations |
| Do not hand-edit generated adapter output to reduce measured size. | out of scope | Non-goals |
| Define future hard total-token regression thresholds. | deferred follow-up | Release gate semantics |
| Add Claude Code or opencode dynamic measurements. | deferred follow-up | Risks and mitigations; Release gate semantics |
| Validate both Markdown and structured release metadata. | in scope | Required release report; Release gate semantics |
| Store benchmark prompts as executable fixtures. | in scope | Benchmark suite; Architecture impact |
| Allow Codex-unavailable handling without silently skipping final-release evidence. | in scope | Release gate semantics; Rollout and rollback |
| Define RC-to-final benchmark-relevant changes. | in scope | Versioning and comparison |
| Define exact YAML metadata shape. | in scope | Required release report |
| Keep first slice manual instead of adding a report generator. | in scope | Required release report; Rollout and rollback |
| Use a minimal downstream-user fixture rather than the RigorLoop repo. | in scope | Benchmark suite |
| Define waiver approval authority. | in scope | Release gate semantics |
| Use compound analyzer signals for unbounded full-file reads. | in scope | Measurement model; Release gate semantics |
| Decide schema validation ownership. | in scope | Architecture impact; Testing and verification strategy |
| Define the first seven benchmark prompts. | in scope | Benchmark suite |
| Decide fixture skill installation model. | in scope | Benchmark suite |
| Define the later report-generator trigger. | in scope | Required release report; Rollout and rollback |
| Decide the public Codex skill output path. | in scope | Benchmark suite |
| Decide YAML parser strategy. | in scope | Testing and verification strategy |
| Decide whether the first implementation includes a benchmark runner. | in scope | Benchmark suite; Rollout and rollback |
| Define temporary directory policy. | in scope | Benchmark suite |
| Decide whether the runner invokes the analyzer automatically. | in scope | Benchmark suite; Testing and verification strategy |
| Require runner invocation metadata for release validation. | in scope | Required release report; Release gate semantics |

## Non-goals

- Do not make token score the only release-quality measure.
- Do not remove safety-critical skill guidance solely to reduce tokens.
- Do not add hosted telemetry infrastructure in the first slice.
- Do not require contributors to install every supported agent tool locally.
- Do not make one-off benchmark variance block release.
- Do not hand-edit generated adapter output to reduce measured size.
- Do not optimize every skill in the same change.
- Do not define hard token-regression release blockers before comparable release history exists.
- Do not make Claude Code or opencode dynamic benchmarks required before their runners and reports are stable.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to trustworthy AI-assisted delivery by making public skills measurable, reviewable, and easier to adopt without hidden context cost.

## Context

The accepted token-cost optimization work identified that token cost is not only static skill size. Agents can also spend large context budget through broad file reads, broad searches, generated-output scans, and verbose command output. The accepted measurement baseline and scope-preservation proposal added static skill measurement, Codex JSONL analysis, command-output amplification reporting, and a first baseline report under `docs/reports/token-cost/`.

A recent baseline report exists at `docs/reports/token-cost/2026-05-10-baseline.md`. It proves the measurement shape, but it is not yet a release-level obligation and does not define per-release report paths, benchmark prompts, release-note linkage, or release verification semantics.

RigorLoop has also moved toward public skill portability. Published skills should not expose repository-internal paths, generated adapter mechanics, selector path constraints, or local maintainer examples. Token-friendliness should therefore measure the public skill surface and runtime behavior, not only internal repo maintenance files.

This proposal does not rely on `docs/project-map.md`; no project map file is present in this checkout.

## Options considered

### Option 1: Track only static skill size

Advantages:

- easy to measure;
- deterministic;
- cheap to run in CI;
- useful for identifying oversized skill files.

Disadvantages:

- does not measure runtime behavior;
- misses broad searches and full-file reads;
- misses command-output amplification;
- can encourage unsafe deletion of useful guidance.

### Option 2: Track only dynamic Codex runtime cost

Advantages:

- closer to real agent cost;
- captures skill-caused behavior;
- exposes broad reads and verbose output.

Disadvantages:

- can vary between runs;
- depends on tool configuration;
- may be harder to reproduce;
- does not explain which skill text is statically oversized.

### Option 3: Track release Token-Friendliness using both static and dynamic measures

Advantages:

- captures both skill file size and runtime behavior;
- supports release-over-release comparison;
- helps identify the largest cost drivers;
- avoids over-optimizing only one dimension.

Disadvantages:

- more setup than static-only measurement;
- requires stable benchmark prompts;
- initial thresholds should stay warning-based until baseline history exists.

## Recommended direction

Choose Option 3.

Every public RigorLoop release should include a Token-Friendliness benchmark report. The report should measure:

1. static skill size;
2. public skill portability;
3. dynamic runtime token usage;
4. command-output amplification;
5. largest cost drivers;
6. comparison with the previous release.

The benchmark should be required as a release artifact, but token score thresholds should be warning-only until the repository has enough comparable release history to define stable gates.

## Token-Friendliness definition

Token-Friendliness measures whether RigorLoop skills are concise, portable, and efficient during agent use.

A token-friendly skill:

- has a bounded static size;
- gives clear triggers and output expectations;
- avoids internal repository leakage in public text;
- prefers summaries, IDs, headings, counts, and targeted excerpts;
- avoids broad full-file reads unless justified;
- avoids large command output by default;
- produces concise handoff results;
- does not duplicate workflow policy that belongs elsewhere.

## Expected behavior changes

- Public release preparation includes a token-friendliness report before release readiness is claimed.
- Release verification checks for the presence and interpretability of the report instead of only validating release metadata and adapter packaging.
- Maintainers compare static skill size and dynamic benchmark cost against the previous release or establish a first release baseline.
- Release notes link to the token-friendliness report.
- Token-cost regressions create warning evidence and required explanation, but not hard release blockers in the first implementation slice.
- Public skill portability becomes part of release token-friendliness evidence, not only a skill-contract concern.

## Measurement model

### Static skill measurement

Use the existing static skill measurement approach.

Measure:

- skill file path;
- line count;
- character count;
- estimated tokens;
- largest section;
- public/internal path references;
- result block presence;
- claim-boundary presence.

Recommended command:

```bash
python scripts/measure-skill-tokens.py
```

### Dynamic runtime measurement

Use a repeatable benchmark set.

Measure:

- input tokens;
- cached input tokens;
- output tokens;
- reasoning output tokens;
- tool calls;
- command-output lines;
- estimated command-output tokens;
- full-file reads;
- broad searches;
- repeated file reads;
- largest cost driver.

Unbounded full-file read detection should use compound signals instead of one brittle heuristic. Strong signals include whole-file commands such as `cat`, large leading ranges such as `sed -n '1,620p'`, output that approximates the known file length, very large single-file output, repeated reads of the same file, and generated or adapter output reads when generated output is not the review target.

The analyzer should avoid false positives when a file is short, the whole file is explicitly the review target, the output is a small excerpt, or the event is only a path list. Reports should classify full-file reads as `none`, `suspected`, `confirmed`, or `justified`, with the signals and justification recorded.

Recommended command pattern:

```bash
codex exec --json --ephemeral \
  "<benchmark prompt>" \
  > docs/reports/token-cost/runs/<release>/<benchmark-id>.jsonl
```

Analyze with:

```bash
python scripts/analyze-codex-jsonl.py \
  docs/reports/token-cost/runs/<release>/<benchmark-id>.jsonl
```

### Command-output amplification

The dynamic analyzer should report command output size from Codex JSONL exports first.

A separate live wrapper such as `scripts/measure-command-output.py` may be added later if local command-output budgeting becomes useful.

## Required release report

Every public release should produce both human-readable Markdown and structured metadata:

```text
docs/reports/token-cost/releases/<release-version>.md
docs/reports/token-cost/releases/<release-version>.yaml
```

Example:

```text
docs/reports/token-cost/releases/v0.1.1.md
docs/reports/token-cost/releases/v0.1.1.yaml
```

Markdown is for reviewers. Structured metadata is for release validation. Release validation should not depend on parsing prose alone.

Use `schema_version: 1` for the first structured metadata format. Recommended schema:

```yaml
schema_version: 1

report:
  release: "v0.1.1"
  report_date: "2026-05-10"
  repository: "xiongxianfei/rigorloop"
  commit: "<git-sha>"
  report_markdown: "docs/reports/token-cost/releases/v0.1.1.md"

benchmark_suite:
  id: "skill-token-runtime-v1"
  manifest: "benchmarks/token-cost/manifest.yaml"
  prompt_count: 7
  fixture: "benchmarks/token-cost/fixtures/minimal-public-project"
  runs_per_prompt: 3

environment:
  primary_tool: "codex"
  codex_available: true
  codex_version: "<codex-version-or-unknown>"
  model: "<model-or-unknown>"
  os: "<os-or-unknown>"
  runner: "maintainer-local | ci | release-runner | unknown"

runner:
  command: "python scripts/run-token-cost-benchmarks.py --release v0.1.1 --suite benchmarks/token-cost/manifest.yaml --tool codex"
  tool: "codex"
  suite: "benchmarks/token-cost/manifest.yaml"
  fixture: "benchmarks/token-cost/fixtures/minimal-public-project"
  skill_source: "dist/adapters/codex/.agents/skills/"
  output_dir: "docs/reports/token-cost/runs/v0.1.1/"
  temp_policy: "system-temp"
  install_public_skills: true

static_skill_size:
  status: "pass" # pass | warning | blocked | not-run
  command: "python scripts/measure-skill-tokens.py"
  skills_measured: 23
  total_estimated_tokens: 54294
  max_skill:
    path: "skills/<skill>/SKILL.md"
    estimated_tokens: 0
  warnings:
    - skill: "skills/<skill>/SKILL.md"
      code: "skill-token-warning"
      message: "<message>"

dynamic_runtime:
  status: "pass" # pass | warning | blocked | not-run | waived
  tool: "codex"
  command_pattern: "codex exec --json --ephemeral ..."
  runs:
    - id: "proposal-short"
      prompt: "benchmarks/token-cost/prompts/proposal-short.md"
      fixture: "benchmarks/token-cost/fixtures/minimal-public-project"
      result: "pass" # pass | fail | blocked | not-run
      evidence:
        raw_jsonl_tracked: true
        jsonl: "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.jsonl"
        analysis: "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.analysis.yaml"
        sanitized_summary: ""
        raw_omission_reason: ""
      usage:
        input_tokens: 57035
        cached_input_tokens: 48768
        output_tokens: 928
        reasoning_output_tokens: 438
      tool_output:
        total_estimated_tokens: 1702
        largest_event:
          kind: "file-read | shell-output | unknown"
          command: "<command-or-event-name>"
          path: "<path-or-null>"
          lines: 138
          estimated_tokens: 1702
      signals:
        full_file_read_count: 0
        broad_search_count: 0
        generated_output_read_count: 0
        repeated_file_read_count: 0
      full_file_read:
        result: "none" # none | suspected | confirmed | justified
        signals: []
        justification: ""

optional_dynamic:
  claude_code:
    status: "not-run"
    reason: "optional in v1"
  opencode:
    status: "not-run"
    reason: "optional in v1"

summary:
  median_input_tokens: 0
  median_cached_input_tokens: 0
  median_output_tokens: 0
  median_reasoning_output_tokens: 0
  max_single_tool_output_estimated_tokens: 0
  full_file_read_count: 0
  broad_search_count: 0
  generated_output_read_count: 0

portability:
  status: "pass" # pass | warning | fail | not-run
  public_skill_internal_path_leaks: 0
  generated_output_internals_in_public_skills: 0
  local_examples_in_public_skills: 0
  notes: []

comparison:
  previous_release: "v0.1.0"
  previous_report: "docs/reports/token-cost/releases/v0.1.0.yaml"
  comparable: true
  deltas:
    static_total_estimated_tokens: 0
    median_input_tokens: 0
    median_output_tokens: 0
    max_single_tool_output_estimated_tokens: 0

rc_reuse:
  reused_from: ""
  benchmark_relevant_changes_since_rc: false
  checked_by: ""
  checked_surface: ""
  rationale: ""

waiver:
  required: false
  status: "none" # none | requested | approved | rejected
  reason: ""
  approved_by: ""
  approval_surface: ""
  evidence: ""

release_gate:
  result: "pass" # pass | warning | blocked | waived
  blockers: []
  warnings: []
  notes:
    - "Token thresholds are warning-only for this release unless portability or report structure fails."
```

The release gate should require these fields:

```text
schema_version
report.release
report.report_date
report.commit
report.report_markdown
benchmark_suite.id
benchmark_suite.manifest
runner.command
runner.suite
runner.fixture
runner.skill_source
runner.output_dir
static_skill_size.status
dynamic_runtime.status
summary
portability.status
release_gate.result
```

If `dynamic_runtime.status` is `waived`, release validation should require `waiver.status: approved`, `waiver.reason`, `waiver.approved_by`, `waiver.approval_surface`, and `waiver.evidence`.

Release validation should also verify that runner metadata agrees with benchmark metadata and run evidence: `runner.suite` should match `benchmark_suite.manifest`, `runner.fixture` should match `benchmark_suite.fixture`, `runner.skill_source` should be the public Codex adapter path, `runner.output_dir` should contain the listed run evidence, and each run should include raw JSONL or analyzer and sanitized summary evidence. Missing raw JSONL is valid only when `raw_jsonl_tracked: false`, `raw_omission_reason` is present, and `analysis` or `sanitized_summary` points to tracked sanitized evidence.

The Markdown report should link the metadata:

```md
# Token-Friendliness Report: v0.1.1

Structured metadata: `v0.1.1.yaml`
```

Raw JSONL benchmark runs, when tracked, should live under:

```text
docs/reports/token-cost/runs/<release-version>/
```

If raw JSONL is too large or contains sensitive local data, the report should record the sanitized summary and note that raw data was not tracked. The metadata should make this explicit through each run's `evidence` block rather than leaving a missing JSONL path ambiguous.

The first implementation should not add a full report generator. Maintainers should write the Markdown report manually, populate structured YAML metadata from existing analyzer outputs, and let release validation read the YAML. A generator can be proposed later after repeated manual-report errors or after three comparable stable reports, whichever comes first.

## Report template

```md
# Token-Friendliness Report: <release-version>

## Summary

- Release:
- Date:
- Commit:
- Benchmark suite:
- Static skill total:
- Dynamic benchmark count:
- Median input tokens:
- Median output tokens:
- Median reasoning output tokens:
- Largest cost driver:
- Overall token-friendliness status:

## Static skill size

| Skill | Estimated tokens | Status | Notes |
|---|---:|---|---|

## Dynamic runtime benchmark

| Benchmark | Input tokens | Cached input | Output tokens | Reasoning output | Largest output source | Result |
|---|---:|---:|---:|---:|---|---|

## Command-output amplification

| Benchmark | Largest command/output | Lines | Estimated tokens | Notes |
|---|---|---:|---:|---|

## Public skill portability

| Check | Result | Notes |
|---|---|---|
| Internal path leakage | pass/fail | |
| Generated-output internals in public skills | pass/fail | |
| Local RigorLoop examples in public skills | pass/fail | |

## Comparison with previous release

| Metric | Previous | Current | Change |
|---|---:|---:|---:|
| Static skill total | | | |
| Median input tokens | | | |
| Median output tokens | | | |
| Largest command-output tokens | | | |

## Top cost drivers

| Rank | Cost driver | Evidence | Suggested action |
|---:|---|---|---|

## Release decision

- Benchmark report present: yes/no
- Token regression requiring explanation: yes/no
- Release blocker: yes/no
- Notes:
```

## Benchmark suite

The first release benchmark suite should be small.

Benchmark prompts should live in executable fixtures rather than only in docs prose:

```text
benchmarks/token-cost/
  manifest.yaml
  fixtures/
    minimal-public-project/
  prompts/
    proposal-short.md
    workflow-route.md
    implement-handoff.md
    code-review-small.md
    verify-final-pack.md
    architecture-no-impact.md
    learn-no-durable-lesson.md
```

The manifest should define the suite, prompt files, expected tool, fixture, expected result, and tags:

```yaml
suite: skill-token-runtime-v1
benchmarks:
  - id: proposal-short
    prompt: prompts/proposal-short.md
    tool: codex
    fixture: fixtures/minimal-public-project
    expected_skill: proposal
    expected_result: pass
    tags:
      - proposal
      - public-skill
      - short-output
```

The first runtime fixture should be a minimal downstream public project, not the RigorLoop repository. Recommended fixture path:

```text
benchmarks/token-cost/fixtures/minimal-public-project/
```

Recommended contents:

```text
benchmarks/token-cost/fixtures/minimal-public-project/
  AGENTS.md
  VISION.md
  README.md
  docs/
    workflows.md
    changes/
      .gitkeep
  src/
    example.txt
```

If the first slice needs Codex-specific skill installation, it may add `.codex/skills/` under a `minimal-codex-project` fixture later. The first fixture should stay small enough that broad reads are obvious, real enough that public skills can operate, and free of RigorLoop repository internals.

The fixture should stay clean. The benchmark runner should create a temporary copy and install or copy the current public Codex skill output into that temp fixture before execution. This keeps the fixture from drifting away from the public release surface.

For the Codex runtime benchmark, the runner should copy public Codex adapter skills from:

```text
dist/adapters/codex/.agents/skills/
```

into the temporary fixture at:

```text
<tmp-fixture>/.agents/skills/
```

The runner should not use repository-local `.codex/skills/` as the public benchmark source. The benchmark should measure the public release surface, not the repository-local generated mirror.

The first implementation should include a small benchmark runner script:

```text
scripts/run-token-cost-benchmarks.py
```

The runner should read `benchmarks/token-cost/manifest.yaml`, create a temporary fixture copy, install public Codex skills from `dist/adapters/codex/.agents/skills/`, run each prompt with `codex exec --json --ephemeral`, and write JSONL runs under `docs/reports/token-cost/runs/<release-version>/`. It should not generate the final Markdown report in the first slice.

The runner should never run benchmarks directly inside the source fixture or mutate the repository fixture. It should copy the configured fixture into a fresh isolated temporary run directory outside the repository working tree, install public skills there, and run `codex exec` from the copied fixture.

For local runs, the default temp root should be the system temp directory, such as `$TMPDIR` with `/tmp` as fallback. For CI runs, the default temp root should be `$RUNNER_TEMP` when available, with the system temp directory as fallback. The runner should support `--temp-root`, `--keep-temp`, `--keep-failed-temp`, and `--output-dir`.

The runner should delete the temp directory after successful completion unless `--keep-temp` is set. On failure, it may preserve the temp directory only when `--keep-failed-temp` or equivalent debug mode is set. Release metadata should record the fixture source, public skill source, output directory, and temp policy, but should not rely on unstable local temp paths as release evidence.

The runner should call `scripts/analyze-codex-jsonl.py` automatically for each JSONL run, save the analyzer summary next to the JSONL output, and print the equivalent analyzer commands for debugging. Automatic analysis is part of repeatable benchmark execution, while Markdown report generation remains deferred.

The per-run analyzer summary should use a minimal stable schema:

```yaml
schema_version: 1
run:
  id: "proposal-short"
  jsonl: "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.jsonl"
usage:
  input_tokens: 57035
  cached_input_tokens: 48768
  output_tokens: 928
  reasoning_output_tokens: 438
tool_output:
  total_estimated_tokens: 0
  largest_event:
    kind: "file-read | shell-output | none"
    command: ""
    path: ""
    lines: 0
    estimated_tokens: 0
signals:
  full_file_read_count: 0
  broad_search_count: 0
  generated_output_read_count: 0
  repeated_file_read_count: 0
verdict:
  result: "pass | warning | blocked"
  warnings: []
  blockers: []
```

The release YAML should reference analyzer summaries instead of relying on duplicated analyzer detail inside the release metadata.

Recommended initial benchmarks:

```text
proposal-short
workflow-route
implement-handoff
code-review-small
verify-final-pack
architecture-no-impact
learn-no-durable-lesson
```

First prompt definitions:

```text
workflow-route:
Use the workflow skill to decide the next step for this project change.
Situation:
- The user has an accepted proposal and wants to know what to do next.
- Do not edit files.
- Output only the recommended next skill and a one-paragraph rationale.

proposal-short:
Use the proposal skill to draft a short proposal for adding a small user-facing feature.
Do not edit files.
Output only:
- proposed proposal path
- proposal title
- one-paragraph summary
- next recommended stage

implement-handoff:
Use the implement skill to inspect the current milestone handoff state.
Do not edit files.
Do not write code.
Output only:
- current milestone
- whether implementation may start
- what evidence is missing, if any
- next recommended action

code-review-small:
Use the code-review skill to review the small changed file in this fixture.
Do not edit files.
Output only:
- review status
- findings, if any
- next stage

verify-final-pack:
Use the verify skill to check whether this fixture has enough final evidence for PR handoff.
Do not edit files.
Output only:
- verification status
- missing evidence, if any
- next stage

architecture-no-impact:
Use the architecture skill to decide whether this small documentation-only change needs architecture work.
Do not edit files.
Output only:
- architecture surface
- rationale
- next stage

learn-no-durable-lesson:
Use the learn skill to decide whether this single non-repeated observation should produce a durable learn session.
Do not edit files.
Output only:
- whether learn should run
- whether a follow-up or no-learn rationale is needed
- where the rationale should be recorded
```

Each benchmark should have:

- stable prompt;
- expected skill;
- expected output shape;
- no requirement to edit files unless the benchmark is specifically testing edits.

Example:

```text
Use the proposal skill to draft a short proposal. Do not edit files. Output only the path and summary.
```

## Release benchmark rule

Before every public release, maintainers should:

1. run static skill measurement;
2. run the dynamic benchmark suite;
3. analyze JSONL outputs;
4. generate the release Token-Friendliness report;
5. compare with the previous release;
6. record any regression explanation;
7. include the report link in release notes.

## Release gate semantics

The first implementation should use a report-required gate, not a score-required gate.

Release verification should block when:

- the Token-Friendliness report is missing;
- structured metadata is missing or unparsable;
- the dynamic benchmark suite was not run and no valid waiver exists;
- the report omits static skill measurement;
- the report omits dynamic runtime measurement and no valid waiver exists;
- raw or summarized results cannot be interpreted;
- runner metadata, benchmark suite metadata, and JSONL run evidence disagree;
- public skill portability checks fail.

Release verification should warn when:

- static skill total increases significantly;
- median dynamic input tokens increase significantly;
- command-output amplification increases significantly;
- a benchmark introduces new full-file reads;
- a public skill exceeds warning thresholds.

For early adoption and RC preparation, dynamic benchmarks may be recorded as `blocked` or `not-run` only with a reason, owner, environment, follow-up, and explicit statement about whether release may proceed.

For a final public release, the Codex dynamic benchmark status should be one of:

- `pass`
- `waived`

A valid `waived` result should name the approving maintainer, reason, approval surface, evidence, and either a statement that no benchmark-relevant change occurred since the last passing run or another approved waiver reason.

A final-release dynamic benchmark waiver is valid only when approved by the release owner or maintainer-of-record and recorded in the structured release token-friendliness metadata. Valid waiver reasons include Codex unavailability with no benchmark-relevant changes since a passing RC run, emergency security or critical fix release with maintainer-approved deferral, or benchmark tooling failure with tracked follow-up and passing static and portability checks. Forgetting to run the benchmark, lack of time, inconvenience, or an unexplained dynamic regression should not be accepted as waiver reasons.

Claude Code and opencode dynamic benchmarks should be optional first. They should become required only after each tool has a stable noninteractive benchmark path, parseable output, consistent prompts, maintainer-operable runners, and comparable reports across releases.

After at least three comparable release reports, the repository may define hard regression thresholds.

The first hard gates after three comparable reports should focus on structural reliability:

- missing report or metadata;
- unparsable metadata;
- missing benchmark suite declaration;
- missing static measurement;
- missing dynamic measurement or waiver;
- public skill portability failure;
- a single command or output exceeding 20,000 estimated tokens without recorded justification;
- an unbounded full-file read without recorded justification;
- a dynamic benchmark omitted for a benchmark-relevant release change without waiver.

Unbounded full-file read gating should use compound evidence, such as whole-file commands, large leading ranges, output that approximates the file length, high-volume single-file output, repeated file reads, and generated-output reads. A single weak signal should not block a release by itself.

Static total token growth, median input-token growth, individual skill growth, cached-input variation, and reasoning-output variation should remain warnings initially. After five or six comparable reports, the repository may consider hard gates for large unexplained static or dynamic regressions with a maintainer override path.

## Suggested warning thresholds

Initial warning thresholds:

```text
Static public skill:
- warning over 4,000 estimated tokens
- high-warning over 5,000 estimated tokens

Dynamic short benchmark:
- warning over 75,000 input tokens
- high warning over 100,000 input tokens

Command-output amplification:
- warning when one command/output exceeds 8,000 estimated tokens
- high warning when one command/output exceeds 20,000 estimated tokens

Broad search:
- warning when output exceeds 80 lines
```

`warning` and `high-warning` severities are not hard release blockers in the first slice. `blocker` applies only to missing or unparsable reports, missing required evidence without waiver, public portability failure, uninterpretable results, or inconsistent release metadata.

## Versioning and comparison

Each report compares against the most recent prior public release report. If no prior report exists, the first report becomes the baseline.

For pre-release candidates, a version such as:

```text
v0.1.1-rc.1
```

may create an RC report.

The final release report should either:

- reuse the RC report if no skill or benchmark-relevant change occurred; or
- rerun the benchmark and create a final report.

A change is benchmark-relevant when it can change skill loading, public skill text, adapter output, workflow guidance, benchmark prompts, analyzer scripts, portability checks, workflow order, handoff behavior, skill descriptions or frontmatter, result format, evidence-reading guidance, tool-output guidance, benchmark fixture behavior, Codex version, model, or release packaging of adapter output.

Unrelated product docs, internal-only plan changes, review-resolution text, change-local artifacts, typo fixes outside public skills or guides, and historical report edits are not usually benchmark-relevant.

When a final release reuses an RC report, structured metadata should record the reuse:

```yaml
rc_reuse:
  reused_from: "v0.1.1-rc.1"
  benchmark_relevant_changes_since_rc: false
  checked_by: "release-owner"
  checked_surface: "release checklist or PR review"
  rationale: "No public skill, adapter, workflow guide, benchmark prompt, analyzer, fixture, model, or release packaging changes since RC."
```

If `benchmark_relevant_changes_since_rc: true`, the final release should rerun the affected benchmarks, rerun the full suite, or record a valid waiver.

## Architecture impact

This is a release process and measurement artifact change. No runtime architecture or workflow stage order change is expected.

Affected surfaces may include:

- release validation guidance;
- `benchmarks/token-cost/`;
- `docs/reports/token-cost/`;
- `scripts/analyze-codex-jsonl.py`;
- `scripts/measure-skill-tokens.py`;
- `scripts/run-token-cost-benchmarks.py`;
- `scripts/validate-token-cost-report.py`;
- release checklist or `docs/workflows.md`;
- `scripts/validate-release.py`;
- `scripts/release-verify.sh`;
- release notes;
- public skill portability checks.

No C4, arc42, persistence, API, deployment infrastructure, or runtime data-flow architecture update is expected unless specification discovers a durable boundary decision.

Schema validation should have clear ownership. A token-cost-specific validator should own token-cost YAML schema validation, required fields, enums, report links, run references, and waiver fields. `scripts/validate-release.py` should own release readiness and delegate to the token-cost validator when the release policy requires a Token-Friendliness report.

The first token-cost validator should use the repository's existing lightweight parser conventions when they can safely parse the `schema_version: 1` metadata shape. If the required metadata shape cannot be parsed safely with existing conventions, implementation may add a small dedicated YAML parser dependency, but the plan should record the reason and scope.

## Testing and verification strategy

Likely validation:

```bash
python scripts/measure-skill-tokens.py
python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release <release-version> --tool codex
python scripts/analyze-codex-jsonl.py <sample-jsonl>
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/<release-version>.yaml
python scripts/validate-release.py --version <release-version>
git diff --check --
```

For release validation:

```bash
python scripts/measure-skill-tokens.py > <static-output>
python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release <release-version> --tool codex
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/<release-version>.yaml
```

If the release changes canonical skills:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

If the implementation adds or changes scripts:

```bash
python -m py_compile scripts/measure-skill-tokens.py scripts/analyze-codex-jsonl.py scripts/run-token-cost-benchmarks.py scripts/validate-token-cost-report.py
```

The later spec should map these checks to concrete requirement IDs and keep the token-cost schema logic reusable for draft report validation, release validation, CI validation, and any future report generator.

## Rollout and rollback

Rollout:

1. Accept this proposal after proposal-review.
2. Add a focused release-process spec or update the existing release-validation contract.
3. Add release Token-Friendliness report template.
4. Add or update release validation guidance.
5. Add `benchmarks/token-cost/manifest.yaml`, prompt fixtures, and the minimal downstream public project fixture.
6. Add `scripts/run-token-cost-benchmarks.py` for repeatable benchmark execution.
7. Add `scripts/validate-token-cost-report.py` and delegate to it from `scripts/validate-release.py`.
8. Define the first structured YAML metadata schema and release validation checks.
9. Run the first release baseline benchmark.
10. Store the Markdown report and YAML metadata under `docs/reports/token-cost/releases/`.
11. Link the report from release notes.
12. Use the report to choose the next skill optimization slice.

The follow-on plan should split implementation into reviewable milestones:

```text
M1 - Metadata schema and validator
M2 - Benchmark fixture and prompt suite
M3 - Runner and analyzer-summary integration
M4 - First baseline report
M5 - Release validation integration
```

Rollback:

- keep existing reports as historical evidence;
- remove the report-required release gate;
- keep static skill measurement;
- continue to record token-cost observations manually until a better benchmark is defined.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Benchmark results vary between runs. | Use stable prompts and report medians when multiple runs are available. |
| Release is delayed by warning-only regressions. | Block only on missing report, uninterpretable results, or portability failures in the first slice. |
| Skills become too terse. | Preserve safety-critical guidance and claim boundaries. |
| Reports become too verbose. | Keep report summary-first and move raw JSONL to `runs/` or leave it untracked if too large. |
| Dynamic benchmark is Codex-specific. | Treat Codex as the first measured runtime; add Claude Code or opencode measurements later if tooling supports it. |
| Raw JSONL may contain local paths. | Sanitize raw data or track only summarized reports for release artifacts. |
| Release verification overfits Markdown prose. | Prefer structured release metadata or narrow report-shape checks when implementing the gate. |
| A report generator locks the format too early. | Use manual Markdown plus structured YAML in the first slice; propose a generator after the report shape stabilizes. |
| Full-file read detection creates false positives. | Use compound analyzer signals and allow `justified` classification when the whole file is the review target. |
| The runner benchmarks the wrong skill source. | Require copying from `dist/adapters/codex/.agents/skills/` into the temporary fixture and avoid `.codex/skills/` for release benchmarks. |
| YAML parsing grows too complex for lightweight conventions. | Start dependency-light, then add a scoped YAML parser dependency only when the schema cannot be parsed safely. |
| Temporary benchmark files pollute the repository. | Use isolated temp directories outside the repo, delete by default, and preserve only with explicit debug flags. |
| Maintainers forget to analyze a JSONL run. | Have the runner invoke `analyze-codex-jsonl.py` automatically and save per-run summaries next to JSONL outputs. |
| JSONL evidence cannot be reproduced. | Require runner command or normalized invocation metadata in the structured release report. |

## Open questions

None currently. Remaining implementation detail should be resolved in the follow-on spec or plan.

## Acceptance criteria

- A release Token-Friendliness report format exists.
- Structured release Token-Friendliness metadata exists.
- Release guidance requires a benchmark report for every public release.
- The first release with this policy creates a baseline report.
- Static skill measurement is included.
- Dynamic runtime benchmark measurement is included.
- Command-output amplification is included.
- Dynamic run evidence distinguishes tracked raw JSONL from sanitized-summary evidence.
- Analyzer summary files have a minimal stable schema.
- Public skill portability results are included.
- The report compares against a previous release when one exists.
- RC report reuse records release-owner or maintainer decision metadata.
- Release validation reads structured metadata, while reviewers read the Markdown report.
- Token-cost schema validation lives in a dedicated validator that release validation delegates to.
- Benchmark prompts are stored as fixture files with a manifest.
- The first benchmark suite includes seven stable prompts covering workflow, proposal, implement, code-review, verify, architecture, and learn.
- The first runtime fixture is a minimal downstream public project rather than the RigorLoop repository.
- The benchmark runner installs current public skills into a temporary copy of the clean fixture.
- The benchmark runner copies public Codex skills from `dist/adapters/codex/.agents/skills/` into `<tmp-fixture>/.agents/skills/`.
- The first implementation includes a small benchmark runner script for repeatable benchmark execution.
- The benchmark runner uses an isolated temporary run directory outside the repository and deletes it by default.
- The benchmark runner automatically invokes the JSONL analyzer and stores per-run summaries.
- Structured metadata records the runner command or normalized invocation.
- The token-cost validator uses lightweight parser conventions first and adds a parser dependency only if needed.
- Dynamic benchmark waivers require maintainer approval recorded in structured metadata.
- Unbounded full-file read detection uses compound analyzer signals.
- Warning labels distinguish `warning`, `high-warning`, and `blocker`.
- The follow-on plan slices implementation into reviewable milestones.
- Release verification blocks on a missing report or uninterpretable results, not on warning-only token regressions.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-10 | Propose a Token-Friendliness report for every public release. | Public skills are a release surface and should be measurable. |
| 2026-05-10 | Propose both static and dynamic measurement. | Static skill size alone does not capture runtime amplification. |
| 2026-05-10 | Propose reports under `docs/reports/token-cost/releases/`. | Maintainers need release-over-release comparison. |
| 2026-05-10 | Propose warning-only token thresholds initially. | Baseline history is needed before hard gates are safe. |
| 2026-05-10 | Use Markdown plus structured YAML metadata for release reports. | Reports are for humans; metadata is for gates. |
| 2026-05-10 | Store benchmark prompts under `benchmarks/token-cost/`. | Prompts are executable fixtures and should be deterministic. |
| 2026-05-10 | Require Codex first and keep Claude Code/opencode optional. | Existing measurement tooling is Codex-oriented; other tools need stable comparable runners first. |
| 2026-05-10 | Use manual Markdown plus YAML metadata in the first slice. | Existing analyzers are enough for validation, and a generator would lock the report format too early. |
| 2026-05-10 | Use a minimal downstream public project fixture. | The benchmark should measure downstream public skill behavior, not RigorLoop repository internals. |
| 2026-05-10 | Require maintainer approval for final-release dynamic benchmark waivers. | Final releases should not silently skip runtime evidence. |
| 2026-05-10 | Validate token-cost report metadata with a dedicated validator delegated from release validation. | Draft report validation, CI, release validation, and future generators should share one schema owner. |
| 2026-05-10 | Use seven fixture-backed prompts for the first suite. | The suite should cover common public skill behaviors while staying small and comparable. |
| 2026-05-10 | Keep fixture projects clean and install public skills into temporary run copies. | The fixture represents the user project; the runner installs the current release surface. |
| 2026-05-10 | Defer a report generator until repeated manual errors or three stable comparable reports. | Automation should wait until the manual report shape is stable or painful enough to justify it. |
| 2026-05-10 | Copy public Codex skills from `dist/adapters/codex/.agents/skills/`. | The release benchmark should measure public adapter output, not the repository-local Codex mirror. |
| 2026-05-10 | Use lightweight YAML parsing first. | Keep the first validator dependency-light unless the schema cannot be parsed safely. |
| 2026-05-10 | Include a small benchmark runner in the first implementation. | A release benchmark has enough moving parts that documented command patterns alone are too error-prone. |
| 2026-05-10 | Use isolated disposable temp directories for benchmark runs. | The clean fixture should not be mutated, and temp paths should not become release evidence. |
| 2026-05-10 | Have the runner invoke the JSONL analyzer automatically. | Repeatable release benchmarks should not depend on manual per-run analyzer commands. |
| 2026-05-10 | Require runner invocation metadata in release metadata. | JSONL proves what happened; runner metadata explains how to reproduce it. |
| 2026-05-11 | Make dynamic benchmark gate wording waiver-aware. | A valid final-release waiver means the suite may not have run for that final release. |
| 2026-05-11 | Add raw JSONL or sanitized-summary evidence metadata. | Release validation needs to distinguish omitted raw data from missing evidence. |
| 2026-05-11 | Define a minimal analyzer summary schema. | Runner-produced summaries need stable fields for release metadata and validation. |
| 2026-05-11 | Require RC reuse decision metadata. | Reusing an RC report requires an attributable release-owner or maintainer decision. |
| 2026-05-11 | Add follow-on plan milestone guidance. | The implementation touches enough surfaces to require reviewable slices. |
| 2026-05-11 | Rename hard warning severity to high-warning. | Warning labels should not sound like release blockers. |

## Next artifacts

- focused spec or release-process update
- benchmark prompt definitions
- release report template
- first release Token-Friendliness baseline report
- release validation update

## Follow-on artifacts

None yet.

## Readiness

Accepted after proposal-review.

This proposal defines the release-level benchmark obligation and report shape. It does not yet pick hard token-regression thresholds.

Core invariant:

```text
Every public release should prove not only that skills work,
but that they remain usable within a reasonable context budget.
```
