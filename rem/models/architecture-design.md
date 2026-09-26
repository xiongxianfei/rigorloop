# Architecture Design model

Architecture Design assigns accountable responsibility to Modules, defines architecturally significant interactions through Interfaces, and records the material physical/software realization needed to make that logical architecture implementable.
The [concept definitions](../concepts/README.md#system-and-architecture-assets) explain these architectural assets and the subordinate architecture realization view.

REM keeps two coupled views:

```text
Logical architecture
  Function / AR → Module ↔ Interface

Physical/software realization
  subordinate properties of those Modules and Interfaces
```

Modules and Interfaces remain the first-class governed architecture entities.
Physical/software realization details do not become independent REM entities by default.

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

## Architecture semantic outputs

Architecture Design produces semantic outputs rather than prescribing a document, directory, serialization format, or diagram.
For the declared architecture scope, the authoritative information is organized around the following concerns.

| Semantic output | Purpose | Primary owner | Expected when |
| --- | --- | --- | --- |
| Module definition | Defines accountable responsibility, purpose, owned state/data, policies, exclusions, and dependencies | Module | For every in-scope Module |
| Function allocation | Identifies the one accountable primary Module and any supporting Modules for logical behavior | Function relationship | For every active in-scope Function |
| AR allocation | Identifies the one Module accountable for a lower-level allocated obligation | AR relationship | For every active in-scope AR |
| Interface definition | Defines a significant logical interaction contract and its provider/consumers | Interface | When cross-Module interaction is architecturally significant |
| State/data ownership | States which Module owns meaning and permitted mutation of significant information | Module | When state/data authority matters to correctness or evolution |
| Software realization | Explains the software structures that materially realize a Module | Module realization view | When software structure matters architecturally |
| Runtime realization | Explains significant execution/process, lifecycle, scaling, isolation, concurrency, or resource boundaries | Module realization view | When runtime boundaries materially affect architecture |
| Persistence realization | Explains physical retention of significant state/data and whether it is authoritative, replicated, cached, or derived | Module realization view | When persistence choices materially affect architecture |
| Deployment realization | Explains significant packaging, placement, isolation, deployment target, or external runtime dependency | Module realization view | When deployment materially affects architecture |
| Interface realization | Explains material interaction mechanism, concrete binding, representation, addressing, and realization-specific guarantees | Interface realization view | When the logical contract requires a concrete architectural realization decision |
| Technology rationale | Explains a material technology selection, its driver, consequences, significant alternatives, and revisit conditions | Owning Module or Interface realization view | When the technology choice has durable architectural consequences |
| Architecture view | Presents selected authoritative information for review, such as logical, interaction, runtime, persistence, deployment, or technology perspectives | Derived | When a view improves understanding or review |

These outputs define meaning, not storage.
A project may represent them in one model, several files, a database, a modeling tool, or another controlled representation.
The representation MUST preserve the ownership and single-source-of-truth semantics above.

State/data ownership is logical authority, not a synonym for physical storage.
A persistence mechanism may retain bytes without owning their domain meaning or permitted mutation.

A realization facet is required only when omitting it would hide a material architectural consequence.
Do not create empty or speculative realization information merely for symmetry.

## Architecture realization views

Each in-scope Module and Interface MAY carry an architecture realization view.
The view records material physical/software choices whose consequences cross implementation units, affect runtime/deployment/state/quality behavior, constrain future evolution, or are needed to understand how the logical architecture is realized.

A realization detail is architecture-significant when at least one of the following is true:

- it changes responsibility, ownership, isolation, lifecycle, or failure boundaries;
- it materially affects a Requirement, AR, Interface guarantee, or system quality;
- it constrains independent evolution, deployment, recovery, compatibility, or security;
- removing it from the architecture model would make the implementation topology or an important design tradeoff misleading.

Incidental implementation choices that fail this test belong to implementation rather than Architecture Design.

A Module realization view may describe, when relevant:

- software units such as applications, libraries, services, workers, adapters, or jobs;
- execution or process boundaries and significant runtime topology;
- persistence mechanisms or datastores used to realize state owned or used by the Module;
- packaging or deployment units and significant deployment targets;
- implementation paths or artifact mappings;
- material technology selections and their rationale;
- significant external runtime dependencies.

An Interface realization view may describe, when relevant:

- interaction mechanism or protocol;
- concrete endpoint, channel, topic, file, ABI, or in-process binding shape;
- serialization or wire/data representation;
- addressing or discovery mechanism;
- technology selections required to realize the logical contract;
- realization-specific compatibility or failure semantics when required by the governing obligations.

These items are subordinate architecture information.
REM does not require stable global identities or independent lifecycles for a service, process, datastore, deployment unit, protocol, or technology choice merely because it appears in a realization view.
Its governed meaning is owned by the Module or Interface definition that contains or references it.

A project MAY use structured subordinate records and local identifiers for validation or tooling.
Aggregate runtime, datastore, deployment, or technology diagrams SHOULD be derived from the authoritative Module and Interface realization information rather than maintained as a second source of truth.

### Organizing subordinate facets

A representation MAY separate the logical Module or Interface definition from its material realization facets.
This separates concerns without introducing new architecture entities or moving logical authority into realization records.

| Owner | Possible realization facets |
| --- | --- |
| Module | Software, runtime, persistence, deployment, technology |
| Interface | Interaction, representation, technology |

These are useful organization choices, not a mandatory set of records for every owner.
Create a facet only when it contains material information or an explicit material deferral.
Its absence does not establish that the concern was assessed, resolved, or inapplicable; completion is assessed against the declared architecture scope.

Subordinate facets inherit their owner's identity, lifecycle, and baseline context unless the project deliberately governs a different arrangement.
When containment already identifies the owner, do not independently author a duplicate ownership relationship.
Separating records does not require an additional global identity or independent lifecycle for each facet.

Distinguish attributed observations of an existing realization from proposed choices and unresolved decisions within the relevant facet.
An observed implementation mapping does not approve a target choice or prove that the logical contract is satisfied.
Record each material technology choice and its rationale once; other affected facets reference that authoritative decision instead of reproducing it.
Shared software, runtime, or deployment mappings may span Modules without creating independently maintained copies of the same fact.

Logical, dependency, runtime, persistence, deployment, and technology views derive from the authoritative definitions, relationships, and facets.
A view may select and explain those facts for its audience, but a new architectural decision belongs with its accountable Module or Interface.
The [Operational Support model](operational-support.md) governs the selected representation and its validation rather than prescribing storage through these semantic rules.

## Logical-to-physical consistency

Physical/software realization MUST preserve the logical architecture rather than silently redefine it.
For each Module and Interface, architecture review SHOULD determine:

- which physical/software units realize the logical responsibility or contract;
- whether runtime/process boundaries preserve accountable ownership and failure boundaries;
- whether persistence choices preserve declared state/data authority;
- whether packaging and deployment choices preserve required interactions and isolation;
- whether selected technologies satisfy the relevant SRs and ARs without introducing unsupported obligations;
- whether a material physical choice has enough rationale to be understood and changed later.

One Module may be realized by several software units, and one software unit may realize responsibilities from several Modules when that composition is deliberate and remains understandable.
The same applies to process, datastore, and deployment mappings.
Do not force one-to-one mappings merely to simplify diagrams.

If a realization choice exposes a new system obligation or invalidates a Function, AR, Module boundary, or Interface contract, return the issue to the owning requirement or design model and reconcile it.

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
Module and Interface realization views may additionally record the physical/software mappings needed for architecture understanding.
Architecture boundaries need not map one-to-one to source directories, packages, services, processes, datastores, or deployment units.
Such mappings are subordinate realization decisions and MUST NOT redefine logical architecture implicitly.

A material realization change is an architecture change when it alters a durable Module responsibility, Interface contract, runtime/deployment constraint, state ownership, or another architecture-significant decision.
A purely internal implementation refactor that preserves those meanings need not change the architecture model.

Preserve historical allocations and realization meaning when current architecture evolves.
Later allocation or technology replacement does not rewrite responsibility or realization choices in an earlier Baseline.
