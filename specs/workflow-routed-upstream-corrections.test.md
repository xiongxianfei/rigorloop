# Workflow-Routed Upstream Corrections Test Specification

## Owning change record

`docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

## Related spec and plan

- Spec: `specs/workflow-routed-upstream-corrections.md`
- Plan: `docs/plans/2026-08-25-workflow-routed-upstream-corrections.md`
- Architecture: `docs/architecture/2026-08-25-workflow-routed-upstream-corrections.md`
- ADR: `docs/adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/workflow-routed-upstream-corrections.md` | `spec` | `spec-review-r3` |
| Architecture | `docs/architecture/2026-08-25-workflow-routed-upstream-corrections.md` | `architecture` | `architecture-review-r3` |
| ADR | `docs/adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md` | `adr-correction-ownership` | `architecture-review-adr-r1` |
| Plan | `docs/plans/2026-08-25-workflow-routed-upstream-corrections.md` | `plan` | `plan-review-r2` |

## Testing strategy

Use isolated temporary repositories around the public CLI and pure engine. Contract tests cover closed request and stored vocabularies. Integration tests cover migration, route and return, exact review settlement, repository ownership, withdrawal, rendering, and recovery. End-to-end fixtures reproduce a review-resolution proof gap and the current duplicate architecture owner. Every rejected operation asserts byte-identical tracked state; every accepted operation is replayed against both stale and refreshed envelopes.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T01, T03, T05, T06 | contract | Three public operations and unknown-operation rejection. |
| R2 | T01, T08 | integration | Existing envelope, revision, idempotence, and transaction. |
| R3 | T03 | integration | Workflow-only route; no destination selection. |
| R4 | T03 | contract | Exact route fields and milestone partition. |
| R5 | T01, T03 | contract | Closed route reasons fail before consistency. |
| R6 | T03 | contract | Closed destination-stage and kind mapping. |
| R7 | T03 | integration | Settled, current, upstream, unique destination. |
| R8 | T03 | integration | Contained exact route evidence. |
| R9 | T03, T08 | integration | Complete immutable snapshot and no semantic mutation. |
| R10 | T03, T07 | integration | Destination routing, null blocker, active route status. |
| R11 | T03 | integration | Only exact destination revision admitted. |
| R12 | T03 | integration | Prior identity, invalidation, and review-required. |
| R13 | T04 | integration | Findings scoped to exact review occurrence. |
| R14 | T05 | integration | Exact workflow return and evidence fields. |
| R15 | T05 | integration | Changed identity and derived approving review authority. |
| R16 | T05 | integration | Exact snapshot restoration without progression. |
| R17 | T03, T05, T08 | integration | Stale, identical, and conflicting replay. |
| R18 | T02 | integration | Cross-change collision rejection. |
| R19 | T02, T10 | integration | Supported repository-only normalized discovery. |
| R20 | T06 | contract | Workflow-only architecture and ADR withdrawal. |
| R21 | T06 | integration | Exact duplicate-registration evidence. |
| R22 | T06 | integration | Pointer and one canonical owner. |
| R23 | T06 | integration | Complete unsafe-withdrawal matrix. |
| R24 | T06, T08 | integration | Only selected active projections removed. |
| R25 | T01, T06 | contract | Deterministic non-owning, non-circular receipt. |
| R26 | T07 | integration | Route-required diagnostic and deferred operation. |
| R27 | T07 | contract | Immediate and deferred operations never conflict. |
| R28 | T07 | contract | Bounded human and JSON parity. |
| R29 | T09 | contract | Git truth, portable independence, authority separation. |
| R30 | T01, T02, T03, T06 | contract | Every new closed vocabulary rejects unknown values first. |
| R31 | T01, T09 | migration | Explicit version-2 migration and old-client refusal. |
| R32 | T08, T10 | integration | Contradiction validation and receipt exclusion. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T03, T10 | Proof gap routes to test-spec while downstream finding stays open. |
| E2 | T04 | Unrelated code-review finding does not block clean test-spec review. |
| E3 | T05 | Exact source blocker and milestone state restore. |
| E4 | T06, T10 | Duplicate architecture registration withdraws without semantic changes. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 | T03 | Current, lateral, and downstream destinations reject. |
| EC2 | T03 | Exact replay is idempotent; conflicting route rejects. |
| EC3 | T03 | Unknown finding identity rejects. |
| EC4 | T03, T08 | Changed destination or route evidence is stale. |
| EC5 | T05 | Return blocks before a new approving review. |
| EC6 | T04 | Unrelated findings remain open but non-blocking. |
| EC7 | T06 | Non-architecture withdrawal rejects. |
| EC8 | T06 | Pointer and owner disagreement rejects. |
| EC9 | T06 | Refreshed exact withdrawal replay is already recorded. |
| EC10 | T08 | Fault restores prior bytes or preserves named recovery state. |
| EC11 | T05 | Every return-evidence mismatch rejects. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R3, R4, R5, R6, R7, R8, R14, R18, R19, R20, R21, R22, R23, R30 | BND-INPUT-001 | T01, T02, T03, T05, T06 | contract | automated | C01, C02, C03 | `evidence/m1-version-ownership.md` | M1 | - | - |
| PRF-002 | covered | R7, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R32 | BND-STATE-001 | T02, T03, T04, T05, T06, T08 | integration | automated | C02, C03, C04 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-003 | covered | R3, R6, R7, R8, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R29 | BND-AUTH-001 | T02, T03, T04, T05, T06, T09 | integration | automated | C02, C03, C04 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-004 | covered | R11, R12, R13, R18, R19, R26, R27, R28, R29, R31, R32 | BND-COMPOSE-001 | T02, T03, T04, T07, T09, T10 | end-to-end | automated | C02, C03, C05 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-005 | covered | R2, R15, R16, R17, R23, R25 | BND-TEMPORAL-001 | T01, T05, T06, T08 | integration | automated | C03, C04 | `evidence/m2-correction-route.md` | M2 | - | - |
| PRF-006 | covered | R2, R17, R18, R19, R20, R21, R22, R23, R24, R25, R30, R31, R32 | BND-RECOVERY-001 | T01, T02, T03, T05, T06, T08 | integration | automated | C02, C03, C04 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-007 | covered | R18, R19, R25, R26, R27, R30, R31, R32 | BND-COMPAT-001 | T01, T02, T06, T07, T09, T10 | integration | automated | C01, C02, C05 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-008 | covered | R8, R18, R19, R21, R22, R23, R24, R25, R28, R29 | BND-ENV-001 | T02, T03, T06, T07, T09, T10 | integration | automated | C02, C03, C05 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-009 | covered | R15, R16, R17 | INT-001 | T04, T05 | integration | automated | C03 | `evidence/m2-correction-route.md` | M2 | - | - |
| PRF-010 | covered | R18, R19, R21, R22, R23, R24, R25 | INT-002 | T02, T06, T08, T10 | end-to-end | automated | C02, C04 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |
| PRF-011 | covered | R26, R27, R31 | INT-003 | T01, T07, T09 | contract | automated | C01, C03, C05 | `evidence/m3-withdrawal-consumers.md` | M3 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js` | existing-plus-expanded | implement | M1 | M1 review | nonzero blocks | zero tests fails | `evidence/m1-version-ownership.md` | temporary fixtures only |
| C02 | `node --test packages/rigorloop/test/lifecycle-artifact-revision.test.js packages/rigorloop/test/lifecycle-ownership.test.js` | planned | implement | M1 | M1 review | nonzero blocks | zero tests fails | `evidence/m1-version-ownership.md` | temporary repositories only |
| C03 | `node --test packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-read.test.js` | planned | implement | M2 | M2 review | nonzero blocks | zero tests fails | `evidence/m2-correction-route.md` | temporary repositories only |
| C04 | `node --test packages/rigorloop/test/lifecycle-withdrawal.test.js packages/rigorloop/test/lifecycle-transaction.test.js` | planned | implement | M3 | M3 review | nonzero blocks | zero tests fails | `evidence/m3-withdrawal-consumers.md` | fixture mutations and fault injection only |
| C05 | `npm test --prefix packages/rigorloop` | existing | implement | cross-milestone | every review | nonzero blocks | zero tests fails | milestone evidence | local package tests only |
| C06 | `python scripts/validate-boundary-first.py --path specs/workflow-routed-upstream-corrections.test.md` | existing | test-spec | authoring | test-spec review | nonzero blocks | not applicable | test-spec authoring evidence | read-only structural validation |
| C07 | `bash scripts/ci.sh --mode broad-smoke` | existing | verify | M3 | final verification | nonzero blocks | selected zero-test checks fail | final verification evidence | repository-local feature validation; no publication |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T01, T02 | none | C01, C02, C05 | `evidence/m1-version-ownership.md` | M1 code review | No workflow consumer migration. |
| M2 | T03, T04, T05, T07, T08 | none | C03, C05 | `evidence/m2-correction-route.md` | M2 code review | Withdrawal remains unavailable. |
| M3 | T06, T09, T10 | none | C04, C05, C07 | `evidence/m3-withdrawal-consumers.md` | final code review | Consumer text follows verified operations. |

## Test cases

| Test ID | Scenario and expected result | Automation location | Required milestone |
| --- | --- | --- | --- |
| T01 | Version-1 remains readable; explicit migration produces deterministic version 2; old clients and every unknown operation, field, reason, stage, kind, reason, route status, and receipt status fail closed before consistency. | `lifecycle-contract.test.js`, `lifecycle-migration-repair.test.js` | M1 |
| T02 | Cross-change normalized ownership accepts one same-entry revision, rejects another owner, and fails closed for unreadable, escaped, contradictory, ambiguous, and symlinked records. | `lifecycle-ownership.test.js`, `lifecycle-artifact-revision.test.js` | M1 |
| T03 | Full route matrix proves exact workflow authority, evidence, source snapshot, null active blocker, destination-only revision, invalidation, replay, and no semantic or milestone mutation. | `lifecycle-correction-route.test.js` | M2 |
| T04 | A clean revised test-spec review settles while unrelated code-review findings remain open; target-occurrence findings still block approval. | `lifecycle-evidence.test.js` | M2 |
| T05 | Return requires every exact route, artifact, review, authority, outcome, chronology, evidence, and revision fact, then restores source state byte-for-byte at field level. | `lifecycle-correction-route.test.js` | M2 |
| T06 | Withdrawal proves exact pointer and canonical owner, rejects every R23 partition, removes only active duplicate projections, stores a non-owning receipt, and replays deterministically. | `lifecycle-withdrawal.test.js` | M3 |
| T07 | Human and JSON context distinguish immediate operations from `available_after_workflow_route`, remain bounded, and omit absolute paths and content. | `lifecycle-read.test.js` | M2 |
| T08 | Every new mutation fault and stale envelope preserves prior bytes or the existing named recoverable state. | `lifecycle-transaction.test.js`, operation suites | M2, M3 |
| T09 | Workflow text requests route, return, and withdrawal; stage skills retain semantic guidance and no field-level settlement or routing mechanics; portable mode is unchanged. | repository skill validation | M3 |
| T10 | Fresh-checkout end-to-end fixtures reproduce the proof-gap correction and duplicate architecture recovery, and CI ignores receipts as owners while detecting contradictory active state. | `lifecycle-correction-route.test.js`, `lifecycle-withdrawal.test.js` | M3 |

## Fixtures and data

Use temporary repositories with supported version-1 and version-2 changes, repeated review stages, open unrelated findings, active milestones, shared architecture pointers, symlink and path-escape attempts, stale revisions, and transaction fault points. The observability scenario is represented as an isolated fixture; this branch does not mutate that feature worktree.

## Mocking/stubbing policy

Stub only filesystem fault points and process identity used by the existing transaction tests. Exercise the real parser, serializer, hash, public CLI, repository discovery, and renderers. No network or Git-host mock is needed.

## Migration or compatibility tests

T01 proves v1 read compatibility, deterministic v2 migration, preservation of blockers and findings, new-operation gating, old-client refusal, and rollback visibility. T02 and T10 prove mixed repositories fail closed without rewriting other changes.

The full `bash scripts/release-verify.sh <tag>` gate remains release-owned and is intentionally deferred until a release candidate has matching archive metadata, release notes, and token-cost evidence. It is not a feature-branch acceptance command.

## Observability verification

T07 checks concise human and JSON result parity. Existing file logging tests remain authoritative for debug detail; lifecycle evidence never depends on logs.

## Security/privacy verification

T02, T06, and T07 cover repository containment, symlink refusal, fail-closed ownership, no absolute paths, no raw content, and structural rather than authenticated authority claims.

## Performance checks

T02 records the number of supported change records read and asserts no generated directory, Git history, network, or unrelated content scan. No timing threshold is normative in the first release.

## Manual QA checklist

No manual-only acceptance. Human output snapshots are automated.

## What not to test and why

Do not test semantic artifact quality, autonomous route choice, malicious maintainers, distributed transactions, PR actions, deployment, or hosted authorization because the approved contract excludes them.

## Uncovered gaps

None.

## Next artifacts

- Independent test-spec review.
- Proof-first M1 implementation after approval.

## Follow-on artifacts

None yet.

## Readiness

Ready for test-spec review after CLI registration; not implementation-ready, verified, or PR-ready.
