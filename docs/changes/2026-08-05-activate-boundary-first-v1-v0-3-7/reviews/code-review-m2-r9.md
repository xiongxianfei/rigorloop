# Code Review: M2 R9

Review ID: code-review-m2-r9
Stage: code-review
Round: 9
Reviewer: two independent L2 Codex reviewers
Target: 18987ad4..c7144973
Reviewed artifact: M2 R8 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r8
Reviewer context ID: m2-r9-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: descriptor ownership; cleanup verification; bounded errors
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@c7144973#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@c7144973#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@c7144973#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@c7144973#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:18987ad4..c7144973.diff@c7144973#sha256:8d00896223e8f8e9bd952979d91ba4596223c5ec5404ddd0e28bf2bb99e59429
Initial packet hash: sha256:8d00896223e8f8e9bd952979d91ba4596223c5ec5404ddd0e28bf2bb99e59429
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: pipe endpoint cleanup verification
Highest-impact failure modes: live endpoint ownership discarded after false closure proof
Changed boundaries: BND-RECOVERY-001; BND-ENV-001
Evidence expected: errno-aware closure proof and bounded cleanup failure matrix
Areas requiring direct inspection: close fallback, fstat proof, terminal cleanup
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: resource ownership; portability; error handling; privacy
Falsifiable review questions: can cleanup report closure while an endpoint remains live
Material findings: BFA-M2-R9-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### BFA-M2-R9-001 — Close fallback can falsely prove endpoint closure

Finding ID: BFA-M2-R9-001
Severity: major
Evidence: `_force_close_descriptor` treats every `fstat` `OSError` as proof of
closure even though only `EBADF` proves invalidation. Unsupported or rejected
`closerange` errors can also escape raw after an initial close failure. Both
reviewers independently reproduced a live endpoint after non-`EBADF`
verification failure; the existing tests cover only successful fallback.
Required outcome: bound fallback capability errors, accept only `EBADF` as
verified invalidation, retain ownership on all other verification errors, and
prove setup, subprocess-failure, and nominal-success cleanup paths invalidate
both endpoints without replacing the primary bounded result.

## Prior-finding reconciliation

BFA-M2-R1-002 and BFA-M2-R2-001 are resolved for classification, privacy, and
post-push uncertainty. BFA-M2-R8-002 is resolved for ordinary unsupported
pipe, blocking-mode, and descriptor-inheritance behavior. Endpoint-lifecycle
requirements from BFA-M2-R7-001, BFA-M2-R8-001, and BFA-M2-R8-002 remain open
through BFA-M2-R9-001.

## Validation evidence

The 19 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, review-structure validation, metadata validation,
and range diff passed. Independent fault injection reproduced the finding.
