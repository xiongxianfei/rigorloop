# Workflow Refactor Change Explanation

## Status

M2 complete; ready for `code-review`.

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

Broader selector, lifecycle, and regression coverage remains scheduled for M3. M2 intentionally keeps project-map lifecycle mechanics and the final learn artifact model out of scope.

The final learn artifact model is deferred to a later learn refactor. M1 records only the temporary workflow behavior required by the approved workflow spec: capture immediately, schedule follow-up, or record a no-learn rationale when a trigger occurs.

## M2 changes

M2 aligns canonical stage skills with the approved workflow contract. `skills/workflow/SKILL.md` now routes by categories, obligation values, triggers, `review-resolution`, and `ci-maintenance` instead of the old overloaded chain.

`skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` now state the standing-artifact gates for first substantive proposals, bootstrap exceptions, and governance/source-of-truth proposals. `skills/ci/SKILL.md` now presents CI work as `ci-maintenance` and separates CI infrastructure from validation execution, test design, and validation-command ownership.

`skills/learn/SKILL.md` now treats `learn` as periodic or explicitly invoked and records the approved temporary closeout options: immediate capture, scheduled follow-up, or explicit no-learn rationale. `skills/verify/SKILL.md` had stale downstream handoff wording, so M2 updates it to hand off to `ci-maintenance` only when hosted workflow automation or related CI infrastructure is triggered.

M2 also adds focused skill-validator assertions for these skill-contract guarantees and regenerates `.codex/skills/` plus generated public adapters under `dist/adapters/` from canonical skill sources.

## Validation

M1 and M2 validation evidence is recorded in `change.yaml` and the active plan. M2 proof covered skill validation, skill regression fixtures, generated Codex skill drift, public adapter regression, adapter drift, adapter validation, and explicit-path CI over the touched M2 authored and generated surfaces.

## Review closeout

`code-review-m1-r1` found one stale-plan wording defect. `review-resolution.md` records the accepted disposition and the plan now states that `specs/rigorloop-workflow.test.md` is active and was updated by the `test-spec` stage before M1.

`code-review-m2-r1` returned `clean-with-notes` with no material findings. M3 remains the next implementation milestone.
