# Script Output Optimization Test Spec

## Status

- active

## Related spec and plan

- Spec: [Script Output Optimization](script-output-optimization.md), approved.
- Proposal: [RigorLoop Script Output Optimization](../docs/proposals/2026-05-21-script-output-optimization.md), accepted.
- Plan: [Script Output Optimization](../docs/plans/2026-05-21-script-output-optimization.md), active.
- Architecture: [System architecture](../docs/architecture/system/architecture.md), updated and approved by `architecture-review-r1`.
- Spec review: `spec-review-r2` approved the spec after `SRO-SR1` and `SRO-SR2` were resolved.
- Plan review: `plan-review-r1` approved the plan with no material findings.

## Testing strategy

- Unit tests cover the result-formatting and argument-boundary behavior that can be isolated inside `scripts/test-select-validation.py`, including summary-line fields, quiet success, conflicting output flags, zero-test handling, and rerun-command eligibility.
- Integration tests execute `scripts/test-select-validation.py` as a subprocess where stdout, stderr, and exit code are observable. They should use deterministic fixture cases or helper entry points rather than relying on the real repository suite failing.
- End-to-end tests run the changed runner through `scripts/ci.sh` to prove wrapper behavior remains quiet on successful child output by default, exposes successful output with wrapper `--verbose`, and surfaces failed child output when relevant.
- Smoke tests run the normal selected validation path for touched files after implementation.
- Manual verification is limited to durable audit and behavior-preservation evidence where baseline/new comparison is review evidence rather than pure executable behavior.
- Contract tests inspect the audit, behavior-preservation matrix, and changed-path set to prove no generated adapter output, public skill files, workflow specs, validation-selection logic, or broad CI behavior changed outside the approved scope.
- Migration/compatibility tests prove the old full pass/check detail remains available through `--verbose` and that JSON support is not newly introduced.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | TSRO-002, TSRO-003, TSRO-007 | integration | Asserts bracketed ASCII status words for pass, fail, and zero-test failure. |
| R2 | TSRO-002 | integration | Asserts one default success summary with suite, nonzero count, and duration. |
| R3 | TSRO-002 | integration | Asserts default success suppresses individual passing tests. |
| R4 | TSRO-003 | integration | Asserts default failure summary fields. |
| R5 | TSRO-003 | integration | Asserts failed test/check names are shown. |
| R6 | TSRO-003 | integration | Asserts assertion or error messages are shown when available. |
| R7 | TSRO-003 | integration | Asserts file location appears when derivable. |
| R8 | TSRO-003 | integration | Asserts passing detail collapses into counts during failure. |
| R9 | TSRO-004 | integration | Asserts `--verbose` and `-v` are accepted. |
| R10 | TSRO-004 | integration, migration | Asserts full pass/check detail remains available in verbose mode. |
| R11 | TSRO-005 | integration | Asserts `--quiet` and `-q` are accepted. |
| R12 | TSRO-005 | integration | Asserts quiet success writes no stdout or stderr. |
| R12a | TSRO-005, TSRO-006, TSRO-007 | integration | Asserts non-success diagnostics remain allowed and actionable. |
| R13 | TSRO-005 | integration | Asserts quiet failure prints the same failure summary and detail as default failure. |
| R14 | TSRO-003, TSRO-005 | integration | Asserts failure reasons are not hidden behind verbose mode. |
| R15 | TSRO-002, TSRO-003, TSRO-004, TSRO-005, TSRO-010 | integration, manual | Asserts pass/failure exit codes remain preserved, except zero-test safety. |
| R15a | TSRO-006 | integration | Asserts `--verbose` and `--quiet` are mutually exclusive. |
| R15b | TSRO-006 | integration | Asserts combined flags fail before tests are selected or run. |
| R15c | TSRO-006 | integration | Asserts stderr names both flags and stdout is empty. |
| R15d | TSRO-006 | integration | Asserts no success, failure, or selected-check summaries are printed for combined flags. |
| R16 | TSRO-007 | integration | Asserts zero executed tests fail when the suite expects tests. |
| R17 | TSRO-007 | integration | Asserts only explicit audit/list/dry-run modes may allow zero selected checks. |
| R18 | TSRO-007 | integration | Asserts zero-test failure explains why no tests/checks ran when available. |
| R19 | TSRO-008 | unit, integration | Asserts scoped rerun appears only when stable exact filter and safe quoting are proven. |
| R20 | TSRO-008 | integration | Asserts missing scoped rerun is acceptable when reliability cannot be proven. |
| R21 | TSRO-008 | integration | Asserts misleading partial scoped rerun commands are not emitted. |
| R22 | TSRO-008 | integration | Asserts omitted or safe broader rerun command behavior. |
| R23 | TSRO-009 | contract | Asserts no new `--json` support is added when absent. |
| R24 | TSRO-009 | contract, migration | Asserts existing stable JSON, if present, is preserved. |
| R25 | TSRO-001 | manual, contract | Asserts script-output audit exists at the change-local path. |
| R26 | TSRO-001 | manual, contract | Asserts audit includes required fields for each assessed candidate. |
| R27 | TSRO-001, TSRO-002, TSRO-003, TSRO-004, TSRO-005, TSRO-006, TSRO-007, TSRO-008, TSRO-009, TSRO-010 | contract | Asserts first implementation target is `scripts/test-select-validation.py`. |
| R28 | TSRO-001, TSRO-011, TSRO-012 | integration, manual | Asserts `scripts/ci.sh` changes only when audit or runner proof shows need. |
| R29 | TSRO-012 | integration | Applies only if `scripts/ci.sh` is touched; asserts existing wrapper modes and child exit behavior remain unchanged. |
| R30 | TSRO-011, TSRO-012 | integration | Asserts successful child output is hidden by default and exposed with wrapper `--verbose`. |
| R31 | TSRO-011, TSRO-012 | integration | Asserts failed child output includes responsible check ID, status, exit reason, elapsed runtime, and command information. |
| R32 | TSRO-010, TSRO-013, TSRO-014 | integration, manual, contract | Asserts validation behavior, selected checks, failure detection, repair evidence, and exit-code semantics are preserved. |
| R33 | TSRO-010 | manual, contract | Asserts behavior-preservation matrix exists for each touched script. |
| R34 | TSRO-010 | manual, contract | Asserts matrix compares pass/fail exits, selected checks, failure detection/evidence, verbose output, quiet failure, and conditional CI semantics. |
| R35 | TSRO-002, TSRO-003, TSRO-004, TSRO-005, TSRO-006, TSRO-007, TSRO-008, TSRO-009, TSRO-011, TSRO-012 | integration, contract | Covers all required output-shape cases. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | TSRO-002 | Default success summary and suppressed pass list. |
| E2 | TSRO-003 | Default failure summary and actionable failure detail. |
| E3 | TSRO-004 | Verbose mode preserves full pass detail and exit code. |
| E4 | TSRO-005 | Quiet success has empty stdout/stderr and preserved success exit. |
| E5 | TSRO-005 | Quiet failure still explains why the command failed. |
| E6 | TSRO-008 | Scoped rerun appears only when reliable; otherwise omitted or broadened. |
| E7 | TSRO-007 | Zero executed tests fail instead of looking like success. |
| E8 | TSRO-011, TSRO-012 | Wrapper stays failure-focused, with conditional wrapper patch coverage. |
| E9 | TSRO-006 | Conflicting flags fail before selection/execution. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | TSRO-002 | Many passing tests collapse to one summary line. |
| EC2 | TSRO-003 | Failing run collapses passing details and expands failures. |
| EC3 | TSRO-005 | Quiet success prints nothing. |
| EC4 | TSRO-005 | Quiet failure remains actionable. |
| EC5 | TSRO-004 | Verbose success prints full detail. |
| EC6 | TSRO-006 | Combined output flags reject before tests run. |
| EC7 | TSRO-007 | Zero executed tests fail unless explicitly allowed. |
| EC8 | TSRO-008 | Reliable exact failed-check filter emits scoped rerun. |
| EC9 | TSRO-008 | Unreliable failed-check filter omits scoped rerun or prints broad rerun only. |
| EC10 | TSRO-008 | Unsafe quoting prevents scoped rerun output. |
| EC11 | TSRO-009 | Existing JSON is preserved if present; absent JSON is not added. |
| EC12 | TSRO-011 | `scripts/ci.sh` remains unchanged when existing behavior is sufficient. |
| EC13 | TSRO-012 | Any `scripts/ci.sh` change is minimal and preserves default success hiding. |

## Acceptance criteria coverage

| Acceptance criterion | Covered by | Notes |
| --- | --- | --- |
| AC1 | TSRO-002 | One `[PASS]` success line with suite, count, and duration. |
| AC2 | TSRO-002 | No individual passing checks in default success. |
| AC3 | TSRO-003 | Failure summary, names, messages, and locations when available. |
| AC4 | TSRO-004 | Verbose exposes full pass/check detail. |
| AC5 | TSRO-005 | Quiet success has empty stdout and stderr. |
| AC5a | TSRO-005 | Quiet failure may emit bounded actionable diagnostics but no success summary. |
| AC6 | TSRO-006 | Combined `--verbose --quiet` usage error behavior. |
| AC7 | TSRO-007 | Zero executed tests fail unless explicitly allowed. |
| AC8 | TSRO-008 | Scoped rerun only when reliable. |
| AC9 | TSRO-009 | No new JSON; preserve existing JSON if present. |
| AC10 | TSRO-001 | Audit exists and identifies first-slice treatment. |
| AC11 | TSRO-010 | Behavior-preservation matrix exists and covers required comparisons. |
| AC12 | TSRO-011, TSRO-012 | Conditional wrapper default and verbose success-output behavior. |
| AC13 | TSRO-011, TSRO-012 | Conditional wrapper failed-child output evidence. |
| AC14 | TSRO-013 | No generated adapters, public skill files, workflow specs, or selector logic changes. |

## Test cases

### TSRO-001. Script-output audit records first-slice boundary

- Covers: R23, R24, R25, R26, R27, R28, AC9, AC10, EC11, EC12
- Level: manual, contract
- Fixture/setup: `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`.
- Steps:
  - Inspect the audit after M1.
  - Confirm each candidate row records script path, user-facing status, approximate current success-line count, current failure usefulness, proposed treatment, and first-slice yes/no.
  - Confirm `scripts/test-select-validation.py` is first-slice yes.
  - Confirm `scripts/ci.sh` is conditional and not treated as a broad rewrite target.
  - Confirm JSON support status is recorded for touched scripts.
- Expected result: The audit establishes the first-slice boundary before implementation and records JSON deferral/preservation status.
- Failure proves: The implementation can expand scope or make presentation changes without baseline evidence.
- Automation location: Manual review evidence plus `git diff --check -- docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`.

### TSRO-002. Default success is one count-bearing summary line

- Covers: R1, R2, R3, R15, R27, R32, R35, E1, EC1, AC1, AC2
- Level: integration
- Fixture/setup: A deterministic passing invocation of `scripts/test-select-validation.py` or a test-runner fixture that selects more than one passing test.
- Steps:
  - Run `python scripts/test-select-validation.py` in default mode against the passing fixture.
  - Capture stdout, stderr, exit code, and elapsed command result.
  - Assert exit code is the success exit code.
  - Assert stdout has exactly one success summary line using `[PASS]`.
  - Assert the line includes `test-select-validation`, a nonzero passed count, and a duration.
  - Assert stdout does not include individual passing test/check names.
  - Assert stderr does not contain success detail.
- Expected result: Default success emits one actionable summary line and suppresses pass-list noise.
- Failure proves: Default success remains noisy, loses count/duration evidence, or changes success exit behavior.
- Automation location: `python scripts/test-select-validation.py` self-tests or subprocess tests inside that file.

### TSRO-003. Default failure expands only actionable failure detail

- Covers: R1, R4, R5, R6, R7, R8, R14, R15, R27, R32, R35, E2, EC2, AC3
- Level: integration
- Fixture/setup: A deterministic failing runner fixture with at least two failed checks and at least one passing check.
- Steps:
  - Run `python scripts/test-select-validation.py` in default mode against the failing fixture.
  - Capture stdout, stderr, and exit code.
  - Assert exit code is the failure exit code.
  - Assert output starts with a `[FAIL] test-select-validation` summary containing failed count, passed count when known, and duration.
  - Assert each failed test/check name is present.
  - Assert each available assertion/error message is present.
  - Assert each derivable file location is present.
  - Assert passing check detail is not listed except through counts.
- Expected result: Failure output is concise for passing work and specific for failing work.
- Failure proves: The formatter hides failure reasons, floods failures with pass detail, or changes failure exit semantics.
- Automation location: `python scripts/test-select-validation.py` self-tests or subprocess tests inside that file.

### TSRO-004. Verbose mode preserves full pass detail

- Covers: R9, R10, R15, R27, R35, E3, EC5, AC4
- Level: integration, migration
- Fixture/setup: Passing runner fixture with known passing test/check names.
- Steps:
  - Run default success and record that pass detail is suppressed.
  - Run `python scripts/test-select-validation.py --verbose`.
  - Run `python scripts/test-select-validation.py -v`.
  - Assert both verbose forms exit with the success code.
  - Assert verbose output includes the full pass/check detail available before the output optimization.
  - Assert verbose output still includes enough summary or final status information to identify the suite result.
- Expected result: Maintainers retain the old full detail path behind `--verbose` and `-v`.
- Failure proves: The compatibility escape hatch was removed or aliases behave inconsistently.
- Automation location: `python scripts/test-select-validation.py`.

### TSRO-005. Quiet mode is silent only on success and actionable on failure

- Covers: R11, R12, R12a, R13, R14, R15, R27, R35, E4, E5, EC3, EC4, AC5, AC5a
- Level: integration
- Fixture/setup: Deterministic passing and failing runner fixtures.
- Steps:
  - Run `python scripts/test-select-validation.py --quiet` against the passing fixture.
  - Run `python scripts/test-select-validation.py -q` against the passing fixture.
  - Assert stdout and stderr are empty for successful quiet runs.
  - Assert success exit code matches default success.
  - Run `python scripts/test-select-validation.py --quiet` against the failing fixture.
  - Assert nonzero exit code matches default failure.
  - Assert quiet failure includes the same failure summary and failure details as default failure.
  - Assert quiet failure does not emit a success summary.
- Expected result: Quiet mode supports shell pipelines on success without hiding errors.
- Failure proves: Quiet mode either remains noisy on success or makes failures harder to repair.
- Automation location: `python scripts/test-select-validation.py`.

### TSRO-006. Conflicting output flags fail before tests run

- Covers: R12a, R15a, R15b, R15c, R15d, E9, EC6, AC6
- Level: integration
- Fixture/setup: A traceable test-selection fixture or runner hook that records whether tests were selected or run.
- Steps:
  - Run `python scripts/test-select-validation.py --verbose --quiet`.
  - Run `python scripts/test-select-validation.py --quiet --verbose`.
  - Assert each command exits with a nonzero usage error.
  - Assert stdout is empty.
  - Assert stderr names both `--verbose` and `--quiet`.
  - Assert no `[PASS]`, `[FAIL]`, `[SKIP]`, or selected-check summary appears.
  - Assert the trace fixture shows no tests were selected or run.
- Expected result: Opposing output modes are rejected deterministically before validation work starts.
- Failure proves: Ambiguous flag precedence can hide user intent or partially run validation.
- Automation location: `python scripts/test-select-validation.py`.

### TSRO-007. Zero executed tests fail safely

- Covers: R1, R12a, R16, R17, R18, R27, R35, E7, EC7, AC7
- Level: integration
- Fixture/setup: Runner fixture or helper that selects zero executable tests while the suite expects at least one test; optional explicit audit/list/dry-run fixture if such a mode exists.
- Steps:
  - Run the zero-executed-tests fixture in default mode.
  - Assert nonzero exit code.
  - Assert output contains `[FAIL] test-select-validation` and explains that zero tests/checks ran when the reason is available.
  - Run the same condition with `--quiet` and assert a bounded actionable diagnostic is still allowed.
  - If an explicit audit/list/dry-run mode exists, run that mode and assert zero selection is documented as allowed before treating it as non-failing.
- Expected result: Zero-test collapse is visible and failing unless an explicit mode allows it.
- Failure proves: A broken or empty test suite can masquerade as a successful compact summary.
- Automation location: `python scripts/test-select-validation.py`.

### TSRO-008. Rerun command is emitted only when reliable

- Covers: R19, R20, R21, R22, R27, R35, E6, EC8, EC9, EC10, AC8
- Level: unit, integration
- Fixture/setup: Failure-detail fixtures for a stable exact test ID, an unmappable failure, and a test ID or filter containing shell-sensitive characters.
- Steps:
  - Format failure detail for a failed check whose ID maps exactly to a stable name filter.
  - Assert a scoped rerun command appears and selects the intended check.
  - Format failure detail for a failed check without an exact stable filter.
  - Assert the scoped rerun command is omitted or replaced with the safe broader command `python scripts/test-select-validation.py`.
  - Format failure detail for a failed check whose name cannot be quoted safely.
  - Assert no unsafe or misleading scoped command appears.
- Expected result: Correct rerun commands help iteration, and uncertain commands are absent or safely broad.
- Failure proves: The runner can mislead maintainers into rerunning the wrong check.
- Automation location: `python scripts/test-select-validation.py`.

### TSRO-009. JSON behavior is deferred or preserved

- Covers: R23, R24, R27, R35, EC11, AC9
- Level: contract, migration
- Fixture/setup: Current CLI help/argument behavior for `scripts/test-select-validation.py` and any touched script.
- Steps:
  - Inspect current support for `--json` before implementation.
  - If `scripts/test-select-validation.py` lacks `--json`, assert the first-slice change does not add it.
  - If any touched script already supports stable `--json`, run its pre-change and post-change JSON path and compare the existing contract fields and exit behavior.
  - Record the result in the audit or behavior-preservation matrix.
- Expected result: JSON remains out of scope unless it already exists, and existing JSON behavior is not broken.
- Failure proves: The first slice introduced a separate machine-readable contract without approval or broke an existing one.
- Automation location: `python scripts/test-select-validation.py` for argument behavior; manual preservation evidence when an existing JSON path is present.

### TSRO-010. Behavior-preservation matrix proves presentation-only change

- Covers: R15, R27, R32, R33, R34, AC11
- Level: manual, contract
- Fixture/setup: `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`.
- Steps:
  - Inspect the matrix for every touched script.
  - Confirm rows compare baseline and new proof for pass exit code, failure exit code, selected tests/checks, failure detection, failure evidence, verbose output, quiet failure output, and CI semantics when `scripts/ci.sh` is touched.
  - Confirm the selected test/check set is represented by count/list/hash or another reviewable stable proof.
  - Confirm failures detected before the change are still detected after the change with same or better repair evidence.
  - Confirm the only permitted semantic difference is the approved zero-test safety failure.
- Expected result: Reviewers can verify output got shorter without validation becoming weaker.
- Failure proves: Output-shape tests passed but the validation behavior or selected work may have changed.
- Automation location: Manual review evidence plus lifecycle validation of the change-local artifact.

### TSRO-011. Existing CI wrapper behavior is sufficient when untouched

- Covers: R28, R30, R31, R32, R35, E8, EC12, AC12, AC13
- Level: integration, manual
- Fixture/setup: Post-M3 runner behavior with `scripts/ci.sh` unchanged.
- Steps:
  - Run `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/ci.sh --jobs 1`.
  - Assert successful child output is hidden by default while stable check status appears.
  - Run the same selected path with wrapper `--verbose`.
  - Assert successful child output is exposed in stable order.
  - Use a failing selected-check fixture if available, or recorded wrapper failure evidence, to confirm failed child output includes check ID, status, exit reason, elapsed runtime, and command information.
  - Record in the audit and behavior-preservation matrix that `scripts/ci.sh` remains unchanged.
- Expected result: M4 can close as no-code when wrapper behavior already satisfies the contract.
- Failure proves: The wrapper needs a minimal M4 patch or the audit conclusion is unsupported.
- Automation location: `bash scripts/ci.sh --mode explicit ...`; recorded M4 evidence.

### TSRO-012. CI wrapper patch preserves selected-check semantics when triggered

- Covers: R28, R29, R30, R31, R32, R35, E8, EC13, AC12, AC13
- Level: integration
- Fixture/setup: Only applicable if M1 or M3 proves `scripts/ci.sh` must be touched.
- Steps:
  - Run the existing wrapper mode regression tests in `scripts/test-select-validation.py`.
  - Run successful selected checks by default and assert child output is hidden while status summary remains stable.
  - Run successful selected checks with wrapper `--verbose` and assert child output appears in stable order.
  - Run failing selected-check fixture and assert failed output includes responsible check ID, status, exit reason, elapsed runtime, and command information.
  - Assert existing wrapper modes, selected-check coverage, and child-process exit behavior match baseline proof.
- Expected result: Any wrapper edit is minimal and preserves the existing selector/wrapper contract.
- Failure proves: The conditional patch changed CI semantics rather than preserving output behavior.
- Automation location: `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit ...`.

### TSRO-013. Scope-boundary proof excludes generated and selector changes

- Covers: R32, AC14
- Level: contract
- Fixture/setup: Final diff and selected validation output.
- Steps:
  - Inspect changed files before code-review and final closeout.
  - Assert no generated adapter output, public skill files, workflow specs, or validation-selection logic changed unless a later approved artifact expands scope.
  - Run selected validation for all changed paths and confirm no unclassified paths.
- Expected result: The implementation remains inside the approved first-slice boundaries.
- Failure proves: The change silently expanded beyond script-output optimization.
- Automation location: `python scripts/select-validation.py --mode explicit ...`; code-review evidence.

### TSRO-014. Final selected smoke covers touched script-output surfaces

- Covers: R32, AC14
- Level: smoke
- Fixture/setup: Final implementation diff after M1 through M4.
- Steps:
  - Run `python scripts/test-select-validation.py`.
  - Run selected CI for `scripts/test-select-validation.py`, `scripts/ci.sh` when touched, `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, the active plan, `docs/plan.md`, and change-local evidence artifacts.
  - Run lifecycle, review-artifact, and change-metadata validators for the change root.
  - Run `git diff --check --`.
- Expected result: Repository-owned selected validation passes and no broad smoke is required unless selected by the wrapper or a later trigger.
- Failure proves: The implementation is not ready for code-review closeout or final lifecycle handoff.
- Automation location: Commands listed in the active plan M5 validation section.

## Fixtures and data

- Passing runner fixture: a deterministic invocation or internal fixture that exercises multiple passing checks without depending on external services, network, or local machine state.
- Failing runner fixture: deterministic failure data with failed names, messages, and file locations when available.
- Zero-test fixture: a controlled path that makes zero executed tests observable without modifying real test selection semantics.
- Rerun fixtures: failure IDs for exact stable filter, unmappable filter, and unsafe quoting cases.
- CI wrapper fixtures: existing selector and temporary workspace helpers in `scripts/test-select-validation.py`, including fake selected-check commands where wrapper behavior must be deterministic.
- Change-local evidence files: `script-output-audit.md` and `behavior-preservation.md`.

## Mocking/stubbing policy

- Use subprocess execution for public CLI behavior so stdout, stderr, and exit codes are real.
- Use internal helper/unit tests only for formatting decisions that cannot be reached deterministically through the public CLI without introducing brittle failures.
- Use temporary workspaces and fake selected-check commands for `scripts/ci.sh` wrapper behavior, following existing `scripts/test-select-validation.py` patterns.
- Do not mock away argument parsing, exit-code mapping, stdout/stderr separation, or selected-check execution when those are the behavior under test.
- Do not use network, secrets, hosted CI, or machine-specific paths as test fixtures.

## Migration or compatibility tests

- `TSRO-004` proves full pass/check detail remains available through `--verbose` and `-v`.
- `TSRO-009` proves JSON support is not newly added, and any existing JSON behavior is preserved.
- `TSRO-010` proves pass/failure exit codes, selected tests/checks, failure detection, and failure evidence are unchanged except for the approved zero-test safety boundary.
- `TSRO-011` and `TSRO-012` preserve existing CI wrapper selected-check semantics.

## Observability verification

- Success output must include suite/check identity, nonzero count, and duration in default mode.
- Failure output must include failed names, messages, locations when available, and reliable rerun guidance when available.
- Quiet success must emit no stdout or stderr.
- Audit and behavior-preservation artifacts must record baseline and new evidence for code-review.
- CI wrapper output must continue to report selected check IDs, statuses, exit reasons, elapsed runtime, and command information for failed checks.

## Security/privacy verification

- Failure output tests must not introduce environment dumps, secrets, credentials, tokens, private keys, or unnecessary machine-local debug data.
- Rerun-command tests must prove shell-sensitive names are safely quoted or omitted.
- CI wrapper failure-output tests must preserve existing bounded command evidence and must not print raw environment values.

## Performance checks

- Duration measurement must use the actual script execution interval and must not rerun tests solely for timing.
- `TSRO-014` smoke validation should compare gross runtime against baseline review notes only to catch obvious formatter-induced reruns or hangs; no hard performance gate is introduced.
- Any added output-shape tests should use deterministic fixtures rather than sleeping for real durations unless needed for existing wrapper timing behavior.

## Manual QA checklist

- Confirm the audit identifies `scripts/test-select-validation.py` as first-slice and `scripts/ci.sh` as conditional.
- Confirm behavior-preservation evidence exists before code-review closeout.
- Confirm default passing output is one summary line and verbose output remains useful for debugging.
- Confirm quiet success produces no stdout or stderr.
- Confirm a representative failure is repairable without rerunning with `--verbose`.
- Confirm the final diff does not touch generated adapter output, public skill files, workflow specs, or validation-selection logic outside an approved follow-up.

## What not to test and why

- Do not test a new JSON schema because new JSON support is explicitly deferred.
- Do not test a common script-output helper library because helper extraction is out of scope.
- Do not add broad tests for every repository script because the first slice targets `scripts/test-select-validation.py` and conditional `scripts/ci.sh` behavior.
- Do not require exact duration values; assert duration presence and valid shape because wall-clock time is inherently variable.
- Do not snapshot entire output logs; assert stable behavioral fields so failures identify contract drift rather than harmless formatting movement.
- Do not require broad smoke unless the selector or a later lifecycle trigger requires it.

## Uncovered gaps

None. Requirements that depend on conditional `scripts/ci.sh` changes have both no-change proof and triggered-change proof paths.

## Next artifacts

```text
implement M1 audit and baseline preservation
code-review M1
implement M2 output contract tests
code-review M2
implement M3 runner output shaping
code-review M3
implement or close M4 conditional CI wrapper preservation
code-review M4 if code changes
implement M5 lifecycle evidence and closeout handoff
code-review M5
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready to guide implementation. Implementation may start with M1 from the active plan; branch readiness, code-review approval, final verification, and PR readiness remain downstream gates.
