# Refine the complete skill inventory and retire stale support

## Challenge

Recent rounds simplified selected skills and retired standalone architecture/ADR authoring. The remaining question is whether every published skill and its supporting material still explains and protects the current design clearly. Repeated recording procedure, stale artifact labels and tests tied to incidental wording can preserve maintenance work without improving supported outcomes.

Initial source inspection at `3c4985f80b242a295116880a5aee9cbbf47b12b0` identifies concrete candidates: the [PR body skeleton](../../skills/pr/assets/pr-body-skeleton.md) still requests an `Explain-change` path although successful Verify owns that explanation; the [validation catalog](../../scripts/lib/validation/validation_selection.py) describes `<change-yaml>` for a wrapper that validates current record sets; and [query-change-record.py](../../scripts/query-change-record.py) exists solely to reject a retired interface. These observations justify assessment, not automatic deletion. Earlier approvals and justified retention decisions remain valid for their original scope.

## Goals

- Assess all 19 published skills and refine every skill whose current instructions, descriptions, resources or output structures need improvement.
- Retire stale descriptions, obsolete resources and unnecessary test cases or scripts, resolving their live dependencies in the same change.
- Preserve supported behavior, specialist judgment, portable use, authority boundaries and distinct failure detection.
- Finish with an explicit refinement or retention disposition for the full inventory, rather than treating a small pilot as completion.

## Scope and non-goals

The scope includes authored skills, shared guidance, current contributor descriptions, supporting scripts, repository and package tests, fixtures, validation selection and packaging consumers. All tests and scripts receive a relevance assessment; only established stale or redundant material is changed. An initial candidate list does not limit the final inventory assessment.

| Initial user intent | Treatment | Destination |
| --- | --- | --- |
| Refine all necessary skills | in scope | Complete skill inventory, with justified edits or retention. |
| Retire stale descriptions | in scope | Current entrypoints, references, assets and directly affected documentation/catalog descriptions. |
| Remove unnecessary test cases | in scope | Repository and package test assessment against current protected failures, including generated cases and fixtures. |
| Remove unnecessary scripts | in scope | Current commands, wrappers and rejection shims assessed with callers, compatibility and replacement proof. |

| Work item | Scope budget treatment | Boundary |
| --- | --- | --- |
| Complete inventory and current-owner mapping | core to this proposal | Record dispositions in ordinary Design, plan and evidence surfaces; no permanent cleanup ledger. |
| Remaining coordination, assessment and handoff guidance | first-slice candidate | Inspect route, verify, pr and review-family navigation and recording detail; Design determines justified changes. |
| Authoring, implementation, discovery and foundation skills | separate implementation slice | Include recently refined skills; retain them where current evidence supports no change. |
| Stale descriptions, test consolidation and script retirement | separate implementation slice | Establish protected behavior and actual dependencies before selecting removals. |
| Shared guidance, validators, selectors, direct callers and package reconciliation | same-slice dependency | Ship each selected cleanup as a complete supported unit. |
| New product capabilities, changed review gates, permissions or record formats | out of scope | A discovered need for such changes returns to its direction owner. |
| Withdrawal of a currently promised obsolete command or rejection shim | core to this proposal | Requires an explicit affected-owner retirement decision before implementation, with current safety obligations retained. |
| Release, publication or installation into active environments | out of scope | Validation supplies no external deployment authority. |

The complete skill population is: proposal, design, plan, proposal-review, design-review, delivery-review, implement, code-review, bugfix, ci-maintenance, route, verify, pr, explore, research, vision, constitution, project-map and learn. Delivery may divide the work into coherent slices without silently deferring any of the four user goals.

## Governing principle

Keep what helps perform or protect a supported task; remove what no longer serves that purpose.

## Proposed direction

Assess each skill against its current owning Design and supported invocation contexts. Make the purpose, prerequisites, core procedure, outputs and limits easy to locate. Simplify repetitive instructions and stale descriptions; place substantial conditional procedure behind clear triggers where that reduces interpretation work. Retain local reminders and specialist detail where they prevent real mistakes. Do not impose one layout or a length quota on every skill.

For every proposed retirement, identify the current obligation, actual consumers and surviving owner or explicit retirement decision. Existing records and historical judgments retain their original meaning. Old-looking names, compatibility guidance and negative tests are not automatically obsolete. Recently improved packages receive the same assessment without a requirement to edit them again.

Assess tests by the plausible failure and observation boundary they protect. Consolidate or replace overlapping checks only after establishing equivalent retained protection; remove checks whose exclusive obligation is explicitly retired. Prefer observable structural or executable failures over incidental prose assertions where suitable, while retaining targeted instruction guards until their owner approves a sufficient replacement. Independent review owns semantic instruction quality; a passing suite alone cannot prove safe removal.

Assess scripts as supported interfaces as well as implementation files. Distinguish unused helpers, active wrappers and intentional rejection shims. Reconcile imports, commands, catalog entries, selectors, direct invocation, generated packages and documentation together. A broad scan identifies candidates; complete caller and protection evidence determines whether each is retained, refined or retired.

Completion requires accounted-for inventory scope, resolved uncertain removals, preserved current obligations and appropriate independent review and validation. Detailed contract amendments, exact deletion sets, delivery sequencing and proof selection belong to Design and Delivery.

## Feasibility

Assessment: feasible using current ownership, conditional resources and validation machinery. [Skill](../design/skill/skill.md), [Assessment](../design/skill/assessment.md) and [Validation](../design/engineering/validation.md) already support proportional guidance, semantic review and protection-preserving maintenance. Existing packaging checks cover canonical-to-installed resource consistency. No new evaluation platform or cleanup subsystem is needed.

The initial inspection covers all entrypoint/resource counts and selected concrete source paths; it is not a completed semantic audit of all skills or a case-by-case test/script assessment. Route, Verify and several review entrypoints still contain substantial inline recording or overlapping control guidance. This warrants inspection, not a claim that their current behavior is defective. The [guidance tests](../../tests/skill/skill_guidance_tests.py) explicitly retain a phrase-based semantic-checklist guard pending an owner-backed replacement; that is a useful assessment target, not permission to discard its protection.

The retired query helper illustrates the main constraint: its [tests](../../tests/engineering/validation/test-query-change-record.py) protect rejection without reading or mutating historical input, and the validation catalog still invokes them. The [metadata wrapper](../../scripts/validate-change-metadata.py) also has active callers and cannot be declared redundant merely because it delegates to another validator. Missing callers, unclear compatibility or unproven replacement protection block the affected retirement. No blocker to beginning Design is known.

## Impact and major trade-offs

This round is broader than the previous focused changes. It can reduce unnecessary instructions and maintenance while increasing review risk if unrelated responsibilities are rewritten together. Coherent delivery slices and explicit retention decisions keep the scope reviewable without dropping the inventory commitment.

Removing a rejection shim can change an old command from a structured unsupported-interface response to an absent command. That compatibility consequence must be explicitly selected by its owning Design; it must not weaken rejection of unsupported inputs through retained interfaces. Moving instructions into references is valuable only when the complete task becomes easier to follow. No test-count reduction, runtime improvement or universal agent-compliance claim is promised.

## Decision requested

Approve a complete inventory refinement and support-retirement round under the preservation and compatibility bounds above. Carry all four user goals through independent Proposal Review, affected Design reconciliation and reviewed delivery allocation. Exact file/test removals and any withdrawal of a promised obsolete entrypoint require the owning Design decision; this proposal does not itself approve those deletions or external publication.
