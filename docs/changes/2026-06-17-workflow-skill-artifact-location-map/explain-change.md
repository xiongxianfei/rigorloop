# Explain Change: Workflow Skill Artifact-Location Map

## Status

- Change ID: `2026-06-17-workflow-skill-artifact-location-map`
- Evidence state: active
- Scope: rationale for the implemented workflow artifact-location map change through M3 handoff.

## Summary

This change makes artifact placement deterministic without moving content ownership into the workflow skill. The workflow guide now carries a project-local artifact registry and human-readable map, the workflow skill explains how to create or refresh that map, and validation checks catch drift between the map, workflow defaults, affected stage skills, and packaged adapter behavior.

The repository-standard plan contract is preserved: `docs/plan.md` is the lifecycle index, while detailed plan bodies live under `docs/plans/YYYY-MM-DD-slug.md`.

## Change Rationale

| Surface | Why it changed |
| --- | --- |
| `docs/workflows.md` | Maintainers needed one deterministic place to answer where workflow-managed artifacts go. The guide now has a canonical YAML registry plus Markdown projections for humans. |
| `skills/workflow/SKILL.md` | The skill owns creating or refreshing the project-local artifact-location map, source-rank behavior, unknown-artifact blocking, and map-update reasons while leaving artifact content to owning stage skills. |
| `skills/plan/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md` | These were inspected for direct placement contradictions. No M1 content edit was needed because their placement text matched the approved map. |
| `scripts/skill_validation.py` and `scripts/test-skill-validator.py` | M2 adds deterministic validation for registry shape, required entries, table/registry agreement, plan-path drift, review-path drift, unknown artifact types, workflow-skill default drift, and directly affected stage-skill contradictions. |
| Change-local M3 evidence | M3 records behavior-preservation, cold-read placement proof, and adapter proof so the branch can proceed to code-review with traceable evidence. |

## Boundaries Preserved

- Lifecycle stage order is unchanged.
- Artifact content schemas are unchanged.
- `docs/plans/YYYY-MM-DD-slug.md` remains the canonical detailed plan-body path.
- Formal review records remain under `docs/changes/<change-id>/reviews/`.
- Stage-skill portable defaults remain available for customer projects without `docs/workflows.md`.
- Generated public adapter output is not hand-edited.

## Validation Evidence

Validation evidence is recorded in the active plan and `docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml`. The M3 handoff passed adapter packaging checks, skill validation, lifecycle validation, metadata validation, whitespace checks, and selected CI.
