# Preflight-First and Measured Script Execution Optimization

## Status

accepted

## Problem

RigorLoop uses repository scripts to validate artifact lifecycle state, change metadata, review artifacts, skills, selected checks, adapter generation, release readiness, clean-install smoke, guides, and branch verification. These checks are essential evidence, but recent verification work showed that repeated cost often came from avoidable orchestration rather than from failing or intrinsically slow tests.

The expensive checks were mostly passing. The repeated cost came from broad validation running before cheap branch-state blockers were resolved, evidence becoming stale after commit state changed, and self-referential commit hashes requiring repeated amendments.

The optimization problem is therefore larger than making individual Python functions faster:

```text
Execute the required checks once, at the correct time, with the smallest
complete input surface, while preserving failure detection and durable evidence.
```

## Goals

- Reduce wall-clock time for routine script and validation execution.
- Prevent expensive validation from running while cheap blockers already prove final readiness cannot pass.
- Measure where time is spent before choosing optimizations.
- Preserve selected-check coverage, failure detection, exit codes, and required evidence.
- Reuse parsed repository state within one invocation.
- Avoid duplicate subprocess startup and duplicate filesystem scans.
- Make changed-surface selection reviewable.
- Introduce safe result reuse only where input identity is complete and deterministic.
- Parallelize only independent, side-effect-free checks after measurement supports it.
- Separate inner-loop validation from final closeout validation.
- Run final branch-readiness verification against stable committed state.
- Avoid self-referential commit-hash evidence.
- Add performance evidence and regression budgets after baselines stabilize.
- Keep diagnostics concise and actionable without confusing output reduction with execution improvement.

## Non-goals

- Do not skip required validation.
- Do not reduce selected-check coverage merely to improve timing.
- Do not treat cache hits as final closeout proof.
- Do not parallelize state-mutating checks.
- Do not add remote or shared caching in the first slice.
- Do not optimize every repository script in one change.
- Do not rewrite validators before profiling identifies a bottleneck.
- Do not introduce approximate or probabilistic cache identity.
- Do not suppress failures to reduce output.
- Do not replace final broad validation when an authoritative trigger requires it.
- Do not require hosted CI for local script optimization.
- Do not make raw elapsed time the only performance metric.
- Do not embed a commit's literal final hash inside files being amended into that same commit.

## Vision fit

fits the current vision

RigorLoop depends on evidence that is durable, inspectable, and trustworthy. Slow or repeatedly executed scripts increase workflow cost and encourage contributors to bypass validation. Optimizing execution sequencing supports the vision when it keeps proof intact and makes rigorous validation easier to retain.

The direction would conflict with the vision if it made validation faster by hiding failures, weakening selected-check coverage, relying on stale results, or claiming branch readiness against a different state from the committed branch.

## Context

The recent verification session separated required cost from avoidable cost.

Required cost included finding a lifecycle fixture defect, detecting untracked authoritative artifacts, and rerunning review or verification after branch-ready state changed.

Avoidable cost included running broad validation before tracked-state blockers were fixed, verifying a pre-commit worktree and then changing the state being verified, recording literal hashes inside a commit that was still being amended, and rerunning broad bundles without reviewable evidence that their inputs changed.

Python provides deterministic profiling with `cProfile`, and CPython's `-X importtime` reports module import timing. Git's porcelain status format is suitable for scripts, and `git diff-index` can compare tracked paths against a tree such as `HEAD`. These are appropriate starting points for separating runtime work, interpreter/import overhead, and cheap repository-state preflight.

The best-practice order is:

```text
measure
-> check cheap preconditions
-> select the smallest complete check set
-> avoid duplicate parsing and process startup
-> reuse results only when identity is provably unchanged
-> parallelize independent work
-> run full boundary validation once
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Improve script execution speed | in scope | Goals, Recommended Direction |
| Reduce repeated verify cost | in scope | Problem, Context, Expected Behavior Changes |
| Avoid unnecessary broad validation | in scope | Goals, Expected Behavior Changes |
| Preserve correctness and coverage | in scope | Non-goals, Risks and Mitigations |
| Add caching | deferred follow-up | Scope Budget, Open Questions |
| Add parallelism | deferred follow-up | Scope Budget, Open Questions |
| Optimize individual Python functions | deferred follow-up | Scope Budget, Options Considered |
| Reduce output noise | out of scope | Non-goals |
| Skip final validation | rejected option | Non-goals, Options Considered |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Timing and profiling instrumentation | core to this proposal | Optimization without measurement is unreliable. |
| Cheap branch and artifact preflight | core to this proposal | Observed repetition included known cheap blockers. |
| Validation phase separation | core to this proposal | Broad checks should not run before basic readiness is established. |
| Changed-surface selection explanation | core to this proposal | Faster validation must remain reviewable. |
| Shared repository-state snapshot | first-slice candidate | It can reduce repeated Git and filesystem inspection without changing validator ownership. |
| In-process composition of related validators | first-slice candidate | It can reduce interpreter startup and duplicate parsing while preserving standalone CLIs. |
| Local safe-result cache | separate implementation slice | Complete identity and final-closeout boundaries need separate review. |
| Parallel independent checks | separate proposal | Schedule as the next optimization proposal after baseline measurements land; independence, resource use, and deterministic output need separate proof. |
| Script-specific algorithm optimization | deferable follow-up | It should be driven by profiling evidence. |
| Remote or shared cache | out of scope | Cross-machine trust and invalidation are larger concerns. |
| Hosted CI redesign | separate proposal | This proposal targets local script execution and verification sequencing. |

## Options Considered

### Option 1: Micro-optimize individual functions

This can improve local hotspots and has low workflow impact, but it may optimize code that contributes little to total time. It also does not address repeated broad validation, process startup, duplicate repository inspection, or stale final verification timing.

This option is insufficient alone.

### Option 2: Parallelize all validation

This may reduce wall-clock time, but it can increase CPU and I/O contention, introduce nondeterminism, create deadlock risks, and make failure output harder to follow. It also does not remove duplicate work, and if startup or duplicate Git inspection dominates runtime, parallel workers can multiply that overhead rather than remove it.

This option is rejected as the first step.

### Option 3: Add caching first

Caching can produce large gains for repeated unchanged runs, but it requires complete input identity and introduces stale-pass risk. It also does not fix premature broad execution.

This option is rejected as the first slice.

### Option 4: Add a cheap verify preflight only

This directly addresses the observed recurrence and has a small implementation surface. It does not reveal broader script bottlenecks or reduce duplicate parsing and startup.

This option is useful but incomplete.

### Option 5: Use measured, preflight-first, tiered execution

This combines timing instrumentation, cheap preflight, focused selection, shared context, duplicate-work reduction, and boundary validation. It addresses the largest avoidable cost first while preserving validation coverage and producing evidence for later caching or parallelism.

This is the recommended direction.

## Recommended Direction

Choose Option 5.

The first implementation direction should establish timing instrumentation, cheap verification preflight, tiered validation sequencing, selection explanation, shared repository-state snapshot support where practical, post-commit final verification guidance, and stable evidence wording.

Caching should remain a measured follow-up unless baseline evidence proves it is necessary in the first slice. Parallel execution should be deferred from the first slice, but the concurrency follow-up should be scheduled to begin after baseline measurements land instead of being left as an indefinite possibility.

## Expected Behavior Changes

Validation execution should become phase-aware:

| Phase | Runs when | Claims |
| --- | --- | --- |
| Preflight | Always | Whether expensive validation may proceed |
| Focused validation | Preflight passes | Changed-surface validation result |
| Boundary validation | Preflight and focused validation pass, or an authoritative override applies | Full-boundary execution result |
| Final verify | Committed state exists and required prior phases pass | Branch readiness |

Cheap blockers such as untracked authoritative artifacts, unmerged paths, open review closeout, stale plan state, missing required artifacts, dirty generated output, or invalid selection inputs should prevent broad validation unless the user explicitly asks for diagnostic execution.

Optimized runs should explain selected checks, changed paths, selection rules, checks not selected, boundary triggers, and any cache status once caching exists.

Timing evidence should record per-check duration, phase, command, result, and a bounded summary of preflight, focused, boundary, and total duration. Detailed timing evidence can live in change-local sidecar files, with retention defined before rollout so high-volume timing data does not become long-term repository bloat by default.

Final branch-readiness verification should run after the commit exists when branch readiness depends on tracked state. Evidence should use stable wording such as current `HEAD`, clean worktree, and tracked branch state rather than a literal self-referential commit hash embedded in the same commit.

## Architecture Impact

The likely affected surfaces are:

| Surface | Expected impact |
| --- | --- |
| Verify workflow and skill | Add preflight-first and post-commit final verification model. |
| Validation selection scripts | Explain selected checks and phases. |
| Validation orchestration | Add timing and phase metadata. |
| Validator library entry points | Accept shared immutable repository context where practical. |
| Git inspection | Consolidate stable preflight queries. |
| Change evidence | Add bounded timing summaries and optional detailed sidecars. |
| Individual validators | Preserve ownership and standalone CLI compatibility. |
| CI | No first-slice redesign. |

A separate architecture artifact is expected only if the implementation introduces a persistent daemon, remote cache, shared service, or new cross-process protocol.

## Testing and Verification Strategy

The downstream test strategy should prove:

| Check ID | What is verified |
| --- | --- |
| `SPEED-001` | Every selected command has measured duration. |
| `SPEED-002` | Timing does not change command result or output contract. |
| `SPEED-003` | A tracked-state blocker prevents boundary validation from starting. |
| `SPEED-004` | A focused validation failure prevents unnecessary boundary validation. |
| `SPEED-005` | An authoritative boundary trigger still runs broad validation. |
| `SPEED-006` | Selection explanation names changed paths and reasons. |
| `SPEED-007` | Shared repository context reduces repeated Git-state collection. |
| `SPEED-008` | Standalone validator commands remain available. |
| `SPEED-009` | Final verify runs against committed tracked state. |
| `SPEED-010` | Same-commit evidence does not require a literal final commit hash. |
| `SPEED-011` | Failure detection and exit codes remain unchanged. |
| `SPEED-012` | Selected-check identity before and after optimization is reviewably equivalent. |
| `SPEED-013` | Cold and warm performance measurements are recorded separately. |
| `SPEED-014` | No cache hit is used as final closeout evidence. |
| `SPEED-015` | Parallel execution, if enabled later, produces deterministic ordered results. |
| `SPEED-016` | Preflight failures name the specific blocker and the cheapest corrective action or rerun command. |

Performance evidence should compare baseline and revised behavior for preflight blockers, focused validation bundles, final committed verify, Python startup/import time, Git inspection calls, and subprocess launches. Success should not be claimed solely from synthetic microbenchmarks.

## Rollout and Rollback

Rollout should start with measurement and non-semantic timing instrumentation, then add cheap preflight, phase classification, selection explanation, shared immutable context, duplicate-work reduction, and final verification sequencing.

Result reuse should be introduced only after the baseline shows remaining material repeated work. Parallel execution should be handled by a scheduled follow-up proposal after the baseline lands, with independence, resource use, and deterministic result aggregation treated as design inputs rather than assumptions.

Rollback should preserve timing evidence even if an optimization is reverted. If preflight incorrectly suppresses required checks, restore prior execution ordering before refining the gate. If result reuse is later introduced and identity validation is incomplete, disable reuse before removing identity validation. If parallel execution is later introduced and output becomes nondeterministic, disable concurrent execution before changing result aggregation.

Standalone validator commands should remain available throughout rollout and rollback.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Preflight incorrectly skips required work | Treat preflight as an execution gate and keep selection coverage independently tested. |
| Timing instrumentation adds overhead | Keep instrumentation lightweight and measure its cost. |
| Shared context couples validators | Share immutable data, not validator ownership rules. |
| Focused selection misses a dependency | Preserve authoritative broad triggers and selection parity fixtures. |
| Cache reuses a stale pass | Defer caching until complete identity is reviewed. |
| Parallelism makes output nondeterministic | Defer parallelism until bounded worker counts and ordered aggregation are specified. |
| Performance thresholds become flaky | Start with baselines and warnings before hard regression budgets. |
| Final verify still causes amend churn | Run branch-readiness proof after commit creation and avoid literal self hashes. |
| New orchestration becomes monolithic | Retain standalone CLIs and clear validator ownership. |
| Preflight correctly blocks broad validation but gives unclear diagnostics | Name the blocker, affected paths when applicable, and the cheapest corrective action or rerun command so contributors do not bypass the gate by manually rerunning broad validation. |

## Open Questions

1. Which workflow should be the first performance pilot?

Resolved direction: final verify for a non-trivial skill or adapter change. It includes repeated broad validation, branch-state preconditions, generated output, and durable evidence, so early measurements should have the strongest signal-to-noise ratio.

2. Should performance thresholds fail validation immediately?

Resolved direction: no. Record baselines and warnings for at least two rollout cycles before promoting any threshold to a failing gate. Premature budgets risk flakiness and teach contributors to retry past performance failures, which weakens the signal when real regressions appear.

3. Should the first slice include caching?

Resolved direction: no. First implement measurement, preflight, selection, and duplicate-work removal. Add caching only after duplicate work is quantified and complete cache identity is specified, because caching work that preflight or selection would eliminate adds stale-pass risk without proving value.

4. Should independent checks run concurrently in the first slice?

Resolved direction: no. Defer concurrency from the first slice even though it may later produce large wall-clock wins. Measurement should first identify whether time is dominated by interpreter startup, duplicate Git inspection, parsing, or truly independent check execution. Concurrency should be a scheduled second-slice proposal after baseline measurements land, with deterministic ordered results and resource independence treated as acceptance conditions.

5. Where should detailed timing evidence live?

Resolved direction: store a bounded summary in change metadata or verify report and detailed timing in a change-local sidecar file. Define the sidecar retention policy before rollout so detailed timing data is kept only where it remains useful and does not accumulate into repository bloat.

6. Should final verify require a clean worktree?

Resolved direction: yes for branch-ready conclusions. Pre-commit verification may run on a dirty worktree, but final branch readiness should identify committed `HEAD` and a clean tracked state.

7. How should correct preflight blockers avoid becoming a friction point?

Resolved direction: preflight failures should name the specific blocker, affected paths when relevant, and the cheapest corrective action or rerun command. A correct but opaque preflight can push contributors to bypass the gate by manually running broad validation, which would recreate the avoidable-cost pattern this proposal is meant to remove.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Optimize execution sequencing before micro-optimizing functions. | The observed repetition was driven mainly by avoidable orchestration and evidence churn. | Start with low-level code tuning. |
| 2026-06-24 | Add cheap preflight before broad validation. | A known tracked-state blocker made an expensive pass unable to succeed. | Always run broad smoke first. |
| 2026-06-24 | Measure before caching or parallelism. | Both techniques introduce correctness and complexity risks. | Add cache and process pools immediately. |
| 2026-06-24 | Separate pre-commit validation from final post-commit verify. | Branch readiness depends on stable tracked state. | Verify only before commit. |
| 2026-06-24 | Avoid literal self-referential commit hashes. | Amending the commit invalidates embedded hash evidence. | Repeatedly amend until the hash stabilizes. |
| 2026-06-24 | Schedule concurrency as a second-slice proposal after baseline measurement. | Parallelism can produce large wins, but it should not multiply startup or Git-inspection overhead or make diagnostics nondeterministic. | Add first-slice concurrency or leave it as an indefinite maybe. |
| 2026-06-24 | Require actionable preflight diagnostics. | Correct but unclear blockers cause contributors to rerun broad validation manually. | Treat preflight blocking as sufficient without corrective guidance. |

## Next Artifacts

- proposal-review
- spec: validation execution performance and preflight contract
- spec-review
- architecture, only if a shared execution service, persistent cache, or new cross-process protocol is introduced
- plan
- plan-review
- test-spec
- implementation
- code-review
- explain-change
- verify
- pr
- follow-up proposal for safe local validation caching after measurement, if still justified
- scheduled follow-up proposal for parallel check execution after baseline measurement and independence proof
- follow-up proposal for performance-budget enforcement after baseline stabilization, if still justified
- follow-up proposal for hosted-CI reuse of local validation selection and timing data, if still justified
- follow-up proposal for a persistent validation worker only if interpreter startup remains a dominant measured cost

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/proposal-review-r1.md`
- Spec: `specs/validation-execution-performance-and-preflight.md`
- Spec review: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/spec-review-r1.md`
- Plan: `docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md`
- Plan review: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/plan-review-r1.md`

## Readiness

Accepted and ready for downstream spec reliance.

## References

- Python `cProfile` and `pstats`: https://docs.python.org/3/library/profile.html
- CPython command-line import timing: https://docs.python.org/3/using/cmdline.html
- Git `diff-index`: https://git-scm.com/docs/git-diff-index
- Git status porcelain format: https://git-scm.com/docs/git-status
- Python `subprocess.run()`: https://docs.python.org/3/library/subprocess.html
- Python `concurrent.futures`: https://docs.python.org/3/library/concurrent.futures.html
