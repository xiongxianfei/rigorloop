# Implement Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-11-implement-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/implement-skill-simplification.md`
- Plan: `docs/plans/2026-08-11-implement-skill-simplification.md`
- Architecture/ADRs: architecture change not required; assessment at `docs/changes/2026-08-11-implement-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/implement-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-11-implement-skill-simplification/reviews/spec-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-11-implement-skill-simplification/architecture-assessment.md` | not applicable | recorded `architecture-not-required` assessment |
| Execution plan | `docs/plans/2026-08-11-implement-skill-simplification.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-11-implement-skill-simplification/reviews/plan-review-r2.md` |

Implementation and the first milestone code review must recheck these paths and their current change-record settlement before relying on this proof map.

## Testing strategy

Contract and unit-level static tests in `scripts/test-skill-validator.py` prove profile classification, exact resource triggers, ownership boundaries, result groups, closed vocabulary, universal semantics, and forbidden runtime machinery. Change-local JSON-compatible YAML fixtures prove semantic and literal inventory contracts plus representative invocation outcomes without executing a target agent.

Integration and end-to-end tests use existing skill-build and adapter-distribution owners to prove canonical-to-generated, archive, and temporary installed-tree resource identity. The selected clean-install check is the smoke layer. Two bounded manual procedures prove complete baseline inventory and final semantic preservation because structural checks cannot establish either conclusion. Migration proof classifies exact-string consumers and requires parser/package contracts to migrate atomically; incidental tests may change with prose. No network, model, prompt, transcript, publication, or destructive operation is part of acceptance.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T2, T10, T11, T12 | contract, integration, manual | Complete package remains `implement` owned. |
| R2 | T2, T12 | contract, manual | Isolated behavior is self-sufficient. |
| R3 | T2, T12 | contract, manual | Universal inline policy is enumerated and semantically reviewed. |
| R4 | T1 | contract | Exactly three valid profiles and one invalid combination. |
| R5 | T1 | contract | Planned predicate uses durable plan and milestone evidence. |
| R6 | T1 | contract | Armed predicate is current, matching, and planned-subordinate. |
| R7 | T1, T9 | contract | Missing, stale, mismatched, contradictory, and ambiguous evidence stops. |
| R8 | T2, T3 | contract | Planned reference mapping and exact profile loads. |
| R9 | T3, T12 | contract, manual | Planned procedure ownership and universal-policy exclusion. |
| R10 | T2, T4 | contract | Automation reference mapping and exact load. |
| R11 | T4, T12 | contract, manual | Automation procedure ownership and no independent milestone authority. |
| R12 | T3, T4, T12 | contract, manual | Cross-reference duplication and owner exchange are rejected. |
| R13 | T5, T12 | contract, manual | One structural asset owns no policy. |
| R14 | T5 | contract | Exact core, planned, and armed fields and applicability. |
| R15 | T5 | contract | Inapplicable groups and placeholders are absent. |
| R16 | T6, T14 | contract, manual | Semantic ledger fields and complete source inventory. |
| R17 | T6 | unit | Closed dispositions fail unknown/missing values first. |
| R18 | T6, T12, T14 | contract, manual | Every significant rule has exactly one justified destination. |
| R19 | T7, T14 | contract, manual | Literal ledger fields and complete consumer inventory. |
| R20 | T7 | unit | Closed classifications fail unknown/missing values first. |
| R21 | T7, T12, T14 | migration, manual | Exact contracts migrate atomically; incidental wording does not own policy. |
| R22 | T6, T7, T10 | contract | Ledgers remain change-local and permanent validation remains bounded. |
| R23 | T8 | unit | LF-normalized unique-resource assembly is deterministic. |
| R24 | T8 | contract | Required profile and package metrics are reported separately. |
| R25 | T8 | contract | Tokens are optional, pinned, and add no dependency. |
| R26 | T8, T12 | contract, manual | Profile improvement and semantic preservation are joint acceptance gates. |
| R27 | T8 | contract | Percentage remains advisory; no material improvement fails. |
| R28 | T1, T5, T6, T7, T9, T11, T12, T14 | contract, integration, manual | All required deterministic proof classes and scenarios are represented. |
| R29 | T9, T10, T11 | contract, integration | Runtime, prompt, transcript, and retry evidence is forbidden. |
| R30 | T10, T11 | integration | Existing owners prove canonical through installed integrity. |
| R31 | T2-T5, T9, T12 | contract, manual | Existing authority, execution, validation, correction, milestone, claim, and handoff semantics remain. |
| R32 | T13 | contract | Recorded assessment precedes plan and ambiguous architecture stops. |
| R33 | T11, T13 | integration, contract | Complete rollout and prior-package rollback are atomic. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 isolated implementation loads no conditional procedure | T1, T2 | `IP0-isolated` loads universal skill and result asset only, plus independently triggered boundary guidance. |
| E2 planned implementation excludes automation procedure | T1-T3 | `IP1-planned` loads only planned procedure. |
| E3 planned armed implementation loads both references | T1-T4 | `IP2-planned-armed` requires matching durable authority. |
| E4 armed but unplanned automation stops | T1, T9 | Invalid combination stops before load or mutation. |
| E5 result groups follow profile applicability | T5 | Exact group matrix and omission behavior. |
| E6 incidental test text does not freeze prose | T7, T12 | Literal classification and semantic review stay separate. |
| E7 runtime execution is rejected as acceptance proof | T9-T11 | No accepted command starts or grades an agent. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R4, R5, R6, R14, R17, R20, R28 | BND-INPUT-001 | T1, T5-T7, T9 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R5, R6, R7, R9, R11, R31, R32, R33 | BND-STATE-001 | T1, T3, T4, T9, T13 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-003 | covered | R1, R3, R5, R6, R9, R11, R13, R21, R31 | BND-AUTH-001 | T1-T7, T12, T14 | contract | hybrid | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-004 | covered | R1, R2, R8, R10, R12, R13, R14, R30 | BND-COMPOSE-001 | T2, T3, T4, T5, T10, T11 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R6, R7, R9, R11, R28, R31, R33 | BND-TEMPORAL-001 | T1, T3, T4, T9, T13 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-006 | covered | R7, R17, R18, R20, R21, R27, R29, R32, R33 | BND-RECOVERY-001 | T1, T6-T9, T13 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | R21, R30, R31, R33 | BND-COMPAT-001 | T7, T11-T13 | integration | hybrid | CMD1, CMD3, CMD6, CMD7 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP1 | - |
| PRF-008 | covered | R23, R24, R25, R28, R29, R30 | BND-ENV-001 | T8, T9, T10, T11 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R4, R5, R6, R7 | INT-001 | T1, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R2, R3, R8, R10 | INT-002 | T2, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-011 | covered | R9, R11, R12 | INT-003 | T3, T4, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-012 | covered | R13, R14, R15 | INT-004 | T5, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-013 | covered | R16, R17, R18, R19, R20, R21 | INT-005 | T6, T7, T12, T14 | contract | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-014 | covered | R23, R24, R25, R26, R27 | INT-006 | T8 | contract | automated | CMD1 | `evidence/simplification-measurements.md` | M3 | - | - |
| PRF-015 | covered | R28, R29, R30 | INT-007 | T9, T10, T11 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-016 | covered | R30, R31, R33 | INT-008 | T10, T11, T13 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 universal rule related to conditional procedure | T2, T6, T12 | Rule remains inline and has one ledger destination. |
| EC2 planned without automation | T1-T3, T5 | Planned reference and planned result group appear; automation surfaces do not. |
| EC3 mismatched automation identity | T1, T9 | Stop before conditional load or mutation. |
| EC4 stale automation after transition | T1, T9 | Current authorization is required. |
| EC5 result field mixes structure and policy | T5, T12 | Label may move; policy stays in instruction owner. |
| EC6 literal has parser and test consumers | T7 | Classify as parser/package and migrate all consumers atomically. |
| EC7 apparently obsolete rule lacks approved change | T6, T12 | Retain or route upstream; never silently remove. |
| EC8 `SKILL.md` shrinks while planned profile grows | T8 | Acceptance fails despite main-file reduction. |
| EC9 references duplicate milestone transition | T3, T4, T12 | Planned reference owns the rule; automation only cites it. |
| EC10 architecture is sufficient but example is stale | T13 | Assessment remains not-required; no architecture ownership is invented. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-implement-skill-simplification"); rules=json.loads((root/"implement-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"implement-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-planned-reference","retained-automation-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; expected={"isolated","planned","planned-armed","invalid-unplanned-armed","stale-or-mismatched-authority","result-group-applicability","validation-failure","specification-gap","accepted-correction-return","code-review-handoff","premature-next-milestone-transition"}; assert rules and literals; assert all(rf <= row.keys() for row in rules); assert all(lf <= row.keys() for row in literals); assert not [row.get("disposition") for row in rules if row.get("disposition") not in rd]; assert not [row.get("classification") for row in literals if row.get("classification") not in lc]; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); assert bad_rule.get("disposition") not in rd; assert bad_literal.get("classification") not in lc; print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected")'` | planned-for-implementation | implement | M1 | M1 code-review | Block milestone; reject unknown values before consistency and require every fixture identity. | Not applicable; assertion command must execute all named checks. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or runtime agent. |
| CMD2 | `python scripts/validate-skills.py skills/implement/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block milestone on canonical structure, resource, placeholder, or claim failure. | Not applicable; validator must report one skill validated. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md` | Repository-local reads only. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block milestone on any regression or missing focused assertion. | Zero discovered tests is failure. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md` | Repository-local test suite; no target runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block milestone on generation, inventory, or resource-parity regression. | Zero discovered tests is failure. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md` | Temporary repository-local output only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block milestone when canonical skills cannot produce a valid temporary generated tree. | Not applicable; build check must complete and validate output. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md` | Temporary output only; tracked generated bodies are not edited. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block milestone on archive, resource, or clean-install regression. | Zero discovered tests is failure. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m3-package-proof.md` | Temporary local package roots; no publication or network. |
| CMD7 | `ADAPTER_OUTPUT_DIR="$(mktemp -d)"; python scripts/build-adapters.py --version 0.0.0-implement-simplification --output-dir "$ADAPTER_OUTPUT_DIR"; python scripts/validate-adapters.py --version 0.0.0-implement-simplification --adapter-root "$ADAPTER_OUTPUT_DIR" --clean-install-smoke --skill implement` | existing/configured | implement | M3 | M3 code-review | Block milestone if any supported archive or temporary installed tree lacks identical mapped resources. | Not applicable; every supported target and selected skill must be validated. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/m3-package-proof.md` | Writes only to a fresh temporary directory; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/implement-skill-simplification.md` | existing/configured | test-spec | not applicable | test-spec-review | Block review when any approved boundary or interaction lacks structurally valid proof mapping. | Not applicable; validator discovers and inspects the matching feature and proof records. | `docs/changes/2026-08-11-implement-skill-simplification/evidence/test-spec-authoring.md` | Repository-local reads only. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-11-implement-skill-simplification/change.yaml` | existing/configured | workflow | all milestones | every lifecycle handoff | Block handoff on illegal, unknown, missing, or contradictory state. | Not applicable; metadata validation must complete. | matching stage-owned evidence | Repository-local reads only. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-implement-skill-simplification` | existing/configured | workflow | not applicable | each formal review | Block review handoff on malformed or missing review evidence. | Not applicable; artifact validator must inspect all selected records. | matching formal review record | Repository-local reads only. |

CMD1 is identical to the approved plan's `M1 change-local ledger and fixture proof` block; implementation must copy it verbatim into execution evidence rather than replace it with a model or new validator.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T6, T7, T9, T14 | MP0 | CMD1, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | M1 code-review | Inventories, negative fixtures, scenarios, baseline, and a complete-source audit exist before prose movement. |
| M2 | T1, T2, T3, T4, T5, T6, T7, T9, T10 | none | CMD1, CMD2, CMD3, CMD4, CMD5, CMD9 | `evidence/m2-package-refactor.md` | M2 code-review | Focused assertions precede package edits and prove all three resource paths. |
| M3 | T8, T9, T10, T11, T12, T13 | MP1 | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8, CMD9, CMD10 | `evidence/m3-package-proof.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 code-review | Profile metrics, semantics, archive, installed-tree, and rollback proof close together. |

## Test cases

### T1. Invocation profiles and authority fail closed

- Covers: R4-R7, R28, R31, E1-E4, EC2-EC4, INT-001
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: static scenario records for isolated, planned, planned-armed, unplanned-armed, missing plan, ambiguous milestone, stale authorization, and mismatched change or milestone.
- Steps: Assert exactly three valid profile results; assert planned and armed predicates require every specified durable field; mutate each authority property to missing, stale, mismatched, contradictory, or ambiguous; assert invalid cases stop before reference load and state mutation.
- Expected result: only identity-bound current profiles proceed and conversational wording never establishes authority.
- Failure proves: conditional procedure or implementation mutation can occur without approved authority.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; change-local scenario fixtures
- Required by milestone: M2

### T2. Universal contract and exact resource loading remain inline

- Covers: R1-R3, R8, R10, R31, E1-E3, EC1, INT-002
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: final canonical package and profile-specific expected/forbidden resource sets.
- Steps: Assert `SKILL.md` contains every R3 contract and exact `READ`/`COPY` mappings; assert IP0 loads neither conditional reference, IP1 loads only planned, and IP2 loads both; allow boundary guidance only under its independent trigger.
- Expected result: direct implementation remains self-sufficient and each valid profile has one exact resource set.
- Failure proves: universal behavior is hidden or conditional content leaks into another profile.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`
- Required by milestone: M2

### T3. Planned reference owns only milestone procedure

- Covers: R8, R9, R12, R31, E2, EC9, INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: planned reference and explicit allowed/forbidden ownership assertions.
- Steps: Assert all R9 procedure is present; assert universal policy and automation classification/correction are absent; assert milestone state and handoff procedure are not duplicated in the automation reference.
- Expected result: planned procedure has one owner and no universal or automation authority.
- Failure proves: the planned reference is incomplete or becomes a competing policy owner.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T4. Automation reference owns only armed review and correction

- Covers: R10-R12, R31, E3, EC9, INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: automation reference and explicit allowed/forbidden ownership assertions.
- Steps: Assert every R11 procedure is present; assert it requires the same planned context; assert universal and planned milestone procedure is absent or cited without duplication.
- Expected result: automation procedure cannot independently establish milestone authority or exchange ownership with the planned reference.
- Failure proves: armed behavior leaks, duplicates policy, or broadens authority.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T5. Result skeleton applies exact structural groups without policy

- Covers: R13-R15, R28, E5, EC2, EC5, INT-004
- Level: contract
- Command IDs: CMD2, CMD3
- Fixture/setup: result asset plus expected field groups for IP0, IP1, and IP2.
- Steps: Assert one core group and exact fields for every profile; assert planned group only for IP1/IP2 and armed group only for IP2; assert inapplicable groups, empty placeholders, `not applicable` filler, status definitions, correction rules, and handoff policy are absent.
- Expected result: the asset owns layout only and emitted structure matches profile applicability.
- Failure proves: output duplication, irrelevant fields, placeholders, or policy leakage remains.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; `scripts/validate-skills.py`
- Required by milestone: M2

### T6. Semantic-rule ledger is complete and fail-closed

- Covers: R16-R18, R22, R28, EC1, EC7, INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: semantic-rule ledger and invalid unknown-disposition fixture.
- Steps: Validate every required field, stable unique ID, applicable profile set, one closed disposition, destination, requirement mapping, and preservation proof; reject missing/unknown disposition before destination checks; require approved contract evidence for obsolete removal.
- Expected result: no significant rule or duplication cluster can disappear silently.
- Failure proves: semantic preservation is incomplete or fail-open.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md`
- Automation location: approved plan CMD1
- Required by milestone: M1

### T7. Literal compatibility is classified separately and migrated safely

- Covers: R19-R22, R28, E6, EC6, INT-005
- Level: unit
- Command IDs: CMD1, CMD3
- Fixture/setup: literal ledger, repository consumers, and invalid unknown-classification fixture.
- Steps: Validate required fields and unique IDs; reject unknown/missing classification first; assert normative literals remain exact, parser/package consumers migrate atomically, incidental tests may change with prose, and obsolete entries cite evidence.
- Expected result: real compatibility is preserved without turning incidental tests into prose-policy owners.
- Failure proves: exact-string compatibility is lost or accidental wording is frozen.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md`
- Automation location: approved plan CMD1; focused consumer assertions in `scripts/test-skill-validator.py`
- Required by milestone: M1

### T8. Profile and package measurements are deterministic and honest

- Covers: R23-R27, EC8, INT-006
- Level: unit
- Command IDs: CMD1
- Fixture/setup: before and after canonical package snapshots and documented load order for IP0, IP1, and IP2.
- Steps: Normalize LF; count each unique resource once; record exact resource identities, Unicode whitespace words, UTF-8 bytes, main file, each resource, package total, duplicate clusters, inline templates, and mapped resources; assert material IP0/IP1 improvement, justified IP2 non-regression, and advisory-only percentage handling.
- Expected result: context reduction and maintenance footprint are visible separately and cannot override semantics.
- Failure proves: metrics are unstable, incomplete, misleading, or show the objective was not met.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/simplification-measurements.md`
- Automation location: change-local standard-library assertions and evidence review
- Required by milestone: M3

### T9. Scenario contract preserves stops, correction, and handoff without a runtime

- Covers: R7, R28, R29, R31, E4, E7, EC3, EC4, INT-001, INT-007
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: eleven static scenario records with required and forbidden outcomes.
- Steps: Assert required/forbidden results for the three profiles, invalid/stale authority, validation failure, spec gap, correction return, review handoff, and premature transition; scan acceptance surfaces for target-agent, prompt, transcript, model-selector, or retry machinery.
- Expected result: scenarios establish contract routing deterministically without claiming model interpretation.
- Failure proves: a required stop or handoff is absent or acceptance has expanded into runtime certification.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md`
- Automation location: approved plan CMD1; `scripts/test-skill-validator.py`
- Required by milestone: M1

### T10. Canonical and generated package validation uses existing owners

- Covers: R1, R22, R29-R31, INT-007, INT-008
- Level: integration
- Command IDs: CMD2, CMD3, CMD4, CMD5
- Fixture/setup: canonical `skills/implement/` and temporary generated skill roots.
- Steps: Validate frontmatter, headings, closed vocabulary, Resource map, containment, placeholders, claims, inventory, and raw resource parity; assert no new standalone simplification validator or runtime dependency exists.
- Expected result: the complete mapped package passes existing canonical and generated owners.
- Failure proves: the refactor violates the published skill contract or introduces forbidden machinery.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m2-package-refactor.md`
- Automation location: existing skill validation and build scripts
- Required by milestone: M2

### T11. Archives and temporary installed packages preserve every resource

- Covers: R1, R28-R30, R33, E7, INT-008
- Level: end-to-end
- Command IDs: CMD6, CMD7
- Fixture/setup: fresh temporary adapter output root for all supported targets with `implement` selected.
- Steps: Build archives; validate inventory and mapped paths; install into temporary roots; compare both references, boundary reference, asset, and `SKILL.md` bytes to canonical; mutate or omit one resource in negative fixture coverage and require failure.
- Expected result: generated, archived, and installed targets contain one complete identical package and no agent is started.
- Failure proves: a target can ship a stale, partial, escaped, or transformed package.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m3-package-proof.md`
- Automation location: existing adapter distribution, build, and validation scripts
- Required by milestone: M3

### T12. Independent semantic review confirms complete behavior and ownership

- Covers: R1-R3, R9, R11-R13, R18, R21, R26, R31, E6, EC1, EC5, EC7, EC9
- Level: manual
- Command IDs: none
- Fixture/setup: final canonical package, approved spec, semantic ledger, literal ledger, baseline package, and deterministic validation results.
- Steps: Execute MP1 exactly.
- Expected result: every significant rule has one correct owner, every literal treatment is justified, universal direct behavior is complete, references and asset do not own forbidden policy, and no semantic or lifecycle behavior was weakened.
- Failure proves: structural tests passed despite semantic loss, duplication, or authority drift.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/semantic-preservation-review.md`
- Automation location: manual MP1
- Required by milestone: M3

### T13. Architecture ordering, rollout, and rollback remain bounded

- Covers: R32, R33, EC10, INT-008
- Level: contract
- Command IDs: CMD9
- Fixture/setup: change record, approved spec/review, architecture assessment, plan, final package identities, and prior canonical revision.
- Steps: Assert assessment follows approved spec review and precedes plan; assert ambiguity would stop; assert rollout changes canonical package/resources and consumers as one reviewed slice; assert rollback restores the prior complete package and regenerates derived targets without rewriting history.
- Expected result: no architecture ownership is invented and no mixed package version is accepted.
- Failure proves: stage order or atomic package recovery is unsafe.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m3-package-proof.md`
- Automation location: change metadata validation and package identity evidence
- Required by milestone: M3

### T14. Current rules and literal consumers are completely inventoried before movement

- Covers: R16, R18, R19, R21, R28, E6, EC6, EC7, INT-005
- Level: manual
- Command IDs: CMD1
- Fixture/setup: pre-change canonical `skills/implement/SKILL.md`, its mapped boundary reference, the two M1 ledgers, exact-string search results across `scripts/`, `tests/`, `specs/`, `skills/`, and adapter/package test surfaces, and CMD1 output.
- Steps: Execute MP0 exactly after CMD1 passes and before any canonical skill prose is changed.
- Expected result: every behaviorally significant rule, duplication cluster, normalized heading, closed vocabulary value, result label, claim term, status, milestone term, Resource-map verb, and exact consumer has one ledger row or an explicit non-behavioral/non-contract rationale.
- Failure proves: deterministic ledger shape passed despite an incomplete semantic or compatibility inventory.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md`
- Automation location: manual MP0 with repository-local `rg` evidence
- Required by milestone: M1

## Fixtures and data

All change-local `.yaml` fixtures use JSON serialization for Python standard-library parsing.

- `implement-rule-disposition.yaml`: complete semantic rule/cluster inventory.
- `implement-literal-compatibility.yaml`: exact-string dependency inventory.
- `fixtures/scenario-contracts.yaml`: exactly eleven scenario records with non-empty `required` and `forbidden` arrays.
- `fixtures/invalid-rule-disposition.yaml`: one value outside the closed semantic disposition set.
- `fixtures/invalid-literal-classification.yaml`: one value outside the closed literal classification set.
- Before/after profile resource manifests: canonical LF-normalized identities counted once in documented order.
- Adapter tests use fresh temporary roots and repository-owned fixtures; they do not modify tracked generated output.

Fixture IDs, paths, and expected results are deterministic. No fixture contains prompts, credentials, user data, model identities, transcripts, wall-clock assumptions, random values, or network dependencies.

## Mocking/stubbing policy

Do not mock profile classification, resource parsing, resource containment, package inventory, canonical-to-generated bytes, archive contents, or temporary installed-tree bytes in their final proof. Static scenario records model contract inputs and expected outcomes; they do not simulate an LLM. Temporary filesystem roots may isolate package generation and installation. Network and target-agent runtimes are not stubbed because they are outside acceptance.

## Migration or compatibility tests

T7 inventories and classifies all discovered exact-string consumers. Normative contract literals remain exact unless the approved contract changes. Parser/package contracts are preserved or migrated with every consumer in the same milestone. Test-only incidental assertions change with simplified prose and do not become policy. T11 proves current generated and installed package compatibility; historical artifacts remain untouched. T13 proves rollback to the prior complete canonical package.

## Observability verification

Every automated failure must identify its test or command ID and the affected rule, literal, profile, resource, target, or invariant. Change-local evidence records inventory counts, profile resource identities, before/after words and bytes, package parity targets, semantic-review outcome, and limitations. No model identity, prompt, transcript, or runtime retry is acceptance evidence.

## Security/privacy verification

CMD2 and T10 retain mapped-resource containment and reject paths escaping `skills/implement/`. CMD7 writes only to a fresh temporary directory and performs no publication or network call. T9 rejects credentials, private prompts, transcripts, runtime calls, and nondeterministic model evidence from acceptance. No user data is processed.

## Performance checks

T8 is the performance proof. It requires material word and byte reduction for IP0 and IP1 and justified non-regression for IP2 while reporting total package change. The 30–45 percent isolated target is advisory. Token estimates are omitted unless an already-pinned repository tool, version, vocabulary, and normalization are recorded; no tokenizer dependency may be added.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Automation rationale: a closed-schema command cannot prove that all meaningful source rules and all exact-string consumers were discovered.
- Owner and stage: independent code reviewer during M1 before any M2 prose movement.
- Required environment: repository checkout at the M1 revision with the unchanged baseline `skills/implement/` package; no network or target agent.
- Inputs: current full `skills/implement/SKILL.md`, mapped boundary reference, both M1 ledgers, CMD1 output, and repository-local `rg` results for headings, vocabulary, result labels, status, claim, milestone, handoff, review, and Resource-map literals across `scripts/`, `tests/`, `specs/`, `skills/`, and adapter/package tests.
- Procedure:
  1. Read the full baseline `SKILL.md` and assign every behaviorally significant paragraph or distinct rule to exactly one semantic ledger row.
  2. Reconcile every repeated rule cluster to one row without merging behaviorally different clauses.
  3. Search the named consumer surfaces for every normalized heading, closed status/milestone value, `READ`/`COPY` mapping, result label, claim term, and exact phrase asserted or parsed from `implement`.
  4. Reconcile every real exact-string consumer to one literal row and record non-contract search matches with a concise exclusion rationale in the evidence artifact.
  5. Confirm unknown-value fixtures failed closed, obsolete semantic removal cites an approved contract change, and no M2 package prose has changed.
- Pass condition: complete baseline semantic and literal coverage, one unique treatment per entry, justified exclusions, CMD1 pass, and unchanged canonical package bytes.
- Failure condition: any uncovered significant rule, duplication cluster, real literal consumer, unjustified exclusion, unknown-value acceptance, or pre-audit package mutation.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/m1-preservation-inventories.md`, including reviewer, revision, searches, counts, exclusions, CMD1 result, baseline hash, findings, and outcome.

### MP1. Semantic preservation and ownership review

- Automation rationale: deterministic validators cannot determine whether compressed or relocated prose preserves complete meaning and correct policy ownership.
- Owner and stage: independent code reviewer during M3 before M3 closeout.
- Required environment: repository checkout at the reviewed M3 revision; no network, target agent, credentials, or generated untracked source required.
- Inputs: approved spec and plan, pre-change `skills/implement/SKILL.md`, final complete `skills/implement/` package, both final ledgers, scenario fixtures, and CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, and CMD7 result summaries.
- Procedure:
  1. Follow every semantic ledger row from source behavior to exactly one final destination and preservation proof.
  2. Confirm every R3 universal behavior is explicit in `SKILL.md` and usable without either conditional reference.
  3. Confirm R9 and R11 procedure appears only in its assigned reference and that cross-references do not duplicate governing rules.
  4. Confirm the result asset owns labels/layout only and its three groups match R14-R15.
  5. Inspect every literal ledger consumer and treatment; reject incidental tests as policy evidence.
  6. Compare stop, validation failure, spec-gap, accepted-correction, rereview, milestone, claim, and code-review handoff semantics before and after.
  7. Confirm measurement and package evidence makes no claim broader than direct proof and contains no target-runtime evidence.
- Pass condition: every significant rule and literal is accounted for, ownership matches R1-R22, R31 semantics are unchanged, and no unresolved ambiguity or forbidden policy leakage remains.
- Failure condition: any missing rule, unjustified literal treatment, universal-policy omission, duplicated or exchanged owner, output-policy leakage, weakened lifecycle behavior, or evidence overclaim.
- Evidence artifact: `docs/changes/2026-08-11-implement-skill-simplification/evidence/semantic-preservation-review.md`, recording reviewer, revision, inputs, row counts, checks, findings, and outcome.

No other manual proof is required.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another target-agent runtime; acceptance covers deterministic package and contract integrity, not model behavior.
- Do not send prompts, grade transcripts, select models, pin runtime versions, or retry nondeterministic journeys.
- Do not add permanent line, word, token, prose-quality, or simplicity thresholds; measurements are change-local evidence.
- Do not test or optimize other skills, workflow stage order, new selectors, schedulers, services, state stores, or architecture.
- Do not hand-edit or track generated adapter skill bodies as source.
- Do not infer semantic preservation from snapshots or file-size reduction alone.
- Do not run publication, release, remote, credentialed, or destructive operations.

## Uncovered gaps

None.

Every R1-R33 requirement, E1-E7 example, EC1-EC10 edge case, BND-INPUT-001 through BND-ENV-001 boundary, and INT-001 through INT-008 interaction has direct automated, manual, or hybrid proof. Any newly discovered behavior or architecture ambiguity returns to the owning spec or architecture assessment rather than being invented here.

## Next artifacts

- Formal `test-spec-review`.
- After an approving current review only: M1 implementation and code review, then the remaining approved milestones and lifecycle gates.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review` after CMD8, CMD9, and structural review-artifact validation pass. This proof map does not authorize implementation until formal review approves it and workflow records the handoff.
