# Boundary-First Proof Model Test Spec Review R4

Review ID: test-spec-review-r4
Stage: test-spec-review
Round: 4
Reviewer: independent Codex test-spec reviewer
Target: specs/boundary-first-proof-model.test.md
Reviewed artifact: specs/boundary-first-proof-model.test.md
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-TSR6, PBF-TSR7
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PBF-TSR6, PBF-TSR7
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/test-spec-review-r4.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md
- Open blockers: immediate-predecessor and complete lifecycle-state inventory proof; rollback metadata-input non-mutation
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: revise and rereview before M3 implementation

## Packet integrity

Pass. The target, feature spec, reviewed plan, plan-review record, and diff all
match the exact revisions and SHA-256 identities in the R4 invocation.

## Findings

### PBF-TSR6

Finding ID: PBF-TSR6
Severity: major
Location: `specs/boundary-first-proof-model.test.md`, T8 and T9
Evidence: T8 requires immutable release tags but does not prove that the
rollback release is the immediately preceding published release. T9's
executable parent fixture names only accepted historical specs even though
PBF-R005c includes accepted, approved, and active paths.
Required outcome: Add controlled release-order fixtures that reject a
non-immediate rollback release, plus explicit parent-revision cases for
accepted, approved, and active inclusion and nonterminal exclusion.
Safe resolution path: Extend the existing T8/T9 fixture descriptions and
assertions; do not add a release writer or historical store.
needs-decision rationale: none

### PBF-TSR7

Finding ID: PBF-TSR7
Severity: major
Location: `specs/boundary-first-proof-model.test.md`, T13
Evidence: T13 snapshots the activation manifest, feature specs, and proof maps
but omits `dist/adapters/manifest.yaml` and the selected tracked release
metadata, even though those are the central read-only inputs.
Required outcome: Snapshot both metadata inputs and require byte identity after
success and every validation failure.
Safe resolution path: Extend T13's existing before-and-after byte assertions;
do not add mutation or recovery behavior.
needs-decision rationale: none

## Prior finding closure

| Finding | R4 result | Evidence |
| --- | --- | --- |
| PBF-TSR3 | resolved | T8 and T9 now define the manifest fields, exclusions, raw-UTF-8 inventory ordering, and controlled parent/activating history. |
| PBF-TSR4 | resolved | T13 names selected-tag output, deterministic ordering, governed-file snapshots, and fail-if-called action sentinels. |
| PBF-TSR5 | resolved | Next artifacts routes to M3 with separate implementation authority. |

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Packet integrity | pass | Every packet revision and byte identity matches. |
| Parent-revision proof | concern | Approved and active lifecycle inclusion need explicit executable cases. |
| Release ordering | block | A non-immediate rollback release is not rejected by named proof. |
| Rollback read-only proof | block | Two central metadata inputs are absent from byte snapshots. |
| Scope control | pass | No writer, receipt, transaction, rollback state, or attestation store is introduced. |
| Milestone ownership | pass | M3 and M4 command ownership and the M3 handoff are coherent. |
| Implementation handoff | block | Two material proof gaps remain. |

## Recommendation

Resolve PBF-TSR6 and PBF-TSR7 in the test spec, then run test-spec-review R5.
No upstream contract or architecture change is required.
