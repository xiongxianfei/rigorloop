# Vision Skill Progressive Disclosure Test Specification

## Owning change record

`docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

## Related spec and plan

- Spec: `specs/vision-skill-progressive-disclosure.md`
- Plan: `docs/plans/2026-08-17-vision-skill-progressive-disclosure.md`
- Architecture/ADRs: not required; `docs/changes/2026-08-17-vision-skill-progressive-disclosure/architecture-assessment.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| proposal | `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md` | proposal | `proposal-review-r5` |
| specification | `specs/vision-skill-progressive-disclosure.md` | spec, sha256 `75838eb48ce591e9f4c5a6ade209b6e99f0ff5fa1f66f451c4a7ce70ba2abe08` | `spec-review-r2` and `reviews/spec-review-r2.md` |
| architecture assessment | `docs/changes/2026-08-17-vision-skill-progressive-disclosure/architecture-assessment.md` | architecture-assessment, sha256 `a9a156f9b19ef098dd6779fb71666f34babfc1103ff1c7786232853bad296691` | `architecture-not-required` |
| execution plan | `docs/plans/2026-08-17-vision-skill-progressive-disclosure.md` | plan, sha256 `2e77376d327ae3bcdb581f5a6d63c6acaecba9be326146bb7828832e55f10997` | `plan-review-r1` and `reviews/plan-review-r1.md` |

## Testing strategy

Use deterministic standard-library contract fixtures for operation, significance, resource, action, marker, manifest, result, retry, and compatibility behavior. Use repository-owned skill, build, adapter, boundary, and lifecycle validators for package and integration proof. Model writes and interruptions with local fixtures and side-effect ledgers; do not change the project vision artifacts, execute a target-agent runtime, grade transcripts, or introduce a separate manual semantic-review gate.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R7 | T-VIS-001 | contract | Package inventory, ownership, mappings, authority separation, and missing-resource stops. |
| R8-R17 | T-VIS-002, T-VIS-003 | contract | Three operations, significance, state routing, independent contexts, and late strategic escalation. |
| R18-R27 | T-VIS-003, T-VIS-004 | contract | Default synchronization, pre-resolved and late skip, markers, exact authority, and planned transitions. |
| R28-R33 | T-VIS-005 | contract | Independent positioning and README actions for establishment and revision. |
| R34-R39 | T-VIS-006 | contract | Structural-only assets, selection predicates, and prospective adoption. |
| R40-R42 | T-VIS-003 | contract | Six assemblies, primary/secondary distinction, and establishment assembly. |
| R43-R47 | T-VIS-007 | contract | Manifest preparation, target fields, zero-write skip, and pre-write validation. |
| R48-R50 | T-VIS-008 | integration | Source-first writes, pre-README revalidation, and complete read-back. |
| R51-R53 | T-VIS-009 | contract | Closed results, zero-write truthfulness, and partial reporting. |
| R54-R56 | T-VIS-010 | integration | Governed prepared evidence, exact retry, concurrency, and non-adoption. |
| R57 | T-VIS-011 | contract | Portable cross-session recovery fails closed without its manifest. |
| R58-R60 | T-VIS-012 | contract | Separate semantic/literal ledgers and unknown-value-first validation. |
| R61-R63 | T-VIS-013 | contract | Deterministic six-assembly measurement and visible package totals. |
| R64 | T-VIS-014 | smoke | Canonical-through-installed inventory and raw-byte parity. |
| R65-R66 | T-VIS-015 | contract | Deterministic acceptance exclusions and architecture escalation. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T-VIS-003 | Normal explicit synchronization selects `VA0-readme-sync`. |
| E2 | T-VIS-004, T-VIS-007, T-VIS-009 | Pre-resolved skip loads no README procedure and settles truthfully with a zero-write manifest. |
| E3 | T-VIS-003, T-VIS-004 | Marker-dependent skip retains its non-`S` assembly. |
| E4 | T-VIS-002, T-VIS-003 | Late strategic evidence loads the reference and reclassifies before writing. |
| E5 | T-VIS-005, T-VIS-007, T-VIS-008 | Material repositioning prepares and commits all applicable targets source-first. |
| E6 | T-VIS-009, T-VIS-010 | Exact retry completes only a pending README target. |
| E7 | T-VIS-004 | Invalid markers without exact authority block before writes. |
| E8 | T-VIS-006 | Narrow historical revision preserves existing structure. |
| E9 | T-VIS-001, T-VIS-014 | Required resource loss blocks locally and in package projections. |
| E10 | T-VIS-011 | Lost portable recovery context is not reconstructed or adopted. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 malformed markers with pre-resolved skip | T-VIS-004 | Whole-file identity settles without marker parsing or validity claims. |
| EC2 skip arrives after marker inspection | T-VIS-003, T-VIS-004 | The invocation retains the non-`S` assembly. |
| EC3 README changes after skip binding | T-VIS-004, T-VIS-010 | Identity drift invalidates settlement and blocks adoption. |
| EC4 full canonical rewrite with README skip | T-VIS-006 | Vision skeleton remains required independently of README loading. |
| EC5 material repositioning creates rationale while README skips | T-VIS-005, T-VIS-006 | Positioning skeleton remains required independently. |
| EC6 canonical commit with pending rationale or README | T-VIS-009, T-VIS-010 | Result is `partial-retry-required`, never complete. |
| EC7 unknown marker-evidence value | T-VIS-002, T-VIS-012 | Vocabulary error occurs before consistency checks. |
| EC8 installed resource missing | T-VIS-014 | Package parity fails. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R8, R9, R10, R11, R28, R40, R51 | BND-INPUT-001 | T-VIS-002, T-VIS-003, T-VIS-005, T-VIS-009, T-VIS-012 | contract | automated | C0, C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-002 | covered | R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R30, R31, R32, R33, R43, R47, R48, R49, R50, R51, R52, R53, R54 | BND-STATE-001 | T-VIS-002, T-VIS-003, T-VIS-004, T-VIS-005, T-VIS-007, T-VIS-008, T-VIS-009, T-VIS-010 | integration | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-003 | covered | R5, R12, R13, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R30, R32, R33, R43, R44, R45, R46, R47, R49, R54 | BND-AUTH-001 | T-VIS-001, T-VIS-002, T-VIS-004, T-VIS-005, T-VIS-007, T-VIS-008, T-VIS-010 | contract | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-004 | covered | R1, R2, R3, R4, R5, R6, R7, R10, R15, R16, R17, R34, R35, R36, R37, R38, R39, R40, R41, R42 | BND-COMPOSE-001 | T-VIS-001, T-VIS-003, T-VIS-006, T-VIS-013, T-VIS-014 | contract | automated | C1, C2, C3, C4, C5, C6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-005 | covered | R25, R26, R27, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54, R55, R56, R57 | BND-TEMPORAL-001 | T-VIS-004, T-VIS-007, T-VIS-008, T-VIS-009, T-VIS-010, T-VIS-011 | integration | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-006 | covered | R7, R11, R17, R23, R32, R47, R49, R51, R52, R53, R54, R55, R56, R57, R66 | BND-RECOVERY-001 | T-VIS-001, T-VIS-002, T-VIS-004, T-VIS-009, T-VIS-010, T-VIS-011, T-VIS-015 | integration | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-007 | covered | R34, R35, R36, R37, R38, R39, R58, R59, R60, R61, R62, R63, R64 | BND-COMPAT-001 | T-VIS-006, T-VIS-012, T-VIS-013, T-VIS-014 | contract | automated | C0, C2, C3, C4, C5, C6 | `evidence/semantic-preservation-review.md` | M3 | - | - |
| PRF-008 | covered | R7, R43, R47, R48, R49, R50, R53, R54, R56, R57, R64, R65, R66 | BND-ENV-001 | T-VIS-001, T-VIS-007, T-VIS-008, T-VIS-009, T-VIS-010, T-VIS-011, T-VIS-014, T-VIS-015 | integration | automated | C2, C6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R10, R15, R16, R17, R40 | INT-001 | T-VIS-002, T-VIS-003 | contract | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-010 | covered | R20, R21, R22, R23, R25, R27, R40, R45, R46, R52 | INT-002 | T-VIS-003, T-VIS-004, T-VIS-007, T-VIS-009 | contract | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-011 | covered | R25, R26, R43, R47, R48, R49, R50, R53, R54, R55, R56 | INT-003 | T-VIS-004, T-VIS-007, T-VIS-008, T-VIS-009, T-VIS-010 | integration | automated | C2 | `evidence/m2-package-implementation.md` | M2 | - | - |
| PRF-012 | covered | R34, R35, R36, R37, R38, R39, R58, R59, R61, R62, R63, R64 | INT-004 | T-VIS-006, T-VIS-012, T-VIS-013, T-VIS-014 | contract | automated | C0, C2, C3, C4, C5, C6 | `evidence/m3-package-proof.md` | M3 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C0 | `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureLedgerTests` | planned-for-implementation | M1 | M1 | M1 | Stop M1 and correct missing dispositions, unknown values, invalid scenarios, or nondeterministic baselines. | Zero selected tests is failure. | `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m1-preservation-inventories.md` | Repository-local deterministic fixtures; canonical vision package remains unchanged. |
| C1 | `python scripts/validate-skills.py skills/vision/SKILL.md` | existing/configured | skill validator | M2 | M2 | Stop on invalid skill structure, resource mapping, claims, or portability. | Not applicable. | M2 and M3 evidence | Reads the canonical skill package only. |
| C2 | `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureTests` | planned-for-implementation | M2 | M2 | M2 | Stop M2 and correct focused contract or fixture failure. | Zero selected tests is failure. | `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m2-package-implementation.md` | Local deterministic fixtures only; no project vision or README mutation. |
| C3 | `python scripts/test-skill-validator.py` | existing/configured | skill validator suite | M2 | M2 | Stop on any skill-contract regression. | Zero tests is failure. | M2 and M3 evidence | Repository-local tests only. |
| C4 | `python scripts/test-build-skills.py` | existing/configured | skill build tests | M2 | M2 | Stop on generation or inventory regression. | Zero tests is failure. | M2 and M3 evidence | Temporary or local generated output only. |
| C5 | `python scripts/build-skills.py --check` | existing/configured | skill builder | M2 | M2 | Stop on canonical/generated drift. | Not applicable. | M2 and M3 evidence | Check mode only. |
| C6 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution suite | M3 | M3 | Stop on archive, release-candidate, or clean-install parity failure. | Zero tests is failure. | `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m3-package-proof.md` | Temporary package and install trees only; no publication. |
| C7 | `python scripts/validate-boundary-first.py --check --path specs/vision-skill-progressive-disclosure.md` | existing/configured | boundary validator | M3 | M3 | Stop on missing, stale, malformed, or unproved boundary mapping. | Not applicable. | M3 evidence | Reads the approved spec and this proof map only. |
| C8 | `python scripts/validate-change-metadata.py docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml` | existing/configured | change metadata validator | M1 | M1 | Stop on invalid lifecycle metadata. | Not applicable. | Every milestone evidence | Reads the owning change record only. |
| C9 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | ci-owned | repository CI contract | M4 | M4 | Stop final verification and route the failing check to its owner. | Zero-test success is forbidden by owned child commands. | final verify report | Final local CI orchestration; does not open a PR. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T-VIS-012, T-VIS-013 | none | C0, C8 | `evidence/m1-preservation-inventories.md`, `evidence/profile-size-baseline.md` | M1 code review | Freezes semantic rules, literals, scenarios, and baselines before package edits. |
| M2 | T-VIS-001-T-VIS-012, T-VIS-015 | none | C1, C2, C3, C4, C5, C8 | `evidence/m2-package-implementation.md` | M2 code review | Proves package ownership, behavior, authority, manifests, and recovery. |
| M3 | T-VIS-012-T-VIS-015 | none | C1, C3, C4, C5, C6, C7, C8 | measurements, semantic preservation, and `evidence/m3-package-proof.md` | M3 code review | Proves six-profile reduction and package parity. |
| M4 | T-VIS-001-T-VIS-015 | none | C0-C9 | final review, explanation, and verify report | PR handoff | Lifecycle closeout only; no implementation scope. |

## Test cases

### T-VIS-001. Package inventory, ownership, and resource failure

- Covers: R1-R7, E9, BND-COMPOSE-001, BND-ENV-001
- Level: contract
- Command IDs: C1, C2
- Fixture/setup: canonical package with the expected main file, two references, two assets, exact mappings, and missing, escaped, stale, contradictory, mixed-version, and transformed resource variants
- Steps: validate inventory, verbs, paths, containment, deterministic triggers, ownership boundaries, no helper script, and each failure variant
- Expected result: each rule and structure has one owner; loading grants no authority; every invalid required resource blocks dependent work without reconstruction
- Failure proves: package composition can weaken universal safety or silently omit required procedure
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-002. Operation, state, significance, and unknown vocabulary

- Covers: R8-R17, EC7, BND-INPUT-001, BND-STATE-001, INT-001
- Level: contract
- Command IDs: C2
- Fixture/setup: absent and existing canonical vision, explicit establishment, revision, sync, read-only question, every significance/context value, and `unknown_value`
- Steps: classify operation and repository state, validate vocabulary first, route mismatches, and introduce late strategic evidence before mutation
- Expected result: exactly three mutations exist; read-only questions stay outside; state mismatch routes explicitly; unknown values fail first; substantive or late strategic work loads required procedure before judgment
- Failure proves: operation selection, state routing, or progressive disclosure is incomplete
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests.test_operation_unknown_value`
- Required by milestone: M2

### T-VIS-003. Six loaded assemblies and late reclassification

- Covers: R10, R15-R22, R40-R42, E1, E3, E4, EC2, INT-001, INT-002
- Level: contract
- Command IDs: C2
- Fixture/setup: all six valid assemblies, establishment, normal sync, editorial and strategic revisions, pre-resolved authority, marker-dependent late skip, and late strategic discovery
- Steps: resolve operation, independently classify strategic and README contexts, record loaded resources, and attempt writes before and after reclassification
- Expected result: each valid combination selects exactly one assembly; establishment uses VA2; primary and secondary profiles remain distinct; late evidence loads required procedure before dependent work
- Failure proves: supported paths are omitted, under-loaded, or measured dishonestly
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-004. README authority, markers, and identity-bound transitions

- Covers: R18-R27, E2, E3, E7, EC1-EC3, BND-AUTH-001, BND-TEMPORAL-001, INT-002, INT-003
- Level: contract
- Command IDs: C2
- Fixture/setup: establishment insertion, default revision/sync, exact pre-resolved skip, late skip, malformed marker families, silence, historical authority, and canonical/README identities inside and outside planned transitions
- Steps: bind authority and manifest, inspect or deliberately avoid marker parsing, mutate each relevant identity, and evaluate action and claims
- Expected result: only exact current authority permits insertion or skip; pre-resolved skip uses whole-file identity and uninspected marker state; any unplanned identity, action, manifest, marker, or authority change blocks
- Failure proves: marker state or stale approval can manufacture write or skip authority
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-005. Independent positioning and README actions

- Covers: R28-R33, E5, EC5, BND-STATE-001, BND-AUTH-001
- Level: contract
- Command IDs: C2
- Fixture/setup: establishment, editorial revision, substantive nonmaterial revision, changed assumption, authorized and unresolved conflict, material repositioning, absent rationale, unrelated rationale, and every known or unknown action
- Steps: classify public significance and both secondary actions independently, then validate permitted target effects
- Expected result: each condition has one exact action; establishment creates rationale; unaffected revisions preserve it; authorized changes update; unresolved choices and unrelated files block; unknown actions fail first
- Failure proves: public significance incorrectly determines secondary writes or unsafe rationale adoption occurs
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests.test_secondary_action_unknown_value`
- Required by milestone: M2

### T-VIS-006. Structural assets and historical preservation

- Covers: R34-R39, E8, EC4, EC5, BND-COMPOSE-001, BND-COMPAT-001, INT-004
- Level: contract
- Command IDs: C1, C2
- Fixture/setup: establishment, narrow historical edit, authorized full canonical rewrite, positioning create/full rewrite, skip assemblies, missing headings, placeholders, and policy-leak phrases
- Steps: select assets independently from references, compose creation and rewrite outputs, and inspect historical narrow edits
- Expected result: assets own only exact structure; applicable creation/full rewrites use them; narrow edits preserve existing structure; no placeholder or policy remains
- Failure proves: structural composition changes authority or forces migration of historical artifacts
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-007. Operation-manifest preparation and zero-write skip

- Covers: R43-R47, E2, E5, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001
- Level: contract
- Command IDs: C2
- Fixture/setup: every operation and applicable target set, absent/prior identities, intended identities, evidence states, zero-write sync skip, missing fields, and stale pre-write baselines
- Steps: prepare manifests, validate every target field and precondition, reread targets, and record attempted mutations
- Expected result: no target write or final skip occurs before one complete exact manifest; skipped README and unchanged canonical remain explicit equal-identity targets; incomplete or stale manifests block with zero writes
- Failure proves: a write or skip can occur without recoverable identity and authority evidence
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-008. Source-first commit and complete read-back

- Covers: R48-R50, E5, BND-STATE-001, BND-TEMPORAL-001, BND-ENV-001, INT-003
- Level: integration
- Command IDs: C2
- Fixture/setup: deterministic write ledger for canonical vision, rationale, and README with identity changes before each boundary and read-back mismatches
- Steps: execute the manifest protocol, mutate dependencies between writes, and validate final targets
- Expected result: canonical writes before rationale and README; README receives an immediate basis recheck; completion occurs only after every required, unchanged, or skipped target reads back exactly
- Failure proves: derived content can lead its source or completion can mask stale targets
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-009. Result vocabulary, zero-write truth, and partial reporting

- Covers: R51-R53, E2, E6, EC6, BND-INPUT-001, BND-RECOVERY-001, INT-002, INT-003
- Level: contract
- Command IDs: C2
- Fixture/setup: complete write, complete zero-write skip, blocked preflight, interruptions after each write, and unknown result value
- Steps: validate result vocabulary before consistency, inspect changed files and claims, and compare committed/pending target reports
- Expected result: only three results are accepted; zero-write skip reports unchanged/skipped without marker or sync claims; blocked preflight writes nothing; partial results name exact identities and never claim completion
- Failure proves: result claims overstate synchronization or hide partial state
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests.test_operation_result_unknown_value`
- Required by milestone: M2

### T-VIS-010. Governed prepared evidence, retry, and concurrency

- Covers: R54-R56, E6, EC3, EC6, BND-TEMPORAL-001, BND-RECOVERY-001, INT-003
- Level: integration
- Command IDs: C2, C8
- Fixture/setup: change-local Markdown authoring evidence with complete prepared manifest, interruptions before and after each write, identical retry, changed target, changed authority, unrelated file, and concurrent mutation
- Steps: verify evidence precedes writes, reconcile completed and pending targets, retry, and introduce each identity conflict
- Expected result: identical retry writes only matching pending targets once; completed targets remain exact; stale, unrelated, ambiguous, or concurrent state blocks without adoption, overwrite, or rollback
- Failure proves: governed recovery silently rebinds or duplicates multi-file work
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-011. Portable lost-manifest recovery boundary

- Covers: R57, E10, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001
- Level: contract
- Command IDs: C2
- Fixture/setup: interrupted portable multi-target state with available identical manifest, unavailable manifest, ambiguous partial files, and explicit owner-directed recovery request
- Steps: attempt same-invocation retry and later cross-session recovery
- Expected result: available exact context may reconcile; unavailable or ambiguous context stops and routes to owner direction without adoption; no persistent recovery mechanism is invented
- Failure proves: portable recovery exceeds the approved persistence and authority boundary
- Evidence artifact: `evidence/m2-package-implementation.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M2

### T-VIS-012. Semantic and literal preservation ledgers

- Covers: R58-R60, EC7, BND-COMPAT-001, INT-004
- Level: contract
- Command IDs: C0, C2
- Fixture/setup: complete and incomplete rule/literal ledgers, duplicate ownership, exact marker/path/verb consumers, incidental prose, and unknown disposition, classification, or vocabulary values
- Steps: validate one disposition and owner per item, separation of semantic and literal evidence, consumer updates, and unknown-value-first behavior
- Expected result: every current rule and consumed literal has one closed treatment; semantic meaning is not inferred from literal movement; every unknown value produces an explicit vocabulary error
- Failure proves: refactoring can hide behavior loss or compatibility drift
- Evidence artifact: `evidence/m1-preservation-inventories.md`, `evidence/semantic-preservation-review.md`
- Automation location: `VisionSkillProgressiveDisclosureLedgerTests`, `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M1 and M3

### T-VIS-013. Deterministic six-assembly measurement

- Covers: R61-R63, BND-COMPOSE-001, BND-COMPAT-001, INT-004
- Level: contract
- Command IDs: C0, C2
- Fixture/setup: flat baseline, canonical final resources, LF/CRLF variants, Unicode whitespace, duplicate resource references, six assembly formulas, both assets, and total package
- Steps: normalize and count each resource and assembly, deduplicate loaded procedural resources, compare to 2,268 words and 15,845 bytes, and report assets and package totals separately
- Expected result: all six procedural assemblies shrink under both metrics while resource, asset, representative composition, and total-package growth remain visible
- Failure proves: simplification is cosmetic, nondeterministic, or hides relocated prose
- Evidence artifact: `evidence/profile-size-baseline.md`, `evidence/simplification-measurements.md`
- Automation location: `VisionSkillProgressiveDisclosureLedgerTests`, `VisionSkillProgressiveDisclosureTests`
- Required by milestone: M1 and M3

### T-VIS-014. Canonical-through-installed resource parity

- Covers: R64, E9, EC8, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001, INT-004
- Level: smoke
- Command IDs: C1, C3, C4, C5, C6
- Fixture/setup: canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode trees with missing, extra, stale, transformed, escaped, and mixed-version resource variants
- Steps: build temporary projections and compare inventories, relative paths, and raw bytes
- Expected result: every required reference and asset is present and byte-identical; every invalid variant fails; no package is published
- Failure proves: canonical ownership is not preserved through supported distribution paths
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing build and adapter suites
- Required by milestone: M3

### T-VIS-015. Acceptance exclusions and architecture escalation

- Covers: R65-R66, BND-RECOVERY-001, BND-ENV-001
- Level: contract
- Command IDs: C2, C7
- Fixture/setup: deterministic repository proof, forbidden runtime/transcript/manual-gate dependencies, existing Markdown evidence, and hypothetical new schema, lifecycle state, persistence surface, or authority owner
- Steps: inspect acceptance dependencies and classify architecture applicability for each evidence model
- Expected result: acceptance remains static and repository-owned; forbidden mechanisms are absent; existing Markdown evidence preserves no-architecture status; any new persistent contract requires architecture before planning
- Failure proves: the simplification introduces hidden runtime acceptance or architecture
- Evidence artifact: `architecture-assessment.md`, `evidence/m3-package-proof.md`
- Automation location: `VisionSkillProgressiveDisclosureTests`, boundary validator
- Required by milestone: M2 and M3

## Fixtures and data

- Closed fixtures for operations, significance, resource contexts, loaded assemblies, positioning actions, README actions, asset contexts, marker evidence, manifest states, and operation results, including unknown values.
- README fixtures for valid, missing, malformed, nested, duplicate, ambiguous, changed, and pre-resolved-skip marker states.
- Identity-bound manifest fixtures for establishment, editorial revision, substantive revision, full rewrite, explicit sync, zero-write skip, interruption, exact retry, changed authority, concurrency, and lost portable context.
- Historical canonical vision and positioning fixtures that prove narrow edits preserve structure while creation and authorized full rewrites use the assets.
- Temporary generated, archived, release-candidate, and installed skill trees for all supported adapters.

## Mocking/stubbing policy

Model filesystem identities, target writes, interruptions, and read-backs with deterministic temporary files and side-effect ledgers. Do not edit the repository's actual `VISION.md`, `docs/vision/strategic-positioning.md`, or README vision block. Do not execute a target-agent runtime or contact external systems.

## Migration or compatibility tests

T-VIS-006 proves prospective structural adoption and historical narrow-edit preservation. T-VIS-012 proves separate semantic and literal dispositions. T-VIS-013 proves honest profile and package measurement. T-VIS-014 proves atomic inventory and byte parity across generated and installed projections. The retired lowercase `vision.md` path is not restored.

## Observability verification

T-VIS-007 through T-VIS-010 assert manifest identity, target actions, prior and intended identities, committed and pending targets, marker-evidence state, changed files, blockers, and claim limitations. Measurement and package evidence record exact resource identities and commands.

## Security/privacy verification

T-VIS-001 and T-VIS-007 prove escaped resources and unsafe target paths stop. T-VIS-004 proves authority cannot be inferred from silence, marker damage, or history. T-VIS-010 proves unrelated and concurrent content is not adopted or overwritten. Existing privacy and research rules remain universal and fixture content contains no credentials or personal data.

## Performance checks

T-VIS-013 measures normalized loaded words and UTF-8 bytes for all six assemblies and reports each resource, both assets, representative compositions, and total package separately. No runtime latency benchmark or tokenizer dependency is required.

## Manual QA checklist

Not applicable. Every acceptance claim is deterministic and automated; ordinary reviewer inspection during test-spec review, code review, and PR review is not a separate manual-proof contract.

## What not to test and why

- Do not edit the project's live vision, strategic positioning, or README front-matter; this change refactors the published skill package, not project strategy.
- Do not execute Codex, Claude Code, opencode, or another target-agent runtime, grade transcripts, or add a separate manual semantic-review gate; R65 requires repository-owned deterministic proof.
- Do not add a helper synchronizer, parser engine, persistence layer, or new lifecycle owner; those are excluded and would require architecture work.
- Do not migrate historical vision artifacts solely to adopt the new skeletons; compatibility is prospective.

## Uncovered gaps

None. Every normative requirement, applicable boundary, selected interaction, example, and named edge case has direct deterministic proof.

## Next artifacts

- Independent `test-spec-review`.
- Implementation milestones M1 through M3 after approval and settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. This artifact does not claim peer-review approval, implementation readiness, validation success, verification, branch readiness, PR readiness, release, or publication.
