# Code Review: M2 R8

Review ID: code-review-m2-r8
Stage: code-review
Round: 8
Reviewer: two independent L2 Codex reviewers
Target: 293d52ea..2ae6ae68
Reviewed artifact: M2 R7 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r7
Reviewer context ID: m2-r8-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: descriptor ownership; platform capability; bounded errors
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@2ae6ae68#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@2ae6ae68#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@2ae6ae68#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@2ae6ae68#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:293d52ea..2ae6ae68.diff@2ae6ae68#sha256:0cb659c64021ce0c54c341368754ddff663c4aea62fbf35152f8c2e3ed76e6cd
Initial packet hash: sha256:0cb659c64021ce0c54c341368754ddff663c4aea62fbf35152f8c2e3ed76e6cd
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: pipe endpoint lifecycle and unsupported-platform failure
Highest-impact failure modes: live endpoint leak and raw pass-fds/setup exception
Changed boundaries: BND-RECOVERY-001; BND-ENV-001
Evidence expected: verified endpoint invalidation and bounded capability matrix
Areas requiring direct inspection: ownership transfer, close fallback, setup, subprocess invocation
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: resource ownership; portability; error handling; privacy
Falsifiable review questions: can a close failure leak; can unsupported APIs escape raw
Material findings: BFA-M2-R8-001, BFA-M2-R8-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R8-001 — Close failure discards live endpoint ownership

Finding ID: BFA-M2-R8-001
Severity: major
Evidence: the reader catches close failure but the caller clears both descriptor
variables, preventing final cleanup; end-to-end probes retain live endpoints.
Required outcome: keep ownership until closure is confirmed and prove all captured
endpoints are invalid after every bounded return path.

### BFA-M2-R8-002 — Unsupported descriptor inheritance escapes bounded handling

Finding ID: BFA-M2-R8-002
Severity: major
Evidence: ValueError/TypeError/NotImplementedError from set-blocking or pass-fds
can escape raw, with setup endpoints potentially leaked.
Required outcome: convert supported capability failures to existing generic codes,
preserve privacy, and close both endpoints in check and publish modes.

## Prior-finding reconciliation

BFA-M2-R5-001 and BFA-M2-R6-001 are resolved by the parent-owned pipe and exact
bounded record parsing. BFA-M2-R7-001 remains open through endpoint ownership.
BFA-M2-R1-002 and BFA-M2-R2-001 remain open through unsupported capability
handling. Other M2 findings remain resolved.

## Validation evidence

The 18 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Injected close and platform
capability probes reproduced both findings.
