# Explain-Change Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml`

## Related spec and plan

- Spec: `specs/explain-change-skill-simplification.md`
- Plan: `docs/plans/2026-08-18-explain-change-skill-simplification.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260818-ordered-final-review-stage-evidence-tail.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Feature spec | `specs/explain-change-skill-simplification.md` | `spec` | `spec-review-r2` at `docs/changes/2026-08-18-explain-change-skill-simplification/reviews/spec-review-r2.md` |
| Plan | `docs/plans/2026-08-18-explain-change-skill-simplification.md` | `plan` | `plan-review-r2` at `docs/changes/2026-08-18-explain-change-skill-simplification/reviews/plan-review-r2.md` |
| Canonical architecture | `docs/architecture/system/architecture.md` | `architecture-system` | `architecture-review-r1` |
| Ordered evidence-tail ADR | `docs/adr/ADR-20260818-ordered-final-review-stage-evidence-tail.md` | `adr-ordered-tail` | `architecture-review-r1` |

## Testing strategy

Use deterministic standard-library fixtures and repository-owned validators. Focused contract tests establish classification, resource loading, mutation boundaries, identity semantics, and negative claims before canonical package edits. Workflow code-state tests prove exact ancestry and path-and-field ownership, and one real temporary Git repository proves the complete `S -> R -> E -> verify` path. Existing build and adapter suites prove generated, archived, release-candidate, and clean-installed resource integrity. Static measurement proves every real loaded assembly decreases without treating relocation as deletion.

No target-agent runtime, network service, credentials, live PR, transcript grading, or manual semantic-review acceptance stage is used.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T01, T16 | contract, integration | Exact resource inventory and no scripts. |
| R2 | T02, T14 | contract | Universal rule ledger and portable behavior. |
| R3 | T02 | contract | EC0 has no conditional resource dependency. |
| R4 | T01, T12 | contract | Governed reference ownership. |
| R5 | T07 | contract | Skeleton structure-only assertions. |
| R6 | T03 | unit | Closed signal vocabulary. |
| R7 | T03 | unit | Invalid signals fail without fallback. |
| R8 | T03, T05 | contract | Loading does not grant authority. |
| R9 | T04 | unit | Closed independent action vocabulary. |
| R10 | T04 | unit | Create target-state matrix. |
| R11 | T04 | unit | Refresh authority matrix. |
| R12 | T04 | unit | Missing refresh target routes without mutation. |
| R13 | T04, T17 | contract | Portable durable path and forbidden governed creation. |
| R14 | T05 | contract | Four exact assemblies. |
| R15 | T05 | contract | Exhaustive and late-loaded combinations. |
| R16 | T06 | contract | Triggered resource failures stop. |
| R17 | T07, T08 | contract | Current-skeleton whole-file composition. |
| R18 | T07 | contract | Historical artifacts stay unchanged without refresh. |
| R19 | T08 | integration | Full atomic write sequence. |
| R20 | T08 | integration | Uncertain output blocks and fresh retry reclassifies. |
| R21 | T08, T18 | contract | No prepared transaction or new owner. |
| R22 | T09 | contract | Complete reviewed-change basis. |
| R23 | T09, T10 | integration | Reviewed diff excludes evidence tail. |
| R24 | T09, T19 | integration, end-to-end | Four distinct revision roles without self-reference. |
| R25 | T09, T17, T19 | integration, end-to-end | Git-derived recording identities and stage-owned writes. |
| R26 | T10, T19 | integration, end-to-end | Exact non-merge direct-child `S -> R -> E`. |
| R27 | T10, T11, T19 | integration, end-to-end | Closed path-and-field sets for R and E. |
| R28 | T10, T11, T19 | integration, end-to-end | Exact partial retry; every broader or reordered tail stales review. |
| R29 | T10, T19 | integration, end-to-end | Later verify evidence alone is non-staling. |
| R30 | T09, T12 | contract | Required governed metadata. |
| R31 | T12 | integration | Review closeout and concise summary. |
| R32 | T13 | contract | Closed Workflow handback fields. |
| R33 | T13 | contract | Handback applicability matrix. |
| R34 | T13, T17 | contract | Forbidden readiness claims. |
| R35 | T13, T17 | contract | Workflow routing and isolation ownership. |
| R36 | T14 | contract | Semantic and literal ledgers. |
| R37 | T14 | unit | Unknown values fail before consistency. |
| R38 | T15 | contract | Closed LF/word/byte formula. |
| R39 | T15 | contract | All assemblies and package parts reported. |
| R40 | T15 | contract | Every assembly strictly decreases. |
| R41 | T16 | integration | Canonical-through-installed parity. |
| R42 | T17 | contract | Published-text portability. |
| R43 | T01-T19 | contract, integration, end-to-end | Deterministic acceptance only. |
| R44 | T18 | contract | Architecture reassessment trigger. |

## Acceptance criterion coverage map

| Acceptance criterion | Covered by | Command IDs | First required milestone | Notes |
| --- | --- | --- | --- | --- |
| AC1 | T01-T19 | CMD-01-CMD-12 | M1 | Requirement proof starts with M1 inventory, closes package behavior in M2-M3, and closes the amended evidence-tail contract in M4. |
| AC2 | T01, T05, T16 | CMD-01, CMD-02, CMD-05, CMD-06, CMD-07, CMD-08 | M2 | Canonical inventory proves one root, one governed reference, one skeleton, and no script; M3 proves packaged parity. |
| AC3 | T03, T05 | CMD-01 | M2 | Closed signal classification and all four governance/output assemblies are exercised directly. |
| AC4 | T04, T07, T08 | CMD-01 | M2 | Target-state selection, refresh authority, skeleton composition, and atomic replacement are composed in one proof slice. |
| AC5 | T08 | CMD-01 | M2 | Concurrency, uncertain replacement, read-back failure, and fresh retry each have a fail-closed outcome. |
| AC6 | T09, T10, T19 | CMD-03, CMD-04, CMD-12 | M4 | Reviewed subject, final-review recording, explanation recording, and handoff identities remain distinct without self-reference. |
| AC7 | T10, T11, T19 | CMD-03, CMD-04, CMD-12 | M4 | Exact `S -> R -> E`, closed path-and-field sets, partial retry, and every broader or reordered tail receive opposite deterministic outcomes. |
| AC8 | T13, T17 | CMD-01, CMD-03, CMD-04, CMD-05 | M2 | Handback fields expose explanation-owned state while forbidden readiness and routing claims fail. |
| AC9 | T07 | CMD-01 | M2 | Untouched historical artifacts remain byte-identical and an authorized refresh adopts the current skeleton. |
| AC10 | T14 | CMD-01 | M1 | Complete semantic and literal ledgers require one closed disposition and owner for every current item. |
| AC11 | T15 | CMD-01 | M1 | The baseline starts in M1; M3 must show strict reduction for EC0 through EC3 and visible total-package size. |
| AC12 | T16 | CMD-02, CMD-05, CMD-06, CMD-07, CMD-08 | M3 | Canonical, generated, archived, release-candidate, and clean-installed inventories and bytes are compared. |
| AC13 | T03, T04, T14 | CMD-01 | M1 | Unknown signal, action, ledger-treatment, and ownership values fail before consistency evaluation. |
| AC14 | T17 | CMD-01, CMD-05 | M3 | Published-text and acceptance-surface assertions exclude target-agent execution, manual semantic review, and prose grading. |
| AC15 | T18 | CMD-01, CMD-10 | M1 | Any new identity, transaction, schema, lifecycle, routing, parser, generator, or cross-stage owner blocks M2 and routes to architecture. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T02 | Portable inline uses EC0 and writes nothing. |
| E2 | T05, T08, T09, T12, T13 | Governed durable path loads EC3 and completes its owned work. |
| E3 | T03 | Malformed signals stop before fallback. |
| E4 | T04, T07, T08 | Explicit refresh uses whole-file skeleton composition. |
| E5 | T09, T10, T19 | Ordered final-review and explanation commits preserve the reviewed subject. |
| E6 | T11, T19 | Broader post-review paths or fields stale review reuse. |
| E7 | T10, T11, T19 | One exact `S -> R` interruption may resume with E; intervening or reordered commits may not. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R6, R7, R9, R10, R11, R12, R13, R32, R37 | BND-INPUT-001 | T03, T04, T13, T14 | contract | automated | CMD-01 | M1/M2 evidence | M2 | - | - |
| PRF-002 | covered | R10, R11, R12, R18, R20, R22, R23, R24, R26, R28, R29, R30, R31 | BND-STATE-001 | T04, T07, T08, T09, T10, T11, T12, T19 | end-to-end | automated | CMD-01, CMD-03, CMD-04, CMD-12 | M2/M4 evidence | M4 | - | - |
| PRF-003 | covered | R7, R8, R10, R11, R13, R22, R25, R26, R27, R28, R31, R35 | BND-AUTH-001 | T03, T04, T09, T10, T11, T12, T13, T17, T19 | end-to-end | automated | CMD-01, CMD-03, CMD-04, CMD-12 | M2/M4 evidence | M4 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R14, R15, R16, R17, R32, R33, R41, R42 | BND-COMPOSE-001 | T01, T02, T05, T06, T07, T13, T16, T17 | integration | automated | CMD-01, CMD-02, CMD-06, CMD-07, CMD-08 | M2/M3 evidence | M3 | - | - |
| PRF-005 | covered | R11, R15, R19, R20, R23, R24, R26, R27, R28, R29 | BND-TEMPORAL-001 | T04, T05, T08, T09, T10, T11, T19 | end-to-end | automated | CMD-01, CMD-03, CMD-04, CMD-12 | M2/M4 evidence | M4 | - | - |
| PRF-006 | covered | R16, R19, R20, R21, R28, R31, R44 | BND-RECOVERY-001 | T06, T08, T10, T11, T12, T18, T19 | integration | automated | CMD-01, CMD-03, CMD-04, CMD-12 | M1/M2/M4 evidence | M4 | - | - |
| PRF-007 | covered | R17, R18, R32, R34, R36, R37, R38, R39, R40, R41, R42 | BND-COMPAT-001 | T07, T13, T14, T15, T16, T17 | integration | automated | CMD-01, CMD-05, CMD-06, CMD-07, CMD-08 | M3 evidence | M3 | - | - |
| PRF-008 | covered | R13, R16, R19, R20, R25, R26, R41, R43 | BND-ENV-001 | T06, T08, T09, T10, T11, T16, T17, T19 | end-to-end | automated | CMD-01, CMD-03, CMD-04, CMD-08, CMD-12 | M2/M3/M4 evidence | M4 | - | - |
| PRF-009 | covered | R6, R7, R8, R13, R14, R15 | INT-001 | T03, T05 | contract | automated | CMD-01 | M2 evidence | M2 | - | - |
| PRF-010 | covered | R10, R11, R12, R17, R19, R20 | INT-002 | T04, T07, T08 | integration | automated | CMD-01 | M2 evidence | M2 | - | - |
| PRF-011 | covered | R22, R23, R24, R25, R26, R27, R28, R29 | INT-003 | T09, T10, T11, T19 | end-to-end | automated | CMD-03, CMD-04, CMD-12 | M4 evidence | M4 | - | - |
| PRF-012 | covered | R30, R32, R33, R34, R35 | INT-004 | T12, T13, T17 | contract | automated | CMD-01, CMD-03, CMD-04 | M2 evidence | M2 | - | - |
| PRF-013 | covered | R2, R4, R5, R14, R16, R36, R38, R39, R40, R41 | INT-005 | T01, T02, T05, T06, T07, T14, T15, T16 | integration | automated | CMD-01, CMD-02, CMD-05, CMD-06, CMD-07, CMD-08, CMD-09 | M3 evidence | M3 | - | - |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 | T04 | Missing portable path blocks without governed root. |
| EC2 | T08 | Target appearance before create commit blocks. |
| EC3 | T04 | Missing refresh target routes to creation without mutation. |
| EC4 | T05 | Late governed discovery loads reference before output. |
| EC5 | T06 | Missing skeleton blocks durable action. |
| EC6 | T08 | Read-back mismatch prevents completion. |
| EC7 | T10, T19 | Later verify evidence does not stale the closed pre-verify tail. |
| EC8 | T11 | An unlisted `change.yaml` field in R or E is rejected even though the path is allowed. |
| EC9 | T07 | Historical layout is untouched until full refresh. |
| EC10 | T15 | Any non-decreasing assembly fails acceptance. |
| EC11 | T10, T19 | Exact `S -> R` may resume with E without rewriting R. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD-01 | `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests` | planned-for-implementation | implement | M1/M2 | M1 | stop milestone | zero tests fail | milestone evidence | local deterministic fixtures only |
| CMD-02 | `python scripts/validate-skills.py skills/explain-change/SKILL.md` | existing/configured | implement | M2/M3 | M2 | stop milestone | not applicable | milestone evidence | read-only validation |
| CMD-03 | `python scripts/test-workflow-automation-state.py` | existing/configured | implement | M2 | M2 | stop milestone | zero tests fail | M2 evidence | local temporary fixtures |
| CMD-04 | `python scripts/test-workflow-automation.py` | existing/configured | implement | M2 | M2 | stop milestone | zero tests fail | M2 evidence | local temporary fixtures |
| CMD-05 | `python scripts/test-skill-validator.py` | existing/configured | implement | M2/M3 | M2 | stop milestone | zero tests fail | milestone evidence | local repository tests |
| CMD-06 | `python scripts/test-build-skills.py` | existing/configured | implement | M2/M3 | M2 | stop milestone | zero tests fail | milestone evidence | temporary build trees only |
| CMD-07 | `python scripts/build-skills.py --check` | existing/configured | implement | M2/M3 | M2 | stop milestone | not applicable | milestone evidence | check mode; no canonical write |
| CMD-08 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 | stop milestone | zero tests fail | M3 package proof | temporary package/install trees only |
| CMD-09 | `python scripts/validate-boundary-first.py --check --path specs/explain-change-skill-simplification.md` | existing/configured | implement | M3 | M3 | stop milestone | not applicable | M3 package proof | read-only contract validation |
| CMD-10 | `python scripts/validate-change-metadata.py docs/changes/2026-08-18-explain-change-skill-simplification/change.yaml` | existing/configured | workflow | all | before every promotion | stop promotion | not applicable | change-local lifecycle evidence | read-only validation |
| CMD-11 | `python scripts/validate-documentation-prose.py --mode audit --path specs/explain-change-skill-simplification.md --path specs/explain-change-skill-simplification.test.md --path docs/plans/2026-08-18-explain-change-skill-simplification.md` | existing/configured | implement | M3 | M3 | stop milestone | not applicable | M3 package proof | read-only prose audit |
| CMD-12 | `python scripts/test-workflow-code-state.py` | existing/configured | implement | M4 | M4 | stop milestone | zero tests fail | M4 ordered-tail evidence | temporary Git repositories and read-only repository inspection |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T14, T15, T18 | none | CMD-01, CMD-10 | M1 preservation inventories and profile baseline | M1 code review | Canonical package remains unchanged. |
| M2 | T01-T13, T17 | none | CMD-01-CMD-07, CMD-10 | M2 package implementation evidence | M2 code review | Direct behavior and compatibility proof precede settlement. |
| M3 | T14-T16 | none | CMD-01, CMD-02, CMD-05-CMD-11 | measurements, semantic preservation, and package proof | M3 code review | All-profile and package-chain gates close together. |
| M4 | T09-T11, T19 | none | CMD-01, CMD-03, CMD-04, CMD-05, CMD-07, CMD-10, CMD-12 | M4 ordered evidence-tail implementation evidence | M4 code review | Direct proof covers identities, fields, ancestry, partial retry, stale cases, and the public workflow path. |
| M5 | T01-T19 | none | CMD-01-CMD-12 | final review at S, review evidence at R, explanation and handback at E, and later verify evidence | final verify | Lifecycle closeout applies the implemented protocol and adds no implementation scope. |

## Test cases

### T01. Package inventory and ownership

- Covers: R1, R4, R43; PRF-004, PRF-013
- Level: contract
- Command IDs: CMD-01, CMD-02
- Fixture/setup: canonical explain-change package fixture
- Steps: assert exactly one root, one governed reference, one skeleton, mapped verbs, and no script or extra policy resource
- Expected result: inventory and ownership match the contract
- Failure proves: package boundary drift or hidden runtime expansion
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T02. Universal portable inline behavior

- Covers: R2, R3; E1; PRF-004, PRF-013
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: no governed signal and exact local diff
- Steps: select inline action, resolve EC0, inspect universal rules and forbidden writes
- Expected result: safe explanation from `SKILL.md` only
- Failure proves: universal safety moved behind a trigger
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T03. Governed-signal classification

- Covers: R6-R8; E3; PRF-001, PRF-003, PRF-009
- Level: unit
- Command IDs: CMD-01
- Fixture/setup: no signal, one valid signal, and malformed/duplicate/conflicting/escaped/unknown variants
- Steps: classify each fixture before authority or action checks
- Expected result: exact three-state result; invalid variants stop without portable fallback
- Failure proves: classifier vocabulary or fail-closed ordering defect
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T04. Output action and refresh authority matrix

- Covers: R9-R13; E4; EC1, EC3; PRF-001-PRF-003, PRF-005, PRF-010
- Level: unit
- Command IDs: CMD-01
- Fixture/setup: absent/existing/ambiguous targets and user/governed/no refresh authority
- Steps: evaluate every admitted matrix row and unknown action
- Expected result: one action or exact stop; no implicit governed state
- Failure proves: create/refresh overlap or authority leakage
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T05. Four assemblies and late loading

- Covers: R8, R14, R15; E2; EC4; PRF-004, PRF-005, PRF-009, PRF-013
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: four governance/output combinations and late signal/durability discovery
- Steps: resolve resource inventory before and after late triggers
- Expected result: exactly EC0, EC1, EC2, or EC3 with no duplicate load
- Failure proves: non-exhaustive or underloaded procedure
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T06. Triggered resource failure

- Covers: R16; EC5; PRF-004, PRF-006, PRF-008
- Level: contract
- Command IDs: CMD-01, CMD-06
- Fixture/setup: missing, unreadable, escaped, mixed-version, and contradictory resource variants
- Steps: invoke each dependent assembly
- Expected result: dependent work blocks and no remembered reconstruction occurs
- Failure proves: resource failure weakens safety
- Evidence artifact: M2/M3 package evidence
- Automation location: skill and build validator fixtures
- Required by milestone: M2

### T07. Skeleton ownership and historical adoption

- Covers: R5, R17, R18; EC9; PRF-004, PRF-007, PRF-010, PRF-013
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: new durable artifact, authorized historical refresh, and untouched historical artifact
- Steps: inspect structure and forbidden policy prose
- Expected result: create/refresh uses complete current skeleton; untouched history stays byte-identical
- Failure proves: structure/procedure drift or bulk migration
- Evidence artifact: M2 package evidence
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M2

### T08. Atomic replacement and uncertain recovery

- Covers: R19-R21; EC2, EC6; PRF-002, PRF-005, PRF-006, PRF-008, PRF-010
- Level: integration
- Command IDs: CMD-01
- Fixture/setup: matching baseline, concurrent target creation/change, replacement failure, and read-back mismatch
- Steps: execute the modeled preflight/write/read-back states
- Expected result: one complete atomic result or blocked fresh retry; no partial adoption
- Failure proves: overwrite, recovery, or transaction-boundary defect
- Evidence artifact: M2 package evidence
- Automation location: deterministic filesystem fixture
- Required by milestone: M2

### T09. Reviewed-change basis and recording identities

- Covers: R22-R25, R30; PRF-002, PRF-003, PRF-005, PRF-011
- Level: integration
- Command IDs: CMD-03, CMD-04, CMD-12
- Fixture/setup: approved final review, exact base and subject S, final-review revision R, explanation revision E, explanation path, and workflow handoff
- Steps: resolve metadata and compare reviewed-subject, final-review-recording, explanation-recording, handoff, content, and governing-basis identities
- Expected result: complete non-self-referential four-part basis with the reviewed diff ending at S and handoff equal to E
- Failure proves: identity conflation or stale evidence acceptance
- Evidence artifact: M4 ordered-tail evidence
- Automation location: workflow code-state and automation tests
- Required by milestone: M4

### T10. Permitted ordered evidence tail and partial retry

- Covers: R23, R26, R29; E5, EC7; PRF-002, PRF-003, PRF-005, PRF-008, PRF-011
- Level: integration
- Command IDs: CMD-03, CMD-04, CMD-12
- Fixture/setup: exact direct-child S, R, and E commits; exact `S -> R` interrupted state; and later verify evidence
- Steps: validate non-merge ancestry, R and E path-and-field manifests, unchanged governing basis, E handoff identity, exact partial retry, and the pre-verify cutoff
- Expected result: `S -> R -> E` preserves final-review reuse; exact `S -> R` may create only E without repeating R; later verify evidence is not retroactively claimed
- Failure proves: self-staleness or cutoff confusion
- Evidence artifact: M4 ordered-tail evidence
- Automation location: workflow code-state and automation tests
- Required by milestone: M4

### T11. Forbidden, reordered, or broader evidence tails

- Covers: R27-R29; E6, EC8; PRF-002, PRF-003, PRF-005, PRF-006, PRF-008, PRF-011
- Level: integration
- Command IDs: CMD-03, CMD-04, CMD-12
- Fixture/setup: forbidden product and documentation paths; allowed shared paths with unknown or sibling fields; reversed R/E order; merge, intervening, additional, non-child, changed-basis, and recorded/Git identity mismatch tails
- Steps: validate each revision's ancestry, exact path set, semantic field set, stage order, and recorded identity against Git
- Expected result: every unknown, broader, reordered, merged, intervening, or mismatched tail stales final-review reuse
- Failure proves: stale or unrelated changes bypass final review
- Evidence artifact: M4 ordered-tail evidence
- Automation location: workflow code-state and automation tests
- Required by milestone: M4

### T12. Governed review closeout and metadata

- Covers: R4, R30, R31; E2; PRF-002, PRF-006, PRF-012
- Level: integration
- Command IDs: CMD-01, CMD-03, CMD-04
- Fixture/setup: clean receipt, closed detailed resolution, open finding, needs-decision, and missing review evidence
- Steps: resolve governed completion and concise disposition summary
- Expected result: only current closed evidence completes; blockers remain exact
- Failure proves: review settlement or staleness bypass
- Evidence artifact: M2 package evidence
- Automation location: skill/workflow validator fixtures
- Required by milestone: M2

### T13. Workflow handback and forbidden readiness claims

- Covers: R32-R35; PRF-001, PRF-003, PRF-004, PRF-007, PRF-012
- Level: contract
- Command IDs: CMD-01, CMD-03, CMD-04
- Fixture/setup: portable inline/durable and governed inline/durable complete/blocked outcomes
- Steps: assert applicability, fields, values, decision owner, and forbidden phrases
- Expected result: only explanation-owned state is emitted and workflow remains route owner
- Failure proves: claim or ownership overreach
- Evidence artifact: M2 package evidence
- Automation location: skill/workflow validator fixtures
- Required by milestone: M2

### T14. Semantic and literal ledgers

- Covers: R2, R36, R37; PRF-001, PRF-007, PRF-013
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: complete disposition ledgers plus unknown classifications and owners
- Steps: validate coverage, closed vocabularies, owner uniqueness, and unknown-first behavior
- Expected result: every current item has one valid treatment and unknowns fail explicitly
- Failure proves: semantic loss, literal drift, or silent vocabulary fallback
- Evidence artifact: M1 preservation inventories
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M1

### T15. Assembly measurement gates

- Covers: R38-R40; EC10; PRF-007, PRF-013
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: LF-normalized canonical files and frozen flat baseline
- Steps: compute EC0-EC3, each resource, and total package words/bytes; exercise equal/growing variants
- Expected result: every assembly strictly decreases and total package remains visible
- Failure proves: measurement ambiguity or root-only optimization
- Evidence artifact: baseline and simplification measurements
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M1 and M3

### T16. Canonical-through-installed parity

- Covers: R1, R41; PRF-004, PRF-007, PRF-008, PRF-013
- Level: integration
- Command IDs: CMD-02, CMD-05, CMD-06, CMD-07, CMD-08
- Fixture/setup: canonical, generated, archive, release-candidate, and clean-install package trees
- Steps: compare inventories, mappings, and raw bytes; exercise missing/extra/transformed variants
- Expected result: required resources match exactly and drift fails
- Failure proves: packaging or distribution defect
- Evidence artifact: M3 package proof
- Automation location: existing build and adapter suites
- Required by milestone: M3

### T17. Portability, privacy, writes, and claims

- Covers: R13, R25, R27, R34, R35, R42; PRF-003, PRF-004, PRF-007, PRF-008, PRF-012
- Level: contract
- Command IDs: CMD-01, CMD-05
- Fixture/setup: customer-project package, sensitive/machine-local evidence, and forbidden mutation/readiness phrases
- Steps: inspect published text and simulated results
- Expected result: no repository-maintainer leakage, sensitive data, cross-stage write, external mutation, or readiness overclaim
- Failure proves: portability, privacy, or authority regression
- Evidence artifact: semantic preservation review
- Automation location: skill validator
- Required by milestone: M2/M3

### T18. Architecture reassessment trigger

- Covers: R21, R44; PRF-006
- Level: contract
- Command IDs: CMD-01, CMD-10
- Fixture/setup: implementation inventory with and without new persistence, schema, lifecycle, routing, cross-stage, parser, or generator needs
- Steps: classify architecture applicability before M4 mutation against accepted ADR-20260818
- Expected result: the accepted Git-derived model proceeds; any additional persistence, schema, lifecycle state, write owner, or broader transaction blocks and routes to architecture
- Failure proves: architecture scope is silently expanded
- Evidence artifact: M4 ordered-tail evidence and architecture basis
- Automation location: focused scenario fixture
- Required by milestone: M4

### T19. Real Git S-to-R-to-E-to-verify journey

- Covers: R23-R29; E5-E7; EC7, EC8, EC11; PRF-002, PRF-003, PRF-005, PRF-006, PRF-008, PRF-011
- Level: end-to-end
- Command IDs: CMD-12, CMD-04
- Fixture/setup: a temporary Git repository with minimal governed change metadata, reviewed implementation subject S, formal final-review files and settlement fields for R, explanation and handback fields for E, and a later verify-owned evidence commit
- Steps: create and commit S; create only allowed review files and fields and commit R; exercise exact `S -> R` retry classification; create only allowed explanation and handback files and fields and commit E; resolve code state and invoke the verify-facing workflow predicate; add verify-owned evidence after E and re-evaluate the recorded pre-verify basis
- Expected result: Git-derived identities equal the committed S, R, and E revisions; E is handoff; the reviewed diff remains base-to-S; exact path-and-field manifests pass; verify accepts the closed tail; later verify evidence does not retroactively enter or stale it
- Failure proves: helper-only proof, synthetic identity proof, self-reference, stage-order, semantic-diff, recovery, or verify-integration defect
- Evidence artifact: `docs/changes/2026-08-18-explain-change-skill-simplification/evidence/m4-ordered-evidence-tail.md`
- Automation location: `scripts/test-workflow-code-state.py` using a temporary repository and the public code-state/workflow entry points
- Required by milestone: M4

## Fixtures and data

- `docs/changes/2026-08-18-explain-change-skill-simplification/fixtures/explain-change-simplification-scenarios.yaml` owns deterministic classification, action, assembly, target, resource, write, tail, handback, and architecture-trigger cases.
- Rule and literal disposition YAML files own closed preservation inventories.
- `scripts/test-workflow-code-state.py` owns the real temporary-repository S/R/E ancestry, semantic shared-file diff, retry, and later verify-evidence journey.
- Existing build and adapter fixtures own generated, archive, release-candidate, and install trees.

Fixtures use fixed identities, paths, and content. They do not use wall-clock time, network, credentials, shared mutable state, or random ordering.

## Mocking/stubbing policy

Use temporary local repositories and filesystem fixtures for Git and atomic-write states. Stub no semantic outcome and no package inventory. External providers and target-agent runtimes are outside scope.

## Migration or compatibility tests

T07 proves prospective skeleton adoption without bulk migration. T09-T13 preserve current final-diff and final-review consumers while migrating misleading readiness structure. T14 proves exact rule and literal dispositions. T16 proves every supported package form migrates atomically and rollback can restore the flat package.

## Observability verification

T03-T13 and T19 assert exact classifications, actions, assemblies, blockers, identities, field ownership, cutoffs, and handback fields. T15 and T16 produce reproducible measurements and parity diagnostics naming the failed assembly, resource, or package surface.

## Security/privacy verification

T03, T04, T06, T11, T13, T17, and T19 cover escaped paths, invalid authority, missing resources, unrelated paths and fields, readiness overclaims, secrets, personal data, and machine-local leakage. No external mutation is authorized.

## Performance checks

T15 is the complete performance proof: exact words and UTF-8 bytes for each loaded assembly. Runtime latency and model behavior are not applicable.

## Manual QA checklist

Not applicable. All acceptance obligations are deterministically inspectable through repository-owned contract, fixture, validator, measurement, and package proof. Ordinary lifecycle reviews remain judgment gates but are not test-spec manual procedures.

## What not to test and why

- Do not execute Codex, Claude Code, opencode, or another target-agent runtime; the contract is static package ownership and authority behavior.
- Do not grade explanation prose or transcripts; ordinary code, verification, and PR review own semantic judgment.
- Do not open a live PR, contact hosted CI, or use credentials; no acceptance outcome depends on external mutation.
- Do not test section-level refresh, managed regions, historical-layout parsing, a new persistent transaction service, or a new identity service because the approved spec excludes them. The existing Git-derived R/E manifest validation remains in scope.
- Do not rewrite historical explanation artifacts merely to exercise the skeleton.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation only after formal approval and workflow promotion.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. This proof map does not claim tests are implemented or executed, implementation handoff is allowed, validation passed, verification passed, branch readiness, or PR readiness.
