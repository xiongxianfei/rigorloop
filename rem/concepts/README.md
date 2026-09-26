# REM concepts

These definitions belong to the proposed [RigorLoop Engineering Method](../README.md).
[Models](../models/README.md) define the relationships and constraints between concepts; [methods](../methods/README.md) explain how to apply them.

## Requirements

Requirements describe what must become or remain true.
They are durable obligations or needs, separate from the Changes that introduce or modify them.

| Concept | Meaning |
| --- | --- |
| Initial Requirement (IR) | Initial durable expression of a stakeholder, business, product, regulatory, operational, or engineering need; explains why the system needs to provide or change something. |
| System Requirement (SR) | Durable obligation imposed on the system as a whole and derived from an IR; should be verifiable and avoid prescribing implementation unless that implementation is required. |
| Allocated Requirement (AR) | Durable lower-level requirement derived from an SR and allocated to an architectural element; remains normative, verifiable, and traceable to its SR. |

An AR expresses what an architectural element must satisfy.
It is not merely a record that an allocation occurred.
Requirement containment is the IR → SR → AR tree defined in the models.

## Requirement analysis entities

| Concept | Meaning |
| --- | --- |
| Scenario | First-class governed requirement-analysis entity describing one concrete, stakeholder-observable situation in which a Feature is exercised. A Scenario has stable identity and lifecycle, belongs to one IR, and records actor, context, goal, trigger, preconditions, black-box interaction, and expected, alternative, or failure outcomes. |

A Scenario is neither a Requirement nor a durable system capability.
It is governed engineering information that preserves stakeholder-visible usage context across Baselines.
An IR can confirm multiple Scenarios, and multiple Scenarios can exercise the same durable Feature over that Feature's lifetime.
Scenario Analysis can reveal candidate system behavior, but a Function becomes part of authoritative System Design only when confirmed through System Requirement analysis.

A Scenario MUST remain black-box: it describes stakeholder-observable interaction and outcomes without prescribing Modules, Interfaces, APIs, internal call sequences, algorithms, source layout, or implementation technology.

## System and architecture assets

These assets describe the system's capabilities, behavior, and architectural responsibilities.
Requirements shape their evolution across Changes and Baselines without becoming their asset hierarchy.

| Concept | Meaning |
| --- | --- |
| Feature | Durable product-visible or stakeholder-visible capability confirmed from Initial Requirement and Scenario Analysis; describes what valuable capability exists across multiple Scenarios and Changes. |
| Function | Durable logical system behavior confirmed through System Requirement analysis; describes what the system does, independently from physical software structure wherever practical. |
| Module | Durable architectural unit of responsibility, potentially owning behavior, data or state, interfaces, dependencies, technical policies, and implementation scope. |
| Interface | Explicit interaction contract between architectural elements, potentially defining operations, messages, data structures, protocols, failures, and compatibility. |
| Realization | Code, configuration, or another implementation artifact that realizes the design; distinct from the design asset it implements. |

A Feature is not a Requirement, and a Module is not a requirement category or merely a grouping label.
Functional responsibility and allocated requirement responsibility meet at architecture.

## Engineering model and its support

| Concept | Meaning |
| --- | --- |
| Engineering model | The requirements, governed analysis entities such as Scenarios, system assets, architecture, and their relationships that describe the product at an identifiable engineering state. |
| Metamodel | Definitions and rules establishing valid engineering entity types, fields, relationships, identities, cardinalities, and constraints. |
| Operational Support | Design domain governing how the engineering model is represented, interpreted, validated, authored, maintained, and evolved. |

An engineering model defines a particular Function; its metamodel defines what a valid Function is.
Operational Support primarily concerns operation of the engineering design system, rather than production operation of the application.
Its scope includes lifecycle, retirement, migration, baseline, and change rules.

## Evolution and history

| Concept | Meaning |
| --- | --- |
| Change | Controlled evolution from one engineering baseline to another; can create, modify, or retire requirements, governed analysis entities, assets, realizations, or verification material. |
| Baseline | Identifiable, coherent engineering state that can include requirements, Scenarios and other governed analysis state, system design, architecture, implementation, verification, and Operational Support or metamodel state. |
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
