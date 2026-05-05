# PR-Self-Contained Lifecycle Completion

## Status

- accepted

## Problem

The current workflow allows plans to defer their `Active` to `Done` transition until after PR merge when the merge is treated as the deciding event. That creates a recurring failure mode: the PR merges, attention shifts to the next task, and no one performs the deferred closeout. `docs/plan.md` and the concrete plan body can then remain stale on `main`.

The closeout rule already exists. The weak point is the timing. Post-merge cleanup depends on memory after the work already feels complete, which makes the routine obligation structurally easy to miss.

The same shape appears in similar repo-local lifecycle cases: an artifact can sometimes defer a status, closeout, or readiness update even though the PR already contains the change that makes the update true. When the state can be true in the PR tree, deferring it to post-merge creates stale shared state for no real benefit.

## Goals

- Make every PR self-consistent: repo-tracked lifecycle claims in the PR tree are true as of that tree.
- Eliminate routine post-merge cleanup for plan completion and analogous repo-local lifecycle updates.
- Keep `docs/plan.md` and concrete plan bodies moving together when plan lifecycle state changes.
- Apply the same principle by analogy to lifecycle-managed proposals, specs, test specs, architecture documents, ADRs, review-resolution closeout, and other tracked readiness or closeout artifacts when the deciding evidence is already inside the PR.
- Preserve truly downstream completion events such as deploys, releases, and external system changes as downstream work.
- Defer merge-SHA recording rules entirely until a real case needs immutable merge metadata.
- Make merge a mechanical integration of pre-validated state rather than the trigger for ordinary repo bookkeeping.

## Non-goals

- Replacing post-merge automation for events that genuinely happen outside the PR tree.
- Forbidding follow-up work.
- Treating unmerged PR branches as authoritative shared state.
- Redesigning plan structure, artifact status vocabulary, or the whole lifecycle model.
- Building a broad project-management system around plans.
- Implementing release, deploy, or external-system completion automation in this proposal.
- Defining a merge-SHA recording exception before there is a real case that needs it.

## Vision fit

fits the current vision

This proposal reinforces RigorLoop's Git-first reviewability promise. It keeps lifecycle state in tracked files that reviewers can inspect before merge, and it reduces reliance on chat memory or after-the-fact cleanup.

## Context

`CONSTITUTION.md` requires durable artifacts, explicit source-of-truth rules, and lifecycle-managed status inside tracked artifacts. It also says final lifecycle closeout for planned initiatives updates both `docs/plan.md` and the plan body, and that `verify` treats stale lifecycle state between them as blocking PR readiness.

`specs/rigorloop-workflow.md` currently says:

- `R8g`: lifecycle state changes update both `docs/plan.md` and the plan body;
- `R8h`: a `Done` transition should happen before PR creation when the outcome is already known, but a merge-dependent `Done` transition may happen in immediate post-merge cleanup when merged state decides completion;
- `R8k` and related artifact-lifecycle rules keep proposal, spec, test-spec, architecture, and ADR status inside the artifact.

`docs/workflows.md` mirrors the same plan lifecycle guidance. A recent learn topic, `docs/learn/topics/plan-lifecycle-closeout.md`, records that post-merge plan closeout is easy to miss and recommends reducing merge-dependent plan states. The recurring failure is not that contributors lack a reminder; it is that the workflow permits ordinary bookkeeping to happen after the salient review event has passed.

## Options considered

### Option 1: Keep merge-dependent Done with better reminders

This preserves the current rule and adds guidance, learn topics, or PR comments reminding contributors to close plans after merge.

It is low-effort, but it keeps the same failure mode. The task still depends on someone remembering to act after the PR feels finished.

### Option 2: Build post-merge automation to perform closeout

Automation could detect merged PRs, update `docs/plan.md`, patch plan bodies, and open follow-up PRs or commits.

This may be useful as a backstop, but it is a heavier solution to a smaller problem. It also has to infer whether a plan is truly complete, whether rollout happened, and what exact wording should change.

### Option 3: Use retroactive drift detection only

A validator on `main` could report active plans that reference merged PRs or other stale lifecycle signs.

This improves visibility but still allows stale state to land first. It catches drift after shared state is already wrong.

### Option 4: Require PR-self-contained lifecycle completion

Plan lifecycle transitions, and analogous repo-local artifact closeouts, happen in the PR that makes the transition true. If completion depends on a later deploy, release, external action, or other downstream event, the artifact stays active and a later PR or automation records completion then.

This moves routine lifecycle truth into reviewable Git state and removes post-merge memory as a required workflow step.

## Recommended direction

Choose Option 4.

Replace the current merge-dependent `Done` exception with a PR-self-contained lifecycle rule:

When a PR performs the work that makes a repo-local lifecycle state true, the PR records that state before it opens for review. For planned initiatives, `docs/plan.md` and the concrete plan body move together in the same PR.

The targeted constitution wording should be:

> Synchronization happens within the PR that performs the lifecycle transition, before the PR opens for review. The merge of a PR is a fast-forward of pre-validated state, not a trigger for further lifecycle changes.

For plans, this means:

- complete at PR time: close the plan to `Done` inside the PR;
- complete at a downstream event: keep the plan `Active` until that event happens, then use a later PR or automation to record the transition;
- blocked or superseded: record the transition as soon as that state is decided, as the current workflow already requires.

Apply the same rule by analogy to similar repo-local lifecycle cases:

- artifact status changes for proposals, specs, test specs, architecture documents, and ADRs;
- `review-resolution.md` closeout when all material findings are actually resolved by the PR;
- active test-spec, verify, explain-change, or change-local readiness wording that would otherwise describe the branch as incomplete after the PR has completed its own scope;
- superseded, archived, abandoned, or deprecated states when the replacing or terminal condition is already present in the PR.

The analogy is bounded. It applies only when the deciding evidence is inside the PR tree or already known before the PR opens for review. It does not apply to genuinely downstream events such as deploys, releases, package publication, external migrations, or hosted checks that have not actually been observed.

Do not specify a merge-SHA recording exception in this change. If a future case genuinely needs immutable merge metadata in a lifecycle artifact, that case should propose the narrow rule then.

## Expected behavior changes

- Plans completed by a PR are moved to `Done` in both `docs/plan.md` and their plan body before the PR opens for review.
- Plans that depend on deploy, release, external migration, or another downstream event remain `Active` and name that event as the next completion condition.
- Top-level lifecycle artifacts stop deferring status or terminal-state updates when the PR already contains the change that makes the update true.
- Review and verification can evaluate lifecycle state from the PR's file tree instead of relying on a promised post-merge cleanup.
- Merge-dependent wording such as "after merge," "post-merge," or "once this lands" becomes reviewer-visible evidence that the author must classify as either a true downstream event or stale lifecycle wording.

## Architecture impact

This is a workflow-governance change, not a runtime architecture change.

Expected affected surfaces:

- `specs/rigorloop-workflow.md`, especially `R8g`, `R8h`, and artifact-lifecycle analogues around `R8k`;
- `docs/workflows.md` planned milestone and artifact lifecycle summaries;
- `CONSTITUTION.md`, with a minimal targeted wording change that makes PR-contained synchronization a governance rule;
- `AGENTS.md` only if its concise guidance conflicts after the constitution and workflow spec change;
- validation scripts that inspect artifact lifecycle consistency, including broader lifecycle artifact inconsistency beyond plan-index/body disagreement;
- GitHub Actions only as a thin caller of repository-owned validation scripts.

No application runtime, generated adapter package layout, release packaging, or external deployment flow is expected to change.

## Testing and verification strategy

The follow-on spec and test spec should cover:

- `docs/plan.md` and a plan body's `Status:` disagreeing inside a PR;
- a completed plan still listed under `## Active`;
- a plan closed to `Done` in the PR that completes implementation, review-resolution, verification, explain-change, and PR handoff;
- a plan remaining `Active` because completion depends on a real downstream event;
- top-level lifecycle artifacts whose status or closeout wording conflicts with the PR tree;
- `review-resolution.md` claiming `Closeout status: open` after all material findings are resolved, or claiming `closed` without required evidence;
- merge-dependent language detection in tracked files at first, including plans and change-local artifacts.

Validation should be repository-owned. The first implementation slice should make broader lifecycle artifact inconsistency blocking, not only plan-index/body disagreement. CI should call the same validator scripts rather than duplicating lifecycle rules in workflow YAML.

## Rollout and rollback

Rollout:

- update the workflow spec to remove the routine merge-dependent `Done` exception and encode the PR-self-contained rule;
- update `CONSTITUTION.md` with the targeted synchronization wording;
- update `docs/workflows.md` and any concise guidance that mentions post-merge plan closeout;
- add or extend validation for plan-index and plan-body agreement plus broader lifecycle artifact inconsistency;
- add a non-blocking warning for merge-dependent language in tracked files that requires reviewer classification;
- perform a one-time migration for any currently active plans or artifacts whose state is stale under the new rule.

Rollback:

- revert the workflow-spec and documentation changes if the rule proves too rigid;
- keep any lifecycle corrections that accurately reflect repository state;
- keep retroactive drift detection as a backstop if it proves useful independently.

## Risks and mitigations

- Risk: contributors mark a plan `Done` in a PR that never merges.
  Mitigation: unmerged branches do not change shared `main`; the inaccurate claim remains isolated to the abandoned branch.

- Risk: contributors conflate "merged" with "rolled out" and close plans too early.
  Mitigation: the rule explicitly distinguishes PR-contained completion from downstream events such as deploy, release, publication, and external migration.

- Risk: the analogy to other lifecycle artifacts becomes too broad.
  Mitigation: scope the analogy to repo-local lifecycle state whose deciding evidence is inside the PR tree or already known before the PR opens for review.

- Risk: language warnings become noisy.
  Mitigation: make merge-dependent wording a visible reviewer attention flag first, not an immediate blocker.

- Risk: existing plans with merge-dependent language create migration churn.
  Mitigation: handle existing stale states in a one-time cleanup PR and apply the new rule prospectively after adoption.

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-05 | Recommend PR-self-contained lifecycle completion as the proposal direction. | It removes the recurring post-merge memory dependency and makes PRs self-consistent before review and merge. | Better reminders; post-merge closeout automation as the primary fix; retroactive drift detection alone. |
| 2026-05-05 | Apply the rule by analogy to similar repo-local lifecycle cases. | Plan closeout is one instance of the broader issue: tracked lifecycle state should be true in the PR tree when the PR already contains the deciding evidence. | Treating plan completion as a special-only rule; broad automation before the policy is settled. |
| 2026-05-05 | Include broader lifecycle artifact inconsistency in the first blocking validation slice. | The analogous stale-state problem is not limited to plan-index/body disagreement. | Limit first enforcement to plans only. |
| 2026-05-05 | Inspect tracked files only for merge-dependent language warnings at first. | This keeps the first warning mechanism repository-local and avoids coupling it to hosted PR metadata. | Inspect PR descriptions through hosted CI event metadata in the first slice. |
| 2026-05-05 | Update `CONSTITUTION.md` with minimal targeted wording. | The constitution is the top repository governance surface and should not silently retain a weaker merge-triggered lifecycle model. | Leave the constitution unchanged and rely only on the workflow spec. |
| 2026-05-05 | Defer merge-SHA recording rules entirely. | No current case requires immutable merge metadata, so specifying an exception now would over-design the policy. | Reserve a merge-SHA exception in this proposal. |

## Follow-on artifacts

- `proposal-review`: approved with no material findings.
- `spec`: [RigorLoop Workflow](../../specs/rigorloop-workflow.md) PR-self-contained lifecycle completion amendment.
- `spec-review`: approved with no material findings and one minor non-blocking note for test-spec classification-recording detail.
- `plan`: [PR-Self-Contained Lifecycle Completion Plan](../plans/2026-05-05-pr-self-contained-lifecycle-completion.md).
- `plan-review`: approved with no material findings.
- `test-spec`: [RigorLoop workflow test spec](../../specs/rigorloop-workflow.test.md) updated with PR-self-contained lifecycle completion coverage.
- `implementation`: M1 through M4 complete.
- `review-resolution`: material M2 code-review finding accepted, fixed, and closed.
- `verify`: completed for PR handoff after PR-mode selected validation and broad smoke.
- `explain-change`: completed in `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md`.
- `pr`: PR #30 opened for human review.

## Readiness

Accepted and implemented. The approved workflow spec amendment, test-spec coverage, execution plan, review closeout, verification evidence, explain-change, and PR handoff are complete; PR #30 is open for human review.
