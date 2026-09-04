# Architecture refinement: CLI trust boundary

Artifact path: docs/architecture/2026-09-03-compact-current-state-change-record.md
Artifact identity: sha256:511ad9b51619c38cc874d9aff9efcd0c1a4470e6a5514fa700983cde355e0c13
Authoring result: complete

The architecture derives operation eligibility from current lifecycle state, active work, target, and exact identities; excludes caller authentication claims; treats durable role labels as responsibility/provenance; and places execution access with OS, sandbox, or enclosing-runner controls.
