# Plan Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-12-plan-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/plan-skill-simplification.md`
- Plan: `docs/plans/2026-08-12-plan-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260813-reviewed-plan-initialization-and-settlement.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/plan-skill-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-12-plan-skill-simplification/reviews/spec-review-r2.md` |
| architecture | `docs/architecture/system/architecture.md` | `architecture` | `architecture-review-r1`; `docs/changes/2026-08-12-plan-skill-simplification/reviews/architecture-review-r1.md` |
| ADR | `docs/adr/ADR-20260813-reviewed-plan-initialization-and-settlement.md` | `adr-reviewed-plan-initialization` | `architecture-review-r1`; accepted in `docs/changes/2026-08-12-plan-skill-simplification/reviews/architecture-review-r1.md` |
| execution plan | `docs/plans/2026-08-12-plan-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-12-plan-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

M1 uses unit and integration tests around metadata semantics, plan-review settlement, workflow coordination, parser authority, and compatibility fixtures before changing published skill text. M2 adds focused skill-contract tests before moving procedure into one governed reference or changing structural assets. M3 proves deterministic profile reduction, semantic preservation, boundary coverage, and the canonical-to-generated-to-archive-to-clean-install package chain.

No target-agent runtime is executed. Static contract fixtures prove routing and failure outcomes; repository-owned validators exercise public parsing and package paths; manual semantic review is used only where automated structure cannot establish meaning or one-owner completeness.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| PSIM-R001-PSIM-R005 | T7-T9, T12-T13 | contract, integration, manual | Package shape, portable sufficiency, ownership, missing resources, and asset policy boundary. |
| PSIM-R006-PSIM-R010 | T1-T2, T5, T8 | integration, contract | Closed operations and equal write boundary with workflow-only continuation. |
| PSIM-R011-PSIM-R012 | T2, T5 | integration | Stable artifact and reviewed revision identities without hashes. |
| PSIM-R013-PSIM-R020 | T2-T5 | integration | Evidence-first initialization, idempotency, retry settlement, legal states, and recovery. |
| PSIM-R021-PSIM-R024 | T6-T8, T13 | migration, integration, manual | Stable-intent plans, sole live state owner, and governed replan boundary. |
| PSIM-R025-PSIM-R028 | T6, T10, T13 | migration, manual | Read-old/write-new compatibility and no reverse synchronization. |
| PSIM-R029 | T7, T13 | contract, manual | Separate semantic and literal ledgers with one disposition each. |
| PSIM-R030-PSIM-R032 | T9, T11, T13 | unit, contract, manual | Deterministic measurements, real PL0/PL1 reduction, and proof exclusions. |
| PSIM-R033 | T9, T11-T12 | integration, e2e | Canonical, generated, archived, and installed parity. |
| PSIM-R034-PSIM-R035 | T5, T10 | contract | Canonical architecture, accepted ADR, and change-local mutable assessment ownership. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T8 | Portable planning loads only common procedure and assets and writes no governed state. |
| E2 | T1-T2 | New governed plan creates stable identity and reaches review without target live state. |
| E3 | T3 | Clean review records judgment and reports initialization required. |
| E4 | T3-T4 | Workflow coordinates initialization and identical settlement retry. |
| E5 | T2-T3 | Stale reviewed revision blocks initialization without mutation. |
| E6 | T6 | Historical plan state cannot override `change.yaml`. |

## Proof map

Boundary model version: boundary-first-v1

Boundary model scope: PSIM-R001, PSIM-R002, PSIM-R003, PSIM-R004, PSIM-R005, PSIM-R006, PSIM-R007, PSIM-R008, PSIM-R009, PSIM-R010, PSIM-R011, PSIM-R012, PSIM-R013, PSIM-R014, PSIM-R015, PSIM-R016, PSIM-R017, PSIM-R018, PSIM-R019, PSIM-R020, PSIM-R021, PSIM-R022, PSIM-R023, PSIM-R024, PSIM-R025, PSIM-R026, PSIM-R027, PSIM-R028, PSIM-R029, PSIM-R030, PSIM-R031, PSIM-R032, PSIM-R033, PSIM-R034, PSIM-R035

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | PSIM-R006, PSIM-R007, PSIM-R008, PSIM-R009 | BND-INPUT-001 | T1, T2 | integration | automated | CMD1, CMD2, CMD7 | `evidence/m1-reviewed-plan-transaction.md`; `evidence/m2-plan-package.md` | M2 | - | - |
| PRF-002 | covered | PSIM-R013, PSIM-R014, PSIM-R015, PSIM-R017, PSIM-R018, PSIM-R019, PSIM-R020 | BND-STATE-001 | T2-T4 | integration | automated | CMD1-CMD4 | `evidence/m1-reviewed-plan-transaction.md` | M1 | - | - |
| PRF-003 | covered | PSIM-R003, PSIM-R006, PSIM-R009, PSIM-R010, PSIM-R011, PSIM-R012 | BND-AUTH-001 | T1-T5, T8 | integration | hybrid | CMD1-CMD4, CMD7 | `evidence/m1-reviewed-plan-transaction.md`; `evidence/semantic-preservation-review.md` | M3 | MP1 | - |
| PRF-004 | covered | PSIM-R001, PSIM-R002, PSIM-R003, PSIM-R004, PSIM-R005 | BND-COMPOSE-001 | T7-T9, T11-T12 | integration | hybrid | CMD6-CMD12 | `evidence/m2-plan-package.md`; `evidence/m3-package-proof.md` | M3 | MP1 | - |
| PRF-005 | covered | PSIM-R013, PSIM-R015, PSIM-R016, PSIM-R017, PSIM-R018 | BND-TEMPORAL-001 | T2-T4 | integration | automated | CMD1-CMD4 | `evidence/m1-reviewed-plan-transaction.md` | M1 | - | - |
| PRF-006 | covered | PSIM-R004, PSIM-R008, PSIM-R009, PSIM-R016, PSIM-R020, PSIM-R027 | BND-RECOVERY-001 | T2-T4, T6, T8, T12 | integration | automated | CMD1-CMD4, CMD6-CMD7, CMD10-CMD12 | `evidence/m1-reviewed-plan-transaction.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-007 | covered | PSIM-R021, PSIM-R023, PSIM-R024, PSIM-R025, PSIM-R026, PSIM-R027, PSIM-R028 | BND-COMPAT-001 | T6, T10, T13 | integration | hybrid | CMD1-CMD5, CMD13 | `evidence/m1-reviewed-plan-transaction.md`; `evidence/semantic-preservation-review.md` | M3 | MP0, MP1 | - |
| PRF-008 | covered | PSIM-R009, PSIM-R013, PSIM-R015, PSIM-R017, PSIM-R020 | INT-001 | T2-T4 | integration | automated | CMD1-CMD4 | `evidence/m1-reviewed-plan-transaction.md` | M1 | - | - |
| PRF-009 | covered | PSIM-R004, PSIM-R003, PSIM-R020 | INT-002 | T8, T12 | integration | automated | CMD6-CMD7, CMD10-CMD12 | `evidence/m2-plan-package.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-010 | covered | PSIM-R023, PSIM-R025, PSIM-R027, PSIM-R028 | INT-003 | T6, T10 | integration | automated | CMD1-CMD5 | `evidence/m1-reviewed-plan-transaction.md` | M1 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 file-entry asymmetry or multiple primary candidates | T1 | fail before plan mutation |
| EC2 plan changed after clean review | T2-T3 | stale review blocks initialization |
| EC3 initialization committed but settlement interrupted | T4 | identical retry settles without semantic rereview |
| EC4 matching `planned_work` already exists | T4 | idempotent initializer no-op and settlement retry |
| EC5 mismatched existing `planned_work` | T2, T4 | stop without replacement or repair |
| EC6 direct clean plan review | T3 | records initialization-required and remains isolated |
| EC7 missing governed reference | T8 | dependent work stops without reconstruction |
| EC8 old-format active plan with complete live state | T6 | stable intent reads while `change.yaml` owns current state |
| EC9 old-format active plan with incomplete live state | T6 | explicit workflow-owned migration required |
| EC10 post-initialization milestone baseline change | T5-T6 | ordinary authoring stops and routes to governed replan |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-change-metadata-validator.py` | existing/configured | implement | M1 | M1 code-review | Block unknown, illegal, or inconsistent metadata states. | Zero discovered tests is failure. | `evidence/m1-reviewed-plan-transaction.md` | Repository-local tests only. |
| CMD2 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | implement | M1 | M1 code-review | Block invalid authoring, review, initialization, or settlement transitions. | Zero discovered tests is failure. | `evidence/m1-reviewed-plan-transaction.md` | Repository-local tests only. |
| CMD3 | `python scripts/test-workflow-automation.py` | existing/configured | implement | M1 | M1 code-review | Block coordination, retry, identity, or routing regressions. | Zero discovered tests is failure. | `evidence/m1-reviewed-plan-transaction.md` | No target-agent runtime or external service. |
| CMD4 | `python scripts/test-workflow-automation-state.py` | existing/configured | implement | M1 | M1 code-review | Block invalid state projection or settlement-retry behavior. | Zero discovered tests is failure. | `evidence/m1-reviewed-plan-transaction.md` | Repository-local tests only. |
| CMD5 | `python scripts/test-query-change-record.py` | existing/configured | implement | M1 | M1 code-review | Block current-state authority or bounded-query regressions. | Zero discovered tests is failure. | `evidence/m1-reviewed-plan-transaction.md` | Read-only fixture tests. |
| CMD6 | `python scripts/validate-skills.py skills/plan/SKILL.md` | existing/configured | implement | M2 | M2 code-review | Block structure, resource, containment, placeholder, or claim defects. | Not applicable; deterministic validation. | `evidence/m2-plan-package.md` | Read-only validation. |
| CMD7 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2 | M2 code-review | Block focused or regression failure. | Zero discovered tests is failure. | `evidence/m2-plan-package.md` | No target-agent runtime. |
| CMD8 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 code-review | Block generated inventory or resource parity regression. | Zero discovered tests is failure. | `evidence/m2-plan-package.md` | Temporary filesystem only. |
| CMD9 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 code-review | Block generated-skill drift. | Not applicable; deterministic check. | `evidence/m2-plan-package.md` | Read-only check. |
| CMD10 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 code-review | Block archive, generation, installation, or parity regression. | Zero discovered tests is failure. | `evidence/m3-package-proof.md` | Temporary files only; no publication. |
| CMD11 | `python -c 'import subprocess, sys, tempfile; version="v0.1.5"; d=tempfile.TemporaryDirectory(prefix="rigorloop-plan-adapters-"); subprocess.run([sys.executable,"scripts/build-adapters.py","--version",version,"--output-dir",d.name],check=True); subprocess.run([sys.executable,"scripts/validate-adapters.py","--version",version,"--adapter-root",d.name,"--clean-install-smoke","--skill","plan"],check=True); d.cleanup()'` | existing/configured | implement | M3 | M3 code-review | Block any supported target missing byte-identical plan resources. | Not applicable; all supported targets must be produced. | `evidence/m3-package-proof.md` | Fresh temporary directory; no network, publication, or agent execution. |
| CMD12 | `python scripts/validate-boundary-first.py --check --path specs/plan-skill-simplification.md` | existing/configured | implement | M3 | M3 code-review | Block missing or invalid boundary and interaction proof. | Not applicable; matching proof map is mandatory. | `evidence/m3-package-proof.md` | Read-only validation. |
| CMD13 | `python scripts/validate-change-metadata.py docs/changes/2026-08-12-plan-skill-simplification/change.yaml` | existing/configured | workflow | lifecycle | every state-changing handoff | Block invalid artifact or planned-work state. | Not applicable; deterministic validation. | owning change record | Read-only validation. |
| CMD14 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-12-plan-skill-simplification` | existing/configured | review stages | lifecycle | every formal review handoff | Block malformed or missing durable review evidence. | Not applicable; deterministic validation. | review log and records | Read-only validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1-T6, T10 | MP0 | CMD1-CMD5, CMD13 | `evidence/m1-reviewed-plan-transaction.md` | M1 code-review | Contracts and deterministic lifecycle support precede package prose movement. |
| M2 | T7-T9 | none | CMD6-CMD9, CMD13 | `evidence/m2-plan-package.md`; rule and literal ledgers | M2 code-review | Focused failing assertions precede canonical package edits. |
| M3 | T9, T11-T13 | MP1 | CMD6-CMD14 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code-review and final holistic review | Proves profile, semantic, boundary, migration, and package-chain acceptance. |

## Test cases

### T1. Governed operations classify exactly and fail closed

- Covers: PSIM-R006-PSIM-R008, PSIM-R010-PSIM-R011; E1-E2; EC1; BND-INPUT-001, BND-AUTH-001
- Level: integration
- Command IDs: CMD1, CMD2, CMD7
- Fixture/setup: create, revise, initialize, portable, missing entry, missing file, multiple primary, mismatched identity, unknown, and ambiguous scenarios.
- Steps: invoke the public classification and validation paths and assert one legal operation or a stop before write.
- Expected result: creation does not require existing identity, revision requires one matching identity, and invalid evidence cannot mutate state.
- Failure proves: operation selection or authority can be inferred ambiguously.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`; `evidence/m2-plan-package.md`
- Automation location: lifecycle fixtures and `scripts/test-skill-validator.py`
- Required by milestone: M1 and M2

### T2. Initialization binds to current clean review and absent live state

- Covers: PSIM-R009, PSIM-R011-PSIM-R016, PSIM-R019-PSIM-R020; E2, E5; EC2, EC5; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001
- Level: integration
- Command IDs: CMD1-CMD4
- Fixture/setup: exact reviewed revision, stale revision, contradictory later review, open resolution, invalid milestones, absent, matching, and mismatched `planned_work`.
- Steps: attempt initialization through the plan-owned path and inspect writes and blockers.
- Expected result: only current clean approved evidence with absent state writes the complete initial structure; identical basis is a no-op; conflicts stop.
- Failure proves: stale judgment or existing state can be overwritten or repaired.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: metadata, lifecycle, and workflow test suites
- Required by milestone: M1

### T3. Clean review records before initialization and remains isolated when direct

- Covers: PSIM-R013-PSIM-R014, PSIM-R018-PSIM-R020; E3, E5; EC2, EC6; BND-STATE-001, BND-TEMPORAL-001; INT-001
- Level: integration
- Command IDs: CMD1-CMD4, CMD14
- Fixture/setup: direct and workflow-managed clean plan-review for a review-required plan without `planned_work`.
- Steps: record judgment, inspect plan state, result, routing, and subsequent eligible action.
- Expected result: durable evidence exists, plan remains review-required, result is initialization-required, direct review stops, and workflow may coordinate the next call.
- Failure proves: review settlement can precede live state or isolation can be bypassed.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: lifecycle and workflow tests
- Required by milestone: M1

### T4. Interrupted settlement retries without semantic rereview

- Covers: PSIM-R015-PSIM-R020; E4; EC3-EC5; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001
- Level: integration
- Command IDs: CMD1-CMD4
- Fixture/setup: matching initial state plus recorded clean review, interrupted settlement, duplicate identical retry, and conflicting review-ID reuse.
- Steps: run workflow reconciliation and plan-review settlement retry while tracking judgment invocations and state writes.
- Expected result: identical retry reuses the record, moves only the plan to active once, and routes onward only after settlement; conflicts stop.
- Failure proves: retries can duplicate judgment, mutate unrelated state, or route early.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: workflow automation and lifecycle tests
- Required by milestone: M1

### T5. Cross-stage ownership remains bounded

- Covers: PSIM-R009-PSIM-R012, PSIM-R015, PSIM-R017-PSIM-R018, PSIM-R034-PSIM-R035; BND-AUTH-001
- Level: contract
- Command IDs: CMD1-CMD4, CMD13
- Fixture/setup: plan, plan-review, workflow, architecture, and change-record ownership fixtures.
- Steps: assert each component's permitted writes and every forbidden sibling, routing, assessment, and settlement write.
- Expected result: plan initializes only missing state, plan-review records and settles, workflow coordinates and routes, and `change.yaml` owns mutable assessment status.
- Failure proves: procedure loading or orchestration broadens ownership.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: metadata and workflow contract tests
- Required by milestone: M1

### T6. Migration is read-old/write-new with one live state owner

- Covers: PSIM-R021-PSIM-R028; E6; EC8-EC10; BND-COMPAT-001, BND-RECOVERY-001; INT-003
- Level: integration
- Command IDs: CMD1-CMD5
- Fixture/setup: new-format plan, portable plan, terminal historical plan, active old-format complete state, incomplete state, conflicting IDs/kinds, and post-initialization baseline edit.
- Steps: exercise public readers, writer output, bounded query, migration route, and ordinary authoring rejection.
- Expected result: writers emit stable intent only; old compatible data reads; `change.yaml` wins; incomplete/conflicting live state and baseline edits stop for explicit migration or replan.
- Failure proves: historical prose can become live authority or be reverse-synchronized.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: lifecycle, query, and compatibility fixtures
- Required by milestone: M1

### T7. Semantic and literal inventories fail closed before prose movement

- Covers: PSIM-R005, PSIM-R021-PSIM-R022, PSIM-R029; BND-COMPOSE-001
- Level: contract
- Command IDs: CMD7
- Fixture/setup: valid rule and literal ledgers plus unknown disposition, unknown classification, duplicate ID, missing field, and inconsistent destination fixtures.
- Steps: validate closed vocabulary before destination consistency and reconcile every source cluster and exact-string consumer.
- Expected result: all current rules and literals have one treatment; unknown values fail first; incidental tests do not own prose.
- Failure proves: semantics can disappear or accidental compatibility can freeze the refactor.
- Evidence artifact: rule and literal ledgers; `evidence/m2-plan-package.md`
- Automation location: focused skill-validator assertions and change-local deterministic fixture check
- Required by milestone: M2

### T8. Portable and governed packages load exact resources and fail safely

- Covers: PSIM-R001-PSIM-R005, PSIM-R010; E1; EC7; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-002
- Level: integration
- Command IDs: CMD6-CMD9
- Fixture/setup: PL0, PL0B, PL1, PL1B, false triggers, missing/unreadable references, escaped paths, contradictions, and mixed versions.
- Steps: validate exact required and forbidden resource loads, authority, containment, and failure results.
- Expected result: portable planning remains self-sufficient; governed and boundary resources load once only when triggered; missing dependent procedure stops without reconstruction.
- Failure proves: progressive disclosure hides universal behavior or grants authority.
- Evidence artifact: `evidence/m2-plan-package.md`
- Automation location: skill and build validation suites
- Required by milestone: M2

### T9. Stable-intent assets contain structure but no policy or mutable state

- Covers: PSIM-R005, PSIM-R021-PSIM-R022, PSIM-R029-PSIM-R033; BND-COMPOSE-001
- Level: integration
- Command IDs: CMD6-CMD9
- Fixture/setup: all three canonical assets, copied representative plan, generated skills, and invalid mutable-state or placeholder fixtures.
- Steps: assert required stable fields, exact asset count, complete sentences, no state/progress fields, no policy, no placeholders, and package parity.
- Expected result: structural output remains complete while mutable state and policy have one external owner.
- Failure proves: asset simplification removes execution intent or recreates a second state owner.
- Evidence artifact: `evidence/m2-plan-package.md`; `evidence/m3-package-proof.md`
- Automation location: skill and build validation suites
- Required by milestone: M2 and M3

### T10. Architecture and governing contracts remain coherent

- Covers: PSIM-R023-PSIM-R028, PSIM-R034-PSIM-R035; BND-COMPAT-001; INT-003
- Level: contract
- Command IDs: CMD1-CMD5, CMD13
- Fixture/setup: canonical architecture, successor ADR, lifecycle specs, instructions, and state fixtures.
- Steps: verify transaction ordering, identity, legal states, recovery, source ownership, and owning change pointers agree across governing surfaces.
- Expected result: no active contract preserves pre-review initialization or plan-body live state authority after M1.
- Failure proves: implementation would have contradictory governing sources.
- Evidence artifact: `evidence/m1-reviewed-plan-transaction.md`
- Automation location: lifecycle tests plus bounded semantic contract inspection
- Required by milestone: M1

### T11. Profile measurement proves real simplification

- Covers: PSIM-R029-PSIM-R032; BND-COMPOSE-001
- Level: unit
- Command IDs: CMD6-CMD9
- Fixture/setup: canonical baseline and final files with documented LF normalization, assembly order, resource identities, and duplicate clusters.
- Steps: count each unique procedure once; compute PL0, PL0B, PL1, PL1B, per-resource, asset, and total-package words and UTF-8 bytes.
- Expected result: PL0 and PL1 decrease, boundary growth is explained, assets and package totals are separate, and semantic preservation overrides percentages.
- Failure proves: relocation or duplication is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: change-local standard-library measurement recorded in evidence
- Required by milestone: M3

### T12. Canonical through installed package parity is exact

- Covers: PSIM-R001, PSIM-R004, PSIM-R032-PSIM-R033; EC7; BND-COMPOSE-001, BND-RECOVERY-001; INT-002
- Level: e2e
- Command IDs: CMD6-CMD12
- Fixture/setup: canonical package and fresh generated, archived, and clean-installed adapter trees plus incomplete and mixed fixtures.
- Steps: compare mapped paths and bytes across every supported target and exercise missing, transformed, stale, escaped, and mixed failures.
- Expected result: complete targets match canonical bytes and every incomplete or mixed target fails closed without agent execution.
- Failure proves: canonical acceptance does not survive distribution.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: build and adapter validation suites
- Required by milestone: M3

### T13. Independent semantic review confirms full preservation

- Covers: PSIM-R001-PSIM-R035; EC8-EC10; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001
- Level: manual
- Command IDs: none
- Fixture/setup: baseline and final package, approved spec and ADR, rule/literal ledgers, scenarios, measurements, migration results, and package proof.
- Steps: execute MP1 and trace every requirement and current significant rule to exactly one owner and direct proof.
- Expected result: portable quality, lifecycle authority, reviewed-plan transaction, migration, assets, claims, and failure behavior remain complete with no unapproved semantic change.
- Failure proves: structural proof passed while behavior or ownership regressed.
- Evidence artifact: `evidence/semantic-preservation-review.md`
- Automation location: manual independent review
- Required by milestone: M3

## Fixtures and data

- Operation and state fixtures cover all three operations, all legal state-table rows, and representative illegal, stale, conflicting, interrupted, and duplicate cases.
- Compatibility fixtures cover new format, portable plans, terminal historical plans, active old complete and incomplete changes, and conflicting milestone identity or kind.
- Rule and literal ledgers are JSON-compatible YAML with stable IDs and closed classifications; invalid fixtures prove unknown values fail first.
- Resource fixtures cover PL0, PL0B, PL1, PL1B, missing, unreadable, escaped, transformed, stale, contradictory, and mixed package states.
- Temporary package trees use a fresh system temporary directory and are removed after validation.

## Mocking/stubbing policy

Do not mock a target-agent runtime because none is part of acceptance. Static fixtures model authoritative artifact and state inputs, while integration tests must exercise public metadata, lifecycle, workflow, skill, build, and adapter paths rather than helper-only shortcuts.

## Migration or compatibility tests

T6 and T10 prove read-old/write-new behavior, sole live state ownership, explicit migration, historical preservation, and governed replan. T7 classifies literal compatibility separately. T12 proves complete-package forward and rollback parity.

## Observability verification

Evidence must record reviewed revision identity, transition result, blocker, state writes, rule and literal counts, profile file lists and measurements, command IDs and outcomes, package targets and byte identities, and semantic conclusions. No new telemetry, trace service, or runtime attestation is introduced.

## Security/privacy verification

All automated proof uses repository files and disposable local directories. Tests must not use credentials, network services, publication endpoints, external mutation, private data, or paths outside declared roots.

## Performance checks

Measure PL0, PL0B, PL1, PL1B, each procedure, each asset, and total package in LF-normalized Unicode words and UTF-8 bytes. Token counts are optional only if an already pinned repository tool supports the same assembly. No runtime timing or permanent percentage gate is added.

## Manual QA checklist

### MP0. Pre-change compatibility inventory audit

- Manual procedure ID: MP0
- Automation rationale: semantic rule equivalence and normative-versus-incidental literal ownership cannot be inferred safely from exact-string tests alone.
- Required environment: tracked M1/M2 baseline with the complete current plan package, governing contracts, parsers, tests, and package consumers.
- Steps:
  1. Read the complete current `skills/plan/` package and the plan, plan-review, workflow, lifecycle, and package consumers named by bounded searches.
  2. Group each significant rule and duplicate cluster under one stable semantic ID.
  3. Classify exact headings, fields, vocabulary, and phrases as normative, parser/package, incidental test, obsolete, or historical fixture.
  4. Reconcile every current source cluster and consumer to one ledger row before package prose moves.
- Evidence artifact: rule and literal ledgers plus `evidence/m2-plan-package.md`
- Pass condition: every material rule, duplicate, and literal consumer has one supported treatment and no unapproved rule disappears.
- Failure condition: any owner, rule, consumer, classification, or source cluster is missing, duplicated, ambiguous, or unsupported.
- Owning stage: implement M2; required before canonical package movement.

### MP1. Final semantic preservation and ownership review

- Manual procedure ID: MP1
- Automation rationale: validators prove structure, state transitions, and bytes but cannot establish complete semantic equivalence or correct prose ownership.
- Required environment: final canonical package and lifecycle implementation with approved spec, architecture, ADR, plan, test spec, ledgers, fixtures, measurements, and deterministic validation evidence.
- Steps:
  1. Trace every PSIM requirement, boundary, interaction, and semantic-rule row to the final owner and direct proof.
  2. Confirm `SKILL.md` remains sufficient for portable planning and every universal stop, claim, quality, and handoff rule.
  3. Confirm the governed reference owns only the three operations and does not grant authority or duplicate universal or boundary procedure.
  4. Confirm new assets preserve stable intent without mutable state or policy and historical readers never restore plan-body authority.
  5. Reconcile PL0/PL1 and total-package measurements with the actual loaded files and package proof.
- Evidence artifact: `docs/changes/2026-08-12-plan-skill-simplification/evidence/semantic-preservation-review.md`
- Pass condition: every rule has one correct owner, all behavior and lifecycle authority are preserved, and all profile and package claims match direct evidence.
- Failure condition: any missing, duplicated, hidden, broadened, contradictory, or unproved behavior remains.
- Owning stage: implement M3; required before M3 code-review and final holistic review.

## What not to test and why

- Do not execute or grade Codex, Claude Code, opencode, or another model runtime; the change is a deterministic contract, parser, and package refactor.
- Do not add prompt journeys, transcript grading, model selection, tokenizer dependencies, prose scores, or permanent simplicity validators.
- Do not test publication, release, deployment, network, credential, or external-service behavior because the approved change introduces none.
- Do not rewrite historical plans merely to prove compatibility; fixture reads and explicit migration failures are the required boundary.
- Do not treat a snapshot or exact sentence as semantic proof unless the literal inventory classifies it as a real contract.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review` evidence.
- M1 lifecycle and compatibility implementation evidence after approval.
- M2 package and preservation evidence.
- M3 measurements, semantic review, and package proof.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. This proof map does not authorize implementation until that formal review approves it and workflow settles the test-spec entry.
