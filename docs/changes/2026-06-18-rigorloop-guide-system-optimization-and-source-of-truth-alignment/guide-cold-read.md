# Guide Cold-Read Proof

Change ID: `2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
Proof date: 2026-06-18

## Method

Reviewer persona: a new contributor using only current repository guide surfaces.

Allowed sources:

- `README.md`
- `CONSTITUTION.md`
- `docs/workflows.md`
- `docs/project-map.md`
- `docs/plan.md`
- `skills/*/SKILL.md` where the workflow guide points to stage skills

Disallowed sources:

- chat history
- previous assistant messages
- learn-session archaeology as live routing authority

## Questions and Answers

| Question | Answer from current guide system | Source used | Chat or learn archaeology needed? |
| --- | --- | --- | --- |
| Where do I start? | Start at `README.md`; its `Where to go next` table routes readers by need. | `README.md` `Where to go next` | No |
| Where does a proposal go? | Workflow-managed proposals go under `docs/proposals/YYYY-MM-DD-slug.md`. | `docs/workflows.md` artifact registry and `Artifact locations` table | No |
| Where does a formal review record go? | Formal review records go under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`. | `docs/workflows.md` artifact registry, `Artifact locations`, and `Review record placement` | No |
| What is `docs/plan.md` for? | It is the bounded lifecycle index for active, blocked, recent done, and superseded planned work; it is not the body of a plan. | `docs/plan.md` opening boundary text and `docs/workflows.md` `Plan surfaces` | No |
| Where is the detailed plan for one workflow-managed planned initiative? | The concrete plan body lives under `docs/plans/YYYY-MM-DD-slug.md`. | `docs/workflows.md` artifact registry, `Artifact locations`, and `Plan surfaces`; `docs/project-map.md` orientation notes | No |
| Which guide explains repository structure? | `docs/project-map.md` explains repository structure and boundaries. | `README.md` guide index and `docs/workflows.md` guide ownership matrix | No |
| Which guide explains governance? | `CONSTITUTION.md` governs source-of-truth order and repository rules. | `README.md` guide index and `docs/workflows.md` guide ownership matrix | No |
| Which file is live routing authority for project-local artifact placement? | `docs/workflows.md` is the project-local workflow guide and artifact-location map, subordinate to higher-priority governance, specs, schemas, and explicit safe constraints. | `docs/workflows.md` source-rank guidance and guide ownership matrix | No |
| Which files are historical rationale only? | Learn sessions under `docs/learn/sessions/` explain historical rationale and are not live routing authority unless a rule is promoted to a live guide, approved spec, schema, or owning stage skill. | `docs/workflows.md` guide ownership matrix and learn-session non-authority note | No |

## Cross-Checks

| Expected distinction | Observed proof |
| --- | --- |
| README orients but does not own full workflow policy. | README links to the workflow guide and shows only a workflow-at-a-glance summary and examples. |
| Workflow guide routes artifacts but does not own artifact schemas. | `docs/workflows.md` says it does not define full schemas, required fields, lifecycle status values, or validation rules. |
| Project map orients to repository structure but does not own workflow policy. | `docs/project-map.md` says it does not own workflow stage order, exact lifecycle artifact placement, or current milestone state. |
| Plan index and plan body are separated. | `docs/plan.md` says it is not the body of a plan; `docs/workflows.md` routes plan bodies to `docs/plans/YYYY-MM-DD-slug.md`. |
| Stage skills remain relevant for customer projects. | `docs/workflows.md` says stage skills own stage execution and portable defaults, and `skills/workflow/SKILL.md` carries project-local guidance plus portable-default/block-on-ambiguity behavior. |

## Result

Pass. The guide system answers the common routing questions without chat history or learn-session archaeology.
