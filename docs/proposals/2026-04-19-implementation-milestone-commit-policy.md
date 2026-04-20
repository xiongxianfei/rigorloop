# Implementation Milestone Commit Policy

## Status
- accepted

## Problem

RigorLoop already emphasizes milestone-based implementation, validation, and plan updates, but it does not yet state the commit boundary for a completed milestone. That leaves two costly failure modes:

- contributors accumulate large uncommitted changes across multiple milestones;
- contributors infer that every milestone should become its own pull request even when the milestone is not independently merge-safe.

Without a clear policy, milestone sequencing becomes harder to review, harder to roll back, and harder to explain from plan progress through verification evidence.

## Goals

- Define the default relationship between milestones, commits, and pull requests.
- Keep each completed milestone in a trustworthy branch state.
- Preserve small, reviewable history without forcing a separate PR for every milestone.
- Give future workflow and implement specs a clear policy to encode.

## Non-goals

- Requiring every milestone to become its own PR.
- Prescribing a universal commit-message format for every commit in the repository.
- Forcing stacked PRs or draft PRs for every multi-milestone change.
- Replacing existing review gates, verification, or plan-update requirements.

## Context

- The current workflow spec treats `implement`, `verify`, and `pr` as enforced stages, and it treats `plan` as the sequencing artifact for multi-step work.
- `AGENTS.md` already says milestone work should update plan progress, decisions, discoveries, and validation notes as work proceeds.
- The repository does not yet define whether a milestone should end in a commit, when a milestone should become a PR boundary, or how to treat milestones that are complete but not yet independently safe to merge.
- The user direction is explicit: commit after every completed milestone, but do not require a PR after every milestone.

## Options considered

### Option 1: Commit only at the end of the whole change

- Advantages:
  - Lowest process overhead while work is in progress.
  - Fewer intermediate commits to manage.
- Disadvantages:
  - Large uncommitted diffs are harder to review, recover, or explain.
  - Milestone progress and validation evidence become less trustworthy.
  - Rollback becomes coarse and branch state becomes harder to audit.

### Option 2: Require both a commit and a PR for every completed milestone

- Advantages:
  - Maximum review granularity.
  - Each milestone can be discussed and merged independently.
- Disadvantages:
  - Over-splits changes that are not independently useful or safe.
  - Encourages PRs with scaffolding or partial behavior that is confusing alone.
  - Adds too much ceremony for normal multi-milestone implementation work.

### Option 3: Require a commit after every completed milestone, but make PR boundaries conditional

- Advantages:
  - Preserves trustworthy milestone boundaries in git history.
  - Keeps PR scope coherent when multiple milestones belong to one review story.
  - Supports single-PR, draft-PR, or stacked-PR tactics without changing the core rule.
- Disadvantages:
  - Requires contributors to distinguish commit boundaries from review boundaries.
  - Still depends on plan quality so milestones are defined coherently.

### Option 4: Leave commit and PR timing to contributor discretion

- Advantages:
  - Maximum flexibility.
  - No new workflow policy to learn.
- Disadvantages:
  - Leaves the current ambiguity unresolved.
  - Makes milestone-based planning less meaningful because "done" has no consistent branch boundary.
  - Produces inconsistent reviewability across contributors and changes.

## Recommended direction

Choose Option 3.

RigorLoop should treat a completed planned milestone as a commit boundary, not automatically as a PR boundary. The core rule is simple: every completed planned milestone ends in a commit, and a PR contains one or more completed milestones. A milestone should become its own PR only when it is independently reviewable, verified, and safe to merge.

This direction preserves the important invariant: each completed planned milestone leaves the branch in a trustworthy state. It also avoids forcing reviewers to consume incomplete scaffolding as a standalone PR when the real review unit is a larger coherent change.

This policy applies to planned milestone work, meaning work governed by a concrete plan that defines one or more explicit milestones. Fast-lane changes and other unplanned single-slice changes do not require milestone-formatted commits unless a concrete plan explicitly introduces milestone boundaries.

The expected contributor practice is:

- finish the milestone deliverable;
- run targeted tests and relevant validation;
- update plan progress and validation evidence;
- record any milestone-level decision changes;
- commit the coherent milestone diff using a standardized milestone subject such as `M1: add skill validation fixtures`;
- either continue the same PR or open/update a PR if the milestone is independently reviewable.

The first-release plan template should also include a milestone closeout checklist so contributors explicitly capture validation, plan progress, decision updates when needed, and the milestone commit before moving on.

Draft PRs and stacked PRs should remain available tactics, not mandatory boundaries.

## Expected behavior changes

- Planned milestone work will no longer be allowed to drift through long uncommitted stretches once a milestone is complete.
- Execution plans and milestone definitions will need to produce coherent commit-sized deliverables rather than only end-state goals.
- A single PR may legitimately contain multiple milestone commits.
- Review guidance will distinguish between commit boundaries and PR boundaries.
- Contributors may open a draft PR after the first verified milestone, but they will not be required to open a separate PR for every milestone.

## Architecture impact

This change affects workflow policy rather than application runtime architecture.

- Primary components affected:
  - `specs/rigorloop-workflow.md`
  - the future test spec for the workflow contract
  - `docs/workflows.md`
  - implementation guidance, including the `implement` skill
  - plan templates or plan-review guidance where milestone closure expectations are described
- Expected boundary decisions:
  - milestone completion versus PR readiness
  - commit policy versus optional PR strategy
  - mandatory milestone evidence versus optional draft-PR tactics

## Testing and verification strategy

- Review the workflow spec and related guidance for consistent milestone terminology.
- Add or update examples showing:
  - one change with multiple milestone commits in a single PR;
  - one milestone that is independently reviewable and becomes its own PR.
- Verify that plan and workflow guidance both require milestone progress and validation updates before the milestone commit.
- Ensure the resulting contract is testable as documentation and artifact presence, not dependent on hidden chat behavior.

## Rollout and rollback

Roll this in as a workflow-contract update before implementation guidance or automation starts to depend on the older ambiguous behavior.

- Update the workflow spec first.
- Then align workflow docs, plan guidance, and implement guidance.
- Keep PR strategy flexible so the change tightens trust without forcing a new contribution model.
- Standardized milestone commits guarantee traceability during branch and pull-request review, but repositories that squash or heavily rewrite history may not preserve those milestone boundaries after merge.

Rollback is straightforward:

- remove the milestone-commit requirement from the workflow spec;
- return commit timing to contributor discretion or broader plan guidance.

## Risks and mitigations

- Risk: contributors interpret the policy as "open a PR after every milestone."
  - Mitigation: state explicitly that PR boundaries are conditional and may contain multiple completed milestones.
- Risk: contributors create milestone commits that are still broken or unverified.
  - Mitigation: tie milestone completion to targeted validation, updated plan progress, and coherent diff boundaries.
- Risk: milestone definitions stay too vague to support coherent commit boundaries.
  - Mitigation: align plan and plan-review guidance so milestones represent understandable, verifiable units of progress.
- Risk: the project drifts into commit-message prescription instead of workflow clarity.
  - Mitigation: standardize only milestone closeout commits, not every commit contributors may create while working locally.

## Open questions

- None for the core policy. The remaining work is to encode these decisions in the workflow spec, planning template, and implementation guidance.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-19 | Treat a completed planned milestone as a commit boundary. | This keeps milestone progress reviewable, revertible, and auditable in git history during branch and pull-request review. | Waiting until the end of the whole change leaves too much uncommitted risk. |
| 2026-04-19 | Do not require every milestone to become its own PR. | PR boundaries should reflect reviewable and merge-safe units, not every internal step. | One-PR-per-milestone would over-fragment normal multi-step work. |
| 2026-04-19 | Allow single-PR, draft-PR, and stacked-PR tactics under the same core policy. | Contributors need flexibility without losing the invariant that completed milestones are committed. | Hardcoding one PR strategy would add ceremony without improving trust for every change. |
| 2026-04-19 | Standardize milestone closeout commit subjects as `M<n>: <completed milestone outcome>`. | This makes milestone boundaries visible in git history without prescribing every commit contributors may create. | Leaving milestone commit wording fully ad hoc would weaken reviewability and traceability. |
| 2026-04-19 | Add an explicit milestone closeout checklist to the plan template. | This makes milestone completion concrete and repeatable instead of relying on contributors to remember the closeout steps from memory. | Depending only on cross-reference to the workflow spec would be easier to miss during implementation. |

## Follow-on artifacts

- `specs/rigorloop-workflow.md`
- `specs/rigorloop-workflow.test.md`
- `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
- `docs/plans/0000-00-00-example-plan.md`

## Readiness

Proposal review is complete. This proposal was accepted and its milestone policy now lives in the merged workflow baseline.

No further proposal-stage action is pending for this artifact.
