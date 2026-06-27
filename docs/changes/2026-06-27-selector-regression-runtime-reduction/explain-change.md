# Explain Change: Selector-Regression Runtime Reduction

Change ID: 2026-06-27-selector-regression-runtime-reduction
Stage: explain-change
Recorded: 2026-06-27
Status: complete
Final verify: not claimed
PR readiness: not claimed

## Summary

This change reduces `python scripts/test-select-validation.py` runtime by removing repeated selector repository preflight work, not by deleting selector-regression coverage. It also records baseline, profile, preservation, and revised runtime evidence so the speedup is auditable.

The measured result is a baseline median of `164.73s` for 109 tests and a revised median of `36.23s` for 111 tests, a `78.01%` median reduction. The revised selected-CI wrapper evidence shows the selector-regression path passes under the default timeout without the earlier 180-second override.

## Problem

The preceding validation-runtime work produced a `0%` validated feature-caused runtime improvement because it added measurement and proof-preservation infrastructure but no runtime-reducing mechanism. The accepted proposal identified `selector.regression` as the developer inner-loop bottleneck and kept broad-smoke parallelism, validation caching, broad validator composition, and final verify changes out of this slice.

The invariant for the change is:

```text
Runtime improvement must come from less duplicate work, not less validation.
```

## Decision Trail

The proposal selected a focused selector-regression runtime-reduction slice after comparing doing nothing, broad-smoke parallelism, caching, broad validator composition, and selector-regression duplicate-work reduction.

The approved spec required:

- `R1`-`R3`: keep the default selector-regression command complete and reduce duplicate work rather than proof.
- `R4`-`R7`: record baseline and revised runtime evidence with comparable environment, counts, deltas, timeout behavior, and limitations.
- `R8`-`R11`: preserve behavioral selector identity, selected-check identity, and distinguish unittest identifier deltas.
- `R12`-`R14`: move only pure selector logic in process and retain subprocess coverage for command boundaries.
- `R15`-`R18`: preserve missing-route blockers, cache-boundary metadata, and broad-smoke classification behavior.
- `R19`: avoid caching, workers, broad validator composition, and broad-smoke parallelism.
- `R20`-`R21`: preserve selected-CI wrapper compatibility and record timeout status.
- `R22`-`R23`: complete `MP-SEL-001` profile proof before closeout.
- `R24`-`R30`: meet the runtime target only with preservation proof, maintain diagnostics, and avoid fixture leakage.

No architecture artifact was required because the implementation did not introduce persistent workers, shared caches, broad validator composition, or a new cross-process protocol.

The plan split implementation into three reviewed milestones:

- M1 recorded baseline runtime, profile, and preservation inventory.
- M2 introduced reusable in-process selector preflight context for pure selector tests.
- M3 recorded revised runtime evidence, timeout status, preservation closeout, and a duration-output regression fix discovered during timing.

Code reviews `code-review-r1`, `code-review-r2`, and `code-review-r3` closed all implementation milestones with no material findings.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/validation_selection.py` | Added `RepositoryPreflightContext` ownership data, public `build_repository_preflight_context`, optional `SelectionRequest.preflight_context`, root-identity validation, and selector-runtime evidence routing. | Reuse expensive repository-state discovery only when the context has complete repository identity, and ensure required runtime evidence files do not create manual-routing debt. | Spec `R3`, `R12`, `R22`-`R23`, `R30`; plan M1/M2. | `test_selector_runtime_evidence_files_route_without_manual_debt`; `test_shared_preflight_context_requires_matching_repository_identity`; selector selected-check proof. |
| `scripts/test-select-validation.py` | Reused one root preflight context for pure selector calls; added identity-guard and selector-runtime evidence tests; retained subprocess CLI and wrapper tests; added duration-reporting regression guard. | Remove repeated `git rev-parse`, `git status`, and `git ls-files` work for pure selector fixtures while preserving command-boundary proof. | Spec `R1`-`R16`, `R20`, `R29`-`R30`; test spec T1-T6, T9. | Full default command timing, `-k selector`, targeted duration and broad-smoke tests. |
| `scripts/ci.sh` | Replaced Bash `$SECONDS` elapsed math with `current_epoch_seconds` and `elapsed_seconds_since`, clamping negative elapsed values to zero. | M3 timing exposed broad-smoke output like `-2s`; selector-regression cannot close with a known default-command failure. | Spec `R18`, `R20`, `R29`; plan M3 decision log. | `test_ci_wrapper_duration_reporting_does_not_use_bash_seconds`; broad-smoke success, verbose, and failure-output tests. |
| `docs/changes/.../selector-regression-profile.md` | Recorded `MP-SEL-001` environment, commands, profile observations, dominant contributor, and safe reduction decision. | Make profiling auditable before relying on optimization decisions. | Spec `R22`-`R23`; test spec T2. | M1 grouped timings showed `ValidationSelectionTests` dominated runtime. |
| `docs/changes/.../selector-regression-runtime-baseline.yaml` | Recorded three baseline runs, selected-check identity, environment, and limitations. | Establish comparable baseline before runtime-reducing code. | Spec `R4`, `R6`-`R7`; test spec T2. | Median real runtime `164.73s`, 109 tests. |
| `docs/changes/.../selector-regression-runtime-result.yaml` | Recorded three revised runs, delta, preservation status, and selected-CI timeout status. | Prove the runtime target was met with preservation evidence. | Spec `R5`-`R7`, `R21`, `R24`-`R28`; test spec T8-T10. | Median real runtime `36.23s`, 111 tests, `78.01%` reduction, no timeout override needed. |
| `docs/changes/.../selector-regression-preservation.md` | Recorded behavioral identity, selected-check identity, unittest identifier deltas, missing-route blockers, CLI-boundary coverage, cache boundary, broad-smoke classification, and final-verify boundary. | Prevent runtime improvement from being accepted if proof coverage regresses. | Spec `R8`-`R18`, `R27`-`R30`; test spec T3, T6, T7. | Approved test-structure deltas for two added tests; selected checks preserved for touched path sets. |
| `docs/proposals/...`, `specs/...`, `docs/plans/...`, `docs/plan.md`, review artifacts, and `change.yaml` | Recorded the accepted proposal, approved spec, active test spec, plan milestones, review receipts, metadata, and lifecycle handoffs. | Keep workflow state and durable reasoning synchronized for a planned initiative. | Repository workflow contract; plan M1-M3. | Lifecycle, metadata, review-artifact, and diff-hygiene validators. |

## Tests Added Or Changed

- `ValidationSelectionTests.test_selector_runtime_evidence_files_route_without_manual_debt`: proves selector-runtime baseline and result YAML files are registered change evidence and route to lifecycle validation instead of blocking selected CI.
- `ValidationSelectionTests.test_shared_preflight_context_requires_matching_repository_identity`: proves a reused preflight context cannot be applied to a different repository root.
- `ValidationSelectionTests.test_first_slice_representative_categories_route_or_block_safely`: exercises representative pure selector categories through the lower-overhead in-process path while preserving route/block behavior.
- `ValidationSelectionTests.test_ci_wrapper_duration_reporting_does_not_use_bash_seconds`: prevents regression to Bash `$SECONDS`, which produced negative elapsed output during M3 timing.
- Existing CLI, wrapper, missing-route, cache-boundary, and broad-smoke classification tests were retained to keep command-boundary and failure-sensitivity proof in the default regression path.

The test levels match the risk: pure selector behavior is tested in process, while CLI parsing, exit codes, wrapper behavior, timeout behavior, output shape, and rerun guidance remain subprocess-backed.

## Validation Evidence Available Before Final Verify

M1 evidence:

- `python scripts/test-select-validation.py -k selector_runtime_evidence_files_route_without_manual_debt`: failed before runtime evidence registration, then passed.
- `/usr/bin/time -p python scripts/test-select-validation.py`: three baseline runs passed; median real duration `164.73s`, 109 tests.
- Grouped profiling showed `ValidationSelectionTests` at about `164.20s`, making repeated selector preflight discovery the dominant safe target.
- Artifact lifecycle, change metadata, review artifact, and diff hygiene checks passed for M1.

M2 evidence:

- `python scripts/test-select-validation.py -k shared_preflight_context_requires_matching_repository_identity`: failed before production support, then passed.
- `/usr/bin/time -p python scripts/test-select-validation.py -k first_slice_representative_categories_route_or_block_safely`: passed in `real 1.05s`.
- `python scripts/test-select-validation.py -k selector`: passed.
- `/usr/bin/time -p python scripts/test-select-validation.py`: passed with 110 tests in `real 35.09s`.
- Selected-CI explicit wrapper command with `--timeout 300`: passed and selected `artifact_lifecycle.validate` plus `selector.regression`.

M3 evidence:

- `python scripts/test-select-validation.py -k duration_reporting_does_not_use_bash_seconds`: failed before replacing `$SECONDS`, then passed.
- Broad-smoke default, verbose, and failure-output targeted tests passed.
- `/usr/bin/time -p python scripts/test-select-validation.py`: three final revised runs passed; median real duration `36.23s`, 111 tests.
- Selected-CI explicit wrapper command passed without timeout override and with `--timeout 300`.
- `python scripts/test-select-validation.py -k selector`: passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`: passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: passed.
- `git diff --check -- ...`: passed.

This evidence is pre-final-verify evidence only. It does not claim hosted CI success, branch readiness, PR readiness, or final verification.

## Review Resolution Summary

Review resolution is closed:

- Material findings: `0`
- Open findings: `0`
- `needs-decision`: none

See `docs/changes/2026-06-27-selector-regression-runtime-reduction/review-resolution.md` and the review records under `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/`.

## Alternatives Rejected

- Do nothing: rejected because it leaves the selected-validation bottleneck in place.
- Start with broad-smoke parallelism: deferred because broad-smoke has a different side-effect and resource-safety profile.
- Enable caching: deferred because cache proof needs complete input identity and final-proof boundaries.
- Broad validator composition: deferred because it is a larger architecture change and was not needed after profiling identified duplicate selector preflight work.
- Add a `--fast` or `--quick` mode: rejected because the default contributor command must remain the complete selector-regression path.
- Remove subprocess boundary tests: rejected because in-process calls cannot prove CLI parsing, exit codes, wrapper behavior, timeout behavior, output shape, or rerun guidance.

## Scope Control

The change preserves these non-goals:

- No required selector-regression category moved to an optional-only command.
- No broad-smoke parallel execution was enabled.
- No validation-result cache was added.
- No persistent validation worker or broad validator composition was introduced.
- No final verify, branch readiness, PR readiness, or hosted CI success claim was made.
- Broad-smoke classification and cache-boundary metadata remain part of the preservation surface.

The raw branch stack also contains the previous validation-runtime follow-through commits because this branch was created on top of that work. This explanation covers only `2026-06-27-selector-regression-runtime-reduction` and its active plan state.

## Risks And Follow-Ups

- Runtime evidence is local WSL2 evidence. Final verify still needs to run the repository-owned verification scope before PR handoff.
- `scripts/ci.sh` duration reporting uses second-resolution wall-clock time and clamps negative elapsed values. That is adequate for current diagnostics but not a high-resolution monotonic timer.
- Broad-smoke remains slow and sequential by design. A separate approved slice should handle broad-smoke parallelism after consuming child-check classification.
- Validation caching and broad validator composition remain follow-up options only if separately specified and reviewed.

## Readiness Statement

All implementation milestones are closed and code-reviewed with no material findings. The next lifecycle stage is `verify`; this explanation does not run verify and does not claim PR readiness.
