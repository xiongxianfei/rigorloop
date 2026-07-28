# Boundary-First Proof Model Test Spec Review R3

Review ID: test-spec-review-r3
Stage: test-spec-review
Round: 3
Reviewer: independent Codex test-spec reviewer
Target: specs/boundary-first-proof-model.test.md
Reviewed artifact: specs/boundary-first-proof-model.test.md
Review date: 2026-07-28
Recording status: recorded
Status: blocked
Review status: blocked
Material findings: PBF-TSR3, PBF-TSR4, PBF-TSR5
Immediate next stage: none
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: blocked
- Material findings: PBF-TSR3, PBF-TSR4, PBF-TSR5
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/test-spec-review-r3.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md
- Open blockers: inconsistent plan identity in the invocation packet and three proof-map findings
- Immediate next stage: none until the inconsistent packet is replaced
- Implementation handoff: not-allowed
- Stop condition: do not rely on R3 or enter M3 implementation

## Review packet integrity

The invocation declared plan revision `1b7e2c6b` with SHA-256
`262decf9d2804bbb854505d479c788c3ece87e0d09af2441102ade5098fbb20d`.
The plan at revision `1b7e2c6b` actually hashes to
`b90ed82fc688368f5b6ae7dd642defa2355fde71235be6c598d24dc9879587b1`.
The declared hash instead identifies the plan at revision `0fbf287e`.
The packet is therefore internally inconsistent and this review cannot approve
the test specification. A new invocation must bind each artifact to an exact
matching revision and byte identity.

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `specs/boundary-first-proof-model.test.md` | `baab0c42a6388047c3f45fb099c298bfd2fde1e8662ccbb04571b3d7194f54c4` |
| `specs/boundary-first-proof-model.md` | `7d10f72e7dfca18c08c4f7117846c5a655f060f5087ec196725a2c5494af25d1` |
| `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md` | `262decf9d2804bbb854505d479c788c3ece87e0d09af2441102ade5098fbb20d` |
| `docs/architecture/system/architecture.md` | `65bc44c6d8a8a6de23879144dca6c524b69558a178ab9127f03907b1f3761843` |
| `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md` | `3d09255eb51dacb2fd2fe756a656fc9719edd6de99763f23ae9ad09fd1b1c1e2` |

## Findings

### PBF-TSR3

Finding ID: PBF-TSR3
Severity: major
Location: `specs/boundary-first-proof-model.test.md`, T8, T9, and fixtures
Evidence: T8 does not enumerate the governed skills, canonical and projection
identities, unique raw-UTF-8-sorted grandfather inventory, or its exclusions.
T9 requires parent-revision behavior without specifying a controlled parent
and activating revision, while the fixture policy disallows Git-history
dependence.
Required outcome: Specify an isolated temporary source-control history or
equivalent seam with parent and activating revisions. Assert the exact
manifest fields, governed set, content identities, inventory eligibility,
exclusions, uniqueness, sorting, and rejection of child-introduced
self-grandfathering.
Safe resolution path: Extend T8 and T9 and clarify that tests avoid ambient
repository history while using deterministic temporary history.
needs-decision rationale: none

### PBF-TSR4

Finding ID: PBF-TSR4
Severity: major
Location: `specs/boundary-first-proof-model.test.md`, T13
Evidence: The rollback proof does not require the selected release tag in
output, raw-UTF-8 adapter ordering, before-and-after snapshots of governed
files, or a sentinel proving that no installation or publication action ran.
Required outcome: Make rollback readiness prove exact release selection,
deterministic package-matrix ordering, repository non-mutation, and absence of
external or installation actions.
Safe resolution path: Add byte snapshots and an injected action sentinel to
the existing read-only integration test; do not add a rollback executor.
needs-decision rationale: none

### PBF-TSR5

Finding ID: PBF-TSR5
Severity: major
Location: `specs/boundary-first-proof-model.test.md`, Next artifacts
Evidence: The test spec still routes to M1 implementation even though M1 and
M2 are closed and the active milestone is M3.
Required outcome: Route only to M3 implementation after a clean recorded
test-spec rereview and separate implementation authority.
Safe resolution path: Replace the stale M1 handoff text and keep
implementation blocked until R4 approves.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Packet integrity | block | The plan revision and hash do not identify the same bytes. |
| Governing-contract alignment | pass | The lightweight two-state direction matches the approved spec and architecture. |
| Requirement coverage | concern | Parent-baseline and rollback-readiness properties are not yet executable enough. |
| Fixture and data design | block | Parent-revision behavior lacks an isolated source-control fixture. |
| Determinism and isolation | concern | Sorting and non-mutation assertions are incomplete. |
| Scope control | pass | Writer, receipt, transaction, rollback-state, and attestation machinery remain removed. |
| Milestone mapping | block | The downstream handoff incorrectly points to closed M1. |
| Implementation handoff | block | R3 is not an approvable packet and three material findings remain open. |

## Recommendation

Resolve PBF-TSR3 through PBF-TSR5, issue a byte-consistent R4 invocation, and
repeat independent test-spec review. No feature-spec, architecture, or plan
revision is required.
