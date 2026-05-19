---
name: proposal
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create a decision-oriented change proposal before writing a feature spec or execution plan. Use after exploration has produced options or when the intended direction is clear enough to evaluate scope, value, risks, and non-goals.
argument-hint: [feature idea, selected option, problem statement, or issue number]
---

# Change proposal

You turn exploration into a reviewable direction. A proposal answers why this change, why now, and why this approach. It does not define every requirement or implementation task.

## Workflow role

- role_name: proposal
- stage: authoring
- upstream: user request, exploration, research, issue, or incident
- downstream: proposal-review
- summary: Author the proposal artifact recording problem, options, recommendation, scope, risks, and readiness.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present: `AGENTS.md`, `CONSTITUTION.md`, `VISION.md`, `docs/project-map.md`, `docs/workflows.md`, local specs or ADRs, related proposals, code, issues, incidents, and user feedback.

Workflow-wide rule: do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects; use portable defaults where safe; block on ambiguity.

## Evidence access

Read standing operating instructions when present, then use the smallest sufficient evidence set.

Default evidence:

- user request
- `VISION.md` when proposal fit matters
- `CONSTITUTION.md` for governance, source-of-truth, workflow, or release-policy changes
- related proposal only when superseding or extending it

Conditional evidence:

- `AGENTS.md` when present
- `docs/project-map.md` when architecture or repository orientation matters
- existing specs or ADRs when the proposal changes their direction
- `docs/workflows.md` when artifact placement or workflow routing matters
- code only when current behavior is part of the decision
- exploration, research, issues, incidents, or user feedback when the proposal relies on them

Bounded discovery is not evidence expansion. Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.

## Artifact placement

Prefer:

```text
docs/proposals/YYYY-MM-DD-slug.md
```

Do not overwrite an older proposal for a new initiative.

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table when that project-local file is present;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Required proposal sections

| Section | Purpose |
|---|---|
| Status | Current artifact lifecycle state. |
| Problem | User or system problem being solved. |
| Goals | Outcomes the change should produce. |
| Non-goals | Explicitly out-of-scope work. |
| Vision fit | Relationship to root `VISION.md` when that project-local file exists. |
| Context | Relevant product, architecture, workflow, repository, or operational background. |
| Options considered | At least three options, or a link to exploration that contains them. |
| Recommended direction | Selected approach and rationale. |
| Expected behavior changes | High-level observable behavior, not detailed requirements. |
| Architecture impact | Expected components, boundaries, and data flow touched. |
| Testing and verification strategy | Likely levels of test coverage and proof. |
| Rollout and rollback | Migration, flags, compatibility, fallback, or recovery. |
| Risks and mitigations | Product, technical, operational, security, and performance risks. |
| Open questions | What must be resolved before spec or architecture. |
| Decision log | Date, decision, reason, and alternatives rejected. |
| Next artifacts | Planned spec, architecture, plan, test-spec, or follow-up work while active. |
| Follow-on artifacts | Actual downstream artifacts or terminal disposition after settlement or closeout. |
| Readiness | Truthful next-stage status. |

Closed enum: proposal status

```text
draft
under review
accepted
rejected
abandoned
superseded
archived
```

If `Follow-on artifacts` appears before real follow-ons exist, write `None yet`.

## Vision fit

Include `Vision fit` in new or substantively revised proposals after the vision spec is adopted.

Closed enum: Vision fit

```text
fits the current vision
may conflict with the current vision
proposes a vision revision
no vision exists yet
```

Use the exact value as the first non-empty line of the section.

When root `VISION.md` does not exist, proposals must use the exact `Vision fit` value `no vision exists yet`.

If root `VISION.md` exists, choose one of the current-vision outcomes and do not use `no vision exists yet`.

Retired root `vision.md` must not prevent `no vision exists yet` when root `VISION.md` is absent.

A short explanatory paragraph may follow the status line. A proposal must not silently redefine project vision outside the `Vision fit` section and normal proposal rationale. Legacy proposals are not invalid solely because they lack `Vision fit`; add it only when the proposal is new or substantively revised after adoption.

## Standing artifact gates

| Gate | Rule |
|---|---|
| Substantive proposal | A substantive proposal is any proposal that chooses product direction, user-facing behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract. |
| Vision gate | `VISION.md` absence blocks the first substantive proposal unless the proposal is bootstrap work to create project vision. |
| Constitution gate | `CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal is bootstrap work to create or migrate the constitution. |
| Bootstrap exception | Bootstrap proposals must identify the bootstrap exception in `Vision fit`; otherwise stop before drafting the substantive proposal. |

## Scope preservation

Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes.

Closed enum: initial goal treatment

```text
in scope
out of scope
deferred follow-up
rejected option
open question
```

Every initial user goal must be visible in the proposal as one of:

- `in scope`
- `out of scope`
- `deferred follow-up`
- `rejected option`
- `open question`

Do not silently drop a user goal when narrowing a proposal.

If a proposal intentionally narrows the user's request, record the narrowing in `Non-goals`, `Options considered`, `Decision log`, `Next artifacts`, `Follow-on artifacts`, or `Open questions`.

For broad or multi-part requests, include:

```md
## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| <goal> | <one initial goal treatment value> | <section> |
```

## Scope budget for broad proposals

Use a scope budget when the proposal is broad or multi-workstream.
Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference.

| Trigger | Meaning |
|---|---|
| Multiple work items | the user request contains two or more independent work items. |
| Multiple lifecycle families | the change touches more than one lifecycle family. |
| Multiple downstream artifacts | the change could reasonably require more than one spec or implementation plan. |
| Policy or generated output | The proposal includes release policy, workflow policy, generated output, public skill behavior, or validation policy. |
| Review concern | `proposal-review` identifies silent narrowing, hidden follow-up risk, or multi-workstream scope. |

Closed enum: scope budget treatment

```text
core to this proposal
first-slice candidate
same-slice dependency
separate implementation slice
deferable follow-up
separate proposal
out of scope
```

When triggered, add:

```md
## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| <work item> | <one scope budget treatment value> | <why> |
```

Allowed treatments:

- `core to this proposal`
- `first-slice candidate`
- `same-slice dependency`
- `separate implementation slice`
- `deferable follow-up`
- `separate proposal`
- `out of scope`

Small single-decision proposals may omit the scope budget.

Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership. Preserve this boundary: workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.

Use authored skill sources for skill truth. Do not search generated adapter output for authored skill truth. Do not add generated public adapter skill bodies back to tracked source.

## Decision quality checklist

| Check | Pass condition |
|---|---|
| Problem framing | The problem is not just a solution in disguise. |
| Alternatives | The recommended option is compared against alternatives. |
| Scope | Non-goals protect the scope. |
| Initial intent | Each initial user goal is classified and traceable when the request is broad or multi-part. |
| User value | User value is explicit. |
| Vision fit | `Vision fit` is present and consistent with root `VISION.md` when required. |
| Architecture | Architecture impact is acknowledged. |
| Verification | Testing and verification are plausible. |
| Risks | Risks are specific enough to act on. |
| Open questions | Open questions do not block writing a spec. |

## Rules

- Skill-local rule: do not write implementation milestones in a proposal.
- Skill-local rule: do not use normative `MUST` requirements unless quoting a known constraint.
- Skill-local rule: do not hide major tradeoffs or skip rejected alternatives.
- Skill-local rule: do not claim a proposal is accepted unless the user or project process accepts it.
- Workflow-wide rule: do not treat `under review` as a durable relied-on state once downstream work is using the proposal. Normalize accepted proposals to `accepted`.
- Workflow-wide rule: preserve `Next artifacts` as planning history. Use `Follow-on artifacts` or equivalent closeout text for actual downstream artifacts or final disposition.
- Workflow-wide rule: if a proposal is superseded, identify the replacement with `superseded_by` or equivalent labeled text.

## Workflow handoff behavior

- In a workflow-managed flow, successful `proposal` completion hands off to `proposal-review` when that review is the next mandatory or triggered downstream stage.
- If open questions or direction gaps still block review, stop and report the blocker instead of implying that `proposal-review` can proceed.
- This v1 contract does not imply `proposal-review -> spec`; review-to-next-authoring transitions remain outside the autoprogression boundary unless a later approved change adds them.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, context can change the conclusion, bounded searches disagree, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
# <Proposal title>
## Status
<one proposal status value>
## Problem
<problem>
## Goals
<goals>
## Non-goals
<non-goals>
## Vision fit
<one Vision fit value and rationale>
## Context
<context>
## Options Considered
<at least three options or exploration link>
## Recommended Direction
<direction and rationale>
## Expected Behavior Changes
<observable changes>
## Architecture Impact
<impact>
## Testing and Verification Strategy
<strategy>
## Rollout and Rollback
<rollout and rollback>
## Risks and Mitigations
<risks and mitigations>
## Open Questions
<questions or None>
## Decision Log
<decisions>
## Next Artifacts
<planned artifacts>
## Follow-on Artifacts
None yet
## Readiness
<next-stage status>
```

## Expected output

- proposal file path;
- clear recommended direction;
- alternatives and rationale;
- non-goals and risks;
- open questions;
- readiness statement for `proposal-review` or blocker state.
