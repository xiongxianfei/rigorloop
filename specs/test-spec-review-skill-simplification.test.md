# Test-Spec-Review Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/test-spec-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-11-test-spec-review-skill-simplification.md`
- Architecture/ADRs: architecture not required; assessment at `docs/changes/2026-08-11-test-spec-review-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/test-spec-review-skill-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/spec-review-r2.md` |
| execution plan | `docs/plans/2026-08-11-test-spec-review-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-11-test-spec-review-skill-simplification/reviews/plan-review-r1.md` |
| architecture assessment | `docs/changes/2026-08-11-test-spec-review-skill-simplification/architecture-assessment.md` | not applicable | `architecture-not-required`; no architecture artifact entry or review required |

## Testing strategy

Use contract-level static scenarios and fail-closed ledger checks before instruction movement, focused skill-validator integration proof during package refactoring, and generated, archived, and temporary-installed package proof after refactoring.
Independent manual review proves semantic completeness and one-owner disposition where deterministic structure cannot judge meaning.

No end-to-end target-agent execution is permitted.
The relevant end-to-end boundary is the deterministic canonical-to-installed filesystem package chain, exercised by existing adapter tooling in temporary directories.
Migration proof classifies and migrates exact consumers without freezing incidental prose.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T2, T10, T11, T12 | contract, integration, manual | One complete `test-spec-review`-owned package. |
| R2 | T1, T4, T12 | contract, manual | Advisory review remains self-sufficient. |
| R3 | T1, T3 | contract | Lifecycle and handoff are independent closed axes. |
| R4 | T1, T3, T9 | contract | Formal identity and stale or ambiguous stops. |
| R5 | T1, T3 | contract | Isolated handoff blocks continuation. |
| R6 | T1, T5, T9 | contract | Boundary applicability is evidence-derived. |
| R7 | T1, T2, T9 | contract | Durable recording trigger is exact and derived. |
| R8 | T1, T2, T5 | contract | Early and late overlay loads are exact. |
| R9 | T1, T2, T5 | contract | Exactly four base assemblies. |
| R10 | T2, T16 | contract | Overlay and finding multiplicity are exact. |
| R11 | T1-T3 | contract | Late overlay cannot upgrade authority. |
| R12 | T2, T3, T12 | contract, manual | Shared and formal-only procedure are visibly separated. |
| R13 | T2, T16 | contract | Shared recording owns durable mechanics. |
| R14 | T3, T15-T16 | contract | Formal settlement writes only the matching entry after evidence. |
| R15 | T2, T5, T16 | contract | Isolated material findings record or report a complete blocker. |
| R16 | T2, T16 | contract | Detailed versus clean records and resolution triggers remain exact. |
| R17 | T2, T12, T16 | contract, manual | Assets own layout only. |
| R18 | T5, T10-T11 | integration | Triggered missing or mixed resources fail safely. |
| R19 | T4, T9, T12 | contract, manual | Universal proof semantics remain complete. |
| R20 | T4, T9 | contract | Status, next-stage, and handoff vocabularies remain closed. |
| R21 | T3-T4 | contract | Approved and non-approved routing remains exact. |
| R22 | T1, T3-T4, T12 | contract, manual | Formal and advisory proof quality matches without shared eligibility. |
| R23 | T3, T15 | contract | Substantive staleness and formatting-only currency are preserved. |
| R24 | T15, T12 | contract, manual | Review independence and record-before-fix are preserved. |
| R25 | T6, T14 | contract, manual | Semantic ledger fields and complete inventory. |
| R26 | T6 | unit | Closed semantic dispositions reject unknown values first. |
| R27 | T7, T14 | contract, manual | Literal inventory fields and independent classification. |
| R28 | T7, T12, T14 | migration, manual | Real consumers migrate atomically; incidental prose may change. |
| R29 | T8 | contract | Deterministic LF-normalized words and bytes accounting. |
| R30 | T8, T12 | contract, manual | Advisory reduction target cannot override semantics. |
| R31 | T6-T12 | contract, integration, manual | Deterministic proof only; runtime acceptance is forbidden. |
| R32 | T9-T12 | contract, integration | No runtime, transcript, tokenizer, or permanent simplicity machinery. |
| R33 | T10-T11 | integration | Existing owners prove structure and package parity. |
| R34 | T5, T10-T11 | integration | Both existing boundary references remain paired and unchanged. |
| R35 | T6, T8, T12, T14 | contract, manual | Repeated rules and structures have one owner. |
| R36 | T13 | contract | Assessment precedes plan and ambiguity routes upstream. |
| R37 | T5, T11, T13 | integration, contract | Complete rollout and rollback; mixed package fails. |
| R38 | T1-T5, T12, T15-T16 | contract, manual | Existing review, recording, settlement, status, and handoff behavior is preserved. |
| R39 | T1, T3, T9 | contract | Exactly three lifecycle/handoff pairs are valid. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T4 | Clean advisory review stays on TSR0. |
| E2 | T1-T2, T16 | Material advisory result adds recording before output. |
| E3 | T1, T3 | Formal isolated review settles and stops. |
| E4 | T1, T3 | Workflow-managed formal approval returns routing to workflow. |
| E5 | T1-T2 | Explicit recording adds no formal authority. |
| E6 | T2, T5 | Boundary resources are independently additive. |
| E7 | T5, T16 | Missing recording resources preserve the finding and block handoff. |
| E8 | T1, T5 | Ordinary review omits boundary procedure. |
| E9 | T1, T3, T9 | Advisory plus workflow-managed stops before review. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R3, R4, R5, R6, R7, R9, R20, R39 | BND-INPUT-001 | T1, T4, T9 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R3, R4, R5, R7, R8, R11, R12, R14, R15, R16, R18, R23, R36, R37, R39 | BND-STATE-001 | T1-T3, T5, T13, T15-T16 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD9 | `evidence/m2-package-refactor.md`; `architecture-assessment.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-003 | covered | R3, R4, R5, R11, R12, R14, R15, R21, R22, R24, R39 | BND-AUTH-001 | T1, T3, T12, T15-T16 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R8, R9, R10, R12, R13, R17, R18, R34, R35, R38 | BND-COMPOSE-001 | T1-T2, T4-T5, T10-T12, T16 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-005 | covered | R8, R13, R14, R15, R18, R23, R24, R37 | BND-TEMPORAL-001 | T2-T3, T5, T13, T15-T16 | contract | automated | CMD1, CMD3, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-006 | covered | R4, R6, R15, R16, R18, R26, R27, R30, R31, R36, R37 | BND-RECOVERY-001 | T1, T5-T9, T13, T16 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD9 | `evidence/m1-preservation-inventories.md`; `architecture-assessment.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | R20, R21, R23, R25, R26, R27, R28, R33, R35, R37, R38 | BND-COMPAT-001 | T4, T6-T8, T10-T15 | integration | hybrid | CMD1, CMD3, CMD6, CMD7 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R18, R29, R31, R32, R33, R34, R37 | BND-ENV-001 | T5, T8-T11, T13 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R3, R5, R7, R8, R11, R14, R39 | INT-001 | T1, T3, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R7, R8, R10, R12, R13, R15, R17 | INT-002 | T1-T3, T16 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-011 | covered | R6, R9, R18, R34 | INT-003 | T1-T2, T5 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-012 | covered | R15, R16, R18 | INT-004 | T2, T5, T16 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-013 | covered | R19, R20, R21, R22, R35, R38 | INT-005 | T4, T12, T15 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-014 | covered | R25, R26, R27, R28, R29, R30 | INT-006 | T6-T9, T12, T14 | contract | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-015 | covered | R31, R32, R33, R34, R37 | INT-007 | T5, T10-T11, T13 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 direct formal review lacks continuation | T1, T3 | settle then stop with allowed handoff value |
| EC2 two advisory material findings | T2, T16 | one overlay load and two finding blocks |
| EC3 clean advisory explicit recording | T1-T2 | record without settlement or eligibility |
| EC4 material finding asset missing | T5, T16 | finding visible, recording blocked, no fix or handoff |
| EC5 formal result asset exists but reference is missing | T5 | stop before recording or settlement |
| EC6 non-boundary text contains `PRF-*` | T1, T5 | text alone does not activate boundary context |
| EC7 one boundary reference is stale | T5, T11 | boundary-dependent verdict and package proof fail |
| EC8 formatting-only test-spec edit | T15 | prior formal approval remains current |
| EC9 unknown review status | T4, T9 | reject unknown before consistency checking |
| EC10 main file shrinks by duplicating policy | T8, T12 | ownership and semantic acceptance fail |
| EC11 target-agent runtime unavailable | T9-T11 | deterministic proof remains sufficient |
| EC12 stale flat architecture example | T13 | route architecture correction before planning |
| EC13 automation requests handoff without formal identity | T1, T3, T9 | stop before review and name missing authority |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-test-spec-review-skill-simplification"); rules=json.loads((root/"test-spec-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"test-spec-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-recording-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/test-spec-review/SKILL.md")) or (row["disposition"] == "retained-recording-reference" and row["destination"].startswith("skills/test-spec-review/references/test-spec-review-recording-and-settlement.md")) or (row["disposition"] == "retained-boundary-reference" and row["destination"].startswith("skills/test-spec-review/references/boundary-first-")) or (row["disposition"] == "asset-owned" and row["destination"].startswith("skills/test-spec-review/assets/")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/test-spec-review/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"advisory-clean-isolated","advisory-explicit-recording","advisory-material-late-overlay","formal-isolated","formal-workflow-managed","advisory-workflow-managed-invalid","boundary-advisory","boundary-formal","missing-recording-reference","missing-result-asset","missing-finding-asset","missing-boundary-resource","stale-formal-target","formal-settlement-isolation","blocked-recording","unknown-review-status"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Block on unknown closed values first, then missing or empty fields, destination inconsistency, duplicate IDs, or incomplete scenarios. | Not applicable; every assertion must execute. | `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/test-spec-review/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block malformed structure, mapping, containment, placeholder, or claim contract. | Not applicable; deterministic validation. | `evidence/m2-package-refactor.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block any focused or regression failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated-skill inventory or resource test failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Temporary filesystem only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated package drift or missing resources. | Not applicable; deterministic check. | `evidence/m2-package-refactor.md` | Temporary generated tree; no tracked output writes. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD7 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "test-spec-review"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Stop on the first failed subprocess; block any generated, archive, or temporary installed target missing byte-identical resources. | Not applicable; direct package selection must produce all supported targets. | `evidence/m3-package-proof.md` | Uses immutable trusted fixture `v0.3.6`; Python owns and removes one fresh temporary directory; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/test-spec-review-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block missing or invalid proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only repository validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every state-changing handoff | Block invalid artifact or planned-work state. | Not applicable; deterministic metadata validation. | owning change validation ledger | Read-only validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-test-spec-review-skill-simplification` | existing/configured | review stages | lifecycle | every formal review handoff | Block malformed or missing review evidence. | Not applicable; deterministic artifact validation. | review log and review records | Read-only validation. |

CMD1 is identical to the approved plan's M1 command and must be copied verbatim into execution evidence.
CMD7 intentionally uses a temporary directory and does not clean it through a destructive command; the operating environment may reclaim it after evidence capture.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T6-T9, T14 | MP0 | CMD1, CMD9 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged. |
| M2 | T1-T5, T9-T10, T15-T16 | none | CMD2, CMD3, CMD4, CMD5, CMD9 | `evidence/m2-package-refactor.md` | M2 code-review | Focused failing assertions precede package text changes. |
| M3 | T8-T13 | MP1 | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8, CMD9, CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves assembly, semantic, and package-chain acceptance. |

## Test cases

### T1. Lifecycle, handoff, boundary, and recording classification fails closed

- Covers: R2-R9, R11, R20, R39; E1-E6, E8-E9; EC1, EC3, EC6, EC13; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001, INT-003
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: static scenarios for all valid lifecycle and handoff pairs, the invalid pair, boundary applicability, formal identity, and false-to-true recording transitions.
- Steps: validate classifications, required evidence, exact base assembly, and stop behavior for every scenario.
- Expected result: valid cases select one authority set and assembly; invalid, stale, ambiguous, or conversational-only cases stop before review, recording, settlement, or routing.
- Failure proves: classification could broaden authority or load the wrong procedure.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused assertions in `scripts/test-skill-validator.py` plus scenario fixtures
- Required by milestone: M2

### T2. Recording overlay loads once and preserves authority

- Covers: R7-R13, R15-R17, R38; E2, E5-E7; EC2-EC5; BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-002, INT-004
- Level: integration
- Command IDs: CMD3
- Fixture/setup: clean advisory, explicit-recording, one- and two-finding advisory, formal clean, and missing asset/reference scenarios.
- Steps: assert overlay timing, one reference and result asset load, finding asset multiplicity, blocked-recording fields, and unchanged lifecycle and handoff values.
- Expected result: recording obligations change only when triggered; no overlay branch grants settlement or continuation.
- Failure proves: late recording can erase findings, duplicate structures, or leak authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py` and static scenarios
- Required by milestone: M2

### T3. Formal settlement and handoff remain independently bounded

- Covers: R3-R5, R11-R14, R21-R24, R38-R39; E3-E4, E9; EC1, EC8, EC13; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-001-INT-002
- Level: integration
- Command IDs: CMD3, CMD9
- Fixture/setup: equivalent approved formal reviews under isolated and workflow-managed handoff, plus advisory invalid handoff and stale target records.
- Steps: assert record-before-settlement, matching-entry-only mutation, authoring-evidence removal, exact review mapping, no workflow write by review, isolated stop, and workflow-owned continuation.
- Expected result: settlement follows formal authority only; handoff controls continuation independently.
- Failure proves: recording, settlement, routing, or implementation eligibility has crossed ownership.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill-validator and change-metadata fixtures
- Required by milestone: M2

### T4. Universal proof, status, staleness, claim, and output semantics stay inline

- Covers: R2, R19-R23, R35, R38; E1, E3-E4; EC8-EC10; BND-INPUT-001, BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: positive and negative inline-section assertions for traceability, failures, commands, fixtures, manual proof, statuses, routing, claims, and compact output.
- Steps: validate exact closed values, approved and non-approved mappings, stale and formatting-only cases, and absence of duplicated policy in conditional resources.
- Expected result: advisory review can judge any proof map truthfully without loading recording procedure.
- Failure proves: common-path simplification weakened review rigor or moved universal policy behind a trigger.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T5. Boundary and recording resource failures are exact

- Covers: R6, R8-R10, R15, R18, R34, R37; E6-E8; EC4-EC7; BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-003-INT-004, INT-007
- Level: integration
- Command IDs: CMD1, CMD2, CMD3
- Fixture/setup: TSR0, TSR0B, TSR1, TSR1B and missing, unreadable, escaped, stale, or mixed resource fixtures.
- Steps: assert exact required and forbidden loads, paired boundary references, blocked recording, finding visibility, and stop-before-dependent-verdict behavior.
- Expected result: untriggered resources do not load; every triggered invalid resource blocks without memory reconstruction.
- Failure proves: progressive disclosure or package integrity can be bypassed.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill-validator tests and static scenarios
- Required by milestone: M2

### T6. Semantic-rule ledger is complete and fail-closed

- Covers: R25-R26, R31, R35; BND-RECOVERY-001, BND-COMPAT-001; INT-006
- Level: unit
- Command IDs: CMD1
- Fixture/setup: valid ledger and invalid unknown-disposition fixture.
- Steps: validate required fields, unique IDs, source coverage, assembly values, disposition vocabulary, destination, and preservation proof; evaluate unknown value first.
- Expected result: complete valid ledger passes and unknown or missing disposition fails before consistency.
- Failure proves: a rule can disappear or validation fails open.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: CMD1
- Required by milestone: M1

### T7. Literal compatibility is separate and safely migrated

- Covers: R27-R28, R31, R38; BND-RECOVERY-001, BND-COMPAT-001; INT-006
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: valid literal inventory, invalid classification fixture, and exact consumer search results.
- Steps: classify each consumer and verify normative preservation, atomic parser migration, incidental test updates, and obsolete evidence.
- Expected result: exact contracts remain or migrate atomically; tests alone do not own prose.
- Failure proves: incidental coupling freezes text or a real consumer breaks.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md`
- Automation location: CMD1 plus focused consumer assertions
- Required by milestone: M1 and M3

### T8. Assembly and package measurements are deterministic and honest

- Covers: R9-R10, R29-R31, R35; EC10; BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: unit
- Command IDs: CMD1
- Fixture/setup: canonical before and after files and documented assembly order.
- Steps: normalize LF, count unique files once, compute words and bytes for every resource, base assembly, overlay, and package, and compare duplicate clusters.
- Expected result: TSR0 materially shrinks, formal and total-package deltas are explicit, and percentage remains advisory.
- Failure proves: relocation or duplication is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: repository-local standard-library measurement recorded in evidence
- Required by milestone: M3

### T9. Static scenarios preserve negative behavior without a runtime

- Covers: R4, R6-R8, R20, R26-R27, R30-R32, R39; E9; EC6, EC9, EC11, EC13; BND-INPUT-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-006
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: exactly sixteen scenario records with non-empty required and forbidden lists.
- Steps: validate every scenario identity and assert no command, fixture, or evidence field invokes or grades an agent runtime.
- Expected result: all required outcomes and stops are represented deterministically.
- Failure proves: negative behavior is unproved or acceptance expanded into runtime testing.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md`
- Automation location: CMD1 and focused skill assertions
- Required by milestone: M1 and M2

### T10. Canonical and generated package validation uses existing owners

- Covers: R1, R18, R31-R34, R37; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-007
- Level: integration
- Command IDs: CMD2, CMD3, CMD4, CMD5
- Fixture/setup: changed canonical package and existing generated-skill tests.
- Steps: validate structure, five resource mappings, containment, unchanged boundary identity, asset placeholders, generated inventory, and parity.
- Expected result: complete valid package passes; missing, escaped, stale, malformed, or mixed resources fail.
- Failure proves: durable package validators do not cover the new reference or existing resources.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: existing skill and build validation suites
- Required by milestone: M2 and M3

### T11. Archives and temporary installed packages preserve every resource

- Covers: R1, R18, R31, R33-R34, R37; EC7, EC11; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-007
- Level: e2e
- Command IDs: CMD6, CMD7
- Fixture/setup: locally generated Codex, Claude Code, and opencode release candidates in a temporary directory.
- Steps: inspect archives and clean installations for the recording reference, both boundary references, and both assets at canonical relative paths and bytes; exercise missing and mixed failure fixtures.
- Expected result: every target is complete and byte-identical; incomplete targets fail.
- Failure proves: canonical acceptance does not survive distribution.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution and validation scripts
- Required by milestone: M3

### T12. Independent semantic review confirms behavior and ownership

- Covers: R1-R2, R12, R17, R19, R22, R24, R28, R30-R32, R35, R38; EC10-EC11; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-002, INT-005-INT-006
- Level: manual
- Command IDs: none
- Fixture/setup: complete final package, spec, plan, test spec, ledgers, scenarios, baseline skill, and literal consumers.
- Steps: execute MP1.
- Expected result: every semantic rule has one correct owner; no universal policy is hidden; advisory and formal quality, settlement, claims, recording, outputs, and handoffs remain intact.
- Failure proves: deterministic structure passed while meaning regressed.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: manual
- Required by milestone: M3

### T13. Architecture ordering, rollout, and rollback stay bounded

- Covers: R36-R37; EC12; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-007
- Level: integration
- Command IDs: CMD6, CMD7, CMD9
- Fixture/setup: recorded assessment, complete current package, simulated incomplete package, and prior complete package identities.
- Steps: verify assessment predates plan; assert reassessment triggers; reject incomplete and mixed assemblies; prove the selected complete package path; restore the trusted prior-package fixture and prove parity again.
- Expected result: no architecture work is invented, ambiguity routes upstream, and rollout and rollback are atomic.
- Failure proves: planning bypassed architecture applicability or package recovery is unsafe.
- Evidence artifact: `architecture-assessment.md`; `evidence/m3-package-proof.md`
- Automation location: change-metadata assertions plus package rollback fixtures
- Required by milestone: M3

### T14. Current rules and literal consumers are fully inventoried

- Covers: R19-R20, R25, R27-R28, R35, R38; BND-COMPAT-001; INT-006
- Level: manual
- Command IDs: CMD1
- Fixture/setup: full current package, scripts, tests, specs, fixtures, and adapter and package consumers.
- Steps: execute MP0 before prose movement and reconcile every source cluster and exact match to one ledger entry.
- Expected result: no significant rule or consumer is omitted and proposed duplicate or obsolete treatments are justified.
- Failure proves: later semantic preservation is based on an incomplete baseline.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: manual audit supported by bounded `rg` searches and CMD1
- Required by milestone: M1

### T15. Review independence and approval staleness remain intact

- Covers: R14, R23-R24, R38; EC8; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD3, CMD10
- Fixture/setup: first-pass material finding, review-driven correction attempt, substantive edit, and confirmed formatting-only edit.
- Steps: assert finding recording before correction, no unauthorized test-spec rewrite, substantive rereview requirement, and formatting-only current approval.
- Expected result: review independence and current-evidence rules match the baseline.
- Failure proves: simplification weakened adversarial review or stale-approval safety.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused skill-validator and review-artifact fixtures
- Required by milestone: M2

### T16. Durable review artifacts and structural assets remain exact

- Covers: R10, R13-R17, R38; E2, E7; EC2-EC5; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002, INT-004
- Level: integration
- Command IDs: CMD3, CMD10
- Fixture/setup: clean formal receipt, material detailed record, two findings, blocked recording, and formal settlement fixtures.
- Steps: validate result and finding labels, no empty finding block, required detailed fields, review-log links, conditional resolution, blocked diagnostics, record-before-settlement, and matching-entry-only writes.
- Expected result: assets provide layout while procedure and authority remain outside them.
- Failure proves: structural simplification changed recording completeness or made assets policy owners.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill-validator and review-artifact validation fixtures
- Required by milestone: M2

## Fixtures and data

- `test-spec-review-rule-disposition.yaml`: JSON-compatible YAML with stable semantic rule records.
- `test-spec-review-literal-compatibility.yaml`: JSON-compatible YAML with exact consumer records.
- `fixtures/scenario-contracts.yaml`: exactly sixteen static scenario records with required and forbidden outcomes.
- `fixtures/invalid-rule-disposition.yaml`: one unknown semantic disposition.
- `fixtures/invalid-literal-classification.yaml`: one unknown literal classification.
- Existing skill, review-artifact, build, and adapter fixtures remain the durable proof owners.
- Temporary generated and installed trees use library-owned temporary directories and are never published.

## Mocking/stubbing policy

Do not mock an agent runtime because no agent runtime is part of acceptance.
Static records model contract inputs and expected outcomes; existing filesystem and package helpers may isolate temporary roots but must not bypass canonical resource parsing, lifecycle validation, or byte comparison.

## Migration or compatibility tests

T7 proves literal-consumer migration, T10-T11 prove generated and distributed package compatibility, T13 proves complete-package rollback, T15 proves staleness compatibility, and T12 proves semantic compatibility.
Historical review and change-local evidence remains readable and is not rewritten.

## Observability verification

Evidence must identify rule, literal, and scenario counts; assembly file lists; words and bytes; command IDs and results; package targets; resource paths and hashes; semantic-review conclusions; recording status and paths; and blockers.
No new runtime logs, metrics, traces, or audit service is required.

## Security/privacy verification

Commands read repository files and use temporary local package roots only.
They must not access credentials, network services, hosted agents, publication endpoints, private data, or paths outside declared package roots.

## Performance checks

Measure loaded words and bytes for `SKILL.md`, TSR0, TSR0B, TSR1, TSR1B, the recording overlay, and total package.
Do not add timing, model-token, or runtime-latency gates; token estimates are optional only when an existing pinned repository implementation is available.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: semantic equivalence and normative-versus-incidental ownership cannot be established by exact-string checks alone.
- Required environment: tracked repository at the M1 baseline with the complete current package and all bounded consumers available.
- Steps:
  1. Read the complete current `skills/test-spec-review/SKILL.md`, both boundary references, and both assets.
  2. Group every behaviorally significant rule and duplicate cluster by stable rule ID.
  3. Search scripts, tests, specs, fixtures, generated/package tests, and adapter validation for exact headings, fields, vocabulary, and phrases.
  4. Reconcile every rule and literal match to exactly one ledger row and validate closed values with CMD1.
- Evidence artifact: `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: every material rule and discovered consumer is accounted for with one justified treatment and no canonical prose has moved.
- Failure condition: any rule, consumer, owner, or classification is missing, duplicated, ambiguous, or unsupported.
- Owning stage: implement M1; required before M1 code-review.

### MP1. Semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: validators can prove structure and bytes but not completeness, procedure ownership, authority, or semantic equivalence.
- Required environment: final canonical package, both ledgers, scenario evidence, measurements, current spec, plan and test spec, and package proof.
- Steps:
  1. Compare every semantic ledger row with its final destination and preservation proof.
  2. Confirm inline completeness for classification, proof semantics, status, staleness, findings, stops, claims, compact result, and handoff.
  3. Confirm the recording reference owns shared mechanics and a visibly separate formal-only settlement section, without redefining universal policy.
  4. Compare advisory and formal proof quality, isolated and workflow-managed handoff, settlement writes, review independence, and implementation eligibility with the baseline.
  5. Confirm literal consumers received their classified treatment and measurements did not hide duplication or loss.
- Evidence artifact: `docs/changes/2026-08-11-test-spec-review-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: every rule has one correct owner, every claim remains evidence-bound, every valid assembly is usable, and no unapproved semantic change exists.
- Failure condition: any rule disappears, duplicates, moves behind an invalid trigger, changes authority, or lacks direct preservation evidence.
- Owning stage: implement M3; required before M3 code-review and final review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime; the product contract is packaged guidance and deterministic resources.
- Do not add prompt journeys, transcript snapshots, model selection, retry scoring, or runtime-version evidence.
- Do not make line, word, byte, token, or prose-quality measurements permanent product validators.
- Do not test unrelated skills, workflow stage order, state schema, implementation behavior, or PR opening beyond preserved ownership assertions.
- Do not publish adapters or access network services; local temporary package inspection is sufficient.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation M1 only after the review is approved and workflow routes implementation authority.

## Follow-on artifacts

None yet

## Readiness

Ready for `test-spec-review`.
