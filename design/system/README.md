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
Feature ── realizedBy ──> Function ── allocatedTo ──> Module
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
JSON uses `realized_by` and `allocated_to` for the corresponding REM relationship names.

The current seven-IR analysis defines eleven Features and 33 Functions, covering knowledge inspection and authoring, traceability, model conformance and migration, baselines and changes, verification and judgments, guidance, and learning.
Functions such as identity resolution, authorization, and evidence assessment are reused where their meaning matches the capability's needs. A quality or policy SR can constrain existing behavior without introducing another Function.
The [requirements review](../requirements/README.md#review-outcome) accounts for the declared initial scope. These draft assets do not establish implementation, approval, or exhaustive coverage of future RigorLoop capabilities.

Apply REM's [clarity and naming criteria](../../rem/models/system-design.md) to each capability and logical behavior.
Asset filenames combine the stable ID with the full descriptive title under the [naming convention](../support/README.md#entity-naming-and-filenames); relationships continue to use stable IDs alone.

Use [Requirement Analysis](../requirements/README.md) for obligations.
Use [Architecture Design](../architecture/README.md) for responsibility boundaries.
Each asset should describe its current state directly, with historical Changes explaining how it evolved.
