# Architecture Design method

Use responsibility-based decomposition to assign logical behavior and allocated obligations to coherent architectural boundaries.
The [Architecture Design model](../models/architecture-design.md) owns Module, Interface, and allocation semantics; the [requirement model](../models/requirements.md) owns SR-to-AR derivation and containment.
The method is independent of tools, programming languages, source layout, and deployment technology.

## Inputs and intended result

Start with the current IRs, SRs, Features, Functions, governed Scenarios, applicable constraints, and attributable existing architecture or implementation information.
Identify whether the work describes existing architecture, proposes target architecture, or changes an established boundary.
Existing implementation is evidence about what exists; it does not automatically determine the intended architecture or transfer approval to a proposal.

Produce understandable Module responsibilities, justified Function allocations, explicit interaction contracts, and assessable ARs derived from their SRs.
Record the scope of the analysis, remaining allocation deferrals, and the conclusions supported by review.
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
8. Target architecture is distinguished from observed implementation, retained history, and the evidence needed to claim satisfaction.

Structural validation checks representation and reference rules; engineering review checks the meaning of responsibilities, contracts, and composed obligations.
Neither a connected graph nor a valid schema establishes architectural adequacy or implementation correctness.
Capture review findings and their resolution against the reviewed model state, and expand to the remaining scope only after reconciling the first example's shared boundaries.

## Iterate and preserve meaning

Architecture development may refine Module boundaries, Interfaces, Functions, or requirement derivation.
Reconcile current allocations and consumers together, preserving stable identity while the same asset or obligation evolves.
Use a new identity when the engineering meaning becomes a distinct asset or obligation; preserve the original allocations in retained baselines.
Do not rewrite old evidence or history to match the new target.

A reviewed architecture draft supports the next engineering decision.
It does not by itself approve a baseline, implement the system, or demonstrate requirement satisfaction.
