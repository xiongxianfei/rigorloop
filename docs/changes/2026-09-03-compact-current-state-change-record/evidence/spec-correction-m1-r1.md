# Specification correction: Projection identities

Artifact path: specs/compact-current-state-change-record.md
Artifact identity: sha256:5199f17dc08e54ff58b2c81002885d6b0ac538f35466533d9cd5b02d8eed810d
Authoring result: complete

## Result

The exact closed Projection record now includes `change_id`, `lifecycle_contract`, and `lifecycle_revision`. This makes the normative table consistent with SR-21 and keeps every bounded view independently attributable without relying on an enclosing transport, Git, pull-request state, logs, or procedural history.

## Validation

- Boundary-first validation passed for the corrected specification.
- Markdown readability validation passed with advisory long-line warnings only.
- `git diff --check` passed as a local whitespace diagnostic; no contract behavior depends on Git.

## Handoff

The revised Design package requires fresh Design Review. This evidence does not claim package approval, implementation completion, or verification.
