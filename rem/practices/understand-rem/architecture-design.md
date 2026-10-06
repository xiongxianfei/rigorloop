# 4. Architecture Design

## 4. Architecture Design

REM Architecture Design is built from the [Module, Interface, and architecture-realization concepts](../../concepts/system-and-architecture.md#system-and-architecture-assets), the allocation and logical/physical separation [Principles](../../principles/README.md), the [Architecture Design model](../../models/architecture-design.md), and the [Architecture Allocation](../../methods/architecture-allocation.md) and [Architecture Design](../../methods/architecture-design.md) methods.

Architecture has two coupled semantic layers:

```text
Logical architecture
  Function ── primaryModule ──> Module
  AR ──────── allocatedTo ────> Module
  Module ───── contains ───────> Module
                                   ↕
                                Interface
  parent boundary ── exposes descendant Interface when required
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
The Module owns architectural responsibility and significant state/data authority. A parent Module may contain child Modules that refine that responsibility; the parent remains a real encapsulation boundary rather than a visual group. Function and AR allocation normally target the lowest coherent accountable Module, while parent roll-up is derived.
The Interface owns a significant logical interaction contract. A descendant-provided Interface remains internal to its containing Module boundary unless explicitly exposed through that boundary and any additional provider ancestors it must cross.
Subordinate realization information explains how those responsibilities and contracts are concretely realized without introducing new universal entity classes.
The [technical model](../../models/architecture-realization.md#technical-model) organizes the intended implementation into components, responsibilities, contracts, data/artifact authority and technology decisions. Technical structure is a Logical reading perspective with explicit mappings back to accountable Modules and Interfaces. Development selects source/package/build organization, Process selects execution, and Physical selects placement from that same owned design. A component does not become a Module or a process merely because it is drawn as a box.

For the Process View, REM uses a stable runtime-topology projection for whole-system orientation when material, and selects Sequence/Interaction, State Machine, Activity/Control-flow, Timing, or formal-concurrency explanations according to the concern and scope when the corresponding authoritative semantics exist. A focused Module interaction need not add a topology diagram solely for symmetry. The [4+1 Architecture View method](../../methods/views/process.md#process-view) owns those selection rules and explicitly forbids deriving execution order from logical graph reachability.

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

The [Architecture Design model](../../models/architecture-design.md#architecture-semantic-outputs) defines semantic outputs rather than filenames or documents.
These include Module definitions and containment, Function and AR allocations, Interface definitions and exposure across parent boundaries, significant state/data ownership, and material software/runtime/persistence/deployment/Interface-realization/technology information where relevant.
Authoritative knowledge may include [authored architecture explanations](../../models/architecture-design.md#authored-architecture-explanations) as well as structured relationships. Derived logical, runtime, datastore, deployment, or technology views render or project those sources for comprehension without acquiring ownership of the underlying facts. Current applicable rationale stays with the engineering owner; judgments and execution history remain [operational records](../../models/operational-support.md#engineering-knowledge-and-operational-records).

[Requirement Analysis](../../methods/requirement-analysis.md#formulate-allocated-requirements-with-architectural-context) defines the requirement-quality rules for AR obligations; [Architecture Allocation](../../methods/architecture-allocation.md#derive-and-allocate-ars) supplies the architectural context in which they are derived/refined and allocated.
[Architecture Allocation](../../methods/architecture-allocation.md) establishes Module containment, logical Function/AR responsibility, Interface contracts, and required exposure through encapsulation boundaries.
[Architecture Design](../../methods/architecture-design.md) completes state/data ownership, material physical/software realization, architecture review, and completion assessment without prescribing a storage format.
[4+1 Architecture Views](../../methods/architecture-views.md) then generates Logical, Process, Development, Physical, and Scenario projections from the same authoritative REM knowledge for comprehension and cross-view validation.

To understand this choice, distinguish the [original 4+1 approach](../../methods/architecture-views.md#origin-and-reference), [REM's adoption and adaptation](../../methods/architecture-views.md#adoption-and-adaptation-in-rem), and a project's presentation of those views. The method owns that distinction. Its six optional [Logical reading perspectives](../../methods/views/logical.md#logical-reading-perspectives) help organize questions within one view; they are neither additional standard 4+1 views nor a prescribed set of pages. A repository's diagrams and navigation remain presentation choices rather than the origin of REM's architecture semantics.

---
