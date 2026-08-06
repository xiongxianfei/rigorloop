# Usability-First Boundary-First v0.4.0 Code Review M3 R3

Review ID: code-review-m3-r3
Stage: code-review
Round: 3
Reviewer: Codex independent blind-first code-review peer
Target: b7ede777..973009b8 with cumulative M3 c7b0babe..973009b8
Reviewed artifact: commit 973009b8
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-r2-resolution
Reviewer context ID: m3-r3-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: finalized-evidence-preservation; pending-preflight-completeness; manifest-identity; prior-finding-reconciliation
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@973009b8#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@973009b8#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@973009b8#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@973009b8#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@973009b8#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@973009b8#sha256:c39837de4c6b3f7634ba38679c32a0a9efbe106dae6b1e0ab63cb73938bcac93; range:b7ede777..973009b8.diff@973009b8#sha256:73dbf81c99fbdca35674cc335136f3b5daacb0c3349f7f6a38a5dfa5b84d4746
Prompt template version: code-review-v1
Initial packet hash: sha256:73dbf81c99fbdca35674cc335136f3b5daacb0c3349f7f6a38a5dfa5b84d4746
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: complete pending preflight evidence and finalized release YAML preservation
Highest-impact failure modes: missing gate rows; stale manifest identity; empty passing smoke evidence; false preparation currency
Changed boundaries: BND-AUTH-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-002; INT-003
Evidence expected: per-row preflight mutations; exact manifest identity; semantic smoke proof; final preparation; both release gates
Areas requiring direct inspection: lifecycle checklist; release preparation predicates; pending validation; release metadata; regressions
Areas intentionally out of scope: M4 active snapshot; live publication; final holistic review; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; generated-artifact-currency=applicable; pending-public-separation=applicable; compatibility=applicable; live-publication=not-applicable:out-of-scope-M3
Falsifiable review questions: Can a pending record omit one gate row? Can a bogus manifest be preserved? Can passing smoke evidence be empty? Do exact tag and registry checks remain enforced?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r3.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/artifact_lifecycle_validation.py; scripts/release_transaction.py; scripts/release-verify.sh; scripts/adapter_distribution.py; scripts/test-release-transaction.py; docs/releases/v0.4.0.md
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
Compressed requirement risk: UBR-M3-CR3-001
Material findings: UBR-M3-CR3-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR3-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR3-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r3.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR3-001
- Verify readiness: not-claimed

## Finding UBR-M3-CR3-001

Finding ID: UBR-M3-CR3-001
Severity: blocker
Location: `scripts/artifact_lifecycle_validation.py:657-667`; `scripts/release_transaction.py:2013-2129`; `scripts/test-release-transaction.py:586-646`
Evidence: Pending checklist validation skips the complete routine preflight row inventory. Isolated finalized YAML with `manifest_version: bogus` or empty passing smoke evidence also passes preparation and preflight.
Required outcome: Pending standing evidence contains every required gate row with a supported state; finalized release YAML binds the expected manifest and semantic passing smoke evidence.
Safe resolution path: Always enumerate required gate rows with parameterized allowed results; validate expected manifest identity and passing smoke semantics; add per-row, bogus-manifest, empty-evidence, and unknown-result regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M3-CR2-001: resolved; exact release, ref, tag, HEAD, and trusted commit identity is enforced and tested.
- UBR-M3-CR2-002: failed-remediation; public state and major sections are now enforced, but complete preflight rows and finalized YAML semantics still fail open.

## Checklist coverage

- Spec alignment, test coverage, edge cases, error handling, architecture boundaries, and generated currency: block on UBR-M3-CR3-001.
- Compatibility, security/privacy, and unrelated-change scope: pass.
- Validation evidence: credible happy path but insufficient against the reproduced mutations.

## Independent validation

- `python scripts/test-release-transaction.py` — pass, 96 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — pass, 162 tests.
- `python scripts/prepare-release.py v0.4.0 --check` — pass on the unmutated tree.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass on the unmutated tree.
- `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.4.0` — pass.
- `git diff --check` and `git status --short` — pass and clean.
- Direct missing-row, bogus-manifest, empty-evidence, and registry-state mutations reproduced the finding.

## Handoff

M3 remains open. Record and resolve UBR-M3-CR3-001, rerun the complete M3 command set, and request independent M3 R4 review.
