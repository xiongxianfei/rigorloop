# Preflight-First Validation Runtime Optimization

## Status

accepted

## Problem

Do not make validation faster by doing less proof.

Make it faster by running cheap blockers first, selecting the complete relevant check set, avoiding duplicate repository inspection, composing only proven-safe validation work, and running final broad verification once against stable committed state.

The accepted [Preflight-First and Measured Script Execution Optimization](2026-06-24-preflight-first-measured-script-execution-optimization.md) proposal and its June 24 implementation established the first version of that model: selected checks now expose phase metadata, timing, `cache_status: not-applicable`, preflight diagnostics, boundary phase metadata, and a shared immutable preflight context.

That work also exposed the next validation-runtime problem. The shipped instrumentation shows that long validation cycles now have two different cost profiles:

- Developer inner-loop cost: `python scripts/test-select-validation.py` passed 102 tests in about 140 seconds, and selected CI needed `--timeout 180` after the default 60-second check timeout expired on `selector.regression`.
- Boundary and PR-readiness cost: `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` passed 11 checks in about 725 seconds.

Those numbers justify different optimization priorities. The 725-second broad-smoke path is the largest wall-clock cost, but broad-smoke parallelization is correctness-sensitive because child checks need side-effect, temporary-directory, resource-use, and output-order classification before they can run concurrently. The 140-second selector regression path is smaller, but it is already a concrete bottleneck in selected validation and blocks normal local feedback unless the user remembers a timeout override.

This follow-on proposal is therefore not a replacement for the June 24 proposal. It is a post-implementation follow-on focused on:

- producing baselines from the instrumentation that now exists;
- reducing the known `selector.regression` selected-validation bottleneck;
- making selector-routing completeness a deterministic blocker class;
- auditing broad-smoke children before any broad-smoke parallelism is enabled;
- keeping cache and multi-validator in-process composition out of the first slice unless measurement proves they are the next safe target.

## Goals

- Use the June 24 timing and phase instrumentation to produce representative baseline evidence.
- Reduce or explain the `selector.regression` selected-validation timeout without weakening selector coverage.
- Treat missing selector routing for new artifact/path classes as a clear selected-validation blocker, not as a silent broad-smoke fallback.
- Distinguish developer-experience validation cost from boundary or PR-readiness validation cost.
- Audit broad-smoke child checks for side effects, scratch paths, shared resources, and deterministic output before proposing broad-smoke parallel execution.
- Preserve selected-check coverage, broad-smoke coverage, failure detection, exit behavior, diagnostics, and evidence.
- Keep final verify distinct from inner-loop validation and based on actual execution against stable committed state.
- Defer cache enablement, remote/shared caching, and broad multi-validator composition until their input identity and contract boundaries are reviewed.

## Non-goals

- Do not supersede or rewrite the accepted June 24 proposal.
- Do not skip required validation to improve timing.
- Do not weaken selected-check routing or broad-smoke coverage.
- Do not claim a fixed percentage runtime reduction before baselines are reviewed.
- Do not enable broad-smoke parallelism before broad-smoke child checks are classified.
- Do not use cache hits as final closeout evidence.
- Do not introduce remote/shared caching in this proposal.
- Do not rewrite multiple validators into a single in-process runner in the first slice.
- Do not change validation output semantics merely to reduce runtime.
- Do not claim verify, branch readiness, PR readiness, or hosted CI success from inner-loop speedups alone.

## Vision fit

fits the current vision

RigorLoop's value depends on trustworthy, durable validation evidence. Slow validation creates pressure to skip checks, while repeated broad validation burns time without adding evidence.

This follow-on supports the current vision by using the evidence surface from the June 24 implementation to improve validation cost without hiding failures or weakening proof. It would conflict with the vision if timing improves because required evidence disappears, selector routing becomes less explainable, broad validation is skipped under an authoritative trigger, or final verify relies on cache-only or stale pre-commit evidence.

## Context

This proposal is a follow-on to the accepted June 24 proposal, not an amendment or supersession.

The June 24 work already shipped the first-slice preflight and measurement foundation. Its plan records that selector/CI timing, phase explanation, preflight diagnostics, boundary phase metadata, and shared immutable preflight context were implemented. Its verification evidence records that a selected-CI run timed out on `selector.regression` at the default 60-second timeout, then passed with `--timeout 180`; the performance baseline identifies `selector.regression` as the dominant selected-CI check, taking about 119.50 seconds of about 129.36 seconds focused selected-check time.

The current code also matters for scope. `scripts/validation_selection.py` already has `RepositoryPreflightContext` with `tracked_paths: frozenset[str]` and `unmerged_paths: tuple[str, ...]`, and selection results expose changed paths as strings. Any future shared validation context should build from that shipped shape or explicitly justify a type or contract change.

The largest cited runtime is broad-smoke at about 725 seconds. This proposal does not ignore that number; it sequences the work so broad-smoke speedups begin with child-check classification rather than immediate concurrency. That keeps the first broad-smoke step reviewable and avoids turning an expensive but deterministic proof into a faster but flaky one.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Speed up long-running validation scripts | in scope | Goals, Recommended Direction |
| Understand whether parallel test execution helps | in scope | Broad-Smoke Audit |
| Avoid unnecessary execution | in scope | Recommended Direction |
| Preserve correctness | in scope | Non-goals, Vision fit |
| Improve broad-smoke runtime | in scope | Context, Broad-Smoke Audit |
| Use caching if safe | deferred follow-up | Scope Budget, Deferred Boundaries |
| Optimize individual Python code | in scope | Selector Regression Focus |
| Keep verification trustworthy | in scope | Goals, Non-goals |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Post-#109 baseline collection | core to this proposal | Instrumentation now exists; the next step is to use it. |
| `selector.regression` runtime analysis | core to this proposal | It is the first measured selected-validation bottleneck. |
| Selector-routing completeness blocker | core to this proposal | Missing routing should block deterministically before broad-smoke. |
| Broad-smoke child classification | core to this proposal | It is the prerequisite for safe broad-smoke parallelism. |
| Broad-smoke parallel execution | separate implementation slice | The 725-second path is large, but child safety must be proven first. |
| Shared validation context beyond preflight | first-slice candidate | Add only if baseline evidence shows repeated discovery remains material. |
| In-process validator composition | separate implementation slice | Multi-validator composition needs readiness analysis to avoid a broad refactor. |
| Local safe-result cache | separate proposal | Complete identity and final-closeout boundaries need separate review. |
| Remote/shared cache | out of scope | Cross-machine trust and invalidation are larger concerns. |
| Persistent validation worker | deferable follow-up | Only justified if startup/import remains dominant after lower-risk work. |

## Options Considered

### Option 1: Start broad-smoke parallelization immediately

Broad-smoke is the largest cited wall-clock cost, so this option appears attractive. It is rejected as the first move because broad-smoke children have not yet been classified for side effects, scratch paths, shared outputs, resource contention, or deterministic result aggregation.

### Option 2: Optimize only `selector.regression`

This targets the known selected-CI timeout and should improve developer feedback. It is insufficient alone because it leaves the 725-second broad-smoke path unexamined and does not address future missing selector-routing blockers.

### Option 3: Add caching immediately

Caching could help repeated identical runs, but it requires complete input identity and should not become final proof. It is deferred because the current first need is to use existing timing evidence and reduce or explain actual measured bottlenecks.

### Option 4: Compose several validators in process

This could reduce Python startup, imports, Git status calls, YAML parsing, and Markdown parsing. It is risky as a first slice because change metadata, review artifacts, artifact lifecycle, and skill/selector validation each have their own CLI contracts and failure-output expectations.

### Option 5: Follow-on baseline plus selector focus plus broad-smoke audit

This option uses the June 24 instrumentation, attacks the first measured selected-validation bottleneck, makes missing selector routes deterministic, and prepares broad-smoke parallelism with explicit safety evidence.

This is the recommended direction.

## Recommended Direction

Use this proposal as a follow-on to the June 24 accepted work.

First, collect and publish a post-#109 baseline using the timing/phase surfaces that now exist. The baseline should distinguish developer inner-loop validation, boundary validation, and final verify. It should also identify whether `selector.regression`, broad-smoke children, repeated Git inspection, subprocess startup, or parsing dominates each scenario.

Second, make `selector.regression` the first concrete selected-validation optimization target. The goal is not to reduce coverage; it is to identify whether runtime is caused by expensive fixtures, repeated process startup, avoidable filesystem scans, overly broad assertions, or unavoidable test execution. If no safe reduction is found, the result should still produce a documented profile and timeout recommendation.

Third, strengthen selector-routing completeness as an explicit blocker class. New lifecycle evidence classes, validator fixture classes, guide artifacts, generated output classes, and release evidence classes should not silently fall through to broad-smoke as a substitute for deterministic selected routing.

Fourth, audit broad-smoke children before enabling broad-smoke parallelism. The audit should classify each child check by side effects, temporary paths, shared outputs, CPU/I/O weight, nested parallelism, and output-order needs. A later implementation slice can enable broad-smoke parallelism only for checks with recorded safety evidence.

Fifth, keep multi-validator in-process composition constrained. This proposal should not start by composing change metadata, review artifacts, artifact lifecycle, and selector validation together. The downstream spec or plan may include a readiness assessment for those validators and may allow one proof-of-concept wrapper only after it proves standalone CLI behavior, exit codes, and diagnostics remain compatible.

## Expected Behavior Changes

Local selected validation should report whether `selector.regression` is the dominant check and should no longer require guesswork about why the default selected-CI timeout is insufficient.

Changed paths without deterministic selector routing should produce a clear selected-validation blocker before broad-smoke. Diagnostic broad-smoke can still run when explicitly requested, but it should not hide the routing blocker.

Broad-smoke should remain sequential until child checks have safety classifications. After classification, a later slice may enable bounded parallelism for eligible broad-smoke children with deterministic result aggregation.

Final verify should remain a distinct branch-readiness step using actual execution evidence against stable committed state.

## Architecture Impact

| Surface | Expected impact |
| --- | --- |
| `scripts/validation_selection.py` | Selector-routing completeness and selected-check explanation remain the main behavior surface. |
| `scripts/test-select-validation.py` | First measured optimization target; coverage should be profiled before any rewrite. |
| `scripts/ci.sh` | Broad-smoke child audit may inform later bounded parallel execution; no first-slice broad-smoke parallelism. |
| Change-local performance evidence | Stores post-#109 baselines, selector profile, and broad-smoke child classification. |
| Shared validation context | Existing `RepositoryPreflightContext` remains the starting point; broader context needs separate readiness proof. |
| Validator CLIs | Standalone behavior remains required; composition is not a first-slice commitment. |

No architecture artifact is expected for baseline collection, selector profiling, routing-blocker refinement, or broad-smoke child classification. Architecture should be revisited if a later slice introduces a persistent worker, shared cache, remote cache, new cross-process protocol, or broad validator composition framework.

## Testing and Verification Strategy

The downstream spec should keep the proposal-level proof simple and move detailed acceptance criteria into requirement/test IDs.

At proposal level, the proof should show:

- post-#109 baseline evidence exists for selected validation, broad-smoke, and final verify;
- `selector.regression` has a profile or runtime breakdown before it is optimized;
- any selector-regression optimization preserves selected-check coverage and failure diagnostics;
- missing selector routing blocks selected validation clearly;
- broad-smoke child classification exists before broad-smoke parallelism is proposed;
- final verify still requires actual execution evidence and stable committed state;
- cache status remains informational only and is not final proof.

Behavior-preservation evidence should remain part of the downstream spec or plan, but the proposal does not need to prescribe every row. The key preservation surfaces are selected-check identity, broad-smoke coverage, exit codes, failure output, branch-readiness ownership, selector blockers, timing evidence, and standalone CLIs.

Performance evidence should record measured baselines first. Any percentage target should be named only after the baseline is reviewed in the downstream spec or plan.

## Broad-Smoke Audit

Broad-smoke is the largest cited cost, so this proposal explicitly starts the path toward optimizing it.

The first broad-smoke work should be a classification artifact, not immediate concurrency. For each broad-smoke child, record:

- command and check ID;
- whether it mutates tracked or generated files;
- temporary directory behavior;
- shared output paths;
- external resource assumptions;
- CPU/I/O intensity;
- nested parallelism risk;
- whether failure output can be aggregated deterministically.

Only checks classified as independent and side-effect-free should become candidates for later bounded broad-smoke parallel execution.

## Selector Regression Focus

The first concrete selected-validation target is `selector.regression`, because current evidence shows it dominates focused selected-CI runtime and can exceed the wrapper's default 60-second timeout.

The first optimization step should profile the suite before changing it. Likely investigation areas include repeated fixture setup, subprocess use, broad static scans, filesystem traversal, slow shell wrapper assertions, and tests that can share immutable setup without sharing mutable state.

If profiling shows no safe reduction, the accepted output should be a clear baseline, a recommended timeout or split strategy, and a follow-up decision. Runtime should not be improved by deleting selector coverage.

## Deferred Boundaries

Caching remains out of scope except for preserving `cache_status` semantics already introduced by the June 24 work. A future cache proposal should own cache identity, cache-hit evidence, TTL, malformed-cache behavior, and final-verify exclusion.

Multi-validator composition remains out of scope for the first slice. Before composing validators in one Python process, the downstream plan should assess each candidate validator's current CLI shape, library entry point availability, mutable global state, failure-output contract, and standalone compatibility tests. If composition remains justified, start with one proof-of-concept validator or wrapper rather than four validators at once.

## Rollout and Rollback

Rollout:

1. Record post-#109 baseline evidence from existing timing/phase output.
2. Profile `selector.regression` and identify the largest contributors.
3. Implement only selector-regression improvements that preserve coverage and diagnostics.
4. Add or refine deterministic missing-route blocker behavior for newly classified path/evidence classes.
5. Record broad-smoke child safety classifications.
6. Decide whether a separate broad-smoke parallelization slice is ready.
7. Decide whether shared context, validator composition, or caching has enough measured value to justify a separate artifact.

Rollback:

- Revert selector-regression optimizations if they remove coverage or obscure failures.
- Keep baseline/profile evidence even if optimization code is reverted.
- Keep missing-route blockers visible unless they incorrectly block classified paths.
- Keep broad-smoke sequential if classification is incomplete or later parallel execution proves flaky.
- Do not remove final actual-run verify or treat cache status as proof.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The proposal optimizes the smaller 140-second cost while 725-second broad-smoke remains slow | Treat `selector.regression` as the selected-validation target and make broad-smoke child classification the required first step toward broad-smoke parallelism. |
| Selector regression gets faster by losing coverage | Require selected-check parity and failure-fixture preservation before accepting runtime improvement. |
| Missing-route blockers become noisy | Keep blocker diagnostics path-specific and require routing registration only for known artifact/path classes. |
| Broad-smoke parallelism creates flakiness | Do not enable it in this slice; classify children first. |
| Multi-validator composition balloons | Defer composition and require readiness assessment plus one proof-of-concept before broad composition. |
| Cache design distracts from measured bottlenecks | Keep cache identity and reuse policy in a future cache proposal. |
| Runtime varies by machine | Compare baselines by scenario and profile shape, not one absolute timing number. |
| Final verify becomes stale or cache-only | Preserve final actual-run verification against stable committed state. |

## Open Questions

1. What is the first pilot?

   Candidate direction: post-#109 baseline plus `selector.regression` profiling, because instrumentation exists and current evidence already identifies this check as the selected-CI bottleneck.

2. When should a numeric runtime target be set?

   Candidate direction: after the post-#109 baseline is reviewed in the downstream spec or plan. This proposal should not anchor on a percentage before measurement.

3. Should broad-smoke become parallel in the first slice?

   Candidate direction: no. The first slice should classify broad-smoke children. Parallel execution belongs in a later slice after safety and output-order evidence exists.

4. Should caching be enabled in the first slice?

   Candidate direction: no. The first slice should use existing `cache_status` metadata only as a boundary marker and leave cache identity to a future cache proposal.

5. Should validator composition be included in the first slice?

   Candidate direction: no broad composition. A downstream plan may include readiness assessment and one proof-of-concept only if baseline evidence shows startup/import or repeated parsing remains material.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-26 | Treat this as a follow-on to June 24, not an amendment or supersession. | The June 24 proposal is accepted and already has downstream artifacts and implementation evidence. | Ask proposal-review to decide the document type. |
| 2026-06-26 | Use post-#109 instrumentation as the starting point. | Timing, phase metadata, preflight diagnostics, and `cache_status` already exist. | Restart the proposal as if no baseline tooling exists. |
| 2026-06-26 | Make `selector.regression` the first selected-validation target. | It is the measured focused-check bottleneck and exceeded the default selected-CI timeout. | Start with unmeasured low-level optimization. |
| 2026-06-26 | Start broad-smoke optimization with child classification. | Broad-smoke is the largest cost, but parallelism needs safety evidence first. | Turn broad-smoke parallel immediately. |
| 2026-06-26 | Remove fixed percentage runtime targets from the proposal. | Targets should follow baseline evidence. | Commit to a 30% target before measurement. |
| 2026-06-26 | Defer cache identity and broad validator composition. | Both can create correctness or scope risk without measured need and contract analysis. | Include cache and four-validator composition in the first slice. |

## Next Artifacts

- proposal-review
- spec amendment or new spec for post-#109 validation runtime follow-through
- spec-review
- plan
- plan-review
- test-spec
- implementation
- code-review
- explain-change
- verify
- pr
- separate follow-up proposal for broad-smoke parallel execution after child classification, if justified
- separate follow-up proposal for local safe-result cache enforcement after complete identity proof, if justified
- separate follow-up proposal for multi-validator composition or a persistent validation worker, if profiling justifies it

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md`
- Proposal review R2: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md`
- Spec: `specs/validation-runtime-follow-through.md`

## Readiness

Approved for specification.

The downstream spec or plan should normalize the open-question candidate answers as decisions, replace `post-#109` shorthand with durable artifact references, define selector-regression preservation proof, and keep broad-smoke parallelism, caching, and broad validator composition out of the first implementation slice unless separately approved.
