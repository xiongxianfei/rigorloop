# Code Review: M2 R10

Review ID: code-review-m2-r10
Stage: code-review
Round: 10
Reviewer: two independent L2 Codex reviewers
Target: 9b000631..62a41087
Reviewed artifact: M2 R9 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r9
Reviewer context ID: m2-r10-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: terminal descriptor ownership; post-push uncertainty
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@62a41087#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@62a41087#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@62a41087#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@62a41087#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:9b000631..62a41087.diff@62a41087#sha256:ddb60664f0343fcae2e31bed722abea26dd16af38a5f5bf325760b75719688bd
Initial packet hash: sha256:ddb60664f0343fcae2e31bed722abea26dd16af38a5f5bf325760b75719688bd
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: terminal endpoint cleanup and post-push classification
Highest-impact failure modes: live endpoints after retry exhaustion; successful publication misclassified as retryable failure
Changed boundaries: BND-RECOVERY-001; BND-ENV-001
Evidence expected: no live local transport authority and phase-correct post-push reconciliation
Areas requiring direct inspection: retry exhaustion, successful-push cleanup, confirmation
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: resource ownership; external mutation; recovery guidance; privacy
Falsifiable review questions: can persistent cleanup return live endpoints; can post-success cleanup suggest rerun
Material findings: BFA-M2-R10-001, BFA-M2-R10-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R10-001 — Retry exhaustion returns with live endpoints

Finding ID: BFA-M2-R10-001
Severity: major
Evidence: `_close_descriptors` stops after three attempts. Persistent close
failure with unavailable fallback leaves both descriptors valid on setup,
failed-push, and nominal-success paths; tests cover only transient recovery.
Required outcome: no path may return live parent-owned transport authority;
remove, invalidate, or transfer terminal ownership and prove exhaustion behavior.

### BFA-M2-R10-002 — Post-success cleanup uses pre-publication recovery

Finding ID: BFA-M2-R10-002
Severity: major
Evidence: cleanup exhaustion after `git push` success raises
`atomic-publication-failed` before fresh confirmation. That code permits rerun
even though external mutation may already have happened.
Required outcome: preserve confirmation after successful push or emit the
existing stop-and-reconcile/no-rerun post-push result.

## Prior-finding reconciliation

EBADF-only verification and ordinary unsupported capability handling are fixed.
BFA-M2-R7-001, BFA-M2-R8-001, BFA-M2-R8-002, and BFA-M2-R9-001 remain open
where terminal ownership is still live. Both reviewers reproduced the terminal
defect; the second reviewer combined its post-success impact into R10-001.

## Validation evidence

The 19 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, review-structure validation, metadata validation,
and range diff passed. Independent persistent-failure probes reproduced both
findings.
