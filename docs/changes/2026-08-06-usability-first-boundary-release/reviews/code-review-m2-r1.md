# Usability-First Boundary-First v0.4.0 Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: ab281b39..3827623e
Reviewed artifact: commit 3827623e
Reviewed milestone: M2
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m2-implementation
Reviewer context ID: m2-r1-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: checked-revision-activation; git-object-identity; rollback-authority; private-diagnostic-output
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@3827623e#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@3827623e#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@3827623e#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@3827623e#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@3827623e#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@3827623e#sha256:e415f66db3f033ef500a94c42c74a851f35fc16519623afac38f461abbe90b6c; range:ab281b39..3827623e.diff@3827623e#sha256:a086480838493c8cdf631148326a385a3c6b036898298887a186ad038dfe78dc
Prompt template version: code-review-v1
Initial packet hash: sha256:a086480838493c8cdf631148326a385a3c6b036898298887a186ad038dfe78dc
Manifest owner: code-review
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: checked-revision activation; exact one-time derivation; rollback selection; private diagnostics; custom-path retirement
Highest-impact failure modes: private path disclosure; replacement-ref substitution; lazy object fetch; synthetic rollback proof; malformed state exception
Changed boundaries: BND-STATE-001; BND-COMPAT-001; BND-RECOVERY-001; BND-ENV-001; INT-002; INT-003
Evidence expected: current-file-only validation; exact no-replacement derivation; repository no-write proof; tracked v0.3.6 metadata; private path suppression; malformed-type regression; retained selector checks
Areas requiring direct inspection: activation parsing; Git subprocesses; rollback fixture construction; CLI serialization; closed vocabularies; retired selector paths
Areas intentionally out of scope: M3; M4; final holistic review; public release actions
Risk classes considered: requirement-fidelity=applicable; checked-revision-activation=applicable; git-object-identity=applicable; compatibility=applicable; privacy=applicable; public-release-mutation=not-applicable:out-of-scope-M3; registry-availability=not-applicable:out-of-scope-M3
Falsifiable review questions: Can a private root path reach CLI output? Can a replacement ref alter derivation for one baseline identity? Does rollback proof read the tracked v0.3.6 record? Can a malformed activation state raise instead of returning an issue?
Confidence: high
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m2-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/validate-boundary-first.py; scripts/test-boundary-first-validation.py; scripts/validation_selection.py; scripts/test-select-validation.py
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*
Requirement-fidelity matched category triggers: spec-derived validators; closed enums
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M2-CR1-001 through UBR-M2-CR1-004
Material findings: UBR-M2-CR1-001, UBR-M2-CR1-002, UBR-M2-CR1-003, UBR-M2-CR1-004
Immediate next stage: review-resolution
Automatic downstream handoff: none
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Open blockers: UBR-M2-CR1-001 through UBR-M2-CR1-004
- Next stage: review-resolution
- Review status: changes-requested
- Recording status: recorded
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Verify readiness: not-claimed

## Finding UBR-M2-CR1-001

Finding ID: UBR-M2-CR1-001
Severity: blocker
Location: `scripts/boundary_first_validation.py:841-849`
Evidence: Missing, parse, and shape errors use the absolute input path. Running the CLI with a sentinel temporary `--root` prints that machine-local path in serialized output.
Required outcome: Activation diagnostics identify only the repository-relative authoritative surface and never expose a machine-local root.
Safe resolution path: Use `ACTIVATION_RECORD.as_posix()` for activation-record diagnostics and add structured and CLI privacy regressions with a sentinel root.
needs-decision rationale: none
auto_fix_class: mechanical

## Finding UBR-M2-CR1-002

Finding ID: UBR-M2-CR1-002
Severity: blocker
Location: `scripts/boundary_first_validation.py:1138-1223`
Evidence: Ordinary Git object resolution honors `refs/replace`. A replacement ref changed the inventory returned for the same exact 40-character baseline from `specs/alpha.md` to `specs/beta.md`; object reads also lack an explicit no-lazy-fetch guard.
Required outcome: Derivation binds to the named commit's real object graph, disables replacement refs and lazy fetch for every Git read, and remains repository-read-only.
Safe resolution path: Give every derivation Git subprocess a minimal shared environment with `GIT_NO_REPLACE_OBJECTS=1` and `GIT_NO_LAZY_FETCH=1`, then regress replacement refs and asserted subprocess environments.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M2-CR1-003

Finding ID: UBR-M2-CR1-003
Severity: major
Location: `scripts/test-boundary-first-validation.py:71-92`
Evidence: The active fixture synthesizes `v0.3.6` metadata by replacing the version string in tracked `v0.3.5`; those artifact hashes differ from the immutable tracked `v0.3.6` record, yet selection passes.
Required outcome: T12 proves exact rollback from the tracked `v0.3.6` metadata and detects substitution with another release's artifact identities.
Safe resolution path: Copy the tracked version-specific record for the positive fixture and add a negative fixture that injects v0.3.5 artifact identities under a v0.3.6 label.
needs-decision rationale: none
auto_fix_class: mechanical

## Finding UBR-M2-CR1-004

Finding ID: UBR-M2-CR1-004
Severity: blocker
Location: `scripts/boundary_first_validation.py:1265-1268`
Evidence: Membership in `ACTIVATION_STATES` occurs before type validation. A JSON list state raises `TypeError` instead of returning `BFR-UNKNOWN-ACTIVATION-STATE`; existing coverage uses only an unknown string.
Required outcome: Every malformed or unknown state fails closed with a bounded issue before consistency checks.
Safe resolution path: Guard `state` with `isinstance(state, str)` before membership and add list, object, and CLI structured-failure regressions.
needs-decision rationale: none
auto_fix_class: mechanical

## Validation evidence

- The full 59-test boundary suite passed, demonstrating the proof gaps rather than resolving them.
- The selector suite passed and the retired custom check remains absent.
- Direct sentinel-root, replacement-ref, tracked-metadata, and malformed-state reproductions established the four findings.
- `git diff --check ab281b39..3827623e` passed.

## Handoff

M2 does not close. Resolve all four findings, rerun the complete M2 command set, and request an independent M2 R2 review. M3 remains blocked until M2 receives a clean review.
