# Behavior Preservation: Plan Asset Split

## Scope

This record covers M2 of the assets-first progressive-disclosure pilot.

## Preserved Rule Locations

| Behavior-significant rule | Preserved location |
| --- | --- |
| Planning happens after stable proposal/spec/architecture direction. | `skills/plan/SKILL.md`, opening guidance and `When to use`. |
| Public skills use project-local evidence and do not require unavailable RigorLoop internals. | `skills/plan/SKILL.md`, `Project-local evidence`. |
| Upstream status settlement is bounded to lifecycle/status metadata. | `skills/plan/SKILL.md`, `Upstream status settlement`. |
| Plan outputs must include source artifacts, context, non-goals, requirements, milestones, validation, risks, dependencies, progress, decision log, surprises, validation notes, outcome, and readiness. | Compact summary in `skills/plan/SKILL.md`; canonical section order in `skills/plan/assets/plan-skeleton.md`. |
| Milestone state vocabulary and milestone loop stay explicit. | `skills/plan/SKILL.md`, `Milestone-aware plans`; repeated milestone shape in `skills/plan/assets/milestone.md`. |
| The active plan `Current Handoff Summary` owns live state and `Readiness` points to it. | `skills/plan/SKILL.md`, `Milestone-aware plans` and `Current Handoff Summary rules`; labels only in `skills/plan/assets/current-handoff-summary.md`. |
| `docs/plan.md` remains an index, not a second plan body. | `skills/plan/SKILL.md`, `Plan authoring rules`. |
| The skill must not claim implementation, review, verification, branch readiness, PR readiness, final closeout readiness, or Done prematurely. | `skills/plan/SKILL.md`, `Workflow role`, `Claims this skill must not make`, `Current Handoff Summary rules`, and `Stop conditions`. |

## Asset Boundary Check

- `skills/plan/assets/plan-skeleton.md` owns the full plan section order, headings, and placeholders.
- `skills/plan/assets/milestone.md` owns only the repeated milestone structure.
- `skills/plan/assets/current-handoff-summary.md` contains field labels and placeholders only; lifecycle consistency and claim-boundary rules remain in `SKILL.md`.
- `skills/plan/assets/decision-log-row.md` contains only the reusable decision-log table row.
- No asset contains repository-root required dependencies, hidden trigger logic, filled example narratives, or paragraph-length workflow procedure.
