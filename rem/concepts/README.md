# REM concepts

These definitions belong to the proposed [RigorLoop Engineering Method](../README.md).
[Models](../models/README.md) define the relationships and constraints between concepts; [methods](../methods/README.md) explain how to apply them.

## Requirements

Requirements describe what must become or remain true.
They are durable obligations or needs, separate from the Changes that introduce or modify them.

| Concept | Meaning |
| --- | --- |
| Initial Requirement (IR) | Initial durable expression of a stakeholder, business, product, regulatory, operational, or engineering need; explains why the system needs to provide or change something. |
| System Requirement (SR) | Durable obligation imposed on the system as a whole and derived from an IR; must be verifiable before approval and avoid prescribing implementation unless that implementation is required. |
| Allocated Requirement (AR) | Durable lower-level requirement derived from an SR and allocated to exactly one accountable Module; remains normative, verifiable, and traceable to its SR. |

An AR expresses what an architectural element must satisfy.
It is not merely a record that an allocation occurred.
Requirement containment is the IR → SR → AR tree defined in the models.

## Requirement analysis entities

| Concept | Meaning |
| --- | --- |
| Scenario | First-class governed Requirement Analysis entity representing one concrete stakeholder-observable situation in which a durable Feature is exercised; has stable identity, lifecycle, one owning IR, and one primary Feature. |

A Scenario is durable analysis knowledge, but it is not a durable system capability.
Its identity allows stakeholder situations and their downstream requirement impact to be traced over time.
A confirmed Scenario belongs to exactly one IR and exercises exactly one primary Feature.
Several Scenarios may exercise the same Feature, and a Feature may remain active when a Scenario becomes obsolete.
Scenario Analysis can reveal candidate system behavior, but a Function becomes part of authoritative System Design only when confirmed through System Requirement analysis.
The [Scenario model](../models/scenarios.md) owns lifecycle, cardinality, and black-box invariants.

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
| Architecture realization view | Subordinate architecture information, owned by a Module or Interface, describing material physical/software realization without creating another first-class REM asset. |
| Software realization | Subordinate view of the software units or implementation structures that realize a Module responsibility. |
| Runtime realization | Subordinate view of material execution, process, lifecycle, scaling, isolation, concurrency, or resource boundaries. |
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
REM uses the classic 4+1 names—Logical, Process, Development, Physical, and Scenario—for standard architecture projections.
The Scenario View is generated from a governed black-box Scenario and relevant downstream architecture; it does not add internal architecture steps to the Scenario entity itself.
A 4+1 Architecture View Graph may normalize the authoritative architecture for graph traversal and projection, but every generated fact must remain attributable to its authoritative source and the graph must remain fully replaceable by regeneration.

## Engineering model and its support

| Concept | Meaning |
| --- | --- |
| Engineering model | The requirements, system assets, architecture, and their relationships that describe the product at an identifiable engineering state. |
| Metamodel | Definitions and rules establishing valid engineering entity types, fields, relationships, identities, cardinalities, and constraints. |
| Operational Support | Design domain governing how the engineering model is represented, interpreted, validated, authored, maintained, and evolved. |

An engineering model defines a particular Function; its metamodel defines what a valid Function is.
Operational Support primarily concerns operation of the engineering design system, rather than production operation of the application.
Its scope includes lifecycle, retirement, migration, baseline, and change rules.

## Evolution and history

| Concept | Meaning |
| --- | --- |
| Change | Controlled evolution from one engineering baseline to another; can create, modify, or retire requirements, assets, realizations, or verification material. |
| Baseline | Identifiable, coherent engineering state that can include requirements, system design, architecture, implementation, verification, and Operational Support or metamodel state. |
| Configuration management | Management of identifiable baselines, controlled changes, comparisons, provenance, preservation, and recovery of historical engineering states. |
| Provenance | Attributable origin and derivation of engineering information, including the source and engineering context needed to understand its meaning. |

Current definitions explain what is true at the current state.
Change history explains how and why that state evolved; configuration history preserves what was true before.
A Change is neither a Requirement nor a design asset.

## Assurance and traceability

| Concept | Meaning |
| --- | --- |
| Verification | Defined means of determining whether a Requirement is satisfied, using techniques such as test, analysis, inspection, demonstration, review, or measurement. |
| Evidence | Actual observed information supporting an engineering conclusion, interpreted in its applicable assessed context. |
| Judgment | Engineering conclusion about what the applicable evidence supports. |
| Traceability | Explicit relationships allowing engineering information to be connected across needs, obligations, assets, realization, verification, evidence, and evolution. |

A verification technique describes how to assess; Evidence records what was observed; Judgment states what those observations support.
The existence of a test file alone does not establish that a Requirement has been satisfied.
Traceability is a typed graph across domains, while requirement parentage remains a tree.
