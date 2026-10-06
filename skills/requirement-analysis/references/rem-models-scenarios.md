<!-- Generated from rem/models/scenarios.md; source SHA-256 a1fe76783ad57048938d690c7d1d3ca9df692d7aa7276f1d77c182a65b98511c. Edit the owning REM source. -->

# Scenario model

Scenarios are first-class governed REM entities used during Initial Requirement analysis.
They describe stakeholder-observable situations in which a durable Feature is exercised.
The [Scenario concept](https://github.com/xiongxianfei/rigorloop/blob/main/rem/concepts/scenarios.md#requirement-analysis-entities) defines their meaning; [Scenario Analysis](rem-methods-scenario-analysis.md) defines how to develop and maintain them.

## Identity and ownership

Every Scenario has a stable identity independent of its title, wording, or physical location.
A Scenario has exactly one owning IR.
The owning IR establishes the requirement-analysis context in which the Scenario was confirmed.

A confirmed Scenario exercises exactly one primary Feature.
That primary Feature MUST be one of the Features confirmed by the Scenario's owning IR.
Several Scenarios may exercise the same Feature, and a Feature may remain active after one or more Scenarios become obsolete.

```text
IR ── confirms ──> Scenario ── exercises ──> Feature
```

If one stakeholder journey appears to require several primary Features, split it into focused Scenarios unless the method later defines a separate Journey concept.
Do not weaken Scenario identity by turning it into an unbounded container for several unrelated capabilities.

## Black-box boundary

A Scenario describes the system from the stakeholder boundary.
It MAY define:

- actor;
- goal;
- context;
- trigger;
- preconditions;
- stakeholder/system interaction;
- expected outcome;
- alternative outcomes;
- failure outcomes;
- recovery outcome where stakeholder-visible recovery matters.

A Scenario MUST NOT define internal architecture or realization, including:

- Module allocation;
- Interface or API design;
- internal Function call sequences;
- persistence schemas;
- implementation classes, packages, crates, or services;
- algorithms, threads, queues, or deployment topology;
- specific implementation technology unless that technology is itself an explicit stakeholder-facing requirement.

A useful quality check is:

> Would this Scenario remain meaningful if the internal implementation were completely replaced?

If not, the Scenario contains design detail that belongs later.

## Relationship to System Requirements

Scenario Analysis uses stakeholder situations to expose system obligations.
A Scenario may inform zero or more SRs while analysis is still incomplete.
Before an IR's Scenario Analysis is considered complete, every confirmed Scenario MUST either:

1. inform at least one SR; or
2. have an explicit analysis conclusion explaining why it introduces no additional system obligation.

```text
Scenario ── informs ──> SR
```

One Scenario may inform several SRs.
One SR may be informed by several Scenarios.
These are traceability relationships, not containment.

A Scenario does not own a Function.
Scenario Analysis may identify candidate behavior, but the [Requirement model](rem-models-requirements.md) records `SR confirms Function` as the authoritative confirmation of logical behavior.

## Lifecycle

The universal Scenario lifecycle is:

```text
draft → confirmed → obsolete
```

- **draft** — analysis is incomplete or unsettled; relationships may still change.
- **confirmed** — the Scenario has a clear black-box stakeholder meaning, one owning IR, one primary Feature, and sufficient downstream obligation analysis.
- **obsolete** — the Scenario no longer represents a supported stakeholder situation, while its historical meaning remains recoverable through configuration history.

Obsolete does not mean that the Feature is obsolete.
Retiring or replacing a Scenario does not change the Feature's identity by itself.

## Cardinalities and invariants

For a confirmed Scenario:

| Relationship | Cardinality | Rule |
| --- | ---: | --- |
| owning IR | exactly 1 | Scenario analysis belongs to one Initial Requirement context |
| primary Feature | exactly 1 | The Feature must be confirmed by the owning IR and is the stakeholder-visible capability exercised by the Scenario |
| informed SRs | 1..* or explicit no-new-obligation conclusion | Scenario analysis must close its downstream obligation question |

Additional descriptive references MAY exist when a project implementation needs them, but they do not change these universal relationships.

## Scenario quality

A confirmed Scenario is acceptable when:

- the actor and stakeholder goal are clear;
- the context and trigger distinguish the situation;
- preconditions are stated where material;
- interaction is externally observable and solution-independent;
- expected, alternative, and failure outcomes are sufficient to expose materially different obligations;
- its primary Feature remains a durable capability rather than a restatement of the Scenario;
- downstream SR traceability is complete or intentionally concluded;
- no Module, Interface, or implementation design is smuggled into the black-box description.

## Architecture walkthroughs

The [Scenario View (+1)](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/views/scenario.md#scenario-view-1) projects architectural context for an existing Scenario. Its [outcome walkthroughs](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/views/scenario.md#outcome-walkthroughs) retain the Scenario's full expected, alternative and failure outcomes, then select relevant obligations and architecture details from their own sources.

The Scenario remains the stakeholder situation; the walkthrough is a derived reading of related engineering knowledge. Selecting architectural or test context does not confirm complete outcome coverage, executed behavior or applicable evidence. Missing explanations remain explicit without rewriting the Scenario to match the available implementation.
