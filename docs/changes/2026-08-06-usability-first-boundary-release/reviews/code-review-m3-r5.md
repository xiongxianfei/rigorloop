# Usability-First Boundary-First v0.4.0 Code Review M3 R5

Review ID: code-review-m3-r5
Stage: code-review
Round: 5
Reviewer: Codex independent blind-first code-review peer
Target: ef125d5f75b2fc3bb9fd36a75bfe06a613cbd31d..8fde262c with cumulative M3 c7b0babe..8fde262c
Reviewed artifact: commit 8fde262c
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-r4-resolution
Reviewer context ID: m3-r5-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: complete-gate-inventory; exact-row-cardinality; state-specific-result-vocabulary; emergency-deferral-authority; prior-finding-reconciliation
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; specs/release-process-contract.md; specs/release-process-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@8fde262c#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@8fde262c#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@8fde262c#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@8fde262c#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@8fde262c#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@8fde262c#sha256:d7e73c2f1e6af91682581e3bf3f76f4f472e9dd21d036e413ad331857002e03a; range:ef125d5f75b2fc3bb9fd36a75bfe06a613cbd31d..8fde262c.diff@8fde262c#sha256:d75cd46b98bbe8dbf630a758c477bc5c3566d8d0985fd9f9aec44551fa8743af
Prompt template version: code-review-v1
Initial packet hash: sha256:d75cd46b98bbe8dbf630a758c477bc5c3566d8d0985fd9f9aec44551fa8743af
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: complete, unambiguous, and state-correct release evidence before preservation or public closeout
Highest-impact failure modes: emergency gate omission; unsupported deferral; inapplicable public proof; contradictory duplicate rows; whitespace-only smoke evidence
Changed boundaries: BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001; INT-002; INT-003
Evidence expected: complete routine and emergency row mutation matrices; state-specific allowed-result proof; prior-finding reproductions; focused release gates
Areas requiring direct inspection: governed row inventories; table cardinality; result vocabularies; emergency deferral binding; preservation predicates; mutation tests
Areas intentionally out of scope: M4 active snapshot; live publication; final holistic review; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; pending-public-separation=applicable; emergency-recovery=applicable; compatibility=applicable; generated-artifact-currency=applicable; live-publication=not-applicable:out-of-scope-M3
Falsifiable review questions: Does every governed row appear exactly once across routine and emergency states? Can unsupported, inapplicable, or unbound deferred results pass? Can whitespace-only proof pass? Do prior identity and public-state safeguards remain intact?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r5.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/artifact_lifecycle_validation.py; scripts/release_transaction.py; scripts/test-artifact-lifecycle-validator.py; scripts/test-release-transaction.py; docs/releases/v0.4.0.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*
Requirement-fidelity matched category triggers: spec-derived validators; metadata validators; closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M3-CR5-001
Material findings: UBR-M3-CR5-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR5-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR5-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r5.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR5-001
- Verify readiness: not-claimed

## Finding UBR-M3-CR5-001

Finding ID: UBR-M3-CR5-001
Severity: blocker
Location: `scripts/artifact_lifecycle_validation.py:125-137`; `scripts/artifact_lifecycle_validation.py:672-716`; `scripts/test-artifact-lifecycle-validator.py:297-328`; `scripts/test-artifact-lifecycle-validator.py:3222-3267`
Evidence: The shared checklist skips all ten preflight cardinality and result checks whenever release type or status marks emergency evidence. Direct mutations removed, duplicated, or assigned unsupported `banana` to each governed row; all 30 emergency mutations passed. The registry matrix accepts `not-applicable` for all five rows even in finalized published npm/CLI evidence, and emergency evidence accepts `deferred` for dist-tag, integrity, fresh install, and CLI/npx rows without binding those results to the named emergency deferral. REL-R14, REL-R63, and AC-REL-005 require every non-deferred emergency gate to pass; REL-R64, REL-R70, and REL-R72 keep registry verification mandatory and permit only fresh-install smoke to be deferred with matching owner-approved evidence.
Required outcome: Enforce exact-one cardinality for all ten preflight rows and all five registry rows in pending, finalized, and emergency states. Derive supported results from release state and applicability: npm build and local packed-install proof cannot be `not-applicable` for this npm release; finalized public registry authority cannot be entirely `not-applicable`; emergency non-deferred gates must pass; and only an applicable fresh-install smoke result may be deferred when it is exactly bound to a complete emergency-deferral row.
Safe resolution path: Replace the emergency bypass and unconditional result sets with one state/applicability-aware row contract, cross-check every deferred result against exactly one complete emergency deferral, and add exhaustive pending/finalized/emergency missing, duplicate, unsupported, not-applicable, and deferred mutation tests across all 15 governed rows.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M3-CR4-001: partially resolved. All ten routine preflight rows and all five registry rows now reject missing and duplicate evidence; routine pending/finalized unsupported values reject; whitespace-only passing smoke fields reject. Emergency preflight and state-specific allowed-result authority remain open as UBR-M3-CR5-001.
- UBR-M3-CR3-001: resolved. Exact finalized manifest identity and nonblank passing-smoke semantics remain enforced.
- UBR-M3-CR2-001: resolved. Requested tag, hosted ref name, dereferenced tag commit, trusted workflow commit, and checked HEAD remain one exact identity.
- UBR-M3-CR2-002: resolved for pending/public standing-state separation. Premature public state and incomplete standing evidence remain rejected; R5's distinct shared finalized/emergency result-authority gap is UBR-M3-CR5-001.
- UBR-M3-CR1-001 through UBR-M3-CR1-004: resolved. Final-tree preparation, profile-owned `latest`, independent trusted commit authority, and the standing record remain intact.

## First-pass checklist

- Spec alignment: block. Emergency and public-result acceptance violates REL-R14, REL-R63, REL-R64, REL-R70, REL-R72, AC-REL-005, UBR-R011, UBR-R012, and AC-UBR-007.
- Test coverage: concern. Routine pending/finalized cardinality and smoke whitespace have direct tests, but emergency row inventories, state-specific applicability, and deferral binding do not.
- Edge cases: block. Emergency omission, unsupported result, inapplicable public proof, and unbound deferral pass.
- Error handling: block. The emergency branch suppresses the checks instead of producing bounded errors.
- Architecture boundaries: pass. The correction stays inside the standing routine release path and adds no publisher.
- Compatibility: concern. The shared standing release-evidence validator still accepts states forbidden by its existing contract.
- Security/privacy: pass. Secret/private-state checks remain active and both focused suites pass.
- Derived artifact currency: pass. Exact preparation and preflight pass on the reviewed tree.
- Unrelated changes: pass. The correction range is limited to the accepted R4 resolution and its evidence.
- Validation evidence: concern. The cited suites pass, but direct adversarial matrices contradict the claimed complete state coverage.

## Independent validation

- `git diff --check ef125d5f75b2fc3bb9fd36a75bfe06a613cbd31d..8fde262c` — pass.
- `python scripts/test-release-transaction.py` — pass, 102 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — pass, 162 tests.
- `python scripts/prepare-release.py v0.4.0 --check` — pass; no changes.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass with one pre-existing report-only literal warning.
- Direct 10-row preflight matrix — pending and finalized reject every missing, duplicate, and unsupported mutation; emergency accepts all 30 mutations.
- Direct 5-row registry matrix — routine rejects every missing, duplicate, unsupported, and deferred mutation; emergency rejects missing/duplicate/unsupported but accepts four deferred rows.
- Direct allowed-result matrix — pending and finalized npm evidence accepts `not-applicable` for package build and local packed-install smoke; finalized published npm/CLI evidence accepts `not-applicable` for all five registry rows.
- Prior-safeguard inspection and suite regressions — exact lightweight/annotated hosted-tag identity, manifest binding, premature-public rejection, complete standing record, and whitespace-only passing-smoke rejection remain effective.

The expensive release-selected CI and full package gate were not repeated after the deterministic state-matrix probe established a blocker; their package-parity success cannot cure the release-evidence authority gap.

## Handoff

M3 remains open. Resolve UBR-M3-CR5-001, rerun the focused lifecycle and transaction suites plus exhaustive state matrices, then request independent M3 R6 review. M4 remains planned and must not start.
