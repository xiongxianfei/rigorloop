# Implement Skill Simplification

## Owning change record

`docs/changes/2026-08-11-implement-skill-simplification/change.yaml`

## Problem

The published `implement` skill carries universal implementation policy, repeated orientation and handoff guidance, planned-milestone lifecycle procedure, automation-only review-packet rules, and two overlapping output structures in one common path.

An isolated implementation request therefore loads and navigates procedure that applies only to workflow-managed milestones or armed review-fix loops.
The result is a 395-line, 3,338-word skill with an estimated static cost of 5,977 tokens, even though many invocations need only authority checks, test-first execution, scoped validation, stop rules, and a handoff to `code-review`.

Simple deletion would be unsafe.
Repeated passages currently carry compatibility-sensitive distinctions about test-spec approval, workflow ownership, milestone state, validation failure, review-fix authority, claim boundaries, and final holistic review.

## Goals

- Make isolated and direct implementation work easier to understand by reducing repeated common-path prose.
- Give each behaviorally significant implementation rule one explicit owner and destination.
- Keep the universal implementation contract self-sufficient in `SKILL.md`.
- Load planned-work and automation procedure only when its exact invocation condition applies.
- Make one packaged asset the sole owner of repeated implementation-result structure.
- Preserve deterministic canonical, generated, archived, and installed package behavior across supported adapters.
- Measure common-path reduction separately from total package size and subordinate both measurements to semantic preservation.

## Non-goals

- Changing the standard workflow stage order or the ownership boundary between `implement`, `workflow`, `code-review`, `verify`, and `pr`.
- Weakening test-first practice, first-pass completeness, validation layering, stop conditions, scope control, milestone review, or claim boundaries.
- Changing the meaning of `smallest scope-complete change`, `first-pass acceptable result`, `review-requested`, or milestone closeout.
- Optimizing `workflow`, review skills, or other published skills in the same change.
- Creating a generic execution framework or a new skill.
- Adding target-agent prompt journeys, transcript grading, model-selection fixtures, or runtime-version evidence.
- Adding a permanent line-count, token-count, prose-quality, or simplicity gate.
- Hand-editing generated public adapter packages or tracking generated skill bodies as authored source.

## Vision fit

fits the current vision

The change makes a central execution skill easier for contributors and agents to inspect and use while preserving the durable evidence, test discipline, review handoff, and resumability that distinguish RigorLoop.
It reduces ceremony that does not improve a given invocation without weakening the traceability chain.

## Context

`skills/` remains the only authored skill source.
A published skill is already treated as a canonical `SKILL.md` plus its explicitly mapped packaged references and assets, with lifecycle and policy ownership remaining at the skill level.

The completed `code-review` simplification demonstrated that progressive disclosure can reduce ordinary-path content while preserving canonical, generated, packed, and installed package parity.
That change also demonstrated the need for a closed rule-disposition ledger, separate common-path and package measurements, independent semantic review, and early inventory of literal vocabulary dependencies.

The current `implement` package maps only the shared boundary-first reference.
Its three largest sections are the boundary-first method at about 607 estimated tokens, first-pass completeness at about 517, and implementation autoprogression at about 477.
Additional repetition exists across the preamble, workflow role, quick guide, purpose, evidence sections, four handoff-oriented sections, stop and claim guidance, and two result structures.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `implement` skill next | in scope | Goals and Recommended Direction |
| Make the skill more concise and easier to use | in scope | Problem, Goals, and Expected Behavior Changes |
| Select the best solution rather than applying blind deletion | in scope | Options Considered and Recommended Direction |
| Preserve implementation rigor and workflow behavior | in scope | Non-goals, Recommended Direction, and Risks and Mitigations |
| Optimize other large skills | out of scope | Non-goals and Scope Budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Inventory and disposition current `implement` rules | core to this proposal | Semantic preservation requires explicit source-to-destination accounting. |
| Consolidate universal common-path prose | core to this proposal | This directly improves isolated and direct implementation use. |
| Add one workflow-managed implementation reference | core to this proposal | Planned-work and automation detail is genuinely conditional. |
| Add one implementation-result asset | core to this proposal | Repeated output structure needs one structural owner. |
| Extend existing skill and adapter proof | same-slice dependency | New mapped resources require deterministic package parity. |
| Assess canonical architecture impact | same-slice dependency | The change adds packaged resources but should reuse the existing published-skill package model. |
| Optimize `workflow` | separate proposal | Its routing authority and larger blast radius require an independent decision. |
| Consolidate contracts across all execution and review skills | separate proposal | Cross-skill ownership would exceed this bounded package refactor. |
| Add a permanent simplicity validator | out of scope | Change-local measurements are evidence, not durable product invariants. |

## Options Considered

### O0: Keep the current skill

This avoids compatibility risk and maintenance work.
It leaves the 5,977-token common path, overlapping result structures, repeated handoffs, and automation-only content unchanged.

### O1: Editorial deduplication only

This would consolidate repeated wording while keeping every procedure inline.
It is the smallest structural change and may reduce common-path content by roughly 15–25 percent.
It does not prevent isolated requests from loading planned-work and automation-only procedure.

### O2: Deduplicate and extract only the result asset

This adds one structural owner for output and consolidates common prose.
It should improve maintainability and may reduce common-path content by roughly 20–30 percent.
Workflow-managed procedure would still occupy the ordinary path.

### O3: Consolidate the universal contract, add one conditional workflow-managed reference, and add one output asset

This keeps direct implementation self-sufficient while moving only planned-work and automation procedure behind an exact load trigger.
It applies the proven progressive-disclosure model without creating several small references.
The expected planning range is a 30–45 percent common-path reduction, subject to semantic preservation.

### O4: Split execution, milestone, evidence, automation, and output guidance into several resources

This could minimize the main file further and enable narrow loading.
It would increase package navigation, resource-map complexity, partial-load risk, and maintenance across several policy fragments.

## Recommended Direction

Choose O3.

Keep a shorter linear `SKILL.md` that owns purpose and trigger, stage authority, prerequisites, test-first execution, the definition of a scope-complete first pass, core validation layering, scope and stop rules, claim boundaries, direct review handoff, exact resource triggers, and required output fields.

Add one mapped `references/workflow-managed-implementation.md` resource.
Load it only for a planned workflow-managed milestone or an armed review-fix correction loop.
It should own change-record milestone inspection, baseline change-pack procedure, state-sync and planned-milestone handoff procedure, milestone commit convention, accepted review-fix returns, automated adversarial-review packet construction, requirement-fidelity routing metadata, forbidden initial-review context, reviewer-declared auto-fix constraints, and the final holistic-review prerequisite for later Phase C work.

Keep the compact boundary decision bridge inline and let the existing mapped boundary-first reference own the detailed shared method.

Add `assets/implementation-result-skeleton.md` as the only copy-and-fill implementation-result structure.
The asset owns field layout only; `SKILL.md` retains all policy governing when fields may be emitted or claimed.

Before moving prose, create a change-local rule-disposition ledger covering every behaviorally significant rule and known duplication cluster.
Use closed dispositions equivalent to retained inline, retained conditional reference, asset owned, removed duplicate, and removed obsolete only with approved contract change.
No rule should disappear without an explicit destination or approved semantic change.

## Expected Behavior Changes

- Isolated implementation requests encounter a shorter, linear common path with less repeated orientation and handoff prose.
- Planned workflow-managed milestones load one additional procedure reference with an exact trigger.
- Armed review-fix loops continue to receive all existing packet, independence, fix-authority, and final-review constraints through that reference.
- Implementation outputs use one mapped result skeleton rather than two overlapping inline structures.
- Canonical, generated, archived, and temporary installed packages include identical mapped resources at stable relative paths.
- Status, milestone, validation, stop, claim, and downstream handoff behavior remains unchanged.

## Architecture Impact

The change affects the published `implement` skill package boundary by adding one conditional reference and one asset.
It reuses the existing canonical-skill, mapped-resource, adapter-generation, and installed-resource integrity architecture.

No new runtime, dependency, persistent state, selector family, or lifecycle owner is expected.
The complete `implement` package remains the policy owner; references and assets do not become independent stages or governance owners.

After specification review, an architecture assessment should determine whether the canonical architecture already covers this package addition or whether its current owning-change pointer and resource examples need a bounded update.
A new ADR is not expected unless the specification introduces a new package-ownership model.

## Testing and Verification Strategy

Use four proof classes:

1. A deterministic rule-disposition and static-scenario proof that rejects unknown dispositions before destination consistency.
2. Focused existing skill-validator coverage for inline ownership, exact conditional loading, output-asset ownership, closed vocabulary, claim boundaries, and absence of target-runtime machinery.
3. Existing skill generation and adapter-distribution proof for canonical, generated, archived, and temporary installed resource parity across Codex, Claude, and opencode.
4. Independent semantic review of trigger clarity, authority, prerequisites, test-first sequence, completeness, validation, stops, claims, milestone behavior, output, handoff, and conditional loading.

Representative static scenarios should include isolated implementation, planned milestone execution, missing or stale authority, failing tests, a discovered specification gap, accepted review-fix return, workflow-managed automated review handoff, and an attempted next-milestone transition before review closeout.

Inventory existing validator assertions that depend on literal headings, phrases, or capitalization before editing the skill.
This avoids discovering compatibility vocabulary only during final verification.

Report before and after line, word, and deterministic token estimates for `SKILL.md`, the conditional reference, and the total package.
Also report duplicate-cluster owners, inline-template count, and mapped-resource count.
The planning percentage is evidence, not an acceptance threshold.

No acceptance command should execute or grade Codex, Claude Code, opencode, or another target-agent runtime.

## Rollout and Rollback

Ship the canonical `implement` package, mapped reference, output asset, validator coverage, and package proof in one atomic change.
Generate adapter output only through existing repository scripts and temporary directories.

Rollback restores the prior complete canonical package and regenerates every derived target from that source.
Do not roll back only `SKILL.md` while leaving new mapped resources or validation expectations in place.

No user data migration, feature flag, external service rollout, or dependency change is expected.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Universal policy moves behind a conditional trigger | Isolated implementations could weaken authority, testing, stops, or handoff behavior. | Define inline and conditional ownership before editing; verify direct scenarios and conduct semantic review. |
| Similar paragraphs encode different behavior | Deduplication could erase planned-versus-isolated or implementation-versus-workflow distinctions. | Use a closed rule ledger with source locations, behavior summaries, and destinations. |
| The conditional trigger is too broad or too narrow | Required workflow procedure may load unnecessarily or fail to load. | Specify one exact trigger and test direct, planned, and armed correction contexts. |
| The output asset becomes a policy owner | Structure and behavioral rules could drift between files. | Keep only fields and layout in the asset; retain policy and claim rules inline. |
| Literal compatibility dependencies are missed | Repository regression tests may fail late despite semantic preservation. | Inventory required headings, phrases, and capitalization before refactoring. |
| Common-path reduction hides package growth | A relocation-only win could increase maintenance cost. | Report common-path and total-package measurements separately. |
| Several small resources fragment execution guidance | Agents and maintainers could miss required procedure. | Use one conditional procedure reference and one structural asset, not a reference per section. |
| Permanent simplicity checks overfit one change | Future semantic improvements could be blocked by arbitrary prose budgets. | Keep measurements and the rule ledger change-local; reuse only durable structural and package validators. |

## Open Questions

- Which current literal headings and phrases are compatibility-sensitive in existing skill and review validators?
- Should the exact conditional trigger distinguish every planned milestone from only workflow-managed planned milestones?
- Does the existing architecture need a pointer or example update when `implement` gains mapped resources, or is an architecture-not-required assessment sufficient?

These questions can be resolved during specification, architecture assessment, and test-spec authoring without changing the selected direction.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Select O3: one conditional workflow-managed reference, one output asset, and one consolidated universal contract. | It offers the best balance of common-path reduction, direct-use clarity, semantic ownership, and bounded package complexity. | O0 leaves the problem intact; O1 and O2 leave conditional procedure inline; O4 fragments policy across too many resources. |
| 2026-08-11 | Treat 30–45 percent as a planning range rather than an acceptance threshold. | Semantic and lifecycle preservation take precedence over numeric optimization. | A hard threshold could encourage unsafe deletion or concealment. |
| 2026-08-11 | Exclude target-agent runtime acceptance. | Deterministic package proof and independent semantic review establish the relevant contract without creating a model-behavior test system. | Prompt journeys and transcript grading are nondeterministic and outside repository ownership. |

## Next Artifacts

- Formal proposal review.
- Contract-level feature specification after proposal approval.
- Architecture assessment after approved specification review, followed by architecture work only when required.
- Execution plan and traceable test specification after the governing contract and architecture decision are stable.

## Follow-on Artifacts

None yet

## Readiness

Ready for `proposal-review`.
The proposal selects one bounded package design and leaves only specification-level trigger wording, compatibility inventory, and architecture-assessment questions open.
