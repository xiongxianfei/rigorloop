# Proposal-Review Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/proposal-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-11-proposal-review-skill-simplification.md`
- Architecture/ADRs: architecture not required; assessment at `docs/changes/2026-08-11-proposal-review-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/proposal-review-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/spec-review-r1.md` |
| execution plan | `docs/plans/2026-08-11-proposal-review-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-11-proposal-review-skill-simplification/reviews/plan-review-r1.md` |
| architecture assessment | `docs/changes/2026-08-11-proposal-review-skill-simplification/architecture-assessment.md` | not applicable | `architecture-not-required`; no architecture artifact entry or review required |

## Testing strategy

Use contract-level static scenarios and fail-closed ledger checks before instruction movement, focused skill-validator integration proof during package refactoring, and generated, archive, and temporary installed-package proof after refactoring.
Independent manual review proves semantic completeness and one-owner disposition where deterministic structure cannot judge meaning.

No end-to-end target-agent execution is permitted.
The end-to-end boundary is the deterministic canonical-to-installed filesystem package chain exercised by existing adapter tooling in temporary directories.
Migration proof classifies exact consumers and migrates real contracts without freezing incidental prose.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T5, T10, T11, T12 | contract, integration, manual | One complete `proposal-review` package. |
| R2 | T1, T3, T12 | contract, manual | Core advisory review is self-sufficient. |
| R3 | T3, T12, T14 | contract, manual | Universal judgment remains complete. |
| R4 | T3, T10, T12 | integration, manual | Default path and shared recording contract remain inline. |
| R5 | T1, T2, T9 | contract | Closed recording and automation modes fail closed. |
| R6 | T1, T2, T9 | contract | Exactly four valid mode combinations. |
| R7 | T1, T2, T9 | contract | Durable triggers are exhaustive. |
| R8 | T2, T5, T9 | contract | Late durable activation precedes effects. |
| R9 | T2, T4, T12 | contract, manual | Recording reference owns detailed procedure only. |
| R10 | T1, T2, T4, T12 | contract, manual | Loading and authority remain separate. |
| R11 | T2, T4 | contract | Advisory durable writes never settle or continue. |
| R12 | T2, T4 | contract | Formal settlement is exact and never advances workflow. |
| R13 | T1, T2, T4 | contract | Automation-only procedure requires formal authority. |
| R14 | T2, T4, T9 | contract | Clean explicit advisory recording stays standalone. |
| R15 | T2, T4, T9 | contract | Governing change-ID order is preserved. |
| R16 | T2, T4, T13 | contract, integration | Generated roots remain recording-only. |
| R17 | T2, T4, T9 | contract | Ambiguity, collision, and write failure block honestly. |
| R18 | T3, T12 | contract, manual | Specialized procedure has one owner. |
| R19 | T3, T6, T9 | contract | Predicate vocabulary and review ownership are closed. |
| R20 | T3, T6, T9 | contract | Combined, late, and ambiguous predicates are governed. |
| R21 | T1, T5, T8 | contract | Exactly four resource assemblies. |
| R22 | T5, T12 | contract, manual | Reference conflicts stop and never override owners. |
| R23 | T5, T9, T11 | contract, integration | Triggered resource failures stop without reconstruction. |
| R24 | T7, T10, T12 | integration, manual | Result asset is the sole overall structure. |
| R25 | T7, T9 | contract | Conditional result groups have exact applicability. |
| R26 | T7, T9 | contract | Omission, blocked data, and placeholders are deterministic. |
| R27 | T7, T12 | contract, manual | Assets own structure only. |
| R28 | T1-T4, T7, T12 | contract, manual | Existing semantics remain intact. |
| R29 | T8, T14 | contract, manual | Semantic ledger is complete. |
| R30 | T8 | unit | Unknown semantic disposition fails first. |
| R31 | T8, T12, T14 | migration, manual | Literal consumers are independently classified and migrated. |
| R32 | T9 | contract | LF-normalized assembly and package measurement. |
| R33 | T9, T12 | contract, manual | Reduction remains advisory and semantic. |
| R34 | T8-T12 | contract, integration, manual | Deterministic proof only; no runtime or permanent machinery. |
| R35 | T10, T11 | integration | Existing owners prove canonical through installed parity. |
| R36 | T13 | contract | Architecture assessment precedes plan and routes ambiguity. |
| R37 | T5, T11, T13 | integration, contract | Complete rollout and rollback; mixed package fails. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1 | Clean advisory review stays PRR0 and isolated. |
| E2 | T2 | Late material evidence activates recording before output. |
| E3 | T2, T4 | Safe generated root records without settlement. |
| E4 | T2, T4 | Formal settlement uses exact same-change authority. |
| E5 | T1, T4 | Automated review without formal authority stops. |
| E6 | T3, T6 | Combined specialized predicates load once and all apply. |
| E7 | T7 | Formal automated specialized result uses all groups. |
| E8 | T5, T11 | Missing required resource stops dependent work. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R5, R6, R7, R14, R15, R19, R20 | BND-INPUT-001 | T1-T3, T6, T9 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R7, R8, R10, R11, R12, R13, R16, R17, R36, R37 | BND-STATE-001 | T1, T2, T4, T5, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD9 | `evidence/m2-package-refactor.md`; `architecture-assessment.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-003 | covered | R10, R11, R12, R13, R14, R15, R16, R17 | BND-AUTH-001 | T1, T2, T4, T12 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R9, R18, R21, R22, R23, R24, R25, R26, R27, R35 | BND-COMPOSE-001 | T1-T7, T10-T12 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-005 | covered | R8, R9, R12, R13, R17, R20, R37 | BND-TEMPORAL-001 | T2-T6, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-006 | covered | R5, R6, R17, R20, R22, R23, R26, R30, R31, R36, R37 | BND-RECOVERY-001 | T1-T9, T13 | contract | automated | CMD1, CMD3, CMD6, CMD7, CMD9 | `evidence/m1-preservation-inventories.md`; `architecture-assessment.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | R4, R28, R29, R30, R31, R35, R36, R37 | BND-COMPAT-001 | T8, T10-T14 | integration | hybrid | CMD1, CMD3, CMD6, CMD7 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R14, R15, R16, R17, R23, R32, R34, R35, R37 | BND-ENV-001 | T2, T5, T9-T11, T13 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R7, R8, R9, R17, R21 | INT-001 | T2, T5, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R10, R11, R12, R15, R16 | INT-002 | T2, T4, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-011 | covered | R18, R19, R20, R21 | INT-003 | T3, T5, T6, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-012 | covered | R23, R25, R26 | INT-004 | T5, T7, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-013 | covered | R29, R30, R31, R32, R33 | INT-005 | T8, T9, T12, T14 | contract | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-014 | covered | R34, R35, R37 | INT-006 | T10, T11, T13 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 non-material `changes-requested` | T1, T2 | durable recording activates |
| EC2 generated fallback collision | T2, T4 | blocked recording with complete finding |
| EC3 clean explicit standalone record | T2, T4 | no formal log or settlement |
| EC4 fallback record without settlement identity | T2, T4 | record succeeds; settlement blocked |
| EC5 two late specialized predicates | T3, T6 | both gates run once before status |
| EC6 installed adapter missing reference | T5, T11 | package and dependent review fail |
| EC7 applicable group lacks receipt path | T7 | group reports blocked and blocker |
| EC8 incidental exact-string test | T8, T14 | test migrates; semantics remain |
| EC9 size reduction hides universal policy | T9, T12 | semantic acceptance fails |
| EC10 stale or cross-change automation | T1, T4 | automated mode is invalid |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-proposal-review-skill-simplification"); rules=json.loads((root/"proposal-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"proposal-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-recording-reference","retained-conditional-gates-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/proposal-review/SKILL.md")) or (row["disposition"] == "retained-recording-reference" and row["destination"].startswith("skills/proposal-review/references/proposal-review-recording-and-settlement.md")) or (row["disposition"] == "retained-conditional-gates-reference" and row["destination"].startswith("skills/proposal-review/references/conditional-proposal-gates.md")) or (row["disposition"] == "asset-owned" and row["destination"].startswith("skills/proposal-review/assets/")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/proposal-review/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"advisory-clean","advisory-explicit-recording","advisory-material-existing-root","advisory-material-generated-root","generated-root-collision","formal-manual","formal-automated","invalid-advisory-automated","invalid-none-automated","late-durable-trigger","vision-exception","ordinary-vision","standing-artifact","standing-artifact-citation-only","scope-budget-broad","scope-budget-focused","combined-specialized","late-specialized","ambiguous-specialized","formal-specialized","result-groups","blocked-result-group","missing-reference","missing-asset","package-parity"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Block on unknown values first, then missing fields, destination inconsistency, duplicate IDs, or incomplete scenarios. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/proposal-review/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block malformed structure, mapping, containment, placeholder, or claim contract. | Not applicable; deterministic validation. | `evidence/m2-package-refactor.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block any focused or regression failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated-skill inventory or resource test failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Temporary filesystem only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated package drift or missing resources. | Not applicable; deterministic check. | `evidence/m2-package-refactor.md` | Temporary generated tree; no tracked output writes. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD7 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "proposal-review"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Stop on first failed subprocess and block any target missing byte-identical resources. | Not applicable; direct selection must produce all supported targets. | `evidence/m3-package-proof.md` | Uses immutable trusted fixture `v0.3.6`; temporary directory only; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/proposal-review-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block missing or invalid proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only repository validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-11-proposal-review-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every state-changing handoff | Block invalid artifact or planned-work state. | Not applicable; deterministic metadata validation. | owning change validation ledger | Read-only validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-proposal-review-skill-simplification` | existing/configured | review stages | lifecycle | every formal review handoff | Block malformed or missing review evidence. | Not applicable; deterministic artifact validation. | review log and review records | Read-only validation. |

CMD1 is identical to the approved plan's M1 command and must be copied verbatim into execution evidence.
CMD7 uses one managed temporary directory and performs no publication, network access, or target-agent execution.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T8, T9, T14 | MP0 | CMD1, CMD9 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged. |
| M2 | T1-T7, T10 | none | CMD2, CMD3, CMD4, CMD5, CMD9 | `evidence/m2-package-refactor.md` | M2 code-review | Focused failing assertions precede package text changes. |
| M3 | T9-T13 | MP1 | CMD1-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves assembly, semantic, and package-chain acceptance. |

## Test cases

### T1. Modes, durable triggers, assemblies, and automation fail closed

- Covers: R5-R7, R10, R13, R21, R28; E1, E5; EC1, EC10; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: static scenarios for every valid and invalid mode pair, durable trigger, assembly, and current, stale, missing, or cross-change automation authority.
- Steps: validate closed values, mode pair, durable predicate, assembly, and independently authorized effects.
- Expected result: valid cases select one pair and assembly; invalid or stale cases stop before dependent effects.
- Failure proves: classification can grant unauthorized recording, automation, or continuation.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused assertions in `scripts/test-skill-validator.py` plus scenario fixtures
- Required by milestone: M2

### T2. Recording activation and fallback roots preserve authority

- Covers: R7-R17, R28; E2-E4; EC1-EC4; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-ENV-001; INT-001-INT-002
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: clean, explicit, late material, existing-root, generated-root, collision, blocked-write, formal manual, and formal automated scenarios.
- Steps: assert reclassification ordering, artifact location, required evidence, allowed writes, settlement identity, and continuation prohibition.
- Expected result: required evidence records or reports blocked; recording-only roots never grant settlement or continuation.
- Failure proves: formal-review recording or authority behavior regressed.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill-validator tests and scenario fixtures
- Required by milestone: M2

### T3. Universal judgment and specialized predicate classification remain complete

- Covers: R2-R3, R18-R20, R28; E6; EC5; BND-INPUT-001, BND-COMPOSE-001, BND-TEMPORAL-001; INT-003
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: ordinary vision, vision exception, standing artifact, citation-only, broad and focused scope, combined, late, and ambiguous predicate scenarios.
- Steps: assert universal judgment stays inline and each specialized predicate has exact positive, negative, combined, late, and ambiguity outcomes.
- Expected result: gates load once and all true predicates apply; ordinary cases remain core; ambiguity blocks approval.
- Failure proves: progressive disclosure hides required judgment or deterministic validation claims semantic ownership.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py` and static scenarios
- Required by milestone: M2

### T4. Recording reference branches preserve side-effect authority

- Covers: R9-R17, R28; E3-E5; EC2-EC4, EC10; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-002
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: canonical reference and mode-specific positive and forbidden operation assertions.
- Steps: verify advisory, formal manual, and formal automated branches and forbidden settlement, packet, correction, workflow, and handoff operations.
- Expected result: detailed procedure is complete while every effect stays within classified authority.
- Failure proves: reference loading became authority or a required recording branch is missing.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused skill-validator assertions
- Required by milestone: M2

### T5. Resource assemblies and missing-resource failures are exact

- Covers: R1-R2, R8-R9, R18, R21-R23, R37; E8; EC6; BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-003-INT-004
- Level: integration
- Command IDs: CMD1-CMD5
- Fixture/setup: four assemblies plus missing, unreadable, escaped, contradictory, and mixed resource fixtures.
- Steps: assert exact required and forbidden loads and stop-before-dependent-work behavior.
- Expected result: untriggered resources do not load; every triggered incomplete resource blocks without reconstruction.
- Failure proves: progressive disclosure or package integrity is bypassable.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill and build validation plus scenario fixtures
- Required by milestone: M2

### T6. Specialized gates compose without becoming policy owners

- Covers: R18-R20, R22, R28; E6; EC5; BND-INPUT-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003
- Level: integration
- Command IDs: CMD3
- Fixture/setup: canonical gates reference and all predicate scenarios.
- Steps: verify detailed gate procedure, all combined outcomes, late activation, ambiguity stop, and absence of materiality, status, recording, or handoff redefinition.
- Expected result: the reference specializes gates only and loads once per invocation.
- Failure proves: policy ownership overlaps or a required gate can be omitted.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T7. Result and finding assets own structure only

- Covers: R24-R28; E7; EC7; BND-COMPOSE-001, BND-RECOVERY-001; INT-004
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: each group alone, every valid group composition, unavailable required data, and unfilled placeholder fixtures.
- Steps: validate labels and applicability outcomes and reject policy text, inapplicable groups, and unfilled placeholders.
- Expected result: core always appears; exact conditional groups appear or report blockers; material findings use one repeated asset.
- Failure proves: asset ownership is ambiguous or output can be incomplete.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused skill-validator assertions
- Required by milestone: M2

### T8. Preservation ledgers are complete and fail closed

- Covers: R29-R31, R34; EC8; BND-RECOVERY-001, BND-COMPAT-001; INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: valid rule and literal ledgers plus unknown disposition and classification fixtures.
- Steps: validate required fields, unique IDs, closed values, destinations, consumers, replacements, and unknown-first behavior.
- Expected result: valid ledgers pass and unknown values fail before consistency checks.
- Failure proves: rules can disappear or tests can become accidental policy owners.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: CMD1
- Required by milestone: M1

### T9. Static scenarios and measurements are deterministic and honest

- Covers: R5-R8, R14-R17, R19-R20, R23, R25-R26, R32-R34; EC1-EC3, EC5, EC7, EC9; BND-INPUT-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-004-INT-005
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: exactly twenty-five scenario records and canonical before and after assembly definitions.
- Steps: validate scenario identities and outcomes; normalize LF; count unique resources once; report every assembly and total package; reject runtime commands.
- Expected result: required negative behavior is explicit, PRR0 materially shrinks, total movement is honest, and percentages stay advisory.
- Failure proves: negative behavior or simplification evidence is incomplete or misleading.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/simplification-measurements.md`
- Automation location: CMD1, focused assertions, and repository-local measurement evidence
- Required by milestone: M1 and M3

### T10. Canonical and generated package validation uses existing owners

- Covers: R1, R4, R24, R34-R35; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: integration
- Command IDs: CMD2-CMD5
- Fixture/setup: changed canonical package and existing generated-skill tests.
- Steps: validate structure, mappings, containment, shared block, assets, placeholders, and generated inventory and parity.
- Expected result: complete valid package passes; missing, escaped, stale, or malformed resources fail.
- Failure proves: durable validators do not cover the new package.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: existing skill and build validation suites
- Required by milestone: M2 and M3

### T11. Archives and installed packages preserve every resource

- Covers: R1, R23, R34-R35, R37; E8; EC6; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: e2e
- Command IDs: CMD6, CMD7
- Fixture/setup: locally generated Codex, Claude Code, and opencode release candidates in a temporary directory.
- Steps: inspect archives and clean installations for both references and both assets at canonical paths and bytes; exercise missing and mixed failures.
- Expected result: every target is complete and byte-identical; incomplete targets fail.
- Failure proves: canonical acceptance does not survive distribution.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution and validation scripts
- Required by milestone: M3

### T12. Independent semantic review confirms behavior and ownership

- Covers: R1-R4, R9-R13, R18, R22, R24, R27-R31, R33-R34; EC8-EC9; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-002-INT-003, INT-005
- Level: manual
- Command IDs: none
- Fixture/setup: complete final package, governing specs, plan, test spec, ledgers, scenarios, baseline skill, and literal consumers.
- Steps: execute MP1.
- Expected result: every semantic rule has one correct owner and all judgment, authority, recording, claims, outputs, and handoffs remain intact.
- Failure proves: deterministic structure passed while meaning regressed.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: manual
- Required by milestone: M3

### T13. Architecture ordering, rollout, and rollback stay bounded

- Covers: R16, R36-R37; BND-STATE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: integration
- Command IDs: CMD6, CMD7, CMD9
- Fixture/setup: recorded assessment, complete current package, simulated incomplete package, and prior complete package identities.
- Steps: verify assessment predates plan, exercise reassessment triggers and mixed-package failure, prove the selected complete package, and restore a trusted complete prior package fixture.
- Expected result: no architecture work is invented, ambiguity routes upstream, and rollout and rollback are atomic.
- Failure proves: architecture applicability or package recovery is unsafe.
- Evidence artifact: `architecture-assessment.md`; `evidence/m3-package-proof.md`
- Automation location: metadata assertions and adapter rollback fixtures
- Required by milestone: M3

### T14. Current rules and literal consumers are fully inventoried

- Covers: R3-R4, R28-R31; EC8; BND-COMPAT-001; INT-005
- Level: manual
- Command IDs: CMD1
- Fixture/setup: full current `skills/proposal-review/` package and bounded scripts, tests, specs, fixtures, and package consumers.
- Steps: execute MP0 before prose movement and reconcile every source cluster and exact match to one ledger row.
- Expected result: no significant rule or consumer is omitted and every duplicate or obsolete treatment is justified.
- Failure proves: semantic preservation uses an incomplete baseline.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: manual audit supported by bounded `rg` searches and CMD1
- Required by milestone: M1

## Fixtures and data

- `proposal-review-rule-disposition.yaml`: JSON-compatible YAML with stable semantic rule records.
- `proposal-review-literal-compatibility.yaml`: JSON-compatible YAML with exact consumer records.
- `fixtures/scenario-contracts.yaml`: exactly twenty-five static scenario records with required and forbidden outcomes.
- `fixtures/invalid-rule-disposition.yaml`: one unknown semantic disposition.
- `fixtures/invalid-literal-classification.yaml`: one unknown literal classification.
- Existing skill, build, and adapter fixtures remain the durable package-proof owners.
- Temporary generated and installed trees use managed temporary directories and are never published.

## Mocking/stubbing policy

Do not mock an agent runtime because no agent runtime is part of acceptance.
Static records model contract inputs and expected outcomes; filesystem/package helpers may isolate temporary roots but must not bypass canonical parsing or byte comparison.

## Migration or compatibility tests

T8 proves literal-consumer migration, T11 proves distributed package compatibility, T13 proves complete-package rollback, and T12 proves semantic compatibility.
Historical review and change-local evidence remains readable and is not rewritten.

## Observability verification

Evidence identifies rule, literal, and scenario counts; assembly file lists and words and bytes; command IDs and results; package targets; resource paths and hashes; semantic-review conclusions; and blockers.
No new runtime logs, metrics, traces, or audit service is required.

## Security/privacy verification

Commands read repository files and use temporary local package roots only.
They must not access credentials, network services, hosted agents, publication endpoints, private data, or paths outside declared package roots.

## Performance checks

Measure loaded words and bytes for PRR0, PRR0G, PRR1, PRR1G, each resource, and total package.
Do not add timing, model-token, or runtime-latency gates; token estimates are optional only when an existing pinned implementation is available.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: semantic equivalence and normative-versus-incidental ownership cannot be established by exact-string checks alone.
- Required environment: tracked repository at the M1 baseline with the complete current proposal-review package and bounded consumers.
- Steps:
  1. Read the complete current package.
  2. Group every behaviorally significant rule and duplicate cluster by stable rule ID.
  3. Search scripts, tests, specs, fixtures, generated/package tests, and adapter validation for exact headings, fields, vocabulary, and phrases.
  4. Reconcile every rule and literal match to exactly one ledger row and validate closed values with CMD1.
- Evidence artifact: `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: every material rule and consumer has one justified treatment and canonical prose has not moved.
- Failure condition: any rule, consumer, owner, or classification is missing, duplicated, ambiguous, or unsupported.
- Owning stage: implement M1; required before M1 code-review.

### MP1. Final semantic preservation review

- Manual procedure ID: MP1
- Automation rationale: structural checks cannot determine whether relocated prose preserves proposal judgment and authority semantics.
- Required environment: complete final canonical package, ledgers, static scenarios, measurement evidence, and governing specs.
- Steps:
  1. Compare every semantic ledger row with its final destination and governing requirement.
  2. Review core advisory use without either reference.
  3. Review advisory durable, formal manual, formal automated, specialized-only, and combined assemblies.
  4. Confirm status, materiality, recording, settlement, isolation, claims, output applicability, and handoff behavior.
  5. Reconcile literal treatments and explain every total-package delta.
- Evidence artifact: `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: every rule has one correct owner, all valid assemblies are complete, no forbidden authority leaks, and no semantic rule disappears.
- Failure condition: any rule is absent, duplicated, hidden behind the wrong trigger, redefined by an asset, or broader or narrower than the approved contract.
- Owning stage: implement M3; required before M3 code-review and final review.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another model runtime; deterministic contract and package evidence is the accepted boundary.
- Do not grade prompts, transcripts, model versions, or prose style; those are neither product invariants nor stable acceptance evidence.
- Do not add permanent simplicity, token, line, word, semantic-classifier, or scenario-framework validators; measurements and scenarios are change-local.
- Do not retest formal-review-recording schema behavior beyond the proposal-review integration boundary; its owning spec and tests remain authoritative.
- Do not test publication or live registry operations; this change stops at local generated, archive, and installed package proof.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation M1 only after the test specification is approved and workflow separately authorizes implementation.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`.
This test specification does not authorize implementation, claim tests have run, or claim branch or PR readiness.
