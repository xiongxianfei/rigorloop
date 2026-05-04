# Test and CI Speed Optimization

## Status

- approved

## Related proposal

- [Test and CI Speed Optimization](../docs/proposals/2026-05-04-test-and-ci-speed-optimization.md)

## Goal and context

This spec defines bounded parallel execution for repository validation checks run through `scripts/ci.sh`.

The goal is to reduce validation wall-clock time for checks that are already selected by the repository-owned selector, without changing which checks are selected, weakening proof requirements, moving validation routing into hosted CI YAML, or introducing caching. The selector still decides what runs. The CI wrapper decides how selected checks execute.

## Glossary

- `selected check`: one check returned by `scripts/select-validation.py` using a stable check ID and catalog command.
- `parallel-safe check`: a selected check that has been reviewed and marked safe to run concurrently with other parallel-safe checks.
- `parallel-safe allowlist`: the set of stable check IDs that may run concurrently when `--jobs` allows it.
- `parallel-unsafe check`: any check not on the parallel-safe allowlist.
- `job slot`: one concurrent process slot available to the wrapper for running a parallel-safe check.
- `leaf check`: the actual validation command that performs proof work, not a recursive wrapper delegation.
- `run-to-completion`: default behavior where the wrapper waits for all started checks and reports their final states before exiting.
- `fail-fast`: opt-in behavior where the wrapper stops launching queued checks after a failure is observed.
- `per-check timeout`: the maximum runtime for one leaf check before the wrapper marks it timed out.
- `stable order`: selector order unless a later approved spec chooses another deterministic order.

## Examples first

### Example E1: parallel-safe selected checks run concurrently

Given selected checks include `skills.regression`, `adapters.regression`, and `artifact_lifecycle.regression`
And all three check IDs are on the parallel-safe allowlist
When a contributor runs `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-artifact-lifecycle-validator.py --jobs 3`
Then the wrapper may run those checks concurrently
And the summary output lists them in stable order
And the wrapper exits `0` only if every required check passes.

### Example E2: non-allowlisted checks remain serial

Given selected checks include one allowlisted regression check and one check that is not on the parallel-safe allowlist
When a contributor runs `bash scripts/ci.sh --mode explicit --path <path> --jobs 4`
Then the allowlisted check may run in parallel with other allowlisted checks
And the non-allowlisted check runs serially
And the wrapper does not treat absence from the allowlist as an error.

### Example E3: jobs one is explicit sequential mode

Given multiple selected checks are on the parallel-safe allowlist
When a contributor runs `bash scripts/ci.sh --mode explicit --path <path> --jobs 1`
Then the wrapper runs selected checks sequentially
And the output still uses the same summary and failure attribution format.

### Example E4: failures wait for started checks by default

Given two parallel-safe selected checks are started
And the first check fails quickly
And the second check is still running
When `--fail-fast` is not supplied
Then the wrapper waits for the second started check to finish
And the wrapper exits nonzero after reporting both final check states.

### Example E5: fail-fast stops queued work

Given selected checks include three parallel-safe checks
And only one job slot is available
And the first check fails
When `--fail-fast` is supplied
Then the wrapper does not start queued checks after the failure is observed
And queued checks that were not started are reported as not started because fail-fast cancelled the remaining queue.

### Example E6: timeout is reported distinctly

Given a selected check exceeds the configured per-check timeout
When the timeout expires
Then the wrapper terminates the check
And reports the check as timed out instead of only reporting a generic nonzero exit.

### Example E7: broad smoke uses leaf-check timeout behavior

Given a selected check is `broad_smoke.repo`
When the wrapper executes broad-smoke validation
Then timeout behavior applies to the leaf checks run by broad-smoke mode
And the wrapper does not need a separate outer timeout for the recursive `broad_smoke.repo` delegation.

## Requirements

R1. `scripts/ci.sh` MUST preserve the existing validation-selection contract: the selector decides which checks are selected, and the wrapper executes selected checks.

R2. `scripts/ci.sh` MUST support `--jobs <positive-integer>`.

R2a. `--jobs 1` MUST force sequential selected-check execution.

R2b. `--jobs 0`, negative values, non-integers, empty values, and unlimited fan-out values MUST fail before validation commands start.

R2c. When `--jobs` is omitted, the wrapper MUST choose a default job count derived from available CPU count minus one with a floor of one.

R2d. The effective parallelism MUST NOT exceed the number of selected checks that are eligible to run concurrently.

R3. `scripts/ci.sh` MUST support `--timeout <positive-seconds>`.

R3a. The default per-check timeout MUST be 60 seconds.

R3b. Invalid timeout values, including zero, negative values, non-integers, and empty values, MUST fail before validation commands start.

R3c. Timeout measurement MUST apply to leaf-check process runtime from process start to process exit.

R3d. Queue wait time MUST NOT count toward a check's elapsed runtime.

R3e. A selected check that times out MUST cause a nonzero wrapper exit unless a later approved spec explicitly defines an allowed timed-out state.

R4. The repository MUST define a parallel-safe allowlist keyed by stable check ID.

R4a. A selected check MUST NOT run concurrently unless its check ID is on the parallel-safe allowlist.

R4b. A selected check that is absent from the allowlist MUST run sequentially and MUST NOT fail solely because it is absent from the allowlist.

R4c. The initial allowlist MUST include only reviewed check IDs that satisfy the parallel-safe definition.

R4d. The initial allowlist MUST include these reviewed regression check IDs after the spec's required safety evidence is recorded:
- `adapters.regression`;
- `artifact_lifecycle.regression`;
- `change_metadata.regression`;
- `review_artifacts.regression`;
- `selector.regression`;
- `skills.regression`.

R5. A check MAY be marked parallel-safe only when it:
- does not write tracked repository paths;
- writes scratch data only to process-unique temporary locations;
- does not mutate shared external resources such as fixed ports, fixed lockfiles, shared services, or global Git configuration;
- writes runtime output only to its own stdout and stderr streams.

R6. The wrapper MUST run all started checks to completion by default, even after one selected check fails.

R7. The wrapper MUST support `--fail-fast`.

R7a. When `--fail-fast` is supplied and a failure is observed while selected checks remain queued, the wrapper MUST stop launching queued checks that have not started.

R7b. `--fail-fast` MUST NOT hide final status for checks that were already started.

R7c. A check skipped because of fail-fast cancellation MUST be reported as not started because fail-fast cancelled the remaining queue.

R8. The wrapper MUST capture stdout and stderr separately for each selected check.

R8a. Parallel checks MUST NOT write directly to the shared wrapper stdout or stderr stream while they run.

R8b. The wrapper MUST decode captured output only for reporting.

R8c. A decode failure MUST NOT crash the scheduler; it MUST be reported against the affected check.

R9. The wrapper MUST print a normal summary after selected check execution.

R9a. The summary MUST list selected checks in stable order.

R9b. Each summary row MUST include at least check ID, status, exit reason, and elapsed runtime.

R9c. Failed check output MUST be printed after the summary in stable order.

R9d. Successful check output MUST be hidden by default.

R10. The wrapper MUST support `--verbose`.

R10a. With `--verbose`, the wrapper MUST make successful check output available in addition to failed check output.

R10b. Verbose output MUST preserve stable check ordering.

R11. Check final status MUST distinguish at least:
- passed;
- exited with code;
- killed by signal;
- timed out;
- not started because fail-fast cancelled the remaining queue.

R12. If any required selected check exits nonzero, is killed by signal, times out, or is unavailable, `scripts/ci.sh` MUST exit nonzero.

R13. If selector output references an unknown check ID, the wrapper MUST fail before running that unknown check.

R13a. Unknown check ID failure output MUST identify the unknown ID.

R14. If a selected check command is unavailable, the wrapper MUST fail and identify the check ID and unavailable command.

R15. If `broad_smoke.repo` is selected, the wrapper MUST preserve the existing non-recursive broad-smoke behavior.

R15a. Timeout enforcement for broad-smoke validation SHOULD apply to the leaf checks run by broad-smoke mode rather than a special outer timeout on the recursive wrapper invocation.

R16. The wrapper MUST preserve the existing mode inputs for `local`, `explicit`, `pr`, `main`, `release`, and `broad-smoke`.

R16a. Existing mode-specific required arguments, such as `--path`, `--base`, `--head`, and `--release-version`, MUST keep their current meaning.

R17. Hosted CI workflow YAML MUST NOT duplicate selector path classification or check-selection rules.

R18. GitHub Actions matrix fan-out MUST NOT be added in this first slice.

R19. Persistent result caching, dependency caching, input-hash skip logic, distributed execution, and per-check sandboxing MUST NOT be added in this first slice.

R20. Configuration ownership MUST follow these boundaries:
- per-check command, paths, version, and parallel-safety live with the check catalog;
- selector decision rules live with the selector;
- wrapper defaults such as default jobs and default timeout live in `scripts/ci.sh`;
- invocation overrides live in command-line flags;
- test fixtures may use environment variables;
- hosted environment details live in workflow YAML.

## Inputs and outputs

Inputs:

- Existing `scripts/ci.sh` modes and mode-specific arguments.
- `--jobs <positive-integer>`.
- `--timeout <positive-seconds>`.
- Optional invocation flag `--fail-fast`.
- Optional `--verbose`.
- Selector output containing selected check IDs, commands, paths, affected roots, versions, and rationale.
- Parallel-safe check metadata.

Outputs:

- Wrapper process exit code.
- Stable normal summary rows for selected checks.
- Failed check stdout and stderr output.
- Successful check output when `--verbose` is supplied.
- Error messages for invalid wrapper arguments, unknown check IDs, unavailable commands, signal kills, and timeouts.

## State and invariants

- The selector remains the source of truth for selected checks.
- The wrapper remains the source of truth for execution behavior and command reporting.
- Absence from the parallel-safe allowlist means serial execution, not failure.
- Required selected checks are not skipped to improve speed.
- Broad-smoke trigger semantics remain governed by the existing validation contract.
- Parallel execution must not change selected-check ordering in normal reports.
- `--jobs 1` is the stable compatibility and race-debugging fallback.

## Error and boundary behavior

- Invalid `--jobs` input fails before selector-selected validation commands run.
- Invalid `--timeout` input fails before selector-selected validation commands run.
- Unknown wrapper arguments fail before selector-selected validation commands run.
- Unknown check IDs fail before that check runs.
- Unavailable selected commands fail with check ID and command evidence.
- A timed-out check is reported as timed out and causes a nonzero wrapper exit.
- A check killed by signal is reported with signal evidence and causes a nonzero wrapper exit.
- If output capture storage cannot be created, the wrapper fails before starting parallel selected checks.
- If `--fail-fast` is supplied and a failure occurs, already-started checks still report final status.
- If selected checks are empty and selector status is `ok`, the wrapper may report no selected checks and exit `0`, preserving existing selector-wrapper behavior.

## Compatibility and migration

- Existing direct validation commands remain valid.
- Existing `scripts/ci.sh` modes remain valid.
- No-argument `bash scripts/ci.sh` continues to mean legacy broad-smoke behavior unless a later approved spec changes it.
- Existing hosted CI may continue calling `scripts/ci.sh` without matrix fan-out.
- Rollback can use `--jobs 1`, remove a check ID from the allowlist, or revert the wrapper change.
- Generated `.codex/skills/` and `dist/adapters/` outputs remain derived outputs and are not hand-edited by this change.

## Observability

- Wrapper output MUST name each selected check ID before or within the summary.
- Wrapper output MUST name commands actually run or make them visible in verbose output.
- Normal output MUST show status and elapsed runtime for each selected check.
- Timeout, signal, unavailable command, and nonzero exit failures MUST be attributable to the responsible check ID.
- Parallel execution MUST NOT produce interleaved check logs in normal output.

## Security and privacy

- Captured output MUST NOT be written to tracked repository paths.
- Temporary output capture paths MUST be process-unique.
- Wrapper logs MUST NOT introduce secrets, tokens, private keys, or machine-local sensitive paths beyond paths already emitted by underlying validation commands.
- Unknown check IDs and mismatched commands MUST NOT be executed.

## Accessibility and UX

No UI is involved.

Contributor-facing output should stay readable in plain terminal logs. Normal output should favor a concise summary and failed-check detail over full successful logs.

## Performance expectations

- The wrapper SHOULD use bounded parallelism only for allowlisted checks.
- The default job count SHOULD leave at least one CPU available when CPU count is greater than one.
- The 60-second default timeout SHOULD be long enough for current legitimate checks and short enough to detect likely hangs.
- Parallel execution SHOULD reduce wall-clock time when multiple allowlisted checks are selected, subject to local CPU and I/O limits.

## Edge cases

EC1. `--jobs 1` with multiple allowlisted checks runs sequentially.

EC2. `--jobs` is omitted on a single-CPU machine; effective jobs is one.

EC3. `--jobs 999` with two allowlisted selected checks runs at most two checks concurrently.

EC4. One allowlisted check and one non-allowlisted check are selected; the non-allowlisted check runs serially.

EC5. One parallel check fails quickly while another started check is still running; default behavior waits for both.

EC6. `--fail-fast` is supplied and a queued check has not started when a failure occurs; the queued check is reported as not started.

EC7. A selected check emits non-UTF-8 bytes; reporting does not crash the scheduler.

EC8. A selected check writes enough output to require temporary capture storage; output remains isolated per check.

EC9. A selected check exceeds 60 seconds with default timeout; it is reported as timed out.

EC10. A selected check is killed by signal; the signal is reported distinctly from ordinary nonzero exit.

EC11. Selector output contains a valid selected check not on the parallel-safe allowlist; it runs serially.

EC12. Selector output contains an unknown check ID; the wrapper fails before running it.

EC13. `broad_smoke.repo` is selected; broad-smoke execution stays non-recursive and timeout behavior applies to leaf checks.

EC14. Hosted CI invokes the wrapper without matrix; selection still comes from repository-owned scripts.

## Non-goals

- GitHub Actions matrix fan-out.
- Persistent result caching.
- Dependency caching.
- Distributed execution.
- Per-check sandboxing, containers, cgroups, or namespaces.
- Dynamic scheduling beyond stable-order launching with a concurrency cap.
- Changing selector path classification rules except where needed to carry per-check execution metadata.
- Changing generated-output sync behavior.

## Acceptance criteria

AC1. `bash scripts/ci.sh --mode explicit --path <path> --jobs 1` preserves sequential execution and reports selected check status.

AC2. `bash scripts/ci.sh --mode explicit --path <path> --jobs N` runs multiple allowlisted selected checks concurrently when at least two are selected and N is greater than one.

AC3. Non-allowlisted selected checks run serially with `--jobs N`.

AC4. Any selected check failure causes nonzero wrapper exit after all started checks finish unless `--fail-fast` applies to queued checks.

AC5. Normal output includes a stable summary and failed-check output without interleaving parallel logs.

AC6. `--verbose` exposes successful check output in stable order.

AC7. Invalid `--jobs`, invalid `--timeout`, unknown check ID, unavailable command, timeout, and signal-kill cases have distinct observable failures.

AC8. The six current `scripts/test-*.py` regression checks are present in the initial parallel-safe allowlist and have recorded evidence supporting that status.

AC9. Hosted workflow YAML does not duplicate selector path classification or selected-check lists.

## Open questions

- Should JSON summary output be included in the first implementation slice or deferred until hosted matrix orchestration needs it?

This does not block spec review because human-readable summary output is sufficient for the first slice.

## Next artifacts

- `spec-review`.
- Architecture update or ADR only if spec review decides check metadata ownership or wrapper execution boundaries require one.
- `specs/test-and-ci-speed-optimization.test.md`.
- Execution plan after review and test-spec readiness.

## Follow-on artifacts

- `spec-review`: approved with no material findings on 2026-05-04.
- `specs/test-and-ci-speed-optimization.test.md`.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`.

## Readiness

Approved. This review does not require an architecture update or ADR because the spec preserves the existing selector, check catalog, wrapper, and hosted CI boundaries. The active test spec and execution plan exist; implementation is next.
