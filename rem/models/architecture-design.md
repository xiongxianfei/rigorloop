# Architecture Design model

Architecture Design assigns responsibility to Modules and defines interactions through Interfaces.
The [concept definitions](../concepts/README.md) explain those architectural assets.

## Allocation

```text
Feature ── realizedBy ──> Function ── allocatedTo ──> Module
SR ── derivation ──> AR ───────────── allocatedTo ──> Module
```

Functional allocation identifies responsibility for behavior.
Requirement allocation identifies responsibility for satisfying an obligation.
Review these allocations together so the assigned behavior, data, policies, and interfaces can satisfy the allocated requirements.

This convergence does not require every AR to pair with one Function.
An obligation may concern state, quality, or another architectural responsibility.
Do not create a Function solely to make a diagram symmetrical.

## Modules and Interfaces

A Module describes a meaningful responsibility boundary and may own behavior, state, dependencies, and technical policies.
A Module can `provide` and `consume` Interfaces; each Interface defines the interaction contract.
The canonical relationship labels are `provides` and `consumes`.

An Interface may specify operations, messages, data structures, inputs, outputs, protocols, failures, and compatibility rules.
Architecturally important interactions SHOULD be explicit Interfaces.
An Interface can describe an internal interaction and need not be a network API.

## Realization and consistency

Modules and Functions may have `realizedBy` references to Implementation.
Architecture boundaries need not map one-to-one to source directories, packages, processes, or deployment units.
Such mappings are implementation decisions and must be understandable where they matter.

Allocated targets must resolve to compatible architectural entities.
An unexplained missing responsibility or incompatible interface is a design issue even if a diagram can be rendered.
Preserve historical allocations when current architecture evolves.
