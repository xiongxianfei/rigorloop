# Plan Lifecycle Closeout

This topic is curated learn guidance. Authoritative lifecycle rules remain in `docs/workflows.md`, `specs/rigorloop-workflow.md`, `CONSTITUTION.md`, and the active plan artifacts.

## 2026-05-05: Reduce Merge-Dependent Plan States

- Source session: `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
- Primary classification: `durable-lesson`
- Secondary routes: candidate workflow or validator follow-up, not yet routed

Post-merge plan closeout is easy to miss because it happens after the PR already feels complete. Move implementation plans to Done inside the PR that performs the lifecycle transition, before the PR opens for review, when implementation, review-resolution, verification, explain-change, and PR handoff are complete.

If completion depends on a true downstream event, such as release, deploy, package publication, external migration, or an observed hosted result, keep the plan Active and name that event or follow-up condition. Do not use merge itself as a routine downstream completion event.

If this keeps recurring, the next improvement should be automated detection: report an Active plan entry or active plan body whose tracked state conflicts with the PR-contained evidence or a named downstream completion event.
