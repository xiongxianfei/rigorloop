<!-- Generated from rem/models/architecture-design.md; source SHA-256 b0fc82ba42194bbf28e0f61ae12d480d4c5d8cb2d0df96f271050e974103bd05. Edit the owning REM source. -->

# Architecture Design model

Architecture Design assigns accountable responsibility to Modules, defines architecturally significant interactions through Interfaces, and records the material physical/software realization needed to make that logical architecture implementable.
The [concept definitions](https://github.com/xiongxianfei/rigorloop/blob/main/rem/concepts/system-and-architecture.md#system-and-architecture-assets) explain these architectural assets and the subordinate architecture realization view.

REM keeps two coupled bodies of authoritative information:

```text
Logical architecture
  Function / AR → Module
  Module ── contains ──> Module
  Module ↔ Interface
  parent boundary ── exposes descendant Interface when required

Physical/software realization
  subordinate properties of those Modules and Interfaces
```

Modules and Interfaces remain the first-class governed architecture entities.
Physical/software realization details do not become independent REM entities by default.
The [technical model](rem-models-architecture-realization.md#technical-model) explains the selected component structure within that realization. Its structural presentation is a Logical reading perspective; Development, Process and Physical select other concerns from the same owned design.


## Focused guidance

- [Technical model](rem-models-architecture-realization.md)
- [Allocation](rem-models-architecture-allocation.md)
- [Module hierarchy and encapsulation](rem-models-architecture-boundaries.md)

## Architecture semantic outputs

Architecture Design produces semantic outputs rather than prescribing a document, directory, serialization format, or diagram.
For the declared architecture scope, the authoritative information is organized around the following concerns.

| Semantic output | Purpose | Primary owner | Expected when |
| --- | --- | --- | --- |
| Module definition | Defines accountable responsibility, purpose, owned state/data, policies, exclusions, and dependencies | Module | For every in-scope Module |
| Module containment | Defines parent-child responsibility refinement and encapsulation boundaries | Module hierarchy relationship | When a Module is decomposed into child Modules |
| Function allocation | Identifies the one accountable primary Module and any supporting Modules for logical behavior | Function relationship | For every active in-scope Function |
| AR allocation | Identifies the one Module accountable for a lower-level allocated obligation | AR relationship | For every active in-scope AR |
| Interface definition and exposure | Defines a significant logical interaction contract, provider/consumers, and any parent boundaries through which a descendant-provided contract is intentionally exposed | Interface | When cross-Module interaction is architecturally significant |
| State/data ownership | States which Module owns meaning and permitted mutation of significant information | Module | When state/data authority matters to correctness or evolution |
| Software realization | Explains the software structures that materially realize a Module | Module realization view | When software structure matters architecturally |
| Runtime realization | Explains significant execution/process topology, lifecycle, scaling, isolation, concurrency, synchronization, communication, resource, failure, ordering, retry, or recovery semantics | Module realization view | When runtime behavior or boundaries materially affect architecture |
| Persistence realization | Explains physical retention of significant state/data and whether it is authoritative, replicated, cached, or derived | Module realization view | When persistence choices materially affect architecture |
| Deployment realization | Explains significant packaging, placement, isolation, deployment target, or external runtime dependency | Module realization view | When deployment materially affects architecture |
| Interface realization | Explains material interaction mechanism, concrete binding, representation, addressing, and realization-specific guarantees | Interface realization view | When the logical contract requires a concrete architectural realization decision |
| Technology rationale | Explains a material technology selection, its driver, consequences, significant alternatives, and revisit conditions | Owning Module or Interface realization view | When the technology choice has durable architectural consequences |
| Architecture view | Presents selected authoritative information for review, such as logical, interaction, runtime, persistence, deployment, or technology perspectives | Derived | When a view improves understanding or review |

These outputs define meaning, not storage.
A project may represent them in one model, several files, a database, a modeling tool, or another controlled representation.
The representation MUST preserve the ownership and single-source-of-truth semantics above.

State/data ownership is logical authority, not a synonym for physical storage.
A persistence mechanism may retain bytes without owning their domain meaning or permitted mutation.

A realization facet is required only when omitting it would hide a material architectural consequence.
Do not create empty or speculative realization information merely for symmetry.

## Authored architecture explanations

Authoritative architecture knowledge may be represented by structured records, prose, or authored diagrams under a declared Module, Interface, or architecture-composition owner. An authored sequence may define significant exchanges and ordering; an authored lifecycle explanation may define states and permitted transitions. These are subordinate architecture information, not new first-class entities merely because they have a title or diagram.

Declare which source owns each semantic fact. An explanation that cites an existing allocation, Interface guarantee, or state rule must preserve that source's meaning rather than establish a competing definition. New or changed guarantees must be reconciled with the responsible requirement, behavior, or contract owner before dependent views rely on them. Resolve disagreement between structured and narrative sources through their declared ownership; neither format has automatic precedence.

Place a local explanation with its responsibility owner. Place a shared composition explanation with the scope accountable for that cooperation, referencing the participants' own contracts and allocations. A child view may link a parent-owned explanation without copying it or acquiring ownership. Scope labels and navigation do not establish that every child participates in every parent interaction.

Rendered diagrams and browser pages present this knowledge under the [Architecture Views method](rem-methods-view-presentation.md#authored-explanations-and-generated-presentations). Changing the rendered presentation alone does not revise the architecture. File layout, diagram syntax, and any structured representation of authored interactions remain project choices.

## Allocation consistency

For each Module, architecture review SHOULD consider together:

- its parent and child Modules, if any, and whether the decomposition refines responsibility coherently;
- Functions for which it is primary;
- Functions it supports;
- ARs allocated to it;
- state and data it owns;
- policies it must enforce;
- Interfaces it provides or consumes;
- descendant Interfaces it exposes through its boundary.

An unexplained missing responsibility, conflicting owner, encapsulation bypass, skipped exposure boundary, or incompatible Interface is a design issue even when a diagram can be rendered.

Use [Architecture Allocation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/architecture-allocation.md) to assign and reconcile these responsibilities.

## Generated 4+1 architecture views

REM adopts five architecture-view kinds using the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.
The method distinguishes the [original 4+1 approach](rem-methods-architecture-views.md#origin-and-reference) from [REM's adoption and adaptation](rem-methods-architecture-views.md#adoption-and-adaptation-in-rem).
Under REM, these views are generated projections of authoritative engineering knowledge, not independent models or authored sources of truth.
Use the [4+1 Architecture View method](rem-methods-architecture-views.md) to construct them; the mappings below describe REM's application.
Apply its [selection and tailoring procedure](rem-methods-architecture-views.md#view-selection-and-tailoring) to record justified omissions, combinations or additional presentations while retaining applicable concern coverage and project obligations.

| View | Primary concern | Typical authoritative inputs |
| --- | --- | --- |
| Logical | Hierarchical responsibilities, contracts and technical component structure, with explicit realization mappings | Module containment, Interfaces, Feature/Function context, Function/AR allocation, state/data ownership and the owned technical model |
| Process | Runtime topology plus concern-specific interaction, lifecycle, control-flow, timing, or formal-concurrency projections | Module runtime realization and runtime-significant Interface realization; authoritative ordering/state/timing facts where applicable |
| Development | Static software organization used for development/build/testing/maintenance | Module software realization, source/package mappings, material dependencies, test groups and supporting infrastructure |
| Physical | Deployment, placement, connectivity, persistence placement, and infrastructure topology | Module deployment/persistence realization, external runtime dependencies, concrete connectivity |
| Scenario | End-to-end architecture participation for one governed stakeholder Scenario | Scenario → SR/Function/AR → Module/Interface plus relevant realization |

The optional [Logical reading perspectives](rem-methods-views-logical.md#logical-reading-perspectives) organize questions within the Logical View. They do not add architecture-view kinds or require separate pages; each project selects its presentation under Operational Support.

A view MAY simplify presentation, for example by collapsing an Interface into a labeled Module-to-Module edge, provided the underlying Interface and authoritative relationship remain discoverable.
A view MUST NOT invent or independently maintain architecture facts.

The Scenario View is the `+1` cross-view validation slice.
The canonical Scenario remains black-box and stakeholder-observable; the generated view derives internal architecture participation without adding those internal steps to the Scenario definition.
Its [outcome walkthroughs](rem-methods-views-scenario.md#outcome-walkthroughs) connect expected, alternative and failure outcomes to selected existing obligations and source-backed architecture details. Reading selections, established coverage and applicable execution evidence remain distinct.
Important Scenarios SHOULD be used to test whether the other four views form a coherent end-to-end explanation of the architecture.

A generated **4+1 Architecture View Graph** MAY normalize authoritative REM entities, Module containment, Interface exposure, allocation relationships, and subordinate realization information for projection. It is a derived, non-authoritative architecture read model, not a general replacement for the REM engineering model.
Generated realization nodes may use local handles for deterministic traversal, but such handles do not create new first-class REM entities.
Generated nodes and edges SHOULD retain provenance to the authoritative REM owner from which they were derived. Logical projections SHOULD begin at the highest useful in-scope Module level and reveal contained Modules, internal Interfaces, Functions, ARs, and state/data authority progressively.
