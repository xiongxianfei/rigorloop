# Code Review: M2 R5

Review ID: code-review-m2-r5
Stage: code-review
Round: 5
Reviewer: two independent L2 Codex reviewers
Target: f445d5ea..11f5edd9
Reviewed artifact: M2 R4 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r4
Reviewer context ID: m2-r5-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: local result parsing; post-readiness tag race
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@11f5edd9#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@11f5edd9#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@11f5edd9#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@11f5edd9#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:f445d5ea..11f5edd9.diff@11f5edd9#sha256:238a92cc84504c8999630482bdbfb6c223313c902c5f30a8095368966c59067b
Initial packet hash: sha256:238a92cc84504c8999630482bdbfb6c223313c902c5f30a8095368966c59067b
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: bounded guard-result handling and tag-race diagnostics
Highest-impact failure modes: unbounded decode traceback and incorrect immutable-tag recovery action
Changed boundaries: BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: malformed result matrix and same/different-target tag races
Areas requiring direct inspection: descriptor parser and guard classification order
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: parsing; privacy; concurrency; recovery; identity
Falsifiable review questions: can malformed bytes escape; can same-T tag appearance be precisely diagnosed
Material findings: BFA-M2-R5-001, BFA-M2-R5-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R5-001 — Malformed local result escapes bounded handling

Finding ID: BFA-M2-R5-001
Severity: major
Evidence: invalid UTF-8 passes path/size checks and raises UnicodeDecodeError.
Required outcome: non-following descriptor reads must bound bytes, verify a regular
file, and collapse all unreadable/malformed results to generic bounded failure.

### BFA-M2-R5-002 — Same-target tag race loses conflict classification

Finding ID: BFA-M2-R5-002
Severity: major
Evidence: Git omits an already-up-to-date raced tag from hook stdin, so the guard
reports mapping-invalid before consulting the supplemental advertisement.
Required outcome: prioritize freshly advertised main drift or existing tag over
generic incomplete-mapping failure, for same-T and different-target races.

## Prior-finding reconciliation

BFA-M2-R3-001 and BFA-M2-R4-001 are resolved by the nonce-bound result channel.
BFA-M2-R1-002 and BFA-M2-R2-001 remain open through these bounded-diagnostic
edge findings. All other M2 findings remain resolved.

## Validation evidence

The 15 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Reviewer probes reproduced
invalid encoding and same-target tag-race misclassification.
