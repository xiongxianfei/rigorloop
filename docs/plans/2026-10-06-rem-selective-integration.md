# Selective REM integration

## Purpose / big picture

Make the existing REM easier to navigate and apply while adopting only the three improvements selected by the user: smaller knowledge documents with Practices, examples and attributable sources; dedicated verification and intended-use validation methods; and explicit architecture-view tailoring.
The semantic baseline is REM at commit `5f1894abc8aeb8353f7cf8ba852edb28f36e3d72`.
The refined reconstruction supplies candidate material, not replacement authority.

## Current Handoff Summary

- Owning Change: `2026-10-06-rem-selective-integration`; resume through `rigorloop change context`.

Mutable progress, review judgments, exact assessed identities and execution results belong to that Change.

## Source artifacts

- Requirement reuse: IR-006/SR-032–034 (canonical guidance and examples), IR-004/SR-025–029 (assessment and evidence), IR-009/SR-056/SR-083 (consistent guidance and bounded adoption).
- Design owner: [Engineering authoring](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md), particularly DES-SR-05/11/15/22.
- Target composition: [REM guidance composition](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/rem-guidance.md).
- Packaging owner: [Package production](../../design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md).
- Review and acceptance standing: owning Change; these references do not assert approval of unrelated draft product capabilities.

## Context and orientation

`rem/` owns portable methodology; `design/` applies it; `skills/` owns published procedures.
`scripts/project-operational-guidance.py` projects selected canonical REM documents into skill resources.
The starting working tree contains an untracked reconstruction and deletions of the old REM files.
Preserve that exact input privately before reconciling it with the tracked baseline.
Inspect actual sources and consumers; the project map is not relied upon for this reorganization.

## Non-goals

- Changes to IR/SR/AR parentage, Scenario ownership/cardinality, all-seven 5W2H analysis, open-question limits, Function coverage, primary Module ownership or subordinate realization identity.
- New runtime formats, public skills, lifecycle gates, adoption profiles or customer migration behavior.
- A standalone REM release, checksum protocol, archive validator or publication workflow.
- Claims that examples demonstrate actual product satisfaction or stakeholder usability.

## Requirements covered

SR-032/033 and SR-056 map to canonical document ownership, navigation and portable generated references.
SR-034 and SR-025–029 map to worked examples, explicit method inputs/outputs and truthful planned-versus-observed assessments.
SR-083 and DES-SR-11/15 map to preservation of method semantics and coordinated consumer updates.
DES-SR-05/22 map to concern-based view selection without omitting material architectural questions.

## File disposition map

| Baseline or proposal content | Final owner | Treatment |
| --- | --- | --- |
| `rem/README.md` | Same entry point | Restore baseline meaning; navigate accepted additions. |
| `rem/concepts/README.md` | Concept index and focused concept documents | Move original sections with unchanged definitions; add intended-use validation distinction. |
| `rem/principles/README.md` | Principle index and individually named principles | Preserve all 22 principles and numbering; refine only view selection wording. |
| Requirements, Scenario and System Design models | Existing model paths | Preserve obligations and cardinalities; reconcile moved links. |
| Architecture Design model | Composition plus allocation, boundary and realization documents | Split cohesive sections without altering responsibility or identity rules. |
| Operational Support model | Existing owner | Preserve representation, authority and maintenance rules. |
| Existing analysis/allocation methods | Existing owners | Preserve procedures and reconcile links. |
| Architecture Design method | Composition plus realization-design procedure | Extract material realization guidance without losing reasoning or completion criteria. |
| Architecture Views method | Core method, focused view documents and presentation guidance | Split by concern; explicitly record selection, omission, combination and additional views. |
| Knowledge reconstruction guide | Practice reading guide and focused explanations | Preserve explanations and examples; update navigation and accepted refinements. |
| Refined Practices and example | Practices and one bounded worked example | Rewrite against baseline semantics; preserve rejected material privately. |
| Refined verification/validation methods | Two dedicated REM methods | Adapt to existing model owners and evidence rules; introduce no workflow gate. |
| Refined source references | Selected source notes and source index | Verify the cited primary sources and state claim-specific limits; no imported claims of executed checks. |
| Refined alternative models/methods and release machinery | Preserved private proposal only | Exclude from the current canonical tree after preserving original bytes. |
| Skills, projections and live references | Existing owning consumers | Update together; remove obsolete generated resources. |

## Milestones

### M1. Preserve and split canonical knowledge

Prerequisites: accepted requirement reuse, reviewed target composition and delivery plan.
Preserve the starting tree, recover baseline sources, split cohesive owners and rewrite all affected live links.
Completion: all baseline sections have a destination; unchanged semantics remain inspectable; no competing proposal owners remain in the canonical tree.
Proof: section-transfer comparison against the baseline, link/anchor checks and explicit inspection of the protected invariants.

### M2. Integrate accepted methods and Practices

Add assessment procedures, explicit view applicability and a worked engineering example using the retained rules.
Source notes distinguish external support from REM-specific decisions.
Completion: readers can select a method and identify its inputs, outputs, evidence limits and applicable owners.
Proof: concrete walkthrough of requirement parentage, Scenario/Feature/Function distinctions, allocation, assessment plans and view selection; source inspection; independent semantic review.

### M3. Reconcile consumers and distribution

Update canonical skills and their resource selection, regenerate references, and remove obsolete generated files.
Completion: repository links and published resources resolve to the same current meaning; relevant checks pass.
Proof: projection freshness, resource validation, isolated adapter generation/validation and selected repository CI.

## Final review checkpoint

After all milestones, obtain one independent whole-change Code Review covering sources, consumers, generated resources, exclusions and proof.
Corrections are reassessed within the same gate before distinct final Verify.

## Change-level verification

Demonstrate that a reader starting from REM and an agent starting from a packaged skill reach compatible governing definitions, that no rejected rule enters the delivered methods/examples, and that tailored views retain all applicable concerns and provenance.
Structural checks cannot establish method effectiveness for actual stakeholders; no such empirical claim is made.

## Validation plan

- Baseline section-transfer and link/anchor inspection: detect dropped knowledge and stale navigation.
- `python scripts/project-operational-guidance.py --check`: generated guidance matches canonical sources.
- Existing skill/resource and isolated adapter checks selected by `bash scripts/ci.sh --mode local`.
- `bash scripts/ci.sh --mode explicit --path rem/README.md`: initial focused validation.
- `bash scripts/ci.sh --mode local`: final actual changed-scope checks using a qualified runtime.
- Independent semantic review: protected rules, example consistency, assessment scope and concern coverage.

## Risks and recovery

The proposal embeds rejected semantics in examples, metadata and links; use baseline-first extraction and explicit semantic review.
Splitting may break anchors or omit packaged dependencies; reconcile all live consumers and inspect actual generated resources.
Preserve original uncommitted bytes in private project-local storage and retain the baseline commit; recovery restores only this Change's owned edits, preserving unrelated work.

## Dependencies

Requirement Review precedes target-design reliance; integrated Design Review precedes delivery reliance; Delivery Review precedes implementation.
Source verification informs attribution only and cannot approve a local engineering rule.

## Readiness

See the owning Change for current progress, review applicability and final verification.
