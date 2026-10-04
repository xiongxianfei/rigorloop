# System Design

System Design describes the durable capabilities and logical behavior of RigorLoop.
The [REM System Design model](../../rem/models/system-design.md) owns the reusable model semantics.

| Asset | Collection | Meaning |
| --- | --- | --- |
| Feature | [features/](features/README.md) | Product-visible or stakeholder-visible capability |
| Function | [functions/](functions/README.md) | Logical behavior that realizes capabilities |

```text
IR ── confirms ──> Feature <── exercises ── Scenario
SR ── confirms ──> Function
Feature ── realizedBy ──> Function ── primaryModule ──> Module
```

Features and Functions have independent identities and lifecycles.
A Function may realize multiple Features.
Functions therefore live in their own collection.

Requirements can constrain both asset types without becoming their containment parents.
IR and Scenario analysis establish Features; SR analysis establishes Functions.
Scenarios are [governed Requirement Analysis entities](../requirements/scenarios/README.md).

Features own their Function references.
Functions own their Module allocations.
Inverse views are derived from those references.
JSON uses `realized_by` for realization and retains `allocated_to` as the selected representation of a Function's accountable primary Module.

The current ten-IR analysis defines 22 Features and 73 Functions. It covers engineering-model capabilities and the [published-product extension](../requirements/published-products.md): explicit command operations, portable guided activities, and tooling distribution.
Functions such as identity resolution, authorization, and evidence assessment are reused where their meaning matches the capability's needs. Under [Functional Analysis](../../rem/methods/functional-analysis.md), every SR must confirm at least one Function before System Design is considered complete; a quality or policy obligation can confirm and constrain existing behavior without introducing another Function.
The [requirements review](../requirements/README.md#review-outcome) retains the initial analysis subject, and the [published-product review](../requirements/published-products.md#review-and-validation) records the extension. These draft assets do not establish implementation, approval, or exhaustive coverage of future RigorLoop capabilities.

The original 63 Functions identify one accountable primary Module among the 15 children in the proposed 19-Module architecture. The four parents show derived descendant coverage without additional allocation or behavior ownership.
The [Architecture Design](../architecture/README.md) records those responsibility boundaries, while the Function definitions retain their logical behavior.
The first detailed example covers IR-001 and the shared SR-012 interpretation responsibility with two Interfaces and ten ARs. Four subsequent Interfaces connect the original product responsibilities. Four [parent-boundary contracts](../architecture/views/browser/index.html#scenarios) now add engineering-state inspection, adopted model-authoring guidance, applicable action authority, and evidence-support assessment. The model has twelve Interfaces, including IF-011 work context and adoption. Four new local-history Functions remain unallocated, and revised existing recording Functions need reconciliation with the retained v3 Interface and realization contracts. Module records state their remaining design limits; allocation of every Function does not establish complete Interface or requirement-allocation coverage.
The [CLI cooperation view](../architecture/views/browser/index.html#cooperation) summarizes how the 18 IR-008 ARs and IF-003/IF-004 support the CLI Scenarios. Function definitions and primary allocations remain unchanged.

Apply REM's [clarity and naming criteria](../../rem/models/system-design.md) to each capability and logical behavior.
Asset filenames combine the stable ID with the full descriptive title under the [naming convention](../support/README.md#entity-naming-and-filenames); relationships continue to use stable IDs alone.

Use [Requirement Analysis](../requirements/README.md) for obligations.
Use [Architecture Design](../architecture/README.md) for responsibility boundaries.
Each asset should describe its current state directly, with historical Changes explaining how it evolved.

The [local operational-history analysis](../requirements/sources.md#src-local-operational-analysis) adds draft backup/restoration, transfer, migration and subject-history behavior. It does not approve allocation or claim implementation of that extension.

## Requirement-first workflow design

The [workflow composition and owning records](../architecture/README.md#requirement-first-workflow-composition) reconciles existing guidance, context and assurance behavior, adds FUNC-078 under MOD-006 and parent-owned IF-011, and allocates SR-079–083 through AR-029–042. Its subordinate contracts define v4 records, v2 operations and explicit installed-unit replacement. FUNC-064 and IF-006 include the narrow SR-065/SCN-063 refinement for separately authorized obsolete-unit retirement. No new Module or runtime implementation is introduced; machine schemas, dispatch and qualified adapter support remain implementation work.

## Customer browser behavior

The requirement basis SR-084–088 needs more than existing definition and relationship navigation. Functional Analysis reuses FUNC-004/007/009/012/013 for retrieval, explanation, traversal and interpretation, FUNC-040/048 for command admission/results, FUNC-060/061 for candidate production/integrity, and FUNC-068/070/071 for release qualification, authority and observations. FUNC-062 remains CLI-specific; MOD-014's skill installation is not generalized into a browser installer.

| Requirement | New behavior and primary owner | Reused behavior |
| --- | --- | --- |
| SR-084 | FUNC-079 capture (MOD-001); FUNC-080/081 composition and assembly (MOD-004) | FUNC-012/013 interpretation and diagnostics |
| SR-085 | FUNC-080/081 qualified projections and reading artifacts (MOD-004) | FUNC-007/009 explanation and relationship navigation |
| SR-086 | FUNC-081 self-contained portable reading (MOD-004) | Selected-state explanation retains its original meaning |
| SR-087 | FUNC-079 input capture; FUNC-081 preparation; FUNC-082 publication/recovery (MOD-004) | Publication authority and source meaning remain separate |
| SR-088 | FUNC-083 actual browser-candidate qualification (MOD-013) | Command, packaging, integrity and release Functions above |

These five additions identify distinct logical outputs/failure boundaries, not one Function per SR or renderer component. FEAT-022 composes them with existing behavior; FEAT-018 adds browser qualification. JSON SR confirmations and Feature realization links own the relationships. Complete links support scoped design assessment; they do not themselves prove adequate behavior, implementation or satisfaction.

Input selection flows through capture and interpretation to qualified projections, then artifact assembly, then separately controlled publication. Check-mode observes currentness without mutation; recovery reconciles actual output state without rerunning source authoring. A captured snapshot is not a retained engineering Baseline, and offline reading is not a hosted service. [Architecture Design](../architecture/README.md#customer-architecture-browser-composition) assigns the boundary contracts and realization.
