# Plan Lifecycle Closeout

This topic is curated learn guidance. Authoritative lifecycle rules remain in `docs/workflows.md`, `specs/rigorloop-workflow.md`, `CONSTITUTION.md`, and the active plan artifacts.

## 2026-05-05: Reduce Merge-Dependent Plan States

- Source session: `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
- Primary classification: `durable-lesson`
- Secondary routes: candidate workflow or validator follow-up, not yet routed

Post-merge plan closeout is easy to miss because it happens after the PR already feels complete. Move implementation plans to Done inside the PR that performs the lifecycle transition, before the PR opens for review, when implementation, review-resolution, verification, explain-change, and PR handoff are complete.

If completion depends on a true downstream event, such as release, deploy, package publication, external migration, or an observed hosted result, keep the plan Active and name that event or follow-up condition. Do not use merge itself as a routine downstream completion event.

If this keeps recurring, the next improvement should be automated detection: report an Active plan entry or active plan body whose tracked state conflicts with the PR-contained evidence or a named downstream completion event.

## 2026-05-07: Separate Verify Handoff From Final Plan Completion

- Source session: `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
- Primary classification: `durable-lesson`
- Secondary routes: candidate plan-template or workflow wording follow-up, not yet routed

`Ready for verify` is a next-gate statement, not a Done state and not PR readiness. It is valid only after the planned implementation milestones are complete, review-resolution is closed when triggered, and code-review has been conducted.

The plan may remain Active after that point while downstream lifecycle gates remain: `verify`, `explain-change`, PR handoff, and final Done transition. To avoid ambiguity, pair the readiness line with remaining gates, for example:

```text
Readiness: Ready for verify.
Remaining completion gates: verify, explain-change, PR handoff, then Done if no true downstream event remains.
```

If a final milestone includes verification and PR handoff, treat it as lifecycle closeout or split it from implementation milestones. Do not use `Ready for verify` while an implementation milestone is still unfinished.
