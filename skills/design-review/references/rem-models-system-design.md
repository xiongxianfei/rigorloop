<!-- Generated from rem/models/system-design.md; source SHA-256 be895c42416ea9d7eccda0a56671e7f8ba329c1b131ac6d60462774c1ced88dc. Edit the owning REM source. -->

# System Design model

System Design describes durable stakeholder-visible capabilities and the durable logical behavior that realizes them.
The [concept definitions](https://github.com/xiongxianfei/rigorloop/blob/main/rem/concepts/README.md#system-and-architecture-assets) distinguish Features and Functions from Requirements.
The [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md) defines the governed stakeholder situations that exercise Features.

```text
IR ── confirms ──────> Feature
Scenario ─exercises──> Feature
SR ── confirms ──────> Function
Feature ─realizedBy──> Function
```

Requirements shape durable system assets without becoming their containment hierarchy.

## Feature relationships

A Feature is a durable stakeholder-visible capability.
Before Initial Requirement analysis is considered complete, each Feature confirmed by that IR MUST be exercised by at least one confirmed Scenario owned by the same IR.
A Feature may be confirmed or affected by several IRs over time, each contributing its own analysis context and Scenarios.

One Feature may be exercised by many Scenarios.
Each confirmed Scenario has exactly one primary Feature, as defined by the [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md).

A Feature may exist before all of its Functions are known.
Once System Design for the Feature is considered complete, it MUST be realized by at least one confirmed Function.

## Function relationships

A Function is durable logical behavior.
Before System Design for an approved SR is considered complete, that SR MUST confirm at least one Function that carries the behavior required by the obligation.
Requirement approval may precede that design; missing Function coverage remains an explicit design obligation, not a prerequisite for accepting the requirement basis.
A Function may be confirmed by several SRs and may realize several Features.
Do not create one Function per SR merely to preserve symmetry.

```text
SR 1 ─┐
SR 2 ─┼── confirms ──> Function A
SR 3 ─┘

Feature X ─┐
Feature Y ─┼── realizedBy ──> Function A
```

When an SR is primarily a quality or constraint obligation, confirm the Function or Functions whose behavior is governed by that requirement rather than inventing a synthetic quality Function.

## Clear names and boundaries

[Principle 16](https://github.com/xiongxianfei/rigorloop/blob/main/rem/principles/README.md) requires understandable, distinguishable engineering definitions.
A Feature or Function name identifies its engineering purpose and subject, distinguishes neighboring assets, and agrees with its description and scope.
Prefer an action and subject, adding a condition when it carries a meaningful distinction; an equally clear noun phrase is acceptable.

For example, "Inspect engineering definitions and their rationale" identifies a stakeholder capability, while "Resolve engineering entity by stable ID" identifies a logical behavior.
Do not depend on broad labels such as "management" or "processing" to explain responsibility.

## Feature definition

A Feature definition SHOULD explain:

- who uses or benefits from the capability;
- what that participant can do or understand;
- why the capability is valuable;
- the capability's included scope and boundary with neighboring Features.

The description explains the durable capability across its Scenarios, not merely one Scenario flow or a list of Functions.
A Feature remains meaningful even if internal architecture is replaced.

## Function definition

A Function MUST have a responsibility boundary clear enough for architectural allocation.
Its definition SHOULD state:

- logical behavior and subject;
- inputs and relevant state;
- applicable conditions or preconditions;
- outputs;
- material failure or incomplete outcomes;
- where responsibility ends and another Function begins.

Keep Function semantics independent of Module, process, package, service, transport, persistence technology, or deployment structure wherever practical.

Every active Function MUST have exactly one accountable primary Module before architecture allocation is considered complete.
A Function MAY use supporting Modules.
The [Architecture Design model](rem-models-architecture-design.md) owns those allocation rules.

## Development method

Use [Scenario Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/scenario-analysis.md) to confirm Features and discover candidate behavior.
Use [Functional Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/functional-analysis.md) to confirm Functions from SR obligations and reconcile Feature-to-Function relationships.

Scenario Analysis does not make candidate behavior authoritative.
Functional Analysis does not allocate Modules.

## Evolution

New requirements may add Functions or change existing behavior while preserving Feature identity.
Current assets describe the resulting current system directly.
Changes explain transitions, and historical states retain their original meanings.

Feature-to-Function and SR-to-Function relationships are each authored once; inverse navigation views are derived.
