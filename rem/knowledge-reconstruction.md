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
- [Scenario](concepts/README.md#requirement-analysis-entities) — a first-class governed stakeholder-visible situation with stable identity, lifecycle, one owning IR, and one primary Feature.
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

The [Requirement model](models/requirements.md) makes the requirement hierarchy normative:

```text
IR
└── SR
    └── AR
```

The [Scenario model](models/scenarios.md) owns Scenario identity, lifecycle, black-box boundaries, and Scenario cardinalities.
The [System Design model](models/system-design.md) owns durable Feature and Function relationships.
The [Architecture Design model](models/architecture-design.md) owns Function/AR allocation to Modules and Module interaction through Interfaces.

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

Scenario Analysis creates and maintains first-class governed Scenario entities and confirms the durable Feature they exercise.
It may reveal candidate behavior, but [Functional Analysis](methods/functional-analysis.md) confirms the corresponding Function only after SR obligations are sufficiently clear.
[Architecture Allocation](methods/architecture-allocation.md) then assigns accountable Module responsibility.

### Why REM is built this way

This separation allows:

- the IR to preserve stakeholder need and context;
- the Feature to remain durable while Scenarios change;
- Scenarios to explain concrete stakeholder use without becoming product architecture;
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
The [System Design model](models/system-design.md#clear-names-and-boundaries) defines Feature and Function clarity criteria. [Scenario Analysis](methods/scenario-analysis.md#step-1--confirm-or-reuse-the-feature) applies them to capabilities, [Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements) derives the SR obligations, and [Functional Analysis](methods/functional-analysis.md) confirms the Functions those SRs require.
The [Operational Support model](models/operational-support.md#naming-and-location) separately owns representation choices such as deriving filenames from an ID and title.

[Requirement Analysis](methods/requirement-analysis.md#derive-system-requirements) owns SR derivation.
[Functional Analysis](methods/functional-analysis.md) owns confirmation and boundary definition of Functions from those SRs and reconciliation of Feature realization.

---

## 4. Architecture Design

REM Architecture Design is built from the [Module, Interface, and architecture-realization concepts](concepts/README.md#system-and-architecture-assets), the allocation and logical/physical separation [Principles](principles/README.md), the [Architecture Design model](models/architecture-design.md), and the [Architecture Allocation](methods/architecture-allocation.md) and [Architecture Design](methods/architecture-design.md) methods.

Architecture has two coupled semantic layers:

```text
Logical architecture
  Function ── primaryModule ──> Module
  AR ──────── allocatedTo ────> Module
                                   ↕
                                Interface
  significant state/data ─────> Module authority

Physical/software realization
  subordinate to Module / Interface
  ├── software realization
  ├── runtime realization
  ├── persistence realization
  ├── deployment realization
  ├── Interface realization
  └── technology rationale
```

The Function says what logical behavior must occur.
The AR says what lower-level obligation the architecture must satisfy.
The Module owns architectural responsibility and significant state/data authority.
The Interface owns a significant logical interaction contract.
Subordinate realization information explains how those responsibilities and contracts are concretely realized without introducing new universal entity classes.

### Why REM keeps logical and physical architecture separate

REM needs architecture to remain understandable when implementation technologies change.
A Module is therefore not synonymous with a service, process, package, datastore, deployment unit, or source directory.
Likewise, an Interface is not synonymous with HTTP, a queue, a function call, or another concrete transport.

The physical/software realization is still architecture when its consequences are material—for example when it changes lifecycle, isolation, failure boundaries, state authority, deployment/recovery, compatibility, significant qualities, or future evolution.
Incidental implementation choices remain implementation detail.

### Why REM keeps the two allocations separate

Functional allocation and requirement allocation answer different questions:

- `Function → Module`: who performs this behavior?
- `AR → Module`: who is responsible for satisfying this allocated obligation?

Reviewing them together helps detect architecture that performs behavior without owning its obligations, or owns obligations without the behavior, state, policy, or interfaces required to satisfy them.

### What Architecture Design must produce

The [Architecture Design model](models/architecture-design.md#architecture-semantic-outputs) defines semantic outputs rather than filenames or documents.
These include Module definitions, Function and AR allocations, Interface definitions, significant state/data ownership, and material software/runtime/persistence/deployment/Interface-realization/technology information where relevant.
Derived logical, runtime, datastore, deployment, or technology views help review but do not own the underlying facts.

The model's [subordinate-facet rules](models/architecture-design.md#organizing-subordinate-facets) allow logical definitions and material realization concerns to be represented separately while retaining one accountable owner.
Module facets may organize software, runtime, persistence, deployment, and technology information; Interface facets may organize interaction, representation, and technology information.
Their presence depends on material content, and their absence cannot stand in for a completion assessment.
Attributed observations, proposed choices, and material deferrals remain distinguishable; shared technology rationale is authored once and referenced by its consumers.
Operational Support chooses storage and naming conventions without turning these facets into universal entity types or making aggregate views authoritative.

[Requirement Analysis](methods/requirement-analysis.md#derive-allocated-requirements) defines how AR obligations are derived.
[Architecture Allocation](methods/architecture-allocation.md) establishes logical Function/AR responsibility and identifies Interfaces.
[Architecture Design](methods/architecture-design.md) completes state/data ownership, material physical/software realization, architecture review, and completion assessment without prescribing a storage format.

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
2. Read Principle 3 in [Principles](principles/README.md).
3. Read the [System Design model](models/system-design.md).
4. Read the [Scenario model](models/scenarios.md) and [Scenario Analysis](methods/scenario-analysis.md).

### Example: Why does SR confirm Function while AR allocates to Module?

1. Read [SR, AR, Function, and Module](concepts/README.md).
2. Read Principles 5–7 in [Principles](principles/README.md).
3. Read the [Requirement model](models/requirements.md), [System Design model](models/system-design.md), and [Architecture Design model](models/architecture-design.md).
4. Read [Requirement Analysis](methods/requirement-analysis.md), [Functional Analysis](methods/functional-analysis.md), and [Architecture Allocation](methods/architecture-allocation.md).

### Example: Why must a Feature or Function name explain its purpose?

1. Read Principle 16 in [Principles](principles/README.md).
2. Read the naming and definition criteria in the [System Design model](models/system-design.md#clear-names-and-boundaries).
3. Follow the Feature procedure in [Scenario Analysis](methods/scenario-analysis.md#step-1--confirm-or-reuse-the-feature), the Function procedure in [Functional Analysis](methods/functional-analysis.md), or the allocation procedure in [Architecture Allocation](methods/architecture-allocation.md).
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
           [Scenario model]
          [System Design model]
       [Architecture Design model]
                    │
                    ▼
               [5W2H]
          [Scenario Analysis]
        [Requirement Analysis]
         [Functional Analysis]
      [Architecture Allocation]
```

Those links, rather than this file alone, define REM.
