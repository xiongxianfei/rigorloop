# Learn Session: Review Approval Status Sync

## Frame

- Trigger: maintainer explicitly invoked `learn` after `proposal-review` approved `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` and the final output suggested manually changing proposal `Status` from `draft` to `accepted`.
- Trigger type: maintainer request / contributor observation.
- Scope: whether an approved formal review result should cause the reviewed artifact status to be updated automatically or by the reviewer, and how that relates to existing artifact status vocabulary.
- Session record path: `docs/learn/sessions/2026-05-12-review-approval-status-sync.md`.

## Evidence Reviewed

- Maintainer statement: "`In my opinion, it the review skill give a approved result, then the document status should set to approved. Of course, we can review it manually to change the status.`"
- `AGENTS.md` says proposal, spec, test-spec, architecture, and ADR status lives inside the artifact, not in PR state or chat-only review outcomes.
- `AGENTS.md` says durable current states include `accepted`, `approved`, and `active`.
- `docs/workflows.md` lifecycle table says proposal settlement state is `accepted`, while spec and architecture settlement state is `approved`.
- `CONSTITUTION.md` says lifecycle-managed top-level artifacts keep status inside the artifact as tracked source of truth.
- `CONSTITUTION.md` says `reviewed` is transitional review output rather than a durable relied-on state.
- `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` remains `Status: draft` after clean proposal-review approval.

## Explicit Exclusions

- This session does not change proposal, spec, workflow, or skill policy.
- This session does not update the proposal status.
- This session does not create topic guidance because the observation is a maintainer direction, not an accumulated durable lesson.
- This session does not claim downstream `spec`, `plan`, implementation, verify, or PR readiness.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`
- `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`

These sessions show recurring confusion around where review outcomes and durable status are recorded, but they do not already settle whether a clean approved review should automatically edit artifact status.

## Observations

### O1: Review approval and artifact status can drift immediately after clean review

The proposal-review result was `approved`, but the reviewed proposal still had `Status: draft`. The reviewer output suggested a manual edit before downstream reliance. That leaves a small handoff gap: the chat review outcome and tracked artifact status disagree until someone updates the artifact.

Evidence:

- `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` has `Status: draft`.
- The proposal-review output said `Review status: approved`.
- `CONSTITUTION.md` and `AGENTS.md` make tracked artifact status the durable source of truth, not chat-only review output.

### O2: Existing vocabulary distinguishes proposal settlement from review approval wording

The maintainer phrasing says the document status should be set to `approved`, but current workflow guidance says proposal settlement uses `accepted`, while specs and architecture use `approved`.

Evidence:

- `docs/workflows.md` lifecycle table lists Proposal settlement as `accepted`.
- `docs/workflows.md` lifecycle table lists Spec and Architecture settlement as `approved`.
- `AGENTS.md` allows durable current states `accepted`, `approved`, and `active`, depending on artifact type.

### O3: This is a direction for an authoritative workflow or skill change

If review skills should edit reviewed artifacts after clean approval, or should require the artifact status update before reporting approval, that changes stage behavior and artifact lifecycle handling. The owning artifact would be a proposal/spec/skill/workflow update, not a learn topic entry.

Evidence:

- The learn skill says maintainer-driven rule adoption without accumulated evidence is `direction`, not durable topic guidance.
- The proposed behavior would affect review skill behavior and lifecycle-managed artifact status.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | direction | direction | Candidate proposal or spec/skill update for review approval status synchronization | Maintainer statement in trigger | The maintainer expressed a desired behavior change, and the evidence shows a real drift point, but the rule is not yet authoritative. |
| O2 | observation | observation | None | Artifact evidence | This records the current vocabulary mismatch risk: proposals use `accepted`, while some review statuses use `approved`. |
| O3 | direction | direction | Action-owning artifact needed before behavior changes | Learn skill contract and workflow evidence | The behavior would alter review-stage responsibilities and cannot be made authoritative by a learn topic. |

## Routing Results

- No topic file was created.
- No authoritative artifact was changed.
- Candidate follow-up: create or extend a proposal for review approval status synchronization if the maintainer wants the behavior to become workflow policy.

Candidate follow-up question for that owning artifact:

```text
When a formal review returns an approving result, should the review skill update the reviewed artifact status itself, require the status update before reporting downstream readiness, or only report the required status transition?
```

The follow-up should preserve current artifact-specific vocabulary unless an accepted proposal changes it:

- proposals settle as `accepted`;
- specs and architecture settle as `approved`;
- plans may use plan-owned lifecycle/status language.

## No Durable Lesson Rationale

No durable topic lesson was captured. The maintainer observation is actionable direction, but it would change review skill behavior and artifact lifecycle handling. That belongs in an authoritative proposal/spec/skill update rather than `docs/learn/topics/`.

## Follow-Ups

- Optional follow-up proposal: review approval status synchronization across formal review skills.
- No downstream stage is started by this learn session.
