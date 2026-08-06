# Code Review: M1 R6

Review ID: code-review-m1-r6
Stage: code-review
Round: 6
Reviewer: two independent L2 Codex reviewers
Target: 848eafe3..93f527c8
Reviewed artifact: M1 R5 correction range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-review-resolution-r5
Reviewer context ID: m1-r6-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: validator behavior; lifecycle gate; compatibility
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M1 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@93f527c8#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@93f527c8#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@93f527c8#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@93f527c8#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:848eafe3..93f527c8.diff@93f527c8#sha256:9591bb3060e566818cc584aeb9824218210a1f5ff161d259d6a7e492c772f6c5
Initial packet hash: sha256:9591bb3060e566818cc584aeb9824218210a1f5ff161d259d6a7e492c772f6c5
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: closed receipt revision authority
Highest-impact failure modes: duplicate-section or duplicate-key substitution
Changed boundaries: BND-AUTH-001; BND-STATE-001; BND-COMPAT-001
Evidence expected: duplicate-aware lexical packet proof and current receipt compatibility
Areas requiring direct inspection: invocation parser and revision binding tests
Areas intentionally out of scope: publication mutation; release payload; real transition; final verify
Risk classes considered: identity; lifecycle; compatibility
Falsifiable review questions: can duplicate sections or keys create parser/lexical disagreement
Material findings: BFA-M1-R6-001
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding

### BFA-M1-R6-001 — Duplicate inventory sections or keys bypass binding

Finding ID: BFA-M1-R6-001
Severity: major
Location: `scripts/boundary_first_validation.py` lexical packet extraction
Evidence: a valid inventory followed by a duplicate inventory containing the
same path/SHA and malformed revision was accepted; an identical duplicate
packet SHA key was also accepted.
Required outcome: reject duplicate mapping keys and inventory sections, and
require the lexical inventory body to consist only of exact packet triples.
Safe resolution path: require unique top-level keys, exactly one inventory
section, exact full-body packet consumption, and duplicate regressions.

## Reconciliation and validation

BFA-M1-R5-002 is resolved: numeric abbreviated base/head revisions pass.
BFA-M1-R5-001 remains open through this narrower duplicate ambiguity. All 87
boundary tests, 146 selector tests, strict validation, compile, exact CMD4, and
diff checks passed but omitted the duplicate cases.
