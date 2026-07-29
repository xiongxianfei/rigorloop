# Progressive Boundary-First Skill Guidance Plan Authoring

Evidence ID: progressive-boundary-first-plan-authoring
Artifact ID: plan
Stage: plan
Artifact:
`docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`
Owning change record:
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`
Completion status: complete
Resulting review-request path:
`docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/plan-review-r2.md`

## Inputs

- Accepted proposal:
  `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Approved feature specification:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved specification review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Approved canonical architecture:
  `docs/architecture/system/architecture.md`
- Accepted resource-composition ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Approved architecture review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md`
- Boundary-first planning method:
  `skills/plan/references/boundary-first-method-v1.md`
- Current projection, activation, skill-validation, selector, generation,
  adapter, and regression-test surfaces under `scripts/`, `skills/`,
  `specs/`, and `templates/`.

## Authoring result

The draft plan sequences the approved first slice into independently reviewable
resource projection, published guidance, selector routing, and package parity
milestones.
It treats the completed exact-owning-change-record lifecycle-validator
correction as a prerequisite rather than duplicating that bug fix.
It preserves `pending` activation through this implementation slice and
requires a later immutable-release activation transaction.

The draft plan maps every approved boundary and interaction to an affected surface,
dependency, rollback unit, and proof milestone.
It reserves proof-map ownership for `test-spec` and `test-spec-review` before
implementation.

## Resolved blocker

The first change-metadata validation failed with:

```text
workflow_state.planned_work: presence must match primary plan registration
```

The refined contract grants `plan` one narrow exception: when it registers a
new primary plan and `planned_work` is absent, it initializes that state once
from the ordered milestone definitions.
Workflow owns every later transition.

This plan initialized M1 through M4 as `planned`, selected M1 as current,
recorded all four implementation milestones as remaining, used an empty
`not-started` latest review, and kept final closeout not ready.
The plan entry can therefore move to `review-required`.

## Validation

- The initial metadata and lifecycle commands reproduced the missing
  `planned_work` blocker.
- The same commands are rerun after deterministic initialization before
  plan-review R2.
- `python scripts/validate-markdown-readability.py docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/plan-authoring.md`
  passed with 14 nonblocking warnings.
- `git diff --check -- docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md docs/plan.md docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/plan-authoring.md`
  passed.
