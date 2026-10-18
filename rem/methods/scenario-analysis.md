# Scenario Analysis method

Use Scenario Analysis during Initial Requirement analysis to develop first-class stakeholder-visible Scenarios, confirm the durable Feature exercised by those Scenarios, and expose candidate system obligations for later SR analysis.

The [Scenario concept](../concepts/scenarios.md#requirement-analysis-entities) defines what a Scenario means.
The [Scenario model](../models/scenarios.md) owns identity, lifecycle, cardinality, and black-box invariants.
The [Requirement model](../models/requirements.md) owns IR/SR/AR and cross-domain traceability.
The [System Design model](../models/system-design.md) owns Features and Functions.

## Inputs

Start with:

- an IR and its current [5W2H analysis](5w2h.md);
- supported stakeholder, product, operational, or engineering context;
- existing Features when the need may extend an already durable capability;
- known constraints, assumptions, and unresolved questions.

Do not begin by assuming a new Feature, Function, Module, Interface, API, or implementation is required.

## Step 1 — Confirm or reuse the Feature

Ask:

> What durable stakeholder-visible capability is required to address the Initial Requirement?

Reuse an existing Feature when the need extends the same durable capability.
Create a new Feature only when the capability has independent stakeholder meaning and a distinct evolution boundary.

Define or refine the Feature using the [System Design criteria](../models/system-design.md#feature-definition):

1. identify who benefits;
2. identify the capability they gain;
3. explain its value;
4. define included scope and boundaries with neighboring Features;
5. give it a clear name that survives implementation changes.

The IR confirms the Feature.
Several IRs may affect the same Feature over time.

## Step 2 — Identify materially distinct stakeholder situations

Identify situations that differ enough to expose different system obligations.
Useful sources of variation include:

- actor or authority;
- stakeholder goal;
- starting information or state;
- operating context;
- trigger;
- important boundary condition;
- expected outcome;
- failure or recovery condition.

Do not create a new Scenario for trivial UI or wording variation.
Create a separate Scenario when the variation is likely to reveal materially different required behavior or constraints.

## Step 3 — Establish Scenario identity

Each Scenario is a first-class governed entity with a stable identity.
A new Scenario begins in `draft` state.

A Scenario belongs to exactly one owning IR.
A confirmed Scenario exercises exactly one primary Feature.

If one apparent Scenario requires several primary Features, split it into focused Scenarios unless REM later defines a separate Journey concept.

## Step 4 — Describe the black-box Scenario

Describe only stakeholder-observable information:

- **actor** — who is trying to achieve the outcome;
- **goal** — what the actor wants to accomplish or understand;
- **context** — the relevant situation;
- **trigger** — what starts the Scenario;
- **preconditions** — what must already be true;
- **interaction** — meaningful actor/system exchanges;
- **expected outcome** — what successful completion means;
- **alternative outcomes** — legitimate materially different results;
- **failure outcomes** — relevant failures and externally visible consequences;
- **recovery outcome** — where recovery matters to the stakeholder.

A Scenario MUST remain black-box.
Do not define Module allocation, Interface/API design, Function call sequences, persistence schemas, implementation classes, packages, services, algorithms, queues, threads, or deployment topology.

Use this test:

> Would the Scenario remain valid if the internal implementation were completely replaced?

If not, remove the internal design detail.

## Step 5 — Analyze alternatives, boundaries, and failures

Do not stop at the happy path.
Consider only materially relevant variations, such as:

- empty or missing result;
- ambiguity;
- invalid or unsupported input;
- authorization difference;
- boundary or capacity condition;
- unavailable dependency as observed by the stakeholder;
- cancellation or recovery where stakeholder-visible.

The purpose is to expose obligations, not to enumerate every possible test case.

## Step 6 — Extract candidate system obligations

For every meaningful interaction and outcome, ask:

> What must the system guarantee for this Scenario to succeed or fail correctly?

Write candidate obligations in system terms without yet committing them as SRs.

Example:

```text
Scenario observation:
The stakeholder requests a known engineering entity and receives it.

Candidate obligation:
The system must resolve a governed engineering entity from its stable identifier.
```

Candidate behavior may also be identified, but remains provisional at this stage.

## Step 7 — Reconcile into SRs

Use [Requirement Analysis](requirement-analysis.md#derive-system-requirements) to turn candidate obligations into durable SRs.

One Scenario may inform several SRs.
One SR may be informed by several Scenarios.

```text
Scenario ── informs ──> SR
```

Before Scenario Analysis for an IR is considered complete, every confirmed Scenario MUST either:

1. inform at least one SR; or
2. have an explicit analysis conclusion explaining why it introduces no additional system obligation.

## Step 8 — Hand off candidate behavior to Functional Analysis

Scenario Analysis may reveal candidate behavior, but does not create authoritative Functions.

Use [Functional Analysis](functional-analysis.md) after SRs are sufficiently clear:

```text
Scenario
   ↓ reveals candidate behavior
SR
   ↓ confirms
Function
```

The SR owns the normative obligation.
The Function owns the durable logical behavior.

## Step 9 — Confirm the Scenario

A draft Scenario may become `confirmed` when:

- its owning IR is clear;
- its primary Feature is clear;
- actor, context, trigger, and stakeholder goal are understandable;
- interaction and outcomes are black-box;
- materially relevant alternative/failure behavior has been considered;
- downstream SR analysis is complete or explicitly concluded;
- no unresolved issue would change the Scenario's essential stakeholder meaning.

## Step 10 — Maintain the Scenario over time

Use the lifecycle:

```text
draft → confirmed → obsolete
```

Mark a Scenario `obsolete` when the stakeholder situation is no longer supported or relevant.
Do not retire the Feature merely because one Scenario becomes obsolete.

When a confirmed Scenario changes materially, reassess:

- its owning IR;
- its Feature;
- informed SRs;
- candidate and confirmed Functions;
- verification scope affected downstream.

Preserve historical meaning through configuration history rather than rewriting the past.

## Completion criteria

Scenario Analysis for an IR is sufficiently complete when:

- the durable Feature is confirmed or an existing Feature is intentionally reused;
- materially distinct stakeholder situations have governed Scenario identities;
- every confirmed Scenario has exactly one owning IR and one primary Feature;
- Scenarios are black-box and solution-independent;
- relevant normal, alternative, failure, and recovery outcomes have been considered;
- candidate obligations have been reconciled into SRs or explicitly concluded as unnecessary;
- candidate behavior is handed to SR/Functional Analysis rather than silently becoming a Function;
- Scenarios, Features, SRs, Functions, Modules, and verification artifacts remain semantically distinct.

Scenario Analysis does not approve requirements, allocate architecture, define implementation, or provide verification evidence.
