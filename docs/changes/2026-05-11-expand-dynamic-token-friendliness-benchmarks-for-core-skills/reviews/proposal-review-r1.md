# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Existing release token report metadata: `docs/reports/token-cost/releases/v0.1.1.yaml`
- Existing release token report Markdown: `docs/reports/token-cost/releases/v0.1.1.md`
- Governance: `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`
- Current public release check: `gh release list --limit 5` showed `v0.1.0` as latest while a tracked `v0.1.1` token report already exists in the repository.

## Findings

### EDTF-PR1 - v2 transition target conflicts with existing tracked v0.1.1 v1 report

Finding ID: EDTF-PR1
Severity: major
Dimension: rollout realism

Evidence:

- The proposal says the first v2 transition report should be `v0.1.1` if that is the next public release, and says existing `skill-token-runtime-v1` reports remain valid historical evidence.
- The repository already contains `docs/reports/token-cost/releases/v0.1.1.yaml` with `benchmark_suite.id: skill-token-runtime-v1`.
- `docs/reports/token-cost/releases/v0.1.1.md` says it is the first release Token-Friendliness report and establishes the comparable baseline.

Problem:

The same release-report path cannot unambiguously serve as both the existing v1 baseline and the first v2 transition baseline unless the proposal defines replacement, supersession, or historical preservation semantics.

Required outcome:

Clarify release-report identity so v2 transition evidence does not overwrite or ambiguously replace existing v1 release-report evidence.

Safe resolution:

Revise `Versioning and comparison` to state that an expanded v2 transition report must not silently overwrite an existing `docs/reports/token-cost/releases/<release>.yaml` report. If `v0.1.1` remains the first v2 target, the proposal should say whether the existing tracked `v0.1.1` v1 report is updated before public release, preserved under a historical path, or superseded with explicit evidence. Otherwise, target the next release or RC report path that does not collide.

### EDTF-PR2 - Result-quality blocker wording can make optional benchmarks release-blocking

Finding ID: EDTF-PR2
Severity: major
Dimension: scope control

Evidence:

- Non-goals say optional or periodic skills should not be release-blocking yet.
- The optional extended suite section says missing optional coverage should not block unless the release claims coverage or the skill changed in a benchmark-relevant way.
- The release gate blocking list says `result-quality status is fail` without limiting that rule to required, transition carryover, changed-skill-required, or claimed optional benchmarks.

Problem:

The unqualified blocker can make any failed optional benchmark a release blocker, which conflicts with the two-tier benchmark model and the proposal's scope-control rationale.

Required outcome:

Align release-gate wording with the two-tier benchmark model so optional benchmarks remain non-blocking unless they are claimed as covered or become required because their public skill changed.

Safe resolution:

Revise `Release gate behavior` to block on result-quality `fail`, `not-reviewed`, or unwaived `inconclusive` only for required benchmarks, transition carryover benchmarks, changed-skill-required benchmarks, or optional benchmarks explicitly claimed as release coverage. Optional extended benchmark failures that are not release-required should warn with notes and follow-up and must not be summarized as coverage pass.

## Checklist coverage

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal clearly frames a coverage gap in dynamic release token-friendliness evidence. |
| User value | pass | The proposal gives maintainers and downstream users broader runtime-cost visibility across the normal delivery path. |
| Option diversity | pass | Benchmark-everything, keep-current-suite, and required-core-plus-optional-extended options are distinct. |
| Decision rationale | pass | The recommended two-tier suite follows from release-cost, comparability, and maintainer burden constraints. |
| Scope control | concern | EDTF-PR2: unqualified result-quality blockers can make optional benchmarks release-blocking. |
| Architecture awareness | pass | The proposal identifies manifest, prompt, fixture, report, validator, analyzer, and release validation boundaries. |
| Testability | pass | The proposal defines prompt fixtures, dry-run validation, metadata checks, result-quality evidence, and runner/analyzer validation. |
| Risk honesty | concern | EDTF-PR1: v1/v2 report identity risk is visible but not resolved for the existing tracked `v0.1.1` report. |
| Rollout realism | concern | EDTF-PR1 must be resolved before spec chooses report paths or migration behavior. |
| Readiness for spec | changes-requested | Direction is sound, but two release-gate semantics need revision before spec authoring relies on the proposal. |

## Scope preservation

Pass. The proposal visibly classifies the initial user goals and later decision refinements in `Initial Intent Preservation`.

## Vision fit

Pass. `Vision fit` uses the required value `fits the current vision` and aligns with `VISION.md`.

## Suggested proposal edits

- Add a versioning rule: do not silently overwrite an existing release token report path when creating a new suite baseline.
- Clarify whether the existing tracked `v0.1.1` v1 report is preserved, superseded, or replaced before public release if v2 also targets `v0.1.1`.
- Scope result-quality blockers to required, transition carryover, changed-skill-required, and explicitly claimed optional coverage.
- Add a warning rule for failed optional benchmarks that were run but not required.

## Recommended next stage

Changes requested. This direct proposal-review remains isolated and does not automatically hand off to `spec`.
