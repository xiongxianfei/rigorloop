# Learn Session: Plan Readiness State Drift

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the stale readiness problem happened again and what best practices should prevent it.
- Trigger type: explicit maintainer request / contributor observation / repeated lifecycle-readiness drift.
- Scope:
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/plan-review-r1.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/plan-review-r2.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r1.md`
  - prior learn records about plan lifecycle closeout, plan readiness versus completion, milestone closeout versus progress, and review finding volume root cause
- Evidence in scope:
  - plan-review R1 finding `PR-F1`, which required per-milestone code-review handoff and review closeout;
  - plan-review R2, which approved the revised per-milestone review-loop plan;
  - code-review R1 finding `CR1-F1`, which found stale `Outcome and Retrospective` readiness text after M1 handoff;
  - the active plan's current state after partial correction, where `Current Handoff Summary` says M1 is in review-resolution while the `Readiness` section still says `Next stage: code-review M1`.
- Explicit exclusions:
  - this session does not change the active plan, review-resolution, workflow specs, skills, validators, templates, topic files, PR readiness, or lifecycle state;
  - this session does not close `CR1-F1`;
  - this session does not route a process or artifact update without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
- Session record path: `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`

## Observe

### O1 - The immediate defect is stale sibling readiness text after a stage transition

Evidence:

- `CR1-F1` reports that the plan's Current Handoff Summary and Readiness section routed M1 to `code-review M1`, while `Outcome and Retrospective` still said the plan was ready for `plan-review`.
- After the partial correction, the plan's Current Handoff Summary says M1 is `resolution-needed` and the next stage is `review-resolution / implement M1 fix`.
- The same plan's Readiness section still says `Next stage: code-review M1` and `Implementation readiness: M1 is implemented and ready for code-review`.

Observation:

The recurring problem is not just a bad sentence. It is a multi-surface state sync failure. A lifecycle transition was applied to the handoff summary and outcome text, but a sibling readiness section still carried the previous state.

### O2 - The root cause is duplicated mutable lifecycle state without a required sweep

Evidence:

- The active plan carries operational state in `Current Handoff Summary`, milestone state fields, `Progress`, `Validation Notes`, `Outcome and Retrospective`, and `Readiness`.
- Plan-review R1 already required adding per-milestone handoff and review closeout state to each implementation milestone.
- Code-review R1 then found stale readiness wording after M1 had moved past plan-review and into implementation/code-review flow.
- The prior learn session `2026-05-09-review-finding-volume-root-cause.md` observed that duplicated lifecycle facts across current handoff, milestone sections, readiness fields, progress notes, plan index, and change metadata made timing-dependent inconsistencies likely.

Observation:

The deepest cause is that the workflow asks the agent to maintain several human-readable copies of the same fact: current milestone, current state, next stage, review status, and final-closeout readiness. The process relies on manual edits, and the validation currently checks artifact shape more reliably than semantic agreement between plan sections.

### O3 - Existing guidance is correct but too distributed for execution-time updates

Evidence:

- `docs/learn/topics/plan-lifecycle-closeout.md` already says readiness is a next-gate statement, not Done or PR readiness.
- `2026-05-07-plan-readiness-vs-completion.md` recommends pairing state with next action and remaining gates.
- `2026-05-09-review-finding-volume-root-cause.md` recommends one concise current-state block and updating mirrored state surfaces together before review.
- The active plan still drifted after those lessons existed.

Observation:

The rule is known, but it is not operationalized tightly enough at the edit point. Agents need a concrete "stage-transition sweep" whenever plan state changes, not just general awareness that readiness differs from completion.

### O4 - The best prevention is to reduce duplicated next-stage claims and add a transition checklist

Evidence:

- The Current Handoff Summary already has the fields needed to be the primary operational state: current milestone, milestone state, last reviewed milestone, review status, remaining milestones, next stage, final closeout readiness, and reason.
- The stale text appeared in lower sections that repeated or paraphrased the same next-stage claim.
- Existing validation selected lifecycle and metadata checks, but did not catch semantic disagreement between `Current Handoff Summary` and `Readiness`.

Observation:

The safest pattern is to make `Current Handoff Summary` the primary next-stage source, keep `Readiness` short and synchronized, and run a targeted stale-stage search after every transition.

## Root Cause

The root cause is duplicated mutable plan state plus incomplete transition hygiene.

The plan repeats the same lifecycle facts in several places. When M1 moved from plan-review/test-spec readiness into implementation handoff and then into code-review resolution, updates were applied locally to the most visible section, but not swept across every section that also names the next stage. Because the validators prove structure and lifecycle language more than cross-section semantic consistency, stale wording survived until review caught it.

## Best Practices

1. Treat every stage transition as a state-sync edit, not a sentence edit.
2. Make `Current Handoff Summary` the primary operational state block.
3. Keep `Readiness` derived from that block, or make it reference the current handoff instead of restating detailed next-stage claims.
4. On every transition, sweep at least: Current Handoff Summary, current milestone state, relevant milestone handoff or closeout, Progress, Validation Notes, Outcome and Retrospective, Readiness, change metadata, review log, and review-resolution.
5. Search for stale prior gates before review handoff, for example `plan-review`, `test-spec`, `code-review M1`, `verify`, `final closeout`, and `PR readiness` depending on the transition.
6. Keep `Outcome and Retrospective` neutral while the plan is active; it should not become a second operational router.
7. Record the review finding ID in the state block while resolution is open, so later sections can be checked against a concrete current state.
8. Prefer one positive invariant per transition: "current stage is X; next stage is Y; final closeout is not ready because Z."
9. Add an automated semantic or grep-based check later if this remains frequent, especially comparing `Current Handoff Summary` and `Readiness`.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Current plan and code-review R1 evidence | This is the concrete repeated failure in the active plan. |
| O2 | process-follow-up | pending confirmation | Possible plan skill, implement skill, code-review skill, plan template, or validator follow-up | Not yet confirmed | The evidence supports a reusable process gap, but changing behavior belongs in action-owning artifacts. |
| O3 | process-follow-up | pending confirmation | Possible checklist addition to plan/implement/code-review guidance | Not yet confirmed | Existing lessons are insufficiently operational at the transition edit point. |
| O4 | process-follow-up | pending confirmation | Possible static check comparing handoff and readiness state | Not yet confirmed | Automation could catch this class, but it needs contributor-confirmed scope. |

Contributor confirmation status: unavailable for derivative updates. This session records candidate classifications and stops before routing.

## Route

No routing performed.

This session does not update topic files, skills, workflow specs, validators, templates, or the active plan because contributor confirmation is required before routing. Candidate follow-up: add a stage-transition sweep requirement to the action-owning artifact that governs plan/implementation state updates, and consider a validator or targeted grep check for stale readiness terms.

## No Durable Route Rationale

The evidence supports a recurring process gap, but the corrective behavior would affect authoritative plan, implement, code-review, template, or validation contracts. `learn` records the evidence and candidate best practices; it does not make that policy authoritative by itself.
