# Code Review: M2 R6

Review ID: code-review-m2-r6
Stage: code-review
Round: 6
Reviewer: two independent L2 Codex reviewers
Target: e0a258b3..aebfc98c
Reviewed artifact: M2 R5 correction range
Reviewed milestone: M2
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r5
Reviewer context ID: m2-r6-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: non-regular local result; concurrent mutation; durable evidence
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@aebfc98c#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@aebfc98c#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@aebfc98c#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@aebfc98c#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:e0a258b3..aebfc98c.diff@aebfc98c#sha256:9ddadbc436caeff342e64043be4fc2915f3049e2412d5140407e9c6125a41b51
Initial packet hash: sha256:9ddadbc436caeff342e64043be4fc2915f3049e2412d5140407e9c6125a41b51
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: prompt bounded parsing of local result objects
Highest-impact failure modes: FIFO hang, truncated record acceptance, and stale evidence claim
Changed boundaries: BND-RECOVERY-001; BND-ENV-001
Evidence expected: FIFO/truncation/growth/path-replacement parser matrix
Areas requiring direct inspection: open flags, descriptor metadata, exact record grammar, evidence outcome
Areas intentionally out of scope: release payload; configured external publication; final verify
Risk classes considered: liveness; parsing; TOCTOU; privacy; evidence fidelity
Falsifiable review questions: can non-regular open block; can incomplete record authorize; can concurrent mutation pass
Material findings: BFA-M2-R6-001, BFA-M2-R6-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M2-R6-001 — Non-regular or truncated guard results are not bounded

Finding ID: BFA-M2-R6-001
Severity: major
Evidence: O_RDONLY blocks on a FIFO before fstat, and the optional newline admits
a truncated record that the hook never completed.
Required outcome: use nonblocking/no-follow open, exact completed records, and
stable descriptor metadata/length across the bounded read.

### BFA-M2-R6-002 — M2 evidence outcome is stale

Finding ID: BFA-M2-R6-002
Severity: minor
Evidence: the proof reflects R6/17 tests but the outcome still names R5.
Required outcome: align the durable outcome and retain only directly proved claims.

## Prior-finding reconciliation

BFA-M2-R5-002 is resolved by precise same/different-target tag-race tests.
BFA-M2-R1-002, BFA-M2-R2-001, and BFA-M2-R5-001 remain open through
BFA-M2-R6-001. Other M2 findings remain resolved.

## Validation evidence

The 17 publication tests, 147 selector tests, compilation, strict boundary
validation, explicit selector, and range diff passed. FIFO probes timed out and
truncated-result probes were accepted; other malformed partitions failed safely.
