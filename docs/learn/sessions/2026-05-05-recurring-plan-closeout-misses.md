# Learn Session: Recurring Plan Closeout Misses

## Frame

- Date: 2026-05-05
- Status: session-recorded-routed
- Trigger: contributor asked how to optimize the workflow because plan lifecycle closeout after merge has been missed several times.
- Trigger type: explicit contributor observation with repeated-pattern claim.
- Scope: planned-initiative lifecycle closeout, especially `docs/plan.md` and plan-body transitions from Active to Done around PR merge.
- Session path: `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`

## Evidence Reviewed

- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `.codex/skills/pr/SKILL.md`
- `.codex/skills/verify/SKILL.md`
- `.codex/skills/workflow/SKILL.md`
- `.codex/skills/implement/SKILL.md`
- `docs/plan.md`
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- Git history for plan lifecycle ownership and post-merge closeout commits.

## Exclusions

- This session does not update `docs/plan.md` or any plan body lifecycle state.
- This session does not change `docs/workflows.md`, `specs/rigorloop-workflow.md`, skill files, validators, or GitHub workflows.
- This session does not open a proposal, issue, or PR for automation.
- No generated Codex runtime or adapter output is touched.

## Prior Learnings Reviewed

- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md`
- No prior topic file existed for plan lifecycle closeout before this session.

## Observations

### O1: The problem is recurring

This is not a single stale-plan incident. The repository history shows repeated post-merge lifecycle closeout work, plus the current PR #29 active-after-merge miss.

Evidence:

- `99907da` introduced plan lifecycle ownership rules.
- `6d507c1` aligned skills with plan lifecycle ownership.
- `0a24fe3` synchronized plan index and plan bodies.
- `331aa38`, `8187556`, `6b051eb`, `c351f09`, `cc0b5bc`, and `8c5245c` are prior after-merge or merge-closeout commits touching plan lifecycle state.
- `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md` records the current PR #29 stale Active state after merge.

### O2: The current rule is correct but operationally fragile

The governing workflow already says plan lifecycle state must update both `docs/plan.md` and the plan body, and that merge-dependent Done transitions may wait only for immediate post-merge cleanup. The miss happens because the required action is outside the PR's normal completion path.

Evidence:

- `docs/workflows.md` says final lifecycle closeout updates both `docs/plan.md` and the plan body.
- `docs/workflows.md` says only merge-dependent Done transitions should wait for immediate post-merge cleanup.
- `specs/rigorloop-workflow.md` R8g and R8h encode the same rule.
- The current PR #29 plan body explicitly deferred Done until merge, but no post-merge closeout followed.

### O3: Default to pre-PR Done when merge is not the deciding event

The strongest workflow optimization is to reduce the number of merge-dependent plan states. Most implementation plans are complete when implementation, review-resolution, verification, explain-change, and PR handoff are complete. In those cases, the plan should move to Done before PR opens, and the PR merge can be recorded as downstream evidence later only when needed.

Evidence:

- `docs/workflows.md` already says outcomes known before PR creation should move to Done before opening the PR.
- Several completed entries in `docs/plan.md` describe PR handoff readiness without needing active plan state to persist until merge.

### O4: When Done really is merge-dependent, make the follow-up tracked before merge

If the plan deliberately remains Active until merge, the PR handoff should leave a tracked, review-visible closeout obligation with owner, exact files, expected lifecycle text, PR number, and validation command. Relying on chat memory or a future agent noticing the stale Active entry is the failure mode.

Evidence:

- `specs/rigorloop-workflow.md` requires tracked or review-visible follow-up records for deferred workflow-governance actions.
- The PR #29 plan recorded pending merge-dependent Done state, but no separately tracked closeout owner or follow-up artifact enforced the post-merge action.

### O5: Automated stale-state detection would reduce recurrence

A validator or maintenance check can catch a completed merged PR still represented as Active. The likely detection rule is narrow: Active plan entry or active plan body references `PR #N` as open/pending, GitHub says PR #N is merged, and the plan is still under `## Active` or says `Status: active`.

Evidence:

- The current stale state is mechanically detectable from `docs/plan.md`, the plan body, and GitHub PR #29 metadata.
- Existing selector and lifecycle validators already recognize plan lifecycle surfaces; this would extend detection rather than invent a new artifact class.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | durable-lesson | durable-lesson | Topic entry | Contributor recurrence claim plus git history | The pattern has repeated evidence beyond one incident. |
| O2 | durable-lesson | durable-lesson | Topic entry | Existing workflow rules plus current miss | The lesson is about operational reliability, not missing policy. |
| O3 | durable-lesson | durable-lesson | Topic entry | Existing workflow rule and repeated closeout history | Reducing merge-dependent states is reusable guidance. |
| O4 | durable-lesson | durable-lesson | Topic entry; candidate workflow/proposal follow-up | Existing deferral/follow-up rules | Tracked follow-up before merge is reusable guidance, while any policy change needs a separate owning artifact. |
| O5 | process-follow-up | observation | Candidate proposal or validator follow-up | Current stale state is mechanically detectable | Automation is likely useful, but this session does not route an unapproved implementation change. |

Contributor confirmation status: confirmed for durable topic guidance by the explicit `$learn` request, recurrence claim, and request for best practices. Not confirmed for workflow, skill, validator, or CI implementation changes.

## Routing Results

- Durable lesson routing: created `docs/learn/topics/plan-lifecycle-closeout.md`.
- Observation routing: kept automation idea in this session as a candidate follow-up.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction or process follow-up routing: not created.

## Best Practices Captured

1. Prefer pre-PR Done for implementation plans whose real work is complete before PR creation.
2. Treat merge-dependent Done as exceptional, not the normal plan lifecycle path.
3. If Done must wait for merge, create a tracked closeout obligation before opening the PR.
4. Make the follow-up concrete: owner, PR number, files to edit, expected status wording, and validation command.
5. Add automated stale-state detection if this remains common: Active plan plus merged PR reference should be reported.
6. Keep `learn` as the observation and guidance surface; plan lifecycle state remains owned by `docs/plan.md` and the plan body.

## Follow-Ups

- Topic created: `docs/learn/topics/plan-lifecycle-closeout.md`.
- Candidate follow-up, not routed here: propose or implement validator/CI detection for Active plans that reference merged PRs.
- Candidate follow-up, not routed here: update workflow or PR-stage guidance so merge-dependent Done deferrals require a tracked closeout obligation before PR handoff.

