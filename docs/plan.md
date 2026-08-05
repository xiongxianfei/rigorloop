# Plan index

`docs/plan.md` is a navigation index to stable plan bodies and owning change
records.
Mutable lifecycle state, current milestones, review state, blockers, and next
stages live in each plan's owning `change.yaml`.

<!--
Index policy:
- Current plan references link stable plan bodies to owning change records.
- Recent history keeps the most recent 10 completed plan references.
- Older Done entries move to docs/plan-archive.md.
- Plan links use relative Markdown targets from this file, for example `[Title](plans/YYYY-MM-DD-slug.md)`.
- Do not use bare repository-root plan paths in this index; they may not render as clickable links.
- Do not copy mutable lifecycle or routing state into this index.
-->

## Active

Compatibility heading only.
Current lifecycle state is not recorded in this index.

## Blocked

Compatibility heading only.
Current blockers are not recorded in this index.

## Current plan references

| Plan | Owning change record |
| --- | --- |
| [Progressive Boundary-First Skill Guidance](plans/2026-07-29-progressive-boundary-first-skill-guidance.md) | [change.yaml](changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml) |
| [Stage-Owned Lifecycle Artifacts and Change-Local Workflow State](plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md) | [change.yaml](changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml) |
| [Preflight-First and Measured Script Execution Optimization](plans/2026-06-24-preflight-first-measured-script-execution-optimization.md) | [change.yaml](changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml) |

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-07-28 Portable Boundary-First Capability for Published Skills](plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md) - done; terminal state: closed; PR #126 opened for review.
- [2026-07-25 Single Bounded Review-Fix Workflow Automation](plans/2026-07-21-single-bounded-review-fix-workflow-automation.md) - done; terminal state: closed; PR #124 opened for review.
- [2026-07-05 Workflow Guide Skeleton Asset](plans/2026-07-05-workflow-guide-skeleton-asset.md) - done; terminal state: closed; PR #122 opened for review.
- [2026-07-04 Markdown Readability Contract](plans/2026-07-04-markdown-readability-contract.md) - done; terminal state: closed; PR #120 opened for review.
- [2026-07-04 Test-Spec Proof-Contract Upgrade](plans/2026-07-04-test-spec-proof-contract-upgrade.md) - done; terminal state: closed; PR #119 merged.
- [2026-06-30 Bounded Review-Fix Autoprogression in Chat](plans/2026-06-30-bounded-review-fix-autoprogression-in-chat.md) - done; terminal state: closed; PR #118 merged.
- [2026-06-29 Release Transaction Automation](plans/2026-06-29-release-transaction-automation.md) - done; terminal state: closed; PR #117 opened for review.
- [2026-06-27 Broad-Smoke Safe Parallelism](plans/2026-06-27-broad-smoke-safe-parallelism.md) - done; terminal state: closed; PR #116 opened for review.
- [2026-06-27 Selector-Regression Runtime Reduction](plans/2026-06-27-selector-regression-runtime-reduction.md) - done; terminal state: done; PR #115 opened for review.
- [2026-06-26 Preflight-First Validation Runtime Optimization](plans/2026-06-26-preflight-first-validation-runtime-optimization.md) - done; terminal state: done; PR #114 opened for review.

## Historical replacements

- None currently indexed.
