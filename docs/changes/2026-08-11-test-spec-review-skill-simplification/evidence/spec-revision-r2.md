# Spec Revision Evidence R2: Test-Spec-Review Skill Simplification

Stage: spec
Date: 2026-08-11

- Artifact: `specs/test-spec-review-skill-simplification.md`
- Prior review: `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/spec-review-r1.md`

## Revision scope

The bounded correction resolves `TSRSIM-SR1` without changing package design, recording policy, or workflow stage order.

## Resolution

- Added R39 with the closed lifecycle-by-handoff validity matrix.
- Preserved formal review with isolated or workflow-managed handoff.
- Preserved advisory review with isolated handoff.
- Rejected advisory review with workflow-managed handoff before review or routing.
- Added E9, EC13, AC-TSRSIM-019, boundary ownership, interaction coverage, state invariants, and error behavior.

## Validation target

The corrected spec requires independent spec-review R2.
Boundary feature-record validation must have no issue other than the staged missing proof map owned by the later test-spec stage.
