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

The current ten-IR analysis defines 20 Features and 63 Functions. It covers engineering-model capabilities and the [published-product extension](../requirements/published-products.md): explicit command operations, portable guided activities, and tooling distribution.
Functions such as identity resolution, authorization, and evidence assessment are reused where their meaning matches the capability's needs. Under [Functional Analysis](../../rem/methods/functional-analysis.md), every approved SR must confirm at least one Function; a quality or policy obligation can confirm and constrain existing behavior without introducing another Function.
The [requirements review](../requirements/README.md#review-outcome) retains the initial analysis subject, and the [published-product review](../requirements/published-products.md#review-and-validation) records the extension. These draft assets do not establish implementation, approval, or exhaustive coverage of future RigorLoop capabilities.

All 63 Functions identify one accountable primary Module in a proposed architecture of 15 Modules.
The [Architecture Design](../architecture/README.md) records those responsibility boundaries, while the Function definitions retain their logical behavior.
The first detailed example covers IR-001 and the shared SR-012 interpretation responsibility with two Interfaces and ten ARs. Four additional Interfaces connect the product responsibilities. Module records state their remaining design limits; allocation of every Function does not establish complete Interface or requirement-allocation coverage.

Apply REM's [clarity and naming criteria](../../rem/models/system-design.md) to each capability and logical behavior.
Asset filenames combine the stable ID with the full descriptive title under the [naming convention](../support/README.md#entity-naming-and-filenames); relationships continue to use stable IDs alone.

Use [Requirement Analysis](../requirements/README.md) for obligations.
Use [Architecture Design](../architecture/README.md) for responsibility boundaries.
Each asset should describe its current state directly, with historical Changes explaining how it evolved.
