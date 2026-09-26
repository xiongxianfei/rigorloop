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
│   ├── modules/                 Architectural responsibility
│   └── interfaces/              Interaction contracts
└── support/
    └── schemas/                 Self-contained requirement and system-design schemas
```

## Initial scope

The [requirements index](requirements/README.md) records the completed analysis for the declared initial scope of seven IRs: 32 SRs, 11 Features, 33 Functions, and 35 Scenarios.
The model covers durable knowledge, traceability, controlled changes, assurance, model conformance, authoring guidance, and learning, with shared responsibilities explicitly reused.
Each Scenario has one owning IR, an explicit stakeholder goal, observable interactions, and one primary Feature. The 35 reviewed Scenarios are `confirmed` as current analysis knowledge.
IRs, SRs, Features, and Functions retain `draft` status; analysis completion does not approve them or establish implementation or satisfaction.
Architecture collections still contain guidance only, and each Function explicitly records why allocation is deferred.
No existing contract has been migrated or retired.
The [review outcome](requirements/README.md#review-outcome) identifies the assessed scope, resolved findings, model digest, and focused validation results.

Requirement records use the JSON authoring shape described in their index, including seven structured 5W2H analysis objects, explicit assumptions and constraints, and one consequential open question only when needed.
Self-contained IR, SR, Scenario, Feature, and Function schemas define the current draft shapes under [Operational Support](support/README.md).
Broader metamodel rules and runtime tooling integration remain to be designed.

The [existing System design](../docs/design/system.md) and its contracts govern existing behavior during migration.
An existing requirement's name or identifier alone does not establish its REM classification.

Migration must preserve meaning, identity, applicable decisions, and verification obligations.
Map each obligation to its destination before retiring its source.

## Model boundaries

Requirements use a containment tree; relationships across domains use stable entity identities.
Author each relationship once and derive inverse views rather than maintaining duplicate lists.
An entity's identity remains stable when its display name or location changes.

Current entity definitions belong in this model.
Change records explain their evolution, and verification evidence supports claims about specific assessed states.
Operational Support defines the draft shapes and the ownership of their cross-domain references; broader lifecycle, architecture, and maintenance rules remain to be developed.
