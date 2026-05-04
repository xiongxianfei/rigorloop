# Learn Artifact Model

## Status

- approved

## Related proposal

- [Optimize Learn Skill](../docs/proposals/2026-05-03-optimize-learn-skill.md)

## Goal and context

This spec defines the contributor-visible artifact model and routing behavior for the `learn` skill. It replaces the temporary learn-recording surfaces currently described in the workflow contract with a single `docs/learn/` namespace, an evidence-bound session process, contributor-confirmed classification, curated topic guidance, and action routing into the authoritative artifact that owns the resulting change.

## Glossary

- learn session: a periodic, incident-driven, contributor-observed, or explicitly requested `learn` run that examines evidence and records what was or was not learned.
- session record: the dated historical record for one learn session under `docs/learn/sessions/`.
- topic file: a curated, topic-organized learning file under `docs/learn/topics/`.
- durable lesson: reusable guidance supported by evidence that future contributors should be able to find.
- observation: evidence-bound context surfaced during a learn session that does not yet justify durable guidance or action.
- primary classification: exactly one required classification assigned to each observation.
- secondary route: an optional derivative action or destination that follows from the primary classification without changing it.
- action-owning artifact: the authoritative artifact that must change when a lesson changes behavior, workflow, validation, architecture, skill behavior, examples, or decisions.
- contributor confirmation: a recorded confirmation or adjustment by the contributor or maintainer before candidate classifications are routed into topic files or action-owning artifacts.
- no-learn rationale: the recorded reason a triggered learn session did not produce durable lessons.
- single event: one isolated change, review finding, incident, command failure, or maintainer request without additional evidence of recurrence, reusability, or systemic gap.
- systemic gap: a missing, misleading, or insufficient contract, process, validation surface, or artifact boundary that can reasonably recur beyond the immediate event.

## Examples first

### Example E1: periodic learn creates a session and topic guidance

Given a cadence learn session reviews several proposal reviews from the same quarter
And multiple reviews show evidence that proposal follow-ups were recorded in untracked aspirational lists
When the contributor confirms the final primary classification as `durable-lesson`
And confirms `process-follow-up` as a secondary route
Then the session record is written under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`
And the relevant `docs/learn/topics/<topic>.md` entry links back to the session
And the follow-up is routed to a linked issue, active plan, or proposal instead of `docs/roadmap.md`.

### Example E2: maintainer-requested single event produces no durable lesson

Given a maintainer explicitly requests a learn session for one unusual review comment
And the evidence shows only one isolated event with no reusable pattern or systemic gap
When classification occurs
Then the session records `no-durable-lesson` with a no-learn rationale
And no topic file or action-owning artifact is updated.

### Example E3: artifact update owns behavior change

Given a learn session finds repeated evidence that the `verify` checklist misses a required workflow gate
When the contributor confirms the final primary classification as `artifact-update`
Then the affected authoritative `verify` skill or workflow artifact is updated
And the learn session links to that update
And any topic entry summarizes the lesson without becoming the source of truth for the checklist behavior.

### Example E4: no confirmation means no routing

Given a learn session produces candidate classifications
And no contributor confirmation is available
When the session is closed
Then the session record may preserve the candidate classifications
But topic files, ADRs, proposals, follow-ups, and action-owning artifacts are not updated from those candidates.

### Example E5: topic guidance is absorbed into an authoritative artifact

Given a topic entry once summarized a recurring validation lesson
And a later workflow spec update fully absorbs that guidance
When the topic file is curated
Then the topic entry may be revised, removed, or marked superseded
And traceability is preserved by linking the absorbing artifact, linking the session that explains the change, or recording the rationale in the topic-file edit or explain-change artifact.

### Example E6: explicit invocation uses bounded evidence

Given a contributor invokes `learn` for a named review artifact
When the relevant classification depends only on that review and one workflow section
Then the skill reads the trigger, named artifact, relevant learn indexes or topic files if present, and the exact workflow section needed
And it does not full-read every governance artifact by default.

### Example E7: periodic frame records the selected window

Given a periodic learn session covers April 2026
When the Frame phase records the session scope
Then it records time window start `2026-04-01`
And time window end `2026-04-30`
And window basis `calendar month`.

## Requirements

R1. `learn` MUST remain a periodic or explicitly invoked retrospective action, not a default final per-change stage.

R2. Any `learn` invocation that reaches the `Frame` phase MUST create or update a tracked session record at `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.

R2a. The session-record requirement in `R2` MUST apply even when the session produces no durable lesson.

R3. Durable topic guidance from learn sessions MUST use `docs/learn/topics/<topic>.md` as the canonical topic-file path.

R4. New learn sessions after this spec is adopted MUST NOT use `docs/learnings/**` or `docs/retrospectives/**` as canonical learn-session or learn-topic surfaces.

R5. The repository MAY include `docs/learn/README.md` as a lightweight namespace index that explains `sessions/` and `topics/`, but the first implementation MUST NOT add session or topic templates.

R6. The first implementation MUST NOT pre-create empty topic files or a fixed topic taxonomy.

R7. A topic file MUST be created only when at least one confirmed durable lesson justifies that topic.

R8. The session record MUST be the primary output of a learn session and MUST link to all derivative topic files, action-owning artifact updates, ADRs, proposals, issues, active-plan follow-ups, or no-learn rationales that result from the session.

R9. A session record MUST identify the trigger, trigger type, scope, evidence in scope, explicit exclusions, prior learnings reviewed, observations, classification decisions, secondary routes, routing results, and no-learn rationale when applicable.

R10. A learn session MUST proceed through four ordered phases: `Frame`, `Observe`, `Classify`, and `Route`.

R11. The `Frame` phase MUST establish the trigger, trigger type, scope, evidence in scope, exclusions, prior learnings reviewed, and the session-record path.

R11a. For periodic learn sessions, the `Frame` phase MUST record the selected time window start date, end date, and basis.

R12. The `Observe` phase MUST bind every observation to evidence and MUST record when no observations were found.

R13. The `Observe` phase MUST check for already-captured lessons before proposing new durable guidance.

R14. The `Classify` phase MUST classify each observation using exactly one primary classification from this set: `observation`, `durable-lesson`, `artifact-update`, `decision`, `direction`, `process-follow-up`, or `no-durable-lesson`.

R15. The `Classify` phase MAY record secondary routes when one observation requires derivative actions or destinations beyond the primary classification, but it MUST preserve one final primary classification for each observation.

R16. The session record MUST include a classification decisions record with observation ID, proposed primary classification, final primary classification, secondary routes, confirmed-by value, and rationale for every routed observation.

R17. Routing MUST NOT proceed for an observation until that observation has a final contributor-confirmed classification.

R18. If contributor confirmation is unavailable, the session MAY record candidate classifications, but it MUST NOT update topic files, ADRs, proposals, follow-ups, or action-owning artifacts from those candidates.

R19. The `Route` phase MUST route `observation` items to the session record only.

R20. The `Route` phase MUST route `durable-lesson` items to the relevant topic file with a date, short lesson, source-session link, primary classification, and secondary routes when present.

R21. The `Route` phase MUST route `artifact-update` items to the affected authoritative artifact and link the update from the session record.

R22. The `Route` phase MUST route `decision` items to the relevant ADR or decision artifact and link that artifact from the session record and any relevant topic entry.

R23. The `Route` phase MUST route `direction` items to a proposal or trackable follow-up and MUST NOT encode the direction as policy in a topic file.

R24. The `Route` phase MUST route `process-follow-up` items to a linked issue when an issue tracker is available, to the active plan when one owns the work, or to a proposal when no tracker or active plan exists.

R25. The `Route` phase MUST route `no-durable-lesson` items to the session record with a no-learn rationale and whether any follow-up was scheduled.

R25a. Review-visible no-record surfaces MUST be allowed only for pre-session trigger closeout when `learn` does not actually run as a session.

R26. A maintainer request, cadence trigger, incident response, contributor observation, or explicit invocation MUST be sufficient to trigger a learn session.

R27. Trigger type MUST NOT lower the evidence standard for capturing a durable lesson.

R28. A single event MUST remain classified as `observation` or `no-durable-lesson` unless the evidence shows a reusable pattern or systemic gap.

R29. Maintainer-driven rule adoption that lacks accumulated evidence MUST be routed to proposal work that may later produce an ADR, not captured as a durable learn lesson.

R30. Empty learn sessions MUST be valid outcomes when evidence does not support durable lessons.

R31. Topic files MUST be curated guidance, not authoritative workflow, product, architecture, validation, skill, or implementation contracts.

R32. Topic files MUST NOT override `CONSTITUTION.md`, approved specs, accepted ADRs, approved architecture docs, workflow docs, skill files, accepted proposals, active plans, or affected action-owning artifacts.

R33. When a lesson changes behavior, workflow, architecture, validation, skill behavior, examples, or decisions, the affected authoritative artifact MUST be updated; a topic file MAY link to that update but MUST NOT be the source of truth.

R34. Topic entries MAY be added, revised, superseded, absorbed into an authoritative artifact, or removed as obsolete.

R35. Removing or absorbing a topic entry MUST preserve traceability through at least one of: a session-record link, an authoritative-artifact link, a topic-file edit rationale, or an explain-change rationale.

R36. Learn evidence collection MUST start from compact summaries and targeted evidence before broad reads.

R37. Every learn session MUST start from the trigger statement and named artifacts.

R38. Every learn session MUST check relevant `docs/learn/` index, session, and topic material when present and relevant to the stated trigger or topic.

R39. Learn sessions MUST check whether governance or workflow context is needed, but MUST NOT full-read every governance or workflow artifact by default.

R40. Governance, workflow, and source-of-truth artifacts MUST be read in exact sections first and full-read only when classification or routing cannot be justified from narrower evidence.

R41. Periodic learn sessions MUST inspect changes in the selected time window, including proposals, plans, change packs, ADRs, recent commits to canonical surfaces, and generated-output or validation records when relevant.

R42. Incident learn sessions MUST inspect the incident report, related artifacts, affected specs or plans, review or verify findings, and relevant postmortem action records when present.

R43. Explicitly invoked learn sessions MUST inspect artifacts named by the user and artifacts implied by the stated pattern.

R44. `docs/learn/sessions/**` and `docs/learn/topics/**` MUST be classified as known learn artifact paths by repository validation selection in the first implementation slice, even if validation remains lightweight.

R45. Implementing this spec MUST update affected workflow-governance surfaces or record them as unaffected with rationale or deferred with owner and follow-up in a contributor-visible tracked or review-visible surface.

R46. Implementing this spec MUST update the current temporary learn-recording rule in `specs/rigorloop-workflow.md` and its matching test spec so the workflow contract no longer points contributors to temporary surfaces as the final learn model.

R47. Changes to canonical `skills/learn/SKILL.md` MUST be propagated to generated `.codex/skills/` and public adapter output through existing generators, not by hand-editing generated files.

## Inputs and outputs

- inputs:
  - trigger statement and trigger type;
  - user-named artifacts;
  - relevant prior session records, topic files, or `docs/learn/README.md` when present;
  - bounded governance, workflow, spec, plan, ADR, review, verify, incident, commit, generated-output, or validation evidence selected by trigger type;
  - contributor confirmation or adjustment for classification decisions.
- outputs:
  - session record under `docs/learn/sessions/YYYY-MM-DD-<slug>.md` when a learn invocation reaches `Frame`;
  - topic file entries under `docs/learn/topics/<topic>.md` only when durable topic guidance is confirmed;
  - updated action-owning artifacts when lessons change authoritative behavior or contracts;
  - ADRs, proposals, issues, or active-plan follow-ups when routing requires them;
  - no-learn rationale when no durable lesson is captured.

## State and invariants

- `learn` remains retrospective and does not own `docs/plan.md`, plan-body lifecycle state, review-resolution closeout, verification readiness, PR readiness, or CI status.
- Session records are the historical thread for learn sessions.
- Topic files are the curated discovery layer for durable lessons.
- Action-owning artifacts remain the source of truth for behavior and contract changes.
- One record type has one canonical surface after adoption: session records under `docs/learn/sessions/`, topic guidance under `docs/learn/topics/`, and actions in the artifact or tracker that owns them.
- A learn trigger establishes that a session may run; evidence determines what the session captures.
- Chat-only notes are not sufficient for tracked learn outputs, follow-ups, or no-learn rationales when the workflow requires a contributor-visible record.

## Error and boundary behavior

- invalid path: a learn artifact path that does not match `docs/learn/sessions/YYYY-MM-DD-<slug>.md`, `docs/learn/topics/<topic>.md`, or the optional `docs/learn/README.md` is not a canonical learn artifact after adoption.
- missing `docs/learn/`: the first learn session may create the needed directory path, and no empty topic taxonomy is required before then.
- no observations: the session records that no observations were found and does not create topic guidance.
- no durable lesson: the session record records a no-learn rationale and whether any follow-up was scheduled.
- pre-session closeout: a triggering review-visible surface may record a scheduled follow-up, deferral, or no-learn rationale only when `learn` does not actually run as a session.
- no contributor confirmation: candidate classifications may remain in the session, but routing stops for those observations.
- no issue tracker and no active plan: a process follow-up is opened as a proposal rather than added to `docs/roadmap.md`.
- conflicting authority: if a topic entry conflicts with a higher-priority authoritative artifact, the higher-priority artifact governs and the topic entry is revised, removed, or absorbed with traceability.
- insufficient evidence: the observation remains `observation` or `no-durable-lesson`; the skill does not manufacture durable guidance.
- private incident details: the session records only the minimum contributor-visible evidence needed and omits secrets or sensitive details.

## Compatibility and migration

- Existing pre-adoption learning notes outside `docs/learn/` may remain in place unless a later approved migration plan relies on them as current guidance.
- New learn sessions after adoption use `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.
- New topic guidance after adoption uses `docs/learn/topics/<topic>.md`.
- The implementation updates `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, and affected skill guidance only where their guidance is affected; unaffected surfaces are recorded with rationale.
- Rollback restores the prior temporary-surface workflow rule and removes or supersedes any new learn-path selector classification introduced by the implementation.
- No runtime storage, network service, external database, release packaging change, or issue-tracker integration is required by this spec.

## Observability

- Learn observability is artifact-based.
- Session records show trigger, scope, evidence, observations, classification decisions, routing, derivative artifact links, and no-learn rationale.
- Topic entries show date, lesson summary, source-session link, primary classification, and secondary routes when present.
- Action-owning artifacts, ADRs, proposals, issues, and active-plan follow-ups are linked from the session record.
- Repository validation selection exposes `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths.

## Security and privacy

- Learn outputs do not create new authentication or authorization behavior.
- Learn outputs must not commit secrets, credentials, tokens, private keys, private incident data, or unnecessary machine-local details.
- Incident-triggered sessions should summarize sensitive evidence and link to appropriate reviewed artifacts when direct details should not be exposed.
- Generated output must be refreshed through repository-owned generators when canonical skill changes require it.

## Accessibility and UX

- No application UI is introduced.
- Contributor-facing paths must use the single `docs/learn/` parent namespace so session records and topic guidance are distinguishable by subdirectory instead of visually similar sibling names.
- Session and topic headings should be stable enough for reviewers to find trigger, evidence, classification, routing, and source links without requiring a separate template in the first implementation.

## Performance expectations

- Learn sessions use bounded evidence collection by default.
- Full governance, workflow, spec, or generated-output reads are reserved for cases where targeted evidence is insufficient.
- Validation for new learn paths may be lightweight in the first implementation, but selector routing must recognize the paths so targeted validation remains predictable.
- The first implementation should avoid adding persistent caches, background jobs, or external indexing services.

## Edge cases

1. A maintainer requests a learn session for a single unusual event with no reusable evidence; the session records `no-durable-lesson`.
2. A repeated finding already has a topic entry and an updated authoritative artifact; the session links the existing lesson and does not duplicate it.
3. One observation suggests a durable lesson and a future process follow-up; the session records primary classification `durable-lesson` and secondary route `process-follow-up`.
4. A topic entry becomes obsolete after an approved spec absorbs the guidance; curation removes or revises the entry with traceability.
5. A process follow-up has no issue tracker and no active plan owner; the follow-up becomes a proposal.
6. A session cannot obtain contributor confirmation; it records candidates and stops before routing.
7. A topic file starts to contradict a higher-priority spec or ADR; the topic file is corrected or removed and links the governing artifact.
8. A small explicit invocation names one artifact; the skill reads only the relevant evidence needed for classification and routing.
9. A periodic session finds no observations in the selected time window; it records that empty outcome.
10. A canonical skill update changes generated outputs; generated `.codex/skills/` and adapter files are refreshed through generators.

## Non-goals

- Making `learn` mandatory for every change.
- Making `learn` a lifecycle bookkeeping owner for plans, review-resolution closeout, verification, PR readiness, or CI status.
- Creating session or topic templates in the first implementation.
- Pre-creating a learn topic taxonomy.
- Building an issue tracker, project-management system, background indexer, or automated lesson triage service.
- Migrating all existing historical notes into `docs/learn/`.
- Treating topic files as policy, specifications, architecture decisions, workflow contracts, or skill contracts.
- Capturing durable lessons from isolated single events without reusable evidence or systemic gap evidence.
- Letting the skill make final primary classification and routing decisions without contributor confirmation.
- Bypassing downstream review for derivative ADRs, proposals, specs, architecture docs, workflow changes, or skill behavior changes.

## Acceptance criteria

- A reviewer can identify the canonical learn session path and topic path without seeing `docs/learnings/**` as an allowed sibling surface.
- A reviewer can trace every routed observation from evidence to proposed primary classification, final primary classification, secondary routes, confirmer, rationale, and derivative artifacts.
- A maintainer-requested session with only one isolated event can close with `no-durable-lesson`.
- A learn-triggered behavior change updates the authoritative artifact that owns the behavior instead of relying on a topic entry as policy.
- A process follow-up without an issue tracker or active plan becomes a proposal rather than a roadmap entry.
- Topic entry removal or absorption preserves traceability through a session link, authoritative-artifact link, topic-file rationale, or explain-change rationale.
- A small explicit learn invocation can complete without full-reading every governance artifact.
- Selector-selected validation treats `docs/learn/sessions/**` and `docs/learn/topics/**` as known learn artifact paths.
- The temporary learn-recording rule in the workflow spec is updated when this spec is implemented.
- Generated skill and adapter output are refreshed through generators if canonical `skills/learn/SKILL.md` changes.

## Open questions

- None.

## Next artifacts

- `spec-review` for this contract.
- Test spec updates for learn artifact routing, evidence standards, selector behavior, and workflow temporary-surface retirement.
- Architecture or ADR only if review determines the learn namespace, selector behavior, or governance routing introduces a durable architecture decision beyond workflow artifact routing.
- Execution plan if implementation touches the workflow spec, test spec, skill source, governance summaries, selector tests, and generated outputs.

## Follow-on artifacts

- Plan: [Learn Artifact Model Implementation Plan](../docs/plans/2026-05-04-learn-artifact-model.md)
- Test spec: [Learn Artifact Model test spec](learn-artifact-model.test.md)

## Readiness

Approved after `spec-review`. The implementation plan passed `plan-review`, and `specs/learn-artifact-model.test.md` is the active proof-planning surface for implementation.
