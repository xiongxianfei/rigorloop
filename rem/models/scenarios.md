# Scenario model

Scenario Analysis belongs to Requirement Analysis, but Scenario is a first-class governed REM entity.
The [Scenario concept](../concepts/README.md#requirement-analysis-entities) defines its meaning; the [Scenario Analysis method](../methods/scenario-analysis.md) explains how engineers create and refine Scenarios.

## Purpose

A Scenario preserves one concrete stakeholder-observable situation in which a durable Feature is exercised.
It provides stable analysis context for deriving System Requirements without becoming a Requirement, Function, architecture element, or verification case.

## Clear Scenario names

A Scenario's title identifies its stakeholder-visible goal or action and subject, adding the condition that distinguishes the situation when needed.
Readers should be able to distinguish neighboring Scenarios from their titles, with the goal, context, and outcomes supplying the complete meaning.
For example, "Retrieve a saved definition in a later session" distinguishes retrieval from saving or revising that definition; "Normal path" does not identify the engineering situation.

The title describes the stakeholder situation rather than internal design, a generic Feature name, or the Scenario's lifecycle state.
Refine the title when it is vague or no longer agrees with the content, using the [identity continuity rules](#identity-continuity) to decide whether the engineering meaning still represents the same Scenario.
[Operational Support](operational-support.md#naming-and-location) governs readable storage labels derived from the identity and title; REM does not prescribe a filename.

## Identity and lifecycle

Every Scenario has stable identity independent of its name or physical location.
A project representation selects the concrete identity syntax; `SCN-001` is illustrative rather than mandated by REM.

The Scenario lifecycle is:

```text
draft → confirmed → obsolete
```

- **draft** — the stakeholder situation is still being analyzed and may be incomplete.
- **confirmed** — the Scenario has a clear actor, goal, context, trigger, black-box interaction and outcomes; its primary Feature is established and the Scenario is accepted as current requirement-analysis knowledge.
- **obsolete** — the Scenario no longer describes a current supported stakeholder situation. Historical Baselines preserve its previous meaning.

An obsolete Scenario MAY identify a replacement Scenario. A replacement does not rewrite the previous Scenario's historical meaning.

## Ownership and cardinality

The canonical relationships are:

```text
IR ── confirms ──> Scenario ── exercises ──> Feature
                         │
                         └── informs ──> SR
```

Rules:

1. Every Scenario belongs to exactly one owning IR.
2. An IR may confirm multiple Scenarios.
3. A confirmed Scenario exercises exactly one primary Feature.
4. Multiple Scenarios may exercise the same Feature.
5. A Scenario may inform multiple SRs.
6. An SR may be informed by multiple Scenarios.
7. Scenario-to-SR relationships do not change the single-parent `IR → SR → AR` requirement tree.
8. A Scenario MUST NOT own or allocate a Module or Interface.
9. A Scenario MUST NOT be used as a Verification result or Evidence.

During drafting, Feature or SR relationships may be incomplete. Before Requirement Analysis is considered complete for the IR, every confirmed Scenario must be accounted for by the resulting SR set or by an explicit analysis conclusion that it introduces no additional system obligation.
Each Scenario follows the [single consequential open-question rule](../methods/requirement-analysis.md#keep-one-consequential-open-question); absence of a recorded question does not establish Scenario confirmation or analysis completeness.

## Black-box content

A confirmed Scenario describes at least:

- **actor** — stakeholder or external role pursuing the goal;
- **goal** — stakeholder-visible outcome;
- **context** — relevant situation or operating condition;
- **trigger** — event or need that starts the Scenario;
- **preconditions** — externally meaningful conditions already true;
- **interaction** — stakeholder/system actions and observable responses;
- **expected outcome** — successful stakeholder-visible result;
- **alternative or failure outcomes** — materially different observable results when relevant.

The Scenario boundary excludes internal solution design. It MUST NOT prescribe:

- Functions as internal call steps;
- Modules or architectural allocation;
- Interfaces or APIs;
- database schemas or internal state representation;
- source files, classes, crates, packages, or services;
- algorithms, threads, queues, protocols, or implementation technology.

A stakeholder-observable channel or constraint may be stated when the IR actually requires it, but the Scenario records the observable requirement rather than an internal implementation mechanism.
When the product models engineering information, its stakeholder interactions may refer to Requirements, Functions, Modules, or Interfaces as the information being authored or inspected. This does not allocate the product's internal behavior or prescribe how the product implements that interaction.

## Identity continuity

A Scenario keeps its identity when wording, detail, or externally equivalent interaction is refined without changing the stakeholder situation it represents.

Create a new Scenario when the change materially changes the Scenario's engineering meaning, such as a different stakeholder goal, a different primary Feature, or a materially distinct situation that exposes different system obligations.

Do not split Scenarios merely because implementation steps differ.

## Relationship to Feature

Feature is the durable stakeholder-visible capability; Scenario is one governed situation exercising that capability.
The Feature can remain active while individual Scenarios are introduced, changed, or made obsolete.

```text
Feature: Engineering Knowledge Search

├── Scenario: find a known entity by identifier
├── Scenario: search without knowing the identifier
└── Scenario: discover related engineering context
```

## Relationship to SR and Function

Scenario Analysis reveals candidate system obligations.
System Requirement analysis decides which obligations become SRs.
SR analysis then confirms the logical Functions required by those obligations.

```text
Scenario
    │ reveals obligations
    ▼
   SR
    │ confirms behavior
    ▼
Function
```

A Scenario does not directly make a Function authoritative.
