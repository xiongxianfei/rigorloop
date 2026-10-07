<!-- Generated from rem/models/architecture-boundaries.md; source SHA-256 a7e312e3d9b9013927e2cd3ed80da82fc2bbddee442e40d737e7cac7671883c1. Edit the owning REM source. -->

# Module hierarchy and encapsulation

## Module hierarchy and encapsulation

A Module MAY contain zero or more child Modules. A Module MAY have at most one parent Module. Containment MUST be acyclic, so each connected containment structure forms a tree and the complete architecture forms a forest of Module trees.

A parent Module is a first-class architectural responsibility with its own purpose, scope, lifecycle, state/data authority, allocations, Interfaces, and realization where applicable. It MUST NOT exist merely as a navigation folder or visual grouping. Each child Module refines part of the parent's broader responsibility while retaining independent stable identity. Moving a Module to a different parent changes current architecture containment but does not by itself change the Module's identity.

REM does not prescribe a universal maximum Module-containment depth. Architecture SHOULD remain shallow enough that each level expresses a meaningful responsibility decomposition rather than implementation structure. A project implementation MAY impose a stricter supported depth as an Operational Support or representation rule, provided that restriction is not presented as universal REM semantics.

A parent Module is an encapsulation boundary. An Interface provided by a descendant is internal to the nearest containing parent boundary unless the Interface is explicitly exposed through that boundary. If the same child-provided contract must be visible beyond additional ancestors, exposure MUST continue through the intervening parent boundaries without skipping them. Exposure preserves the descendant provider and the Interface identity; it does not create a wrapper Interface automatically.

If the broader parent responsibility genuinely owns the external contract, the parent SHOULD provide an Interface in its own right rather than presenting a child-owned contract as parent-owned.

## Modules

A Module is a meaningful architectural responsibility boundary and may own:

- Functions;
- state or data;
- policies and constraints;
- provided and consumed Interfaces;
- dependencies;
- realization scope.

Module boundaries SHOULD be justified by responsibility and evolution rather than copied mechanically from current source directories, packages, processes, or deployment units. Parent-child decomposition SHOULD likewise reflect responsibility refinement and encapsulation rather than organization charts or filesystem convenience.

### Module names and identity

A Module name should identify its responsibility and subject in terms that distinguish it from neighboring Modules. Avoid repeated generic qualifiers and broad words such as “management” when they hide the actual responsibility. Retain context needed to make the canonical name understandable outside its current tree position; brevity alone is not the goal. Parent names describe the broader responsibility, while child names distinguish the parts they own. The [Architecture Design method](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/architecture-design.md#define-coherent-module-boundaries) applies these criteria when refining a decomposition.

A clearer name for the same responsibility preserves the Module's stable identity, allocations, Interfaces, and containment. If the work changes any of those relationships or the responsibility boundary, assess that architectural change explicitly rather than treating it as a cosmetic rename. [Operational Support](rem-models-operational-support.md#naming-and-location) owns reference and location reconciliation; the [view method](rem-methods-view-presentation.md#rendered-readability-and-navigation) owns faithful shortened display labels.

## Interfaces

A Module may `provide` and `consume` Interfaces.
The canonical relationship labels are `provides` and `consumes`.

Each Interface MUST have exactly one provider Module.
An Interface MAY have zero or more consumer Modules.
An Interface may describe operations, messages, data structures, inputs, outputs, protocols, failure semantics, and compatibility constraints.
Architecturally significant cross-Module interactions SHOULD be explicit Interfaces.

An Interface covers a cohesive interaction needed by its consumers. A Module MAY provide several Interfaces, and one Interface MAY contain several related operations. Its scope need not cover the provider's entire responsibility or correspond one-to-one with a child Module. Separate contracts when their purpose, authority, failure guarantees, or independent evolution differ materially; explain their cooperation where needed.

The provider is the Module accountable for the contract: its promised outcomes, failures, consistency, and compatibility. Provider ownership is distinct from the behavior or implementation that realizes the contract. A parent MAY provide an Interface whose behavior is realized through child responsibilities. Those children retain their Function/AR allocations and state authority without becoming additional providers. A child's implementation contribution alone does not create a `consumes` relationship either.

Choose the provider from the scope of contract accountability. Do not infer it from source-code location, directory containment, or the Module that executes an operation. Explain how the accountable boundary is realized through its contributing responsibilities and material realization information. Containment alone does not establish that every descendant implements every parent Interface; a tool needs explicit supporting facts before projecting that relationship.

An Interface can describe an internal interaction and need not be a network API.

When its provider is a contained Module, an Interface is internal to that containment boundary by default. A consumer outside the provider's containing parent may use the Interface only when the contract is explicitly exposed through that parent boundary. If the consumer lies beyond additional ancestors, every intervening provider-side parent boundary MUST expose the same Interface. Exposure does not alter provider/consumer identity, imply runtime call direction, or create a second contract.

Architecture review SHOULD distinguish Interfaces owned directly by a parent Module from descendant Interfaces merely exposed through that parent boundary.

A parent-provided Interface needs no exposure through its own provider. If that provider is itself contained and the contract crosses higher boundaries, the normal ancestor-exposure rules still apply. Moving contract accountability is a controlled model change: preserve identity when the same contract continues, reconcile provider participation and exposure, and retain the earlier state's meaning.


## Source rationale

[Parnas on decomposition](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S10.md) supports examining significant design decisions and change consequences when choosing boundaries.
REM owns its Module hierarchy, Interface exposure and allocation rules; the paper does not establish their exact cardinalities.
