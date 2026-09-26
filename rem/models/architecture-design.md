# Architecture Design model

Architecture Design assigns accountable responsibility to Modules and defines architecturally significant interactions through Interfaces.
The [concept definitions](../concepts/README.md#system-and-architecture-assets) explain these architectural assets.

## Allocation

```text
Feature ── realizedBy ──> Function ── primaryModule ──> Module
                                 └── supportingModule ──> Module (0..*)

SR ── derivation ──> AR ── allocatedTo ──> Module
```

Functional allocation and requirement allocation are separate engineering relationships.
Review them together so the assigned behavior, state, policy, data, and interfaces can satisfy the allocated obligations.

## Function allocation cardinality

Every active Function MUST have exactly one accountable primary Module before architecture allocation is considered complete.
A Function MAY involve zero or more supporting Modules.

The primary Module owns the architectural responsibility for the Function.
Supporting Modules may contribute required behavior or services without becoming co-owners of the Function.

If no single Module can own the Function coherently, reconsider the Function boundary or Module boundaries rather than leaving responsibility ambiguous.

## AR allocation cardinality

Every active AR MUST be allocated to exactly one Module.

If an allocated obligation genuinely belongs to several Modules, decompose it into separate ARs under the same parent SR so each lower-level obligation has one accountable Module.
Do not assign one AR to several Modules to avoid deciding responsibility.

This convergence does not require every AR to pair one-to-one with a Function.
An AR may govern state, quality, policy, data, or another architectural responsibility.

## Modules

A Module is a meaningful architectural responsibility boundary and may own:

- Functions;
- state or data;
- policies and constraints;
- provided and consumed Interfaces;
- dependencies;
- realization scope.

Module boundaries SHOULD be justified by responsibility and evolution rather than copied mechanically from current source directories, packages, processes, or deployment units.

## Interfaces

A Module may `provide` and `consume` Interfaces.
The canonical relationship labels are `provides` and `consumes`.

Each Interface MUST have exactly one provider Module.
An Interface MAY have zero or more consumer Modules.
An Interface may describe operations, messages, data structures, inputs, outputs, protocols, failure semantics, and compatibility constraints.
Architecturally significant cross-Module interactions SHOULD be explicit Interfaces.

An Interface can describe an internal interaction and need not be a network API.

## Allocation consistency

For each Module, architecture review SHOULD consider together:

- Functions for which it is primary;
- Functions it supports;
- ARs allocated to it;
- state and data it owns;
- policies it must enforce;
- Interfaces it provides or consumes.

An unexplained missing responsibility, conflicting owner, or incompatible Interface is a design issue even when a diagram can be rendered.

Use [Architecture Allocation](../methods/architecture-allocation.md) to assign and reconcile these responsibilities.

## Realization and history

Modules and Functions MAY have `realizedBy` references to Implementation.
Architecture boundaries need not map one-to-one to source directories, packages, processes, or deployment units.
Such mappings are realization decisions and must not redefine architecture implicitly.

Preserve historical allocations when current architecture evolves.
Later allocation does not rewrite responsibility in an earlier Baseline.
