# Code Review: M2 R3

Review ID: code-review-m2-r3
Stage: code-review
Round: 3
Reviewer: two independent L2 Codex reviewers
Target: 9f3b59cb..e4fa9e34
Reviewed artifact: M2 R2 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r2
Reviewer context ID: m2-r3-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: diagnostic provenance; private runtime values; replacement history
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@e4fa9e34#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@e4fa9e34#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@e4fa9e34#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@e4fa9e34#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:9f3b59cb..e4fa9e34.diff@e4fa9e34#sha256:0991377775b34183bf919a831f905df8ee9535634b5602360cd49abdcba7a531
Initial packet hash: sha256:0991377775b34183bf919a831f905df8ee9535634b5602360cd49abdcba7a531
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: diagnostic provenance and replacement-candidate recovery
Highest-impact failure modes: provider-forged context, private-runtime disclosure, and replacement from wrong P
Changed boundaries: BND-AUTH-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: authenticated local guard result; private-runtime collision suppression; same-P replacement history
Areas requiring direct inspection: stderr marker parsing; context filtering; replacement ancestry
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: privacy; provenance; identity; recovery; evidence fidelity
Falsifiable review questions: can remote stderr forge a guard result; can env values leak as SHAs; does replacement descend exact P and exclude rejected T
Material findings: BFA-M2-R3-001, BFA-M2-R3-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R3-001 — Provider output can forge trusted diagnostic context

Finding ID: BFA-M2-R3-001
Severity: major
Evidence: unanchored parsing accepts a remote hook's guard-shaped stderr and a
syntactically valid 40-hex private environment value can serialize as identity.
Required outcome: accept classifications only from an authenticated local-hook
line and suppress identity values colliding with bounded private runtime data.

### BFA-M2-R3-002 — Replacement fixture does not preserve authorized P

Finding ID: BFA-M2-R3-002
Severity: major
Evidence: the replacement uses an unrelated repository whose P differs and does
not contain the rejected P or prove transition exclusion/count.
Required outcome: rebuild from the same remote's exact P, prove one new T,
exclude rejected T from first-parent history, and validate full readiness.

## Prior-finding reconciliation

BFA-M2-R1-002, BFA-M2-R1-003, BFA-M2-R2-001, and BFA-M2-R2-002 remain open
through these failed-remediation findings. Path authority, CAS mapping, real
atomic-capability failure, selective-ref atomicity, and post-push reconciliation
are otherwise resolved.

## Validation evidence

The 14 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. Reviewer adversarial probes
reproduced both provenance gaps.
