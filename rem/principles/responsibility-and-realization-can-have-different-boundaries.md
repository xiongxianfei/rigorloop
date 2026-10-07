# Responsibility and realization can have different boundaries

Identity: `rem:principle:responsibility`.

## Key takeaway

Where code executes does not alone determine which architectural responsibility owns an outcome.

## Summary

Logical responsibilities are chosen to explain accountability and design concerns. Processes, libraries, hardware and deployment units answer different questions. Their boundaries can coincide, but neither coincidence nor separation is a universal requirement.

## Statement and example
A service process may realize several responsibilities, and one responsibility may span an adapter and a worker. A parent may promise an end-to-end result using several children. Reassigning the contract merely because its code moved can erase the original accountability without establishing a replacement.

## Source basis and REM synthesis

[Kruchten](../references/kruchten-1995-architectural-blueprints.md#located-contributions) describes mappings between logical, process, development and physical views that need not be one-to-one. REM's Module/Interface accountability and subordinate realization are selected rules in its [Architecture model](../models/architecture-design.md), not rules derived from the paper's class diagrams.

## Methodological consequences
An architecture discussion can use separate descriptions for “what is owned” and “where it runs,” connected by a rationale. This supports deployment changes, consolidation and extraction without inventing a new capability merely because an executable appears.

## Limits and counter-signal
A real operational constraint may require responsibility and process boundaries to align—for isolation, certification, ownership or fault containment. In that context a purely logical split is insufficient. A mapping with no explanation of the critical state, failures or dependencies is only a naming correspondence.

## Applications
[Architecture realization](../models/architecture-realization.md); [Architecture Allocation](../methods/architecture-allocation.md); [Realization Design](../methods/realization-design.md); [Architecture Views](../methods/architecture-views.md).
