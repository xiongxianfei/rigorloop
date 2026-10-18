# Architecture Allocation method

Use Architecture Allocation after Functions and architectural responsibilities are sufficiently understood to assign behavior and lower-level obligations to Modules.
Architecture Allocation establishes the logical responsibility model; it does not by itself select services, processes, datastores, deployment units, protocols, or implementation technologies.
The [Architecture Design model](../models/architecture-design.md) owns allocation cardinalities and Interface relationships.

## Purpose

Architecture Allocation answers two separate questions:

1. Which Module is accountable for performing each Function?
2. Which Module is responsible for satisfying each Allocated Requirement?

These allocations approach architecture from different directions and MUST be reviewed together.

## Inputs

Start with:

- confirmed Functions from [Functional Analysis](functional-analysis.md);
- approved or otherwise applicable SRs from [Requirement Analysis](requirement-analysis.md), plus any existing ARs that remain applicable;
- candidate or existing Module responsibilities and containment relationships;
- known state, policy, data, interaction, ownership, and encapsulation boundaries.

Do not begin by forcing existing source directories or services to become Modules.

## Establish or refine the Module hierarchy

Identify broad architectural responsibilities first, then decompose a Module only when child responsibilities form meaningful boundaries with clearer ownership, state authority, policy, evolution, or collaboration. A parent Module must remain a real architectural responsibility rather than a container introduced only for navigation.

Use containment only for true responsibility refinement:

```text
Parent Module
└── Child Module
    └── Child Module ...
```

Each Module has at most one parent and containment must remain acyclic. REM does not impose a universal maximum depth; stop decomposing when another level would primarily describe implementation structure rather than durable architecture.

Treat each parent as an encapsulation boundary. Record which descendant-provided Interfaces remain internal and which must be intentionally exposed through the parent boundary.

## Allocate Functions

Every active Function MUST have exactly one accountable primary Module before architecture allocation is considered complete.
A Function MAY involve zero or more supporting Modules.

```text
Function ── primaryModule ──> Module
Function ── supportingModule ──> Module (0..*)
```

The primary Module owns the Function's architectural responsibility.
Supporting Modules may provide required capabilities without becoming co-owners of the Function.

Allocate to the lowest Module in the hierarchy that can coherently own the complete Function. Do not duplicate the allocation on ancestors merely to make parent views complete; derive parent roll-up visibility from containment. Allocate directly to a parent only when the behavior genuinely belongs to the broader parent responsibility.

If no Module can own the Function coherently, reconsider the Module boundaries or the Function boundary rather than assigning arbitrary ownership.

## Derive and allocate ARs

Once Module responsibilities are coherent enough to make lower-level accountability meaningful, derive or refine the ARs needed to express architecture-level obligations. Apply the [Requirement Analysis AR rules](requirement-analysis.md#formulate-allocated-requirements-with-architectural-context) so each AR remains a real verifiable requirement rather than an allocation placeholder.

Every active AR MUST be allocated to exactly one Module.

```text
AR ── allocatedTo ──> Module
```

If one lower-level obligation genuinely belongs to several Modules, decompose it into multiple ARs under the same parent SR so each obligation has one accountable architectural owner.
Do not use multi-owner ARs to avoid deciding responsibility.

Allocate to the lowest Module in the hierarchy that can coherently own the complete obligation. Do not repeat descendant AR allocation on parent Modules for roll-up. Allocate an AR directly to a parent only when the obligation applies to the broader parent boundary itself.

## Reconcile requirement and functional allocation

For each Module, review together:

- parent/child responsibility and derived descendant roll-up, where applicable;
- Functions it owns directly;
- ARs allocated to it directly;
- state or data it owns;
- policies it must enforce;
- Interfaces it provides or consumes;
- descendant-provided Interfaces it exposes through its boundary.

Look for mismatches such as:

- a Module owns a Function but no relevant allocated obligation explains required constraints;
- an AR is allocated to a Module that lacks the behavior, state, policy, or interaction needed to satisfy it;
- one Function's primary responsibility is split ambiguously across Modules;
- one AR spans several Modules without decomposition.

Not every AR must map one-to-one to a Function.
ARs may govern state, quality, policy, or another architectural responsibility.

## Identify Interfaces

Create or refine an Interface when architecturally significant information or behavior crosses a Module boundary.
Each Interface MUST have exactly one provider Module and MAY have zero or more consumer Modules.

First identify the Module accountable for the contract's complete outcomes and compatibility. Then explain the behavioral contributions that realize it. A parent-owned contract may rely on child Functions, ARs, state, and realization without transferring those allocations to the parent or giving the Interface a second provider. Do not add child consumption merely to stand for implementation.

```text
Module ── provides ──> Interface
Module ── consumes ──> Interface
```

Define the interaction contract at the architectural level without prescribing realization details that are not required by the design.

When the provider is a contained Module, keep the Interface internal to its nearest parent boundary unless a consumer outside that boundary requires the contract. In that case, explicitly expose the same Interface through the parent. If visibility must extend beyond additional ancestors, expose it continuously through each intervening parent boundary; do not skip a boundary or create automatic wrapper Interfaces.

If the broader parent responsibility genuinely owns the external contract, define the parent itself as the provider instead of merely exposing a child-owned Interface.

### Derive a contract from a consumer Scenario

1. Select a governed Scenario and its applicable SR obligations and Functions. Identify the consumer's requested outcome and the exact responsibility boundary crossed; containment rollups do not create additional consumers.
2. Compare existing Interfaces with that need. Reuse a contract whose meaning fits, refine one when its coherent scope evolves, or create a distinct contract when the required interaction has a different purpose or guarantees. Do not expose an internal Interface wholesale merely because its provider is nearby.
3. Define the consumer's inputs and state/scope/authority basis, provider outcomes, incomplete and failure cases, consistency, and compatibility. Keep observations, authority, retention, judgments, and actual execution distinct. Group operations by coherent consumer need rather than one Interface per Module, child, or Function.
4. Assign the single accountable provider, then explain the child behavior, data, policies, and existing allocations that contribute. A parent contract may compose several children. Do not infer execution order or per-Interface realization edges solely from containment.
5. Walk ordinary, alternative, and failure Scenario outcomes through the contract and consumer responsibility. Identify exactly which outcomes the contract supports and what remains outside it. A successful inspection, applicable grant, or favorable evidence assessment must not become a stronger claim such as retained state, executed work, or complete qualification without its own basis.
6. Record the derivation at the authoritative contract and participant owners. Reconcile current definitions and deferrals, then regenerate views. Revisit Requirements or System Design when the walkthrough exposes a missing obligation or behavior; do not invent an Interface to hide that gap.

A baseline consumer may need coherent model content before arranging retention; an inspection contract can supply that content while retention confirmation remains a separate collaboration. Similarly, authority and evidence support are separate contracts when one can be valid while the other prevents the proposed action. The resulting analysis must expose those limits before declaring the Scenario's architecture complete.

## Completion criteria

Architecture Allocation is complete enough for realization when:

- Module containment, where used, is acyclic and every parent/child relationship represents genuine responsibility refinement;
- every active Function has exactly one primary Module, normally the lowest coherent accountable Module;
- required architecture-level obligations have been expressed as justified ARs, and every active AR has exactly one allocated Module, normally the lowest coherent accountable Module;
- supporting Module participation is explicit where needed;
- requirement allocation and functional allocation have been reconciled;
- architecturally significant cross-Module interactions have explicit Interfaces;
- every Interface has exactly one provider Module;
- descendant-provided Interfaces that cross parent boundaries are explicitly exposed through every intervening provider-side parent boundary;
- unresolved ownership, containment, encapsulation, or interaction gaps are explicit;
- allocations describe responsibility rather than merely mirroring the current code layout.

After logical allocation is coherent, use [Architecture Design](realization-design.md#design-the-physicalsoftware-realization) to define the material physical/software realization as subordinate Module and Interface views.
