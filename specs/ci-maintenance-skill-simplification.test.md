# CI-Maintenance Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml`

Boundary model version: boundary-first-v1

## Related spec and plan

- Spec: `specs/ci-maintenance-skill-simplification.md`
- Plan: `docs/plans/2026-08-19-ci-maintenance-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/architecture-assessment.md`; architecture not required

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature specification | `specs/ci-maintenance-skill-simplification.md` | `spec`; `sha256:b7ee60ec3dcdfa54d54f1945d43cb1d6f51297554e81a7375a8d6b764a020ec7` | `spec-review-r2`; `docs/changes/2026-08-19-ci-maintenance-skill-simplification/reviews/spec-review-r2.md` |
| Execution plan | `docs/plans/2026-08-19-ci-maintenance-skill-simplification.md` | `plan`; commit `54bc0ce2`; `sha256:f60fdbd0d3759f8802d76eedf80ec17459eae0f5fd584d24aeb6a279790353c6` | `plan-review-r1`; `docs/changes/2026-08-19-ci-maintenance-skill-simplification/reviews/plan-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-19-ci-maintenance-skill-simplification/architecture-assessment.md` | architecture assessment | `architecture-not-required` bound to the approved spec identity |
| Existing feature contract | `specs/ci-maintenance-skill.md` | legacy focused contract | preserved except the five explicit R54 amendment rows |

## Testing strategy

Use deterministic contract and fixture tests for closed classifications, resource selection, policy ownership, privileged authority, conditional commits, dependency batches, compatibility, and claims. Use existing skill, build, boundary, adapter, metadata, and prose validators for integration and package proof. Use exact LF-normalized word and UTF-8 byte measurements for every real assembly. No live hosted workflow, external platform mutation, live PR, target-agent runtime, transcript grading, or manual semantic gate is part of acceptance.

Proof is staged. M1 freezes ownership, literals, scenarios, and baselines. M2 proves the package split, policy boundaries, privilege behavior, skeleton, and claims. M3 proves conditional one-file commits and non-atomic batches. M4 proves all-assembly reduction and package parity. Each test fails closed when an approved identity, vocabulary, authority, or resource is unknown.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R3 | T1, T5, T14 | contract, integration | Package inventory, universal ownership, narrow review sufficiency, and no runtime additions. |
| R4-R10 | T1-T2, T15 | contract | Closed operation/concern/target/provider axes, target-state behavior, compatibility matrix, external-state route, and unknown failure. |
| R11-R14 | T4, T15 | contract | Privilege classification, exact design/review basis, safe defaults, and forbidden inference. |
| R15-R20 | T3, T15 | contract | Sole semantic placement ownership, command ownership, risk-map triggers, narrow-review exclusion, and conflict stops. |
| R21-R24 | T5 | contract | Minimal skeleton, forbidden examples, structure modes, and complete-file revision. |
| R25-R28 | T1, T4-T5 | contract | Every assembly and variant, separate external evidence, late loading, resource failures, and approved-design realization branch. |
| R29-R34 | T6-T8 | contract, integration | Prepared target identity, no-clobber create, identity-guarded revise, read-back boundary, unsupported capability, and idempotent retry. |
| R35-R41 | T9-T10 | contract, integration | Batch classification, manifest, cross-target validation, safe ordering, atomic-group stop, partial results, and fresh retry. |
| R42-R44 | T11 | contract | Complete result fields, fixed hosted observation, and forbidden readiness claims. |
| R45-R46 | T12, T15 | contract | Rule/literal ledgers and unknown-value-first regression coverage. |
| R47-R49 | T13 | contract | Exact measurement method, every assembly and conditional variant, external-evidence disclosure, and reduction gates. |
| R50-R52 | T14 | integration | Canonical-through-installed parity, published portability, deterministic acceptance, and excluded external/runtime execution. |
| R53 | T8-T10, T14 | contract | Every persistent coordination, parser, provider, external-state, or authority trigger routes back to architecture. |
| R54 | T12, T14 | contract, integration | Five legacy amendments and every coupled consumer migrate atomically; unlisted clauses remain authoritative. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Command IDs | First proof milestone | Notes |
| --- | --- | --- | --- | --- |
| AC1 | T1-T15 | CMD1-CMD9 | M1 | Every requirement row above and every proof obligation below maps directly. |
| AC2 | T5, T14 | CMD1-CMD6 | M2 | Exact package inventory and absence of scripts/runtime machinery. |
| AC3 | T1-T2, T4-T5, T9, T11, T15 | CMD1, CMD3 | M2 | Independent vocabularies and unknown-first behavior. |
| AC4 | T3 | CMD1, CMD3 | M2 | Risk map owns placement and authoring reference owns serialization only. |
| AC5 | T1, T4-T5 | CMD1-CMD3 | M2 | Exhaustive ordinary, project-native, coverage, structure, and privilege assemblies. |
| AC6 | T4 | CMD1, CMD3 | M2 | Exact current design authority and forbidden inference. |
| AC7 | T6-T8 | CMD1, CMD3 | M3 | No-clobber, identity guard, and read-back boundaries. |
| AC8 | T9-T10 | CMD1, CMD3 | M3 | Dependencies, intermediate validity, exact partial state, and pre-write atomic-group block. |
| AC9 | T2, T11 | CMD1, CMD3 | M2 | External state is read-only and hosted observation is fixed. |
| AC10 | T5 | CMD1-CMD3 | M2 | Forbidden skeleton content is absent. |
| AC11 | T12 | CMD1, CMD3 | M1 | Every rule and consumed literal has one treatment. |
| AC12 | T13 | CMD1, CMD3 | M4 | Every assembly and variant decreases and total package remains visible. |
| AC13 | T14 | CMD2-CMD6 | M4 | Canonical-through-installed inventory and raw-byte parity. |
| AC14 | T11, T14 | CMD1-CMD9 | M4 | Acceptance has no live workflow, PR, target runtime, or prose-grading gate. |
| AC15 | T8-T10, T14 | CMD1, CMD3 | M1 | Architecture triggers are explicit and fail closed. |
| AC16 | T12, T14 | CMD1-CMD7 | M1 | Legacy overlaps have exact dispositions and retained clauses remain active. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T11 | Root-only review, no mutation, fixed hosted observation. |
| E2 | T1, T3, T5-T6 | Coverage create selects CIM2 and no-clobber commit. |
| E3 | T4 | Approved-design realization and omitted-field safe-default stop. |
| E4 | T6 | Concurrent appearance cannot be overwritten. |
| E5 | T7 | Concurrent identity change cannot be overwritten. |
| E6 | T9-T10 | Provider-first ordered batch and group completion. |
| E7 | T9 | Atomic-group-required blocks before write and routes architecture need. |
| E8 | T3 | Mapping/composition disagreement stops without local precedence. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1: missing review target | T2 | Read-only `missing-target`; no create or mutation. |
| EC2: GitHub target with other provider | T2, T15 | Invalid combination fails before provider procedure. |
| EC3: path-filter edit affects coverage | T3 | Risk map becomes required before judgment or mutation. |
| EC4: privileged design cannot safely default | T4 | Stop without inference or partial implementation. |
| EC5: target appears or changes after preflight | T6-T7 | Conditional commit fails without overwrite. |
| EC6: read-back differs | T8 | No success claim; result is blocked and bytes are uncertain. |
| EC7: provider commits but wrapper blocks | T10 | `partial-blocked` names both sets and proves provider validity. |
| EC8: retry after unrelated changes | T10 | Rebuild graph; do not resume stale manifest. |
| EC9: skeleton absent for narrow revise | T5 | Compatible revise proceeds because the asset predicate is false. |
| EC10: root shrinks but complete package grows | T13 | Per-assembly gate and total-package disclosure remain separate. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R4, R5, R6, R7, R11, R23, R35, R40, R42, R43, R46 | BND-INPUT-001 | T1-T2, T4, T9, T11, T15 | contract | automated | CMD1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R5, R12, R29, R30, R31, R33, R34, R35, R38, R39, R40, R41 | BND-STATE-001 | T2, T4, T6-T10 | contract | automated | CMD1 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 | - | - |
| PRF-003 | covered | R5, R8, R9, R10, R12, R13, R14, R16, R20, R23, R28, R29, R30, R31, R34 | BND-AUTH-001 | T2-T7 | contract | automated | CMD1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R15, R17, R18, R19, R21, R22, R23, R24, R25, R26, R27, R28, R50, R51 | BND-COMPOSE-001 | T1, T3-T5, T14 | integration | automated | CMD1-CMD6 | `evidence/m4-package-proof.md` | M4 | - | - |
| PRF-005 | covered | R29, R30, R31, R32, R33, R34, R36, R37, R38, R40, R41 | BND-TEMPORAL-001 | T6-T10 | integration | automated | CMD1 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 | - | - |
| PRF-006 | covered | R20, R27, R30, R31, R33, R34, R39, R40, R41, R53 | BND-RECOVERY-001 | T3, T5-T10 | contract | automated | CMD1 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 | - | - |
| PRF-007 | covered | R21, R22, R23, R24, R25, R45, R46, R47, R48, R49, R50, R51, R54 | BND-COMPAT-001 | T5, T12-T14 | integration | automated | CMD1-CMD7 | `evidence/m4-package-proof.md` | M4 | - | - |
| PRF-008 | covered | R8, R9, R10, R13, R29, R30, R31, R32, R33, R43, R44, R50, R52, R53 | BND-ENV-001 | T2, T4, T6-T11, T14 | integration | automated | CMD1-CMD6 | `evidence/m4-package-proof.md` | M4 | - | - |
| PRF-009 | covered | R4, R5, R6, R7, R8, R10, R25, R26 | INT-001 | T1-T2, T5, T15 | contract | automated | CMD1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R12, R13, R14, R21, R22, R25, R28 | INT-002 | T4-T5 | contract | automated | CMD1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R15, R16, R17, R18, R19, R20 | INT-003 | T3 | contract | automated | CMD1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R29, R30, R31, R32, R33, R34 | INT-004 | T6-T8 | integration | automated | CMD1 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 | - | - |
| PRF-013 | covered | R35, R36, R37, R38, R39, R40, R41 | INT-005 | T9-T10 | integration | automated | CMD1 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 | - | - |
| PRF-014 | covered | R42, R43, R44, R47, R48, R49, R50, R52 | INT-006 | T11-T14 | integration | automated | CMD1-CMD7 | `evidence/m4-package-proof.md` | M4 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests` | planned-for-implementation | M1 focused fixtures and validator tests | M1-M4 | M1 | Stop the milestone on any failed scenario or assertion. | A missing class or zero selected tests fails. | milestone evidence for M1-M4 | Local read/write only inside test-owned temporary directories. |
| CMD2 | `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md` | existing/configured | repository skill validation | M2-M4 | M2 | Stop on structural, mapping, path, or resource failure. | Not applicable; validates one explicit skill. | `evidence/m2-package-implementation.md` | Reads canonical skill package only. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | repository skill-validator regression suite | M2-M4 | M2 | Stop on any failure. | Zero discovered tests fails under the existing runner. | milestone evidence for M2-M4 | Local tests and temporary fixtures only. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | repository build regression suite | M2-M4 | M2 | Stop on build or package-selection regression. | Zero discovered tests fails under the existing runner. | `evidence/m4-package-proof.md` | Temporary package trees only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | repository skill builder | M2-M4 | M2 | Stop on canonical/generated drift or invalid inventory. | Not applicable; explicit check mode. | `evidence/m4-package-proof.md` | Read-only check mode. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution regression suite | M4 | M4 | Stop on generated, archive, release-candidate, or install parity failure. | Zero discovered tests fails under the existing runner. | `evidence/m4-package-proof.md` | Temporary adapter/package/install trees; no publication. |
| CMD7 | `python scripts/validate-boundary-first.py --check --path specs/ci-maintenance-skill-simplification.md` | existing/configured | boundary-first validator | M4 | M4 | Stop on missing, stale, malformed, or unproved boundary/proof IDs. | Not applicable; explicit spec path. | `evidence/m4-package-proof.md` | Read-only structural and proof-map validation. |
| CMD8 | `python scripts/validate-change-metadata.py docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml` | existing/configured | change-metadata validator | M1-M5 | M1 | Stop on lifecycle, vocabulary, evidence, or milestone inconsistency. | Not applicable; explicit record path. | stage-owned evidence | Read-only metadata validation. |
| CMD9 | `python scripts/validate-documentation-prose.py --mode audit --path specs/ci-maintenance-skill-simplification.md --path specs/ci-maintenance-skill-simplification.test.md --path docs/plans/2026-08-19-ci-maintenance-skill-simplification.md` | existing/configured | documentation prose validator | M1-M5 | test-spec-review | Stop on errors; review and resolve warnings before claims. | Not applicable; explicit paths. | review and final verification evidence | Read-only audit mode. |
| CMD10 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | existing/configured | repository PR validation wrapper | M5 | M5 | Stop final closeout on any blocking check. | The wrapper's own zero-test and missing-command policy applies. | `verify-report.md` | Local PR-mode validation; does not open a PR or run hosted CI. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T12-T13, T15 | none | CMD1, CMD8-CMD9 | `evidence/m1-preservation-inventories.md`, `evidence/profile-size-baseline.md` | M1 code review | Freeze ownership, compatibility, baselines, unknown values, and architecture-trigger absence before package edits. |
| M2 | T1-T5, T11-T12, T15 | none | CMD1-CMD5, CMD8-CMD9 | `evidence/m2-package-implementation.md` | M2 code review | Prove package split, classifications, assemblies, policy ownership, privilege, skeleton, resource safety, and claims. |
| M3 | T6-T10, T15 | none | CMD1-CMD3, CMD5, CMD8-CMD9 | `evidence/m3-conditional-commit-and-batch-proof.md` | M3 code review | Prove single-file concurrency, read-back, capability stops, dependency ordering, partial results, and retry. |
| M4 | T12-T15 | none | CMD1-CMD9 | measurements, preservation review, and `evidence/m4-package-proof.md` | M4 code review | Prove final semantics, boundaries, every assembly, package parity, and excluded execution surfaces. |
| M5 | T1-T15 | none | CMD1-CMD10 | final review, explanation, review resolution when required, and verify report | PR handoff | Final holistic coherence only after all implementation milestones close. |

## Test cases

### T1. Closed axes select exactly one supported assembly

- Covers: R1-R7, R25-R28, R42; E1-E2; AC2-AC3, AC5; BND-INPUT-001, BND-COMPOSE-001; INT-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Every valid operation, target, provider, concern, privilege, and structure combination plus late-discovered predicates.
- Steps: Resolve each axis independently, select resources, then introduce a late coverage, structure, or privilege predicate before dependent judgment.
- Expected result: Every valid invocation selects exactly one named assembly and its conditional variant; late predicates load exact additions once; external evidence is reported separately.
- Failure proves: The assembly model is incomplete, duplicated, or allows dependent judgment under an underloaded profile.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `CiMaintenanceSkillSimplificationTests`
- Required by milestone: M2

### T2. Target and provider compatibility fail closed

- Covers: R5-R10; E1; EC1-EC2; AC3, AC9; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-ENV-001; INT-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Absent, existing, ambiguous, escaped, and conflicting repository targets across GitHub, project-native, external, and invalid provider/storage combinations.
- Steps: Exercise create, revise, and review against every target state and compatibility row.
- Expected result: Valid repository-file combinations use exact procedure; missing review target is read-only; external state routes only; every unsupported or ambiguous combination stops without fallback.
- Failure proves: Operation changes silently, provider procedure leaks across targets, or external state becomes mutable.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `CiMaintenanceSkillSimplificationTests`
- Required by milestone: M2

### T3. Risk placement and GitHub serialization have one owner

- Covers: R15-R20; E8; EC3; AC4; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-003.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Complete, missing, stale, and conflicting risk maps; narrow concern reviews; coverage-sensitive path, trigger, job, matrix, and command changes.
- Steps: Classify map applicability and compare settled placement with requested GitHub composition.
- Expected result: The map alone selects checks and boundaries; the authoring reference only serializes them; narrow non-coverage review omits the map; conflict stops with the exact risk.
- Failure proves: Policy ownership overlaps, coverage-sensitive work bypasses the map, or a missing command is invented.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `CiMaintenanceSkillSimplificationTests`
- Required by milestone: M2

### T4. Privileged realization binds exact approved design

- Covers: R11-R14, R25, R28; E3; EC4; AC5-AC6; BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001, BND-ENV-001; INT-002.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Ordinary, approved, absent, stale, conflicting, target-mismatched, non-approved, and ambiguous design bases with complete and omitted fields.
- Steps: Review and mutate each context, including a compatible safe default and a field that cannot safely default.
- Expected result: Review remains read-only; mutation uses only one exact approved design; compatible defaults remain safe; every unsupported omission or inference stops.
- Failure proves: Procedure, skeleton, conversation, or general knowledge grants privileged authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `CiMaintenanceSkillSimplificationTests`
- Required by milestone: M2

### T5. Resource triggers and minimal skeleton are exact

- Covers: R1, R21-R28; EC9; AC2, AC5, AC10; BND-COMPOSE-001, BND-COMPAT-001; INT-001-INT-002.
- Level: contract
- Command IDs: CMD1-CMD3
- Fixture/setup: All resource predicates; missing, unreadable, escaped, stale, contradictory, and mixed-version resources; skeleton content inventory.
- Steps: Select each profile, inspect the skeleton, and remove or corrupt each triggered and untriggered resource in turn.
- Expected result: Triggered resources fail closed; untriggered resources do not block; the skeleton contains only approved safe structure and no forbidden examples or policy.
- Failure proves: Procedure is reconstructed, an unneeded resource blocks, or the skeleton grants behavior or privilege.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: focused fixtures and skill validation
- Required by milestone: M2

### T6. Create uses atomic no-clobber

- Covers: R29-R30, R32-R34; E4; EC5; AC7; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004.
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Temporary targets absent at preflight, unchanged through commit, appearing before commit, and already equal to intended content.
- Steps: Exercise the described create commit point and idempotent retry classification.
- Expected result: Only commit-time absence creates; a concurrent file is never replaced; exact intended content with unchanged basis is idempotent.
- Failure proves: Preflight or overwrite-capable rename is treated as no-clobber safety.
- Evidence artifact: `evidence/m3-conditional-commit-and-batch-proof.md`
- Automation location: deterministic temporary-filesystem fixtures
- Required by milestone: M3

### T7. Revise uses identity-guarded replacement

- Covers: R29, R31-R34; E5; EC5; AC7; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004.
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Temporary target at prior identity A, unchanged A, concurrently changed B, intended identity, and unrelated content.
- Steps: Exercise the described revision commit point and retry classification.
- Expected result: Replacement occurs only while current identity equals A; B is preserved and blocks; exact intended content is idempotent only under unchanged evidence.
- Failure proves: Revision can overwrite concurrent or unrelated work.
- Evidence artifact: `evidence/m3-conditional-commit-and-batch-proof.md`
- Automation location: deterministic temporary-filesystem fixtures
- Required by milestone: M3

### T8. Commit capability, read-back, and retry remain fail closed

- Covers: R32-R34, R41, R53; EC6; AC7, AC15; BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Unsupported conditional primitives, successful commit with matching and mismatching read-back, stale evidence, and architecture-triggering persistence requests.
- Steps: Classify each capability and result, then retry from current state.
- Expected result: Unsupported or uncertain environments block; read-back confirms only; stale evidence reclassifies; persistent coordination routes to architecture.
- Failure proves: The contract weakens concurrency safety or adopts uncertain output to avoid architecture work.
- Evidence artifact: `evidence/m3-conditional-commit-and-batch-proof.md`
- Automation location: focused scenario fixtures
- Required by milestone: M3

### T9. Batch classification and ordering protect dependencies

- Covers: R35-R39; E6-E7; AC8, AC15; BND-INPUT-001, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-005.
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Independent targets, a script-provider/workflow-wrapper dependency, changed shared configuration, cycles, and target sets with no safe intermediate state.
- Steps: Build the full manifest, validate references, classify the graph, and determine commit order before mutation.
- Expected result: Independent targets remain independent; providers precede wrappers; incomplete dependencies cannot commit; cycles or unsafe states return `blocked-before-write` without mutation.
- Failure proves: Dependency-free sequencing or unsupported atomicity can expose an invalid repository state.
- Evidence artifact: `evidence/m3-conditional-commit-and-batch-proof.md`
- Automation location: deterministic dependency-graph fixtures
- Required by milestone: M3

### T10. Partial batch results and retry are exact

- Covers: R36-R41; EC7-EC8; AC8, AC15; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-005.
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Complete batch, independently valid provider followed by blocked wrapper, invalid completed target, and retry after related or unrelated changes.
- Steps: Apply safe manifest order, interrupt or block at each target, report aggregate state, then invoke a fresh retry.
- Expected result: Only all-success is complete; partial-blocked reports exact completed and pending targets plus validity; retry rebuilds the graph and rejects stale adoption.
- Failure proves: Partial work implies group success or stale in-memory state controls retry.
- Evidence artifact: `evidence/m3-conditional-commit-and-batch-proof.md`
- Automation location: deterministic dependency-graph fixtures
- Required by milestone: M3

### T11. Result and claim boundaries remain truthful

- Covers: R9, R42-R44, R52; E1; AC9, AC14; BND-INPUT-001, BND-ENV-001; INT-006.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Review, create, revise, complete, blocked, and partial results with configured commands, local validation, read-back, and no hosted execution.
- Steps: Render every result and scan closed fields and forbidden claims.
- Expected result: Required fields are present; hosted observation is always `not-performed-by-ci-maintenance`; no external mutation or downstream readiness is claimed.
- Failure proves: Static or local evidence is misrepresented as hosted CI or lifecycle readiness.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: focused result fixtures
- Required by milestone: M2

### T12. Semantic, literal, and legacy-clause ownership migrate atomically

- Covers: R45-R46, R54; AC11, AC16; BND-COMPAT-001; INT-006.
- Level: contract
- Command IDs: CMD1, CMD3, CMD7
- Fixture/setup: Current rules, literals, five amended clauses, all unlisted legacy clauses, parser consumers, incidental prose, duplicates, and unknown dispositions.
- Steps: Validate ledgers before and after migration and compare every coupled consumer with its owner.
- Expected result: Every item has one treatment and owner, amended consumers follow new authority, unlisted clauses remain active, duplicates and unknown values fail first.
- Failure proves: Extraction loses behavior, leaves conflicting authority, or freezes incidental prose.
- Evidence artifact: `evidence/m1-preservation-inventories.md`, `evidence/semantic-preservation-review.md`
- Automation location: focused ledger and validator fixtures
- Required by milestone: M1

### T13. Every real assembly decreases with honest accounting

- Covers: R47-R49; EC10; AC12; BND-COMPAT-001; INT-006.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Frozen canonical baseline, final root/resources, fixed assemblies, conditional CIM5/CIM6/CIM8 variants, external evidence, and complete package.
- Steps: LF-normalize, count Unicode whitespace-separated words and UTF-8 bytes, include each unique packaged file once, and compare every profile.
- Expected result: Every supported assembly strictly decreases in both metrics; total package and external-evidence exclusions remain separately visible.
- Failure proves: Root-only shrinkage, double counting, hidden privileged growth, or misleading token-only reporting.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: focused deterministic measurement fixture
- Required by milestone: M4

### T14. Package parity and acceptance boundaries hold

- Covers: R1, R50-R54; AC2, AC13-AC16; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006.
- Level: integration
- Command IDs: CMD2-CMD7, CMD9
- Fixture/setup: Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode package trees plus missing, transformed, escaped, additional, and mixed resources.
- Steps: Build/check packages, validate inventory and raw bytes, inspect public portability, and confirm excluded runtime/external operations remain absent.
- Expected result: Every target has exact required resources once, drift fails, public text remains portable, and no architecture trigger or excluded acceptance surface is introduced.
- Failure proves: A supported distribution ships a different contract or implementation expands architecture/testing scope.
- Evidence artifact: `evidence/m4-package-proof.md`
- Automation location: existing build and adapter distribution suites
- Required by milestone: M4

### T15. Unknown closed values fail before consistency checks

- Covers: R4, R6-R7, R11, R23, R25, R35, R40, R43, R46; AC3; BND-INPUT-001; INT-001.
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: One unknown value for each new or changed closed vocabulary, with otherwise valid and consistency-invalid variants.
- Steps: Validate each fixture and inspect error ordering and identity.
- Expected result: Every unknown produces an explicit unknown-value failure before dependent consistency checks; fixture or test names contain `unknown_value` or `not_in_vocabulary`.
- Failure proves: A closed vocabulary silently falls through to behavior or a misleading secondary error.
- Evidence artifact: milestone evidence for M1-M3
- Automation location: focused and broad validator regression tests
- Required by milestone: M1

## Fixtures and data

- `docs/changes/2026-08-19-ci-maintenance-skill-simplification/fixtures/` will hold deterministic YAML/Markdown scenario inputs for classifications, assemblies, authority, resources, results, conditional commits, dependencies, compatibility, and measurements.
- Test-owned temporary directories will model repository files and package/install trees; fixtures must not access live host settings, credentials, hosted workflows, or external accounts.
- M1 rule and literal ledgers are proof inputs, not new normative behavior owners.
- Baseline files record exact canonical identities, LF-normalization, word/byte formulas, and every assembly composition.

## Mocking/stubbing policy

Stub only external host state, unavailable filesystem capability, and package/install roots through deterministic local fixtures. Do not mock the classifier, ownership decision, target-state transition, dependency ordering, measurement formula, or validator under test. No provider API, hosted CI runner, target-agent runtime, or external network call is used.

## Migration or compatibility tests

T12 proves the five explicit R54 amendments and retention of every unlisted legacy clause. T14 proves atomic migration across canonical and every derived package. Existing project workflows remain untouched unless independently targeted by a later real maintenance invocation. Rollback restores the prior flat package and coupled consumers without migrating historical workflows.

## Observability verification

T1-T11 verify visible classifications, resource selections, external evidence, target identities, commit/batch outcomes, blockers, validation evidence, and hosted observation. T12-T14 verify disposition and measurement reports. No telemetry or external audit service is introduced.

## Security/privacy verification

T2-T5 and T11 prove exact authority, least-privilege skeleton defaults, fork/secret and privileged-design boundaries, no external mutation, and forbidden claims. Fixtures contain no credentials, tokens, private keys, real secret names, inaccessible evidence, or unnecessary personal data.

## Performance checks

T13's LF-normalized words and UTF-8 bytes are the required loaded-context metrics. Cache, matrix, or CI runtime optimization remains project-evidence-bound and is not benchmarked here. No wall-clock, tokenizer, hosted-runner, or target-agent performance gate is introduced.

## Manual QA checklist

Not applicable. Every requirement, boundary, interaction, example, edge case, and acceptance criterion has deterministic automated or contract proof. Ordinary independent lifecycle reviews remain required gates but are not a separate manual proof procedure.

## What not to test and why

- Do not open a live PR or execute a hosted workflow; the change is published guidance and repository packaging, and hosted observation remains explicitly unperformed.
- Do not run Codex, Claude Code, opencode, or another target-agent runtime; deterministic contract and package proof owns acceptance.
- Do not grade prose quality with a model or manual semantic rubric beyond ordinary lifecycle review; exact structural, behavioral, readability, and ownership assertions are sufficient.
- Do not mutate branch protection, environments, cloud accounts, secrets, or other external platform state; those surfaces are review-or-route only.
- Do not test privileged design quality; architecture/security owners approve that design, while this skill only validates exact current authority and bounded realization.
- Do not require multi-file atomicity or cross-session recovery; `atomic-group-required` stops before write and retry rebuilds current state.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation may begin only after approving review settlement and workflow routing.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer-review approval, implementation readiness, command execution, hosted-CI status, verification, branch readiness, or PR readiness.
