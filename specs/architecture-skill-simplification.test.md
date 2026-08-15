<!-- Template: test-spec-skeleton-v1 -->

# Architecture Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/architecture-skill-simplification.md`
- Plan: `docs/plans/2026-08-15-architecture-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-15-architecture-skill-simplification/architecture-assessment.md`; architecture is not required because the prepared manifest remains ordinary Markdown authoring evidence under existing package and lifecycle ownership

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/architecture-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-15-architecture-skill-simplification/reviews/spec-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-15-architecture-skill-simplification/architecture-assessment.md` | not applicable | Recorded `architecture-not-required` assessment |
| Execution plan | `docs/plans/2026-08-15-architecture-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-15-architecture-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic contract fixtures for package loading, classification, assessment binding, prepared manifests, dependency-safe commits, retries, asset ownership, compatibility, measurement, and missing resources. Existing validators own permanent skill, lifecycle, boundary, build, and adapter checks. Change-local ledgers, scenarios, representative output, and measurements prove semantic disposition and real loaded-context reduction. No target-agent runtime or separate manual semantic-review acceptance gate is part of this proof map.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R7 | T1-T2, T12 | contract | Package inventory, universal ownership, exact mapping, and fail-safe resources. |
| R8-R15 | T3-T4 | contract | Closed classifications, assemblies, assessment receipts, and isolation. |
| R16-R20 | T5 | contract | Current required assessment basis for portable and governed authoring. |
| R21-R30 | T6-T7 | contract | Per-target manifests, prepared evidence before writes, bounded progress, and settlement. |
| R31-R42 | T8-T10 | contract | Dependencies, commit groups, commit points, batch outcomes, retry, concurrency, and recovery. |
| R43-R48 | T11 | contract | Asset ownership, semantic and literal dispositions, and unknown-value-first validation. |
| R49-R51 | T13 | integration | Deterministic measurement and reduction of all real loaded assemblies. |
| R52-R54 | T12, T14 | integration | Package parity, deterministic acceptance, and architecture escalation boundary. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Command IDs | Required milestone | Notes |
| --- | --- | --- | --- | --- |
| AC1 | T1-T14 | CMD1-CMD10 | M1-M3 | Every R1-R54 requirement maps through the requirement table, exact proof obligations, and stable test cases. |
| AC2 | T13 | CMD1 | M3 | AA0, AA1, and AA2 words and bytes must decrease while total package size remains visible. |
| AC3 | T3-T5, T11 | CMD1, CMD3 | M2 | Assessment, action, governed-signal, operation, evidence, and batch vocabularies reject unknown, stale, malformed, and conflicting values. |
| AC4 | T5-T7 | CMD3, CMD9 | M2 | Workflow-managed authoring binds current assessment, spec, and spec-review identities before mutation. |
| AC5 | T6-T7 | CMD3 | M2 | The complete manifest and every intended identity are durable before target mutation. |
| AC6 | T8-T10 | CMD3 | M2 | Dependencies, commit groups, commit points, ADR supersession, partial results, and retries have direct proof. |
| AC7 | T11 | CMD1, CMD3 | M1-M2 | Semantic rules, compatibility-sensitive literals, and asset instructions receive one closed owner and disposition. |
| AC8 | T2, T12 | CMD2-CMD7 | M2-M3 | Missing or invalid required resources stop dependent work and fail package parity. |
| AC9 | T12 | CMD4-CMD7 | M3 | Canonical, generated, archived, release-candidate, and installed resources retain raw-byte parity. |
| AC10 | T14 | CMD1-CMD10 | M3 | Deterministic repository proof excludes target-agent execution and a separate manual semantic-review gate. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T3 | Assessment-only loads AA0 and returns one truthful result. |
| E2 | T4-T5 | Portable authoring requires a current inline required judgment and writes no lifecycle state. |
| E3 | T4 | Invalid governed signals stop without portable fallback. |
| E4 | T5 | A stale assessment basis blocks workflow-managed authoring. |
| E5 | T6 | The complete manifest and intended identities are durable before target mutation. |
| E6 | T7, T10 | An interrupted canonical package resumes only from its exact persisted manifest. |
| E7 | T8-T9 | Diagram and ADR dependencies commit before canonical Markdown. |
| E8 | T9 | Partial completion preserves only independently valid targets. |
| E9 | T8 | ADR supersession follows dependency order while review retains approval. |
| E10 | T2, T12 | Missing conditional resources stop without remembered reconstruction. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R8, R9, R10, R11, R12, R13, R21, R22, R27, R37 | BND-INPUT-001 | T3-T4, T11 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R14, R15, R16, R17, R18, R19, R20, R25, R26, R27, R28, R29, R30, R37, R38, R39, R40, R41, R42 | BND-STATE-001 | T3, T5-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R10, R11, R12, R16, R17, R18, R19, R20, R21, R22, R23, R24, R30, R36 | BND-AUTH-001 | T4-T6, T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R6, R7, R23, R24, R31, R32, R33, R34, R35, R43, R44, R45 | BND-COMPOSE-001 | T1-T2, T8, T11-T12 | integration | automated | CMD2-CMD8 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R25, R26, R27, R28, R29, R30, R31, R32, R37, R38, R39, R40, R41, R42 | BND-TEMPORAL-001 | T6-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R7, R26, R28, R29, R31, R32, R33, R34, R37, R38, R39, R40, R41, R42, R54 | BND-RECOVERY-001 | T2, T6-T10, T14 | contract | automated | CMD1-CMD3, CMD8 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R43, R44, R45, R46, R47, R48, R49, R50, R51, R52 | BND-COMPAT-001 | T11-T13 | integration | automated | CMD1-CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R7, R15, R29, R39, R42, R52, R53 | BND-ENV-001 | T2, T4, T7, T10, T12, T14 | integration | automated | CMD2, CMD4-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R10, R11, R12, R17, R18 | INT-001 | T4-T5 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R25, R26, R28, R29, R40, R41, R42 | INT-002 | T6-T7, T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R24, R31, R32, R33, R34, R35, R38 | INT-003 | T8-T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R45, R46, R47, R49, R50, R51, R52 | INT-004 | T11-T13 | integration | automated | CMD1-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| EC1: isolated assessment concludes not-required | T3 | Return a rationale without loading either conditional reference or writing lifecycle state. |
| EC2: spec changes after required assessment | T5 | Treat the assessment as stale and stop before target mutation. |
| EC3: prepared evidence exists with no target write | T7, T10 | Revalidate the exact basis and resume without duplicating evidence. |
| EC4: diagram exists outside the manifest | T7, T10 | Refuse adoption and stop with the exact unrecorded-file blocker. |
| EC5: replacement ADR is valid but predecessor update fails | T8-T9 | Preserve only independently valid completed work and report `partial-blocked`. |
| EC6: canonical Markdown would reference an incomplete dependency | T8-T9 | Do not write the canonical commit point. |
| Unknown closed-vocabulary value | T3, T11 | Reject it before any consistency check. |
| Required resource is missing, escaped, transformed, or mixed-version | T2, T12 | Stop dependent work and fail package parity. |
| Concurrent authority or baseline change after preparation | T7, T10 | Stop without adopting or overwriting the changed state. |
| Total package grows while all loaded assemblies shrink | T13 | Report and justify growth without failing solely on a fixed percentage. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-skill-validator.py ArchitectureSkillSimplificationLedgerTests` | planned-for-implementation | M1 implementation | M1 | M1 | Stop M1 and retain the failing ledger, vocabulary, scenario, or measurement fixture. | A missing class or zero-test result fails. | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | Existing repository runner with deterministic change-local fixtures only. |
| CMD2 | `python scripts/validate-skills.py skills/architecture/SKILL.md` | existing/configured | repository skill validation | M2 | M2 | Stop on structural, mapping, path, or resource failure. | Not applicable. | `evidence/m2-package-implementation.md` | Reads canonical skill package only. |
| CMD3 | `python scripts/test-skill-validator.py ArchitectureSkillSimplificationTests` | planned-for-implementation | M2 implementation | M2 | M2 | Stop on any focused contract regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local deterministic tests only. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | repository skill validation | M2 | M2 | Stop on any skill-contract regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local tests only. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | repository package validation | M2 | M2 | Stop on build or package regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Uses repository-owned temporary package fixtures. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | repository package generation | M2 | M2 | Stop on stale or invalid generated skill output. | Not applicable. | `evidence/m2-package-implementation.md` | Check mode does not publish packages. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | repository adapter validation | M3 | M3 | Stop on generated, archived, release-candidate, or installed parity failure. | A zero-test result fails. | `evidence/m3-package-proof.md` | Uses repository-owned temporary adapter trees; no publication. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/architecture-skill-simplification.md` | existing/configured | boundary contract validation | M3 | M3 | Stop on incomplete requirement, boundary, interaction, or proof mapping. | Not applicable. | `evidence/m3-package-proof.md` | Read-only structural validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-15-architecture-skill-simplification/change.yaml` | existing/configured | lifecycle metadata validation | all | test-spec-review | Stop on invalid lifecycle or artifact metadata. | Not applicable. | stage-owned lifecycle evidence | Read-only metadata validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-15-architecture-skill-simplification` | existing/configured | review evidence validation | all | test-spec-review | Stop on incomplete or inconsistent review evidence. | Not applicable. | change-local review records | Read-only review validation. |
| CMD11 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | ci-owned | repository PR validation | M4 | final verify | Stop final closeout on any required CI failure. | A zero-test result fails where the selected command owns tests. | final verify report | Repository-owned PR-mode checks; no publication. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T3-T4, T11, T13 | none | CMD1, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | M1 code review | Freeze rule, literal, asset, scenario, and measurement ownership before canonical edits. |
| M2 | T1-T11 | none | CMD1-CMD6, CMD9 | `evidence/m2-package-implementation.md` | M2 code review | Prove the canonical package, classification, assessment basis, prepared transactions, dependencies, assets, and recovery. |
| M3 | T12-T14 | none | CMD2, CMD4-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code review and final closeout | Prove real-profile reduction, complete boundary proof, lifecycle validity, and package parity. |
| M4 | T14 | none | CMD1-CMD11 | final review, explanation, and verify evidence | PR handoff | Run holistic deterministic closeout after all implementation milestones and review resolution are closed. |

## Test cases

### T1. Package ownership and loaded assemblies are exact

- Covers: R1-R6, R13; BND-COMPOSE-001
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Canonical package plus assessment-only, portable-authoring, and governed-authoring invocations.
- Steps: Resolve each resource assembly and inspect universal and conditional ownership.
- Expected result: AA0 loads only the universal file, AA1 adds the method reference, AA2 adds both references, and assets are copied only for applicable authoring output.
- Failure proves: Universal safety moved behind a trigger or conditional procedure is loaded on the wrong path.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill contract fixtures.
- Required by milestone: M2

### T2. Missing or invalid resources fail before dependent work

- Covers: R6-R7; E10; BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Missing, unreadable, escaped, stale, contradictory, and mixed-version references or assets.
- Steps: Trigger each resource and attempt dependent assessment or authoring.
- Expected result: The invocation names the blocker and stops before reconstruction, mutation, or dependent claims.
- Failure proves: Package failure can weaken method or lifecycle safety.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Resource-map and temporary package fixtures.
- Required by milestone: M2

### T3. Assessment and action vocabularies route deterministically

- Covers: R8-R9, R13-R15, R48; E1; EC1; BND-INPUT-001, BND-STATE-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Every assessment mode, judgment, route, action, valid combination, and unknown value.
- Steps: Classify each invocation and inspect loaded resources, receipt fields, writes, and result.
- Expected result: Known values map exactly, unknown values fail first, workflow receipts preserve required fields, ambiguity pauses, and isolated assessment writes only to an explicit valid path.
- Failure proves: Assessment routing or write authority is open-ended.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Closed-vocabulary and assessment fixtures.
- Required by milestone: M2

### T4. Governed signals fail closed without portable fallback

- Covers: R10-R13; E2-E3; BND-INPUT-001, BND-AUTH-001, BND-ENV-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: No signal, one valid signal, malformed fields, duplicate, stale, escaped, mismatched, and conflicting signals.
- Steps: Request portable or governed authoring and inspect reference loading and mutation.
- Expected result: Only no signal permits portable behavior, one candidate loads governed procedure for validation, and every invalid or ambiguous signal stops.
- Failure proves: Malformed ownership can fall through to unsafe portable mutation.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Signal and authority fixtures.
- Required by milestone: M2

### T5. Authoring binds one current required assessment

- Covers: R16-R20; E2, E4; EC2; BND-STATE-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Current, missing, stale, contradictory, not-required, and ambiguous workflow assessments plus portable inline judgments.
- Steps: Resolve action, spec identity, spec-review identity, and assessment receipt before authoring.
- Expected result: Workflow authoring proceeds only on the exact current required basis, portable authoring repeats the judgment inline, and every other state stops before mutation.
- Failure proves: Obsolete or contradictory applicability can authorize architecture writes.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Assessment-basis fixtures.
- Required by milestone: M2

### T6. Prepared evidence is durable before target mutation

- Covers: R21-R28; E5; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Canonical, ADR, and combined manifests with exact operations, files, identities, dependencies, groups, and evidence dispositions.
- Steps: Interrupt before preparation, after preparation, and before the first target write.
- Expected result: All intended identities and commit points exist in ordinary authoring evidence before mutation, pre-preparation interruption writes nothing, and changed authority or baseline blocks writes.
- Failure proves: Crash recovery relies on an in-memory or incomplete manifest.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Prepared-evidence and interruption fixtures.
- Required by milestone: M2

### T7. Manifest-bounded writes and target settlement reject drift

- Covers: R21-R30, R39-R42; E6; EC3-EC4; BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD3, CMD9
- Fixture/setup: Prepared manifests with exact files, unrecorded files, changed baselines, competing writes, partial progress, and completed targets.
- Steps: Attempt each write, record progress, and settle entries.
- Expected result: Only recorded files change, only completed targets reach `review-required`, identical state resumes or no-ops once, and drift stops without adoption.
- Failure proves: Governed authoring exceeds its persisted transaction or lifecycle write set.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Temporary filesystem and metadata fixtures.
- Required by milestone: M2

### T8. Dependencies and commit groups preserve intermediate validity

- Covers: R24, R31-R36; E7, E9; EC5-EC6; BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Canonical Markdown, diagrams, replacement and predecessor ADRs, independent targets, coupled targets, and failing dependencies.
- Steps: Execute the manifest in dependency order and interrupt at every commit boundary.
- Expected result: Diagrams and replacement ADR content validate first, unsafe targets share a group, predecessor changes precede canonical links, canonical Markdown commits last, and architecture-review retains approval.
- Failure proves: Partial authoring exposes broken references or settles an ADR decision.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Dependency graph and commit-order fixtures.
- Required by milestone: M2

### T9. Batch outcomes preserve only safe completed targets

- Covers: R31-R39; E8; EC5-EC6; BND-STATE-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Complete batch, failure before writes, independent partial completion, unsafe group failure, and incomplete full manifest.
- Steps: Classify the batch result and inspect target files, progress, settlement, and handoff.
- Expected result: Only `complete` qualifies the full manifest for review, `partial-blocked` retains independently valid targets and reports both sets, and `blocked-before-write` changes no target file.
- Failure proves: Partial or unsafe work is misrepresented as complete architecture authoring.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Batch-result fixtures.
- Required by milestone: M2

### T10. Exact retry and recovery never rebind a transaction

- Covers: R28-R42; E6; EC3-EC4; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-002
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Interruption after each prepared or target write plus changed target, order, input, path, identity, dependency, group, authority, and concurrent state.
- Steps: Replay the identical or changed operation and compare files, evidence, entries, and transitions.
- Expected result: Exact retries resume once without duplication, changed manifests become new operations, and unrelated, dangling, ambiguous, or conflicting state stops.
- Failure proves: Recovery adopts unknown files, overwrites concurrency, or silently changes transaction identity.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Retry and recovery fixtures.
- Required by milestone: M2

### T11. Assets and preservation ledgers have one closed owner

- Covers: R43-R48; BND-INPUT-001, BND-COMPOSE-001, BND-COMPAT-001; INT-004
- Level: contract
- Command IDs: CMD1-CMD4
- Fixture/setup: Three assets, semantic rule ledger, literal ledger, asset disposition ledger, duplicate clusters, parser consumers, incidental tests, and unknown values.
- Steps: Validate ownership, copied structure, exact styles, destinations, classifications, and unknown-value behavior.
- Expected result: Assets own structure only, method policy has one reference owner, literal styles remain exact, every rule and literal has one treatment, and unknown values fail first.
- Failure proves: Extraction loses behavior, freezes incidental prose, or turns assets into policy owners.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md`
- Automation location: Change-local ledger and focused skill fixtures.
- Required by milestone: M1 and M2

### T12. Canonical and derived packages retain complete byte parity

- Covers: R1, R6-R7, R52-R53; E10; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004
- Level: integration
- Command IDs: CMD2, CMD4-CMD7
- Fixture/setup: Canonical package and freshly generated, archived, release-candidate, and installed adapter trees.
- Steps: Build packages, select `architecture`, and compare every required path and raw byte.
- Expected result: Every target contains both references and all three assets exactly once; missing, transformed, escaped, stale, additional, or mixed resources fail.
- Failure proves: Canonical validation does not guarantee the published package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T13. Measurements prove real loaded-context reduction

- Covers: R49-R51; BND-COMPAT-001; INT-004
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled with LF normalization and unique-file counting.
- Steps: Measure AA0, AA1, AA2, every procedure, every asset, representative copied output, duplicate clusters, and total package.
- Expected result: All three loaded assemblies use fewer words and bytes, total package change remains separately visible and justified, and no percentage overrides preservation.
- Failure proves: Relocation or file splitting is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local deterministic measurement assertions.
- Required by milestone: M3

### T14. Final deterministic acceptance respects the architecture boundary

- Covers: R53-R54; BND-RECOVERY-001, BND-ENV-001
- Level: smoke
- Command IDs: CMD1-CMD11
- Fixture/setup: Completed M1-M3 package and evidence, plus an authoring-evidence model unable to represent required manifests or dependencies.
- Steps: Run the full command ledger and test the architecture-escalation condition.
- Expected result: Deterministic repository proof passes without target-agent execution or an extra manual gate, while any need for a new schema, authority, persistence surface, or owner returns to architecture before implementation.
- Failure proves: Acceptance is nondeterministic or conceals an architecture change.
- Evidence artifact: `evidence/m3-package-proof.md`; final review and verify evidence
- Automation location: Existing repository validators and lifecycle review.
- Required by milestone: M3 and M4

## Fixtures and data

- Change-local YAML ledgers for semantic rules, literal consumers, and asset dispositions.
- Change-local scenarios for assemblies, classifications, assessment bases, target operations, prepared evidence, dependencies, commit groups, batch outcomes, retries, resource failures, and forbidden writes.
- Existing controlled skill and adapter fixtures extended only where focused `architecture` coverage is absent.
- Temporary canonical, diagram, and ADR trees representing absent, prepared, partial, complete, stale, ambiguous, conflicting, and concurrent states.

## Mocking/stubbing policy

Use temporary filesystem fixtures for architecture targets, change records, assessment receipts, prepared evidence, conditional resources, generated adapters, and interrupted writes. Do not mock away public resource assembly, applicability, governed-signal classification, lifecycle authority, dependency validation, commit points, or architecture-review handoff. No network, hosted service, target-agent runtime, publication, or external state mutation is required.

## Migration or compatibility tests

T11 proves separate semantic, literal, and asset ownership plus atomic parser-consumer treatment. T12 proves atomic migration across canonical and every derived package. T13 proves honest before-and-after accounting. Historical architecture documents, ADRs, and review evidence remain unchanged.

## Observability verification

T3-T10 verify visible classification, assessment basis, manifest state, target progress, batch outcome, blockers, retries, and settlement. T11-T13 verify disposition and measurement reports. No telemetry is introduced.

## Security/privacy verification

T2, T4-T10, T12, and T14 prove exact authority, safe paths, bounded writes, no unrecorded-file adoption, concurrency stops, fail-safe resources, absence of secrets, and no network or target-runtime dependency.

## Performance checks

AA0, AA1, and AA2 LF-normalized words and UTF-8 bytes are the required loaded-context metrics. Resource, asset, representative-output, and total-package sizes are reported separately. No wall-clock, tokenizer, or target-runtime benchmark is required.

## Manual QA checklist

None. Deterministic proof owns test acceptance; ordinary lifecycle review and human PR review retain their normal roles and are not represented as a new manual QA procedure.

## What not to test and why

- Do not execute or grade a target-agent runtime; this is a deterministic content and package refactor.
- Do not add a permanent tokenizer, prose classifier, architecture artifact validator, or simplicity validator; change-local evidence and existing owners are sufficient.
- Do not turn ordinary reviewer judgment into a scripted manual acceptance procedure or pre-implementation gate.
- Do not test publication, release, deployment, network, or destructive Git behavior because those systems do not change.
- Do not rewrite historical architecture or ADR artifacts solely for this refactor.
- Do not optimize `architecture-review` in this change.

## Uncovered gaps

None.

## Next artifacts

`test-spec-review`, then M1 implementation and code review if the proof map is approved.

## Follow-on artifacts

None yet.

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer approval, implementation readiness, validation success, verification, branch readiness, or PR readiness.
