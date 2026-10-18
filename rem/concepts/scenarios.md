# Requirement analysis entities

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
