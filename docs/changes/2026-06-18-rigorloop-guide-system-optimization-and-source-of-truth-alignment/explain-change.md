# Explain Change

Change ID: `2026-06-18-rigorloop-guide-system-optimization-and-source-of-truth-alignment`
Explain date: 2026-06-18

## Why This Change Exists

RigorLoop had several useful guide-like surfaces, but contributors could still struggle to tell which guide answered which question. The approved spec requires the guide system to separate orientation guides from normative contracts, preserve the workflow-map source-of-truth boundary, keep stage skills portable, and make drift detectable.

## What Changed

### M1. Guide surface alignment

- `README.md` gained a compact `Where to go next` guide index so first-contact readers can find vision, governance, workflow/artifact paths, repository orientation, current work, and stage skills without README becoming the workflow manual.
- `docs/workflows.md` gained guide ownership/source-rank guidance and learn-session non-authority wording while preserving the workflow-map registry as the project-local artifact-location map.
- `docs/project-map.md` now explicitly says it orients to repository structure and does not own workflow stage order, exact lifecycle artifact placement, or current milestone state.
- `docs/plan.md` remains a bounded lifecycle index and points active work to the concrete plan body.

### M2. Cross-guide validation

- Added `scripts/validate-guide-system.py` for deterministic cross-guide checks covering README links, workflow guide ownership sections, project-map scope, plan-index boundary, learn-session non-authority, stage-skill path drift, and duplicate registry placement outside `docs/workflows.md`.
- Added `scripts/test-guide-system-validator.py` fixture coverage for the guide-system checks.
- Updated selected validation so relevant guide surfaces and guide-validator source changes run the appropriate guide-system checks.
- Resolved `GUIDE-CR1` by composing `skill_validation.validate_workflow_artifact_map_contract` instead of duplicating workflow-map registry/table semantics inside the guide-system validator.

### M3. Proof and lifecycle evidence

- Added `behavior-preservation.md` to prove the guide-system change preserves governance, exact workflow-map ownership, plan-body placement, stage-skill portability, generated output policy, lifecycle order, artifact schemas, baseline-drift handling, and security/privacy posture.
- Added `guide-cold-read.md` to answer common guide-routing questions using current guide surfaces only.
- Added this `explain-change.md` as the durable rationale surface for the non-trivial change.

## Important Decisions

| Decision | Reason |
| --- | --- |
| Do not create `docs/guides.md` in the first slice. | README and `docs/workflows.md` can carry the guide index/ownership without adding another guide surface. |
| Keep exact artifact-location registry semantics owned by the workflow-map contract. | The guide-system spec owns source-of-truth alignment, not a second artifact registry contract. |
| Keep cross-guide checks out of `validate-skills.py`. | Skill validation should stay focused on skill-file constraints; cross-guide drift belongs to a guide-system validator. |
| Do not edit stage skills for style or symmetry. | Stage skills must remain portable and only direct contradictions were in scope; no canonical skill files changed in this branch. |
| Do not migrate historical artifacts. | The first slice defines forward alignment and records baseline drift; migration requires separate approval. |

## Validation Summary

Validation evidence is recorded in `change.yaml` and the active plan. The core proof includes:

- guide-system regression tests and validator runs;
- selected validation for changed guide and validator surfaces;
- workflow-map owner tests for registry/table consistency;
- lifecycle and review-artifact validation for recorded review evidence;
- selected CI over the final M3 proof and lifecycle surfaces.

## Scope Boundaries

This change does not:

- change lifecycle stage order;
- change artifact schemas;
- change canonical plan-body placement from `docs/plans/YYYY-MM-DD-slug.md`;
- make README the authoritative workflow manual;
- make learn sessions live routing authority;
- migrate historical artifacts;
- hand-edit generated adapter output;
- claim verify, PR, branch, or release readiness.
