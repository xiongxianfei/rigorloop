# Usability-First Boundary-First v0.4.0 Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex independent blind-first code-review peer
Target: d2e3e404..56832cd5 with cumulative M3 c7b0babe..56832cd5
Reviewed artifact: commit 56832cd5
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-r1-resolution
Reviewer context ID: m3-r2-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: trusted-tag-identity; finalized-evidence-preservation; pending-public-separation; prior-finding-reconciliation
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@56832cd5#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@56832cd5#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@56832cd5#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@56832cd5#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@56832cd5#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@56832cd5#sha256:8046f56eb8de85181a1aaac1247ef52f20d248113617d57bf87c82c34e611f10; range:d2e3e404..56832cd5.diff@56832cd5#sha256:4f99f5e15d596686a1ffc311122eb54a1bc11f91fcef87567ebf51476114f2e8
Prompt template version: code-review-v1
Initial packet hash: sha256:4f99f5e15d596686a1ffc311122eb54a1bc11f91fcef87567ebf51476114f2e8
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: routine v0.4.0 identity; profile-owned dist-tag; trusted workflow binding; finalized evidence preservation; three-target package proof
Highest-impact failure modes: mixed tag identities; stale or incomplete preserved evidence; premature public claims; archive divergence; external mutation
Changed boundaries: BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003
Evidence expected: real tag fixtures; strict finalized-surface validation; pending/public state checks; archive parity; rollback proof; both release gates
Areas requiring direct inspection: release workflow; standing gate; preparation predicates; pending validation; release records; metadata; tests; activation; rollback
Areas intentionally out of scope: M4 active snapshot; live publication; final holistic review; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; trusted-release-identity=applicable; generated-artifact-currency=applicable; pending-public-separation=applicable; compatibility=applicable; privacy=applicable; live-publication=not-applicable:out-of-scope-M3
Falsifiable review questions: Can the release argument differ from the hosted tag ref and pass? Can incomplete finalized evidence be preserved? Can pending evidence claim publication without public closeout? Do package and rollback identities remain exact?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r2.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: .github/workflows/release.yml; scripts/release-verify.sh; scripts/release_transaction.py; docs/releases/v0.4.0.md; docs/releases/v0.4.0/; docs/releases/profiles/v0.4.0.yaml; packages/rigorloop/
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
Compressed requirement risk: UBR-M3-CR2-001, UBR-M3-CR2-002
Material findings: UBR-M3-CR2-001, UBR-M3-CR2-002
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR2-001, UBR-M3-CR2-002
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR2-001, UBR-M3-CR2-002
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR2-001, UBR-M3-CR2-002
- Verify readiness: not-claimed

## Finding UBR-M3-CR2-001

Finding ID: UBR-M3-CR2-001
Severity: blocker
Location: `scripts/release-verify.sh:18-45`; `scripts/test-adapter-distribution.py:5024-5054`
Evidence: Trusted tag mode does not require the explicit release argument to equal `GITHUB_REF_NAME`. An adversarial run with the ref name for one release and argument for another succeeds when both resolve to the same checked commit; tests omit successful exact light/annotated tags and mixed-name rejection.
Required outcome: Hosted tag verification proves the ref name, requested release version, dereferenced tag, checked HEAD, and trusted commit are one identity.
Safe resolution path: Require non-empty exact `GITHUB_REF_NAME`, dereference `refs/tags/${GITHUB_REF_NAME}^{commit}`, and add real Git tests for correct lightweight/annotated tags, mixed names, and wrong or rewritten tag commits.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M3-CR2-002

Finding ID: UBR-M3-CR2-002
Severity: blocker
Location: `scripts/release_transaction.py:350-397`, `scripts/release_transaction.py:1576-1586`, `scripts/release_transaction.py:1913-1968`
Evidence: Finalized standing-record detection accepts a premature `Status: published` while registry rows remain not-applicable. Release YAML preservation and pending validation accept surfaces with required tools, adapter paths, entrypoints, and validation categories removed because they rely on substring and pass-count heuristics.
Required outcome: Finalized artifact preservation and pending validation reject incomplete surfaces and every unsupported public claim.
Safe resolution path: Validate preserved release YAML and standing records with their complete schemas; enforce pending-publication and pre-public public fields; add partial, stale, and premature-publication regressions.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M3-CR1-001: resolved for the exact current tree; CR2-002 is a new fail-open classification issue.
- UBR-M3-CR1-002: resolved; profile-owned `latest` and explicit publish tagging are enforced.
- UBR-M3-CR1-003: failed-remediation; commit binding exists, but mixed ref-name/release-argument identity remains accepted.
- UBR-M3-CR1-004: resolved for presence and current completeness; CR2-002 concerns state validation and future preservation.

## Checklist coverage

- Spec alignment, tests, edge cases, error handling, architecture boundaries, and derived artifact currency: block on the two findings.
- Compatibility: pass; legacy profiles and v0.3.6 rollback remain intact.
- Security/privacy: pass for inspected evidence.
- Unrelated changes: pass; the ranges are scoped to M3.
- Validation evidence: concern; happy paths pass but omit the reproduced failures.

## Handoff

M3 remains open. Record and resolve both findings, rerun the complete M3 command set, and request independent M3 R3 review.
