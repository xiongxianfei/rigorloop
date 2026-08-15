---
name: proposal
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create a decision-oriented change proposal before spec or plan. Use when the user has a selected direction, explored options, problem statement, or issue that needs problem, goals, non-goals, options, recommendation, risks, rollout, and readiness recorded. Use proposal-review to review an existing proposal; use spec, plan, implement, or verify for downstream work.
argument-hint: [feature idea, selected option, problem statement, or issue number]
---

# Change proposal

Turn a problem or selected direction into a reviewable decision: why this change, why now, and why this approach, without requirements or implementation tasks.

## Workflow role

- role_name: proposal
- stage: authoring
- upstream: user request, exploration, research, issue, or incident
- downstream: proposal-review
- summary: Author the proposal artifact recording problem, options, recommendation, scope, risks, and readiness.
- must_not_claim: proposal-review approval, spec readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Project-local evidence

Public skills use customer-project mode by default and project-local artifacts when present, including `docs/workflows.md` for local routing or placement. Do not require RigorLoop repository-internal artifacts in customer projects; use portable defaults or block on ambiguity.

## Evidence access

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

## Artifact placement and operation

Prefer `docs/proposals/YYYY-MM-DD-slug.md`; honor project-local placement and never overwrite an older initiative. Resolve one exact target from input, current metadata, governing contract, guidance, or default; stop on ambiguity.

Operations are exactly `create-primary-proposal` and `revise-primary-proposal`. Portable create requires absence; revise requires the exact existing target. Portable authoring writes only the proposal artifact, never lifecycle, review, automation, or routing state.

## Invocation classification

`governed_proposal_candidate_context` requires an explicit change ID, workflow-managed exact change, or valid structured owning-change pointer. Conversational wording alone does not establish it. Loading does not grant mutation authority; failure must not fall back to portable authoring.

Specialized predicates are exactly `vision_exception_context`, `standing_artifact_context`, `initial_intent_table_context`, and `scope_budget_context`. Truth is semantic proposal judgment. Predicates apply independently; a non-empty set loads exactly once. Resolve material ambiguity before drafting or readiness.

The four loaded assemblies are `PA0-portable`, `PA0G-portable-gated`, `PA1-governed`, and `PA1G-governed-gated`.

## Resource map

- READ `references/governed-proposal-authoring.md` when `governed_proposal_candidate_context` is true. Validate authority before governed work.
- READ `references/strategic-and-scope-gates.md` when any specialized predicate is true. Apply all true predicates once.
- COPY `assets/proposal-skeleton.md` when creating a proposal.
  Fields: universal proposal sections and every applicable conditional group.
  Do not emit unfilled placeholders.

Missing, unreadable, escaped, contradictory, stale, or mixed-version required resources stop dependent work; must not reconstruct them. Untriggered resources do not block.

## Proposal contract

Cover problem, goals, non-goals, context, three options or linked exploration, recommendation, behavior, architecture, testing, rollout/rollback, risks, questions, decisions, artifacts, and readiness. Preserve `Next artifacts` as history; use `Follow-on artifacts` for results and `None yet` before any exist.

Frame the problem independently, compare tradeoffs, protect scope and intent, state value, and make risks actionable. Do not write milestones, invent `MUST` rules, hide tradeoffs, or claim acceptance without authority.

## Vision fit

Include `Vision fit` in new or substantively revised proposals after vision adoption; Legacy proposals need it when revised. Its first non-empty line is `fits the current vision`, `may conflict with the current vision`, `proposes a vision revision`, or `no vision exists yet`.

When root `VISION.md` does not exist, proposals must use the exact `Vision fit` value `no vision exists yet`. If root `VISION.md` exists, choose one of the current-vision outcomes. Retired root `vision.md` must not prevent `no vision exists yet`. A proposal must not silently redefine project vision.

## Scope preservation

Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes. Every initial user goal must be visible in the proposal as one `initial goal treatment` enum value. Do not silently drop a user goal when narrowing a proposal. If a proposal intentionally narrows the user's request, record the narrowing.

Use `initial_intent_table_context` for broad or multi-part requests. Use `scope_budget_context` for multiple work items/families/artifacts, policy, generated output, public skill behavior, or review concern about narrowing, hidden follow-up, or multi-workstream ambiguity. Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference. Small single-decision proposals may omit the scope budget.

## Structural groups

The skeleton owns structure only; procedure owns meaning and applicability. Inapplicable conditional groups are omitted. Applicable but unresolved groups report an explicit blocker. Never emit an unfilled placeholder.

## Generated Markdown readability

Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines. Preserve stable IDs and tables. Diagrams are optional. Do not require manual-proof contracts from this readability guidance alone.

## Source, claims, and handoff

Use authored skill sources for skill truth. Do not search generated adapter output for authored skill truth. Do not add generated public adapter skill bodies back to tracked source.

Workflow-managed completion hands off to `proposal-review` when it is the next mandatory or triggered downstream stage; direction gaps stop. Approval belongs to review. Do not claim later-stage, branch, PR, release, deployment, or publication readiness.

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
COPY `assets/proposal-skeleton.md` for <proposal path>.
Fill every universal section and each applicable conditional group.
Omit inapplicable groups and do not emit unfilled placeholders.
```

## Expected output

Return path, operation, assembly, recommendation, rationale, risks, blockers, and review readiness or stop.
