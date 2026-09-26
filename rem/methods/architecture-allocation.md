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
- SRs and derived ARs from [Requirement Analysis](requirement-analysis.md);
- candidate or existing Module responsibilities;
- known state, policy, data, interaction, and ownership boundaries.

Do not begin by forcing existing source directories or services to become Modules.

## Allocate Functions

Every active Function MUST have exactly one accountable primary Module before architecture allocation is considered complete.
A Function MAY involve zero or more supporting Modules.

```text
Function ── primaryModule ──> Module
Function ── supportingModule ──> Module (0..*)
```

The primary Module owns the Function's architectural responsibility.
Supporting Modules may provide required capabilities without becoming co-owners of the Function.

If no Module can own the Function coherently, reconsider the Module boundaries or the Function boundary rather than assigning arbitrary ownership.

## Allocate ARs

Every active AR MUST be allocated to exactly one Module.

```text
AR ── allocatedTo ──> Module
```

If one lower-level obligation genuinely belongs to several Modules, decompose it into multiple ARs under the same parent SR so each obligation has one accountable architectural owner.
Do not use multi-owner ARs to avoid deciding responsibility.

## Reconcile requirement and functional allocation

For each Module, review together:

- Functions it owns;
- ARs allocated to it;
- state or data it owns;
- policies it must enforce;
- Interfaces it provides or consumes.

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

```text
Module ── provides ──> Interface
Module ── consumes ──> Interface
```

Define the interaction contract at the architectural level without prescribing realization details that are not required by the design.

## Completion criteria

Architecture Allocation is complete enough for realization when:

- every active Function has exactly one primary Module;
- every active AR has exactly one allocated Module;
- supporting Module participation is explicit where needed;
- requirement allocation and functional allocation have been reconciled;
- architecturally significant cross-Module interactions have explicit Interfaces;
- every Interface has exactly one provider Module;
- unresolved ownership or interaction gaps are explicit;
- allocations describe responsibility rather than merely mirroring the current code layout.

After logical allocation is coherent, use [Architecture Design](architecture-design.md#design-the-physicalsoftware-realization) to define the material physical/software realization as subordinate Module and Interface views.
