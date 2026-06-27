# Selector-Regression Runtime Reduction

## Status

approved

## Related proposal

- Proposal: [Selector-Regression Runtime Reduction With Coverage-Preservation Proof](../docs/proposals/2026-06-27-selector-regression-runtime-reduction.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r1.md)
- Proposal review R2: [proposal-review-r2](../docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r2.md)
- Parent runtime spec: [Validation Runtime Follow-Through](validation-runtime-follow-through.md)
- Prior runtime foundation: [Validation Execution Performance and Preflight](validation-execution-performance-and-preflight.md)

## Goal and context

The previous validation-runtime follow-through work produced measurement, proof preservation, selector-route blockers, and broad-smoke classification, but did not introduce a runtime-reducing mechanism. The current focused target is the selected-validation regression command:

```bash
python scripts/test-select-validation.py
```

Recorded evidence put that command at about 140 seconds for 102 tests, making it a developer inner-loop bottleneck. Broad-smoke remains the larger boundary-validation cost, but broad-smoke parallelism, validation-result caching, persistent workers, and broad validator composition are separate risk profiles and are outside this spec.

This spec defines the observable contract for reducing selector-regression runtime only by removing duplicate execution work while preserving selector behavior, missing-route blockers, CLI command boundaries, failure diagnostics, and final verification semantics.

## Glossary

- `selector-regression command`: the default `python scripts/test-select-validation.py` command.
- `selector-regression coverage`: required tests and fixtures that prove selected-validation routing, selected check selection, missing-route blockers, cache-boundary metadata, broad-smoke classification metadata, CLI behavior, wrapper behavior, exit codes, output shape, timeout behavior, rerun guidance, and diagnostics.
- `behavioral selector identity`: the set of selector scenarios, changed-path fixtures, expected selected checks, expected blockers, and expected pass/fail outcomes that define the selector contract.
- `selected-check identity`: the selected check IDs, route reasons, and path triggers produced for each selector scenario.
- `unittest identifier identity`: the test runner's test IDs or names for selector-regression cases.
- `CLI-boundary behavior`: behavior observable only through command execution, including argument parsing, exit codes, stdout, stderr, timeout override behavior, wrapper integration, and rerun guidance.
- `pure selector logic`: selector behavior that can be observed without proving command-line parsing, process boundaries, or wrapper behavior.
- `failure sensitivity`: proof that negative cases still fail when selector routing, cache-boundary metadata, broad-smoke classification metadata, or wrapper configuration is wrong.
- `no-safe-reduction record`: evidence that profiling found no safe runtime reducer and identifies the dominant bottleneck plus the next measured target.

## Examples first

Example E1: default command remains complete
Given a contributor runs `python scripts/test-select-validation.py`
When the selector-regression suite completes
Then the command includes all required selector-regression coverage
And no required selector-regression category is available only through an optional quick or fast command.

Example E2: pure selector cases move in process without changing behavior
Given a changed source path fixture selects the same check IDs before the refactor
When that fixture is exercised through an in-process selector path after the refactor
Then behavioral selector identity and selected-check identity are unchanged
And no CLI-boundary assertion is removed from the dedicated subprocess coverage.

Example E3: CLI-boundary cases remain subprocess-backed
Given a selector CLI invocation has invalid arguments
When the selector-regression suite exercises command-boundary behavior
Then the test proves the command exit code, stderr or stdout shape, and rerun guidance through subprocess execution.

Example E4: missing-route blockers remain hard failures
Given a changed path belongs to a lifecycle or evidence class that requires deterministic selector routing
When no selector route applies
Then selector validation reports a hard missing-route blocker
And the optimized selector-regression suite still fails if that blocker is weakened or hidden.

Example E5: runtime target does not override proof preservation
Given the revised selector-regression command does not meet the 25% paired median runtime target
When behavioral selector identity, selected-check identity, CLI-boundary coverage, and failure sensitivity are preserved
Then the work may close only with a no-safe-reduction record naming the next measured bottleneck
And it must not delete required coverage to meet the target.

## Requirements

R1. The selector-regression command MUST remain the default complete regression path for required selector-regression coverage.

R2. The selector-regression command MUST NOT move required selector-regression coverage into an optional-only `--fast`, `--quick`, filtered, skipped, or expected-failure path.

R3. Runtime reduction MUST come from reducing duplicate work, subprocess repetition, repeated repository-state discovery, repeated fixture setup, or other measured overhead, not from reducing required selector-regression coverage.

R4. Before accepting a runtime-reducing implementation, the change MUST record baseline runtime evidence for the selector-regression command.

R5. Before accepting a runtime-reducing implementation, the change MUST record revised runtime evidence for the selector-regression command under a comparable environment or record why exact comparability was not practical.

R6. Runtime evidence SHOULD use at least three same-environment paired runs and compare medians when practical.

R7. Runtime evidence MUST record command, environment, repository state, test count, baseline duration, revised duration, delta, timeout behavior, limitations, and preservation result.

R8. The implementation MUST preserve behavioral selector identity for all required selector scenarios unless an approved spec change explicitly changes selector behavior.

R9. The implementation MUST preserve selected-check identity for each changed-path fixture unless an approved spec change explicitly changes selected-check routing.

R10. The implementation MUST treat unittest identifier identity as preservation evidence, but a test-name-only delta MAY be accepted when the change records an approved test-structure delta and preserves behavioral selector identity plus selected-check identity.

R11. The selector-regression suite MUST distinguish behavioral selector identity, selected-check identity, and unittest identifier identity in its preservation evidence.

R12. Pure selector logic MAY be exercised in process when command-line parsing, process boundary behavior, wrapper behavior, exit code behavior, timeout behavior, output shape, and rerun guidance are not the behavior under test.

R13. CLI-boundary behavior MUST remain covered through subprocess execution.

R14. Subprocess coverage MUST include CLI parsing, exit codes, stdout or stderr diagnostics, timeout override behavior, wrapper integration, and rerun guidance.

R15. Missing selector-route cases MUST remain hard failures.

R16. Missing-route failure evidence MUST cover unknown changed paths, unregistered change evidence, unknown lifecycle artifacts, new evidence classes without selector routes, and at least one registered route that still selects expected checks.

R17. Cache-boundary metadata for this slice MUST remain `not-applicable` unless a separate approved cache proposal changes the cache contract.

R18. Broad-smoke classification fixtures MUST preserve their expected pass and fail behavior, but this spec MUST NOT enable broad-smoke parallel execution.

R19. The implementation MUST NOT enable validation-result caching, remote/shared caching, persistent validation workers, or broad validator composition.

R20. The implementation MUST preserve selected-CI wrapper compatibility for selected selector-regression execution.

R21. The implementation MUST record whether the selected-CI timeout override remains required after the revised selector-regression runtime evidence.

R22. The selector-regression profile proof MUST exist before implementation closeout.

R23. The selector-regression profile proof MUST record proof ID, environment, commit or HEAD, worktree state, commands, baseline duration, timeout behavior, selected checks observed, dominant contributors or instrumentation limitations, safe reduction identified, no-safe-reduction rationale when applicable, and follow-up decision.

R24. The preferred success target SHOULD be at least a 25% paired median runtime reduction for the selector-regression command while preserving behavioral selector identity, selected-check identity, CLI-boundary behavior, and failure sensitivity.

R25. The alternative success target SHOULD be that selected CI no longer requires the 180-second timeout override for the selector-regression path while preserving behavioral selector identity, selected-check identity, CLI-boundary behavior, and failure sensitivity.

R26. If neither success target is met, the change MAY close only with a complete no-safe-reduction record that names the dominant bottleneck and next measured runtime target.

R27. Lower elapsed time alone MUST NOT be accepted as success unless preservation evidence passes.

R28. Final verify semantics MUST remain unchanged; selector-regression runtime evidence MUST NOT claim final verification, branch readiness, PR readiness, or hosted CI success.

R29. Failure diagnostics MUST remain actionable by identifying the failed selector scenario, changed path or fixture class when applicable, expected outcome, observed outcome, and corrective action or rerun guidance when available.

R30. Any reusable fixtures introduced by this work MUST avoid cross-test mutable state leakage or reset state between test groups.

## Inputs and outputs

Inputs include selector-regression commands, selected-CI wrapper invocations, changed-path fixtures, selector route fixtures, missing-route negative fixtures, cache-boundary fixtures, broad-smoke classification fixtures, CLI argument fixtures, timeout override fixtures, baseline timing measurements, revised timing measurements, repository state, Python version, OS, runner type, and worktree state.

Outputs include selector-regression pass/fail results, selected check IDs, selector route reasons, blocker diagnostics, CLI stdout and stderr, exit codes, timeout behavior, baseline runtime evidence, revised runtime evidence, preservation evidence, profile proof, and no-safe-reduction record when applicable.

## State and invariants

- Required selector-regression coverage remains complete through the default command.
- Runtime improvement is valid only when proof preservation also passes.
- Behavioral selector identity and selected-check identity are mandatory preservation surfaces.
- Unittest identifier identity is useful evidence but is not the sole preservation contract.
- CLI-boundary behavior remains subprocess-backed.
- Missing selector routes remain blockers.
- Broad-smoke, cache, broad validator composition, final verify, branch readiness, and PR readiness semantics remain unchanged.

## Error and boundary behavior

- If baseline runtime evidence is missing, implementation closeout is blocked.
- If revised runtime evidence is missing, implementation closeout is blocked unless the work records a no-safe-reduction result from complete profiling evidence.
- If behavioral selector identity changes without an approved selector contract change, implementation closeout is blocked.
- If selected-check identity changes without an approved selector routing change, implementation closeout is blocked.
- If a missing-route fixture stops failing, implementation closeout is blocked even when runtime improves.
- If CLI-boundary subprocess coverage is removed for command-boundary behavior, implementation closeout is blocked.
- If the default selector-regression command omits required coverage, implementation closeout is blocked.
- If runtime variance prevents stable measurement, the evidence must record limitations and use same-environment paired runs where possible.

## Compatibility and migration

Existing contributor and CI entry points remain compatible. The default selector-regression command remains `python scripts/test-select-validation.py`. Selected-CI wrapper behavior remains compatible, including timeout override behavior while evidence determines whether the override is still needed.

No migration of historical selector-regression evidence is required. New evidence for this slice should use the change-local paths named by the accepted proposal.

Rollback restores prior selector-regression test structure if coverage, diagnostics, or CLI-boundary behavior regress. Profiling and runtime evidence may remain as historical evidence after rollback, but runtime improvement must not be claimed after rollback.

## Observability

Runtime and preservation evidence must be reviewable from tracked or change-local artifacts.

The selector-regression profile evidence records environment, command, repository state, selected checks, dominant contributors or instrumentation limitations, and the safe reduction decision.

The selector-regression preservation evidence records behavioral selector identity, selected-check identity, unittest identifier identity or approved test-structure delta, missing-route failure sensitivity, registered-route behavior, CLI-boundary coverage, diagnostics, broad-smoke classification behavior, cache-boundary metadata, and final-verify boundary preservation.

## Security and privacy

Selector-regression runtime and preservation evidence must not record secrets, credentials, tokens, private keys, or host-specific debug paths unless they are intentionally part of reviewed fixtures. Commands should use explicit arguments rather than shell-dependent strings when repository-owned tooling controls invocation.

## Accessibility and UX

No graphical or web UI accessibility impact. Command-line diagnostics should remain readable and actionable for contributors. Output reduction is acceptable only when it does not remove failure reason, affected path or fixture, expected outcome, observed outcome, or rerun guidance needed to fix selector failures.

## Performance expectations

The primary success target is at least a 25% paired median runtime reduction for `python scripts/test-select-validation.py` in a comparable environment while preserving required proof.

The alternative success target is eliminating the need for the 180-second selected-CI timeout override for the selector-regression path while preserving required proof.

These targets are success targets, not permission to remove coverage. If neither target is safely achieved, the acceptable closeout path is a complete no-safe-reduction record that names the next measured bottleneck.

## Edge cases

EC1. The revised suite is faster but omits a missing-route negative fixture.

EC2. The revised suite preserves selected-check identity but removes subprocess coverage for CLI parsing.

EC3. Pure selector tests are converted in process and unittest names change while behavioral selector identity and selected-check identity remain unchanged.

EC4. Runtime measurements vary across runs enough that median comparison is inconclusive.

EC5. Profiling shows subprocess startup is not dominant and no safe selector-runtime reduction is available.

EC6. A broad-smoke classification fixture fails after selector-regression restructuring.

EC7. Cache-boundary metadata changes from `not-applicable` without a separate approved cache contract.

EC8. The selected-CI wrapper still requires the 180-second timeout override after optimization.

EC9. A shared fixture leaks state and makes a later selector fixture pass or fail incorrectly.

EC10. Diagnostic output is shortened enough that a contributor can no longer identify the failed route or corrective action.

## Non-goals

- Do not reduce runtime by deleting required selector-regression coverage.
- Do not add a first-slice `--fast` or `--quick` command as the primary speed mechanism.
- Do not change selector routing semantics merely to make tests pass faster.
- Do not remove subprocess tests that prove CLI or wrapper behavior.
- Do not enable broad-smoke parallel execution.
- Do not enable validation-result caching, remote/shared caching, or cache-hit final proof.
- Do not introduce persistent validation workers.
- Do not compose broad validators into one in-process runner.
- Do not change final verify, branch readiness, PR readiness, or hosted CI semantics.
- Do not claim runtime improvement when proof preservation fails or after rollback.

## Acceptance criteria

AC1. Baseline selector-regression runtime evidence exists for `python scripts/test-select-validation.py`.

AC2. Revised selector-regression runtime evidence exists for `python scripts/test-select-validation.py`, or a complete no-safe-reduction record explains why no revised runtime reduction was safely available.

AC3. Baseline and revised runtime evidence are comparable, or measurement limitations are recorded with same-environment paired runs where practical.

AC4. Behavioral selector identity is preserved or an approved selector contract change is cited.

AC5. Selected-check identity is preserved or an approved selector routing change is cited.

AC6. Unittest identifier identity is preserved or an approved test-structure delta records why changed test IDs do not change behavioral selector identity or selected-check identity.

AC7. The default `python scripts/test-select-validation.py` command continues to run all required selector-regression contract coverage.

AC8. No required selector-regression category is moved to an optional-only command.

AC9. Missing selector-route blockers still fail.

AC10. Registered selector routes still select the expected checks.

AC11. CLI-boundary subprocess coverage remains present for CLI parsing, exit codes, stdout or stderr diagnostics, timeout override behavior, wrapper integration, and rerun guidance.

AC12. In-process tests are used only where command-boundary behavior is not under test.

AC13. Cache-boundary metadata remains `not-applicable` unless a separate approved cache proposal changes it.

AC14. Broad-smoke classification fixtures preserve expected pass and fail behavior, and broad-smoke execution behavior remains unchanged.

AC15. Selected-CI wrapper compatibility is preserved, and timeout override status is recorded.

AC16. Failure diagnostics remain actionable.

AC17. No broad-smoke, cache, validator-composition, final-verify, branch-readiness, PR-readiness, or hosted-CI behavior changes are introduced.

AC18. Runtime improvement is measured and attributed to this slice, or a no-safe-reduction rationale names the next measured bottleneck.

## Open questions

None for this spec. Broad-smoke parallelism, validation caching, broad validator composition, persistent workers, and permanent runtime budgets require separate approved artifacts.

## Next artifacts

- spec-review
- test-spec amendment or focused test spec
- plan
- plan-review
- implementation
- code-review
- explain-change
- verify
- pr

Architecture is not expected unless implementation introduces persistent workers, shared caches, broad validator composition, or new cross-process execution protocols.

## Follow-on artifacts

- Spec review: `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/spec-review-r1.md`
- Plan: `docs/plans/2026-06-27-selector-regression-runtime-reduction.md`
- Test spec: `specs/selector-regression-runtime-reduction.test.md`
- Test-spec review: `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/test-spec-review-r1.md`

## Readiness

Approved for planning and test-spec authoring.
