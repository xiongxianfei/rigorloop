# Preflight-First Validation Runtime Optimization Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-06-26-preflight-first-validation-runtime-optimization
- Start date: 2026-06-26
- Last updated: 2026-06-26
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan sequences the accepted validation-runtime follow-through work into reviewable implementation slices. The goal is to use the June 24 validation timing surfaces to identify and safely reduce the selected-validation bottleneck, make missing selector routes block deterministically, and prepare broad-smoke optimization through read-only child classification without enabling broad-smoke parallelism in this slice.

## Source artifacts

- Proposal: `docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md`
- Spec: `specs/validation-runtime-follow-through.md`
- Prior spec: `specs/validation-execution-performance-and-preflight.md`
- Prior timing evidence: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/script-performance-baseline.yaml`
- Architecture: not-required for this slice; revisit only if scope introduces a persistent worker, shared/remote cache, cross-process protocol, or broad validator composition framework.
- Test spec: `specs/validation-runtime-follow-through.test.md`

## Context and orientation

The June 24 validation work already added selected-check phase metadata, timing, preflight diagnostics, boundary phase metadata, `cache_status: not-applicable`, and immutable preflight context. The current follow-through work starts from those surfaces rather than re-implementing the phase model.

Likely implementation surfaces:

- `scripts/validation_selection.py` for selector route classification, missing-route blocker behavior, and selected-check explanation.
- `scripts/test-select-validation.py` for selector regression profiling, preservation fixtures, and selected-check identity proof.
- `scripts/ci.sh` for any wrapper-visible selected-CI behavior or broad-smoke child command inventory.
- `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/` for baseline, selector profile, preservation, and broad-smoke classification evidence.
- `specs/validation-runtime-follow-through.test.md` after plan-review for the traceable proof map.

## Non-goals

- Do not enable broad-smoke parallel execution in this initiative.
- Do not enable local, remote, or shared validation result caching.
- Do not compose multiple validators into one in-process runner.
- Do not remove selector regression coverage to improve runtime.
- Do not claim branch readiness, PR readiness, hosted CI success, or final closeout from inner-loop speedups.
- Do not supersede the June 24 proposal or `specs/validation-execution-performance-and-preflight.md`.

## Requirements covered

- R1-R5: M1 baseline and upstream-foundation evidence.
- R6-R11: M1 profile evidence and M2 selector-regression optimization/preservation.
- R12-R15: M2 missing selector-route blocker behavior.
- R16-R19: M3 broad-smoke child classification and parallelism boundary.
- R20: M1-M3 cache boundary evidence.
- R21-R23: M1-M3 composition deferral and optional readiness-only assessment.
- R24-R25: M1-M3 preservation of final verify boundaries, coverage, diagnostics, and rerun guidance.

## Current Handoff Summary

- Current milestone: M3. Broad-Smoke Child Classification
- Current milestone state: review-requested
- Latest review evidence: docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r2.md
- Last reviewed milestone: M2. Selector Preservation and Missing-Route Blockers
- Review status: approved; stage=code-review; round=r2
- Remaining in-scope implementation milestones: M3
- Next stage: code-review
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — M1 and M2 are closed after clean code-review; M3 implementation is ready for code-review; final holistic code-review, explain-change, verify, and PR handoff are not complete.

## Milestones

### M1. Baseline and Selector Regression Profile

- Milestone state: closed
- Goal: Record durable post-June-24 baseline evidence and profile `selector.regression` before any optimization.
- Requirements: R1, R2, R3, R4, R5, R6, R20, R21, R22, R24, R25
- Files/components likely touched:
  - `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml`
  - `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
  - `scripts/test-select-validation.py`
  - `scripts/validation_selection.py`
- Dependencies:
  - Spec-review R1 recorded with no material findings.
  - Test spec maps M1 proof obligations before implementation.
- Tests to add/update:
  - Selector-regression profiling proof in `scripts/test-select-validation.py` or change-local evidence, depending on what is feasible without changing runtime behavior.
  - Static or fixture proof that baseline evidence cites durable June 24 artifacts instead of PR-number shorthand.
- Implementation steps:
  - Record baseline scenarios for selected validation, broad-smoke, and final verify using existing timing output where available.
  - Profile `selector.regression` enough to identify dominant contributors or explain profiling limitations.
  - Record whether repeated startup, import, Git inspection, or parsing is material enough to justify only a future readiness assessment.
  - Preserve cache and composition as deferred boundaries unless the plan is revised after review.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --timeout 180 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`
  - If the 180-second wrapper proof times out, record that timeout behavior and rerun the same selected-wrapper path with `--timeout 300`.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
- Expected observable result: Baseline evidence distinguishes selected validation, broad-smoke, and final verify; `selector.regression` has profile evidence before optimization.
- Commit message: `M1: record validation runtime baseline and selector profile`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Profiling may vary by machine and produce noisy timings.
  - Broad-smoke baseline may be expensive.
- Rollback/recovery:
  - Keep baseline/profile evidence if useful; remove only misleading or invalid measurements.
  - If broad-smoke is too costly for local profiling, record the limitation and use existing June 24 evidence until plan-review/test-spec authorizes another proof path.

### M2. Selector Preservation and Missing-Route Blockers

- Milestone state: closed
- Goal: Preserve selector proof while improving or explaining `selector.regression`, and make missing selector routes deterministic blockers.
- Requirements: R7, R8, R9, R10, R11, R12, R13, R14, R15, R20, R24, R25
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md`
- Dependencies:
  - M1 profile evidence complete.
  - Test spec identifies selected-check identity and failure-sensitivity fixtures.
- Tests to add/update:
  - Selected-check identity parity fixture.
  - Negative routing fixtures proving expected failures still fail.
  - Positive routing fixtures proving expected routes still pass.
  - Missing-route blocker fixture proving diagnostic broad-smoke does not erase the selected-validation blocker.
- Implementation steps:
  - Add or update preservation fixtures before optimizing selector-regression runtime.
  - Optimize only demonstrated bottlenecks that preserve selected-check identity and diagnostics.
  - Add missing-route blocker behavior for known artifact/path classes requiring routing.
  - Record no-safe-reduction rationale if the profile does not expose a safe optimization.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
- Expected observable result: Selector-regression proof is preserved, missing selector routes block deterministically, and any runtime improvement is backed by before/after evidence.
- Commit message: `M2: preserve selector proof and block missing routes`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Runtime optimization could accidentally remove coverage or diagnostics.
  - Missing-route blockers could overmatch legitimate paths.
- Rollback/recovery:
  - Revert optimization while keeping preservation tests.
  - Narrow route-blocker classification if a legitimate path is blocked incorrectly.

### M3. Broad-Smoke Child Classification

- Milestone state: review-requested
- Goal: Produce read-only broad-smoke child classification evidence without changing broad-smoke execution behavior.
- Requirements: R16, R17, R18, R19, R20, R21, R22, R23, R24, R25
- Files/components likely touched:
  - `scripts/ci.sh`
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md`
- Dependencies:
  - M1 baseline evidence identifies broad-smoke as the boundary-cost scenario.
  - Test spec defines expected classification fields and proof that execution remains sequential.
- Tests to add/update:
  - Static or fixture proof that every broad-smoke child has the required classification fields.
  - Proof that this slice does not enable broad-smoke parallel execution.
  - Proof that low-confidence or side-effecting children are not parallel-safe candidates.
- Implementation steps:
  - Inventory broad-smoke child checks and commands.
  - Classify read/write behavior, temporary roots, shared outputs, network use, CPU/I/O expectations, nested parallelism risk, output-order risk, failure-output dependency, candidate status, and confidence.
  - Add tests or static checks that classification is complete and read-only.
  - Record follow-up recommendation for broad-smoke parallelization only if classification supports it.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --timeout 180 --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/validation-runtime-follow-through.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
- Expected observable result: Broad-smoke child classification exists, contains required fields, and does not change broad-smoke ordering or concurrency.
- Commit message: `M3: classify broad-smoke children`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Classification may be incomplete if child commands are implicit or shell-expanded.
  - A classification artifact could be mistaken for permission to parallelize.
- Rollback/recovery:
  - Treat incomplete classification as no-candidate status and keep broad-smoke sequential.
  - Remove candidate claims while preserving inventory evidence.

## Validation plan

- `python scripts/test-select-validation.py`: selector routing, selected-check identity, blocker behavior, CI wrapper behavior, and broad-smoke classification checks.
- `bash scripts/ci.sh --mode explicit --timeout 180 --path <changed paths>`: selected validation for changed implementation and evidence surfaces.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`: review evidence structure.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`: change metadata validity.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <touched lifecycle artifacts>`: lifecycle state and artifact consistency.
- `git diff --check -- <touched paths>`: whitespace and patch hygiene.
- State-sync check before downstream handoff: validate plan body, `docs/plan.md`, and change metadata agree on the current stage and touched artifacts.

## Risks and recovery

- Risk: The plan over-optimizes `selector.regression` without preserving proof.
  - Recovery: Require preservation fixtures before accepting optimization; revert optimization while keeping tests.
- Risk: Broad-smoke classification becomes an accidental concurrency contract.
  - Recovery: Keep M3 explicitly read-only and leave parallel execution to a separate proposal or implementation slice.
- Risk: Baseline timings vary by machine.
  - Recovery: Compare scenario shape and dominant contributor, not a fixed percentage target.
- Risk: Missing-route blockers overmatch unrelated paths.
  - Recovery: Narrow the classifier, add explicit out-of-scope rationale, and preserve the negative fixture.

## Dependencies

- Accepted proposal and approved spec.
- Clean recorded spec-review.
- Plan-review before test-spec.
- Test spec before implementation.
- Existing June 24 timing and phase output.
- No architecture artifact required unless scope expands into persistent worker, shared/remote cache, cross-process protocol, or broad validator composition framework.

## Progress

- 2026-06-26: Proposal accepted and two clean proposal-review receipts recorded.
- 2026-06-26: Focused follow-through spec authored.
- 2026-06-26: Spec-review R1 approved the spec with no material findings.
- 2026-06-26: Plan created and ready for plan-review.
- 2026-06-26: Plan-review R1 approved the plan with no material findings.
- 2026-06-26: Test spec authored at `specs/validation-runtime-follow-through.test.md`; ready for test-spec-review.
- 2026-06-26: Test-spec-review R1 requested changes for `TSR1-F1`; next stage is review-resolution and test-spec revision.
- 2026-06-26: Test spec revised with `MP-SEL-001`, and test-spec-review R2 approved the proof map for implementation handoff.
- 2026-06-26: Test-spec-review R3 reconfirmed the active proof map with no material findings.
- 2026-06-26: M1 implementation started. Recorded `script-performance-baseline.yaml` and `selector-regression-profile.md` before any selector optimization.
- 2026-06-26: M1 added selector-profile evidence routing for `selector-regression-profile.md` after selected CI reported deterministic evidence-registration debt for that required M1 evidence artifact.
- 2026-06-26: M1 implementation is ready for code-review. Current milestone state moved to `review-requested`; next stage is `code-review`.
- 2026-06-26: Code-review R1 passed with no material findings. M1 is closed; next stage is M2 implementation.
- 2026-06-26: M2 implementation started. Added selector preservation, missing-route diagnostic, and diagnostic broad-smoke regression tests before changing selector diagnostics.
- 2026-06-26: M2 implementation is ready for code-review. Current milestone state moved to `review-requested`; next stage is `code-review`.
- 2026-06-26: Code-review R2 passed with no material findings. M2 is closed; next stage is M3 implementation.
- 2026-06-26: M3 implementation started. Scope is limited to read-only broad-smoke child classification evidence and static checks; broad-smoke execution order and concurrency remain unchanged.
- 2026-06-26: M3 implementation added read-only broad-smoke child classification evidence, selector evidence routing for `broad-smoke-child-classification.md`, and static checks for required classification fields, actual broad-smoke child coverage, unsafe candidate guardrails, and unchanged sequential broad-smoke execution.
- 2026-06-26: M3 implementation is ready for code-review. Current milestone state moved to `review-requested`; next stage is `code-review`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-26 | Use a new focused plan for validation runtime follow-through. | The June 24 plan owns the general preflight-first implementation and this work is a follow-on slice. | Reopen or supersede the June 24 plan. |
| 2026-06-26 | Sequence selector baseline/profile before optimization. | The spec requires proof before accepting runtime changes. | Optimize selector tests immediately. |
| 2026-06-26 | Keep broad-smoke parallelism out of this plan. | The spec allows only read-only child classification in this slice. | Enable bounded broad-smoke concurrency in M3. |
| 2026-06-26 | Record 180-second selected-wrapper timeout and use a 300-second override for M1 wrapper proof. | The required M1 evidence path timed out `selector.regression` at 180.12s but passed with a 300-second repository-supported timeout. | Hide the timeout, lower selector coverage, or treat the failed 180-second run as sufficient proof. |
| 2026-06-26 | Use `--timeout 300` for M2 selected-wrapper proof. | M1 established that the same selector-regression wrapper path can exceed 180 seconds locally, and M2 does not claim a runtime optimization. | Repeat a known 180-second timeout before running the passing wrapper proof. |
| 2026-06-26 | Treat broad-smoke classification as inventory, not execution permission. | R18-R19 keep broad-smoke sequential until a later approved artifact consumes the classification and authorizes bounded parallelism. | Mark child checks parallel-safe in M3 or change broad-smoke execution behavior. |

## Surprises and discoveries

- 2026-06-26: `selector-regression-profile.md` initially triggered `manual-routing-required` evidence-registration debt. M1 fixed this with a narrow evidence-class registration and targeted selector test because the profile artifact is required by the active test spec.
- 2026-06-26: Selected CI with `--timeout 180` timed out `selector.regression`; `--timeout 300` passed. M2 should preserve this timeout behavior in any optimization or no-safe-reduction decision.
- 2026-06-26: M2 did not identify a safe selector-regression runtime reduction. The milestone records a no-safe-reduction rationale and preserves the timeout behavior for follow-up optimization work.
- 2026-06-26: M3 direct selector regression passed but took longer than prior M2 evidence: 108 tests, suite `260.64s`, `/usr/bin/time` real `248.35s`. Selected-wrapper explicit validation still passed within the 180-second per-check timeout with `selector.regression` at `174.54s`.

## Validation notes

- 2026-06-26: Plan-review R1 recording validated with review-artifact, change-metadata, artifact-lifecycle, and whitespace checks.
- 2026-06-26: Test-spec authoring checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/validation-runtime-follow-through.md --path specs/validation-runtime-follow-through.test.md --path docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/plan.md --path docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md`
  - `git diff --check -- specs/validation-runtime-follow-through.md specs/validation-runtime-follow-through.test.md docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md docs/plan.md docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
- 2026-06-26: Selected CI command `bash scripts/ci.sh --mode explicit --timeout 180 --path ...` blocked before running checks because new authoritative artifacts are untracked; rerun after staging/tracking the new spec, plan, proposal, and change-pack files.
- 2026-06-26: M1 profiling commands passed:
  - `/usr/bin/time -p python scripts/test-select-validation.py` passed 103 tests; suite reported 142.65s; time reported real 135.04s, user 5.39s, sys 22.61s.
  - `/usr/bin/time -p python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --json` passed in real 1.18s and selected `selector.regression`.
  - `/usr/bin/time -p python scripts/test-select-validation.py -k preflight` passed 2 tests; suite reported 0.04s; time reported real 0.16s.
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 180 --path ...` timed out `selector.regression` after 180.12s, after `artifact_lifecycle.validate` passed.
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 300 --path ...` passed; `artifact_lifecycle.validate` took 0.47s and `selector.regression` took 273.28s.
- 2026-06-26: M1 validation passed:
  - `python scripts/test-select-validation.py -k registered_change_evidence`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md docs/plan.md specs/validation-runtime-follow-through.md specs/validation-runtime-follow-through.test.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path specs/validation-runtime-follow-through.test.md --path docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/plan.md --path docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r3.md`
- 2026-06-26: M2 focused selector checks passed:
  - `python scripts/test-select-validation.py -k selector_preservation_surface`
  - `python scripts/test-select-validation.py -k unregistered_change_evidence`
  - `python scripts/test-select-validation.py -k diagnostic_broad_smoke`
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md --json`
- 2026-06-26: M2 selector regression and selected-wrapper validation passed:
  - `/usr/bin/time -p python scripts/test-select-validation.py` passed 105 tests; suite reported 153.67s; time reported real 146.03s, user 5.44s, sys 24.35s.
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md` passed; `artifact_lifecycle.validate` took 0.18s and `selector.regression` took 142.54s.
- 2026-06-26: M2 lifecycle and metadata checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `git diff --check --cached -- scripts/validation_selection.py scripts/test-select-validation.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md docs/plan.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path specs/validation-runtime-follow-through.test.md --path docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/plan.md --path docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r3.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r1.md`
- 2026-06-26: M3 red test confirmed missing classification evidence before implementation:
  - `python scripts/test-select-validation.py -k broad_smoke_child_classification` failed because `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` did not exist.
- 2026-06-26: M3 targeted selector checks passed:
  - `python scripts/test-select-validation.py -k broad_smoke_classification` passed 2 tests.
  - `python scripts/test-select-validation.py -k broad_smoke_child_classification` passed 1 test.
  - `python scripts/test-select-validation.py -k registered_change_evidence` passed 5 tests.
  - `python scripts/select-validation.py --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md --json` selected `artifact_lifecycle.validate` and `selector.regression` with no broad-smoke requirement.
- 2026-06-26: M3 selector regression and selected-wrapper validation passed:
  - `/usr/bin/time -p python scripts/test-select-validation.py` passed 108 tests; suite reported `260.64s`; time reported real `248.35s`, user `5.51s`, sys `26.29s`.
  - `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 180 --path scripts/ci.sh --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md` passed; `artifact_lifecycle.validate` took `0.28s`, `selector.regression` took `174.54s`, and focused phase timing was `174.81s`.
- 2026-06-26: M3 lifecycle and metadata checks passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-26-preflight-first-validation-runtime-optimization`
  - `git diff --check -- scripts/validation_selection.py scripts/test-select-validation.py docs/changes/2026-06-26-preflight-first-validation-runtime-optimization docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md docs/plan.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path scripts/validation_selection.py --path scripts/test-select-validation.py --path specs/validation-runtime-follow-through.md --path specs/validation-runtime-follow-through.test.md --path docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/plan.md --path docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/change.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-log.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/review-resolution.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/script-performance-baseline.yaml --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/broad-smoke-child-classification.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/plan-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r2.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/test-spec-review-r3.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r1.md --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/code-review-r2.md`

## Outcome and retrospective

- Filled after completion.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not Done; downstream gates remain open.
