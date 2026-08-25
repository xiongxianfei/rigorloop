# Governed lifecycle routing

## Load condition

Read this procedure only when a valid current governed change record must be interpreted, audited, resumed, settled, or mutated, or after a successful automation bootstrap requires reclassification. It owns canonical lifecycle applicability and transitions. It does not own automation commands or workflow-guide authoring.

## Governed identity and evidence

Require the exact change identity and a readable `docs/changes/<change-id>/change.yaml`; read the complete `change.yaml` before state-changing routing. Require `lifecycle_contract: stage-owned-change-local-v1` for mutation.

For every new governed change, create `lifecycle_contract: stage-owned-change-local-v1` without requiring another parameter. Before the first mutation of resumed nonterminal historical work, migrate the record once; read-only historical inspection never creates the marker.

Derive routing only from current artifact settlement, the active plan identity, stage-owned evidence, review resolution, and workflow-owned transition receipts. File existence alone is not settlement. Stop on missing, stale, mismatched, contradictory, or illegal evidence, including failed available change-metadata validation.

## Mutation boundary

Update only `workflow_state`, the selected `workflow.automation` target state, and workflow-owned transition evidence; preserve `artifact_states` and all stage-owned evidence. Keep `workflow_state` to lifecycle state, current and next stage, blockers, evidence pointers, and `planned_work` only when a primary plan exists.

Plan owns only the one-time deterministic initialization of missing primary-plan `planned_work`; workflow owns every later `planned_work` transition. Accept plan's initialization without rewriting it. Stop on failed available change-metadata validation instead of repairing another stage's state.

Use the lifecycle CLI for governed correction coordination. When an upstream authoring context returns `RL_WORKFLOW_ROUTE_REQUIRED`, workflow may write exact route evidence and request `route-correction`; it supplies the source, earlier destination and artifact, closed reason, current finding IDs, return stage, and active milestone. After the revised artifact receives an exact approving review and settlement, write the CLI-requested return evidence and request `return-correction`. For a provable duplicate architecture or ADR registration, write exact ownership evidence and request `withdraw-artifact-registration`. Never emulate these operations by editing lifecycle fields, and never ask a stage skill to choose the route, settle another stage, or withdraw ownership.

## Canonical applicability

Architecture-assessment applicability and routing are owned here. After approved recorded `spec-review`, record exactly one assessment: `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`.

- `architecture-required` routes through architecture authoring and review.
- `architecture-not-required` skips those stages.
- `architecture-ambiguous` pauses for owner resolution.
- A requested conditional target that is not applicable stops as `target-not-applicable`; it is not silently treated as reached.

Stage transitions and settlement are owned here. A stage advances only from the evidence its owner is permitted to write. Authoring skills write their own governed artifact and authoring transition. Review skills write formal review evidence and matching settlement. Workflow reads those surfaces and performs the next transition.

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

Milestone-local review is not final holistic review. Before `explain-change` or `verify`, require final holistic code-review evidence for the complete final diff and cross-milestone interactions.

After final holistic review is clean, route triggered CI maintenance, then `explain-change`, then `verify`. Verification failure returns a blocker; it does not silently authorize repair. `verify` may establish branch readiness. `pr` remains a separate boundary.

## Dependency contract

Automation asks this governed lifecycle procedure for the next valid lifecycle transition. Automation must not redefine stage order, architecture applicability, settlement, milestone completion, final holistic-review applicability, or closeout.

Guide authoring may render these established rules into project documentation but does not own or change them.
