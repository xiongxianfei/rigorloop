# Behavior Parity: Plan Asset Pilot

## Scope

This record covers M3 behavior-parity evidence for the assets-first `plan` pilot.

## Reference Corpus

The reference corpus uses contract-era, contract-compliant plans:

| Plan | Use |
| --- | --- |
| `docs/plans/2026-05-18-skill-readability-self-containment.md` | Primary reference plan |
| `docs/plans/2026-05-19-published-skill-design-spec-family.md` | Secondary reference plan |
| `docs/plans/2026-05-19-published-skill-design-plan-family.md` | Secondary reference plan |

## Strict Parity Checks

| Area | Result | Evidence |
| --- | --- | --- |
| Required plan sections | pass | `assets/plan-skeleton.md` includes Status, Purpose / big picture, Source artifacts, Context and orientation, Non-goals, Requirements covered, Current Handoff Summary, Milestones, Validation plan, Risks and recovery, Dependencies, Progress, Decision log, Surprises and discoveries, Validation notes, Outcome and retrospective, and Readiness. |
| Milestone shape | pass | `assets/milestone.md` preserves milestone state, goal, requirements, files/components, dependencies, tests, implementation steps, validation commands, expected result, commit message, closeout checklist, risks, and rollback/recovery. |
| Decision log shape | pass | `assets/decision-log-row.md` preserves Date, Decision, Reason, and Alternatives rejected columns. |
| Current handoff summary | pass | `assets/current-handoff-summary.md` preserves current milestone, milestone state, last reviewed milestone, review status, remaining implementation milestones, next stage, final closeout readiness, and reason. Lifecycle consistency rules remain in `skills/plan/SKILL.md`. |
| Validation evidence | pass | The skeleton keeps Validation plan and Validation notes, and the milestone template keeps Validation commands. |
| Implementation and review handoff | pass | `skills/plan/SKILL.md` retains milestone-aware handoff rules, including `review-requested`, `resolution-needed`, review-resolution loops, next-milestone handoff, and final-closeout blocking while milestones remain open. |
| Claim boundaries | pass | `skills/plan/SKILL.md` retains claims this skill must not make, readiness-vs-Done rules, stop conditions, and current-handoff claim limits. |
| Recording discipline | pass | `skills/plan/SKILL.md` retains upstream status settlement, review-log and review-resolution blockers, and lifecycle settlement reporting requirements. |

## Milestone Asset Reuse

| Reference plan | Implementation milestone blocks | Expected `assets/milestone.md` copies |
| --- | ---: | ---: |
| `docs/plans/2026-05-18-skill-readability-self-containment.md` | 3 | 3 |
| `docs/plans/2026-05-19-published-skill-design-spec-family.md` | 3 | 3 |
| `docs/plans/2026-05-19-published-skill-design-plan-family.md` | 3 | 3 |

The reusable milestone asset is used once per implementation milestone. Lifecycle-only closeout sections are not counted as implementation milestone copies.

## Follow-On Pattern Guidance

- Constructive skills that assemble structured artifacts from repeated substructures should treat `assets/` as the primary packaged-resource pattern.
- Deliberative skills that rely on rule-heavy judgment guidance should treat `references/` as the primary packaged-resource pattern, with `assets/` reserved for small copied output structures.
- This pilot does not authorize broad asset rollout without a separate proposal or spec amendment.
