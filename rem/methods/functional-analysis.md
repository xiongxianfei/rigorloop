# Functional Analysis method

Use Functional Analysis after System Requirements are sufficiently clear to confirm the durable logical behavior the system must perform.
The [Function concept](../concepts/system-and-architecture.md#system-and-architecture-assets) defines what a Function means, and the [System Design model](../models/system-design.md) owns Feature-to-Function and SR-to-Function relationships.

## Purpose

Functional Analysis answers:

> What logical behavior must the system perform to satisfy the confirmed System Requirements and realize the stakeholder-visible Features?

It does not allocate behavior to Modules and does not prescribe implementation technology.

## Inputs

Start with:

- approved or sufficiently mature SRs;
- confirmed Features and Scenarios relevant to those SRs;
- existing Functions that may already represent the required behavior;
- unresolved behavioral questions from Scenario or Requirement Analysis.

## Identify required behavior

For each SR, ask:

- What behavior must occur for this obligation to be satisfied?
- What inputs or selected state does that behavior operate on?
- Under what conditions does it apply?
- What outputs or externally meaningful results does it produce?
- What material failure or incomplete outcomes belong to the behavior?
- Does an existing Function already express this behavior?

Do not create one Function merely because one SR exists.
SR-to-Function relationships may be many-to-many.

## Define the Function boundary

A Function definition SHOULD make clear:

- behavior name and subject;
- inputs and relevant state;
- conditions or preconditions;
- logical behavior performed;
- outputs;
- material failure or incomplete outcomes;
- where this responsibility ends and another Function begins.

Keep the definition independent of Module, process, source directory, service, class, transport, or deployment structure wherever practical.

## Reuse versus create

Reuse an existing Function when the required behavior has the same engineering meaning and evolution boundary.
Create a new Function when the behavior has a distinct responsibility or must evolve independently.

Do not merge Functions solely because their implementations look similar.
Do not split Functions solely to mirror requirement identifiers.

## Confirm relationships

Before System Design for an approved SR is considered complete, it MUST confirm at least one Function that carries the behavior required by the obligation.
An approved requirement may enter Functional Analysis without that relationship; approval establishes the obligation to design against, not completed logical behavior.
The same Function may be confirmed by several SRs.
A Function may realize several Features.

```text
SR ── confirms ──> Function
Feature ── realizedBy ──> Function
```

When an SR is primarily a quality or constraint obligation, confirm the Function or Functions whose behavior is governed by that obligation rather than inventing a synthetic "quality Function."

## Completion criteria

Functional Analysis is complete enough for architecture allocation when:

- every approved SR confirms at least one relevant Function;
- Functions have clear, non-overlapping responsibility boundaries where practical;
- Feature-to-Function relationships explain how the stakeholder-visible capability is realized;
- Functions remain logical and implementation-independent;
- unresolved behavior gaps are explicit rather than hidden in architecture;
- duplicate or near-duplicate Functions have been reconciled intentionally.

Functional Analysis does not allocate Modules, define Interfaces, or establish verification evidence.
