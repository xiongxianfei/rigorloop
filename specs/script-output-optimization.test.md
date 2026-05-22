# Script Output Optimization Test Spec

## Status

- active

## Related spec and plan

- Spec: [Script Output Optimization](script-output-optimization.md), approved.
- Proposal: [RigorLoop Script Output Optimization](../docs/proposals/2026-05-21-script-output-optimization.md), accepted.
- Proposal: [Broad-Smoke and Fixture-Suite Output Compaction](../docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md), accepted.
- Plan: [Script Output Optimization](../docs/plans/2026-05-21-script-output-optimization.md), done.
- Plan: [Broad-Smoke and Fixture-Suite Output Compaction](../docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md), active.
- Architecture: [System architecture](../docs/architecture/system/architecture.md), updated and approved by `architecture-review-r1`.
- Spec review: `spec-review-r2` approved the spec after `SRO-SR1` and `SRO-SR2` were resolved.
- Plan review: `plan-review-r1` approved the plan with no material findings.
- Broad-smoke proposal review: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r2.md`, approved.
- Broad-smoke spec review: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/spec-review-r2.md`, approved.
- Broad-smoke plan review: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/plan-review-r1.md`, approved.

## Testing strategy

- Unit tests cover the result-formatting and argument-boundary behavior that can be isolated inside `scripts/test-select-validation.py`, including summary-line fields, quiet success, conflicting output flags, zero-test handling, and rerun-command eligibility.
- Integration tests execute `scripts/test-select-validation.py` as a subprocess where stdout, stderr, and exit code are observable. They should use deterministic fixture cases or helper entry points rather than relying on the real repository suite failing.
- End-to-end tests run the changed runner through `scripts/ci.sh` to prove wrapper behavior remains quiet on successful child output by default, exposes successful output with wrapper `--verbose`, and surfaces failed child output when relevant.
- Smoke tests run the normal selected validation path for touched files after implementation.
- Manual verification is limited to durable audit and behavior-preservation evidence where baseline/new comparison is review evidence rather than pure executable behavior.
- Contract tests inspect the audit, behavior-preservation matrix, and changed-path set to prove no generated adapter output, public skill files, workflow specs, validation-selection logic, or broad CI behavior changed outside the approved scope.
- Migration/compatibility tests prove the old full pass/check detail remains available through `--verbose` and that JSON support is not newly introduced.
- Broad-smoke integration tests exercise the `scripts/ci.sh --mode broad-smoke` orchestration path with deterministic noisy and failing child fixtures so capture, aggregate success, failure evidence, verbose output, and exit behavior are observable.
- Wrapper-mode consistency tests statically or structurally inspect `scripts/ci.sh` orchestration modes that run validation producers and fail when a mode streams child output directly without an approved exception.
- Producer integration tests execute `scripts/test-change-metadata-validator.py` as a subprocess for default, `--verbose` / `-v`, `--quiet` / `-q`, zero-test, pass/fail exit, and selected-test identity proof.
- Ordinary-validation guard tests prove broad-smoke and producer output-contract tests are included in ordinary post-implementation validation or that a normal validation command fails when they fail.

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
| R36 | TSRO-015 | manual, contract | Asserts output-layer audit exists at the broad-smoke change-local path. |
| R37 | TSRO-015 | manual, contract | Asserts audit records producer, direct-run, orchestrator, capture-policy, high-use, and treatment fields. |
| R38 | TSRO-015 | manual, contract | Asserts selected-CI and broad-smoke are separate orchestrator paths. |
| R39 | TSRO-017 | integration | Asserts broad-smoke `run_check` captures child stdout/stderr by default. |
| R40 | TSRO-017 | integration | Asserts successful child stdout/stderr is not streamed in default broad-smoke success. |
| R41 | TSRO-017 | integration | Asserts aggregate `[PASS] broad-smoke` summary with count and duration. |
| R42 | TSRO-017 | integration, contract | Asserts default success is not one line per child. |
| R43 | TSRO-018 | integration | Asserts failed child check name is shown. |
| R44 | TSRO-018 | integration | Asserts failed child command is shown. |
| R45 | TSRO-018 | integration | Asserts child exit code or exit reason is shown. |
| R46 | TSRO-018 | integration | Asserts failed child duration is shown. |
| R47 | TSRO-018 | integration | Asserts captured stdout/stderr is shown with combined ordering preserved or separated streams labeled. |
| R48 | TSRO-019 | integration | Asserts broad-smoke `--verbose` emits successful child output in stable check order. |
| R49 | TSRO-016, TSRO-018, TSRO-019, TSRO-026 | integration, contract | Asserts broad-smoke command selection/order, child exit behavior, failure detection, and wrapper exit behavior are preserved. |
| R50 | TSRO-016 | manual, contract | Asserts ordered broad-smoke command list and SHA-256 hash exist before and after. |
| R51 | TSRO-020 | unit, integration | Asserts wrapper-mode consistency guard checks each `scripts/ci.sh` orchestration mode that runs validation producers. |
| R52 | TSRO-020 | unit, integration | Asserts checked modes use capture policy or have a documented exception. |
| R53 | TSRO-015, TSRO-021 | contract, integration | Asserts the first targeted producer is `scripts/test-change-metadata-validator.py` unless an approved audit exception exists. |
| R54 | TSRO-021 | integration | Asserts default producer success is one `[PASS]` summary with name, nonzero count, and duration. |
| R55 | TSRO-021 | integration | Asserts producer default success hides individual passing tests. |
| R56 | TSRO-021 | integration | Asserts producer default failure includes `[FAIL]`, failed names, messages, and locations when available. |
| R57 | TSRO-021 | integration | Asserts producer default failure collapses passing detail into counts. |
| R58 | TSRO-022 | integration | Asserts producer accepts `--verbose` and `-v`. |
| R59 | TSRO-022 | integration, migration | Asserts producer verbose mode preserves full pass/check listing. |
| R60 | TSRO-023 | integration, migration | Asserts producer `--quiet` and `-q` remain accepted. |
| R60a | TSRO-023 | contract, migration | Asserts no custom compact quiet formatter is added for the producer. |
| R60b | TSRO-023 | integration, migration | Asserts `--quiet` and `-q` are not converted into unsupported invocations. |
| R60c | TSRO-023 | contract | Asserts future custom quiet formatting requires a new approved output contract and preservation proof. |
| R61 | TSRO-024 | integration | Asserts producer zero executed tests fail unless an explicit mode allows zero selection. |
| R62 | TSRO-024 | manual, contract | Asserts producer selected test/check identity list and SHA-256 hash exist before and after. |
| R63 | TSRO-025 | integration, contract | Asserts output-contract tests run in ordinary validation or are guarded by ordinary validation. |
| R64 | TSRO-026 | integration, contract | Asserts selected-CI behavior does not regress. |
| R65 | TSRO-026, TSRO-027 | contract, smoke | Asserts no generated artifacts, skills, adapters, JSON support, validation selection logic, or validation coverage changes. |

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
| E10 | TSRO-017 | Broad-smoke success is aggregate and does not stream successful child output. |
| E11 | TSRO-018 | Broad-smoke failure shows failed child identity, command, exit reason, duration, and captured output. |
| E12 | TSRO-019 | Broad-smoke `--verbose` preserves successful child detail in stable order. |
| E13 | TSRO-021 | Direct producer success is compact. |
| E14 | TSRO-021 | Direct producer failure remains actionable. |
| E15 | TSRO-020 | Wrapper-mode consistency guard checks every applicable orchestration mode. |

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
| EC14 | TSRO-017 | Broad-smoke child checks pass while emitting stdout/stderr; default output is aggregate only. |
| EC15 | TSRO-018 | Broad-smoke child fails while emitting stdout/stderr; failure output includes labeled or ordered captured output. |
| EC16 | TSRO-019 | Broad-smoke verbose prints successful child output in stable order. |
| EC17 | TSRO-020 | New non-capturing orchestration mode without documented exception fails the consistency guard. |
| EC18 | TSRO-021 | Producer passing run with many tests emits one summary line. |
| EC19 | TSRO-021 | Producer failing run expands failed tests and collapses passing tests into counts. |
| EC20 | TSRO-022 | Producer `--verbose` passes and includes full pass/check detail. |
| EC21 | TSRO-023 | Producer `--quiet` passes, writes no stdout, and may write normal unittest quiet summary to stderr. |
| EC21a | TSRO-023 | Producer `-q` matches `--quiet` when accepted in baseline. |
| EC22 | TSRO-016 | Non-deterministic broad-smoke command-list extraction blocks preservation claims. |

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
| AC15 | TSRO-015 | Output-layer audit maps producers, orchestrators, capture policy, high-use status, and first-slice treatment. |
| AC16 | TSRO-017 | Broad-smoke `run_check` captures child stdout/stderr by default. |
| AC17 | TSRO-017 | Broad-smoke default success does not stream successful child output. |
| AC18 | TSRO-017 | Broad-smoke default success reports aggregate `[PASS] broad-smoke` summary with count and duration. |
| AC19 | TSRO-018 | Broad-smoke default failure includes child name, command, exit code/reason, duration, and captured stdout/stderr. |
| AC20 | TSRO-019 | Broad-smoke `--verbose` emits full successful child output in stable order. |
| AC21 | TSRO-016 | Broad-smoke selected child command list and exit-code behavior are unchanged with ordered list plus SHA-256 hash proof. |
| AC22 | TSRO-020 | Wrapper-mode consistency is checked for every validation-producing `scripts/ci.sh` mode or documented exception. |
| AC23 | TSRO-021 | Producer default success is one `[PASS]` summary with name, nonzero count, and duration. |
| AC24 | TSRO-021 | Producer default success hides individual passing checks. |
| AC25 | TSRO-021 | Producer default failure includes `[FAIL]`, failed names, messages, and locations when available. |
| AC26 | TSRO-022 | Producer `--verbose` exposes full pass/check detail. |
| AC27 | TSRO-024 | Producer selected test/check identity and pass/fail exit codes are unchanged with ordered list plus SHA-256 hash proof. |
| AC28 | TSRO-025 | Broad-smoke and producer output-contract tests run in ordinary validation or are guarded by ordinary validation. |
| AC29 | TSRO-026 | Selected-CI behavior does not regress. |
| AC30 | TSRO-026, TSRO-027 | No generated artifacts, skills, adapters, JSON support, validation selection logic, or validation coverage changes. |
| AC31 | TSRO-023 | Producer `--quiet` remains accepted. |
| AC32 | TSRO-023 | Producer `-q` remains accepted when accepted in baseline. |
| AC33 | TSRO-023 | Producer quiet success preserves current unittest-compatible stdout/stderr behavior. |
| AC34 | TSRO-023 | Spec does not claim producer `--quiet` is unsupported. |
| AC35 | TSRO-017, TSRO-023 | Broad-smoke compaction is implemented through `run_check` capture, not producer quiet. |
| AC36 | TSRO-023 | Future custom producer quiet formatting requires a new approved output contract and preservation proof. |

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

### TSRO-015. Output-layer audit records producers and orchestrators

- Covers: R36, R37, R38, R53, R60, R60a, R60b, AC15, AC31, AC32, AC33, AC34, AC35
- Level: manual, contract
- Fixture/setup: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md`.
- Steps:
  - Inspect the audit after M1.
  - Confirm it includes `scripts/test-select-validation.py`, `scripts/test-change-metadata-validator.py`, selected-CI, and broad-smoke.
  - Confirm selected-CI and broad-smoke are separate orchestrator paths, not one combined wrapper row.
  - Confirm each assessed producer records direct-run success shape, direct-run failure usefulness, orchestrators, orchestrator capture policy, high-use direct-run status, and first-slice treatment.
  - Confirm the first targeted producer is `scripts/test-change-metadata-validator.py` unless the audit records owner approval for a replacement.
  - Confirm the audit records current `scripts/test-change-metadata-validator.py --quiet` and `-q` compatibility and does not treat those flags as unsupported.
  - Confirm broad-smoke compaction is assigned to `run_check` capture rather than producer-level quiet flags.
- Expected result: The audit proves the slice is reasoning about every printing layer and wrapper path before implementation.
- Failure proves: The implementation can fix one noisy path while leaving another unenumerated output layer to diverge.
- Automation location: Manual review evidence plus `git diff --check -- docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md`.

### TSRO-016. Broad-smoke command identity proof is deterministic

- Covers: R49, R50, AC21, EC22
- Level: manual, contract
- Fixture/setup: Broad-smoke command-list extraction method and durable evidence under `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/`.
- Steps:
  - Run or inspect the deterministic broad-smoke command-list extraction method defined by implementation.
  - Capture the ordered broad-smoke child command list before output changes.
  - Compute and record a SHA-256 hash over the ordered list.
  - Repeat the extraction after broad-smoke capture is implemented.
  - Assert the post-change ordered list and hash match baseline.
  - If extraction is non-deterministic or depends on streamed output formatting, block behavior-preservation closeout.
- Expected result: Reviewers can prove broad-smoke selected child commands and order did not change independently from output text.
- Failure proves: Shorter broad-smoke logs may have changed command selection or order.
- Automation location: Repository-owned extraction helper or documented command in `behavior-preservation.md`; lifecycle validation for the evidence artifact.

### TSRO-017. Broad-smoke default success captures noisy child output

- Covers: R39, R40, R41, R42, R49, AC16, AC17, AC18, AC35, E10, EC14
- Level: integration
- Fixture/setup: Deterministic broad-smoke fixture or stub child checks that pass while writing recognizable stdout and stderr markers.
- Steps:
  - Run `bash scripts/ci.sh --mode broad-smoke` against the noisy passing fixture.
  - Capture stdout, stderr, and exit code.
  - Assert success exit code matches baseline.
  - Assert child stdout and stderr marker lines are absent from default output.
  - Assert output includes exactly one aggregate `[PASS] broad-smoke` summary with passed child-check count and duration.
  - Assert output does not print one success line per child.
  - Assert the command does not invoke producer-level `--quiet` to achieve broad-smoke compaction.
- Expected result: Broad-smoke success output is constant-size aggregate evidence owned by the wrapper.
- Failure proves: Broad-smoke still streams child success output, reintroduces output growth with child count, or relies on producer quiet behavior instead of wrapper capture.
- Automation location: `scripts/test-select-validation.py` wrapper tests or another repository-owned script-output test selected by ordinary validation.

### TSRO-018. Broad-smoke failure emits captured child evidence

- Covers: R43, R44, R45, R46, R47, R49, AC19, E11, EC15
- Level: integration
- Fixture/setup: Deterministic broad-smoke fixture with one failing child that writes recognizable stdout and stderr and exits nonzero.
- Steps:
  - Run `bash scripts/ci.sh --mode broad-smoke` against the failing fixture.
  - Capture stdout, stderr, and exit code.
  - Assert the wrapper exits nonzero with the same failure semantics as baseline.
  - Assert output identifies the failed child check name.
  - Assert output includes the failed child command.
  - Assert output includes child exit code or exit reason.
  - Assert output includes failed child duration.
  - Assert captured stdout and stderr are included.
  - If stdout and stderr are separated, assert streams are clearly labeled; if combined, assert child emission ordering is preserved.
- Expected result: Broad-smoke is quiet on success but fully actionable on failure.
- Failure proves: Capture hides failure evidence, loses stderr, reorders diagnostically important output without labels, or changes failure semantics.
- Automation location: `scripts/test-select-validation.py` wrapper tests or another repository-owned script-output test selected by ordinary validation.

### TSRO-019. Broad-smoke verbose preserves successful child detail

- Covers: R48, R49, AC20, E12, EC16
- Level: integration, migration
- Fixture/setup: Deterministic broad-smoke fixture with two or more successful child checks that write ordered stdout/stderr markers.
- Steps:
  - Run `bash scripts/ci.sh --mode broad-smoke --verbose` against the fixture.
  - Assert success exit code matches default mode.
  - Assert successful child output appears.
  - Assert child output appears in stable child-check order.
  - Assert the selected child command list matches default broad-smoke mode.
- Expected result: `--verbose` remains the escape hatch for full broad-smoke child output without changing what runs.
- Failure proves: Wrapper capture removed maintainers' access to successful child detail or made verbose output non-deterministic.
- Automation location: `scripts/test-select-validation.py` wrapper tests or another repository-owned script-output test selected by ordinary validation.

### TSRO-020. Wrapper-mode consistency guard is enforceable

- Covers: R51, R52, AC22, E15, EC17
- Level: unit, integration
- Fixture/setup: Static or structural fixture for `scripts/ci.sh` orchestration modes, plus a negative fixture that introduces a validation-producing mode without capture or documented exception.
- Steps:
  - Run the wrapper-mode consistency guard against current `scripts/ci.sh`.
  - Assert every orchestration mode that runs validation producers either uses capture-on-success/show-on-failure-or-verbose behavior or has a documented spec/test-spec exception.
  - Run the guard against the negative fixture.
  - Assert the guard fails and identifies the non-capturing mode.
  - Assert the guard is part of ordinary validation or covered by TSRO-025.
- Expected result: Wrapper-mode consistency is enforced as a regression guard, not only documented.
- Failure proves: The broad-smoke divergence class remains open for the next orchestration mode.
- Automation location: Repository-owned static/structural test selected by ordinary validation.

### TSRO-021. Change metadata validator default output is compact and actionable

- Covers: R53, R54, R55, R56, R57, AC23, AC24, AC25, E13, E14, EC18, EC19
- Level: integration
- Fixture/setup: Deterministic passing and failing invocations of `scripts/test-change-metadata-validator.py`, with failure fixture exposing failed test names, messages, and locations when available.
- Steps:
  - Run `python scripts/test-change-metadata-validator.py` against the passing suite.
  - Assert success exit code.
  - Assert stdout contains one `[PASS] test-change-metadata-validator` summary with nonzero passed count and duration.
  - Assert default success does not list individual passing tests.
  - Run the failing fixture in default mode.
  - Assert nonzero failure exit code.
  - Assert output includes a `[FAIL] test-change-metadata-validator` summary.
  - Assert failed test names, assertion/error messages, and file locations appear when available.
  - Assert passing test detail is collapsed into counts.
- Expected result: Direct producer runs are compact on success and still repair-oriented on failure.
- Failure proves: The direct producer remains noisy, loses failure evidence, or changes pass/fail exit behavior.
- Automation location: `scripts/test-change-metadata-validator.py` self-tests or a repository-owned subprocess test selected by ordinary validation.

### TSRO-022. Change metadata validator verbose mode preserves full detail

- Covers: R58, R59, AC26, EC20
- Level: integration, migration
- Fixture/setup: Passing `scripts/test-change-metadata-validator.py` suite with known individual test/check names.
- Steps:
  - Run `python scripts/test-change-metadata-validator.py --verbose`.
  - Run `python scripts/test-change-metadata-validator.py -v`.
  - Assert both commands exit successfully.
  - Assert both outputs include the full pass/check listing that default mode suppresses.
  - Assert verbose mode does not change selected test/check identity compared with default mode.
- Expected result: Maintainers can still request full unittest-style detail through `--verbose` and `-v`.
- Failure proves: Producer compaction removed the compatibility escape hatch or changed selected tests.
- Automation location: `scripts/test-change-metadata-validator.py` self-tests or a repository-owned subprocess test selected by ordinary validation.

### TSRO-023. Change metadata validator quiet compatibility is preserved

- Covers: R60, R60a, R60b, R60c, AC31, AC32, AC33, AC34, AC35, AC36, EC21, EC21a
- Level: integration, migration, contract
- Fixture/setup: Current unittest-compatible `scripts/test-change-metadata-validator.py --quiet` and `-q` behavior.
- Steps:
  - Run `python scripts/test-change-metadata-validator.py --quiet` against the passing suite.
  - Assert exit code is `0`.
  - Assert stdout is empty.
  - Assert stderr may contain the normal unittest quiet success summary.
  - Run `python scripts/test-change-metadata-validator.py -q` when accepted in baseline.
  - Assert `-q` behavior matches `--quiet`.
  - Assert neither flag is converted to an unsupported usage error.
  - Inspect producer output changes and assert no custom compact quiet formatter from `scripts/test-select-validation.py` is introduced for this producer.
  - Inspect broad-smoke behavior and assert success compaction does not depend on invoking this producer with `--quiet`.
  - Confirm any future custom quiet formatting remains out of scope and would require a new approved output contract and preservation proof.
- Expected result: Quiet compatibility is preserved exactly as a compatibility boundary, while broad-smoke compaction stays owned by the wrapper layer.
- Failure proves: The slice accidentally breaks an accepted producer invocation or solves wrapper noise at the wrong layer.
- Automation location: Subprocess tests plus behavior-preservation evidence.

### TSRO-024. Change metadata validator selected-test identity and zero-test safety are preserved

- Covers: R61, R62, AC27
- Level: integration, manual, contract
- Fixture/setup: Deterministic producer selected test/check identifier extraction method and zero-test fixture if implementation supports filtered selection.
- Steps:
  - Extract and record the ordered producer selected test/check identifier list before output changes.
  - Compute and record a SHA-256 hash over that ordered list.
  - Repeat extraction after producer output shaping.
  - Assert post-change ordered list and hash match baseline.
  - Run default passing and failing producer fixtures and assert pass/fail exit codes match baseline.
  - If a zero-test condition can be produced through an accepted invocation, assert it exits nonzero unless an explicit audit/list/dry-run mode documents zero selection as allowed.
- Expected result: Producer output formatting does not change which checks run or how pass/fail exits are reported.
- Failure proves: Compact output masked selected-test drift, exit-code drift, or a zero-test false success.
- Automation location: Repository-owned extraction helper or documented command in `behavior-preservation.md`; subprocess tests where feasible.

### TSRO-025. Output-contract tests are covered by ordinary validation

- Covers: R63, AC28
- Level: integration, contract
- Fixture/setup: Ordinary post-implementation validation command named by the plan and this test spec.
- Steps:
  - Identify the repository-owned output-contract tests for broad-smoke and `scripts/test-change-metadata-validator.py`.
  - Run the ordinary validation command expected after implementation, such as `python scripts/test-select-validation.py`, `python scripts/test-change-metadata-validator.py`, or the test-spec-named output-contract command.
  - Confirm the output-contract tests are included in ordinary validation, or that a normal guard fails when those tests fail.
  - Record the command and result in the active plan and change metadata.
- Expected result: Required output-contract proof cannot pass only as a separate diagnostic command that ordinary validation skips.
- Failure proves: A prior failure pattern recurred: special output tests can be green in isolation while ordinary validation excludes them.
- Automation location: Ordinary validation command named by the implementation and selected CI for changed files.

### TSRO-026. Selected-CI behavior and out-of-scope surfaces do not regress

- Covers: R49, R64, R65, AC29, AC30
- Level: integration, contract
- Fixture/setup: Final implementation diff and selected-CI invocation for touched files.
- Steps:
  - Run `bash scripts/ci.sh --mode selected --jobs 1` or the selected-CI command named by the active plan.
  - Assert selected-CI exits successfully on a passing workspace.
  - Compare selected-CI output and child-output policy to first-slice behavior when `scripts/ci.sh` is touched.
  - Inspect the changed file list.
  - Assert no generated artifacts, skill files, adapter files, JSON support, validation selection logic, or validation coverage changed unless an approved artifact explicitly expands scope.
- Expected result: Broad-smoke and producer compaction do not regress selected-CI or silently broaden the slice.
- Failure proves: A wrapper/shared-helper change leaked into selected-CI or out-of-scope repository surfaces.
- Automation location: `bash scripts/ci.sh --mode selected --jobs 1`, selected explicit CI, and code-review diff evidence.

### TSRO-027. Final broad-smoke fixture-suite smoke covers the coordinated slice

- Covers: R65, AC30
- Level: smoke
- Fixture/setup: Final implementation diff after M1 through M4.
- Steps:
  - Run the output-contract command named by this test spec or implementation, if one is added.
  - Run `python scripts/test-select-validation.py`.
  - Run `python scripts/test-change-metadata-validator.py`.
  - Run `python scripts/test-change-metadata-validator.py --verbose`.
  - Run `python scripts/test-change-metadata-validator.py --quiet`.
  - Run `python scripts/test-change-metadata-validator.py -q`.
  - Run `bash scripts/ci.sh --mode broad-smoke`.
  - Run `bash scripts/ci.sh --mode broad-smoke --verbose`.
  - Run selected explicit CI for `scripts/ci.sh`, `scripts/test-change-metadata-validator.py`, `scripts/test-select-validation.py`, `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, the active plan, `docs/plan.md`, and change-local evidence.
  - Run lifecycle, review-artifact, and change-metadata validators for the change root.
  - Run `git diff --check --`.
- Expected result: The coordinated wrapper-plus-producer slice passes repository-owned focused and smoke validation without changing out-of-scope surfaces.
- Failure proves: The implementation is not ready for final code-review closeout or downstream explain-change/verify handoff.
- Automation location: Commands listed in the active broad-smoke plan M4 validation section.

## Fixtures and data

- Passing runner fixture: a deterministic invocation or internal fixture that exercises multiple passing checks without depending on external services, network, or local machine state.
- Failing runner fixture: deterministic failure data with failed names, messages, and file locations when available.
- Zero-test fixture: a controlled path that makes zero executed tests observable without modifying real test selection semantics.
- Rerun fixtures: failure IDs for exact stable filter, unmappable filter, and unsafe quoting cases.
- CI wrapper fixtures: existing selector and temporary workspace helpers in `scripts/test-select-validation.py`, including fake selected-check commands where wrapper behavior must be deterministic.
- Change-local evidence files: `script-output-audit.md` and `behavior-preservation.md`.
- Broad-smoke noisy child fixture: a deterministic broad-smoke child that passes while emitting recognizable stdout and stderr markers.
- Broad-smoke failing child fixture: a deterministic broad-smoke child that exits nonzero while emitting recognizable stdout and stderr markers.
- Wrapper-mode consistency negative fixture: a synthetic `scripts/ci.sh` mode or parseable fixture that runs validation producers without capture and without a documented exception.
- Producer selected-test identity fixture: ordered `scripts/test-change-metadata-validator.py` test/check identifiers and SHA-256 hash before and after output shaping.
- Broad-smoke command identity fixture: ordered broad-smoke child commands and SHA-256 hash before and after wrapper output shaping.

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
- `TSRO-019` proves broad-smoke `--verbose` preserves full successful child output after wrapper capture is added.
- `TSRO-022` proves `scripts/test-change-metadata-validator.py --verbose` and `-v` preserve full pass/check detail after producer compaction.
- `TSRO-023` proves `scripts/test-change-metadata-validator.py --quiet` and `-q` remain accepted with existing unittest-compatible behavior.
- `TSRO-026` proves selected-CI behavior does not regress.

## Observability verification

- Success output must include suite/check identity, nonzero count, and duration in default mode.
- Failure output must include failed names, messages, locations when available, and reliable rerun guidance when available.
- Quiet success must emit no stdout or stderr.
- Audit and behavior-preservation artifacts must record baseline and new evidence for code-review.
- CI wrapper output must continue to report selected check IDs, statuses, exit reasons, elapsed runtime, and command information for failed checks.
- Broad-smoke default success must report aggregate broad-smoke identity, passed child-check count, and duration.
- Broad-smoke default failure must identify failed child name, command, exit reason, duration, and captured stdout/stderr.
- Wrapper-mode consistency guard results must be reviewable through ordinary validation output or recorded evidence.
- Producer quiet compatibility evidence must distinguish accepted unittest-compatible quiet behavior from custom compact quiet formatting.

## Security/privacy verification

- Failure output tests must not introduce environment dumps, secrets, credentials, tokens, private keys, or unnecessary machine-local debug data.
- Rerun-command tests must prove shell-sensitive names are safely quoted or omitted.
- CI wrapper failure-output tests must preserve existing bounded command evidence and must not print raw environment values.
- Broad-smoke capture must not persist child output outside normal command output unless a later approved artifact defines storage and privacy handling.
- Captured broad-smoke output tests must use synthetic marker text, not secrets or machine-local environment dumps.

## Performance checks

- Duration measurement must use the actual script execution interval and must not rerun tests solely for timing.
- `TSRO-014` smoke validation should compare gross runtime against baseline review notes only to catch obvious formatter-induced reruns or hangs; no hard performance gate is introduced.
- Broad-smoke capture should use existing validation output volume and must not require child checks to run more than once.
- `TSRO-027` should catch obvious wrapper or producer hangs but does not add a hard timing threshold.
- Any added output-shape tests should use deterministic fixtures rather than sleeping for real durations unless needed for existing wrapper timing behavior.

## Manual QA checklist

- Confirm the audit identifies `scripts/test-select-validation.py` as first-slice and `scripts/ci.sh` as conditional.
- Confirm behavior-preservation evidence exists before code-review closeout.
- Confirm default passing output is one summary line and verbose output remains useful for debugging.
- Confirm quiet success produces no stdout or stderr.
- Confirm a representative failure is repairable without rerunning with `--verbose`.
- Confirm the final diff does not touch generated adapter output, public skill files, workflow specs, or validation-selection logic outside an approved follow-up.
- Confirm the broad-smoke output-layer audit names selected-CI and broad-smoke separately.
- Confirm broad-smoke success is aggregate, not per-child success lines.
- Confirm broad-smoke failure includes captured stderr.
- Confirm broad-smoke verbose output includes successful child output in stable order.
- Confirm wrapper-mode consistency is enforced by an ordinary guard.
- Confirm `scripts/test-change-metadata-validator.py --quiet` and `-q` remain accepted and are not changed to custom compact quiet formatting.
- Confirm command/test identity hashes are recorded before and after output changes.

## What not to test and why

- Do not test a new JSON schema because new JSON support is explicitly deferred.
- Do not test a common script-output helper library because helper extraction is out of scope.
- Do not add broad tests for every repository script because the first slice targets `scripts/test-select-validation.py` and conditional `scripts/ci.sh` behavior.
- Do not rewrite this test spec to require every verbose unittest producer to be compacted; the broad-smoke slice targets `scripts/test-change-metadata-validator.py` only.
- Do not test custom compact quiet formatting for `scripts/test-change-metadata-validator.py` because the approved contract preserves existing unittest-compatible quiet behavior instead.
- Do not require per-child broad-smoke success lines; the approved broad-smoke success contract is aggregate.
- Do not use producer-level `--quiet` as the broad-smoke success-compaction proof because broad-smoke owns capture through `run_check`.
- Do not require exact duration values; assert duration presence and valid shape because wall-clock time is inherently variable.
- Do not snapshot entire output logs; assert stable behavioral fields so failures identify contract drift rather than harmless formatting movement.
- Do not require broad smoke for the first script-output slice; the broad-smoke and fixture-suite slice does require broad-smoke validation.

## Uncovered gaps

None. First-slice requirements that depend on conditional selected-CI wrapper changes have both no-change proof and triggered-change proof paths. Broad-smoke requirements have dedicated wrapper capture, consistency-guard, command-identity, and final smoke proof paths.

## Next artifacts

```text
implement M1 output-layer audit and baseline identity proof
code-review M1
implement M2 broad-smoke capture and wrapper-mode consistency guard
code-review M2
implement M3 first producer compact default and verbose compatibility
code-review M3
implement M4 preservation evidence and lifecycle closeout
code-review M4
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready to guide implementation for the approved broad-smoke and fixture-suite output compaction plan. Implementation may start with M1 from the active plan; branch readiness, code-review approval, final verification, and PR readiness remain downstream gates.
