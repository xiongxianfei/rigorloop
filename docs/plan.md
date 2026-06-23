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
| [Workflow-State Projection and Pre-Transition Synchronization Gate](plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md) | active | code-review M5 | `2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate` |
| [Evidence-Bound and Incremental Project Map Skill](plans/2026-06-23-evidence-bound-incremental-project-map.md) | active | hosted CI and human review | `2026-06-23-evidence-bound-incremental-project-map` |
| [Published Skill Resource Integrity Architecture Pilot](plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md) | active | hosted CI and human review | `2026-06-22-published-skill-resource-integrity-architecture-pilot` |
| [Workflow Skill Artifact-Location Map](plans/2026-06-18-workflow-skill-artifact-location-map.md) | active | hosted CI and human review | `2026-06-17-workflow-skill-artifact-location-map` |

## Blocked

No blocked plans.

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-06-18 Guide System Source-of-Truth Alignment](plans/2026-06-18-guide-system-source-of-truth-alignment.md) - done; terminal state: done; PR #100 merged.
- [2026-05-26 CI-Maintenance Skill Rename and Workflow Authoring](plans/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md) - done; terminal state: done; PR #98 merged.
- [2026-05-25 Spec-Review Testability Routing and Output Consolidation](plans/2026-05-25-spec-review-testability-routing-output-consolidation.md) - done; terminal state: done; PR #96 merged.
- [2026-05-25 Adopter-Facing Vision and README Principle Rewrite](plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md) - done; terminal state: done; PR #94 merged through release PR #95.
- [2026-05-25 Installed-Skill Artifact Placement Contract](plans/2026-05-25-installed-skill-artifact-placement-contract.md) - done; terminal state: done; PR #93 merged.
- [2026-05-24 Target-Native Init Commands](plans/2026-05-24-target-native-init-commands.md) - done; terminal state: done; PR #92 merged.
- [2026-05-24 Cache-Aware Inner-Loop Lifecycle Validation Helper](plans/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md) - done; terminal state: done; PR #91 merged.
- [2026-05-23 Public Discovery and Developer Adoption Surface](plans/2026-05-23-public-discovery-and-developer-adoption-surface.md) - done; terminal state: done; PR #90 merged.
- [2026-05-22 Bounded Plan Index and Completed-Plan Archive](plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md) - done; terminal state: done; PR #86 merged.
- [2026-05-21 Compact Change Validation Metadata](plans/2026-05-21-compact-change-validation-metadata.md) - done; terminal state: done; PR #84 merged.

## Superseded
- none yet
