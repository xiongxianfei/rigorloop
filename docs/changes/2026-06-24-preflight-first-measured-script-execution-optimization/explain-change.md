# Explain Change: Preflight-First and Measured Script Execution Optimization

## Summary

This change implements the first slice of the accepted preflight-first validation execution proposal. It adds cheap Git/artifact preflight evidence to selection, makes selected checks expose phase and cache status, reports selected-CI phase timing, preserves existing selected-check execution semantics, and records workflow evidence through proposal, spec, test-spec, plan, implementation review, and verification routing.

## Problem

The proposal identified repeated verification cost caused by broad validation running before cheap blockers were resolved, duplicate repository inspection, stale evidence after repository state changed, and self-referential commit-hash evidence. The implementation targets the local selector and selected-CI wrapper first because those surfaces decide what runs, why it runs, and what evidence is visible.

## Decision Trail

| Source | Decision reflected in the diff |
| --- | --- |
| Proposal | Optimize sequencing and evidence before caching or new parallelism. |
| Spec | Preflight runs before focused/boundary execution; blocked preflight names the blocker and corrective action. |
| Test spec | Selector and CI wrapper tests cover preflight results, phase metadata, cache status, timing output, and blocked execution. |
| Plan | Five milestones split timing, preflight, boundary preservation, shared context, and final-verify boundaries. |
| Code review | M1-M5 reviews recorded clean with no material findings. |

## Diff Rationale By Area

| Area | Change | Why |
| --- | --- | --- |
| `scripts/validation_selection.py` | Adds `RepositoryPreflightContext`, preflight result records, boundary/focused phase metadata, and `cache_status: not-applicable`. | Makes cheap blockers and selected-check identity explicit without enabling unsafe cache reuse. |
| `scripts/validation_selection.py` | Builds tracked/unmerged Git state once for selector preflight. | Reduces repeated Git inspection in the implemented selector path while keeping standalone CLI behavior. |
| `scripts/validation_selection.py` | Blocks untracked governing artifacts with `untracked-authoritative-artifacts` and `git add -- <path>` action. | Prevents expensive validation from running when final readiness is already impossible and gives an actionable fix. |
| `scripts/ci.sh` | Requires `preflight_results`, prints preflight diagnostics, check phase, and phase timing summary. | Makes selection and timing reviewable while preserving the existing check summary format. |
| `scripts/test-select-validation.py` | Adds coverage for preflight pass/block behavior, phase/cache metadata, boundary phase selection, and CI timing output. | Proves the new contract without reducing selected-check coverage. |
| Lifecycle artifacts | Adds proposal, approved spec, active test spec, active plan, review log, clean review receipts, and plan index entry. | Keeps the change reviewable under the repository workflow. |

## Tests Added Or Changed

- Selector JSON now verifies `phase` and `cache_status`.
- Boundary smoke selection verifies `phase: boundary`.
- Temporary Git fixtures verify tracked authoritative artifacts pass preflight.
- Temporary Git fixtures verify untracked authoritative artifacts block with a concrete `git add -- <path>` action.
- Selected-CI fixture output verifies preflight diagnostics, per-check phase output, and phase timing summary.

## Validation Evidence Before Final Verify

- `python scripts/test-select-validation.py`: passed 102 tests after implementation.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization`: passed with 8 reviews, 0 findings, 8 log entries, 0 resolution entries.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml`: passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: passed for the proposal, spec, test spec, plan, plan index, change metadata, and review log.

## Review Resolution Summary

No material findings were recorded in proposal-review R1, spec-review R1, plan-review R1, or code-review M1-M5. No `review-resolution.md` file is required for this change at this point.

## Alternatives Rejected

- First-slice caching was deferred because complete input identity and final-closeout boundaries require separate review.
- New first-slice parallel execution was deferred because independence, deterministic output ordering, and resource contention need separate proof.
- Literal final commit hashes are not used as same-commit evidence; final verify evidence uses stable current-HEAD and clean-worktree wording.

## Scope Control

The implementation intentionally limits behavior changes to selector preflight, selected-CI evidence, and tests around those surfaces. It does not introduce a remote cache, persistent worker, hosted-CI redesign, new process pool, or broad validator rewrite.

## Risks And Follow-Ups

- Preflight authoritative-path coverage should be expanded only with tests that prove required diagnostic and lifecycle paths are not over-blocked.
- Detailed timing sidecars, cache identity, and new concurrency behavior remain follow-up proposals after baseline measurements.
- Final branch readiness must be verified against the committed current `HEAD` with a clean worktree.
