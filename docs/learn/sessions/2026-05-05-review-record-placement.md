# Learn Session: Review Record Placement

## Frame

- Date: 2026-05-05
- Status: session-recorded
- Trigger: contributor asked why `proposal-review`, `plan-review`, and `spec-review` results are not under `docs/changes`.
- Trigger type: explicit contributor observation.
- Scope: review-result placement for the `2026-05-04-test-and-ci-speed-optimization` change.
- Session path: `docs/learn/sessions/2026-05-05-review-record-placement.md`

## Evidence Reviewed

- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `specs/rigorloop-workflow.test.md`
- `docs/learn/README.md`
- `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md`
- `specs/test-and-ci-speed-optimization.md`
- `specs/test-and-ci-speed-optimization.test.md`
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/change.yaml`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/review-log.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/review-resolution.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r1.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r2.md`

## Exclusions

- No workflow, spec, plan, proposal, or change-pack policy update is made by this session.
- No learn topic entry is created.
- No new review-resolution entry is created for clean upstream reviews.
- No generated Codex runtime or adapter output is touched.

## Prior Learnings Reviewed

- `docs/learn/README.md`
- No prior session or topic file existed for this specific observation.

## Observations

### O1: Detailed review records are conditional

The governing workflow requires detailed review files for material findings, blocking non-approval outcomes, reconstructed reviews, closeout evidence citations, or explicit durable-record requests. Clean formal reviews with no material findings may settle in the reviewed artifact instead of creating empty detailed review files.

Evidence:

- `AGENTS.md` says workflow-managed formal reviews create detailed review records only for the listed triggers, and clean reviews may settle artifact-locally when no detailed-record trigger applies.
- `specs/rigorloop-workflow.md` R12an-R12at define the detailed-review triggers and explicitly state that clean formal reviews do not require empty detailed review files solely because the review was required.

### O2: Upstream review outcomes for this change settled artifact-locally

The `proposal-review`, `spec-review`, and `plan-review` outcomes are present, but they live in the artifacts they reviewed or in the downstream lifecycle context.

Evidence:

- `docs/proposals/2026-05-04-test-and-ci-speed-optimization.md` records `proposal-review`: approved with no material findings.
- `specs/test-and-ci-speed-optimization.md` records `spec-review`: approved with no material findings on 2026-05-04.
- `specs/test-and-ci-speed-optimization.test.md` records `spec-review` as approved and `plan-review` as approved with no material findings; it also states no detailed review record was required for plan-review.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` records plan-review complete.

### O3: The change-local review records exist for code-review because code-review produced material findings

The change-local review pack contains detailed `code-review` records and `review-resolution.md` because the code-review rounds produced material findings that required disposition and closeout evidence.

Evidence:

- `docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r1.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/reviews/code-review-r2.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/review-log.md`
- `docs/changes/2026-05-04-test-and-ci-speed-optimization/review-resolution.md`

### O4: Discoverability may still be confusing

The question shows that the distinction between artifact-local clean review settlement and change-local detailed review records may not be obvious during PR review. This is a single contributor observation and does not by itself justify a new durable lesson or workflow change.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | None | Existing workflow contract evidence | The rule already exists in authoritative artifacts; this session should not duplicate it as learn topic policy. |
| O2 | observation | observation | None | Current change artifacts | The missing `docs/changes` files are explained by existing artifact-local records. |
| O3 | observation | observation | None | Current change-local review records | The code-review records are present because material findings triggered detailed review handling. |
| O4 | observation | observation | Candidate process-follow-up only if the contributor confirms a recurring discoverability problem | Contributor question | One event is not enough evidence for a durable lesson or artifact update. |

Contributor confirmation status: not confirmed for routing. This session records the observations only.

## Routing Results

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction or process follow-up routing: not created.

## No-Durable-Lesson Rationale

No durable lesson was captured because the governing workflow already covers the behavior, the current change artifacts contain the upstream review outcomes, and the only new signal is a single discoverability question.

## Follow-Ups

- None scheduled.
- If this confusion recurs, evaluate a focused workflow-doc clarification or a proposal for review-result discoverability.

