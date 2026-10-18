# Design the physical/software realization

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

### Author the technical model

Use the [technical-model contract](../models/architecture-realization.md#technical-model) to make the selected architectural implementation explicit before organizing its presentation.

1. Identify the governing responsibilities, Functions, ARs and existing Interfaces. Reuse their identities and ownership.
2. Define the necessary technical components, each component's responsibility/exclusions and its realization mappings. Name coherent roles before attaching technology choices; do not introduce a Module for every executable or dependency.
3. Define or reference the connecting contracts: participants, requests/results or data representation, guarantees, compatibility and material failures. State who owns and may mutate each significant state or artifact.
4. Record material technology choices with rationale, alternatives and consequences. Expose unresolved mappings and distinguish design intent from implementation observations.
5. Walk through a normal interaction and material failure or incompatible-input cases to assess the composition. Draw Technical structure within Logical; use Development for source/package/build organization, Process for execution and Physical for placement. These projections reuse the same owned facts.

Start with prose, component/contract tables and attributable diagrams at existing owners. Refine structured realization records when their semantics and tooling need are settled; the method does not require a new schema, standalone technical-model document or implementation before design.

### Derive realization views

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
