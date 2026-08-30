# Proposal: Simplify the RigorLoop Proposal Contract

## Challenge

RigorLoop proposals currently tend to contain more information than developers need to decide whether a direction should be pursued.

Detailed architecture, behavioral requirements, implementation planning, verification strategy, rollout mechanics, and exhaustive risk analysis can appear during proposal authoring or be requested during proposal review.

This creates several problems:

- the challenge and proposed direction are harder to identify;
- developers must read downstream design detail before making a direction-level decision;
- proposal authors spend tokens and effort on decisions owned by later stages;
- proposal review can require information that Design Review or Delivery Review should own;
- downstream stages lose meaningful design authority because decisions have already been made;
- proposal artifacts become larger and harder to maintain than necessary.

RigorLoop's consolidated review model now provides clearer downstream ownership:

```text
Proposal Review
→ Design Review
→ Delivery Review
→ Code Review
→ Verify
```

The proposal contract should be simplified to match that model.

## Goals

This change should:

- make proposals concise and easy for developers to evaluate;
- focus proposal approval on whether a direction is worth pursuing;
- clearly define what proposal approval does and does not lock;
- require enough feasibility evidence to avoid approving an unrealistic direction;
- keep detailed behavioral and architectural decisions for Design;
- keep implementation sequencing and verification design for Delivery;
- prevent `proposal-review` from requiring downstream detail;
- reduce proposal-stage agent context and duplicated reasoning;
- keep routine vision-alignment judgment in Proposal Review rather than duplicating it in every proposal;
- keep proposal lifecycle state and ownership in `docs/changes/<change-id>/change.yaml` rather than duplicating it in the proposal;
- preserve additional impact analysis when a change is large enough for it to affect approval;
- update proposal authoring, review, templates, references, and published packages as one coherent contract.

## Scope and non-goals

### In scope

This change will refine:

- the `proposal` skill;
- the `proposal-review` skill;
- the canonical proposal structure;
- proposal-review criteria;
- proposal templates;
- proposal-review templates;
- supporting references and examples;
- `CONSTITUTION.md`, `AGENTS.md`, and workflow guidance that define the proposal contract;
- proposal lifecycle validation and its tests;
- generated proposal-stage packages for supported adapters;
- the meaning of proposal approval;
- the handoff from Proposal Review into Design.

These are same-slice dependencies because leaving any one of them on the previous contract would preserve conflicting proposal requirements. Adapter work means updating canonical generation and release-validation surfaces, not hand-editing generated release archives.

### Non-goals

This change will not:

- redesign Design Review;
- redesign Delivery Review;
- change architecture or specification ownership;
- change plan or verification ownership;
- merge proposal with feasibility, design, or delivery artifacts;
- introduce automatic semantic proposal validation;
- require a fixed proposal length or token budget;
- define detailed architecture inside the proposal;
- migrate already-settled historical proposals into the new format;
- redesign the complete RigorLoop lifecycle;
- change lifecycle ownership or metadata rules for architecture, specification, plan, test-specification, or other governed artifacts.

Those concerns remain owned by their existing or separately proposed changes.

## Governing principle

> **A proposal should contain only the information needed to decide whether a direction is worth pursuing and feasible enough to continue into Design.**

## Proposed direction

Redefine the RigorLoop proposal as a lightweight **direction-approval artifact**.

### Required structure

Every proposal should contain these seven sections:

```text
Challenge
Goals
Scope and non-goals
Governing principle
Proposed direction
Feasibility
Decision requested
```

One additional section should be conditional:

```text
Impact and major trade-offs
```

It should appear only when the consequences of the proposed direction could materially affect the approval decision.

These seven sections define the complete semantic and structural contract of a proposal. A proposal should not contain mutable lifecycle status, an owning-change pointer, or routine vision-alignment metadata.

For a governed change, `docs/changes/<change-id>/change.yaml` should reference the proposal and remain the sole owner of proposal lifecycle state and ownership. A portable proposal may exist without a change record. Accepting or governing that proposal should create or update the change record without rewriting the proposal to add reverse lifecycle metadata.

Proposal Review should independently compare the proposed direction with `VISION.md`. Ordinary alignment should be recorded in review evidence rather than repeated in the proposal. A material vision conflict, requested vision revision, or exception that could affect approval should be disclosed in `Impact and major trade-offs` and made explicit in `Decision requested`.

### Challenge

The Challenge should explain:

> **What is insufficient today, and why is the problem worth addressing?**

It should describe the problem before introducing a preferred implementation.

It should be concrete enough that Proposal Review can challenge whether the problem is real, material, and correctly framed.

### Goals

Goals should describe the outcomes the change should achieve.

They should avoid detailed design.

For example:

```text
Good:
Reduce unnecessary agent context required for governed operations.

Too detailed:
Return no more than five JSON fields from successful commands.
```

The first is a goal.

The second is a downstream behavioral or design decision.

### Scope and non-goals

This section should define:

- what problem the proposal authorizes work on;
- what adjacent work is included;
- what is explicitly excluded;
- which major product boundaries must not be implicitly expanded.

It should prevent proposal approval from being interpreted as authorization for a substantially larger change.

### Governing principle

Every proposal should include one short governing principle.

The principle should:

- follow from the challenge and goals;
- remain independent of detailed implementation;
- constrain later design decisions;
- normally fit in one sentence.

For example:

> Deterministic lifecycle rules should be enforced by deterministic software rather than repeatedly interpreted by agents.

It should not be a summary of the proposal or a disguised implementation decision.

### Proposed direction

This section should answer:

> **Given the challenge, goals, scope, and governing principle, what high-level direction should RigorLoop pursue?**

The direction must be specific enough for a developer to approve or reject.

It should stop before detailed behavior or architecture.

For example:

```text
Appropriate:
Introduce one deterministic interface for governed lifecycle transitions.

Too detailed:
Implement a Node CLI using revision counters, atomic file renames,
a particular locking mechanism, and a fixed JSON response schema.
```

The proposal authoring skill should use this inclusion test:

> **Would changing this decision later mean the developer approved a materially different direction?**

If yes, it likely belongs in the proposal.

If no, it should normally be left to Design or Delivery.

### Feasibility

Feasibility should be required for every proposal, but its depth should be proportional to uncertainty.

It should answer:

> **Is there a credible way to pursue this direction within the known constraints?**

For an ordinary change, the section may be only a few sentences:

```text
Feasibility: Feasible.

The direction relies on mechanisms already present in the repository
and introduces no significant new platform or dependency constraint.

No known blocker prevents proceeding to Design.
```

For a more uncertain change:

```text
Feasibility: Feasible with constraints.

The direction appears technically credible, but cross-platform
persistence and compatibility constraints require further Design work.

No known constraint currently invalidates the direction.
```

Feasibility may identify:

- evidence supporting viability;
- known blockers;
- important constraints;
- unresolved uncertainty.

It should not define:

- exact architecture;
- APIs or commands;
- state models;
- persistence mechanisms;
- concurrency algorithms;
- implementation milestones;
- complete verification strategy.

When deeper investigation is needed, the proposal may summarize supporting analysis rather than embedding it all in the proposal.

### Impact and major trade-offs

This section should be optional.

Include it only when an impact or disadvantage could reasonably cause the developer to reject or materially reshape the proposed direction.

Examples include:

- significant compatibility or migration impact;
- major workflow or public API changes;
- security, privacy, or authority-model changes;
- substantial persistence or data-model changes;
- cross-team or cross-platform impact;
- substantial maintenance or operational obligations;
- difficult-to-reverse product decisions.

Routine implementation cost or generic statements such as "this increases complexity" do not justify the section.

Proposal Review should not create a finding merely because an ordinary proposal omits it.

### Decision requested

Every proposal should end with an explicit approval request.

Proposal approval should lock:

```text
challenge
goals
scope and non-goals
governing principle
high-level direction
feasibility sufficient to proceed
material proposal-level impacts, when applicable
```

It should not lock:

```text
detailed behavioral requirements
architecture
APIs or commands
schemas
component design
implementation sequence
verification design
test cases
rollout mechanics
```

The standard meaning should be:

> **Approve this direction as sufficiently valuable, bounded, and feasible to proceed to Design.**

### Proposal Review

`proposal-review` should be updated at the same time as `proposal`.

Its central question should be:

> **Does this proposal provide enough evidence for a responsible decision about whether to pursue the direction?**

Proposal Review should evaluate:

1. whether the challenge is clear and material;
2. whether the goals address the challenge;
3. whether scope and non-goals are sufficiently bounded;
4. whether the governing principle is sound and implementation-independent;
5. whether the proposed direction is concrete enough to approve;
6. whether the direction follows reasonably from the preceding reasoning;
7. whether feasibility evidence is proportionate to uncertainty;
8. whether material impact is disclosed when needed;
9. whether the direction aligns with `VISION.md`, or clearly discloses a material conflict, revision, or exception;
10. whether downstream decisions have remained downstream;
11. whether the requested decision is explicit.

Proposal Review should not require:

- completed specification;
- detailed architecture;
- implementation planning;
- detailed test design;
- rollout plans;
- exhaustive risk registers;
- exact APIs, commands, schemas, or algorithms;
- a routine `Vision fit` section when the reviewer can establish ordinary alignment directly from `VISION.md`.

A proposal should receive a material finding when it is either:

```text
too vague
→ no meaningful direction can be approved

or

too detailed
→ downstream decisions are being prematurely settled
```

### Handoff to Design

After Proposal Review passes, Design receives:

```text
approved challenge
approved goals
approved scope and non-goals
approved governing principle
approved direction
known feasibility constraints
material impact information, when applicable
material vision constraints or exceptions, when applicable
```

Design is then responsible for developing the behavioral and technical solution.

If Design discovers that progress requires changing one of the approved proposal-level decisions, the issue should route back to proposal ownership rather than being silently changed downstream.

### Templates and references

The canonical proposal template should contain only:

```text
Challenge
Goals
Scope and non-goals
Governing principle
Proposed direction
Feasibility
Decision requested
```

with `Impact and major trade-offs` available conditionally.

The template should not contain proposal-owned lifecycle metadata. Governed ownership and mutable status should be represented only by the matching `change.yaml` entry, which points to the proposal.

The proposal template should not contain mandatory placeholders for:

- architecture;
- testing strategy;
- rollout;
- implementation plan;
- exhaustive risks;
- detailed alternatives;
- mutable status;
- an owning-change pointer;
- routine vision-alignment metadata.

Supporting references should provide deeper guidance only when needed, including examples of:

- strong challenges;
- outcome-oriented goals;
- good governing principles;
- proportionate feasibility analysis;
- vague proposals;
- proposals containing premature architecture;
- material impact that belongs in the proposal;
- information that should instead be deferred to Design or Delivery;
- Proposal Review examples for ordinary vision alignment, material vision conflict, and requested vision revision.

Templates provide reusable structure; the skill and authoritative references remain responsible for policy.

## Feasibility

**Assessment: Feasible.**

The workflow's consolidation into Proposal Review, Design Review, Delivery Review, Code Review, and Verify creates clearer ownership for information that can be removed from proposal artifacts.

Detailed behavior and architecture have a clear home in Design.

Implementation sequencing and verification planning have a clear home in Delivery.

The proposal-stage optimization therefore does not require removing engineering rigor. It primarily relocates detail to the stage that owns the corresponding decision.

Implementation will require coordinated changes to:

- `proposal`;
- `proposal-review`;
- proposal templates;
- proposal-review templates;
- conditional references;
- `CONSTITUTION.md` and `AGENTS.md` proposal rules;
- workflow handoff guidance;
- proposal lifecycle validation and tests;
- conformance examples;
- generated adapter packages.

No known unsettled existing proposal currently requires migration.

This proposal is a deliberate bootstrap instance of the simplified contract. The developer explicitly requested that it demonstrate the proposed seven-section form rather than first reproducing the contract it seeks to retire.

The compatibility policy should be:

```text
proposal settled before cutover
→ remains valid under the contract it was approved with

proposal created before cutover
→ continues under the current contract unless explicitly migrated at cutover

proposal created after cutover
→ uses the simplified contract

proposal still unsettled at cutover
→ adopts the simplified contract before later settlement
```

This avoids rewriting historical evidence while preventing active work from continuing under two proposal-stage contracts.

No known technical or lifecycle blocker prevents proceeding.

## Impact and major trade-offs

This change affects a core RigorLoop stage and its published skills, so its impact is material enough to state explicitly.

### Smaller proposal, greater downstream responsibility

Proposal artifacts will contain less technical detail.

Design and Delivery must therefore reliably own the decisions removed from proposal.

The consolidated review workflow provides those ownership boundaries.

### Less proposal-stage context

Agents and developers should need less context to author and review proposals.

The trade-off is that reviewers must resist requesting downstream detail merely because additional information might be useful.

Proposal Review should require **decision sufficiency**, not maximum available information.

### Existing historical proposals remain structurally different

Previously approved proposals may remain larger than proposals created under the simplified contract.

That is acceptable. Historical artifacts represent the contract in effect when they were settled and should not be rewritten merely for formatting consistency.

### Less duplicated lifecycle and vision metadata

New proposals will no longer carry an owning-change pointer, embedded lifecycle status, or routine `Vision fit` section. This removes reverse references and repeated judgments from the direction artifact.

The trade-off is that `change.yaml` and Proposal Review evidence must remain reliable owners of lifecycle identity and vision-alignment judgment. Material vision conflicts or revision requests remain proposal-level decisions and must still be disclosed before approval.

## Decision requested

Approve the following direction:

1. Redefine `proposal` as a concise direction-approval artifact.
2. Require seven core sections: Challenge, Goals, Scope and non-goals, Governing principle, Proposed direction, Feasibility, and Decision requested.
3. Make `Impact and major trade-offs` conditional on material influence rather than universally required.
4. Require feasibility for every proposal, with depth proportional to uncertainty.
5. Remove proposal-owned lifecycle status, owning-change pointers, and routine vision-alignment metadata from the proposal document.
6. Keep governed proposal ownership and lifecycle state solely in `docs/changes/<change-id>/change.yaml`, which references the proposal.
7. Have Proposal Review evaluate ordinary vision alignment and require the proposal to disclose only material conflicts, revision requests, or exceptions.
8. Remove detailed specification, architecture, implementation planning, verification design, rollout, and exhaustive risk analysis from the standard proposal contract.
9. Update `proposal-review` so it evaluates direction-level decision sufficiency rather than downstream design completeness.
10. Update constitutional guidance, operating guidance, proposal templates, review templates, references, validators, tests, handoff guidance, and adapter generation and release-validation surfaces together.
11. Preserve already-settled historical proposals under their existing contract.
12. At cutover, require proposals created afterward—and any proposal still unsettled at cutover—to use the simplified contract.
13. Proceed to specification and implementation of the revised proposal-stage contract.

> **Approval authorizes RigorLoop to simplify proposal authoring and review around direction-level decisions; it does not approve changes to the Design Review, Delivery Review, Code Review, or Verify contracts.**
