# Governed plan authoring

Load this reference only after the parent resolves one exact governed change with plan authority. The parent owns plan quality; this reference owns authoring registration and the existing one-time initialization exception.

Governed plan authoring is available only for v3. Historical non-v3 work never re-enters plan authoring. If plan context identifies a historical contract, stop and return the context to Workflow rather than authoring or routing.

## CLI-bound authoring

Run `rigorloop lifecycle context plan --change <change-id> --format json`. Require settled inputs, exact target or unambiguous creation path, legal authority, and no blocker. Capture the current target digest before revision.

If context returns `RL_WORKFLOW_ROUTE_REQUIRED`, do not author or mutate state. Return its route facts to workflow and resume only after context makes `record-artifact-revision` immediately available.

Write only the plan, navigation entry, and evidence containing `Artifact path`, `Artifact identity`, and `Authoring result: complete`. Creation requires an absent primary plan. Revision preserves stable intent and requires exact prior identity; changes to relied-on milestone identity, order, kind, criteria, or evidence route to governed replan or migration.

Refresh context and submit `record-artifact-revision` with the returned lifecycle revision, exact plan ID, `artifact_kind: plan`, `artifact_role: primary`, path, evidence path, `stage_authority: plan`, and prior digest for revision. The CLI derives `review-required`; never directly edit artifact lifecycle or review fields.

## Approved-plan initialization

Retain the contract's narrow authority to initialize `workflow_state.planned_work` exactly once when the approved current Delivery Review package contains the primary plan and work is absent. Set every implementation milestone to `planned`, select the first implementation milestone, set `latest_review.status: not-started` and `final_closeout.readiness: not-ready`, and bind the Delivery Review ID and plan path. Never replace existing work: plan must not replace or update existing `planned_work`; workflow owns every later `planned_work` transition. If CLI enforcement rejects this exception, stop for workflow correction.

## Result

Report authoring and CLI results, initialization state when applicable, blockers, and the v3 handoff: `delivery-review`. Do not settle or route.
