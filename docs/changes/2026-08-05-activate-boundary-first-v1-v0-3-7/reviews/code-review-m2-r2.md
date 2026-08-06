# Code Review: M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: two independent L2 Codex reviewers
Target: 443cabf9..2b2b4c6d
Reviewed artifact: M2 R1 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r1
Reviewer context ID: m2-r2-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: remote mutation; diagnostics; privacy; recovery proof
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@2b2b4c6d#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@2b2b4c6d#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@2b2b4c6d#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@2b2b4c6d#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:443cabf9..2b2b4c6d.diff@2b2b4c6d#sha256:ffa2a46c0e848de153fa7938787a98dccda73dbd166d5bdc8edec0430c162ce4
Initial packet hash: sha256:ffa2a46c0e848de153fa7938787a98dccda73dbd166d5bdc8edec0430c162ce4
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: bounded publication diagnostics and recovery proof
Highest-impact failure modes: private-input disclosure, ambiguous post-push state, and unproved partial-ref rejection recovery
Changed boundaries: BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: authenticated safe context; post-push reconciliation; selective-ref rejection; fresh replacement candidate
Areas requiring direct inspection: error context provenance; confirmation failure; receive hooks; replacement history
Areas intentionally out of scope: release payload; actual external publication; final verify
Risk classes considered: privacy; identity; remote mutation; recovery; evidence fidelity
Falsifiable review questions: can untrusted input leak; can post-push uncertainty advise rerun; does one-ref rejection mutate either ref; is replacement proven
Material findings: BFA-M2-R2-001, BFA-M2-R2-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R2-001 — Diagnostic privacy and post-push reconciliation remain incomplete

Finding ID: BFA-M2-R2-001
Severity: major
Evidence: invalid release and forged 40-hex candidate values can be serialized;
some tag failures lose available context; confirmation-advertisement failure is
misclassified as readiness and advises rerun after mutation may have occurred.
Required outcome: report only authenticated or bounded context, preserve safe
authenticated identities, and classify post-push uncertainty as confirmation
requiring stop-and-reconcile.

### BFA-M2-R2-002 — Selective-ref rejection and replacement recovery are unproved

Finding ID: BFA-M2-R2-002
Severity: major
Evidence: the receive hook rejects the entire transaction rather than one
destination, and modified-evidence rejection does not construct a fresh valid
replacement candidate history.
Required outcome: add a tag-selective update-hook fixture and a fresh replacement
candidate fixture, assert both refs and no forbidden fallback, and align evidence.

## R1 reconciliation

- BFA-M2-R1-001: resolved.
- BFA-M2-R1-002: failed remediation; remains open through BFA-M2-R2-001.
- BFA-M2-R1-003: failed remediation; remains open through BFA-M2-R2-002.

## Validation evidence

The 12 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Reviewer probes reproduced
the diagnostic issues and confirmed implementation atomicity under a selective
tag-ref rejection, but repository-owned automation did not yet retain that proof.
