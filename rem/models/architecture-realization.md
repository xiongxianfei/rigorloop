# Technical model

## Technical model

A technical model describes the intended architectural implementation through components, their responsibilities, contracts, relationships, data authority and material technology choices. It makes the responsibility architecture implementable while retaining the accountable Modules, Interfaces and Function/AR allocations. It can be authored before code exists; implementation observations retain their separate qualification.

| Element | Required meaning when material |
| --- | --- |
| Component | A coherent technical responsibility, its scope and exclusions, and its mapping to the Modules/Functions it realizes |
| Contract | The interaction's participants, inputs/outputs or representation, guarantees, failures and compatibility; reference an existing Interface or detailed owner where applicable |
| Relationship | An explicit meaning such as uses, realizes, produces, consumes or embeds; containment means technical composition, not automatically Module containment or process membership |
| Data and artifact authority | Who interprets, produces, mutates or only reads each significant input, state or output |
| Technology decision | The selected technology, governing need, alternatives, consequences and revisit conditions |
| Qualification and limits | Intended design versus observed implementation, unresolved mappings and the constraints needed to assess the composition |

One component may realize contributions from several Modules, and one Module may be realized by several components. Preserve those mappings explicitly; co-location does not transfer Function or AR accountability. A component, library or technology label does not acquire first-class REM identity merely by appearing in the technical model. Local names suffice unless a project has a justified identity contract.

The Technical structure perspective of the Logical View presents components and their contracts with relevant technology annotations. Development presents their organization into source units, packages, build resources and tests. Process presents independently executing participants and their interactions; Physical presents artifact placement and deployment constraints. Reuse the same authoritative relationships and distinguish each diagram's edge meanings. A technology list alone does not establish a technical model, and a structural dependency does not establish execution order.

Author the model with proportionate prose, component/contract tables and diagrams at the existing Module or Interface owner. Cross-owner composition references the participating owners rather than moving their authority into a convenient executable or document. Structured realization fields may be added when their semantics and tooling need are settled; no new entity class, universal schema, standalone document or sixth view is required.

## Architecture realization views

Each in-scope Module and Interface MAY carry an architecture realization view.
Here, the retained term “realization view” denotes owner-held architecture information, including the technical model. It is not a separately authoritative generated 4+1 presentation.
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
- authoritative runtime communication, synchronization, ordering, lifecycle, retry, transaction, failure, or recovery semantics when architecturally material;
- persistence mechanisms or datastores used to realize state owned or used by the Module;
- packaging or deployment units and significant deployment targets;
- implementation paths or artifact mappings;
- test groups assessing the responsibility, their observation boundaries, fixtures and execution dependencies;
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

Test organization is supporting realization information: the containing Module identifies the responsibility assessed by its test groups. It does not acquire ownership of shared execution tooling, and test code does not become an implementation of the behavior it assesses. Reference the actual coverage and execution owners, preserve material gaps, and keep test definitions separate from observed Verification Evidence. See the [Development View's test architecture](../methods/views/development.md#test-architecture).

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

## Realization and history

Modules and Functions MAY have `realizedBy` references to Implementation.
Module and Interface realization views may additionally record the physical/software mappings needed for architecture understanding.
Architecture boundaries need not map one-to-one to source directories, packages, services, processes, datastores, or deployment units.
Such mappings are subordinate realization decisions and MUST NOT redefine logical architecture implicitly.

A material realization change is an architecture change when it alters a durable Module responsibility, Interface contract, runtime/deployment constraint, state ownership, or another architecture-significant decision.
A purely internal implementation refactor that preserves those meanings need not change the architecture model.

Preserve historical allocations and realization meaning when current architecture evolves.
Later allocation or technology replacement does not rewrite responsibility or realization choices in an earlier Baseline.
