# Progressive Boundary-First Skill Guidance Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review skill
Target: docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md
Status: blocked
Original review source: User-requested `$plan-review` on 2026-07-29.
Material findings: none
Immediate next stage: resolve lifecycle registration blocker
Automatic downstream handoff: none

## Result

- Skill: plan-review
- Review status: blocked
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/plan-review-r1.md`
- Review log:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-log.md`
- Review resolution:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-resolution.md#plan-review-r1`
- Open blockers:
  `workflow_state.planned_work` cannot be made consistent by the plan or
  plan-review owner under the current fixed write boundaries
- Immediate next stage: blocked

## Lifecycle precondition

The plan body and plan-authoring record exist, and the matching plan entry is
correctly still `authoring`.

Required change-metadata validation failed:

```text
workflow_state.planned_work: presence must match primary plan registration
```

The current lifecycle contract requires `planned_work` exactly when a primary
plan is registered.
It separately allows `plan` to write only the plan artifact, plan-authoring
evidence, and matching plan artifact-state transition.
Only `workflow` may write `workflow_state`.

Because the plan stage cannot complete its required validation without a
workflow-owned write, it cannot transition the plan entry to
`review-required`.
Plan-review requires `review-required` plus complete authoring evidence before
settlement.
The review therefore records the blocker without changing the plan, its
artifact entry, or workflow routing.

## Review inputs

- Draft plan:
  `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Plan authoring evidence:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/evidence/plan-authoring.md`
- Accepted proposal:
  `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Approved specification:
  `specs/progressive-boundary-first-skill-guidance.md`
- Approved spec review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/spec-review-r1.md`
- Approved canonical architecture:
  `docs/architecture/system/architecture.md`
- Accepted ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Approved architecture review:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/reviews/architecture-review-r2.md`
- Boundary-first review method:
  `skills/plan-review/references/boundary-first-method-v1.md`
- Stage-owned lifecycle specification:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`

The matching test specification does not exist yet, as expected before an
approved plan-review.

## Findings

No material plan-content finding is recorded because lifecycle prerequisites
prevented the plan from becoming reviewable.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Self-contained context | pass | The draft names source artifacts, current modules, prerequisite bug fix, activation boundary, non-goals, milestones, commands, and recovery. |
| Source alignment | pass | The draft preserves the approved compact core, family resources, artifact slicing, scenario restraint, selector ownership, pending activation, and package parity. |
| Milestone size | pass | Four implementation units separate resource projection, published guidance, selector routing, and derived package proof. |
| Sequencing | pass | Test-spec review precedes M1; each later milestone depends on reviewed earlier behavior; actual activation remains later. |
| Scope discipline | pass | The draft does not delete lifecycle validation, invent release identities, activate the capability, or track derived output. |
| Validation quality | concern | Commands are concrete, but formal reliance is blocked until the plan authoring transition validates. |
| TDD readiness | pass | Each milestone lists tests before implementation and the preimplementation proof gate maps all approved IDs. |
| Risk coverage | pass | Resource drift, over-formalization, slice insufficiency, selector narrowing, package divergence, false activation, and measurement misuse have recovery paths. |
| Architecture alignment | pass | Manifest, source owners, projection identities, skill maps, selector, tracked transaction, derived proof, and pending activation match ADR-20260729. |
| Operational readiness | block | The plan cannot enter `review-required` under the current cross-owner metadata invariant. |
| Plan maintainability | pass | Stable requirement, boundary, interaction, dependency, rollback, and validation mappings are explicit without mutable progress state. |

## Missing lifecycle transition

The stage-owned lifecycle contract needs one validator-clean way to register a
primary plan and initialize `workflow_state.planned_work` while preserving the
plan and workflow write boundaries.

Safe resolution requires the owning lifecycle specification and validator to
choose and test one of these contract-level patterns:

1. allow a primary plan in `authoring` or `review-required` without
   `planned_work`, then require workflow to initialize it before implementation
   routing; or
2. define an atomic coordinator transaction that writes the plan entry through
   the plan owner and `planned_work` through workflow ownership without an
   invalid observable intermediate state.

Plan-review does not choose or implement that upstream behavior.

## Recommendation

Blocked.

Resolve the lifecycle registration transition, rerun the plan authoring
validation, move only the plan entry to `review-required`, and rerun
plan-review.

This direct review remains isolated.
It does not edit the plan, settle the plan entry, modify `workflow_state`,
start `test-spec`, or authorize implementation.
