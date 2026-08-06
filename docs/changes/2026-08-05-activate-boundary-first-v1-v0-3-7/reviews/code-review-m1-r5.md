# Code Review: M1 R5

Review ID: code-review-m1-r5
Stage: code-review
Round: 5
Reviewer: two independent L2 Codex reviewers
Target: 841b2ef4..c90c7ad3
Reviewed artifact: M1 R4 correction range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-review-resolution-r4
Reviewer context ID: m1-r5-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: validator behavior; release boundary; lifecycle gate; privacy
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M1 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@c90c7ad3#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@c90c7ad3#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@c90c7ad3#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@c90c7ad3#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:841b2ef4..c90c7ad3.diff@c90c7ad3#sha256:3ca9ff312bc19d74e1fb682a207a9f37fd5b80fa616dc0b7295537788525ce92
Initial packet hash: sha256:3ca9ff312bc19d74e1fb682a207a9f37fd5b80fa616dc0b7295537788525ce92
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: tagged readiness; receipt authority; private diagnostics
Highest-impact failure modes: malformed receipt acceptance and valid numeric revision rejection
Changed boundaries: BND-AUTH-001; BND-STATE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: tagged readiness; closed receipt matrix; numeric revisions; short-secret probes
Areas requiring direct inspection: shared authority derivation; invocation parser; runtime privacy values
Areas intentionally out of scope: publication mutation; release payload; real transition; public release; final verify
Risk classes considered: identity; lifecycle; compatibility; privacy; recovery
Falsifiable review questions: can unrelated revisions substitute; can valid numeric SHAs pass
Material findings: BFA-M1-R5-001, BFA-M1-R5-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Findings

### BFA-M1-R5-001 — Unrelated nested revision can authorize a malformed packet

Finding ID: BFA-M1-R5-001
Severity: blocker
Location: `scripts/boundary_first_validation.py` packet revision validation
Evidence: a packet with `revision: NOT-A-REVISION` passed when allowed nested
`risk_map` content supplied a four-space `revision: deadbeef` line.
Required outcome: bind lexical revision validation to each actual
`initial_packet_inventory` entry.
Safe resolution path: extract and compare each packet block rather than count
file-wide revision lines; retain closed-field checks and add the reproducer.

### BFA-M1-R5-002 — Numeric abbreviated base/head revisions are falsely rejected

Finding ID: BFA-M1-R5-002
Severity: major
Location: `scripts/boundary_first_validation.py` base/head revision validation
Evidence: unquoted `12345678` and `87654321` are valid hexadecimal
abbreviations but parse as YAML integers and fail the string type requirement.
Required outcome: validate base/head identities lexically as 8–64 hexadecimal
characters regardless of YAML scalar coercion.
Safe resolution path: bind raw top-level fields to parsed keys and add numeric
abbreviation positive cases plus malformed negatives.

## R4 reconciliation

- BFA-M1-R4-001 resolved: tagged readiness passes and candidate mode still
  rejects the same tag.
- BFA-M1-R4-002 resolved for current accepted receipts; R5 findings separately
  cover malformed substitution and numeric-scalar compatibility.
- BFA-M1-R4-003 resolved: short PIN, API-key, and auth-code values redact.

## Validation evidence

CMD1 passed 86 tests; CMD2, CMD3, exact CMD4, selector regression (146 tests),
and `git diff --check` passed. Those results omit the two parser reproductions.
