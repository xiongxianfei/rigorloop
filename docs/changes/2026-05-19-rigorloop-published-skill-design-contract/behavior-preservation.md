# Published Skill Design Pilot Behavior Preservation Notes

## Scope

Changed pilot skills:

- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`

M1 records the preservation template and baseline protected behavior. M3 must fill the final rows after any behavior-significant wording is removed, moved, or rewritten.

## Preservation Template

| Skill | Removed or rewritten wording | Why safe | Essential rule preserved where |
| --- | --- | --- | --- |
| `proposal` | Frontmatter description was rewritten from a general proposal-authoring description into capability, trigger-context, and near-miss routing wording. `Workflow role` gained an explicit `must_not_claim` line. | Safe because the normal proposal procedure, required sections, artifact placement, evidence access, gates, scope preservation, handoff behavior, and output skeleton were not removed. The description now carries routing context that was previously split between the description and body. | Routing: frontmatter `description`. Claim boundary: `Workflow role` `must_not_claim` plus `Workflow handoff behavior`, `Rules`, and `Expected output`. Proposal artifact shape: `Required proposal sections` and `Output skeleton`. |
| `proposal-review` | Frontmatter description was rewritten from a general review description into capability, trigger-context, and near-miss routing wording. `Workflow role` gained an explicit `must_not_claim` line. | Safe because the review dimensions, vision and standing-gate checks, scope review, material finding contract, recording obligations, isolation behavior, closed enums, and output skeleton were not removed. The description now carries routing context that was previously implied by body sections. | Routing: frontmatter `description`. Claim boundary: `Workflow role` `must_not_claim` plus `Workflow handoff behavior`, `Isolation and Recording`, and `Rules`. Review result shape: `Material findings`, closed enums, and `Output skeleton`. |

## `proposal` Protected Behavior

M3 must preserve these behavior groups:

- author a decision-oriented proposal before spec or plan;
- record problem, goals, non-goals, vision fit, context, options, recommendation, expected behavior, architecture impact, testing strategy, rollout, risks, open questions, decision log, next artifacts, follow-on artifacts, and readiness;
- treat `VISION.md`, `CONSTITUTION.md`, `AGENTS.md`, `docs/project-map.md`, `docs/workflows.md`, local specs, ADRs, related proposals, code, issues, incidents, and user feedback as project-local conditional evidence, not RigorLoop repository prerequisites;
- preserve artifact placement defaults and no-overwrite behavior for new proposals;
- preserve standing gate checks for vision and constitution;
- preserve initial-intent and scope preservation treatment;
- preserve artifact lifecycle status guidance, including `accepted` and `Follow-on artifacts`;
- preserve handoff to `proposal-review` when no blocker remains;
- preserve output skeleton shape for proposal artifacts;
- preserve bounded evidence and full-file read escape conditions.

## `proposal-review` Protected Behavior

M3 must preserve these behavior groups:

- independently review a proposal before specification;
- challenge problem clarity, user value, option diversity, decision rationale, scope control, architecture awareness, testability, risk honesty, rollout realism, and readiness for spec;
- preserve formal review recording behavior, including recording status, blocker reporting, detailed records for material findings, review log updates, and review-resolution when required;
- preserve material finding completeness: finding ID, severity, location, evidence, required outcome, and safe resolution or needs-decision rationale;
- preserve scope-preservation review and vision-fit checks;
- preserve standing gates for `VISION.md` and `CONSTITUTION.md`;
- preserve output skeleton shape for review result and material findings;
- preserve immediate-next-stage wording without automatic downstream handoff for isolated reviews;
- preserve bounded evidence and full-file read escape conditions.

## M3 Closeout Rule

M3 must not close on structural validation alone if either pilot skill changes behavior-significant wording.

Closeout evidence must show:

- what wording moved or changed;
- why the change is safe;
- where the essential rule now lives;
- behavior-parity evidence did not weaken lifecycle rules.
