---
name: proposal
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create a concise direction-approval proposal before Design. Use when the user has a selected direction, explored options, problem statement, or issue that needs its challenge, goals, bounds, governing principle, direction, and feasibility recorded. Use proposal-review to review an existing proposal; use architecture and spec for detailed Design decisions.
argument-hint: [feature idea, selected option, problem statement, or issue number]
---

# Change proposal

Turn a problem or selected direction into a concise direction-approval artifact: why the problem matters, what outcome is sought, what direction should be pursued, and whether it is credible enough to enter Design.

## Workflow role

### Compact current-state contract

For `compact-current-state-v1`, consume the bounded CLI projection and only its required paths. Author the proposal in its canonical location, update no lifecycle file directly, and submit the transient authoring operation through the CLI. The CLI is a consistency tool, not a permission principal. The proposal becomes review-ready; its stable current review record settles the adjacent gate. Do not create routine request, authoring-evidence, review-log, or correction-receipt artifacts.

- role_name: proposal
- stage: authoring
- upstream: user request, exploration, research, issue, or incident
- downstream: proposal-review
- summary: Author the proposal artifact recording the challenge, goals, bounds, governing principle, direction, feasibility, and requested decision.
- must_not_claim: proposal-review approval, spec readiness, implementation readiness, verification, branch readiness, or PR readiness.

## Project-local evidence

Public skills use customer-project mode by default and project-local artifacts when present. Consume authoritative CLI workflow context for governed routing or placement. Do not require RigorLoop repository-internal artifacts in customer projects; use portable defaults without governed claims or block on ambiguity.

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
- authoritative CLI workflow context when governed artifact placement or workflow routing matters
- code only when current behavior is part of the decision
- exploration, research, issues, incidents, or user feedback when the proposal relies on them

Bounded discovery is not evidence expansion. Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.

## Artifact placement and operation

Prefer `docs/proposals/YYYY-MM-DD-slug.md`; honor project-local placement and never overwrite an older initiative. Resolve one exact target from input, current metadata, governing contract, guidance, or default; stop on ambiguity.

Operations are exactly `create-primary-proposal` and `revise-primary-proposal`. Portable create requires absence; revise requires the exact existing target. Portable authoring writes only the proposal artifact, never lifecycle, review, automation, or routing state.

## Invocation classification

`governed_proposal_candidate_context` requires an explicit change ID, workflow-managed exact change, or valid structured owning-change pointer. Conversational wording alone does not establish it. Loading does not grant mutation authority; failure must not fall back to portable authoring.

Specialized predicates are exactly `vision_exception_context`, `standing_artifact_context`, `initial_intent_table_context`, and `scope_budget_context`. Truth is semantic proposal judgment. Predicates apply independently; a non-empty set loads exactly once. Resolve material ambiguity before drafting or review readiness. Record applicable detail inside `Scope and non-goals`, `Impact and major trade-offs`, or `Decision requested`; specialized predicates do not add level-two sections.

The four loaded assemblies are `PA0-portable`, `PA0G-portable-gated`, `PA1-governed`, and `PA1G-governed-gated`.

## Resource map

- READ `references/requirement-to-delivery-model.md` when clarifying an incoming need into proposal direction or explaining how proposal approval feeds Design.
- READ `references/governed-proposal-authoring.md` when `governed_proposal_candidate_context` is true. Validate authority before governed work.
- READ `references/strategic-and-scope-gates.md` when any specialized predicate is true. Apply all true predicates once.
- COPY `assets/proposal-skeleton.md` when creating a proposal.
  Fields: the seven required sections and the conditional material-impact section.
  Do not emit unfilled placeholders.

Missing, unreadable, escaped, contradictory, stale, or mixed-version required resources stop dependent work; must not reconstruct them. Untriggered resources do not block.

## Proposal contract

Treat the incoming need as RR and the approved proposal as the durable IR-level direction.

The proposal has exactly seven required level-two sections, in this order:

1. `Challenge`
2. `Goals`
3. `Scope and non-goals`
4. `Governing principle`
5. `Proposed direction`
6. `Feasibility`
7. `Decision requested`

`Impact and major trade-offs` is the only optional level-two section. Include it only when it could materially affect approval, and place it between `Feasibility` and `Decision requested`. Nested headings may organize content inside an allowed section.

Frame the challenge before the solution. State outcomes rather than detailed design. Bound included and excluded work. Give one short implementation-independent governing principle. Make the direction concrete enough to approve while leaving detailed behavior and architecture to Design and implementation sequencing and proof design to Delivery.

Every proposal contains exactly one non-empty `Feasibility` section with an explicit assessment, credible evidence or bounded assumptions, material constraints, and blockers that would prevent responsible Design work. Its depth is proportional to uncertainty; a few sentences are sufficient for an ordinary low-uncertainty change. Supporting research may be linked, but the proposal contains the relied-on conclusion. Create no standalone feasibility artifact, skill, lifecycle state, or review gate.

Use this inclusion test: would changing the decision later mean the developer approved a materially different direction? If yes, it likely belongs in the proposal. Otherwise leave it downstream. Do not settle detailed behavior, architecture, APIs, commands, schemas, component design, implementation sequencing, verification design, test cases, and rollout mechanics. No fixed word count, length, or token budget applies; decision sufficiency and proportionality govern.

Portable authoring requires no `change.yaml`, status, owning-change pointer, routine `Vision fit`, or lifecycle command. For governed work, `change.yaml` is the sole owner of governed proposal lifecycle state and ownership. Proposal Review records routine vision alignment; a material conflict, revision request, or bootstrap exception belongs in `Impact and major trade-offs` and `Decision requested` because it can change approval.

## Scope preservation

Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes. Keep each material goal visible in `Goals`, `Scope and non-goals`, or the requested decision. Do not silently drop a user goal when narrowing a proposal; state intentional narrowing and its reason.

Use `initial_intent_table_context` for broad or multi-part requests. Use `scope_budget_context` for multiple work items/families/artifacts, policy, generated output, public skill behavior, or review concern about narrowing, hidden follow-up, or multi-workstream ambiguity. Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference. Small single-decision proposals may omit the scope budget.

## Structural groups

The skeleton owns structure only; procedure owns meaning and applicability. Omit the material-impact section when it is not needed. Keep applicable strategic and scope detail inside an allowed section. Never emit an unfilled placeholder.

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

Return path, operation, assembly, requested decision, blockers, and proposal-review readiness or stop.
