# Learn Session: Milestone Finished vs Committed

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation: "the same problem, milestone 1 is finised. But the change isn't commit."
- Trigger type: explicit maintainer request / contributor observation / repeated milestone closeout confusion.
- Scope:
  - current git status and recent commit history;
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`;
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r3.md`;
  - prior learn sessions about milestone closeout, implement review-fix handoff drift, and plan readiness state drift.
- Evidence in scope:
  - `git log --oneline -5` shows M1 implementation commit `4c41494 M1: align architecture surface test spec`;
  - `git status --short` shows uncommitted changes to `change.yaml`, `review-log.md`, `review-resolution.md`, the active plan, three code-review records, and two learn sessions;
  - the active plan says M1 is `resolution-needed`, M1 CR1-F1/CR2-F1 are not resolved and returned to code-review, and M1 is not closed;
  - code-review R3 says it is clean only for the CR1/CR2 open-state alignment slice and explicitly does not close CR1-F1 or CR2-F1.
- Explicit exclusions:
  - this session does not create a git commit;
  - this session does not close M1, CR1-F1, CR2-F1, review-resolution, or the active plan;
  - this session does not update implement skill behavior, workflow specs, plan templates, validators, or topic files;
  - this session does not claim branch readiness, verification readiness, PR readiness, or final lifecycle closeout.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `docs/learn/sessions/2026-05-09-implement-review-fix-handoff-drift.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`
- Session record path: `docs/learn/sessions/2026-05-09-milestone-finished-vs-committed.md`

## Observe

### O1 - M1 implementation content is committed, but M1 is not closed

Evidence:

- `git log --oneline -5` shows `4c41494 M1: align architecture surface test spec`.
- The active plan says `Milestone state: resolution-needed`.
- The active plan progress says `M1 CR1-F1 and CR2-F1 resolved and returned to code-review` is still unchecked.
- The active plan progress says `M1 closed after clean code-review` is still unchecked.

Observation:

"M1 is finished" is too broad. The implementation-content commit exists, but the milestone is not finished in workflow terms because review-resolution remains open and the milestone is not closed.

### O2 - Current review/learn evidence is uncommitted

Evidence:

- `git status --short` shows modified `change.yaml`, `review-log.md`, `review-resolution.md`, and the active plan.
- `git status --short` shows untracked `code-review-r1.md`, `code-review-r2.md`, `code-review-r3.md`, `2026-05-09-plan-readiness-state-drift.md`, and `2026-05-09-implement-review-fix-handoff-drift.md`.

Observation:

Even the current review-resolution bookkeeping and learn evidence are not yet durable in git. That makes any "finished" claim unsafe unless it is narrowly scoped to "implementation content was committed earlier."

### O3 - The same prior lesson already exists

Evidence:

- `2026-05-07-milestone-closeout-vs-progress.md` diagnosed the same class: progress was marked complete before milestone closeout and commit evidence were complete.
- That session records the implement skill invariant that a milestone should not be marked complete without the milestone commit.
- The current case repeats the same terminology drift with a different shape: a commit exists for initial M1 implementation, but new required review-resolution evidence remains uncommitted and the milestone remains open.

Observation:

This is not a new durable lesson. It is the same underlying failure: treating partial progress, review-slice cleanliness, or an earlier implementation commit as milestone completion.

## What's Wrong

The word "finished" is being used for the wrong unit.

For this change, the safe state is:

- M1 implementation content: committed in `4c41494`;
- M1 review-resolution: open;
- M1 milestone state: `resolution-needed`;
- current review/learn evidence: uncommitted;
- M1 milestone closeout: not complete.

So the problem is not that "finished work was not committed." The problem is that the workflow is again allowing a partial state to sound finished. The actual state is "M1 has committed implementation content, but required review-resolution and current evidence remain open and uncommitted."

## Best Practices

1. Avoid saying a milestone is "finished" unless the plan state is `closed`, required review-resolution is closed, and the closeout commit exists.
2. Use narrower labels:
   - `implementation-content-committed`
   - `review-resolution-open`
   - `review-alignment-clean`
   - `milestone-closed`
3. Before claiming a milestone is finished, check both `git status --short` and `git log --oneline`.
4. If `git status --short` has in-scope modified or untracked files, say what remains uncommitted.
5. A clean review of a sub-slice, such as code-review R3's open-state alignment review, does not close the milestone.
6. Review records, review-resolution updates, plan state changes, and learn sessions are real change artifacts. If they are in scope, they must be committed or explicitly excluded before durable closeout claims.
7. Keep the active plan progress wording aligned with git state: "implementation content committed" is not the same as "milestone closed."

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Active plan context | Git log and active plan evidence | The current state distinguishes committed implementation content from open milestone closeout. |
| O2 | observation | observation | Active working-tree context | Git status evidence | The current review/learn evidence remains uncommitted. |
| O3 | no-durable-lesson | no-durable-lesson | Prior learn session reference | Prior session plus current evidence | The durable lesson already exists in the 2026-05-07 milestone closeout session. |

Contributor confirmation status: unavailable for derivative updates. This session records the repeated observation and stops before routing.

## Route

No routing performed.

The next operational action belongs to review-resolution/implement for M1, not to learn: either continue resolving CR1-F1/CR2-F1 and then commit the resulting closeout evidence, or explicitly keep M1 in `resolution-needed` with the uncommitted state visible.

## No Durable Route Rationale

No new topic entry or policy update was created. The durable lesson is already captured by `2026-05-07-milestone-closeout-vs-progress.md`; this session records that the same confusion recurred in the current initiative.
