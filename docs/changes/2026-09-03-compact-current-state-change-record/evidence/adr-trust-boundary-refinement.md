# ADR refinement: CLI trust boundary

Artifact path: docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Artifact identity: sha256:089519c8ae5604a07e3c90d2506045a0eed1b02d5f556216cff1625cbfdc007a
Authoring result: complete

The decision excludes request-level authority claims, derives structural operation eligibility from current records, treats role labels as responsibility/provenance, and identifies OS, sandbox, or enclosing-runner controls as the actual execution permission boundary.
