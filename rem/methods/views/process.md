# Process View

## Process View

The Process View answers:

> How does the architecture execute, communicate, coordinate, change runtime state, and fail where those concerns are architecturally significant?

Prefer these semantic inputs:

- Module runtime realization;
- runtime-significant Interface realization;
- execution/process boundaries and architecturally significant tasks/workers;
- lifecycle, scaling, isolation, concurrency, resource, synchronization, and failure-boundary information;
- runtime communication that realizes logical Interfaces;
- authoritative ordering, state-transition, timing, retry, transaction, or recovery information when explicitly modeled.

Runtime/process items are subordinate realization information unless REM defines them elsewhere as first-class entities. The Process View MUST preserve the owning Module/Interface relationship and Module containment context so readers can move from runtime structure back to logical responsibility and understand which runtime interactions cross encapsulation boundaries.

### Primary model kind — Runtime Topology Graph

Use a **Runtime Topology Graph** as the primary whole-system Process projection whenever runtime concerns are material. It is a typed directed graph of architecturally significant runtime participants/resources and their declared runtime communication relationships.

Typical generated participant kinds include process, task/worker, external runtime, and runtime resource. These are realization projections, not new first-class REM entities. Each participant SHOULD retain its owning Module realization and, where material, its runtime kind, multiplicity, lifecycle, concurrency/isolation role, and failure boundary.

Typical communication-edge kinds include synchronous call, asynchronous message/event, stream, shared-state access, or another explicitly modeled runtime channel. Each edge SHOULD retain direction, its owning or realized logical Interface when applicable, and material synchronization, delivery, ordering, or failure semantics.

A topology edge states a runtime communication relationship. It MUST NOT, by itself, assert that one participant executes before another.

### Conditional Process model kinds

Select additional model kinds by the runtime concern that needs explanation. Do not use a diagram merely because a rendering tool supports it.

| Runtime question | Preferred model kind | Selection rule |
| --- | --- | --- |
| What executes independently and how do runtime participants communicate? | Runtime Topology Graph | Primary Process projection when runtime architecture is material |
| In what established causal/order sequence do participants interact for a selected runtime operation? | Sequence/Interaction Diagram | Use only when authoritative runtime information establishes the participants and relevant ordering/messages |
| What lifecycle states and transitions govern a runtime participant or resource? | State Machine | Use when durable runtime state/transition semantics are architecturally material |
| How does control or data branch, merge, fork, and join across activities? | Activity/Control-flow Diagram | Use when control-flow or parallel-flow structure is material and cannot be understood from topology/interaction alone |
| What timing relationships or deadlines materially constrain execution? | Timing model/diagram | Use when timing semantics are explicit architecture constraints |
| Can synchronization, reachability, boundedness, deadlock, or liveness require formal concurrency analysis? | Formal concurrency model such as a Petri net | Use only when the analytical question and available semantics justify formal modeling |

UML-style Sequence, State Machine, and Activity notations are useful standard presentations for the corresponding model kinds, but REM does not mandate UML, Mermaid, PlantUML, Graphviz, or another renderer. A project MAY use any notation that preserves the selected model-kind semantics and provenance.

### Readable behavioral explanations

Give each diagram a clear question and declared scope. Use a sequence to explain who exchanges what and in which established order, an activity/control-flow diagram to explain decisions and branching, and a state machine to explain allowed lifecycle transitions. Do not choose a flowchart merely to avoid unfamiliar sequence notation when participant cooperation is the concern.

For a sequence or interaction explanation:

- Name actual roles or architectural participants and make their responsibilities clear. Relate them to owning Modules and significant Interface contracts where applicable; do not equate a role with a process or assign ownership through visual placement.
- Use concrete messages that identify the request, result, information, or decision exchanged. Make meaningful ordering and preconditions explicit without inventing timing or delivery guarantees.
- Keep the main path focused. A substantial correction, retry, or recovery interaction may have its own linked diagram with an explicit trigger and outcome; do not turn every conditional step into another diagram.
- Use ordinary language for conditions. Combined fragments or other formal notation are appropriate when they clarify material semantics, but readers should not need unexplained notation to follow routine cooperation.
- Keep material failures, alternatives, concurrency, and uncertain outcomes discoverable in the diagram or adjacent owning explanation. A simple success sequence must not imply that every attempt succeeds or that omitted paths are impossible.

Separate diagrams remain parts of one coherent design. Identify where an alternate path begins, what basis it uses, and whether it returns to the main interaction, stops affected work, or leaves recovery unresolved. Splitting a diagram must not discard ordering, authority, state, or failure guarantees. Rendering tests establish presentation behavior; the [readability assessment](../view-presentation.md#rendered-readability-and-navigation) also checks whether the result explains its intended question.

### Process drill-down and Scenario separation

At whole-system scope, the primary Process presentation SHOULD remain a stable runtime topology when execution boundaries and communication are material. A reader MAY select a runtime participant, channel, or operation and drill down to the applicable Sequence, State Machine, Activity, timing, or formal-concurrency projection. This progressive structure keeps detailed explanations connected to the architecture they explain.

At a Module or selected-operation scope, lead with the model kind that answers the reader's actual question. A focused interaction may be the useful first presentation; it does not require an additional topology diagram solely to fill the page. Identify the containing responsibility and relevant collaborators, and retain access to material wider topology where it exists. Roles, logical responsibilities, and independently executing processes must remain distinguishable; drawing a participant does not create a deployed service. Missing runtime facts remain explicit rather than being inferred from a role or Module name.

A Process interaction diagram explains runtime mechanics. The Scenario View starts from a governed stakeholder-observable Scenario and traces its architecture participation across obligations, Functions, Modules, Interfaces, and relevant realization. A Scenario View MAY select a Process interaction projection as supporting runtime detail, but that interaction does not become part of the canonical black-box Scenario.

### Semantic safeguards

The Process projection MUST NOT infer:

- execution order from Logical Module/Interface reachability;
- synchronous behavior merely because one Module consumes an Interface;
- concurrency merely because two Functions are independent in the logical graph;
- transaction, retry, persistence, or recovery semantics from implementation names;
- deployment placement from process membership unless Physical realization establishes it.

When the authoritative model establishes only runtime topology, render only topology. When ordering, lifecycle, control-flow, timing, or formal concurrency semantics are absent, mark that detail as unknown/deferred rather than manufacturing a more complete behavioral diagram.

Do not invent runtime detail merely to populate the view. A library or simple system may have a minimal Process View when runtime boundaries are not architecturally material.
