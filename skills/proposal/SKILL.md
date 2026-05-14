---
name: proposal
description: >
  Create a decision-oriented change proposal before writing a feature spec or execution plan. Use after exploration has produced options or when the intended direction is clear enough to evaluate scope, value, risks, and non-goals.
argument-hint: [feature idea, selected option, problem statement, or issue number]
---

# Change proposal

You are turning exploration into a concrete, reviewable direction.

A proposal answers “why this change, why now, and why this approach?” It does not define every requirement and it does not prescribe every implementation task.

## Inputs to read

Read, if present:

- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/project-map.md`
- relevant exploration artifact
- relevant research artifact
- related specs
- related architecture docs or ADRs
- related issues, incidents, or user feedback
- root `VISION.md` when present

## Output path

Prefer:

```text
docs/proposals/YYYY-MM-DD-slug.md
```

Do not overwrite an older proposal for a new initiative.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Required sections

1. **Status**: draft, under review, accepted, rejected, abandoned, superseded, archived.
2. **Problem**: the user or system problem being solved.
3. **Goals**: outcomes the change should produce.
4. **Non-goals**: explicitly out-of-scope work.
5. **Vision fit**: relationship to root `VISION.md`.
6. **Context**: relevant repo, product, architecture, or operational background.
7. **Options considered**: summarize at least three options or link to `explore`.
8. **Recommended direction**: selected approach and rationale.
9. **Expected behavior changes**: high-level observable behavior, not detailed requirements.
10. **Architecture impact**: expected components, boundaries, and data flow touched.
11. **Testing and verification strategy**: likely levels of test coverage.
12. **Rollout and rollback**: migration, flags, compatibility, fallback.
13. **Risks and mitigations**: product, technical, operational, security, performance.
14. **Open questions**: what must be resolved before spec or architecture.
15. **Decision log**: date, decision, reason, alternatives rejected.
16. **Next artifacts**: planned spec, architecture, plan, test-spec, or follow-up work while the proposal is active.
17. **Follow-on artifacts**: actual downstream artifacts or terminal disposition after settlement or closeout. If present before any real follow-ons exist, say `None yet`.
18. **Readiness**: truthful next-stage status.

## Vision fit

Include `Vision fit` in new or substantively revised proposals after the vision spec is adopted.

The first non-empty line of the section states exactly one of:

- `fits the current vision`
- `may conflict with the current vision`
- `proposes a vision revision`
- `no vision exists yet`

When root `VISION.md` does not exist, proposals must use the exact `Vision fit` value `no vision exists yet`.

If root `VISION.md` exists, choose one of the current-vision outcomes and do not use `no vision exists yet`.

Retired root `vision.md` must not prevent `no vision exists yet` when root `VISION.md` is absent.

A short explanatory paragraph may follow the status line.

A proposal must not silently redefine project vision outside the `Vision fit` section and normal proposal rationale.

Legacy proposals are not invalid solely because they lack `Vision fit`; add it only when the proposal is new or substantively revised after adoption.

## Standing artifact gates

A substantive proposal is any proposal that chooses product direction, user-facing behavior, workflow policy, architecture direction, compatibility policy, release policy, or contributor-visible contract.

`VISION.md` absence blocks the first substantive proposal unless the proposal is bootstrap work to create project vision.

`CONSTITUTION.md` absence blocks governance adoption, workflow-governance changes, and source-of-truth changes unless the proposal is bootstrap work to create or migrate the constitution.

Bootstrap proposals must identify the bootstrap exception in `Vision fit`. If the proposal is not bootstrap work and the required standing artifact is missing, stop before drafting a substantive proposal.

## Scope preservation

Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes.

Every initial user goal must be visible in the proposal as one of:

- `in scope`
- `out of scope`
- `deferred follow-up`
- `rejected option`
- `open question`

Do not silently drop a user goal when narrowing a proposal.

If a proposal intentionally narrows the user's request, record the narrowing in `Non-goals`, `Options considered`, `Decision log`, `Next artifacts`, `Follow-on artifacts`, or `Open questions`.

For broad or multi-part requests, include this section or an equivalent table:

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| <goal> | in scope / out of scope / deferred follow-up / rejected option / open question | <section> |

## Scope budget for broad proposals

Use a scope budget when a proposal is broad or multi-workstream.
Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference.

A scope budget is expected when any of these are true:

- the user request contains two or more independent work items;
- the change touches more than one lifecycle family;
- the change could reasonably require more than one spec or implementation plan;
- the proposal includes release policy, workflow policy, generated output, public skill behavior, or validation policy;
- `proposal-review` identifies silent narrowing, hidden follow-up risk, or multi-workstream scope.

Small single-decision proposals may omit the scope budget.

When triggered, add this proposal section or equivalent work-item classification:

```md
## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| <work item> | <treatment> | <why> |
```

Allowed treatments:

- `core to this proposal`: belongs to the current proposal direction.
- `first-slice candidate`: belongs in the first implementation slice if the proposal is accepted.
- `same-slice dependency`: must move with the current slice for the main change to pass.
- `separate implementation slice`: belongs to a later implementation slice under the same accepted direction.
- `deferable follow-up`: real future work, routed to an owner surface but not required now.
- `separate proposal`: related work that needs its own direction decision.
- `out of scope`: explicitly excluded from this change.

Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership.
Preserve this boundary: workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.

Use authored skill sources for skill truth.
Do not search generated adapter output for authored skill truth.
Do not add generated public adapter skill bodies back to tracked source.

## Decision quality checklist

Before marking accepted or ready for review, verify:

- the problem is not just a solution in disguise;
- the recommended option is compared against alternatives;
- non-goals protect the scope;
- each initial user goal is classified and traceable when the request is broad or multi-part;
- user value is explicit;
- `Vision fit` is present and consistent with root `VISION.md` when required;
- architecture impact is acknowledged;
- testing and verification are plausible;
- risks are specific enough to act on;
- open questions do not block writing a spec.

## Rules

- Do not write implementation milestones here.
- Do not use normative `MUST` requirements here unless quoting a known constraint.
- Do not hide major tradeoffs.
- Do not skip the rejected alternatives.
- Do not claim a proposal is accepted unless the user or project process accepts it.
- Do not treat `under review` as a durable relied-on state once downstream work is using the proposal. Normalize accepted proposals to `accepted`.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` or equivalent closeout text for actual downstream artifacts or final disposition.
- If a proposal is superseded, identify the replacement with `superseded_by` or equivalent labeled text.

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

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- proposal file path;
- clear recommended direction;
- alternatives and rationale;
- non-goals and risks;
- open questions;
- readiness statement for `proposal-review` or blocker state.
