# Selector-Regression Runtime Reduction Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-27-selector-regression-runtime-reduction
- Owner: agent
- Start date: 2026-06-27
- Last updated: 2026-06-27
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan sequences the accepted selector-regression runtime reduction contract into reviewable implementation slices. The goal is to reduce `python scripts/test-select-validation.py` runtime by removing duplicate work while preserving selector behavior, selected-check identity, missing-route blockers, CLI-boundary behavior, diagnostics, and final verification boundaries.

## Source artifacts

- Proposal: [Selector-Regression Runtime Reduction With Coverage-Preservation Proof](../proposals/2026-06-27-selector-regression-runtime-reduction.md)
- Spec: [Selector-Regression Runtime Reduction](../../specs/selector-regression-runtime-reduction.md)
- Parent runtime spec: [Validation Runtime Follow-Through](../../specs/validation-runtime-follow-through.md)
- Architecture: not-required for this slice; revisit only if implementation introduces persistent workers, shared caches, broad validator composition, or new cross-process execution protocols.
- Test spec: [Selector-Regression Runtime Reduction Test Spec](../../specs/selector-regression-runtime-reduction.test.md)
- Change metadata: [change.yaml](../changes/2026-06-27-selector-regression-runtime-reduction/change.yaml)
- Explain change: [explain-change.md](../changes/2026-06-27-selector-regression-runtime-reduction/explain-change.md)
- Verify report: [verify-report.md](../changes/2026-06-27-selector-regression-runtime-reduction/verify-report.md)
- Review log: [review-log.md](../changes/2026-06-27-selector-regression-runtime-reduction/review-log.md)
- Proposal reviews: [proposal-review-r1](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r1.md), [proposal-review-r2](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r2.md)
- Spec review: [spec-review-r1](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/spec-review-r1.md)
- Test-spec review: [test-spec-review-r1](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/test-spec-review-r1.md)
- Code reviews: [code-review-r1](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r1.md), [code-review-r2](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r2.md), [code-review-r3](../changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r3.md)

## Upstream status settlement

- Upstream artifact: `specs/selector-regression-runtime-reduction.md`
- Review evidence: `docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/spec-review-r1.md`; review log has no open findings.
- Previous status: draft
- New status: approved
- Settlement result: updated
- Settlement blocker: none

## Context and orientation

The implementation surface is selector validation and its regression suite:

- `scripts/test-select-validation.py` owns the default selector-regression command, suite output behavior, selector fixtures, CLI/wrapper tests, and the likely fixture restructuring surface.
- `scripts/validation_selection.py` owns selected check IDs, selector route classification, cache-boundary metadata, broad-smoke classification metadata, and route reasons.
- `scripts/ci.sh` owns selected-CI wrapper behavior, timeout handling, and broad-smoke execution boundaries.
- `docs/changes/2026-06-27-selector-regression-runtime-reduction/` owns runtime baseline, runtime result, profile, preservation, review, rationale, and verification evidence.

The broader June 26 validation-runtime follow-through work already added selector-route blocker and broad-smoke classification infrastructure. This plan should not reopen broad-smoke parallelism, caching, broad validator composition, or final verify semantics.

## Non-goals

- Do not reduce runtime by deleting required selector-regression coverage.
- Do not add a first-slice `--fast` or `--quick` command as the primary speed mechanism.
- Do not change selector routing semantics merely to make tests pass faster.
- Do not remove subprocess tests that prove CLI or wrapper behavior.
- Do not enable broad-smoke parallel execution.
- Do not enable validation-result caching, remote/shared caching, persistent workers, or broad validator composition.
- Do not change final verify, branch readiness, PR readiness, or hosted CI semantics.

## Requirements covered

- `R1`-`R3`: M1 coverage inventory and M2 default-command preservation.
- `R4`-`R7`: M1 baseline runtime evidence and M3 revised runtime evidence.
- `R8`-`R11`: M1 identity inventory and M2/M3 preservation proof.
- `R12`-`R14`: M2 in-process conversion boundaries and retained subprocess coverage.
- `R15`-`R18`: M2 missing-route, cache-boundary, and broad-smoke classification fixture preservation.
- `R19`: M2/M3 scope guardrails for cache, workers, and composition.
- `R20`-`R21`: M2/M3 selected-CI wrapper compatibility and timeout evidence.
- `R22`-`R23`: M1 selector-regression profile proof.
- `R24`-`R27`: M3 success target or no-safe-reduction closeout.
- `R28`-`R30`: M2/M3 final verify boundary, diagnostics, and fixture state-leakage guardrails.
- `AC1`-`AC18`: covered across M1 through M3 and final lifecycle closeout.

## Current Handoff Summary

- Current milestone: M3. Runtime Result and Closeout Evidence
- Current milestone state: closed
- Latest review evidence: docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/code-review-r3.md
- Last reviewed milestone: M3. Runtime Result and Closeout Evidence
- Review status: approved; stage=code-review; round=r3
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, pr-handoff-pending — implementation milestones, code-review, explain-change, and verify are closed, but PR handoff remains.

## Milestones

### M1. Baseline, Profile, and Identity Inventory

- Milestone state: closed
- Goal: Record selector-regression baseline runtime, profile evidence, and identity/failure-sensitivity inventory before restructuring tests.
- Requirements: `R1`-`R11`, `R22`-`R23`, `AC1`, `AC3`-`AC6`
- Files/components likely touched:
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
  - `scripts/test-select-validation.py`
  - `scripts/validation_selection.py`
- Dependencies:
  - Plan-review approves this plan.
  - Test spec maps M1 proof obligations before implementation.
- Tests to add/update:
  - Baseline selected-check identity extraction or fixture evidence.
  - Missing-route negative fixture inventory.
  - Profile proof procedure for `python scripts/test-select-validation.py`.
- Implementation steps:
  - Record same-environment selector-regression baseline timing, using three paired runs when practical.
  - Record profile evidence with environment, worktree state, commands, timeout behavior, selected checks observed, dominant contributors or instrumentation limits, and safe-reduction decision.
  - Record baseline behavioral selector identity, selected-check identity, unittest identifier identity, missing-route failures, registered-route passes, CLI-boundary coverage, cache-boundary behavior, and broad-smoke classification behavior.
- Validation commands:
  - `/usr/bin/time -p python scripts/test-select-validation.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/selector-regression-runtime-reduction.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
  - `git diff --check -- docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`
- Expected observable result: Baseline and profile evidence exists before runtime-reducing changes; identity and failure-sensitivity surfaces are named for comparison.
- Commit message: `M1: record selector regression baseline and profile`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Runtime measurements may vary by machine.
  - Profile evidence may identify no safe reducer.
- Rollback/recovery:
  - Keep valid baseline/profile evidence; remove or revise only misleading measurements.
  - If no safe reducer is found, stop M2/M3 runtime-reduction work and prepare no-safe-reduction closeout evidence.

### M2. Fixture Reuse and In-Process Selector Conversion

- Milestone state: closed
- Goal: Convert pure selector logic coverage to lower-overhead in-process/table-driven execution while retaining subprocess-backed command-boundary coverage.
- Requirements: `R1`-`R3`, `R8`-`R21`, `R28`-`R30`, `AC4`-`AC17`
- Files/components likely touched:
  - `scripts/test-select-validation.py`
  - `scripts/validation_selection.py`
  - `scripts/ci.sh`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
- Dependencies:
  - M1 profile and baseline evidence complete.
  - Test spec identifies required in-process and subprocess proof boundaries.
- Tests to add/update:
  - Table-driven pure selector fixtures for source, spec, test-spec, lifecycle, review, evidence, broad-smoke classification, and selector implementation paths.
  - Subprocess tests for CLI parsing, exit codes, stdout/stderr diagnostics, timeout override behavior, wrapper integration, and rerun guidance.
  - Negative fixtures proving missing selector routes still fail.
  - Cache-boundary and broad-smoke classification fixture checks.
- Implementation steps:
  - Introduce shared immutable fixture builders or resettable fixture groups for pure selector cases.
  - Convert only pure selector logic cases to in-process calls.
  - Preserve or add subprocess tests for command-boundary behavior.
  - Update preservation evidence to distinguish behavioral selector identity, selected-check identity, and unittest identifier identity.
  - Verify shared fixtures do not leak mutable state between cases.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-select-validation.py -k selector`
  - `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
- Expected observable result: The default command still runs complete coverage; pure selector cases avoid unnecessary subprocess overhead; CLI-boundary proof remains subprocess-backed.
- Commit message: `M2: reduce selector regression duplicate work`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - In-process conversion could accidentally stop proving CLI behavior.
  - Shared fixtures could hide state leakage.
  - Test ID changes could be mistaken for behavior changes or vice versa.
- Rollback/recovery:
  - Revert in-process conversion while keeping preservation tests and evidence.
  - Split leaky shared fixtures back into isolated fixtures.
  - Record approved test-structure delta when unittest identifiers change without behavior change.

### M3. Runtime Result and Closeout Evidence

- Milestone state: closed
- Goal: Record revised runtime, compare preservation evidence, decide timeout status, and close with either measured runtime reduction or no-safe-reduction evidence.
- Requirements: `R4`-`R7`, `R21`, `R24`-`R30`, `AC1`-`AC18`
- Files/components likely touched:
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md`
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
  - `docs/plans/2026-06-27-selector-regression-runtime-reduction.md`
- Dependencies:
  - M2 implementation complete and reviewed.
  - Baseline and revised evidence are comparable or limitations are recorded.
- Tests to add/update:
  - Runtime result evidence validation where feasible.
  - Preservation proof covering required identity and failure-sensitivity surfaces.
  - Selected-CI timeout status evidence.
- Implementation steps:
  - Record revised selector-regression runtime under comparable conditions, using three paired runs when practical.
  - Compare baseline and revised behavioral selector identity, selected-check identity, unittest identifier identity or approved delta, missing-route blockers, registered routes, CLI-boundary behavior, diagnostics, broad-smoke classification behavior, and cache-boundary metadata.
  - Record whether selected CI still needs the 180-second timeout override.
  - If runtime target is not met, record no-safe-reduction rationale and next measured bottleneck.
  - Update plan progress, validation notes, change metadata, and follow-on decision.
- Validation commands:
  - `/usr/bin/time -p python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/selector-regression-runtime-reduction.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`
  - `git diff --check -- scripts docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`
- Expected observable result: Revised runtime and preservation proof either demonstrate safe runtime reduction or document no safe reduction and the next measured bottleneck.
- Commit message: `M3: record selector regression runtime result`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Runtime target may not be met even after safe duplicate-work reduction.
  - Machine variance may obscure true improvement.
  - Timeout override may remain required.
- Rollback/recovery:
  - Keep preservation proof and no-safe-reduction evidence.
  - Revert runtime-reducing test restructuring if preservation or diagnostics regress.
  - Route next speed work to broad-smoke parallelism, validation context composition, or safe inner-loop cache adoption through separate approved artifacts.

## Validation plan

- `python scripts/test-select-validation.py`: default complete selector-regression coverage.
- `/usr/bin/time -p python scripts/test-select-validation.py`: runtime baseline and revised timing evidence.
- `python scripts/test-select-validation.py -k selector`: focused selector slice during implementation when useful; not a substitute for the default command.
- `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: selected-CI wrapper compatibility and timeout-aware selected validation, with additional touched paths added by the implementing milestone.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`: review evidence structure.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: compact change metadata validity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/selector-regression-runtime-reduction.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: lifecycle state and artifact consistency, with additional touched lifecycle artifacts added by the implementing milestone.
- `git diff --check -- scripts docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`: whitespace and patch hygiene.
- State-sync check before downstream handoff: validate that plan body, `docs/plan.md`, and change metadata agree on current stage, lifecycle state, and touched artifacts.

## Risks and recovery

- Risk: Runtime improves by dropping proof.
  - Recovery: Block milestone closeout unless behavioral selector identity, selected-check identity, failure sensitivity, and CLI-boundary coverage are preserved.
- Risk: In-process tests miss command-boundary defects.
  - Recovery: Keep subprocess coverage for CLI parsing, exit codes, output diagnostics, timeout behavior, wrapper integration, and rerun guidance.
- Risk: Fixture reuse hides mutable state leakage.
  - Recovery: Use immutable fixtures or reset per group; revert to isolated fixtures if leakage appears.
- Risk: Runtime measurements are noisy.
  - Recovery: Use paired same-environment medians where practical and record limitations.
- Risk: The selected-CI timeout override remains needed.
  - Recovery: Record timeout status and no-safe-reduction rationale or next bottleneck instead of weakening coverage.

## Dependencies

- Accepted proposal and approved spec.
- Clean recorded proposal-review and spec-review evidence.
- Plan-review before test-spec.
- Test spec before implementation.
- No architecture artifact required unless scope expands into persistent workers, shared caches, broad validator composition, or cross-process execution protocols.
- Existing selector regression suite and selected-CI wrapper remain compatibility surfaces.

## Progress

- 2026-06-27: Proposal accepted and proposal-review R1/R2 recorded with no material findings.
- 2026-06-27: Focused selector-regression runtime reduction spec authored.
- 2026-06-27: Spec-review R1 approved the spec with no material findings.
- 2026-06-27: Upstream status settlement normalized spec status to `approved`.
- 2026-06-27: Plan created and ready for plan-review.
- 2026-06-27: Plan-review R1 approved the plan with no material findings.
- 2026-06-27: Test spec authored and ready for test-spec-review.
- 2026-06-27: Test-spec-review R1 approved the active test spec with no material findings; implementation handoff allowed for M1.
- 2026-06-27: M1 implementation started; baseline/profile/preservation evidence collection in progress.
- 2026-06-27: M1 discovered `selector-regression-runtime-baseline.yaml` was unregistered change evidence; added a selector regression test and registered selector-runtime YAML evidence routing before recording baseline evidence.
- 2026-06-27: M1 recorded selector-regression profile, runtime baseline, and preservation baseline evidence. Baseline median real runtime is 164.73s for 109 tests.
- 2026-06-27: M1 targeted validation passed and M1 moved to review-requested for code-review.
- 2026-06-27: Code-review R1 closed M1 with no material findings; next stage is implement M2.
- 2026-06-27: M2 implementation added reusable repository preflight context for pure selector calls, preserved subprocess CLI/wrapper tests, and moved M2 to review-requested after targeted validation passed.
- 2026-06-27: Code-review R2 closed M2 with no material findings; next stage is implement M3.
- 2026-06-27: M3 recorded revised runtime result evidence, selected-CI timeout status, preservation closeout, and a broad-smoke duration-output regression fix; M3 moved to review-requested after targeted validation passed.
- 2026-06-27: Code-review R3 closed M3 with no material findings; all in-scope implementation milestones are closed and the next stage is explain-change.
- 2026-06-27: Explain-change recorded durable rationale for the selector-regression runtime reduction and moved the next stage to verify.
- 2026-06-27: Verify passed fresh selector-regression, selected-CI, review-artifact, and broad-smoke checks; branch-ready evidence recorded and the next stage is PR handoff.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-27 | Create a focused plan for selector-regression runtime reduction. | The accepted proposal and spec define a narrower runtime-reducing slice than the June 26 follow-through plan. | Reopen the completed June 26 plan or fold this work into broad-smoke optimization. |
| 2026-06-27 | Sequence baseline/profile before in-process conversion. | The spec requires profile and baseline evidence before accepting runtime-reducing implementation. | Convert selector tests first and measure afterward. |
| 2026-06-27 | Keep architecture not required for this plan. | The spec excludes workers, caches, broad composition, and cross-process protocols. | Create an architecture artifact for a test-suite restructuring slice. |
| 2026-06-27 | Use three implementation milestones. | Baseline/profile, restructuring, and runtime-result proof have distinct evidence and review boundaries. | One large implementation milestone or per-test micro-milestones. |
| 2026-06-27 | Register selector runtime YAML evidence during M1. | The approved M1/M3 evidence filenames must not create manual-routing debt before selected validation can run. | Leave the evidence file as unregistered debt or hide it from selected validation. |
| 2026-06-27 | Reuse immutable repository preflight context for pure selector tests. | Per-test timing showed `test_first_slice_representative_categories_route_or_block_safely` spent about 105.804s repeating repository-state discovery; reusable preflight context preserves selector behavior while avoiding repeated `git` discovery. | Remove table rows, convert CLI-boundary tests in process, or cache without repository identity. |
| 2026-06-27 | Fix broad-smoke duration reporting during M3. | Revised timing exposed a negative elapsed value in broad-smoke output; selector-regression cannot close with a known default-command failure. | Ignore the failed timing run or weaken the output regex. |

## Surprises and discoveries

- M1 selector probing found `selector-regression-runtime-baseline.yaml` was initially classified as unregistered change evidence. The fix adds a deterministic `selector-regression-runtime` evidence class for baseline and result YAML files.
- Grouped timing showed the broad `ValidationSelectionTests` bucket accounts for nearly all selector-regression wall time, while smaller `ci_wrapper`, script-output, and broad-smoke classification focused groups are much shorter.
- M2 per-test timing identified one dominant duplicate-work case: `ValidationSelectionTests.test_first_slice_representative_categories_route_or_block_safely` took about 105.804s because the table re-ran repository preflight discovery for each pure selector row.
- Reusing a frozen `RepositoryPreflightContext` for `ROOT` reduced the representative table to `real 1.05s` while adding an identity guard that raises if the context is used with a different repository root.
- M3 revised timing initially exposed `test_broad_smoke_verbose_prints_successful_child_output_in_order` failing on a negative broad-smoke elapsed value (`-2s`). M3 fixed duration reporting to avoid Bash `$SECONDS`, added a regression guard, and restarted the three-run timing evidence after the fix.

## Validation notes

- M1 in progress:
  - `python scripts/test-select-validation.py -k selector_runtime_evidence_files_route_without_manual_debt`: failed before registering `selector-regression-runtime` evidence, then passed after the route was added.
  - `/usr/bin/time -p python scripts/test-select-validation.py`: three baseline runs passed with 109 tests; real durations 165.71s, 164.73s, and 161.13s; median real duration 164.73s.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k ci_wrapper`: passed, 21 tests, real 7.61s.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k ScriptOutputContractTests`: passed, 10 tests, real 1.96s.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k broad_smoke`: passed, 13 tests, real 4.13s.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k ValidationSelectionTests`: passed, 99 tests, real 164.20s.
  - `python scripts/test-select-validation.py`: passed, 109 tests in 179.92s after the selector-runtime evidence route was added.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/selector-regression-runtime-reduction.md --path specs/selector-regression-runtime-reduction.test.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/proposals/2026-06-27-selector-regression-runtime-reduction.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/review-log.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/review-resolution.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r1.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/proposal-review-r2.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/spec-review-r1.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/plan-review-r1.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/reviews/test-spec-review-r1.md`: passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: passed.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`: passed.
  - `git diff --check -- scripts docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md specs/selector-regression-runtime-reduction.test.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`: passed.
- Code-review R1 direct proof:
  - `python scripts/test-select-validation.py -k selector_runtime_evidence_files_route_without_manual_debt`: passed.
  - `python scripts/select-validation.py --mode explicit --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md --path specs/selector-regression-runtime-reduction.md --path specs/selector-regression-runtime-reduction.test.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md`: selector status `ok`, selected checks `artifact_lifecycle.validate` and `selector.regression`, no blockers, no registration debt.
- M2 validation:
  - `python scripts/test-select-validation.py -k shared_preflight_context_requires_matching_repository_identity`: failed before production support with missing import, then passed after adding `build_repository_preflight_context` and root identity validation.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k first_slice_representative_categories_route_or_block_safely`: passed, 1 test in 0.57s, real 1.05s.
  - `python scripts/test-select-validation.py -k selector`: passed, 12 tests in 3.34s.
  - `/usr/bin/time -p python scripts/test-select-validation.py`: passed, 110 tests in 38.45s, real 35.09s.
  - `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`: passed; selected checks `artifact_lifecycle.validate` and `selector.regression`; `selector.regression` elapsed 39.39s.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/test-select-validation.py --path scripts/validation_selection.py --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: passed.
  - `git diff --check -- scripts docs/changes/2026-06-27-selector-regression-runtime-reduction docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`: passed.
- Code-review R2 result:
  - `code-review-r2`: clean-with-notes; no material findings; M2 closed.
- M3 validation:
  - First attempted revised timing loop found one failure before final runtime evidence: `test_broad_smoke_verbose_prints_successful_child_output_in_order` failed because broad-smoke printed `-2s` elapsed. This was fixed before recording the final three-run revised runtime evidence.
  - `python scripts/test-select-validation.py -k duration_reporting_does_not_use_bash_seconds`: failed before replacing Bash `$SECONDS` duration reporting, then passed after the fix.
  - `python scripts/test-select-validation.py -k broad_smoke_default_success_captures_child_output_and_prints_aggregate`: passed.
  - `python scripts/test-select-validation.py -k broad_smoke_verbose_prints_successful_child_output_in_order`: passed.
  - `python scripts/test-select-validation.py -k broad_smoke_failure_prints_command_exit_duration_and_captured_output`: passed.
  - `/usr/bin/time -p python scripts/test-select-validation.py`: three final revised runs passed with 111 tests; real durations 36.23s, 36.19s, and 36.46s; median real duration 36.23s.
  - `bash scripts/ci.sh --mode explicit --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`: passed without timeout override; selected checks `artifact_lifecycle.validate` and `selector.regression`; `selector.regression` elapsed 36.47s.
  - `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/test-select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`: passed; selected checks `artifact_lifecycle.validate` and `selector.regression`; `selector.regression` elapsed 36.92s.
  - `python scripts/test-select-validation.py -k selector`: passed, 12 tests in 3.20s.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`: passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml`: passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/selector-regression-runtime-reduction.md --path docs/plans/2026-06-27-selector-regression-runtime-reduction.md --path docs/plan.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/change.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-profile.md --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-baseline.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-runtime-result.yaml --path docs/changes/2026-06-27-selector-regression-runtime-reduction/selector-regression-preservation.md`: passed.
  - `git diff --check -- scripts docs/changes/2026-06-27-selector-regression-runtime-reduction specs/selector-regression-runtime-reduction.md docs/plans/2026-06-27-selector-regression-runtime-reduction.md docs/plan.md`: passed.
- Code-review R3 result:
  - `code-review-r3`: clean-with-notes; no material findings; M3 closed; all in-scope implementation milestones closed.
- Explain-change result:
  - `docs/changes/2026-06-27-selector-regression-runtime-reduction/explain-change.md`: recorded the problem-to-diff rationale, tests, validation evidence, alternatives rejected, scope control, risks, and verify handoff.
- Verify result:
  - `python scripts/test-select-validation.py`: passed, 111 tests in 36.99s.
  - `python scripts/select-validation.py --mode explicit --path ...`: passed with selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`; no blockers or registration debt.
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-27-selector-regression-runtime-reduction`: passed.
  - `bash scripts/ci.sh --mode explicit --path ...`: passed; selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `guide_system.validate`, and `selector.regression`; focused phase total 50.37s.
  - `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped`: passed, 11 checks in 354s.
  - Post-report selected validation for verify-stage bookkeeping passed with selected checks `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `guide_system.validate`.

## Outcome and retrospective

- Pending; fill after implementation, review, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done.
