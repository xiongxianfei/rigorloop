---
name: learn
description: >
  Capture durable lessons after implementation, review, verification, or incidents. Use when the workflow revealed recurring mistakes, spec gaps, architecture discoveries, testing improvements, CI gaps, or process changes that should guide future agents.
argument-hint: [feature name, completed plan, incident, review findings, or retrospective]
---

# Learning and retrospective capture

You are running a learn session only when learning is periodic or explicitly invoked by cadence, incident response, contributor observation, repeated review findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem action, explicit maintainer request, or another stated trigger.

`learn` is periodic or explicitly invoked. It is not the default final stage for every change, and it blocks downstream only when a higher-priority artifact explicitly makes it blocking. When a trigger occurs, capture the lesson immediately, create a scheduled follow-up, or record an explicit no-learn rationale in the appropriate surface.

Do not fabricate lessons. The trigger decides whether a session may run; evidence decides what the session captures. A single event remains `observation` or `no-durable-lesson` unless the evidence shows a reusable pattern or systemic gap. Maintainer request, incident response, contributor observation, cadence, and explicit invocation do not lower the evidence standard for durable guidance.

## Output Surfaces

When a learn invocation reaches the Frame phase, create or update a tracked session record at `docs/learn/sessions/YYYY-MM-DD-<slug>.md`. This applies even when the session is empty or produces `no-durable-lesson`.

Use `docs/learn/topics/<topic>.md` only when contributor-confirmed durable guidance justifies a topic entry. Do not pre-create empty topic files, a fixed topic taxonomy, session templates, or topic templates.

The session record is the primary output. It links to every derivative topic entry, action-owning artifact update, ADR, proposal, issue, active-plan follow-up, scheduled follow-up, or explicit no-learn rationale produced by the session.

The boundary is simple: topic files are curated guidance, not policy. They must not override `CONSTITUTION.md`, approved specs, accepted ADRs, approved architecture docs, workflow docs, skill files, accepted proposals, active plans, or action-owning artifacts. If a lesson changes behavior, workflow, architecture, validation, skill behavior, examples, or decisions, update the action-owning artifact and link that update from the session record.

Pre-session trigger closeout is different from a learn session; pre-session trigger closeout may record a scheduled follow-up, deferral, or explicit no-learn rationale only when `learn` does not actually run as a session. Use a contributor-visible tracked or review-visible surface.

## Inputs To Read

Start from bounded evidence:

1. trigger statement and named artifacts;
2. relevant `docs/learn/README.md`, prior session records, and topic files when present and relevant;
3. compact summaries, headings, stable IDs, and exact sections first for governance, workflow, spec, plan, ADR, review, verify, incident, commit, generated-output, or validation evidence;
4. full-file reads only when narrower evidence is insufficient for classification or routing.

For periodic learn sessions, inspect changes in the selected time window when relevant, including proposals, plans, change packs, ADRs, recent commits to canonical surfaces, and generated-output or validation records.

For incident sessions, inspect the incident report, related artifacts, affected specs or plans, review or verify findings, and relevant postmortem action records when present. Summarize sensitive evidence; do not commit secrets, credentials, tokens, private keys, private incident data, or unnecessary machine-local details.

For explicit invocations, inspect artifacts named by the user and artifacts implied by the stated pattern.

## Four Phases

Run every learn session in this order: Frame, Observe, Classify, Route.

### Frame

Establish and record:

- trigger and trigger type;
- scope;
- evidence in scope;
- explicit exclusions;
- prior learnings reviewed;
- session record path under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.

For periodic learn sessions, also record time window start, time window end, and window basis.

### Observe

Examine the evidence for patterns, surprises, drift, and gaps. Every observation must be evidence-bound.

Before proposing durable guidance, check whether the lesson is already captured in a prior session, topic entry, action-owning artifact, ADR, proposal, active plan, or workflow artifact. If no observations are found, record that explicit no-observation result in the session record.

### Classify

Each observation has exactly one primary classification:

- `observation`
- `durable-lesson`
- `artifact-update`
- `decision`
- `direction`
- `process-follow-up`
- `no-durable-lesson`

An observation may also have secondary routes. Secondary routes are derivative actions or destinations and do not become additional primary classifications.

Record classification decisions with observation ID, proposed primary classification, final primary classification, secondary routes, confirmed-by, and rationale.

Contributor confirmation is required before routing. If confirmation is unavailable, record candidate classifications in the session record and stop before updating topic files, ADRs, proposals, follow-ups, or action-owning artifacts.

### Route

Route only contributor-confirmed final classifications:

- `observation`: keep in the session record only.
- `durable-lesson`: add or update the relevant topic file with date, short lesson, source-session link, primary classification, and secondary routes when present.
- `artifact-update`: update the affected authoritative artifact and link that update from the session record.
- `decision`: create or update the relevant ADR or decision artifact, then link it from the session record and any relevant topic entry.
- `direction`: open a proposal or trackable follow-up; do not encode direction as topic-file policy.
- `process-follow-up`: link an issue when an issue tracker exists, use the active plan when it owns the work, or open a proposal when no tracker or active plan owns it. Do not use `docs/roadmap.md` as the fallback for learn follow-ups.
- `no-durable-lesson`: record the no-learn rationale and whether any follow-up was scheduled in the session record.

## Topic Curation

Topic entries may be added, revised, superseded, removed, or absorbed into an authoritative artifact. When you remove, revise, or absorb an entry, preserve traceability through a session link, authoritative-artifact link, topic-file rationale, or explain-change rationale.

Topic files exist for discovery. Keep them concise and curated; do not let them become policy, workflow contracts, architecture decisions, validation contracts, or skill contracts.

## Generated Output Boundary

If this canonical skill changes, generated `.codex/skills/` output and public adapter output under `dist/adapters/`, including `.agents/skills`, `.claude/skills`, and `.opencode/skills`, must be refreshed through repository-owned generators. Do not hand-edit generated skill or adapter output.

## Rules

- Do not manufacture observations to justify a session.
- Do not capture durable lessons from isolated single events without reusable pattern or systemic gap evidence.
- Do not repeat already-captured lessons.
- Do not make final classification decisions unilaterally.
- Do not route without contributor confirmation.
- Do not bypass downstream review for derivative ADRs, proposals, specs, architecture docs, workflow changes, or skill behavior changes.
- Do not use `learn` as the authoritative owner of plan index state, plan-body lifecycle state, review-resolution closeout, verification readiness, PR readiness, or CI status.
- If nothing durable was learned, record the empty outcome honestly in the session record once Frame has occurred.

## Expected output

- session record path and status;
- trigger, scope, evidence reviewed, and exclusions;
- observations found, or explicit no-observation result;
- classification decisions and contributor confirmation status;
- routing results and derivative artifact links;
- no-learn rationale when no durable lesson was captured;
- follow-ups created, scheduled, or explicitly not needed;
- validation or generated-output commands run when this skill changed.
