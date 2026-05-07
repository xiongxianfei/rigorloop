# Learn Session: Milestone Closeout vs Progress

## Frame

- Date: 2026-05-07
- Status: session-recorded-routed
- Trigger: contributor asked why a milestone is reported finished while its milestone closeout checklist remains open and no git commit exists.
- Trigger type: explicit contributor observation.
- Scope: active-plan milestone progress, milestone closeout checklists, and git commit evidence for the review skill material-finding recording initiative.
- Session path: `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`

## Evidence Reviewed

- `docs/plans/2026-05-07-review-skill-material-finding-recording.md`
- `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
- `docs/learn/topics/plan-lifecycle-closeout.md`
- `skills/implement/SKILL.md`
- `.codex/skills/implement/SKILL.md`
- `git status --short`
- `git log --oneline -5`

## Exclusions

- This session does not change plan milestone state.
- This session does not create git commits.
- This session does not update authoritative workflow, skill, validator, or template behavior.
- This session does not route a topic update without contributor confirmation.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
- `docs/learn/topics/plan-lifecycle-closeout.md`

The prior learning captures the distinction between verify handoff and final plan completion. It does not fully cover the narrower mismatch between checked progress items, open milestone closeout checklists, and missing milestone commits.

## Observations

### O1: Progress was marked complete before milestone closeout was complete

The active plan marks M1, M2, and M3 complete in the `Progress` section, but each milestone's own closeout checklist still contains open items for validation, lifecycle/progress/decision/validation-note updates, and milestone commit creation.

Evidence:

- `docs/plans/2026-05-07-review-skill-material-finding-recording.md` progress marks M1, M2, and M3 complete.
- The M1, M2, and M3 closeout checklists still contain unchecked closeout items.

### O2: The combined implementation slice was not reconciled with per-milestone closeout

The plan records that M1, M2, and M3 were implemented as one green implementation slice because M1 assertions could not pass before M2 source guidance and M3 generated output existed. That can be valid, but the plan did not then reconcile the individual milestone closeout checklists with the combined-slice reality.

Evidence:

- The decision log says M1, M2, and M3 were implemented as one green implementation slice.
- The surprises section says a standalone M1 closeout could not be green.
- The individual milestone closeout checklists still ask for separate milestone commits.

### O3: No milestone closeout commit exists in the current branch history

The current working tree has many modified and untracked files, and recent git history ends at PR #31. There are no commits for the review skill material-finding recording milestones.

Evidence:

- `git status --short` reports modified and untracked files for the current initiative.
- `git log --oneline -5` shows the latest commit as `6f03c4e Merge pull request #31...`, with no M1/M2/M3 milestone commit.

### O4: The implement skill requires milestone commits before marking milestones complete

The implement skill says a completed milestone must create a milestone closeout commit and says not to mark a milestone complete without the milestone commit.

Evidence:

- `skills/implement/SKILL.md` says: `When the milestone is complete, create a milestone closeout commit...`
- `skills/implement/SKILL.md` says: `Do not mark a milestone complete without the milestone commit.`
- The generated `.codex/skills/implement/SKILL.md` carries the same rule.

## Diagnosis

The direct cause is that the plan used `Progress` checkboxes to mean "the implementation content for M1-M3 exists and has passed validation," while the milestone closeout checklist and git history still say "the milestone has not been formally closed."

That split is inconsistent. Under the current implement rule, a milestone should not be marked complete until its closeout checklist is reconciled and its milestone commit exists. If multiple milestones are intentionally implemented as one green slice, the plan needs an explicit aggregate closeout model before progress is marked complete.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | artifact-update | artifact-update | Active plan correction | Contributor direction to re-plan M1-M3 as one explicit aggregate closeout | The active plan had contradictory progress and closeout signals, and the owner selected aggregate closeout as the recovery. |
| O2 | process-follow-up | process-follow-up | Active plan replan; broader template or skill clarification remains unrouted | Contributor direction to re-plan M1-M3 as one explicit aggregate closeout | Combined milestone slices need a clear closeout rule; the current routing fixes the active plan without changing templates or skills. |
| O3 | observation | observation | Active plan context | git evidence | The absence of commits explains why milestone closeout remains open. |
| O4 | observation | observation | Active plan context | implement skill evidence | Existing guidance already says milestone completion requires a commit. |

Contributor confirmation status: confirmed for active-plan correction. Not confirmed for topic update, workflow/spec/skill change, validator change, or template change.

## Candidate Corrective Actions

1. Reconcile the active plan by changing M1-M3 progress from completed to implementation-content-complete but closeout-pending until the commit exists.
2. Or, if the owner accepts a combined closeout, update the plan to explicitly say M1-M3 are closed by one aggregate milestone closeout commit, then create that commit.
3. Add future guidance that when milestones are combined into one green implementation slice, the plan must rewrite the closeout checklist before marking progress complete.

## Routing Results

- Session record: created and routed.
- Topic update: not routed; contributor confirmation is pending.
- Active plan correction: routed to `docs/plan.md` and `docs/plans/2026-05-07-review-skill-material-finding-recording.md`.
- Proposal, ADR, issue, workflow, skill, validator, or template update: not routed.
