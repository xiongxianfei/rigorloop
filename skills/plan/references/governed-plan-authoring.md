# Governed plan authoring

Load this reference only after the parent resolves one exact governed change with plan authority. The parent owns plan quality; this reference owns authoring registration and the existing one-time initialization exception.

## CLI-bound authoring

Run `rigorloop lifecycle context plan --change <change-id> --format json`. Require settled inputs, exact target or unambiguous creation path, legal authority, and no blocker. Capture the current target digest before revision.

Write only the plan, navigation entry, and evidence containing `Artifact path`, `Artifact identity`, and `Authoring result: complete`. Creation requires an absent primary plan. Revision preserves stable intent and requires exact prior identity; changes to relied-on milestone identity, order, kind, criteria, or evidence route to governed replan or migration.

Refresh context and submit `record-artifact-revision` with the returned lifecycle revision, exact plan ID, `artifact_kind: plan`, `artifact_role: primary`, path, evidence path, `stage_authority: plan`, and prior digest for revision. The CLI derives `review-required`; never directly edit artifact lifecycle or review fields.

## Approved-plan initialization

Retain the contract's narrow authority to initialize `workflow_state.planned_work` exactly once when a current clean plan review requires it and work is absent. Set every implementation milestone to `planned`, select the first implementation milestone, set `latest_review.status: not-started` and `final_closeout.readiness: not-ready`, bind the exact review and plan revision, and report `settlement-retry-required`. Never replace existing work: plan must not replace or update existing `planned_work`; workflow owns every later `planned_work` transition. If CLI enforcement or repository compatibility rejects this exception, stop for workflow migration.

## Result

Report authoring and CLI results, initialization state when applicable, blockers, and `plan-review` handoff. Do not settle or route.
