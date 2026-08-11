# Verify Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-11-verify-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/verify-skill-simplification.md`
- Plan: `docs/plans/2026-08-11-verify-skill-simplification.md`
- Architecture/ADRs: architecture not required; assessment at `docs/changes/2026-08-11-verify-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/verify-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-11-verify-skill-simplification/reviews/spec-review-r1.md` |
| execution plan | `docs/plans/2026-08-11-verify-skill-simplification.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-11-verify-skill-simplification/reviews/plan-review-r2.md` |
| architecture assessment | `docs/changes/2026-08-11-verify-skill-simplification/architecture-assessment.md` | not applicable | `architecture-not-required`; no architecture artifact entry or review required |

## Testing strategy

Use contract-level static scenarios and fail-closed ledger checks before instruction movement, focused skill-validator integration proof during package refactoring, and generated/archive/temporary-installed package proof after refactoring.
Independent manual review proves semantic completeness and one-owner disposition where deterministic structure cannot judge meaning.

No end-to-end target-agent execution is permitted.
The relevant end-to-end boundary is the deterministic canonical-to-installed filesystem package chain, exercised by existing adapter tooling in temporary directories.
Migration proof classifies and migrates exact consumers without freezing incidental prose.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T4, T10, T11, T12 | contract, integration, manual | One complete `verify`-owned package. |
| R2 | T1, T3, T12 | contract, manual | Scoped path is self-sufficient. |
| R3 | T3, T12, T14 | contract, manual | Universal inline ownership is inventoried and reviewed. |
| R4 | T1, T9 | contract | Closed outcomes and fail-closed unknown/ambiguous requests. |
| R5 | T1, T3 | contract | Scoped target and claim vocabulary. |
| R6 | T1, T9 | contract | Exact repository, revision, and evidence identity. |
| R7 | T1, T2, T9 | contract | Governed-final requires current same-change authority. |
| R8 | T1, T5, T9 | contract | Missing, stale, contradictory, cross-target identity stops. |
| R9 | T1, T4, T9 | contract | Boolean evidence applicability without release authority. |
| R10 | T1, T2 | contract | Mode and profile are independent closed axes. |
| R11 | T2, T9, T12 | contract, manual | Isolated writes and PR behavior are forbidden. |
| R12 | T2, T4, T12 | contract, manual | Verify, workflow, and pr ownership remains separated. |
| R13 | T1, T5, T8 | contract | Exactly four deterministic profile assemblies. |
| R14 | T1, T4, T5 | contract | Exact final-reference load and owner. |
| R15 | T5, T10, T11 | integration | Boundary reference remains unchanged and additive. |
| R16 | T5, T9, T11 | contract, integration | Triggered resource failure stops without reconstruction. |
| R17 | T3, T9, T12 | contract, manual | Universal evidence states and source limits. |
| R18 | T4, T12 | contract, manual | Final applicability and aggregation owner. |
| R19 | T4, T12 | contract, manual | Conditional reference exclusions. |
| R20 | T3, T9 | contract | Supported scoped evidence classes need no final reference. |
| R21 | T3, T4, T12, T14 | contract, manual | Verification dimensions remain complete. |
| R22 | T2, T3, T12 | contract, manual | Branch-ready and forbidden claims remain bounded. |
| R23 | T6, T14 | contract, manual | Semantic ledger fields and complete inventory. |
| R24 | T6 | unit | Closed dispositions reject unknown/missing values first. |
| R25 | T7, T14 | contract, manual | Literal ledger fields and independent classification. |
| R26 | T7, T12, T14 | migration, manual | Real consumers migrate atomically; incidental prose may change. |
| R27 | T8 | contract | Deterministic LF-normalized words/bytes accounting. |
| R28 | T8, T12 | contract, manual | Advisory target and semantic acceptance gates. |
| R29 | T6-T12 | contract, integration, manual | Deterministic proof only; runtime and permanent machinery forbidden. |
| R30 | T10, T11 | integration | Existing owners prove canonical through installed parity. |
| R31 | T1-T5, T9, T12, T14 | contract, manual | Existing verification behavior and authority are preserved. |
| R32 | T13 | contract | Assessment precedes plan and ambiguity routes upstream. |
| R33 | T5, T11, T13 | integration, contract | Complete rollout and rollback; mixed package fails. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T3 | Scoped command result loads VP0 and stays bounded. |
| E2 | T3 | Individual evidence classes use inline semantics. |
| E3 | T1, T2 | Direct final readiness is isolated. |
| E4 | T1, T2, T4 | Governed-final uses current authority and owner-specific completion. |
| E5 | T1, T9 | Informal wording cannot create governed-final mode. |
| E6 | T1, T4, T9 | Release-sensitive evidence adds no release authority. |
| E7 | T5, T11 | Missing final reference blocks verdict and package proof. |
| E8 | T5 | Boundary reference is independently additive. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R4, R5, R6, R7, R8, R9 | BND-INPUT-001 | T1, T9 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R7, R8, R9, R10, R11, R12, R16, R32, R33 | BND-STATE-001 | T1, T2, T5, T13 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-refactor.md`; `architecture-assessment.md` | M2 | - | - |
| PRF-003 | covered | R6, R7, R8, R9, R10, R11, R12, R14, R18, R19, R22 | BND-AUTH-001 | T1, T2, T4, T12 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R3, R13, R14, R15, R16, R17, R18, R19, R20, R30, R31 | BND-COMPOSE-001 | T1, T3-T5, T10-T12 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-005 | covered | R7, R8, R16, R17, R33 | BND-TEMPORAL-001 | T1, T3, T5, T9, T13 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-006 | covered | R4, R8, R16, R24, R25, R26, R28, R29, R32, R33 | BND-RECOVERY-001 | T1, T5-T9, T13 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | R23, R24, R25, R26, R30, R31, R32, R33 | BND-COMPAT-001 | T6, T7, T11-T14 | integration | hybrid | CMD1, CMD3, CMD6, CMD7 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R16, R27, R29, R30, R33 | BND-ENV-001 | T5, T8-T11, T13 | integration | automated | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R4, R5, R6, R7, R8, R13, R14 | INT-001 | T1, T5, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R10, R11, R12, R18, R19 | INT-002 | T2, T4, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-011 | covered | R16, R17, R18, R19, R20 | INT-003 | T3-T5, T12 | contract | hybrid | CMD3 | `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-012 | covered | R7, R8, R16, R17 | INT-004 | T1, T3, T5, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-013 | covered | R23, R24, R25, R26, R27, R28, R31 | INT-005 | T6-T8, T12, T14 | contract | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-014 | covered | R29, R30, R33 | INT-006 | T9-T11, T13 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 multiple active changes | T1, T9 | stop before final-reference loading |
| EC2 informal direct final wording | T1, T9 | no governed-final classification |
| EC3 local-only CI evidence | T3, T9 | local claim only; no hosted-CI claim |
| EC4 generated source unknown | T3 | inconclusive/block, never current |
| EC5 incomplete manual proof | T3, T9 | insufficient evidence cannot support claim |
| EC6 installed adapter missing reference | T5, T11 | package and dependent verification fail |
| EC7 boundary-first scoped trigger | T5 | VP0B only, no branch reference |
| EC8 undecidable release sensitivity | T1, T4, T9 | final readiness stops |
| EC9 incidental exact-string test | T7, T14 | test migrates; semantics remain |
| EC10 common path shrinks through duplication | T8, T12 | semantic/ownership acceptance fails |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-verify-skill-simplification"); rules=json.loads((root/"verify-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"verify-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-branch-readiness-reference","retained-boundary-reference","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; dest=lambda row: (row["disposition"] == "retained-inline" and row["destination"].startswith("skills/verify/SKILL.md")) or (row["disposition"] == "retained-branch-readiness-reference" and row["destination"].startswith("skills/verify/references/branch-readiness-verification.md")) or (row["disposition"] == "retained-boundary-reference" and row["destination"].startswith("skills/verify/references/boundary-first-method-v1.md")) or (row["disposition"] == "removed-duplicate" and row["destination"].startswith("skills/verify/")) or (row["disposition"] == "removed-obsolete-with-approved-contract-change" and row["destination"].startswith(("specs/","docs/"))); vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else (["destination-inconsistent"] if not dest(row) else []))); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"scoped-command","scoped-ci","scoped-generated-output","scoped-manual-proof","scoped-release-metadata","direct-branch-readiness","governed-final-verification","ambiguous-target","cross-target-evidence","informal-final-wording","release-sensitive","missing-branch-reference","boundary-additive-scoped","boundary-additive-final","isolated-write-prohibition","governed-handoff","stale-evidence"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Block on unknown closed values first, then missing/empty fields, disposition-specific destination inconsistency, duplicate IDs, or incomplete scenarios. | Not applicable; every assertion must execute. | `docs/changes/2026-08-11-verify-skill-simplification/evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/verify/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block malformed structure, mapping, containment, placeholder, or claim contract. | Not applicable; deterministic validation. | `evidence/m2-package-refactor.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block any focused or regression failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated-skill inventory or resource test failure. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Temporary filesystem only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated package drift or missing resources. | Not applicable; deterministic check. | `evidence/m2-package-refactor.md` | Temporary generated tree; no tracked output writes. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD7 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "verify"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Stop on the first failed subprocess; block any generated, archive, or temporary installed target missing byte-identical resources. | Not applicable; direct package selection must produce all supported targets. | `evidence/m3-package-proof.md` | Uses immutable trusted fixture `v0.3.6`; Python owns and removes one fresh temporary directory; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/verify-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block missing or invalid proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only repository validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-11-verify-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every state-changing handoff | Block invalid artifact or planned-work state. | Not applicable; deterministic metadata validation. | owning change validation ledger | Read-only validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-verify-skill-simplification` | existing/configured | review stages | lifecycle | every formal review handoff | Block malformed or missing review evidence. | Not applicable; deterministic artifact validation. | review log and review records | Read-only validation. |

CMD1 is identical to the approved plan's M1 command and must be copied verbatim into execution evidence.
CMD7 intentionally uses a temporary directory and does not clean it through a destructive command; the operating environment may reclaim it after evidence capture.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T6, T7, T9, T14 | MP0 | CMD1, CMD9 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical package remains unchanged. |
| M2 | T1-T5, T9, T10 | none | CMD2, CMD3, CMD4, CMD5, CMD9 | `evidence/m2-package-refactor.md` | M2 code-review | Focused failing assertions precede package text changes. |
| M3 | T8-T13 | MP1 | CMD1, CMD2, CMD3, CMD4, CMD5, CMD6, CMD7, CMD8, CMD9, CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves profile, semantic, and package-chain acceptance. |

## Test cases

### T1. Requested outcomes, targets, profiles, and authority fail closed

- Covers: R4-R10, R13-R14, R31; E1, E3-E6; EC1-EC2, EC8; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-001, INT-004
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: static scenarios for every valid outcome/profile and missing, stale, contradictory, ambiguous, cross-target, and conversational-only authority.
- Steps: validate outcome, exact target, release flag, resource profile, and independently classified mode for every scenario.
- Expected result: valid cases select exactly one outcome/profile/mode; invalid cases stop before conditional loading or writes.
- Failure proves: classification or target identity could broaden a claim or leak procedure/authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: focused assertions in `scripts/test-skill-validator.py` plus scenario fixtures
- Required by milestone: M2

### T2. Isolated and governed-final completion preserve authority

- Covers: R10-R12, R22, R31; E3-E4; BND-STATE-001, BND-AUTH-001; INT-002
- Level: integration
- Command IDs: CMD3
- Fixture/setup: equivalent VP1 inputs under isolated and governed-final modes.
- Steps: assert permitted recording, forbidden state/routing writes, workflow handoff, and PR behavior for each mode.
- Expected result: isolated mode never progresses workflow or invokes/prepares PR; governed-final performs verify-owned recording only and returns progression to workflow.
- Failure proves: shared procedure has become shared authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T3. Universal evidence semantics support scoped checks

- Covers: R2-R3, R5, R17, R20-R22, R31; E1-E2; EC3-EC5; BND-COMPOSE-001, BND-TEMPORAL-001; INT-003-INT-004
- Level: integration
- Command IDs: CMD3
- Fixture/setup: scoped command, local/hosted CI, generated-output, manual-proof, and release-metadata scenarios across current, stale, failed, skipped, pending, not-run, unknown, and conflicting states.
- Steps: assert item semantics and claims are present inline and branch-readiness loading is forbidden.
- Expected result: each item receives a truthful scoped verdict and limitation without final aggregation.
- Failure proves: scoped verification is under-specified or overclaims evidence.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py` and scenario fixtures
- Required by milestone: M2

### T4. Branch-readiness reference owns aggregation only

- Covers: R1, R9, R12, R14, R18-R19, R21, R31; E4, E6; EC8; BND-AUTH-001, BND-COMPOSE-001; INT-002-INT-003
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: canonical branch reference plus positive and forbidden ownership assertions.
- Steps: verify exact load trigger, final prerequisite/applicability/aggregation procedure, mode-labeled completion, and absence of universal status/claim/workflow/PR policy redefinition.
- Expected result: one reference provides final procedure under `verify` ownership without becoming an authority owner.
- Failure proves: policy ownership overlaps or final procedure is incomplete.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T5. Resource loading and failures are exact

- Covers: R8, R13-R16, R31, R33; E7-E8; EC6-EC7; BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-003-INT-004
- Level: integration
- Command IDs: CMD1, CMD2, CMD3
- Fixture/setup: VP0, VP0B, VP1, VP1B and missing/unreadable/mixed resource fixtures.
- Steps: assert exact required/forbidden loads and stop-before-dependent-work behavior.
- Expected result: untriggered resources do not load; every triggered missing resource blocks without reconstruction.
- Failure proves: progressive disclosure is unsafe or package integrity can be bypassed.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: skill-validator tests and static scenarios
- Required by milestone: M2

### T6. Semantic-rule ledger is complete and fail-closed

- Covers: R23-R24, R29; BND-RECOVERY-001, BND-COMPAT-001; INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: valid ledger and invalid unknown-disposition fixture.
- Steps: validate required fields, unique IDs, source coverage, profile values, disposition vocabulary, destination, and preservation proof; evaluate unknown value first.
- Expected result: complete valid ledger passes and unknown/missing disposition fails before consistency.
- Failure proves: a rule can disappear or validation fails open.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: CMD1
- Required by milestone: M1

### T7. Literal compatibility is separate and safely migrated

- Covers: R25-R26, R29, R31; EC9; BND-RECOVERY-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: valid literal inventory, invalid classification fixture, and exact consumer search results.
- Steps: classify each consumer and verify normative preservation, atomic parser migration, incidental test updates, and obsolete evidence.
- Expected result: exact contracts remain or migrate atomically; tests alone do not own prose.
- Failure proves: incidental coupling freezes text or a real consumer breaks.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md`
- Automation location: CMD1 plus focused consumer assertions
- Required by milestone: M1 and M3

### T8. Profile and package measurements are deterministic and honest

- Covers: R13, R27-R29; EC10; BND-RECOVERY-001, BND-ENV-001; INT-005
- Level: unit
- Command IDs: CMD1
- Fixture/setup: canonical before/after files and documented profile assembly order.
- Steps: normalize LF, count unique files once, compute words/bytes for every resource/profile/package, and compare duplicate clusters.
- Expected result: VP0 materially shrinks, final/profile/package deltas are explicit, and percentage remains advisory.
- Failure proves: relocation or duplication is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: repository-local standard-library measurement recorded in evidence
- Required by milestone: M3

### T9. Static scenarios preserve negative behavior without a runtime

- Covers: R4-R9, R11, R16-R17, R20, R29, R31; E5-E6; EC1-EC3, EC5, EC8; BND-INPUT-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001, INT-004, INT-006
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: exactly seventeen scenario records with non-empty required and forbidden lists.
- Steps: validate every scenario identity and assert no command, fixture, or evidence field invokes or grades an agent runtime.
- Expected result: all required outcomes and stops are represented deterministically.
- Failure proves: negative behavior is unproved or acceptance expanded into runtime testing.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md`
- Automation location: CMD1 and focused skill assertions
- Required by milestone: M1 and M2

### T10. Canonical and generated package validation uses existing owners

- Covers: R1, R15, R29-R30; BND-COMPOSE-001, BND-ENV-001; INT-006
- Level: integration
- Command IDs: CMD2, CMD3, CMD4, CMD5
- Fixture/setup: changed canonical verify package and existing generated-skill tests.
- Steps: validate structure, both resource mappings, containment, reference identity, and generated inventory/parity.
- Expected result: complete valid package passes; missing, escaped, stale, or malformed resources fail.
- Failure proves: durable package validators do not cover the new reference.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: existing skill/build validation suites
- Required by milestone: M2 and M3

### T11. Archives and temporary installed packages preserve resources

- Covers: R1, R15-R16, R29-R30, R33; E7; EC6; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: e2e
- Command IDs: CMD6, CMD7
- Fixture/setup: locally generated Codex, Claude Code, and opencode release candidates in a temporary directory.
- Steps: inspect archives and clean installations for both mapped references at canonical relative paths and bytes; exercise missing/mixed failure fixtures.
- Expected result: every target is complete and byte-identical; incomplete targets fail.
- Failure proves: canonical acceptance does not survive distribution.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: adapter distribution and validation scripts
- Required by milestone: M3

### T12. Independent semantic review confirms behavior and ownership

- Covers: R1-R3, R11-R12, R17-R22, R26, R28-R29, R31; EC9-EC10; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-002-INT-003, INT-005
- Level: manual
- Command IDs: none
- Fixture/setup: complete final package, spec, plan, test spec, ledgers, scenarios, current baseline skill, and literal consumers.
- Steps: execute MP1.
- Expected result: every semantic rule has one correct owner; no universal policy is hidden; direct/governed authority, claims, recording, outputs, and handoffs remain intact.
- Failure proves: deterministic structure passed while meaning regressed.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: manual
- Required by milestone: M3

### T13. Architecture ordering, rollout, and rollback stay bounded

- Covers: R32-R33; BND-STATE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: integration
- Command IDs: CMD7, CMD9
- Fixture/setup: recorded assessment, complete current package, simulated incomplete package, and prior complete package identities.
- Steps: verify assessment predates plan; assert reassessment triggers; prove partial rollout fails and full prior revision restores valid parity.
- Expected result: no architecture work is invented, ambiguity routes upstream, and rollout/rollback are atomic.
- Failure proves: planning bypassed architecture applicability or package recovery is unsafe.
- Evidence artifact: `architecture-assessment.md`; `evidence/m3-package-proof.md`
- Automation location: metadata/package assertions
- Required by milestone: M3

### T14. Current rules and literal consumers are fully inventoried

- Covers: R3, R21, R23, R25-R26, R31; EC9; BND-COMPAT-001; INT-005
- Level: manual
- Command IDs: CMD1
- Fixture/setup: full current `skills/verify/SKILL.md`, mapped reference, scripts, tests, specs, fixtures, and adapter/package consumers.
- Steps: execute MP0 before prose movement and reconcile every source cluster and exact match to a ledger entry.
- Expected result: no significant rule or consumer is omitted and proposed duplicate/obsolete treatments are justified.
- Failure proves: later semantic preservation is based on an incomplete baseline.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: manual audit supported by bounded `rg` searches and CMD1
- Required by milestone: M1

## Fixtures and data

- `verify-rule-disposition.yaml`: JSON-compatible YAML with stable semantic rule records.
- `verify-literal-compatibility.yaml`: JSON-compatible YAML with exact consumer records.
- `fixtures/scenario-contracts.yaml`: exactly seventeen static scenario records with required and forbidden outcomes.
- `fixtures/invalid-rule-disposition.yaml`: one unknown semantic disposition.
- `fixtures/invalid-literal-classification.yaml`: one unknown literal classification.
- Existing skill, build, and adapter fixtures remain the durable package-proof owners.
- Temporary generated and installed trees use `mktemp -d` and are never published.

## Mocking/stubbing policy

Do not mock an agent runtime because no agent runtime is part of acceptance.
Static records model contract inputs and expected outcomes; existing filesystem/package helpers may isolate temporary roots but must not bypass canonical resource parsing or byte comparison.

## Migration or compatibility tests

T7 proves literal-consumer migration, T11 proves distributed package compatibility, T13 proves complete-package rollback, and T12 proves semantic compatibility.
Historical review and change-local evidence remains readable and is not rewritten.

## Observability verification

Evidence must identify rule/literal/scenario counts, profile file lists, words/bytes, command IDs and results, package targets, resource paths/hashes, semantic-review conclusions, and blockers.
No new runtime logs, metrics, traces, or audit service is required.

## Security/privacy verification

Commands read repository files and use temporary local package roots only.
They must not access credentials, network services, hosted agents, publication endpoints, private data, or paths outside declared package roots.

## Performance checks

Measure loaded words and bytes for VP0, VP0B, VP1, VP1B and total package.
Do not add timing, model-token, or runtime-latency gates; token estimates are optional only when an existing pinned repository implementation is available.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: semantic equivalence and normative-versus-incidental ownership cannot be established by exact-string checks alone.
- Required environment: tracked repository at the M1 baseline with current verify package and all bounded consumers available.
- Steps:
  1. Read the complete current `skills/verify/SKILL.md` and mapped boundary reference.
  2. Group every behaviorally significant rule and duplicate cluster by stable rule ID.
  3. Search scripts, tests, specs, fixtures, generated/package tests, and adapter validation for exact headings, fields, vocabulary, and phrases.
  4. Reconcile every rule and literal match to exactly one ledger row and validate closed values with CMD1.
- Evidence artifact: `docs/changes/2026-08-11-verify-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: every material rule and discovered consumer is accounted for with one justified treatment and no canonical prose has moved.
- Failure condition: any rule, consumer, owner, or classification is missing, duplicated, ambiguous, or unsupported.
- Owning stage: implement M1; required before M1 code-review.

### MP1. Semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: validators can prove structure and bytes but not completeness, procedure ownership, authority, or semantic equivalence.
- Required environment: final canonical package, both ledgers, scenario evidence, measurements, current spec/plan/test spec, and package proof.
- Steps:
  1. Compare every semantic ledger row with its final destination and preservation proof.
  2. Confirm inline completeness for scoped verification, item semantics, stops, claims, result, and handoff.
  3. Confirm the branch reference owns only final applicability, aggregation, closeout, and mode-labeled completion.
  4. Compare direct and governed authority, lifecycle/review closeout, CI/release safety, and PR boundaries with the baseline.
  5. Confirm literal consumers received their classified treatment and measurements did not hide duplication or loss.
- Evidence artifact: `docs/changes/2026-08-11-verify-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: every rule has one correct owner, every claim remains evidence-bound, every profile is usable, and no unapproved semantic change exists.
- Failure condition: any rule disappears, duplicates, moves behind an invalid trigger, changes authority, or lacks direct preservation evidence.
- Owning stage: implement M3; required before M3 code-review and final review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime; the product contract is packaged guidance and deterministic resources.
- Do not add prompt journeys, transcript snapshots, model selection, retry scoring, or runtime-version evidence.
- Do not make line, word, byte, token, or prose-quality measurements permanent product validators.
- Do not test unrelated skills, workflow stage order, state schema, CI/release policy, or PR opening behavior beyond preserved ownership assertions.
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
The proof map covers every requirement, example, edge case, boundary, interaction, milestone, command, fixture, failure path, and manual semantic judgment without target-agent execution.
