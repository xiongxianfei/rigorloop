# Learn Session: Validation Runtime Speed Best Practices

## Frame

- Date: 2026-06-26
- Status: session-recorded; no topic update routed
- Trigger: maintainer explicitly invoked `learn` and asked why scripts take too long, what best practices would speed them up, and whether running test cases in parallel would help.
- Trigger type: explicit maintainer request / contributor observation after final verification runtime pain.
- Scope: validation runtime practices for repository scripts, especially final verify, selected CI, broad smoke, and large unittest-style suites.
- Session path: `docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`

## Evidence Reviewed

- Current verify report for `2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`:
  - PR-scoped CI blocked before selected checks because two changed paths lacked deterministic selector routing.
  - Direct proof for the bounded spec-read fixture passed.
  - `python scripts/test-select-validation.py` passed 102 tests in about 140 seconds.
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` passed 11 checks in 725 seconds.
  - direct validator suites passed, including 241 skill tests, 96 review-artifact tests, 142 artifact-lifecycle tests, and 43 change-metadata tests.
- `scripts/ci.sh`:
  - selected modes accept `--jobs` and default to CPU count minus one;
  - selected checks marked parallel-safe are run through a `ThreadPoolExecutor`;
  - broad-smoke uses sequential `run_check` calls.
- `scripts/validation_selection.py`:
  - check catalog entries carry a `parallel_safe` flag;
  - new changed paths without deterministic classification block selected CI.
- Prior learn session `2026-05-22-change-local-selector-routing`:
  - repeated selector blockers happen when new evidence classes are introduced without selector routing.
- Prior learn topic `script-output-optimization`:
  - optimize output layers while preserving pass/fail status, counts, durations, failure reasons, rerun guidance, and exit behavior.
- Prior learn session `2026-06-24-verify-repetition-cost`:
  - expensive validation should not run repeatedly while cheap branch-state or artifact-state preconditions are already false.

## Exclusions

- This session does not change `scripts/ci.sh`, validator code, selector routing, workflow policy, or test framework dependencies.
- This session does not claim branch readiness, PR readiness, hosted CI status, or verify closeout.
- This session does not decide to add a new test dependency such as pytest or pytest-xdist.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-22-change-local-selector-routing.md`
- `docs/learn/topics/script-output-optimization.md`
- `docs/learn/sessions/2026-06-24-verify-repetition-cost.md`

## Observations

### O1 - The fastest run is the one skipped by a cheap failing preflight

The current final verify ran substantial direct validation and broad smoke, but PR-scoped CI still blocked before selected checks because selector routing was incomplete. Prior learn evidence shows the same pattern: expensive tests can pass while a cheaper branch-readiness precondition is already false.

Best practice: run cheap gates first:

1. clean worktree / tracked authoritative artifacts;
2. selector classification for the full changed-path set;
3. plan/index and review closeout state;
4. only then broad smoke or expensive generated-output checks.

### O2 - Parallelism helps most at the selected-check level, not blindly inside every test file

`scripts/ci.sh` already has the right shape for selected checks: each catalog check can declare `parallel_safe`, selected modes accept `--jobs`, and parallel-safe chunks run concurrently. That is safer than blindly parallelizing every unittest method because check-level isolation is easier to reason about.

Best practice: prefer check-level parallelism first. Promote a check to `parallel_safe` only when it:

- writes only to unique temporary directories;
- does not mutate tracked files;
- does not rely on global process environment that sibling checks can change;
- does not contend for the same cache path, generated output directory, port, or release artifact location;
- has deterministic output and exit behavior when run concurrently.

### O3 - Broad smoke is still serial and is a real optimization candidate

The current broad-smoke run took 725 seconds for 11 checks. `scripts/ci.sh` broad-smoke still calls `run_check` sequentially, while selected CI has parallel-safe chunking. That makes broad-smoke a likely place to recover wall-clock time, provided checks are classified by safety and resource use.

Best practice: if broad-smoke parallelization is pursued, reuse the selected-check safety model instead of backgrounding arbitrary commands. Keep output captured per check and print successful output only under `--verbose`.

### O4 - Some individual suites may be parallelizable, but only after isolation audit

The unittest fixture suites create many temp directories and subprocesses, which may make some cases parallelizable. They also inspect repository files, spawn Git workspaces, build generated outputs, and use shared scripts. Without an isolation audit, method-level parallelism can create nondeterminism that costs more than it saves.

Best practice: before parallelizing inside a suite, measure per-test or per-class duration, then split only independent groups. Prefer coarse class/module sharding over method-level concurrency unless the test harness proves temp paths, cache paths, environment variables, and generated outputs are isolated.

### O5 - Output compaction and runtime optimization are related but separate

Long scripts are expensive in two ways: runtime and transcript cost. Existing topic guidance already says to compact output without hiding failure evidence. That does not reduce wall-clock time by itself, but it makes long runs easier to monitor and prevents context loss.

Best practice: keep compact success summaries, but optimize wall-clock time through selector precision, caching, sharding, and safe parallel execution.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | process-follow-up | pending confirmation | possible verify/CI preflight improvement | not confirmed | There is repeated evidence that expensive runs occur after cheap blockers, but changing verify or CI sequencing belongs in an owning artifact. |
| O2 | observation | observation | session record only | maintainer question and current `ci.sh` evidence | Check-level parallelism already exists; this session explains how to use and extend it safely. |
| O3 | process-follow-up | pending confirmation | possible CI-maintenance proposal or plan item for broad-smoke parallelism | not confirmed | Broad-smoke runtime is substantial and implementation belongs in CI scripts/tests, not in learn. |
| O4 | direction | pending confirmation | possible research/proposal for unittest sharding | not confirmed | Method-level parallelism may help, but needs measurement and isolation audit before becoming a rule. |
| O5 | observation | observation | existing script-output topic remains relevant | prior topic guidance | Existing guidance already covers transcript compaction; no new topic entry is needed. |

Contributor confirmation status: explicit trigger confirmed. Routing to topic updates, CI-maintenance, workflow guidance, or implementation is not confirmed in this session.

## Route

- Session record created.
- No topic update made because the core practices are either already captured in prior topics or require an action-owning artifact before becoming policy.
- No CI, selector, workflow, or test harness change made by this session.

## Practical Answer

Recommended order for speeding up scripts:

1. Add a cheap preflight path that fails before broad validation when selector classification, branch state, review closeout, or plan/index state is already invalid.
2. Fix selector coverage so changed paths route to the smallest sufficient check set; missing selector routes cause costly reruns and block PR-scoped CI.
3. Use `bash scripts/ci.sh --mode explicit` or `--mode pr` with selected checks for normal development; reserve broad smoke for final gates or when policy triggers it.
4. Use existing `--jobs` check-level parallelism for selected CI. This is safer than method-level parallelism.
5. Profile before parallelizing individual suites. Shard slow suites by class or module only after proving temp directories, caches, generated outputs, environment variables, and subprocess state are isolated.
6. Consider broad-smoke parallelization as a CI-maintenance change, reusing the check catalog's `parallel_safe` model and preserving per-check output capture.
7. Keep compact success output and detailed failure output; transcript reduction is not a substitute for runtime reduction.

Would running test cases in parallel help?

Yes, but the safest first target is parallelizing independent checks, not every test case. The repo already does this for selected CI through `--jobs` and `parallel_safe` catalog entries. Parallelizing broad-smoke checks would likely help wall-clock time because the current broad-smoke path is serial and recently took 725 seconds. Parallelizing individual unittest methods might help some suites, but it should follow measurement and an isolation audit because fixture suites use subprocesses, Git workspaces, temp directories, generated outputs, and shared environment.

## Candidate Follow-Ups

Pending contributor confirmation:

1. CI-maintenance: add selector routes for the current `VERIFY-F1` blocker before rerunning final verify.
2. CI-maintenance or proposal: add a cheap preflight mode for full changed-path selector classification before broad smoke.
3. CI-maintenance or proposal: parallelize broad-smoke checks using the existing `parallel_safe` catalog model.
4. Research/profiling: add timing output or a benchmark script for the slowest validator suites, then decide whether class/module sharding is worthwhile.

## Validation

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`: passed; no lifecycle-managed artifact files were selected.
- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-guide-system.py`: passed.
- `git diff --check -- docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`: passed.
