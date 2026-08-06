# Code Review: M2 R7

Review ID: code-review-m2-r7
Stage: code-review
Round: 7
Reviewer: two independent L2 Codex reviewers
Target: e206aa32..cadfb349
Reviewed artifact: M2 R6 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r6
Reviewer context ID: m2-r7-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: mutable local authority channel; close failures; concurrent rewrite
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@cadfb349#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@cadfb349#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@cadfb349#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@cadfb349#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:e206aa32..cadfb349.diff@cadfb349#sha256:e9362d49d379888f196bc48954daf0b203cd4925d61dd214e1720bf894280d08
Initial packet hash: sha256:e9362d49d379888f196bc48954daf0b203cd4925d61dd214e1720bf894280d08
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: stability and closure of local guard-result authority
Highest-impact failure modes: same-size rewrite substitutes classification and close error escapes bounded handling
Changed boundaries: BND-AUTH-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: immutable parent-owned channel, close-error fallback, and substitution rejection
Areas requiring direct inspection: authority transport lifecycle and bounded parser
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: concurrency; parsing; provenance; liveness; privacy
Falsifiable review questions: can a mutable file rewrite or close error alter/escape the result
Material findings: BFA-M2-R7-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### BFA-M2-R7-001 — Mutable result transport cannot prove stable bounded authority

Finding ID: BFA-M2-R7-001
Severity: major
Evidence: a same-length concurrent rewrite can preserve compared metadata and
substitute a valid result; an injected descriptor-close error escapes raw.
Required outcome: replace mutable pathname authority with a parent-owned bounded
channel, and make read/close/malformed outcomes generic and private-safe.

## Prior-finding reconciliation

BFA-M2-R6-002 is resolved by current R7 evidence. BFA-M2-R1-002,
BFA-M2-R2-001, BFA-M2-R5-001, and BFA-M2-R6-001 remain open through this
transport finding. Other M2 findings remain resolved.

## Validation evidence

The 18 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Same-size substitution and
descriptor-close probes reproduced the remaining gap.
