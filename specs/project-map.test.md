<!-- Template: test-spec-skeleton-v1 -->

# Project-Map Skill Contract Test Specification

## Owning change record

`docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/project-map.md`
- Plan: `docs/plans/2026-08-14-project-map-skill-simplification.md`
- Architecture/ADRs: `docs/architecture/system/architecture.md`; existing published-skill resource-integrity and progressive-disclosure ADRs; no new ADR

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/project-map.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-14-project-map-skill-simplification/reviews/spec-review-r1.md` |
| Architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r1`; `docs/changes/2026-08-14-project-map-skill-simplification/reviews/architecture-review-r1.md` |
| Execution plan | `docs/plans/2026-08-14-project-map-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-14-project-map-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic contract fixtures for operation and target selection, coordination preflight, resource assembly, universal evidence rules, root/area structure, area transaction recovery, compatibility, and missing resources. Existing validators own permanent skill, boundary, lifecycle, build, and distribution checks. Change-local ledgers and measurements prove semantic disposition and loaded-profile reduction, while MP0 and MP1 provide the semantic judgments deterministic validation cannot make. No target-agent runtime, transcript grading, prompt journey, tokenizer dependency, network service, publication, or release action is part of acceptance.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R5 | T1, T7, T14 | contract | Orientation-only role, portability, normalized skill shape, and workflow role. |
| R6-R15 | T1-T4, T12 | contract | Closed operation/scope output, target-state selection, audit isolation, and placement. |
| R16-R29 | T5, T6, T13 | contract | Metadata, freshness, dirty baselines, refresh triggers, and correction notes. |
| R30-R48 | T5, T13 | contract | Evidence classes, source ranking, command truthfulness, and runtime evidence. |
| R49-R71 | T7-T10 | contract | Root/area relationships, structural ownership, required sections, and diagrams. |
| R72-R84 | T1, T14-T17 | integration | Reliance, handoff, rollout bounds, generated resources, and behavior preservation. |
| R85-R101 | T2-T4, T7, T14-T16 | contract | Package ownership, bounded preflight, PMA0/PMA1, late loading, and fail-safe resources. |
| R102-R111 | T8-T11 | contract | Existing-root prerequisite, complete identity, commit order, retry, conflict, and audit isolation. |
| R112-R117 | T1, T12, T14-T17 | integration | Result migration, semantic/literal preservation, deterministic measurement, parity, and no target runtime. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T7 | Root creation composes the required map structure from the skeleton. |
| E2 | T8-T10 | Area maps name and register their parent through the root. |
| E3 | T5 | Intent artifacts never become current-state proof. |
| E4 | T13 | Configured and executed commands retain distinct evidence. |
| E5 | T5, T6 | Dirty Git evidence records SHA+dirty and inspected paths. |
| E6 | T6 | Wrong-at-baseline evidence emits a correction note without a new status. |
| E7 | T1 | Create cannot replace an existing target. |
| E8 | T1, T4 | Audit remains read-only, including missing targets and later correction. |
| E9 | T2 | PMA0 is selected only after all seven preflight surfaces are clear. |
| E10 | T3 | Late coordination discovery loads PMA1 without changing operation or scope. |
| E11 | T9 | Area content is validated before root registration commits the operation. |
| E12 | T10, T11 | Exact partial state is recoverable and mismatched state is rejected. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71, R72, R73, R74, R75, R76, R77, R78, R79, R80, R81, R82, R83, R84, R85, R86, R87, R88, R89, R90, R91, R92, R93, R94, R95, R96, R97, R98, R99, R100, R101, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111, R112, R113, R114, R115, R116, R117

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R6, R7, R8, R9, R10, R11, R93, R94, R95, R96, R97, R98, R99, R100, R112, R113 | BND-INPUT-001 | T1, T2, T3, T12 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R7, R8, R9, R10, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | BND-STATE-001 | T1, T5, T6, T8, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R10, R14, R15, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | BND-AUTH-001 | T4, T5, T8, T9, T10, T11, T13 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-implementation.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R85, R86, R87, R88, R89, R90, R91, R92, R93, R94, R95, R96, R97, R98, R99, R100, R101 | BND-COMPOSE-001 | T2, T3, T4, T7, T8, T14, T15 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | MP1 | - |
| PRF-005 | covered | R100, R104, R105, R106, R107, R108, R109, R110, R111 | BND-TEMPORAL-001 | T3, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R57, R95, R101, R108, R109, R110, R111 | BND-RECOVERY-001 | T4, T5, T6, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R81, R82, R83, R84, R112, R113, R114, R115, R116, R117 | BND-COMPAT-001 | T12, T14, T15, T16, T17 | integration | hybrid | CMD1, CMD2, CMD4, CMD5, CMD6, CMD7, CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R23, R24, R25, R42, R43, R44, R45, R46, R47, R48, R93, R94, R95 | BND-ENV-001 | T2, T5, T13, T15 | integration | automated | CMD2, CMD3, CMD7 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R6, R7, R8, R9, R10, R112, R113 | INT-001 | T1, T12 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R93, R94, R95, R96, R97, R98, R99, R100, R101 | INT-002 | T2, T3, T4 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R102, R103, R104, R105, R106, R107, R108, R109, R110, R111 | INT-003 | T8, T9, T10, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R23, R24, R25, R26, R27, R28, R29, R87, R116 | INT-004 | T5, T6, T16 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-implementation.md`; `evidence/simplification-measurements.md` | M3 | MP1 | - |
| PRF-013 | covered | R85, R86, R87, R88, R89, R90, R91, R101, R112, R113, R114, R115, R116, R117 | INT-005 | T4, T7, T12, T14, T15, T16, T17 | integration | hybrid | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| Unknown operation, scope, disposition, literal class, status, or proof value | T1, T12, T14 | Fail closed before consistency checks or writes. |
| Create targets an existing map or refresh targets an absent map | T1 | Stop and name the required operation without converting it. |
| Audit target is absent or correction is requested after audit | T1, T4 | Emit `missing-map` without mutation; correction starts a new refresh. |
| Known coordination surface is unavailable, conflicting, or discovered late | T2-T4 | Load PMA1 before dependent work or stop when its reference is unavailable. |
| Git is unavailable or inspected paths are dirty | T5 | Record the alternate baseline or SHA+dirty with inspected paths. |
| Prior claim was wrong at its original baseline | T6 | Emit one correction note and retain the three-value freshness vocabulary. |
| Area creation has no valid root | T8 | Stop and route to root creation without implicit root creation. |
| Root changes after the area file is written | T9-T11 | Stop without overwriting or adopting the changed root. |
| Orphan area, dangling registration, conflicting parent, or multiple candidates | T10, T11 | Reconcile only exact missing registration; every mismatch stops. |
| Required reference is missing, unreadable, escaped, contradictory, or mixed | T4, T15 | Stop dependent behavior without remembered reconstruction. |
| Main file shrinks while PMA0 or PMA1 grows | T16 | Acceptance fails unless an independently approved semantic-preservation exception names the reason. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-14-project-map-skill-simplification"); load=lambda path: json.loads(path.read_text(encoding="utf-8")); rules=load(root/"project-map-rule-disposition.yaml")["rules"]; literals=load(root/"project-map-literal-compatibility.yaml")["literals"]; scenarios=load(root/"fixtures/scenario-contracts.yaml")["scenarios"]; bad_rule=load(root/"fixtures/invalid-rule-disposition.yaml"); bad_literal=load(root/"fixtures/invalid-literal-classification.yaml"); rd={"retained-inline","retained-maintenance-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete","historical-fixture"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else []); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else []); assert rules and literals and scenarios; assert all(vr(row)==[] for row in rules); assert all(vl(row)==[] for row in literals); assert vr(bad_rule)[0]=="unknown-disposition"; assert vl(bad_literal)[0]=="unknown-classification"; assert len({row["rule_id"] for row in rules})==len(rules); assert len({row["literal_id"] for row in literals})==len(literals); assert len({row["scenario"] for row in scenarios})==len(scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Reject unknown values first, then missing fields, duplicates, or scenario drift. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/project-map/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block structure, mapping, containment, placeholder, or claim defects. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py ProjectMapSkillSimplificationTests` | planned-for-implementation | implement | M2 | M2 code-review | Block operation, assembly, transaction, structure, or failure defects. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block broad skill-contract regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Repository-local tests; no target-agent runtime. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource regression. | Zero discovered tests is failure. | `evidence/m2-package-implementation.md` | Temporary filesystem only. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-package drift or missing resources. | Not applicable. | `evidence/m2-package-implementation.md` | Read-only check against canonical sources. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD8 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "project-map"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Block generated, archive, or installed resource mismatch. | Not applicable; all supported targets are selected. | `evidence/m3-package-proof.md` | Fresh temporary directory; no publication, network, or agent execution. |
| CMD9 | `python scripts/validate-boundary-first.py --check --path specs/project-map.md` | existing/configured | implement | M2 | M2 code-review | Block invalid or missing proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m2-package-implementation.md` | Read-only repository validation. |
| CMD10 | `python scripts/validate-change-metadata.py docs/changes/2026-08-14-project-map-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | Every state-changing handoff | Block invalid artifact, review, or planned-work state. | Not applicable. | Owning change validation ledger | Read-only validation. |
| CMD11 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-14-project-map-skill-simplification` | existing/configured | review stages | lifecycle | Every formal review handoff | Block malformed or missing review evidence. | Not applicable. | Review log and records | Read-only validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T14, T16 | MP0 | CMD1, CMD10 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged while ownership and baselines are frozen. |
| M2 | T1-T14 | none | CMD2-CMD6, CMD9-CMD11 | `evidence/m2-package-implementation.md` | M2 code-review | Focused failing assertions precede the atomic canonical package change. |
| M3 | T12-T17 | MP1 | CMD1-CMD11 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves assembly reduction, semantics, boundary coverage, and package parity. |
| M4 | T17 | MP1 | CMD1-CMD11 | Final review, explanation, and verify evidence | verify | Lifecycle closeout begins only after M1-M3 are closed. |

## Test cases

### T1. Operation and target state select one valid outcome

- Covers: R6-R11, R112-R113; E7-E8; BND-INPUT-001, BND-STATE-001, BND-COMPAT-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Every create, refresh, and audit combination with absent, existing, ambiguous, and conflicting repository or area targets.
- Steps: Classify the operation and scope, resolve the target state, and inspect the emitted result without performing repository mutation.
- Expected result: Create accepts only absence, refresh accepts only existence, audit remains read-only, full rewrite remains refresh, and invalid combinations stop without conversion.
- Failure proves: Operation names can bypass target-state procedure or acquire unintended writes.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `scripts/test-skill-validator.py` focused fixtures.
- Required by milestone: M2

### T2. Coordination preflight selects PMA0 only after all known surfaces are clear

- Covers: R93-R99; E9; BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Each of the seven preflight surfaces individually empty, present, unavailable, conflicting, and ambiguous.
- Steps: Run the bounded preflight and classify the procedural assembly.
- Expected result: Only a clear no-evidence result selects PMA0; any coordination selects PMA1, and unresolved known surfaces require reference-owned resolution or stop.
- Failure proves: Simple root creation can omit required coordination procedure.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused static scenario fixtures.
- Required by milestone: M2

### T3. Late coordination discovery loads PMA1 without reclassifying the request

- Covers: R96-R100; E10; BND-INPUT-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Root creation initially classified PMA0 that later discovers an area file or registration before writing.
- Steps: Discover coordination after the first preflight and before dependent judgment.
- Expected result: The reference loads once, operation remains create, scope remains repository, and no dependent write precedes PMA1.
- Failure proves: Late evidence causes stale classification, duplicated loading, or unsafe writes.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused static scenario fixtures.
- Required by milestone: M2

### T4. Required-resource failure stops dependent procedure

- Covers: R85-R101; E9-E10; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-002, INT-005
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Missing, unreadable, escaped, contradictory, and mixed-version conditional references plus untriggered missing-reference control.
- Steps: Exercise PMA1 and PMA0 resource loading.
- Expected result: Defective required resources stop before dependent judgment or writes; PMA0 does not load or depend on an untriggered reference.
- Failure proves: The shortened common path reconstructs or partially executes missing procedure.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Skill and resource-map validator fixtures.
- Required by milestone: M2

### T5. Universal evidence, freshness, and command meanings remain inline

- Covers: R16-R25, R30-R48; E3-E5; BND-STATE-001, BND-AUTH-001, BND-ENV-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Current, partial, stale, inferred, unknown, Git-unavailable, dirty-worktree, configured-command, and executed-command scenarios.
- Steps: Evaluate each scenario using `SKILL.md` without requiring the maintenance reference where its trigger is false.
- Expected result: Evidence and statuses retain their exact meanings, material claims cite paths, dirty baselines name inspected paths, and commands never overclaim execution.
- Failure proves: A universal safety rule moved behind conditional loading or changed meaning.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused canonical skill assertions and static scenarios.
- Required by milestone: M2

### T6. Refresh comparison produces truthful freshness and correction outcomes

- Covers: R19-R29, R87; E5-E6; BND-STATE-001, BND-RECOVERY-001; INT-004
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Material cited changes, unrelated changes, unavailable evidence, and wrong-at-baseline claims.
- Steps: Load PMA1, compare current and prior evidence, and classify the result.
- Expected result: Material changes affect freshness, unrelated changes do not stale every map, unavailable evidence stays partial or unknown, and wrong prior claims produce correction notes without a fourth status.
- Failure proves: Relocated refresh procedure changes the public freshness contract.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused refresh fixtures.
- Required by milestone: M2

### T7. Skeleton remains the sole structural owner

- Covers: R49-R65, R85-R92; E1-E2; BND-COMPOSE-001; INT-005
- Level: contract
- Command IDs: CMD2-CMD5
- Fixture/setup: Root without areas, root with registered areas, and area output assembled from the canonical skeleton.
- Steps: Inspect canonical ownership and compose representative outputs.
- Expected result: The skeleton owns labels, required section order, tables, and placeholders; `Area maps` is conditional; no output retains placeholders; no policy moves into the asset.
- Failure proves: Structure is duplicated or the asset becomes a policy owner.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Skill validator and representative output fixtures.
- Required by milestone: M2

### T8. Area creation requires an existing valid root and absent targets

- Covers: R49-R57, R102-R105; E2, E11; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Missing root, malformed root, existing area, existing registration, and one valid root with both targets absent.
- Steps: Resolve the area transaction prerequisites and intended identities.
- Expected result: Only one valid root with absent area and registration proceeds; no invocation implicitly creates a root or adopts existing state.
- Failure proves: Area creation expands scope or starts from conflicting identity.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static transaction fixtures.
- Required by milestone: M2

### T9. Area registration is the final commit write

- Covers: R104-R107; E11; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Valid area transaction plus interruption before area write, after area write, and before registration.
- Steps: Bind identities, validate and write the area, re-read the root, register last, and validate reciprocal fields.
- Expected result: The root registration is written only after complete area validation and unchanged-root confirmation and acts as the commit point.
- Failure proves: A dangling root row can publish an absent area or a stale root can be overwritten.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static ordered-write fixtures.
- Required by milestone: M2

### T10. Exact missing-registration retry completes idempotently

- Covers: R108-R110; E12; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Matching area without registration and fully committed matching artifacts.
- Steps: Replay the original transaction identity in each state.
- Expected result: The first state completes only registration, and the fully committed state returns success without another write.
- Failure proves: Retry duplicates writes or cannot safely recover its exact partial state.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static retry fixtures.
- Required by milestone: M2

### T11. Conflicting area transaction states fail closed

- Covers: R108-R111; E12; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Mismatched area identity, dangling registration, changed root, stale basis, conflicting parent, and multiple candidates.
- Steps: Attempt retry and audit each state.
- Expected result: Mutation stops without adoption or overwrite; audit may report the state but remains read-only.
- Failure proves: Retry or audit can corrupt root/area consistency.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Static conflict fixtures.
- Required by milestone: M2

### T12. Result and literal compatibility use read-old/write-new behavior

- Covers: R6-R11, R112-R115; E7-E8; BND-INPUT-001, BND-COMPAT-001; INT-001, INT-005
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: New results, each legacy mode, ambiguous legacy area, parser consumers, incidental assertions, and historical fixtures.
- Steps: Emit new results and classify or migrate every legacy consumer.
- Expected result: New output contains `Operation` and `Map scope` only; deterministic legacy forms map correctly; ambiguous area stops; real contracts migrate atomically; historical maps remain readable.
- Failure proves: Old and new output contracts are mixed or tests become prose-policy owners.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md`
- Automation location: Ledger proof and focused compatibility fixtures.
- Required by milestone: M2

### T13. Command and runtime claims remain evidence-bound

- Covers: R34-R48, R66-R71; E3-E4; BND-AUTH-001, BND-ENV-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Static trace, test-demonstrated flow, actual execution, inference, configured command, and risky command request.
- Steps: Produce representative claims and diagram edges for each evidence mode.
- Expected result: Paths support material claims, evidence modes remain visible, risky execution requires go-ahead, and diagrams do not present planned or inferred flow as observed runtime.
- Failure proves: Simplification weakens trust boundaries beyond freshness procedure.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused canonical and representative-output fixtures.
- Required by milestone: M2

### T14. Rule, literal, and scenario inventories are closed before package edits

- Covers: R83-R84, R115-R117; BND-COMPAT-001; INT-005
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Complete valid ledgers and scenarios plus unknown disposition and literal-classification fixtures.
- Steps: Validate closed values first, required fields, unique IDs, destinations, preservation proof, and scenario inventory.
- Expected result: Valid evidence passes; unknown values fail before consistency checks; every significant rule and literal has one treatment.
- Failure proves: Semantic or exact-string behavior can disappear without trace.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: Change-local standard-library assertion command.
- Required by milestone: M1

### T15. Canonical and generated packages retain complete resource parity

- Covers: R61-R65, R81, R85, R101, R117; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005
- Level: integration
- Command IDs: CMD2, CMD4-CMD8
- Fixture/setup: Canonical package and freshly generated Codex, Claude Code, and opencode package/archive/install trees.
- Steps: Validate mapping, build packages, select `project-map`, and compare required relative paths and raw bytes.
- Expected result: Every target contains the conditional reference and skeleton exactly once with required identity; missing or mixed resources fail.
- Failure proves: Canonical success does not guarantee a complete published package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T16. Procedural measurements prove real simplification

- Covers: R83-R84, R116-R117; BND-COMPAT-001; INT-004-INT-005
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled in documented order with LF normalization and unique-file counting.
- Steps: Measure `SKILL.md`, reference, skeleton, PMA0, PMA1, representative output, duplicate clusters, mapped-resource count, and total package.
- Expected result: PMA0 and PMA1 words and bytes both decrease unless an independently approved semantic-preservation exception identifies the exact reason; total package change remains separately visible.
- Failure proves: File splitting is misreported as context reduction.
- Evidence artifact: `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local measurement plus MP1.
- Required by milestone: M3

### T17. Final deterministic acceptance excludes target-agent execution

- Covers: R78-R84, R116-R117; BND-COMPAT-001
- Level: smoke
- Command IDs: CMD1-CMD11
- Fixture/setup: Completed M1-M3 package and evidence with every applicable boundary and interaction mapped.
- Steps: Run the command ledger, independent semantic review, review-artifact validation, and final boundary proof.
- Expected result: Contract, scenarios, packages, parity, preservation, and measurements pass without invoking or grading Codex, Claude Code, opencode, or another target runtime.
- Failure proves: Acceptance is incomplete or depends on a nondeterministic system outside the approved proof boundary.
- Evidence artifact: `evidence/m3-package-proof.md`; final review and verify evidence
- Automation location: Existing repository validators plus MP1.
- Required by milestone: M3 and M4

## Fixtures and data

- Change-local JSON-compatible YAML ledgers for semantic rules and literal consumers.
- Change-local scenario fixtures for operation, preflight, assembly, freshness, audit, structure, area transaction, compatibility, and resource failure.
- Existing controlled skill fixtures and generated adapter fixtures extended only where focused `project-map` coverage is absent.
- Representative root, root-with-areas, area, dirty-baseline, stale-map, and conflicting transaction outputs.

## Mocking/stubbing policy

Use temporary filesystem fixtures for map targets, project guidance, Git availability, resource packages, generated adapters, and interrupted writes. Do not mock away public skill/resource assembly or the root/area composed path. No network, hosted service, target-agent runtime, publication, or external state mutation is required.

## Migration or compatibility tests

T12 proves new result output, legacy mapping, ambiguous legacy rejection, parser migration, incidental-test updates, and historical-map readability. T15 proves the package migration is atomic across canonical and derived targets. Existing maps are never rewritten solely for this change.

## Observability verification

T5, T6, T12, T13, and T16 verify visible status, baseline, evidence class, path citations, command outcome, correction note, result fields, blockers, and size accounting. No telemetry is introduced.

## Security/privacy verification

T4, T5, T13, and T15 prove missing-resource failure, command authority, absence of secret or machine-local requirements, bounded filesystem use, and no network or target-runtime dependency.

## Performance checks

PMA0 and PMA1 LF-normalized words and UTF-8 bytes are the required portable context metrics. Total package and representative output sizes are reported separately. No wall-clock, tokenizer, or target-runtime benchmark is required.

## Manual QA checklist

### MP0. Baseline inventory audit

- Procedure: Compare the complete pre-edit `skills/project-map/` package and exact-string consumers against the rule and literal ledgers; sample every duplicate cluster and confirm each scenario has requirement-owned behavior.
- Evidence: `docs/changes/2026-08-14-project-map-skill-simplification/evidence/m1-preservation-inventories.md`

### MP1. Final semantic preservation review

- Procedure: Read the complete final package, both ledgers, representative outputs, and measurement report; confirm universal rules remain inline, conditional procedure has one owner, the skeleton is policy-free, operation and transaction outcomes match the spec, and no target-agent execution occurred.
- Evidence: `docs/changes/2026-08-14-project-map-skill-simplification/evidence/semantic-preservation-review.md`

## What not to test and why

- Do not execute or grade a target-agent runtime; the change is a deterministic content and package refactor.
- Do not add a permanent tokenizer, prose-quality, project-map artifact, or simplicity validator; change-local evidence and existing owners are sufficient.
- Do not require a full natural-language output corpus before concrete drift exists; the approved first slice uses bounded representative outputs.
- Do not test publication, release, deployment, or network behavior because those systems do not change.
- Do not rewrite historical project maps or test them as if they were newly emitted results.

## Uncovered gaps

None.

## Next artifacts

`test-spec-review`, then M1 implementation and code review if the proof map is approved.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer approval, implementation readiness, validation success, verification, branch readiness, or PR readiness.
