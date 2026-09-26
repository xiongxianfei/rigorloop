# Modules

A Module is a durable architectural unit of responsibility with a meaningful boundary.
Its responsibilities can include behavior, data or state, interfaces, dependencies, and technical policies.

The intended collection uses one `MOD-<id>.json` file per Module.
Names and responsibility descriptions belong in the entity content, independently of its stable identity.
No Module records are present yet.

Describe the responsibility boundary and the decisions needed to understand it.
Author `provides` and `consumes` references to [Interfaces](../interfaces/README.md) here.
Identify the implementation that realizes the Module without requiring an identically named code directory.

Discover assigned [Functions](../../system/functions/README.md) through their `allocatedTo` references.
Discover [Allocated Requirements](../../requirements/README.md) through their own `allocatedTo` references.
Use those allocations to assess whether the Module's responsibility and interactions can satisfy its obligations.
