# Usability-First Boundary-First v0.4.0 Code Review M3 R6

Review ID: code-review-m3-r6
Stage: code-review
Round: 6
Reviewer: Codex independent blind-first code-review peer
Target: 4104462e8e180e585d2da1479ecd5c233f874e81..d63e7eee with cumulative M3 c7b0babe..d63e7eee
Reviewed artifact: commit d63e7eee
Reviewed milestone: M3
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m3-r5-resolution
Reviewer context ID: m3-r6-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: three-state-row-matrix; emergency-deferral-completeness; closed-status-vocabulary; historical-release-compatibility; prior-finding-reconciliation
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; specs/release-process-contract.md; specs/release-process-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@d63e7eee#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@d63e7eee#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@d63e7eee#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@d63e7eee#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@d63e7eee#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@d63e7eee#sha256:7be1a5d50b7424cde90abc1a5641f50335157722d185d013f423ed5bb247c2fd; range:4104462e8e180e585d2da1479ecd5c233f874e81..d63e7eee.diff@d63e7eee#sha256:e9689495df64c64cd7a7c2c52735f8ea73884e5fccab5312095e5fa2d1cab870
Prompt template version: code-review-v1
Initial packet hash: sha256:e9689495df64c64cd7a7c2c52735f8ea73884e5fccab5312095e5fa2d1cab870
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: state-correct release evidence and owner-approved emergency deferral authority
Highest-impact failure modes: omitted or duplicate rows; unsupported results; unknown status; incomplete or contradictory deferral authority; historical evidence rejection
Changed boundaries: BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003
Evidence expected: exhaustive three-state row matrices; exact deferral completeness and binding probes; closed-status proof; historical record validation; prior-safeguard regressions
Areas requiring direct inspection: row contracts; status vocabulary; deferral fields and sentinels; one-to-one binding; historical records; preparation; trusted identity tests
Areas intentionally out of scope: M4 active snapshot; live publication; final holistic review; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; pending-public-separation=applicable; emergency-recovery=applicable; compatibility=applicable; generated-artifact-currency=applicable; live-publication=not-applicable:out-of-scope-M3
Falsifiable review questions: Do all fifteen rows have exact state authority? Is fresh-install smoke bound to one genuinely complete deferral row? Do unknown status and historical evidence behave correctly? Do prior safeguards remain intact?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m3-r6.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/artifact_lifecycle_validation.py; scripts/test-artifact-lifecycle-validator.py; docs/releases/v0.4.0.md
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
Compressed requirement risk: UBR-M3-CR6-001
Material findings: UBR-M3-CR6-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M3-CR6-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M3-CR6-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m3-r6.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M3-CR6-001
- Verify readiness: not-claimed

## Finding UBR-M3-CR6-001

Finding ID: UBR-M3-CR6-001
Severity: blocker
Location: `scripts/artifact_lifecycle_validation.py:610-651`; `scripts/artifact_lifecycle_validation.py:754-775`; `scripts/test-artifact-lifecycle-validator.py:3350-3380`
Evidence: Row-label binding is exact, but required deferral fields reuse the generic blank predicate, which treats `not-applicable` as substantive. Direct mutations replaced each of approving owner, emergency rationale, reason, validation impact, risk accepted, follow-up location, deadline, and status with `not-applicable`; all eight incomplete emergency records passed. A `none` sentinel row also passed alongside the real fresh-install deferral, contradicting the record's declaration that no deferral exists. REL-R14, REL-R14a, and REL-R63 require actual owner approval, rationale, impact, risk, follow-up, and deadline evidence for every deferred gate.
Required outcome: A matching fresh-install deferral must contain substantive, non-placeholder values in every required field and must be the sole semantic deferral row; `none` may appear only when no deferred result or real deferral exists. The active deferred record status must use its supported open-state value rather than an arbitrary nonblank value.
Safe resolution path: Add a deferral-specific placeholder predicate and closed deferral-status vocabulary, reject `none` mixed with real deferrals, and extend the binding test across every required field and sentinel combination.
Named inputs: Emergency Deferrals table rows and normalized deferred registry results.
Named outputs: Bounded checklist errors or one valid exactly-bound fresh-install deferral.
Forbidden paths: release publication code, profiles, workflow publication wiring, feature spec, architecture, plan, and historical release records.
Acceptance criteria: every required-field empty/placeholder mutation fails; unknown or terminal-without-closeout status fails; `none` plus a real deferral fails; one complete open fresh-install row passes and remains bound to one deferred result.
Required validation commands: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-release-transaction.py`; direct three-state row and deferral-completeness matrices; `python scripts/prepare-release.py v0.4.0 --check`; `python scripts/release-preflight.py v0.4.0 --skip-remote`.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior-finding reconciliation

- UBR-M3-CR5-001: failed-remediation. Exact row cardinality, state-specific result vocabularies, sole fresh-install deferral selection, unknown status, and row-label binding are corrected, but the required complete owner-approved matching row remains fail-open for placeholders and contradictory `none`.
- UBR-M3-CR4-001: resolved. The complete 10-row and 5-row inventories, exact cardinality, unsupported-result rejection, and whitespace-only smoke semantics remain effective.
- UBR-M3-CR3-001: resolved. Exact manifest binding and nonblank passing-smoke evidence remain effective.
- UBR-M3-CR2-001: resolved. Requested tag, hosted ref name, dereferenced tag, trusted workflow commit, and checked HEAD remain one exact identity.
- UBR-M3-CR2-002: resolved. Pending/public standing-state separation and incomplete standing-record rejection remain effective.
- UBR-M3-CR1-001 through UBR-M3-CR1-004: resolved. Final-tree preparation, profile-owned `latest`, independent trusted commit authority, and standing release evidence remain intact.

## First-pass checklist

- Spec alignment: block. Placeholder owner/rationale/follow-up evidence violates REL-R14, REL-R14a, REL-R63, AC-REL-005, UBR-R011, and AC-UBR-007.
- Test coverage: concern. The state/result matrix is strong, but completeness tests cover empty owner only and omit placeholder values, every other required field, deferral status vocabulary, and mixed `none`.
- Edge cases: block. Placeholder-complete and contradictory-sentinel deferrals pass.
- Error handling: block. Generic blank semantics are too broad for emergency authority fields.
- Architecture boundaries: pass. The correction remains within the standing release-evidence validator and adds no publication path.
- Compatibility: pass. All nine tracked historical release records validate, including `v0.3.0` non-public evidence.
- Security/privacy: pass. Existing evidence-safety checks and the focused lifecycle suite remain effective.
- Derived artifact currency: pass. Exact preparation and preflight pass on the reviewed tree.
- Unrelated changes: pass. The correction range is limited to R5 resolution and review evidence.
- Validation evidence: concern. Both focused suites pass, but direct completeness mutations contradict the claimed complete binding proof.

## Independent validation

- `git diff --check 4104462e8e180e585d2da1479ecd5c233f874e81..d63e7eee` — pass.
- `python scripts/test-artifact-lifecycle-validator.py` — pass, 166 tests.
- `python scripts/test-release-transaction.py` — pass, 102 tests.
- `python scripts/prepare-release.py v0.4.0 --check` — pass; no changes.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass with one pre-existing report-only literal warning.
- Historical explicit-path validation — all nine tracked release records pass, including `v0.3.0` `not-published` and `v0.4.0` pending-publication evidence.
- Direct 15-row three-state matrix — all missing, duplicate, unsupported, `not-applicable`, and `deferred` outcomes match the required state matrix; only pending registry `not-applicable` and emergency fresh-install `deferred` pass.
- Direct binding matrix — missing, duplicate, and unmatched deferral labels reject, but all eight required-field `not-applicable` mutations and mixed `none` plus real-deferral evidence pass.
- Unknown `Status: banana` rejects. Whitespace passing-smoke, exact lightweight/annotated hosted-tag identity, manifest binding, incomplete standing record, and premature-public regressions pass in the focused suites.

The expensive release-selected CI and full package gate were not repeated after deterministic deferral-completeness probes established a blocker; package parity cannot supply missing owner-approved emergency evidence.

## Handoff

M3 remains open. Resolve UBR-M3-CR6-001, rerun focused suites and the complete deferral-field/sentinel matrix, then request independent M3 R7 review. M4 remains planned and must not start.
