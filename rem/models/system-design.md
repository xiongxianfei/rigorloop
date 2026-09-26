# System Design model

System Design describes what capabilities exist and what logical behavior realizes them.
The [concept definitions](../concepts/README.md) distinguish Features and Functions from Requirements.

```text
Feature ── realizedBy ──> Function
```

A Feature is durable and may evolve under many Requirements and Changes.
A Function may realize several Features; it is not contained exclusively by one Feature.
Requirements constrain these assets through explicit relationships rather than becoming their parents.

## Function definition

A Function SHOULD have clear inputs, outputs, and behavior.
Describe relevant state, conditions, and failure outcomes where they affect understanding of that behavior.
Keep the logical behavior independent of physical software structure wherever practical.

A Function SHOULD have an accountable architectural responsibility unless the architecture deliberately leaves it unallocated.
Allocation is owned by the [Architecture Design model](architecture-design.md).
Implementation references identify realization without replacing the logical definition.

## Evolution

New requirements may add Functions or change existing behavior while preserving the Feature's identity.
Current assets describe the resulting current system directly.
Changes explain the transitions, and historical states retain their own meanings.

A Feature-to-Function relationship is authored once; the opposite navigation view is derived.
The project representation chooses its storage direction without creating two independently maintained facts.
