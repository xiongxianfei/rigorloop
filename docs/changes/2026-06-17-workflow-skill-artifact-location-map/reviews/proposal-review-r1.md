# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Target: docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md
Reviewed artifact: docs/proposals/2026-06-17-workflow-skill-artifact-location-map.md
Review date: 2026-06-17
Reviewer: Maintainer proposal-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: WFO-PR1, WFO-PR2, WFO-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md
- Review resolution: docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md
- Open blockers: none after proposal revision
- Immediate next stage: proposal-review R2
- No automatic downstream handoff: this review does not start spec, test-spec, plan, or implementation work.

## Overall Verdict

The proposal is directionally strong. It correctly identifies that the `workflow` skill owns the project-local routing map while stage skills own artifact content and portable defaults.

The proposal is not ready for spec as originally written because the plan-location contract, `docs/workflows.md` representation, and stage-skill edit boundary need to be decided before downstream spec work.

## Findings

### WFO-PR1 - Plan-location direction is both a goal and an open question

Finding ID: WFO-PR1
Severity: major
Location: `Goals`, `Recommended Direction`, `Open Questions`
Evidence: The proposal lists `docs/changes/<change-id>/plan.md` as the intended detailed workflow-managed plan location, but later asks whether `docs/plans/*.md` should be migrated, retained, or reclassified, and whether `CONSTITUTION.md` should be updated or `docs/plans/` preserved.
Required outcome: The proposal must choose one first-slice direction.
Safe resolution: Choose `docs/changes/<change-id>/plan.md` as the forward canonical workflow-managed change plan, keep `docs/plan.md` as the global index, retain existing `docs/plans/*.md` as legacy or historical in this slice, and require the downstream spec to update `CONSTITUTION.md` and `docs/workflows.md` together.

### WFO-PR2 - `docs/workflows.md` representation needs a single authoritative machine-checkable surface

Finding ID: WFO-PR2
Severity: major
Location: `Open Questions`, `Testing and Verification Strategy`
Evidence: The proposal asks whether `docs/workflows.md` should be Markdown-table-only, YAML-block-only, or both, but its validation strategy depends on deterministic checks.
Required outcome: Define a representation model before spec.
Safe resolution: Use both a canonical fenced YAML artifact registry for validators and synchronized Markdown tables for users, with validation checking that the Markdown table and YAML registry agree.

### WFO-PR3 - Stage-skill edit boundary is under-specified

Finding ID: WFO-PR3
Severity: major
Location: `Open Questions`, `Architecture Impact`, `Scope budget`
Evidence: The proposal says stage skills should not contradict `docs/workflows.md`, but leaves open whether stage skills should be edited in the same implementation slice or only when validation detects contradiction.
Required outcome: Make the stage-skill edit policy explicit.
Safe resolution: Edit stage skills in the same slice only when they directly contradict the new workflow map or source-rank model. Required first-slice candidates are `workflow`, `plan` if its default plan-body path conflicts, `proposal-review` if formal review path text conflicts, and `spec-review` if formal review path text conflicts. Do not bulk-edit all lifecycle skills for stylistic consistency.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal names real artifact-placement ambiguity. |
| User value | pass | Deterministic placement improves traceability and adopter confidence. |
| Option diversity | pass | It compares narrative workflow, workflow-only, stage-skill-only, and dual-layer models. |
| Decision rationale | pass with revisions | Option 4 is correct; plan-location decision must be finalized. |
| Scope control | concern | Plan path and stage-skill edit scope need sharper boundaries. |
| Architecture awareness | pass | The source-of-truth layering is correctly framed. |
| Testability | concern | Good checks, but representation model must be decided. |
| Risk honesty | pass | It explicitly names drift, over-centralization, and current guidance conflict. |
| Readiness for spec | changes-requested | Resolve `WFO-PR1`, `WFO-PR2`, and `WFO-PR3` first. |

## Recommended Next Stage

Revise the proposal to resolve `WFO-PR1`, `WFO-PR2`, and `WFO-PR3`, then rerun proposal-review before downstream spec reliance.
