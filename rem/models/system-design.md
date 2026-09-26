# System Design model

System Design describes what stakeholder-visible capabilities exist and what logical behavior realizes them.
The [concept definitions](../concepts/README.md#system-and-architecture-assets) distinguish Features and Functions from Requirements. [Scenario](../concepts/README.md#requirement-analysis-entities) is a first-class governed Requirement Analysis entity whose identity, lifecycle, and relationships are owned by the [Scenario model](scenarios.md).

```text
IR ── confirms ──────> Feature
Scenario ─exercises──> Feature
SR ── confirms ──────> Function
Feature ─realizedBy──> Function
```

A Feature is durable and may be exercised by many governed Scenarios and evolve under many Requirements and Changes.
An IR confirms the stakeholder-visible Feature established through requirement and scenario analysis.
A Function is durable logical behavior; SR analysis confirms the Functions required by the system obligations.
A Function may realize several Features and is not contained exclusively by one Feature.
Requirements shape these assets through explicit relationships rather than becoming their parents.

## Clear names and boundaries

[Principle 16](../principles/README.md) requires understandable, distinguishable engineering definitions.
A Feature or Function name identifies its engineering purpose and subject, distinguishes neighboring assets, and agrees with its description and scope.
Prefer an action and subject, adding a condition when it carries a meaningful distinction; an equally clear noun phrase is acceptable.
Do not depend on a broad label such as "management" or "processing" to explain the asset's responsibility.

For example, "Inspect engineering definitions and their rationale" identifies a stakeholder capability, while "Resolve engineering entity by stable ID" identifies a logical behavior.
"Check entity identity presence and uniqueness" makes the check's scope explicit, and "Retrieve engineering definition from selected model state" distinguishes retrieval from identity resolution.
These are naming examples, not prescribed assets or implementation choices.

Define "current" relative to the selected engineering model state, with that state identifiable to readers.
When using "supported," identify the applicable profile or declared conditions rather than hiding an undefined behavior boundary behind the word.
Review related definitions together so the handoff between their responsibilities is understandable from current authoritative information.

## Feature definition

A Feature definition should explain:

- who uses or benefits from the capability;
- what that participant can do or understand;
- why the capability is valuable;
- the capability's included scope and its boundary with neighboring Features.

The description should explain the durable capability across its Scenarios, not merely list Functions or repeat one scenario's flow.
For example, "Author and revise engineering definitions" can distinguish a capability for changing definitions from a capability for inspecting them.
State the actual supported scope so the name does not imply that all related authoring activities are already provided.

## Function definition

A Function SHOULD have clear inputs, outputs, and behavior.
Explain the input subjects and state, applicable preconditions, the logical behavior performed, the resulting outputs, and meaningful failure or incomplete outcomes.
Make its responsibility distinguishable from neighboring Functions: checking identity presence and uniqueness, resolving one entity, retrieving its definition, and presenting its meaning are different behaviors.
State where this Function's responsibility ends and what information it supplies for subsequent behavior; reuse authoritative definitions rather than copying their contracts.
Keep the logical behavior independent of physical software structure wherever practical.

A Function SHOULD have an accountable architectural responsibility unless the architecture deliberately leaves it unallocated.
Allocation is owned by the [Architecture Design model](architecture-design.md).
Implementation references identify realization without replacing the logical definition.

These definition criteria do not require Features or Functions to use the requirement 5W2H template or extend the IR/SR/Scenario open-question policy to System Design assets.
The project representation selects fields and storage conventions through [Operational Support](operational-support.md).

## Evolution

New requirements may add Functions or change existing behavior while preserving the Feature's identity.
Current assets describe the resulting current system directly.
Changes explain the transitions, and historical states retain their own meanings.

A Feature-to-Function relationship is authored once; the opposite navigation view is derived.
The project representation chooses its storage direction without creating two independently maintained facts.
