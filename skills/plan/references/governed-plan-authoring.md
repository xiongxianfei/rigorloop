# Governed plan authoring

Load this reference only after the parent resolves one exact governed `stage-owned-change-local-v1` change with plan-owned authority. It owns only the three governed operations.

## Change-record authoring transition

For every operation, read the complete `change.yaml` before writing. Require `lifecycle_contract: stage-owned-change-local-v1` and resolve authority by artifact ID, `kind`, and normalized `path`. For creation, create only that entry with a unique stable ID. For creation or revision, use `authoring`, remove any prior `review`, set `authoring_evidence`, and finish at `review-required`. Preserve every other entry. Stop on failed available change-metadata validation.

## Create primary plan

Use `create-primary-plan` only when the canonical file and primary entry are absent; no prior identity is required. Resolve one deterministic path, reject conflicts or multiple candidates, write the plan and navigation, register artifact ID, kind `plan`, role `primary`, and normalized path, and leave `planned_work` absent. File-entry asymmetry stops.

## Revise primary plan

Use `revise-primary-plan` only for one canonical file and matching entry in a legal authoring state. Revise stable content and return it to `review-required` without changing `planned_work`. Later changes to settled milestone identity, order, kind, criteria, or evidence require governed replan or migration. Stop on asymmetry, stale identity, illegal state, or ambiguity.

## Initialize approved plan

Use `initialize-approved-plan` only for a `review-required` primary plan with absent work, a current clean review of the exact revision, no later edit, contradictory review, or open resolution, and valid ordered milestones.

Plan may initialize `workflow_state.planned_work` exactly once. Record review ID, round, record path, reviewed artifact path, and repository revision as `initialization_basis`; set every implementation milestone to `planned`; select the first implementation milestone; list all remaining milestones; set `latest_review.status: not-started` and `final_closeout.readiness: not-ready`. Write no other lifecycle or sibling field. Plan must not replace or update existing `planned_work`; workflow owns every later `planned_work` transition.

Report `settlement-retry-required`; workflow may coordinate the identical settlement retry, but plan does not settle or route.

## Retry and recovery

An identical request with matching basis and state is an idempotent no-op. Mismatched work, stale review, open resolution, invalid milestones, validation failure, or write conflict stops without repair.

Plan-review records judgment first. With absent work, clean review leaves `review-required` and reports `initialization-required`. After matching initialization, an identical retry reuses that judgment and alone may activate the plan. Preserve review evidence after failure.

## Historical compatibility

Write stable intent only. Historical and portable plans remain readable. For active governed history, read intent from the plan and state from `change.yaml`. Never reverse-synchronize, infer missing work from prose, or repair conflicts; route them to workflow migration or governed replan.

## Write boundary

Plan may write the plan, navigation, authoring evidence, matching transition, and one initialization. It must not write review judgment, settlement, later work transitions, routing, automation, implementation, verification, or PR state. Unknown operations, missing procedure, or failed complete-state validation block without partial mutation.
