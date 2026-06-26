# Learn Session: Zero Runtime Improvement Root Cause

## Frame

- Date: 2026-06-26
- Status: session-recorded; no topic update routed
- Trigger: maintainer explicitly invoked `learn` after PR #114 and asked why the improvement was 0% and what the root reason was.
- Trigger type: explicit maintainer request / contributor observation after final verification and PR handoff.
- Scope: root-cause analysis for why `2026-06-26-preflight-first-validation-runtime-optimization` produced 0% validated feature-caused runtime improvement.
- Session path: `docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`

## Evidence Reviewed

- Accepted proposal: `docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md`
- Approved spec: `specs/validation-runtime-follow-through.md`
- Active test spec: `specs/validation-runtime-follow-through.test.md`
- M1 baseline: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml`
- M1 selector profile: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
- M2 preservation proof: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md`
- M3 broad-smoke classification: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md`
- Final holistic code review: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r4.md`
- Final verify report: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/verify-report.md`
- Prior learn session: `docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`
- Prior learn session: `docs/learn/sessions/2026-06-24-verify-repetition-cost.md`

## Exclusions

- This session does not change `scripts/ci.sh`, selector logic, validator implementation, workflow policy, or performance budgets.
- This session does not claim hosted CI status or PR merge readiness.
- This session does not open a new optimization proposal or mark broad-smoke parallelism, caching, or validator composition as approved.
- This session does not add topic guidance because final routing has not been confirmed.

## Prior Learnings Reviewed

- `2026-06-26-validation-runtime-speed-best-practices` already captured broad validation speed practices, check-level parallelism guidance, and broad-smoke parallelism as a candidate follow-up.
- `2026-06-24-verify-repetition-cost` already captured preflight-before-expensive-verify cost lessons.

## Observations

### O1 - The slice had no runtime-speed actuator

Evidence:

- The proposal, spec, and plan explicitly kept broad-smoke parallel execution, cache reuse, and broad validator composition out of scope.
- `code-review-r4` says the code changes were limited to selector evidence-class routing, missing-route diagnostics, and selector regression tests.
- `code-review-r4` also says the branch did not enable broad-smoke parallel execution, local or remote cache reuse, broad in-process validator composition, or final readiness claims from inner-loop validation.
- `broad-smoke-child-classification.md` records `Execution behavior changed: no`, `Broad-smoke parallel execution enabled: no`, `Cache behavior changed: no`, and `Validator composition changed: no`.

Observation:

The root reason the validated feature-caused improvement is 0% is that the first slice did not implement any mechanism that could reduce wall-clock runtime. It implemented measurement, evidence routing, preservation tests, deterministic blockers, and broad-smoke classification. Those are prerequisites for safe speed work, not speed work itself.

### O2 - The only first-slice optimization target ended in a no-safe-reduction decision

Evidence:

- `selector-regression-profile.md` records `Safe reduction identified: no`.
- `selector-preservation.md` records `Safe reduction identified: no` and says M2 did not isolate a behavior-preserving runtime reduction.
- The profile limitations say the current scripts did not emit per-test timing, Git inspection counts, subprocess counts, or filesystem bytes inspected.
- Final verify direct selector evidence was `108 tests passed in 150.73s`, `/usr/bin/time` real `142.93s`.
- M1 direct selector baseline was `/usr/bin/time` real `135.04s`.

Observation:

The selected-validation path did not improve because the work stopped correctly at "profile and preserve proof" once no safe, isolated optimization was found. The direct selector suite was slightly slower in final verify than the M1 baseline:

```text
baseline real: 135.04s
final real:    142.93s
raw delta:     -5.8% improvement, meaning about 5.8% slower
```

That raw delta should not be overinterpreted because the runs were local, single-sample, and changed test count from 103 to 108. The important root-cause fact is that no selector runtime optimization was implemented.

### O3 - The broad-smoke raw improvement was not attributable to the feature

Evidence:

- The proposal cited prior broad-smoke evidence of about `725s`.
- Final verify broad-smoke passed 11 checks with `/usr/bin/time` real `351.49s`.
- `broad-smoke-child-classification.md` proves broad-smoke execution behavior was unchanged and sequential.
- The spec R18-R19 required classification only and explicitly kept broad-smoke parallel execution disabled.

Observation:

The raw broad-smoke comparison looks like about 51.5% faster:

```text
(725s - 351.49s) / 725s = 51.5%
```

But this cannot be credited to the feature because the feature did not change broad-smoke execution. The difference is measurement variability, environment/load differences, changed repository state, or prior-run conditions. The attributable broad-smoke runtime improvement is therefore 0%.

### O4 - The word "optimization" created an expectation mismatch

Evidence:

- The proposal title uses "Validation Runtime Optimization".
- The approved scope included measurement, selector profile, missing-route blockers, broad-smoke child classification, and deferral of broad-smoke parallelism, caching, and composition.
- The spec performance expectation says the slice measures before setting numeric targets and should reduce or explain the selected bottleneck.
- The final result chose the "explain" branch: no safe selector reduction, broad-smoke classified only, and future speed mechanisms deferred.

Observation:

The work was correctly scoped as a safe optimization pipeline, but the title and goal language can imply immediate runtime reduction. The implemented slice produced optimization readiness and safety evidence, not a measurable runtime speedup.

## Root Cause

The root cause of 0% validated feature-caused improvement is scope-mechanism mismatch:

```text
The change was called a runtime optimization, but the accepted first slice
implemented measurement, proof preservation, routing blockers, and broad-smoke
classification. It intentionally deferred the mechanisms that could reduce
runtime: selector implementation optimization, broad-smoke parallelism, cache
reuse, and validator composition.
```

This was not a failed optimization implementation. It was a successful prerequisite slice whose measurable output was safety and evidence, not speed.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record only | maintainer trigger and PR #114 evidence | The evidence directly explains the 0% result; no artifact change is needed to state the fact. |
| O2 | process-follow-up | pending confirmation | possible profiling follow-up for per-test timing, subprocess counts, Git inspection counts, and filesystem scan counts | not confirmed | A future selector optimization needs better bottleneck attribution, but implementation belongs in a plan/proposal, not in learn. |
| O3 | observation | observation | session record only | verify report and broad-smoke classification evidence | The raw broad-smoke speedup is non-attributable because execution behavior did not change. |
| O4 | direction | pending confirmation | possible proposal/spec wording pattern: distinguish "optimization-readiness" slices from "runtime-reduction" slices | not confirmed | Naming/success-metric guidance could prevent expectation mismatch, but changing proposal conventions needs an owning artifact or maintainer confirmation. |

Contributor confirmation status: the maintainer confirmed the trigger and asked for root-cause learning. Routing process follow-ups or proposal guidance is not confirmed in this session.

## Route

- Session record created.
- No topic update made.
- No proposal, spec, plan, workflow, CI, selector, or validator change made.

## Candidate Follow-Ups

Pending contributor confirmation:

1. Proposal or plan a true runtime-reduction slice with at least one approved speed actuator:
   - selector implementation optimization with per-test timing evidence;
   - broad-smoke parallel execution after child safety proof;
   - local cache reuse after complete identity proof;
   - one-validator composition proof of concept if startup/import/parsing is measured as material.
2. Add profiling telemetry before another selector optimization attempt:
   - per-test or per-class timing;
   - subprocess counts;
   - Git inspection counts;
   - filesystem scan counts.
3. In future proposals, separate success metrics into:
   - evidence/readiness outcomes;
   - actual wall-clock reduction outcomes;
   - non-attributable raw timing observations.

## Practical Answer

The improvement is 0% because the PR did not ship a runtime reducer. It shipped the safe preconditions for future runtime reduction.

Concrete root reasons:

1. `selector.regression` was profiled, but no behavior-preserving optimization was found.
2. Broad-smoke was classified, but not parallelized.
3. Cache reuse was explicitly deferred.
4. Broad validator composition was explicitly deferred.
5. The code diff added routing, diagnostics, and tests; it did not change the slow execution paths.

## Validation

- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-guide-system.py`: passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`: passed; validated 0 artifact files.
- `git diff --check -- docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`: passed.
