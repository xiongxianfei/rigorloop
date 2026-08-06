# Usability-First Boundary-First v0.4.0 Code Review M3 R4

Review ID: code-review-m3-r4
Stage: code-review
Round: 4
Reviewer: Codex independent blind-first code-review peer
Target: 868e1c2c..79fc68bc with cumulative M3 c7b0babe..79fc68bc
Reviewed artifact: commit 79fc68bc
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-r3-resolution
Reviewer context ID: m3-r4-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: complete-gate-inventory; exact-row-cardinality; smoke-evidence-semantics; prior-finding-reconciliation
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@79fc68bc#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@79fc68bc#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@79fc68bc#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@79fc68bc#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@79fc68bc#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@79fc68bc#sha256:b0ca5135f43ba102725baef6d0c6d5660798d14895e2303cf27fccd051f5484f; range:868e1c2c..79fc68bc.diff@79fc68bc#sha256:64fff62540e5dab0084c0151782acefb90aa41e6b8896137152fa0d3d6666abd
Prompt template version: code-review-v1
Initial packet hash: sha256:64fff62540e5dab0084c0151782acefb90aa41e6b8896137152fa0d3d6666abd
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: complete and unambiguous pending/finalized release evidence
Highest-impact failure modes: omitted gate categories; contradictory duplicate rows; whitespace-only passing proof
Changed boundaries: BND-AUTH-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-002; INT-003
Evidence expected: complete row mutation matrix; duplicate rejection; trimmed smoke semantics; release gates
Areas requiring direct inspection: governed row inventories; table parsing; preparation predicates; mutation tests
Areas intentionally out of scope: M4 active snapshot; live publication; final holistic review; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; generated-artifact-currency=applicable; pending-public-separation=applicable; compatibility=applicable; live-publication=not-applicable:out-of-scope-M3
Falsifiable review questions: Can any row be omitted or duplicated? Can unsupported states pass? Can whitespace-only passing proof be preserved?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r4.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/artifact_lifecycle_validation.py; scripts/release_transaction.py; scripts/test-release-transaction.py; docs/releases/v0.4.0.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*
Requirement-fidelity matched category triggers: spec-derived validators; metadata validators; generated-output or package parity validators; closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M3-CR4-001
Material findings: UBR-M3-CR4-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR4-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR4-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r4.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR4-001
- Verify readiness: not-claimed

## Finding UBR-M3-CR4-001

Finding ID: UBR-M3-CR4-001
Severity: blocker
Location: `scripts/artifact_lifecycle_validation.py:113-121`; `scripts/artifact_lifecycle_validation.py:574-582`; `scripts/artifact_lifecycle_validation.py:661-682`; `scripts/release_transaction.py:2055-2138`; `scripts/test-release-transaction.py:617-730`
Evidence: Three required preflight rows are absent from the governed inventory; first-match lookup accepts conflicting duplicate preflight and registry rows; whitespace-only passing smoke evidence is preserved.
Required outcome: Validate all ten routine rows and all five registry rows exactly once with supported states, and treat whitespace-only passing smoke fields as empty.
Safe resolution path: Complete the row inventory with allowed-state metadata, enforce exact cardinality, strip semantic smoke fields, and add removal/result/duplicate mutations across every row.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M3-CR3-001: failed-remediation; manifest and ordinary empty-smoke checks are fixed, but the gate inventory/cardinality and whitespace semantics remain incomplete.
- UBR-M3-CR2-001: resolved; exact hosted identity remains enforced.
- UBR-M3-CR2-002: failed-remediation through contradictory duplicate public state.

## Independent validation

- 100 release-transaction tests, 162 lifecycle tests, 149 adapter tests, preparation, preflight, dry-run release verification, diff check, and clean worktree passed.
- Complete row removal/result/duplicate, registry duplicate, manifest, and smoke whitespace probes reproduced the finding.

## Handoff

M3 remains open. Resolve UBR-M3-CR4-001, rerun the complete M3 command set, and request independent M3 R5 review.
