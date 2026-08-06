# Usability-First Boundary-First v0.4.0 Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex independent blind-first code-review peer
Target: 9502421a..52c2beba
Reviewed artifact: commit 52c2beba with cumulative M2 context
Reviewed milestone: M2
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m2-r1-resolution
Reviewer context ID: m2-r2-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: git-environment-authority; checked-revision-activation; private-output-control
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@52c2beba#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@52c2beba#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@52c2beba#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@52c2beba#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@52c2beba#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@52c2beba#sha256:afee20b29f7537f562d05c26b25efd4b43a98ecfeed583334b1a3eb62aee6e64; range:9502421a..52c2beba.diff@52c2beba#sha256:cb9547f6991da89b4381379b5566a761a0a326b6cb67c5a562897867c7e82e4f
Prompt template version: code-review-v1
Initial packet hash: sha256:cb9547f6991da89b4381379b5566a761a0a326b6cb67c5a562897867c7e82e4f
Manifest owner: code-review
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: derivation repository authority and Git subprocess output control
Highest-impact failure modes: ambient GIT_DIR redirects root; trace variables write private output; config injection changes object authority
Changed boundaries: BND-STATE-001; BND-ENV-001; INT-002
Evidence expected: restricted Git environment; root-redirection failure; no trace output; prior-finding reconciliation; full M2 gates
Areas requiring direct inspection: derivation environment construction; every derivation Git subprocess
Areas intentionally out of scope: M3; M4; final holistic review; public release actions
Risk classes considered: requirement-fidelity=applicable; checked-revision-activation=applicable; git-object-identity=applicable; privacy=applicable; public-release-mutation=not-applicable:out-of-scope-M3
Falsifiable review questions: Can GIT_DIR redirect an empty supplied root? Can ambient Git trace variables create output? Do all R1 reproductions remain resolved?
Confidence: high
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m2-r2.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/test-boundary-first-validation.py
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M2-CR2-001
Material findings: UBR-M2-CR2-001
Immediate next stage: review-resolution
Automatic downstream handoff: none
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Finding UBR-M2-CR2-001

Finding ID: UBR-M2-CR2-001
Severity: blocker
Location: `scripts/boundary_first_validation.py:1147-1149`
Evidence: Derivation copies all of `os.environ`. With an empty supplied root and ambient `GIT_DIR` pointing at this repository, it returned the repository inventory instead of a bounded unavailable-baseline issue. Ambient Git trace/output and config-injection variables are also inherited.
Required outcome: The supplied root and exact commit exclusively own derivation; ambient Git variables cannot redirect object authority or create output.
Safe resolution path: Use a restricted subprocess environment containing only required executable/locale inputs plus no-replacement, no-lazy-fetch, and no-system/global-config guards. Regress `GIT_DIR` redirection and trace-file creation.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M2-CR1-001: resolved; private activation paths remain suppressed.
- UBR-M2-CR1-002: replacement refs and lazy fetch are guarded, but ambient repository authority remains; the residual is UBR-M2-CR2-001.
- UBR-M2-CR1-003: resolved; tracked v0.3.6 bytes and identities are pinned.
- UBR-M2-CR1-004: resolved; malformed state types fail closed.

## Validation evidence

The 61-test boundary suite, selector suite, focused check, explicit selector, py_compile, and both correction/cumulative diff checks pass. A direct ambient-`GIT_DIR` reproduction establishes the residual finding.

## Handoff

M2 remains open. Resolve UBR-M2-CR2-001 and rerun independent review before M3.
