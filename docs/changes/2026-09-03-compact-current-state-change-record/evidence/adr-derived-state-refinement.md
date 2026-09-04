# ADR refinement: derived compact state

Artifact path: docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Artifact identity: sha256:9dbd3c6b7935432f4304e24fac236a7d2e802b3c655e4a5782a591af1de0dd4d
Authoring result: complete

The decision now rejects caller-constructed final state, assigns derived coordination and revision construction to the evaluator, resolves evidence dependencies through typed current references, and limits compact v1 to prospective creation.
