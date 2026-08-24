# Governed plan-review settlement

Load only for `governed_plan_candidate_context`. The parent owns judgment and handoff; this reference owns CLI recording and settlement.

Require one matching governed primary plan, exact review identity, `review-required`, complete authoring evidence, and absent `planned_work` for `initial-review`. Changed identity requires fresh review; ambiguity, open resolution, orphaned work, or contradiction blocks. A later `settlement-retry` must not perform semantic rereview or duplicate evidence.

After writing the review and log, run `rigorloop lifecycle context plan-review --change <change-id> --format json` and submit `record-review` with its lifecycle revision, exact plan ID, review path, and `stage_authority: plan-review`. Plan-review must not initialize or mutate `planned_work`, edit the plan, route, or authorize implementation.

Approved review with absent work returns `initialization-required`. After exact one-time initialization, refresh context and submit `settle-artifact` with `stage_authority: plan-review`; preserve authoring, review, and initialization evidence and report test-spec eligibility. Matching active state or `already-recorded` is `settled-active` with `state_changed: false`. Any CLI rejection stops unchanged without direct repair.

Workflow-managed execution requires matching authority, fresh context, and a Phase 1 manifest. Automation, settlement, and continuation authority remain separate. It records phase evidence and returns control without routing.
