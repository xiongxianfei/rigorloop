<!-- Template: test-spec-skeleton-v1 -->

# Learn Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-16-learn-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/learn-skill-simplification.md`
- Plan: `docs/plans/2026-08-17-learn-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-16-learn-skill-simplification/architecture-assessment.md`; architecture is not required because stable routes remain ordinary learn-owned Markdown and no recovery, registry, polling, integration, or cross-owner mutation mechanism is introduced

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/learn-skill-simplification.md` | `spec` | `spec-review-r2`; `docs/changes/2026-08-16-learn-skill-simplification/reviews/spec-review-r2.md` |
| Architecture assessment | `docs/changes/2026-08-16-learn-skill-simplification/architecture-assessment.md` | not applicable | `architecture-assessment-001`; `architecture-not-required` |
| Execution plan | `docs/plans/2026-08-17-learn-skill-simplification.md` | `plan` | `plan-review-r2`; `docs/changes/2026-08-16-learn-skill-simplification/reviews/plan-review-r2.md`; settlement retry receipt at `evidence/plan-settlement-retry.md` |

## Testing strategy

Use deterministic contract fixtures for package loading, operation classification, trigger ownership, session path selection, fail-closed interruption, contributor confirmation, topic effects, stable route rows, completion-kind matching, exact owner-result backlinks, historical compatibility, legacy cross-spec dispositions, architecture triggers, and missing resources. Existing validators own permanent skill, lifecycle, boundary, build, and adapter checks. Change-local ledgers, scenarios, and measurements prove semantic preservation and both real loaded-profile reductions. No target-agent runtime, transcript grading, live external mutation, or separate manual semantic-review acceptance gate is part of this proof map.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R6 | T1, T13 | contract, integration | Exact package, universal ownership, one session reference, one-time loading, and missing-resource stops. |
| R7-R10 | T2 | contract | Two operations, direct invocation, removed assessment surface, and trigger-owner closeout. |
| R11-R18 | T3 | contract | Session basis, canonical path, suffix collision, first write, durable outcome, no partial resume, complete rerun, and changed basis. |
| R19-R24 | T4-T6 | contract | Evidence truth, confirmation boundary, classifications, topic ownership, and idempotent topic effects. |
| R25-R26, R26a, R27-R30 | T7 | contract | Stable route IDs, complete fields, immutable completion kinds, closed settlements, and route meanings. |
| R31-R35 | T8-T9 | contract | Exact owner-result input, bounded write set, idempotency, completion-kind validation, and same-turn destination ownership. |
| R36 | T10 | contract | Prospective compatibility preserves historical sessions without implicit migration. |
| R37 | T15 | contract | The complete compact result is asserted for both operations and representative idempotent and blocked outcomes. |
| R38-R40, R47 | T9, T11 | contract | Semantic and literal ledgers, unknown-value-first validation, and exact legacy dispositions. |
| R41-R45 | T12-T14 | integration | Measurement, both-profile reduction, package parity, deterministic acceptance, and portability. |
| R46 | T16 | contract | M1 detects every architecture trigger and stops before canonical mutation. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Command IDs | Required milestone | Notes |
| --- | --- | --- | --- | --- |
| AC1 | T1-T16 | CMD1-CMD10 | M1-M3 | Every R1-R47 clause maps to stable cases and exact proof obligations. |
| AC2 | T1, T13 | CMD2-CMD7 | M2-M3 | One universal skill, one mapped reference, and no asset, template, or script. |
| AC3 | T2 | CMD1, CMD3 | M2 | Direct sessions and exact result recording are the only operations; trigger assessment is absent. |
| AC4 | T3 | CMD1, CMD3 | M2 | Collision, interruption, changed basis, complete rerun, and concurrency have one result. |
| AC5 | T5, T9 | CMD1, CMD3 | M2 | Confirmation never grants destination mutation. |
| AC6 | T7 | CMD1, CMD3 | M2 | Every new derivative route has stable identity, fields, completion kind, and settlement. |
| AC7 | T8-T9 | CMD1, CMD3 | M2 | Backlink completion remains narrow and owner-result kinds must match. |
| AC8 | T10 | CMD1, CMD3 | M2 | Historical sessions stay readable, unchanged, and ineligible for implicit result recording. |
| AC9 | T11 | CMD1, CMD3 | M1-M3 | Semantic and literal ledgers close every current rule and compatibility dependency. |
| AC10 | T12 | CMD1 | M3 | LR0 and LR1 both shrink while resource and total-package sizes remain visible. |
| AC11 | T13 | CMD2, CMD4-CMD7 | M3 | Canonical, generated, archived, release-candidate, and installed resources retain raw-byte parity. |
| AC12 | T14 | CMD2, CMD4-CMD11 | M3 | Acceptance is deterministic and excludes target-agent execution and a separate manual semantic gate. |
| AC13 | T16 | CMD1, CMD9 | M1 | Any persistent recovery, polling, integration, or new ownership need returns to architecture before M2. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1-T2 | Direct invocation selects a session and loads the method reference once. |
| E2 | T3 | Occupied base and `-2` paths select `-3` without overwrite. |
| E3 | T3 | Partial prior content is not resumed, repaired, adopted, or overwritten. |
| E4 | T5 | Pending confirmation records the decision and performs no dependent effect. |
| E5 | T7, T9 | Specification work becomes a pending exact owner-bound route, not a learn write. |
| E6 | T8 | Exact owner-produced specification identity completes only the matching backlink. |
| E7 | T8 | Repeating the same backlink is an idempotent no-op. |
| E8 | T8 | A different existing or supplied identity blocks replacement. |
| E9 | T10 | Historical sessions remain readable but cannot be implicitly upgraded. |
| E10 | T4 | A no-observation or no-lesson session records its durable outcome. |
| E11 | T1 | Missing session method stops before session creation. |
| E12 | T2 | Trigger-owner no-learn closeout remains outside learn. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R26a, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R7, R8, R11, R21, R22, R25, R26a, R27, R31, R34 | BND-INPUT-001 | T2-T3, T5, T7-T8 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R9, R10, R14, R15, R16, R17, R18, R21, R23, R24, R27, R28, R29, R30, R32, R33, R36 | BND-STATE-001 | T2-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R8, R9, R10, R11, R18, R20, R21, R23, R25, R26, R26a, R31, R32, R33, R34, R35, R47 | BND-AUTH-001 | T2-T9, T11 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R6, R12, R13, R23, R36, R37, R38, R39, R43, R45 | BND-COMPOSE-001 | T1, T3, T6, T10-T13, T15 | integration | automated | CMD1-CMD8 | `evidence/m2-package-implementation.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R12, R13, R16, R17, R18, R24, R25, R32, R33, R36 | BND-TEMPORAL-001 | T3, T6-T8, T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R6, R13, R15, R16, R17, R21, R24, R30, R32, R33 | BND-RECOVERY-001 | T1, T3, T5-T8 | contract | automated | CMD1-CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R36, R38, R39, R40, R41, R42, R43, R45, R47 | BND-COMPAT-001 | T9-T13 | integration | automated | CMD1-CMD8 | `evidence/m1-preservation-inventories.md`; `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R6, R11, R12, R13, R19, R23, R31, R34, R43, R44 | BND-ENV-001 | T1, T3-T4, T6, T8, T13-T14 | integration | automated | CMD2, CMD4-CMD9 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R8, R9, R10, R11 | INT-001 | T2 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R12, R13, R14, R16, R18 | INT-002 | T3 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R20, R21, R23, R25, R26, R26a, R31, R32, R34, R35, R47 | INT-003 | T5, T7-T9 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R27, R28, R29, R31, R32, R33, R36 | INT-004 | T7-T10 | contract | automated | CMD1, CMD3 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-013 | covered | R3, R5, R6, R38, R39, R42, R43, R45 | INT-005 | T1, T11-T13 | integration | automated | CMD1-CMD8 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-014 | covered | R46 | BND-RECOVERY-001 | T16 | contract | automated | CMD1, CMD9 | `evidence/m1-preservation-inventories.md` | M1 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected handling |
| --- | --- | --- |
| EC1: route named without a session | T2, T8 | Operation classification or input validation blocks before writes. |
| EC2: candidate path becomes occupied before creation | T3 | Recompute an absent suffix or stop without overwrite. |
| EC3: evidence becomes insufficient after Frame | T4 | Preserve the bounded durable outcome and create no derivative route. |
| EC4: contributor rejects confirmation | T5 | Perform no confirmation-dependent topic or route effect. |
| EC5: two routes name different owners | T7 | Assign independent ascending IDs and settlements. |
| EC6: expected destination path exists without exact identity | T8 | Keep pending or block; never infer completion. |
| EC7: scheduled follow-up is supplied for authoritative-artifact route | T8 | Reject the completion-kind mismatch and leave the route pending. |
| EC8: historical session resembles the new table without stable IDs | T10 | Do not infer or insert route identities. |
| EC9: canonical reference is absent from one adapter | T13 | Package validation fails. |
| EC10: total package grows while only one profile shrinks | T12 | Acceptance fails because LR0 and LR1 must both shrink. |
| EC11: authoritative-artifact route receives scheduled follow-up | T8 | Result recording stops without changing the route. |
| Unknown operation, classification, completion kind, settlement, or ledger value | T2, T5, T7, T11 | Reject the unknown value before consistency checks. |
| Missing, escaped, stale, contradictory, or mixed-version reference | T1, T13 | Stop dependent work and fail package parity. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-skill-validator.py LearnSkillSimplificationLedgerTests` | planned-for-implementation | M1 implementation | M1 | M1 | Stop M1 and retain the failing ledger, vocabulary, caller, scenario, architecture-trigger, or measurement fixture. | A missing class or zero-test result fails. | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | Deterministic change-local fixtures only. |
| CMD2 | `python scripts/validate-skills.py skills/learn/SKILL.md` | existing/configured | repository skill validation | M2 | M2 | Stop on structural, mapping, path, or resource failure. | Not applicable. | `evidence/m2-package-implementation.md` | Reads the canonical learn package only. |
| CMD3 | `python scripts/test-skill-validator.py LearnSkillSimplificationTests` | planned-for-implementation | M2 implementation | M2 | M2 | Stop on any focused operation, session, route, authority, or compatibility regression. | A missing class or zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local deterministic tests only. |
| CMD4 | `python scripts/test-skill-validator.py` | existing/configured | repository skill validation | M2 | M2 | Stop on any skill-contract regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-local tests only. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | repository package validation | M2 | M2 | Stop on build or package regression. | A zero-test result fails. | `evidence/m2-package-implementation.md` | Repository-owned temporary package fixtures. |
| CMD6 | `python scripts/build-skills.py --check` | existing/configured | repository package generation | M2 | M2 | Stop on stale or invalid generated skill output. | Not applicable. | `evidence/m2-package-implementation.md` | Check mode does not publish packages. |
| CMD7 | `python scripts/test-adapter-distribution.py` | existing/configured | repository adapter validation | M3 | M3 | Stop on generated, archived, release-candidate, or installed parity failure. | A zero-test result fails. | `evidence/m3-package-proof.md` | Uses temporary adapter trees; no publication. |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/learn-skill-simplification.md` | existing/configured | boundary contract validation | M3 | M3 | Stop on incomplete requirement, boundary, interaction, or proof mapping. | Not applicable. | `evidence/m3-package-proof.md` | Read-only structural validation. |
| CMD9 | `python scripts/validate-change-metadata.py docs/changes/2026-08-16-learn-skill-simplification/change.yaml` | existing/configured | lifecycle metadata validation | all | test-spec-review | Stop on invalid lifecycle or artifact metadata. | Not applicable. | stage-owned lifecycle evidence | Read-only metadata validation. |
| CMD10 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-16-learn-skill-simplification` | existing/configured | review evidence validation | all | test-spec-review | Stop on incomplete or inconsistent review evidence. | Not applicable. | change-local review records | Read-only review validation. |
| CMD11 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | ci-owned | repository PR validation | M4 | final verify | Stop final closeout on any required CI failure. | A zero-test result fails where the selected command owns tests. | final verify report | Repository-owned PR-mode checks; no publication. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T11-T12, T16 | none | CMD1, CMD9 | `evidence/m1-preservation-inventories.md`; `evidence/profile-size-baseline.md` | M1 code review | Freeze rules, literals, callers, legacy dispositions, scenarios, architecture triggers, and measurements before canonical edits. Every M1 case is runnable through CMD1. |
| M2 | T1-T10, T15 | none | CMD1-CMD6, CMD9 | `evidence/m2-package-implementation.md` | M2 code review | Prove package loading, session behavior, confirmation, topics, stable routes, exact backlinks, ownership, historical compatibility, and compact results. |
| M3 | T11-T14 | none | CMD2, CMD4-CMD10 | `evidence/simplification-measurements.md`; `evidence/semantic-preservation-review.md`; `evidence/m3-package-proof.md` | M3 code review and final closeout | Prove both-profile reduction, boundary proof, lifecycle validity, and package parity. |
| M4 | T14 | none | CMD1-CMD11 | final review, explanation, and verify evidence | PR handoff | Run holistic deterministic closeout after implementation milestones and resolution are closed. |

## Test cases

### T1. Universal and conditional package ownership is exact

- Covers: R1-R6; E1, E11; AC2; BND-COMPOSE-001, BND-RECOVERY-001
- Level: contract
- Command IDs: CMD2-CMD4
- Fixture/setup: Canonical package plus LR0 and LR1 contexts and missing, unreadable, escaped, stale, contradictory, and mixed-version reference variants.
- Steps: Resolve both assemblies, inspect rule ownership, and trigger each resource failure.
- Expected result: LR0 loads only `SKILL.md`; LR1 loads `SKILL.md` then `session-method.md` once; no asset, template, or script exists; resource failure stops before session creation or dependent judgment.
- Failure proves: Universal safety moved behind the trigger or package failure can weaken learn behavior.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused skill and temporary package fixtures.
- Required by milestone: M2

### T2. Operation and trigger ownership classify before writes

- Covers: R7-R10; E12; EC1; BND-INPUT-001, BND-STATE-001, BND-AUTH-001; INT-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Direct `$learn`, exact route-result request, ordinary question, trigger-owner closeout, missing route input, combined request, and unknown operation.
- Steps: Classify the operation and inspect permitted writes.
- Expected result: Direct learn selects `run-learn-session`; exact result input selects `record-learn-route-result`; no assessment operation exists; trigger-owner closeout creates no learn artifact; invalid inputs fail before writes.
- Failure proves: An artificial operation or ambiguous prompt acquires learn-owned mutation authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Operation and caller fixtures.
- Required by milestone: M2

### T3. Session path creation, collision, and interruption fail safely

- Covers: R11-R18; E2-E3; EC2; BND-INPUT-001, BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-002
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Absent base path, occupied base and suffixes, concurrent occupation, unsafe slug, complete session, partial session, and changed trigger, scope, or basis.
- Steps: Resolve and create each session candidate and attempt repeats or collisions.
- Expected result: The lowest absent suffix is selected and rechecked; first creation records identity and complete Frame; partial or competing bytes are never resumed or overwritten; exact complete rerun is idempotent; changed basis gets a new path.
- Failure proves: Historical evidence can be adopted, overwritten, or rebound silently.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Temporary session-path fixtures.
- Required by milestone: M2

### T4. Observation and durable outcomes remain evidence-bound

- Covers: R15, R19, R22; E10; EC3; BND-STATE-001, BND-ENV-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Recorded evidence, bounded inference, unavailable transcript, sensitive incident detail, no observation, no reusable lesson, and insufficient evidence after Frame.
- Steps: Run Observe and Classify against each evidence state.
- Expected result: Claims distinguish observation, inference, unknown, and exclusion; sensitive content is minimized; every started session records a bounded outcome; no unsupported lesson or route is manufactured.
- Failure proves: Learn overclaims evidence or loses required session history.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Evidence-selection and sensitive-data fixtures.
- Required by milestone: M2

### T5. Contributor confirmation gates topic and route effects only

- Covers: R20-R22; E4; EC4; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001; INT-003
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Pending, confirmed, rejected, and unknown confirmation values across every primary classification.
- Steps: Attempt classification, topic write, route creation, destination mutation, and workflow continuation.
- Expected result: Pending and rejected states record no dependent effect; confirmed classification permits only learn-owned topic or route work; unknown values fail first; no state grants destination or workflow authority.
- Failure proves: Human confirmation is treated as universal mutation authority.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Confirmation and authority fixtures.
- Required by milestone: M2

### T6. Confirmed topic effects are exact and idempotent

- Covers: R23-R24; BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: New confirmed topic, identical repeat, conflicting content, higher-priority authority conflict, and unsafe topic path.
- Steps: Apply and repeat the topic effect with exact session and content identities.
- Expected result: Valid guidance records a session backlink; identical repeat is a no-op; conflict or unsafe path blocks; topic guidance never becomes authoritative policy.
- Failure proves: Topic curation overwrites conflict or changes source-of-truth ownership.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Topic-effect fixtures.
- Required by milestone: M2

### T7. Stable route rows have closed identity and state

- Covers: R25-R30; E5; EC5; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001; INT-003-INT-004
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Multiple confirmed routes, duplicate or renumbered IDs, both completion kinds, all settlements, missing fields, and unknown values.
- Steps: Create route rows and validate their ordered fields and transitions.
- Expected result: IDs begin at ROUTE-001 and rise without reuse; every field is present; completion kind is immutable; settlements have narrow meanings; unknown or inconsistent values fail first.
- Failure proves: Later result recording cannot identify or interpret one exact route safely.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Route-row contract fixtures.
- Required by milestone: M2

### T8. Owner-result recording is bounded, kind-matched, and idempotent

- Covers: R29, R31-R34; E6-E8; EC1, EC6-EC7, EC11; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Exact artifact result, exact permitted follow-up, missing identity, wrong kind, wrong owner, stale basis, identical backlink, different existing backlink, and concurrent session edit.
- Steps: Record each result and compare all session, topic, destination, workflow, and route fields.
- Expected result: Only an exact kind-matched result updates the matching backlink and settlement; identical repeat is a no-op; every mismatch stops; no other field or surface changes.
- Failure proves: Result recording becomes polling, reconciliation, replacement, or cross-owner settlement.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Route-result and concurrent-write fixtures.
- Required by milestone: M2

### T9. Destination owners satisfy legacy authoritative outcomes

- Covers: R20, R32, R35, R47; E5-E6; AC5, AC7; BND-AUTH-001, BND-COMPAT-001; INT-003
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Exact dispositions for legacy R21-R24, R33, Example E3, outputs, invariant, and acceptance surface plus separately authorized same-turn owner execution.
- Steps: Trace classification, route creation, destination mutation, destination review gate, and backlink recording.
- Expected result: Learn never writes the destination; owner-produced authoritative outcomes remain mandatory; same-turn work uses the owning skill; the session links the exact result without claiming its lifecycle state.
- Failure proves: The amendment leaves two writers or weakens required authoritative updates.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/m2-package-implementation.md`
- Automation location: Cross-spec disposition and owner-bound fixtures.
- Required by milestone: M2

### T10. Historical sessions remain readable and unchanged

- Covers: R36; E9; EC8; BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-COMPAT-001; INT-004
- Level: contract
- Command IDs: CMD1, CMD3
- Fixture/setup: Historical sessions with no route IDs, route-like tables, legacy links, and new prospective sessions.
- Steps: Read all sessions and request route-result recording against historical variants.
- Expected result: Every historical record remains readable and byte-unchanged; missing stable IDs are never inferred; only prospective routes are eligible without a separately governed migration.
- Failure proves: Compatibility silently rewrites historical evidence.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Historical-session fixtures.
- Required by milestone: M2

### T11. Semantic and literal ledgers close preservation before mutation

- Covers: R38-R40, R47; BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Current skill, contract, caller, parser, package, and test consumers plus valid and unknown ledger classifications.
- Steps: Validate one owner and disposition for every semantic rule, duplicate cluster, sensitive literal, and legacy writer surface.
- Expected result: No current rule or literal is missing or duplicated, incidental prose is not frozen, legacy conflict has exact disposition, and unknown ledger values fail first.
- Failure proves: Procedure relocation hides semantic loss or compatibility drift.
- Evidence artifact: `evidence/m1-preservation-inventories.md`; `evidence/semantic-preservation-review.md`
- Automation location: Change-local ledgers and focused validator tests.
- Required by milestone: M1 and M3

### T12. Measurements prove both real profiles shrink

- Covers: R41-R42; EC10; AC10; BND-COMPOSE-001, BND-COMPAT-001; INT-005
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Before and after canonical resources assembled with LF normalization and unique-file counting.
- Steps: Measure LR0, LR1, `SKILL.md`, `session-method.md`, duplicate ownership, and total package in words and UTF-8 bytes.
- Expected result: LR0 and LR1 each remain below 1,712 words and 12,375 bytes; every resource and total package is reported; relocation is not presented as deletion.
- Failure proves: Simplification improves only the main file or one real operation path.
- Evidence artifact: `evidence/profile-size-baseline.md`; `evidence/simplification-measurements.md`
- Automation location: Standard-library measurement fixture.
- Required by milestone: M1 and M3

### T13. Canonical and derived packages retain complete byte parity

- Covers: R1, R5-R6, R43, R45; EC9; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005
- Level: integration
- Command IDs: CMD2, CMD4-CMD7
- Fixture/setup: Canonical package and freshly generated, archived, release-candidate, and installed Codex, Claude, and opencode trees.
- Steps: Build packages, select learn, and compare every required path and raw byte.
- Expected result: Every target contains the exact reference once, no asset, template, or script appears, portable text remains valid, and missing, transformed, escaped, stale, additional, or mixed resources fail.
- Failure proves: Canonical checks do not protect published package integrity.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Existing skill, build, and adapter distribution tests.
- Required by milestone: M3

### T14. Acceptance and portability boundaries remain closed

- Covers: R44-R45; AC12; BND-ENV-001
- Level: contract
- Command IDs: CMD2, CMD4-CMD11
- Fixture/setup: Planned deterministic command ledger, forbidden runtime and external operations, and published skill text with repository-maintainer mechanics placed in contributor or governing surfaces.
- Steps: Inspect command ownership, acceptance exclusions, and the canonical and packaged skill text.
- Expected result: Acceptance uses only repository-owned deterministic proof; no target runtime or live external mutation runs; published procedure remains project-portable and excludes maintainer-only packaging mechanics.
- Failure proves: The content refactor silently adds runtime evaluation or leaks repository-maintainer procedure into shipped skill text.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: Command-ledger, portability, and package fixtures.
- Required by milestone: M3

### T15. Compact results distinguish every required field and outcome

- Covers: R37; AC1; BND-COMPOSE-001
- Level: contract
- Command IDs: CMD3
- Fixture/setup: Successful `run-learn-session` with topic and routes, a no-lesson session, successful `record-learn-route-result`, identical route-result replay, and blocked identity or completion-kind mismatch.
- Steps: Produce the compact result for each fixture and inspect operation, session identity and path, trigger and scope, confirmation, session recording, topic effects, route IDs and settlements, owner-result identities, blockers, next owner or handoff, and claim limitations.
- Expected result: Every required R37 concept is distinguishable in every result; applicable values are exact, inapplicable values are unambiguously omitted or represented as not applicable according to one fixture contract, idempotent replay is distinguishable from a new write, blocked outcomes identify the exact blocker, and claim limits never imply destination approval, workflow completion, implementation, or correctness.
- Failure proves: A caller cannot reliably interpret the operation outcome or the result overclaims downstream state.
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: Focused compact-result contract fixtures.
- Required by milestone: M2

### T16. M1 closes the architecture trigger before canonical mutation

- Covers: R46; AC13; BND-RECOVERY-001
- Level: contract
- Command IDs: CMD1, CMD9
- Fixture/setup: M1 caller, scenario, ledger, and baseline inventories plus variants requiring transaction-grade phase recovery, a new persistent route or session schema owner, polling or coordination, external integration, or new cross-owner mutation authority.
- Steps: Run the M1 ledger fixture against the no-trigger baseline and each architecture-trigger variant before any canonical learn-package edit.
- Expected result: The baseline records an exact no-trigger result; every listed R46 condition fails the M1 gate and routes to architecture assessment; the canonical learn package remains unchanged in both paths.
- Failure proves: M2 could begin while an architecture-bearing recovery, persistence, integration, or authority requirement is unresolved.
- Evidence artifact: `evidence/m1-preservation-inventories.md`
- Automation location: M1 ledger and architecture-trigger fixtures.
- Required by milestone: M1

## Fixtures and data

- Change-local semantic-rule and literal-compatibility YAML ledgers with closed valid and unknown-value fixtures.
- Deterministic session-path fixtures for absent, occupied, partial, complete, changed-basis, unsafe, and concurrent states.
- Session and topic Markdown fixtures containing evidence, confirmation, topic-effect, route, owner-result, and historical variants.
- Cross-spec disposition fixture for legacy R21-R24, R33, Example E3, outputs, invariant, and acceptance wording.
- Temporary canonical, generated, archived, release-candidate, and installed package trees.
- No live user session, external tracker, target-agent transcript, credential, or private incident data is required.

## Mocking/stubbing policy

Use filesystem fixtures and pure contract data for session, topic, route, and package behavior. Model owner-produced results as exact local identities; do not call an issue tracker, hosted service, target-agent runtime, or external destination. Existing package builders may use their repository-owned temporary directories.

## Migration or compatibility tests

T9 proves exact legacy writer dispositions and preserved authoritative outcomes. T10 proves prospective adoption without historical rewriting. T13 proves atomic canonical and derived package rollout. Rollback proof restores the flat skill and old package inventory without touching historical sessions or topic guidance.

## Observability verification

T2-T16 inspect operation, session identity and path, trigger and scope, confirmation, session result, topic effects, route IDs, completion kinds, settlements, owner-result identities, blockers, handoff owner, claim limits, measurements, ledgers, and architecture triggers. Configured commands and executed commands remain distinguishable in evidence.

## Security/privacy verification

T3-T6 cover contained paths, sensitive evidence minimization, unavailable evidence, confirmation authority, topic conflicts, and forbidden cross-owner writes. T8 verifies that supplied owner-result identities never grant destination mutation or external-system access.

## Performance checks

T12 deterministically measures both real loaded assemblies and total package size. No runtime latency, background polling, cache, or service-level performance test applies.

## Manual QA checklist

Not applicable. All acceptance claims are covered by deterministic repository-owned proof. Ordinary lifecycle and PR review remain review gates, not a second manual acceptance system.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another target agent; the change is a static published-skill contract and package refactor.
- Do not grade transcripts or semantic model behavior; deterministic rule ownership, contract fixtures, and normal lifecycle review own acceptance.
- Do not open issues, mutate trackers, poll destinations, or publish packages; those external effects are outside learn and test-spec authority.
- Do not migrate historical sessions or infer route IDs; compatibility requires byte preservation.
- Do not test transaction-grade phase recovery; the approved contract fails closed and makes that behavior an architecture reassessment trigger.
- Do not require templates or scripts for learn artifacts; the approved first version explicitly excludes them.

## Uncovered gaps

None. Any newly discovered normative outcome returns to `spec`; any persistent recovery, registry, polling, integration, schema-owner, or cross-owner mutation need returns to architecture assessment; any proof-only omission returns to this test specification.

## Next artifacts

- Independent `test-spec-review` of proof adequacy and implementation handoff readiness.
- Implementation begins only after approving review settlement and workflow routing.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim peer-review approval, implementation readiness, validation success, verification, branch readiness, or PR readiness.
