<!-- Template: test-spec-skeleton-v1 -->

# Plan-Review Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/plan-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-13-plan-review-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-13-plan-review-skill-simplification/architecture-assessment.md`; `ADR-20260623-published-skill-resource-integrity`; `ADR-20260813-reviewed-plan-initialization-and-settlement`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/plan-review-skill-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/spec-review-r2.md` |
| Execution plan | `docs/plans/2026-08-13-plan-review-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-13-plan-review-skill-simplification/reviews/plan-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-13-plan-review-skill-simplification/architecture-assessment.md` | `architecture-assessment` | `architecture-not-required` |

## Testing strategy

Use deterministic contract fixtures for operation classification, authority, state transitions, output applicability, resource loading, closed vocabularies, and package parity. Existing validators own permanent structural and distribution checks. Change-local ledgers and measurements prove semantic disposition and loaded-profile reduction, while MP0 and MP1 supply the human judgments that deterministic validation cannot make. No target-agent runtime, transcript grading, prompt journey, tokenizer dependency, network service, or publication action is part of acceptance.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R3 | T1, T2, T12 | contract | Package ownership, portable completeness, and formal recording. |
| R4-R10 | T3-T7 | contract | Exhaustive initial-review and retry state machine. |
| R11-R17 | T2, T3, T8 | contract | Candidate loading remains distinct from validated authority. |
| R18-R25 | T2, T4, T8, T9 | contract | Judgment, transaction, non-clean, and blocked-recording behavior. |
| R26-R32 | T5-T7 | contract | Pending, matching, active, invalid, concurrent, and interrupted retries. |
| R33-R41 | T1, T8, T10 | integration | Four profiles, exact conditional loading, resource failure, and boundary identity. |
| R42-R47 | T9, T11 | contract | Result groups, omission rules, placeholders, and finding compatibility. |
| R48-R50 | T12, T13 | contract | Separate fail-closed semantic and literal inventories. |
| R51-R53 | T14, T16 | integration | Deterministic measurement and bounded acceptance. |
| R54 | T15 | integration | Canonical-through-installed resource parity and atomic rollback. |
| R55 | T16 | contract | Bounded architecture assessment and escalation rule. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T2 | Portable review remains complete without governed procedure. |
| E2 | T3, T8 | Invalid governed candidates stop without fallback. |
| E3 | T4 | Clean initial review records once and waits for initialization. |
| E4 | T5 | Pending retry reuses judgment without duplicate evidence. |
| E5 | T6 | Matching retry activates only the exact entry. |
| E6 | T6, T7 | Already-active and interrupted retries reconcile idempotently. |
| E7 | T7, T9 | Invalid retry blocks without manufacturing judgment. |
| E8 | T4 | Non-clean statuses have distinct durable effects. |
| E9 | T8, T10 | Required-resource failure stops dependent work. |
| E10 | T12-T16 | Ledgers, profiles, semantics, and package parity all gate acceptance. |

## Proof map

Boundary model version: boundary-first-v1

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R4, R11, R13, R16, R18, R19 | BND-INPUT-001 | T2, T3, T9, T13 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R4-R10, R20-R32 | BND-STATE-001 | T3-T7 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-003 | covered | R5, R7, R8, R10-R17, R27-R30, R39 | BND-AUTH-001 | T2, T3, T6-T8 | contract | hybrid | CMD1, CMD3 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | R1, R2, R12, R33-R47 | BND-COMPOSE-001 | T1, T8-T11, T15 | integration | hybrid | CMD2-CMD8 | `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md` | M3 | MP1 | - |
| PRF-005 | covered | R4-R10, R26-R32 | BND-TEMPORAL-001 | T4-T7 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-006 | covered | R10, R13, R24, R25, R29, R30, R32, R35, R36, R44, R45, R49, R50, R52-R55 | BND-RECOVERY-001 | T7-T10, T12-T16 | contract | hybrid | CMD1-CMD10 | `evidence/m3-package-proof.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-007 | covered | R18, R19, R31, R40, R47-R55 | BND-COMPAT-001 | T6, T10-T16 | integration | hybrid | CMD1, CMD3-CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | R36, R51, R53, R54 | BND-ENV-001 | T8, T14-T16 | integration | automated | CMD2-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R4, R5, R7, R11-R15 | INT-001 | T3, T5, T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R7, R8, R21, R26 | INT-002 | T5 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-011 | covered | R27, R28, R30-R32 | INT-003 | T6, T7 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-012 | covered | R29, R42-R45 | INT-004 | T7, T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-013 | covered | R33-R41 | INT-005 | T1, T8, T10 | contract | hybrid | CMD2-CMD5 | `evidence/m2-package-refactor.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-014 | covered | R48-R53 | INT-006 | T12-T14, T16 | contract | hybrid | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-015 | covered | R47, R54 | INT-007 | T11, T15 | integration | automated | CMD4-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| Unknown operation, mode, status, transaction, disposition, or classification | T3, T9, T12, T13 | Fail closed before consistency logic or writes. |
| Candidate points to a missing, stale, or mismatched entry | T3, T8 | Load the governed procedure, then stop without portable fallback. |
| Clean review exists while initialization is absent | T5 | Reuse one exact judgment and return `initialization-required`. |
| Initialization exists without a valid clean review | T7 | Block as contradictory state. |
| Multiple clean reviews or initialization bases exist | T7 | Block as ambiguous before mutation. |
| Matching entry is already active | T6 | Return idempotent success with no write. |
| Interruption follows compare-and-set | T7 | Reconcile exact active identity without rereview or duplicate evidence. |
| Required conditional resource is missing or mixed-version | T8, T10, T15 | Stop dependent behavior and never reconstruct from memory. |
| Invalid retry cannot safely resolve prior judgment | T9 | Omit judgment group and report blocked transaction. |
| Main file shrinks while a loaded profile grows | T14 | Acceptance fails despite main-file reduction. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-13-plan-review-skill-simplification"); rules=json.loads((root/"plan-review-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"plan-review-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-governed-reference","retained-boundary-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete","historical-fixture"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_profiles","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; vr=lambda row: ["unknown-disposition"] if row.get("disposition") not in rd else (["missing-required-fields"] if not rf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in rf) else [])); vl=lambda row: ["unknown-classification"] if row.get("classification") not in lc else (["missing-required-fields"] if not lf <= row.keys() else (["empty-required-fields"] if not all(row[field] for field in lf) else [])); expected={"portable-clean","portable-material","blocked-recording","governed-candidate-invalid","governed-initial-clean","governed-changes-requested","governed-blocked","governed-inconclusive","retry-initialization-absent","retry-matching","retry-already-active","retry-stale-plan","retry-duplicate-review","retry-mismatched-basis","retry-open-resolution","planned-work-without-clean-review","interrupted-settlement","boundary-portable","boundary-governed","missing-resource","asset-judgment-omitted","workflow-managed","invalid-vocabulary"}; assert rules and literals; assert all(vr(row) == [] for row in rules); assert all(vl(row) == [] for row in literals); assert vr(bad_rule)[0] == "unknown-disposition"; assert vl(bad_literal)[0] == "unknown-classification"; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected-first")'` | planned-for-implementation | implement | M1 | M1 code-review | Reject unknown values first, then incomplete ledgers, duplicate IDs, or scenario drift. | Not applicable; every assertion executes. | `evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/plan-review/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block skill structure, mapping, containment, placeholder, or claim defects. | Not applicable; deterministic validation. | `evidence/m2-package-refactor.md` | Read-only repository validation. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block focused or regression failures. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Repository-local tests; no target-agent runtime. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource regressions. | Zero discovered tests is failure. | `evidence/m2-package-refactor.md` | Temporary filesystem only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-package drift or missing resources. | Not applicable. | `evidence/m2-package-refactor.md` | Read-only check against canonical sources. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block adapter generation, archive, install, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication or network. |
| CMD7 | `plan_review_adapter_tmp="$(mktemp -d)"; trap 'rm -rf "$plan_review_adapter_tmp"' EXIT; python scripts/build-adapters.py --version v0.1.5 --output-dir "$plan_review_adapter_tmp"; python scripts/validate-adapters.py --version v0.1.5 --adapter-root "$plan_review_adapter_tmp" --clean-install-smoke --skill plan-review` | existing/configured | implement | M3 | M3 code-review | Block generation or any archive/installed resource mismatch. | Not applicable; all supported targets are selected. | `evidence/m3-package-proof.md` | One fresh temporary directory is removed; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/plan-review-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block invalid or missing proof for any boundary or interaction. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only repository validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-13-plan-review-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | Every state-changing handoff | Block invalid artifact, review, or planned-work state. | Not applicable. | Owning change validation ledger | Read-only validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-13-plan-review-skill-simplification` | existing/configured | review stages | lifecycle | Every formal review handoff | Block malformed or missing review evidence. | Not applicable. | Review log and records | Read-only validation. |

CMD1 is the approved plan's standard-library proof serialized as one shell command without semantic change. CMD7 is the approved temporary adapter proof serialized as one shell command with the same version, cleanup, build, validation, and skill-selection arguments.

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T12-T14 | MP0 | CMD1, CMD9 | `evidence/profile-size-baseline.md`; `evidence/m1-preservation-inventories.md` | M1 code-review | Canonical skill prose remains unchanged while ownership is frozen. |
| M2 | T1-T11 | none | CMD2-CMD5, CMD8-CMD10 | `evidence/m2-package-refactor.md` | M2 code-review | Focused failing assertions precede the atomic package refactor. |
| M3 | T10-T16 | MP1 | CMD1-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final review | Proves boundary, profile, semantics, and package-chain acceptance. |

## Test cases

### T1. Procedural profiles load exact resources once

- Covers: R1, R2, R33-R36; E1, E9; BND-COMPOSE-001; INT-005
- Level: contract
- Command IDs: CMD2-CMD5
- Fixture/setup: Static fixtures for all four profiles, late discovery, missing resources, and mixed versions.
- Steps: Assemble each profile in documented order, then exercise required, forbidden, late, missing, and duplicate loads.
- Expected result: Each profile loads only its exact unique resources, late discovery precedes dependent work, and required-resource failure stops safely.
- Failure proves: Progressive disclosure is incomplete, duplicated, or unsafe.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Existing skill validator tests.
- Required by milestone: M2

### T2. Portable formal review remains complete and isolated

- Covers: R2, R3, R16-R20, R37; E1; BND-INPUT-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD2, CMD3
- Fixture/setup: Portable clean and material formal-review fixtures with no governed candidate.
- Steps: Perform judgment, required recording, result construction, and handoff classification using only the portable profile.
- Expected result: Review evidence is recorded or blocked, transaction is `recorded-isolated` or `not-settled`, and no governed eligibility or mutation is claimed.
- Failure proves: Universal behavior was hidden behind governed procedure.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Existing skill validator tests.
- Required by milestone: M2

### T3. Operation and candidate authority fail closed

- Covers: R4, R5, R9-R17; E2; BND-INPUT-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Valid, stale, mismatched, ambiguous, unknown-vocabulary, and changed-plan candidate fixtures.
- Steps: Classify operation and candidate, load governed procedure when indicated, and validate exact authority before judgment or writes.
- Expected result: Only exact supported state proceeds; invalid candidates stop without mutation or portable fallback, and changed identity requires fresh review.
- Failure proves: Loading or wording can manufacture authority or reuse stale judgment.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Static scenarios and existing validator tests.
- Required by milestone: M2

### T4. Initial review records one deterministic result

- Covers: R5, R6, R18-R25; E3, E8; BND-STATE-001, BND-TEMPORAL-001
- Level: contract
- Command IDs: CMD1, CMD3, CMD10
- Fixture/setup: Portable and governed initial-review fixtures for every review status and a blocked-recording case.
- Steps: Perform semantic review, record evidence, and apply the status-specific transaction mapping.
- Expected result: One review occurrence is created; clean, changes-requested, blocked, inconclusive, and recording failure produce their exact distinct outcomes.
- Failure proves: Judgment, recording, or lifecycle settlement is conflated.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Static scenarios and review-artifact tests.
- Required by milestone: M2

### T5. Pending initialization reuses one clean judgment

- Covers: R7, R8, R21, R26; E4; BND-STATE-001, BND-TEMPORAL-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: One exact clean review, `review-required` entry, and absent `planned_work`.
- Steps: Invoke plan-review repeatedly for the unchanged tuple.
- Expected result: Every later invocation is a retry, returns `initialization-required`, and creates no duplicate evidence.
- Failure proves: Pending initialization can cause semantic rereview or duplicate records.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Static lifecycle fixture.
- Required by milestone: M2

### T6. Matching and active retries settle idempotently

- Covers: R27, R28, R30, R31; E5, E6; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-003
- Level: contract
- Command IDs: CMD1, CMD3, CMD9
- Fixture/setup: Matching clean-review and initialization bases with entry states `review-required` and `active`.
- Steps: Execute settlement once, then replay the exact retry.
- Expected result: Only the exact entry becomes active once, replay reports `state_changed: false`, and all basis evidence remains.
- Failure proves: Settlement is non-idempotent, over-broad, or deletes traceability.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Static lifecycle fixture.
- Required by milestone: M2

### T7. Invalid and interrupted retries preserve state

- Covers: R10, R29-R32; E6, E7; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003, INT-004
- Level: contract
- Command IDs: CMD1, CMD3, CMD9
- Fixture/setup: Duplicate reviews, conflicting bases, open resolution, planned work without clean review, pre-write failure, post-write interruption, and concurrent update.
- Steps: Attempt settlement and recovery for each fixture.
- Expected result: Invalid states block before mutation; post-write interruption reconciles exact active state without rereview or duplicates.
- Failure proves: Retry safety or recovery is incomplete.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Static lifecycle fixture.
- Required by milestone: M2

### T8. Governed reference has a bounded write set

- Covers: R11-R17, R35-R39; E2, E9; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-001, INT-005
- Level: contract
- Command IDs: CMD2, CMD3
- Fixture/setup: Candidate, validated, invalid, manual, managed, missing-resource, and forbidden-write fixtures.
- Steps: Inspect reference ownership and exercise each authority boundary.
- Expected result: The reference validates and settles only its owned exact entry and never initializes planned work, routes workflow, edits plan content, or grants automation.
- Failure proves: Conditional procedure broadens lifecycle authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Existing validator tests and static scenarios.
- Required by milestone: M2

### T9. Result groups distinguish judgment from transaction

- Covers: R18, R19, R42-R46; E7, E8; BND-INPUT-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-004
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Performed judgment, reused judgment, invalid retry with and without resolvable prior judgment, blocked data, and every conditional group.
- Steps: Render each applicable result structure and scan for forbidden groups and placeholders.
- Expected result: Core and recording groups always appear, judgment appears only when performed or safely reused, and blocked data is explicit.
- Failure proves: Output manufactures semantic status or assets become policy owners.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Existing review-family fixture tests.
- Required by milestone: M2

### T10. Boundary activation and identity remain unchanged

- Covers: R40, R41; E9; BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: contract
- Command IDs: CMD2-CMD5, CMD8
- Fixture/setup: Current, stale, missing, ambiguous, conflicting, and sufficient approved boundary evidence.
- Steps: Validate exact trigger behavior, reference path, version, identifier grammar, and generated parity.
- Expected result: Existing activation loads the byte-consistent reference only when required and never creates a competing boundary policy.
- Failure proves: Simplification changed shared boundary ownership or activation.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Boundary and build validators.
- Required by milestone: M3

### T11. Review assets remain structural and compatible

- Covers: R42-R47; BND-COMPOSE-001, BND-COMPAT-001; INT-007
- Level: contract
- Command IDs: CMD3-CMD5
- Fixture/setup: All result groups, missing data, no-material result, and material finding fixtures.
- Steps: Validate labels, group omission, explicit blockers, placeholders, policy absence, and finding bytes.
- Expected result: Assets own only structure, and the finding block remains byte-identical to the parser-owned review-family contract.
- Failure proves: Structural extraction changed policy or parser compatibility.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: Existing skill and build tests.
- Required by milestone: M2

### T12. Semantic rule dispositions are complete and fail closed

- Covers: R48, R49, R52, R53; E10; BND-RECOVERY-001, BND-COMPAT-001; INT-006
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Complete rule ledger plus unknown, missing, duplicate, and empty-field fixtures.
- Steps: Run closed-vocabulary validation before consistency checks and reconcile rows against the current package.
- Expected result: Every significant rule has one valid destination and unknown dispositions fail first.
- Failure proves: Simplification can silently delete, duplicate, or misplace behavior.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: Change-local standard-library proof.
- Required by milestone: M1

### T13. Literal dependencies remain separate from semantic rules

- Covers: R50, R53; BND-INPUT-001, BND-COMPAT-001; INT-006
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Complete literal inventory and unknown-classification fixture with real consumer searches.
- Steps: Classify every exact dependency and prove contract literals are preserved or migrated while incidental tests do not own prose.
- Expected result: Every literal has one closed treatment and unknown classification fails before consistency checks.
- Failure proves: Accidental wording coupling blocks valid simplification or breaks a real consumer.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: Change-local proof plus MP0.
- Required by milestone: M1

### T14. Profile accounting is deterministic and honest

- Covers: R51-R53; E10; BND-COMPAT-001, BND-ENV-001; INT-006
- Level: integration
- Command IDs: CMD1, CMD3
- Fixture/setup: Baseline and final LF-normalized canonical resources with all four profile assemblies and both assets.
- Steps: Count each unique procedural resource once in documented order and compare words, bytes, duplicate owners, assets, and total package.
- Expected result: Portable and governed profiles both shrink, unexplained growth fails, and no fixed percentage overrides preservation.
- Failure proves: Relocation or selective metrics are misrepresented as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: Change-local measurement proof.
- Required by milestone: M3

### T15. Package-chain resources retain exact parity

- Covers: R1, R47, R54; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-007
- Level: integration
- Command IDs: CMD4-CMD7
- Fixture/setup: Canonical, generated, packed, archived, and clean-installed package targets, including missing and transformed resource fixtures.
- Steps: Build temporary targets, select plan-review directly, and compare required paths and raw bytes.
- Expected result: Every target contains both references and both assets exactly; partial rollout and drift fail.
- Failure proves: Release packaging can omit or alter the new package resources.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing build and adapter tests plus temporary proof.
- Required by milestone: M3

### T16. Acceptance and architecture remain bounded

- Covers: R52-R55; E10; BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-006
- Level: contract
- Command IDs: CMD1-CMD10
- Fixture/setup: Final package, all evidence, architecture assessment, and fixtures that propose a new runtime, package model, or state owner.
- Steps: Review acceptance commands and architecture triggers, then compare final package semantics with the ledgers and approved contract.
- Expected result: Existing architecture remains sufficient unless its stated triggers occur, no target runtime or permanent simplicity machinery is added, and semantic review approves.
- Failure proves: The refactor exceeded its accepted architecture or proof boundary.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: Deterministic checks plus MP1.
- Required by milestone: M3

## Fixtures and data

M1 creates JSON-compatible YAML ledgers and static scenario records under the owning change root. Scenario fixtures cover portable clean and material reviews, recording failure, governed candidate validation, every semantic status, absent/matching/invalid initialization, pending/matching/already-active/stale/ambiguous/interrupted retries, boundary variants, output omission, workflow-managed authority, missing resources, and unknown vocabulary. Existing repository fixtures remain the owners of skill parsing, review-family structure, build output, and adapter packaging.

## Mocking/stubbing policy

Use static filesystem fixtures and temporary package directories only. Do not mock an agent runtime or infer semantic behavior from generated transcripts. Lifecycle fixtures must provide explicit identities and state rather than caller-asserted authority.

## Migration or compatibility tests

T10, T11, T13, and T15 prove unchanged boundary identity, byte-identical finding structure, classified literal migration, and canonical-through-installed resource parity. Rollback restores the prior complete package and directly coupled consumers atomically; mixed versions are invalid.

## Observability verification

Change-local evidence records profile inputs and identities, command results, rule and literal treatments, semantic-review conclusions, and package paths. No production logs, metrics, or traces are introduced.

## Security/privacy verification

All proof is repository-local. Temporary package roots are deleted, network access and publication are excluded, and fixtures contain no secrets or personal data.

## Performance checks

Loaded-profile UTF-8 bytes and Unicode whitespace-separated words are the only required performance proxies. Token estimates and runtime benchmarks are out of scope.

## Manual QA checklist

### MP0. Pre-movement semantic and literal inventory audit

- Manual procedure ID: MP0
- Automation rationale: Exact-string checks cannot decide semantic equivalence or normative ownership.
- Required environment: Tracked M1 baseline with the complete current plan-review package and bounded consumers.
- Steps: Read the full package, group every significant rule and duplicate cluster, search all consumers for exact dependencies, and reconcile every item to one valid ledger row before prose moves.
- Evidence artifact: `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/m1-preservation-inventories.md`
- Pass condition: Every rule, duplicate, literal, source, consumer, and intended owner has one supported treatment.
- Failure condition: Any material rule or consumer is missing, duplicated, ambiguous, or unsupported.
- Owning stage: Implement M1 before M1 code-review.

### MP1. Final semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: Validators cannot establish completeness of judgment, authority, recording, transaction, or claim semantics.
- Required environment: Final package, ledgers, scenarios, measurements, approved artifacts, and package proof.
- Steps: Compare every rule with its destination; confirm portable completeness; validate candidate, initial-review, retry, evidence-retention, output, boundary, automation, failure, claim, and handoff behavior; and verify literal treatments and measurements.
- Evidence artifact: `docs/changes/2026-08-13-plan-review-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: Every rule has one correct owner, every profile remains usable, every write is authorized, and no unapproved semantic change exists.
- Failure condition: Any rule disappears, duplicates, loads behind the wrong trigger, broadens authority, or lacks direct evidence.
- Owning stage: Implement M3 before M3 code-review and final review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime because this change refactors published guidance and deterministic resources.
- Do not add prompt journeys, transcript snapshots, runtime-version evidence, tokenizer dependencies, or permanent size and prose validators.
- Do not test unrelated skills, redesign workflow stages, mutate planned-work ownership, publish adapters, or open a pull request.
- Do not infer semantic boundary truth with deterministic validators; they validate the approved record shape and exact IDs only.

## Uncovered gaps

None.

## Next artifacts

- Independent formal `test-spec-review`.
- Implementation M1 only after review approval and subsequent workflow routing.

## Follow-on artifacts

None yet

## Readiness

Active proof map ready for formal `test-spec-review`. This artifact does not claim implemented tests, validation success, implementation eligibility, verification, branch readiness, or PR readiness.
