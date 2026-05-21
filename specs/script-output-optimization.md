# Script Output Optimization

## Status

approved

## Related proposal

- [RigorLoop Script Output Optimization](../docs/proposals/2026-05-21-script-output-optimization.md), accepted.

## Goal and context

RigorLoop validation and test scripts should make passing evidence compact and failure evidence actionable. This spec defines the first-slice behavior for user-facing script output around `scripts/test-select-validation.py` and the minimal `scripts/ci.sh` wrapper boundary needed to preserve quiet-success and loud-failure behavior.

The change is presentation-only. It must not change validation coverage, selected checks, failure detection, or exit-code semantics.

## Glossary

- **Default mode**: Script execution without `--verbose` or `--quiet`.
- **Verbose mode**: Execution with `--verbose` or `-v`, exposing passing check detail that default mode suppresses.
- **Quiet mode**: Execution with `--quiet` or `-q`, suppressing success output while preserving failure reasons.
- **Summary line**: A single line that reports status, suite/check name, count, and duration when applicable.
- **Failure detail**: Failed test/check name, assertion or error message, file location when available, and reliable rerun command when available.
- **Scoped rerun command**: A rerun command that targets the failed check through a stable, exact filter.
- **Behavior-preservation matrix**: Change evidence comparing baseline and new behavior for exit codes, selected checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when touched.

## Examples first

Example E1: default success is summarized
Given `scripts/test-select-validation.py` runs 62 tests successfully
When the script is run in default mode
Then output contains one summary line like `[PASS] test-select-validation: 62 passed in 7.77s`
And output does not list every passing test.

Example E2: default failure shows actionable detail
Given `scripts/test-select-validation.py` runs 62 tests and 2 fail
When the script is run in default mode
Then output starts with `[FAIL] test-select-validation: 2 failed, 60 passed in 7.81s`
And output includes each failed test name, failure message, and file location when available
And passing test detail is collapsed into the summary count.

Example E3: verbose mode preserves full pass detail
Given `scripts/test-select-validation.py` has passing tests
When the script is run with `--verbose`
Then output includes the full passing-test detail available before this change
And the command exit code is unchanged.

Example E4: quiet success prints nothing
Given `scripts/test-select-validation.py` passes
When the script is run with `--quiet`
Then stdout is empty
And stderr is empty
And the command exits with the same success code as default mode.
Quiet mode does not suppress diagnostics for non-success outcomes.

Example E5: quiet failure still explains failure
Given `scripts/test-select-validation.py` fails
When the script is run with `--quiet`
Then output includes the failure summary and failure detail needed to repair the issue
And the maintainer does not need to rerun with `--verbose` to learn why it failed.

Example E6: scoped rerun is reliable or absent
Given a failed check has a stable exact filter
When the script prints failure detail
Then the script may print a scoped rerun command such as `Re-run: python scripts/test-select-validation.py -k "test_name"`
But if the filter cannot be generated safely, the script omits the scoped rerun command or prints a safe broader command.

Example E7: zero executed tests do not look like success
Given `scripts/test-select-validation.py` expects at least one executed test
When no tests execute
Then output includes a failure summary such as `[FAIL] test-select-validation: 0 tests run; expected at least 1 selected test`
And the command exits with a failure code unless an explicit audit, list, or dry-run mode allows zero selection.

Example E8: CI wrapper stays failure-focused
Given `scripts/ci.sh` runs selected checks
When selected checks pass
Then the wrapper continues to hide successful child output by default and report stable check status
When a selected check fails
Then the wrapper surfaces failed check output and preserves enough detail to repair the failure.

Example E9: conflicting output flags fail before tests run
Given `scripts/test-select-validation.py` supports `--verbose` and `--quiet`
When the script is run with both `--verbose` and `--quiet`
Then the command exits with a nonzero usage error
And stdout is empty
And stderr names both `--verbose` and `--quiet`
And no tests are selected or run
And no success, failure, or selected-check summaries are printed.

## Requirements

R1. First-slice summary output MUST use bracketed ASCII status words: `[PASS]`, `[FAIL]`, and `[SKIP]` when a skip state is applicable.

R2. Default successful output for `scripts/test-select-validation.py` MUST be one summary line containing the suite name, nonzero passed count, and duration.

R3. Default successful output for `scripts/test-select-validation.py` MUST NOT list individual passing tests.

R4. Default failure output for `scripts/test-select-validation.py` MUST include a summary line with failed count, passed count when known, suite name, and duration.

R5. Default failure output for `scripts/test-select-validation.py` MUST include each failed test/check name.

R6. Default failure output for `scripts/test-select-validation.py` MUST include the assertion or error message for each failure when available.

R7. Default failure output for `scripts/test-select-validation.py` MUST include a file location for each failure when the runner can derive one.

R8. Passing test/check detail MUST collapse into summary counts in default failure output.

R9. `scripts/test-select-validation.py` MUST support `--verbose` and `-v`.

R10. Verbose mode MUST preserve access to the full pass/check listing that default mode suppresses.

R11. `scripts/test-select-validation.py` MUST support `--quiet` and `-q`.

R12. When `scripts/test-select-validation.py --quiet` completes successfully, it MUST write no output to stdout or stderr.

R12a. The quiet-success no-output contract applies only to successful outcomes. Non-success outcomes, including usage errors, validation errors, test failures, and zero-test safety failures, MAY write bounded actionable diagnostics.

R13. Quiet-mode failure MUST print the same failure summary and failure details as default failure mode.

R14. Failure reasons MUST NOT be hidden behind `--verbose`.

R15. `scripts/test-select-validation.py` MUST preserve pass and failure exit codes across default, verbose, and quiet modes, except where the approved zero-test behavior turns a previously ambiguous zero-test success into a defined failure.

R15a. `scripts/test-select-validation.py` MUST treat `--verbose` and `--quiet` as mutually exclusive.

R15b. When `--verbose` and `--quiet` are both provided, `scripts/test-select-validation.py` MUST reject the invocation with a nonzero usage error before selecting or running tests.

R15c. The combined-flag diagnostic MUST name both `--verbose` and `--quiet`, MUST be written to stderr, and MUST leave stdout empty.

R15d. Combined-flag rejection MUST NOT print success, failure, or selected-check summaries.

R16. Zero executed tests MUST be a failure for first-slice test-runner behavior when the suite expects at least one test.

R17. Zero selected checks MAY be non-failing only for an explicit audit, list, or dry-run mode that documents zero selection as allowed.

R18. A zero-test failure MUST explain why no tests or checks were selected or run when that reason is available.

R19. Scoped rerun commands MUST be emitted only when the runner supports a stable name filter, the failed check ID maps exactly to that filter, the filter is known to select the intended check, and quoting can be generated safely.

R20. A missing scoped rerun command MUST be acceptable when R19 cannot be satisfied.

R21. A wrong or misleading rerun command MUST be treated as a defect.

R22. When a reliable scoped rerun command cannot be generated, failure output MAY omit the rerun command or print a safe broader command such as `Re-run: python scripts/test-select-validation.py`.

R23. The first slice MUST NOT add new `--json` support to scripts that lack it.

R24. If a touched script already has stable `--json` output, the change MUST preserve that output's existing behavior.

R25. The first slice MUST include a script-output audit under `docs/changes/<change-id>/script-output-audit.md`.

R26. The audit MUST record, for each assessed candidate script, script path, whether it is user-facing, approximate current success-line count, current failure usefulness, proposed treatment, and whether it is in the first slice.

R27. The first implementation slice MUST target `scripts/test-select-validation.py`.

R28. `scripts/ci.sh` MUST be changed only when the audit or runner change shows the wrapper must change to preserve quiet-on-success and loud-on-failure behavior.

R29. If `scripts/ci.sh` is touched, it MUST preserve the existing selected-check execution semantics, wrapper modes, check coverage, and child-process exit behavior.

R30. `scripts/ci.sh` MUST continue to hide successful child-check output by default and expose successful check output with `--verbose` in stable order.

R31. `scripts/ci.sh` MUST surface failed check output in stable order with the responsible check ID, status, exit reason, elapsed runtime, and relevant command information.

R32. Output optimization MUST NOT change validation behavior, selected checks, failure detection, required repair evidence, or exit-code semantics beyond the defined zero-test failure behavior.

R33. Implementation evidence MUST include a behavior-preservation matrix for each touched script.

R34. The behavior-preservation matrix MUST compare baseline and new proof for pass exit code, failure exit code, selected tests/checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when `scripts/ci.sh` is touched.

R35. Output-shape tests MUST cover default success, default failure, verbose success, quiet success, quiet failure, zero-test failure, reliable scoped rerun behavior, unreliable rerun omission or broader rerun behavior, and JSON deferral/preservation behavior.

## Inputs and outputs

Inputs:

- Command-line invocation of `scripts/test-select-validation.py`.
- Optional `--verbose` / `-v`.
- Optional `--quiet` / `-q`.
- Existing `scripts/ci.sh` invocations, including explicit, local, PR, main, release, and broad-smoke modes when wrapper behavior is relevant.

Outputs:

- Human-readable stdout/stderr summaries and failure details.
- Process exit code.
- Change-local audit and behavior-preservation evidence.

No new machine-readable JSON output is introduced in the first slice.

## State and invariants

- Selected tests and checks remain the same for equivalent inputs.
- Failure detection remains the same for equivalent inputs.
- Required failure evidence remains visible in default and quiet failure modes.
- Verbose mode remains the escape hatch for full pass/check detail.
- Quiet mode never hides failure reasons.
- A shorter success log is not valid if it changes selected checks, exit codes, or failure detection.

## Error and boundary behavior

- Unknown output flags fail according to the script's existing argument-parsing behavior.
- `--verbose` and `--quiet` are mutually exclusive.
- When both `--verbose` and `--quiet` are provided, `scripts/test-select-validation.py` rejects the invocation with a nonzero usage error before selecting or running tests. The diagnostic names both flags, writes to stderr, leaves stdout empty, and does not print success, failure, or selected-check summaries.
- Zero executed tests fail unless an explicit mode documents zero selection as allowed.
- Rerun commands are omitted or broadened when exact safe quoting cannot be generated.
- CI wrapper failures continue to identify the responsible check ID and failure reason.

## Compatibility and migration

This is a presentation change for user-facing script output. Existing validation semantics, selector behavior, check coverage, CI wrapper modes, and exit-code behavior remain compatible except for the defined zero-test failure boundary.

Local users who need the old full pass-list behavior use `--verbose`. CI logs become shorter on success but retain failure output. Rollback restores the previous output formatter while preserving validation behavior and any tests that still match the restored contract.

## Observability

- Success output reports suite/check identity, counts, and duration.
- Failure output reports failed names, messages, locations when available, and reliable rerun guidance when available.
- CI wrapper output continues to report selected check IDs, statuses, exit reasons, elapsed runtime, and relevant command information.
- The audit and behavior-preservation matrix provide durable review evidence for the presentation-only claim.

## Security and privacy

The change must not introduce secrets, credentials, private keys, tokens, machine-local paths, or unnecessary environment dumps into output. Failure output may include existing file paths and command text needed for repair, but new output formatting must not expand sensitive data exposure beyond underlying validation output.

## Accessibility and UX

First-slice status markers use ASCII words rather than glyph-only signals so logs remain readable in terminals, CI systems, plain text, and copied excerpts. Color must not be required to understand status.

## Performance expectations

Output shaping must not materially increase validation runtime. Duration measurement should use the script's actual execution interval and should not require rerunning tests or checks.

## Edge cases

EC1. A passing suite with many tests prints one summary line and no pass list in default mode.

EC2. A failing suite with many passing tests prints failed details and collapses passing tests into counts.

EC3. `--quiet` success prints nothing.

EC4. `--quiet` failure prints enough detail to repair the failure without rerunning with `--verbose`.

EC5. `--verbose` success prints full pass/check detail.

EC6. `--verbose --quiet` exits with a nonzero usage error, writes no stdout, names both flags in stderr, and runs no tests.

EC7. Zero executed tests fail unless the mode explicitly allows zero selection.

EC8. A failed check with a reliable exact filter prints a scoped rerun command.

EC9. A failed check without a reliable exact filter omits scoped rerun or prints only a safe broader rerun command.

EC10. Rerun command quoting containing spaces or shell-sensitive characters is safe or the command is omitted.

EC11. Existing JSON output, if any, is preserved; missing JSON output is not added.

EC12. `scripts/ci.sh` is unchanged when the audit proves wrapper behavior already preserves quiet-success and loud-failure behavior.

EC13. `scripts/ci.sh` is touched only minimally when needed and continues to hide successful child output by default.

## Non-goals

- Do not change what any script validates.
- Do not change selected-check logic.
- Do not change failure detection.
- Do not remove required validation evidence.
- Do not make CI logs silent when failures occur.
- Do not require all scripts to emit identical formats outside the first slice.
- Do not change generated adapter output, skill files, workflow specs, or validation selection logic as part of this first slice.
- Do not replace the existing test framework.
- Do not add new JSON output support in the first slice.
- Do not introduce a common script-output helper library in the first slice.

## Acceptance criteria

AC1. `scripts/test-select-validation.py` default success output is one `[PASS]` summary line with suite name, nonzero pass count, and duration.

AC2. `scripts/test-select-validation.py` default success output hides individual passing checks.

AC3. `scripts/test-select-validation.py` default failure output includes `[FAIL]` summary, failed names, failure messages, and locations when available.

AC4. `scripts/test-select-validation.py --verbose` exposes full pass/check detail.

AC5. `scripts/test-select-validation.py --quiet` success writes no output to stdout or stderr.

AC5a. `scripts/test-select-validation.py --quiet` failure may emit bounded actionable diagnostics, but does not emit success summaries.

AC6. `python scripts/test-select-validation.py --verbose --quiet` exits with a nonzero usage error before tests are selected or run, names both flags in stderr, leaves stdout empty, and prints no success, failure, or selected-check summaries.

AC7. Zero executed tests fail unless an explicit mode allows zero selection.

AC8. Scoped rerun commands appear only when reliable; an unreliable scoped command is not emitted.

AC9. New `--json` support is not added in the first slice, and existing JSON output is preserved if present.

AC10. Script-output audit exists under `docs/changes/<change-id>/script-output-audit.md` and identifies first-slice treatment.

AC11. Behavior-preservation matrix exists for each touched script and proves exit codes, selected checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when touched.

AC12. If `scripts/ci.sh` is touched, it continues to hide successful child output by default and show successful child output with `--verbose` in stable order.

AC13. If `scripts/ci.sh` is touched, failed child output is expanded with responsible check ID, status, exit reason, elapsed runtime, and relevant command information.

AC14. No generated adapters, public skill files, workflow specs, or validation selection logic are changed unless a later approved artifact expands scope.

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec for output-shape and behavior-preservation behavior
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Canonical architecture update: `docs/architecture/system/architecture.md`

## Readiness

Approved after `spec-review-r2`. Ready for architecture handling, then downstream planning and test-spec work.
