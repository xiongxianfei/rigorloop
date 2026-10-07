# 2. Requirement Analysis

## 2. Requirement Analysis

REM requirement analysis is built from the requirement [Concepts](../../concepts/requirements.md#requirements), the requirement-related [Principles](../../principles/README.md), the [Requirement model](../../models/requirements.md), and the [Requirement Analysis methods](../../methods/README.md).

### Concepts

REM distinguishes:

- [Raw Requirement (RR)](../../concepts/requirement-input.md#requirement-input) — incoming request/proposal/issue/incident/source material offered for analysis, not a durable normative Requirement by itself.
- [Initial Requirement (IR)](../../concepts/requirements.md#requirements) — the initial durable expression of the need after reconciliation with current requirement knowledge.
- [System Requirement (SR)](../../concepts/requirements.md#requirements) — the durable system-level obligation derived from the IR.
- [Allocated Requirement (AR)](../../concepts/requirements.md#requirements) — the durable lower-level obligation derived from an SR and allocated to architecture.
- [Scenario](../../concepts/scenarios.md#requirement-analysis-entities) — a first-class governed stakeholder-visible situation with stable identity, lifecycle, one owning IR, and one primary Feature.
- [Feature](../../concepts/system-and-architecture.md#system-and-architecture-assets) — the durable stakeholder-visible capability.
- [Function](../../concepts/system-and-architecture.md#system-and-architecture-assets) — the durable logical system behavior.

These distinctions exist so REM does not collapse need, capability, usage context, obligation, behavior, and architecture into one kind of record.

### Principles

[Needs can outlive solutions](../../principles/needs-can-outlive-solutions.md), [satisfaction depends on domain assumptions](../../principles/satisfaction-depends-on-domain-assumptions.md), and [origin differs from realization](../../principles/origin-and-realization-answer-different-questions.md) explain relevant relationships. They do not uniquely imply REM's selected hierarchy.

### Selected model commitments

The current models below retain these commitments:

- requirements remain distinct from system assets;
- the durable requirement hierarchy is `IR → SR → AR`;
- Features and Functions are durable assets;
- requirement allocation and functional allocation are separate but must remain consistent;
- true containment uses trees while cross-domain traceability uses typed graph relationships;
- semantic facts are authored once.

### Models

The [Requirement model](../../models/requirements.md) makes the requirement hierarchy normative:

```text
IR
└── SR
    └── AR
```

The [Scenario model](../../models/scenarios.md) owns Scenario identity, lifecycle, black-box boundaries, and Scenario cardinalities.
The [System Design model](../../models/system-design.md) owns durable Feature and Function relationships.
The [Architecture Design model](../../models/architecture-design.md) owns Function/AR allocation to Modules and Module interaction through Interfaces.

Together they define the core traceability:

```text
IR ── confirms ──────> Feature
IR ── confirms ──────> Scenario
Scenario ─exercises──> Feature
Scenario ─informs────> SR
SR ── confirms ──────> Function
Function ─primaryModule──> Module
AR ── allocatedTo ──────> Module
```

### Methods

REM currently uses [5W2H analysis](../../methods/5w2h.md) to analyze every IR, SR, and AR.

5W2H answers:

- What?
- Why?
- Who?
- When?
- Where?
- How?
- How much?

The [Requirement Analysis method](../../methods/requirement-analysis.md) first reconciles RR input with current requirements, then establishes or refines justified IRs and derives/refines SRs. AR formulation uses the same requirement-quality rules later, once Architecture Allocation has enough responsibility context to make lower-level allocation meaningful.

For the IR, REM additionally uses [Scenario Analysis](../../methods/scenario-analysis.md):

```text
RR input
    │
    ▼
reconcile current needs
    │
    ▼
5W2H
    │
    ▼
IR
├── confirms → Feature
└── confirms → Scenario(s)
                  │
                  ├── exercises → Feature
                  └── informs → SR
                                   │
                                   └── confirms → Function
```

Scenario Analysis creates and maintains first-class governed Scenario entities and confirms the durable Feature they exercise.
It may reveal candidate behavior, but [Functional Analysis](../../methods/functional-analysis.md) confirms the corresponding Function only after SR obligations are sufficiently clear.
[Architecture Allocation](../../methods/architecture-allocation.md) then assigns each Function to accountable Module responsibility and, with architecture context available, derives/refines and allocates the required AR obligations.

### Why REM is built this way

This separation allows:

- the IR to preserve stakeholder need and context;
- the Feature to remain durable while Scenarios change;
- Scenarios to explain concrete stakeholder use without becoming product architecture;
- SRs to turn stakeholder situations into assessable system obligations;
- Functions to describe logical behavior independently from the requirement text;
- ARs to allocate lower-level obligations without turning Modules into requirement categories.

---
