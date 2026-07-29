<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec/SKILL.md -->

# Stage-Owned Lifecycle Artifacts and Change-Local Workflow State Test Spec

## Status

draft

## Owning change record

`docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`

## Related spec and plan

- Spec:
  `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Plan:
  `docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`

## Input artifact identities

This feature deliberately does not use content hashes.
Stable artifact IDs, paths, and formal review IDs identify the inputs.

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` | `stage-owned-lifecycle-spec` | approved by `spec-review-r6`; `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md` |
| Plan | `docs/plans/2026-07-29-stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md` | `stage-owned-lifecycle-plan` | approved by `plan-review-r2`; `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/plan-review-r2.md` |
| Architecture | `docs/architecture/system/architecture.md` | `canonical-architecture` | approved by `architecture-review-r2`; `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r2.md` |
| ADR | `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md` | `adr-stage-owned-lifecycle` | included in approved `architecture-review-r2` |
| Compatibility audit | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/compatibility-audit.md` | `stage-owned-compatibility-audit` | accepted input to `spec-review-r6` |

The feature spec retains its preactivation embedded `draft` marker.
Its formal R6 review is the durable evidence that authorizes this proof
authoring pass.

## Testing strategy

Unit tests extend the existing change-metadata and bounded state-adapter suites
for exact field shapes, closed values, legal transitions, identity binding,
unknown-value precedence, and migration behavior.
Contract tests inspect canonical published skills and assets for each stage's
writable outputs, read-only inputs, independent invocation behavior, and
route-back behavior.
Integration tests compose author, reviewer, workflow, downstream, status,
off, retry, migration, and milestone-resume paths without substituting a
helper-only result for the public path.
End-to-end tests exercise one independent review and one workflow-managed
change through conservative replay and final verify stop behavior.
Adapter tests use the existing temporary versioned distribution harness and
never hand-edit generated output.
Smoke proof runs once before activation and once after the atomic cutover.
Migration tests preserve historical reads, migrate resumed nonterminal work
once, and reject mixed current writers.
Agent semantic review is limited to published-skill meaning and final
external-action containment, which deterministic substring checks cannot
prove completely.
These non-scripted reviews are required pre-PR evidence.
They do not replace the final human review performed after PR submission.

## Boundary-first proof map

Boundary model version: boundary-first-v1

Boundary model scope: every requirement defined in
`specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`,
`SLA-R001` through `SLA-R077`, including the defined suffixed requirements.

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | SLA-R001, SLA-R005, SLA-R048, SLA-R064a | BND-INPUT-001 | T1, T2, T11, T12 | contract | automated | CMD1, CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-input-boundary.md` | M3 | - | - |
| PRF-002 | covered | SLA-R012a, SLA-R012b, SLA-R035, SLA-R037h, SLA-R037k, SLA-R037oa, SLA-R050, SLA-R057 | BND-STATE-001 | T3, T8, T9, T12 | integration | automated | CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-state-boundary.md` | M3 | - | - |
| PRF-003 | covered | SLA-R020, SLA-R023, SLA-R027, SLA-R034, SLA-R039, SLA-R042, SLA-R053, SLA-R054 | BND-AUTH-001 | T15, T23 | contract | hybrid | CMD2, CMD3 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m1-authority-boundary.md` | M1 | MP1 | - |
| PRF-004 | covered | SLA-R028, SLA-R029, SLA-R033, SLA-R044, SLA-R046, SLA-R063, SLA-R064, SLA-R072, SLA-R074b | BND-COMPOSE-001 | T15, T16, T24 | integration | hybrid | CMD2, CMD3, CMD8 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m5-composition-boundary.md` | M5 | MP1 | - |
| PRF-005 | covered | SLA-R019a, SLA-R030, SLA-R031, SLA-R032, SLA-R037la, SLA-R050a, SLA-R057, SLA-R058 | BND-TEMPORAL-001 | T5, T7, T9, T12, T19 | integration | automated | CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-temporal-boundary.md` | M3 | - | - |
| PRF-006 | covered | SLA-R025, SLA-R026, SLA-R043, SLA-R044, SLA-R047, SLA-R060, SLA-R062, SLA-R064 | BND-RECOVERY-001 | T6, T10, T12, T13, T20 | end-to-end | automated | CMD4, CMD6, CMD11 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m5-recovery-boundary.md` | M5 | - | - |
| PRF-007 | covered | SLA-R003, SLA-R004, SLA-R065, SLA-R067, SLA-R068, SLA-R074a, SLA-R074c, SLA-R074d, SLA-R074e | BND-COMPAT-001 | T1, T14, T15, T21, T26 | integration | automated | CMD1, CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m4-compatibility-boundary.md` | M4 | - | - |
| PRF-008 | covered | SLA-R007, SLA-R037c, SLA-R061, SLA-R069, SLA-R071 | BND-ENV-001 | T2, T13, T17, T21 | end-to-end | hybrid | CMD4, CMD8, CMD11 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m6-environment-boundary.md` | M6 | MP2 | - |
| PRF-009 | covered | SLA-R018, SLA-R019a, SLA-R023, SLA-R027 | INT-001 | T23 | contract | hybrid | CMD2, CMD3 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m1-interaction-001.md` | M1 | MP1 | - |
| PRF-010 | covered | SLA-R022, SLA-R028, SLA-R032, SLA-R033, SLA-R038 | INT-002 | T6, T7, T19 | integration | automated | CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-interaction-002.md` | M3 | - | - |
| PRF-011 | covered | SLA-R037i, SLA-R037j, SLA-R037k, SLA-R037l, SLA-R037la, SLA-R037oa, SLA-R037ob, SLA-R037p | INT-003 | T9 | integration | automated | CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-interaction-003.md` | M3 | - | - |
| PRF-012 | covered | SLA-R050b, SLA-R051, SLA-R052, SLA-R053, SLA-R054, SLA-R055, SLA-R058 | INT-004 | T11, T20 | end-to-end | automated | CMD2, CMD4, CMD6 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m3-interaction-004.md` | M3 | - | - |
| PRF-013 | covered | SLA-R065, SLA-R066, SLA-R067, SLA-R074a, SLA-R074b, SLA-R074c, SLA-R074d, SLA-R074e | INT-005 | T14, T15, T16, T21 | integration | automated | CMD1, CMD2, CMD4, CMD6, CMD8 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m5-interaction-005.md` | M5 | - | - |
| PRF-014 | covered | SLA-R060, SLA-R061, SLA-R062, SLA-R063, SLA-R064 | INT-006 | T12, T13, T21 | end-to-end | hybrid | CMD6, CMD11 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m6-interaction-006.md` | M6 | MP2 | - |
| PRF-015 | covered | SLA-R042, SLA-R043, SLA-R044, SLA-R045, SLA-R046, SLA-R047 | INT-007 | T10, T20 | end-to-end | automated | CMD2, CMD6, CMD11 | `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/evidence/m5-interaction-007.md` | M5 | - | - |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| SLA-R001-SLA-R004 | T1, T21, T26 | migration, e2e | Exact marker, sole current contract, historical reads, and migrate-before-write. |
| SLA-R005-SLA-R012c | T2, T3 | unit, contract | Registry shape, IDs, paths, reviews, closed states, legal transitions, and terminal behavior. |
| SLA-R013-SLA-R017 | T4 | contract | Stable change pointer and stable artifact/plan content without mutable workflow fields. |
| SLA-R018-SLA-R021c | T5 | integration | Authoring entry, completion evidence, bounded correction, closeout, supersession, and ADR deprecation ownership. |
| SLA-R022-SLA-R029 | T6, T19 | integration, e2e | Evidence-first peer settlement, outcome mapping, isolation, and workflow-managed equivalence. |
| SLA-R030-SLA-R033 | T7 | integration | Idempotent reconciliation, conflicting reuse, and incomplete-settlement pause. |
| SLA-R034-SLA-R037c | T8 | unit, integration | Sole routing owner, exact workflow shape, stages, blockers, and evidence paths. |
| SLA-R037d-SLA-R037p | T9 | unit, integration | Planned-work shape, ordered milestones, current review occurrence, remaining work, and final readiness. |
| SLA-R038-SLA-R041 | T8, T9 | integration | Evidence-derived routing and pointer-only compact state. |
| SLA-R042-SLA-R047 | T10, T20 | integration, e2e | Downstream challenge, owner revision, fresh review, and conservative replay. |
| SLA-R048-SLA-R050b | T11, T12 | unit, integration | Structured target, six-field automation record, status, transitions, and terminal recurrence. |
| SLA-R051-SLA-R059 | T11, T20 | integration, e2e | One target, no extra parameter, fixed authority, prerequisites, isolation, and retired-state absence. |
| SLA-R060-SLA-R064a | T12, T13, T25 | integration, e2e | Pause conditions, cutover and final external boundaries, verify stop, read-only status, cancellation, and unknown values. |
| SLA-R065-SLA-R069 | T1, T14, T21, T26 | migration, e2e | One-way prospective migration, classified proof, preserved evidence, one writer, no mass migration, and excluded mechanisms. |
| SLA-R070-SLA-R074 | T17 | unit, contract | Minimal deterministic validation, claim boundary, adapter parity, and unknown-value precedence. |
| SLA-R074a-SLA-R074b | T15, T16 | contract, integration | Published skill ownership and generated adapter preservation. |
| SLA-R074c-SLA-R074e | T14 | migration, contract | Closed subject replacement, reciprocal notices, retained behavior, and stale proof-map handling. |
| SLA-R075-SLA-R077 | T18 | contract | Complete boundary record, exact proof consumption, and example subordination. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Level | Notes |
| --- | --- | --- | --- |
| AC-SLA-001-AC-SLA-004 | T1, T2, T3, T4 | unit, contract, migration | Activation, historical reads, stable artifacts, and closed registry identity. |
| AC-SLA-005-AC-SLA-012 | T5, T6, T7, T19 | integration, e2e | Authoring, review evidence, settlement, isolation, retries, and incomplete settlement. |
| AC-SLA-013-AC-SLA-016 | T4, T8, T9, T10 | integration, contract | Routing ownership, stable plans, challenge recording, and conservative replay. |
| AC-SLA-017-AC-SLA-022 | T11, T12, T13, T20, T25 | integration, e2e | One target, no added parameter, fixed writes, prerequisites, pauses, and verify stop. |
| AC-SLA-023-AC-SLA-025 | T14, T17, T21, T26 | migration, unit | One-way migration, proof classification, honest validation claims, and unknown-value precedence. |
| AC-SLA-026-AC-SLA-027 | T15, T16 | contract, integration | Canonical/generated guidance and closed reciprocal subjects. |
| AC-SLA-028-AC-SLA-031 | T3, T5, T6, T9, T12 | unit, integration | Terminal evidence, review readiness, deterministic planned work, and automation transitions. |
| AC-SLA-032-AC-SLA-035 | T14, T15, T16, T18 | contract, migration | Cross-surface agreement, boundary/example proof, and stale proof-map replacement. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T19 | Independent approved proposal review settles only proposal state. |
| E2 | T6, T19 | Changes-requested review settles revision-required and isolated review stops. |
| E3 | T5 | Authoring invalidates settlement before substantive revision. |
| E4 | T7 | Workflow pauses while review evidence and settlement disagree. |
| E5 | T20 | Managed review settles first, then workflow advances routing. |
| E6 | T11 | One verify target supplies repository-local continuation without wider writes. |
| E7 | T11 | Future state is not pre-completed by target selection. |
| E8 | T13, T25 | Cutover and final verify stop before every external action. |
| E9 | T10 | Implementation records a plan defect and routes to plan without editing it. |
| E10 | T1, T14 | Historical read is side-effect free and resumed work migrates once. |
| E11 | T2, T6 | Two ADR IDs remain distinct and review settles only the named one. |
| E12 | T5, T6 | Interrupted authoring remains unreviewable. |
| E13 | T9 | Planned-work resume selects M2 and derives the current stop state. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1-EC2 | T19 | Independent approved and changes-requested outcomes settle without routing. |
| EC3 | T5 | Revision enters authoring before content mutation. |
| EC4-EC6 | T7 | Missing settlement reconciles; conflicting reuse and workflow approval fail. |
| EC7-EC8 | T4, T5 | Plan and test-spec content remain stable while state and closeout live elsewhere. |
| EC9-EC10 | T11, T20 | Early target persists without future completion or another authorization. |
| EC11 | T13, T25 | Scope expansion pauses for owner decision at cutover and final verify. |
| EC12-EC13 | T13, T25 | Verify success stops before PR; failure pauses without repair. |
| EC14-EC15 | T1, T14 | Historical reads do not migrate; resumed mutation migrates exactly once. |
| EC16 | T17 | Review can report unexpected upstream diff without validator attribution. |
| EC17 | T17 | Unknown state fails before consistency checks. |
| EC18-EC19 | T2 | Multiple supporting ADRs pass; duplicate paths or primary roles fail. |
| EC20 | T5, T6 | Interrupted authoring cannot be settled. |
| EC21 | T9 | Inconsistent current milestone ordering fails. |
| EC22 | T12, T17 | Unknown automation state or target fails before mutation. |
| EC23 | T15 | Published upstream-write or extra-authorization language blocks publication. |
| EC24 | T18 | Missing, duplicate, or unknown boundary dimension fails structurally. |
| EC25 | T18 | Ownerless example or test routes to spec rather than creating behavior. |

## Validation commands

These commands are inspected and registered during authoring but are not run
by the test-spec stage.

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/validate-boundary-first.py --path specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md --path specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.test.md` | existing/configured | test-spec-review and implement | preimplementation gate | test-spec-review | block proof-map approval or the owning milestone | not applicable; deterministic validator | test-spec-review record and change validation ledger | read-only repository validation |
| CMD2 | `python scripts/test-skill-validator.py` | existing/configured | implement | M1 | M1 code-review | block changed published-skill handoff | zero tests is failure | M1, M2, M5, or M6 implementation evidence | local tests and temporary fixtures only |
| CMD3 | `python scripts/validate-skills.py` | existing/configured | implement | M1 | M1 code-review | block canonical skill handoff | not applicable; deterministic validator | M1, M2, M5, or M6 implementation evidence | read-only canonical skill validation |
| CMD4 | `python scripts/test-change-metadata-validator.py` | existing/configured | implement | M3 | M3 code-review | block metadata, transition, or migration handoff | zero tests is failure | M3, M4, or M6 implementation evidence | local tests and temporary fixtures only |
| CMD5 | `python scripts/validate-change-metadata.py docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml` | existing/configured | test-spec, workflow, and verify | lifecycle | test-spec authoring handoff | block state-changing handoff | not applicable; deterministic validator | change validation ledger | read-only validation of one change record |
| CMD6 | `python scripts/test-workflow-automation-state.py` | existing/configured | implement | M3 | M3 code-review | block bounded state-adapter or migration handoff | zero tests is failure | M3, M4, or M6 implementation evidence | local tests and temporary repositories only |
| CMD7 | `python scripts/build-skills.py --check` | existing/configured | implement | M5 | M5 code-review | block canonical/generated skill parity | not applicable; deterministic check | M5 or M6 implementation evidence | check mode; no tracked output mutation |
| CMD8 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M5 | M5 code-review | block generated adapter parity | zero tests is failure | M5 or M6 implementation evidence | versioned temporary output only; no network or publication |
| CMD9 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state` | existing/configured | test-spec-review and verify | lifecycle | test-spec-review | block malformed review evidence | not applicable; deterministic validator | review log | local read-only validation |
| CMD10 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state` | existing/configured | verify | M7 | M7 closeout | block closeout while findings remain open | not applicable; deterministic validator | review resolution and verify evidence | local read-only validation |
| CMD11 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | implement and verify | M5 | M5 code-review | block preactivation, cutover, or final readiness | any selected test suite with zero tests is failure | M5/M6 implementation evidence and verify evidence | local repository validation; no publication or external mutation |
| CMD12 | `bash scripts/ci.sh --mode pr --base "$(git merge-base HEAD main)" --head HEAD` | ci-owned | verify | M7 | final verify | block PR readiness | any selected test suite with zero tests is failure | final verify evidence | local diff-scoped validation; no PR creation, push, or publication |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Preimplementation test-proof alignment | T14, T18 | none | CMD1, CMD5, CMD9 | this test spec; revised dependent test specs; test-spec-review record | M1 implementation | Every stale proof map must be revised and approved; any remaining stale row blocks M1. |
| M1 | T4, T15, T23 | MP1 | CMD2, CMD3, CMD5 | M1 implementation evidence and agent semantic-review matrix | M1 code-review | Only published stage ownership and peer-stage guidance are required; state integration is deferred to M3. |
| M2 | T15, T24 | MP1 | CMD2, CMD3, CMD5 | M2 workflow-composition evidence and agent semantic-review matrix | M2 code-review | Only published workflow composition is required while marker creation stays disabled; state and end-to-end proof remain deferred. |
| M3 | T2, T3, T5, T6, T7, T8, T9, T11, T12, T17, T19, T22 | none | CMD2, CMD4, CMD5, CMD6 | M3 metadata and bounded state-adapter evidence | M3 code-review | State integration, retry, peer settlement, routing, and bounded-cost proof first become executable here. |
| M4 | T1, T26 | none | CMD4, CMD5, CMD6 | M4 migration matrix and compatibility evidence | M4 code-review | Runtime migration consumes the preimplementation CP-001 through CP-032 classification as read-only input. |
| M5 | T10, T15, T16, T18, T20, T24 | MP1, MP2 | CMD1, CMD2, CMD3, CMD4, CMD6, CMD7, CMD8, CMD11 | generated parity, behavior preservation, preactivation marker-disabled evidence, and agent semantic-review matrices | M5 code-review | Complete preactivation and generated-composition proof closes before cutover. |
| M6 | T1, T11, T12, T13, T16, T21, T22 | MP2 | CMD2, CMD4, CMD6, CMD7, CMD8, CMD11 | exact cutover diff, post-cutover scenario evidence, and activation audit | M6 code-review | One workflow-skill activation source; rollback does not restore retired writers. |
| M7 | T25 | MP2 | CMD5, CMD9, CMD10, CMD11, CMD12 | current M1-M6 evidence, final holistic review, explain-change, verify, agent containment recheck, and PR handoff evidence | final verify and PR handoff | T9/T20 evidence is consumed, not re-owned; human PR review occurs afterward. |

### Progressive proof activation

| Behavior | First proof | Later composed proof |
| --- | --- | --- |
| Author/review peer ownership | M1: T23 with CMD2/CMD3 and MP1 | M3: T5, T6, and T19 with CMD4/CMD6 |
| Workflow routing-only composition | M2: T24 with CMD2/CMD3 and MP1 | M3: T7, T8, T11, and T12; M5: T10 and T20 |
| Bounded state cost | M3: T22 with CMD4/CMD6 | M6: T22 post-cutover recheck |
| Compatibility classification and migration | Preimplementation: T14 with CMD1 | M4: T1 and T26 with CMD4/CMD6 |
| External-action containment | M5: MP2 preactivation audit | M6: T13 plus MP2; M7: T25 plus MP2 and CMD12 |

An earlier milestone does not claim a later command or state integration result.
The later rows strengthen composed proof without making the earlier published
skill contract depend on an unavailable implementation surface.

## Test cases

### T1. Marker activation, historical reads, and resumed migration

- Covers: SLA-R001-SLA-R004, SLA-R065-SLA-R069, E10, EC14, EC15
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: new governed, historical terminal, historical nonterminal, resumed, already-migrated, and ambiguous legacy change records.
- Steps: Read each record; attempt the first resumed mutation; repeat the mutation; inspect state and evidence.
- Expected result: Reads are side-effect free, new and resumed nonterminal work receives the exact marker before mutation, migration occurs once, and ambiguous records pause.
- Failure proves: activation or migration can mutate history, skip the current contract, or create two current writers.
- Evidence artifact: M4 migration matrix and M6 post-cutover evidence.
- Automation location: `scripts/test-change-metadata-validator.py`; `scripts/test-workflow-automation-state.py`.
- Required by milestone: M4 and M6

### T2. Artifact registry shape, identities, paths, and closed values

- Covers: SLA-R005-SLA-R012, E11, EC17-EC19
- Level: unit
- Command IDs: CMD4
- Fixture/setup: valid primary/supporting artifacts and variants with malformed IDs, duplicate paths, duplicate primary roles, escaping paths, missing/additional fields, invalid reviews, and unknown values.
- Steps: Validate each fixture and compare vocabulary failures with consistency failures.
- Expected result: Valid multiple-ADR state passes; every malformed or unknown value fails before dependent consistency checks.
- Failure proves: ambiguous or expanded artifact identity can enter routing or settlement.
- Evidence artifact: M3 metadata evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.
- Required by milestone: M3

### T3. Artifact lifecycle and terminal transition matrix

- Covers: SLA-R012a-SLA-R012c, SLA-R021a-SLA-R021c, AC-SLA-028
- Level: unit
- Command IDs: CMD4
- Fixture/setup: every legal transition and representative absent, cross-kind, terminal-reopen, invalid deprecation, and supersession-without-replacement transition.
- Steps: Apply transitions through the metadata semantic layer.
- Expected result: Only the closed legal matrix commits; terminal states never reopen; replacement and closeout evidence are required.
- Failure proves: lifecycle state can bypass its owning closeout or artifact-kind rules.
- Evidence artifact: M3 transition evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.
- Required by milestone: M3

### T4. Governed artifacts and plans contain stable intent only

- Covers: SLA-R013-SLA-R017, EC7, EC8
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: affected canonical skills and assets plus governed proposal, spec, architecture, ADR, plan, test-spec, and `docs/plan.md` fixtures.
- Steps: Generate representative artifacts and inspect their permitted stable fields and owning-change pointers.
- Expected result: No mutable status, progress, current review, blocker, routing, or closeout field is emitted; plan intent and navigation remain.
- Failure proves: an upstream artifact remains a competing mutable workflow-state surface.
- Evidence artifact: M1 artifact-shape audit.
- Automation location: `scripts/test-skill-validator.py` plus M1 semantic review.
- Required by milestone: M1

### T5. Authoring owns revision invalidation and bounded closeout

- Covers: SLA-R018-SLA-R021c, E3, E12, EC3, EC20, INT-001
- Level: integration
- Command IDs: CMD2, CMD4, CMD6
- Fixture/setup: accepted/approved/active artifacts, interrupted authoring, complete authoring record, non-substantive correction, replacement, abandonment, archive, and ADR deprecation cases.
- Steps: Begin revision, interrupt it, complete it, and exercise each permitted closeout.
- Expected result: Only the matching entry enters authoring before content mutation; review is cleared; review-required needs complete evidence; closeout follows its exact owner.
- Failure proves: an author can self-approve, mutate another state entry, or expose partial content to review.
- Evidence artifact: M3 authoring-transition integration evidence.
- Automation location: canonical skill tests and change-metadata fixtures.
- Required by milestone: M3

### T6. Review peers settle one matching artifact from review-required

- Covers: SLA-R022-SLA-R029, SLA-R021c, E1, E2, E11, EC1, EC2, EC20
- Level: integration
- Command IDs: CMD2, CMD4, CMD6
- Fixture/setup: every review-stage/artifact mapping, ADR settlement values, non-review-required inputs, open findings, and approved, changes-requested, blocked, and inconclusive outcomes.
- Steps: Record evidence, attempt settlement, and inspect reviewed content, sibling state, and routing.
- Expected result: Evidence precedes settlement; only the named entry changes; outcomes map exactly; reviewed content and workflow routing remain unchanged.
- Failure proves: review can rewrite its target, settle stale content, or advance workflow.
- Evidence artifact: M3 peer-review settlement integration evidence.
- Automation location: skill fixtures and change-metadata/state-adapter tests.
- Required by milestone: M3

### T7. Interrupted review settlement reconciles idempotently

- Covers: SLA-R030-SLA-R033, E4, EC4-EC6, INT-002
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: durable review evidence with missing settlement, identical retry, changed record path, changed outcome, changed round, and workflow evaluation before settlement.
- Steps: Retry identical and conflicting settlement, then evaluate routing.
- Expected result: Identical retry reconciles once without rerunning review; conflicting reuse fails; workflow pauses and never approves.
- Failure proves: review identity can change meaning or workflow can manufacture settlement.
- Evidence artifact: M3 reconciliation evidence.
- Automation location: `scripts/test-change-metadata-validator.py`; `scripts/test-workflow-automation-state.py`.
- Required by milestone: M3

### T8. Workflow state is the exact compact routing owner

- Covers: SLA-R034-SLA-R037c, SLA-R038-SLA-R041
- Level: unit
- Command IDs: CMD4, CMD6
- Fixture/setup: valid routing records plus unknown stages, invalid blockers, duplicate/escaping evidence paths, duplicated findings, and routing inconsistent with artifact settlement.
- Steps: Validate and project each record.
- Expected result: The exact closed shape and current evidence pass; unknown, stale, duplicated, or content-heavy state fails or pauses.
- Failure proves: workflow state can widen into another evidence store or route from stale settlement.
- Evidence artifact: M3 routing-state evidence.
- Automation location: change-metadata and bounded state-adapter tests.
- Required by milestone: M3

### T9. Planned work binds milestone occurrence and positive closeout evidence

- Covers: SLA-R037d-SLA-R037p, E13, EC21, INT-003
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: ordered M1-M7 plan projection with legal/illegal transitions, stale prior review, wrong artifact or milestone occurrence, incomplete gates, and fully positive closeout evidence.
- Steps: Advance milestones, request/reconcile reviews, calculate remaining work, and derive final readiness.
- Expected result: Current milestone is the first nonterminal milestone, reviews rebind explicitly, every open gate yields ordered reasons, and ready requires all positive evidence.
- Failure proves: stale review or plan prose can create false resume or closeout readiness.
- Evidence artifact: M3 planned-work evidence and M7 closeout evidence.
- Automation location: change-metadata and bounded state-adapter tests.
- Required by milestone: M3 and M7

### T10. Downstream challenge routes to the owner without write-back

- Covers: SLA-R042-SLA-R047, E9, INT-007
- Level: e2e
- Command IDs: CMD2, CMD3, CMD6, CMD11
- Fixture/setup: implementation discovers a blocking plan contradiction after downstream evidence exists.
- Steps: Record challenge evidence, inspect plan and plan state, route to plan, revise through authoring, review again, and resume.
- Expected result: Downstream writes only its evidence; workflow pauses and routes; owner plus fresh review settle the revision; downstream stages rerun conservatively.
- Failure proves: downstream work can rewrite its governing contract or reuse stale settlement.
- Evidence artifact: M5 route-back scenario evidence.
- Automation location: published-skill scenario fixture and broad-smoke composition.
- Required by milestone: M5

### T11. One structured target validates prerequisites without widening authority

- Covers: SLA-R048-SLA-R059, E6, E7, EC9, EC10, INT-004
- Level: integration
- Command IDs: CMD2, CMD4, CMD6
- Fixture/setup: verify, milestone, and singleton targets at early, current, stale, malformed, and complete lifecycle positions.
- Steps: Persist targets, inspect future state, invoke each current prerequisite, resume repeated occurrences, and omit retired profile fields.
- Expected result: One exact target is sufficient; no later state is pre-completed; stage writes stay fixed; stale binding fails; absent retired state does not pause.
- Failure proves: target selection becomes blanket write authority or requires another public parameter.
- Evidence artifact: M3 target-bound scenario evidence.
- Automation location: skill, metadata, and bounded state-adapter tests.
- Required by milestone: M3

### T12. Automation transitions, status, off, and terminal runs fail closed

- Covers: SLA-R049-SLA-R050b, SLA-R063, SLA-R064, SLA-R064a, EC22
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: every legal automation transition, representative illegal transitions, terminal resume, new occurrence, unknown target/status, status read, and off retry.
- Steps: Exercise the bounded state adapter and inspect before/after records.
- Expected result: Only legal transitions commit; status is byte-for-byte read-only; off preserves evidence and stops scheduling; terminal runs require a new invocation.
- Failure proves: automation can silently reopen, mutate on status, or accept an unknown authority state.
- Evidence artifact: M3 automation-state evidence and M6 post-cutover evidence.
- Automation location: change-metadata and workflow-state tests.
- Required by milestone: M3 and M6

### T13. Cutover stop conditions contain every external action

- Covers: SLA-R060-SLA-R062, E8, EC11-EC13, INT-006
- Level: e2e
- Command IDs: CMD6, CMD11
- Fixture/setup: owner decision, open finding, scope expansion, stale evidence, failed validation, cancellation, missing tool, verify failure, and verify success with fail-on-call external doubles.
- Steps: Reach each stop condition through the post-cutover public workflow and trace success and failure exits.
- Expected result: Every condition pauses or cancels durably; failure never repairs; success completes before PR and only reports `pr` next.
- Failure proves: automation can exceed repository-local consent or mutate implementation/external state after verify.
- Evidence artifact: M6 containment evidence.
- Automation location: workflow-state scenarios and broad smoke.
- Required by milestone: M6

### T14. Closed compatibility projections classify stale proof before M1

- Covers: SLA-R074c-SLA-R074e, AC-SLA-027, AC-SLA-035
- Level: integration
- Command IDs: CMD1
- Fixture/setup: all 32 reciprocal source/test-spec pairs, CP-001 through CP-032, reviewed non-conflicts, historical evidence, and missing, duplicate, unknown, or contradictory projection fixtures.
- Steps: Compare every source notice with its projection row, apply the row's whole-subject rule to the dependent proof map, and inspect retained and historical proof classifications.
- Expected result: Every dependent notice cites exactly one matching projection; superseded proof is historical-only; retained proof remains current; any stale, missing, duplicate, unknown, or contradictory projection blocks M1; history remains unchanged.
- Failure proves: a retired writer or stale proof map can remain authoritative before implementation begins.
- Evidence artifact: CP-001 through CP-032, revised dependent notices, compatibility audit, and test-spec-review record.
- Automation location: boundary-first structural validation and semantic test-spec review.
- Required by milestone: preimplementation gate

### T15. Canonical published skills preserve stage-owned behavior

- Covers: SLA-R072, SLA-R074a, AC-SLA-026, EC23, BND-AUTH-001
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: complete affected-skill inventory and mutations that add upstream writes, self-approval, workflow settlement, routing by review, or an extra authorization request.
- Steps: Run structural checks and perform MP1 against each changed skill and asset.
- Expected result: Every skill declares correct writes, read-only inputs, isolation, and route-back behavior; semantic drift blocks handoff.
- Failure proves: published guidance still authorizes upstream write-back or an added consent layer.
- Evidence artifact: M1/M2 skill inventory and semantic review matrix.
- Automation location: skill tests plus MP1.
- Required by milestone: M1 and M2

### T16. Generated adapters preserve canonical ownership and isolation

- Covers: SLA-R073, SLA-R074b, AC-SLA-026, AC-SLA-032
- Level: e2e
- Command IDs: CMD7, CMD8
- Fixture/setup: canonical skill tree and existing versioned temporary adapter-distribution harness for every supported adapter.
- Steps: Generate temporary adapters, compare normalized published behavior, and perturb one generated skill.
- Expected result: Clean generation passes; drift, added writes, missing isolation, or hand-edited output fails with the canonical source as owner.
- Failure proves: adapter consumers receive a different lifecycle contract.
- Evidence artifact: M5/M6 adapter parity evidence.
- Automation location: build check and adapter distribution tests.
- Required by milestone: M5 and M6

### T17. Deterministic validation stays minimal and honest

- Covers: SLA-R069-SLA-R071, SLA-R074, EC16, EC17
- Level: unit
- Command IDs: CMD2, CMD4
- Fixture/setup: unknown value before inconsistent dependent fields, unexpected upstream diff, and fixtures tempting actor-attribution, hash, selector, or protected-path claims.
- Steps: Validate each fixture and inspect diagnostics and selected implementation surface.
- Expected result: Unknown vocabulary fails first; consistency is checked; no validator claims writer identity or requires excluded machinery.
- Failure proves: scripts have become a second workflow or overclaim process-level assurance.
- Evidence artifact: M3 validation-claim evidence.
- Automation location: skill and change-metadata validator tests.
- Required by milestone: M3

### T18. Boundary record, proof map, and examples remain requirement-owned

- Covers: SLA-R075-SLA-R077, AC-SLA-033, AC-SLA-034, EC24, EC25
- Level: integration
- Command IDs: CMD1
- Fixture/setup: governing feature/test-spec pair plus missing dimension, duplicate boundary, unknown interaction, missing direct proof, and ownerless example fixtures.
- Steps: Validate exact IDs, scope, proof rows, interactions, and example ownership; inspect semantic completeness.
- Expected result: The current pair passes; every structural or ownership defect fails or routes to spec revision without inventing behavior.
- Failure proves: the proof map can repair or replace its governing contract.
- Evidence artifact: test-spec-review record.
- Automation location: boundary-first validation and semantic test-spec review.
- Required by milestone: preimplementation gate

### T19. Independent author and review peers settle without routing

- Covers: SLA-R018-SLA-R033, E1, E2, E4, INT-001, INT-002
- Level: e2e
- Command IDs: CMD2, CMD4, CMD6
- Fixture/setup: independent proposal/spec authoring and review scenarios with complete, partial, clean, finding, and interrupted settlement variants.
- Steps: Invoke each peer in isolation and compare governed content, matching state, sibling state, and routing.
- Expected result: Author and reviewer write only their owned surfaces; review stops after settlement; interrupted identical settlement reconciles.
- Failure proves: independent skills require workflow or cross-write another stage's surface.
- Evidence artifact: M3 independent peer settlement evidence.
- Automation location: composed skill/state fixtures.
- Required by milestone: M3

### T20. Workflow-managed lifecycle follows evidence through conservative replay

- Covers: SLA-R029, SLA-R038-SLA-R062, E5, EC9-EC13, INT-004, INT-007
- Level: e2e
- Command IDs: CMD2, CMD4, CMD6, CMD11
- Fixture/setup: one governed change targeted at final verify with a downstream plan defect introduced after initial settlement.
- Steps: Progress through current prerequisites, trigger route-back, revise and rereview, replay downstream, then run passing and failing verify variants.
- Expected result: Routing follows settled evidence, never widens writes, replays conservatively, pauses on failure, and completes before PR on success.
- Failure proves: the public composed lifecycle bypasses ownership, current prerequisites, or the external-action boundary.
- Evidence artifact: M5 complete preactivation scenario evidence and M7 verify evidence.
- Automation location: published workflow scenarios and broad smoke.
- Required by milestone: M5 and M7

### T21. Atomic cutover changes one public activation source

- Covers: SLA-R001-SLA-R004, SLA-R061, SLA-R065-SLA-R069, INT-005, INT-006
- Level: e2e
- Command IDs: CMD2, CMD4, CMD6, CMD8, CMD11
- Fixture/setup: M5 preactivation tree, M6 workflow-skill cutover diff, new change, resumed nonterminal change, historical read, status/off, cancellation, and verify variants.
- Steps: Prove marker creation disabled before cutover; apply the one source change; rerun focused scenarios and adapter parity; exercise rollback.
- Expected result: New marker creation begins only after M6; migration is once-before-write; rollback disables new creation without restoring retired writers or deleting evidence.
- Failure proves: activation is partial, has multiple owners, or cannot be rolled back safely.
- Evidence artifact: M5 marker-disabled evidence and M6 activation evidence.
- Automation location: focused skill, metadata, state-adapter, adapter, and broad-smoke tests.
- Required by milestone: M6

### T22. State checks remain bounded and status reads remain cheap

- Covers: performance expectations
- Level: smoke
- Command IDs: CMD4, CMD6
- Fixture/setup: bounded change records with increasing artifact, milestone, and evidence-pointer counts plus a status-only invocation.
- Steps: Measure validation growth and inspect invoked operations.
- Expected result: Work grows linearly with bounded state and linked indexes; status performs no stage invocation, polling, network, or repository-wide hashing.
- Failure proves: the simple repository-local mechanism acquired an unbounded or background execution cost.
- Evidence artifact: M3/M6 performance notes.
- Automation location: focused metadata/state tests.
- Required by milestone: M3 and M6

### T23. Published author and review peers preserve reciprocal ownership

- Covers: SLA-R018, SLA-R019a, SLA-R020, SLA-R023, SLA-R027, SLA-R042, INT-001, BND-AUTH-001
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: changed canonical authoring and matching review skills plus mutations that authorize self-approval, reviewed-content edits, sibling-state writes, or workflow routing.
- Steps: Run structural skill checks, then apply MP1 to the paired author/reviewer guidance and their independent-invocation paths.
- Expected result: Each author owns content and authoring transition only; each reviewer owns review evidence and matching settlement only; neither peer writes the other's output or workflow routing.
- Failure proves: M1 can publish peer-stage guidance that permits self-approval or cross-owner mutation before state integration exists.
- Evidence artifact: M1 peer-ownership semantic matrix.
- Automation location: canonical skill checks plus MP1.
- Required by milestone: M1

### T24. Published workflow composition remains routing-only

- Covers: SLA-R028, SLA-R029, SLA-R033, SLA-R034, SLA-R039, SLA-R044, SLA-R046, SLA-R053, SLA-R054, SLA-R063, SLA-R064, BND-COMPOSE-001
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: changed workflow guidance and author/review/downstream sibling skills plus mutations that let workflow settle review, let review route workflow, add another public authorization, or bypass the current prerequisite.
- Steps: Run structural skill checks, then apply MP1 to independent and workflow-managed public paths while marker creation remains disabled.
- Expected result: Workflow invokes and routes only; each stage retains fixed writes; review settlement precedes routing; one target needs no extra public authorization.
- Failure proves: M2 can publish a composed path that bypasses peer ownership before the durable state adapter is implemented.
- Evidence artifact: M2 workflow-composition semantic matrix.
- Automation location: canonical skill checks plus MP1.
- Required by milestone: M2 and M5

### T25. Final verify rechecks containment before PR submission

- Covers: SLA-R060-SLA-R062, EC11-EC13, INT-006
- Level: e2e
- Command IDs: CMD5, CMD9, CMD10, CMD11, CMD12
- Fixture/setup: current M1-M6 evidence, passing and failing verify variants, cancellation, stale review evidence, open findings, and fail-on-call external doubles.
- Steps: Validate lifecycle closeout, run final repository checks, apply MP2 to the complete public path, and inspect the PR handoff boundary.
- Expected result: Failure or cancellation stops without repair; success records PR handoff evidence but performs no PR, push, merge, publication, credential, or destructive action.
- Failure proves: final verification can exceed repository-local authority or claim human PR approval.
- Evidence artifact: M7 verify evidence and agent containment recheck.
- Automation location: final validation commands plus MP2; final human judgment occurs after PR submission.
- Required by milestone: M7

### T26. Runtime migration rejects mixed or stale lifecycle authority

- Covers: SLA-R003, SLA-R004, SLA-R065-SLA-R068, BND-COMPAT-001
- Level: integration
- Command IDs: CMD4, CMD6
- Fixture/setup: CP-classified historical records, resumed nonterminal records, already-migrated records, ambiguous legacy records, mixed-writer records, and records whose proof classification is missing or stale.
- Steps: Read each record, attempt the first governed mutation, retry migration, and inspect lifecycle state plus preserved historical evidence.
- Expected result: Historical reads remain unchanged; eligible resumed work migrates once before mutation; already-migrated work is idempotent; ambiguous, mixed-writer, or stale-proof authority pauses without mutation.
- Failure proves: runtime migration can reactivate a superseded proof owner, rewrite history, or create competing lifecycle state.
- Evidence artifact: M4 migration matrix and compatibility evidence.
- Automation location: change-metadata and bounded state-adapter tests.
- Required by milestone: M4

## Fixtures and data

- Add governed current, historical terminal, historical nonterminal, migrated,
  ambiguous legacy, and mixed-writer records under
  `tests/fixtures/change-metadata/`.
- Extend existing skill fixtures with one valid stage-ownership matrix and
  focused invalid upstream-write, self-approval, routing, and
  extra-authorization variants.
- Extend workflow state tests with exact current target, settlement,
  occurrence, retry, cancellation, and migration records.
- Use the existing adapter-distribution temporary tree and supported-adapter
  inventory.
- Keep external-action doubles fail-on-call and credential-free.
- Preserve historical fixtures; do not rewrite them into current state.

## Mocking/stubbing policy

Mock only external or destructive boundaries and clock/concurrency conditions
that cannot be exercised safely.
Do not mock change-metadata parsing, transition semantics, published skill
content, canonical-to-generated adapter flow, or repository-relative path
normalization.
Composed tests must use the public skill/state path rather than calling only a
helper and treating that result as end-to-end proof.

## Migration or compatibility tests

T1, T21, and T26 own runtime migration proof.
T14 owns the required preimplementation classification of dependent proof.
The 32 matching source test specs are compatibility inputs and must carry a
current proof-alignment notice before `test-spec-review`.
Their historical evidence remains unchanged.
A stale row may continue to describe pre-adoption behavior, but it must not
authorize governed current behavior and must point to this proof map for the
replacement subject.

### Compatibility proof projections

For each row, the superseded-proof rule applies to every coverage row, test
case, manual procedure, milestone row, and expected outcome in the dependent
test spec that asserts the named replaced subject.
Those rows remain historical evidence only for pre-adoption changes.
The retained disposition remains current and must continue to pass.

| Projection ID | Dependent test spec | Source specification | Superseded proof rule for governed changes | Retained proof disposition | Replacement test IDs |
| --- | --- | --- | --- | --- | --- |
| CP-001 | `artifact-status-lifecycle-ownership.test.md` | `artifact-status-lifecycle-ownership.md` | Lifecycle-state storage inside governed artifacts and downstream normalization of that state. | Retain lifecycle meanings, terminal history, staleness detection, and explicit replacement evidence. | T2, T3, T5, T6, T14 |
| CP-002 | `single-source-of-workflow-state.test.md` | `single-source-of-workflow-state.md` | Active-plan and `docs/plan.md` ownership of current milestone, review, blocker, next-stage, and closeout state. | Retain milestone ordering, review evidence, closeout gates, portability, and historical plan intent. | T4, T8, T9, T14 |
| CP-003 | `rigorloop-workflow.test.md` | `rigorloop-workflow.md` | Peer/downstream edits to reviewed content or plan progress, settlement outside the matching transition, and another public authorization inside one target. | Retain lifecycle order, formal review gates, isolation, correction budgets, and stop conditions. | T10, T11, T12, T14, T20, T24 |
| CP-004 | `single-bounded-review-fix-workflow-automation.test.md` | `single-bounded-review-fix-workflow-automation.md` | Additional authorization, capability, activation-selector, profile, and selector-ledger mechanisms. | Retain structured targets, occurrence binding, review independence, bounded correction, evidence-first resume, historical reads, and external-action prohibitions. | T11, T13, T14, T20, T25 |
| CP-005 | `formal-review-recording.test.md` | `formal-review-recording.md` | Artifact-local lifecycle settlement and mutable status stored in reviewed artifacts or plans. | Retain formal review receipts, detailed findings, review-log indexing, and review-resolution obligations. | T6, T7, T14, T19, T23 |
| CP-006 | `downstream-status-settlement-before-reliance.test.md` | `downstream-status-settlement-before-reliance.md` | Downstream edits to upstream lifecycle, readiness, follow-on, or closeout metadata. | Retain clear-review-evidence checks, fail-closed reliance, and blocking on contradictory or unresolved evidence. | T6, T7, T10, T14, T19 |
| CP-007 | `proposal-family-assets-progressive-disclosure.test.md` | `proposal-family-assets-progressive-disclosure.md` | Proposal-status sections, values, and status-preserving asset requirements. | Retain proposal asset packaging, progressive disclosure, Vision fit, scope, review dimensions, and recording behavior. | T4, T14, T15, T23 |
| CP-008 | `spec-family-assets-progressive-disclosure.test.md` | `spec-family-assets-progressive-disclosure.md` | Embedded spec status, proposal-status settlement gates, and active-plan handoff ownership. | Retain spec asset packaging, progressive disclosure, boundary guidance, and evidence-access behavior. | T4, T14, T15, T23 |
| CP-009 | `review-finding-resolution-contract.test.md` | `review-finding-resolution-contract.md` | Artifact-local settlement and clean-review settlement through proposal-status or decision-log mutation. | Retain finding shape, review logging, dispositions, resolution closeout, and referential integrity. | T6, T7, T14, T19, T23 |
| CP-010 | `review-skill-family-consistency-parser-owned-finding-shape.test.md` | `review-skill-family-consistency-parser-owned-finding-shape.md` | Downstream reliance on embedded proposal status. | Retain review-family consistency, parser-owned finding shape, asset policy, and formal review evidence. | T6, T14, T19, T23 |
| CP-011 | `stage-evidence-access-contracts-for-cost-bounded-rigor.test.md` | `stage-evidence-access-contracts-for-cost-bounded-rigor.md` | Accepted proposal status settlement as an output or acceptance criterion. | Retain bounded evidence access, escalation, and contributor-visible evidence reporting. | T4, T6, T14, T23 |
| CP-012 | `stop-tracking-generated-public-adapter-skill-bodies.test.md` | `stop-tracking-generated-public-adapter-skill-bodies.md` | Accepted proposal status settlement as a downstream-reliance prerequisite. | Retain canonical skill ownership, adapter archive installation, release metadata, and generated-output policy. | T6, T14, T16 |
| CP-013 | `workflow-stage-autoprogression.test.md` | `workflow-stage-autoprogression.md` | Artifact-local status gates and separately armed authoring or implementation profiles. | Retain stage ordering, review gates, bounded correction, resume safety, test-spec proof, and stop-before-PR behavior. | T11, T12, T14, T20, T24 |
| CP-014 | `change-record-catalog-registration-and-bounded-read-model.test.md` | `change-record-catalog-registration-and-bounded-read-model.md` | Active-plan `Current Handoff Summary` as the current live-state source. | Retain change-record registration, bounded discovery, evidence pointers, and historical reads. | T4, T8, T9, T14 |
| CP-015 | `cost-bounded-rigor-m5-progressive-loading-follow-through.test.md` | `cost-bounded-rigor-m5-progressive-loading-follow-through.md` | Active-plan handoff state as the first implementation-state read. | Retain progressive loading, quick guides, bounded evidence, and full-read escape conditions. | T8, T9, T14 |
| CP-016 | `learn-artifact-model.test.md` | `learn-artifact-model.md` | Mutable process follow-ups routed into the active plan. | Retain learn session/topic ownership, classification, deduplication, and owning-surface routing. | T4, T8, T10, T14 |
| CP-017 | `milestone-aware-review-handoff.test.md` | `milestone-aware-review-handoff.md` | Code-review updates or required updates to active-plan milestone and handoff state. | Retain milestone identity, review outcomes, finding resolution, and next-milestone sequencing. | T6, T8, T9, T14 |
| CP-018 | `plan-index-lifecycle-ownership.test.md` | `plan-index-lifecycle-ownership.md` | Plan-body and plan-index ownership of mutable lifecycle, progress, blocker, and closeout state. | Retain stable navigation, historical plan preservation, archive integrity, and bounded index presentation. | T4, T8, T9, T14 |
| CP-019 | `progressive-loading-high-cost-public-skills.test.md` | `progressive-loading-high-cost-public-skills.md` | Active-plan `Current Handoff Summary` as the authoritative handoff-state source. | Retain progressive evidence loading, token-cost controls, quick guides, and safety escape conditions. | T8, T9, T14 |
| CP-020 | `release-process-contract.test.md` | `release-process-contract.md` | Release-stage updates to active-plan lifecycle or handoff state. | Retain release evidence, safety gates, rollback, registry verification, and transactional release behavior. | T8, T9, T14 |
| CP-021 | `skill-contract.test.md` | `skill-contract.md` | Artifact-local settlement, embedded mutable status, and current-handoff templates duplicating change-local state. | Retain normalized skill structure, resource integrity, claim boundaries, portability, and adapter parity. | T4, T14, T15, T16 |
| CP-022 | `workflow-skill-artifact-location-map.test.md` | `workflow-skill-artifact-location-map.md` | Plan bodies and `docs/plan.md` as mutable lifecycle-state or current-routing owners. | Retain artifact placement, change-root mapping, review locations, portable defaults, and workflow-guide ownership. | T4, T8, T14 |
| CP-023 | `cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md` | `cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md` | Current-handoff or active-plan state as the first current-state source and implementation-handoff owner. | Retain bounded evidence order, escalation, follow-up classification, and cost controls. | T8, T9, T14 |
| CP-024 | `cost-bounded-rigor-m2-selected-skill-reminders.test.md` | `cost-bounded-rigor-m2-selected-skill-reminders.md` | Implementation rationale, progress, or validation evidence recorded in the active plan. | Retain selected-skill reminders, no-change rationale, and contributor-visible evidence requirements. | T4, T8, T14 |
| CP-025 | `cost-bounded-rigor-m4-lifecycle-token-cost-summary.test.md` | `cost-bounded-rigor-m4-lifecycle-token-cost-summary.md` | Mutable summary triggers, decisions, or follow-ups owned by the active plan. | Retain lifecycle token-cost summaries, trigger classification, report shape, and evidence limits. | T4, T8, T14 |
| CP-026 | `follow-up-ownership-and-deferred-work-register.test.md` | `follow-up-ownership-and-deferred-work-register.md` | Current-change execution or learn follow-ups written to the active plan. | Retain cross-change admission, ownership fields, deduplication, and terminal dispositions. | T4, T8, T10, T14 |
| CP-027 | `guide-system-source-of-truth-alignment.test.md` | `guide-system-source-of-truth-alignment.md` | `docs/plan.md` as a mutable live-work index. | Retain guide classification, navigation, source-rank reporting, and bounded presentation. | T4, T8, T14 |
| CP-028 | `implement-first-attempt-correctness.test.md` | `implement-first-attempt-correctness.md` | Implementation rationale, progress, or alignment state written into the active plan body. | Retain same-slice completeness, first-pass proof, validation selection, and aligned-surface auditing. | T4, T8, T10, T14 |
| CP-029 | `installed-skill-artifact-placement-contract.test.md` | `installed-skill-artifact-placement-contract.md` | Lifecycle state and milestone progress placed in `docs/plan.md` or the plan body. | Retain artifact-type distinctions, path discovery, portable defaults, and placement diagnostics. | T4, T8, T14 |
| CP-030 | `project-artifact-location-guide-and-examples-surface.test.md` | `project-artifact-location-guide-and-examples-surface.md` | Active-plan metadata as current lifecycle authority or a higher-ranked mutable path source. | Retain location guidance, example isolation, path lookup, and generated-surface validation. | T4, T8, T14 |
| CP-031 | `release-transaction-automation.test.md` | `release-transaction-automation.md` | Active-plan `Current Handoff Summary` as the next workflow-action owner. | Retain transactional release stages, evidence, safety checks, rollback, and stop conditions. | T8, T9, T12, T14 |
| CP-032 | `test-spec-review-gate.test.md` | `test-spec-review-gate.md` | Active-plan ownership of current workflow state. | Retain proof-map review, implementation handoff gating, coverage, and review evidence. | T6, T8, T14, T18 |

## Observability verification

The mechanism has no runtime logs, metrics, or traces.
Verify durable repository evidence instead:

- exact artifact and milestone IDs;
- authoring and review record paths;
- transition and stop evidence paths;
- migration and cutover evidence;
- review-log and review-resolution state; and
- generated adapter parity evidence.

Diagnostics must identify the invalid field or transition, offending identity,
allowed contract, and safe next owner without exposing credentials or private
reasoning.

## Security/privacy verification

T13, T25, and MP2 prove the repository-local boundary.
Tests must fail if any path can open a PR, push, publish, release, deploy,
merge, run destructive Git, access credentials, or mutate an external system.
Evidence stores paths, outcomes, and concise diagnostics, not secrets,
credential values, or private chain-of-thought.

## Performance checks

T22 checks linear bounded-state behavior and read-only status cost.
No fixed wall-clock budget is introduced because repository and CI sizes vary.
A regression that adds repository-wide content hashing, background polling, or
external lookup fails the architectural and non-goal boundary regardless of
timing.

## Manual QA checklist

`Manual` in the proof taxonomy means non-scripted semantic judgment.
MP1 and MP2 are performed by an independent review agent before PR submission.
They produce durable, reviewable feedback from multiple named perspectives.
The human reviewer remains the final PR approval authority after submission;
automation and agent evidence MUST NOT claim that human review has occurred.

### MP1. Agent published-skill semantic ownership audit

- Stable ID: MP1.
- Automation rationale: Structural and substring checks can prove required
  fields and reject known text patterns, but cannot decide whether the complete
  shipped guidance could reasonably authorize cross-owner writes, self-review,
  workflow settlement, or another public consent layer.
- Owning stage and required gates:
  - M1 code-review audits author/review peer ownership in every changed stage
    skill and asset.
  - M2 code-review audits independent and workflow-managed composition in
    `workflow` and every changed sibling skill.
  - M5 code-review rechecks all changed canonical skills and every generated
    supported-adapter counterpart before activation.
- Reviewer: an agent acting in the independent `code-review` role, not the
  implementation pass that authored the reviewed guidance.
- Required environment: a local repository checkout containing the changed
  canonical `skills/` sources, applicable assets, the owning spec and plan,
  and, at M5, temporary generated adapter output from the repository harness.
  No network, credentials, publication, or tracked generated-output edits.
- Perspectives:
  - output ownership and read-only inputs;
  - author/reviewer peer separation;
  - independent invocation and isolation;
  - workflow-managed composition and route-back;
  - ambiguity or implied extra authorization;
  - canonical/generated behavioral parity at M5.
- Exact steps:
  1. List the changed canonical skills and applicable generated counterparts.
  2. Read each as shipped user-facing guidance, including writable outputs,
     read-only inputs, independent behavior, route-back, and stop behavior.
  3. Trace one independent author, one independent review, one
     workflow-managed review, and one downstream challenge path.
  4. Record one matrix row per skill and perspective with file location,
     observed behavior, `pass` or finding, and required correction.
  5. Confirm deterministic CMD2/CMD3 evidence and, at M5, CMD7/CMD8 evidence
     cover structure and parity without substituting for semantic judgment.
- Evidence artifact: the owning milestone code-review record plus
  `evidence/m<milestone>-published-skill-semantic-matrix.md`.
- Pass condition: Every perspective has an evidence-backed `pass`; no stage
  claims another stage's output; review never edits its target or routes
  workflow; workflow never settles review; downstream never writes upstream;
  generated guidance preserves the canonical result.
- Failure condition: Any missing perspective, ambiguous authority statement,
  cross-owner write, self-approval, workflow settlement, additional public
  authorization, generated semantic drift, or unsupported caller assertion
  creates a material code-review finding and blocks the owning gate.
- Escalation: Route the finding to the owning skill milestone.
  Do not repair it from the review pass.

### MP2. Agent external-action and activation-owner audit

- Stable ID: MP2.
- Automation rationale: Fail-on-call doubles prove exercised external
  boundaries, but cannot establish that every public, alternate, cancellation,
  rollback, or activation path was selected and interpreted completely.
- Owning stage and required gates:
  - M5 code-review audits complete preactivation composition and confirms
    marker creation remains disabled.
  - M6 code-review audits the exact cutover, single activation owner, post-
    cutover stop paths, and rollback.
  - M7 `verify` rechecks the complete path immediately before PR handoff.
- Reviewer: an agent acting in the independent `code-review` role at M5/M6
  and the independent `verify` role at M7.
- Required environment: a local repository checkout with current M1-M6
  evidence as applicable, the canonical workflow skill, bounded persistence
  adapter, temporary adapter output, and credential-free fail-on-call doubles.
  Real PR, push, merge, publish, release, deploy, credential, destructive Git,
  and hosted-system actions are prohibited.
- Perspectives:
  - single activation ownership;
  - fixed stage authority and no automatic repair;
  - success, failure, cancellation, status, and stale-evidence containment;
  - rollback and preserved evidence;
  - external, credential, destructive, and hosted-action reachability;
  - PR handoff versus final human PR approval.
- Exact steps:
  1. Identify the one public marker-creation owner and every persistence call.
  2. Trace preactivation, successful cutover, failure, cancellation, status,
     stale evidence, rollback, verify success, and verify failure.
  3. Inspect fail-on-call coverage for each prohibited external boundary.
  4. Record one matrix row per path and perspective with source location,
     observed outcome, `pass` or finding, and required correction.
  5. At M7, confirm successful verify records handoff only and makes no claim
     about PR submission, human approval, or merge.
- Evidence artifact: M5/M6 code-review records and
  `evidence/m5-preactivation-audit.md`,
  `evidence/m6-activation-containment-audit.md`, and
  `evidence/m7-final-containment-recheck.md`.
- Pass condition: Marker creation has one owner; preactivation stays disabled;
  every failure and cancellation stops without repair; rollback preserves
  evidence without retired writers; no prohibited external action is
  reachable; M7 ends at PR handoff.
- Failure condition: A second activation source, missing path, automatic
  repair, credential access, destructive or external mutation, rollback to a
  retired writer, PR creation, or human-approval claim creates a material
  finding and blocks the owning gate.
- Escalation: Route the finding to the owning implementation milestone.
  Do not invoke the prohibited action or repair implementation from review.

The submitted PR includes links to MP1 and MP2 evidence for the human reviewer.
Human feedback after submission returns to the owning stage and reruns the
affected deterministic checks and agent semantic review before resubmission.

## What not to test and why

- Do not test actor attribution for arbitrary file writes; the contract
  explicitly excludes it.
- Do not add content-hash, protected-path, interception, immutable-snapshot,
  selector-ledger, risk-profile, or hosted-state tests.
- Do not prove selective downstream reuse; conservative replay is normative.
- Do not test publication, deployment, merge, or real credential flows.
- Do not duplicate published-skill semantics in a new workflow validator.
- Do not treat examples, fixtures, or substring checks as normative owners.
- Do not mass-migrate historical changes or rewrite historical evidence.

## Uncovered gaps

None in the governing feature boundary record.

All 32 dependent proof maps now carry the compatibility revision described by
T14.
Implementation remains blocked until this test spec and those revisions pass
`test-spec-review`.

## Next artifacts

- Run `test-spec-review` over this proof map and the 32 compatibility
  revisions.
- Begin M1 only after the review is approved with no proof gap.

## Follow-on artifacts

None yet.

## Readiness

The primary proof map and all 32 dependent compatibility projections are ready
for `test-spec-review`.
They are not yet ready for implementation or M1.
