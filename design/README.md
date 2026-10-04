# RigorLoop engineering model

This is the current repository-held engineering definition. The reusable method lives in [rem/](../rem/README.md); this tree records its application to RigorLoop. Entity status, review applicability and implementation claims retain their explicit scope. A relocation or generated view does not approve a draft or establish implementation.

| Domain | Owns | Start here |
| --- | --- | --- |
| Requirements | IR, SR, AR and governed Scenarios | [Requirement model](requirements/README.md) |
| System design | Features and logical Functions | [System model](system/README.md) |
| Architecture | Modules, Interfaces, realization and composition | [Architecture model](architecture/README.md) |
| Support | Representation, repository practices and shared testing rules | [Support](support/README.md) |

```text
design/
├── requirements/     IR → SR → AR; Scenarios
├── system/           Features and Functions
├── architecture/
│   ├── modules/      Module records, detailed contracts and realization
│   ├── interfaces/   Interface records and realization
│   ├── composition.md
│   └── views/        Generated projections and browser
└── support/          Schemas, development, validation and shared test rules
```

## Model boundaries

Requirements define obligations; System Design defines logical behavior; Architecture Design defines accountable boundaries and realization. Stable entity IDs survive display-name and location changes. Author each relationship once and derive inverse views.

Detailed Markdown contracts remain beside their responsible Module or Interface. [Ownership](support/ownership.md) defines their status and maps current responsibilities; [architecture composition](architecture/composition.md) retains system-wide cooperation and integrated acceptance. Contract clause IDs remain source-qualified references, not new REM entities. Repository check execution is supporting practice, distinct from product model conformance.

Current definitions, applicable rationale and design proof intent belong here. CLI-managed local records own mutable Change state, review judgments and execution results; bulky evidence lives in the artifact store. Current meaning is readable without the operational database. Historical assessments keep their original subjects and are not promoted by this consolidation.

The [architecture browser](architecture/views/browser/index.html) projects owned entity, realization and supporting design sources. It is a view of this model, not an independently authored design. See [view documentation](architecture/views/README.md) for generation and limitations.
