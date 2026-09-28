# 4+1 Architecture View method

Use this method to generate complementary architecture views from authoritative REM engineering knowledge after enough Architecture Design information exists to support meaningful projection.
The method preserves the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.

The [Architecture Design model](../models/architecture-design.md) owns Module, Interface, allocation, state/data-ownership, and physical/software-realization semantics.
The [Scenario model](../models/scenarios.md) owns Scenario identity, lifecycle, and black-box stakeholder meaning.
This method does not create a second authoritative architecture model; the 4+1 Architecture View Graph is a derived, replaceable read model.

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
Use the project's [generated-view maintenance contract](../models/operational-support.md#generated-view-maintenance) to identify applicable interpretation, projection rules, outputs, and relevant rendering configuration.
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

> What architectural responsibilities exist, what behavior and obligations do they own, and how do they collaborate logically?

Prefer these semantic inputs:

- Feature and Function context where it helps explain capability and behavior;
- Function-to-Module primary/supporting allocation;
- AR-to-Module allocation;
- Module definitions, responsibilities, exclusions, dependencies, and significant state/data ownership;
- logical Interfaces and their providers/consumers.

The Logical View SHOULD begin with the highest useful in-scope Module level so a reader can understand the major responsibility boundaries before seeing lower-level detail. Show parent Modules and the significant Interfaces visible at that level first; reveal child Modules and internal Interfaces when the reader drills into a parent. Functions, ARs, Features, and state/data ownership SHOULD be progressively disclosed only after the relevant Module context is understood.

A parent Module boundary SHOULD hide descendant-internal Interfaces by default. A descendant-provided Interface that is explicitly exposed through that parent MAY appear at the parent level while retaining the descendant provider as its authoritative owner.

Label directly parent-provided contracts as provided by that parent. Keep contract ownership distinct from child behavior and exposed child-owned contracts. Views MUST NOT infer Interface implementation by every child from containment alone.

Physical technologies, process boundaries, deployment targets, and source paths SHOULD be hidden by default unless needed to explain a logical constraint.

A simplified Module-to-Module edge MAY be rendered for readability when it is derived from an Interface, provided the underlying Interface remains discoverable and the simplification does not change the contract meaning.

Show recorded collaboration limits beside the overview to distinguish undeveloped contracts from architectural independence. An isolated Module or a missing edge does not establish that no collaboration is needed. Summarize known gaps from their authoritative owners; do not invent Interface edges to complete the picture. Allocation and Interface counts describe modeled content and MUST NOT be presented as proof of completeness or satisfaction.

### Public-entry navigation

When readers need to discover available public capabilities, provide a compact entry index alongside the logical responsibility overview. Expand command, procedure, or other entry groups beneath their owning boundary; expose purpose, logical correspondence, accountable responsibilities, and the detailed contract before incidental implementation detail. Keep the initial Module/Interface diagram focused on architecture.

Apply the [public-entry realization model](../models/architecture-design.md#public-entry-discoverability): observe existing names and source contracts, analyze role-qualified Function correspondence, then derive Feature and Module context from their existing relationships. Distinguish observed availability in inspected source from proposed correspondence and runtime qualification. An entry may involve responsibilities outside its catalog's containing Module; preserve those exact allocations.

Generate every inventory of the same entries from the authoritative owner record or link to that inventory. Mark missing correspondence explicitly. Common invocation behavior alone does not establish complete specialist coverage. Detailed syntax and procedures remain with their source contracts; readers should reach them through attributable links.

Validate entry identity within its owner, supported mapping roles, compatible references, source navigation, and agreement between inventories. A mapping change must refresh affected views without changing Function ownership or creating Scenario participation. Review semantic contributions against the actual contract; successful reference validation is not an adequacy judgment.

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
The Process View MUST preserve the owning Module/Interface relationship and Module containment context so readers can move from runtime structure back to logical responsibility and understand which runtime interactions cross encapsulation boundaries.

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

The Development View MUST NOT redefine Module boundaries or parent-child containment from current package or source layout.
It shows how hierarchical logical responsibility is realized by software organization, including deliberate many-to-many mappings when they exist.

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

Choose a presentation tool for the intended reading environment. A browser view MAY use generated interactive diagrams and linked detail pages; a document MAY use small linked diagrams. The tool remains replaceable, and its graph/layout source MUST derive from the authoritative model rather than become a second authored architecture.

Show one useful responsibility level at a time. Keep public-entry catalogs, complete allocation inventories, and provenance outside the initial diagram. A reader SHOULD be able to select a Module or Interface, understand its responsibility or contract, follow its children or collaborators, and return to the previous context. Diagram simplification MUST retain discoverable exact relationship owners and recorded scope limits.

Assess readability in the rendered presentation. Inspect label size, edge distinction, navigation, and representative narrow and wide displays. Structural validity, successful generation, and complete reference links do not by themselves establish human comprehension. Retain a detailed text reference where useful, but do not require readers to traverse that inventory to understand the architectural overview.

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
- the Process View exposes material runtime/execution concerns where applicable;
- the Development View maps material software organization back to the logical architecture;
- the Physical View exposes material deployment/persistence placement where applicable;
- important confirmed Scenarios have Scenario Views that trace through relevant obligations, behavior, architecture, and realization;
- displayed relationships preserve authoritative REM meaning and provenance;
- intended reading or traversal tasks have been exercised and assessed in the actual presentation, with evidence identifying the inspected subject, environment, and limitations;
- findings that prevent faithful interpretation or the declared reading tasks have been resolved with the responsible knowledge, projection, presentation, or maintenance owner;
- material unmodeled engineering scope and other remaining limitations stay explicit;
- derived views remain replaceable and regenerable, and their source state, generation rules, and freshness are identifiable under the project's maintenance contract.

The 4+1 views support architecture comprehension and review.
They do not approve a baseline, implement the system, or provide evidence that requirements are satisfied.
