# Test and CI Speed Optimization Test Spec

## Status

- active

## Related spec and plan

- Spec: [Test and CI Speed Optimization](test-and-ci-speed-optimization.md), approved.
- Proposal: [Test and CI Speed Optimization](../docs/proposals/2026-05-04-test-and-ci-speed-optimization.md), accepted.
- Plan: [Test and CI Speed Optimization Implementation Plan](../docs/plans/2026-05-04-test-and-ci-speed-optimization.md), active.
- Spec-review outcome: approved with no architecture update required; the `--fail-fast` minor finding was resolved in the approved spec.
- Plan-review outcome: approved with no material findings; no detailed review record was required.
- Architecture: no new architecture artifact is required unless implementation changes selector ownership, hosted CI topology, or introduces a new wrapper module boundary.

## Testing strategy

- Unit tests cover check catalog metadata, parallel-safe defaults, reviewed allowlist membership, default job-count calculation, and stable selected-check result classification.
- Integration tests exercise `scripts/ci.sh` through `scripts/test-select-validation.py` using selector fixtures, temporary workspaces, and fake scripts placed at existing catalog command paths.
- Contract tests inspect `docs/workflows.md` and `.github/workflows/ci.yml` to prove contributor guidance and hosted CI remain aligned with the selector/wrapper boundary.
- Smoke tests run the six reviewed regression scripts through the wrapper with bounded parallelism and run direct broad smoke before PR readiness.
- Manual verification is limited to implementation-review evidence for the six initial parallel-safe checks and any host behavior that cannot be made deterministic in the Python test harness.
- Tests must use repository files, Bash, Python standard library facilities, and existing fixture environment variables. They must not require network access, secrets, hosted CI, or new runtime dependencies.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1` | `T2`, `T14`, `T16`, `T18` | Selector remains the source of selected checks; wrapper executes only selector-approved commands. |
| `R2`-`R2d` | `T2`, `T3`, `T4`, `T5`, `T6`, `T7` | CLI support, invalid values, default jobs, `--jobs 1`, cap by eligible checks, and bounded concurrency. |
| `R3`-`R3e` | `T2`, `T3`, `T12`, `T15` | CLI support, invalid values, 60-second default, leaf-runtime timing, queue exclusion, and nonzero timeout exit. |
| `R4`-`R4d` | `T1`, `T6`, `T7`, `T18` | Stable-ID allowlist, initial reviewed IDs, default unsafe behavior, and non-error serial fallback. |
| `R5` | `T1`, `T19` | Parallel-safe evidence and tracked-path, scratch-dir, shared-resource, and stdout/stderr safety criteria. |
| `R6` | `T8` | Default run-to-completion after observed failures. |
| `R7`-`R7c` | `T2`, `T9` | Required `--fail-fast` support, queued-check cancellation, started-check reporting, and not-started status. |
| `R8`-`R8c` | `T10`, `T11` | Per-check stdout/stderr capture, no live interleaving, decode-at-reporting, and decode failure attribution. |
| `R9`-`R9d` | `T5`, `T10`, `T11`, `T12`, `T13`, `T14` | Normal summary, stable order, required row fields, failed output, and hidden successful logs by default. |
| `R10`-`R10b` | `T2`, `T10` | `--verbose` support and stable successful-output reporting. |
| `R11` | `T5`, `T9`, `T12`, `T13`, `T14` | Passed, exited, killed, timed-out, unavailable, and fail-fast not-started statuses. |
| `R12` | `T8`, `T12`, `T13`, `T14` | Nonzero wrapper exit for required selected-check failures. |
| `R13`-`R13a` | `T14` | Unknown check IDs fail before execution and identify the ID. |
| `R14` | `T14` | Unavailable commands fail with check ID and command evidence. |
| `R15`-`R15a` | `T15` | Broad-smoke non-recursion is preserved; timeout behavior is verified at leaf-check execution. |
| `R16`-`R16a` | `T2`, `T16` | Existing modes and mode-specific arguments keep their current meaning. |
| `R17` | `T17` | Hosted CI does not duplicate selector classification or check-selection rules. |
| `R18` | `T17` | No GitHub Actions matrix fan-out is introduced in this slice. |
| `R19` | `T17`, `T18` | No caching, skip logic, distributed execution, or sandboxing is introduced. |
| `R20` | `T1`, `T2`, `T3`, `T17`, `T19` | Configuration ownership remains in the catalog, selector, wrapper constants, CLI flags, fixture env vars, and workflow YAML. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T6`, `T18` | Multiple allowlisted regression checks run concurrently and summarize in stable order. |
| `E2` | `T7` | A non-allowlisted check runs serially and absence from the allowlist is not an error. |
| `E3` | `T5`, `T10` | `--jobs 1` uses sequential execution with the same deterministic reporting model. |
| `E4` | `T8` | Default behavior waits for started checks after one failure. |
| `E5` | `T9` | `--fail-fast` stops launching queued checks and reports not-started checks. |
| `E6` | `T12` | Timeout is distinct from ordinary nonzero exit. |
| `E7` | `T15` | Broad-smoke behavior remains non-recursive and bounded at leaf-check execution. |

## Edge case coverage

- EC1, `--jobs 1` with multiple allowlisted checks: `T5`
- EC2, omitted jobs on a single-CPU machine: `T4`
- EC3, `--jobs 999` with two allowlisted checks: `T4`, `T6`
- EC4, allowlisted and non-allowlisted checks selected together: `T7`
- EC5, one started parallel check fails while another runs: `T8`
- EC6, fail-fast skips queued unstarted checks: `T9`
- EC7, non-UTF-8 bytes: `T11`
- EC8, large output requiring isolated capture storage: `T11`
- EC9, default timeout exceeded: `T12`
- EC10, signal-killed check: `T13`
- EC11, valid selected check absent from allowlist: `T7`
- EC12, unknown selected check ID: `T14`
- EC13, `broad_smoke.repo` selected: `T15`
- EC14, hosted CI invokes wrapper without matrix: `T17`

## Acceptance criteria coverage

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T5` | Explicit sequential execution and selected-check status reporting. |
| `AC2` | `T6`, `T18` | Concurrent execution for multiple allowlisted checks. |
| `AC3` | `T7` | Non-allowlisted checks run serially. |
| `AC4` | `T8`, `T9`, `T12`, `T13`, `T14` | Failure exits and fail-fast semantics. |
| `AC5` | `T10`, `T11` | Stable summary and non-interleaved failed output. |
| `AC6` | `T10` | Verbose successful output in stable order. |
| `AC7` | `T3`, `T12`, `T13`, `T14` | Distinct invalid argument and check failure modes. |
| `AC8` | `T1`, `T18`, `T19` | Six regression checks are allowlisted with safety evidence and smoke proof. |
| `AC9` | `T17` | Hosted workflow stays thin and selector-owned. |

## Test cases

### T1. Catalog records reviewed parallel-safe metadata

- Covers: `R4`-`R4d`, `R5`, `R20`, `AC8`
- Level: unit, manual evidence review
- Fixture/setup:
  - `scripts/validation_selection.py`
  - the current six regression check IDs named in `R4d`
  - recorded implementation evidence for the safe-check inspection
- Steps:
  - Load `CHECK_CATALOG` from `scripts/validation_selection.py`.
  - Assert every catalog entry exposes explicit parallel-safety metadata.
  - Assert entries default to not parallel-safe unless deliberately marked.
  - Assert exactly these initial regression IDs are marked parallel-safe: `adapters.regression`, `artifact_lifecycle.regression`, `change_metadata.regression`, `review_artifacts.regression`, `selector.regression`, and `skills.regression`.
  - Inspect recorded evidence for those six IDs against the `R5` criteria.
- Expected result:
  - The allowlist is keyed by stable check ID, includes only the reviewed initial IDs, and keeps all other checks serial by default.
- Failure proves:
  - The scheduler can parallelize unreviewed checks or lose the deliberate review gate for parallel safety.
- Automation location:
  - `python scripts/test-select-validation.py`
  - evidence recorded in the active plan, change-local artifact, or implementation review notes

### T2. Wrapper accepts new flags without breaking existing modes

- Covers: `R1`, `R2`, `R3`, `R7`, `R10`, `R16`, `R16a`, `R20`
- Level: integration
- Fixture/setup:
  - selector fixture returning `status: "ok"` with no selected checks
  - `RIGORLOOP_CI_SELECTOR_ARGV_FILE` to capture selector arguments
- Steps:
  - Run `scripts/ci.sh` in `explicit`, `pr`, `main`, and `release` modes with their existing required arguments.
  - Add valid `--jobs`, `--timeout`, `--fail-fast`, and `--verbose` wrapper flags.
  - Assert selector-facing arguments still contain only the mode-specific selector arguments and do not forward wrapper execution flags.
  - Run direct `--mode broad-smoke` with the existing broad-smoke stub.
- Expected result:
  - New wrapper flags are accepted, existing mode inputs keep their meaning, and selector routing remains unchanged.
- Failure proves:
  - The flag parser changed selector behavior or broke compatibility for existing wrapper invocations.
- Automation location:
  - `python scripts/test-select-validation.py`

### T3. Invalid wrapper values fail before selector-selected commands run

- Covers: `R2b`, `R3b`, `R20`, `AC7`
- Level: integration
- Fixture/setup:
  - selector fixture containing a selected check command that would create a marker file if executed
  - `RIGORLOOP_CI_SELECTOR_ARGV_FILE` or equivalent trace file
- Steps:
  - Run invalid `--jobs` cases: `0`, negative number, non-integer, empty value, and any advertised unlimited value.
  - Run invalid `--timeout` cases: `0`, negative number, non-integer, and empty value.
  - Run an unknown wrapper argument.
  - Assert the marker file is not created.
  - Assert the failure message identifies the invalid flag and value class.
- Expected result:
  - Invalid wrapper arguments fail before validation commands start.
- Failure proves:
  - A malformed invocation can partially execute validation work or hide the true input error.
- Automation location:
  - `python scripts/test-select-validation.py`

### T4. Default and effective job counts are bounded

- Covers: `R2c`, `R2d`, `EC2`, `EC3`
- Level: unit, integration
- Fixture/setup:
  - deterministic CPU-count fixture hook or implementation helper for the wrapper job-count calculation
  - selector fixture with two or more allowlisted selected checks
  - temporary workspace fake scripts at existing catalog command paths
- Steps:
  - Simulate a single available CPU and omit `--jobs`.
  - Simulate more than one available CPU and omit `--jobs`.
  - Run with `--jobs 999` and two eligible selected checks.
  - Record maximum observed concurrent starts using marker files or file locks in a temporary directory.
- Expected result:
  - Omitted `--jobs` resolves to CPU count minus one with a floor of one.
  - Effective parallelism never exceeds the lower of requested jobs and eligible selected checks.
- Failure proves:
  - The wrapper can overload small machines or launch more work than the selected eligible set allows.
- Automation location:
  - `python scripts/test-select-validation.py`

### T5. `--jobs 1` runs selected checks sequentially with stable reporting

- Covers: `R2a`, `R9`-`R9d`, `R11`, `E3`, `EC1`, `AC1`
- Level: integration
- Fixture/setup:
  - selector fixture with multiple allowlisted selected checks in a known order
  - temporary workspace fake scripts that write start/end marker files and successful stdout/stderr
- Steps:
  - Run `bash scripts/ci.sh --mode explicit --path <fixture-path> --jobs 1`.
  - Assert the second check starts only after the first check finishes.
  - Assert the summary lists checks in selector order.
  - Assert every summary row includes check ID, status, exit reason, and elapsed runtime.
  - Assert successful logs are hidden by default.
- Expected result:
  - `--jobs 1` is an explicit sequential compatibility mode while using the same result-reporting format as parallel runs.
- Failure proves:
  - The rollback/debugging path can race or report differently from normal execution.
- Automation location:
  - `python scripts/test-select-validation.py`

### T6. Allowlisted selected checks run concurrently within the cap

- Covers: `R2d`, `R4a`, `R8a`, `R9a`, `E1`, `EC3`, `AC2`
- Level: integration
- Fixture/setup:
  - selector fixture selecting at least two allowlisted regression IDs in a known order
  - temporary workspace fake scripts at those catalog command paths
  - process-unique temporary marker directory
- Steps:
  - Run the wrapper with `--jobs 2` or higher.
  - Make each fake script record a started marker, wait for a peer marker, then exit successfully.
  - Assert both scripts were simultaneously active without relying only on elapsed wall-clock time.
  - Assert summary and any output still print in selector order, not finish order.
- Expected result:
  - Reviewed safe checks run concurrently and reporting remains deterministic.
- Failure proves:
  - Parallel-safe metadata is ignored, the concurrency cap is ineffective, or output order depends on scheduler timing.
- Automation location:
  - `python scripts/test-select-validation.py`

### T7. Non-allowlisted selected checks run alone

- Covers: `R4a`, `R4b`, `R11`, `E2`, `EC4`, `EC11`, `AC3`
- Level: integration
- Fixture/setup:
  - selector fixture with one allowlisted check, one non-allowlisted catalog check, and another allowlisted check
  - fake scripts that record overlapping runtime markers
- Steps:
  - Run with `--jobs 4`.
  - Assert the non-allowlisted check does not overlap with either allowlisted check.
  - Assert absence from the allowlist is reported, if at all, as serial execution rather than an error.
  - Assert all passing selected checks still produce passed statuses.
- Expected result:
  - Unreviewed checks run sequentially and do not block the wrapper solely because they are absent from the allowlist.
- Failure proves:
  - The wrapper either parallelizes unsafe checks or turns conservative default behavior into a false failure.
- Automation location:
  - `python scripts/test-select-validation.py`

### T8. Default failure behavior waits for all started checks

- Covers: `R6`, `R12`, `E4`, `EC5`, `AC4`
- Level: integration
- Fixture/setup:
  - selector fixture with two allowlisted checks
  - fake scripts where one exits nonzero quickly and the other finishes later
- Steps:
  - Run with `--jobs 2` and without `--fail-fast`.
  - Assert both checks started.
  - Assert the slower started check is allowed to finish.
  - Assert the wrapper exits nonzero after reporting both final statuses.
- Expected result:
  - Default execution is run-to-completion for started checks and does not hide sibling results.
- Failure proves:
  - Contributors lose useful failure information after the first failing check.
- Automation location:
  - `python scripts/test-select-validation.py`

### T9. `--fail-fast` cancels queued checks without hiding started checks

- Covers: `R7`-`R7c`, `R11`, `E5`, `EC6`, `AC4`
- Level: integration
- Fixture/setup:
  - selector fixture with at least three allowlisted checks
  - `--jobs 1` or a controlled `--jobs 2` setup that leaves at least one check queued
  - fake scripts where the first started check fails
- Steps:
  - Run with `--fail-fast`.
  - Assert queued checks after the observed failure do not start.
  - Assert already-started checks report their final status.
  - Assert skipped queued checks are reported as not started because fail-fast cancelled the remaining queue.
  - Assert the wrapper exits nonzero.
- Expected result:
  - Fail-fast saves queued work without erasing the state of checks already in progress.
- Failure proves:
  - The required fail-fast flag either has no effect or drops necessary failure attribution.
- Automation location:
  - `python scripts/test-select-validation.py`

### T10. Per-check output capture is deterministic and verbose is stable

- Covers: `R8`-`R8b`, `R9`-`R10b`, `AC5`, `AC6`
- Level: integration
- Fixture/setup:
  - selector fixture with passing and failing selected checks
  - fake scripts that write distinguishable stdout and stderr lines
- Steps:
  - Run without `--verbose`.
  - Assert wrapper stdout/stderr does not contain live interleaved script output before the summary.
  - Assert failed check output appears after the summary in selector order.
  - Assert successful output is hidden.
  - Run again with `--verbose`.
  - Assert successful output is printed in the same stable order as selected checks.
  - Assert stdout and stderr sections remain distinguishable in reporting.
- Expected result:
  - Parallel execution produces readable, deterministic logs with full failed output and optional successful output.
- Failure proves:
  - Log interleaving or unstable ordering can make failures difficult to triage.
- Automation location:
  - `python scripts/test-select-validation.py`

### T11. Decode failures and large output stay isolated per check

- Covers: `R8b`, `R8c`, `R9c`, `EC7`, `EC8`, `AC5`
- Level: integration
- Fixture/setup:
  - byte-capturing CI test helper that does not decode wrapper output before assertions
  - fake script emitting invalid UTF-8 bytes
  - fake script emitting enough output to exercise the implementation's capture path
- Steps:
  - Run the wrapper with a selected check that emits invalid UTF-8.
  - Assert the scheduler does not crash with an unhandled decode exception.
  - Assert the affected check has a decode-failure reporting note and nonzero status if the implementation treats undecodable output as failed.
  - Run with large stdout/stderr output from two checks.
  - Assert output from one check does not appear inside the other check's report section.
- Expected result:
  - Output decoding happens at reporting boundaries and capture storage remains per-check.
- Failure proves:
  - A single unusual output stream can crash or corrupt the entire wrapper report.
- Automation location:
  - `python scripts/test-select-validation.py`

### T12. Per-check timeout is distinct and excludes queue wait

- Covers: `R3`-`R3e`, `R9b`, `R11`, `R12`, `E6`, `EC9`, `AC7`
- Level: integration
- Fixture/setup:
  - selector fixture with queued selected checks
  - fake script that sleeps past the configured timeout
  - fake script that waits in the queue before running but exits quickly once started
- Steps:
  - Run with omitted `--timeout` and a fake script that exceeds the default 60 seconds, or use a shorter override for the automated test while separately asserting the default constant is 60.
  - Run with `--timeout 1` to keep the regression test fast.
  - Assert timed-out checks are reported as timed out rather than ordinary exit failures.
  - Assert the wrapper exits nonzero.
  - Assert elapsed runtime is measured from process start to process exit and does not include queue wait time.
- Expected result:
  - Timeout behavior catches hangs, is attributable to the check ID, and reports elapsed time for the leaf process only.
- Failure proves:
  - Hangs can stall the wrapper, or queueing can produce misleading timeout and elapsed-runtime data.
- Automation location:
  - `python scripts/test-select-validation.py`

### T13. Signal-killed checks are reported distinctly

- Covers: `R9b`, `R11`, `R12`, `EC10`, `AC7`
- Level: integration
- Fixture/setup:
  - POSIX-capable environment
  - fake script that terminates itself with a signal or is killed by a helper process
- Steps:
  - Run the wrapper with the signal-kill fixture.
  - Assert the summary status distinguishes killed-by-signal from ordinary nonzero exit.
  - Assert the signal name or signal number is visible with the responsible check ID.
  - Assert the wrapper exits nonzero.
- Expected result:
  - Signal failures are diagnosable without guessing from a raw return code.
- Failure proves:
  - OOM, manual kill, and other signal failures can be misreported as generic exit failures.
- Automation location:
  - `python scripts/test-select-validation.py`

### T14. Selector trust boundaries reject unknown and unavailable commands

- Covers: `R1`, `R11`-`R14`, `R13a`, `EC12`, `AC7`
- Level: integration
- Fixture/setup:
  - selector fixture with an unknown check ID and a marker-writing command
  - selector fixture with a known check ID but tampered command
  - temporary workspace missing the executable for a known catalog command
- Steps:
  - Run the unknown ID fixture.
  - Assert the wrapper fails before running the marker command and identifies the unknown ID.
  - Run the tampered known-ID command fixture.
  - Assert existing command-mismatch protection still prevents execution.
  - Run the unavailable command fixture.
  - Assert output identifies both the check ID and unavailable command.
- Expected result:
  - The wrapper never executes unknown or mismatched selector commands and reports unavailable commands with actionable evidence.
- Failure proves:
  - Selector output can bypass catalog trust boundaries or produce ambiguous command failures.
- Automation location:
  - `python scripts/test-select-validation.py`

### T15. Broad-smoke behavior remains non-recursive and leaf-bounded

- Covers: `R3c`, `R15`, `R15a`, `E7`, `EC13`
- Level: integration, smoke
- Fixture/setup:
  - existing `RIGORLOOP_CI_BROAD_SMOKE_STUB`
  - selector fixture selecting `broad_smoke.repo`
  - timeout override for a leaf check where implementation exposes broad-smoke leaf execution through the shared result runner
- Steps:
  - Run direct `bash scripts/ci.sh --mode broad-smoke` with malformed selector fixture data and the broad-smoke stub.
  - Assert direct broad smoke does not parse selector fixture JSON.
  - Run selected `broad_smoke.repo` through `--mode explicit`.
  - Assert selected broad smoke delegates to the non-recursive broad-smoke path.
  - Verify timeout behavior for broad-smoke leaf checks through the shared selected-check timeout mechanism or record why direct broad-smoke leaf timeout cannot be automated in this slice.
- Expected result:
  - Existing broad-smoke semantics remain intact, and timeout behavior is attached to leaf work rather than an extra recursive wrapper layer.
- Failure proves:
  - The wrapper can recurse through the selector unexpectedly or apply timeout behavior at the wrong boundary.
- Automation location:
  - `python scripts/test-select-validation.py`
  - direct `bash scripts/ci.sh --mode broad-smoke` during final validation

### T16. Existing selector and wrapper boundary behavior remains compatible

- Covers: `R1`, `R16`, `R16a`, compatibility behavior
- Level: integration
- Fixture/setup:
  - existing selector fixtures for `blocked`, `fallback`, malformed JSON, no selected checks, and mode argument forwarding
- Steps:
  - Keep existing wrapper tests for blocked selector output, fallback rejection, malformed JSON, selected command failure, no-selected-check success, and mode argument forwarding.
  - Run no-argument `bash scripts/ci.sh` only through the existing legacy broad-smoke expectation, not as the normal targeted proof path.
  - Assert selected-check execution does not start for selector statuses that already blocked execution before this change.
- Expected result:
  - Bounded parallelism does not weaken existing selector/wrapper safety behavior.
- Failure proves:
  - The implementation changed compatibility semantics outside the approved speed-optimization slice.
- Automation location:
  - `python scripts/test-select-validation.py`

### T17. Contributor guidance and hosted CI remain thin and matrix-free

- Covers: `R17`, `R18`, `R19`, `R20`, `EC14`, `AC9`
- Level: contract
- Fixture/setup:
  - `docs/workflows.md`
  - `.github/workflows/ci.yml`
- Steps:
  - Assert `docs/workflows.md` documents `--jobs`, `--jobs 1`, `--timeout`, `--fail-fast`, and `--verbose` after implementation.
  - Assert `.github/workflows/ci.yml` still calls `scripts/ci.sh`.
  - Assert workflow YAML does not contain `matrix:`, hardcoded stable check-ID lists as matrix axes, path classification rules, persistent caching steps, distributed execution setup, or sandbox runner setup.
  - Assert any hosted-environment details remain in workflow YAML and selection logic remains in repo-owned scripts.
- Expected result:
  - Contributors can discover the new wrapper flags, and hosted CI remains a thin caller of repository validation logic.
- Failure proves:
  - The first slice accidentally becomes a hosted CI redesign or duplicates repo-owned routing.
- Automation location:
  - `python scripts/test-select-validation.py`
  - final inspection command: `rg -n "matrix:|check-id:|fromJson|actions/cache|select-validation|scripts/ci.sh" .github/workflows/ci.yml docs/workflows.md`

### T18. Initial six regression checks pass under bounded parallelism

- Covers: `R4d`, `R17`-`R19`, `E1`, `AC2`, `AC8`
- Level: smoke
- Fixture/setup:
  - repository working tree with implementation changes
  - six reviewed regression script paths from the proposal
- Steps:
  - Run `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path scripts/test-adapter-distribution.py --path scripts/test-change-metadata-validator.py --path scripts/test-review-artifact-validator.py --path scripts/test-select-validation.py --path scripts/test-artifact-lifecycle-validator.py --jobs 6`.
  - Confirm all six selected regression checks pass.
  - Confirm the wrapper summary shows stable check IDs and elapsed runtime for each selected check.
  - Run `bash scripts/ci.sh --mode broad-smoke` before PR readiness.
- Expected result:
  - The reviewed initial allowlist is useful in the real repository, and broad-smoke compatibility remains proven.
- Failure proves:
  - The real initial candidates are not safe or the wrapper cannot execute the intended rollout path.
- Automation location:
  - plan validation notes and final verification evidence

### T19. Output capture and parallel-safe evidence do not dirty tracked paths

- Covers: `R5`, security and privacy requirements, `R20`
- Level: integration, manual evidence review
- Fixture/setup:
  - clean temporary workspace or tracked-path snapshot
  - selected fake checks that write output and scratch data
  - implementation evidence for the six reviewed regression scripts
- Steps:
  - Run selected fake checks that create scratch data only under process-unique temporary directories.
  - Assert no tracked repository paths are created or modified by wrapper output capture.
  - Assert wrapper-created temporary paths, if any, are process-unique.
  - Inspect wrapper logs for newly introduced secrets, tokens, private keys, or unrelated machine-local sensitive paths.
  - Record safety evidence for the six initial allowlisted regression checks against tracked writes, scratch paths, shared external resources, and stdout/stderr-only runtime output.
- Expected result:
  - Parallel execution and output capture do not create tracked artifacts or leak new sensitive data.
- Failure proves:
  - The wrapper can introduce repository dirtiness, shared scratch collisions, or privacy-sensitive log output.
- Automation location:
  - `python scripts/test-select-validation.py`
  - implementation review or final verify notes for the recorded safe-check evidence

## Fixtures and data

- Existing selector fixture hooks:
  - `RIGORLOOP_SELECTOR_FIXTURE`
  - `RIGORLOOP_SELECTOR_FIXTURE_EXIT`
  - `RIGORLOOP_CI_SELECTOR_ARGV_FILE`
  - `RIGORLOOP_CI_BROAD_SMOKE_STUB`
- Temporary workspaces should copy `scripts/ci.sh` and `scripts/validation_selection.py`, then create fake scripts at existing catalog command paths such as `scripts/test-skill-validator.py` and `scripts/test-adapter-distribution.py`.
- Fake scripts should coordinate through process-unique temporary directories created by the test harness. They may write marker files, sleep briefly, emit stdout/stderr, emit invalid bytes, exit nonzero, or terminate by signal.
- Concurrency assertions should rely on marker files, peer-start barriers, or file locks rather than elapsed wall-clock time alone.
- CPU-count behavior should be tested through an implementation helper or test fixture hook that does not become a documented user-facing configuration surface.
- Large-output fixtures should be large enough to exercise the implementation's capture mechanism without making tests slow or memory-heavy.

## Mocking/stubbing policy

- Stub the selector only through the existing fixture environment variables.
- Stub selected commands by creating temporary fake scripts at real catalog command paths; do not add test-only check IDs to the production catalog.
- Do not stub `scripts/ci.sh` itself for behavior tests. Run the real wrapper script.
- Do not stub hosted CI execution. Inspect `.github/workflows/ci.yml` as a tracked contract surface.
- Do not use network services, fixed ports, global Git configuration mutation, or shared lockfiles in tests.

## Migration or compatibility tests

- Existing wrapper modes `local`, `explicit`, `pr`, `main`, `release`, and `broad-smoke` remain covered by `T2` and `T16`.
- Existing no-argument `bash scripts/ci.sh` legacy broad-smoke behavior remains covered by `T16` and final broad-smoke validation.
- Existing selector blocking, fallback, malformed-output, command-mismatch, command-unavailable, and selected-command-failure tests must remain in `scripts/test-select-validation.py`.
- Rollback compatibility is covered by `T5`: `--jobs 1` remains the explicit sequential fallback.

## Observability verification

- `T5`, `T10`, `T11`, `T12`, `T13`, and `T14` verify that wrapper output names selected check IDs, status, exit reason, elapsed runtime, and relevant commands.
- Failed check output must appear after the summary in stable order.
- Successful check output must be hidden by default and shown with `--verbose` in stable order.
- Timeout, signal-kill, unavailable-command, unknown-ID, and nonzero-exit failures must be attributable to the responsible check ID.
- Normal output must not include interleaved live logs from parallel child processes.

## Security/privacy verification

- `T14` proves unknown check IDs and mismatched commands are not executed.
- `T19` proves wrapper output capture does not write tracked repository paths, uses process-unique temporary paths when temporary storage exists, and does not introduce new secret or machine-local path leakage beyond underlying validation command output.
- Tests must avoid real secrets and must not require hosted credentials.

## Performance checks

- `T4` verifies default and effective concurrency are bounded.
- `T6` verifies concurrent start for allowlisted checks without relying only on timing.
- `T18` verifies the real initial six regression checks run through `scripts/ci.sh --jobs 6`.
- The test spec does not require a fixed wall-clock improvement threshold. Local CPU and I/O conditions vary; the required proof is that bounded concurrency is actually used and that the real initial allowlist passes under that execution shape.

## Manual QA checklist

- Confirm recorded safety evidence exists for the six initial parallel-safe regression check IDs before marking M1 complete.
- Confirm `docs/workflows.md` names the new flags and preserves selector-selected proof guidance after M4.
- Confirm `.github/workflows/ci.yml` remains matrix-free and delegates to `scripts/ci.sh`.
- Confirm final validation notes include the exact commands run for selector-selected proof, six-check parallel proof, and direct broad smoke.

## What not to test

- Do not test GitHub Actions matrix fan-out; `R18` excludes it from this slice.
- Do not test persistent caching, dependency caching, input-hash skip logic, distributed execution, or per-check sandboxing; `R19` excludes them from this slice.
- Do not test dynamic priority scheduling or longest-job-first behavior; stable-order FIFO with a concurrency cap is enough for this scope.
- Do not add tests for exact speedup percentages or runner-minute cost. The contract is bounded concurrency with deterministic output, not a portable benchmark.
- Do not retest every validator's internal behavior through the wrapper. Existing validator-specific tests remain the owner of validator correctness.

## Uncovered gaps

- None known. If implementation cannot make CPU-count defaulting, broad-smoke leaf timeout behavior, or output-capture storage failure deterministic enough for automated proof, record the limitation in the active plan and return to spec or plan review before treating that requirement as satisfied manually.

## Next artifacts

- `implement` for M1 after this active test spec passes lifecycle validation.
- `code-review`, `verify`, `explain-change`, and `pr` after the implementation milestones close.

## Follow-on artifacts

- None yet.

## Readiness

This active test spec is the current proof-planning surface for `specs/test-and-ci-speed-optimization.md` and `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`.

After lifecycle validation passes for this test spec, implementation is ready to start at M1.
