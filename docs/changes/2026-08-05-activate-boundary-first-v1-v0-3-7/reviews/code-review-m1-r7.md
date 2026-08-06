# Code Review: M1 R7

Review ID: code-review-m1-r7
Stage: code-review
Round: 7
Reviewer: two independent L2 Codex reviewers
Target: 5d465a20..bab0395f
Reviewed artifact: M1 R6 correction range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-review-resolution-r6
Reviewer context ID: m1-r7-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: validator behavior; lifecycle authority; compatibility
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M1 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@bab0395f#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@bab0395f#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@bab0395f#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@bab0395f#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:5d465a20..bab0395f.diff@bab0395f#sha256:2466ad73f00f758d81e72310b7080a9d15c201c0d093be713a1ae08a0635cd60
Initial packet hash: sha256:2466ad73f00f758d81e72310b7080a9d15c201c0d093be713a1ae08a0635cd60
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: closed lifecycle receipt uniqueness
Highest-impact failure modes: parser-equivalent duplicate keys and contradictory duplicate paths
Changed boundaries: BND-AUTH-001; BND-STATE-001; BND-COMPAT-001
Evidence expected: parser-equivalent duplicate rejection and unique packet paths
Areas requiring direct inspection: top-level key normalization and packet tuple validation
Areas intentionally out of scope: publication mutation; release payload; real transition; final verify
Risk classes considered: identity; lifecycle; compatibility
Falsifiable review questions: can spaced duplicate keys or repeated paths pass
Material findings: BFA-M1-R7-001, BFA-M1-R7-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M1-R7-001 — Parser-equivalent spaced duplicate keys bypass detection

Finding ID: BFA-M1-R7-001
Severity: major
Evidence: `base_revision :`, `head_revision :`, and
`initial_packet_inventory :` are normalized by the parser but not recognized by
the duplicate-key regex, allowing lexical and parsed authorities to diverge.
Required outcome: duplicate detection must use parser-equivalent key syntax.

### BFA-M1-R7-002 — Duplicate packet paths permit contradictory identities

Finding ID: BFA-M1-R7-002
Severity: major
Evidence: two fully valid triples with the same path and conflicting revision
or SHA values are consumed and accepted.
Required outcome: every inventory packet path must be unique.

## Validation evidence

The 87 boundary tests, 146 selector tests, strict validation, compilation,
exact CMD4, and diff checks passed but omitted these two variants.
