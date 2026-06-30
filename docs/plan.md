# Plan index

`docs/plan.md` is the bounded lifecycle index for active, blocked, recent done, and superseded planned work. It is not the body of a plan.

<!--
Index policy:
- Active and Blocked are complete and first.
- Done (recent) keeps the most recent 10 completed plans.
- Older Done entries move to docs/plan-archive.md.
- Plan links use relative Markdown targets from this file, for example `[Title](plans/YYYY-MM-DD-slug.md)`.
- Do not use bare repository-root plan paths in this index; they may not render as clickable links.
- Done entries are one line: date, title, plan link, terminal state, PR/disposition.
- Do not place active, blocked, unresolved, or review-needed work in the archive.
-->

## Active

| Plan | State | Next stage | Change ID |
| --- | --- | --- | --- |
| [Preflight-First and Measured Script Execution Optimization](plans/2026-06-24-preflight-first-measured-script-execution-optimization.md) | active | pr | 2026-06-24-preflight-first-measured-script-execution-optimization |

## Blocked

No blocked plans.

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-06-29 Release Transaction Automation](plans/2026-06-29-release-transaction-automation.md) - done; terminal state: closed; PR #117 opened for review.
- [2026-06-27 Broad-Smoke Safe Parallelism](plans/2026-06-27-broad-smoke-safe-parallelism.md) - done; terminal state: closed; PR #116 opened for review.
- [2026-06-27 Selector-Regression Runtime Reduction](plans/2026-06-27-selector-regression-runtime-reduction.md) - done; terminal state: done; PR #115 opened for review.
- [2026-06-26 Preflight-First Validation Runtime Optimization](plans/2026-06-26-preflight-first-validation-runtime-optimization.md) - done; terminal state: done; PR #114 opened for review.
- [2026-06-26 Requirement-Fidelity Gate for Spec-Canonical Reviews](plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md) - done; terminal state: done; PR #113 merged.
- [2026-06-26 Independent Test-Spec-Review Gate](plans/2026-06-25-independent-test-spec-review-gate.md) - done; terminal state: done; PR #111 merged.
- [2026-06-25 Independent Adversarial Review Gates](plans/2026-06-25-independent-adversarial-review-gates.md) - done; terminal state: done; PR #110 merged.
- [2026-06-24 Implementation Autoprogression Through Verify](plans/2026-06-24-implementation-autoprogression-through-verify.md) - done; terminal state: done; PR #108 merged.
- [2026-06-24 Proposal-Gated Authoring Autoprogression Through Plan Review](plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md) - done; terminal state: done; PR #106 opened for review.
- [2026-06-23 Published Skill Resource Integrity Architecture Pilot](plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md) - done; terminal state: done; PR #101 merged.

## Superseded
- none yet
