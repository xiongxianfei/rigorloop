# REM Knowledge Reconstruction

**Purpose:** Explain how the existing REM Concepts, Principles, Models, and Methods combine to build the RigorLoop Engineering Method and why each part exists.

This file is an integration guide.
It does not introduce another REM knowledge category and it does not redefine the linked material.
The linked files remain authoritative for their own definitions, rules, structures, and procedures.

---

## 1. How REM knowledge is built

REM reconstructs engineering knowledge through four complementary kinds of material:

- [Concepts](concepts/README.md) define what the engineering terms mean.
- [Principles](principles/README.md) define the durable commitments REM must preserve.
- [Models](models/README.md) define valid structures, relationships, and invariants.
- [Methods](methods/README.md) define how engineers create and refine valid engineering information.

A reader should use this file to understand how those sources work together.

The general pattern is:

```text
engineering question
      │
      ▼
Concepts
what do the terms mean?
      │
      ▼
Principles
what must remain true?
      │
      ▼
Models
how does the information fit together?
      │
      ▼
Methods
how do engineers perform the work?
      │
      ▼
coherent REM engineering knowledge
```

The arrows show how to reconstruct the reasoning.
They do not make Concepts, Principles, Models, and Methods a lifecycle or hierarchy.

---

## 2. Requirement Analysis

REM requirement analysis is built from the requirement [Concepts](concepts/README.md#requirements), the requirement-related [Principles](principles/README.md), the [Requirement model](models/requirements.md), and the [Requirement Analysis methods](methods/README.md).

### Concepts

REM distinguishes:

- [Initial Requirement (IR)](concepts/README.md#requirements) — the initial durable expression of the need.
- [System Requirement (SR)](concepts/README.md#requirements) — the durable system-level obligation derived from the IR.
- [Allocated Requirement (AR)](concepts/README.md#requirements) — the durable lower-level obligation derived from an SR and allocated to architecture.
- [Scenario](concepts/README.md#requirement-analysis-entities) — a first-class governed black-box stakeholder situation with stable identity and lifecycle.
- [Feature](concepts/README.md#system-and-architecture-assets) — the durable stakeholder-visible capability.
- [Function](concepts/README.md#system-and-architecture-assets) — the durable logical system behavior.

These distinctions exist so REM does not collapse need, capability, usage context, obligation, behavior, and architecture into one kind of record.

### Principles

The requirement reasoning is governed primarily by the [REM principles](principles/README.md):

- requirements remain distinct from system assets;
- the durable requirement hierarchy is `IR → SR → AR`;
- Features and Functions are durable assets;
- requirement allocation and functional allocation are separate but must remain consistent;
- true containment uses trees while cross-domain traceability uses typed graph relationships;
- semantic facts are authored once.

### Models

The [Requirement model](models/requirements.md) makes the requirement hierarchy normative, while the [Scenario model](models/scenarios.md) owns governed Scenario identity, lifecycle, and cross-domain Scenario relationships:

```text
IR
└── SR
    └── AR
```

Cross-domain traceability is divided by authoritative owner:

```text
Scenario model:
IR ── confirms ──────> Scenario
Scenario ─exercises──> Feature
Scenario ─informs────> SR

System Design model:
IR ── confirms ──────> Feature
SR ── confirms ──────> Function

Architecture Design model:
AR ── allocatedTo ───> Module
```

The [System Design model](models/system-design.md) owns the durable Feature and Function relationships.
The [Architecture Design model](models/architecture-design.md) owns allocation to Modules and interaction through Interfaces.

### Methods

REM currently uses [5W2H analysis](methods/5w2h.md) to analyze every IR, SR, and AR.

5W2H answers:

- What?
- Why?
- Who?
- When?
- Where?
- How?
- How much?

The [Requirement Analysis method](methods/requirement-analysis.md) uses that analysis to establish the IR, derive SRs, and derive ARs.

For the IR, REM additionally uses [Scenario Analysis](methods/scenario-analysis.md):

```text
initial need
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

Scenario Analysis creates and governs first-class stakeholder-visible Scenario entities and confirms the durable Feature those situations exercise.
It may reveal candidate behavior, but the corresponding Function becomes authoritative through SR analysis.

### Why REM is built this way

This separation allows:

- the IR to preserve stakeholder need and context;
- the Feature to remain durable while Scenarios change;
- Scenarios to preserve concrete stakeholder-use context with stable identity and lifecycle without becoming product architecture;
- SRs to turn stakeholder situations into assessable system obligations;
- Functions to describe logical behavior independently from the requirement text;
- ARs to allocate lower-level obligations without turning Modules into requirement categories.

---

## 3. System Design

REM System Design is built from the [Feature and Function concepts](concepts/README.md#system-and-architecture-assets), the durable-asset and clarity [Principles](principles/README.md), and the [System Design model](models/system-design.md).

The essential structure is:

```text
IR ── confirms ──────> Feature
Scenario ─exercises──> Feature
SR ── confirms ──────> Function
Feature ─realizedBy──> Function
```

### Why Feature exists

A Feature is durable because one stakeholder-visible capability can be exercised through many Scenarios over its lifetime.

For example:

```text
Feature: Engineering Knowledge Search

Scenario: find by identifier
Scenario: search by text
Scenario: filter by requirement type
Scenario: agent discovers related architecture
```

The Scenarios may change or become obsolete while the Feature retains its identity.

### Why Function exists

A Function represents logical system behavior rather than a requirement statement or implementation component.

The SR establishes what the system must satisfy.
The Function expresses the behavior the system performs to satisfy that obligation.

Principle 16 connects naming to engineering meaning.
The [System Design model](models/system-design.md#clear-names-and-boundaries) defines the Feature and Function clarity criteria; [Scenario Analysis](methods/scenario-analysis.md#1-confirm-the-stakeholder-goal-and-feature) applies them to capabilities, and [Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements) applies them before an SR confirms a Function.
The [Operational Support model](models/operational-support.md#naming-and-location) separately owns representation choices such as deriving filenames from an ID and title.

The [Requirement Analysis method](methods/requirement-analysis.md#derive-system-requirements) currently supplies the entry point for confirming Functions from SRs.
A dedicated general Functional Analysis method has not yet been authored in the current REM package; that is a visible method gap rather than an implicit procedure.

---

## 4. Architecture Design

REM Architecture Design is built from the [Module and Interface concepts](concepts/README.md#system-and-architecture-assets), the allocation [Principles](principles/README.md), and the [Architecture Design model](models/architecture-design.md).

Two engineering paths converge on architecture:

```text
Function ── allocatedTo ──> Module
AR ──────── allocatedTo ──> Module
                              ↕
                           Interface
```

The Function says what logical behavior must occur.
The AR says what lower-level obligation the architecture must satisfy.
The Module owns architectural responsibility.
The Interface defines significant interactions between Modules.

### Why REM keeps the allocations separate

Functional allocation and requirement allocation answer different questions:

- `Function → Module`: who performs this behavior?
- `AR → Module`: who is responsible for satisfying this allocated obligation?

Reviewing them together helps detect architecture that performs behavior without owning its obligations, or owns obligations without the behavior, state, policy, or interfaces required to satisfy them.

The current [Requirement Analysis method](methods/requirement-analysis.md#derive-allocated-requirements) defines how ARs are derived.
The current REM package does not yet contain a standalone Architecture Design procedure beyond the structural [Architecture Design model](models/architecture-design.md); that gap should remain explicit until such a Method is authored.

---

## 5. Operational Support

REM Operational Support is built from the engineering-model and metamodel [Concepts](concepts/README.md#engineering-model-and-its-support), the metamodel and tool-independence [Principles](principles/README.md), and the [Operational Support model](models/operational-support.md).

Operational Support answers how the engineering model itself is:

- represented;
- named;
- validated;
- authored;
- maintained;
- migrated;
- versioned;
- interpreted across historical states.

The [Operational Support model](models/operational-support.md) deliberately separates universal REM semantics from project representation choices.

For example:

```text
REM concept:
stable engineering identity

project representation:
JSON field, database key, repository identifier, or another mechanism
```

This is why REM does not define Git, JSON, Rust, or filesystem layout as universal methodology requirements.

A dedicated Operational Support procedure has not yet been authored in [Methods](methods/README.md).
Until one exists, the model defines the required semantics while project-specific procedures remain outside the universal REM method.

---

## 6. Verification, Evidence, and Engineering Claims

The assurance knowledge is built from the [Verification, Evidence, Judgment, and Traceability concepts](concepts/README.md#assurance-and-traceability), Principle 13 in the [REM principles](principles/README.md), and the [Assurance model](models/README.md#assurance).

The core relationship is:

```text
Requirement
    │ verifiedBy
    ▼
Verification
    │ produces
    ▼
Evidence
    │ supports
    ▼
Judgment
```

REM keeps these concepts separate because:

- a Requirement states what must be true;
- Verification defines how it will be assessed;
- Evidence records what was actually observed;
- Judgment states what the applicable Evidence supports.

The current REM package defines these concepts and model relationships but does not yet contain a dedicated Verification Method file.
That is another explicit method gap.

---

## 7. Change, Baseline, and Provenance

Evolution knowledge is built from the [Change, Baseline, Configuration Management, and Provenance concepts](concepts/README.md#evolution-and-history), Principles 10–12 and 15 in the [REM principles](principles/README.md), and the [Evolution model](models/README.md#evolution).

The core idea is:

```text
Baseline N
    │
    │ Change
    ▼
Baseline N+1
```

Current engineering definitions explain what is true now.
Changes explain why the current state evolved.
Configuration history preserves what was true before.

This is why REM is tool-independent.
A project may use Git or another configuration-management mechanism, but the REM concepts are Change, Baseline, Provenance, and recoverable history rather than Git-specific objects.

---

## 8. How to reconstruct an REM decision

When a reader asks why REM contains a particular rule, follow the links in this order.

### Example: Why does REM use `IR → SR → AR`?

1. Read the requirement definitions in [Concepts](concepts/README.md#requirements).
2. Read Principles 1, 2, 5, 7, and 8 in [Principles](principles/README.md).
3. Read the containment and cross-domain rules in the [Requirement model](models/requirements.md).
4. Read [5W2H](methods/5w2h.md) and [Requirement Analysis](methods/requirement-analysis.md) to see how engineers create the three levels.

### Example: Why does REM keep Feature separate from Scenario?

1. Read [Scenario](concepts/README.md#requirement-analysis-entities) and [Feature](concepts/README.md#system-and-architecture-assets).
2. Read Principles 3, 10, and 17 in [Principles](principles/README.md).
3. Read the [Scenario model](models/scenarios.md) and [System Design model](models/system-design.md).
4. Read [Scenario Analysis](methods/scenario-analysis.md).

### Example: Why does SR confirm Function while AR allocates to Module?

1. Read [SR, AR, Function, and Module](concepts/README.md).
2. Read Principles 5–7 in [Principles](principles/README.md).
3. Read the [Requirement model](models/requirements.md), [System Design model](models/system-design.md), and [Architecture Design model](models/architecture-design.md).
4. Read the SR and AR procedures in [Requirement Analysis](methods/requirement-analysis.md).

### Example: Why must a Feature or Function name explain its purpose?

1. Read Principle 16 in [Principles](principles/README.md).
2. Read the naming and definition criteria in the [System Design model](models/system-design.md#clear-names-and-boundaries).
3. Follow the Feature procedure in [Scenario Analysis](methods/scenario-analysis.md#1-confirm-the-stakeholder-goal-and-feature) or the Function procedure in [Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements).
4. Read [Operational Support](models/operational-support.md#naming-and-location) for the separate question of how a project represents that name in directories, filenames, or other storage.

This is the intended role of this file: it tells the reader which authoritative knowledge to follow rather than restating that knowledge here.

---

## 9. How REM itself should be renewed

When REM knowledge changes:

1. identify the engineering problem;
2. locate the authoritative [Concept](concepts/README.md), [Principle](principles/README.md), [Model](models/README.md), or [Method](methods/README.md) that owns the affected fact;
3. change that owner;
4. follow its links to dependent REM knowledge;
5. reconcile affected Concepts, Principles, Models, and Methods;
6. exercise the changed reasoning end-to-end;
7. keep unresolved method gaps explicit rather than inventing undocumented procedure.

For example, changing what `Feature` means requires checking:

- the [Feature concept](concepts/README.md#system-and-architecture-assets);
- the durable-asset [Principle](principles/README.md);
- the [Requirement model](models/requirements.md);
- the [System Design model](models/system-design.md);
- [Scenario Analysis](methods/scenario-analysis.md);
- [Requirement Analysis](methods/requirement-analysis.md).

The goal is not to fill four document categories.
The goal is to preserve one coherent engineering method.

---

## 10. Canonical reading path

A new REM reader should normally follow:

1. [REM overview](README.md)
2. [Concepts](concepts/README.md)
3. [Principles](principles/README.md)
4. [Models](models/README.md)
5. [Methods](methods/README.md)
6. this reconstruction guide whenever they need to understand how those sources combine and why a REM decision exists.

For Requirement Analysis specifically:

```text
[IR / SR / AR / Scenario / Feature / Function concepts]
                    │
                    ▼
              [REM principles]
                    │
                    ▼
          [Requirement model]
          [System Design model]
                    │
                    ▼
               [5W2H]
          [Scenario Analysis]
        [Requirement Analysis]
```

Those links, rather than this file alone, define REM.
