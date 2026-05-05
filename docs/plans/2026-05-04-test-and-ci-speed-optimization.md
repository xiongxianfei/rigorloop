# Test and CI Speed Optimization Implementation Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-04
- Last updated: 2026-05-05
- Related issue or PR: none yet
- Supersedes: none
- selected_workflow_contract: refactored
- broad_smoke_required: true
- broad_smoke_reason: This initiative changes `scripts/ci.sh`, the repository-owned validation wrapper. Milestone validation should use focused selector-selected proof first, but final verification must include direct broad smoke so the legacy broad-smoke path, wrapper command parsing, and selected-check behavior are all exercised before PR readiness.

## Purpose / Big Picture

Implement bounded parallel execution for selected validation checks in `scripts/ci.sh`.

The implementation should reduce local validation wall-clock time while preserving the selector/wrapper boundary: `scripts/select-validation.py` decides which checks are required, and `scripts/ci.sh` decides how to execute the selected checks. The first slice must be deliberately narrow: parallelize only reviewed safe checks, keep non-allowlisted checks serial, keep logs deterministic, and defer matrix execution, caching, distributed execution, and sandboxing.

## Source Artifacts

- Proposal: [Test and CI Speed Optimization](../proposals/2026-05-04-test-and-ci-speed-optimization.md), accepted.
- Spec: [Test and CI Speed Optimization](../../specs/test-and-ci-speed-optimization.md), approved.
- Spec-review outcome: approved. The one minor finding about `--fail-fast` optionality was resolved by changing `R7` to require `--fail-fast` and by making queued-check cancellation behavior testable.
- Architecture: no update required by spec-review. The approved work preserves the existing selector, check catalog, wrapper, and hosted CI boundaries recorded in [system architecture](../architecture/system/architecture.md). If implementation introduces a new wrapper helper module, changes hosted CI topology, or changes selector ownership beyond catalog metadata, stop and update architecture before implementation continues.
- Test spec: [Test and CI Speed Optimization Test Spec](../../specs/test-and-ci-speed-optimization.test.md), active.
- Project map: `docs/project-map.md` is absent. No-map rationale: this plan does not rely on repository-map claims for module ownership or runtime flow. Orientation comes from the approved proposal, approved spec, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/test-layering-and-change-scoped-validation.md`, current system architecture, and direct reads of `scripts/ci.sh`, `scripts/validation_selection.py`, and `scripts/test-select-validation.py`.

## Context and Orientation

- `scripts/validation_selection.py` owns the check catalog and path selection. `CheckCatalogEntry` currently carries `id`, `command_template`, and `category`; this initiative adds reviewed parallel-safety metadata there.
- `scripts/ci.sh` currently parses wrapper mode arguments, calls the selector for `local`, `explicit`, `pr`, `main`, and `release`, validates selected commands against the catalog, and runs selected commands serially through an embedded Python block. It also preserves non-recursive `--mode broad-smoke`.
- `scripts/test-select-validation.py` already tests selector behavior and CI-wrapper behavior. It has `RIGORLOOP_SELECTOR_FIXTURE`, temporary workspace helpers, and existing tests for selector blocking, malformed JSON, command mismatch, unavailable commands, direct broad smoke, and broad-smoke delegation.
- Tests for parallel behavior should use temporary workspaces with fake `scripts/test-*.py` or validator files that match catalog commands. That avoids adding test-only commands to the real catalog and avoids relying only on wall-clock timing.
- `docs/workflows.md` tells contributors to use selector-selected proof first and `bash scripts/ci.sh --mode explicit --path ...` as the wrapper command. It should document the new wrapper flags after implementation.
- `.github/workflows/ci.yml` is expected to remain unchanged in this slice. If touched, it must stay a thin caller of repo-owned scripts and must not add matrix fan-out.
- No new runtime dependency is expected. Python standard-library subprocess and scheduling tools are enough.
- Generated `.codex/skills/` and `dist/adapters/` output are not authored surfaces for this change.
- M1 aligned-surface audit: `docs/workflows.md` remains intentionally unchanged until M4 because contributor guidance should describe the complete behavior after scheduler and reporting work exists. `.github/workflows/ci.yml` remains intentionally unchanged because hosted CI topology, matrix fan-out, and workflow routing are out of scope for this first slice. `docs/architecture/system/architecture.md` remains intentionally unchanged because M1 preserves the existing selector, catalog, wrapper, and hosted CI boundaries.

## Non-Goals

- Do not change which checks the selector selects.
- Do not weaken required validation or skip selected checks for speed.
- Do not run every selected check in parallel by default.
- Do not add GitHub Actions matrix fan-out in this slice.
- Do not add persistent result caching, dependency caching, input hashing, distributed execution, or per-check sandboxing.
- Do not add dynamic priority scheduling. Stable-order FIFO with a concurrency cap is enough.
- Do not move selector path classification or check selection into workflow YAML.
- Do not change generated-output sync behavior.
- Do not add new external dependencies.

## Requirements Covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`, `R16`, `R16a` | Preserve selector-owned check selection and existing wrapper modes in `scripts/ci.sh` and wrapper regression tests. |
| `R2`-`R2d` | Add `--jobs`, positive-integer validation, CPU-minus-one default, `--jobs 1`, and concurrency capping in `scripts/ci.sh`. |
| `R3`-`R3e` | Add `--timeout`, 60-second default, leaf runtime measurement, timeout termination, and timeout reporting in `scripts/ci.sh`. |
| `R4`-`R5` | Add parallel-safe metadata to the check catalog in `scripts/validation_selection.py` and tests for the initial six reviewed regression IDs. |
| `R6`-`R7c` | Implement default run-to-completion and required `--fail-fast` queued-check cancellation in the selected-check runner. |
| `R8`-`R10b` | Capture per-check stdout/stderr, prevent interleaved logs, decode at reporting, provide stable summary output, failed logs, and `--verbose` successful logs. |
| `R11`-`R12` | Distinguish passed, exited, killed by signal, timed out, unavailable, and not-started statuses and preserve nonzero wrapper exits. |
| `R13`-`R14` | Preserve unknown check ID and unavailable command failures with check ID and command evidence. |
| `R15`-`R15a` | Preserve non-recursive broad-smoke behavior and apply timeout behavior to selected leaf checks rather than a recursive outer special case. |
| `R17`-`R19` | Keep hosted CI thin, do not add matrix, caching, distributed execution, or sandboxing. |
| `R20` | Keep per-check metadata in the catalog, selector rules in selector code, wrapper defaults in `scripts/ci.sh`, invocation overrides as CLI flags, fixtures in environment variables, and hosted environment details in workflow YAML. |

## Immediate Test-Spec Handoff

The active test spec is `specs/test-and-ci-speed-optimization.test.md`.

It maps every `MUST` in `specs/test-and-ci-speed-optimization.md` to concrete tests or justified manual verification. It explicitly covers:

- invalid `--jobs` and `--timeout` values failing before selector-selected commands run;
- `--jobs 1` sequential execution;
- default job count calculation with a single-CPU simulation if feasible;
- initial parallel-safe allowlist metadata for the six regression check IDs;
- allowlisted checks running concurrently while non-allowlisted checks run alone;
- stable summary and stable failed-output ordering;
- stdout/stderr separation and non-UTF-8 decode handling;
- run-to-completion by default;
- `--fail-fast` not starting queued checks after failure while preserving started-check final status;
- timeout, signal kill, nonzero exit, unknown check ID, and unavailable command reporting;
- broad-smoke non-recursion;
- workflow YAML remaining free of matrix fan-out and duplicated selector rules.

Implementation milestones are test-first inside their scope: add or update failing tests before changing the paired wrapper or catalog behavior.

## Milestones

### M1. Catalog Metadata And Wrapper Flag Contract

- Goal: Add the metadata and CLI contract needed for bounded parallel execution without changing selected-check execution semantics yet.
- Requirements: `R2`, `R2a`, `R2b`, `R2c`, `R3`, `R3a`, `R3b`, `R4`, `R4c`, `R4d`, `R5`, `R7`, `R10`, `R16`, `R16a`, `R20`.
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `scripts/ci.sh`
  - `specs/test-and-ci-speed-optimization.test.md`
  - this plan
- Dependencies:
  - accepted plan-review
  - active matching test spec
- Tests to add/update:
  - catalog tests for `parallel_safe` metadata and the six reviewed regression check IDs;
  - wrapper argument tests for valid `--jobs`, `--timeout`, `--fail-fast`, and `--verbose`;
  - wrapper argument tests proving invalid `--jobs` and `--timeout` fail before selector-selected commands start;
  - usage/help text tests if existing test style supports them.
- Implementation steps:
  - Extend `CheckCatalogEntry` with parallel-safety metadata using a default unsafe value.
  - Mark only `adapters.regression`, `artifact_lifecycle.regression`, `change_metadata.regression`, `review_artifacts.regression`, `selector.regression`, and `skills.regression` as parallel-safe.
  - Add a small helper for looking up whether a check ID is parallel-safe.
  - Add top-level wrapper defaults in `scripts/ci.sh` for default timeout and default jobs.
  - Parse `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` in `scripts/ci.sh`.
  - Reject invalid flag values before calling the selector or running selected commands.
  - Keep existing modes and mode-specific arguments unchanged.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/ci.sh specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Expected observable result: contributors can pass the new flags, invalid values fail early, and the catalog has explicit reviewed safe-check metadata without changing which checks are selected.
- Commit message: `M1: add CI parallelism flag and catalog metadata`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: adding metadata to the catalog could accidentally alter selector JSON or check order.
- Rollback/recovery: revert the metadata and flag parsing changes; existing serial wrapper behavior remains the recovery path.

### M2. Deterministic Sequential Runner And Failure Attribution

- Goal: Replace ad hoc serial command execution with the deterministic selected-check result model that works for `--jobs 1` and non-allowlisted checks.
- Requirements: `R1`, `R2a`, `R3c`, `R3d`, `R3e`, `R6`, `R8`-`R14`, `R16`, `R16a`, `R20`.
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `specs/test-and-ci-speed-optimization.test.md`
  - this plan
- Dependencies:
  - M1 complete
- Tests to add/update:
  - `--jobs 1` runs selected checks sequentially with the new summary format;
  - failed check output appears after the summary in stable order;
  - successful output is hidden by default and shown with `--verbose`;
  - stdout and stderr are captured separately and reported deterministically;
  - non-UTF-8 output reports a decode failure against the affected check without crashing the scheduler;
  - timeout, signal kill, ordinary nonzero exit, unknown check ID, and unavailable command are distinct observable failures;
  - output capture storage failure is manually verified or covered with a controlled temp-dir failure if practical.
- Implementation steps:
  - Keep the selected-check validation against `catalog_command` before execution.
  - Introduce an internal result record with check ID, command, status, exit reason, elapsed runtime, stdout bytes, stderr bytes, and reporting notes.
  - Run each selected command through subprocess capture rather than direct shared stdout/stderr streaming.
  - Measure elapsed runtime from process start to process exit.
  - Terminate timed-out checks and report timeout distinctly.
  - Report signal-killed checks distinctly from ordinary nonzero exits.
  - Print a stable summary after execution, then failed check output in stable order.
  - Preserve existing no-selected-check behavior.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --jobs 1 --timeout 60 --verbose`
  - `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --jobs 1`
  - `git diff --check -- scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Expected observable result: sequential selected-check runs produce deterministic summaries, failure attribution, per-check logs, and timeout/signal/unavailable reporting.
- Commit message: `M2: add deterministic CI check reporting`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: switching from live streamed output to captured output can make debugging harder if `--verbose` is incomplete.
- Rollback/recovery: revert the runner changes and keep the M1 flag parsing disabled or accepted without changing serial behavior until reporting tests are repaired.

### M3. Bounded Parallel Scheduling And Fail-Fast

- Goal: Run reviewed parallel-safe checks concurrently with a bounded concurrency cap while keeping non-allowlisted checks serial and output deterministic.
- Requirements: `R2c`, `R2d`, `R4a`, `R4b`, `R6`, `R7`-`R7c`, `R8a`, `R9a`, `R9c`, `R10b`, `R11`, `R12`, `R20`.
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `specs/test-and-ci-speed-optimization.test.md`
  - this plan
- Dependencies:
  - M1 catalog metadata complete
  - M2 selected-check result model complete
- Tests to add/update:
  - two or more allowlisted checks prove concurrent start using temporary workspace marker files, not fragile timing alone;
  - `--jobs 1` still forces sequential execution for allowlisted checks;
  - a non-allowlisted selected check runs alone and does not overlap with allowlisted peers;
  - effective parallelism never exceeds selected eligible checks or `--jobs`;
  - default jobs uses CPU count minus one with a floor of one, with single-CPU behavior simulated if feasible;
  - default run-to-completion waits for already-started checks after a failure;
  - `--fail-fast` stops launching queued checks after a failure and reports queued checks as not started.
- Implementation steps:
  - Use stable-order FIFO scheduling.
  - Treat consecutive allowlisted checks as eligible for bounded parallel launch.
  - Flush running parallel checks before running a non-allowlisted check so unsafe checks run alone.
  - Keep result printing independent of finish order.
  - Under default behavior, continue launching remaining queued checks after failures until all selected checks have final states.
  - Under `--fail-fast`, stop launching checks that have not started after the first observed failure while still waiting for already-started checks.
  - Mark fail-fast-skipped queued checks as not started.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 3`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 1`
  - `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --jobs 2`
  - `git diff --check -- scripts/ci.sh scripts/validation_selection.py scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Expected observable result: selected allowlisted regression checks can run concurrently; unsafe checks stay serial; output remains stable; failures preserve useful attribution.
- Commit message: `M3: run parallel-safe CI checks concurrently`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: scheduler bugs can create flaky ordering, hidden races, or lost output.
- Rollback/recovery: run with `--jobs 1`, remove a check ID from the parallel-safe allowlist, or revert the M3 scheduler changes while keeping sequential reporting from M2.

### M4. Contributor Guidance, Hosted-CI Boundary, And Final Proof

- Goal: Document the new wrapper flags, confirm hosted CI remains thin and matrix-free, and complete final validation evidence.
- Requirements: `R9`, `R10`, `R15`, `R17`-`R20`, acceptance criteria `AC1`-`AC9`.
- Files/components likely touched:
  - `docs/workflows.md`
  - `.github/workflows/ci.yml` only if inspection finds a required thin-wrapper alignment
  - `scripts/test-select-validation.py`
  - `specs/test-and-ci-speed-optimization.test.md`
  - `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - `docs/plan.md`
  - change-local artifacts when implementation starts
- Dependencies:
  - M1-M3 complete
- Tests to add/update:
  - guidance assertion or selector test proving workflow YAML does not add matrix fan-out or hardcoded check lists, if the test spec requires automated proof;
  - broad-smoke non-recursion test remains passing;
  - final acceptance criteria mapping in the test spec is complete.
- Implementation steps:
  - Update `docs/workflows.md` with concise contributor guidance for `--jobs`, `--jobs 1`, `--timeout`, `--fail-fast`, and `--verbose`.
  - Inspect `.github/workflows/ci.yml`; leave it unchanged unless it conflicts with `R17` or needs a thin-wrapper call adjustment.
  - Record `.github/workflows/ci.yml` as unaffected with rationale if unchanged.
  - Run focused selected proof, concurrent regression proof, and direct broad smoke.
  - Keep plan progress, decision log, surprises, and validation notes current.
  - Prepare for code-review, verify, explain-change, and PR after implementation is complete.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md --jobs 2`
  - `bash scripts/ci.sh --mode broad-smoke`
  - `rg -n "matrix:|check-id:|fromJson|select-validation|scripts/ci.sh" .github/workflows/ci.yml docs/workflows.md`
  - `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/ci.sh scripts/validation_selection.py scripts/test-select-validation.py specs/test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.test.md docs/proposals/2026-05-04-test-and-ci-speed-optimization.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/plan.md`
- Expected observable result: contributors can discover and use bounded parallel execution safely; hosted CI remains a thin wrapper; final proof covers wrapper behavior and broad smoke.
- Commit message: `M4: document bounded CI parallelism`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks: documentation can imply matrix or caching work that is intentionally deferred.
- Rollback/recovery: revert documentation changes or remove allowlist entries; `--jobs 1` remains the operational fallback.

## Validation Plan

Use targeted proof first for each milestone, then broaden only when the touched surfaces require it.

- Plan creation validation:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
- Test-spec validation after plan-review:
  - `python scripts/select-validation.py --mode explicit --path specs/test-and-ci-speed-optimization.test.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path specs/test-and-ci-speed-optimization.test.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
- Implementation milestone validation: use the commands listed in each milestone.
- Final validation before PR readiness:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`
  - `bash scripts/ci.sh --mode broad-smoke`
  - selector-selected explicit proof for every touched authored file
  - `git diff --check -- <touched-authored-files>`

## Risks and Recovery

- Hidden shared state in a check marked parallel-safe: remove the check ID from the allowlist and rerun with `--jobs 1`; preserve recorded safety evidence for any future re-addition.
- Scheduler flake or output loss: fall back to the M2 sequential result model and keep parallel scheduling disabled until tests isolate the race.
- Local resource pressure: use CPU-minus-one default, allow explicit lower `--jobs`, and document `--jobs 1`.
- Timeout too tight for a legitimate future check: use invocation-level `--timeout <seconds>` first; add per-check catalog override only in a later reviewed slice.
- Hosted workflow drift: leave `.github/workflows/ci.yml` matrix-free in this slice and require any future matrix proposal to consume repo-owned stable check IDs.
- Broad-smoke failure after wrapper changes: first rerun with `--jobs 1` to separate scheduler issues from validation failures, then inspect failed-check output by stable check ID.

## Dependencies

- `specs/test-and-ci-speed-optimization.md` is approved and must remain the behavior source of truth.
- Plan-review is complete.
- `specs/test-and-ci-speed-optimization.test.md` is active before implementation.
- No architecture update is required unless implementation introduces a new wrapper module, changes hosted CI topology, or changes selector/check-catalog ownership beyond parallel-safety metadata.
- No external dependencies are planned.
- `.github/workflows/ci.yml` should remain unchanged unless implementation finds a direct conflict with the approved spec.

## Progress

- [x] Proposal accepted.
- [x] Spec approved.
- [x] Spec-review approved with SR-1 resolved by requiring `--fail-fast`.
- [x] Plan created.
- [x] Plan-review complete.
- [x] Test spec active.
- [x] M1 complete.
- [x] M2 complete.
- [x] M3 complete.
- [x] M4 complete.
- [x] Code-review complete.
- [x] Verify complete.
- [x] Explain-change complete.
- [x] PR ready.

## Decision Log

- 2026-05-04: Use a four-milestone implementation sequence: metadata and flags, sequential deterministic reporting, parallel scheduling, then guidance and final proof. This keeps risky scheduler work behind the result model it depends on.
- 2026-05-04: Keep the first implementation slice inside existing wrapper/catalog/test surfaces. Avoid adding a new CI runner module unless plan-review or implementation proves the embedded wrapper path is too brittle.
- 2026-05-04: Require final direct broad smoke because this initiative changes the validation wrapper itself, while still using targeted proof as the first validation layer for each milestone.
- 2026-05-05: Keep M2 sequential even when `--jobs` is greater than one -> the selected-check result model, timeout enforcement, and deterministic output are now in place before M3 introduces bounded concurrent scheduling.
- 2026-05-05: Keep M3 scheduling inside `scripts/ci.sh` -> the embedded runner can use standard-library `ThreadPoolExecutor` around the existing per-check process runner without introducing a new module or changing selector ownership.
- 2026-05-05: Add `RIGORLOOP_CI_CPU_COUNT_FIXTURE` as a test fixture hook only -> default job-count behavior can be deterministic in tests while wrapper defaults remain owned by `scripts/ci.sh`.
- 2026-05-05: Leave `.github/workflows/ci.yml` unchanged in M4 -> inspection and the new T17 contract test show it already delegates to `scripts/ci.sh` without matrix fan-out, hardcoded check IDs, caching, distributed execution, or sandbox setup.

## Surprises and Discoveries

- `docs/project-map.md` is absent; this plan records a no-map rationale and relies on direct reads of governing artifacts and implementation surfaces.
- `scripts/test-select-validation.py` already has fixture hooks and temporary workspace helpers that can support deterministic parallel-run tests without adding test-only catalog commands.
- No architecture update is currently required because the existing system architecture already models selector and CI wrapper responsibility at the right level.
- M1 did not need a new wrapper helper module. The implementation stayed inside `scripts/ci.sh`, `scripts/validation_selection.py`, and existing selector-wrapper regression tests.
- M1 parallel-safety evidence is recorded in `docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`. The initial allowlist scripts either perform no writes or write only under process-created temporary fixture directories; the only Git mutations found are local to temporary repositories.
- M2 preserves the single-file wrapper implementation. The embedded Python runner now owns a stable `CheckPlan`/`CheckResult` model, but no new helper module or architecture boundary was introduced.
- Successful selected-check output is hidden by default, including selected `broad_smoke.repo` output. Existing non-recursive broad-smoke proof uses `--verbose` when it needs to inspect successful child output.
- The first M2 selector-selected wrapper validation exposed an outer-timeout regression for `broad_smoke.repo`: broad smoke legitimately exceeded 60 seconds as a delegated wrapper command. M2 now excludes `broad_smoke.repo` from the selected-check outer timeout path so the later leaf-timeout work stays aligned with `R15a`.
- M3 did not need changes to `scripts/validation_selection.py` or the test spec. The existing catalog metadata and test-spec cases were sufficient; M3 adds scheduler tests and wrapper behavior only.
- The direct `--jobs 3` proof selected `adapters.drift` and `adapters.validate` between allowlisted checks. That is useful coverage: it proves non-allowlisted selected checks flush the parallel chunk and run alone while surrounding allowlisted checks still report in stable order.
- M4 did not need changes to `.github/workflows/ci.yml`; it already stays a thin wrapper around `scripts/ci.sh` for PR and main modes.
- The real six-script `--jobs 6` proof also selects `adapters.drift` and `adapters.validate` for the adapter path. That keeps the final proof closer to real selector behavior than a regression-ID-only fixture would.

## Validation Notes

- 2026-05-04: Plan creation selector inspection passed:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - Selected `artifact_lifecycle.validate` and `broad_smoke.repo` because this plan sets `broad_smoke_required: true`.
- 2026-05-04: Plan creation wrapper validation passed:
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - The run completed `artifact_lifecycle.validate` and delegated `broad_smoke.repo`; broad smoke passed.
- 2026-05-04: Test-spec creation selector inspection passed:
  - `python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - Selected `artifact_lifecycle.validate` and `broad_smoke.repo` because this plan sets `broad_smoke_required: true`.
- 2026-05-04: Test-spec lifecycle validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - The validator reported `validated 3 artifact files in explicit-paths mode`.
- 2026-05-04: Test-spec wrapper validation passed:
  - `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - The run completed `artifact_lifecycle.validate` and delegated `broad_smoke.repo`; broad smoke passed.
- 2026-05-04: M1 red proof passed:
  - `python scripts/test-select-validation.py`
  - Result: expected failure before implementation. New regressions failed because `is_parallel_safe_check` and catalog `parallel_safe` metadata did not exist, and `scripts/ci.sh` rejected `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` as unknown arguments.
- 2026-05-04: M1 focused regression suite passed:
  - `python scripts/test-select-validation.py`
  - Result: 43 tests passed after adding catalog metadata and wrapper flag parsing.
- 2026-05-04: M1 change metadata validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Result: valid change metadata.
- 2026-05-04: M1 selector-selected validation inspection passed:
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- 2026-05-04: M1 wrapper-selected validation passed:
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path scripts/ci.sh --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Executed `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`; all selected checks passed.
- 2026-05-04: M1 diff check passed:
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py scripts/ci.sh specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/proposals/2026-05-04-test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.md docs/plan.md`
- 2026-05-05: M2 red proof passed:
  - `python scripts/test-select-validation.py`
  - Result: expected failure before implementation. New regressions failed because the M1 runner streamed child output live, stopped after the first selected-check failure, lacked a stable summary/output model, did not enforce per-check timeout, and did not isolate undecodable child output.
- 2026-05-05: M2 focused regression suite passed:
  - `python scripts/test-select-validation.py`
  - Result: 49 tests passed after adding the deterministic sequential result model, per-check output capture, timeout handling, signal attribution, unavailable-command summary rows, verbose successful-output reporting, large-output isolation proof, and default-timeout constant proof.
- 2026-05-05: M2 focused wrapper proof passed:
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --jobs 1 --timeout 60 --verbose`
  - Selected `selector.regression`; the summary reported `selector.regression | passed | ok`.
- 2026-05-05: M2 selector-selected validation inspection passed:
  - `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
- 2026-05-05: M2 selector-selected wrapper validation initially failed, then passed after removing the selected-check outer timeout from `broad_smoke.repo`:
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path docs/plan.md --jobs 1`
  - Final result: selected checks passed; `broad_smoke.repo` reported `passed | ok` after completing in 39.53s on the final recorded run.
- 2026-05-05: M2 metadata, lifecycle, diff, and whitespace validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - `git diff --check -- scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/plan.md`
  - `rg -n '[[:blank:]]$|\\t' scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/plan.md`
- 2026-05-05: M2 code-review R2 recorded and CR2-F1 resolution proof passed:
  - Review record: `docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r2.md`
  - Resolution: added the missing large-output isolation test and default-timeout constant assertion.
  - `python scripts/test-select-validation.py`
  - Result: 49 tests passed.
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path docs/changes/2026-05-04-test-and-ci-speed-optimization/review-log.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/review-resolution.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r2.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --jobs 1`
  - Result: selected checks passed: `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - `git diff --check -- scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/plan.md`
  - `rg -n '[[:blank:]]$|\\t' scripts/ci.sh scripts/test-select-validation.py specs/test-and-ci-speed-optimization.test.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization docs/plan.md`
  - Result: all passed; whitespace scan found no matches.
- 2026-05-05: M3 red proof passed:
  - `python scripts/test-select-validation.py`
  - Result: expected failure before implementation. New M3 regressions failed because selected checks still ran sequentially, the CPU-count fixture did not affect default jobs, parallel siblings were not started together, and `--fail-fast` did not skip queued checks.
- 2026-05-05: M3 focused regression suite passed:
  - `python scripts/test-select-validation.py`
  - Result: 54 tests passed after adding bounded parallel-safe scheduling, fail-fast queued cancellation, non-allowlisted serial boundaries, default job-count fixture coverage, and stable scheduler reporting.
- 2026-05-05: M3 direct wrapper proofs passed:
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 3`
  - Result: selected checks passed: `skills.regression`, `adapters.regression`, `adapters.drift`, `adapters.validate`, and `artifact_lifecycle.regression`.
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 1`
  - Result: the same selected checks passed through the explicit sequential fallback.
- 2026-05-05: M3 selector-selected validation inspection and wrapper proof passed:
  - `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
  - Selected `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.test.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
- 2026-05-05: M3 closeout metadata, lifecycle, selected wrapper, diff, and whitespace validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Result: valid change metadata.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Result: validated 3 artifact files in explicit-paths mode.
  - `python scripts/select-validation.py --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
  - `git diff --check -- scripts/ci.sh scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
  - `rg -n '[[:blank:]]$|\\t' scripts/ci.sh scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: no trailing whitespace or tabs found.
- 2026-05-05: M4 red proof passed:
  - `python scripts/test-select-validation.py`
  - Result: expected failure before documentation update. New T17 coverage failed because `docs/workflows.md` did not yet document `--jobs`, `--jobs 1`, `--timeout`, `--fail-fast`, and `--verbose`.
- 2026-05-05: M4 focused regression suite passed:
  - `python scripts/test-select-validation.py`
  - Result: 55 tests passed after adding workflow-guidance flag assertions, hosted-CI matrix-free assertions, and concise contributor guidance.
- 2026-05-05: M4 six-script bounded-parallel proof passed:
  - `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`
  - Result: selected checks passed: `skills.regression`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.regression`, `artifact_lifecycle.regression`, `change_metadata.regression`, and `selector.regression`.
- 2026-05-05: M4 authored-surface selector inspection and wrapper proof passed:
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md`
  - Selected `artifact_lifecycle.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/plan.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
- 2026-05-05: M4 direct broad smoke and hosted-CI boundary inspection passed:
  - `bash scripts/ci.sh --mode broad-smoke`
  - Result: broad smoke passed.
  - `rg -n "matrix:|check-id:|fromJson|select-validation|scripts/ci.sh|actions/cache" .github/workflows/ci.yml docs/workflows.md`
  - Result: only expected `scripts/select-validation.py` and `scripts/ci.sh` documentation references plus `.github/workflows/ci.yml` wrapper calls were returned; no `matrix:`, `check-id:`, `fromJson`, or `actions/cache` matches were present.
- 2026-05-05: M4 closeout metadata, lifecycle, selected wrapper, direct broad smoke, diff, and whitespace validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Result: valid change metadata.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Result: validated 3 artifact files in explicit-paths mode.
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode broad-smoke`
  - Result: direct broad smoke passed and validated the changed review artifact root.
  - `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/ci.sh scripts/validation_selection.py scripts/test-select-validation.py specs/test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.test.md docs/proposals/2026-05-04-test-and-ci-speed-optimization.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/plan.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
  - `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: no trailing whitespace or tabs found.
- 2026-05-05: Direct M4 code-review completed:
  - Review status: `clean-with-notes`.
  - Findings: no blocking or required-change findings.
  - Recommended next stage: `verify`.
- 2026-05-05: Verify passed after post-code-review lifecycle bookkeeping:
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode broad-smoke`
  - Result: direct broad smoke passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: review artifact closeout validation passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Result: valid change metadata.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Result: artifact lifecycle validation passed.
  - `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
  - `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: no trailing whitespace or tabs found.
- 2026-05-05: Explain-change closeout passed:
  - Updated `docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md` with the completed problem-to-diff rationale, tests, review-resolution summary, verification evidence, alternatives rejected, scope control, risks, and PR handoff summary.
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md`
  - Selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path .github/workflows/ci.yml --path scripts/test-select-validation.py --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --jobs 2`
  - Result: selected checks passed, including `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode broad-smoke`
  - Result: direct broad smoke passed.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: review artifact closeout validation passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
  - Result: valid change metadata.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml --path docs/changes/2026-05-04-test-and-ci-speed-optimization/explain-change.md --path docs/plan.md --path docs/plans/2026-05-04-test-and-ci-speed-optimization.md --path docs/proposals/2026-05-04-test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.md --path specs/test-and-ci-speed-optimization.test.md`
  - Result: artifact lifecycle validation passed.
  - `git diff --check -- docs/workflows.md .github/workflows/ci.yml scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Passed.
  - `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/test-select-validation.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization`
  - Result: no trailing whitespace or tabs found.
- 2026-05-05: PR handoff readiness passed:
  - Replayed the branch onto fresh `origin/main` as `2026-05-04-test-and-ci-speed-optimization`.
  - `python scripts/select-validation.py --mode pr --base origin/main --head HEAD`
  - Selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `broad_smoke.repo`.
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
  - Result: selected checks passed, including `broad_smoke.repo`.
  - `git diff --check origin/main...HEAD`
  - Passed.
  - `rg -n '[[:blank:]]$|\\t' docs/workflows.md scripts/ci.sh scripts/test-select-validation.py scripts/validation_selection.py docs/plan.md docs/plans/2026-05-04-test-and-ci-speed-optimization.md docs/changes/2026-05-04-test-and-ci-speed-optimization specs/test-and-ci-speed-optimization.md specs/test-and-ci-speed-optimization.test.md`
  - Result: no trailing whitespace or tabs found.

## Outcome and Retrospective

- Initiative is active. M1, M2, M3, M4, direct code-review, verify, explain-change, and PR handoff readiness are complete; merge-dependent Done state remains pending.

## Readiness

- Ready to open a PR.
- Keep this plan current during implementation, including progress, decisions, discoveries, and validation notes.
