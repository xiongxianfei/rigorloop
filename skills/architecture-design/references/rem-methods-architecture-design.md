<!-- Generated from rem/methods/architecture-design.md; source SHA-256 41b33b8b828e5918283cf7b7932a365417ffef493bd812ec4ab64d1e0b4a1e71. Edit the owning REM source. -->

# Architecture Design method

Use responsibility-based decomposition to assign logical behavior and allocated obligations to coherent architectural boundaries.
The [Architecture Design model](rem-models-architecture-design.md) owns Module, Interface, and allocation semantics; the [requirement model](rem-models-requirements.md) owns SR-to-AR derivation and containment.
The method is tool-independent at the REM level: it does not mandate a particular language, source layout, runtime, datastore, deployment platform, or protocol.
A concrete architecture may nevertheless select such technologies when the choice is material to the system's physical/software realization.


## Focused guidance

- [Design the physical/software realization](rem-methods-realization-design.md)

## Inputs and intended result

Start with the current IRs, SRs, Features, Functions, governed Scenarios, applicable constraints, and attributable existing architecture or implementation information.
Identify whether the work describes existing architecture, proposes target architecture, or changes an established boundary.
Existing implementation is evidence about what exists; it does not automatically determine the intended architecture or transfer approval to a proposal.

Produce the semantic architecture outputs defined by the [Architecture Design model](rem-models-architecture-design.md#architecture-semantic-outputs): coherent hierarchical Module responsibilities, justified Function and AR allocations, explicit Interface contracts and exposure across encapsulation boundaries, state/data ownership where material, and only the physical/software realization information needed to understand significant architectural consequences.
Record the scope of the analysis, remaining logical or realization deferrals, and the conclusions supported by review.
A bounded first example may establish only part of the architecture; it must not imply that the remaining system has been allocated or implemented.

## Examine the whole responsibility landscape

Before choosing a first example, examine all currently defined Functions and the SRs that confirm or constrain them.
For each Function, identify:

- the behavior and engineering information it concerns;
- the selected state it reads or changes and the rules that must remain true;
- the decisions, policies, or retained information for which someone must be accountable;
- the cooperation needed to produce its outputs and distinguish failure or incomplete outcomes.

Group these responsibilities into candidate top-level Modules, comparing related Functions across Features and IRs. Decompose a candidate into child Modules only when the child responsibilities refine a broader parent responsibility with meaningful ownership, policy, state, evolution, or collaboration boundaries.
Do not reproduce the Feature hierarchy or assume one Module per Function, SR, source package, organizational team, or user interface.
Shared behavior may serve several Features without acquiring several accountable owners.

An exploratory responsibility map records proposed boundaries and allocation candidates with an explicit status.
Once allocations are authored in the model, derive the map from those relationships; do not maintain a second authoritative assignment list.
Explain which decisions remain provisional instead of treating every candidate as an established Module.

## Define coherent Module boundaries

For each candidate, use the [Module definition criteria](rem-models-architecture-boundaries.md#modules) and [Module hierarchy rules](rem-models-architecture-boundaries.md#module-hierarchy-and-encapsulation) to explain its purpose, responsibilities, owned information or state, exclusions, cooperation, and relationship to any parent or child Modules.
Group behavior when it enforces closely related rules over the same authoritative information or must coordinate to maintain a meaningful invariant.
Separate responsibilities when they have distinct authority, independent policies or evolution, or a contract that readers can explain and assess.
Treat these as engineering reasons to compare alternatives, not a numeric formula for producing a fixed number of Modules or hierarchy levels. REM does not prescribe a maximum Module depth; keep decomposing only while each level expresses durable architectural responsibility rather than implementation detail.

Distinguish the Module accountable for the meaning and permitted changes of information from a Module providing retention or transport.
If both participate, identify their respective duties and the contract between them; do not call both the unrestricted owner of the same state.
If a proposed Function spans unclear boundaries, refine the boundary or the logical behavior on its merits rather than hiding the uncertainty behind shared accountability.

A parent Module must remain meaningful as an architectural boundary in its own right; do not introduce it only to make a directory or diagram easier to browse. Its children refine portions of its responsibility, and descendant allocations should roll up for comprehension rather than being copied onto the parent.

Apply the [Module naming criteria](rem-models-architecture-boundaries.md#module-names-and-identity) to the complete affected neighborhood. Read the parent and child names together, then check each name outside the tree: its definition should make the responsibility, subject, and distinction from collaborators clear. For example, repeated names such as “Engineering model storage” and “Engineering model authoring” may be clearer as “Model storage” and “Model authoring” when those names still identify the responsibility unambiguously. Do not shorten a name until its subject becomes unclear.

Before renaming, decide whether this is a wording change or a responsibility/decomposition change. For wording alone, retain stable identity and existing relationships, reconcile current references and representation labels, and regenerate affected views. If a clearer name exposes overlapping or missing responsibilities, resolve that design issue explicitly; do not move allocations or reshape the hierarchy merely to make names look consistent.
Document significant boundary choices and their basis in the authoritative definitions or their supported sources; a separate decision document is useful only when the reasoning needs it.

## Walk through a bounded Scenario set

Select a coherent IR or stakeholder capability as the first architecture example while keeping the whole responsibility landscape in view.
Use its existing governed Scenarios to check ordinary, alternative, failure, and incomplete outcomes.
For each situation, determine which Functions participate, which Module is accountable for each Function, and which responsibilities must cooperate.
Check state selection, permitted changes, identity, failure reporting, and any applicable authority or evidence constraints.

This is an architectural walkthrough using Scenario inputs, not a rewrite of the Scenario into an internal call sequence.
Keep governed Scenarios black-box and stakeholder-observable under the [Scenario model](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md).
Record internal responsibility and contract decisions in architecture.
When the walkthrough exposes missing system behavior or a new obligation, return it to System Design or Requirement Analysis and reconcile the affected definitions.

## Allocate Functions and define Interfaces

Assign an accountable Module to each Function within the declared architecture scope, following the Architecture Design model's cardinality and hierarchy rules. Prefer the lowest Module that can coherently own the complete Function; use parent allocation only when the behavior belongs to the parent boundary itself.
Leave a Function explicitly deferred when its accountable boundary is not sufficiently understood; a placeholder Module does not resolve that uncertainty.
Cooperation with another Module is expressed through a contract rather than an additional accountable allocation under REM's single-primary-owner rule.

For each architecturally important interaction, define an Interface using the [Interface definition criteria](rem-models-architecture-boundaries.md#interfaces).
Apply [consumer Scenario contract derivation](rem-methods-architecture-allocation.md#derive-a-contract-from-a-consumer-scenario) to decide reuse, refinement, or a new cohesive contract. A provider need not expose its entire responsibility through one Interface; each selected contract must explain the consumer outcome it supports and the Scenario scope that remains elsewhere.
Explain the service or exchange, inputs, outputs, applicable state and preconditions, and meaningful failure or incomplete outcomes.
Include consistency, authority, compatibility, ordering, or retry behavior where the obligations require them.
Do not invent transaction semantics, protocols, performance targets, or technology constraints merely to fill a template.
If a material guarantee remains undecided, retain that uncertainty and do not claim the dependent architectural obligation is settled.

Identify the providing and consuming Modules using the model's authoritative relationship direction.
Check that a consumer receives enough information to fulfill its responsibility and that the provider can deliver the promised outcomes.

Choose the provider by contract accountability before considering implementation location. When a parent owns the external promise, record that parent as provider and explain the contributing child behavior through its retained allocations and material realization. Check ordinary and failure outcomes across those contributions; do not infer a second provider or child consumption from implementation participation.

When an Interface is provided by a contained Module, treat it as internal to the nearest parent boundary by default. If a consumer lies outside that boundary, explicitly expose the same Interface through the parent. Continue exposure through each additional provider ancestor that the contract must cross; do not skip a boundary. Exposure retains the child provider and contract identity. If the parent genuinely owns the external contract, define a parent-provided Interface instead of disguising the child contract as parent-owned.

An Interface may be a logical in-process contract; it need not imply a network service or separately deployed component.

## Derive and allocate requirements with architectural context

Once Module responsibilities are coherent enough to make lower-level accountability meaningful, use [Architecture Allocation](rem-methods-architecture-allocation.md#derive-and-allocate-ars) to derive/refine the necessary ARs and allocate each to exactly one accountable Module. Apply the [Requirement Analysis AR rules](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md#formulate-allocated-requirements-with-architectural-context) so the result remains a real verifiable requirement rather than an allocation placeholder.

Architecture Design MUST keep the composed AR obligations consistent with their parent SR, Function allocation, Module boundaries, state/data authority, Interface guarantees, and encapsulation. Where the architecture cannot yet support a justified allocation, retain the affected SR scope as deferred and revisit the responsible Requirement or System Design decision rather than manufacturing an AR.

## Establish state and data ownership

Before selecting persistence technology, identify architecturally significant state and data and determine logical authority.
For each important information set, determine:

- which Module owns its meaning and governing invariants;
- which Module or Interface may create, modify, or retire it;
- which other Modules may read or derive from it;
- which consistency, identity, lifecycle, retention, or recovery rules are required by the governing obligations;
- which information is authoritative versus cached, replicated, indexed, or otherwise derived.

Do not infer logical ownership from the location of a database, file, cache, or current implementation type.
If two Modules appear to own unrestricted mutation of the same state, resolve the responsibility or define a deliberate coordination contract before proceeding.

## Complete material realization

Apply [Design the physical/software realization](rem-methods-realization-design.md) after logical responsibilities, Interfaces, allocation and state authority are coherent enough for the scope.
Its technology reasoning, technical model and realization facets remain part of this Architecture Design procedure.

## Generate and use the 4+1 architecture views

After enough logical and physical/software architecture exists to support useful projection, apply the [4+1 Architecture View method](rem-methods-architecture-views.md).
Generate the classic **Logical**, **Process**, **Development**, **Physical**, and **Scenario** views from the authoritative REM knowledge or from the derived **4+1 Architecture View Graph**.

Do not separately author the same architectural facts in the views.
Use the views to improve comprehension and expose missing or contradictory architecture:

- Logical: hierarchy, responsibility, allocation, encapsulation/exposure, Interface, technical-component/contract mapping, and state/data-authority gaps;
- Process: runtime, lifecycle, communication, isolation, scaling, concurrency, or failure-boundary gaps;
- Development: software organization, implementation mappings, and test organization or execution-ownership gaps;
- Physical: deployment, persistence-placement, connectivity, and external-runtime gaps;
- Scenario: end-to-end gaps revealed by tracing a governed Scenario through obligations, Functions, Modules, Interfaces, and relevant realization.

When a view exposes an architecture gap, update the authoritative Requirement, Function, Module, Interface, allocation, state/data ownership, or realization information and regenerate the affected views.
Use the Architecture Views method's [correction ownership](rem-methods-view-presentation.md#correction-ownership) for projection, presentation, and maintenance findings.

## Reconcile and review the architecture

Review the two allocation paths together:

```text
Feature → Function → Module
            SR → AR → Module ↔ Interface
```

Within the declared scope, assess whether:

1. Each Module's name, purpose, responsibilities, state authority, and exclusions agree and distinguish it from its neighbors; parent-child containment refines responsibility coherently and every parent remains meaningful in its own right.
2. Each allocated Function has accountable responsibility, justified behavior, and the inputs and contracts needed to perform it.
3. Each AR has one parent SR, a supported derivation, a responsible Module, complete seven-part analysis, and assessable acceptance criteria.
4. Function allocations and AR obligations agree without requiring artificial one-to-one pairings.
5. Interfaces connect compatible responsibilities, including the outcomes needed for Scenario failure and incomplete cases; descendant-provided Interfaces cross parent boundaries only through explicit continuous exposure.
6. The composed responsibilities address the selected SRs and Scenarios, with remaining gaps and allocation deferrals visible.
7. Stable identity, naming, typed references, authoritative relationship direction, and source attribution remain consistent.
8. Logical architecture is distinguished from its physical/software realization, and realization choices do not silently redefine Module or Interface meaning.
9. Material software-unit, runtime/process, persistence, packaging/deployment, and technology choices are recorded or explicitly deferred for the selected scope.
10. Physical realization preserves state authority, contracts, and allocation responsibilities and is traceable to the Module or Interface that owns it.
11. Target architecture is distinguished from observed implementation, retained history, and the evidence needed to claim satisfaction.

Structural validation checks representation and reference rules; engineering review checks the meaning of responsibilities, contracts, and composed obligations.
Neither a connected graph nor a valid schema establishes architectural adequacy or implementation correctness.
Capture review findings and their resolution against the reviewed model state, and expand to the remaining scope only after reconciling the first example's shared boundaries.

## Architecture outputs and completion

Architecture Design produces a coherent set of semantic outputs, not one mandatory document, directory, diagram, or serialization.
The owning [Architecture Design model](rem-models-architecture-design.md#architecture-semantic-outputs) defines the output categories and ownership.

For the declared scope, architecture review SHOULD be able to answer from authoritative information:

- What Modules exist, which Modules contain which children, what does each own, and what is explicitly outside each boundary?
- Which Module is primarily accountable for every active Function in scope, and which Modules support it?
- Which Module is accountable for every active AR in scope?
- Which architecturally significant interactions are Interfaces, who provides them, who consumes them, and which descendant contracts are intentionally exposed through parent boundaries?
- Who owns the meaning and permitted mutation of significant state/data?
- Which software structures materially realize each Module?
- Which runtime/process boundaries materially affect lifecycle, scaling, isolation, failure, concurrency, or resources?
- How is significant state physically persisted, and is that persistence authoritative, replicated, cached, or derived?
- Which packaging/deployment choices materially affect the architecture?
- Which Interface realization choices materially affect interaction behavior or guarantees?
- Which technology choices are architecturally material, why were they selected, what consequences do they impose, and when should they be revisited?
- Which logical or realization decisions are intentionally deferred?

Architecture Design is complete enough for the declared scope when:

1. Module containment in scope is acyclic, every parent/child relationship represents genuine responsibility refinement, and parent encapsulation is explicit;
2. every active Function in scope has exactly one accountable primary Module, normally the lowest coherent Module;
3. every active AR in scope is allocated to exactly one Module, normally the lowest coherent Module;
4. significant cross-Module interactions have explicit Interface contracts and descendant-provided contracts crossing parent boundaries have continuous explicit exposure;
5. significant state/data has clear logical authority and permitted mutation;
6. Module purposes, responsibilities, exclusions, dependencies, and containment relationships are mutually coherent;
7. governed Scenario walkthroughs expose no unexplained responsibility, encapsulation, or interaction gaps;
8. material software, runtime, persistence, deployment, Interface-realization, and technology decisions are recorded or explicitly deferred;
9. physical/software realization preserves rather than silently changes logical responsibilities, contracts, containment, and state authority;
10. every material technology decision is attributable to an architectural need or constraint and records enough rationale to revisit it;
11. traceability to governing Functions, SRs, ARs, and Scenarios remains intact;
12. the selected architecture presentations cover applicable Logical, Process, Development, Physical and Scenario concerns from the same authoritative architecture without semantic contradiction, with explicit omission/combination rationale under [view tailoring](rem-methods-architecture-views.md#view-selection-and-tailoring);
13. unresolved decisions are visible and do not masquerade as completed architecture.

Logical Module/Interface definitions, allocations, and state/data ownership are architecture truth.
Subordinate realization information explains how that truth is made concrete.
Authoritative knowledge includes [authored architecture explanations](rem-models-architecture-design.md#authored-architecture-explanations) with declared ownership. Derived diagrams, inventories, and topology views present that knowledge and MUST NOT become independent sources of the same facts.

## Iterate and preserve meaning

Architecture development may refine Module boundaries, Interfaces, Functions, or requirement derivation.
Reconcile current allocations and consumers together, preserving stable identity while the same asset or obligation evolves.
Use a new identity when the engineering meaning becomes a distinct asset or obligation; preserve the original allocations in retained baselines.
Do not rewrite old evidence or history to match the new target.

A reviewed architecture draft supports the next engineering decision.
It does not by itself approve a baseline, implement the system, or demonstrate requirement satisfaction.
