<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->

# Published-Skill-First Repository Simplification Test Spec

## Owning change record

`docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related spec and plan

- Spec: `specs/published-skill-first-repository-simplification.md`
- Plan: `docs/plans/2026-08-10-published-skill-first-repository-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/published-skill-first-repository-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/spec-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r2`; `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/architecture-review-r2.md` |
| Validation ADR | `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md` | `adr-published-skill-validation` | `architecture-review-r2`; `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/architecture-review-r2.md` |
| Execution plan | `docs/plans/2026-08-10-published-skill-first-repository-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Fixture-backed unit tests prove Gate A, closed vocabularies, ledger transitions, admission records, and diagnostics.
Integration tests prove equivalent all-target Gate B parity, Gate C composition, governance composition, direct CI routing, and exact contract disposition.
Local end-to-end tests build temporary adapter and release candidates and, only when inventory proves extra installer logic, materialize a local package into an empty temporary directory for filesystem inspection.
Smoke proof exercises the final direct command graph without network, publication, target-agent execution, prompts, transcripts, or model-derived results.
Migration tests run old and replacement proof over representative accepted and rejected fixtures before each independently recoverable removal.
Semantic skill quality uses manual review procedure MP1 because clarity and ownership are judgment, not deterministic acceptance.

Scenarios are selected for distinct outcomes and composed hazards.
No Cartesian product of gates, targets, fixtures, or retirement states is required.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T2, T4, T6 | contract | Product proof chain is canonical source through package and release. |
| R2 | T2 | unit | Every named canonical integrity failure has positive and negative fixtures. |
| R3 | T2, T3, MP1 | integration, manual | Gate A stops at deterministic facts; MP1 owns meaning. |
| R4 | T4 | integration | All three targets receive independent equivalent package proof. |
| R5 | T4 | integration | Declared transforms pass; undeclared transforms and drift fail. |
| R6 | T7, T15 | integration | Acceptance command graphs reject runtime and prompt dependencies. |
| R7 | T6 | integration | Gate C adds release-only deterministic facts to current A/B proof. |
| R8 | T6 | integration | Composition exposes underlying gate failures without copied rules. |
| R9 | T5 | contract | Installer inventory selects no smoke for pure copy or a narrow smoke for extra logic. |
| R10 | T5, T15 | e2e | Any retained smoke ends at local filesystem inspection. |
| R11 | T3, MP1 | manual | MP1 covers all nine semantic-review dimensions through an auditable review procedure. |
| R12 | T8 | integration | One public governance entry point composes focused owners. |
| R13 | T8 | unit | Unknown values fail before consistency and report repair data. |
| R14 | T1, T14 | contract | Every retained or added check has a complete admission record. |
| R15 | T14 | integration | Prohibited new subsystem categories are absent. |
| R16 | T2, T4, T6, T8, T14 | integration | New logic stays inside an existing requirement owner. |
| R17 | T1, T13 | migration | Accepted and rejected fixtures map to an exact owner or de-contracting decision. |
| R18 | T1, T13 | migration | Unknown or contradictory behavior pauses the slice. |
| R19 | T13 | migration | Old-versus-replacement results and rollback are recorded before removal. |
| R20 | T13, T16 | migration | Removal requires complete retained proof or approved de-contracting. |
| R21 | T9, T16 | integration | CI calls stable owners directly; exceptions require approved evidence. |
| R22 | T10, T13 | integration | Metrics accompany but cannot replace failure coverage. |
| R23 | T11 | migration | Workflow ordering, review evidence, and automation behavior remain unchanged. |
| R24 | T7, T11 | migration | Historical evidence remains available but is absent from required acceptance. |
| R25 | T1, T13, T16 | migration | Active subsystem contracts block removal until exact disposition. |
| R26 | T12 | contract | Every named prospective skill-contract clause has the approved disposition. |
| R27 | T2, T4, T12 | contract | Structural, resource, transform, archive, and byte proof remain. |
| R28 | T4, T6 | integration | Codex, Claude Code, and opencode package compatibility remains equivalent. |
| R29 | T3, T7, T12 | contract | Runtime-selection claims and broad semantic scoring stay prohibited. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC1 | T2 | unit | Gate A positive and named negative fixtures. |
| AC2 | T4 | integration | Three-target package and transformation matrix. |
| AC3 | T6 | integration | Current A/B composition plus release-only checks. |
| AC4 | T7, T15 | integration | Static command-graph and local-run exclusion proof. |
| AC5 | T5 | contract, e2e | Inventory selects pure-copy sufficiency or narrow materialization. |
| AC6 | T3, T8, MP1 | manual, integration | Semantic review and governance have separate owners. |
| AC7 | T1, T14 | contract | Admission completeness and zero-new-subsystem enforcement. |
| AC8 | T13, T16 | migration | Per-slice inventory, comparison, disposition, absence, and rollback. |
| AC9 | T9 | integration | Stable direct CI graph and measured exception path. |
| AC10 | T10 | integration | Metrics never satisfy the coverage field. |
| AC11 | T11 | migration | Workflow behavior and historical evidence are preserved. |
| AC12 | T2, T4, T12 | contract | Runtime obligations retire while deterministic parity remains. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T2 | Missing or escaping mapped resources fail Gate A actionably. |
| E2 | T4 | Stale target bytes fail only the affected Gate B target. |
| E3 | T3 | Structurally valid unclear prose passes gates and can fail MP1 review. |
| E4 | T7 | A successful transcript is neither required nor sufficient. |
| E5 | T5 | Pure-copy inventory produces no separate materialization gate. |
| E6 | T5, T15 | Extra logic runs only against local temporary filesystem state. |
| E7 | T1, T13 | Undocumented failure pauses retirement. |
| E8 | T6 | Gate C consumes current product-gate results. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R4, R7, R14, R17 | BND-INPUT-001 | T1, T2, T4, T6 | contract | automated | CMD1, CMD3, CMD6, CMD9 | `evidence/m1-retirement-ledger.md`; `evidence/m2-gate-a.md`; `evidence/m3-gate-b.md`; `evidence/m4-gate-c.md` | M4 | - | - |
| PRF-002 | covered | R17, R18, R19, R20, R25 | BND-STATE-001 | T13, T16 | integration | automated | CMD1, CMD15 | `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-003 | covered | R1, R3, R5, R11, R12, R13, R14, R15, R16 | BND-AUTH-001 | T3, T4, T8, T14 | contract | hybrid | CMD6, CMD11 | `evidence/m2-gate-a.md`; `evidence/m3-gate-b.md`; `evidence/m5-governance.md` | M5 | MP1 | - |
| PRF-004 | covered | R4, R7, R8, R12, R21 | BND-COMPOSE-001 | T4, T6, T8, T9 | integration | automated | CMD6, CMD9, CMD11, CMD15 | Owning milestone evidence | M6 | - | - |
| PRF-005 | covered | R18, R19, R20, R24, R25 | BND-TEMPORAL-001 | T13 | integration | automated | CMD1 | `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-006 | covered | R5, R13, R18, R19, R20 | BND-RECOVERY-001 | T4, T8, T13 | integration | automated | CMD1, CMD6, CMD11 | Owning milestone evidence | M6 | - | - |
| PRF-007 | covered | R23, R24, R25, R26, R27, R28 | BND-COMPAT-001 | T11, T12, T13 | integration | automated | CMD1, CMD13 | `evidence/m1-retirement-ledger.md`; `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-008 | covered | R6, R9, R10, R28, R29 | BND-ENV-001 | T5, T7, T15 | end-to-end | automated | CMD8, CMD10, CMD15 | `evidence/m3-gate-b.md`; `evidence/m4-gate-c.md`; `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-009 | covered | R4, R5, R17, R18, R19, R20 | INT-001 | T4, T13 | integration | automated | CMD1, CMD6 | `evidence/m3-gate-b.md` | M3 | - | - |
| PRF-010 | covered | R7, R8, R21 | INT-002 | T6, T9 | integration | automated | CMD9, CMD15 | `evidence/m4-gate-c.md`; `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-011 | covered | R11, R12, R13, R14, R15, R16 | INT-003 | T2, T3, T14 | contract | hybrid | CMD3, CMD14 | `evidence/m2-gate-a.md` | M2 | MP1 | - |
| PRF-012 | covered | R17, R18, R19, R20, R25 | INT-004 | T1, T13, T16 | integration | automated | CMD1, CMD15 | `evidence/m1-retirement-ledger.md`; `evidence/m6-ci-retirement.md` | M6 | - | - |
| PRF-013 | covered | R6, R9, R10 | INT-005 | T5, T7, T15 | end-to-end | automated | CMD8, CMD10, CMD15 | `evidence/m3-gate-b.md`; `evidence/m6-ci-retirement.md` | M6 | - | - |

Evidence paths are relative to `docs/changes/2026-08-10-published-skill-first-repository-simplification/`.

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 mixed deterministic and semantic check | T2, T3, T13 | Retain deterministic fixtures and route judgment to MP1. |
| EC2 intentional target transform | T4 | Complete declaration is required for acceptance. |
| EC3 target-specific installer logic | T5 | Only uncovered RigorLoop-owned branches receive smoke proof. |
| EC4 unnamed old-fixture behavior | T1, T13 | The affected slice pauses. |
| EC5 measured selector or cache value | T9, T16 | Only an approved, measured exception may retain it. |
| EC6 parity passes but release data is wrong | T6 | Gate C independently fails. |
| EC7 historical transcript helps review | T7, T11 | It remains optional context, never gate evidence. |
| EC8 distinct lifecycle vocabulary parser | T8, T13 | Consolidation pauses until unknown-value behavior is preserved. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-retirement-ledger.py` | planned-for-implementation | implement | M1 | code-review M1 | Block on incomplete admission, contract disposition, transition, comparison, or rollback fields. | Zero tests is failure. | `evidence/m1-retirement-ledger.md` | Repository-local fixtures only. |
| CMD2 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.yaml` | existing/configured | implement | M1 | code-review M1 | Block malformed or unregistered ledger lifecycle evidence. | Not applicable; deterministic validator. | `evidence/m1-retirement-ledger.md` | Read-only explicit-path validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | code-review M2 | Block Gate A fixture, ownership, or diagnostic regression. | Zero tests is failure. | `evidence/m2-gate-a.md` | Repository-local fixtures only. |
| CMD4 | `python scripts/validate-skills.py` | existing/configured | implement | M2 | code-review M2 | Block invalid canonical skills or resources. | Not applicable; deterministic validator. | `evidence/m2-gate-a.md` | Read-only canonical validation. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | code-review M2 | Block canonical generated-skill drift. | Not applicable; deterministic build check. | `evidence/m2-gate-a.md` | Check mode must not mutate canonical source. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | code-review M3 | Block any target inventory, byte, transform, archive, or materialization regression. | Zero tests is failure. | `evidence/m3-gate-b.md` | Local fixtures and temporary archives only. |
| CMD7 | `python scripts/build-adapters.py --version v0.1.5 --output-dir <temporary-output>` | existing/configured | implement | M3 | code-review M3 | Block generation failure for any supported target. | Not applicable; deterministic build. | `evidence/m3-gate-b.md` | Caller supplies a newly created temporary directory; no publication. |
| CMD8 | `python scripts/validate-adapters.py --version v0.1.5 --adapter-root <temporary-output>` | planned-for-implementation | implement | M3 | code-review M3 | Block parity or declared-transform failure for any target. | Not applicable; deterministic validator. | `evidence/m3-gate-b.md` | Reads local temporary output; starts no target runtime. |
| CMD9 | `python scripts/test-release-transaction.py` | existing/configured | implement | M4 | code-review M4 | Block Gate C composition or release-only integrity regression. | Zero tests is failure. | `evidence/m4-gate-c.md` | Local release fixtures only. |
| CMD10 | `bash scripts/release-verify.sh <local-fixture-version>` | release-owned | implement | M4 | code-review M4 | Block local candidate readiness and expose the failing underlying gate. | Zero selected checks is failure. | `evidence/m4-gate-c.md` | Local fixture only; no tag, push, registry, network publication, or runtime launch. |
| CMD11 | `python scripts/test-artifact-lifecycle-validator.py && python scripts/test-change-metadata-validator.py && python scripts/test-review-artifact-validator.py` | existing/configured | implement | M5 | code-review M5 | Block governance composition, transition, evidence, or unknown-value regression. | Zero tests in any suite is failure. | `evidence/m5-governance.md` | Repository-local fixtures only. |
| CMD12 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <governed-fixtures>` | existing/configured | implement | M5 | code-review M5 | Block if the single public entry point misses an owned governance failure. | Not applicable; deterministic validator. | `evidence/m5-governance.md` | Read-only fixture validation. |
| CMD13 | `python scripts/test-select-validation.py` | existing/configured | implement | M1, M6 | code-review M1 | Block incorrect old-graph inventory initially and direct-graph compatibility during cutover. | Zero tests is failure. | `evidence/m1-retirement-ledger.md`; `evidence/m6-ci-retirement.md` | Local fixtures only; retained only while its contract remains active. |
| CMD14 | `python scripts/validate-boundary-first.py --check` | existing/configured | implement | M2 | code-review M2 | Block structural boundary/proof drift without judging semantic adequacy. | Not applicable; deterministic validator. | `evidence/m2-gate-a.md` | Read-only structural check. |
| CMD15 | `bash scripts/ci.sh --mode pr` | ci-owned | implement | M6 | code-review M6 | Block if the direct graph omits a required owner, invokes excluded runtime evidence, or loses a protected failure. | Zero selected checks is failure. | `evidence/m6-ci-retirement.md` | Repository-local validation; no release publication or target runtime. |
| CMD16 | `python scripts/validate-change-metadata.py docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml` | existing/configured | test-spec | lifecycle | test-spec authoring | Block illegal authoring, review, workflow, or automation state. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only metadata validation. |
| CMD17 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-10-published-skill-first-repository-simplification` | existing/configured | test-spec-review | lifecycle | test-spec-review | Block malformed, unindexed, or unresolved formal review evidence. | Not applicable; deterministic validator. | Review log and resolution. | Read-only review validation. |
| CMD18 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/published-skill-first-repository-simplification.test.md --path docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml --path docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/test-spec-revision-r2.md` | existing/configured | test-spec | lifecycle | test-spec authoring | Block incomplete proof-map revision evidence or illegal settlement. | Not applicable; deterministic validator. | Change metadata validation entry. | Read-only explicit-path validation. |

Angle-bracket operands are fixture bindings that implementation must replace with exact safe local values in milestone evidence; they are not shell commands to run literally.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preimplementation gate | T1-T16 | MP1 | CMD16, CMD17, CMD18 | This test spec, authoring evidence, and test-spec-review record | implementation handoff | Every requirement, criterion, example, edge case, boundary, interaction, milestone, and command is mapped. |
| M1 | T1, T10, T11, T12, T14 | none | CMD1, CMD2, CMD13 | `evidence/m1-retirement-ledger.md` | code-review M1 | Exact ownership and contract disposition precede acceptance changes or deletion. |
| M2 | T2, T3, T7, T14 | MP1 | CMD3, CMD4, CMD5, CMD14 | `evidence/m2-gate-a.md` | code-review M2 | Proves deterministic Gate A and the separate semantic-review owner. |
| M3 | T4, T5, T7, T15 | none | CMD6, CMD7, CMD8 | `evidence/m3-gate-b.md` | code-review M3 | Proves equivalent all-target packages and the minimum installer boundary. |
| M4 | T6, T7, T10, T11, T15 | none | CMD9, CMD10 | `evidence/m4-gate-c.md` | code-review M4 | Proves composed local release integrity without publication or runtime execution. |
| M5 | T8, T14 | none | CMD11, CMD12 | `evidence/m5-governance.md` | code-review M5 | Proves one public governance result while focused modules retain exact invariants. |
| M6 | T7, T9, T10, T11, T13, T15, T16 | none | CMD1, CMD13, CMD15 | `evidence/m6-ci-retirement.md` | code-review M6 | Each ledger-eligible removal is a separately recorded sub-slice with direct proof, absence audit, and rollback before aggregate closeout. |

## Test cases

### T1. Retirement ledger fails closed

- Covers: R14, R17, R18, R25, E7, EC4, AC7, BND-INPUT-001, INT-004
- Level: unit
- Command IDs: CMD1, CMD2
- Fixture/setup: Complete ledger plus missing, unknown, contradictory, duplicate-owner, and active-contract variants.
- Steps: Parse each entry and attempt every allowed transition.
- Expected result: Only complete inventoried entries proceed; unknown or conflicting ownership pauses.
- Failure proves: A check can become eligible without an exact protected-failure and contract disposition.
- Evidence artifact: `evidence/m1-retirement-ledger.md`
- Automation location: `scripts/test-retirement-ledger.py`
- Required by milestone: M1

### T2. Gate A proves only canonical deterministic integrity

- Covers: R1-R3, R16, R27, E1, EC1, AC1, INT-003
- Level: unit
- Command IDs: CMD3, CMD4, CMD5, CMD14
- Fixture/setup: Valid skill plus every R2 invalid property and structurally valid ambiguous prose.
- Steps: Run Gate A across each fixture and inspect diagnostics.
- Expected result: Deterministic defects fail actionably; ambiguous prose does not receive a semantic score.
- Failure proves: Canonical integrity is incomplete or Gate A has become a semantic oracle.
- Evidence artifact: `evidence/m2-gate-a.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T3. Semantic review owns published-skill meaning

- Covers: R3, R11, R29, E3, EC1, AC6, BND-AUTH-001, INT-003
- Level: manual
- Command IDs: none
- Fixture/setup: One changed published skill and the concise review checklist.
- Steps: Execute MP1 against the changed canonical skill and its mapped resources.
- Expected result: Material semantic concerns become review findings; structural presence alone cannot approve meaning.
- Failure proves: No accountable surface evaluates semantic skill quality.
- Evidence artifact: `evidence/m2-gate-a.md`
- Automation location: MP1 evidence in the M2 code-review record and `evidence/m2-gate-a.md`
- Required by milestone: M2

### T4. Gate B proves equivalent target packages and declared transforms

- Covers: R4, R5, R16, R27, R28, E2, EC2, AC2, INT-001
- Level: integration
- Command IDs: CMD6, CMD7, CMD8
- Fixture/setup: Codex, Claude Code, and opencode trees with valid, stale, missing, extra, unsafe, malformed-archive, declared-transform, and undeclared-transform variants.
- Steps: Generate each target independently and validate inventory, paths, bytes, transform contract, and archive.
- Expected result: All targets receive equivalent proof; only complete declared transformations may differ.
- Failure proves: A target can ship stale, unsafe, or undeclared content.
- Evidence artifact: `evidence/m3-gate-b.md`
- Automation location: `scripts/test-adapter-distribution.py`
- Required by milestone: M3

### T5. Installer inventory chooses the smallest filesystem proof

- Covers: R9, R10, E5, E6, EC3, AC5, BND-ENV-001, INT-005
- Level: e2e
- Command IDs: CMD6, CMD8
- Fixture/setup: Pure-copy installer and each inventoried extra materialization branch using local archives and empty temporary directories.
- Steps: Classify coverage; skip separate smoke for pure copy; invoke only uncovered logic and inspect files otherwise.
- Expected result: Proof stops at deterministic filesystem state and starts no target runtime.
- Failure proves: Installer logic is unproved or smoke has escaped the owned boundary.
- Evidence artifact: `evidence/m3-gate-b.md`
- Automation location: `scripts/test-adapter-distribution.py` or retained packed CLI test named by M1
- Required by milestone: M3

### T6. Gate C composes current product proof

- Covers: R1, R7, R8, R16, R28, E8, EC6, AC3, INT-002
- Level: integration
- Command IDs: CMD9, CMD10
- Fixture/setup: Passing and failing A/B results plus invalid version, metadata, archive, checksum, notes, parity, and rollback fixtures.
- Steps: Run local release proof and perturb one owner or release-only fact at a time.
- Expected result: Gate C reports the underlying owner failure or the exact release-only invariant without copied semantics.
- Failure proves: Release readiness can pass stale product proof or obscure its owner.
- Evidence artifact: `evidence/m4-gate-c.md`
- Automation location: `scripts/test-release-transaction.py`
- Required by milestone: M4

### T7. Acceptance contains no target-runtime evidence

- Covers: R6, R24, R26, R29, E4, EC7, AC4
- Level: integration
- Command IDs: CMD3, CMD6, CMD9, CMD13, CMD15
- Fixture/setup: Acceptance command and dependency graph plus historical runtime-evidence paths.
- Steps: Inspect required invocations and execute representative local gates with runtime binaries absent.
- Expected result: Required acceptance has no runtime launch, prompt, transcript grade, model matrix, or nondeterministic retry; historical files remain optional.
- Failure proves: Repository correctness still depends on target-model behavior.
- Evidence artifact: Owning milestone evidence
- Automation location: command-graph fixtures and reference audit
- Required by milestone: M6

### T8. Governance fails closed behind one public owner

- Covers: R12, R13, R16, EC8, AC6, BND-AUTH-001, BND-RECOVERY-001
- Level: integration
- Command IDs: CMD11, CMD12
- Fixture/setup: Valid lifecycle bundle and shape, transition, reference, dangling-evidence, contradiction, and unknown-value variants.
- Steps: Invoke the public entry point and focused internal suites.
- Expected result: The public result preserves every failure; unknown values report field, value, allowed values, and repair before consistency.
- Failure proves: Consolidation silently loses governance behavior.
- Evidence artifact: `evidence/m5-governance.md`
- Automation location: lifecycle validator suites
- Required by milestone: M5

### T9. CI uses a thin direct command graph

- Covers: R21, EC5, AC9, BND-COMPOSE-001, INT-002
- Level: integration
- Command IDs: CMD13, CMD15
- Fixture/setup: Representative skill, adapter, release, lifecycle, mixed, and exception change sets.
- Steps: Resolve and execute the final graph; inspect every retained indirection.
- Expected result: Stable owners run directly; any retained selector, cache, or scheduler has approved measured evidence.
- Failure proves: Publication still depends on opaque orchestration.
- Evidence artifact: `evidence/m6-ci-retirement.md`
- Automation location: CI command-graph fixtures
- Required by milestone: M6

### T10. Simplification metrics cannot substitute for proof

- Covers: R22, AC10
- Level: integration
- Command IDs: CMD1, CMD9, CMD15
- Fixture/setup: Complete and incomplete retirement records with identical favorable metrics.
- Steps: Validate both records and record command count, runtime, changed lines, and owner.
- Expected result: Metrics are reported; incomplete protected-failure mapping still blocks.
- Failure proves: A faster or smaller graph can erase contractual coverage.
- Evidence artifact: Owning milestone evidence
- Automation location: retirement-ledger tests
- Required by milestone: M6

### T11. Workflow and historical evidence remain compatible

- Covers: R23, R24, EC7, AC11, BND-COMPAT-001
- Level: migration
- Command IDs: CMD1, CMD9, CMD13
- Fixture/setup: Current workflow records, target-bound automation fixtures, and historical prompt/transcript records.
- Steps: Compare workflow behavior before and after and verify historical evidence remains readable but unrequired.
- Expected result: Stage order, review recording, independence, automation behavior, and historical availability remain unchanged.
- Failure proves: Simplification changed an explicitly preserved product contract.
- Evidence artifact: `evidence/m1-retirement-ledger.md`; `evidence/m4-gate-c.md`
- Automation location: existing workflow and lifecycle suites
- Required by milestone: M4

### T12. Skill-contract disposition is exact

- Covers: R26, R27, R29, AC12, BND-COMPAT-001
- Level: contract
- Command IDs: CMD1, CMD3, CMD6
- Fixture/setup: Clause inventory for every R26 entry plus retained R35c/R35d and deterministic parity clauses.
- Steps: Compare active prospective requirements with the approved disposition map.
- Expected result: Only named runtime, semantic parity, and clean-install portions are superseded; deterministic proof remains active.
- Failure proves: Migration either retains forbidden runtime proof or weakens package integrity.
- Evidence artifact: `evidence/m1-retirement-ledger.md`
- Automation location: ledger and skill-contract regression fixtures
- Required by milestone: M1

### T13. Every retirement sub-slice dual-runs and rolls back

- Covers: R17-R20, R22, R25, E7, EC4, EC8, AC8, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, INT-004
- Level: integration
- Command IDs: CMD1, CMD13, CMD15
- Fixture/setup: Per-check accepted/rejected inventory, old and replacement runners, mismatch, partial removal, and rollback variants.
- Steps: Run old-only, dual, replacement-only, removal, absence audit, and rollback states for one ledger entry at a time.
- Expected result: Only matching complete slices retire; mismatches pause; rollback restores the last slice and its invocation.
- Failure proves: M6 can perform a big-bang or unrecoverable deletion.
- Evidence artifact: `evidence/m6-ci-retirement.md`
- Automation location: retirement-ledger and command-graph tests
- Required by milestone: M6

### T14. Admission budget prevents a replacement validation subsystem

- Covers: R14-R16, AC7, BND-AUTH-001, INT-003
- Level: contract
- Command IDs: CMD1, CMD3, CMD6, CMD9, CMD11
- Fixture/setup: Changed-file inventory and ownership map for new or retained validation logic.
- Steps: Classify each executable, parser, cache, scheduler, selector, and gate change.
- Expected result: No new standalone validator CLI, selector, cache, or scheduler exists; additions belong to an existing owner and invariant.
- Failure proves: Simplification recreated the subsystem under new names.
- Evidence artifact: Owning milestone evidence
- Automation location: retirement-ledger ownership audit
- Required by milestone: M5

### T15. Local proof is safe and repository-owned

- Covers: R6, R10, E6, AC4, BND-ENV-001, INT-005
- Level: smoke
- Command IDs: CMD6, CMD8, CMD10, CMD15
- Fixture/setup: Local packages, temporary roots, absent credentials, disabled network, and target-runtime launch sentinel.
- Steps: Run adapter, optional materialization, release, and final CI proof in safe mode.
- Expected result: All proof completes locally without publication, credentials, network, target runtime, prompts, or private logs.
- Failure proves: Acceptance has an external or nondeterministic dependency.
- Evidence artifact: Owning milestone evidence
- Automation location: safe-mode integration fixtures
- Required by milestone: M6

### T16. Final reference audit preserves every protected failure

- Covers: R20, R21, R25, AC8, EC5, BND-STATE-001, INT-004
- Level: integration
- Command IDs: CMD1, CMD13, CMD15
- Fixture/setup: Final repository references, command graph, retired-path denylist, retained exceptions, and representative former failures.
- Steps: Search active invocations, execute representative negatives through retained owners, and test rollback of the last removal.
- Expected result: Retired paths are absent, exceptions remain justified, and every contractual failure is observable through one owner.
- Failure proves: Final cutover contains a dangling path or lost invariant.
- Evidence artifact: `evidence/m6-ci-retirement.md`
- Automation location: final command-graph and reference-audit tests
- Required by milestone: M6

## Fixtures and data

- Gate A fixtures extend `tests/fixtures/skills/` with one valid skill and one focused variant per deterministic property.
- Gate B fixtures extend existing adapter-distribution data with independent Codex, Claude Code, and opencode package trees and transform declarations.
- Gate C uses local release profiles, tracked notes, archives, and checksum fixtures; no publishable candidate is created.
- Governance reuses lifecycle, change-metadata, and review-artifact fixtures and adds unknown-value cases before consistency cases.
- The retirement ledger records each old command, accepted and rejected fixtures, active clauses, replacement owner, comparison result, removal references, metrics, and rollback point.
- Temporary roots are newly created per test and are never repository, home, credential, or target-runtime directories.

## Mocking/stubbing policy

Stub target runtime launch, network, credentials, registry publication, and release publication so any attempted call fails the test.
Do not mock canonical bytes, adapter archives, filesystem materialization, lifecycle parser output, command-graph ownership, or old-versus-replacement fixture results.
Gate C may inject recorded Gate A/B results only when integration tests also exercise the real shared owner boundary.

## Migration or compatibility tests

T11-T13 and T16 are mandatory migration proof.
Every retirement entry progresses through inventoried, dual-proof, removable, and retired states; any unknown, mismatch, active-clause conflict, partial removal, or failed rollback moves the entry to paused.
Historical evidence is read-only, all three adapter targets remain supported, and the latest removal is independently reversible.

## Observability verification

T2, T4, T6, T8, and T13 assert stable owner or gate name, affected artifact or target, violated invariant, result, and repair.
Each retirement evidence record includes commands, fixtures, differences, removed references, rollback, command count, runtime, changed lines, and maintenance owner.
No transcript, model ID, prompt outcome, retry log, or LLM score is an observability requirement.

## Security/privacy verification

T2 rejects resource traversal.
T4 rejects unsafe archive paths.
T5 and T15 use local packages and fresh temporary roots and fail on network, credential, runtime, or publication attempts.
Evidence excludes private prompts, user transcripts, model logs, and secrets.

## Performance checks

T10 records baseline and replacement wall time and command count per retirement slice.
No numeric threshold can override protected-failure proof, and no cache, selector, or scheduler exception is accepted without separate approved scale evidence.

## Manual proof cases

### MP1. Published-skill semantic review

- Automation rationale: Description clarity, instructional sufficiency, ownership judgment, and handoff quality are semantic decisions. Deterministic automation cannot decide them without becoming the prohibited semantic oracle from R3 and R11.
- Owner role: independent published-skill reviewer.
- Owning stage: M2 code review.
- Required environment: the canonical changed skill under `skills/`, its mapped packaged resources, the approved feature spec, M2 implementation evidence, and a writable formal code-review record. No target-agent runtime, prompt, transcript, model output, network access, or generated adapter execution is required.
- Exact steps:
  1. Read the changed canonical skill and each mapped resource it instructs the user to load.
  2. Assess description and trigger clarity.
  3. Confirm the skill owns only its named artifact, stage, or recurring responsibility.
  4. Confirm prerequisites and required inputs are explicit.
  5. Follow the procedure as written and identify any hidden repository knowledge or missing decision.
  6. Confirm resource references match the packaged Resource map.
  7. Confirm stop conditions prevent guessing when required information or authority is missing.
  8. Confirm claims do not exceed the skill's approval, readiness, verification, or handoff authority.
  9. Confirm the output artifact and downstream handoff are explicit.
  10. Record each material concern as a formal code-review finding; otherwise record a clean MP1 result.
- Evidence artifact: the M2 code-review record, cross-referenced from `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/m2-gate-a.md`.
- Pass condition: all nine review dimensions were assessed, the evidence names the reviewed canonical skill and resource set, and no MP1 material finding remains open.
- Failure condition: a review dimension was skipped, the reviewed artifact or resources are unidentified, or any material semantic finding remains open. M2 code-review closeout is then blocked.
- Rerun condition: rerun MP1 after any substantive change to the reviewed skill description, ownership, prerequisites, procedure, resources, stop conditions, claims, output, or handoff.

## Manual QA checklist

- Confirm MP1 names the reviewed skill and mapped resource set.
- Confirm all MP1 steps have recorded outcomes.
- Confirm the M2 code-review record contains either a clean MP1 result or formal findings.
- Confirm no target-agent runtime or semantic scoring was used as a substitute for MP1 judgment.

## What not to test and why

- Do not start Codex, Claude Code, or opencode; repository acceptance does not own model interpretation.
- Do not send prompts, grade outputs, inspect routing transcripts, select model IDs, maintain runtime matrices, or retry model runs.
- Do not convert semantic skill quality into a structural or scoring oracle; MP1 owns judgment.
- Do not require all-target clean-install behavior when Gate B proves package copying; only uncovered RigorLoop-owned materialization receives filesystem proof.
- Do not publish, tag, push, deploy, access credentials, or depend on network services.
- Do not delete historical evidence to prove it is no longer required.
- Do not enumerate a Cartesian product after each distinct boundary and interaction outcome has direct proof.

## Uncovered gaps

None.

The M1 inventory may discover a new normative contract decision.
That discovery is not an uncovered proof gap: it pauses the affected slice and routes to `spec` before implementation continues.

## Next artifacts

- Formal `test-spec-review` record.
- M1 implementation evidence only after approval and workflow handoff.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`.
This proof map does not authorize implementation until the formal review is approved and workflow routing advances.
