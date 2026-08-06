# Code Review: M2 R4

Review ID: code-review-m2-r4
Stage: code-review
Round: 4
Reviewer: two independent L2 Codex reviewers
Target: e1716af4..c1d6ec95
Reviewed artifact: M2 R3 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r3
Reviewer context ID: m2-r4-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: diagnostic provenance; provider privacy
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@c1d6ec95#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@c1d6ec95#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@c1d6ec95#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@c1d6ec95#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:e1716af4..c1d6ec95.diff@c1d6ec95#sha256:025e6e7c216e8108de376e2edf02f8825519914ec77559c8e87efcd256fbb172
Initial packet hash: sha256:025e6e7c216e8108de376e2edf02f8825519914ec77559c8e87efcd256fbb172
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: local guard diagnostic provenance
Highest-impact failure modes: provider-controlled stderr impersonates local guard authority
Changed boundaries: BND-AUTH-001; BND-ENV-001
Evidence expected: invocation-bound local-only result channel and provider spoof rejection
Areas requiring direct inspection: hook result transport and push failure classification
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: provenance; privacy; identity; remote mutation
Falsifiable review questions: can exact unprefixed provider stderr classify or disclose a conflict identity
Material findings: BFA-M2-R4-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### BFA-M2-R4-001 — Exact stderr shape does not authenticate local provenance

Finding ID: BFA-M2-R4-001
Severity: major
Evidence: an untrusted exact unprefixed guard-shaped stderr line is accepted as
remote-main drift and its 40-hex value is admitted as conflict context.
Required outcome: accept guard result only through an invocation-authenticated
local channel; provider stderr must remain generic and unserialized.

## Prior-finding reconciliation

BFA-M2-R1-003, BFA-M2-R2-002, and BFA-M2-R3-002 are resolved by the exact-P
replacement proof. Private-runtime collision suppression is resolved. The
remaining diagnostic-provenance portions of BFA-M2-R1-002, BFA-M2-R2-001, and
BFA-M2-R3-001 stay open through BFA-M2-R4-001.

## Validation evidence

The 14 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Both reviewers reproduced
the remaining untrusted exact-stderr substitution.
