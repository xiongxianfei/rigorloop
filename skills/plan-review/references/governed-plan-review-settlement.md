# Governed plan-review settlement

Load only for `governed_plan_candidate_context`. `SKILL.md` owns judgment and handoff; this reference owns validation and transactions.

## Candidate validation

read the complete `change.yaml`; require `lifecycle_contract: stage-owned-change-local-v1` and one matching primary plan entry. Identity uses review ID, round, record and artifact paths, and repository revision or commit—never a new hash. Classify `validated-governed-plan-entry` or `invalid-governed-candidate`; invalid evidence stops without mutation or fallback.

## Operation state

Require `review-required` and complete authoring evidence for `initial-review`, plus absent `planned_work` and no exact clean review. Thereafter use `settlement-retry`; it must not perform semantic rereview or duplicate evidence. Changed identity requires fresh review. Multiple bases, open resolution, orphaned `planned_work`, mismatch, unknown, or contradiction fails closed.

## Initial-review mapping

Write the durable review record first with `id`, `artifact_id`, `outcome`, `record`, and `round`; preserve unrelated state.

- `approved`: keep `review-required`; return `initialization-required` without test-spec eligibility.
- Map `changes-requested` to `revision-required`; record details.
- `blocked`: after recording, map only the entry and transaction to `blocked`.
- Map `blocked` or `inconclusive` to `blocked`; keep an inconclusive entry `review-required`.
- recording failure: leave state unchanged; return `not-settled` with paths and corrective action.

Plan-review must not initialize or mutate `planned_work`, edit the plan, advance routing, or authorize implementation.

## Settlement retry

- Absent `planned_work`: reuse approval, keep `review-required`, return `initialization-required`, create nothing.
- Matching initialization and `review-required`: settle only the matching plan entry by mapping `approved` to `active`; return `settled-active`, report test-spec eligibility, and preserve authoring, review, and initialization evidence.
- Already matching `active`: return `settled-active` and `state_changed: false`; write nothing.
- Invalid, stale, ambiguous, or conflicting state: return `blocked` unchanged and route to its owner.

## Retry and recovery

Validate the record and identities, then perform at most one compare-and-set. Retry identical incomplete settlement without rerunning the review. Preserve basis evidence. Conflict or failed available change-metadata validation stops without advancing routing.

## Workflow-managed review

Workflow-managed execution requires matching authority, fresh context, and a Phase 1 manifest. Automation, settlement, and continuation authority remain separate. Report eligibility without routing.
