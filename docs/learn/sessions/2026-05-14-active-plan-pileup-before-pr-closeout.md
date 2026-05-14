# Learn Session: Active Plan Pileup Before PR Closeout

## Frame

- Trigger: maintainer invoked `$learn` and asked why `docs/plan.md` accumulated many Active plans even though the workflow has a rule that actions should be done before PR.
- Trigger type: explicit maintainer retrospective / repeated lifecycle-state observation.
- Scope: plan lifecycle closeout rules, recent stale Active plan entries, prior plan-closeout learn guidance, and the current status-sync repair.
- Session path: `docs/learn/sessions/2026-05-14-active-plan-pileup-before-pr-closeout.md`
- Evidence in scope:
  - `AGENTS.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `docs/plan.md`
  - `docs/plans/2026-05-10-token-cost-measurement-baseline-and-proposal-scope-preservation.md`
  - `docs/plans/2026-05-12-record-every-formal-review.md`
  - `docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md`
  - `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
  - `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
  - `docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md`
  - `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`
  - GitHub PR state observed for PRs `#40`, `#48`, `#50`, `#51`, `#52`, `#53`, and `#58`
- Explicit exclusions:
  - This session does not use `learn` as the owner of `docs/plan.md` or plan-body lifecycle state.
  - This session does not create new workflow policy; authoritative rules already live in `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `AGENTS.md`.
  - This session does not claim PR #58 is done. GitHub reported PR #58 open with hosted CI passing.
  - This session does not update topic files or follow-up registers without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md`
  - `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`

## Observe

### O1: The "done before PR" rule exists and is already authoritative

The current workflow contract says planned initiative lifecycle state must be synchronized before review-ready PR handoff when the PR performs the completing transition. `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `AGENTS.md` all say the plan index and plan body must move together, and merge is not a routine lifecycle-closeout trigger.

Evidence:

- `docs/workflows.md` says lifecycle synchronization happens inside the PR that performs the lifecycle transition, before that PR opens for review.
- `docs/workflows.md` says if a PR completes a planned initiative, move it to `Done` in both `docs/plan.md` and the plan body before opening the PR for review.
- `specs/rigorloop-workflow.md` requirement `R8h` says merge is a fast-forward of pre-validated repository state, not a trigger for further lifecycle changes.
- `specs/rigorloop-workflow.md` requirement `R8ha` says the completing PR must record the `Done` transition in both `docs/plan.md` and the plan body before review.
- `AGENTS.md` says final lifecycle closeout updates both `docs/plan.md` and the plan body before review opens, and `verify` treats stale lifecycle state between the index and plan body as blocking PR readiness.

### O2: The active-plan pileup came from older downstream-gate wording and missed follow-through

The stale Active entries were not active implementation work. They were lifecycle-state debt from plans that kept themselves Active while waiting for PR review, hosted CI, or release publication. After those downstream events completed, the plan index and plan bodies were not synchronized until the later status-sync repair.

Evidence:

- PRs `#40`, `#48`, `#50`, `#51`, `#52`, and `#53` were observed as merged with hosted CI passed.
- Releases `v0.1.2` and `v0.1.3` were observed as published.
- The repaired `docs/plan.md` moved those six plans from `Active` to `Done`.
- The corresponding plan bodies were updated from `Status: active` to `Status: done` and their current handoff summaries now record done state.

### O3: Some downstream-active exceptions were legitimate before the downstream event completed

The rule is not "every plan must always be Done before any PR exists." The workflow allows a plan to remain Active when a true downstream event remains, such as release publication, deploy, package publication, external migration, or an unobserved hosted check. That exception explains why several plans originally remained Active at PR handoff time.

The error was letting those exceptions persist after the downstream events completed, or using PR merge itself as the implied completion event without a tracked closeout.

Evidence:

- `specs/rigorloop-workflow.md` example `E12` allows a plan to stay Active when it depends on a later release or deploy.
- `specs/rigorloop-workflow.md` edge case `32` allows release, deploy, package publication, external migration, or unobserved hosted check to keep an otherwise implemented plan active.
- `docs/learn/topics/plan-lifecycle-closeout.md` says completion may stay Active only for a true downstream event and must name that event or follow-up condition; it also says not to use merge itself as a routine downstream completion event.

### O4: Validation caught index/body disagreement, but not "both stale in the same way"

The artifact lifecycle validator correctly blocked when `docs/plan.md` listed the repaired plans as Done while the plan bodies still said `Status: active`. It did not catch the earlier pileup because the index and plan bodies were internally consistent in the wrong direction: both still said Active.

The missing automated check is not ordinary artifact lifecycle consistency. It is stale-active detection against external or recorded completion evidence, such as an Active plan referencing PR `#N` as open while GitHub says PR `#N` merged, or an Active release plan whose named release was already published.

Evidence:

- During the status-sync repair, `validate-artifact-lifecycle.py` blocked until the six plan bodies were changed from `Status: active` to `Status: done`.
- Prior learn topic guidance already says the next improvement should be automated detection for an Active plan entry or active plan body whose tracked state conflicts with PR-contained evidence or a named downstream completion event.

### O5: The durable lesson already exists; the current event is another example

This session does not need a new topic rule. The existing `plan-lifecycle-closeout` topic already captures the durable lesson: reduce lifecycle states that depend on later merge observation, keep a plan Active only for true downstream events, and consider automated detection if the failure keeps recurring.

The current pileup strengthens the evidence for the existing candidate automation, but it does not create a new independent lesson.

Evidence:

- `docs/learn/topics/plan-lifecycle-closeout.md` already says after-merge plan closeout is easy to miss and that implementation plans should move to Done inside the completing PR when the real work is complete.
- The same topic already names automated detection as the next improvement if recurrence continues.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Workflow, spec, and AGENTS evidence | The rule already exists in authoritative artifacts. |
| O2 | observation | observation | None | Stale plan entries, PR states, and status-sync repair | The pileup was stale lifecycle bookkeeping, not real active implementation work. |
| O3 | observation | observation | None | Workflow downstream-event exception evidence | Some plans were legitimately Active before downstream events completed. |
| O4 | process-follow-up | candidate process-follow-up | Candidate validator or maintenance check | Contributor confirmation pending | Repeated stale-active evidence suggests automation may be useful, but learn must not route without confirmation. |
| O5 | no-durable-lesson | no-durable-lesson | Existing topic covers it | Existing topic and prior sessions | The lesson is already captured; this session adds evidence but does not need a new topic entry. |

## Route

- Created session record: `docs/learn/sessions/2026-05-14-active-plan-pileup-before-pr-closeout.md`
- No topic entry was created because the durable lesson already exists in `docs/learn/topics/plan-lifecycle-closeout.md`.
- No workflow, spec, validator, skill, or follow-up artifact was updated from this learn session.
- Candidate process follow-up, pending contributor confirmation: create a narrow automated stale-active check for plans that reference merged PRs, passed hosted CI, or published releases while still listed as Active.

## Answer

There were many Active plans because several older plan handoffs treated PR review, hosted CI, or release publication as downstream completion gates. That can be legitimate while the downstream event is still unknown. It becomes wrong after the PR merges, hosted CI passes, or the release publishes.

The repository already has the stricter rule now: if the PR itself completes the planned initiative, the PR must move both `docs/plan.md` and the plan body to `Done` before review. Merge should integrate that pre-validated state; it should not be the normal trigger for later lifecycle bookkeeping.

The stale entries accumulated because:

1. Some plans were written before or during the transition to the stricter pre-PR lifecycle rule.
2. Several plans explicitly kept Active state for PR review, hosted CI, or release publication.
3. After those events completed, nothing forced a synchronized plan-index and plan-body update.
4. Existing lifecycle validation catches index/body disagreement, but it does not query GitHub or release state when both surfaces are stale in the same way.

The practical fix is what the status-sync repair did: move completed plans to `Done` in both the index and plan body. The better future fix is automation that reports Active plans whose named PR is merged or whose named release has already published.

## No-Durable-Route Rationale

No new durable topic entry was added because the plan lifecycle closeout lesson already exists. This session records the current recurrence and explains the root cause.

## Follow-Ups

- Candidate follow-up, not routed here: add a validator or maintenance command that detects Active plans referencing merged PRs, passed hosted CI, or published releases.
