# Plan Lifecycle Closeout

This topic is curated learn guidance. Authoritative lifecycle rules remain in `docs/workflows.md`, `specs/rigorloop-workflow.md`, `CONSTITUTION.md`, and the active plan artifacts.

## 2026-05-05: Reduce Merge-Dependent Plan States

- Source session: `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
- Primary classification: `durable-lesson`
- Secondary routes: candidate workflow or validator follow-up, not yet routed

Post-merge plan closeout is easy to miss because it happens after the PR already feels complete. Prefer moving implementation plans to Done before opening the PR when implementation, review-resolution, verification, explain-change, and PR handoff are complete.

Use merge-dependent Done only when the merge itself is the deciding completion event. When that exception is needed, create a tracked closeout obligation before opening the PR. The follow-up should name the owner, PR number, files to update, expected lifecycle wording, and validation command.

If this keeps recurring, the next improvement should be automated detection: report an Active plan entry or active plan body that references a PR GitHub already reports as merged.

