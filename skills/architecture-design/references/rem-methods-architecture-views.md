<!-- Generated from rem/methods/architecture-views.md; source SHA-256 d0fb214a9352a18debfefef2f30395025c48a9bf48de163a0e1864d134b71a5a. Edit the owning REM source. -->

# 4+1 Architecture View method

Use this method to generate complementary architecture views from authoritative REM engineering knowledge after enough Architecture Design information exists to support meaningful projection.
The method preserves the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.

The [Architecture Design model](rem-models-architecture-design.md) owns Module, Interface, allocation, state/data-ownership, and physical/software-realization semantics.
The [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md) owns Scenario identity, lifecycle, and black-box stakeholder meaning.
This method does not create a second authoritative architecture model; the 4+1 Architecture View Graph is a derived, replaceable read model.

## Origin and reference

REM adopts the five-view framework introduced by Philippe Kruchten in *Architectural Blueprints—The “4+1” View Model of Software Architecture*, published in *IEEE Software*, volume 12, issue 6, November 1995, pages 42–50.
See the [author-deposited manuscript](https://arxiv.org/pdf/2006.04975) and [publication DOI](https://doi.org/10.1109/52.469759). The author's manuscript was deposited in arXiv in 2020; the publication and method date from 1995.

Kruchten distinguishes Logical, Process, Development, and Physical concerns, with selected use cases or Scenarios as the `+1` perspective that helps discover, illustrate, and validate the architecture.
His Logical examples use object-oriented abstractions while allowing other forms, including data-oriented models.
REM's responsibility-based Module/Interface projection below is an explicit adaptation of that concern.

## Adoption and adaptation in REM

Keep the original framework, REM's engineering rules, and a project's presentation choices distinguishable.

| Original concern | REM interpretation and authoritative inputs |
| --- | --- |
| Logical: abstractions supporting functionality | Module responsibilities and containment, Interface contracts, allocations and state/data authority, plus technical components/contracts and their explicit realization mappings |
| Process: execution, concurrency, and synchronization | Module runtime and Interface realization information about execution boundaries, lifecycle, communication, and failure behavior |
| Development: static software organization | Module software realization, source/package mappings, material build dependencies, and test organization |
| Physical: software mapping onto hardware and distribution | Deployment and persistence realization, placement, connectivity, and significant external infrastructure |
| Scenarios (+1): selected situations that connect and assess the four views | Existing governed stakeholder Scenarios and derived architecture participation across the other views |

REM adds governed entity types, stable identities, explicit ownership and allocation, one authoritative representation of each semantic fact, provenance, and regenerable projections.
Those are REM rules; adopting 4+1 alone does not prescribe them.
REM keeps the canonical Scenario black-box and derives internal architecture participation separately; graph reachability does not establish execution order or requirement satisfaction.

A project's Operational Support selects representation, tools, and presentation resources under these rules.
Browser pages, diagrams, reading levels, labels, and navigation are presentation choices; they are neither additional 4+1 view kinds nor first-class REM entities.
The [Logical reading perspectives](#logical-reading-perspectives) are optional REM guidance for organizing comprehension within one view, not a subdivision prescribed by Kruchten's paper.

### Viewpoint and model-kind basis

REM treats each 4+1 view as a concern-oriented architecture projection rather than as one mandatory diagram notation. This is consistent with ISO/IEC/IEEE 42010:2022, which distinguishes architecture viewpoints and model kinds and does not prescribe one notation or tool for an architecture description. See the [ISO standard entry](https://www.iso.org/standard/74393.html).

For Process View behavioral drill-downs, REM uses established modeling semantics where they fit the concern rather than inventing diagram meaning. UML 2.5.1 standardizes Interactions, State Machines, and Activities as distinct behavioral formalisms; see the [OMG UML 2.5.1 specification](https://www.omg.org/spec/UML/2.5.1/About-UML/). For concurrency requiring formal analysis beyond descriptive architecture, high-level Petri nets provide a standardized formal technique for concurrent discrete-event systems; see [ISO/IEC 15909-1:2019](https://www.iso.org/standard/67235.html).

These references supply a scientific and standards-based foundation for model-kind selection. REM still owns the semantic correspondence to its Modules, Interfaces, runtime realization, provenance, and generated-view rules; adopting a notation does not transfer architecture authority to the diagram.

## Purpose

The 4+1 views help humans and agents understand one architecture from several concerns without independently maintaining several descriptions of the same facts.

```text
Authoritative REM knowledge
        │
        ▼
4+1 Architecture View Graph
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

## Knowledge, projection, and presentation

Keep three responsibilities distinct:

| Layer | Responsibility | Change owner |
| --- | --- | --- |
| Authoritative engineering knowledge | Defines requirements, behavior, architectural responsibility, contracts, and material realization information | The applicable REM engineering entity or subordinate information owner |
| Semantic projection | Selects scope, traverses typed relationships, derives inverse relationships, aggregates or collapses detail, and retains exact source ownership and provenance | The projection rules for the selected view |
| Rendered presentation | Arranges labels and diagrams and provides navigation, search, filtering, or other interaction appropriate to the reader | The presentation rules and resources |

```text
Authoritative engineering knowledge
        ↓ semantic projection
Derived view content
        ↓ presentation
Rendered view
```

These layers do not require separate files, services, or new first-class engineering entities.
The derived Architecture View Graph may support several projections, and a projection may support several presentations.
Material Module/Interface realization information belongs to the authoritative knowledge layer even when called a realization view.

Presentation choices MUST preserve the selected engineering meaning.
A change to which relationships are included or how ownership is aggregated changes the projection rules, even when implemented in a rendering tool.
Visual arrangement MUST NOT create Module containment, Interface ownership, allocation, or an execution sequence absent from the authoritative information.

### Authored explanations and generated presentations

Authoritative engineering knowledge may include structured definitions and relationships, prose, and authored interaction or lifecycle explanations. The [Architecture Design model](rem-models-architecture-design.md#authored-architecture-explanations) owns their semantic authority. Authoring a sequence in an owning design is a way to define or explain an interaction; rendering that sequence in a 4+1 view is a presentation of the same source.

```text
Owning architecture knowledge
├── Structured definitions and relationships
└── Authored interaction and lifecycle explanations
                    │
                    ▼
       Selected, attributable view content
                    │
                    ▼
        Rendered 4+1 presentations
```

Do not require a tool to invent an interaction from a dependency graph, or require every authored exchange to become a new entity or duplicate structured record. Select the authoritative explanation, retain its owner and source state, and render or reference it in the relevant view. When a presentation combines authored explanations and derived relationships, distinguish what each source establishes; a shared page does not establish an unrecorded relationship between them.

A diagram source can contain engineering semantics as well as layout instructions. A change to participants, ordering, conditions, guarantees, or outcomes belongs to the engineering owner. A change only to spacing, visual arrangement, or faithful labels belongs to presentation. Correct the source that owns the changed meaning, reconcile affected contracts, and regenerate; do not maintain a separately edited browser version of the interaction.

## Inputs

Start from the current applicable REM information:

- Features and Functions;
- SRs and ARs relevant to the architecture scope;
- governed Scenarios;
- Module definitions, containment hierarchy, and Function/AR allocations;
- Interface definitions and explicit exposure through parent Module boundaries;
- significant state/data ownership;
- material software, runtime, persistence, deployment, Interface-realization, and technology information owned by Modules or Interfaces.

Do not author view-only architecture facts to make a diagram look complete.
If a needed relationship is absent, return to the authoritative Requirement, System Design, Architecture Design, or realization information and resolve it there.

## Build the projection source

Normalize the authoritative architecture relationships into a generated **4+1 Architecture View Graph** or equivalent read model suitable for traversal and projection.
The Architecture View Graph is derived and non-authoritative; it exists specifically to support the five 4+1 architecture projections and related human/agent navigation, not to replace the broader REM engineering model.

First-class REM entities retain their stable identities.
Subordinate realization items MAY receive generated local handles for view/query purposes, but those handles do not promote them to first-class REM entities.

A generated node or relationship SHOULD retain enough provenance to identify its authoritative owner, relationship, or realization facet.

Identify the source state and scope used by each projection.
When inputs include working changes, a baseline identifier alone is insufficient to identify that state.
Use the project's [generated-view maintenance contract](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/operational-support.md#generated-view-maintenance) to identify applicable interpretation, projection rules, outputs, and relevant rendering configuration.
The contract owns reproducibility, freshness checking, and failed-refresh handling without prescribing a particular configuration-management technology.

## Generation and assessment cycle

1. Select the intended readers, architectural concerns, in-scope engineering state, and reading or traversal tasks.
2. Resolve the applicable authoritative information and validate its identities, containment, compatible references, and interpretation.
3. Derive the selected semantic projection, preserving exact responsibility, provenance, and recorded scope limits.
4. Render the projection using a presentation appropriate to the intended reading environment.
5. Assess semantic fidelity against the authoritative inputs: selection, collapsed boundaries, allocations, Interface direction and ownership, and source qualifications must retain their meaning.
6. Exercise the intended reading and navigation tasks in the actual presentation, using the [readability criteria](#rendered-readability-and-navigation).
7. Return findings to their [responsible owner](#correction-ownership), regenerate affected outputs, and reassess the changed scope.
8. Make the assessed output available under the project's generation and refresh contract, retaining its source identity, assessment context, and remaining limits.

The cycle applies to the view's declared purpose and audience.
Structural validation, projection assessment, and rendered usability assessment answer distinct questions; success in one does not establish the others.
Architectural adequacy remains an engineering judgment against the applicable obligations and Scenarios.

## Logical View

The Logical View answers:

> What architectural responsibilities and technical components exist, what contracts connect them, and how do the components realize the accountable responsibilities?

Prefer these semantic inputs:

- Feature and Function context where it helps explain capability and behavior;
- Function-to-Module primary/supporting allocation;
- AR-to-Module allocation;
- Module definitions, responsibilities, exclusions, dependencies, and significant state/data ownership;
- logical Interfaces and their providers/consumers.
- the owned technical model's component responsibilities, contracts, state/artifact authority, realization mappings and relevant technology annotations.

The Logical View SHOULD begin with the highest useful in-scope Module level so a reader can understand the major responsibility boundaries before seeing lower-level detail. Show parent Modules and the significant Interfaces visible at that level first; reveal child Modules and internal Interfaces when the reader drills into a parent. Functions, ARs, Features, and state/data ownership SHOULD be progressively disclosed only after the relevant Module context is understood.

A parent Module boundary SHOULD hide descendant-internal Interfaces by default. A descendant-provided Interface that is explicitly exposed through that parent MAY appear at the parent level while retaining the descendant provider as its authoritative owner.

Label directly parent-provided contracts as provided by that parent. Keep contract ownership distinct from child behavior and exposed child-owned contracts. Views MUST NOT infer Interface implementation by every child from containment alone.

Begin with responsibilities and contracts. Technical structure MAY then expose selected components and technology choices that explain their realization. Runtime process boundaries, deployment targets and source paths retain their Process, Physical and Development concerns; do not infer them from a component box.

A simplified Module-to-Module edge MAY be rendered for readability when it is derived from an Interface, provided the underlying Interface remains discoverable and the simplification does not change the contract meaning.

Show recorded collaboration limits beside the overview to distinguish undeveloped contracts from architectural independence. An isolated Module or a missing edge does not establish that no collaboration is needed. Summarize known gaps from their authoritative owners; do not invent Interface edges to complete the picture. Allocation and Interface counts describe modeled content and MUST NOT be presented as proof of completeness or satisfaction.

### Logical reading perspectives

A Logical presentation MAY separate or combine the following reading perspectives to answer its readers' questions while preserving the responsibility overview and progressive disclosure.
They are optional presentations of the Logical concern, not additional architecture-view kinds, owning models, mandatory pages, or mandatory diagrams.

| Reading perspective | Reader's question | Selected information |
| --- | --- | --- |
| Architecture overview | What are the major responsibilities? | Highest useful Module boundaries and significant visible Interfaces |
| Technical structure | Which components and contracts realize those responsibilities? | Owned technical model: component boundaries, meaningful dependencies, data/artifact authority, technology annotations and explicit Module/Interface mappings |
| Public capabilities | What can a participant use? | Public entry names, purposes, contracts, and attributed Function correspondence |
| Module structure | How is this responsibility divided? | Selected Module, immediate children, responsibilities, exclusions, and state/data ownership |
| Collaboration | How do these responsibilities interact? | Named Interfaces, exact providers/consumers, and declared boundary exposure |
| Interface contract | What does this interaction promise? | Operations, inputs, outputs, guarantees, failures, and compatibility |
| Behavior and requirement allocation | What behavior and obligations belong here? | Feature/Function context, accountable Modules, and direct versus descendant AR allocations |

Readers SHOULD be able to move between an entry, its relevant behavior, its accountable responsibilities, and its contracts using the recorded relationships.
These navigation paths do not imply an execution sequence or transfer responsibility to the entry's catalog owner.
Select and combine perspectives for the intended concern rather than requiring a fixed number of screens or one complete diagram.

A production responsibility and its logical artifact contract may appear here when modeled.
The technical model may show a generator as a component with an input/output contract. Its source units, build transformations and package dependencies belong in Development; runtime execution and physical placement retain their respective view concerns. Classify the relationship by the question it answers, rather than assigning every diagram containing a software component or technology name to Development.
Missing production mappings must be resolved with their authoritative owners before a view can present them as established facts.

### Public-entry navigation

When readers need to discover available public capabilities, provide a compact entry index alongside the logical responsibility overview. Expand command, procedure, or other entry groups beneath their owning boundary; expose purpose, logical correspondence, accountable responsibilities, and the detailed contract before incidental implementation detail. Keep the initial Module/Interface diagram focused on architecture.

Related public capabilities MAY share a presentation grouping or reading level.
Grouping MUST NOT establish Module containment, Interface ownership, dependency, or execution order.
A visual layer is not an architectural layer unless the authoritative model separately establishes the relevant responsibility and relationships.
An implementation chooses its actual capability categories; REM does not require any particular public product form.

Apply the [public-entry realization model](rem-models-architecture-design.md#public-entry-discoverability): observe existing names and source contracts, analyze role-qualified Function correspondence, then derive Feature and Module context from their existing relationships. Distinguish observed availability in inspected source from proposed correspondence and runtime qualification. An entry may involve responsibilities outside its catalog's containing Module; preserve those exact allocations.

Generate every inventory of the same entries from the authoritative owner record or link to that inventory. Mark missing correspondence explicitly. Common invocation behavior alone does not establish complete specialist coverage. Detailed syntax and procedures remain with their source contracts; readers should reach them through attributable links.

Validate entry identity within its owner, supported mapping roles, compatible references, source navigation, and agreement between inventories. A mapping change must refresh affected views without changing Function ownership or creating Scenario participation. Review semantic contributions against the actual contract; successful reference validation is not an adequacy judgment.

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

Separate diagrams remain parts of one coherent design. Identify where an alternate path begins, what basis it uses, and whether it returns to the main interaction, stops affected work, or leaves recovery unresolved. Splitting a diagram must not discard ordering, authority, state, or failure guarantees. Rendering tests establish presentation behavior; the [readability assessment](#rendered-readability-and-navigation) also checks whether the result explains its intended question.

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

## Development View

The Development View answers:

> How is the architecture realized in the static organization of software used for development, build, testing, and maintenance?

Prefer these semantic inputs:

- Module software realization;
- implementation/source/package mappings;
- applications, libraries, services, workers, adapters, jobs, or other software units when material;
- build/package dependencies that matter architecturally;
- concrete Interface implementation/binding relationships where useful;
- test groups and the responsibilities or contracts they assess;
- test observation boundaries, including material substitutions and their limits;
- fixtures, test helpers, selection catalogs, runners, entrypoints, and build or installed artifacts required by those groups.

The Development View MUST NOT redefine Module boundaries or parent-child containment from current package or source layout.
It shows how hierarchical logical responsibility is realized by software organization, including deliberate many-to-many mappings when they exist.
Its component names may match the Logical technical structure, but its relationships explain source units, package dependencies, builds and maintenance. A component-and-contract overview belongs to Logical; source organization is more than a filename inventory and can be designed before files exist. Keep these projections attributable to one technical design instead of maintaining competing component definitions.

Development describes intended software organization independently of implementation progress. Its design can be authored and reviewed before source files, builds or tests exist. Keep software units, material dependencies, build/resource relationships and test architecture grounded in the governing requirements and architectural decisions. Existing source mappings and observed behavior provide supporting traceability and conformance information; they do not automatically define or approve the intended design. Preserve their qualification and any divergence. A design-oriented presentation should lead with the design and rationale, with implementation references available separately; missing references do not invalidate a design, and references alone do not fill a design gap. This design/observation distinction applies across all five views.

### Test architecture

The Development View SHOULD explain the static organization of the test system when it is material to understanding or maintaining the architecture. Show coherent behavior groups and their dependencies, rather than an inventory of every test case. Make it possible to find the assessed responsibility, governing coverage contract, test sources, fixture/support sources, and execution entrypoints.

A test group **assesses** a responsibility; it does not thereby **implement** that responsibility. Keep the owner of the protected behavior, the owner of shared test execution tooling, and the owner of evidence assessment distinct. Recording tests alongside a Module's realization provides subject context without assigning all referenced fixtures, runners, or CI infrastructure to that Module. Shared dependencies should be referenced where used and described at their authoritative owner. A missing architectural allocation for execution tooling remains an explicit gap until responsibility analysis resolves it.

Record observation boundaries and material limits, including substituted dependencies and required artifacts. A direct source test, a public command test, and an installed-product test observe different boundaries. A source path, test catalog entry, or coverage mapping alone establishes neither adequate coverage nor passing execution.

Use the other concerns for complementary information: Process explains material scheduling, concurrency, isolation, timeouts and cleanup; Physical explains execution environments and infrastructure. Verification defines the assessment, Evidence records actual observations, and the resulting judgment retains its scope. Static test dependency arrows must not imply runtime order, requirement satisfaction, or an executed test result.

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

The Physical View SHOULD distinguish logical state/data authority and Module encapsulation from the physical mechanism or location that stores or deploys them.
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
                                │
                                ├── contained by → parent Module(s)
                                ↕
                             Interface
                       (internal or exposed)
                                ↓
                       relevant realization
```

The Scenario View MAY overlay relevant Logical, Process, Development, or Physical details when they help explain how the scenario is satisfied.

### Outcome walkthroughs

Organize a Scenario walkthrough around its expected outcome and its material alternative and failure outcomes. Begin with the stakeholder situation and full observable outcome, then explain the relevant obligations, accountable responsibilities, collaboration contracts and realization. Keep broad traceability available as supporting detail. An outcome with incomplete architectural explanation must remain visible.

An outcome walkthrough SHOULD make these questions answerable:

- Which existing SR or AR criteria are relevant to this outcome, and what is their analysis basis?
- Which Modules hold the selected allocations, and which Modules provide the applicable Interface contracts?
- Which recorded Process interactions or lifecycle details help explain the outcome and its failure boundaries?
- Which Development software mappings and Physical placements apply within the selected scope?
- Which test organization is relevant context, what outcome-specific coverage has actually been established, and what applicable evidence exists?
- Which connections or explanations remain unselected, incomplete or unresolved?

Operational Support MAY define a bounded reading profile selecting canonical outcomes, criteria and realization references. The profile supplies explanatory scope; it does not create requirements, allocations, execution order or assurance claims. Resolve substantive outcome text, criteria, responsibilities and realization details from their authoritative sources. Short display labels may aid navigation but must retain access to the complete canonical meaning and source attribution. Validate selected references and their scope before generating the view.

Scenario records remain stakeholder-facing. Do not embed internal architecture in them to support presentation. New guarantees, responsibilities or interactions discovered during walkthrough analysis belong with the appropriate requirement or architecture owner before the view relies on them.

Test groups selected through a responsibility or a source contract are contextual test organization. Establish an outcome-specific coverage argument before presenting them as verifying that outcome; actual execution evidence and its applicability require their separate assessment. Missing evidence in a bounded projection means none is linked there, not that no evidence exists elsewhere. Similarly, an unselected realization detail is a reading gap, not proof that the architecture lacks it.

### Participation and consistency

Reachability establishes relevant participation, not execution order. An SR or Feature may cover behavior beyond one Scenario, so a reachable Function is not automatically a step in that Scenario. Generate internal sequencing, concurrency, and placement only from sufficient authoritative architecture information. Prose-only realization may support an attributed explanation while leaving a more detailed diagram deferred.

When an allocated child participates beneath a parent-owned contract, a Scenario projection MAY show the declared ancestor contract as boundary context. Preserve the exact provider and source relationship, and keep that context separate from allocated behavior. An ancestor's `provides` relationship alone does not establish that its Interface executes in the Scenario or that every descendant realizes it.

Select Interface context for each Scenario from its declared analysis scope and actual relationships. A participating consumer's selected Interface may reveal a provider outside its ancestry; show that exact contract owner as context without inventing an executing participant. A shared ancestor or a contract selected for another Scenario is insufficient to make it applicable here. Expose relevant recorded design limits so a bounded contract contribution cannot appear to complete the entire Scenario.

Use the Scenario View to validate the other four views:

- Does every required Function have accountable architecture?
- Do the AR obligations have responsible Modules?
- Are required Module collaborations represented by Interfaces?
- Can runtime/software/deployment realization support the required outcomes?
- Are failure, incomplete, or alternative Scenario outcomes left without architectural responsibility?

Investigate a broken or unexplained path against the authoritative sources.
A missing architectural obligation, responsibility, or contract is an architecture-analysis finding; a relationship omitted or misrepresented by the projection is a projection finding.
Apply [correction ownership](#correction-ownership) and regenerate the affected view after reconciliation.

## Progressive disclosure

Human-facing views SHOULD begin with the smallest useful architectural picture and reveal detail on demand.
For hierarchical architecture, the Logical View SHOULD normally start with top-level or otherwise highest-useful parent Modules and their visible cross-boundary Interfaces. Expanding a parent reveals its child Modules and internal/exposed Interfaces; expanding a child then reveals Functions, ARs, state/data ownership, and realization.

Do not flatten the entire Module hierarchy into one first-frame graph merely because every relationship can be rendered.

The readable navigation SHOULD follow the same containment as the diagrams. Child details belong within their parent's expansion or a linked child view, rather than appearing as peer entries beside every ancestor. Navigation should first lead to readable architectural context while retaining separately accessible canonical sources.

Separate responsibility and collaboration explanations from optional full allocation and provenance inventories. An empty allocation or state section MUST describe only what the selected owner and its actual descendants establish; a leaf Module must not imply that missing obligations are allocated beneath it.

Agent-facing views SHOULD expose deterministic typed nodes, typed relationships, and provenance sufficient for traversal such as neighborhood, upstream-why, downstream-how, and Scenario participation queries.

Human and agent views SHOULD derive from the same semantic projection rules even when their presentation formats differ.

### Rendered readability and navigation

Choose a presentation tool for the intended reading environment. A browser view MAY use generated interactive diagrams and linked detail pages; a document MAY use small linked diagrams. The tool remains replaceable. Generated graph/layout source MUST derive from authoritative knowledge; when the selected input is an authored architecture explanation, render that owning source without creating a second independently maintained account of its semantics.

Show one useful responsibility level at a time. Keep public-entry catalogs, complete allocation inventories, and provenance outside the initial diagram. A reader SHOULD be able to select a Module or Interface, understand its responsibility or contract, follow its children or collaborators, and return to the previous context. Diagram simplification MUST retain discoverable exact relationship owners and recorded scope limits.

Lead visible labels with meaningful names. A diagram SHOULD explain Module responsibilities and Interface contracts without requiring readers to interpret stable identifiers. Identifiers need not appear beside every label.

A presentation MAY shorten a canonical name when the resulting label remains faithful and unambiguous within the selected view. Preserve the words needed to distinguish neighboring responsibilities and contracts; if shortening creates ambiguity, restore meaningful context. An identifier alone does not resolve unclear engineering meaning. A presentation label MUST retain its mapping to the canonical entity and MUST NOT redefine its identity, scope, ownership, or relationships.

Keep the full canonical name and stable identity available in linked details or an equivalent reference. Interactive views SHOULD also expose them on hover and keyboard focus, with detail navigation usable without hovering. When search is available, it SHOULD accept canonical names and stable identifiers as well as any shortened visible labels. Static views SHOULD provide attributable references that allow the same identity lookup without interactive controls.

Assess readability in the rendered presentation. Inspect label meaning and ambiguity, size, edge distinction, navigation, and representative narrow and wide displays. Verify that readers can understand visible names and reach full names, stable identities, and exact contract owners. Structural validity, successful generation, and complete reference links do not by themselves establish human comprehension. Retain a detailed text reference where useful, but do not require readers to traverse that inventory to understand the architectural overview.

Choose representative tasks for the declared audience and concern.
For example, a reader of a Logical view should be able to locate an accountable Module, distinguish its children from surrounding context, understand an Interface's purpose and exact provider/consumers, follow an allocation, and reach the authoritative source.
For a static document, linked sections or references may support these tasks; interactive controls are a presentation choice.
Agent-facing projections should be assessed through the declared typed traversal and provenance tasks.

Record the assessed source state, projection and presentation identity, rendered artifact or reproducible subject, reading environment, tasks exercised, observations, and unresolved limitations.
An automated navigation check establishes the behavior it exercised; the assessment must also judge whether the selected content and presentation explain the intended architectural concern.
Evidence for one artifact or reading environment does not establish usability for uninspected outputs or environments.

## Correction ownership

Investigate whether the finding originates in engineering knowledge, derivation, presentation, or maintenance before changing its owner.

| Finding | Responsible correction |
| --- | --- |
| Missing or contradictory obligation, responsibility, contract, allocation, or realization decision | Reconcile the authoritative engineering information, then regenerate dependent views |
| Incorrect selection, traversal, aggregation, source attribution, or collapsed ownership | Correct the semantic projection rules and regenerate the affected outputs |
| Overlapping labels, ambiguous visual notation, unreadable scale, or confusing navigation | Correct presentation rules or resources while preserving the engineering meaning |
| Stale, mixed, or incomplete generated output presented as current | Correct generation, freshness checking, publication, or recovery under Operational Support |

A finding may involve more than one owner.
Reconcile each affected responsibility and reassess the corrected subject.
Editing generated output alone does not provide a durable correction; make the change in its authoritative input, projection rule, presentation resource, or maintenance procedure.

## View completeness

The views need not contain equal amounts of information.
A library may have a rich Logical and Development View but minimal Process or Physical views.
A distributed service may require rich Process and Physical views.

A view is sufficient when it exposes the architecture-significant information applicable to its concern and any material absence or deferral is explicit.
Do not introduce a separate tailoring layer merely to make a sparse view optional; applicability follows from the architecture itself.

## Completion criteria

The 4+1 view set is sufficiently generated for a declared architecture scope when:

- the Logical View explains the Module hierarchy from the highest useful level, primary responsibilities, allocations, encapsulation/exposure, significant Interfaces, and state/data authority;
- the Process View exposes material runtime/execution concerns where applicable, using a stable Runtime Topology Graph for whole-system orientation when needed and selecting focused behavioral/formal explanations by scope and authoritative semantics;
- the Development View maps material software and test organization back to the logical architecture, preserving assessed subjects and execution ownership;
- the Physical View exposes material deployment/persistence placement where applicable;
- important confirmed Scenarios have Scenario Views that trace through relevant obligations, behavior, architecture, and realization;
- displayed relationships preserve authoritative REM meaning and provenance;
- intended reading or traversal tasks have been exercised and assessed in the actual presentation, with evidence identifying the inspected subject, environment, and limitations;
- findings that prevent faithful interpretation or the declared reading tasks have been resolved with the responsible knowledge, projection, presentation, or maintenance owner;
- material unmodeled engineering scope and other remaining limitations stay explicit;
- derived views remain replaceable and regenerable, and their source state, generation rules, and freshness are identifiable under the project's maintenance contract.

The 4+1 views support architecture comprehension and review.
They do not approve a baseline, implement the system, or provide evidence that requirements are satisfied.
