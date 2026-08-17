---
name: learn
description: >
  Capture durable lessons after implementation, review, verification, or incidents. Use when recurring mistakes, systemic gaps, or explicit retrospective work should guide future contributors.
argument-hint: [trigger, scope, session, or route result]
---

# Learning and retrospective capture

## Purpose

Record evidence-bound learning without becoming a policy, lifecycle, or destination owner.

## When to use

`learn` is periodic or explicitly invoked for repeated review findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem action, explicit maintainer request, incident response, contributor observation, cadence, or another stated trigger. capture the lesson immediately, create a scheduled follow-up, or record an explicit no-learn rationale. It blocks downstream only when a higher-priority artifact explicitly makes it blocking.

## When not to use

Do not run it by default, manufacture patterns, or bypass a destination owner.

## Inputs to read

Read the trigger, named artifacts, relevant prior learning, and the smallest decision-bearing evidence.

## Outputs

Produce a session record after Frame, justified topic guidance, owner-bound routes, and reconciled owner-result identities. Pre-session closeout remains in a contributor-visible tracked or review-visible surface owned by the trigger source.

## Handoff

- Normal next stage: none; record the session or route result and stop.
- Conditional next stages: send owner-bound work to the applicable skill or process; use `workflow` for governed routing.

## Operations and profiles

Select exactly one operation:

- `run-learn-session` (`LR1-session`): record a triggered session, topic effects, and owner-bound routes.
- `record-learn-route-result` (`LR0-route-result`): reconcile one route with an exact owner result.

An explicit direct `$learn` invocation selects `run-learn-session` unless the request explicitly identifies one current session, one stable route ID, and one owner result for `record-learn-route-result`. Pre-session trigger assessment and pre-session trigger closeout belong to the trigger owner.

An unknown, missing, combined, or ambiguous operation stops before writes. Operation selection does not grant contributor confirmation, destination mutation, workflow continuation, or external-system authority.

For `run-learn-session`, READ `references/session-method.md` exactly for `run-learn-session`, at most once. If it is missing, unreadable, escaped, stale, contradictory, or mixed-version, stop before session creation or dependent judgment and must not reconstruct it. `record-learn-route-result` does not load it.

## Resource map

- READ `references/session-method.md` exactly for `run-learn-session`, at most once. It owns phases, collision handling, topic effects, and routes.

Untriggered resources do not block `LR0-route-result`.

## Evidence and classification safety

The trigger permits a session; evidence controls capture. A single event remains `observation` or `no-durable-lesson` without a reusable pattern or systemic gap. Trigger type does not lower this standard.

Maintainer-driven rule adoption without accumulated evidence is not durable capture. Without repeated review findings, repeated incidents, failed smoke patterns, recurring validation gaps, or prior session evidence, classify the item as `direction`, not `durable-lesson`, and route it to proposal work. That proposal may later produce an ADR or another accepted authoritative artifact.

Contributor confirmation settles classification only, not destination mutation. Candidate classifications may be recorded; effects require confirmation.

Start from the trigger statement and named artifacts and exact sections first; use full-file reads only when narrower evidence is insufficient. Periodic learn sessions record time window start, time window end, and window basis. Never commit secrets or sensitive details.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Surfaces and ownership

After the Frame phase begins, the primary output is `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. Confirmed guidance may update `docs/learn/topics/<topic>.md`; create no templates, empty topics, or fixed taxonomy.

topic files are curated guidance and must not override `CONSTITUTION.md`, approved specs, accepted ADRs, architecture, workflow docs, skills, proposals, active plans, or an action-owning artifact. Preserve traceability when topic entries are revised, superseded, absorbed, or removed.

Behavior-changing work belongs to its action-owning artifact. `learn` records routes and owner-result identities; it cannot mutate destinations, bypass reviews, poll, or treat chat as completion. Historical sessions remain readable without implicit migration.

## Route-result recording

`record-learn-route-result` requires exact session identity and path, route ID, destination owner and basis, owner-result kind and identity, and session-write authority. The result kind must match the route's immutable required completion kind. Missing, stale, conflicting, duplicated, ambiguous, or mismatched input stops.

Update only the matching route. Record `complete` with `authoritative-artifact` or `durable-scheduled-follow-up`, or `blocked` with evidence. Do not change classification, confirmation, topics, other routes, or destinations. The same result is idempotent success; a different one requires fresh reconciliation.

## Stop conditions

Stop when trigger, scope, evidence, identity, path, confirmation, owner, authority, or required resource is insufficient; when a session collision or interrupted record cannot be classified safely; or when sensitive evidence cannot be summarized. Do not manufacture observations or repeat captured lessons.

## Claims this skill must not make

Do not claim new workflow policy or any authoritative artifact is accepted merely because learning was recorded. This skill does not prove destination approval, implementation, release, workflow completion, verification, branch readiness, PR readiness, CI status, or lifecycle closeout. Route through `workflow` when another governed stage is required.

## Expected output

```md
## Result

- Skill: learn
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
```

Also report operation; session identity and path; trigger and scope; confirmation result; session recording result; topic effects; route IDs and settlements; owner-result identities; next owner or handoff; claim limitations; and validation commands actually run when files changed.
