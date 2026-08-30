# Specification revision evidence R2

Operation: revise-primary-spec
Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Artifact ID: spec
Artifact path: specs/consolidated-review-gates.md
Prior artifact identity: sha256:64fbc97dc179d86b24c9aa04434521f3fe73349b643e9bf7845ed227ebee2a62
Artifact identity: sha256:ae8b9452fc028fadb9cdd616f3d6d07ce312847951ee178e874aab753a1c357c
Loaded profile: SA1-governed
Boundary model: boundary-first-v1
Resolved review finding: CRG-SR4 pending independent rereview
Validation: documentation prose passes; boundary structure remains valid with only the matching proof map deliberately pending the downstream `test-spec` stage.
Authoring result: complete
Downstream authority: independent `spec-review-r3` only

The revision makes upstream authority part of package identity without introducing per-document hashes. A design package binds the accepted Proposal Review ID, while a delivery package binds the approved aggregate design-package revision. The CLI calculates one aggregate revision from the component bytes and that upstream binding; lifecycle status remains solely in the owning change record.
