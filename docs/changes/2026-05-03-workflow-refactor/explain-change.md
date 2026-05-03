# Workflow Refactor Change Explanation

## Status

M1 complete; ready for `code-review`.

## Source artifacts

- Proposal: `docs/proposals/2026-05-01-workflow-refactor.md`
- Spec: `specs/rigorloop-workflow.md`
- Test spec: `specs/rigorloop-workflow.test.md`
- Plan: `docs/plans/2026-05-03-workflow-refactor.md`

## M1 changes

M1 aligns root and contributor-facing workflow guidance with the approved workflow category model. The changed guidance distinguishes standing artifacts, living references, workflow infrastructure, on-demand artifacts, the per-change chain, and periodic learning.

The root guidance now treats `docs/project-map.md` as a living reference that cannot be relied on when absent, stale, contradicted, or missing the relied-on area. This change records a no-map rationale in the plan because M1 relies on approved workflow artifacts and bounded root guidance, not on repository-shape claims from a project map.

The M1 guidance also separates `ci-maintenance` from validation execution, keeps `review-resolution` as closeout for material review findings rather than a review stage, and describes `learn` as periodic or explicitly invoked rather than part of the default per-change chain.

## Affected surfaces

- `CONSTITUTION.md`: updated where current wording conflicted with the approved workflow contract.
- `AGENTS.md`: updated for the practical execution chain, project-map no-reliance, learning, autoprogression, and `ci-maintenance` wording.
- `README.md`: updated to present the category model and the per-change chain without implying that `explore`, `research`, `learn`, or CI infrastructure maintenance are default per-change stages.
- `docs/workflows.md`: updated as the short operating summary for categories, obligations, handoffs, and stage boundaries.
- `docs/plan.md` and `docs/plans/2026-05-03-workflow-refactor.md`: updated as lifecycle and execution-plan surfaces for the active refactor.

## Deferred surfaces

Canonical stage skills, generated `.codex/skills/`, generated public adapters, and validator/regression coverage remain scheduled for later milestones. M1 intentionally does not update them.

The final learn artifact model is deferred to a later learn refactor. M1 records only the temporary workflow behavior required by the approved workflow spec: capture immediately, schedule follow-up, or record a no-learn rationale when a trigger occurs.

## Validation

M1 validation evidence is recorded in `change.yaml` and the active plan. Selector-selected proof covered artifact lifecycle validation, change metadata regression and validation, README validation, README vision marker validation, and selector regression coverage.

## Review closeout

`code-review-m1-r1` found one stale-plan wording defect. `review-resolution.md` records the accepted disposition and the plan now states that `specs/rigorloop-workflow.test.md` is active and was updated by the `test-spec` stage before M1.
