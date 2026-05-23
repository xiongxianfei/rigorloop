# Learn Session: Workstream Slice Model

## Frame

- Date: 2026-05-23
- Status: session-recorded; routing pending contributor confirmation
- Trigger: maintainer explicitly invoked `learn` after observing that the workflow does not define how to handle workstream A / workstream B style work.
- Trigger type: explicit maintainer observation after a large workflow-managed change.
- Scope: best practices for handling distinct workstreams inside a planned initiative when the workflow currently defines milestones, slices, and lifecycle closeout but not a first-class `workstream` artifact model.
- Session path: `docs/learn/sessions/2026-05-23-workstream-slice-model.md`

## Evidence Reviewed

- `specs/change-record-catalog-registration-and-bounded-read-model.md`
  - Defines two local workstreams:
    - Workstream A: evidence registration and selector routing.
    - Workstream B: bounded read/query model and stage-skill guidance.
  - Requires Workstream A as the first implementation slice.
  - Preserves existing workflow stage order, review status meanings, milestone state values, readiness semantics, and validation evidence requirements.
- `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
  - Implements Workstream A through M1 and M2.
  - Implements Workstream B through M3 and M4.
  - Uses M5 for lifecycle evidence and final closeout.
  - Records that both workstreams share one active plan and one change-local metadata surface.
- `docs/workflows.md`
  - Defines planned initiatives, implementation milestones, milestone states, repeated `implement -> code-review -> review-resolution` loops, and lifecycle-closeout sections.
  - Does not define `workstream` as a first-class workflow construct.
- Prior learn sessions:
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `docs/learn/sessions/2026-05-22-change-local-selector-routing.md`
  - `docs/learn/sessions/2026-05-22-change-yaml-reading-scope-after-compaction.md`

## Exclusions

- This session does not update `docs/workflows.md`, `specs/rigorloop-workflow.md`, skills, templates, validators, or generated outputs.
- This session does not change PR #87 readiness, hosted CI status, merge readiness, or plan lifecycle state.
- This session does not retroactively change how PR #87 is structured.

## Prior Learnings Reviewed

- `2026-05-07-milestone-closeout-vs-progress` already captures that combined or aggregate implementation slices need explicit closeout rules before milestone completion is claimed.
- `2026-05-22-change-local-selector-routing` captures the Workstream A failure mode: new deterministic change-local evidence requires selector routing and regression proof.
- `2026-05-22-change-yaml-reading-scope-after-compaction` captures the Workstream B failure mode: compact or preserved metadata still needs bounded read/query guidance.

## Observations

### O1: Workstream A and Workstream B were feature-local architecture groupings, not workflow-owned stages

The change-record catalog feature used `Workstream A` and `Workstream B` as a useful way to separate risk:

- A: selector and CI routing risk.
- B: query helper and stage-skill behavior risk.

The workflow handled those through ordinary milestones and review loops. It did not give either workstream an independent lifecycle state, metadata file, review log, or final readiness owner.

### O2: The plan successfully mapped workstreams to milestones, but the workflow lacks a named convention for that mapping

The active plan made the mapping concrete:

- M1 and M2 were Workstream A.
- M3 and M4 were Workstream B.
- M5 was lifecycle closeout.

That was workable, but the pattern is not defined in the general workflow. Future plans could accidentally blur the levels by treating a workstream as a milestone, treating a milestone as a workstream, or co-shipping independent risk groups after saying they should be separate.

### O3: Shared validation metadata made the workstreams look less separate than the implementation actually was

Both workstreams appended validation evidence to the same legacy `change.yaml`. That made the final change metadata look like one large command transcript even though implementation risk was separated across milestones.

This is not a failure of the workstream split. It is a limitation of the current validation evidence storage model.

### O4: Workstreams are most useful when they are planning labels with explicit boundaries, dependencies, and rollback rules

The useful parts of the Workstream A / Workstream B model were:

- each workstream had a distinct risk owner;
- the plan sequenced A before B;
- each workstream had separate code-review and review-resolution loops;
- M4 waited until M3 query-helper commands were stable;
- rollback surfaces were separable.

The confusing part was that the workflow had no standard vocabulary for how a workstream relates to milestones, validation evidence, and final closeout.

## Best Practices

### 1. Treat workstreams as planning groupings, not lifecycle stages

A workstream should group related milestones by risk, ownership, or rollback boundary. It should not replace workflow stages such as `spec`, `plan`, `implement`, `code-review`, `verify`, or `pr`.

Recommended shape:

```text
Workstream A: selector/CI routing
  M1: registered evidence routing
  M2: unregistered evidence debt and deferrals

Workstream B: query/skill behavior
  M3: query helper
  M4: skill guidance

Lifecycle closeout:
  M5: explain-change, verify, PR handoff
```

### 2. Give each workstream an explicit boundary table in the plan

For each workstream, name:

- owned files/components;
- risk class;
- dependencies;
- first milestone;
- last milestone;
- validation family;
- rollback surface;
- what it must not claim.

This keeps “same feature” from becoming “same implementation slice.”

### 3. Keep milestone state as the executable unit

The workflow already knows how to review and close milestones. Workstreams should not add a second state machine unless an approved workflow/spec change defines one.

Good:

```text
M2 state: closed
Workstream A status: complete because M1 and M2 are closed
```

Avoid:

```text
Workstream A state: closed
M1/M2 state: unclear
```

### 4. Review and rollback by workstream boundary

Use workstreams to decide review focus and rollback strategy:

- Workstream A review asks: did selector routing remain deterministic and safe?
- Workstream B review asks: do bounded reads answer the right questions without hiding evidence?

Rollback should be able to revert B without breaking A whenever the proposal says the risks are separate.

### 5. Do not use shared `change.yaml` size as evidence that workstreams were blurred

A large `change.yaml` can mean the validation evidence model is verbose, not that workstreams were poorly separated.

For workstream separation, inspect:

- milestone boundaries;
- commits;
- review records;
- tests;
- rollback notes;
- implementation dependencies.

For metadata verbosity, route a separate compact-write or validation-evidence aggregation proposal.

### 6. Add a workflow follow-up if this pattern will recur

If RigorLoop expects more large initiatives with multiple risk families, the owning artifact should define a lightweight workstream convention in workflow guidance or plan examples.

Candidate convention:

```text
Workstreams are optional plan-level groupings over milestones.
They may define sequencing and rollback boundaries.
They do not own lifecycle state; milestones do.
The active plan must map each workstream to concrete milestones and validation families.
```

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record | Maintainer question and feature evidence | This explains the current mismatch between feature-local terminology and workflow-owned stages. |
| O2 | process-follow-up | candidate process-follow-up | Possible workflow/spec or plan-template update | Confirmation pending | A general workstream convention would change workflow guidance, so learn should not route it unilaterally. |
| O3 | observation | observation | Possible separate compact-write proposal | Current `change.yaml` evidence | Metadata verbosity is related but belongs to a different storage/write concern. |
| O4 | direction | candidate direction | Proposal or workflow/spec amendment if maintainer confirms | Confirmation pending | Best practices are clear enough to propose, but not yet authoritative workflow policy. |

Contributor confirmation status: pending for authoritative routing. The maintainer explicitly asked for best practices, but has not yet confirmed a workflow/spec/template update.

## Routing Results

- Session record: created.
- Topic update: not performed.
- Authoritative artifact update: not performed.
- Candidate follow-up: define an optional workstream convention in `docs/workflows.md`, `specs/rigorloop-workflow.md`, and/or the example plan template after maintainer confirmation.

## No-Policy Rationale

This session identifies a reusable planning convention, but `learn` does not own workflow policy. If the convention should become required or recommended behavior, route it through the workflow/spec/template owner.
