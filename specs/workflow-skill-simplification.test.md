# Workflow Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/workflow-skill-simplification.md`
- Plan: `docs/plans/2026-08-11-workflow-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/workflow-skill-simplification.md` | spec | `spec-review-r2`; `docs/changes/2026-08-11-workflow-skill-simplification/reviews/spec-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | architecture | `architecture-review-r2`; `docs/changes/2026-08-11-workflow-skill-simplification/reviews/architecture-review-r2.md` |
| Execution plan | `docs/plans/2026-08-11-workflow-skill-simplification.md` | plan | `plan-review-r1`; `docs/changes/2026-08-11-workflow-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Contract and unit-level static tests in `scripts/test-skill-validator.py` prove exact assembly classification, resource triggers, ownership boundaries, bootstrap order, stateless commands, universal semantics, and forbidden runtime machinery. Change-local JSON-compatible YAML fixtures prove semantic and literal inventory contracts plus representative outcomes without executing a target agent.

Integration and end-to-end tests use existing skill-build and adapter-distribution owners to prove canonical-to-generated, archive, and temporary installed-tree resource identity. The selected clean-install check is the smoke layer. Two bounded manual procedures prove complete baseline inventory and final semantic preservation because structural checks cannot establish either conclusion. Migration proof classifies exact-string consumers and requires real parser/package contracts to migrate atomically; incidental tests may change with prose.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T2, T5, T10 | contract | One workflow-owned package across all targets. |
| R2 | T2, T12 | unit, manual | Universal contract stays inline and semantically complete. |
| R3 | T2, T10, T11 | integration | Exact mappings and package resources. |
| R4 | T1 | unit | Four predicates only. |
| R5 | T1 | unit | Seven valid assemblies and explicit invalid results. |
| R6 | T3 | unit | Command context never implies armed authority. |
| R7 | T3 | unit | Bootstrap order is exact. |
| R8 | T3, T7 | unit | Bootstrap is transient and stops before unsafe persistence. |
| R9 | T4, T7 | unit | Invalid automation/guide and missing-governed states stop. |
| R10 | T1, T6 | unit | Governed reads load governed procedure without mutation authority. |
| R11 | T5, T12 | contract, manual | Governed lifecycle owns applicability and transitions. |
| R12 | T5, T12 | contract, manual | Automation is subordinate to governed transitions. |
| R13 | T5, T12 | contract, manual | Guide authoring renders but does not own policy. |
| R14 | T5 | unit | Skeleton remains structural only. |
| R15 | T5, T7 | unit | Contradiction stops without precedence guessing. |
| R16 | T7, T10 | integration | Required resources are checked before use. |
| R17 | T7, T11 | integration | Mixed or missing procedure cannot be reconstructed. |
| R18 | T1, T2 | unit | False triggers remain unloaded. |
| R19 | T6 | unit | Stateless and current-run status/off paths differ correctly. |
| R20 | T4 | unit | Stale or mismatched identities stop without mutation. |
| R21 | T8, T12 | manual | Complete semantic-rule ledger. |
| R22 | T8 | unit | Closed dispositions fail before consistency checks. |
| R23 | T8, T9 | migration | Separate literal ledger. |
| R24 | T8, T9 | migration | Closed classifications and atomic real-contract migration. |
| R25 | T2, T10, T11 | integration | Existing permanent validation owners remain authoritative. |
| R26 | T13 | unit | Deterministic LF-normalized assembly accounting. |
| R27 | T13, T14 | manual | Material WP0 improvement and honest total package evidence. |
| R28 | T1-T7, T10-T12 | contract | Deterministic scenarios and semantic review cover required outcomes. |
| R29 | T10, T11, T15 | integration | Acceptance never executes or grades a target agent. |
| R30 | T12, T14 | manual | Lifecycle and state semantics remain unchanged. |
| R31 | T14 | contract | Architecture assessment and reviewed update precede planning. |
| R32 | T11, T14 | integration | Atomic rollout and complete-package rollback. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T2 | WP0 loads common path only. |
| E2 | T6 | Read-only governed audit loads governed procedure. |
| E3 | T3 | Bootstrap validates and reclassifies before persistence. |
| E4 | T3 | Conversation alone creates no automation authority. |
| E5 | T4 | Active automation plus guide authoring stops. |
| E6 | T7 | Unreadable governed reference stops before interpretation. |
| E7 | T5 | Automation consumes governed transition decisions. |
| E8 | T9 | Incidental test wording is migrated, not preserved as policy. |
| E9 | T6 | Stateless status returns `no-active-run` and creates no state. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1-EC2 | T2, T6, T12 | Universal rule remains inline; governed read remains read-only. |
| EC3-EC5 | T3, T4, T6 | Stateless, failed bootstrap, and mismatched identity paths stop or return exactly as specified. |
| EC6 | T1 | WP4 loads governed and guide resources without automation. |
| EC7-EC8 | T7 | Unreadable and contradictory resources fail closed. |
| EC9 | T9 | Mixed parser/test consumers use parser-or-package treatment. |
| EC10 | T13 | Assembly and total-package deltas are reported and justified. |
| EC11 | T14 | Canonical architecture update is owned and reviewed without an unnecessary ADR. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R4, R5, R19, R22, R24, R28 | BND-INPUT-001 | T1, T6, T8 | unit | automated | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-002 | covered | R6, R7, R8, R9, R10, R11, R19, R20, R30, R31 | BND-STATE-001 | T3, T4, T6, T12, T14 | contract | hybrid | CMD1, CMD8 | `evidence/semantic-preservation-review.md`; `architecture-assessment.md` | M3 | MP2 | - |
| PRF-003 | covered | R1, R2, R6, R7, R9, R11, R12, R13, R20, R24, R30 | BND-AUTH-001 | T3, T4, T5, T9, T12 | contract | hybrid | CMD1 | `evidence/semantic-preservation-review.md` | M3 | MP2 | - |
| PRF-004 | covered | R1, R2, R3, R5, R10, R12, R13, R14, R15, R18 | BND-COMPOSE-001 | T1, T2, T5, T7, T10 | integration | automated | CMD2, CMD3, CMD4, CMD5 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-005 | covered | R7, R8, R9, R19, R20, R28, R30, R32 | BND-TEMPORAL-001 | T3, T4, T6, T14 | contract | hybrid | CMD1 | `evidence/semantic-preservation-review.md` | M3 | MP2 | - |
| PRF-006 | covered | R8, R9, R15, R16, R17, R20, R22, R24, R27, R31, R32 | BND-RECOVERY-001 | T4, T7, T8, T13, T14 | contract | hybrid | CMD1, CMD8 | `evidence/semantic-preservation-review.md` | M3 | MP2 | - |
| PRF-007 | covered | R24, R25, R30, R31, R32 | BND-COMPAT-001 | T9, T10, T11, T12, T14 | integration | hybrid | CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 | MP2 | - |
| PRF-008 | covered | R16, R17, R25, R26, R28, R29, R32 | BND-ENV-001 | T7, T10, T11, T13, T15 | smoke | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R6, R7, R8, R20 | INT-001 | T3, T4 | unit | automated | CMD1 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-010 | covered | R5, R9, R13 | INT-002 | T4 | unit | automated | CMD1 | `evidence/m2-package-refactor.md` | M2 | - | - |
| PRF-011 | covered | R10, R11, R12, R15 | INT-003 | T5, T7, T12 | contract | hybrid | CMD1 | `evidence/semantic-preservation-review.md` | M3 | MP2 | - |
| PRF-012 | covered | R16, R17, R18 | INT-004 | T7, T10, T11 | integration | automated | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-013 | covered | R21, R22, R23, R24 | INT-005 | T8, T9, T12 | manual | hybrid | CMD1 | `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md` | M3 | MP1, MP2 | - |
| PRF-014 | covered | R25, R26, R27, R29 | INT-006 | T10, T11, T13, T15 | integration | hybrid | CMD2, CMD3, CMD4, CMD5, CMD6, CMD7 | `evidence/simplification-measurements.md`; `evidence/m3-package-proof.md` | M3 | MP2 | - |
| PRF-015 | covered | R30, R31, R32 | INT-007 | T12, T14 | contract | hybrid | CMD8, CMD9 | `architecture-assessment.md`; `evidence/semantic-preservation-review.md` | M3 | MP2 | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python -c 'import json; from pathlib import Path; root=Path("docs/changes/2026-08-11-workflow-skill-simplification"); rules=json.loads((root/"workflow-rule-disposition.yaml").read_text())["rules"]; literals=json.loads((root/"workflow-literal-compatibility.yaml").read_text())["literals"]; scenarios=json.loads((root/"fixtures/scenario-contracts.yaml").read_text())["scenarios"]; bad_rule=json.loads((root/"fixtures/invalid-rule-disposition.yaml").read_text()); bad_literal=json.loads((root/"fixtures/invalid-literal-classification.yaml").read_text()); rd={"retained-inline","retained-governed-reference","retained-automation-reference","retained-guide-reference","asset-owned","removed-duplicate","removed-obsolete-with-approved-contract-change"}; lc={"normative-contract","parser-or-package-contract","test-only-incidental","obsolete"}; rf={"rule_id","source_locations","behavior","governing_requirements","applicable_assemblies","disposition","destination","preservation_proof"}; lf={"literal_id","literal","source_location","consumers","classification","required_semantics","disposition","replacement"}; expected={"wp0-generic-routing","wp1-governed","wp2-governed-automated","wp3-guide-authoring","wp4-governed-guide-authoring","wpb-automation-bootstrap","wps-stateless-automation-command","conversation-not-armed","active-automation-guide-stop","active-without-governed-stop","stale-or-mismatched-authority","missing-or-unreadable-resource","contradictory-or-mixed-resource","governed-read-only","milestone-and-review-routing","final-holistic-review"}; assert rules and literals; assert all(rf <= row.keys() for row in rules); assert all(lf <= row.keys() for row in literals); assert not [row.get("disposition") for row in rules if row.get("disposition") not in rd]; assert not [row.get("classification") for row in literals if row.get("classification") not in lc]; assert len({row["rule_id"] for row in rules}) == len(rules); assert len({row["literal_id"] for row in literals}) == len(literals); assert {row["scenario"] for row in scenarios} == expected; assert all(row.get("required") and row.get("forbidden") for row in scenarios); assert bad_rule.get("disposition") not in rd; assert bad_literal.get("classification") not in lc; print(f"rules={len(rules)} literals={len(literals)} scenarios={len(scenarios)} unknown_values=rejected")'` | planned-for-implementation | implement | M1 | M1 code-review | Block on missing fields, duplicate IDs, incomplete scenario identity, or unknown closed values before consistency checks. | Not applicable; the assertion command must execute every named check. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m1-preservation-inventories.md` | Repository-local reads only; no network or target-agent runtime. |
| CMD2 | `python scripts/validate-skills.py skills/workflow/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block on canonical structure, resource, placeholder, or claim failure. | Not applicable; validator must report the selected skill. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m2-package-refactor.md` | Repository-local reads only. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block on any focused or regression failure. | Zero discovered tests is failure. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m2-package-refactor.md` | Temporary repository-local fixtures only. |
| CMD4 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block on generation, inventory, or resource-parity regression. | Zero discovered tests is failure. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m2-package-refactor.md` | Temporary repository-local output only. |
| CMD5 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block on generated-skill drift. | Not applicable. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m2-package-refactor.md` | Check mode; no authored output mutation. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block on archive, resource, or clean-install regression. | Zero discovered tests is failure. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m3-package-proof.md` | Temporary local package roots; no publication or network. |
| CMD7 | `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.3.6"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "workflow"], check=True)""")'` | existing/configured | implement | M3 | M3 code-review | Block if any supported archive or installed tree lacks identical mapped resources. | Every supported target and selected skill must be validated. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m3-package-proof.md` | Fresh temporary directory; no publication, network, or agent execution. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/workflow-skill-simplification.md` | existing/configured | test-spec | M1 | test-spec-review | Block on missing or invalid boundary-to-proof coverage. | Not applicable. | `docs/changes/2026-08-11-workflow-skill-simplification/evidence/test-spec-authoring.md` | Repository-local reads only. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-11-workflow-skill-simplification/change.yaml` | existing/configured | workflow | M1 | every lifecycle gate | Block on invalid artifact or planned-work state. | Not applicable. | stage-owned lifecycle evidence | Repository-local reads only. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-workflow-skill-simplification` | existing/configured | workflow | M1 | every formal review | Block on malformed or unindexed review evidence. | Not applicable. | stage-owned review evidence | Repository-local reads only. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T8, T9, T13 | MP1 | CMD1, CMD8-CMD10 | `evidence/m1-preservation-inventories.md`; `evidence/assembly-size-baseline.md` | M1 code-review | No canonical workflow prose moves before inventory coverage. |
| M2 | T1-T7, T10 | none | CMD1-CMD5, CMD8-CMD10 | `evidence/m2-package-refactor.md` | M2 code-review | Focused assertions precede package edits and prove exact loading. |
| M3 | T10-T15 | MP2 | CMD1-CMD10 | `evidence/m3-package-proof.md`; `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md` | M3 code-review | Metrics, semantics, installed parity, and rollback close together. |

## Test cases

### T1. Predicates select exactly seven valid assemblies

- Covers: R4, R5, R10, R18, E1, E2, EC6
- Level: unit
- Command IDs: CMD1, CMD3
- Fixture/setup: static predicate records and exact expected/forbidden resource sets.
- Steps: Evaluate WP0-WP4, WPB, WPS, and every invalid combination; include boundary-triggered variants without renaming assemblies.
- Expected result: each valid input selects one exact assembly and every unsupported combination stops.
- Failure proves: classification is incomplete, overlapping, or inferred from the wrong evidence.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; change-local scenarios
- Required by milestone: M2

### T2. Universal contract and resource map remain complete

- Covers: R1-R3, R18, R25, E1, EC1
- Level: integration
- Command IDs: CMD2-CMD5
- Fixture/setup: final canonical workflow package.
- Steps: Validate frontmatter, required headings, inline universal clauses, exact READ/COPY mappings, containment, and false-trigger nonloading.
- Expected result: generic routing is self-sufficient and all package resources are mapped exactly once.
- Failure proves: universal policy is hidden or resource structure is invalid.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: existing skill validation
- Required by milestone: M2

### T3. Command and bootstrap authority are ordered

- Covers: R6-R8, R20, E3, E4, EC4
- Level: unit
- Command IDs: CMD1, CMD3
- Fixture/setup: new target, conversation-only request, successful and failed governed identity records.
- Steps: Assert command context alone is unarmed; assert exact WPB load, identity validation, reclassification, governed load, and persistence order.
- Expected result: no durable automation state exists before valid governed identity.
- Failure proves: conversational or transient state can acquire authority.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; change-local scenarios
- Required by milestone: M2

### T4. Invalid combined and stale authority stops

- Covers: R9, R20, E5, EC5
- Level: unit
- Command IDs: CMD1, CMD3
- Fixture/setup: active automation plus guide request; active run without governed record; stale and mismatched identities.
- Steps: exercise each invalid path and inspect forbidden mutations.
- Expected result: every path stops without rebind, resume, cancellation, guide write, or other mutation.
- Failure proves: invalid authority can cross workflow boundaries.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; change-local scenarios
- Required by milestone: M2

### T5. References have one-way, non-overlapping ownership

- Covers: R11-R15, E7, EC8
- Level: unit
- Command IDs: CMD2, CMD3
- Fixture/setup: final SKILL, three references, and skeleton.
- Steps: assert owned clauses, forbidden clauses, automation-to-governed dependency, guide rendering boundary, structural-only skeleton, and contradiction stop.
- Expected result: each policy has one owner and conditional resources cannot override upstream contracts.
- Failure proves: extraction created competing workflow models.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T6. Governed reads and status/off paths preserve authority

- Covers: R10, R19, E2, E9, EC2, EC3
- Level: unit
- Command IDs: CMD1, CMD3
- Fixture/setup: governed read, WPS status/off, and WP2 status/off records.
- Steps: assert exact loads, read-only behavior, `no-active-run`, and absence or presence of current-run handling.
- Expected result: governed reads do not imply mutation; stateless commands create no state; current-run commands load both references.
- Failure proves: status behavior creates authority or loads the wrong contract.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: `scripts/test-skill-validator.py`; change-local scenarios
- Required by milestone: M2

### T7. Required-resource and contradiction failures stop safely

- Covers: R15-R17, E6, EC7, EC8
- Level: integration
- Command IDs: CMD1-CMD3
- Fixture/setup: missing, unreadable, contradictory, and mixed-version required resources plus false-trigger controls.
- Steps: reach the resource gate and assert no dependent interpretation, state mutation, guide write, or fallback reconstruction.
- Expected result: triggered defects stop; untriggered resources stay unloaded.
- Failure proves: shortened common path can bypass package integrity.
- Evidence artifact: `evidence/m2-package-refactor.md`
- Automation location: existing skill tests and change-local scenarios
- Required by milestone: M2

### T8. Semantic and literal ledgers fail closed

- Covers: R21-R24
- Level: unit
- Command IDs: CMD1
- Fixture/setup: complete ledgers and unknown/missing disposition/classification fixtures.
- Steps: validate fields, unique IDs, closed values before consistency, destinations, consumers, and preservation proof.
- Expected result: every rule/literal is classified exactly once and unknown values fail explicitly.
- Failure proves: behavior can disappear or tests can become accidental policy owners.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: change-local standard-library proof
- Required by milestone: M1

### T9. Exact-string consumers migrate by contract class

- Covers: R23, R24, E8, EC9
- Level: manual
- Command IDs: CMD1
- Fixture/setup: repository-local `rg` results across scripts, tests, specs, skills, and adapter/package tests.
- Steps: classify every consumer; preserve normative text; atomically migrate parser/package consumers; update incidental assertions; evidence obsolete removals.
- Expected result: genuine compatibility remains and accidental wording does not freeze prose.
- Failure proves: literal compatibility is lost or conflated with semantics.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: MP1
- Required by milestone: M1

### T10. Canonical and generated package validation remains deterministic

- Covers: R1, R3, R16, R25, R28, R29
- Level: integration
- Command IDs: CMD2-CMD5
- Fixture/setup: final canonical package and generated skill output.
- Steps: validate structure, vocabulary, Resource map, containment, placeholders, claims, inventory, and raw resource parity.
- Expected result: existing owners accept the complete workflow package without a new validator or runtime.
- Failure proves: package or permanent validation compatibility regressed.
- Evidence artifact: `evidence/m2-package-refactor.md`; `evidence/m3-package-proof.md`
- Automation location: existing skill/build validation
- Required by milestone: M3

### T11. Archives and installed packages preserve every resource

- Covers: R3, R17, R25, R29, R32
- Level: smoke
- Command IDs: CMD6, CMD7
- Fixture/setup: fresh temporary adapter output for every supported target with workflow selected.
- Steps: build archives, validate inventory, install into temporary roots, compare SKILL, four references, and skeleton paths/bytes, and require negative omission/staleness failure.
- Expected result: every target contains one complete identical package and no agent starts.
- Failure proves: rollout can create a partial or mixed package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing adapter distribution/build/validation scripts
- Required by milestone: M3

### T12. Independent semantic review proves lifecycle preservation

- Covers: R2, R11-R13, R21, R28, R30
- Level: manual
- Command IDs: CMD1
- Fixture/setup: pre/post package, spec, architecture, rule ledger, literal ledger, and static scenarios.
- Steps: inspect every rule destination and each valid/invalid assembly; compare lifecycle, state, review, milestone, automation, isolation, claim, and handoff semantics.
- Expected result: no significant rule disappears, duplicates owners, or changes workflow behavior.
- Failure proves: structural success hides semantic loss.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: MP2
- Required by milestone: M3

### T13. Assembly and total-package measurements are honest

- Covers: R26, R27, EC10
- Level: unit
- Command IDs: CMD1
- Fixture/setup: pre/post canonical package and exact resource manifests.
- Steps: normalize LF, count unique resources once, record identities, Unicode whitespace words, UTF-8 bytes, each assembly, boundary variants, main file, each resource, and total package.
- Expected result: WP0 materially improves; all other deltas are reported and justified; 35-50 percent remains advisory.
- Failure proves: relocation or regression is disguised as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: change-local deterministic measurement
- Required by milestone: M3

### T14. Architecture, rollout, and rollback remain coherent

- Covers: R27, R30-R32, EC11
- Level: contract
- Command IDs: CMD8-CMD10
- Fixture/setup: approved spec/reviews, architecture assessment/update/review, plan, package proof, and rollback record.
- Steps: confirm ordering and ownership; compare state and lifecycle semantics; prove rollback restores the prior complete package and regeneration path.
- Expected result: package location changes without a new state architecture and rollback never mixes versions.
- Failure proves: simplification escaped its approved architecture or recovery boundary.
- Evidence artifact: `architecture-assessment.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md`
- Automation location: lifecycle validation plus MP2
- Required by milestone: M3

### T15. Acceptance excludes target runtimes and new machinery

- Covers: R25, R28, R29
- Level: integration
- Command IDs: CMD2-CMD7
- Fixture/setup: final diff, commands, tests, evidence, and dependencies.
- Steps: inspect for runtime invocation, prompts, transcripts, model selection, retries, scheduler, selector, state store, runtime hash, and permanent simplicity/token validators.
- Expected result: none participates in implementation or acceptance.
- Failure proves: scope or determinism boundary was violated.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: repository search plus semantic review
- Required by milestone: M3

## Fixtures and data

- `fixtures/scenario-contracts.yaml`: seven valid assemblies, boundary-trigger variants, and distinct invalid/failure outcomes.
- `fixtures/invalid-rule-disposition.yaml`: value outside the closed semantic disposition vocabulary.
- `fixtures/invalid-literal-classification.yaml`: value outside the closed literal classification vocabulary.
- Temporary package trees created and removed by existing adapter tooling.
- No model prompts, transcripts, user data, credentials, or network fixtures.

## Mocking/stubbing policy

Do not mock classification, Resource-map parsing, containment, package inventory, canonical-to-generated bytes, archive contents, or installed-tree bytes in final proof. Static scenarios model contract inputs and expected outcomes; they do not simulate an LLM. Temporary filesystem roots may isolate package generation and installation. Network and target runtimes are outside acceptance, not stubbed.

## Migration or compatibility tests

T9 inventories every exact-string consumer and applies its approved class. T10-T11 prove current canonical, generated, archived, and installed package compatibility. T12 proves lifecycle and persistence semantics remain unchanged. T14 proves rollback restores one prior complete package without rewriting historical evidence.

## Observability verification

Every automated failure identifies its test or command ID and affected rule, literal, assembly, resource, target, or invariant. Change-local evidence records inventory counts, resource identities, before/after words and bytes, package targets, semantic-review outcome, and limitations. No model identity, prompt, transcript, or runtime retry is evidence.

## Security/privacy verification

CMD2 and T10 retain containment checks. CMD7 writes only to a fresh temporary directory and performs no network or publication call. T15 rejects credentials, private prompts, transcripts, runtime calls, and nondeterministic model evidence. No user data is processed.

## Performance checks

T13 is the performance proof. It requires material WP0 word and byte reduction, justified non-regression for other assemblies, and total-package accounting. Token estimates are omitted unless an already-pinned repository tool, version, vocabulary, and normalization are recorded; no tokenizer dependency may be added.

## Manual QA checklist

### MP1. Complete semantic and literal baseline

- Automation rationale: structural checks cannot decide whether repeated prose encodes distinct behavior or whether an exact-string consumer is normative, parser-owned, incidental, or obsolete.
- Required environment: a clean repository worktree view with the current canonical workflow package, repository-local search tools, and no network or target runtime.
- Owner / owning stage: implement, M1.
- Inputs: current full workflow package, both ledgers, exact-string search results, and CMD1 output.
- Procedure: trace every significant rule and discovered literal to one disposition/classification and destination; challenge apparent duplicates and obsolete claims.
- Evidence: `docs/changes/2026-08-11-workflow-skill-simplification/evidence/m1-preservation-inventories.md`.
- Pass: no rule or consumer is unaccounted for and no test-only literal owns policy.
- Failure: any significant rule, duplication cluster, literal consumer, governing requirement, destination, or preservation proof is missing, ambiguous, multiply owned, or incorrectly classified.

### MP2. Final semantic and lifecycle preservation review

- Automation rationale: validators prove structure and byte identity but cannot judge whether relocated prose retains the same routing, authority, lifecycle, claim, and handoff meaning.
- Required environment: the reviewed repository revision with approved governing artifacts, complete pre/post canonical package evidence, both ledgers, static scenarios, measurements, and package proof; no network or target runtime.
- Owner / owning stage: implement, M3 before code-review.
- Inputs: approved spec, architecture, plan, pre/post package, ledgers, scenarios, measurements, and package proof.
- Procedure: independently inspect universal completeness, all assemblies, bootstrap/status/failure behavior, ownership direction, lifecycle/state invariants, claims, handoffs, rollout, and rollback.
- Evidence: `docs/changes/2026-08-11-workflow-skill-simplification/evidence/semantic-preservation-review.md`.
- Pass: all behaviorally significant rules retain one owner and no lifecycle behavior changes outside R1-R32.
- Failure: any rule disappears, acquires competing ownership, loads under the wrong assembly, changes an approved lifecycle or authority outcome, or lacks direct evidence no broader than its claim.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another model runtime; the contract accepts deterministic package and semantic evidence.
- Do not add prompt journeys, transcript grading, model matrices, version selection, or nondeterministic retry evidence.
- Do not add permanent word, token, line, prose-quality, or simplicity thresholds; measurements are change-local.
- Do not hand-edit or track generated adapter skill bodies as source.
- Do not retest unrelated workflow stages beyond preservation assertions required by R30.

## Uncovered gaps

None. Every approved requirement, example, boundary, and selected interaction has direct automated, manual, or hybrid proof.

## Next artifacts

- Formal `test-spec-review`.
- After approval, implementation starts at M1 under the owning change record.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. Readiness is not implementation authorization or Done.
