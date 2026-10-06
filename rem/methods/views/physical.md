# Physical View

## Physical View

The Physical View answers:

> How is the software architecture physically packaged, placed, connected, and supported by deployment and persistence topology?

Prefer these semantic inputs:

- Module deployment realization;
- material persistence/datastore placement;
- deployment/package units and significant targets;
- material external runtime dependencies;
- placement/isolation relationships that affect architecture;
- concrete Interface connectivity where it matters to the physical topology.

The Physical View SHOULD distinguish logical state/data authority and Module encapsulation from the physical mechanism or location that stores or deploys them.
A datastore, cache, index, deployment unit, node, cluster, or device shown in this view remains subordinate realization information unless it has an independent REM identity for another reason.
