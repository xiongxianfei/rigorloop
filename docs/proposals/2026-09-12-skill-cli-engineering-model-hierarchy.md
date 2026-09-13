# Skill, CLI and Engineering model hierarchy

Owning change: [unified-validation-model](../changes/2026-09-12-unified-validation-model/change.json).

## Challenge

RigorLoop publishes skills and a CLI, but its current model inventory mixes product behavior, data contracts, development methods and delivery operations at one level. Skill is too narrowly defined around presentation, while behavior is scattered across peer owners. System consequently explains document relationships more readily than how the project produces useful skills and a reliable executable.

## Goals

Organize the project around three main models: Skill defines published skill behavior, CLI defines executable behavior, and Engineering defines how RigorLoop realizes and proves both using its own workflow. Permit cohesive submodels within each main model. System explains the product, its hierarchy, shared interfaces and the path to high-quality published artifacts. Preserve independent tests, bounded parallel execution, removal of validation caching and actual cleanup of superseded designs and exclusive scripts.

## Scope and non-goals

| User intent | Treatment | Scope allocation |
| --- | --- | --- |
| Three main models with useful submodels | in scope | core to this proposal: decompose responsibilities around the two deliverables and their engineering process. |
| Skill owns behavior, not only presentation | in scope | core to this proposal: reconcile capability inputs, procedures, outputs, handoffs, failure behavior and limits with existing specialist contracts. |
| CLI owns executable behavior | in scope | core to this proposal: reconcile commands, records, side effects, compatibility, installation and recovery under the executable product boundary. |
| Engineering explains development through RigorLoop itself | in scope | core to this proposal: define development, validation, packaging and release responsibilities without duplicating product behavior. |
| Independent cases, parallel validation and no cache | in scope | separate implementation slice: retain the selected unified-Validation outcomes under Engineering. |
| Remove obsolete designs, scripts and default cache directory | in scope | separate implementation slice: exact source/consumer disposition and removal; preserve remaining proof and historical record identities. |
| Coherent interfaces, governance and generated consumers | in scope | same-slice dependency: reconcile affected instructions and contracts with each transferred responsibility. |

Individual skills remain usable without the CLI for their scoped outputs. The current governed workflow-recording features require the CLI for inspection and safe persistence; independent skill use does not claim that governed completion. Skill installation through the CLI requires the executable for that method only, not as a prerequisite for every way of obtaining or using skills. These usage boundaries constrain both Skill and CLI design.

This is an expansion of the earlier [unified-Validation direction](2026-09-12-unified-validation-model.md), not a cancellation of its goals. Its original proposal and review remain evidence of that narrower direction. No new customer runtime, orchestration service, skill inventory expansion, validation cache or automatic external publication is selected. Main-model count does not prescribe exactly three files, a directory migration, or one submodel per skill. Delivery owns implementation sequencing and proof allocation.

## Governing principle

Organize contracts around what the product must do and how the project establishes that it does it; give each behavior one owner.

## Proposed direction

System is the composition root for Skill, CLI and Engineering. Skill owns published capability behavior and common capability conventions. CLI owns the observable behavior of the executable and its data interfaces. Engineering owns this repository's development, validation, packaging and release method and uses the skill and CLI contracts without redefining them.

Each main model can delegate a coherent responsibility to a named submodel. Its parent defines the boundary and integration; the child defines the detailed contract once. Cross-model consumers reference that contract. Existing Workflow, Design, Review and Closeout, Record Format, Validation, Distribution and Release responsibilities must be reconciled into this hierarchy by obligation rather than by blindly moving whole files. For example, the public installation command belongs under CLI, while producing and checking its distributable input belongs under Engineering.

The product behavior of an assessment skill and the repository's decision to require that assessment are distinct. Likewise, a candidate CLI being assessed cannot acquire correctness merely because development used RigorLoop. Engineering identifies the development tool basis and candidate evidence so that self-use supports delivery without replacing independent judgment.

## Feasibility

Assessment: feasible as a bounded model consolidation with coordinated consumer changes. The two implementation surfaces already exist at `skills/` and `packages/rigorloop/`. Existing models cover the relevant methods, record format, validation execution, packaging and release; the main work is preserving and reallocating their contracts rather than inventing another runtime.

The principal uncertainty is the exact split of mixed responsibilities, especially shared proof criteria, skill assessment behavior versus repository closeout policy, and installation behavior versus package production. Design must assign each retained obligation one owner, identify actual readers and preserve negative/recovery proof before source deletion. No technical blocker prevents that design work. The breadth requires reviewed implementation slices; renaming headings alone will not complete the direction.

## Impact and major trade-offs

This expands beyond the previously reviewed Validation proposal. The earlier approval does not establish approval of three-model ownership changes. Current reviewed contracts retain their applicable authority until the explicitly mapped changes are adopted; historical records and judgments retain their exact subjects.

Hierarchy makes the product easier to reason about but adds value only when children have clear boundaries. Engineering must not become a duplicate copy of every published skill, and Skill must not absorb implementation mechanics merely because an agent invokes them. Exact source transfers, governance reconciliation and cleanup remain required parts of the initiative.

## Decision requested

Record the user's accepted direction of three main models with cohesive submodels and the retained validation/cleanup goals. Independent Proposal Review assesses this expanded direction before detailed ownership-transfer Design and Delivery rely on it. This proposal does not claim that review, implementation or final verification has occurred.
