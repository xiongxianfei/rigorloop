# Architecture Revision Evidence R1

Finding: CRSIM-AR1
Stage: architecture
Date: 2026-08-10

The canonical architecture now requires every supported `code-review` target, including pure-copy installation, to be materialized into a temporary installed tree and compared for mapped-resource inventory, relative paths, and raw-byte identity. Additional installer behavior may retain its bounded filesystem checks.

The correction updates the code-review package building block, package-loading flow, target deployment boundary, and crosscutting composition rule. It preserves the existing deterministic Gate A/Gate B ownership and does not add a target runtime, network dependency, fourth semantic gate, or validator family.

Ready for architecture-review R2.
