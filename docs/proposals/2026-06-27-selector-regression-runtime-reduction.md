# Selector-Regression Runtime Reduction With Coverage-Preservation Proof

## Status

accepted

## Problem

The previous validation-runtime follow-through slice produced 0% validated feature-caused runtime improvement. That does not mean there is no room to improve validation speed. It means the slice shipped measurement, proof preservation, selector-route blockers, and broad-smoke classification, but did not enable a runtime-reducing mechanism.

The current measured pain has two distinct profiles:

| Surface | Observed cost | Meaning |
| --- | ---: | --- |
| `python scripts/test-select-validation.py` | about 140 seconds for 102 tests | selected-validation and developer inner-loop bottleneck |
| `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` | about 725 seconds for 11 checks | boundary and PR-readiness bottleneck |

The June 26 proposal correctly treats these as different optimization targets. Selector regression is a selected-validation bottleneck, while broad-smoke needs child-check side-effect classification before safe parallelization.

The immediate opportunity is to reduce selector-regression runtime without reducing selected-check coverage, hiding missing selector routes, or weakening final verification.

The accepted June 24 validation-runtime proposal already defines the safe order:

```text
measure
-> run cheap preconditions
-> select the smallest complete check set
-> avoid duplicate parsing and process startup
-> reuse only with complete identity
-> parallelize only independent work
-> run final broad verification once against stable state
```

This proposal applies that discipline to the first runtime-reducing target: `selector.regression`.

## Goals

- Produce an actual, measured runtime reduction for the selector-regression path.
- Preserve the full selected-validation behavior covered by `scripts/test-select-validation.py`.
- Keep missing selector-route detection strict and deterministic.
- Reduce runtime through safe mechanisms: fixture reuse, avoiding repeated repository-state discovery, avoiding unnecessary subprocess invocations, splitting pure selector logic from CLI-boundary tests, batching repeated cases, and preserving only essential subprocess tests for command-boundary behavior.
- Record before/after runtime evidence.
- Record selected-check identity before and after optimization.
- Preserve failure sensitivity for missing routes, changed-path classification, cache-boundary metadata, and broad-smoke classification.
- Keep the selected-CI wrapper behavior compatible.
- Keep broad-smoke parallelism, validation caching, and broad validator composition out of this first runtime-reduction slice.
- Preserve final verify as actual-run evidence against stable state.

## Non-goals

- Do not reduce runtime by deleting required selector tests.
- Do not weaken selected-check routing.
- Do not make broad-smoke run in parallel in this proposal.
- Do not enable validation-result caching in this proposal.
- Do not use cache hits as final verification proof.
- Do not rewrite all validators.
- Do not change selector semantics merely to make tests pass faster.
- Do not remove subprocess tests that prove CLI or wrapper behavior.
- Do not hide selected-route blockers by falling back to broad-smoke.
- Do not claim branch readiness, PR readiness, or hosted CI readiness from this proposal alone.
- Do not set a permanent runtime budget before baseline and revised measurements are compared.

## Vision fit

fits the current vision

RigorLoop depends on trustworthy validation evidence. Slow validation increases the temptation to skip proof, while careless speedups can hide defects. This proposal keeps the proof intact and reduces avoidable runtime in the selected-validation path.

This proposal would conflict with the current vision if selected-check coverage is reduced, a missing selector route stops being detected, test runtime improves only because subprocess boundary tests were removed, broad-smoke passes are treated as a substitute for selector routing, final verify relies on inner-loop evidence, runtime evidence cannot show what changed, or failure diagnostics become less actionable.

## Context

The June 26 zero-runtime learn session says the earlier slice produced 0% feature-caused improvement because the implemented mechanisms were not runtime reducers. It added measurement and readiness infrastructure, not an actual speed lever.

The validation-runtime speed learn session also records that selected modes already have some `parallel_safe` support, while broad-smoke still runs sequential `run_check` calls. It also notes that new changed paths without deterministic selector classification can block selected CI before the intended checks run.

The test-spec review found the manual selector-regression profiling proof was under-specified: it lacked required environment, exact profiling steps, pass/fail criteria, and owning stage. That gap should be closed before relying on profiling-driven runtime decisions.

This proposal therefore starts with a profile proof, then implements one measured runtime reducer.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Confirm whether there is still improvement space | in scope | Problem, Recommended direction |
| Use best practices, not blind optimization | in scope | Recommended direction, Testing and verification strategy |
| Target real runtime improvement | in scope | Goals, Success metrics |
| Preserve validation rigor | in scope | Non-goals, Acceptance criteria |
| Avoid broad unsafe changes | in scope | First-slice boundary |
| Treat current 0% result honestly | in scope | Problem, Context |
| Decide what to optimize next | in scope | Options considered, Follow-up decision |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Selector-regression profiling proof | core to this proposal | Exact bottleneck evidence should exist before changing tests. |
| `scripts/test-select-validation.py` runtime reduction | core to this proposal | This is the selected-validation bottleneck. |
| Selected-check identity preservation | core to this proposal | Runtime should not improve by losing coverage. |
| Missing selector-route blocker preservation | core to this proposal | Missing routes should remain hard blockers. |
| CLI/subprocess boundary test audit | core to this proposal | Keep subprocess tests that prove command behavior. |
| In-process selector fixture reuse | first-slice candidate | Likely safe runtime reducer. |
| Broad-smoke child parallelism | separate implementation slice | Needs side-effect classification first. |
| Local safe-result cache | separate proposal | Requires complete input identity and final-verify boundary. |
| Broad validator composition | deferable follow-up | Only justified if profiling shows startup/import remains dominant. |
| Persistent validation worker | out of scope | Too large for this slice. |

## Options Considered

### Option 1: Do nothing

This has the lowest immediate coverage-regression risk, but it leaves the selected-validation bottleneck in place, keeps local feedback above the default selected-CI timeout, and does not use the measurement infrastructure already built.

Rejected.

### Option 2: Start with broad-smoke parallelism

This targets the largest observed wall-clock cost, but broad-smoke child checks need side-effect and resource classification first. Immediate parallelism can create nondeterminism and shared-temp-root conflicts. It is also boundary-validation work, not the developer inner-loop bottleneck.

Deferred.

### Option 3: Enable caching

Caching can produce large gains for repeated identical runs, but it requires complete command, input, and policy identity. Cache hits should not become final closeout evidence. Prior cache adoption work also showed that opt-in flag paths are brittle when not wired into normal usage.

Deferred.

### Option 4: Broad validator composition

Broad composition could reduce repeated Python startup and repository discovery, but it has a larger architecture and ownership surface. It can also merge validator contracts too early. It should be justified only if profiling shows startup/import is a dominant cost.

Deferred.

### Option 5: Target selector-regression duplication and subprocess overhead

This directly targets the measured selected-validation bottleneck, keeps broad-smoke and caching safety boundaries intact, and can preserve full behavior with selected-check identity and failure-sensitivity proof.

Recommended.

## Recommended Direction

Use a focused selector-regression runtime-reduction slice.

The governing rule:

```text
Runtime improvement should be caused by less duplicate work,
not by less proof.
```

The recommended implementation strategy is to complete profiling evidence, identify selector-regression runtime contributors, split selector tests into logical categories, replace repeated subprocess execution with in-process selector calls where the subprocess boundary is not the behavior under test, reuse expensive fixtures and repository-state snapshots inside the test process, keep dedicated subprocess tests for CLI, wrapper, exit-code, timeout, and output behavior, compare selected-check identity and failure sensitivity before and after, and record the measured runtime change.

## Expected Behavior Changes

Before this change, `python scripts/test-select-validation.py` runs all selector regression coverage through a slower structure, takes about 140 seconds in recorded evidence, and requires the selected-CI wrapper to use a timeout override in known evidence.

After this change, `python scripts/test-select-validation.py` should run the same required selector coverage with shared fixtures and in-process selector calls where safe. It should retain subprocess tests for command-boundary behavior and record either lower runtime or a precise no-safe-reduction rationale.

The expected runtime result is a measured selector-regression runtime reduction, or explicit evidence that selector-regression is not safely reducible. A no-safe-reduction result is acceptable only if the profiling proof is complete and points to the next target.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `scripts/test-select-validation.py` | Refactor selector-regression tests for fixture reuse and in-process selector calls where safe. |
| `scripts/validation_selection.py` | No semantic change expected; helper entry points may be exposed if needed. |
| Selected-CI wrapper | Should remain compatible; timeout override may no longer be needed if runtime drops enough. |
| Change evidence | Add selector profile and before/after runtime evidence. |
| Broad-smoke | No execution behavior change. |
| Cache | No behavior change. |
| Final verify | No behavior change. |
| Runtime application | No change. |

Architecture is not expected unless the implementation introduces persistent workers, broad validator composition, cross-process protocols, or cache semantics.

## Testing and Verification Strategy

The downstream spec or test-spec should preserve these proof targets:

| Check ID | What is verified |
| --- | --- |
| `SRT-001` | Baseline selector-regression runtime is recorded. |
| `SRT-002` | Revised selector-regression runtime is recorded under comparable environment. |
| `SRT-003` | Ordered selected test/check identity is preserved. |
| `SRT-004` | Missing selector-route fixtures still fail. |
| `SRT-005` | Known selector-route fixtures still select the same checks. |
| `SRT-006` | Cache-boundary metadata remains `not-applicable` unless a separate cache proposal changes it. |
| `SRT-007` | Broad-smoke classification fixtures still pass/fail as before. |
| `SRT-008` | CLI-boundary subprocess tests remain present. |
| `SRT-009` | In-process tests do not replace exit-code or output-shape tests. |
| `SRT-010` | Selected-CI wrapper command still works. |
| `SRT-011` | Runtime reduction is not achieved by skipped test classes. |
| `SRT-012` | Failure diagnostics remain actionable. |
| `SRT-013` | No final verify or PR readiness claim is made from selector-runtime evidence. |

Suggested internal test-suite categories are:

| Category | Purpose | Runtime strategy |
| --- | --- | --- |
| `selector.core` | Pure changed-path classification and check selection | in-process, shared fixtures |
| `selector.fixtures` | Known path classes and missing-route blockers | in-process, table-driven |
| `selector.cache-boundary` | `cache_status` and no-cache final-proof metadata | in-process unless CLI behavior matters |
| `selector.broad-smoke-classification` | broad-smoke child classification fields | in-process or fixture-backed |
| `selector.cli-boundary` | CLI parsing, exit codes, output shape, wrapper behavior | subprocess retained |
| `selector.integration` | selected-CI wrapper route over changed paths | subprocess retained, minimized |

The goal is not to skip categories. The goal is to stop using the most expensive execution method for every category.

## Behavior-Preservation Proof

Create:

```text
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md
```

The proof should compare:

| Surface | Baseline | Revised proof | Expected result |
| --- | --- | --- | --- |
| selected test IDs | ordered list or hash | same or approved delta | preserved |
| selected check IDs | ordered list or hash | same or approved delta | preserved |
| missing-route blockers | fail fixtures | still fail | preserved |
| registered routes | pass/select fixtures | still pass/select | preserved |
| CLI behavior | subprocess fixtures | still covered | preserved |
| diagnostics | failure fixtures | same actionability | preserved |
| broad-smoke classification | fixture coverage | unchanged | preserved |
| cache boundary | `not-applicable` | unchanged | preserved |
| final verify | actual-run owner | unchanged | preserved |

## Manual Profiling Proof Dependency

Before implementation closeout, the selector-regression manual proof should be complete.

Suggested evidence artifact:

```text
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md
```

It should record:

```text
proof ID
environment
commit or HEAD
worktree state
commands
baseline duration
timeout behavior
selected checks observed
dominant contributors or instrumentation limitations
safe reduction identified
no-safe-reduction rationale, if applicable
follow-up decision
```

This responds directly to the test-spec-review finding that the previous manual proof shape was not adequate for implementation reliance.

## Performance Evidence

Create:

```text
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml
docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml
```

Record at minimum:

```yaml
scenario: selector-regression
command: python scripts/test-select-validation.py
environment:
  runner:
  os:
  python:
  cpu_class:
  local_or_ci:
repository_state:
  head:
  worktree_state:
baseline:
  duration_ms:
  test_count:
  selected_check_identity:
revised:
  duration_ms:
  test_count:
  selected_check_identity:
delta:
  duration_ms:
  percent:
preservation:
  selected_identity_preserved: true
  failure_sensitivity_preserved: true
notes:
  timeout_behavior:
  limitations:
```

Use median of at least three runs when practical. If machine variance prevents stable measurement, record that explicitly and rely on same-environment paired runs.

## Success Metrics

Primary success is a median runtime decrease of at least 25% for `python scripts/test-select-validation.py` in a comparable environment while preserving selected-check identity and failure sensitivity.

Alternative success is bringing the command below the default selected-CI timeout without requiring the 180-second override, while preserving selected-check identity and failure sensitivity.

If neither is achieved, this proposal can still close only if it records complete profiling evidence, the dominant bottleneck, why no safe reduction was available, and the next recommended runtime target. It should not claim runtime improvement in that case.

## Rollout and Rollback

Rollout:

1. Complete profiling proof and baseline evidence.
2. Record environment, commands, timeout behavior, selected checks, and dominant contributors.
3. Record selected test/check identity and missing-route negative fixtures.
4. Introduce shared fixtures and convert pure selector logic tests to in-process calls where safe.
5. Keep CLI-boundary subprocess tests and preserve selected-check identity.
6. Record revised runtime, compare identity, rerun failure-sensitivity fixtures, and record whether the selected-CI timeout override is still needed.
7. Review runtime and preservation evidence.
8. Decide whether the next speed slice should target broad-smoke parallelism, validation context composition, or safe inner-loop cache adoption.

Rollback:

- Restore the prior test structure if selector coverage or diagnostics regress.
- Keep profiling evidence.
- Keep reusable fixture helpers only if they remain behavior-preserving.
- Do not keep a faster suite if it drops failure-sensitivity coverage.
- Do not change broad-smoke or cache behavior during rollback.
- Do not claim runtime improvement after rollback.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Runtime improves by skipping tests | Preserve ordered test/check identity and negative fixtures. |
| In-process tests miss CLI bugs | Retain subprocess tests for CLI and wrapper behavior. |
| Fixture reuse hides state leakage | Make fixtures immutable or reset per test group. |
| Runtime varies by machine | Use same-environment paired measurements and medians. |
| Selector helper extraction changes semantics | Add before/after selection identity proof. |
| Missing routes become warnings | Keep missing routes as hard blockers. |
| Broad-smoke remains slow | Treat broad-smoke parallelism as the next slice, not this one. |
| Optimization creates unreadable tests | Keep table-driven fixtures named by behavior and expected outcome. |
| Timeout override remains needed | Record no-safe-reduction rationale or next bottleneck. |

## First-Slice Boundary

First slice includes:

```text
selector-regression profiling proof
selector-regression baseline
shared selector fixtures
in-process pure selector tests
retained CLI subprocess boundary tests
selected-check identity proof
missing-route failure-sensitivity proof
runtime result evidence
```

Out of scope:

```text
broad-smoke parallel execution
local validation cache
remote/shared cache
persistent validation worker
broad in-process validator composition
final verify changes
PR readiness changes
```

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-SRT-001` | Baseline selector-regression runtime evidence exists. |
| `AC-SRT-002` | Revised selector-regression runtime evidence exists. |
| `AC-SRT-003` | Baseline and revised runs are comparable or limitations are recorded. |
| `AC-SRT-004` | Selected test/check identity is preserved or any delta is explicitly approved. |
| `AC-SRT-005` | Missing selector-route blockers still fail. |
| `AC-SRT-006` | Registered selector routes still produce the expected selected checks. |
| `AC-SRT-007` | CLI-boundary subprocess tests remain present. |
| `AC-SRT-008` | In-process tests are used only where command-boundary behavior is not under test. |
| `AC-SRT-009` | Failure diagnostics remain actionable. |
| `AC-SRT-010` | Runtime improvement is measured and attributed to this slice, or a no-safe-reduction rationale is recorded. |
| `AC-SRT-011` | No broad-smoke, cache, validator-composition, final-verify, or PR-readiness behavior changes. |
| `AC-SRT-012` | The follow-up decision names the next measured bottleneck if this slice cannot safely reduce runtime. |
| `AC-SRT-013` | The default `python scripts/test-select-validation.py` command continues to run all required selector-regression contract coverage; no required category is moved to an optional-only command. |
| `AC-SRT-014` | The implementation distinguishes behavioral selector identity, selected-check identity, and unittest identifier identity. |

## Open-Question Resolutions

- Runtime target: use a paired median target of 25% reduction or falling below the default selected-CI timeout. Do not reduce coverage to hit the target.
- Quick mode: no first-slice `--fast` or `--quick`; optimize the default regression command.
- Broad-smoke parallelism: separate slice.
- Caching: separate slice.
- Subprocess tests: retain command-boundary subprocess coverage; move only pure selector logic in-process.
- No-safe-reduction: allowed only with complete profiling evidence and a named next measured bottleneck.

## Open Questions

### 1. What runtime target should be required?

Candidate answer: use 25% median reduction or falling below the default selected-CI timeout as success. Avoid a hard absolute target until baseline evidence is recorded.

### 2. Should the suite add a `--fast` or `--quick` mode?

Candidate answer: no in this slice. Optimize the default regression path first. A separate quick mode risks becoming a weaker path that contributors rely on.

### 3. Should broad-smoke parallelism be bundled into this work?

Candidate answer: no. Broad-smoke has a different risk profile and should consume the child-check classification artifact in a separate slice.

### 4. Should caching be bundled into this work?

Candidate answer: no. Cache adoption needs complete identity, normal-command-path integration, and a separate final-proof boundary.

### 5. Should subprocess tests be removed?

Candidate answer: no. Reduce unnecessary subprocess repetition, but keep subprocess tests for CLI, wrapper, exit-code, timeout, and output behavior.

### 6. What happens if profiling shows no safe selector reduction?

Candidate answer: record the complete no-safe-reduction rationale and route the next proposal to the measured next bottleneck, likely broad-smoke parallelism or validation context composition.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-27 | Target selector-regression first. | It is the measured selected-validation bottleneck and affects local feedback. | Start with broad-smoke parallelism. |
| 2026-06-27 | Preserve selected-check identity. | Runtime should not improve by losing coverage. | Count-only proof. |
| 2026-06-27 | Keep subprocess tests for command boundaries. | In-process calls cannot prove CLI behavior. | Convert all tests to library calls. |
| 2026-06-27 | Defer cache. | Cache needs a separate identity and final-proof contract. | Add cache flags now. |
| 2026-06-27 | Defer broad-smoke parallelism. | Broad-smoke needs side-effect classification before concurrency. | Parallelize all broad-smoke checks immediately. |

## Next Artifacts

```text
spec or focused spec amendment
spec-review
test-spec amendment
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Architecture is not expected unless implementation introduces persistent workers, shared caches, broad validator composition, or new cross-process execution protocols.

Completed:

- Proposal review approved with no material findings and no open blockers.

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-06-27-selector-regression-runtime-reduction/review-log.md`
- Spec: `specs/selector-regression-runtime-reduction.md`

## Readiness

Ready for a focused spec or spec amendment.

## Core Invariant

```text
A faster selector-regression suite is valuable only if it proves the same
selector behavior, the same route blockers, the same command boundaries, and
the same failure sensitivity.

The improvement should come from less duplicate work, not less validation.
```
