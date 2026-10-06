<!-- Generated from rem/methods/architecture-views.md; source SHA-256 c1ecd50c2f56d5ce5f7d7f054aa6fe81b197cfa77da335decd043d92f830b215. Edit the owning REM source. -->

# 4+1 Architecture View method

Use this method to generate complementary architecture views from authoritative REM engineering knowledge after enough Architecture Design information exists to support meaningful projection.
The method preserves the classic 4+1 names: **Logical**, **Process**, **Development**, **Physical**, and **Scenario**.

The [Architecture Design model](rem-models-architecture-design.md) owns Module, Interface, allocation, state/data-ownership, and physical/software-realization semantics.
The [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md) owns Scenario identity, lifecycle, and black-box stakeholder meaning.
This method does not create a second authoritative architecture model; the 4+1 Architecture View Graph is a derived, replaceable read model.


## Focused guidance

- [Knowledge, projection, and presentation](rem-methods-view-presentation.md)
- [Logical View](rem-methods-views-logical.md)
- [Process View](rem-methods-views-process.md)
- [Development View](rem-methods-views-development.md)
- [Physical View](rem-methods-views-physical.md)
- [Scenario View (+1)](rem-methods-views-scenario.md)

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
The [Logical reading perspectives](rem-methods-views-logical.md#logical-reading-perspectives) are optional REM guidance for organizing comprehension within one view, not a subdivision prescribed by Kruchten's paper.

### Viewpoint and model-kind basis

REM treats each 4+1 view as a concern-oriented architecture projection rather than as one mandatory diagram notation. This is consistent with ISO/IEC/IEEE 42010:2022, which distinguishes architecture viewpoints and model kinds and does not prescribe one notation or tool for an architecture description. See the [ISO standard entry](https://www.iso.org/standard/74393.html).

For Process View behavioral drill-downs, REM uses established modeling semantics where they fit the concern rather than inventing diagram meaning. UML 2.5.1 standardizes Interactions, State Machines, and Activities as distinct behavioral formalisms; see the [OMG UML 2.5.1 specification](https://www.omg.org/spec/UML/2.5.1/About-UML/). For concurrency requiring formal analysis beyond descriptive architecture, high-level Petri nets provide a standardized formal technique for concurrent discrete-event systems; see [ISO/IEC 15909-1:2019](https://www.iso.org/standard/67235.html).

These references supply a scientific and standards-based foundation for model-kind selection. REM still owns the semantic correspondence to its Modules, Interfaces, runtime realization, provenance, and generated-view rules; adopting a notation does not transfer architecture authority to the diagram.

## View selection and tailoring

Identify the reader, declared architecture scope and questions before selecting presentations.
Use Logical, Process, Development, Physical and Scenario as the standard concern vocabulary; select views that expose the material concerns in that scope.
For each selected view, state the question answered and its authoritative sources.
Record an omitted or combined view's reason and where any applicable concern is covered, using the owning design's existing explanation or a small selection table.
An additional view may address a named concern when its source meaning and relationship to the standard views are explicit.

Tailoring does not waive a requirement, hide a missing architectural fact or remove a project-required artifact.
An unknown concern remains a gap; it is not a justified omission.
A combined view must preserve the distinctions between logical responsibility, source organization, execution and placement.
For example, a small library may combine Logical and Development explanations and describe its execution and placement assumptions in prose; a distributed service still needs coverage of material concurrency, failure and deployment concerns.

[Kruchten's tailoring discussion](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S11.md) supports omission and combination of unhelpful presentations.
REM's explicit coverage rationale, authoritative-source rules and permission boundaries remain local method decisions.
The [worked example](https://github.com/xiongxianfei/rigorloop/blob/main/rem/practices/engineer-change/WORKED-EXAMPLE.md#design-and-selected-views) demonstrates a selection without inventing additional architecture.

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

1. Select the intended readers, architectural concerns, in-scope engineering state, and reading or traversal tasks. Apply [view selection and tailoring](#view-selection-and-tailoring) and record the coverage rationale.
2. Resolve the applicable authoritative information and validate its identities, containment, compatible references, and interpretation.
3. Derive the selected semantic projection, preserving exact responsibility, provenance, and recorded scope limits.
4. Render the projection using a presentation appropriate to the intended reading environment.
5. Assess semantic fidelity against the authoritative inputs: selection, collapsed boundaries, allocations, Interface direction and ownership, and source qualifications must retain their meaning.
6. Exercise the intended reading and navigation tasks in the actual presentation, using the [readability criteria](rem-methods-view-presentation.md#rendered-readability-and-navigation).
7. Return findings to their [responsible owner](rem-methods-view-presentation.md#correction-ownership), regenerate affected outputs, and reassess the changed scope.
8. Make the assessed output available under the project's generation and refresh contract, retaining its source identity, assessment context, and remaining limits.

The cycle applies to the view's declared purpose and audience.
Structural validation, projection assessment, and rendered usability assessment answer distinct questions; success in one does not establish the others.
Architectural adequacy remains an engineering judgment against the applicable obligations and Scenarios.

## View completeness

The views need not contain equal amounts of information.
A library may have a rich Logical and Development View but minimal Process or Physical views.
A distributed service may require rich Process and Physical views.

A view is sufficient when it exposes the architecture-significant information applicable to its concern and any material absence or deferral is explicit.
Apply the [selection and tailoring procedure](#view-selection-and-tailoring) to record omission, combination or additional presentations and their concern coverage; no separate profile or tailoring artifact is required.

## Completion criteria

The selected architecture presentations are sufficient for a declared scope when their selection rationale accounts for applicable concerns and:

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

These criteria describe concern coverage; an omitted or combined presentation uses the explicit rationale above rather than leaving an applicable criterion unanswered.

The 4+1 views support architecture comprehension and review.
They do not approve a baseline, implement the system, or provide evidence that requirements are satisfied.
