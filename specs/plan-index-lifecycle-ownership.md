# Plan Index Lifecycle Ownership

## Status
- approved

## Related proposal

- [Plan index lifecycle ownership](../docs/proposals/2026-04-20-plan-index-lifecycle-ownership.md)

## Goal and context

This spec defines the repository-visible contract for keeping `docs/plan.md` and individual plan files synchronized when an initiative changes lifecycle state.

The goal is to prevent completed, blocked, or superseded initiatives from continuing to look active after the real lifecycle decision is already known. The repository already treats `docs/plan.md` as the index of active, blocked, done, and superseded plans, but its lifecycle-closeout ownership has been too implicit. This spec makes that ownership explicit and defines when closeout must happen.

## Glossary

- `plan index`: `docs/plan.md`, the repository index of active, blocked, done, and superseded execution plans.
- `plan body`: the concrete initiative plan file under `docs/plans/`.
- `planned initiative`: work that has a concrete plan file under `docs/plans/` and an index entry in `docs/plan.md`.
- `lifecycle state`: the repository-visible initiative state recorded as `Active`, `Blocked`, `Done`, or `Superseded`.
- `lifecycle closeout`: the update that moves a planned initiative to its correct lifecycle state in both the plan index and the plan body.
- `merge-dependent done transition`: a `Done` transition where the branch is not truly complete until the PR is merged.

## Examples first

### Example E1: done transition before PR

Given a planned initiative completes all required implementation and verification work before PR creation
When the contributor prepares the review package
Then lifecycle closeout updates both `docs/plan.md` and the plan body to `Done` before the PR is opened.

### Example E2: done transition after merge

Given a planned initiative is review-ready on the branch but repository policy treats merge as the deciding event for completion
When the PR merges
Then immediate post-merge cleanup may perform lifecycle closeout, provided that it updates both the plan index and the plan body promptly.

### Example E3: blocked initiative

Given a planned initiative cannot proceed because of an unresolved dependency or decision
When maintainers decide the work is blocked
Then the plan index and the plan body move to `Blocked` as soon as that decision is made rather than waiting for PR or merge.

### Example E4: superseded initiative

Given a newer plan replaces an older active plan
When the replacement decision is made
Then the older plan moves to `Superseded` in both the plan index and the plan body as part of that replanning change.

### Example E5: learn is not lifecycle authority

Given a contributor later runs `learn` and captures retrospective lessons
When that retrospective is written
Then it may add durable lessons, but it does not own plan-index bookkeeping and does not substitute for lifecycle closeout.

## Requirements

R1. This spec applies to planned initiatives only. Fast-lane work and unplanned single-slice work MUST NOT be forced to create or update plan-index lifecycle state solely because of this spec.

R2. The repository MUST treat `docs/plan.md` as lifecycle bookkeeping for planned initiatives, not as the body of a plan.

R3. The repository MUST keep the plan index and the corresponding plan body synchronized when a planned initiative changes lifecycle state.

R3a. A planned initiative MUST appear under exactly one lifecycle section in `docs/plan.md`: `Active`, `Blocked`, `Done`, or `Superseded`.

R3b. A plan body whose lifecycle state is `Done`, `Blocked`, or `Superseded` MUST NOT still present itself as an active or in-progress initiative through status or outcome/readiness wording.

R4. Lifecycle-closeout ownership MUST be split as follows:
- `plan` creates or revises the plan file and its index entry when an initiative starts or is re-planned;
- `implement` keeps progress, decisions, discoveries, and validation notes current during execution;
- `verify` checks whether lifecycle state in the plan index and the plan body still matches reality before `branch-ready` is claimed;
- final lifecycle closeout updates both the plan index and the plan body when lifecycle state changes;
- `learn` captures durable lessons and MUST NOT be the authoritative owner of lifecycle-state bookkeeping.

R5. Final lifecycle closeout MUST update both:
- the initiative entry in `docs/plan.md`; and
- the plan file's own lifecycle surfaces, including status and any outcome or readiness wording that would otherwise keep the plan looking active.

R6. When the outcome is already known before PR, lifecycle closeout SHOULD happen before PR creation rather than being deferred.

R6a. A `Done` transition MAY be completed in immediate post-merge cleanup only when merged state is the deciding event for completion.

R6b. `Blocked` and `Superseded` transitions MUST be recorded as soon as they are decided. They MUST NOT be deferred only because no PR has been opened or merged yet.

R7. `verify` MUST NOT treat a planned initiative as `branch-ready` when stale lifecycle state remains in either the plan index or the plan body.

R7a. For this spec, stale lifecycle state includes at minimum:
- a completed initiative still listed under `## Active`;
- a blocked or superseded initiative still listed under `## Active`;
- a plan index entry moved to `Done`, `Blocked`, or `Superseded` while the plan body still presents the initiative as active or in progress;
- a plan body marked complete, blocked, or superseded while `docs/plan.md` still lists the initiative under a conflicting lifecycle section.

R8. Contributor-facing workflow guidance MUST make lifecycle ownership discoverable without requiring chat history.

R8a. At minimum, the repository's workflow summary and plan guidance MUST describe:
- that `docs/plan.md` is an index rather than a plan body;
- that `implement` owns ongoing plan-body updates during execution;
- that final lifecycle closeout owns state transitions in both the plan index and the plan body; and
- that `verify` challenges stale lifecycle state before `branch-ready`.

R9. When this rule is adopted, previously stale plan-index or plan-body lifecycle state that is already known to be wrong SHOULD be corrected as part of the migration to the clarified ownership model.

## Inputs and outputs

### Inputs

- `docs/plan.md`
- the concrete plan file under `docs/plans/`
- the workflow summary and plan guidance surfaces that tell contributors how to manage plans
- the actual initiative outcome known at closeout time

### Outputs

- a synchronized plan index entry under the correct lifecycle section
- a synchronized plan body whose status and readiness wording match that lifecycle state
- workflow guidance that makes ownership of those updates explicit

## State and invariants

- `docs/plan.md` remains an index, not the body of a plan.
- Each planned initiative has one current lifecycle state in the plan index.
- The plan body and plan index describe the same lifecycle state.
- `learn` remains retrospective and non-authoritative for lifecycle-state bookkeeping.
- Post-merge cleanup is an exception for merge-dependent `Done` transitions, not the default rule for all lifecycle changes.

## Error and boundary behavior

- If a contributor claims `branch-ready` while the plan index and plan body disagree about lifecycle state, the initiative is not ready.
- If a `Done` transition is clearly known before PR and still left under `## Active`, that is stale lifecycle state.
- If an initiative becomes `Blocked` or `Superseded`, waiting for a later merge or retrospective to update the plan state is incorrect.
- If a repository has no planned initiative for the work, this spec does not require creating one just to satisfy lifecycle-closeout rules.
- If a plan is replaced by a new plan, the old plan may remain tracked, but it must be marked `Superseded` rather than silently left `Active`.

## Compatibility and migration

- This change is compatibility-sensitive because it affects contributor-visible workflow behavior and what later work must treat as active guidance.
- Adoption SHOULD correct any already-known stale plan-index or plan-body state so the new rule starts from a truthful baseline.
- Existing plan structure does not need to be redesigned; this spec changes lifecycle ownership and timing, not the overall plan format.
- Rollback, if needed, is a reversal of the clarified ownership wording, but truthfully corrected lifecycle state SHOULD be preserved.

## Observability

- Manual review MUST be able to compare `docs/plan.md` and the corresponding plan body and determine whether lifecycle state is synchronized.
- Workflow and plan-guidance artifacts MUST make the ownership split discoverable to contributors.
- Verification results MUST name the specific lifecycle-state evidence reviewed when this rule is relevant to `branch-ready`.

## Security and privacy

- This spec MUST NOT introduce automation or workflow claims that fake merge state, CI state, or review completion.
- Lifecycle-state bookkeeping MUST remain in tracked repository artifacts rather than hidden in chat-only or host-local state.

## Performance expectations

- Lifecycle-state checks SHOULD remain lightweight manual or structural review steps that fit normal contributor closeout and verification work.
- This spec does not require new heavyweight automation or continuous background synchronization.

## Edge cases

EC1. A plan may remain `Active` during implementation even if all code is written, as long as required verification or review gates are still intentionally outstanding and completion is not yet claimed.

EC2. A plan may move to `Done` after merge when repository policy or branch protection makes merge the deciding event for completion.

EC3. A plan that is abandoned because a replacement plan exists must move to `Superseded` even if no user-visible code shipped from it.

EC4. A plan that pauses for an external dependency or product decision must move to `Blocked` without waiting for a future retrospective.

EC5. A repository MAY later automate lifecycle-state enforcement, but automation is not required by this spec and does not replace the ownership model defined here.

## Non-goals

- Replacing `docs/plan.md` with a new planning system.
- Redesigning the internal section structure of every plan file.
- Turning `learn` into a mandatory bookkeeping stage.
- Requiring post-merge cleanup for every lifecycle transition.
- Introducing large CI or script automation as part of the initial rule change.

## Acceptance criteria

- Contributors can tell from repository guidance that `docs/plan.md` is the lifecycle index and that plan bodies carry initiative detail.
- The ownership split between `plan`, `implement`, `verify`, final lifecycle closeout, and `learn` is explicit and non-conflicting.
- A completed, blocked, or superseded planned initiative does not remain under `## Active` once the real lifecycle decision is known.
- A planned initiative does not present conflicting lifecycle state between `docs/plan.md` and its plan body.
- `verify` treats stale lifecycle state as blocking `branch-ready` for planned initiatives.
- The post-merge exception is limited to merge-dependent `Done` transitions rather than becoming the default for all lifecycle changes.

## Open questions

None.

## Readiness

This spec is approved. The plan-index lifecycle ownership change is implemented and merged into the repository baseline.

No further implementation-stage action is pending for this artifact.
