# Learn Session: Follow-Up Register Activation and Closeout

## Frame

- Trigger: explicit maintainer invocation of `$learn` after questions about why `FU-004` was chosen while many follow-ups were open, why `FU-001` through `FU-003` were not closed, and after maintainer-directed closure of `FU-001` through `FU-003`.
- Trigger type: explicit maintainer retrospective / contributor observation.
- Scope:
  - `docs/follow-ups.md`
  - `specs/rigorloop-cli-lockfile.md`
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/spec-review-r2.md`
  - prior learn sessions about plan state drift, active plan pileup, and proposal-scope preservation
- Evidence in scope:
  - `docs/follow-ups.md` currently lists open `FU-004` through `FU-010` and closed `FU-001` through `FU-003`.
  - `FU-002` and `FU-003` were already completed by PR #62 but remained open until the maintainer challenged the state.
  - `FU-001` was closed by explicit maintainer decision.
  - `FU-004` was activated as the next spec without asking the maintainer to choose among several open follow-ups.
  - `spec-review-r1` found `SR1-F1`; the spec was revised; `spec-review-r2` closed `SR1-F1` and opened `SR2-F1`.
  - Current `review-resolution.md` records `SR2-F1` as open.
- Explicit exclusions:
  - This session does not close `SR2-F1`.
  - This session does not approve the lockfile spec.
  - This session does not update workflow policy, skills, validators, or topic files.
  - This session does not create a new proposal or plan.
  - This session does not claim branch readiness or PR readiness.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-14-active-plan-pileup-before-pr-closeout.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`
  - `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`
- Session record path: `docs/learn/sessions/2026-05-15-follow-up-register-activation-and-closeout.md`

## Observe

### O1: Follow-up activation was technically defensible but not user-selected

`FU-004` was chosen because durable `rigorloop.lock` writes were a direct dependency left unresolved by the merged CLI first slice. That choice was defensible from dependency order: the first slice already emits `planned_lockfile`, and the proposal explicitly blocks durable lockfile writes until a lockfile spec exists.

However, the open register also contained other valid next user-value slices such as `new-change`, `status`, `validate`, and npm release hardening. The maintainer asked why `FU-004` was chosen, which shows the activation decision was not obvious enough from the request "start new spec from follow-ups.md".

Evidence:

- `docs/follow-ups.md` had multiple open entries when the spec was started.
- The maintainer later asked why `FU-004` was chosen.
- The assistant answer acknowledged an assumption instead of a maintainer-selected priority.

### O2: Completed follow-ups remained open after PR #62

`FU-002` and `FU-003` described first-slice CLI package architecture/command contracts and first Codex init implementation. PR #62 completed those surfaces, but they remained listed as open until the maintainer asked why they were not closed.

Evidence:

- `docs/follow-ups.md` now records `FU-002` and `FU-003` as closed by PR #62.
- The maintainer asked why `FU-001` through `FU-003` were not closed.
- The assistant acknowledged that `FU-002` and `FU-003` should have been cleaned up after PR #62 lifecycle closeout or before starting `FU-004`.

### O3: FU-001 closure was a maintainer decision, not evidence-derived completion

`FU-001` was unrelated to the CLI first-slice work. It was closed after the maintainer explicitly said it could close. That is valid as maintainer direction, but it is not evidence that a token-friendliness proposal was completed.

Evidence:

- `docs/follow-ups.md` closed entry for `FU-001` says "Closed by maintainer request; no active proposal needed."
- No proposal or implementation artifact completed `FU-001`.

### O4: Follow-up register wording can go stale within the review loop

After `spec-review-r2`, `review-resolution.md` records `SR1-F1` as resolved and `SR2-F1` as open. The current `FU-004` row still mentions `spec-review-r1` and `SR1-F1` as the next action. That means even the follow-up pointer can become stale during a fast review/revision loop.

Evidence:

- `docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md` says `SR1-F1` is resolved and `SR2-F1` remains open.
- `docs/follow-ups.md` still says `spec-review-r1` requested changes for `SR1-F1`.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Candidate process-follow-up | Maintainer question plus follow-up register evidence | The activation choice was defensible but user priority was ambiguous. One event is not enough to change policy. |
| O2 | process-follow-up | candidate process-follow-up | Possible follow-up register hygiene checklist after PR lifecycle closeout or before activating a new follow-up | Contributor confirmation pending | Completed follow-ups remaining open caused maintainer correction; routing a checklist or validator needs confirmation. |
| O3 | observation | observation | None | Maintainer decision and closed follow-up row | This records that the closure was owner direction rather than completed work evidence. |
| O4 | artifact-update | candidate artifact-update | Update `FU-004` row to name `SR2-F1` as current blocker | Contributor confirmation pending | The register appears stale relative to review-resolution, but learn must not route artifact updates without confirmation. |

## Route

- Created session record: `docs/learn/sessions/2026-05-15-follow-up-register-activation-and-closeout.md`
- No topic file was created.
- No workflow, spec, validator, skill, proposal, plan, or follow-up entry was updated by this learn session.
- Candidate artifact update, pending contributor confirmation: update `FU-004` to say `SR1-F1` is resolved and `SR2-F1` is the current open spec-review blocker.
- Candidate process follow-up, pending contributor confirmation: add a small follow-up-register hygiene step before activating a new follow-up or after PR lifecycle closeout records closed follow-up work.

## No-Durable-Route Rationale

The observations are useful but do not yet justify a new durable topic or authoritative workflow rule. The pattern overlaps with existing lifecycle-state drift lessons: state surfaces must be synchronized when real work completes or review state changes. A follow-up-register-specific rule or validator would need contributor confirmation and an action-owning artifact.

## Follow-Ups

- Candidate, not routed: update `FU-004` to reflect `SR2-F1` as the current blocker.
- Candidate, not routed: define a lightweight follow-up register hygiene check in an owning workflow or validator artifact if this recurs.
