# Learn Session: Plan Index Active After Merge

## Frame

- Date: 2026-05-05
- Status: session-recorded-unrouted
- Trigger: contributor asked why `docs/plan.md` still says the test and CI speed optimization plan is active after PR #29 merged.
- Trigger type: explicit contributor observation.
- Scope: merged lifecycle state for `2026-05-04-test-and-ci-speed-optimization`.
- Session path: `docs/learn/sessions/2026-05-05-plan-index-active-after-merge.md`

## Evidence Reviewed

- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/plan.md`
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- GitHub PR #29 metadata: merged into `main` on 2026-05-05 at merge commit `76a8e837bf102652d90d11a8b083a00b8a011d83`.
- `origin/main` after fetching the merge commit.

## Exclusions

- This session does not update `docs/plan.md`.
- This session does not update the plan body lifecycle status.
- This session does not create a learn topic entry.
- This session does not open a PR or create a lifecycle-closeout branch beyond this learn-session branch.
- No generated Codex runtime or adapter output is touched.

## Prior Learnings Reviewed

- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- No prior learn topic file exists for post-merge plan closeout.

## Observations

### O1: The stale Active state exists in merged source, not only in a local branch

After fetching `origin/main`, `docs/plan.md` still lists the test and CI speed optimization plan under `## Active`, and the plan body still says `Status: active`.

Evidence:

- `docs/plan.md` lists `2026-05-04 Test and CI speed optimization` under `## Active`.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` line 3 says `Status: active`.
- PR #29 is merged into `main` at merge commit `76a8e837bf102652d90d11a8b083a00b8a011d83`.

### O2: The plan intentionally deferred Done until after merge

The plan body recorded the pre-merge state as active and explicitly said the merge-dependent Done state remained pending. That was coherent before merge because the deciding completion event was the PR merge.

Evidence:

- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` says PR #29 was opened.
- The plan outcome says the initiative is active and the merge-dependent Done state remains pending.

### O3: The immediate post-merge closeout did not happen

The reason `docs/plan.md` still says active is that the PR merged, but no immediate post-merge lifecycle closeout updated both the plan index and plan body from active to done.

Evidence:

- `docs/workflows.md` says final lifecycle closeout updates both `docs/plan.md` and the plan body when lifecycle state changes.
- `docs/workflows.md` says only merge-dependent Done transitions should wait for immediate post-merge cleanup.
- `specs/rigorloop-workflow.md` R8g and R8h encode the same contract.

### O4: This is not a new durable workflow lesson

The governing rule already exists. The gap is execution of the existing rule, not absence of the rule.

Evidence:

- `docs/workflows.md` and `specs/rigorloop-workflow.md` already describe the required final lifecycle closeout.
- `AGENTS.md` and `CONSTITUTION.md` already require planned lifecycle state to update both the plan index and plan body when lifecycle state changes.

### O5: The likely next action is an artifact update, but learn should not perform it unilaterally

The action-owning fix is to run a post-merge lifecycle closeout that moves the plan from Active to Done in both `docs/plan.md` and the plan body, with PR #29 merge evidence. This learn session records the observation only because `learn` is not the authoritative owner of plan index state or plan-body lifecycle state.

Evidence:

- The `learn` skill says not to use `learn` as the authoritative owner of plan index state or plan-body lifecycle state.
- The `learn` skill requires contributor confirmation before routing observations into derivative artifact updates or process follow-ups.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | None | Merged `origin/main` evidence | The stale state is factual and evidence-bound. |
| O2 | observation | observation | None | Plan-body outcome text | The pre-merge active state was intentionally merge-dependent, not an arbitrary omission at PR time. |
| O3 | process-follow-up | observation | Candidate process-follow-up: post-merge lifecycle closeout | Contributor question plus merged PR evidence | The missed closeout likely needs action, but learn cannot route it without explicit confirmation. |
| O4 | no-durable-lesson | no-durable-lesson | None | Existing workflow contract evidence | The rule is already captured in authoritative workflow artifacts. |
| O5 | artifact-update | observation | Candidate artifact update: `docs/plan.md` and `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` | Existing learn and workflow rules | The artifact update is the likely repair, but it is not routed by this learn session. |

Contributor confirmation status: not confirmed for routing. This session records candidate routes only.

## Routing Results

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction or process follow-up routing: not created.

## No-Durable-Lesson Rationale

No durable lesson was captured because the workflow already says merge-dependent Done transitions wait only for immediate post-merge cleanup and lifecycle state changes must update both `docs/plan.md` and the plan body. The current issue is a missed application of that rule after PR #29 merged.

## Follow-Ups

- No follow-up was scheduled by this learn session.
- Candidate follow-up, not routed here: update `docs/plan.md` and `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` to record PR #29 as merged and move the plan to Done.

