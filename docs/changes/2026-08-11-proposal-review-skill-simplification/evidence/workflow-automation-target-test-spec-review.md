# Workflow Automation Target: Test-Spec Review

Stage: workflow
Date: 2026-08-11
Change: `2026-08-11-proposal-review-skill-simplification`
Mechanism: `bounded-review-fix`
Target: `test-spec-review`
Occurrence: singleton
Authorization: explicit user command `$workflow auto: test-spec-review`

## Starting position

The proposal is accepted by `proposal-review-r4`, all recorded proposal findings are resolved, and the governed change record is valid under `stage-owned-change-local-v1`.

The canonical next stage is `spec`. The automation target authorizes progression through specification, formal spec review, architecture assessment and any required architecture work, planning, formal plan review, test-spec authoring, and formal test-spec review.

## Boundaries

- Every authoring and review stage retains ownership of its artifact and settlement.
- Every formal review must be recorded before promotion.
- Material findings may enter only bounded same-stage correction and rereview.
- `blocked`, `inconclusive`, `needs-decision`, ambiguous architecture applicability, or failed required validation pauses automation.
- Reaching a recorded `test-spec-review` result stops the run regardless of outcome.
- This authorization does not permit implementation, PR work, pushing, publishing, release, deployment, merge, destructive Git operations, credential use, or external-system mutation.

## Boundary-first routing

This change defines new public skill behavior. Specification must establish stable requirement, boundary, interaction, example, and acceptance identities before downstream proof planning. Test-spec must consume those approved identities rather than inventing outcomes.
