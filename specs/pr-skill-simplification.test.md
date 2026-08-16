# PR Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-16-pr-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/pr-skill-simplification.md`
- Plan: `docs/plans/2026-08-16-pr-skill-simplification.md`
- Architecture/ADRs: not required; `docs/changes/2026-08-16-pr-skill-simplification/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| proposal | `docs/proposals/2026-08-16-pr-skill-simplification.md` | proposal | `proposal-review-r4` |
| specification | `specs/pr-skill-simplification.md` | spec | `spec-review-r2` and `reviews/spec-review-r2.md` |
| architecture assessment | `docs/changes/2026-08-16-pr-skill-simplification/architecture-assessment.md` | architecture-assessment | `architecture-not-required` |
| execution plan | `docs/plans/2026-08-16-pr-skill-simplification.md` | plan | `plan-review-r1` and `reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic standard-library unit and contract fixtures for classification, authority, verification-basis compatibility, Git ancestry, remote PR state, hosted CI, operation ordering, retry, result claims, and forbidden mutation. Use repository-owned skill, build, adapter, boundary, and change-metadata validators for package and lifecycle proof. Static host-state fixtures replace live PR creation; no target-agent runtime or transcript grading is used.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R4 | T-PR-001, T-PR-002 | contract | Package inventory, conditional ownership, and structural-only asset. |
| R5-R7 | T-PR-003, T-PR-004 | contract | Tri-state signals, loading, no fallback, and missing-resource stops. |
| R8-R10 | T-PR-005 | contract | Submission intent and zero-write preparation. |
| R11-R15 | T-PR-006, T-PR-007 | contract | Independent refresh/state authority and byte preservation. |
| R16-R18 | T-PR-008 | contract | Directional branch ancestry and non-force behavior. |
| R19-R21 | T-PR-009, T-PR-010 | contract | PR-state matrix, reuse, creation, refresh, and result vocabulary. |
| R22-R23 | T-PR-011 | contract | Hosted-CI vocabulary, exact-head evidence, and claims. |
| R24-R27 | T-PR-012, T-PR-013 | contract | Verify ownership, normalized basis, legacy compatibility, and no inference. |
| R28-R30 | T-PR-014 | contract | Evidence-tail identity, permitted diff, and exact operation tuple. |
| R31-R36 | T-PR-015 | integration | Preflight, repeated rereads, mutation, and final read-back. |
| R37-R38 | T-PR-016 | integration | Retry, concurrent creation, partial success, and readiness separation. |
| R39-R41 | T-PR-017 | contract | Write boundary, result shape, and body groups. |
| R42-R45 | T-PR-018 | contract | Ledgers, unknown values, deterministic measurement, and reduction. |
| R46-R47 | T-PR-019 | smoke | Generated-through-installed parity and no live/runtime acceptance. |
| R48-R49 | T-PR-020 | contract | Architecture escalation and published-text portability. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T-PR-005, T-PR-013 | Preparation remains read-only with incomplete legacy evidence. |
| E2 | T-PR-009 | Adequate existing open PR is reused unchanged. |
| E3 | T-PR-006 | Default open intent preserves an existing draft. |
| E4 | T-PR-008 | Remote work absent locally blocks push. |
| E5 | T-PR-015, T-PR-016 | A moved base preserves external truth but invalidates readiness. |
| E6 | T-PR-016 | Concurrent matching-PR creation is reconciled without duplication. |
| E7 | T-PR-007 | Stale body without whole-body authority remains byte-identical. |
| E8 | T-PR-003 | Malformed governed signals stop without portable fallback. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 remote unavailable during preparation | T-PR-005 | Prepared result names evidence limit and remains non-ready. |
| EC2 branch appears between preflight and push | T-PR-008, T-PR-015 | Baseline reread reclassifies or blocks. |
| EC3 multiple matching PRs | T-PR-009 | `ambiguous`; no mutation. |
| EC4 adequate draft for default open | T-PR-006, T-PR-009 | Reuse without publication. |
| EC5 whole-body authority without title authority | T-PR-006, T-PR-007 | Body only changes. |
| EC6 push succeeds and PR create fails | T-PR-016 | Push fact is reported; opening remains blocked. |
| EC7 evidence tail changes unrelated state | T-PR-014 | Opening readiness becomes stale. |
| EC8 pending exact-head CI | T-PR-011 | May open only under policy and never says passed. |
| EC9 matching merged PR | T-PR-009 | Stop without duplicate or lifecycle completion. |
| EC10 installed resource missing | T-PR-019 | Package parity validation fails. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R5, R6, R8, R11, R12, R16, R19, R21, R22, R43 | BND-INPUT-001 | T-PR-003, T-PR-005, T-PR-006, T-PR-008, T-PR-009, T-PR-010, T-PR-011, T-PR-018 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R8, R9, R13, R15, R16, R17, R18, R19, R20, R23, R37, R38, R39 | BND-STATE-001 | T-PR-005, T-PR-006, T-PR-008, T-PR-009, T-PR-011, T-PR-016, T-PR-017 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R5, R6, R11, R12, R13, R24, R25, R26, R28, R30, R36, R39 | BND-AUTH-001 | T-PR-003, T-PR-006, T-PR-012, T-PR-014, T-PR-015, T-PR-017 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R6, R7, R41, R42, R46, R49 | BND-COMPOSE-001 | T-PR-001, T-PR-002, T-PR-004, T-PR-017, T-PR-018, T-PR-019, T-PR-020 | contract | automated | C2, C3, C4, C5, C6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R28, R31, R32, R33, R34, R35, R36, R37, R38 | BND-TEMPORAL-001 | T-PR-014, T-PR-015, T-PR-016 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R7, R10, R18, R20, R23, R27, R29, R32, R33, R34, R35, R36, R37, R38 | BND-RECOVERY-001 | T-PR-004, T-PR-008, T-PR-009, T-PR-011, T-PR-013, T-PR-014, T-PR-015, T-PR-016 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R14, R24, R25, R26, R27, R42, R43, R44, R45, R46, R49 | BND-COMPAT-001 | T-PR-007, T-PR-012, T-PR-013, T-PR-018, T-PR-019, T-PR-020 | contract | automated | C1, C2, C3, C4, C5, C6 | `evidence/semantic-preservation-review.md` | M3 | - | - |
| PRF-008 | covered | R9, R16, R17, R18, R19, R20, R22, R23, R31, R32, R33, R34, R35, R36, R38, R47 | BND-ENV-001 | T-PR-005, T-PR-008, T-PR-009, T-PR-011, T-PR-015, T-PR-016, T-PR-019 | integration | automated | C1, C6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R5, R6, R7 | INT-001 | T-PR-003, T-PR-004 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R8, R9, R10, R11, R12, R13 | INT-002 | T-PR-005, T-PR-006 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R24, R25, R26, R27, R28, R29 | INT-003 | T-PR-012, T-PR-013, T-PR-014 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R16, R17, R18, R31, R32 | INT-004 | T-PR-008, T-PR-015 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-013 | covered | R19, R20, R33, R34, R35, R37 | INT-005 | T-PR-009, T-PR-015, T-PR-016 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-014 | covered | R32, R33, R35, R36, R38 | INT-006 | T-PR-015, T-PR-016 | integration | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-015 | covered | R14, R15, R41 | INT-007 | T-PR-002, T-PR-007, T-PR-017 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-016 | covered | R22, R23, R40 | INT-008 | T-PR-011, T-PR-017 | contract | automated | C1 | `evidence/m2-package-implementation.md` | M2 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C0 | `python docs/changes/2026-08-16-pr-skill-simplification/fixtures/validate-pr-simplification.py` | planned-for-implementation | M1 | M1 | M1 | Stop M1 and correct an incomplete ledger, unknown vocabulary, invalid scenario, or nondeterministic baseline. | The command must execute every declared fixture family; an empty family is failure. | `docs/changes/2026-08-16-pr-skill-simplification/evidence/m1-preservation-inventories.md` | Python standard library and change-local files only; canonical skills and external systems are read-only. |
| C1 | `python scripts/test-skill-validator.py PRSkillSimplificationTests` | planned-for-implementation | M2 | M2 | M2 | Stop M2 and correct focused contract or fixture failure. | Zero selected tests is failure. | `docs/changes/2026-08-16-pr-skill-simplification/evidence/m2-package-implementation.md` | Local deterministic fixtures only; no remote or PR mutation. |
| C2 | `python scripts/validate-skills.py skills/pr/SKILL.md skills/verify/SKILL.md` | existing/configured | skill validator | M2 | M2 | Stop on invalid structure, resources, claims, or portability. | Not applicable. | M2 and M3 evidence | Reads canonical skill packages only. |
| C3 | `python scripts/test-skill-validator.py` | existing/configured | skill validator suite | M2 | M2 | Stop on any skill-contract regression. | Zero tests is failure. | M2 and M3 evidence | Repository-local tests; no external mutation. |
| C4 | `python scripts/test-build-skills.py` | existing/configured | skill build tests | M2 | M2 | Stop on generation or inventory regression. | Zero tests is failure. | M2 and M3 evidence | Temporary/local output only. |
| C5 | `python scripts/build-skills.py --check` | existing/configured | skill builder | M2 | M2 | Stop on canonical/generated drift. | Not applicable. | M2 and M3 evidence | Check mode only. |
| C6 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution suite | M3 | M3 | Stop on archive, release-candidate, or install parity failure. | Zero tests is failure. | `docs/changes/2026-08-16-pr-skill-simplification/evidence/m3-package-proof.md` | Uses temporary package/install trees; no publication. |
| C7 | `python scripts/validate-boundary-first.py --check --path specs/pr-skill-simplification.md` | existing/configured | boundary validator | M3 | M3 | Stop on missing, stale, malformed, or unproved boundary mapping. | Not applicable. | M3 evidence | Reads spec and proof map only. |
| C8 | `python scripts/validate-change-metadata.py docs/changes/2026-08-16-pr-skill-simplification/change.yaml` | existing/configured | change metadata validator | M1 | M1 | Stop on invalid lifecycle metadata. | Not applicable. | Every milestone evidence | Reads the owning change record only. |
| C9 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | ci-owned | repository CI contract | M4 | M4 | Stop final verification and route the failing check to its owner. | Zero-test success is forbidden by owned child commands. | final verify report | Final local CI orchestration; does not open a PR. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T-PR-018 | none | C0, C8 | `evidence/m1-preservation-inventories.md`, `evidence/profile-size-baseline.md` | M1 code review | Canonical skill packages remain unchanged. |
| M2 | T-PR-001-T-PR-017, T-PR-020 | none | C1, C2, C3, C4, C5, C8 | `evidence/m2-package-implementation.md` | M2 code review | Producer and consumer contract changes land atomically. |
| M3 | T-PR-018-T-PR-020 | none | C2, C3, C4, C5, C6, C7, C8 | measurements, semantic preservation, and `evidence/m3-package-proof.md` | M3 code review | Proves real profile reduction and package parity. |
| M4 | T-PR-001-T-PR-020 | none | C1-C9 | final review, explanation, and verify report | PR handoff | Lifecycle closeout only; no implementation scope. |

## Test cases

### T-PR-001. Package inventory and resource map

- Covers: R1-R4, AC-PRSIM-015, AC-PRSIM-016
- Level: contract
- Command IDs: C1, C2
- Fixture/setup: canonical PR skill with expected main file, one reference, one asset, and exact `READ`/`COPY` mappings
- Steps: validate inventory, triggers, verbs, paths, one-load behavior, and package-relative containment
- Expected result: the selected three-file package is complete and each rule or structure has one owner
- Failure proves: package shape, mapping, or ownership drifted
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-002. Structural body groups remain policy-free

- Covers: R4, R41, INT-007
- Level: contract
- Command IDs: C1
- Fixture/setup: core, governed, impact, inapplicable, unresolved, and placeholder body compositions
- Steps: compose each allowed group set and inspect headings, omissions, blockers, and forbidden policy phrases
- Expected result: structure is exact, inapplicable groups omit, unresolved required data blocks, and no placeholder or policy remains
- Failure proves: asset structure or policy ownership is wrong
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-003. Governed-signal tri-state classification

- Covers: R5, R6, E8, INT-001
- Level: contract
- Command IDs: C1
- Fixture/setup: absent, exact, malformed, duplicated, stale, conflicting, unsafe, and escaped signals
- Steps: classify each signal set and attempt portable or governed routing
- Expected result: only no signal permits portable handling; one exact candidate loads the reference; every invalid set stops
- Failure proves: governed work can fall through or load ambiguously
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-004. Missing conditional resources fail closed

- Covers: R7, INT-001
- Level: contract
- Command IDs: C1, C2
- Fixture/setup: missing, unreadable, escaped, stale, transformed, and mixed-version reference or asset
- Steps: trigger each resource and evaluate dependent judgment or body generation
- Expected result: dependent work stops and common procedure does not reconstruct it
- Failure proves: missing package material weakens safety
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-005. Submission intent and preparation side effects

- Covers: R8-R10, E1, EC1, INT-002
- Level: contract
- Command IDs: C1
- Fixture/setup: open, draft, prepare-only, unknown intent, provider unavailable, and readiness blocker states
- Steps: classify request, record attempted external calls, and inspect result fields
- Expected result: preparation makes zero calls; blocked opening is not renamed; unknown intent fails first
- Failure proves: requested and actual operations or side effects are conflated
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-006. Independent refresh and PR-state authority

- Covers: R11-R13, E3, EC4, EC5, INT-002
- Level: contract
- Command IDs: C1
- Fixture/setup: every valid and invalid intent, refresh authority, state-transition authority, and existing open/draft state combination
- Steps: classify permitted title/body/state mutations and inspect untouched fields
- Expected result: each authority permits only its exact action and default intent preserves existing draft/open state
- Failure proves: submission intent grants unrelated mutation authority
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-007. Whole-body preservation and no section parser

- Covers: R14, R15, E7, EC5, INT-007
- Level: contract
- Command IDs: C1
- Fixture/setup: duplicate headings, code-fence headings, nested headings, reviewer-authored prose, and explicit whole-body authority
- Steps: request title refresh, insufficient body refresh, and authorized whole-body replacement
- Expected result: title-only preserves body bytes, insufficient authority blocks, whole-body authority replaces only the body, and no section parsing occurs
- Failure proves: reviewer content can be overwritten without complete authority
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-008. Directional branch relation and push safety

- Covers: R16-R18, E4, EC2, INT-004
- Level: contract
- Command IDs: C1
- Fixture/setup: absent, same, both ancestry directions, diverged, ambiguous, and unknown relation
- Steps: evaluate permitted push and exact command properties before and after baseline reread
- Expected result: only absent creation or normal remote-ancestor fast-forward is allowed; no force, delete, overwrite, or unseen-remote-work push occurs
- Failure proves: branch safety or vocabulary is incomplete
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-009. Remote PR-state operation matrix

- Covers: R19, R20, E2, EC3, EC4, EC9, INT-005
- Level: contract
- Command IDs: C1
- Fixture/setup: absent, open, draft, closed, merged, ambiguous, and multiple matching PRs with adequate or stale content
- Steps: select create, reuse, authorized refresh, transition, or stop
- Expected result: one exact operation follows the closed matrix and no closed/merged/ambiguous state creates another PR
- Failure proves: PR selection can duplicate or mutate unsupported state
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-010. Operation-result unknown values fail first

- Covers: R21, R43
- Level: contract
- Command IDs: C1
- Fixture/setup: every result value plus `unknown_value`
- Steps: validate vocabulary before result consistency
- Expected result: known values reach consistency checks; unknown value produces an explicit vocabulary error
- Failure proves: closed result vocabulary can silently fall through
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests.test_operation_result_unknown_value`
- Required by milestone: M2

### T-PR-011. Hosted-CI truthfulness

- Covers: R22, R23, EC8, INT-008
- Level: contract
- Command IDs: C1
- Fixture/setup: every CI state, unknown state, exact and mismatched heads, required and optional pre-open policies
- Steps: evaluate opening permission, body wording, blocker, and readiness claim
- Expected result: only current exact-head evidence can pass; pending/unavailable/unobserved never say passed; unknown fails first
- Failure proves: CI evidence or claims are overstated
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests.test_hosted_ci_unknown_value`
- Required by milestone: M2

### T-PR-012. Verify-owned normalized basis

- Covers: R24-R26, AC-PRSIM-013
- Level: contract
- Command IDs: C1
- Fixture/setup: portable verify result and governed verify report with immutable tuple values
- Steps: validate producer ownership, required fields, resolved identities, and PR consumption
- Expected result: verify owns and emits the basis; PR only consumes and revalidates it
- Failure proves: branch-ready or identity ownership moved or became ambiguous
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-013. Legacy verification evidence is preparation-only

- Covers: R26, R27, E1, AC-PRSIM-014
- Level: contract
- Command IDs: C1
- Fixture/setup: complete basis, prose-only, command-only, unresolved-name, missing, stale, conflicting, and ambiguous historical reports
- Steps: attempt preparation and opening for each evidence form
- Expected result: only complete current basis proceeds to remote revalidation; every incomplete form permits truthful preparation only and routes to fresh verify
- Failure proves: PR reconstructs an unsupported verified basis
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-014. Verify-owned evidence-tail compatibility

- Covers: R28-R30, EC7, INT-003
- Level: contract
- Command IDs: C1
- Fixture/setup: same revision, one allowed direct child, multiple commits, wrong parent, allowed paths/fields, and every forbidden path/field class
- Steps: derive handoff revision and operation tuple from each case
- Expected result: only same revision or the exact single evidence tail remains eligible; all broader changes invalidate opening readiness
- Failure proves: post-verify mutation is accepted too broadly or legitimate durable evidence is rejected
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-015. Exact external-operation sequence and read-back

- Covers: R31-R36, E5, EC2, INT-004, INT-005, INT-006
- Level: integration
- Command IDs: C1
- Fixture/setup: deterministic host transcript model with mutable base, remote head, PR state, title, body, and draft status
- Steps: run preflight, immediate pre-push read, push, post-push reread, pre-mutation reread, one authorized operation, and final read-back
- Expected result: each call occurs in order; every identity matches at its use; readiness is true only after exact final confirmation
- Failure proves: stale evidence can authorize an external write or readiness claim
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-016. Retry, concurrency, and partial external success

- Covers: R37, R38, E5, E6, EC6, INT-005, INT-006
- Level: integration
- Command IDs: C1
- Fixture/setup: concurrent matching PR creation, push-only success, failed mutation read-back, moved base, and identical retry
- Steps: interrupt at each external boundary, reread state, and retry
- Expected result: no duplicate or blind replay occurs; confirmed writes remain truthful facts; readiness stays false when identities changed
- Failure proves: retry is non-idempotent or readiness masks partial failure
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-017. Result, claims, body, and lifecycle write boundary

- Covers: R39-R41, INT-008
- Level: contract
- Command IDs: C1
- Fixture/setup: portable/governed prepared, opened, draft-opened, updated, reused, and blocked results with tracked filesystem writes
- Steps: validate required fields, URL conditions, body groups, claims, and changed paths
- Expected result: results separate requested and actual facts, URLs appear only after read-back, and no lifecycle or downstream state changes
- Failure proves: the skill overclaims or mutates an unowned surface
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests`
- Required by milestone: M2

### T-PR-018. Preservation ledgers and profile measurement

- Covers: R42-R45, AC-PRSIM-017, AC-PRSIM-018
- Level: contract
- Command IDs: C0, C1
- Fixture/setup: M1 ledgers, baseline and final canonical resources, duplicate clusters, and unknown-value fixture
- Steps: validate closed dispositions, deterministic LF/word/byte assembly, PR0/PR1 reduction, and separate total package report
- Expected result: every item has one owner, unknown values fail first, both profiles shrink, and package growth is explicit
- Failure proves: semantic loss or cosmetic simplification is hidden
- Evidence artifact: `evidence/simplification-measurements.md`, `evidence/semantic-preservation-review.md`
- Automation location: `docs/changes/2026-08-16-pr-skill-simplification/fixtures/validate-pr-simplification.py` and `PRSkillSimplificationTests`
- Required by milestone: M1 and M3

### T-PR-019. Canonical-through-installed parity

- Covers: R46, R47, EC10, AC-PRSIM-019, AC-PRSIM-020
- Level: smoke
- Command IDs: C2, C3, C4, C5, C6
- Fixture/setup: canonical, generated, archive, release-candidate, and clean-installed Codex, Claude, and opencode trees
- Steps: compare inventory, relative paths, and raw bytes; remove or alter one required resource in negative fixtures
- Expected result: every required resource is byte-identical and every missing, stale, extra, or transformed resource fails; no live PR or agent runtime executes
- Failure proves: the published package chain is incomplete or nondeterministic
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing build and adapter suites
- Required by milestone: M3

### T-PR-020. Architecture escalation and published portability

- Covers: R48, R49
- Level: contract
- Command IDs: C1, C2
- Fixture/setup: existing result/report fields, hypothetical new durable evidence owner, hypothetical section parser, and published skill text scans
- Steps: classify architecture applicability and validate shipped text for repository-maintainer leakage
- Expected result: existing evidence remains no-architecture; new owner/parser scenarios require architecture; published text remains project-portable
- Failure proves: scope silently introduces architecture or leaks maintainer mechanics
- Evidence artifact: `architecture-assessment.md`, `evidence/m2-package-implementation.md`
- Automation location: `PRSkillSimplificationTests` and skill validator
- Required by milestone: M2

## Fixtures and data

- Closed YAML or JSON fixtures for signal, intent, refresh, state-transition, branch, PR, operation-result, and CI vocabularies.
- Verification-basis fixtures for portable and governed current evidence and every legacy/incomplete variant.
- Evidence-tail Git-identity fixtures for permitted and forbidden paths, fields, parent relations, and commit counts.
- Deterministic host-state transcripts for base/head/PR rereads, concurrent creation, partial success, read-back failure, and retry.
- PR-body fixtures with reviewer-authored prose, duplicate headings, code fences, nested sections, and whole-body replacement authority.
- Temporary generated, packed, release-candidate, and installed skill trees for all supported adapters.

## Mocking/stubbing policy

Model Git ancestry, remote refs, PR host state, and hosted CI as deterministic local data. Assert the ordered operations and side-effect ledger directly. Do not contact a live provider, use credentials, push a branch, or create/update a real PR for acceptance.

## Migration or compatibility tests

T-PR-013 proves read-old/preparation-only behavior for legacy verify evidence. T-PR-014 proves the narrow verify-owned evidence-tail compatibility rule. T-PR-018 proves semantic and literal disposition. T-PR-019 proves atomic resource migration through every package projection. Historical review and verify reports remain unchanged.

## Observability verification

T-PR-015 through T-PR-017 assert ordered read/reread evidence, actual operation, actual mutation, current PR state, readiness booleans, hosted-CI state, blockers, URL availability, and claim limitations. Measurement and package evidence name exact resource identities and commands.

## Security/privacy verification

Focused fixtures prove unsafe or escaped paths and identities stop, external mutation requires exact authority, force/delete/overwrite operations are absent, and the actual-diff check remains universal. No credentials or personal data are used.

## Performance checks

T-PR-018 measures deterministic loaded words and UTF-8 bytes for PR0 and PR1 and reports asset, representative composition, and total package separately. No runtime latency benchmark is required.

## Manual QA checklist

Not applicable. Every acceptance claim is deterministic and automated; ordinary reviewer inspection during code review and PR review is not a separate manual-proof contract.

## What not to test and why

- Do not open, refresh, publish, convert, close, merge, or otherwise mutate a live PR; acceptance must be deterministic and side-effect free.
- Do not execute Codex, Claude Code, opencode, or another target-agent runtime; content and package contracts are proven statically.
- Do not grade transcripts or add prose classification, tokenizer, or permanent simplicity validators.
- Do not test automatic merge, release, publication, labels, reviewer assignment, or provider engines because they are explicit non-goals.
- Do not infer legacy verification bases; fresh verify is the specified compatibility path.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation milestone M1 only after approving review and workflow handoff.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. It does not authorize implementation until that review settles the exact artifact to active.
