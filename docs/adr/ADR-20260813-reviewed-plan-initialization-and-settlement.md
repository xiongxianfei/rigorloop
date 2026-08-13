# ADR-20260813: Reviewed Plan Initialization and Settlement

## Owning change record

`docs/changes/2026-08-12-plan-skill-simplification/change.yaml`

## Context

ADR-20260729 assigns `plan` the one-time initialization of missing primary-plan `planned_work` when the plan is first registered. That ordering creates live execution state before plan-review can request changes to milestone identity, order, kind, completion criteria, or required evidence. Because `plan` may not replace existing `planned_work`, an ordinary review revision could leave the stable plan and live state inconsistent.

The approved plan-skill simplification spec requires one mutable state owner, plan-owned initial derivation, review-owned judgment and settlement, workflow-owned routing, deterministic interruption recovery, read-old/write-new compatibility, and no governed-document hashes.

## Decision

Amend the initialization order to an evidence-initialization-settlement transaction:

1. Plan authoring registers or revises the stable primary plan and leaves its entry `review-required` without `planned_work`.
2. Plan-review records a clean review for the exact current repository revision but does not settle the plan to `active`; it reports `initialization-required`.
3. Workflow-managed execution invokes the plan-owned `initialize-approved-plan` operation. An isolated review stops after reporting the required action.
4. Plan validates the stable artifact tuple, exact reviewed revision, current clean review record, no later edit or contradictory review, closed resolution state, stable milestone definitions, and absent `planned_work`. It writes only the missing initial projection.
5. Workflow invokes the identical plan-review settlement retry. Plan-review reuses the recorded judgment and moves only the plan entry to `active`.
6. Workflow may route onward only after both initialization and settlement succeed.

Stable artifact identity is artifact ID, kind `plan`, role `primary`, and normalized path. Reviewed revision identity is review ID, round, review record path, reviewed artifact path, and reviewed repository revision or commit. No governed-document hash or `content_identity` field is introduced.

Legal temporary states are authoring, revision-required, or blocked without `planned_work`; review-required before review; review-required with clean current review and missing `planned_work`; review-required with clean current review and matching initialized `planned_work`; and active with matching settled review and `planned_work`. Every other combination fails closed.

New plan writers emit stable intent only. Historical plan structures remain readable, but governed current milestone state comes only from `change.yaml`. Active legacy work with missing or conflicting authoritative state requires explicit workflow-owned migration. Existing `planned_work` is never silently replaced, repaired, or reverse-synchronized into plan prose.

This ADR narrowly supersedes ADR-20260729 only for the timing and legal-state invariant of initial primary-plan `planned_work` creation. It retains ADR-20260729 for sole state ownership, stage-owned writes, workflow routing, evidence-first review, idempotent settlement, no hashes, and external-action boundaries.

## Alternatives considered

### Initialize before review

Rejected because review-driven milestone changes can diverge from immutable live state.

### Let plan-review initialize state while settling

Rejected because it widens review authority into plan-owned derivation and `workflow_state` mutation.

### Let workflow derive planned work

Rejected because workflow would become a second owner of plan semantics rather than a coordinator.

### Add a content hash

Rejected because existing stable artifact metadata plus durable reviewed-revision evidence is sufficient and the governing architecture intentionally avoids document hashes.

### Permit plan to replace initialized work after review

Rejected because replacement weakens one-time initialization, risks losing execution progress, and blurs replan ownership.

## Consequences

- Plan-review approval becomes two-phase for a new or revised primary baseline: judgment evidence first and settlement after plan-owned initialization.
- The lifecycle validator must permit the two review-required temporary states and reject early routing or invalid combinations.
- Workflow coordinates two existing stage owners but does not create a verdict or derive milestones.
- Interrupted initialization or settlement can resume idempotently from durable evidence.
- Direct isolated plan review remains isolated and reports the pending initialization action.
- The feature spec, skills, validators, parsers, fixtures, migration proof, and generated packages must change atomically.
- Historical plans remain readable without rewriting or regaining current-state authority.

## Follow-up

- Amend the stage-owned lifecycle feature spec and matching test spec.
- Update the `plan`, `plan-review`, and `workflow` skill contracts and lifecycle validators.
- Add read-old/write-new migration fixtures and package-parity proof.
- Run architecture-review before execution planning.
