<!-- Template: proposal-skeleton-v1; Skill: proposal; Template status: normative -->

# Workflow-Routed Upstream Corrections

## Owning change record

`docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

## Problem

The governed lifecycle CLI correctly rejects an authoring request when another stage owns the current workflow position, but the product has no supported operation for workflow to route a downstream-discovered correction back to an already settled upstream artifact. The same gap appears when a change accidentally registers a shared governed artifact already owned by another change: validation detects the duplicate, but no guarded operation can withdraw the invalid registration.

This creates a governance deadlock. Direct `change.yaml` editing violates the mandatory transition boundary, while the CLI exposes neither a route that authorizes the owner-stage revision nor a narrow recovery operation. The result is structurally safe rejection without a supported path to restore valid progress.

## Goals

- Let workflow request an explicit upstream correction route without giving the CLI semantic routing authority.
- Preserve the current milestone, open findings, correction reason, evidence, and deterministic return destination.
- Let the routed artifact owner register an exact revision without bypassing review or settlement.
- Prevent new cross-change artifact-path collisions before mutation.
- Provide a narrow guarded withdrawal for an existing duplicate registration when another change is the artifact's exact canonical owner.
- Return short actionable diagnostics that distinguish immediate operations from operations available after workflow routing.
- Keep skills focused on semantic work rather than lifecycle field-editing procedure.

## Non-goals

- No generic `set-stage`, `reopen`, `force`, arbitrary field setter, or blocker bypass.
- No automatic choice of correction destination, semantic resolution, finding closure, artifact settlement, or workflow continuation.
- No cross-repository transaction or hosted authorization service.
- No automatic modification of the semantic artifact whose registration is withdrawn.
- No weakening of stale-revision, evidence-freshness, review, milestone, or authority checks.
- No requirement that portable skill use create governed lifecycle state.

## Vision fit

fits the current vision

The change makes blocked work resumable from durable repository evidence without relying on chat memory or unsupported YAML edits. It strengthens the traceability chain while preserving human and workflow ownership of semantic decisions.

## Context

The first governed lifecycle CLI release intentionally assigns workflow routing to the workflow layer and mechanical mutation validation to the CLI. That separation remains correct. The missing capability is a semantic transaction through which workflow records its already-made route decision and the CLI verifies that the route is legal.

The current observability change demonstrates both failure modes. Code review found an upstream proof-contract gap while M1 findings remained open, so `test-spec` authoring was rejected. Repository validation also found that the change registered `docs/architecture/system/architecture.md` even though its owning pointer and canonical registration belong to the governed lifecycle CLI change. Both rejections are useful; neither currently provides an authorized corrective operation.

## Options Considered

### Option 1: Permit direct lifecycle edits during correction

This is operationally simple but recreates the unsupported transition problem the CLI exists to prevent. It cannot guarantee stale-operation protection, exact ownership, deterministic diffs, or atomic validation.

Rejected.

### Option 2: Let authoring commands ignore workflow blockers

This would make revisions easy but would let any settled upstream artifact reopen without a durable route, reason, return destination, or workflow authority. Open findings and milestone state could become detached from the correction.

Rejected.

### Option 3: Add workflow-requested correction routing and narrow registration withdrawal

Workflow supplies the exact source, destination, reason, evidence, preserved milestone, and return destination. The CLI validates the closed transition, records it atomically, and then admits only the destination owner's normal revision operation. A separate narrow withdrawal operation repairs only a provable cross-change duplicate registration and never edits semantic content.

Recommended.

## Recommended Direction

Add two operation-oriented capabilities to the governed lifecycle CLI.

First, a workflow-authorized correction-route operation records an exact route from the current downstream stage to one upstream owner stage. The request identifies the current lifecycle revision, source stage and occurrence, destination artifact and stage, reason code, evidence path, preserved finding IDs and milestone, and return stage. The CLI validates this supplied decision against a closed route matrix; it does not select a destination. The route makes the destination owner's `record-artifact-revision` operation structurally available while preserving open findings and downstream state.

Second, an artifact-registration withdrawal operation removes only the selected change's registration and matching derived review or validation registrations when repository evidence proves that the same normalized artifact path has exactly one different canonical owning change. It requires exact current identities, an evidence record, and stage or workflow authority. It must refuse unique artifacts, ambiguous ownership, semantic file deletion, or arbitrary entry removal.

Registration of a new artifact must also scan supported change records and reject a normalized path already owned by another governed change before mutation.

The CLI should report a stable route-required diagnostic containing current stage, requested stage, route owner, blocking findings, and the operation available after routing. Human output remains short; structured output carries exact identities and evidence paths.

## Expected Behavior Changes

- A `test-spec` revision requested while workflow remains at `review-resolution` is rejected with a route-required diagnostic instead of a generic or internally rendered blocker.
- Workflow can record a legal correction route without closing findings, completing a milestone, or settling the destination artifact.
- After routing, only the exact destination owner can register the artifact revision.
- The revised artifact requires its normal same-stage peer review before workflow may return to the recorded destination.
- A stale, arbitrary, mismatched, or unsupported correction route is rejected atomically.
- New cross-change artifact-path collisions are rejected before registration.
- An existing provable duplicate registration can be withdrawn without deleting or rewriting the shared artifact.
- Context output distinguishes `permitted_operations` from `available_after_workflow_route`.

## Architecture Impact

This changes the public lifecycle operation schema, transition engine, effective-state interpreter, repository discovery boundary, transaction validation, and workflow integration. It therefore requires architecture assessment and likely an ADR amendment to the governed lifecycle CLI transaction boundary.

The durable route should remain in `change.yaml` because a fresh checkout must reconstruct the suspended downstream state and return destination. It is snapshot coordination state, not a hidden queue or autonomous runner.

## Testing and Verification Strategy

Proof should cover:

- downstream review-resolution to architecture, spec, plan, or test-spec correction routes admitted only by the closed matrix;
- preserved milestone, finding set, source occurrence, reason, evidence, and return stage;
- stale revision, wrong source, unknown destination, unknown reason, ambiguous target, and illegal forward-route rejection;
- authoring blocked before routing and admitted only for the exact routed destination afterward;
- review required before return and return rejected while destination evidence is stale or unsettled;
- identical route retry and conflicting replay behavior;
- cross-change normalized-path collision rejection during registration;
- exact duplicate withdrawal, unique-owner refusal, ambiguous-owner refusal, semantic-file preservation, and derived-registration cleanup;
- atomicity and post-validation recovery for both mutations;
- concise human and JSON diagnostic equivalence;
- unchanged portable mode and unrelated lifecycle operations.

The observability change that exposed the defect should become an integration fixture after this capability is implemented, without importing its entire branch as the feature's unit-test basis.

## Rollout and Rollback

Ship the new operations additively behind a repository/CLI compatibility check. Update workflow integration before published skills rely on correction routing. Existing repositories remain readable, and no migration is required until they record a correction route.

Collision prevention and guarded withdrawal ship together: prevention stops new duplicates, while withdrawal supplies the supported recovery path for already invalid registrations. Use the withdrawal operation once per proven duplicate, then keep collision prevention enabled for all new registrations. Rollback disables new route creation and withdrawal while preserving already recorded routes as readable blocked state; a compatibility release must resolve active routes before removing their schema.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| The CLI becomes the routing decision-maker | Require workflow to supply the exact route and validate only a closed transition matrix. |
| Correction routing becomes a generic reopen escape hatch | Require downstream evidence, exact destination ownership, preserved findings, and a recorded return stage. |
| Open findings disappear during upstream work | Preserve their IDs and resolution state; routing never closes or reclassifies them. |
| Withdrawal deletes meaningful history | Remove only the invalid registration and derived registrations; retain review records, evidence, and the semantic artifact. |
| Repository-wide discovery is expensive or ambiguous | Scan only supported change records, normalize paths deterministically, and fail closed on ambiguous ownership. |
| Skills regain large lifecycle procedures | Keep detailed mechanics in CLI/workflow contracts and give skills only context/request/handoff instructions. |
| Active old clients cannot understand correction state | Gate mutation by schema/CLI compatibility and keep read diagnostics actionable. |

## Open Questions

The specification should settle the exact public command names, route reason vocabulary, allowed source/destination matrix, return readiness rules, and whether withdrawal is represented as its own operation or one closed named repair condition. None of these questions changes the selected authority boundary.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-25 | Preserve workflow as route decision owner. | The CLI should enforce, not choose, semantic workflow direction. | CLI-selected automatic rerouting |
| 2026-08-25 | Require a durable correction return record. | Suspended downstream work must be resumable from a fresh checkout. | Chat-only or agent-local return context |
| 2026-08-25 | Add cross-change collision prevention and narrow withdrawal. | Detection without a guarded recovery path leaves invalid branches permanently blocked. | Direct YAML repair or generic artifact deletion |
| 2026-08-25 | Keep findings and milestone state open during correction. | Upstream revision is evidence toward resolution, not review closure. | Closing findings when routing begins |

## Next Artifacts

1. Independent proposal review.
2. Feature specification and spec review.
3. Architecture assessment and architecture/ADR update with independent review.
4. Execution plan and plan review.
5. Test specification and independent test-spec review.
6. Guarded implementation, code review, explanation, and verification.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent `proposal-review`. The direction and authority split are selected; exact schemas and transition matrices belong to specification and architecture.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Revise a test spec when downstream review discovers a proof gap | in scope | Recommended Direction, Expected Behavior Changes |
| Keep workflow as the routing owner | in scope | Recommended Direction |
| Avoid adding settlement mechanics to skills | in scope | Goals, Risks and Mitigations |
| Preserve open findings without blocking authorized correction | in scope | Recommended Direction, Risks and Mitigations |
| Improve short, actionable CLI diagnostics | in scope | Recommended Direction, Expected Behavior Changes |
| Address the current duplicate architecture registration blocker | in scope | Recommended Direction, Rollout and Rollback |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Workflow-requested upstream correction route | core to this proposal | It removes the authoring deadlock without transferring route decisions to the CLI. |
| Durable return context and preserved findings/milestone | same-slice dependency | A route is unsafe and non-resumable without them. |
| Route-required diagnostics | same-slice dependency | Callers need the authorized next action rather than a generic rejection. |
| Cross-change path-collision prevention | same-slice dependency | It prevents recurrence of the current registration defect. |
| Narrow duplicate-registration withdrawal | same-slice dependency | Detection without the guarded recovery path would leave existing invalid branches blocked. |
| Published skill text reduction | separate implementation slice | Skills consume the operation but should not duplicate its mechanics. |
| Repair of the active observability change | separate implementation slice | It should consume the shipped capability after this contract is approved. |
| Generic workflow engine or arbitrary lifecycle editor | out of scope | It would violate the selected product boundary. |
