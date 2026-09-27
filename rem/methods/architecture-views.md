# 4+1 Architecture View method

Use this method to generate complementary architecture views from authoritative REM engineering knowledge after enough Architecture Design information exists to support meaningful projection.
The method preserves the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.

The [Architecture Design model](../models/architecture-design.md) owns Module, Interface, allocation, state/data-ownership, and physical/software-realization semantics.
The [Scenario model](../models/scenarios.md) owns Scenario identity, lifecycle, and black-box stakeholder meaning.
This method does not create a second architecture model.

## Purpose

The 4+1 views help humans and agents understand one architecture from several concerns without independently maintaining several descriptions of the same facts.

```text
Authoritative REM knowledge
        │
        ▼
Generated semantic graph/read model
        │
        ├── Logical View
        ├── Process View
        ├── Development View
        ├── Physical View
        └── Scenario View (+1)
```

Each view selects and emphasizes relevant authoritative facts.
A view MAY collapse or omit detail for comprehension, but it MUST NOT change semantic meaning.
Every displayed fact SHOULD retain provenance back to the authoritative REM information from which it was derived.

## Inputs

Start from the current applicable REM information:

- Features and Functions;
- SRs and ARs relevant to the architecture scope;
- governed Scenarios;
- Module definitions and Function/AR allocations;
- Interface definitions;
- significant state/data ownership;
- material software, runtime, persistence, deployment, Interface-realization, and technology information owned by Modules or Interfaces.

Do not author view-only architecture facts to make a diagram look complete.
If a needed relationship is absent, return to the authoritative Requirement, System Design, Architecture Design, or realization information and resolve it there.

## Build the projection source

Normalize the authoritative REM relationships into a generated semantic graph or equivalent read model suitable for traversal and projection.
The generated graph is not an additional source of truth.

First-class REM entities retain their stable identities.
Subordinate realization items MAY receive generated local handles for view/query purposes, but those handles do not promote them to first-class REM entities.

A generated node or relationship SHOULD retain enough provenance to identify its authoritative owner, relationship, or realization facet.

Identify the source state and scope used by each projection. When inputs include working changes, a baseline identifier alone is insufficient to identify that state. The representation may retain source-content identities without imposing a particular configuration-management technology. Given the same inputs, scope, and projection rules, generated semantic content SHOULD be reproducible.

## Logical View

The Logical View answers:

> What architectural responsibilities exist, what behavior and obligations do they own, and how do they collaborate logically?

Prefer these semantic inputs:

- Feature and Function context where it helps explain capability and behavior;
- Function-to-Module primary/supporting allocation;
- AR-to-Module allocation;
- Module definitions, responsibilities, exclusions, dependencies, and significant state/data ownership;
- logical Interfaces and their providers/consumers.

The Logical View SHOULD emphasize Modules and Interfaces first and allow Functions, ARs, Features, and state/data ownership to be expanded as explanatory context.
Physical technologies, process boundaries, deployment targets, and source paths SHOULD be hidden by default unless needed to explain a logical constraint.

A simplified Module-to-Module edge MAY be rendered for readability when it is derived from an Interface, provided the underlying Interface remains discoverable and the simplification does not change the contract meaning.

## Process View

The Process View answers:

> How does the architecture behave at runtime, especially where execution boundaries, concurrency, lifecycle, communication, isolation, or failure behavior are architecturally significant?

Prefer these semantic inputs:

- Module runtime realization;
- runtime-significant Interface realization;
- execution/process boundaries;
- worker or background execution relationships;
- lifecycle, scaling, isolation, concurrency, resource, and failure-boundary information;
- runtime communication that realizes logical Interfaces.

Runtime/process items are subordinate realization information unless REM defines them elsewhere as first-class entities.
The Process View MUST preserve the owning Module/Interface relationship so readers can move from runtime structure back to logical responsibility.

Do not invent runtime detail merely to populate the view.
A library or simple system may have a minimal Process View when runtime boundaries are not architecturally material.

## Development View

The Development View answers:

> How is the architecture realized in the static organization of software used for development, build, and maintenance?

Prefer these semantic inputs:

- Module software realization;
- implementation/source/package mappings;
- applications, libraries, services, workers, adapters, jobs, or other software units when material;
- build/package dependencies that matter architecturally;
- concrete Interface implementation/binding relationships where useful.

The Development View MUST NOT redefine Module boundaries from current package or source layout.
It shows how logical responsibility is realized by software organization, including deliberate many-to-many mappings when they exist.

## Physical View

The Physical View answers:

> How is the software architecture physically packaged, placed, connected, and supported by deployment and persistence topology?

Prefer these semantic inputs:

- Module deployment realization;
- material persistence/datastore placement;
- deployment/package units and significant targets;
- material external runtime dependencies;
- placement/isolation relationships that affect architecture;
- concrete Interface connectivity where it matters to the physical topology.

The Physical View SHOULD distinguish logical state/data authority from the physical mechanism or location that stores it.
A datastore, cache, index, deployment unit, node, cluster, or device shown in this view remains subordinate realization information unless it has an independent REM identity for another reason.

## Scenario View (+1)

The Scenario View answers:

> How does the architecture participate in satisfying one governed stakeholder Scenario end-to-end?

The Scenario View MUST be anchored by an existing governed Scenario.
The authoritative Scenario remains black-box and stakeholder-observable; do not add internal Modules, Interfaces, or call sequences to the Scenario definition itself.

Generate an architecture participation slice by traversing relevant relationships such as:

```text
Scenario
    ↓ informs
SR
    ├── confirms → Function ──> Module
    └── derives  → AR ─────────> Module
                                ↕
                             Interface
                                ↓
                       relevant realization
```

The Scenario View MAY overlay relevant Logical, Process, Development, or Physical details when they help explain how the scenario is satisfied.

Reachability establishes relevant participation, not execution order. An SR or Feature may cover behavior beyond one Scenario, so a reachable Function is not automatically a step in that Scenario. Generate internal sequencing, concurrency, and placement only from sufficient authoritative architecture information. Prose-only realization may support an attributed explanation while leaving a more detailed diagram deferred.

Use the Scenario View to validate the other four views:

- Does every required Function have accountable architecture?
- Do the AR obligations have responsible Modules?
- Are required Module collaborations represented by Interfaces?
- Can runtime/software/deployment realization support the required outcomes?
- Are failure, incomplete, or alternative Scenario outcomes left without architectural responsibility?

A broken or unexplained path is an architecture-analysis finding, not something to repair only in the generated view.
Return the issue to the authoritative REM owner and regenerate the view after reconciliation.

## Progressive disclosure

Human-facing views SHOULD begin with the smallest useful architectural picture and reveal detail on demand.
For example, the Logical View may initially show only Module-to-Module interactions, then expand a Module to reveal Functions, ARs, state/data ownership, Interfaces, and realization.

Agent-facing views SHOULD expose deterministic typed nodes, typed relationships, and provenance sufficient for traversal such as neighborhood, upstream-why, downstream-how, and Scenario participation queries.

Human and agent views SHOULD derive from the same semantic projection rules even when their presentation formats differ.

## View completeness

The views need not contain equal amounts of information.
A library may have a rich Logical and Development View but minimal Process or Physical views.
A distributed service may require rich Process and Physical views.

A view is sufficient when it exposes the architecture-significant information applicable to its concern and any material absence or deferral is explicit.
Do not introduce a separate tailoring layer merely to make a sparse view optional; applicability follows from the architecture itself.

## Completion criteria

The 4+1 view set is sufficiently generated for a declared architecture scope when:

- the Logical View explains the primary Module responsibilities, allocations, significant Interfaces, and state/data authority;
- the Process View exposes material runtime/execution concerns where applicable;
- the Development View maps material software organization back to the logical architecture;
- the Physical View exposes material deployment/persistence placement where applicable;
- important confirmed Scenarios have Scenario Views that trace through relevant obligations, behavior, architecture, and realization;
- displayed relationships preserve authoritative REM meaning and provenance;
- contradictions or gaps discovered through one view are reconciled in the authoritative model rather than patched in the view;
- derived views remain replaceable and regenerable.

The 4+1 views support architecture comprehension and review.
They do not approve a baseline, implement the system, or provide evidence that requirements are satisfied.
