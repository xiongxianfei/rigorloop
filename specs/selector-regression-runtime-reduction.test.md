# Selector-Regression Runtime Reduction Test Spec

## Status

active

## Related spec and plan

- Spec: [Selector-Regression Runtime Reduction](selector-regression-runtime-reduction.md)
- Plan: [Selector-Regression Runtime Reduction Plan](../docs/plans/2026-06-27-selector-regression-runtime-reduction.md)
- Proposal: [Selector-Regression Runtime Reduction With Coverage-Preservation Proof](../docs/proposals/2026-06-27-selector-regression-runtime-reduction.md)
- Spec review: [spec-review-r1](../docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/spec-review-r1.md)
- Plan review: [plan-review-r1](../docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/plan-review-r1.md)
- Architecture/ADRs: not applicable for this slice unless implementation expands into persistent workers, shared caches, broad validator composition, or new cross-process execution protocols.

## Testing strategy

Unit coverage exercises pure selector logic in process through `scripts/test-select-validation.py`, using table-driven changed-path fixtures and immutable or resettable fixture builders.

Integration coverage keeps subprocess proof for command boundaries: selector CLI parsing, exit codes, stdout or stderr diagnostics, timeout override behavior, selected-CI wrapper integration, and rerun guidance.

End-to-end coverage is the unchanged default command:

```bash
python scripts/test-select-validation.py
```

Smoke coverage runs the default selector-regression command plus lifecycle, review, metadata, and diff-hygiene validators for the touched artifacts.

Manual coverage records MP-SEL-001 profiling evidence, baseline and revised runtime evidence, paired median comparison when practical, timeout status, and any no-safe-reduction rationale.

Contract coverage compares behavioral selector identity, selected-check identity, unittest identifier identity or approved test-structure delta, missing-route failure sensitivity, registered-route behavior, cache-boundary metadata, broad-smoke classification behavior, CLI-boundary coverage, diagnostics, and final-verify boundary preservation.

Migration coverage verifies the default contributor command and selected-CI wrapper remain compatible and that no required selector-regression category moves to an optional-only command.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T9 | smoke | Default command remains the complete selector-regression path. |
| R2 | T1, T9 | smoke | No required category moves behind a quick, fast, skipped, filtered, or expected-failure path. |
| R3 | T1, T4, T8 | contract | Runtime gains are accepted only when they come from reduced duplicate work and preservation evidence passes. |
| R4 | T2 | manual | Baseline runtime evidence is required before accepting runtime-reducing implementation. |
| R5 | T8 | manual | Revised runtime evidence or a complete no-safe-reduction record is required. |
| R6 | T2, T8 | manual | Evidence uses at least three paired runs and median comparison when practical. |
| R7 | T2, T8 | contract | Runtime evidence records command, environment, repository state, counts, timings, deltas, timeout behavior, limitations, and preservation result. |
| R8 | T3, T6 | contract | Behavioral selector identity is mandatory unless an approved spec change changes selector behavior. |
| R9 | T3, T6 | contract | Selected-check identity is mandatory unless an approved spec change changes routing. |
| R10 | T3 | contract | Unittest identifier deltas are allowed only with an approved test-structure delta. |
| R11 | T3 | contract | Preservation evidence distinguishes behavioral, selected-check, and unittest identifier identity. |
| R12 | T4 | unit | In-process tests are limited to pure selector logic. |
| R13 | T5 | integration | CLI-boundary behavior remains subprocess-backed. |
| R14 | T5, T9 | integration | Subprocess coverage includes parsing, exit codes, diagnostics, timeout override, wrapper integration, and rerun guidance. |
| R15 | T6 | integration | Missing selector-route cases remain hard failures. |
| R16 | T6 | integration | Negative and registered-route fixtures cover unknown paths, unregistered evidence, unknown lifecycle artifacts, new evidence classes, and registered routes. |
| R17 | T7 | contract | Cache-boundary metadata remains `not-applicable`. |
| R18 | T7 | integration | Broad-smoke classification pass/fail behavior is preserved and broad-smoke parallel execution remains out of scope. |
| R19 | T7, T10 | contract | Cache, workers, broad validator composition, and broad-smoke parallelism remain disabled. |
| R20 | T5, T9 | integration | Selected-CI wrapper compatibility is preserved. |
| R21 | T8, T9 | manual | Timeout override status is recorded after revised runtime evidence. |
| R22 | T2 | manual | Selector-regression profile proof exists before implementation closeout. |
| R23 | T2 | manual | Profile proof contains the required MP-SEL-001 fields. |
| R24 | T8 | manual | Primary success target is a 25% paired median reduction with preservation. |
| R25 | T8, T9 | manual | Alternative success target is removing the 180-second selected-CI timeout override need with preservation. |
| R26 | T8 | manual | Fallback closeout requires complete no-safe-reduction evidence and next bottleneck. |
| R27 | T3, T8 | contract | Lower elapsed time alone is not success. |
| R28 | T8, T10 | contract | Selector-runtime evidence does not claim final verify, branch readiness, PR readiness, or hosted CI success. |
| R29 | T5, T6 | integration | Diagnostics identify scenario, fixture/path class, expected and observed outcome, and corrective action or rerun guidance when available. |
| R30 | T4 | unit | Reusable fixtures avoid mutable state leakage or reset between test groups. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T9 | Default command completeness and no optional-only coverage. |
| E2 | T3, T4 | In-process pure selector conversion preserves behavior and selected checks. |
| E3 | T5 | CLI-boundary cases stay subprocess-backed. |
| E4 | T6 | Missing-route blockers remain hard failures. |
| E5 | T8 | Runtime targets do not override proof preservation. |

## Edge case coverage

| Edge case | Covered by | Level | Notes |
| --- | --- | --- | --- |
| EC1 | T1, T6 | integration | Faster suite that omits a missing-route fixture is blocked. |
| EC2 | T5 | integration | CLI parsing subprocess coverage cannot be removed. |
| EC3 | T3 | contract | Test-name-only delta is accepted only with preserved behavioral and selected-check identity. |
| EC4 | T2, T8 | manual | Noisy runtime evidence records limitations and uses paired runs where practical. |
| EC5 | T2, T8 | manual | No safe selector reduction requires a complete rationale and next target. |
| EC6 | T7 | integration | Broad-smoke classification fixtures must still pass and fail as expected. |
| EC7 | T7 | contract | Cache-boundary metadata cannot change without a separate cache contract. |
| EC8 | T8, T9 | manual | Remaining timeout override need is recorded rather than hidden. |
| EC9 | T4 | unit | Shared fixture leakage is caught by isolated or resettable fixture assertions. |
| EC10 | T5, T6 | integration | Diagnostics remain actionable after output or test-structure changes. |

## Test cases

### T1. Default Selector-Regression Command Remains Complete

- Covers: R1, R2, R3, E1, EC1
- Level: smoke
- Fixture/setup: Default repository selector-regression suite in `scripts/test-select-validation.py`.
- Steps: Run `python scripts/test-select-validation.py`; inspect the test suite structure after implementation for required selector-regression categories.
- Expected result: The command exits successfully and exercises required selector-regression coverage for selector logic, missing-route blockers, cache-boundary metadata, broad-smoke classification metadata, CLI output behavior, wrapper behavior, exit codes, timeout behavior, rerun guidance, and diagnostics. No required category is optional-only, skipped, filtered out, expected-failure, or delegated to a first-slice quick mode.
- Failure proves: Runtime was reduced by removing or hiding required proof, or the default contributor command is no longer the complete regression path.
- Automation location: `scripts/test-select-validation.py`; command `python scripts/test-select-validation.py`.

### T2. Baseline Runtime And MP-SEL-001 Profile Evidence Are Complete

- Covers: R4, R6, R7, R22, R23, EC4, EC5
- Level: manual
- Fixture/setup: Stable worktree state and change-local evidence files under `docs/changes/2026-06-27-selector-regression-runtime-reduction/`.
- Steps: Record `/usr/bin/time -p python scripts/test-select-validation.py` baseline evidence, using at least three same-environment runs and median comparison when practical. Create `selector-regression-profile.md` and `selector-regression-runtime-baseline.yaml`.
- Expected result: Profile evidence records proof ID, environment, commit or HEAD, worktree state, commands, baseline duration, timeout behavior, selected checks observed, dominant contributors or instrumentation limitations, safe reduction identified, no-safe-reduction rationale when applicable, and follow-up decision. Baseline YAML records command, environment, repository state, test count, duration, selected-check identity, limitations, and preservation baseline.
- Failure proves: Implementation closeout would rely on unauditable performance evidence.
- Automation location: Manual evidence in `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md` and `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml`; command `/usr/bin/time -p python scripts/test-select-validation.py`.

### T3. Preservation Evidence Separates Behavioral, Selected-Check, And Test-Runner Identity

- Covers: R8, R9, R10, R11, R27, E2, EC3
- Level: contract
- Fixture/setup: Baseline and revised selector scenarios, changed-path fixtures, selected checks, route reasons, pass/fail outcomes, and unittest IDs from the selector-regression suite.
- Steps: Record baseline and revised preservation evidence in `selector-regression-preservation.md`; compare behavioral selector identity and selected-check identity for each required fixture; record unittest identifier identity or an approved test-structure delta.
- Expected result: Behavioral selector identity and selected-check identity are preserved unless an approved spec change is cited. Test-name-only deltas are identified as test-structure deltas and do not mask selector behavior changes.
- Failure proves: The optimized suite may be faster because it changed selector behavior or selected routing.
- Automation location: `scripts/test-select-validation.py`, especially selector identity tests such as `test_selector_preservation_surface_keeps_selected_check_identity`; evidence file `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`.

### T4. Pure Selector Fixtures Run In Process Without Mutable State Leakage

- Covers: R12, R30, E2, EC9
- Level: unit
- Fixture/setup: Table-driven changed-path fixtures for source paths, spec paths, test-spec paths, lifecycle artifacts, review records, unknown evidence paths, broad-smoke classification paths, and selector implementation paths.
- Steps: Exercise pure selector scenarios through in-process selector calls where CLI parsing, process boundaries, wrapper behavior, exit codes, timeout behavior, output shape, and rerun guidance are not under test. Reuse immutable fixtures or reset fixture state between test groups.
- Expected result: In-process cases produce the same selected checks, route reasons, blockers, and pass/fail outcomes as the baseline. Mutating one fixture cannot affect a later fixture.
- Failure proves: In-process conversion changed selector semantics or fixture reuse introduced state leakage.
- Automation location: `scripts/test-select-validation.py`, under `ValidationSelectionTests` or new focused fixture tests.

### T5. CLI Boundary Behavior Remains Subprocess-Backed

- Covers: R13, R14, R20, R29, E3, EC2, EC10
- Level: integration
- Fixture/setup: Existing `run_selector`, `run_runner`, and `run_ci` subprocess helpers; invalid-argument, output-contract, timeout, wrapper, and rerun-guidance fixtures.
- Steps: Run subprocess-backed tests for selector CLI JSON output, invalid invocation, blocked selector output, output summaries, failure diagnostics, rerun guidance, selected-CI wrapper execution, and timeout or signal behavior.
- Expected result: Command-boundary behavior is asserted through subprocess execution, including parsing, return codes, stdout or stderr shape, timeout override behavior, wrapper integration, and rerun guidance.
- Failure proves: In-process tests replaced command-boundary proof or diagnostics are no longer actionable.
- Automation location: `scripts/test-select-validation.py`, including `ScriptOutputContractTests`, `test_cli_outputs_json_for_classified_skill_path`, `test_missing_mode_specific_inputs_return_json_error`, `test_ci_wrapper_executes_selector_selected_path_and_root_checks`, `test_ci_wrapper_timeout_and_signal_failures_have_distinct_statuses`, and related wrapper tests.

### T6. Missing-Route Blockers And Registered Routes Preserve Failure Sensitivity

- Covers: R8, R9, R15, R16, R29, E4, EC1, EC10
- Level: integration
- Fixture/setup: Missing-route and registered-route changed-path fixtures for unknown changed paths, unregistered change evidence, unknown lifecycle artifacts, new evidence classes without selector routes, and registered evidence classes.
- Steps: Run selector scenarios that must block on missing routes and scenarios that must select expected checks for registered routes. Verify blocker diagnostics include path, path class, expected action, and corrective guidance when available.
- Expected result: Missing routes remain hard blockers, broad-smoke does not erase missing-route blockers, and registered routes still select expected checks.
- Failure proves: Runtime reduction weakened route blocking, registered routing, or failure diagnostics.
- Automation location: `scripts/test-select-validation.py`, including `test_unregistered_change_evidence_produces_registration_debt`, `test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker`, `test_unclassified_path_blocks_without_fail_open`, `test_mixed_classified_and_unclassified_paths_block_partial_execution`, `test_registered_change_evidence_selects_declared_checks_and_governing_metadata`, and the planned table-driven negative fixtures.

### T7. Cache-Boundary And Broad-Smoke Classification Behavior Stay Unchanged

- Covers: R17, R18, R19, EC6, EC7
- Level: integration
- Fixture/setup: Cache-boundary selector checks and broad-smoke child classification fixtures.
- Steps: Assert selected checks still report `cache_status: not-applicable` for this slice; run broad-smoke classification tests; inspect the broad-smoke wrapper body to ensure runtime remains sequential and no parallel-safe execution path is introduced.
- Expected result: Cache-boundary metadata remains `not-applicable`; broad-smoke classification rows retain required fields and expected pass/fail behavior; broad-smoke execution behavior remains unchanged; no caching, workers, broad validator composition, or broad-smoke parallelism appears.
- Failure proves: This selector-regression slice crossed into excluded cache or broad-smoke execution behavior.
- Automation location: `scripts/test-select-validation.py`, including cache-status assertions, `test_broad_smoke_child_classification_covers_ci_children`, `test_broad_smoke_classification_blocks_unsafe_candidate_claims`, and `test_broad_smoke_classification_keeps_runtime_sequential`.

### T8. Revised Runtime Result Or No-Safe-Reduction Closeout Is Auditable

- Covers: R5, R6, R7, R21, R24, R25, R26, R27, R28, E5, EC4, EC5, EC8
- Level: manual
- Fixture/setup: Completed M2 implementation or complete profiling evidence proving no safe selector reducer; baseline evidence from T2; preservation evidence from T3.
- Steps: Record revised `/usr/bin/time -p python scripts/test-select-validation.py` evidence in a comparable environment, using at least three paired runs and median comparison when practical. Compare baseline and revised evidence. If no success target is safely met, record no-safe-reduction rationale and next measured runtime target.
- Expected result: Runtime result YAML records baseline, revised, delta, percent, selected-check identity, preservation result, timeout behavior, limitations, and whether the 25% median target or selected-CI timeout target was met. If neither target is met, the no-safe-reduction record names the dominant bottleneck and next target without claiming runtime improvement.
- Failure proves: The work claims speedup without auditable runtime evidence, preservation proof, timeout status, or safe fallback rationale.
- Automation location: `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml`; command `/usr/bin/time -p python scripts/test-select-validation.py`.

### T9. Selected-CI Wrapper Compatibility And Timeout Status Are Preserved

- Covers: R1, R2, R14, R20, R21, R25, E1, EC8
- Level: integration
- Fixture/setup: Selected-CI explicit mode with touched selector paths and change-local evidence paths.
- Steps: Run selected-CI wrapper coverage with explicit paths and timeout flags as named by the plan. Verify selector arguments, execution flags, wrapper diagnostics, selected checks, and timeout behavior.
- Expected result: `bash scripts/ci.sh --mode explicit --timeout 300 ...` remains compatible. Execution flags are handled by the wrapper without corrupting selector arguments. Timeout override status is recorded after revised runtime evidence.
- Failure proves: Selector-regression restructuring broke selected-CI compatibility or hid the timeout override boundary.
- Automation location: `scripts/test-select-validation.py` wrapper tests and plan command `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`.

### T10. Lifecycle Evidence And Scope Guardrails Validate

- Covers: R19, R28
- Level: smoke
- Fixture/setup: Touched lifecycle-managed artifacts, change metadata, review evidence, plan body, and plan index.
- Steps: Run artifact lifecycle validation, change metadata validation, review artifact structure validation, and diff hygiene checks for touched artifacts. Confirm the evidence does not claim final verify, branch readiness, PR readiness, or hosted CI success before those stages run.
- Expected result: Lifecycle artifacts remain internally consistent; change metadata references the test spec; review evidence remains clean; broad-smoke, cache, validator composition, final verify, branch readiness, PR readiness, and hosted CI semantics are unchanged.
- Failure proves: The test-planning or implementation slice drifted beyond the approved scope or left lifecycle state stale.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/selector-regression-runtime-reduction.md --path specs/selector-regression-runtime-reduction.test.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`; `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`; `git diff --check -- docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md specs/selector-regression-runtime-reduction.test.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`.

## Fixtures and data

- Changed source path fixture: a path that selects source or script validation.
- Changed spec path fixture: a path under `specs/` that selects lifecycle and spec-related checks.
- Changed test-spec path fixture: a path under `specs/*.test.md` that selects test-spec and lifecycle checks where applicable.
- Changed lifecycle artifact fixture: proposal, spec, plan, review, review-resolution, verify, or PR handoff artifact paths.
- Changed review record fixture: review files under a change-local `reviews/` directory and the matching review-log path.
- Unknown evidence path fixture: unregistered change-local evidence that must block unless owner-deferred with complete fields.
- Registered evidence path fixture: known registered change evidence such as selector profile, runtime baseline, runtime result, preservation proof, or broad-smoke classification evidence.
- Broad-smoke classification fixture: rows parsed from the existing classification artifact and `scripts/ci.sh` child checks.
- Selector implementation path fixture: `scripts/validation_selection.py` and `scripts/test-select-validation.py`, which must select `selector.regression`.
- CLI invalid-argument fixture: invalid selector arguments that produce JSON error output and non-zero exit status.
- Wrapper timeout fixture: selected-CI workspace or fixture command proving timeout override behavior.
- Evidence files:
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`

## Mocking/stubbing policy

Use temporary repositories and fixture workspaces for repository-state and selected-CI wrapper scenarios. Do not mock selector outputs for pure selector behavior when the selector library can be called directly. It is acceptable to use existing wrapper fixture mechanisms for selected-CI command execution, malformed selector output, timeout, signal, and unavailable-command scenarios because those tests target wrapper behavior.

Do not stub subprocess execution for CLI-boundary behavior. Do not use network access. Do not use cache hits as proof for this slice.

## Migration or compatibility tests

Compatibility is covered by T1 and T9. The default selector-regression command remains `python scripts/test-select-validation.py`, and selected-CI wrapper behavior remains compatible. No historical evidence migration is required.

## Observability verification

T2, T3, and T8 verify reviewable evidence for environment, command, repository state, test count, selected checks, route reasons, blocker diagnostics, baseline and revised duration, delta, timeout behavior, limitations, preservation result, and no-safe-reduction rationale when applicable.

T5 and T6 verify command-line diagnostics remain actionable by preserving failure reason, affected path or fixture class, expected outcome, observed outcome, and corrective action or rerun guidance when available.

## Security/privacy verification

T2 and T8 evidence must not record secrets, credentials, tokens, private keys, or host-specific debug paths unless intentionally reviewed as fixture data. Runtime commands should be recorded explicitly enough to rerun without shell-dependent local workarounds.

## Performance checks

Performance proof is manual and evidence-backed:

- Baseline: `/usr/bin/time -p python scripts/test-select-validation.py`
- Revised: `/usr/bin/time -p python scripts/test-select-validation.py`
- Pairing: at least three same-environment paired runs and median comparison when practical.
- Primary success target: at least 25% median reduction with preservation.
- Alternative success target: selected-CI no longer requires the 180-second timeout override for selector-regression execution with preservation.
- Fallback: complete no-safe-reduction record naming dominant bottleneck and next measured runtime target.

## Manual QA checklist

- MP-SEL-001 profile proof exists.
- Profile proof records proof ID, environment, commit or HEAD, worktree state, commands, baseline duration, timeout behavior, selected checks observed, dominant contributors or instrumentation limitations, safe reduction identified, no-safe-reduction rationale when applicable, and follow-up decision.
- Baseline runtime YAML exists and records required fields.
- Revised runtime YAML or no-safe-reduction record exists and records required fields.
- Preservation proof compares behavioral selector identity, selected-check identity, unittest identifier identity or approved test-structure delta, missing-route blockers, registered routes, CLI behavior, diagnostics, broad-smoke classification, cache boundary, and final-verify boundary.
- Timeout override status is recorded.
- Runtime evidence does not claim final verify, branch readiness, PR readiness, hosted CI success, broad-smoke parallel readiness, or cache readiness.

## What not to test and why

- Do not test broad-smoke parallel execution; this slice must keep broad-smoke runtime sequential.
- Do not test validation-result caching, remote/shared caching, or cache-hit final proof; caching requires a separate approved contract.
- Do not test persistent validation workers or broad validator composition; they are excluded architecture surfaces.
- Do not test final verify, branch readiness, PR readiness, or hosted CI success as outcomes of selector-runtime evidence.
- Do not add or validate a first-slice quick or fast mode; the default command is the target.

## Uncovered gaps

None. If implementation discovers a need for persistent workers, shared caches, broad validator composition, cross-process execution protocols, or changed selector semantics, return to spec or architecture before implementation proceeds.

## Next artifacts

- test-spec-review
- implementation after test-spec-review approval
- code-review for each implementation milestone
- explain-change
- verify
- pr

## Follow-on artifacts

- Test-spec-review R1: `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/test-spec-review-r1.md`

## Readiness

Approved by `test-spec-review-r1` for implementation handoff. This test spec defines the proof surface only; it does not claim implementation, validation, branch readiness, or PR readiness.
