# Workflow Route: M2 Package Simplification to Specification

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Source stage: code-review
Destination artifact: spec
Reason: upstream-contract-gap
Finding IDs: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
Return stage: code-review
Lifecycle revision: sha256:d8e9028796ded7bca0b78300254948cc01142c285e96050344055618e62e9277

The workflow owner directed M2 to replace aggregate and per-document hash authority with explicit package member IDs, repository paths, review identity, and state. Specification owns the revised observable contract before architecture and implementation are changed.
