# Governed Lifecycle CLI Test Specification

## Owning change record

`docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`

## Related spec and plan

- Spec: `specs/governed-lifecycle-cli.md`
- Plan: `docs/plans/2026-08-24-governed-lifecycle-cli.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/governed-lifecycle-cli.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/spec-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r2`; `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/architecture-review-r2.md` |
| ADR | `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` | `adr-lifecycle-cli` | `architecture-review-r2`; accepted |
| Execution plan | `docs/plans/2026-08-24-governed-lifecycle-cli.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/plan-review-r1.md` |

## Testing strategy

Use shared conformance fixtures to prove the pure Node interpreter and Python compatibility consumers agree before mutation is enabled. Unit tests cover closed vocabularies, normalization, identity, transitions, and invalidation. Integration tests exercise the public CLI, filesystem repository adapter, output renderers, lock and recovery protocol, existing validators, skills, adapters, and CI. Fault injection covers every durable-write phase. Fresh-checkout and packaged-command smoke tests prove repository-contained truth. All proof is automated; no manual-only criterion is admitted.

Tests are introduced with their owning milestone and must fail for the intended missing behavior before production code is added. Each milestone closes its focused commands and full package regression before code review. Mandatory enforcement remains disabled until the final gate tests prove all prerequisites simultaneously.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T16, T24 | integration, smoke | Reconstruct from tracked checkout without local history. |
| R2 | T01, T17 | contract, integration | Command family and supported lifecycle contract. |
| R3 | T01, T24 | contract, smoke | Exact first-release vocabulary, including artifact revision registration, is present; unknown operations fail. |
| R4 | T01 | contract | Versioned request, unknown field, value, and operation rejection. |
| R5 | T01, T17 | contract, integration | No arbitrary setter or caller-selected state. |
| R6 | T03 | integration | Human and JSON share one result. |
| R7 | T03 | contract | Required JSON fields and version. |
| R8 | T03 | contract | Stable diagnostic fields and bounded correction. |
| R9 | T04 | integration | Recorded, evidence, and effective state. |
| R10 | T05 | integration | Minimal stage context and registration authority. |
| R11 | T02 | integration | Zero, one, many, and explicit change selection. |
| R11a | T06a, T17 | integration | Creation and revision bind exact authored bytes and evidence, invalidate replaced-identity registrations, derive review-required, and preserve routing. |
| R12 | T06 | integration | Review registration validates all linked evidence. |
| R13 | T07 | integration | Validation registration cannot imply approval. |
| R14 | T07 | integration | Resolution registration and closed dispositions. |
| R15 | T08 | integration | Settlement derives state and blocks bad evidence. |
| R16 | T09 | integration | Milestone ordering, proof, review, and projection. |
| R17 | T08, T09 | contract, integration | Every invalidation-matrix row is direct proof. |
| R18 | T10 | integration | Revision comparison precedes mutation. |
| R19 | T17 | integration | Only `change.yaml` changes; semantic artifacts stay owned. |
| R20 | T11, T12 | integration | Full durable transaction and recovery bundle. |
| R21 | T11, T12 | integration | Pre-replace immutability and post-replace restore/block. |
| R22 | T10 | integration | Old revision is stale; current equivalent request is idempotent. |
| R23 | T13 | integration | Full validation dimensions and manual-corruption detection. |
| R24 | T14 | integration | Enumerated deterministic migration only. |
| R25 | T15 | integration | Closed named repairs, dry run, revision, and refusal. |
| R26 | T16 | contract, integration | Unsupported and mixed versions fail with stable codes. |
| R27 | T03, T22 | contract, integration | Stable output, revision, diagnostics, and diff. |
| R28 | T18, T19, T21 | contract, integration | Governed callers use CLI only after activation. |
| R29 | T18 | contract | Semantic and portable clauses are retained. |
| R30 | T21 | integration | Enforcement is gated on all required evidence. |
| R31 | T17 | integration | No routing, agents, semantic authoring, PR, network, or deployment. |
| R32 | T05, T23 | integration | Diagnostics suppress sensitive and machine-local values. |
| R33 | T16, T24 | integration, smoke | Same commit reconstructs same effective result. |
| R34 | T20, T21 | integration | Split token report and threshold gate. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T08 | Open `F-12` produces `RL_UNRESOLVED_MATERIAL_FINDING` and no write. |
| E2 | T08 | Review for identity A cannot settle identity B. |
| E3 | T05, T18 | Governed spec review receives bounded context and no field-edit procedure. |
| E4 | T18 | Portable invocation requires no governed record. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 | T02 | `RL_CHANGE_NOT_FOUND`; no files created. |
| EC2 | T02 | `RL_AMBIGUOUS_CHANGE`; candidate IDs only. |
| EC3 | T01, T23 | Invalid or escaping request fails before mutation. |
| EC4 | T04, T08 | Changed evidence is stale and unusable. |
| EC5 | T10 | One concurrent commit; one stale rejection. |
| EC6 | T10 | Old envelope is stale; refreshed equivalent is `already-recorded`. |
| EC7 | T12 | Restore prior bytes or preserve recovery-blocked condition. |
| EC8 | T15, T16 | Unknown repair or newer schema fails closed. |
| EC9 | T17 | Eligibility is reported without routing. |
| EC10 | T18 | Portable use remains isolated from unrelated changes. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R3, R4, R5, R6, R7, R8, R11, R24, R25, R26 | BND-INPUT-001 | T01, T02, T14, T15, T16 | contract | automated | C01, C02, C05 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m1-conformance.md` | M1 | - | - |
| PRF-002 | covered | R9, R15, R16, R17, R18, R22, R23, R24, R25, R30 | BND-STATE-001 | T04, T08, T13 | integration | automated | C02, C04 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m4-evidence-settlement.md` | M4 | - | - |
| PRF-003 | covered | R9, R15, R16, R17, R18, R22, R23, R24, R25, R30 | BND-STATE-002 | T09 | integration | automated | C05 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m5-milestone-migration-repair.md` | M5 | - | - |
| PRF-004 | covered | R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R28, R29, R30, R31 | BND-AUTH-001 | T05, T06, T07, T08 | integration | automated | C02, C04 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m4-evidence-settlement.md` | M4 | - | - |
| PRF-005 | covered | R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R28, R29, R30, R31 | BND-AUTH-002 | T17, T18 | integration | automated | C04, C07 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m6-skill-migration.md` | M6 | - | - |
| PRF-006 | covered | R6, R10, R19, R23, R28, R29, R30, R31 | BND-COMPOSE-001 | T03, T13, T19 | integration | automated | C02, C08 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m6-adapter-parity.md` | M6 | - | - |
| PRF-007 | covered | R6, R10, R19, R23, R28, R29, R30, R31 | BND-COMPOSE-002 | T18, T19, T21 | contract | automated | C07, C08, C11 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m7-enforcement.md` | M7 | - | - |
| PRF-008 | covered | R17, R18, R20, R21, R22, R27 | BND-TEMPORAL-001 | T10, T11, T12 | integration | automated | C03 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m3-fault-matrix.md` | M3 | - | - |
| PRF-009 | covered | R20, R21, R22, R23, R24, R25 | BND-RECOVERY-001 | T11, T12 | integration | automated | C03 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m3-fault-matrix.md` | M3 | - | - |
| PRF-010 | covered | R20, R21, R22, R23, R24, R25 | BND-RECOVERY-002 | T12, T15 | integration | automated | C03, C05 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m5-milestone-migration-repair.md` | M5 | - | - |
| PRF-011 | covered | R24, R26, R27, R28, R29, R30, R33, R34 | BND-COMPAT-001 | T14, T16, T19, T21 | integration | automated | C05, C08, C11 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m7-enforcement.md` | M7 | - | - |
| PRF-012 | covered | R1, R20, R31, R32, R33 | BND-ENV-001 | T16, T17, T23, T24 | smoke | automated | C02, C12 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m2-fresh-checkout.md` | M2 | - | - |
| PRF-013 | covered | R15, R17, R18 | INT-001 | T08, T10 | integration | automated | C04 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m4-evidence-settlement.md` | M4 | - | - |
| PRF-014 | covered | R19, R20, R21 | INT-002 | T11, T12, T17 | integration | automated | C03 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m3-fault-matrix.md` | M3 | - | - |
| PRF-015 | covered | R24, R25, R26, R27, R28, R29, R30 | INT-003 | T15, T16, T18, T19, T21 | end-to-end | automated | C07, C08, C11 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m7-enforcement.md` | M7 | - | - |
| PRF-016 | covered | R6, R7, R8, R9, R10, R32 | INT-004 | T03, T04, T05, T23 | integration | automated | C02 | `docs/changes/2026-08-24-governed-lifecycle-cli/evidence/m2-output-parity.md` | M2 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | `node --test packages/rigorloop/test/lifecycle-contract.test.js` | planned-for-implementation | implement | M1 | M1 code review | nonzero blocks M1 | zero tests is failure | M1 conformance report | fixture and parser tests only |
| C02 | `node --test packages/rigorloop/test/lifecycle-read.test.js` | planned-for-implementation | implement | M2 | M2 code review | nonzero blocks M2 | zero tests is failure | M2 read/parity report | read-only fixtures and temporary repositories |
| C03 | `node --test packages/rigorloop/test/lifecycle-transaction.test.js` | planned-for-implementation | implement | M3 | M3 code review | nonzero blocks M3 | zero tests is failure | M3 fault matrix | temporary repositories; test-only fault points |
| C04 | `node --test packages/rigorloop/test/lifecycle-evidence.test.js` | planned-for-implementation | implement | M4 | M4 code review | nonzero blocks M4 | zero tests is failure | M4 transition report | temporary repositories only |
| C05 | `node --test packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-migration-repair.test.js` | planned-for-implementation | implement | M5 | M5 code review | nonzero blocks M5 | zero tests is failure | M5 transition report | temporary repositories; repairs use fixtures |
| C06 | `npm test --prefix packages/rigorloop` | existing/configured | package maintainers | cross-milestone | every milestone code review | nonzero blocks milestone | zero tests is failure | milestone validation report | local package tests only |
| C07 | `python3 scripts/validate-skills.py && python3 scripts/test-skill-validator.py && python3 scripts/test-build-skills.py && python3 scripts/build-skills.py --check` | existing/configured | skill maintainers | M6 | M6 code review | first nonzero blocks M6 | each zero-test result is failure | M6 semantic migration report | validates canonical source and generated parity; no release |
| C08 | `python3 scripts/test-adapter-distribution.py` | existing/configured | adapter maintainers | M6 | M6 code review | nonzero blocks M6 | zero tests is failure | M6 adapter parity report | local distribution fixtures only |
| C09 | `python3 scripts/test-artifact-lifecycle-validator.py && python3 scripts/test-change-metadata-validator.py && python3 scripts/test-review-artifact-validator.py` | existing/configured | validator maintainers | cross-milestone | M1 and M7 | first nonzero blocks promotion | each zero-test result is failure | parity and protected-failure ledger | validation only |
| C10 | `python3 scripts/validate-npm-package.py` | existing/configured | package maintainers | cross-milestone | M1 | nonzero blocks package promotion | not applicable | package validation report | reads package metadata/output only |
| C11 | `python3 scripts/measure-lifecycle-skill-tokens.py --change 2026-08-24-governed-lifecycle-cli` | planned-for-implementation | implement | M6 | M6 code review | missing partitions or nonzero blocks M6 | zero measured profiles is failure | M6 token report | local canonical/package text only |
| C12 | `node packages/rigorloop/dist/bin/rigorloop.js lifecycle validate --format json` | planned-for-implementation | implement | M7 | M7 code review | nonzero blocks enforcement | not applicable | M7 CI enforcement report | non-interactive read-only validation |
| C13 | `bash scripts/ci.sh` | existing/configured | repository maintainers | M7 | final M7 review | nonzero blocks enforcement and closeout | selected zero-test checks fail | full validation report | repository-local CI; no release or deployment |
| C14 | `python3 scripts/validate-boundary-first.py --path specs/governed-lifecycle-cli.md --path specs/governed-lifecycle-cli.test.md` | existing/configured | test-spec | authoring | test-spec-review | nonzero blocks test-spec handoff | not applicable | authoring validation output | structural validation only |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T01, T22 | none | C01, C06, C09, C10 | M1 inventory and conformance report | M1 code review | No mutating command exposed. |
| M2 | T02, T03, T04, T05, T13, T16, T23, T24 | none | C02, C06, C09, C10 | M2 parity, output, privacy, and fresh-checkout reports | M2 code review | Public read path only. |
| M3 | T10, T11, T12 | none | C03, C06, C10 | M3 fault matrix and filesystem identities | M3 code review | Mutation remains unexposed until recovery closes. |
| M4 | T06, T07, T08, T17 | none | C04, C06, C09 | M4 operation and transition matrices | M4 code review | Registration and settlement remain separate. |
| M5 | T09, T14, T15 | none | C05, C06, C09 | M5 milestone, migration, and repair matrices | M5 code review | Closed operation and repair vocabularies. |
| M6 | T18, T19, T20 | none | C07, C08, C11 | M6 clause dispositions, package parity, and token report | M6 code review | Semantic retention is a gate, not a token metric. |
| M7 | T21, T25 | none | C06, C08, C09, C12, C13 | M7 enforcement, rollback, and full validation reports | final M7 code review | Enforcement activates only when all gates pass. |

## Test cases

### T01. Closed CLI, request, and YAML domain

- Covers: R2-R5, AC1, AC2, BND-INPUT-001, EC3
- Level: contract
- Command IDs: C01
- Fixture/setup: valid minimal change plus one fixture for every accepted and rejected YAML/request partition
- Steps: invoke each public operation schema; vary version, operation, field, value, YAML node, duplicate key, alias, tag, merge, document count, number, path, and lifecycle contract
- Expected result: accepted partitions normalize deterministically; unknown or unsafe partitions return the documented usage or stable error before consistency checks and no arbitrary setter exists
- Failure proves: the public vocabulary is open, unsafe YAML is admitted, or mutation can bypass semantic operations
- Evidence artifact: M1 conformance report
- Automation location: `packages/rigorloop/test/lifecycle-contract.test.js`
- Required by milestone: M1

### T02. Governed change discovery and selection

- Covers: R11, EC1, EC2, BND-INPUT-001
- Level: integration
- Command IDs: C02
- Fixture/setup: temporary repositories with zero, one, and multiple active governed changes
- Steps: run read commands with and without `--change`
- Expected result: one candidate selects; zero and many return the matching stable diagnostic without writes; explicit valid identity selects exactly
- Failure proves: ambiguous or missing change state can be silently targeted
- Evidence artifact: M2 read/parity report
- Automation location: `packages/rigorloop/test/lifecycle-read.test.js`
- Required by milestone: M2

### T03. Shared human and JSON result contract

- Covers: R6-R8, R27, AC4, AC5, BND-COMPOSE-001, INT-004
- Level: contract
- Command IDs: C02
- Fixture/setup: success, blocked, invalid, stale, and warning results
- Steps: render the same internal result as human and JSON and compare semantic fields and exit status
- Expected result: all required JSON keys and stable error facts match the human result without representation-specific interpretation
- Failure proves: callers observe divergent lifecycle truth
- Evidence artifact: M2 output parity report
- Automation location: `packages/rigorloop/test/lifecycle-read.test.js`
- Required by milestone: M2

### T04. Effective status and invalidation visibility

- Covers: R9, R17, R23, EC4, BND-STATE-001, INT-004
- Level: integration
- Command IDs: C02
- Fixture/setup: current, stale, contradictory, unsettled, settled, and invalid snapshots
- Steps: request status and vary every invalidation-matrix subject
- Expected result: recorded, evidence, and effective states are distinct; historical evidence stays visible but cannot authorize operations
- Failure proves: raw fields can masquerade as effective approval
- Evidence artifact: M2 parity report
- Automation location: `packages/rigorloop/test/lifecycle-read.test.js`
- Required by milestone: M2

### T05. Minimal stage context and diagnostic privacy

- Covers: R10, R28, R32, E3, BND-AUTH-001, INT-004
- Level: integration
- Command IDs: C02
- Fixture/setup: representative authoring and review stages with secrets, absolute paths, and unrelated artifacts present
- Steps: request stage context in both formats
- Expected result: only exact target, settled inputs, round, output path, blockers, revision, and permitted registration operation appear; secrets and machine-local paths do not
- Failure proves: skills need repository-wide mechanics or diagnostics leak private context
- Evidence artifact: M2 context/privacy report
- Automation location: `packages/rigorloop/test/lifecycle-read.test.js`
- Required by milestone: M2

### T06. Review registration

- Covers: R12, BND-AUTH-001
- Level: integration
- Command IDs: C04
- Fixture/setup: valid and invalid review record, log, identity, outcome, round, and finding sets
- Steps: submit `record-review` against current and mismatched evidence
- Expected result: only a complete exact semantic record is registered; judgment text is never changed or inferred
- Failure proves: incomplete or wrong review evidence can enter lifecycle state
- Evidence artifact: M4 evidence settlement report
- Automation location: `packages/rigorloop/test/lifecycle-evidence.test.js`
- Required by milestone: M4

### T06a. Authored artifact revision registration

- Covers: R3-R5, R11a, R17-R19, R22, R27-R28, R31
- Level: integration
- Command IDs: C01, C04
- Fixture/setup: absent-entry creation and existing-entry revision fixtures for every authorized authoring stage, plus wrong kind, role, path, authority, prior identity, stale revision, missing evidence, duplicate, and routing-drift partitions
- Steps: invoke `record-artifact-revision` through the public CLI for each partition and compare exact resulting bytes and registrations
- Expected result: valid creation or revision changes only the matching artifact entry, records current artifact and authoring-evidence identities, invalidates registrations tied to the prior identity, derives `review-required`, is idempotent at the current revision, and never changes workflow routing
- Failure proves: authoring skills still require direct lifecycle edits or the CLI has gained arbitrary authoring or routing authority
- Evidence artifact: M6 authoring-registration matrix
- Automation location: `packages/rigorloop/test/lifecycle-artifact-revision.test.js`
- Required by milestone: M6

### T07. Validation and finding-resolution registration

- Covers: R13, R14, BND-AUTH-001
- Level: integration
- Command IDs: C04
- Fixture/setup: exact, stale, unknown-disposition, missing-owner, missing-proof, and log-inconsistent evidence
- Steps: invoke both recording operations
- Expected result: exact existing evidence registers; command success never implies approval; unknown values fail before consistency
- Failure proves: mechanical success or malformed resolution can become semantic authority
- Evidence artifact: M4 operation matrix
- Automation location: `packages/rigorloop/test/lifecycle-evidence.test.js`
- Required by milestone: M4

### T08. Exact artifact settlement and evidence invalidation

- Covers: R15, R17, E1, E2, EC4, AC2, BND-STATE-001, BND-AUTH-001, INT-001
- Level: integration
- Command IDs: C04
- Fixture/setup: every invalidation-matrix row plus missing, contradictory, unresolved, wrong-round, wrong-artifact, and unauthorized evidence
- Steps: request settlement for each partition
- Expected result: current complete evidence derives the only permitted state; all other partitions block with stable evidence and byte-identical repository state
- Failure proves: stale or unresolved evidence can settle an artifact
- Evidence artifact: M4 transition matrix
- Automation location: `packages/rigorloop/test/lifecycle-evidence.test.js`
- Required by milestone: M4

### T09. Milestone transitions and plan invalidation

- Covers: R16, R17, AC2, BND-STATE-002
- Level: integration
- Command IDs: C05
- Fixture/setup: eligible, predecessor-incomplete, wrong kind, proof-incomplete, review-incomplete, complete, repeated, and changed-plan fixtures
- Steps: start and complete milestones in each state
- Expected result: only the unique eligible milestone changes; projections are exact; plan changes invalidate affected evidence and later starts
- Failure proves: milestones can skip ordering, proof, review, or plan identity
- Evidence artifact: M5 milestone matrix
- Automation location: `packages/rigorloop/test/lifecycle-milestone.test.js`
- Required by milestone: M5

### T10. Optimistic concurrency, stale envelopes, and replay

- Covers: R18, R22, EC5, EC6, BND-TEMPORAL-001, INT-001
- Level: integration
- Command IDs: C03
- Fixture/setup: two callers sharing a revision, completed facts, and conflicting facts
- Steps: race changed operations, replay the old envelope, refresh, then replay equivalent and conflicting requests
- Expected result: one commit wins; stale envelopes return `RL_STALE_OPERATION`; refreshed identical facts return `already-recorded`; conflicts fail
- Failure proves: stale callers overwrite state or replay duplicates evidence
- Evidence artifact: M3 fault matrix
- Automation location: `packages/rigorloop/test/lifecycle-transaction.test.js`
- Required by milestone: M3

### T11. Pre-replacement atomicity and lock behavior

- Covers: R20, R21, AC3, BND-TEMPORAL-001, BND-RECOVERY-001, INT-002
- Level: integration
- Command IDs: C03
- Fixture/setup: injected failure at validation, candidate, lock, bundle, fsync, and pre-replace points; live and orphan locks
- Steps: trigger each failure and inspect bytes, modes, identities, and allowed next operations
- Expected result: prior bytes remain exact; fixed transient files use `0600`; no time-based lock theft occurs
- Failure proves: a rejected or competing operation can partially mutate governed state
- Evidence artifact: M3 fault matrix
- Automation location: `packages/rigorloop/test/lifecycle-transaction.test.js`
- Required by milestone: M3

### T12. Post-replacement validation, restoration, and reconciliation

- Covers: R20, R21, EC7, BND-RECOVERY-001, BND-RECOVERY-002, INT-002
- Level: integration
- Command IDs: C03
- Fixture/setup: valid prior/candidate identities, each closed phase, invalid candidate, failed restore, malformed bundle, and nonce mismatch
- Steps: interrupt after replace and restart; inject post-validation and restoration failures
- Expected result: candidate completes only after validation; otherwise prior bytes restore and verify, or bundle remains recovery-blocked with only validate/named reconcile allowed
- Failure proves: failed persistence can be reported as settled or recovery can mutate unknown state
- Evidence artifact: M3 fault matrix
- Automation location: `packages/rigorloop/test/lifecycle-transaction.test.js`
- Required by milestone: M3

### T13. Repository validation and corruption detection

- Covers: R23, BND-STATE-001, BND-COMPOSE-001
- Level: integration
- Command IDs: C02, C09
- Fixture/setup: one fixture per validation dimension plus detectable unsupported manual mutations
- Steps: run Node validation and compatibility consumers over the same corpus
- Expected result: schema, identities, combinations, evidence, review, milestones, revisions, and corruption agree or enforcement stays disabled
- Failure proves: the canonical interpreter and protected validators disagree
- Evidence artifact: parity ledger
- Automation location: lifecycle read tests and Python validator suites
- Required by milestone: M2 and M7

### T14. Enumerated deterministic migration

- Covers: R24, AC2, BND-INPUT-001, BND-COMPAT-001
- Level: integration
- Command IDs: C05
- Fixture/setup: every enumerated legacy version, supported existing artifacts, unsupported older/newer, ambiguous, dry-run, and repeated migration
- Steps: run migration twice, compare planned and committed bytes, and inspect seeded artifact registrations
- Expected result: supported transformations are deterministic and idempotent; they register current supported artifact and available authoring-evidence identities without changing settlement state; all other versions remain unchanged
- Failure proves: migration guesses or rewrites unsupported state
- Evidence artifact: M5 migration matrix
- Automation location: `packages/rigorloop/test/lifecycle-migration-repair.test.js`
- Required by milestone: M5

### T15. Closed named repair

- Covers: R25, EC8, BND-INPUT-001, BND-RECOVERY-002, INT-003
- Level: integration
- Command IDs: C05
- Fixture/setup: each approved condition, unknown corruption, wrong revision, dry-run, and unsafe prior bytes
- Steps: request repair codes and compare dry-run with result
- Expected result: only an exact named recoverable condition mutates as previewed; unknown or arbitrary edits return `RL_REPAIR_UNSAFE`
- Failure proves: repair is an administrative state setter
- Evidence artifact: M5 repair matrix
- Automation location: `packages/rigorloop/test/lifecycle-migration-repair.test.js`
- Required by milestone: M5

### T16. Compatibility and fresh-checkout reconstruction

- Covers: R1, R26, R33, AC6, BND-COMPAT-001, BND-ENV-001
- Level: smoke
- Command IDs: C02, C12
- Fixture/setup: clean checkouts at supported and incompatible combinations with caches and transient files absent
- Steps: run status and validate and compare effective results
- Expected result: supported commits reproduce state; incompatible combinations return stable guidance and never mutate
- Failure proves: hidden state or mixed versions control lifecycle meaning
- Evidence artifact: M2 fresh-checkout report
- Automation location: lifecycle read/smoke tests
- Required by milestone: M2 and M7

### T17. Mutation authority and negative capability

- Covers: R2, R5, R19, R31, EC9, BND-AUTH-002, INT-002
- Level: integration
- Command IDs: C04, C05
- Fixture/setup: watched repository with semantic artifacts, routing, PR metadata, network trap, and unauthorized requested targets
- Steps: execute every mutation operation and compare all paths and external effects
- Expected result: only exact `change.yaml` changes plus documented transient siblings; routing and semantic artifacts remain unchanged; no network or agent action occurs
- Failure proves: CLI authority expands beyond lifecycle registration/settlement
- Evidence artifact: operation write-set report
- Automation location: lifecycle operation tests
- Required by milestone: M4 and M5

### T18. Governed skill reduction with semantic and portable preservation

- Covers: R28, R29, E3, E4, EC10, BND-AUTH-002, BND-COMPOSE-002, INT-003
- Level: contract
- Command IDs: C07
- Fixture/setup: clause-disposition ledger for every governed canonical skill and representative portable invocations
- Steps: scan for direct lifecycle-field mutation procedure; assert retained semantic criteria, artifact ownership, authority, stop, handback, and portable clauses; build packages
- Expected result: mechanics route through CLI while semantic guidance and portable operation remain present and equivalent
- Failure proves: optimization removes rigor or still duplicates settlement machinery
- Evidence artifact: M6 skill migration report
- Automation location: skill validator and build tests
- Required by milestone: M6

### T19. Adapter and caller parity

- Covers: R28, AC7, BND-COMPOSE-001, BND-COMPOSE-002, BND-COMPAT-001, INT-003
- Level: integration
- Command IDs: C08
- Fixture/setup: generated Codex, Claude Code, and opencode packages from the same canonical skills
- Steps: validate command availability, structured context consumption, recording requests, and retained semantic clauses
- Expected result: supported adapters expose the same lifecycle contract and no generated package is hand-edited
- Failure proves: adapter-specific lifecycle behavior or package drift remains
- Evidence artifact: M6 adapter parity report
- Automation location: `scripts/test-adapter-distribution.py`
- Required by milestone: M6

### T20. Token measurement without semantic erosion

- Covers: R34, AC9
- Level: integration
- Command IDs: C11
- Fixture/setup: versioned before/after representative governed stage profiles
- Steps: measure mechanical instructions, semantic guidance, returned CLI context, and total loaded tokens independently
- Expected result: the provisional 30% mechanics objective is met, or an explicit owner-approved threshold is recorded; semantic dispositions remain passing
- Failure proves: savings are assumed, shifted into CLI output, or achieved by deleting required guidance
- Evidence artifact: M6 token report
- Automation location: planned measurement script
- Required by milestone: M6

### T21. Mandatory-enforcement gate

- Covers: R28, R30, R34, AC8, AC10, BND-COMPOSE-002, BND-COMPAT-001, INT-003
- Level: end-to-end
- Command IDs: C08, C09, C11, C12, C13
- Fixture/setup: pass/fail state for migration, compatibility, conformance, recovery, adapter, CI, and measurement evidence
- Steps: evaluate activation with each gate missing and with all gates current
- Expected result: enforcement remains off for every missing or owner-unresolved gate and activates once for the complete compatible set
- Failure proves: the mandatory boundary can strand callers or activate without proof
- Evidence artifact: M7 enforcement decision
- Automation location: CI and lifecycle enforcement tests
- Required by milestone: M7

### T22. Deterministic identity, serialization, and diff

- Covers: R27, AC4
- Level: contract
- Command IDs: C01, C06
- Fixture/setup: repeated normalized snapshots with reordered source keys and documented provenance variations
- Steps: calculate revisions and candidates repeatedly and compare JSON and bytes
- Expected result: identical supported inputs yield identical revisions, diagnostics, and schema-ordered UTF-8/LF diffs except documented provenance
- Failure proves: callers cannot safely compare revisions or retry
- Evidence artifact: M1 determinism report
- Automation location: lifecycle contract tests
- Required by milestone: M1

### T23. Filesystem containment and privacy

- Covers: R32, BND-ENV-001, INT-004
- Level: integration
- Command IDs: C02, C03
- Fixture/setup: symlink escapes, read-only directories, private request values, credentials, hostnames, and absolute paths
- Steps: invoke read and mutation paths and inspect both outputs
- Expected result: unsafe filesystem states block without traversal; output contains bounded repository-relative evidence only
- Failure proves: repository containment or diagnostic privacy can be bypassed
- Evidence artifact: M2 privacy and M3 filesystem reports
- Automation location: lifecycle read and transaction tests
- Required by milestone: M2 and M3

### T24. Packaged public-command smoke

- Covers: R1, R3, R33, AC6
- Level: smoke
- Command IDs: C10, C12
- Fixture/setup: packed npm artifact installed into a clean temporary checkout
- Steps: invoke help, status, context, and validate without source-tree-only modules or caches
- Expected result: the packaged executable exposes the supported read contract and reconstructs repository state
- Failure proves: behavior works only in the development tree
- Evidence artifact: package smoke report
- Automation location: package validation and smoke tests
- Required by milestone: M2 and M7

### T25. Full governed lifecycle conformance

- Covers: AC1-AC10
- Level: end-to-end
- Command IDs: C06, C07, C08, C09, C11, C12, C13
- Fixture/setup: representative change from authored proposal through milestones, including stale review, interruption, migration, skill invocation, and enforcement states
- Steps: execute supported operations in order and inject one protected failure from every milestone
- Expected result: valid transitions produce deterministic repository state; every invalid path fails before unauthorized mutation; semantic and routing decisions remain outside the CLI
- Failure proves: focused suites do not compose into the approved product boundary
- Evidence artifact: M7 full conformance report
- Automation location: repository CI
- Required by milestone: M7

## Fixtures and data

- Versioned valid and invalid `change.yaml`, request, review, review-log, resolution, validation, plan, milestone, migration, and recovery fixtures under `packages/rigorloop/test/fixtures/lifecycle/`.
- A closed fixture manifest identifies expected parser acceptance, lifecycle revision, effective result, diagnostic, operation result, resulting bytes, Python parity status, and owning requirement IDs.
- Transaction tests create isolated temporary repositories and expose test-only fault points; fixtures never mutate the working repository.
- Token fixtures preserve the pre-migration baseline and post-migration canonical and packaged profiles so later text changes cannot rewrite the baseline.

## Mocking/stubbing policy

Mock only clocks and explicitly documented provenance, process interruption, filesystem fault points, and adapter invocation shells. Use real parsing, normalization, digesting, serialization, temporary-filesystem operations, public CLI dispatch, canonical skill files, package generation, and Python validators. Network access is trapped and fails the test because the first release has no network dependency.

## Migration or compatibility tests

T13-T16 and T21 prove every supported current, enumerated legacy, unsupported newer/older, mixed-version, repair, and fresh-checkout partition. The protected-failure ledger must name each Python behavior retained during dual-run and the exact reviewed evidence required before retirement or delegation.

## Observability verification

T03-T05 verify stable result fields, error codes, blockers, identities, permitted operations, supporting repository paths, prior/result revisions, and exit status. No test treats verbose text as a separate semantic source; both renderers are checked against the same internal result.

## Security/privacy verification

T01, T17, and T23 prove path normalization, regular-file checks, symlink containment, no shell evaluation, fixed `0600` transient files, closed repair authority, no network side effects, and suppression of secrets, raw environment values, credentials, private hostnames, request bodies, and absolute machine paths.

## Performance checks

Record read-only status and context time over small and large governed fixture sets in M2 and compare again in M7. The test fails if read-only commands invoke unrelated language toolchains, scan unrelated archives, access the network, or regress beyond the reviewed fixture threshold established in M2. Correctness and freshness checks may not be skipped to meet the threshold.

## Manual QA checklist

Not applicable. Human-output readability, no-color behavior, corrective guidance, and packaged invocation are deterministic and covered by automated snapshots plus semantic-field assertions in T03 and T24.

## What not to test and why

- Semantic correctness of proposals, specs, reviews, code, or owner decisions: the CLI records but does not make those judgments.
- Workflow routing, agent invocation, PR, push, merge, release, deployment, or hosted-service behavior: explicitly outside R31.
- Cross-repository or distributed transactions, malicious-maintainer resistance, cryptographic identity, or event sourcing: outside first-release scope.
- Generated adapter body edits: canonical `skills/` and repository-owned build/validation paths are the supported source surface.

## Uncovered gaps

None.

## Next artifacts

- Independent formal `test-spec-review`.
- M1 test and implementation work only after the test spec is approved and workflow routes implementation.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`; not approved, implementation-ready, validated, verified, branch-ready, or PR-ready.
