# Preflight-First and Measured Script Execution Optimization Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-24-preflight-first-measured-script-execution-optimization
- Owner: agent
- Start date: 2026-06-24
- Last updated: 2026-06-24
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved preflight-first validation execution contract so routine validation avoids known cheap blockers, records timing and selection evidence, preserves required proof, and stops repeated final-verify churn from stale or self-invalidating evidence.

## Source artifacts

- Proposal: [Preflight-First and Measured Script Execution Optimization](../proposals/2026-06-24-preflight-first-measured-script-execution-optimization.md)
- Spec: [Validation Execution Performance and Preflight](../../specs/validation-execution-performance-and-preflight.md)
- Architecture: not-required; architecture assessment recorded in [change.yaml](../changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml)
- Test spec: [Validation Execution Performance and Preflight test spec](../../specs/validation-execution-performance-and-preflight.test.md)
- Change metadata: [change.yaml](../changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml)
- Review log: [review-log.md](../changes/2026-06-24-preflight-first-measured-script-execution-optimization/review-log.md)
- Proposal review: [proposal-review-r1](../changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/proposal-review-r1.md)
- Spec review: [spec-review-r1](../changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/spec-review-r1.md)

## Upstream status settlement

- Settlement result: not-needed
- New status: not-applicable
- Settlement blocker: none
- Evidence: proposal status is `accepted`; spec status is `approved`; proposal-review R1 and spec-review R1 are approved with no material findings; review log has no open findings.

## Context and orientation

The implementation surface is repository validation and workflow tooling: validation selectors, artifact-lifecycle validation, change metadata validation, review-artifact validation, verify guidance, timing evidence, and workflow-facing diagnostics. The first slice should not introduce a persistent worker, remote cache, shared service, cross-process protocol, or first-slice concurrency.

Existing standalone CLIs remain compatibility surfaces. The implementation should prefer shared immutable context and in-process composition where practical, but each validator's standalone behavior remains testable.

## Non-goals

- Do not reduce selected-check coverage.
- Do not skip final boundary validation when authoritative triggers apply.
- Do not add first-slice caching or parallel execution.
- Do not redesign hosted CI.
- Do not create a persistent daemon, remote cache, shared service, or cross-process protocol.
- Do not hand-edit generated public adapter output.

## Requirements covered

- `R1`-`R6`: M2 preflight and phase gating.
- `R7`-`R8`: M3 boundary trigger and selected-check preservation.
- `R9`-`R12`: M1 timing and selection explanation.
- `R13`-`R14`: M4 shared context and CLI compatibility.
- `R15`-`R16`, `R19`-`R20`: M5 follow-up boundaries for cache, concurrency, and budgets.
- `R17`-`R18`: M5 final verify sequencing and stable evidence wording.
- `R21`-`R22`: M1 and M5 timing retention and output/runtime distinction.
- `AC1`-`AC14`: covered across M1 through M5.

## Current Handoff Summary

- Current milestone: M5. Final Verify Sequencing and Follow-Up Boundaries
- Current milestone state: closed
- Latest review evidence: code-review-m5-r1
- Last reviewed milestone: M5. Final Verify Sequencing and Follow-Up Boundaries
- Review status: approved; stage=code-review; round=r1
- Remaining in-scope implementation milestones: none
- Next stage: pr
- Final closeout readiness: ready
- Reason final closeout is or is not ready: ready — local verify complete; PR handoff remains.

## Milestones

### M1. Baseline, Timing, and Selection Explanation

- Milestone state: closed
- Goal: Add non-semantic timing instrumentation and reviewable selection explanation.
- Requirements: `R9`-`R12`, `R21`-`R22`, `AC5`, `AC6`, `AC14`
- Files/components likely touched:
  - `scripts/select-validation.py`
  - `scripts/validation_selection.py`
  - validation orchestration scripts
  - `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/`
- Dependencies:
  - Approved test spec.
- Tests to add/update:
  - Selection explanation includes changed paths, selected checks, omitted checks, reasons, and boundary triggers.
  - Timing summary records check ID, phase, result, and duration without changing exit semantics.
  - Detailed timing sidecar retention policy is represented before sidecars are generated.
- Implementation steps:
  - Add lightweight timing wrapper around selected checks.
  - Add normal and verbose selection explanation output.
  - Record baseline cold/warm timing expectations for representative final verify.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml`
  - `git diff --check -- scripts docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization`
- Expected observable result: selected validation can explain why checks ran and how long each phase took without changing selected-check semantics.
- Commit message: `M1: record validation timing and selection reasons`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
- Risks:
  - Timing overhead could distort small checks.
  - Explanation output could become too noisy.
- Rollback/recovery:
  - Disable timing/explanation flags while preserving baseline evidence.

### M2. Cheap Preflight Gate

- Milestone state: closed
- Goal: Add deterministic preflight blockers before focused or boundary validation.
- Requirements: `R1`-`R6`, `R8`, `AC1`, `AC2`, `AC9`, `AC13`
- Files/components likely touched:
  - validation orchestration scripts
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
- Dependencies:
  - M1 measurement output.
- Tests to add/update:
  - Untracked authoritative artifact blocks boundary validation.
  - Unmerged paths block boundary validation.
  - Focused validation failure prevents boundary validation.
  - Preflight diagnostics name blocker, paths, and corrective action.
- Implementation steps:
  - Collect cheap Git and artifact state before selected validation.
  - Gate focused and boundary phases on preflight result.
  - Add explicit diagnostic override path that cannot claim final readiness.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md`
  - `git diff --check -- scripts`
- Expected observable result: known cheap blockers stop broad validation and give actionable diagnostics.
- Commit message: `M2: gate validation with cheap preflight`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
- Risks:
  - Preflight may over-block diagnostic work.
- Rollback/recovery:
  - Keep diagnostics but disable gate enforcement until selection rules are corrected.

### M3. Boundary Trigger Preservation

- Milestone state: closed
- Goal: Preserve broad validation when authoritative triggers require it.
- Requirements: `R7`-`R8`, `AC3`, `AC4`, `AC9`
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - selector fixtures
- Dependencies:
  - M2 preflight gate.
- Tests to add/update:
  - Validator implementation change triggers boundary validation.
  - Selector implementation change triggers boundary validation.
  - Release or package boundary change triggers broad validation.
  - Focused selection parity remains reviewable.
- Implementation steps:
  - Classify boundary triggers explicitly.
  - Add selector tests for authoritative broad triggers.
  - Ensure non-selected checks are explained rather than hidden.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py`
  - `git diff --check -- scripts`
- Expected observable result: narrow validation stays narrow only when no authoritative broad trigger applies.
- Commit message: `M3: preserve authoritative boundary validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
- Risks:
  - Trigger list may become stale.
- Rollback/recovery:
  - Revert selector narrowing and run existing broad validation behavior.

### M4. Shared Immutable Repository Context

- Milestone state: closed
- Goal: Reduce duplicate repository inspection while preserving standalone validator CLIs.
- Requirements: `R13`-`R14`, `AC7`, `AC8`
- Files/components likely touched:
  - validation helper modules under `scripts/`
  - affected validator CLIs
  - validator regression tests
- Dependencies:
  - M1 baseline and M3 selector behavior.
- Tests to add/update:
  - Shared context is built once for composed validation.
  - Standalone commands still work.
  - Git inspection count is reduced for the representative bundle.
- Implementation steps:
  - Introduce immutable repository-state snapshot helper.
  - Route composed validators through shared context where safe.
  - Keep CLI adapters thin and compatible.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `git diff --check -- scripts`
- Expected observable result: related validation commands avoid repeated Git and filesystem inspection within one invocation.
- Commit message: `M4: share immutable validation context`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
- Risks:
  - Shared context could couple validator ownership.
- Rollback/recovery:
  - Restore per-validator state collection while keeping standalone CLIs.

### M5. Final Verify Sequencing and Follow-Up Boundaries

- Milestone state: closed
- Goal: Align final verify evidence with committed state and keep cache/concurrency as separate governed follow-ups.
- Requirements: `R15`-`R20`, `R22`, `AC10`-`AC12`
- Files/components likely touched:
  - verify guidance
  - workflow guidance
  - change evidence templates if needed
  - validation selector tests
- Dependencies:
  - M1 through M4.
- Tests to add/update:
  - Final verify evidence requires committed tracked state for branch-ready claims.
  - Same-commit evidence avoids literal mutable final commit hashes.
  - Cache and parallel execution remain disabled unless separately enabled.
  - Performance budgets are warnings only during initial rollout.
- Implementation steps:
  - Update verify guidance and validation evidence wording.
  - Add checks or fixtures for same-commit hash wording where practical.
  - Record follow-up boundaries for caching, parallelism, and performance-budget enforcement.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md --path docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path docs/workflows.md --path scripts`
  - `git diff --check -- docs scripts`
- Expected observable result: final branch readiness is proved after commit state is stable and does not require self-invalidating hash evidence.
- Commit message: `M5: align final verify evidence sequencing`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone handed to code-review
- Risks:
  - Guidance-only changes may not catch all self-hash wording.
- Rollback/recovery:
  - Keep stable wording guidance and remove any over-strict validator checks.

## Validation plan

- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization`: validate review evidence.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml`: validate change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-preflight-first-measured-script-execution-optimization.md --path specs/validation-execution-performance-and-preflight.md --path docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md --path docs/plan.md --path docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml --path docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/review-log.md`: validate lifecycle-managed artifacts.
- `git diff --check -- docs/proposals/2026-06-24-preflight-first-measured-script-execution-optimization.md specs/validation-execution-performance-and-preflight.md docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md docs/plan.md docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization`: validate whitespace.

## Risks and recovery

- Risk: preflight suppresses required work.
  - Recovery: disable gate enforcement and restore prior broad validation while retaining tests and diagnostics.
- Risk: selection explanation becomes too verbose.
  - Recovery: keep concise default output and move detail behind verbose output or sidecar evidence.
- Risk: shared context couples validators.
  - Recovery: keep shared context immutable and preserve standalone CLIs as fallback.
- Risk: final verify sequencing still causes evidence churn.
  - Recovery: tighten final-verify evidence wording and rerun final closeout after committed state exists.

## Dependencies

- Approved spec.
- Clean spec-review and architecture assessment.
- Clean plan-review before test-spec.
- Test spec before implementation.
- Repository-owned validation scripts for proof.

## Progress

- 2026-06-24: Proposal accepted, spec approved, architecture assessment recorded as not required, and plan authored for plan-review.
- 2026-06-24: Test spec authored and activated before implementation.
- 2026-06-24: Implemented selector/CI timing, phase explanation, preflight diagnostics, boundary phase metadata, and shared immutable preflight context; code-review M1-M5 recorded clean with no material findings.
- 2026-06-24: Explain-change recorded; next lifecycle stage is verify.
- 2026-06-24: Verify report recorded; local verification passed and next lifecycle stage is PR handoff.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-24 | Use five implementation milestones. | The work separates measurement, preflight, boundary trigger preservation, shared context, and final verify sequencing into reviewable slices. | One broad validator rewrite. |
| 2026-06-24 | Record architecture as not required. | The first slice avoids persistent services, remote cache, cross-process protocols, and durable new system boundaries. | Create architecture package for script-level orchestration changes. |

## Surprises and discoveries

- None yet.

## Validation notes

- `python scripts/test-select-validation.py` passed 102 tests after selector and CI wrapper implementation.
- Code-review M1-M5 recorded clean with no material findings.
- `bash scripts/ci.sh --mode explicit --timeout 180 ...` passed selected validation after the default 60-second selected-CI attempt timed out on the long selector regression check.

## Outcome and retrospective

- Filled after completion.

## Readiness

- See `Current Handoff Summary`.
- Lifecycle routing is owned by `Current Handoff Summary`.
