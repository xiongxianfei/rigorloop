# Workflow route: M2 package simplification to architecture

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Source stage: code-review
Destination artifact: adr-consolidated-review-package-topology
Reason: upstream-contract-gap
Finding IDs: CRG-M2-CR1, CRG-M2-CR2, CRG-M2-CR3, CRG-M2-CR4
Return stage: code-review
Lifecycle revision: sha256:c3c21e5e22b1b8222e78e8d702f1ef43475e42b5b9e36718ae30f19dcb5c9245

The approved specification now requires explicit artifact ID-to-path maps and governed invalidation events without aggregate or per-member hashes. The accepted architecture decision still selects aggregate package revisions and must be superseded before M2 implementation can be corrected.
