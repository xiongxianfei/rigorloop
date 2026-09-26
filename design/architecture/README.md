# Architecture Design

Architecture Design assigns responsibility and describes interactions between architectural elements.
The [REM Architecture Design model](../../rem/models/architecture-design.md) owns the reusable model semantics.

| Asset | Collection | Meaning |
| --- | --- | --- |
| Module | [modules/](modules/README.md) | Durable architectural unit of responsibility |
| Interface | [interfaces/](interfaces/README.md) | Explicit interaction contract |

```text
Allocated Requirement ── allocatedTo ──> Module
Function ────────────── allocatedTo ──> Module
Module ──────────────── provides ─────> Interface
Module ──────────────── consumes ─────> Interface
```

Requirement allocation and functional allocation approach the same architecture from different directions.
Review them together for consistency between a Module's assigned behavior and obligations.

ARs and Functions need not pair one-to-one.
An obligation may concern data, quality, or another architectural responsibility.

ARs and Functions own their `allocatedTo` references.
Modules own their `provides` and `consumes` references, while Interfaces own the interaction contract itself.
Derive inverse relationship views rather than authoring competing copies.

Architectural boundaries need not correspond one-to-one with packages or source directories.
Realization references identify implementation locations.
Keep architecture distinct from code organization.
