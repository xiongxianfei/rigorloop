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
    └── schemas/                 Self-contained model authoring schemas
```

## Current scope

The [requirements index](requirements/README.md) records 10 IRs, 61 SRs, 20 Features, 63 Functions, and 62 Scenarios.
The original seven-IR analysis covers durable knowledge, traceability, controlled changes, assurance, model conformance, authoring guidance, and learning.
The [published-product extension](requirements/published-products.md) adds explicit CLI operations, portable guided engineering activities, and trustworthy compatible tooling distribution, with shared responsibilities reused.
Each Scenario has one owning IR, an explicit stakeholder goal, observable interactions, and one primary Feature. The 62 reviewed Scenarios are `confirmed` as current analysis knowledge.
IRs, SRs, Features, and Functions retain `draft` status; analysis completion does not approve them or establish implementation or satisfaction.
The [architecture draft](architecture/README.md) proposes 15 Modules and assigns one accountable primary Module to each Function.
Its first detailed example covers IR-001 with nine ARs and two Interfaces, plus one shared interpretation AR under SR-012 in IR-005. Four further Interfaces connect the proposed command, record, guidance, packaging, installation, and release responsibilities. Further Interfaces and ARs remain explicitly deferred.
The extension maps 130 numbered obligations in six existing product contracts. Their detailed authority remains retained; no source is retired or declared fully migrated.
The [system-analysis review](requirements/README.md#review-outcome) and [first architecture review](architecture/README.md#review-and-validation) retain their earlier subjects. The [published-product review](requirements/published-products.md#review-and-validation) identifies the extended model and its checks.

Requirement records use the JSON authoring shape described in their index, including seven structured 5W2H analysis objects, explicit assumptions and constraints, and one consequential open question only when needed.
Eight self-contained schemas define IR, SR, AR, Scenario, Feature, Function, Module, and Interface records under [Operational Support](support/README.md).
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
Operational Support defines the draft shapes and ownership of cross-domain references; broader lifecycle, remaining architecture interactions, and maintenance rules remain to be developed.
