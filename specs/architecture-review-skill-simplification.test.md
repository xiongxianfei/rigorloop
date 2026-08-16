<!-- Template: test-spec-skeleton-v1 -->

# Architecture-Review Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/architecture-review-skill-simplification.md`
- Plan: `docs/plans/2026-08-16-architecture-review-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-16-architecture-review-skill-simplification/architecture-assessment.md`; architecture is not required because the prepared settlement manifest remains ordinary formal-review Markdown evidence under existing lifecycle ownership

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/architecture-review-skill-simplification.md` | `spec` | `spec-review-r1`; `docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/spec-review-r1.md` |
| Architecture assessment | `docs/changes/2026-08-16-architecture-review-skill-simplification/architecture-assessment.md` | not applicable | Recorded `architecture-not-required` assessment |
| Execution plan | `docs/plans/2026-08-16-architecture-review-skill-simplification.md` | `plan` | `plan-review-r1`; `docs/changes/2026-08-16-architecture-review-skill-simplification/reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic contract fixtures for package loading, surface and authority classification, exact review subjects, governing bases, evidence-scoped dispositions, prepared settlement, retries, compatibility, measurement, and missing resources. Existing validators own permanent skill, lifecycle, boundary, build, and adapter checks. Change-local ledgers, scenarios, formal-review evidence fixtures, and measurements prove semantic disposition and real loaded-context reduction. No target-agent runtime or separate manual semantic-review acceptance gate is part of this proof map.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R10 | T1-T3, T12 | contract | Package inventory, universal ownership, exact mappings, missing resources, and shared-block parity. |
| R11-R19 | T4-T5 | contract | Closed surfaces, modes, valid authority combinations, durable-recording triggers, advisory isolation, and execution boundaries. |
| R20-R27 | T6-T7 | contract | Exact review subject, governing basis, optional target set, record-only identity, reuse, and staleness. |
| R28-R36 | T8-T9 | contract | One overall status, per-kind approved destinations, invalid ADR-intent stops, scoped findings and blockers, exact target dispositions, no partial approval, and settlement authority. |
| R37-R46 | T10-T11 | contract | Evidence-before-settlement, prepared manifests, per-target progress, exact retry, concurrency, and bounded writes. |
| R47-R52 | T3, T8, T13 | contract | Finding fields, compact results, semantic and literal ledgers, and unknown-value-first validation. |
| R53-R58 | T12-T14 | integration | Deterministic measurement, primary-profile reduction, package parity, portable text, runtime exclusion, and architecture fallback. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Command IDs | Required milestone | Notes |
| --- | --- | --- | --- | --- |
| AC1 | T1-T14 | CMD1-CMD11 | M1-M3 | Every R1-R58 requirement maps through requirement rows, exact proof obligations, and stable cases. |
| AC2 | T1-T2, T12 | CMD2-CMD7 | M2-M3 | The package has one universal file, exactly two references, and no new asset. |
| AC3 | T3 | CMD1, CMD3-CMD4 | M1-M2 | The shared block remains byte-identical and has one normative owner. |
| AC4 | T4-T5 | CMD1, CMD3 | M2 | Four surfaces, four assemblies, six valid combinations, and invalid combinations have direct proof. |
| AC5 | T6-T7 | CMD3, CMD9 | M2 | Every formal occurrence binds its subject and governing basis separately from optional targets. |
| AC6 | T8-T9 | CMD3, CMD9 | M2 | Non-approval approves no target and mutates only evidence-supported targets. |
| AC7 | T10-T11 | CMD3, CMD9 | M2 | Prepared intent precedes transition, and exact partial retry adopts no changed state. |
| AC8 | T3, T13 | CMD1, CMD3 | M1-M3 | Semantic and literal ledgers give each current rule and compatibility dependency one disposition. |
| AC9 | T13 | CMD1 | M3 | ARR1 and ARR1M shrink while total package growth remains visible. |
| AC10 | T12 | CMD2, CMD4-CMD7 | M3 | Canonical, generated, archived, release-candidate, and installed packages retain raw-byte parity. |
| AC11 | T14 | CMD1-CMD11 | M3 | Acceptance is deterministic and excludes target-agent execution and a separate manual semantic gate. |
| AC12 | T10, T14 | CMD1, CMD3, CMD9 | M1-M3 | Insufficient formal-review evidence capability returns to architecture before implementation. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T6 | A no-impact review binds exact assessment and upstream basis with no settlement targets. |
| E2 | T2 | Canonical and ADR review load the method reference exactly once. |
| E3 | T2 | Missing recording procedure stops before durable evidence or target mutation. |
| E4 | T7 | Changed governing basis requires a new review occurrence. |
| E5 | T8 | One affected ADR becomes revision-required while unaffected targets remain review-required. |
| E6 | T9 | Inconclusive review performs no target settlement by default. |
| E7 | T10 | The complete settlement manifest is durable before lifecycle mutation. |
| E8 | T11 | Partial physical settlement resumes only from exact recorded intent. |
| E9 | T11 | Concurrent target change blocks retry without adoption. |
| E10 | T5 | Advisory durable recording without a safe location reports blocked and creates no governed state. |
| E11 | T3 | The shared isolation block remains byte-identical through package migration. |
| E12 | T4 | Every unlisted authority combination fails before side effects. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R11, R12, R13, R14, R16, R28, R29, R40 | BND-INPUT-001 | T4, T8, T10, T13 | contract | automated | CMD1, CMD3 | `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R15, R19, R24, R25, R28, R30, R31, R32, R33, R34, R35, R36, R37, R38, R40, R41, R42, R43, R44, R45, R46 | BND-STATE-001 | T5-T11 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R13, R14, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R29, R36 | BND-AUTH-001 | T4-T9 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R16, R22, R23, R49, R50, R51, R55, R57 | BND-COMPOSE-001 | T1-T3, T6, T12-T13 | integration | automated | CMD1-CMD8 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R26, R27, R37, R38, R39, R40, R41, R42, R43, R44, R45 | BND-TEMPORAL-001 | T7, T10-T11 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R7, R14, R18, R25, R34, R37, R38, R41, R42, R43, R44, R45, R46, R58 | BND-RECOVERY-001 | T2, T5-T7, T9-T11, T14 | contract | automated | CMD1-CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R8, R9, R10, R47, R48, R50, R51, R52, R53, R54, R55, R57 | BND-COMPAT-001 | T3, T12-T13 | integration | automated | CMD1-CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R7, R17, R18, R45, R55, R56 | BND-ENV-001 | T2, T5, T11-T12, T14 | integration | automated | CMD2, CMD4-CMD9 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R13, R14, R17, R18, R19 | INT-001 | T4-T5 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R20, R21, R23, R24, R25, R26, R27 | INT-002 | T6-T7 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R28, R29, R31, R32, R33, R35 | INT-003 | T8-T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R37, R38, R39, R41, R42, R43, R44, R45 | INT-004 | T10-T11 | contract | automated | CMD1, CMD3, CMD9 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-013 | covered | R8, R9, R10, R50, R51, R54, R55, R57 | INT-005 | T3, T12-T13 | integration | automated | CMD1-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| EC1: formal record-only review lacks a stable subject | T6 | Block formal recording or remain advisory without inventing a lifecycle target. |
| EC2: architecture method changes after review | T7 | Reject identical retry and require a new occurrence. |
| EC3: one ADR has a material finding in a combined subject | T8 | Move only that ADR to revision-required and leave other targets review-required. |
| EC4: review-occurrence blocker prevents recording | T9 | Record the blocker when possible and perform no target settlement. |
| EC5: target-set-wide conflict is evidenced | T9 | Block all exact targets without implying any approval. |
| EC6: manifest is prepared before any target transition | T10-T11 | Exact retry revalidates the same intent and begins only pending writes. |
| EC7: one target already matches expected post-state and progress | T11 | Verify it without duplicating settlement evidence. |
| EC8: target state changes independently after preparation | T11 | Block retry without adoption or unrelated mutation. |
| EC9: authoring evidence records ADR intent as `accepted` or `active` | T8 | Set each ADR to its exact recorded state while canonical architecture becomes `approved`. |
| EC10: intended ADR state is missing or ambiguous | T8 | Block the complete settlement, leave every target unchanged at `review-required`, and grant no downstream eligibility. |
| Unknown closed-vocabulary value | T4, T8, T10, T13 | Reject it before any consistency check. |
| Required resource is missing, escaped, transformed, or mixed-version | T2, T12 | Stop dependent work and fail package parity. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-skill-validator.py ArchitectureReviewSkillSimplificationLedgerTests` | planned-for-implementation | M1 implementation | M1 | M1 | Stop M1 and retain the failing ledger, vocabulary, scenario, capability, or measurement fixture. | A missing class or zero-test result fails. | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | Deterministic change-local fixtures only. |
| CMD2 | `python scripts/validate-skills.py skills/architecture-review/SKILL.md` | existing/configured | repository skill validation | M2 | M2 | Stop on structural, mapping, path, or resource failure. | Not applicable. | `evidence/m2-package-implementation.md` | Reads the canonical skill package only. |
| CMD3 | `python scripts/test-skill-validator.py ArchitectureReviewSkillSimplificationTests` | planned-for-implementation | M2 implementation | M2 | M2 | Stop on any focused contract regression. | A missing class or zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local deterministic tests only. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | repository skill validation | M2 | M2 | Stop on any skill-contract regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local tests only. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | repository package validation | M2 | M2 | Stop on build or package regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-owned temporary package fixtures. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | repository package generation | M2 | M2 | Stop on stale or invalid generated skill output. | Not applicable. | `evidence/m2-package-implementation.md` | Check mode does not publish packages. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | repository adapter validation | M3 | M3 | Stop on generated, archived, release-candidate, or installed parity failure. | A zero-test result fails. | `evidence/m3-package-proof.md` | Uses temporary adapter trees; no publication. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/architecture-review-skill-simplification.md` | existing/configured | boundary contract validation | M3 | M3 | Stop on incomplete requirement, boundary, interaction, or proof mapping. | Not applicable. | `evidence/m3-package-proof.md` | Read-only structural validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml` | existing/configured | lifecycle metadata validation | all | test-spec-review | Stop on invalid lifecycle or artifact metadata. | Not applicable. | stage-owned lifecycle evidence | Read-only metadata validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-16-architecture-review-skill-simplification` | existing/configured | review evidence validation | all | test-spec-review | Stop on incomplete or inconsistent review evidence. | Not applicable. | change-local review records | Read-only review validation. |
| CMD11 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | ci-owned | repository PR validation | M4 | final verify | Stop final closeout on any required CI failure. | A zero-test result fails where the selected command owns tests. | final verify report | Repository-owned PR-mode checks; no publication. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T3-T7, T10, T13 | none | CMD1, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | M1 code review | Freeze rules, literals, scenarios, evidence capability, and measurements before canonical edits. |
| M2 | T1-T11, T13 | none | CMD1-CMD6, CMD9 | `evidence/m2-package-implementation.md` | M2 code review | Prove package loading, shared bytes, review identity, scoped dispositions, prepared settlement, and recovery. |
| M3 | T12-T14 | none | CMD2, CMD4-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code review and final closeout | Prove real-profile reduction, boundary proof, lifecycle validity, and package parity. |
| M4 | T14 | none | CMD1-CMD11 | final review, explanation, and verify evidence | PR handoff | Run holistic deterministic closeout after implementation milestones and resolution are closed. |

## Test cases

### T1. Universal and conditional package ownership is exact

- Covers: R1-R6; AC2; BND-COMPOSE-001
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Canonical package plus all four loaded-assembly contexts.
- Steps: Resolve each assembly and inspect universal and conditional ownership.
- Expected result: ARR0 loads only `SKILL.md`, ARR0M adds the method reference, ARR1 adds the recording reference, ARR1M adds both, each reference loads once, and no asset is added.
- Failure proves: Universal safety moved behind a trigger or conditional procedure loads on the wrong path.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill contract fixtures.
- Required by milestone: M2

### T2. Missing or invalid resources fail before dependent work

- Covers: R6-R7; E2-E3; BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Missing, unreadable, escaped, stale, contradictory, and mixed-version references.
- Steps: Trigger each reference and attempt dependent method judgment, recording, or settlement.
- Expected result: The invocation names the blocker and stops before reconstruction, durable writes, target mutation, automation, or dependent claims.
- Failure proves: Package failure can weaken review or lifecycle safety.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Resource-map and temporary package fixtures.
- Required by milestone: M2

### T3. Shared recording bytes and preservation ownership remain exact

- Covers: R8-R10, R47-R52; E11; BND-INPUT-001, BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: contract
- Command IDs: CMD1, CMD3-CMD4
- Fixture/setup: Shared template, canonical skill, both ledgers, duplicate clusters, parser consumers, incidental tests, and unknown classifications.
- Steps: Compare shared bytes and validate every semantic and literal disposition.
- Expected result: Exactly one inline block matches the template byte-for-byte, the recording reference does not restate it, every rule and literal has one treatment, and unknown values fail first.
- Failure proves: Extraction changes normative shared policy, loses behavior, or freezes incidental prose.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md`
- Automation location: Change-local ledgers and focused skill fixtures.
- Required by milestone: M1 and M2

### T4. Surface, mode, and authority vocabularies route deterministically

- Covers: R11-R16; E12; BND-INPUT-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Four surfaces, three recording modes, two settlement modes, two execution modes, six valid combinations, representative invalid combinations, and unknown values.
- Steps: Classify each invocation and inspect loaded resources and available writes.
- Expected result: Known combinations map exactly, unknown and unlisted combinations fail first, and loading never grants mutation or routing authority.
- Failure proves: Review classification or side-effect authority is open-ended.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Closed-vocabulary and authority fixtures.
- Required by milestone: M2

### T5. Durable recording and isolation obey bounded authority

- Covers: R15, R17-R19; E10; BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001, BND-ENV-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Clean non-formal review, formal review, explicit advisory recording with valid and invalid paths, material outcomes, and manual or workflow-managed execution.
- Steps: Resolve recording requirement, location, writes, and handoff for each case.
- Expected result: Formal and material outcomes record, advisory writes remain standalone, unsafe location reports blocked with complete output, manual execution stays isolated, and automation returns control without routing itself.
- Failure proves: Recording or execution mode silently acquires governed authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Recording and path fixtures.
- Required by milestone: M2

### T6. Every formal surface binds an exact subject and optional targets

- Covers: R20-R25; E1; EC1; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Canonical package, ADR, no-impact, proposal/spec-gap, and unresolved record-only subjects.
- Steps: Build the subject, governing basis, and settlement-target set for each surface.
- Expected result: Artifact surfaces bind exact package or ADR identities, record-only surfaces bind exact upstream evidence with an empty target set, and unstable identity blocks formal recording without inventing an artifact.
- Failure proves: A formal occurrence is identity-free or a record-only review creates settlement authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Review-subject fixtures.
- Required by milestone: M2

### T7. Judgment reuse requires an unchanged complete basis

- Covers: R20-R27; E4; EC2; BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Exact review identities plus changed spec, spec review, assessment, decision basis, method contract, repository revision, target identity, and target order.
- Steps: Attempt judgment reuse and identical retry for unchanged and changed cases.
- Expected result: Exact identity reuses one judgment, while any decision-bearing change requires a new occurrence and creates no settlement write.
- Failure proves: Stale architecture judgment can be replayed against a different basis.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Identity and staleness fixtures.
- Required by milestone: M2

### T8. Settlement status and findings mutate only supported targets

- Covers: R28-R32, R34-R36, R47-R49; E5; EC3, EC9-EC10; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-003
- Level: contract
- Command IDs: CMD1, CMD3, CMD9
- Fixture/setup: Combined subjects containing canonical architecture and ADR targets whose current authoring evidence records `accepted`, records `active`, omits intended ADR state, or provides ambiguous intended ADR state, plus one-target changes-requested, target-scoped blocked, target-set blocked, and review-occurrence blocked outcomes.
- Steps: Derive and apply the expected post-state for every exact target, then exercise each finding and blocker scope.
- Expected result: Approved canonical architecture becomes `approved`; ADRs become exactly `accepted` or `active` according to current authoring evidence; missing or ambiguous intended ADR state blocks the complete settlement, leaves every target unchanged at `review-required`, and grants no downstream eligibility; changes-requested affects only named targets; scoped blockers affect only supported targets; occurrence blockers settle none; and every non-approved result grants no eligibility.
- Failure proves: Approval invents or ignores an ADR destination, invalid ADR intent permits partial mutation, or one overall non-approval status over-mutates targets or creates partial approval.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Finding, blocker, and lifecycle fixtures.
- Required by milestone: M2

### T9. Inconclusive and authority failures preserve unsupported state

- Covers: R28-R36; E6; EC4-EC5; BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD3, CMD9
- Fixture/setup: Inconclusive evidence, recording failure, stale authority, ambiguous target, invalid lifecycle state, and exact target-set blockers.
- Steps: Attempt settlement and inspect every target and eligibility result.
- Expected result: Inconclusive and occurrence failures leave targets review-required by default, only separately evidenced blockers may block targets, and no case grants approval or continuation.
- Failure proves: Epistemic uncertainty becomes unsupported lifecycle mutation.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Negative settlement fixtures.
- Required by milestone: M2

### T10. Prepared settlement evidence is durable before target mutation

- Covers: R37-R42, R58; E7; EC6; BND-INPUT-001, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-004
- Level: contract
- Command IDs: CMD1, CMD3, CMD9
- Fixture/setup: Review evidence capable and incapable of recording complete subject, basis, target pre-state, disposition, expected post-state, and progress.
- Steps: Interrupt before review recording, before manifest preparation, after preparation, and before the first target transition.
- Expected result: All review evidence and a complete prepared manifest exist before mutation, incomplete evidence changes no target, manifest states reject unknown values, and insufficient evidence capability routes to architecture.
- Failure proves: Settlement relies on in-memory or reconstructed intent or conceals a new architecture requirement.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md`
- Automation location: Prepared-manifest and interruption fixtures.
- Required by milestone: M1 and M2

### T11. Exact partial retry never rebinds or duplicates settlement

- Covers: R41-R46; E8-E9; EC6-EC8; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004
- Level: contract
- Command IDs: CMD3, CMD9
- Fixture/setup: Interruption after each target write plus exact replay, already-complete target, changed basis, order, identity, state, authority, manifest, and concurrent mutation.
- Steps: Reconcile each partial state against its prepared manifest.
- Expected result: Exact retry completes only pending matching writes once, verifies completed targets without duplication, marks complete only after all targets match, and every changed condition blocks without adoption or unrelated mutation.
- Failure proves: Recovery reconstructs intent, overwrites concurrency, or creates duplicate review evidence.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Retry, concurrency, and lifecycle fixtures.
- Required by milestone: M2

### T12. Canonical and derived packages retain complete byte parity

- Covers: R1, R6-R10, R55, R57; E3, E11; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005
- Level: integration
- Command IDs: CMD2, CMD4-CMD7
- Fixture/setup: Canonical package and freshly generated, archived, release-candidate, and installed Codex, Claude, and opencode trees.
- Steps: Build packages, select `architecture-review`, and compare every required path and raw byte.
- Expected result: Every target contains both references exactly once, no asset appears, shared bytes remain exact, and missing, transformed, escaped, stale, additional, or mixed resources fail.
- Failure proves: Canonical validation does not guarantee the published package.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T13. Measurements prove real formal-profile reduction

- Covers: R50-R54; BND-INPUT-001, BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled with LF normalization and unique-file counting.
- Steps: Measure ARR0, ARR0M, ARR1, ARR1M, each reference, duplicate ownership, and total package.
- Expected result: ARR1 and ARR1M use fewer words and bytes, all other measurements remain visible, total package change is justified, and no fixed percentage overrides preservation.
- Failure proves: Relocation or file splitting is misreported as simplification.
- Evidence artifact: `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local deterministic measurement assertions.
- Required by milestone: M3

### T14. Final deterministic acceptance respects architecture and runtime boundaries

- Covers: R55-R58; BND-RECOVERY-001, BND-ENV-001
- Level: smoke
- Command IDs: CMD1-CMD11
- Fixture/setup: Completed M1-M3 package and evidence plus a formal-review evidence model unable to represent the required manifest.
- Steps: Run the full command ledger and test the architecture-escalation condition.
- Expected result: Deterministic repository proof passes without target-agent execution or an extra manual gate, while any need for a new schema, persistent record, lifecycle state, or owner returns to architecture before implementation.
- Failure proves: Acceptance is nondeterministic or conceals an architecture change.
- Evidence artifact: `evidence/m3-package-proof.md`; final review and verify evidence
- Automation location: Existing repository validators and lifecycle review.
- Required by milestone: M3 and M4

## Fixtures and data

- Change-local YAML ledgers for semantic rules and literal consumers.
- Change-local scenarios for assemblies, surfaces, authority combinations, subjects, bases, target dispositions, prepared manifests, retries, resource failures, and forbidden writes.
- Existing controlled skill and adapter fixtures extended only where focused `architecture-review` coverage is absent.
- Temporary review evidence and change records representing absent, prepared, partial, complete, stale, ambiguous, conflicting, and concurrent states.

## Mocking/stubbing policy

Use temporary filesystem fixtures for review subjects, governing artifacts, change records, formal-review evidence, conditional references, generated adapters, and interrupted writes. Do not mock away public resource assembly, review-surface classification, recording requirement, lifecycle authority, prepared evidence, compare-and-set behavior, or workflow handoff. No network, hosted service, target-agent runtime, publication, or external state mutation is required.

## Migration or compatibility tests

T3 proves separate semantic and literal ownership plus exact shared-block parity. T12 proves atomic migration across canonical and every derived package. T13 proves honest before-and-after accounting. Historical architecture reviews and lifecycle evidence remain unchanged.

## Observability verification

T4-T11 verify visible surface, mode, subject, governing basis, target dispositions, manifest state, per-target progress, blockers, retries, and settlement results. T3 and T13 verify disposition and measurement reports. No telemetry is introduced.

## Security/privacy verification

T2, T4-T12, and T14 prove exact authority, safe paths, bounded writes, no identity-free formal record, no changed-state adoption, fail-safe resources, absence of secrets, and no network or target-runtime dependency.

## Performance checks

ARR1 and ARR1M LF-normalized words and UTF-8 bytes are the required loaded-context acceptance metrics. ARR0, ARR0M, each reference, and total-package size are reported separately. No wall-clock, tokenizer, or target-runtime benchmark is required.

## Manual QA checklist

None. Deterministic proof owns test acceptance; ordinary lifecycle review and human PR review retain their normal roles and are not represented as a new manual QA procedure.

## What not to test and why

- Do not execute or grade a target-agent runtime; this is a deterministic content and package refactor.
- Do not add a permanent tokenizer, prose classifier, architecture artifact validator, or simplicity validator; change-local evidence and existing owners are sufficient.
- Do not turn ordinary reviewer judgment into a scripted manual acceptance procedure or pre-implementation gate.
- Do not test publication, release, deployment, network, or destructive Git behavior because those systems do not change.
- Do not rewrite historical architecture-review evidence solely for this refactor.
- Do not optimize `architecture` or another review skill in this change.

## Uncovered gaps

None.

## Next artifacts

`test-spec-review`, then M1 implementation and code review if the proof map is approved.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. This artifact does not claim peer-review approval, implementation readiness, validation, verification, branch readiness, or PR readiness.
