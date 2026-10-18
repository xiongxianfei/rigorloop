<!-- Generated from rem/methods/views/physical.md; source SHA-256 c8e88c58305e45314b11e78d7c45ae0e603dd3084953a17b16133e552b2a23ff. Edit the owning REM source. -->

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
