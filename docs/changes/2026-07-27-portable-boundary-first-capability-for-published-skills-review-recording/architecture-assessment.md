# Architecture Assessment

Stage: architecture-assessment
Applicability: required
Spec identity: sha256:d56e3ce553f2970f7ac872f7d4372bd24d138de8617dba240190f9dbd378e16b

## Rationale

The approved boundary-first contract changes the source and projection model
for a shared published-skill reference, the canonical and generated skill
trees, adapter archives, installed Codex, Claude Code, and opencode trees,
structural validation, activation evidence, and compatibility enforcement.

Those surfaces cross authored-source, generated-output, package, validation,
and release boundaries.
The change also needs durable decisions for the canonical reference owner,
projection command, activation baseline, and rollback unit.

## Result

Proceed to a direct update of the canonical architecture package and a new
ADR.
Architecture review is required before planning.
