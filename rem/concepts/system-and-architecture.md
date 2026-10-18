# System and architecture assets

## System and architecture assets

These assets describe the system's capabilities, behavior, and architectural responsibilities.
Requirements shape their evolution across Changes and Baselines without becoming their asset hierarchy.

| Concept | Meaning |
| --- | --- |
| Feature | Durable product-visible or stakeholder-visible capability confirmed from Initial Requirement and Scenario Analysis; describes what valuable capability exists across multiple Scenarios and Changes. |
| Function | Durable logical system behavior confirmed through System Requirement analysis; describes what the system does, independently from physical software structure wherever practical. |
| Module | Durable architectural unit of responsibility, potentially owning behavior, data or state, interfaces, dependencies, technical policies, and implementation scope; a Module may contain child Modules that refine part of its broader responsibility. |
| Module containment | Tree relationship in which a parent Module owns a broader architectural responsibility and contained child Modules refine portions of that responsibility while remaining first-class Modules. |
| Interface | Explicit interaction contract between architectural elements, potentially defining operations, messages, data structures, protocols, failures, and compatibility. |
| Interface exposure | Explicit declaration that an Interface provided by a contained Module may cross one or more parent Module encapsulation boundaries; exposure preserves the Interface and provider identities rather than creating a wrapper contract automatically. |
| Realization | Code, configuration, or another implementation artifact that realizes the design; distinct from the design asset it implements. |
| Technical model | Owned architecture design of the intended implementation: components, responsibilities, contracts, relationships, data authority and material technology choices. Its structural projection is a Logical reading perspective; components retain explicit mappings to accountable Modules and Interfaces. |
| Architecture realization view | Subordinate architecture information, owned by a Module or Interface, describing material physical/software realization without creating another first-class REM asset. |
| Software realization | Subordinate view of the software units or implementation structures that realize a Module responsibility. |
| Runtime realization | Subordinate view of material execution, process, lifecycle, scaling, isolation, concurrency, synchronization, communication, resource, failure, ordering, retry, or recovery semantics where architecturally significant. |
| Persistence realization | Subordinate view of how architecturally significant state or data is retained, including authority, derivation, consistency, recovery, or lifecycle implications. |
| Deployment realization | Subordinate view of material packaging, placement, isolation, target, or external runtime dependencies. |
| Technology rationale | Attributable reasoning for a technology choice whose consequences are architecturally material, including driver, consequences, significant alternatives, and revisit conditions. |
| Architecture view | Derived presentation of authoritative architecture information for a particular concern. REM standardizes the classic 4+1 view kinds: Logical, Process, Development, Physical, and Scenario. |
| 4+1 Architecture View Graph | Generated, non-authoritative typed architecture graph/read model derived from authoritative REM entities, relationships, hierarchy, exposure, and subordinate realization information for 4+1 traversal, query, and view generation. |

A Feature is not a Requirement, and a Module is not a requirement category or merely a grouping label.
Functional responsibility and allocated requirement responsibility meet at architecture.

A parent Module is itself a first-class architectural responsibility and encapsulation boundary, not a visual folder. A child Module refines part of that broader responsibility while retaining its own stable identity, lifecycle, allocations, state authority, and Interfaces. Module containment is true containment: each Module has at most one parent, containment is acyclic, and the overall hierarchy is a forest of Module trees. REM does not prescribe a universal maximum hierarchy depth; projects and implementations may impose a shallower operational limit without changing the REM meaning of Module containment.

An Interface provided by a contained Module is internal to its containing boundary unless it is explicitly exposed through that boundary. Exposure may continue through additional ancestors when the contract must be visible farther outward. Exposure does not change the Interface provider, duplicate the Interface, or imply that the parent provides the contract. If the parent genuinely owns the external contract, the parent should provide that Interface directly.

Modules and Interfaces are the first-class governed Architecture Design assets in the REM core.
A Module may own software, runtime, persistence, deployment, and technology realization information; an Interface may own interaction, representation, and technology realization information.
Those realization facets are semantic outputs of Architecture Design, not universal entity classes.
Services, libraries, processes, datastores, deployment units, deployment targets, protocols, and technology choices do not acquire independent REM identity merely because they appear in those views.
A project may structure or locally identify subordinate realization information for tooling, but storage structure does not change its REM meaning or promote it to a first-class entity.
Architecture views are derived presentations and do not own facts that belong to Module, Interface, Requirement, Function, Scenario, or realization information.
The [technical model](../models/architecture-realization.md#technical-model) is subordinate architecture knowledge. Its Logical technical-structure presentation and its Development, Process and Physical projections select different concerns without creating additional engineering entities or duplicated authority.
REM uses the classic 4+1 names—Logical, Process, Development, Physical, and Scenario—for standard architecture projections.
The Scenario View is generated from a governed black-box Scenario and relevant downstream architecture; it does not add internal architecture steps to the Scenario entity itself.
A 4+1 Architecture View Graph may normalize the authoritative architecture for graph traversal and projection, but every generated fact must remain attributable to its authoritative source and the graph must remain fully replaceable by regeneration.
