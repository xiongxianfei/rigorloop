# Behavior Preservation: Workflow Skill Artifact-Location Map

## Status

- Change ID: `2026-06-17-workflow-skill-artifact-location-map`
- Evidence state: active
- Scope: M3 adapter proof, cold-read evidence, and lifecycle preservation evidence.

## Preservation Matrix

| Surface | Baseline | M3 proof | Preservation |
| --- | --- | --- | --- |
| Lifecycle order | The standard chain remains proposal, proposal-review, spec, spec-review, architecture when required, architecture-review when required, plan, plan-review, test-spec, implement, code-review, review-resolution when triggered, ci-maintenance when triggered, explain-change, verify, pr. | `docs/workflows.md` still exposes the same lifecycle graph; M3 does not edit lifecycle ordering. | Preserved. |
| Stage ownership | Stage skills own artifact content; workflow owns routing and the project-local map. | `skills/workflow/SKILL.md` keeps the content-ownership boundary and M3 changes only proof/lifecycle surfaces. | Preserved. |
| Plan index | `docs/plan.md` is a bounded lifecycle index, not a plan body. | The cold-read proof answers this from `docs/workflows.md`, `skills/workflow/SKILL.md`, and `docs/plan.md`. | Preserved and clarified. |
| Plan body | Workflow-managed detailed plan bodies use `docs/plans/YYYY-MM-DD-slug.md`. | The cold-read proof records this answer and M3 does not change plan placement. | Preserved. |
| Review records | Formal review records live under `docs/changes/<change-id>/reviews/` unless a higher-priority source permits another path. | The cold-read proof records proposal-review placement under `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`. | Preserved. |
| Customer projects | Stage-skill portable defaults remain available when `docs/workflows.md` is absent or silent. | M3 records portability as unchanged and does not remove any stage-skill portable defaults. | Preserved. |
| Generated adapters | Generated public adapter output is maintained through repository-owned scripts, not hand edits. | Adapter validation is in scope because `dist/adapters/manifest.yaml` includes `workflow`; M3 uses build/check commands and does not hand-edit generated public adapter output. | Preserved. |

## Cold-Read Proof

Method: cold-read tracked workflow artifacts without relying on chat history.

Evidence sources:

- `docs/workflows.md`
- `skills/workflow/SKILL.md`
- `docs/plan.md`

| Question | Answer from tracked artifacts |
| --- | --- |
| Where does a proposal-review record go? | `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`, unless a higher-priority explicit path, active metadata, approved spec, schema, safety constraint, or user instruction permits another path. |
| Where does a workflow-managed detailed change plan go? | `docs/plans/YYYY-MM-DD-slug.md`. |
| What is `docs/plan.md` for? | Bounded lifecycle index of active, blocked, recent done, and active supersession context; it is not a concrete plan body. |

Basis:

- `docs/workflows.md` registry and review-placement sections place formal review records under `docs/changes/<change-id>/reviews/`.
- `skills/workflow/SKILL.md` says formal lifecycle recording creates or identifies the change pack before formal review records.
- `docs/workflows.md` plan surfaces identify `docs/plans/YYYY-MM-DD-slug.md` as the plan body path.
- `skills/workflow/SKILL.md` lists `docs/plans/YYYY-MM-DD-slug.md` as the detailed plan default and explicitly rejects `docs/changes/<change-id>/plan.md` as the plan body.
- `docs/workflows.md`, `skills/workflow/SKILL.md`, and the index policy comment at the top of `docs/plan.md` all describe `docs/plan.md` as an index.

## Boundary Check

- M3 does not change lifecycle order.
- M3 does not redefine proposal, spec, plan, review, verify, PR, or learn artifact content schemas.
- M3 does not migrate historical `docs/plans/*.md` files.
- M3 does not hand-edit generated public adapter output.
- M3 does not change stage-skill placement behavior.

## Validation Evidence

M3 validation evidence is recorded in the active plan and `change.yaml`. The selected CI run passed adapter drift, skill generation, lifecycle, metadata, and selector checks for the M3 path set.
