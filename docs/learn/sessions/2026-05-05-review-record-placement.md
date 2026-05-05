# Learn Session: Review Record Placement

## Frame

- Date: 2026-05-05
- Status: session-recorded
- Trigger: contributor asked why `proposal-review`, `plan-review`, and `spec-review` results are not under `docs/changes`.
- Follow-up trigger: contributor clarified that spec-review did include minor finding `SR-1` about `--fail-fast` optionality.
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
- Contributor-provided spec-review outcome text from the 2026-05-05 learn invocation.
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

The governing workflow requires detailed review files for material findings, blocking non-approval outcomes, reconstructed reviews, closeout evidence citations, or explicit durable-record requests. A formal review that has no material findings may settle in the reviewed artifact instead of creating empty detailed review files, even if it has a minor non-blocking note that is resolved artifact-locally.

Evidence:

- `AGENTS.md` says workflow-managed formal reviews create detailed review records only for the listed triggers, and clean reviews may settle artifact-locally when no detailed-record trigger applies.
- `specs/rigorloop-workflow.md` R12an-R12at define the detailed-review triggers and explicitly state that clean formal reviews do not require empty detailed review files solely because the review was required.
- `specs/rigorloop-workflow.md` R12b allows routine non-material review notes to remain in contributor-visible review surfaces when they do not require material finding disposition.

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

### O5: SR-1 was a minor non-blocking finding, not a material detailed-record trigger

The contributor is correct that spec-review had one finding: `SR-1`, a minor non-blocking concern that `--fail-fast` optionality was underspecified for test-spec authoring. That explains why the earlier phrase "no material findings" was correct but too compressed. The reason there is no `docs/changes/.../reviews/spec-review-r1.md` is not that SR-1 did not exist; it is that SR-1 was non-blocking, did not require a material finding disposition, and was resolved in the approved spec by changing `R7` from optional to required `--fail-fast` support.

Evidence:

- Contributor-provided spec-review outcome: `approved`, one minor non-blocking concern, no blocking or major findings.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` records that the one minor finding about `--fail-fast` optionality was resolved by changing `R7` to require `--fail-fast`.
- `docs/plans/2026-05-04-test-and-ci-speed-optimization.md` progress records `Spec-review approved with SR-1 resolved by requiring --fail-fast`.
- `specs/test-and-ci-speed-optimization.test.md` records that the `--fail-fast` minor finding was resolved in the approved spec.
- `specs/test-and-ci-speed-optimization.md` now states `R7. The wrapper MUST support --fail-fast`.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | None | Existing workflow contract evidence | The rule already exists in authoritative artifacts; this session should not duplicate it as learn topic policy. |
| O2 | observation | observation | None | Current change artifacts | The missing `docs/changes` files are explained by existing artifact-local records. |
| O3 | observation | observation | None | Current change-local review records | The code-review records are present because material findings triggered detailed review handling. |
| O4 | observation | observation | Candidate process-follow-up only if the contributor confirms a recurring discoverability problem | Contributor question | One event is not enough evidence for a durable lesson or artifact update. |
| O5 | observation | observation | None | Contributor clarification plus current plan, spec, and test-spec records | SR-1 existed, but it was minor and non-blocking; current workflow does not require detailed `docs/changes` review files for non-material notes that are resolved artifact-locally. |

Contributor confirmation status: not confirmed for routing. This session records the observations only.

## Routing Results

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction or process follow-up routing: not created.

## No-Durable-Lesson Rationale

No durable lesson was captured because the governing workflow already covers the behavior, the current change artifacts contain the upstream review outcomes and SR-1 resolution, and the only new signal is a single discoverability question about the difference between minor non-blocking review notes and material findings.

## Follow-Ups

- None scheduled.
- If this confusion recurs, evaluate a focused workflow-doc clarification or a proposal for review-result discoverability.
