# Governed lifecycle routing

## Load condition

Read this procedure only when authoritative CLI context establishes a valid current governed change that must be interpreted, audited, resumed, settled, or mutated, or after a successful automation bootstrap requires reclassification. It owns canonical lifecycle applicability and transitions. It does not own automation commands.

## Governed identity and evidence

Require exact change identity from `rigorloop workflow-context --change <change-id>`. Require `stage-owned-change-local-v3` for every current route and reject non-v3 progression. Historical records remain readable without mutation authority. Treat the returned lifecycle revision as stale after any mutation or observed identity drift and refresh the complete change-phase context before another dependent action.

For every new governed change, create v3 without requiring another parameter. Do not migrate prior-contract records in place; read-only historical inspection never creates or changes lifecycle state.

Use CLI-projected artifact settlement, active plan identity, stage-owned evidence, review resolution, workflow-owned transition receipts, blockers, and permitted operations as the deterministic routing basis. File existence alone is not settlement. Stop on missing, stale, mismatched, contradictory, or illegal evidence. Do not reconstruct deterministic facts from repository prose or guessed paths.

## Mutation boundary

Update only `workflow_state`, the selected `workflow.automation` target state, and workflow-owned transition evidence; preserve `artifact_states` and all stage-owned evidence. Keep `workflow_state` to lifecycle state, current and next stage, blockers, evidence pointers, and `planned_work` only when a primary plan exists.

Plan owns only the one-time deterministic initialization of missing primary-plan `planned_work`; route owns every later `planned_work` decision and uses the stable `stage_authority: workflow` protocol token for the mutation. Accept plan's initialization without rewriting it. Stop on failed available change-metadata validation instead of repairing another stage's state.

Use the lifecycle CLI for governed correction coordination. When an upstream authoring context returns `RL_WORKFLOW_ROUTE_REQUIRED`, route may write exact route evidence and request `route-correction`; it supplies the source, earlier destination and artifact, closed reason, current finding IDs, return stage, and active milestone. After the revised artifact receives an exact approving review and settlement, write the CLI-requested return evidence and request `return-correction`. For a provable duplicate architecture or ADR registration, write exact ownership evidence and request `withdraw-artifact-registration`. Never emulate these operations by editing lifecycle fields, and never ask a stage skill to choose the route, settle another stage, or withdraw ownership.

## Canonical applicability

Architecture and specification are both mandatory design-package members. Route architecture authoring before specification finalization, then reconcile both artifacts before `design-review`.

Stage transitions and settlement are owned here. A stage advances only from the evidence its owner is permitted to write. Authoring skills write their own governed artifact and authoring transition. Review skills write formal review evidence and matching settlement. Route interprets those surfaces and chooses the next structurally permitted transition.

## Review and milestone routing

Material findings require durable recording. A material non-approval routes to correction or owner decision according to the finding; `needs-decision` keeps closeout open. Closed review resolution requires final dispositions, validation evidence, and no open findings.

For milestone plans:

1. Select the unique current implementation milestone.
2. Require its prior prerequisites and implementation authority.
3. After implementation, route to milestone-local code review.
4. A clean non-final milestone review closes only that milestone and selects the next in-scope milestone.
5. A non-clean result follows the recorded review-resolution route and must be rereviewed when required.
6. Final-closeout readiness requires no open implementation milestone and no required open review resolution.

Use `lifecycle-closeout` for milestones or sections that track downstream gates without adding implementation scope.

## Final holistic review and closeout

Milestone-local review is not final holistic review. Before `verify`, require final holistic code-review evidence for the complete final diff and cross-milestone interactions.

After final holistic review is clean, route triggered CI maintenance and then current v3 directly to `verify`, which generates the final explanation only on success. Historical contracts select no route. Verification failure returns a blocker and route sends it to the exact owner; it does not silently authorize Verify repair. `verify` may establish branch readiness. `pr` remains a separate boundary.

## Dependency contract

Automation asks this governed lifecycle procedure for the next valid lifecycle transition. Automation must not redefine stage order, architecture applicability, settlement, milestone completion, final holistic-review applicability, or closeout.
