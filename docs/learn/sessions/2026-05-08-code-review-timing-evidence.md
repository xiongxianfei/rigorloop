# Learn Session: Code Review Timing Evidence

## Frame

- Date: 2026-05-08
- Status: session-recorded; no durable lesson
- Trigger: contributor asked whether code-review R1 finding CR1 was invalid or a timing effect because the current plan no longer contains `Milestone state: implementing`.
- Trigger type: explicit contributor observation and learn invocation.
- Scope: CR1 evidence timing, current active-plan state, and review-record reproducibility for the active single-workflow initiative.
- Session path: `docs/learn/sessions/2026-05-08-code-review-timing-evidence.md`

## Evidence Reviewed

- `docs/learn/README.md`
- `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r1.md`
- `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
- `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`

## Exclusions

- No review-resolution closeout is changed by this session.
- No code-review finding is accepted, rejected, withdrawn, or closed by this session.
- No workflow, spec, skill, validator, or topic guidance is changed.
- No learn topic entry is created.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-05-review-record-placement.md` recorded that review-record placement and discoverability can be confusing from a single contributor observation, but did not create a durable lesson.
- `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md` recorded that material review findings need durable records when they drive tracked artifact edits, while broader policy routing needs confirmation.

## Observations

### O1: The missing text is explained by timing

The current active plan no longer contains `Milestone state: implementing` for M1. It now shows M1 as `resolution-needed` in both the current handoff and the M1 milestone section.

Evidence:

- `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` current handoff records `Current milestone state: resolution-needed`.
- `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md` M1 section records `Milestone state: resolution-needed`.
- `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/code-review-r1.md` records the pre-bookkeeping finding text that cited the earlier `implementing` state.
- `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md` records code-review R1 as open with unresolved CR1.

### O2: The finding was timing-dependent, but the record is hard to verify after bookkeeping edits

CR1 was based on the plan state observed before the code-review record and review bookkeeping updates were applied. After the review record was created, the active plan was updated to `resolution-needed`, so a later reader cannot reproduce the exact cited text from the current plan file.

This does not prove that CR1 was invalid. It does show a review-record quality issue: when a finding cites a mutable state that the same review bookkeeping immediately changes, the durable record should make the timing explicit or preserve enough snapshot detail for readers to understand why the current file no longer shows the old text.

### O3: One event is not enough for a durable lesson or policy change

This session found a concrete review-record reproducibility issue, but it is a single event. Existing learn records already cover related review-record discoverability and material-finding traceability concerns.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | None | Current plan and code-review record evidence | The current file state explains why the contributor cannot find the earlier text. |
| O2 | observation | observation | Candidate review-resolution handling for CR1 only | Current review record plus contributor observation | The issue is real but localized to the current CR1 record and does not justify a new durable lesson by itself. |
| O3 | no-durable-lesson | no-durable-lesson | None | Prior learn sessions plus single-event evidence | One timing/reproducibility event is insufficient evidence for topic guidance or policy change. |

Contributor confirmation status: not confirmed for routing beyond this session record.

## Routing Results

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Process follow-up routing: not created.

## No-Durable-Lesson Rationale

No durable lesson was captured because the evidence is a single timing-dependent review-record reproducibility issue. The next action, if any, belongs to the active CR1 review-resolution flow, not to a learn topic or standalone policy change.

## Follow-Ups

- None scheduled by this learn session.
- Candidate only: during CR1 review-resolution, clarify whether CR1 should be closed as already fixed by the `resolution-needed` bookkeeping update, or revise the code-review record with an explicit pre-bookkeeping snapshot note before rerunning `code-review M1`.
