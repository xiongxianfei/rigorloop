# Spec-Review Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/spec-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-12-spec-review-skill-simplification.md`
- Architecture/ADRs: architecture not required; assessment at `docs/changes/2026-08-12-spec-review-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/spec-review-skill-simplification.md` | `spec` | `spec-review-r4`; `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/spec-review-r4.md` |
| execution plan | `docs/plans/2026-08-12-spec-review-skill-simplification.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-12-spec-review-skill-simplification/reviews/plan-review-r2.md` |
| architecture assessment | `docs/changes/2026-08-12-spec-review-skill-simplification/architecture-assessment.md` | not applicable | `architecture-not-required`; no architecture artifact entry or review required |

## Testing strategy

Use change-local contract scenarios and fail-closed ledger checks before instruction movement, focused skill-validator integration proof during the package refactor, and generated/archive/temporary-installed package proof after refactoring. Independent manual review proves semantic completeness and one-owner disposition where deterministic checks cannot judge meaning.

No target-agent runtime execution is permitted. The end-to-end boundary is the deterministic canonical-to-installed filesystem package chain, exercised through existing build and adapter validation in temporary directories. Migration proof classifies literal consumers without freezing incidental prose.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R2 | T4, T10-T12, T14 | contract, integration, manual | Complete package and self-sufficient isolated path. |
| R3-R5 | T1, T9, T14 | contract, manual | Formal ownership, outside-skill routing, and ambiguity. |
| R6-R10 | T1-T2, T9 | contract | Closed settlement and automation authority. |
| R11-R16 | T1, T4-T5, T8 | contract, integration | Four exact profiles and one automation branch. |
| R17-R19 | T3-T4, T12, T14 | contract, manual | Universal review and recording remain inline. |
| R20-R22 | T2-T3, T9, T12 | contract, manual | Isolated writes, blocked recording, and claim limits. |
| R23-R25 | T2, T4-T5, T12 | contract, manual | Governed reference ownership and exact settlement. |
| R26-R28 | T5, T10-T11, T13 | integration, contract | Checked boundary identity, order, and grandfathering. |
| R29-R31 | T4, T9-T10, T12 | contract, manual | One structural asset owner and conditional groups. |
| R32 | T5, T9, T11, T13 | contract, integration | Resource failure and mixed-package stop behavior. |
| R33-R34 | T6, T14 | unit, manual | Semantic ledger completeness and closed dispositions. |
| R35-R36 | T7, T12, T14 | migration, manual | Separate literal classification and treatment. |
| R37-R39 | T8, T12 | contract, manual | Deterministic measurement and semantic-first success. |
| R40-R41 | T6-T11, T13 | integration, contract | Existing deterministic proof owners and no runtime acceptance. |
| R42 | T1-T5, T9, T12, T14 | contract, manual | Full behavioral and lifecycle preservation. |
| R43 | T13 | contract | Architecture assessment precedes planning. |
| R44 | T11, T13 | integration | Atomic rollout, rollback, and mixed-version rejection. |
| R45 | T3-T4, T12 | contract, manual | `SFA-R6` obligations remain inline. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T3 | Isolated clean review records from the common path. |
| E2 | T2-T3 | Material isolated review remains durable without settlement. |
| E3 | T1-T2, T4 | Governed manual review loads and bounds settlement. |
| E4 | T1-T2, T4 | Automation shares SR2 assembly but not authority. |
| E5 | T1, T9 | Informal critique routes outside formal result profiles. |
| E6 | T5, T10 | Boundary resources remain independently additive. |
| E7 | T4-T5, T9 | Missing governed procedure preserves recording and blocks settlement. |
| E8 | T6-T8, T12, T14 | Size evidence cannot hide semantic loss. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R3, R4, R5, R6, R7, R8, R9, R10 | BND-INPUT-001 | T1, T9 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R6, R7, R8, R9, R10, R20, R21, R22, R23, R24, R25, R32, R43, R44 | BND-STATE-001 | T1, T2, T3, T4, T5, T9, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD9 | `evidence/m2-package-refactor.md`; `architecture-assessment.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-003 | covered | R6, R7, R8, R9, R10, R20, R21, R22, R23, R24, R25 | BND-AUTH-001 | T1, T2, T3, T4, T12 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R11, R12, R13, R14, R15, R16, R17, R18, R19, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R41, R42 | BND-COMPOSE-001 | T1, T3, T4, T5, T9, T10, T11, T12 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-005 | covered | R18, R19, R20, R21, R22, R23, R24, R25, R32, R44 | BND-TEMPORAL-001 | T2, T3, T4, T5, T9, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-006 | covered | R5, R6, R7, R8, R9, R10, R22, R28, R32, R33, R34, R35, R36, R37, R38, R39, R40, R43, R44 | BND-RECOVERY-001 | T1, T3, T5, T6, T7, T8, T9, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD8, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | R26, R27, R28, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45 | BND-COMPAT-001 | T5, T6, T7, T8, T10, T11, T12, T13, T14 | integration | hybrid | CMD1, CMD3, CMD6, CMD7, CMD8 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R32, R37, R40, R41, R44 | BND-ENV-001 | T5, T8, T9, T10, T11, T13 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16 | INT-001 | T1, T5, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R18, R19, R20, R21, R22, R23, R24, R25 | INT-002 | T2, T3, T4, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-011 | covered | R23, R24, R25, R32 | INT-003 | T4, T5, T9, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-012 | covered | R26, R27, R28, R32 | INT-004 | T5, T10, T13 | integration | automated | CMD3, CMD8 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-013 | covered | R33, R34, R35, R36, R37, R38, R39, R40, R42 | INT-005 | T6, T7, T8, T12, T14 | contract | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-014 | covered | R41, R44 | INT-006 | T10-T11, T13 | integration | automated | CMD2-CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 existing root without matching entry | T1-T3 | isolated recording without settlement |
| EC2 material recording-only root | T2-T3 | durable evidence without workflow activation |
| EC3 missing governed reference after recording | T4-T5, T9 | preserve record and block settlement |
| EC4 mismatched authorization | T1-T2, T9 | settlement and automation stop |
| EC5 late boundary activation | T5, T10 | ordered resource load before verdict |
| EC6 undecidable grandfathering | T5, T9 | approval blocked for owner resolution |
| EC7 applicable asset group lacks data | T9 | explicit blocked state, no placeholder |
| EC8 parser consumes exact heading | T7, T14 | preserve or migrate atomically |
| EC9 main file shrinks but isolated profile does not | T8, T12 | acceptance fails |
| EC10 total package grows | T8, T12 | separate justification required |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-12-spec-review-skill-simplification"); rules=json.loads((root/"spec-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"spec-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else [])); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"outside-skill-feedback","isolated-clean","isolated-material","isolated-recording-root","blocked-recording","governed-manual","governed-automated","stale-authorization","missing-governed-reference","isolated-boundary","governed-boundary","late-boundary-activation","grandfathered-nonsubstantive","substantive-ambiguous","asset-groups","retry-conflict","invalid-axis"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Block unknown values first, then incomplete ledgers, duplicate IDs, or incomplete scenarios. | Not applicable; all assertions must execute. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/spec-review/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block structure, mapping, containment, placeholder, or claim defects. | Not applicable; deterministic validation. | `evidence/m2-package-refactor.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block any focused or regression failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource test failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Temporary filesystem only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-package drift or missing resources. | Not applicable; deterministic check. | `evidence/m2-package-refactor.md` | Read-only check against canonical sources. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD7 | `spec_review_adapter_tmp="$(mktemp -d)"; trap 'rm -rf "$spec_review_adapter_tmp"' EXIT; python scripts/build-adapters.py --version v0.1.5 --output-dir "$spec_review_adapter_tmp"; python scripts/validate-adapters.py --version v0.1.5 --adapter-root "$spec_review_adapter_tmp" --clean-install-smoke --skill spec-review` | existing/configured | implement | M3 | M3 code-review | Stop on failed generation or any archive/installed target missing required byte-identical resources. | Not applicable; direct package selection must produce all supported targets. | `evidence/m3-package-proof.md` | One fresh temporary directory is removed by trap; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/spec-review-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block missing or invalid proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only repository validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-12-spec-review-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every state-changing handoff | Block invalid artifact or planned-work state. | Not applicable; deterministic metadata validation. | owning change validation ledger | Read-only validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-12-spec-review-skill-simplification` | existing/configured | review stages | lifecycle | every formal review handoff | Block malformed or missing review evidence. | Not applicable; deterministic artifact validation. | review log and records | Read-only validation. |

CMD1 copies the approved plan's `M1 change-local evidence proof` exactly. CMD7 is semantically identical to the approved multiline command and preserves the same version, temporary-root, cleanup, build, validation, and skill-selection arguments.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T6-T9, T14 | MP0 | CMD1, CMD9 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged. |
| M2 | T1-T5, T9-T10 | none | CMD2-CMD5, CMD9 | `evidence/m2-package-refactor.md` | M2 code-review | Focused failing assertions precede package text changes. |
| M3 | T8-T14 | MP1 | CMD1-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves profile, semantic, boundary, and package-chain acceptance. |

## Test cases

### T1. Formal routing and authority classifications fail closed

- Covers: R3-R16, R42; E1, E3-E5; EC1, EC4; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: static scenarios for outside-skill feedback, isolated/governed formal review, manual/automated modes, stale and mismatched evidence, and invalid axis combinations.
- Steps: validate exactly one formal route, settlement mode, automation mode, and resource profile or a fail-closed result.
- Expected result: valid cases select one profile; invalid or ambiguous evidence stops before governed loading or mutation.
- Failure proves: classification can broaden review status, resource loading, or authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: scenario fixtures and focused assertions in `scripts/test-skill-validator.py`
- Required by milestone: M2

### T2. Isolated and governed writes remain distinct

- Covers: R7-R10, R20-R25, R42; E2-E4; EC1-EC4; BND-STATE-001, BND-AUTH-001; INT-002
- Level: integration
- Command IDs: CMD3
- Fixture/setup: equivalent clean and material review inputs under isolated, governed-manual, and governed-automated authority.
- Steps: assert permitted recording, forbidden isolated state writes, exact matching settlement, automation evidence, and return-to-workflow behavior.
- Expected result: recording never grants settlement; governed writes affect only the matching spec entry after successful recording.
- Failure proves: shared review procedure leaks mutation authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T3. Universal recording is complete without the governed reference

- Covers: R2-R3, R17-R22, R42, R45; E1-E2; EC1-EC2; BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001
- Level: integration
- Command IDs: CMD3
- Fixture/setup: isolated clean, material, generated-root, collision, retry, and blocked-location scenarios with the governed reference forbidden.
- Steps: assert selection order, clean/detailed choice, log synchronization, conditional resolution, retry, blocked fields, and claim limits.
- Expected result: every isolated review records or reports blocked recording without governed procedure or lifecycle mutation.
- Failure proves: the shortened common path is not executable or weakens recording.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py` and static scenarios
- Required by milestone: M2

### T4. Governed reference owns only conditional procedure

- Covers: R14-R16, R23-R25, R29-R32, R42; E3-E4, E7; EC3-EC4; BND-AUTH-001, BND-COMPOSE-001; INT-002-INT-003
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: canonical governed reference plus positive and forbidden ownership assertions.
- Steps: verify exact load trigger, complete matching settlement and automation branches, recording precondition, and absence of universal review, recording, status, stage-order, or edit authority.
- Expected result: one package-owned reference specializes governed procedure without becoming an authority owner.
- Failure proves: ownership overlaps or conditional procedure is incomplete.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T5. Boundary and resource loading remain exact and fail safe

- Covers: R11-R16, R26-R28, R32, R42; E6-E7; EC3, EC5-EC6; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-003-INT-004
- Level: integration
- Command IDs: CMD2, CMD3, CMD8
- Fixture/setup: SR1, SR1B, SR2, SR2B plus late activation, grandfathering, missing/unreadable, and mixed-version cases.
- Steps: assert exact required and forbidden loads, compact-core-first order, feature trigger, projection identity, and dependent-stop behavior.
- Expected result: untriggered resources do not load; triggered failures stop without reconstruction; boundary behavior remains unchanged.
- Failure proves: progressive disclosure or boundary compatibility is unsafe.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: focused skill and boundary validation
- Required by milestone: M2 and M3

### T6. Semantic-rule ledger is complete and fail closed

- Covers: R33-R34, R40, R42; BND-RECOVERY-001, BND-COMPAT-001; INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: valid rule ledger and invalid unknown-disposition fixture.
- Steps: validate required fields, unique IDs, source coverage, profiles, vocabulary, destination, and preservation proof; evaluate unknown value first.
- Expected result: the complete valid ledger passes and unknown or missing disposition fails before consistency.
- Failure proves: a governing rule can disappear or validation fails open.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: CMD1
- Required by milestone: M1

### T7. Literal compatibility remains separate and atomic

- Covers: R35-R36, R40, R42; EC8; BND-RECOVERY-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: valid literal inventory, unknown-classification fixture, and bounded exact consumer search.
- Steps: verify normative preservation, atomic parser/package migration, incidental-test updates, and obsolete evidence.
- Expected result: real contracts remain intact while tests alone do not freeze prose.
- Failure proves: incidental coupling becomes policy or a real consumer breaks.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md`
- Automation location: CMD1 plus focused consumer assertions
- Required by milestone: M1 and M3

### T8. Profile measurements are deterministic and honest

- Covers: R11-R16, R37-R40; E8; EC9-EC10; BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: canonical baseline and final files with documented resource assembly order.
- Steps: normalize LF, count each unique resource once, compute words/bytes for all resources/profiles/package, and compare duplicate owners.
- Expected result: SR1 decreases; governed and total deltas are explicit; no fixed percentage overrides preservation.
- Failure proves: relocation or duplication is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: repository-local standard-library measurement recorded in evidence
- Required by milestone: M3

### T9. Static scenarios preserve failure and output behavior

- Covers: R3-R10, R18-R22, R29-R32, R40, R42; E5, E7; EC3-EC7; BND-INPUT-001, BND-RECOVERY-001; INT-001, INT-003
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: exactly seventeen required scenario records with non-empty required and forbidden outcomes.
- Steps: validate scenario identity, output groups, blockers, claims, and absence of target-agent runtime fields.
- Expected result: all material normal and failure outcomes are represented deterministically.
- Failure proves: negative behavior or asset applicability is unproved.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md`
- Automation location: CMD1 and focused skill assertions
- Required by milestone: M1 and M2

### T10. Canonical and generated validation uses existing owners

- Covers: R1, R26-R32, R40-R42; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004, INT-006
- Level: integration
- Command IDs: CMD2-CMD5, CMD8
- Fixture/setup: changed canonical package and existing generated-skill and boundary projection tests.
- Steps: validate structure, all mappings, containment, projected identity, asset shape, generated inventory, and parity.
- Expected result: complete package passes; missing, escaped, stale, malformed, or drifted resources fail.
- Failure proves: permanent validators do not cover the package change.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: existing skill/build/boundary validation suites
- Required by milestone: M2 and M3

### T11. Archives and temporary installations preserve resources

- Covers: R1, R26, R32, R40-R41, R44; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: end-to-end
- Command IDs: CMD6, CMD7
- Fixture/setup: locally generated Codex, Claude Code, and opencode release candidates in a fresh temporary directory.
- Steps: inspect archives and clean installations for all mapped references and assets at canonical paths and bytes; exercise incomplete/mixed failure fixtures.
- Expected result: every target is complete and byte-consistent; incomplete targets fail.
- Failure proves: canonical acceptance does not survive distribution.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution and validation scripts
- Required by milestone: M3

### T12. Independent semantic review confirms one-owner preservation

- Covers: R1-R3, R17-R25, R29-R31, R36-R45; E8; EC8-EC10; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-002-INT-003, INT-005
- Level: manual
- Command IDs: -
- Fixture/setup: complete final package, governing artifacts, ledgers, scenarios, baseline skill, literal consumers, measurements, and package proof.
- Steps: execute MP1.
- Expected result: every rule has one correct owner; universal recording and claims remain inline; governed and boundary resources specialize only their triggers; no unapproved semantic change exists.
- Failure proves: deterministic structure passed while meaning regressed.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: manual
- Required by milestone: M3

### T13. Architecture ordering, rollout, and rollback stay bounded

- Covers: R26-R28, R32, R40-R44; EC5-EC6; BND-STATE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-004, INT-006
- Level: integration
- Command IDs: CMD6-CMD9
- Fixture/setup: recorded assessment, current package, simulated incomplete package, and prior complete package identities.
- Steps: verify assessment predates plan, reassessment triggers, mixed-package rejection, selected complete package proof, and prior-package restoration.
- Expected result: no architecture is invented and rollout or rollback never leaves a mixed package.
- Failure proves: planning bypassed architecture applicability or recovery is unsafe.
- Evidence artifact: `architecture-assessment.md`; `evidence/m3-package-proof.md`
- Automation location: metadata, boundary, and adapter package fixtures
- Required by milestone: M3

### T14. Baseline inventories cover every current rule and consumer

- Covers: R17-R19, R33-R36, R42, R45; EC8; BND-COMPAT-001; INT-005
- Level: manual
- Command IDs: CMD1
- Fixture/setup: full current spec-review package and bounded scripts, tests, specs, fixtures, and adapter/package consumers.
- Steps: execute MP0 before prose movement and reconcile every source cluster and exact match to one ledger row.
- Expected result: no significant rule, duplicate, or consumer is omitted and every proposed treatment is justified.
- Failure proves: later preservation relies on an incomplete baseline.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: manual audit supported by bounded `rg` searches and CMD1
- Required by milestone: M1

## Fixtures and data

- `spec-review-rule-disposition.yaml`: JSON-compatible YAML with stable semantic rule records.
- `spec-review-literal-compatibility.yaml`: JSON-compatible YAML with exact consumer records.
- `fixtures/scenario-contracts.yaml`: exactly seventeen static scenario records with required and forbidden outcomes.
- `fixtures/invalid-rule-disposition.yaml`: one unknown semantic disposition.
- `fixtures/invalid-literal-classification.yaml`: one unknown literal classification.
- Existing skill, build, boundary, and adapter fixtures remain permanent package-proof owners.
- Temporary generated and installed trees use `mktemp -d`, automatic cleanup, and no publication.

## Mocking/stubbing policy

Do not mock a target-agent runtime because no agent runtime is part of acceptance. Static records model contract inputs and expected outcomes; filesystem/package helpers may isolate temporary roots but must not bypass canonical parsing, boundary projection, or byte comparison.

## Migration or compatibility tests

T7 proves literal-consumer migration, T10 proves unchanged boundary projection, T11 proves distributed compatibility, T13 proves complete-package rollback, and T12 proves semantic compatibility. Historical review and change-local evidence remain readable and are not rewritten.

## Observability verification

Evidence records rule, literal, duplicate, and scenario counts; exact profile file lists and words/bytes; command IDs and outcomes; package targets and hashes; semantic conclusions; and blockers. No runtime logs, metrics, traces, or external audit service are introduced.

## Security/privacy verification

Commands read repository files and use temporary local package roots only. They must not access credentials, network services, hosted agents, publication endpoints, private data, or paths outside declared package roots.

## Performance checks

Measure loaded words and bytes for `SR1`, `SR1B`, `SR2`, `SR2B`, manual and automated governed evaluation, and total package. Do not add timing, target-runtime, model-token, or permanent percentage gates.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: semantic equivalence and normative-versus-incidental ownership cannot be established by exact-string checks alone.
- Required environment: tracked repository at the M1 baseline with the complete current spec-review package and bounded consumers.
- Steps:
  1. Read the complete current `skills/spec-review/SKILL.md`, both mapped boundary references, and both assets.
  2. Group every significant rule and duplicate cluster by stable rule ID.
  3. Search scripts, tests, specs, fixtures, generated/package tests, and adapter validation for exact headings, fields, values, and phrases.
  4. Reconcile every rule and literal match to one ledger row and validate closed values with CMD1.
- Evidence artifact: `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: every material rule, duplicate, and consumer has one justified treatment and no canonical skill prose has moved.
- Failure condition: any owner, rule, consumer, classification, or source cluster is missing, duplicated, ambiguous, or unsupported.
- Owning stage: implement M1; required before M1 code-review.

### MP1. Semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: validators can prove structure and bytes but not completeness, authority, recording safety, or semantic equivalence.
- Required environment: final canonical package, ledgers, scenarios, measurements, approved artifacts, and package proof.
- Steps:
  1. Compare every semantic ledger row with its final destination and preservation proof.
  2. Confirm inline completeness for formal classification, judgment, recording, stops, claims, result, and handoff.
  3. Confirm the governed reference owns only exact same-change settlement and automation procedure.
  4. Confirm boundary activation, projections, grandfathering, assets, lifecycle ownership, and recording behavior match baseline.
  5. Confirm literal consumers received their classified treatment and measurements did not hide duplication or loss.
- Evidence artifact: `docs/changes/2026-08-12-spec-review-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: every rule has one correct owner, every claim remains bounded, every profile is usable, and no unapproved semantic change exists.
- Failure condition: any rule disappears, duplicates, moves behind an invalid trigger, changes authority, or lacks direct preservation evidence.
- Owning stage: implement M3; required before M3 code-review and final review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime; the contract is published guidance plus deterministic resources.
- Do not add prompt journeys, transcript snapshots, runtime-version evidence, tokenizer dependencies, or permanent size/prose validators.
- Do not test unrelated skills, lifecycle schemas, workflow stage order, release publication, or PR opening beyond preserved ownership assertions.
- Do not publish adapters or access network services; local temporary package inspection is sufficient.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation M1 only after review approval and later workflow routing.

## Follow-on artifacts

None yet

## Readiness

Active proof map ready for formal `test-spec-review`. This artifact does not claim implemented tests, validation success, implementation eligibility, verification, branch readiness, or PR readiness.
