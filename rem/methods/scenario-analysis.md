# Scenario Analysis method

Use this method during Initial Requirement analysis to describe concrete stakeholder-visible situations, confirm the durable Feature needed by the IR, and expose candidate system behavior for later System Requirement analysis.

The [Scenario concept](../concepts/README.md#requirement-analysis-artifacts) defines what a Scenario means.
The [System Design model](../models/system-design.md) owns the relationships among IR, Scenario, Feature, SR, and Function.
The [Requirement model](../models/requirements.md#cross-domain-relationships) owns the cross-domain traceability rules.

## Inputs

Start with:

- an IR and its current [5W2H analysis](5w2h.md);
- supported stakeholder, product, operational, or engineering context;
- existing Features when the need may extend an already durable capability;
- known constraints and unresolved questions.

Do not begin by assuming a new Feature or Module is required.

## Develop scenarios

For each materially distinct stakeholder situation, describe:

- **actor** — who is trying to achieve an outcome;
- **context** — the relevant operating or engineering situation;
- **trigger** — what starts the scenario;
- **preconditions** — what must already be true;
- **flow** — the meaningful stakeholder/system interaction;
- **expected outcome** — what success means to the stakeholder;
- **alternatives or failures** — materially different paths when relevant.

A Scenario should be concrete enough to reveal required behavior without becoming an implementation script.

## Confirm the Feature

Ask what durable stakeholder-visible capability is exercised across the scenarios.

Reuse an existing Feature when the scenarios extend an already established capability.
Create a new Feature only when the stakeholder-visible capability has independent durable meaning.

Define or refine the Feature using the [System Design criteria](../models/system-design.md#feature-definition):

1. Identify the participant, the capability they gain, and its value across the Scenarios.
2. Give the Feature a name that communicates its purpose and subject; add a condition when needed to distinguish it from neighboring capabilities.
3. Describe its included scope and the boundary with related Features, using the declared profile when support is intentionally limited.
4. Read the name, description, scope, and Scenarios together and correct any broader promise or hidden responsibility.

For example, "Inspect engineering definitions and their rationale" identifies what a participant can inspect; the description establishes who benefits and which information the capability covers.
Clarity takes precedence over forcing a particular grammatical form.

The IR confirms the Feature.
Several IRs may affect the same Feature over time, and one Feature may be exercised by many Scenarios.

Do not use one Scenario as the Feature definition.
A Scenario may become obsolete while the Feature remains active.

## Identify candidate behavior

Use the Scenarios to identify logical behavior the system appears to need.

At this stage, behavior is a candidate.
Do not make the Scenario the authoritative Function definition.

Candidate behavior feeds System Requirement derivation.
The corresponding Function becomes authoritative when the SR analysis confirms that logical behavior.

```text
IR
├── confirms → Feature
└── confirms → Scenario
                  │
                  ├── exercises → Feature
                  └── informs → SR
                                   │
                                   └── confirms → Function
```

## Reconcile with System Requirements

For each Scenario, ask:

- What system obligation is required for the expected outcome?
- Which condition or failure path requires a separate obligation?
- Which behavior is required by that obligation?
- Is the behavior already represented by an existing Function?
- Does one SR require several Functions?
- Does one Function support several SRs or Features?

Use [Requirement Analysis](requirement-analysis.md#derive-system-requirements) to author the SRs.
The SR owns the normative system obligation; the Function owns the logical behavior.

## Completion criteria

Scenario Analysis is sufficiently complete when:

- the IR has one or more supported Scenarios where Scenario Analysis is relevant;
- the stakeholder-visible Feature is confirmed or an existing Feature is intentionally reused;
- the Feature's name, purpose, participant value, and scope agree and distinguish it from neighboring capabilities;
- each Scenario has a clear actor, context, trigger, and expected outcome;
- candidate behavior has been identified without prematurely fixing architecture;
- system obligations revealed by the Scenarios are either represented by SRs or remain explicit open questions;
- Scenarios, Features, SRs, and Functions are not treated as interchangeable concepts.

Scenario Analysis does not approve requirements, allocate architecture, or provide verification evidence.
