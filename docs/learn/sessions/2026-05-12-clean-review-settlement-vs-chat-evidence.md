# Learn Session: Clean Review Settlement vs Chat Evidence

## Status

- captured

## Frame

- Date: 2026-05-12
- Trigger: explicit maintainer invocation asking how to handle this review-evidence issue: "spec-review approved in chat with no material findings, but no durable tracked review evidence exists and the spec still has Status: draft."
- Trigger type: explicit maintainer question / contributor observation.
- Scope:
  - clean formal review recording;
  - artifact-local lifecycle status settlement;
  - whether chat-only approval is enough evidence for downstream stages.
- Session path: `docs/learn/sessions/2026-05-12-clean-review-settlement-vs-chat-evidence.md`

## Evidence Reviewed

- `CONSTITUTION.md`
- `docs/workflows.md`
- `specs/formal-review-recording.md`
- `specs/downstream-status-settlement-before-reliance.md`
- `skills/spec-review/SKILL.md`
- `skills/architecture/SKILL.md`
- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`

## Exclusions

- No workflow, spec, skill, architecture, ADR, or plan policy update is made by this session.
- No learn topic entry is created.
- No detailed review record, review-log, or review-resolution file is created by this session.
- No claim is made that any current proposal, spec, architecture, plan, implementation, verification, or PR stage is ready.

## Prior Learnings Reviewed

- `docs/learn/README.md`
- `docs/learn/sessions/2026-05-05-review-record-placement.md`
- `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
- Existing topic files were checked for fit; no topic update is made because the governing workflow already owns the rule.

## Observations

### O1: Clean formal reviews do not need empty detailed review files by default

A required formal review with no material findings can remain lightweight. The normal settlement path is artifact-local when no detailed-record trigger applies. That means a clean `spec-review` does not automatically require a detailed review file, `review-log.md`, or an empty `review-resolution.md`.

Evidence:

- `CONSTITUTION.md` says clean required formal reviews with no material findings may settle in the reviewed artifact when no detailed-record trigger applies.
- `specs/formal-review-recording.md` says clean required reviews may be recorded through artifact-local settlement and that clean reviews recorded only this way do not require `review-log.md` or `review-resolution.md` solely for that review.
- `skills/spec-review/SKILL.md` says clean reviews remain lightweight and can settle artifact-locally when no detailed review trigger applies.

### O2: Chat-only approval is not enough durable lifecycle state when the reviewed artifact remains draft

Chat approval can explain what happened during the current conversation, but downstream stages should not treat chat-only review outcome as a replacement for tracked artifact state. If the spec still says `Status: draft`, later architecture or plan work has a legitimate blocker even if the chat said the review was clean.

Evidence:

- `CONSTITUTION.md` says chat-only reasoning stays subordinate to tracked repository artifacts once written guidance exists.
- `docs/workflows.md` says lifecycle-managed top-level artifacts keep their own tracked status, and chat-only review outcomes do not replace artifact-local lifecycle state.
- `specs/downstream-status-settlement-before-reliance.md` requires clear durable review and status evidence before downstream reliance.
- `skills/architecture/SKILL.md` maps spec-review approval with no unresolved material findings to spec `Status: approved` before architecture can rely on the spec as settled.

### O3: The practical fix is artifact-local settlement, not review-file boilerplate

For a clean `spec-review` with no material findings and no detailed-record trigger, the best repair is to update the reviewed spec itself: set the lifecycle status to `approved`, record readiness or handoff language, and optionally note the clean review in the artifact's follow-on or decision/history section if that artifact has one.

This gives durable tracked evidence without creating empty change-local review files. Detailed review records are reserved for material findings, blocking outcomes, reconstructed records, closeout evidence citations, explicit durable-record requests, or other governing triggers.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Existing governance evidence | The rule already exists in authoritative artifacts; this session should not duplicate it as topic-file policy. |
| O2 | observation | observation | None | Existing governance evidence plus maintainer question | The issue is a practical application of existing chat-vs-artifact precedence and downstream settlement rules. |
| O3 | observation | observation | Candidate artifact-update only if recurring confusion requires workflow or skill wording changes | Existing governance evidence plus maintainer question | The repair path follows existing rules. A new durable rule is not justified by this single event. |

Contributor confirmation status: not confirmed for routing. This session records the observations only.

## Routing Results

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction or process follow-up routing: not created.

## No-Durable-Lesson Rationale

No durable lesson or topic entry was created because the governing workflow already covers the behavior. The useful takeaway is operational: clean reviews do not need empty detailed review files, but clean review approval must be reflected in durable tracked artifact state before downstream stages rely on it.

## Best-Practice Answer

For a clean `spec-review` with no material findings:

1. Do not create empty detailed review files solely because the review happened.
2. Do update the spec's tracked lifecycle state when the review approves it, for example `Status: approved`.
3. Do record enough artifact-local readiness or handoff text for the next stage to rely on the spec.
4. Use detailed review records only when a material finding, blocking outcome, reconstructed record, explicit durable-record request, or another governing trigger applies.
5. Treat chat evidence as useful context, not durable workflow evidence, when it conflicts with or is absent from tracked artifact state.

In the reported case, the problem was not the missing review file. The problem was that the clean approval stayed in chat while the spec still said `Status: draft`.

## Follow-Ups

- None scheduled.
- If this confusion recurs, consider a focused update to `skills/spec-review/SKILL.md` or `docs/workflows.md` that emphasizes artifact-local status settlement immediately after clean approval.
