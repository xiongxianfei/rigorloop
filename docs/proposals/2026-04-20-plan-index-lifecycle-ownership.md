# Plan index lifecycle ownership

- Status: accepted

## Problem

`docs/plan.md` is the repository index of active, blocked, done, and superseded execution plans, but its lifecycle ownership is currently too implicit.

In practice, the repository just finished a full initiative, merged the PR, and still left the first-release plan listed under `## Active`. That stale index entry later created review confusion for the constitution migration, because reviewers had to treat the older completed plan as live guidance until the index was corrected.

The workflow currently makes plan creation and plan-body updates clear enough, but it does not make final plan-index closeout explicit enough. That leaves a gap after implementation and PR work, especially when users do not trigger `plan` again once the real work is already finished.

## Goals

- Make `docs/plan.md` reliably reflect real initiative lifecycle state.
- Keep the plan file's own lifecycle state synchronized with `docs/plan.md` when an initiative moves between `Active`, `Blocked`, `Done`, and `Superseded`.
- Define clear ownership boundaries between the plan body and the plan index.
- Prevent merged or completed initiatives from staying under `## Active`.
- Make stale plan-index state visible during review and verification instead of discovering it later by accident.
- Keep the rule simple enough that agents can follow it during normal workflow closeout.

## Non-goals

- Redesign the structure of plan files or replace `docs/plan.md` with a new system.
- Introduce a large plan-management automation layer in this change.
- Change how milestone progress, decisions, or validation notes are recorded inside plan bodies.
- Turn `learn` into general repository bookkeeping.

## Context

- `docs/plan.md` is already documented as an index, not a plan body, in `AGENTS.md` and `docs/workflows.md`.
- Current practice already implies a split:
  - `implement` updates the active plan body during execution;
  - `verify` checks whether the plan still matches reality;
  - `pr` prepares the final review package.
- What is still missing is an explicit rule for when an initiative changes lifecycle state:
  - active to done
  - active to blocked
  - active to superseded
- The recent first-release work exposed the gap directly: the work was complete and merged, but `docs/plan.md` still treated that plan as active.
- This also affects future governance work, because active-plan indexing influences what later changes must treat as live guidance.

## Options considered

### Option 1. Keep the current implicit ownership

Leave the current behavior mostly as-is and rely on contributors to remember to update `docs/plan.md` when appropriate.

- Pros:
  - no workflow change
  - no extra rules to learn
- Cons:
  - already failed in practice
  - stale active-plan state becomes visible only much later
  - encourages plan-index updates to fall between `implement`, `verify`, and `pr`

### Option 2. Make `learn` the owner of plan-index closeout

Treat post-merge reflection as the stage that updates `docs/plan.md` and closes plans.

- Pros:
  - happens after the final outcome is known
  - keeps closeout near retrospective thinking
- Cons:
  - `learn` is optional and advice-oriented, not guaranteed for every initiative
  - lifecycle bookkeeping is operational state, not retrospective insight
  - would still leave stale index entries whenever no `learn` stage runs

### Option 3. Make final closeout own the plan index

Keep plan-body ownership during execution with `implement`, but require the final closeout stage, usually `pr` or immediate post-merge cleanup, to update `docs/plan.md` when initiative lifecycle state changes. Make `verify` responsible for flagging stale index state before PR readiness.

- Pros:
  - matches the real lifecycle moment when state changes
  - fits the existing workflow better than adding a new bookkeeping stage
  - gives `verify` a concrete drift check to enforce
  - keeps `learn` focused on lessons rather than operational cleanup
- Cons:
  - requires explicit workflow/spec wording so contributors do not assume `plan` owns everything
  - may still need a small follow-up rule for post-merge cases when a PR closes without updating the index

### Option 4. Add full automation for plan-index state transitions

Build scripts or CI automation that infer initiative status and update or enforce `docs/plan.md`.

- Pros:
  - stronger consistency in the long term
  - reduces human forgetfulness
- Cons:
  - more complexity than the current problem requires
  - hard to infer lifecycle state from git/PR state alone without project-specific rules
  - risks adding automation before the ownership model is stable

## Recommended direction

Choose Option 3.

The repository should treat `docs/plan.md` as lifecycle bookkeeping owned by final closeout, not by retrospective learning and not only by the original `plan` stage. The clean split is:

- `plan`: create or revise the plan file and index entry when an initiative starts or is re-planned
- `implement`: keep the plan body accurate during execution
- `verify`: flag drift when `docs/plan.md` does not match actual initiative state
- `pr` or immediate post-merge closeout: move the initiative between `Active`, `Blocked`, `Done`, or `Superseded`
- `learn`: capture durable lessons, not plan-index bookkeeping

Final closeout MUST update both `docs/plan.md` and the plan file's own lifecycle state, including status and any outcome/readiness wording that would otherwise keep the plan looking active.

This is the smallest rule change that closes the real gap the repository just hit.

## Expected behavior changes

- Completed initiatives will no longer remain under `## Active` after merge or equivalent closeout.
- Completed initiatives will no longer leave plan files marked in-progress or PR-pending after the initiative is actually closed.
- `docs/plan.md` will become a more trustworthy source for identifying current active guidance.
- Contributors will treat plan-body updates and plan-index updates as related but different responsibilities.
- Verification and review will have an explicit reason to challenge stale plan-index state before PR readiness.

## Architecture impact

This is primarily a workflow and documentation-governance change.

Likely affected artifact types:

- workflow contract in `specs/`
- workflow summary in `docs/workflows.md`
- governance guidance in `AGENTS.md` and the constitution surface
- plan template or plan guidance if closeout expectations need to be more explicit
- verification expectations if stale `docs/plan.md` state becomes a named review or verify check

No runtime architecture, product behavior, or data-flow change is expected.

## Testing and verification strategy

Likely proof surfaces:

- manual review that the workflow and governance docs assign ownership clearly
- test-spec coverage for:
  - plan-index and plan-body state staying synchronized during done, blocked, and superseded transitions
  - completed plans moving out of `## Active`
  - blocked and superseded transitions
  - `verify` catching stale plan-index state
  - `learn` remaining optional and non-authoritative for plan-index bookkeeping
- example-plan and workflow-summary review to confirm contributors can discover the rule without reading chat history

## Rollout and rollback

Rollout:

- update the governing workflow/guidance artifacts to define lifecycle ownership for `docs/plan.md`
- align the example plan or plan guidance if needed
- default to updating lifecycle state before PR when the outcome is already known; allow immediate post-merge cleanup only when merge state is the deciding event
- apply the clarified rule to currently stale plan-index state

Rollback:

- revert the documentation/spec change if the ownership model proves confusing or too rigid
- preserve corrected plan-index state where it reflects reality, even if wording changes later

## Risks and mitigations

- Risk: ownership becomes split across too many stages and stays confusing.
  - Mitigation: define one simple rule set with `implement` for plan body, `pr` for lifecycle closeout, and `verify` for drift detection.
- Risk: contributors assume merged PRs always update `docs/plan.md` in the same branch.
  - Mitigation: allow immediate post-merge closeout when necessary, but still make it mandatory operational cleanup.
- Risk: `learn` is still used informally for bookkeeping and reintroduces ambiguity.
  - Mitigation: explicitly state that `learn` captures lessons, not lifecycle state transitions.
- Risk: later automation is added before the ownership rule is stable.
  - Mitigation: treat automation as a follow-on option, not part of the initial proposal.

## Open questions

- Should the normative lifecycle-closeout rule live primarily in `specs/rigorloop-workflow.md`, in the constitution surface, or in both?
- Should the repository require the plan-index move to happen before PR creation, or allow immediate post-merge cleanup when the merged state is only known afterward?
- Should `verify` fail hard on stale `docs/plan.md` state, or treat it as a named concern that blocks PR readiness?

## Decision log

- 2026-04-20: Rejected keeping ownership implicit. Reason: the repository already experienced stale active-plan state after a completed and merged initiative.
- 2026-04-20: Rejected making `learn` the owner. Reason: `learn` is optional and retrospective, while `docs/plan.md` is operational lifecycle state.
- 2026-04-20: Chose final-closeout ownership with `verify` drift detection as the leading direction. Reason: it matches the real lifecycle transition point with the smallest process change.
- 2026-04-20: Deferred automation. Reason: automation is easier to design after the ownership model is explicit and stable.

## Follow-on artifacts

- `specs/plan-index-lifecycle-ownership.md`
- `specs/plan-index-lifecycle-ownership.test.md`
- `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
- `docs/explain/2026-04-20-plan-index-lifecycle-ownership.md`

## Readiness

Proposal review is complete. The accepted direction is now carried by `specs/plan-index-lifecycle-ownership.md` and `docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`.

No further proposal-stage action is pending for this artifact.
