# Learn Session: Milestone Commit Policy Mismatch

Date: 2026-05-08
Status: recorded

## Frame

- Trigger: explicit maintainer request to create a learn session after observing that the active plan requires `milestone committed` for each milestone while no new milestone commit exists for the current initiative.
- Trigger type: contributor observation and explicit maintainer request.
- Scope: active plan milestone closeout wording, actual Git commit state, and the learn-session behavior that previously returned `Session path: none`.
- Evidence in scope:
  - `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
  - `docs/plan.md`
  - `.codex/skills/implement/SKILL.md`
  - `docs/workflows.md`
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `git log --oneline -15`
  - `git status --short`
- Explicit exclusions:
  - This session does not update active plan milestone state, close review-resolution, create commits, or claim PR readiness.
  - This session does not create a topic entry because the durable lesson is already covered by a prior learn session.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
- Session record path: `docs/learn/sessions/2026-05-08-milestone-commit-policy-mismatch.md`

## Observe

### O1: The active plan still carries commit closeout criteria that do not match actual Git state

The active plan lists `Commit message` and `milestone committed` under milestone closeout for M1 through M6. M1 and M2 are already marked closed, and M3 is in review-resolution after code-review R4.

Evidence:

- `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` has `milestone committed` in each milestone closeout checklist.
- `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` marks M1 and M2 closed and M3 as `resolution-needed`.
- `git log --oneline -15` shows recent commits from the prior skill-contract initiative, not new M1/M2/M3 commits for this current initiative.
- `git status --short` shows current initiative plan/change files are still untracked or modified, so they cannot already be represented by milestone commits.

### O2: The implement skill treats milestone commits as a closeout requirement

The implement skill says implementation output includes a milestone handoff commit and later says not to mark a milestone complete without the milestone commit.

Evidence:

- `.codex/skills/implement/SKILL.md` says implementation outputs include "a milestone handoff commit that sets the milestone to `review-requested`."
- `.codex/skills/implement/SKILL.md` says: "Do not mark a milestone complete without the milestone commit."
- `.codex/skills/implement/SKILL.md` also lists a stop condition when the current milestone cannot be updated to `review-requested` with validation evidence and a milestone commit.

### O3: The broader workflow allows PRs with one or more completed milestone commits, but the active plan does not name an aggregate or deferred commit policy

The workflow summary says a PR may contain one or more completed milestone commits when that is the clearest review boundary. That permits either per-milestone commits or an aggregate commit strategy, but the active plan currently lists `milestone committed` without recording which strategy is being used or why commit evidence is deferred.

Evidence:

- `docs/workflows.md` says a pull request may contain one or more completed milestone commits when that is the clearest review boundary.
- The active plan has per-milestone commit messages and `milestone committed` checklist items, but no explicit `Commit policy` or `Commit status` field.

### O4: The previous `Session path: none` answer was wrong after an explicit session request

The learn skill says that when a learn invocation reaches Frame, the agent creates or updates a tracked session record. The maintainer explicitly asked to create a session. Returning `Session path: none` treated the request as quick Q&A instead of entering Frame.

Evidence:

- `.codex/skills/learn/SKILL.md` says a learn invocation that reaches Frame creates or updates `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.
- The user explicitly asked: "Please create a session."

### O5: The durable lesson is already captured; this recurrence needs active-plan correction rather than a new topic

The 2026-05-07 learn session already records the distinction between progress, closeout checklists, and missing milestone commits. The current incident repeats the same pattern on a new active plan.

Evidence:

- `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md` records that milestone progress was marked complete while milestone closeout checklists still required separate milestone commits.
- The same prior session states that under the current implement rule, a milestone should not be marked complete until closeout checklist and milestone commit evidence are reconciled, or the plan needs an aggregate closeout model.

## Classify

| Observation | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | process-follow-up candidate | session evidence | The mismatch is real and review-visible, but learn does not own plan state or commits. |
| O2 | observation | observation | active plan follow-up | session evidence | The skill behavior explains why the mismatch matters. |
| O3 | process-follow-up | process-follow-up candidate | active plan commit-policy update | pending owner confirmation | The active plan should choose per-milestone commits or aggregate/deferred commit evidence, but this session does not route edits without confirmation. |
| O4 | no-durable-lesson | no-durable-lesson | none | maintainer correction | The learn-session behavior was a local handling mistake and is fixed by creating this session. |
| O5 | no-durable-lesson | no-durable-lesson | link prior session | prior learn session | The durable lesson already exists; duplicating a topic entry would add noise. |

## Route

- Session record created: `docs/learn/sessions/2026-05-08-milestone-commit-policy-mismatch.md`
- Topic updates: none.
- Action-owning artifact updates: none in this session.
- Candidate follow-up: update `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` to replace generic `milestone committed` checklist items with explicit `Commit policy` and `Commit status` fields, or create the required scoped milestone commits before marking milestones closed.
- Candidate follow-up owner: active plan / review-resolution for the current initiative.

## No-Durable-Lesson Rationale

No new durable topic lesson was captured because the reusable guidance is already recorded in `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`. This session records a recurrence and the specific current active-plan follow-up.
