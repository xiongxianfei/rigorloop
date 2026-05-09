# Single Source of Workflow State

## Status

accepted

## Problem

RigorLoop now has one standard workflow and the final closeout order is:

```text
explain-change -> verify -> pr
```

However, implementation and review work is still interrupted by stale or contradictory state across multiple artifacts.

The recurring issue is not the workflow order itself. The issue is duplicated current-state wording.

Several artifacts can independently describe:

* current milestone
* next stage
* review status
* review-resolution status
* verify readiness
* PR readiness
* plan lifecycle status

When one artifact is updated and another is not, later reviews correctly find contradictions. This causes repeated review findings, extra correction rounds, and uncertainty about which artifact should be trusted.

Recent learn sessions identified the same pattern:

* `Current Handoff Summary` and `Readiness` can disagree about the next stage.
* implementation fixes can update only part of the required state surface.
* milestones can be described as finished while related closeout, review-resolution, or commit evidence remains incomplete.
* generated or copied guidance can amplify stale canonical wording.

The repository needs a simpler state ownership model.

## Goals

* Define one primary owner for each workflow state fact.
* Make the active plan’s `Current Handoff Summary` the single live state block for planned initiatives.
* Prevent `Readiness`, `Progress`, `review-resolution.md`, `change.yaml`, and `explain-change.md` from duplicating live next-stage claims.
* Require state synchronization at every stage transition.
* Reduce review interruptions caused by stale or contradictory state text.
* Keep the policy simple enough for agents and contributors to apply.
* Preserve the existing one-standard-workflow model.
* Preserve `explain-change -> verify -> pr` final closeout order.
* Avoid adding heavy semantic validators in the first implementation slice.

## Non-goals

* Do not redesign the workflow stage order.
* Do not reintroduce a fast lane or small-change lane.
* Do not add a new lifecycle stage.
* Do not make every artifact carry a full workflow-state table.
* Do not turn `change.yaml` into a long-form state tracker.
* Do not make `review-resolution.md` own plan readiness.
* Do not make `verify` own PR readiness.
* Do not add a broad semantic validator in the first slice.
* Do not migrate historical plans that are not active, touched, or relied on.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop’s Git-first reviewability by making workflow state easier to find, update, and audit. It reduces process noise by assigning each state fact one primary owner and making other artifacts link or summarize rather than restate live state.

## Context

RigorLoop already uses one standard workflow and has moved durable explanation before final verification. The remaining problem is state duplication.

Recent evidence shows three recurring drift patterns:

1. **Plan readiness drift**

   The active plan’s `Current Handoff Summary` may say one thing while `Readiness` still points to an older stage.

2. **Review-fix handoff drift**

   A review finding may require synchronizing the active plan, change metadata, review-resolution, validation notes, and readiness, but implementation updates only some of those surfaces.

3. **Milestone closeout confusion**

   A milestone may be described as finished while closeout evidence, review-resolution, or commit evidence is still incomplete.

These are not separate workflow-design problems. They are symptoms of the same root cause: too many files record the same live state.

## Options considered

### Option 1: Keep current state recording behavior

Advantages:

* No immediate workflow or artifact changes.
* Contributors can write state wherever convenient.
* No new validation or guidance needed.

Disadvantages:

* Continues stale readiness and next-stage contradictions.
* Makes reviews spend time detecting state drift.
* Leaves agents uncertain about which artifact is authoritative.
* Encourages every artifact to restate current state.

### Option 2: Add more validation without changing state ownership

Advantages:

* Could catch some contradictions automatically.
* Avoids changing artifact guidance.

Disadvantages:

* Validators would need to infer which duplicated state is correct.
* Semantic plan-state validation is likely brittle.
* Does not fix the underlying problem that state is duplicated.

### Option 3: Define single-source workflow state ownership

Advantages:

* Makes each state fact have one primary owner.
* Reduces duplicated next-stage wording.
* Makes stage transitions easier to audit.
* Keeps the workflow simple and readable.
* Allows lightweight static checks before adding heavier validators.

Disadvantages:

* Requires updating plans, skills, and workflow guidance.
* Requires contributors to stop writing live state in multiple places.
* Some existing artifacts may need cleanup when touched.

## Recommended direction

Choose Option 3.

RigorLoop should define one primary owner for each workflow state fact.

The active plan owns current workflow state for planned initiatives through a single live section:

```md
## Current Handoff Summary

- Current milestone:
- Current milestone state:
- Last reviewed milestone:
- Review status:
- Remaining in-scope implementation milestones:
- Next stage:
- Verify readiness:
- Reason verify is or is not ready:
```

Other plan sections should not duplicate live next-stage claims.

Instead:

* `Progress` records dated history.
* `Decision log` records decisions.
* `Validation notes` records evidence.
* `Readiness` points to `Current Handoff Summary`.
* `Outcome / Retrospective` is final-only or explicitly historical.

## State ownership matrix

| State fact                          | Primary owner                                      | Other surfaces may do                                   |
| ----------------------------------- | -------------------------------------------------- | ------------------------------------------------------- |
| Current workflow guide              | `docs/workflows.md`                                | Link or summarize.                                      |
| Current planned-initiative handoff  | active plan `Current Handoff Summary`              | Link or cite.                                           |
| Milestone state                     | active plan milestone table / current handoff      | Summarize only.                                         |
| Review event evidence               | `docs/changes/<change-id>/reviews/<stage>-r<n>.md` | Link only.                                              |
| Review finding disposition          | `review-resolution.md`                             | Summarize count/status only.                            |
| Review event index                  | `review-log.md`                                    | N/A.                                                    |
| Change metadata                     | `change.yaml`                                      | Store compact status and pointers, not live next stage. |
| Final change rationale              | `explain-change.md`                                | PR body summarizes.                                     |
| Final validation / branch readiness | `verify` output or verify report                   | PR body summarizes.                                     |
| PR readiness                        | PR body / PR stage                                 | Do not back-propagate into plan except final closeout.  |
| Plan lifecycle status               | active plan and `docs/plan.md` index               | Other files should not invent lifecycle status.         |

## Current Handoff Summary rule

For active milestone-based plans, `Current Handoff Summary` is the only authoritative live state block.

Other sections must not independently state the next stage unless they are historical notes.

Recommended `Readiness` section:

```md
## Readiness

See `Current Handoff Summary`.

This plan is not Done until final closeout is complete.
```

## Stage transition state-sync rule

Every stage transition that changes workflow state must perform a state-sync check.

Minimum checklist:

```md
## State sync checklist

- [ ] Active plan `Current Handoff Summary` updated.
- [ ] Current milestone state updated.
- [ ] `review-resolution.md` closeout status updated, if findings exist.
- [ ] `review-log.md` open findings updated, if review records changed.
- [ ] `change.yaml` review/status summary updated, if change metadata changed.
- [ ] `docs/plan.md` index updated, if plan lifecycle status changed.
- [ ] No stale next-stage wording remains in touched artifacts.
```

## Milestone state rule

Use one milestone state field.

Allowed states:

```text
planned
implementing
review-requested
resolution-needed
closed
```

State transitions:

```text
planned -> implementing
implementing -> review-requested
review-requested -> closed, when review is clean and no review-resolution is required
review-requested -> resolution-needed, when findings require review-resolution or fixes
resolution-needed -> review-requested, when fixes need re-review
resolution-needed -> closed, when findings are dispositioned and no re-review is required
```

Do not use `implementation-complete` or `review-clean` as milestone state values. They may appear as evidence descriptions, not state values.

## Next-stage wording rule

Only these surfaces should make live next-stage claims:

* active plan `Current Handoff Summary`
* current skill result
* workflow skill routing result
* PR body at PR handoff

Other artifacts should avoid live next-stage claims.

Examples:

* `review-resolution.md` owns closeout status, not next stage.
* `change.yaml` owns compact metadata, not next stage.
* `explain-change.md` owns final rationale, not branch readiness.
* `verify` owns validation proof, not PR body readiness.

## Plan closeout rule

Plans should move to `done` inside the PR when the workflow lifecycle is complete:

```text
implementation milestones closed
review-resolution closed when triggered
explain-change complete
verify complete
pr handoff complete
```

A plan remains `active` only when a true downstream event remains, such as:

* release
* deploy
* package publication
* external migration
* observed hosted result

Merge itself should not be the normal plan-completion event.

## Skill impact

### `plan`

The `plan` skill should:

* create and maintain `Current Handoff Summary`
* make `Readiness` point to the summary
* avoid duplicating live next-stage state in multiple plan sections
* require state-sync checks when stage transitions occur

### `implement`

The `implement` skill should:

* set the milestone state to `review-requested`
* update progress and validation notes
* not claim milestone closed
* not claim verify readiness
* not claim review passed

### `code-review`

The `code-review` skill should:

* transition `review-requested -> closed` for clean reviews
* transition `review-requested -> resolution-needed` when findings exist
* require same-milestone review-resolution before continuing
* hand off to the next implementation milestone when one remains
* hand off to final closeout only when no implementation milestone remains

### `review-resolution`

Review-resolution guidance should:

* keep findings attached to the reviewed milestone
* update closeout status
* require state-sync before continuing

### `verify`

The `verify` skill should check:

* all in-scope implementation milestones are closed
* required review-resolution is closed
* explain-change exists and is current
* final validation evidence is recorded

## Public skill surface

Published skills should not expose RigorLoop repository-internal details.

Use portable language such as:

```text
project workflow guide
local workflow contract, if present
project validation command
active plan
change metadata
```

Avoid public skill references to RigorLoop-only internal paths, validator scripts, generated adapter internals, or local examples.

## Expected behavior changes

* Active plans have one live current-state block.
* `Readiness` no longer duplicates next-stage wording.
* `change.yaml` summarizes status and links to owners instead of carrying next-stage state.
* `review-resolution.md` owns finding disposition, not plan readiness.
* `explain-change.md` owns rationale, not validation proof.
* `verify` owns final validation proof, not PR readiness.
* Stage transitions become less error-prone because state-sync is explicit.
* Review interruptions from stale state should decrease.

## Architecture impact

This is a workflow and artifact-governance change, not a runtime architecture change.

Likely touched surfaces:

* `docs/workflows.md`
* `skills/workflow/SKILL.md`
* `skills/plan/SKILL.md`
* `skills/implement/SKILL.md`
* `skills/code-review/SKILL.md`
* `skills/verify/SKILL.md`
* review-resolution guidance, wherever currently located
* `AGENTS.md`, if it summarizes workflow state ownership
* generated public skill/adapters, when canonical skill wording changes

No service boundary, storage layer, API, deployment, or packaging architecture is expected to change.

## Testing and verification strategy

First implementation should use guidance and static wording checks only.

Do not add semantic plan-state validation in the first slice.

Focused checks should prove:

* skills describe `Current Handoff Summary` as the live state owner
* `Readiness` guidance points to the summary instead of duplicating next stage
* `implement` does not claim verify readiness or review success
* `code-review` contains milestone-aware state transitions
* `verify` checks explain-change before final verification
* public skills do not expose RigorLoop-internal paths
* generated skill/adapters are in sync after canonical skill changes

Suggested validation:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
git diff --check --
```

If change metadata or review artifacts are touched, also run the corresponding metadata and review-artifact checks.

## Rollout

1. Proposal-review confirms state ownership model.
2. Spec or workflow guidance update defines state ownership and current-handoff summary rules.
3. Plan skill updates current-handoff and readiness guidance.
4. Implement/code-review/verify skill updates align ownership claims.
5. Public skill boundary checks are updated if needed.
6. Generated outputs are regenerated from canonical skills.
7. Static validation and targeted checks run.
8. Code-review verifies that stale state claims no longer appear in touched surfaces.

## Rollback

If the model proves too strict, rollback by restoring previous skill wording and workflow summary guidance.

Already-written `Current Handoff Summary` sections remain valid plan history. They do not need migration unless they are contradicted by the restored policy.

## Risks and mitigations

| Risk                                                       | Mitigation                                                                               |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Contributors forget to update the current handoff summary. | Add state-sync checklist to plan, implement, code-review, and verify guidance.           |
| `Readiness` sections become too terse.                     | Allow `Readiness` to link to `Current Handoff Summary` and state final closeout caveats. |
| `change.yaml` loses useful state.                          | Keep compact review/status fields and links to owners.                                   |
| Static checks become brittle.                              | Use positive required wording and small incident-based forbidden phrases only.           |
| Historical plans remain inconsistent.                      | Do not migrate old plans unless active, touched, or relied on.                           |
| Agents still restate next-stage in many artifacts.         | Add “next-stage wording rule” to workflow and skill guidance.                            |

## Open questions

None.

## Decision log

| Date       | Decision                                                                                     | Reason                                                                              |
| ---------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 2026-05-09 | Drafted single-source workflow state proposal.                                               | Repeated review interruptions were caused by state duplication, not workflow order. |
| 2026-05-09 | Chose active plan `Current Handoff Summary` as the live state owner for planned initiatives. | It is the most natural place to record milestone state and next handoff.            |
| 2026-05-09 | Chose guidance/static checks for first implementation.                                       | Semantic state validation is too brittle before the artifact model stabilizes.      |

## Next artifacts

* proposal-review (completed)
* focused workflow/spec update (started)
* skill updates for plan, implement, code-review, verify, and workflow
* generated output refresh after canonical skill updates
* explain-change and verify after implementation

## Follow-on artifacts

- Spec: `specs/single-source-of-workflow-state.md`

## Readiness

Accepted after proposal-review R2. `specs/single-source-of-workflow-state.md` is authored for the next review gate.

The proposal resolves the main direction: write current state once, make the active plan own current handoff, let other artifacts link or summarize, and require state synchronization at every workflow transition.

## Core invariant

```text
Write current state once.
Link to it everywhere else.
Update it at every handoff.
```
