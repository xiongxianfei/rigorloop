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
| [Independent Test-Spec-Review Gate](plans/2026-06-25-independent-test-spec-review-gate.md) | active | pr | 2026-06-25-independent-test-spec-review-gate |
| [Preflight-First and Measured Script Execution Optimization](plans/2026-06-24-preflight-first-measured-script-execution-optimization.md) | active | pr | 2026-06-24-preflight-first-measured-script-execution-optimization |

## Blocked

No blocked plans.

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-06-25 Independent Adversarial Review Gates](plans/2026-06-25-independent-adversarial-review-gates.md) - done; terminal state: done; PR #110 merged.
- [2026-06-24 Implementation Autoprogression Through Verify](plans/2026-06-24-implementation-autoprogression-through-verify.md) - done; terminal state: done; PR #108 merged.
- [2026-06-24 Proposal-Gated Authoring Autoprogression Through Plan Review](plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md) - done; terminal state: done; PR #106 opened for review.
- [2026-06-23 Published Skill Resource Integrity Architecture Pilot](plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md) - done; terminal state: done; PR #101 merged.
- [2026-06-23 Evidence-Bound and Incremental Project Map Skill](plans/2026-06-23-evidence-bound-incremental-project-map.md) - done; terminal state: done; PR #102 merged.
- [2026-06-23 Workflow-State Projection and Pre-Transition Synchronization Gate](plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md) - done; terminal state: done; PR #103 merged.
- [2026-06-18 Workflow Skill Artifact-Location Map](plans/2026-06-18-workflow-skill-artifact-location-map.md) - done; terminal state: done; PR #99 merged.
- [2026-06-18 Guide System Source-of-Truth Alignment](plans/2026-06-18-guide-system-source-of-truth-alignment.md) - done; terminal state: done; PR #100 merged.
- [2026-05-26 CI-Maintenance Skill Rename and Workflow Authoring](plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md) - done; terminal state: done; PR #98 merged.
- [2026-05-25 Spec-Review Testability Routing and Output Consolidation](plans/2026-05-25-spec-review-testability-routing-output-consolidation.md) - done; terminal state: done; PR #96 merged.

## Superseded
- none yet
