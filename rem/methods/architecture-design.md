# Architecture Design method

Use responsibility-based decomposition to assign logical behavior and allocated obligations to coherent architectural boundaries.
The [Architecture Design model](../models/architecture-design.md) owns Module, Interface, and allocation semantics; the [requirement model](../models/requirements.md) owns SR-to-AR derivation and containment.
The method is tool-independent at the REM level: it does not mandate a particular language, source layout, runtime, datastore, deployment platform, or protocol.
A concrete architecture may nevertheless select such technologies when the choice is material to the system's physical/software realization.

## Inputs and intended result

Start with the current IRs, SRs, Features, Functions, governed Scenarios, applicable constraints, and attributable existing architecture or implementation information.
Identify whether the work describes existing architecture, proposes target architecture, or changes an established boundary.
Existing implementation is evidence about what exists; it does not automatically determine the intended architecture or transfer approval to a proposal.

Produce the semantic architecture outputs defined by the [Architecture Design model](../models/architecture-design.md#architecture-semantic-outputs): coherent Module responsibilities, justified Function and AR allocations, explicit Interface contracts, state/data ownership where material, and only the physical/software realization information needed to understand significant architectural consequences.
Record the scope of the analysis, remaining logical or realization deferrals, and the conclusions supported by review.
A bounded first example may establish only part of the architecture; it must not imply that the remaining system has been allocated or implemented.

## Examine the whole responsibility landscape

Before choosing a first example, examine all currently defined Functions and the SRs that confirm or constrain them.
For each Function, identify:

- the behavior and engineering information it concerns;
- the selected state it reads or changes and the rules that must remain true;
- the decisions, policies, or retained information for which someone must be accountable;
- the cooperation needed to produce its outputs and distinguish failure or incomplete outcomes.

Group these responsibilities into candidate Modules, comparing related Functions across Features and IRs.
Do not reproduce the Feature hierarchy or assume one Module per Function, SR, source package, or user interface.
Shared behavior may serve several Features without acquiring several accountable owners.

An exploratory responsibility map records proposed boundaries and allocation candidates with an explicit status.
Once allocations are authored in the model, derive the map from those relationships; do not maintain a second authoritative assignment list.
Explain which decisions remain provisional instead of treating every candidate as an established Module.

## Define coherent Module boundaries

For each candidate, use the [Module definition criteria](../models/architecture-design.md#modules) to explain its purpose, responsibilities, owned information or state, exclusions, and cooperation.
Group behavior when it enforces closely related rules over the same authoritative information or must coordinate to maintain a meaningful invariant.
Separate responsibilities when they have distinct authority, independent policies or evolution, or a contract that readers can explain and assess.
Treat these as engineering reasons to compare alternatives, not a numeric formula for producing a fixed number of Modules.

Distinguish the Module accountable for the meaning and permitted changes of information from a Module providing retention or transport.
If both participate, identify their respective duties and the contract between them; do not call both the unrestricted owner of the same state.
If a proposed Function spans unclear boundaries, refine the boundary or the logical behavior on its merits rather than hiding the uncertainty behind shared accountability.

Name each Module for its responsibility and subject, and compare the name with neighboring Modules.
Document significant boundary choices and their basis in the authoritative definitions or their supported sources; a separate decision document is useful only when the reasoning needs it.

## Walk through a bounded Scenario set

Select a coherent IR or stakeholder capability as the first architecture example while keeping the whole responsibility landscape in view.
Use its existing governed Scenarios to check ordinary, alternative, failure, and incomplete outcomes.
For each situation, determine which Functions participate, which Module is accountable for each Function, and which responsibilities must cooperate.
Check state selection, permitted changes, identity, failure reporting, and any applicable authority or evidence constraints.

This is an architectural walkthrough using Scenario inputs, not a rewrite of the Scenario into an internal call sequence.
Keep governed Scenarios black-box and stakeholder-observable under the [Scenario model](../models/scenarios.md).
Record internal responsibility and contract decisions in architecture.
When the walkthrough exposes missing system behavior or a new obligation, return it to System Design or Requirement Analysis and reconcile the affected definitions.

## Allocate Functions and define Interfaces

Assign an accountable Module to each Function within the declared architecture scope, following the selected profile's cardinality rules.
Leave a Function explicitly deferred when its accountable boundary is not sufficiently understood; a placeholder Module does not resolve that uncertainty.
Cooperation with another Module is expressed through a contract rather than an additional accountable allocation in the single-owner profile.

For each architecturally important interaction, define an Interface using the [Interface definition criteria](../models/architecture-design.md#interfaces).
Explain the service or exchange, inputs, outputs, applicable state and preconditions, and meaningful failure or incomplete outcomes.
Include consistency, authority, compatibility, ordering, or retry behavior where the obligations require them.
Do not invent transaction semantics, protocols, performance targets, or technology constraints merely to fill a template.
If a material guarantee remains undecided, retain that uncertainty and do not claim the dependent architectural obligation is settled.

Identify the providing and consuming Modules using the model's authoritative relationship direction.
Check that a consumer receives enough information to fulfill its responsibility and that the provider can deliver the promised outcomes.
An Interface may be a logical in-process contract; it need not imply a network service or separately deployed component.

## Derive allocated requirements

For each SR in the selected architecture scope, determine the lower-level obligations needed from the responsible Modules.
Create an AR only when its accountable boundary is known well enough to state and assess that obligation.
Follow [Requirement Analysis](requirement-analysis.md#derive-allocated-requirements): retain exactly one parent SR, apply all seven [5W2H](5w2h.md) questions at the allocated level, and state observable acceptance criteria.

Explain what the Module must satisfy, under which conditions, and why that obligation follows from the parent SR and the supported architecture choice.
Distinguish a derived architectural obligation from a new system need; an AR must not silently introduce a broader unsupported product commitment.
Several independent Module obligations can produce several ARs under one SR.
An AR may concern behavior, state integrity, a policy, an interaction guarantee, or a quality constraint; do not invent a matching Function for each AR.

When an AR constrains a Function, check the Function's behavior and accountable allocation against that obligation.
If satisfying an SR requires cooperation, make the separate responsibilities and necessary Interface guarantees explicit.
Assess the composed obligations against the SR's acceptance criteria; individually plausible ARs do not establish system-level coverage.
Where obligations cannot yet be allocated, identify the deferred SR scope rather than manufacturing an AR or declaring the SR fully allocated.

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

## Design the physical/software realization

After the logical Module, Interface, allocation, and state/data-ownership model is coherent enough for the selected scope, define the material physical/software realization.
Keep these decisions subordinate to their owning Module or Interface rather than creating new universal REM entity classes.

Record a realization detail only when it is architecture-significant: it changes or explains responsibility, lifecycle, isolation, failure behavior, state authority, deployment/recovery, compatibility, a governing requirement/quality, or an important future-evolution constraint.
Leave incidental internal implementation choices to implementation.

For each Module, identify only the realization details needed to understand significant structural, runtime, persistence, deployment, or technology consequences.
Consider:

- which software units realize the Module responsibility, such as applications, services, libraries, workers, adapters, or scheduled jobs;
- which execution or process boundaries matter for lifecycle, scaling, failure isolation, security, or resource ownership;
- which persistence mechanisms or datastores realize owned or required state;
- how the software is packaged or deployed when that boundary is architecturally significant;
- which implementation paths or artifacts realize the Module when a current implementation exists;
- which technology selections materially constrain the Module and why.

For each Interface, determine whether its logical contract needs a concrete realization decision.
Where material, record:

- interaction mechanism or protocol;
- endpoint/channel/topic/file/in-process binding form;
- serialization or exchanged data representation;
- addressing/discovery assumptions;
- technology choices required for the interaction;
- realization-specific compatibility, ordering, failure, or delivery semantics required by the governing obligations.

Do not assign a global REM identity to every service, process, datastore, deployment unit, or technology.
Treat them as structured subordinate information owned by the Module or Interface unless a later REM refinement demonstrates that independent identity is required.

### Organize realization under its owner

Use the [subordinate-facet rules](../models/architecture-design.md#organizing-subordinate-facets) when organizing the selected representation.
Keep logical responsibilities, state authority, and interaction contracts in the Module and Interface definitions.
Separate software, runtime, persistence, deployment, interaction, representation, or technology information only when that separation helps readers understand material architecture.
Do not create empty records to make every owner look complete.

For existing realization, identify the source and assessed state that support each observation.
For proposed realization, explain the choice and its architectural basis without presenting it as implemented behavior.
Keep unresolved material choices explicit under their owner even when no current realization exists; a missing facet is not a completion judgment.
When moving information between representations, preserve its owner, meaning, attribution, and historical applicability, and reconcile dependent references and views.

### Choose technologies last enough to preserve reasoning

Do not start architecture by selecting products or frameworks.
First establish the logical responsibility, contract, state ownership, and runtime/deployment need.
Then select technology that satisfies those decisions and applicable requirements.

For each material technology choice, retain enough rationale to answer:

- what architectural need or constraint drives the choice;
- what significant alternatives were considered;
- what consequences or limitations the choice introduces;
- what condition would justify revisiting it.

The rationale may be stored in the owning Module or Interface realization view or in an attributable decision record when the reasoning deserves independent review.
Author that rationale once and reference it from other affected facets, including across Modules or Interfaces when a decision is shared.

### Derive physical views

Logical and dependency views derive from the authoritative definitions and relationships.
Runtime topology, datastore topology, deployment topology, and technology inventories are useful views, but they SHOULD be generated or derived from the authoritative Module and Interface realization information.
Do not create independently maintained copies of the same physical relationships.

Example:

```text
MOD-query
  logical responsibility: engineering query behavior
  realization:
    software units: query service, indexing worker
    runtime: API process + worker process
    persistence: search index
    packaging: server deployment unit
    technology: selected search/runtime technologies

IF-engineering-query
  logical contract: query engineering entities
  realization:
    mechanism: selected request/response protocol
    representation: selected request/result encoding
```

The example describes subordinate views, not new first-class REM entities.

## Reconcile and review the architecture

Review the two allocation paths together:

```text
Feature → Function → Module
            SR → AR → Module ↔ Interface
```

Within the declared scope, assess whether:

1. Each Module's name, purpose, responsibilities, state authority, and exclusions agree and distinguish it from its neighbors.
2. Each allocated Function has accountable responsibility, justified behavior, and the inputs and contracts needed to perform it.
3. Each AR has one parent SR, a supported derivation, a responsible Module, complete seven-part analysis, and assessable acceptance criteria.
4. Function allocations and AR obligations agree without requiring artificial one-to-one pairings.
5. Interfaces connect compatible responsibilities, including the outcomes needed for Scenario failure and incomplete cases.
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
The owning [Architecture Design model](../models/architecture-design.md#architecture-semantic-outputs) defines the output categories and ownership.

For the declared scope, architecture review SHOULD be able to answer from authoritative information:

- What Modules exist, what does each own, and what is explicitly outside each boundary?
- Which Module is primarily accountable for every active Function in scope, and which Modules support it?
- Which Module is accountable for every active AR in scope?
- Which architecturally significant interactions are Interfaces, who provides them, and who consumes them?
- Who owns the meaning and permitted mutation of significant state/data?
- Which software structures materially realize each Module?
- Which runtime/process boundaries materially affect lifecycle, scaling, isolation, failure, concurrency, or resources?
- How is significant state physically persisted, and is that persistence authoritative, replicated, cached, or derived?
- Which packaging/deployment choices materially affect the architecture?
- Which Interface realization choices materially affect interaction behavior or guarantees?
- Which technology choices are architecturally material, why were they selected, what consequences do they impose, and when should they be revisited?
- Which logical or realization decisions are intentionally deferred?

Architecture Design is complete enough for the declared scope when:

1. every active Function in scope has exactly one accountable primary Module;
2. every active AR in scope is allocated to exactly one Module;
3. significant cross-Module interactions have explicit Interface contracts;
4. significant state/data has clear logical authority and permitted mutation;
5. Module purposes, responsibilities, exclusions, and dependencies are mutually coherent;
6. governed Scenario walkthroughs expose no unexplained responsibility or interaction gaps;
7. material software, runtime, persistence, deployment, Interface-realization, and technology decisions are recorded or explicitly deferred;
8. physical/software realization preserves rather than silently changes logical responsibilities, contracts, and state authority;
9. every material technology decision is attributable to an architectural need or constraint and records enough rationale to revisit it;
10. traceability to governing Functions, SRs, ARs, and Scenarios remains intact;
11. unresolved decisions are visible and do not masquerade as completed architecture.

Logical Module/Interface definitions, allocations, and state/data ownership are architecture truth.
Subordinate realization information explains how that truth is made concrete.
Derived diagrams, inventories, and topology views are presentations and MUST NOT become independent sources of the same facts.

## Iterate and preserve meaning

Architecture development may refine Module boundaries, Interfaces, Functions, or requirement derivation.
Reconcile current allocations and consumers together, preserving stable identity while the same asset or obligation evolves.
Use a new identity when the engineering meaning becomes a distinct asset or obligation; preserve the original allocations in retained baselines.
Do not rewrite old evidence or history to match the new target.

A reviewed architecture draft supports the next engineering decision.
It does not by itself approve a baseline, implement the system, or demonstrate requirement satisfaction.
