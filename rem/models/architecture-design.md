# Architecture Design model

Architecture Design assigns accountable responsibility to Modules, defines architecturally significant interactions through Interfaces, and records the material physical/software realization needed to make that logical architecture implementable.
The [concept definitions](../concepts/README.md#system-and-architecture-assets) explain these architectural assets and the subordinate architecture realization view.

REM keeps two coupled views:

```text
Logical architecture
  Function / AR → Module
  Module ── contains ──> Module
  Module ↔ Interface
  parent boundary ── exposes descendant Interface when required

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

Allocate the Function to the lowest Module in the containment hierarchy that can coherently own the complete behavior. Parent Modules receive derived roll-up visibility over descendant allocations but do not become additional owners merely because they contain the accountable Module. A Function MAY be allocated directly to a parent when the behavior genuinely belongs to that broader responsibility boundary.

If no single Module can own the Function coherently, reconsider the Function boundary or Module boundaries rather than leaving responsibility ambiguous.

## AR allocation cardinality

Every active AR MUST be allocated to exactly one Module.

If an allocated obligation genuinely belongs to several Modules, decompose it into separate ARs under the same parent SR so each lower-level obligation has one accountable Module.
Do not assign one AR to several Modules to avoid deciding responsibility.

This convergence does not require every AR to pair one-to-one with a Function.
An AR may govern state, quality, policy, data, or another architectural responsibility.

Allocate the AR to the lowest Module in the containment hierarchy that can coherently own the complete obligation. Parent Modules receive derived roll-up visibility over descendant ARs but are not additional allocated owners. An AR MAY be allocated directly to a parent when the obligation applies to the broader parent boundary itself.

## Module hierarchy and encapsulation

A Module MAY contain zero or more child Modules. A Module MAY have at most one parent Module. Containment MUST be acyclic, so each connected containment structure forms a tree and the complete architecture forms a forest of Module trees.

A parent Module is a first-class architectural responsibility with its own purpose, scope, lifecycle, state/data authority, allocations, Interfaces, and realization where applicable. It MUST NOT exist merely as a navigation folder or visual grouping. Each child Module refines part of the parent's broader responsibility while retaining independent stable identity. Moving a Module to a different parent changes current architecture containment but does not by itself change the Module's identity.

REM does not prescribe a universal maximum Module-containment depth. Architecture SHOULD remain shallow enough that each level expresses a meaningful responsibility decomposition rather than implementation structure. A project implementation MAY impose a stricter supported depth as an Operational Support or representation rule, provided that restriction is not presented as universal REM semantics.

A parent Module is an encapsulation boundary. An Interface provided by a descendant is internal to the nearest containing parent boundary unless the Interface is explicitly exposed through that boundary. If the same child-provided contract must be visible beyond additional ancestors, exposure MUST continue through the intervening parent boundaries without skipping them. Exposure preserves the descendant provider and the Interface identity; it does not create a wrapper Interface automatically.

If the broader parent responsibility genuinely owns the external contract, the parent SHOULD provide an Interface in its own right rather than presenting a child-owned contract as parent-owned.

## Modules

A Module is a meaningful architectural responsibility boundary and may own:

- Functions;
- state or data;
- policies and constraints;
- provided and consumed Interfaces;
- dependencies;
- realization scope.

Module boundaries SHOULD be justified by responsibility and evolution rather than copied mechanically from current source directories, packages, processes, or deployment units. Parent-child decomposition SHOULD likewise reflect responsibility refinement and encapsulation rather than organization charts or filesystem convenience.

## Interfaces

A Module may `provide` and `consume` Interfaces.
The canonical relationship labels are `provides` and `consumes`.

Each Interface MUST have exactly one provider Module.
An Interface MAY have zero or more consumer Modules.
An Interface may describe operations, messages, data structures, inputs, outputs, protocols, failure semantics, and compatibility constraints.
Architecturally significant cross-Module interactions SHOULD be explicit Interfaces.

An Interface covers a cohesive interaction needed by its consumers. A Module MAY provide several Interfaces, and one Interface MAY contain several related operations. Its scope need not cover the provider's entire responsibility or correspond one-to-one with a child Module. Separate contracts when their purpose, authority, failure guarantees, or independent evolution differ materially; explain their cooperation where needed.

The provider is the Module accountable for the contract: its promised outcomes, failures, consistency, and compatibility. Provider ownership is distinct from the behavior or implementation that realizes the contract. A parent MAY provide an Interface whose behavior is realized through child responsibilities. Those children retain their Function/AR allocations and state authority without becoming additional providers. A child's implementation contribution alone does not create a `consumes` relationship either.

Choose the provider from the scope of contract accountability. Do not infer it from source-code location, directory containment, or the Module that executes an operation. Explain how the accountable boundary is realized through its contributing responsibilities and material realization information. Containment alone does not establish that every descendant implements every parent Interface; a tool needs explicit supporting facts before projecting that relationship.

An Interface can describe an internal interaction and need not be a network API.

When its provider is a contained Module, an Interface is internal to that containment boundary by default. A consumer outside the provider's containing parent may use the Interface only when the contract is explicitly exposed through that parent boundary. If the consumer lies beyond additional ancestors, every intervening provider-side parent boundary MUST expose the same Interface. Exposure does not alter provider/consumer identity, imply runtime call direction, or create a second contract.

Architecture review SHOULD distinguish Interfaces owned directly by a parent Module from descendant Interfaces merely exposed through that parent boundary.

A parent-provided Interface needs no exposure through its own provider. If that provider is itself contained and the contract crosses higher boundaries, the normal ancestor-exposure rules still apply. Moving contract accountability is a controlled model change: preserve identity when the same contract continues, reconcile provider participation and exposure, and retain the earlier state's meaning.

## Architecture semantic outputs

Architecture Design produces semantic outputs rather than prescribing a document, directory, serialization format, or diagram.
For the declared architecture scope, the authoritative information is organized around the following concerns.

| Semantic output | Purpose | Primary owner | Expected when |
| --- | --- | --- | --- |
| Module definition | Defines accountable responsibility, purpose, owned state/data, policies, exclusions, and dependencies | Module | For every in-scope Module |
| Module containment | Defines parent-child responsibility refinement and encapsulation boundaries | Module hierarchy relationship | When a Module is decomposed into child Modules |
| Function allocation | Identifies the one accountable primary Module and any supporting Modules for logical behavior | Function relationship | For every active in-scope Function |
| AR allocation | Identifies the one Module accountable for a lower-level allocated obligation | AR relationship | For every active in-scope AR |
| Interface definition and exposure | Defines a significant logical interaction contract, provider/consumers, and any parent boundaries through which a descendant-provided contract is intentionally exposed | Interface | When cross-Module interaction is architecturally significant |
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

## Public-entry discoverability

An architecturally relevant public entry identifies how a participant accesses a capability: for example, a command, endpoint, or published procedure. Record its readable name, purpose, authoritative contract, and relevant source realization under the responsible Module or Interface. Such entries are subordinate realization information, not new first-class entities merely because they are named or grouped for navigation.

Separate observed existence and published meaning from analyzed correspondence to the engineering model. A source artifact or supported command name does not establish that an installed product works, that a proposed Function is completely realized, or that every specialist obligation has been translated. Preserve the source's applicability, the mapping rationale, and any unmapped scope.

A public entry may guide a participant in performing a Function, invoke behavior, or contribute to realizing behavior. State the particular contribution and its basis. One entry may relate to several Functions across Modules; several entries may contribute to the same Function. These references do not replace Function allocation or establish execution order. A shared invocation Module may catalog procedures whose specialist behavior remains accountable elsewhere.

Derive Feature context from existing Feature-to-Function relationships and architectural responsibility from existing Function allocation, retaining an explicit unallocated disposition. Author only the additional public-entry correspondence. Exact syntax, protocol, procedural detail, and failure guarantees retain their owning contract rather than becoming a second catalog specification.

The Logical view may expose these mappings as expandable navigation beneath the responsible boundary. Navigation groups are presentation aids; they do not create Module containment, Interface ownership, or permission to execute. Other inventories of the same entries should derive from, or link to, this authoritative mapping.

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

- its parent and child Modules, if any, and whether the decomposition refines responsibility coherently;
- Functions for which it is primary;
- Functions it supports;
- ARs allocated to it;
- state and data it owns;
- policies it must enforce;
- Interfaces it provides or consumes;
- descendant Interfaces it exposes through its boundary.

An unexplained missing responsibility, conflicting owner, encapsulation bypass, skipped exposure boundary, or incompatible Interface is a design issue even when a diagram can be rendered.

Use [Architecture Allocation](../methods/architecture-allocation.md) to assign and reconcile these responsibilities.

## Generated 4+1 architecture views

REM standardizes five architecture-view kinds using the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.
These are generated projections of the authoritative semantic architecture, not independent models or authored sources of truth.
Use the [4+1 Architecture View method](../methods/architecture-views.md) to construct them.

| View | Primary concern | Typical authoritative inputs |
| --- | --- | --- |
| Logical | Hierarchical responsibilities, behavior, obligations, logical collaboration, encapsulation, and state/data authority | Module containment, exposed/internal Interfaces, Feature/Function context, Function/AR allocation, Module definitions, state/data ownership |
| Process | Runtime behavior, execution boundaries, concurrency, lifecycle, communication, isolation, and failure boundaries | Module runtime realization and runtime-significant Interface realization |
| Development | Static software organization used for development/build/maintenance | Module software realization, implementation/source/package mappings, material software dependencies |
| Physical | Deployment, placement, connectivity, persistence placement, and infrastructure topology | Module deployment/persistence realization, external runtime dependencies, concrete connectivity |
| Scenario | End-to-end architecture participation for one governed stakeholder Scenario | Scenario → SR/Function/AR → Module/Interface plus relevant realization |

A view MAY simplify presentation, for example by collapsing an Interface into a labeled Module-to-Module edge, provided the underlying Interface and authoritative relationship remain discoverable.
A view MUST NOT invent or independently maintain architecture facts.

The Scenario View is the `+1` cross-view validation slice.
The canonical Scenario remains black-box and stakeholder-observable; the generated view derives internal architecture participation without adding those internal steps to the Scenario definition.
Important Scenarios SHOULD be used to test whether the other four views form a coherent end-to-end explanation of the architecture.

A generated **4+1 Architecture View Graph** MAY normalize authoritative REM entities, Module containment, Interface exposure, allocation relationships, and subordinate realization information for projection. It is a derived, non-authoritative architecture read model, not a general replacement for the REM engineering model.
Generated realization nodes may use local handles for deterministic traversal, but such handles do not create new first-class REM entities.
Generated nodes and edges SHOULD retain provenance to the authoritative REM owner from which they were derived. Logical projections SHOULD begin at the highest useful in-scope Module level and reveal contained Modules, internal Interfaces, Functions, ARs, and state/data authority progressively.

## Realization and history

Modules and Functions MAY have `realizedBy` references to Implementation.
Module and Interface realization views may additionally record the physical/software mappings needed for architecture understanding.
Architecture boundaries need not map one-to-one to source directories, packages, services, processes, datastores, or deployment units.
Such mappings are subordinate realization decisions and MUST NOT redefine logical architecture implicitly.

A material realization change is an architecture change when it alters a durable Module responsibility, Interface contract, runtime/deployment constraint, state ownership, or another architecture-significant decision.
A purely internal implementation refactor that preserves those meanings need not change the architecture model.

Preserve historical allocations and realization meaning when current architecture evolves.
Later allocation or technology replacement does not rewrite responsibility or realization choices in an earlier Baseline.
