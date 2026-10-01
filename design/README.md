# RigorLoop engineering model

This directory starts the manual refactor toward the proposed RigorLoop Engineering Method (REM).
The initial scope is Requirement Analysis, System Design, and Architecture Design.
The reusable methodology is maintained in [rem/](../rem/README.md); this directory records its application to RigorLoop.

| Domain | Content | Engineering question |
| --- | --- | --- |
| [Requirement Analysis](requirements/README.md) | Initial, System, and Allocated Requirements; Scenarios | Why is this needed, in which situations, and what must be satisfied? |
| [System Design](system/README.md) | Features and Functions | What capabilities and logical behavior does the system provide? |
| [Architecture Design](architecture/README.md) | Modules and Interfaces | Where does responsibility live, and how do elements interact? |
| [Operational Support](support/README.md) | Record schemas and relationship conventions | How is engineering-model content represented and checked? |

```text
design/
├── requirements/                 IR → SR → AR
│   └── scenarios/               Governed situations, each owned by one IR
├── system/
│   ├── features/                Durable capabilities
│   └── functions/               Logical behavior
├── architecture/
│   ├── modules/                 Owner directories: module.json + optional realization/
│   ├── interfaces/              Owner directories: interface.json + optional realization/
│   └── views/                   Derived 4+1 views and supporting perspectives
└── support/
    └── schemas/                 Self-contained model authoring schemas
```

## Current scope

The [requirements index](requirements/README.md) records 10 IRs, 76 SRs, 22 Features, 73 Functions, and 80 Scenarios.
The original seven-IR analysis covers durable knowledge, traceability, controlled changes, assurance, model conformance, authoring guidance, and learning.
The [published-product extension](requirements/published-products.md) adds explicit CLI operations, portable guided engineering activities, and trustworthy compatible tooling distribution, with shared responsibilities reused.
Each Scenario has one owning IR, an explicit stakeholder goal, observable interactions, and one primary Feature. 70 Scenarios are confirmed: 57 retain their earlier scope and eight workflow and five browser Scenarios are confirmed by their document-based author assessments. Five revised and five local-history Scenarios remain draft.
The [requirement-first workflow package](requirements/workflow-refactor.md) proposes IR-009 refinement and stage-specific obligations before detailed skill and architecture refactoring.
IRs, SRs, Features, and Functions retain `draft` status; analysis completion does not approve them or establish implementation or satisfaction.
The [architecture draft](architecture/README.md) proposes 19 Modules in four responsibility trees and retains primary allocations for the original 63 Functions; four new local-history Functions have explicit deferred allocation. The 15 children retain their direct allocations; the four parents own broader integration boundaries with derived descendant coverage.
Its first detailed example covers IR-001 with nine ARs and two Interfaces, plus one shared interpretation AR under SR-012 in IR-005. The published-product extension added four Interfaces. The [parent-boundary contract analysis](../docs/changes/2026-09-26-rem-architecture-refinement/boundary-contracts.md) adds four selected contracts for engineering-state inspection, adopted model-authoring guidance, action authority, and claim evidence support. The current model contains twelve Interfaces and 317 engineering entities. Further Interfaces and ARs remain explicitly deferred where their cooperation is not yet designed.
IR-008 has 18 ARs, with the workflow allocation bringing the model to 42 overall. Its nine SRs include the history-query extension; earlier allocation arguments for changed SR-042–045 criteria are explicitly historical pending reconciliation. The [cooperation view](architecture/views/browser/index.html#cooperation) relates the original nine command Scenarios to their two Modules and two Interfaces; the [logical view](architecture/views/browser/index.html#contributions) renders the SR-owned arguments. The workflow extension adds AR-029–042 under IR-009; remaining product allocation and detailed realization stay scoped.
The [4+1 views](architecture/views/README.md) provide a Logical overview beginning with the parent Modules and exposing lower-level detail, plus Process, Development, and Physical projections of the recorded CLI, skill catalog, product production, and installation facets. The Scenario projection selects SCN-019, SCN-046, SCN-047, SCN-053, and SCN-066 with explicit contract scopes. Engineering-state inspection does not establish Baseline retention, guidance covers the adopted model-authoring branch, and authority and evidence assessments remain separate inputs to release coordination. Remaining realization and platform qualification stay explicit.
The [architecture browser](architecture/views/browser/index.html) provides shared navigation across all five views, clickable Module/Interface diagrams, and separate searchable public command and skill catalogs. Module details retain complete allocations and provenance. IF-004's interaction facet and MOD-012's software facet own observed names and separately proposed Function correspondence; Feature and accountable Module context derive from existing relationships. The same skill entries generate the [published inventory](requirements/published-products.md#existing-published-capabilities-and-owners). MOD-013's software facet records source inputs, transformations, and candidate output layouts for skills and CLI packaging. These subordinate observations do not add engineering entities, change Function allocation, or establish successful builds.
The extension maps 130 numbered obligations in six existing product contracts. Their detailed authority remains retained; no source is retired or declared fully migrated.
The [system-analysis review](requirements/README.md#review-outcome) and [first architecture review](architecture/README.md#review-and-validation) retain their earlier subjects. The [published-product review](requirements/published-products.md#review-and-validation) identifies the extended model and its checks.
The later [CLI allocation review](../docs/changes/2026-09-26-rem-architecture-refinement/architecture-review.md#review-and-validation) records its separate subject and validation results.

Requirement records use the JSON authoring shape described in their index, including seven structured 5W2H analysis objects, explicit assumptions and constraints, and one consequential open question only when needed.
Eight self-contained schemas define IR, SR, AR, Scenario, Feature, Function, Module, and Interface records under [Operational Support](support/README.md). Seven additional self-contained schemas validate optional architecture realization facets; these files are subordinate to their Module or Interface and do not add entity types.
Broader metamodel rules and runtime tooling integration remain to be designed.

The [existing System design](../docs/design/system.md) and its contracts govern existing behavior during migration.
An existing requirement's name or identifier alone does not establish its REM classification.

Migration must preserve meaning, identity, applicable decisions, and verification obligations.
Map each obligation to its destination before retiring its source.

## Model boundaries

Requirements use a containment tree; relationships across domains use stable entity identities.
Author each relationship once and derive inverse views rather than maintaining duplicate lists.
An entity's identity remains stable when its display name or location changes.

Module composition belongs to the existing parent responsibility; system-wide composition belongs to the architecture index. The [workflow composition](architecture/README.md#requirement-first-workflow-composition) applies this boundary without adding a workflow submodel. Entity records own facts, subordinate realization facets own choices and rationale, and generated views present those sources. Accepted design remains current until deliberately revised; review outcomes and execution results identify their assessed subjects separately. Delivery sequencing belongs in the owning plan.

Current entity definitions belong in this model.
Change records explain their evolution, and verification evidence supports claims about specific assessed states.
Operational Support defines the draft shapes and ownership of cross-domain references; broader lifecycle, remaining architecture interactions, and maintenance rules remain to be developed.
