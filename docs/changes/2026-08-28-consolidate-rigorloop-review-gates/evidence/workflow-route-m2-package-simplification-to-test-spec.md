# Workflow route: M2 package simplification to test spec

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Source stage: code-review
Destination artifact: test-spec
Reason: upstream-contract-gap
Finding IDs: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
Return stage: code-review
Lifecycle revision: sha256:5003fd981da2ab6d7b999e4691bffc6e3d8a7db48221e2e85ee665610f975261

The approved spec, ADR, and plan now use visible package members and governed invalidation. The proof map must remove aggregate/hash cases and directly prove member paths, invalidation, outcome blockers, and finding ownership.
