# Proposal: Introduce a Lightweight Requirement-to-Delivery Model

## Challenge

RigorLoop currently organizes work primarily through lifecycle artifacts such as proposal, specification, architecture, plan, implementation, and verification.

These artifacts are useful, but the relationship between them is not expressed through one simple conceptual model. Developers and agents may therefore need to infer how an original request becomes an approved direction, how that direction becomes system requirements, how architecture realizes those requirements, how requirements are allocated into implementation work, how milestones and tasks relate to requirements, and how implementation evidence traces back to the original intent.

Two established views help explain different parts of this process:

```text
Requirement refinement

RR → IR → SR → AR

Raw Requirement
→ Initial Requirement
→ System Requirement
→ Allocated Requirement
```

```text
Work decomposition

Epic
→ Feature
→ Story
→ Task
```

Introducing every concept as a new RigorLoop artifact, identifier, lifecycle stage, and review gate would add substantial ceremony. RigorLoop needs a systematic requirement-to-delivery model without becoming a heavyweight requirements-management platform.

## Goals

This change should:

* provide a simple conceptual model from original need to implementation;
* clarify the responsibilities of proposal, specification, architecture, and plan;
* distinguish requirement refinement from work decomposition;
* improve traceability between intent, requirements, design, delivery work, and evidence;
* let lower-level work explain why it exists;
* let important requirements show where they are realized;
* reuse existing RigorLoop artifacts rather than introducing many new entity types;
* support small changes without requiring unnecessary hierarchy;
* support larger changes with deeper decomposition when needed;
* provide a conceptual foundation for later simplification of individual skills and artifacts.

## Scope and non-goals

### In scope

This proposal introduces a lightweight conceptual model covering:

* RR — Raw Requirement;
* IR — Initial Requirement;
* SR — System Requirement;
* AR — Allocated Requirement;
* Epic / Feature / Story / Task work decomposition;
* the relationship of these concepts to proposal, specification, architecture, plan, implementation, review, and verification.

The model will initially be expressed through skill guidance, shared references, templates, and review criteria.

### Scope budget

| Work item | Treatment |
| --- | --- |
| Define the requirement-refinement and work-decomposition concepts | core to this proposal |
| Map the concepts to existing RigorLoop artifacts and review gates | core to this proposal |
| Add shared guidance, focused skill guidance, templates, examples, and review criteria | first-slice candidate |
| Add new lifecycle stages, artifacts, or mandatory entity identities | out of scope |
| Add machine-readable traceability or external tracker integrations | separate proposal |
| Remove test-spec or redistribute verification responsibilities | separate proposal |

### Non-goals

This proposal does not:

* create mandatory `RR`, `IR`, or `AR` artifacts;
* introduce new lifecycle stages for RR / IR / SR / AR;
* require persisted IDs for every conceptual level;
* require every change to use Epic → Feature → Story → Task;
* establish a one-to-one mapping between requirement and work hierarchies;
* introduce a requirements database or hosted management system;
* define integrations with Jira, GitHub Issues, Linear, or similar tools;
* remove `test-spec.md`;
* redistribute test-spec responsibilities;
* change Delivery Review behavior;
* define detailed machine-readable traceability;
* redesign the current review-gate workflow.

Concrete lifecycle changes that build on this model should remain separately owned proposals.

## Governing principle

> **RigorLoop should refine intent into requirements and allocate those requirements into work using existing artifacts, adding new structure only when it materially improves engineering decisions or traceability.**

## Proposed direction

Adopt two related but distinct conceptual views:

```text
Requirement refinement:
RR → IR → SR → AR

Work decomposition:
Epic → Feature → Story → Task
```

These views should connect to each other, but should not be treated as equivalent hierarchies.

### 1. RR — Raw Requirement

RR represents the original need before RigorLoop has clarified or approved it. It may be a customer request, bug report, developer idea, support issue, business need, technical concern, or stakeholder feedback. It may be vague, incomplete, unverified, solution-biased, or expressed in stakeholder language.

RigorLoop should not require a separate RR artifact. The original issue, request, prompt, or referenced source may serve as the raw input.

```text
Raw input
   ↓
RR
```

### 2. IR — Initial Requirement

The proposal performs the RR → IR refinement. It clarifies what problem matters, which outcomes are desired, what is in and out of scope, which principle guides the direction, which direction should be pursued, and whether that direction is feasible enough to continue.

```text
RR
 ↓ clarify
Proposal
 ↓ approve
IR
```

The approved proposal therefore serves as RigorLoop's durable IR-level artifact. No separate `ir.md` is required.

### 3. SR — System Requirement

The specification owns SR-level requirements. SRs state what the system must provide and should be sufficiently clear, observable, specific, testable, and verifiable.

For example:

```text
SR-07
A rejected governed mutation shall return a stable blocker code.

SR-08
A rejected governed mutation shall not modify governed state.
```

Stable SR identities remain useful because architecture, planning, implementation, review, and verification need to refer back to system behavior.

```text
IR
 ↓ specify
SR
```

### 4. Architecture — realization of SRs

Architecture should not be treated as another requirement level. It answers:

> **How can the approved system requirements be realized within the technical constraints of the system?**

Architecture may establish system boundaries, assign responsibilities to components, identify technical constraints, define structural invariants, and reveal limits that shape the final SR contract.

The relationship is iterative:

```text
SR
 ↕
Architecture
```

Design Review should confirm that SRs and architecture form one coherent design.

### 5. AR — Allocated Requirement

AR represents the allocation of system requirements to a concrete realization boundary. It answers:

> **Where is responsibility for satisfying this requirement assigned?**

That boundary might be a component, subsystem, module, service, milestone, team, or work package.

In the first version of this model, AR should remain a concept rather than a mandatory persisted entity. For example:

```text
SR-08
Rejected mutations must preserve governed state.

Architecture:
Transition validation occurs before mutation commit.

Plan:
M2 — Guard lifecycle mutation
Requirements:
- SR-08
```

The plan has effectively performed AR-level allocation without introducing `AR-001`, `AR-002`, or `AR-003` unless such identities later prove useful.

```text
SR + Architecture
       ↓ allocate
      AR
```

### 6. Work decomposition is a separate dimension

RigorLoop should explicitly avoid:

```text
RR = Epic
IR = Feature
SR = Story
AR = Task
```

Requirement refinement asks what is needed, how it has been clarified, and where responsibility is allocated. Work decomposition asks how implementation effort should be broken into manageable work. Their relationship is naturally many-to-many.

```text
SR-01 ──┐
SR-02 ──┼──→ Story A
SR-04 ──┘

SR-02 ─────→ Story B
```

One Story may realize several SRs, and one SR may require several Stories or milestones.

### 7. Epic / Feature / Story / Task should be proportional

RigorLoop should not require all four work levels.

A small change may need:

```text
Change
  ↓
M1
  ├── Task 1
  └── Task 2
```

A larger initiative may benefit from:

```text
Epic
  ↓
Feature
  ↓
Story
  ↓
Task
```

The hierarchy should expand only when an additional level improves ownership, sequencing, reviewability, traceability, or coordination. Taxonomy completeness is not itself a goal.

### 8. Plan becomes the primary allocation surface

The plan should be understood conceptually as the bridge from approved design into executable work:

```text
SR + Architecture
       ↓
Allocation
       ↓
Milestones / Stories
       ↓
Tasks / Subtasks
```

A milestone should make it possible to answer why it exists, which SRs it realizes, which architecture boundary it affects, what depends on it, and what work belongs inside it. The exact future plan contract should be defined separately.

### 9. Verification is a parallel traceability concern

Verification should not be introduced as another level in `RR → IR → SR → AR`. Instead, it checks whether the realized system actually satisfies the requirement chain.

```text
Requirement / design
       ↓
required verification
       ↓
tests / checks / evidence
```

This is parallel to implementation allocation:

```text
                 ┌→ allocation → work → implementation
SR + Architecture
                 └→ verification → evidence
```

The exact ownership of test design, test groups, or verification planning remains outside this conceptual proposal.

### 10. End-to-end traceability

The intended conceptual forward path is:

```text
Raw need
   ↓
RR
   ↓
Proposal / IR
   ↓
Specification / SR
   ↓
Architecture realization
   ↓
AR-style allocation
   ↓
Milestone / Story
   ↓
Task / Subtask
   ↓
Implementation
```

The important traceability property is:

> **Every lower-level work item should be able to explain why it exists, and every important higher-level requirement should be able to show where it is realized.**

Verification should then be able to traverse the result backward:

```text
Evidence
   ↑
Implementation
   ↑
Milestone / allocated work
   ↑
SR
   ↑
Approved proposal / IR
   ↑
Original need
```

### 11. Alignment with RigorLoop review gates

The conceptual model should clarify the purpose of the existing review gates without adding new ones.

#### Proposal Review

Conceptually evaluates `RR → IR` by asking whether the original need was correctly transformed into a worthwhile, bounded, and feasible direction.

#### Design Review

Conceptually evaluates `IR → SR ↔ Architecture` by asking whether the system requirements and architecture form a coherent realization of the approved direction.

#### Delivery Review

Conceptually evaluates allocation from `SR + Architecture` into milestones and work by asking whether the design has been allocated into a safe and credible delivery structure.

#### Code Review

Conceptually evaluates allocated work becoming implementation by asking whether the implementation correctly realizes the allocated design responsibilities.

#### Verify

Conceptually checks the complete evidence-to-implementation-to-SR-to-IR chain by asking whether the resulting evidence supports the approved system requirements and original direction.

### 12. Skill ownership

The conceptual model should be implemented through focused skill guidance rather than copied into every skill.

```text
proposal
→ RR → IR refinement

spec
→ IR → SR refinement

architecture
→ SR realization

plan
→ SR allocation + work decomposition

delivery-review
→ allocation and delivery coherence

verify
→ reverse traceability and evidence closure
```

A shared reference can explain the complete model. Each skill should load only the part relevant to its responsibility. This preserves progressive disclosure and avoids replacing workflow complexity with terminology complexity.

## Feasibility

**Assessment: Feasible.**

The proposed model largely formalizes relationships that already exist implicitly in RigorLoop. Existing artifacts already provide natural homes for the main concepts:

```text
Raw input       → RR
Proposal        → IR
Specification   → SR
Architecture    → realization
Plan            → allocation and work decomposition
Implementation  → execution
Verify          → evidence closure
```

The first implementation does not require new lifecycle stages, new mandatory artifacts, a requirements database, persisted RR / IR / AR identities, mandatory Epic / Feature / Story entities, or significant expansion of `change.yaml`.

The main risk is introducing too much terminology. That should be controlled by treating the model as explanatory structure rather than requiring every conceptual level to appear explicitly in every change.

No known blocker prevents proceeding to detailed design of the skill and reference changes.

## Impact and major trade-offs

This change affects RigorLoop's conceptual model across several existing stages, so its impact is material.

The main benefit is stronger systematic traceability without adding more lifecycle artifacts. The main trade-off is additional terminology: RR, IR, SR, AR, Epic, Feature, Story, Task, and Milestone.

RigorLoop should expose only terminology useful in the current context:

* RR normally needs no new identifier;
* IR is represented by the approved proposal;
* SR remains the primary durable requirement identity;
* AR initially remains an allocation concept;
* Epic / Feature / Story / Task remain optional decomposition concepts;
* milestones remain valid RigorLoop delivery units.

## Decision requested

Approve the following direction:

1. Adopt RR → IR → SR → AR as RigorLoop's lightweight requirement-refinement model.
2. Treat the original incoming need as RR without introducing a mandatory RR artifact.
3. Treat the approved proposal as the durable IR-level clarification of that need.
4. Treat specification requirements as the primary SR-level behavioral contract.
5. Treat architecture as the realization layer for SRs rather than another requirement level.
6. Treat AR initially as an allocation concept represented through existing architecture and planning artifacts rather than as a mandatory new entity.
7. Treat Epic → Feature → Story → Task as a separate, proportional work-decomposition model.
8. Do not enforce a one-to-one mapping between requirement-refinement levels and work-decomposition levels.
9. Strengthen conceptual traceability from original need → proposal → SR → architecture → allocated work → implementation → evidence.
10. Implement the model first through shared references, skill guidance, templates, examples, and review criteria rather than new lifecycle state.
11. Leave concrete lifecycle consequences—including removal of `test-spec`, redistribution of verification responsibilities, or new machine-readable traceability—to separately owned proposals.

> **Approval establishes the conceptual requirement-to-delivery model for RigorLoop; it does not approve new RR/IR/AR artifacts, mandatory Epic/Feature/Story entities, removal of existing lifecycle artifacts, or a detailed traceability implementation.**
