# Expand Dynamic Token-Friendliness Benchmarks for Core Skills

## Status

accepted

## Problem

RigorLoop now has a release Token-Friendliness benchmark that measures both static skill size and dynamic runtime cost.

The first dynamic benchmark proved that runtime measurement is valuable. Static size identified large public skills such as `workflow` and `code-review`, but dynamic runs also showed confirmed skill-file reads across the benchmark suite and a dynamic input-token warning for `verify-final-pack`.

The current benchmark suite is useful, but it does not yet cover enough of the standard delivery workflow to confidently measure the user-facing cost of RigorLoop's most important public skills.

If the benchmark remains too narrow:

- runtime regressions in unmeasured core skills can ship unnoticed;
- optimization may over-focus on already measured skills;
- release reports cannot show which parts of the workflow are covered;
- maintainers cannot compare token-friendliness across the full delivery path.

## Goals

- Expand the dynamic benchmark suite to cover the core standard workflow.
- Add dynamic coverage for high-value skills that users rely on during normal delivery.
- Keep the required release benchmark suite small enough to run consistently.
- Separate release-required core benchmarks from optional extended benchmarks.
- Add benchmark coverage metadata to release reports.
- Measure both token cost and result correctness.
- Use benchmark evidence to choose future optimization slices.
- Avoid making every skill benchmark release-blocking immediately.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Expand the dynamic benchmark suite to cover the core standard workflow. | in scope | Goals; Recommended direction; Release-required core suite |
| Add dynamic coverage for high-value normal-delivery skills. | in scope | Goals; Release-required core suite |
| Keep the release-required suite small and consistent. | in scope | Goals; Recommended direction; Risks and mitigations |
| Separate required core benchmarks from optional extended benchmarks. | in scope | Recommended direction; Optional extended suite |
| Add benchmark coverage metadata to release reports. | in scope | Benchmark coverage metadata; Acceptance criteria |
| Measure token cost and result correctness. | in scope | Measurement requirements; Result-quality status |
| Use evidence to choose future optimization slices. | in scope | Goals; Rollout and rollback |
| Avoid benchmarking every skill immediately. | out of scope | Non-goals; Options considered |
| Avoid hard token regression gates in this proposal. | out of scope | Non-goals; Release gate behavior |
| Avoid requiring Claude Code or opencode dynamic runs. | out of scope | Non-goals; Acceptance criteria |
| Keep safety-critical guidance even when optimizing tokens. | in scope | Non-goals; Risks and mitigations |
| Add core prompts for `plan`, `explain-change`, and `pr`. | in scope | Release-required core suite; Expansion phases |
| Keep optional coverage for review-heavy, authoring, support, and periodic skills. | in scope | Optional extended suite; Expansion phases |
| Keep `architecture-no-impact` and `learn-no-durable-lesson` required for one transition release. | in scope | Recommended direction; Transition carryover benchmarks |
| Record result quality through manual review first. | in scope | Result-quality status |
| Use `skill-token-runtime-v2` for the expanded suite. | in scope | Recommended direction; Versioning and comparison |
| Conditionally require optional benchmarks when their public skill changes. | in scope | Changed public skill benchmark policy |
| Put coverage metadata in YAML and Markdown. | in scope | Benchmark coverage metadata |
| Use `v0.1.1` or `v0.1.1-rc.1` for the first v2 transition report. | in scope | Versioning and comparison |
| Define the manual `result_quality` YAML shape. | in scope | Result-quality status |
| Trace generated adapter changes back to canonical skill ownership. | in scope | Changed public skill benchmark policy |
| Add `architecture-review` as the first optional extended benchmark after core expansion. | in scope | Optional extended suite |

## Non-goals

- Do not benchmark every RigorLoop skill in the first expansion.
- Do not make optional or periodic skills release-blocking yet.
- Do not add hard token regression gates in this proposal.
- Do not remove safety-critical guidance solely to reduce tokens.
- Do not replace static skill-size measurement.
- Do not require Claude Code or opencode dynamic benchmarks in this slice.
- Do not introduce a hosted telemetry system.
- Do not optimize skill text as part of this benchmark-coverage change.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to trustworthy AI-assisted software delivery by making public skill runtime cost visible, repeatable, and release-reviewable across more of the normal delivery path.

## Context

RigorLoop's accepted release Token-Friendliness benchmark now measures static skill size, dynamic runtime usage, command-output amplification, public skill portability, analyzer summaries, and release report metadata.

The first release baseline showed that:

- static size warnings identify large public skills;
- dynamic runs reveal whole-skill reads that static measurement cannot show;
- dynamic input token warnings can come from multiple context sources;
- command-output amplification is only one part of runtime cost;
- benchmark results should guide optimization rather than intuition.

The current suite in `benchmarks/token-cost/manifest.yaml` covers `workflow`, `proposal`, `implement`, `code-review`, `verify`, `architecture`, and `learn`. That suite is a useful baseline, but it omits `plan`, `explain-change`, and `pr`, which are central to normal delivery handoff and final review readiness.

As of 2026-05-11, `gh release list --limit 5` shows `v0.1.0` as the latest public GitHub release. Therefore the first expanded transition report should naturally target `v0.1.1`, or `v0.1.1-rc.1` if the project publishes an RC first.

The next step is to expand coverage to more of the standard workflow while keeping the release process practical and comparable.

This proposal does not rely on `docs/project-map.md`; no project map file is present in this checkout.

## Options considered

### Option 1: Benchmark every skill immediately

Advantages:

- broadest coverage;
- fewer blind spots;
- more complete evidence for optimization decisions.

Disadvantages:

- expensive to run;
- harder to stabilize;
- more noisy results;
- can slow releases;
- may overburden maintainers before thresholds are mature.

### Option 2: Keep the current small suite only

Advantages:

- simple;
- already working;
- easy to compare across releases.

Disadvantages:

- misses important workflow skills;
- under-measures user-facing runtime cost;
- may hide regressions in `plan`, `explain-change`, and `pr` handoff behavior.

### Option 3: Add a release-required core suite plus optional extended suite

Advantages:

- covers the normal workflow path;
- keeps release benchmarks manageable;
- makes coverage gaps explicit;
- supports gradual expansion;
- avoids making every skill a release blocker too early.

Disadvantages:

- requires benchmark coverage metadata;
- still leaves some skills optional until later;
- requires maintenance of more prompt fixtures;
- may change how currently required `architecture` and `learn` prompts are classified.

## Recommended direction

Choose Option 3.

RigorLoop should use a two-tier dynamic benchmark model:

```text
release-required core suite
+ optional extended suite
```

The release-required suite should cover the most important user-facing standard workflow path. The optional extended suite should cover review-heavy, authoring, periodic, and support skills that are important but should not block every release yet.

The expanded suite should use a new suite ID:

```text
skill-token-runtime-v2
```

The suite ID should change because the required benchmark coverage, manifest shape, coverage metadata, and result-quality evidence are changing. Existing `skill-token-runtime-v1` reports remain valid historical evidence. The first expanded report becomes the baseline for the v2 suite, with overlapping v1 prompts compared only as informational continuity.

The currently required `architecture-no-impact` and `learn-no-durable-lesson` prompts should remain required for one transition release as carryover baselines. After one comparable v2 transition report, they should move to optional extended coverage unless the corresponding public skills change in a benchmark-relevant way.

## Release-required core suite

The required release benchmark suite should cover:

```text
workflow
proposal
plan
implement
code-review
explain-change
verify
pr
```

These skills represent the core delivery path from routing and direction through implementation, review, explanation, final verification, and PR handoff.

Required core prompt fixtures should live under:

```text
benchmarks/token-cost/prompts/
```

Required core prompts:

```text
workflow-route.md
proposal-short.md
plan-handoff.md
implement-handoff.md
code-review-small.md
explain-change-summary.md
verify-final-pack.md
pr-handoff.md
```

## Optional extended suite

The optional extended suite should include:

```text
proposal-review
spec
spec-review
architecture
architecture-review
plan-review
test-spec
learn
research
explore
vision
project-map
```

After the core expansion, the first optional extended benchmark to add should be:

```text
architecture-review
```

`architecture-review` is the best next optional benchmark because it is review-heavy, safety-sensitive, interacts with proposal/spec/architecture boundaries, and likely carries complex guidance. The initial prompt should stay small:

```text
Use the architecture-review skill to review the fixture's architecture change.

Do not edit files.

Output only:
- review surface
- review status
- findings, if any
- required next action
```

The first fixture scenario should avoid a heavy architecture document and test the intended review behavior directly: a canonical architecture update exists, no change-local architecture delta exists, ADR is not required, and `architecture-review` should not demand a change-local delta.

Recommended fixture path:

```text
benchmarks/token-cost/fixtures/minimal-public-project-architecture-review/
```

Recommended fixture contents:

```text
AGENTS.md
VISION.md
README.md
docs/workflows.md
docs/architecture/system/architecture.md
docs/architecture/system/diagrams/context.mmd
docs/architecture/system/diagrams/container.mmd
docs/adr/README.md
docs/changes/2026-05-11-architecture-review-benchmark/change.yaml
docs/changes/2026-05-11-architecture-review-benchmark/explain-change.md
specs/example-feature.md
src/app.txt
```

The fixture should state that clear architecture changes update the canonical architecture package directly and that no ADR is required for the benchmark scenario. The change-local artifacts should link to the canonical architecture update but should not contain a separate change-local architecture delta.

The benchmark should fail manual quality review if output says a change-local architecture delta must be created before review can proceed.

Use a separate fixture directory for the first implementation. Do not add the architecture-review scenario directly to the generic `minimal-public-project` fixture yet. This keeps the base fixture small, avoids changing all existing benchmark prompts, and makes architecture-review cost attributable to the scenario. If several future fixtures duplicate the same base files, a later proposal can introduce shared base fixtures or overlays.

Trigger a shared base-fixture or overlay proposal when either condition happens:

- three or more scenario fixtures duplicate the same base files;
- duplicate fixture drift causes a review finding or implementation error.

Until then, fixture directories should remain self-contained. This keeps the first implementation reviewable and avoids adding overlay copy or merge rules before duplication is a proven maintenance risk.

If optional extended benchmark coverage expands quickly, count the first review-heavy scenario after `architecture-review` as the likely third duplicated scenario fixture. The preferred trigger candidate is:

```text
minimal-public-project-proposal-review
```

If that `proposal-review` fixture duplicates the same minimal public-project base files as `minimal-public-project` and `minimal-public-project-architecture-review`, create a follow-up proposal for shared base fixtures or scenario overlays.

Run the extended suite:

- before major releases;
- before large skill refactors;
- when touched skills are in the extended set;
- when a maintainer explicitly requests broader coverage.

Missing optional extended coverage should not block release unless the release claims coverage for that skill or the skill was changed in a benchmark-relevant way and the approved spec makes that case release-governed.

## Transition carryover benchmarks

The expanded suite should not drop existing v1 baseline prompts silently.

For the first v2 transition release, these prompts should remain required as carryover benchmarks:

```text
architecture-no-impact
learn-no-durable-lesson
```

After that transition release, they should move to optional extended coverage unless their corresponding public skills change.

Core rule:

```text
Do not remove baseline prompts silently.
Retire them through a named transition.
```

## Changed public skill benchmark policy

Optional extended benchmarks should become conditionally required when their corresponding public skill changes in the release and a benchmark exists for that skill.

Changed public skill detection should live in release validation. The token-cost validator should validate the metadata that release validation produces or requires.

Release validation should detect changed surfaces, decide which optional benchmarks become required, and pass that required benchmark list into token-cost validation context. The token-cost validator should then validate benchmark metadata schema, required benchmark entries, result-quality status, waivers, and coverage consistency.

Changed public skill detection should use canonical detection first and generated-output tracing second.

Release validation should pass a small structured required-benchmark context object or file to token-cost validation. Example:

```yaml
schema_version: 1
context_source: release-validation

release:
  version: v0.1.1
  stage: final
  commit: "<sha>"

benchmark_suite:
  id: skill-token-runtime-v2
  manifest: benchmarks/token-cost/manifest.yaml

required_benchmarks:
  core:
    - workflow-route
    - proposal-short
    - plan-handoff
    - implement-handoff
    - code-review-small
    - explain-change-summary
    - verify-final-pack
    - pr-handoff
  transition_carryover:
    - architecture-no-impact
    - learn-no-durable-lesson
  required_due_to_changes:
    - benchmark: architecture-review
      skill: architecture-review
      reason: public-skill-changed
      changed_surfaces:
        canonical:
          - skills/architecture-review/SKILL.md
        generated:
          - dist/adapters/codex/.agents/skills/architecture-review/SKILL.md
          - dist/adapters/claude/.claude/skills/architecture-review/SKILL.md
          - dist/adapters/opencode/.opencode/skills/architecture-review/SKILL.md

optional_benchmarks:
  extended:
    - proposal-review
    - spec
    - spec-review
    - architecture
    - architecture-review
    - plan-review
    - test-spec
    - learn
    - research
    - explore
    - vision
    - project-map

waiver_policy:
  final_release_requires_pass_or_waiver: true
  inconclusive_requires_waiver_for_required_benchmarks: true
  allowed_approver_roles:
    - release-owner
    - release-manager
    - repository-maintainer
```

The validator should support both transport forms: release validation may pass required benchmark context directly as an in-memory object, and standalone CLI or test flows may pass a temporary YAML file. Conceptual API:

```text
validate_token_cost_report(metadata, required_benchmark_context=None)
```

Conceptual CLI:

```bash
python scripts/validate-token-cost-report.py \
  docs/reports/token-cost/releases/v0.1.1.yaml \
  --required-benchmark-context /tmp/required-benchmarks.yaml
```

Core rule:

```text
One validation contract.
Two transport forms: object for code, YAML for humans and CLI.
```

The standalone CLI context YAML should be generated transiently by default. In CI, release validation can write it under `$RUNNER_TEMP/required-token-benchmarks.yaml`; locally it can use a system temp path such as `/tmp/rigorloop-required-token-benchmarks.yaml`.

Track the context YAML only when it becomes release decision evidence, such as when release validation behavior is disputed, a waiver depends on the exact required benchmark set, a generated `required_due_to_changes` list is surprising, a release gate failure needs debugging, or a release owner explicitly cites it. In that exceptional case, use a path such as:

```text
docs/reports/token-cost/releases/v0.1.1.required-benchmarks.yaml
```

Core rule:

```text
The release report is durable evidence.
The required benchmark context is validation input.
Track validation input only when it is part of the decision record.
```

The primary trigger is a canonical public skill change:

```text
skills/<name>/SKILL.md
```

Generated adapter skill changes should be traced back to the owning canonical skill:

```text
dist/adapters/codex/.agents/skills/<name>/SKILL.md
dist/adapters/claude/.claude/skills/<name>/SKILL.md
dist/adapters/opencode/.opencode/skills/<name>/SKILL.md
```

map to:

```text
skills/<name>/SKILL.md
```

Generated adapter changes should not independently define benchmark ownership. If generated output changes without a corresponding canonical skill change, treat that as adapter drift or regeneration evidence and require adapter validation rather than automatically requiring a new dynamic skill benchmark.

Recommended metadata:

```yaml
changed_skill_benchmarks:
  required_due_to_changes:
    - skill: architecture-review
      trigger:
        canonical_changed: true
        generated_changed: true
      benchmark: architecture-review
      status: pass
  generated_trace:
    - generated_path: dist/adapters/codex/.agents/skills/architecture-review/SKILL.md
      owning_skill: skills/architecture-review/SKILL.md
      benchmark: architecture-review
```

Examples:

| Changed surface | Benchmark expectation |
|---|---|
| `skills/architecture/SKILL.md` public text changed | run `architecture-no-impact` or the current architecture benchmark |
| `skills/learn/SKILL.md` public text changed | run `learn-no-durable-lesson` |
| `skills/spec-review/SKILL.md` changed | run the `spec-review` benchmark if defined |
| generated adapters changed only because a covered skill changed | run that skill's benchmark |
| internal-only tests or plans changed | no extended benchmark required |

If no benchmark exists yet for the changed public skill, release metadata should record the gap and follow-up. That gap should warn rather than block unless the release claims complete coverage for that skill.

## Benchmark prompt requirements

Each prompt should be:

- short;
- fixture-backed;
- single-skill focused;
- output-bounded;
- stable across releases;
- free of RigorLoop-internal local examples;
- explicit about whether file edits are allowed.

Most prompts should say:

```text
Do not edit files.
Output only:
...
```

Editing benchmarks may be added later, but the first expanded suite should focus on runtime cost, handoff correctness, and routing correctness.

## Initial prompt shapes

### `workflow-route.md`

```text
Use the workflow skill to decide the next step for this project change.

Do not edit files.

Output only:
- recommended next skill
- one-paragraph rationale
- blockers, if any
```

### `proposal-short.md`

```text
Use the proposal skill to draft a short proposal for a small user-facing feature.

Do not edit files.

Output only:
- proposed proposal path
- proposal title
- one-paragraph summary
- next recommended stage
```

### `plan-handoff.md`

```text
Use the plan skill to inspect the current handoff state for this fixture.

Do not edit files.

Output only:
- current milestone
- milestone state
- next stage
- whether verify is ready
```

### `implement-handoff.md`

```text
Use the implement skill to inspect whether the current milestone is ready for implementation.

Do not edit files.
Do not write code.

Output only:
- implementation readiness
- missing evidence, if any
- next recommended action
```

### `code-review-small.md`

```text
Use the code-review skill to review the small changed file in this fixture.

Do not edit files.

Output only:
- review status
- findings, if any
- next stage
```

### `explain-change-summary.md`

```text
Use the explain-change skill to summarize the completed fixture change.

Do not edit files.

Output only:
- explain-change path
- summary of changed surfaces
- missing evidence, if any
- next stage
```

### `verify-final-pack.md`

```text
Use the verify skill to check whether this fixture has enough final evidence for PR handoff.

Do not edit files.

Output only:
- verification status
- missing evidence, if any
- next stage
```

### `pr-handoff.md`

```text
Use the pr skill to decide whether this fixture is ready for PR handoff.

Do not edit files.

Output only:
- PR readiness
- missing blockers, if any
- durable artifacts to link
```

## Benchmark coverage metadata

Release metadata should include benchmark coverage. YAML is the release gate; Markdown reports should include a human-readable coverage table.

Example:

```yaml
benchmark_coverage:
  suite_id: skill-token-runtime-v2
  required_core:
    - workflow-route
    - proposal-short
    - plan-handoff
    - implement-handoff
    - code-review-small
    - explain-change-summary
    - verify-final-pack
    - pr-handoff
  required_core_status: pass
  transition_carryover_required:
    - architecture-no-impact
    - learn-no-durable-lesson
  transition_carryover_status: pass
  extended_optional:
    - proposal-review
    - spec
    - spec-review
    - architecture
    - architecture-review
    - plan-review
    - test-spec
    - learn
    - research
    - explore
    - vision
    - project-map
  extended_run:
    - architecture-no-impact
    - learn-no-durable-lesson
  changed_skill_benchmark_status: pass
  changed_skill_benchmarks:
    required_due_to_changes: []
    missing_benchmarks: []
  missing_required: []
  missing_optional: []
  missing_important_skills:
    - spec
    - architecture-review
```

Markdown reports should summarize the same evidence for reviewers:

```md
## Benchmark coverage

| Coverage group | Required? | Benchmarks | Status |
|---|---:|---|---|
| Core workflow | yes | workflow, proposal, plan, implement, code-review, explain-change, verify, pr | pass |
| Transition carryover | yes for this release | architecture-no-impact, learn-no-durable-lesson | pass |
| Changed public skills | conditional | none | pass |
| Extended optional | no | spec, spec-review, architecture-review, plan-review, test-spec, research, explore, vision, project-map | not run |
```

## Measurement requirements

For each benchmark run, record:

- input tokens;
- cached input tokens;
- output tokens;
- reasoning output tokens;
- estimated command-output tokens;
- full-file read signals;
- repeated file-read signals;
- generated-output read signals;
- broad-search signals;
- largest cost driver;
- result-quality status.

## Result-quality status

Each benchmark should report:

```text
pass
fail
inconclusive
not-reviewed
```

Token cost alone is insufficient. A low-token result that gives the wrong handoff is not a good benchmark result.

The first slice should use manual review for result quality and record the review in YAML. Structured expected-output checks should be deferred until manual result-quality review produces stable patterns.

Example:

```yaml
result_quality:
  status: pass
  reviewed_by: maintainer
  review_surface: docs/reports/token-cost/releases/v0.1.1.md
  reviewed_at: "2026-05-11"
  criteria:
    - id: obeyed_no_edit_instruction
      expectation: The benchmark did not edit files.
      result: pass
      notes: ""
    - id: output_shape
      expectation: The response followed the prompt's requested output shape.
      result: pass
      notes: ""
    - id: no_forbidden_readiness_claim
      expectation: The response did not claim downstream readiness that the skill does not own.
      result: pass
      notes: ""
    - id: correct_next_stage
      expectation: The response named the expected next stage for the fixture.
      result: pass
      notes: ""
  notes: Manual review found the output acceptable for this benchmark.
  blockers: []
```

Failed result-quality evidence should identify the failed criterion and blocker:

```yaml
result_quality:
  status: fail
  reviewed_by: maintainer
  review_surface: docs/reports/token-cost/releases/v0.1.1.md
  reviewed_at: "2026-05-11"
  criteria:
    - id: no_forbidden_readiness_claim
      expectation: The response must not claim PR readiness before verify evidence.
      result: fail
      notes: The response said the change was PR-ready.
  notes: Benchmark output violated skill ownership boundaries.
  blockers:
    - forbidden readiness claim
```

For required benchmarks, release validation should require `result_quality.status`, `reviewed_by`, `review_surface`, `reviewed_at`, `criteria`, `notes`, and `blockers`. It should reject `not-reviewed` for required benchmarks. `inconclusive` should be allowed only with notes and follow-up. The actual correctness judgment can remain manual in the first slice.

For final public releases, required benchmarks should normally have `result_quality.status: pass`. Required benchmarks with `fail` or `inconclusive` should block final public release unless an explicit release-owner waiver is recorded. Optional extended benchmarks with `inconclusive` should warn with notes and follow-up unless they became required because their public skill changed.

Waiver example:

```yaml
result_quality:
  status: inconclusive
  reviewed_by: release-owner
  reviewed_at: "2026-05-11"
  notes: Output was incomplete because Codex returned truncated text, but no benchmark-relevant skill changes occurred since the RC passing run.
  follow_up: Rerun benchmark in next RC environment.
  release_may_proceed: true
  waiver:
    status: approved
    approved_by: xiongxianfei
    approved_role: release-owner
    approval_surface: release checklist
    approved_at: "2026-05-11"
    reason: Known benchmark runner instability; no affected public skill changed.
    evidence: docs/reports/token-cost/releases/v0.1.1-rc.1.yaml
```

Valid waiver approval roles should be:

```text
release-owner
release-manager
repository-maintainer
```

Waivers should require both an approver identity and an approved role. Vague role values such as `owner`, `admin`, or `maintainer-ish` should not validate.

The first implementation should validate `approved_by` only as a non-empty review-visible string and `approved_role` as one of the allowed roles. It should not validate approver identity against GitHub collaborators, CODEOWNERS, or maintainer registries yet. That authority lookup can be added later if waiver misuse becomes a real problem.

Examples:

- `verify-final-pack` should not claim PR readiness when final evidence is missing.
- `code-review-small` should not hand off to final verify if more implementation milestones remain.
- `plan-handoff` should identify the active plan handoff state when present.
- `pr-handoff` should not claim implementation or verification passed unless evidence exists.

## Release gate behavior

The release-required core suite should be required for public releases.

Release validation should block when:

- required core suite metadata is missing;
- transition carryover metadata is missing during the transition release;
- any required core benchmark is missing without waiver;
- any transition carryover benchmark is missing without waiver during the transition release;
- an existing benchmark for a changed public skill is missing without waiver;
- any required core benchmark has invalid or unparsable analyzer evidence;
- result-quality status is `fail` for a required benchmark, transition carryover benchmark, changed-skill-required benchmark, or optional benchmark explicitly claimed as release coverage;
- result-quality status is `inconclusive` for a required final-release benchmark without waiver;
- result-quality status is `not-reviewed` for a required benchmark;
- public skill portability checks fail.

Release validation should warn when:

- input-token warning threshold is exceeded;
- command-output amplification warning threshold is exceeded;
- full-skill reads increase;
- repeated file reads increase;
- an extended suite skill remains unmeasured.
- an optional extended benchmark is `inconclusive` with notes and follow-up;
- an optional extended benchmark fails but was not required by changed public skill policy and was not explicitly claimed as release coverage.

Optional extended benchmark failures that are not release-required should not be summarized as coverage pass. They should be visible as warning evidence with notes and follow-up.

Use stable warning codes for optional benchmark result-quality problems:

```text
optional-benchmark-failed
optional-benchmark-inconclusive
```

Do not encode the benchmark or skill name into the code. Put benchmark and skill identity in separate metadata fields.

Example:

```yaml
warnings:
  - code: optional-benchmark-failed
    benchmark: architecture-review
    skill: architecture-review
    severity: warning
    message: Optional benchmark failed, but it is not required for this release.
    follow_up: Review before making architecture-review benchmark required.
  - code: optional-benchmark-inconclusive
    benchmark: learn-no-durable-lesson
    skill: learn
    severity: warning
    message: Optional benchmark result quality was inconclusive.
    follow_up: Rerun or improve expected-output criteria before relying on this benchmark.
```

If an optional benchmark becomes required because the public skill changed, use required-benchmark blocking codes instead:

```text
required-benchmark-failed
required-benchmark-inconclusive
required-benchmark-missing
```

The first implementation should keep token thresholds warning-only unless benchmark evidence is missing or invalid, result quality fails, or an already hard structural gate fails.

## Expected behavior changes

- `benchmarks/token-cost/manifest.yaml` distinguishes release-required core prompts from optional extended prompts.
- Release reports identify which skills were covered by the dynamic benchmark.
- Release metadata can distinguish missing required core evidence from missing optional extended evidence.
- Dynamic run summaries include result-quality status in addition to token and analyzer signals.
- The required core suite expands from seven prompts to eight core delivery prompts, adding `plan-handoff`, `explain-change-summary`, and `pr-handoff`.
- The current `architecture-no-impact` and `learn-no-durable-lesson` prompts remain required for one v2 transition release, then move to optional extended coverage unless their public skills change.

## Versioning and comparison

The expanded required-core suite should use `skill-token-runtime-v2`.

The first v2 report should be treated as a new suite baseline. It may compare overlapping prompts with the v1 report for context, but it should not compute strict numeric regressions between v1 and v2 required-suite totals.

The first v2 transition report should be `v0.1.1` if that is the next public release. If the project publishes a release candidate first, use `v0.1.1-rc.1` for the RC transition report. Do not backdate the v2 transition report to `v0.1.0`; the public latest is already `v0.1.0`.

An expanded v2 transition report must not silently overwrite an existing release token report path. The repository already contains a tracked pre-release `v0.1.1` report using `skill-token-runtime-v1`. If `v0.1.1` remains the first public v2 transition target, the v2 implementation should explicitly supersede that tracked pre-release v1 report before the public release is finalized. The supersession should preserve the v1 report as historical evidence, either by moving it to a clearly historical path or by recording the v1 values as overlap-comparison evidence in the v2 report. If `v0.1.1` is finalized before v2 lands, the first v2 transition report should move to the next public release line or RC path instead.

The preferred preservation path is to keep the final v2 report at the canonical release path:

```text
docs/reports/token-cost/releases/v0.1.1.md
docs/reports/token-cost/releases/v0.1.1.yaml
```

and move the existing pre-transition v1 report to:

```text
docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md
docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml
```

The v2 report should then reference the pre-transition v1 report as overlap-comparison evidence.

Example:

```yaml
comparison:
  baseline: true
  comparable: false
  previous_release: v0.1.0
  previous_suite_id: skill-token-runtime-v1
  prior_pretransition_report: docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.yaml
  overlap_comparison_available: true
  rationale: First skill-token-runtime-v2 release report. Suite totals are not comparable with v1, but overlapping prompts are retained as historical evidence.
```

Markdown reports should include an overlap comparison note:

```md
## Overlap comparison

This is the first `skill-token-runtime-v2` report.

The earlier pre-transition `skill-token-runtime-v1` report is preserved at:

`docs/reports/token-cost/releases/v0.1.1-skill-token-runtime-v1-pretransition.md`

Suite totals are not directly comparable. Overlapping prompts may be compared as continuity evidence only.
```

Core rule:

```text
Do not silently replace release report identity.
Either supersede pre-release report evidence explicitly, or choose a non-colliding release path.
```

One canonical final report should exist per release version. Historical pre-transition reports should be preserved separately and linked.

Example:

```yaml
benchmark_suite:
  id: skill-token-runtime-v2
  previous_suite_id: skill-token-runtime-v1
  baseline_for_suite: true
  transition_report: true
  transition_from_release: v0.1.0
  manifest: benchmarks/token-cost/manifest.yaml

comparison:
  baseline: true
  comparable: false
  previous_release: v0.1.0
  previous_suite_id: skill-token-runtime-v1
  overlap_comparison_available: true
  rationale: First skill-token-runtime-v2 report; suite totals are not directly comparable with v1, but overlapping prompts may be compared.
```

## Architecture impact

This is a release benchmark coverage change.

Affected surfaces may include:

- `benchmarks/token-cost/manifest.yaml`;
- `benchmarks/token-cost/prompts/`;
- `docs/reports/token-cost/releases/`;
- `scripts/run-token-cost-benchmarks.py`;
- `scripts/validate-token-cost-report.py`, if metadata validation changes;
- `scripts/analyze-codex-jsonl.py`, only if needed for coverage metadata or result-quality evidence;
- release validation integration if the report schema changes.

No workflow stage order, runtime architecture, or adapter package layout change is expected.

## Testing and verification strategy

Likely validation should include:

```bash
python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test
python scripts/analyze-codex-jsonl.py <sample-jsonl>
python scripts/validate-token-cost-report.py <sample-release-metadata.yaml>
python scripts/measure-skill-tokens.py
git diff --check --
```

If scripts are changed:

```bash
python -m py_compile scripts/run-token-cost-benchmarks.py scripts/analyze-codex-jsonl.py scripts/validate-token-cost-report.py
```

If canonical skill text changes:

```bash
python scripts/build-adapters.py --check
python scripts/validate-adapters.py
```

The next test spec should cover required-core versus optional-extended manifest validation, release metadata coverage validation, result-quality status validation, and dry-run coverage for the added prompt fixtures.

## Rollout and rollback

Rollout:

1. Review and accept this proposal.
2. Write a spec or amendment to `specs/release-token-friendliness-benchmark-for-skills.md`.
3. Add or update benchmark manifest fields for `skill-token-runtime-v2`, required core, transition carryover, and optional extended prompts.
4. Add `plan-handoff`, `explain-change-summary`, and `pr-handoff` prompt fixtures.
5. Update release metadata validation for benchmark coverage, changed public skill benchmark requirements, and manual result-quality status.
6. Run the expanded core suite and update the next release report.
7. Use the expanded report to choose targeted skill optimization work.

Rollback:

- keep the existing seven-prompt suite as the release-required baseline;
- preserve any new prompts as optional fixtures;
- remove benchmark coverage metadata from release gating if it proves unstable;
- continue recording static skill size and existing dynamic benchmark evidence.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Release benchmark becomes too slow. | Keep only the core suite required; extended suite remains optional. |
| Benchmarks become flaky. | Use stable prompts, small fixtures, and output-bounded tasks. |
| Token cost improves but correctness regresses. | Add result-quality status. |
| Every skill becomes a release blocker. | Keep extended suite optional until stable and explicitly governed. |
| Reports become too verbose. | Store summary in release reports; raw run evidence stays under `docs/reports/token-cost/runs/`. |
| Optimization deletes safety guidance. | Use benchmark results to guide targeted refactors while preserving safety-critical rules. |
| Current baseline comparability is blurred by moving `architecture` and `learn` to optional. | Keep them required for one transition release, then record suite version and coverage metadata so release reports explain comparison boundaries. |

## Open questions

None.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-11 | Propose phased expansion of dynamic benchmark coverage. | The first dynamic benchmark proved runtime measurement is useful but incomplete. |
| 2026-05-11 | Make core delivery skills the required benchmark focus. | They represent the normal public workflow path. |
| 2026-05-11 | Keep extended skills optional. | Avoid overloading every release with every skill benchmark. |
| 2026-05-11 | Add result-quality status. | Token cost without correctness is not meaningful release evidence. |
| 2026-05-11 | Use `skill-token-runtime-v2` for the expanded suite. | Required coverage and manifest shape change enough to create a new comparable series. |
| 2026-05-11 | Keep `architecture-no-impact` and `learn-no-durable-lesson` required for one transition release. | Baseline prompts should be retired through a named transition, not dropped silently. |
| 2026-05-11 | Use manual result-quality review first. | Human judgment is less brittle than premature semantic output automation. |
| 2026-05-11 | Conditionally require benchmarks for changed public skills when benchmarks exist. | Changed public skill behavior should have runtime evidence without making missing optional benchmarks hard blockers. |
| 2026-05-11 | Store coverage metadata in YAML and Markdown. | YAML gates release validation; Markdown helps reviewers see coverage at a glance. |
| 2026-05-11 | Target `v0.1.1`, or `v0.1.1-rc.1` if there is an RC, for the first v2 transition report. | Public latest is `v0.1.0`; the v2 transition belongs to the next release line. |
| 2026-05-11 | Define structured manual `result_quality` metadata per run. | Manual review remains auditable while expected-output automation is deferred. |
| 2026-05-11 | Detect changed public skills from canonical skill changes and trace generated adapter changes back to canonical ownership. | Canonical skill text owns behavior; generated output should prove adapter drift or traceability, not define benchmark ownership alone. |
| 2026-05-11 | Add `architecture-review` as the first optional extended benchmark after core expansion. | It is review-heavy, safety-sensitive, boundary-sensitive, and likely token-expensive. |
| 2026-05-11 | Treat required benchmark `inconclusive` result quality as a final-release blocker unless waived. | Inconclusive required evidence does not prove the public skill behaved acceptably. |
| 2026-05-11 | Put changed public skill detection in release validation. | Release validation owns release diff context; token-cost validation owns report completeness and consistency. |
| 2026-05-11 | Use a tiny architecture-review fixture with a canonical architecture update and no change-local delta. | The benchmark should guard the simplified architecture-review rule directly. |
| 2026-05-11 | Pass required benchmark context from release validation to token-cost validation. | Release validation decides what is required; token-cost validation proves the report satisfies it. |
| 2026-05-11 | Use a separate architecture-review scenario fixture directory first. | Keeping scenarios isolated avoids hidden fixture growth and preserves cost attribution. |
| 2026-05-11 | Limit waiver approval roles to `release-owner`, `release-manager`, and `repository-maintainer`. | Waivers should be explicit, role-scoped, and review-visible. |
| 2026-05-11 | Support required benchmark context as both an in-memory object and a CLI YAML file. | Object transport keeps release validation simple; YAML transport supports tests, debugging, and review. |
| 2026-05-11 | Validate waiver approver identity as a non-empty review-visible string in the first slice. | Collaborator lookup would add network, permission, and identity-mapping complexity before there is evidence it is needed. |
| 2026-05-11 | Trigger shared fixture-base work after three duplicated scenario fixtures or a duplication-related review finding. | Simple duplicated fixtures are easier to review until duplication becomes a maintenance risk. |
| 2026-05-11 | Use stable `required_benchmark_context` fields for release-to-token-cost validation. | The context needs one validation contract across in-process and CLI transports. |
| 2026-05-11 | Generate CLI required-benchmark context YAML transiently by default. | The context is validation input, not durable release evidence unless explicitly cited. |
| 2026-05-11 | Count `proposal-review` as the likely third duplicated scenario fixture trigger. | It is the next review-heavy scenario likely to share the minimal public-project base. |
| 2026-05-11 | Preserve or explicitly supersede existing `v0.1.1` v1 report evidence if v2 also targets `v0.1.1`. | New suite baselines must not silently overwrite existing release-report identity. |
| 2026-05-11 | Scope result-quality blockers to required or explicitly claimed benchmark coverage. | Optional suite failures should warn unless the benchmark became release-required or was claimed as release evidence. |
| 2026-05-11 | Preserve existing pre-release v1 report as `v0.1.1-skill-token-runtime-v1-pretransition` if v2 also targets `v0.1.1`. | One canonical final report should exist per release version, while historical pre-transition evidence remains linked. |
| 2026-05-11 | Use `optional-benchmark-failed` and `optional-benchmark-inconclusive` warning codes. | Stable generic codes keep warning semantics consistent while benchmark and skill fields carry specificity. |

## Next artifacts

- spec-review
- architecture or no-architecture decision
- execution plan
- test spec

## Follow-on artifacts

- Proposal-review R2 approved this proposal with no material findings.
- Spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`.

## Readiness

Accepted. The downstream feature spec has been drafted and is listed in Follow-on artifacts.

This accepted proposal expands the proven dynamic Token-Friendliness benchmark while keeping the release-required suite focused and practical.

Core invariant:

```text
Benchmark the skills users rely on most.
Keep the required suite small.
Use optional suites to expand coverage without blocking every release.
```
