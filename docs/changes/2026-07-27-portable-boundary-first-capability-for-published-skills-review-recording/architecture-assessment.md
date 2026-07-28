# Architecture Assessment

Stage: architecture-assessment
Applicability: required
Spec identity: approved at commit 011fc64d

## Rationale

The approved boundary-first contract changes the source and projection model
for a shared published-skill reference, the canonical and generated skill
trees, adapter archives, installed Codex, Claude Code, and opencode trees,
structural validation, release activation evidence, and package rollback
validation.

Those surfaces cross authored-source, generated-output, package, validation,
and release boundaries.
The change also needs durable decisions for the canonical reference owner,
projection command, activation manifest, immutable grandfathering baseline,
and operator boundary for rollback.

## Result

Proceed to a direct update of the canonical architecture package and a new
ADR.
Architecture review is required before planning.
