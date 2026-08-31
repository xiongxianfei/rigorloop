# Retire the Standalone Test-Spec Stage Test Specification

## Owning change record

`docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`

## Related spec and plan

- Spec: `specs/retire-standalone-test-spec-stage.md`
- Plan: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`
- Architecture: `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md`
- ADR: `docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Specification | `specs/retire-standalone-test-spec-stage.md` | `sha256:e05c78bc2ce875d18d173fe3ae63caf72e37372663a335019c4794198aad7db4` | `design-review-r2` at `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/design-review-r2.md` |
| Architecture | `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md` | `sha256:98023a64b3248bd4095a25242dd830b7f71bff280f050127a1390f623175129c` | `design-review-r2` at `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/design-review-r2.md` |
| ADR | `docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md` | `sha256:fb9409e89524101cc54cb0af1ab9d7a22b6472a7a2cabe556ac9aaf3a91e795e` | `design-review-r2` at `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/design-review-r2.md` |
| Plan | `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md` | `sha256:727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938` | Delivery Review pending |

## Testing strategy

Use contract and integration tests for lifecycle classification, package composition, routing, mutation, retry, and recovery. Use repository-owned validator fixtures for schemas, closed vocabularies, historical compatibility, documentation, and review evidence. Use skill and adapter distribution tests for authority wording, required plan structure, progressive-disclosure resource mapping, active entrypoint retirement, generated archive parity, and clean-install resolution. Use one public-path end-to-end fixture for a new v2 change and one manifest-bound compatibility fixture for a prior-contract change.

Tests are written before or with each milestone. Every changed closed vocabulary receives a named `unknown_value` or `not_in_vocabulary` regression whose assertion checks the vocabulary diagnostic before any consistency diagnostic. Structural checks do not claim semantic adequacy; Delivery Review, Code Review, and Verify retain that judgment.

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: RTS-R1, RTS-R2, RTS-R3, RTS-R4, RTS-R5, RTS-R6, RTS-R7, RTS-R8, RTS-R9, RTS-R10, RTS-R11, RTS-R12, RTS-R13, RTS-R14, RTS-R15, RTS-R16, RTS-R17, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23, RTS-R24, RTS-R25

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | RTS-R3, RTS-R4, RTS-R6, RTS-R7, RTS-R8, RTS-R9, RTS-R10, RTS-R11, RTS-R13, RTS-R14, RTS-R15, RTS-R18 | BND-INPUT-001 | TS-007, TS-008, TS-010 | contract | automated | CMD-07, CMD-08, CMD-14 | `evidence/m3-verification-ownership.md` | M3 | - | - |
| PRF-002 | covered | RTS-R1, RTS-R2, RTS-R13, RTS-R18, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-STATE-001 | TS-001, TS-003, TS-005, TS-006 | integration | automated | CMD-01, CMD-02, CMD-03, CMD-04 | `evidence/m1-contract-classification.md`, `evidence/m2-dual-lifecycle.md` | M2 | - | - |
| PRF-003 | covered | RTS-R3, RTS-R4, RTS-R5, RTS-R6, RTS-R13, RTS-R14, RTS-R15, RTS-R16, RTS-R18, RTS-R21, RTS-R24, RTS-R25 | BND-AUTH-001 | TS-007, TS-010, TS-011 | contract | automated | CMD-06, CMD-07, CMD-14, CMD-15, CMD-16 | `evidence/m3-verification-ownership.md`, final review and Verify evidence | M3, M6 | - | - |
| PRF-004 | covered | RTS-R2, RTS-R11, RTS-R12, RTS-R13, RTS-R15, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | BND-COMPOSE-001 | TS-004, TS-009, TS-012, TS-013 | integration | automated | CMD-07, CMD-08, CMD-09, CMD-10, CMD-14 | `evidence/m4-preactivation-parity.md` | M4 | - | - |
| PRF-005 | covered | RTS-R3, RTS-R6, RTS-R8, RTS-R9, RTS-R10, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-TEMPORAL-001 | TS-003, TS-005, TS-006, TS-014 | integration | automated | CMD-01, CMD-02, CMD-05 | `evidence/m2-dual-lifecycle.md`, `evidence/m5-v2-activation.md` | M5 | - | - |
| PRF-006 | covered | RTS-R3, RTS-R9, RTS-R14, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-RECOVERY-001 | TS-002, TS-004, TS-006, TS-014 | integration | automated | CMD-02, CMD-03, CMD-04, CMD-09 | `evidence/m5-v2-activation.md` | M5 | - | - |
| PRF-007 | covered | RTS-R1, RTS-R17, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-COMPAT-001 | TS-001, TS-004, TS-005, TS-006, TS-014 | integration | automated | CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-11, CMD-12 | `evidence/m5-v2-activation.md` | M5 | - | - |
| PRF-008 | covered | RTS-R12, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | BND-ENV-001 | TS-009, TS-013 | end-to-end | automated | CMD-07, CMD-08, CMD-09, CMD-13, CMD-14 | `evidence/m4-preactivation-parity.md`, `evidence/m5-v2-activation.md` | M5 | - | - |
| PRF-009 | covered | RTS-R1, RTS-R18, RTS-R20, RTS-R22 | INT-001 | TS-004, TS-005 | integration | automated | CMD-01, CMD-02, CMD-03, CMD-04 | `evidence/m2-dual-lifecycle.md` | M2 | - | - |
| PRF-010 | covered | RTS-R13, RTS-R15, RTS-R18 | INT-002 | TS-010 | contract | automated | CMD-05, CMD-06, CMD-07 | `evidence/m3-verification-ownership.md` | M3 | - | - |
| PRF-011 | covered | RTS-R6, RTS-R8, RTS-R9, RTS-R10 | INT-003 | TS-008 | contract | automated | CMD-07 | `evidence/m3-verification-ownership.md` | M3 | - | - |
| PRF-012 | covered | RTS-R18, RTS-R19, RTS-R23 | INT-004 | TS-002, TS-012, TS-013, TS-014 | end-to-end | automated | CMD-03, CMD-04, CMD-07, CMD-08, CMD-09, CMD-10, CMD-13, CMD-14, CMD-15, CMD-16 | `evidence/m5-v2-activation.md`, final review and Verify evidence | M5, M6 | - | - |
| PRF-013 | covered | RTS-R20, RTS-R21, RTS-R22, RTS-R23 | INT-005 | TS-005, TS-006, TS-014 | integration | automated | CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-11, CMD-12 | `evidence/m5-v2-activation.md` | M5 | - | - |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| RTS-R1, RTS-R2 | TS-003, TS-004, TS-017 | integration, end-to-end | Proves the v2 route and absence of active test-spec surfaces or replacement stages. |
| RTS-R3-RTS-R5 | TS-007, TS-011 | contract | Proves behavior, architecture, and mechanics remain with their named owners. |
| RTS-R6-RTS-R10 | TS-008, TS-017 | contract, end-to-end | Proves engineering-led milestones, local verification, and separate integrated proof. |
| RTS-R11 | TS-008, TS-017 | contract, end-to-end | Traverses SR, milestone, TG, concrete proof, and evidence without one-to-one identities. |
| RTS-R12 | TS-009, TS-013 | contract, end-to-end | Proves proportional plan-owned methods in canonical and installed packages. |
| RTS-R13-RTS-R15 | TS-010 | contract, integration | Proves exact package authority, joint judgment, rejection, and correction ownership. |
| RTS-R16 | TS-011, TS-017 | contract, end-to-end | Preserves implementation, Code Review, and Verify responsibilities. |
| RTS-R17 | TS-009, TS-013 | contract, end-to-end | Removes active standalone entrypoints and relocates retained methods. |
| RTS-R18 | TS-004, TS-012, TS-013, TS-017 | integration, end-to-end | Proves coherent runtime, guidance, validation, templates, and adapter packages. |
| RTS-R19 | TS-002 | unit, integration | Direct unknown-value proof for every changed closed vocabulary. |
| RTS-R20 | TS-005, TS-018 | integration, end-to-end | Historical records remain readable and byte-unchanged from a fresh checkout. |
| RTS-R21 | TS-005, TS-006 | integration | Prior contracts continue; first implementation provides no implicit or optional migration operation. |
| RTS-R22 | TS-002, TS-004, TS-005 | integration | Legacy context cannot authorize active old or wholly unknown values. |
| RTS-R23 | TS-012-TS-014 | integration, end-to-end | Activation and recovery operate on complete compatible packages. |
| RTS-R24 | TS-011 | contract | Unaffected stage ownership and spec/plan separation remain explicit. |
| RTS-R25 | TS-007, TS-008, TS-010, TS-012 | contract | Deterministic checks remain structural and semantic decisions remain review-owned. |

## Acceptance criterion coverage map

| Acceptance criterion ID | Covered by | Direct outcome |
| --- | --- | --- |
| RTS-AC1 | TS-003, TS-017 | New v2 work reaches one plan-centered Delivery Review without test-spec. |
| RTS-AC2 | TS-007 | Specification guidance makes material behavior and scenarios testable without mechanics. |
| RTS-AC3 | TS-008 | Plan structure preserves engineering-led sequencing and complete verification allocation. |
| RTS-AC4 | TS-010 | Delivery Review makes one joint readiness decision and routes deficiencies correctly. |
| RTS-AC5 | TS-008, TS-017 | TG identities provide lightweight end-to-end traceability without new lifecycle identity. |
| RTS-AC6 | TS-009 | Specialist methods are plan-owned, conditional, and portable. |
| RTS-AC7 | TS-002, TS-004 | Active test-spec and unknown values fail closed with direct regressions. |
| RTS-AC8 | TS-005, TS-018 | Completed historical records remain readable and unchanged without active authority. |
| RTS-AC9 | TS-006 | Prior-contract continuation is preserved and ambiguous conversion is rejected. |
| RTS-AC10 | TS-012, TS-013, TS-017 | Canonical, executable, documented, validated, and generated surfaces remain coherent. |
| RTS-AC11 | TS-014 | Recovery restores one complete prior package only before first v2 use. |
| RTS-AC12 | TS-011, TS-017 | Unaffected lifecycle and downstream authority remain unchanged. |
| RTS-AC13 | TS-011 | The exact approved Design Review package remains the coherent upstream authority for every allocated requirement. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | TS-007 | SR behavior is testable without implementation mechanics. |
| E2 | TS-008 | One milestone maps several SRs into one related TG objective. |
| E3 | TS-008, TS-017 | Change-level verification remains separate from local milestone proof. |
| E4 | TS-010 | Delivery Review issues one joint readiness decision and routes gaps to plan. |
| E5 | TS-004, TS-005 | Historical test-spec remains readable while active v2 use is rejected. |
| E6 / AGENTS-CLOSED-VOCABULARY | TS-002 | Unknown values fail before consistency checks with named regressions. |
| E7 | TS-005, TS-006 | Prior-contract continuation is explicit; migration is not inferred or implemented in this slice. |

## Edge case coverage

| Edge case | Covered by | Expected outcome |
| --- | --- | --- |
| EC1 | TS-008 | Many SRs may map to one TG when the trace is explicit. |
| EC2 | TS-008, TS-017 | One SR may span milestones, with local checks and final integrated proof. |
| EC3 | TS-008 | Packaging or documentation work may cite a justified non-SR obligation. |
| EC4 | TS-008, TS-014 | A safe intermediate state is locally proved and final workflow correctness remains change-level. |
| EC5 | TS-009 | Manual or operational evidence is permitted without creating a separate artifact contract. |
| EC6 | TS-004, TS-005 | Historical `test-spec-review` is readable only in exact prior context. |
| EC7 | TS-004, TS-010 | A test-spec attachment is rejected from a v2 Delivery Review package. |
| EC8 | TS-007, TS-008 | A plan may name commands while specification guidance excludes mechanics. |
| EC9 | TS-013 | Omitted specialist resources fail generated-package parity. |
| EC10 | TS-018 | Historical reading needs no network, migration, or regeneration. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD-01 | `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-transaction.test.js` | existing/configured | implement | M1, M2, M5 | M1 | Any nonzero exit blocks the milestone. | A zero-test result blocks because named files must execute tests. | milestone evidence | Local repository fixtures only; no network. |
| CMD-02 | `npm test --prefix packages/rigorloop` | existing/configured | implement | M2, M5, M6 | M2 | Any nonzero exit blocks the milestone. | A zero-test result blocks. | milestone evidence | Local package tests; no publication. |
| CMD-03 | `python scripts/test-change-metadata-validator.py` | existing/configured | implement | M1, M4, M5 | M1 | Any failure blocks contract classification or activation. | A zero-test result blocks. | milestone evidence | Temporary fixtures only. |
| CMD-04 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | implement | M1, M4, M5 | M1 | Any failure blocks lifecycle or compatibility claims. | A zero-test result blocks. | milestone evidence | Temporary fixtures only. |
| CMD-05 | `python scripts/test-workflow-automation.py && python scripts/test-workflow-automation-policy.py && python scripts/test-workflow-automation-state.py` | existing/configured | implement | M2, M5 | M2 | The first nonzero command stops the group and blocks routing claims. | A zero-test result in any script blocks. | milestone evidence | Local fixtures; no external workflow mutation. |
| CMD-06 | `python scripts/test-review-artifact-validator.py` | existing/configured | implement | M2, M4, M5 | M2 | Any failure blocks package-review evidence claims. | A zero-test result blocks. | milestone evidence | Temporary review fixtures only. |
| CMD-07 | `python scripts/test-skill-validator.py` | existing/configured | implement | M3, M4, M5 | M3 | Any failure blocks skill authority or inventory claims. | A zero-test result blocks. | milestone evidence | Reads canonical skills and temporary fixtures only. |
| CMD-08 | `python scripts/test-build-skills.py && python scripts/build-skills.py --check` | existing/configured | implement | M3, M4, M5 | M3 | Any failure blocks resource-map or generated-skill parity claims. | A zero-test result in the test script blocks. | milestone evidence | Check and temporary build behavior only; tracked generated bodies are not edited. |
| CMD-09 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M4, M5 | M4 | Any failure blocks supported-adapter publication. | A zero-test result blocks. | milestone evidence | Generates only in test-owned temporary directories. |
| CMD-10 | `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` | existing/configured | implement | M4, M5 | M4 | Any error blocks publication; warnings are recorded and assessed. | Not applicable; deterministic path audit. | milestone evidence | Read-only audit. |
| CMD-11 | `python scripts/test-lifecycle-cli-conformance.py` | existing/configured | implement | M5 | M5 | Any failure blocks activation. | A zero-test result blocks. | `evidence/m5-v2-activation.md` | Temporary lifecycle fixtures only. |
| CMD-12 | `python scripts/test-governed-lifecycle-cli-validator.py` | existing/configured | implement | M5 | M5 | Any failure blocks activation. | A zero-test result blocks. | `evidence/m5-v2-activation.md` | Temporary lifecycle fixtures only. |
| CMD-13 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | verify | M5, M6 | M5 | Any nonzero exit blocks activation or final readiness. | A zero-check or silently skipped required suite blocks. | activation and Verify evidence | Repository broad smoke; no release publication. |
| CMD-14 | `python scripts/validate-skills.py skills/spec/SKILL.md skills/plan/SKILL.md skills/delivery-review/SKILL.md skills/workflow/SKILL.md` | existing/configured | implement | M3 | M3 | Any validation error blocks M3. | Not applicable; deterministic explicit-path validation must return a result for every named skill. | `evidence/m3-verification-ownership.md` | Read-only validation of canonical authored skills. |
| CMD-15 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-31-retire-standalone-test-spec-stage` | existing/configured | verify | M6 | M6 | Any finding, log, resolution, or closeout inconsistency blocks final readiness. | Not applicable; deterministic change-root validation. | final review and Verify evidence | Read-only closeout audit. |
| CMD-16 | `python scripts/validate-change-metadata.py docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml` | existing/configured | verify | M6 | M6 | Any lifecycle, artifact, review, milestone, or routing inconsistency blocks final readiness. | Not applicable; deterministic one-record validation. | final review and Verify evidence | Read-only metadata validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | TS-001, TS-002, TS-015 | none | CMD-01, CMD-03, CMD-04 | `evidence/m1-contract-classification.md` | M1 Code Review | New-change remains v1. |
| M2 | TS-003, TS-004, TS-005, TS-006, TS-010, TS-015 | none | CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-06 | `evidence/m2-dual-lifecycle.md` | M2 Code Review | V2 behavior remains inactive by default. |
| M3 | TS-007 through TS-011 and TS-016 | none | CMD-07, CMD-08, CMD-14 | `evidence/m3-verification-ownership.md` | M3 Code Review | Semantic sufficiency also requires independent review. |
| M4 | TS-002, TS-009, TS-012, TS-013, TS-016 | none | CMD-03, CMD-04, CMD-06, CMD-07, CMD-08, CMD-09, CMD-10 | `evidence/m4-preactivation-parity.md` | M4 Code Review | Temporary generation only. |
| M5 | TS-001 through TS-006 and TS-009 through TS-018 | none | CMD-01 through CMD-13 | `evidence/m5-v2-activation.md` | M5 Code Review | Activation is one complete reviewed slice. |
| M6 | TS-017, TS-018, and all applicable regressions | none | CMD-02 through CMD-16 | final review, explanation, and Verify evidence | PR handoff | Complete-change proof; no implementation occurs in M6. |

## Test cases

### TS-001. Contract manifest classification

- Covers: RTS-R20-RTS-R23, BND-STATE-001, BND-COMPOSE-001, BND-COMPAT-001, E7.
- Level: integration
- Command IDs: CMD-01, CMD-03, CMD-04
- Fixture/setup: Explicit v2, explicit v1, unversioned, missing-entry, duplicate, reordered, and class-mismatch change records plus a deterministic activation manifest.
- Steps: Exercise runtime and Python classification against the same fixtures and repeat after changing non-authoritative dates, stage names, artifact presence, Git availability, and network availability.
- Expected result: Only v2 or exact manifest-matched prior classes are admitted; manifest ordering is raw-UTF-8 deterministic; heuristic facts never change classification.
- Failure proves: Contract selection is permissive, nondeterministic, or inconsistent across owners.
- Evidence artifact: `evidence/m1-contract-classification.md`
- Automation location: lifecycle contract/read tests and lifecycle validator fixtures.
- Required by milestone: M1.

### TS-002. Unknown and removed vocabularies fail closed

- Covers: RTS-R19, RTS-R22, RTS-AC7, BND-RECOVERY-001, BND-COMPAT-001, E6, AGENTS-CLOSED-VOCABULARY.
- Level: unit and integration
- Command IDs: CMD-01, CMD-03, CMD-04, CMD-06, CMD-07
- Fixture/setup: One unknown value for every changed contract, stage, artifact kind, review kind, settlement, package-role, manifest-class, resource-map, and adapter-inventory closed set; known removed test-spec values in active and historical contexts.
- Steps: Submit each value through its public validator or lifecycle path and record diagnostic order.
- Expected result: Each wholly unknown or active removed value produces an explicit vocabulary error before consistency errors; known legacy values pass only in exact historical context.
- Failure proves: A membership guard or fall-through admits or obscures an unknown value.
- Evidence artifact: milestone evidence naming every changed vocabulary and regression test.
- Automation location: Node lifecycle tests and Python validator/skill fixtures with `unknown_value` or `not_in_vocabulary` in test names.
- Required by milestone: M1-M5 as vocabularies change.

### TS-003. V2 stage graph and package authority

- Covers: RTS-R1, RTS-R2, RTS-R13, RTS-AC1, BND-STATE-001, BND-TEMPORAL-001.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-05, CMD-06
- Fixture/setup: An explicit valid v2 change with approved Design Review and registered primary plan.
- Steps: Request permitted and retired transitions, inspect context, compose Delivery Review, settle it, and let Workflow advance.
- Expected result: Only `design-review -> plan -> delivery-review -> implement` is admitted; package membership is the exact plan plus approved Design authority; settlement is isolated from advancement.
- Failure proves: V2 still depends on test-spec, permits a bypass, or conflates review with routing.
- Evidence artifact: `evidence/m2-dual-lifecycle.md`
- Automation location: lifecycle stage/package/read and workflow automation tests.
- Required by milestone: M2.

### TS-004. Active test-spec and mixed-package rejection

- Covers: RTS-R1, RTS-R17-RTS-R19, RTS-R22, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, INT-001, EC6, EC7.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-06, CMD-07
- Fixture/setup: V2 records containing a test-spec artifact, stage, review, settlement, or package member; packages mixing old routing and new skills.
- Steps: Validate, read, settle, and route each fixture through public paths.
- Expected result: Every active legacy or mixed surface blocks with the exact offending identity; no partial authority or repair is created.
- Failure proves: Compatibility or composition permits a retired active surface.
- Evidence artifact: `evidence/m2-dual-lifecycle.md`, `evidence/m4-preactivation-parity.md`
- Automation location: lifecycle, review, metadata, workflow, and skill fixtures.
- Required by milestone: M2 and M4.

### TS-005. Manifest-bound historical and post-gate v1 continuation

- Covers: RTS-R20-RTS-R22, BND-STATE-001, BND-TEMPORAL-001, BND-COMPAT-001, INT-001, INT-005, E5, E7, EC6, EC10.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-11, CMD-12
- Fixture/setup: A completed historical v1 record and a nonterminal v1 record with settled legacy Delivery Review at implementation or later, both exactly listed in the manifest.
- Steps: Read the historical record, resume the nonterminal record through common downstream stages, and compare artifact bytes before and after.
- Expected result: Historical evidence remains unchanged and readable; post-gate v1 continuation succeeds without active legacy authoring entrypoints; neither record grants legacy authority to v2.
- Failure proves: Activation invalidates history, strands downstream v1 work, rewrites records, or leaks authority.
- Evidence artifact: `evidence/m5-v2-activation.md`
- Automation location: lifecycle compatibility and public CLI conformance fixtures.
- Required by milestone: M5.

### TS-006. Preactivation blocker and omitted migration

- Covers: RTS-R21-RTS-R23, RTS-AC9, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, INT-005.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-11, CMD-12
- Fixture/setup: Manifest-listed prior records before Delivery Review, with stale identities, ambiguous state, and after Delivery Review.
- Steps: Run the activation prerequisite and inspect public operations for a migration command added by this change.
- Expected result: Every pre-gate record blocks activation by exact change ID; post-gate records do not; no implicit or newly implemented v1-to-v2 migration exists in the first slice.
- Failure proves: Activation can strand work or silently convert its authority.
- Evidence artifact: `evidence/m5-v2-activation.md`
- Automation location: workflow policy, lifecycle conformance, and activation fixtures.
- Required by milestone: M5.

### TS-007. Specification and architecture ownership

- Covers: RTS-R3-RTS-R5, RTS-R24, RTS-R25, RTS-AC2, E1, EC8.
- Level: contract
- Command IDs: CMD-07, CMD-08, CMD-14
- Fixture/setup: Canonical spec and architecture skills/assets plus positive and negative skill fixtures.
- Steps: Validate required observable behavior prompts, verification-relevant architecture boundaries, forbidden test mechanics in specification ownership, and semantic-review claim limits.
- Expected result: Specification asks what must be demonstrably true; architecture identifies realization; neither allocates implementation test mechanics or delivery work.
- Failure proves: Ownership is incomplete or merged.
- Evidence artifact: `evidence/m3-verification-ownership.md`
- Automation location: skill validator and build-skill fixtures.
- Required by milestone: M3.

### TS-008. Engineering-led plan structure and traceability

- Covers: RTS-R6-RTS-R11, RTS-R25, RTS-AC3, RTS-AC5, INT-003, E2, E3, EC1-EC4, EC8.
- Level: contract
- Command IDs: CMD-07, CMD-08, CMD-14
- Fixture/setup: Plan skeleton and milestone fixtures for many-to-many SRs, one SR across milestones, non-SR packaging work, safe intermediate states, and integrated behavior.
- Steps: Validate required milestone fields, TG identity rules, change-level triggers, evidence expectations, and forbidden implications from milestone completion.
- Expected result: Engineering dependencies determine sequence; verification attaches to milestones; TGs trace without one-to-one requirements; integrated proof is explicit.
- Failure proves: Plan is incomplete, test-driven in the wrong sense, or treats local completion as full correctness.
- Evidence artifact: `evidence/m3-verification-ownership.md`
- Automation location: skill and asset validator fixtures.
- Required by milestone: M3.

### TS-009. Conditional specialist verification methods

- Covers: RTS-R12, RTS-R17, RTS-AC6, BND-COMPOSE-001, BND-ENV-001, EC5, EC9.
- Level: contract and end-to-end
- Command IDs: CMD-07, CMD-08, CMD-09, CMD-14
- Fixture/setup: Ordinary and risk-triggered plan invocations plus generated clean installs for each supported adapter.
- Steps: Resolve inline guidance and each specialist family, inspect load conditions, remove one mapped resource, and repeat from a clean installed skill root.
- Expected result: Ordinary planning does not load all methods; each approved risk family resolves conditionally; missing or escaped resources block; no standalone replacement skill exists.
- Failure proves: Expertise is lost, always loaded, nonportable, or repackaged as a mandatory stage.
- Evidence artifact: `evidence/m3-verification-ownership.md`, `evidence/m4-preactivation-parity.md`
- Automation location: skill, build, and adapter distribution tests.
- Required by milestone: M3 and M4.

### TS-010. Joint Delivery Review readiness decision

- Covers: RTS-R13-RTS-R15, RTS-R25, RTS-AC4, INT-002, E4, EC7.
- Level: contract and integration
- Command IDs: CMD-05, CMD-06, CMD-07, CMD-14
- Fixture/setup: Exact plan packages with sufficient coverage, missing SR allocation, missing local or change-level proof, unrealistic evidence, and a test-spec substitute.
- Steps: Run Delivery Review context, structural validation, independent semantic review fixtures, settlement, and correction routing.
- Expected result: One exact plan-centered decision assesses sequence and verification; material gaps withhold authority and route to plan or specification; reviewer does not author fixes or defer them to Verify.
- Failure proves: The gate is partial, non-independent, or accepts the retired artifact as compensation.
- Evidence artifact: `evidence/m3-verification-ownership.md`
- Automation location: lifecycle package, workflow, review validator, and skill fixtures.
- Required by milestone: M3.

### TS-011. Preserved implementation and downstream authority

- Covers: RTS-R16, RTS-R24, RTS-AC12, RTS-AC13, BND-AUTH-001.
- Level: contract
- Command IDs: CMD-06, CMD-07, CMD-14, CMD-15, CMD-16
- Fixture/setup: Skill contracts for proposal, architecture, specification, Design Review, plan, Delivery Review, implementation, Code Review, Verify, and PR.
- Steps: Validate write sets, claims, reciprocal handoffs, and absence of spec/plan merge or downstream substitution.
- Expected result: Only the approved test-spec removal and Delivery Review membership change; the exact coherent Design Review package remains upstream authority; implementation owns mechanics and evidence; downstream reviews retain their roles.
- Failure proves: The change expands or collapses unrelated authority.
- Evidence artifact: `evidence/m3-verification-ownership.md`
- Automation location: skill validator authority fixtures.
- Required by milestone: M3.

### TS-012. Normative surface coherence

- Covers: RTS-R18, RTS-R23-RTS-R25, BND-COMPOSE-001, BND-RECOVERY-001, INT-004.
- Level: integration
- Command IDs: CMD-03, CMD-04, CMD-06, CMD-07, CMD-08, CMD-09, CMD-10, CMD-14
- Fixture/setup: Inventory of current normative governance, workflow specs, docs, templates, examples, schemas, validators, and skill resources; settled historical documents excluded from mutation scope.
- Steps: Scan active surfaces, validate intended contract markers, inject one stale old route and one missing v2 owner, and audit documentation.
- Expected result: All active surfaces agree; mixed or missing owners block; historical records remain untouched; validators make only structural claims.
- Failure proves: Publication can expose contradictory workflow contracts.
- Evidence artifact: `evidence/m4-preactivation-parity.md`
- Automation location: lifecycle/review/skill validators and prose audit.
- Required by milestone: M4.

### TS-013. Supported adapter and clean-install parity

- Covers: RTS-R12, RTS-R17-RTS-R19, RTS-R23, BND-COMPOSE-001, BND-ENV-001, INT-004, EC9.
- Level: end-to-end
- Command IDs: CMD-07, CMD-08, CMD-09, CMD-13, CMD-14
- Fixture/setup: Temporary Codex, Claude Code, and opencode archives built from canonical skills; drifted, missing-resource, extra-entrypoint, and escaped-path variants.
- Steps: Build, validate inventories and checksums, install cleanly, resolve plan resources, and reject each variant.
- Expected result: Every supported package omits active standalone test-spec entrypoints, resolves specialist resources locally, and matches canonical routing.
- Failure proves: One supported adapter publishes an incomplete or mixed contract.
- Evidence artifact: `evidence/m4-preactivation-parity.md`, `evidence/m5-v2-activation.md`
- Automation location: skill build and adapter distribution tests.
- Required by milestone: M4 and M5.

### TS-014. Activation and recovery boundary

- Covers: RTS-R20-RTS-R23, RTS-AC11, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, INT-004, INT-005, EC4.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-09, CMD-11, CMD-12, CMD-13
- Fixture/setup: Complete preactivation package, partial package variants, interrupted activation, no-v2-record state, and first-v2-record state.
- Steps: Exercise activation validation, simulated interruption, whole-package pre-use rollback, and attempted silent rollback after a v2 record exists.
- Expected result: Partial activation never publishes; pre-use rollback restores one complete v1 package; post-use silent rollback blocks and requires forward correction; history is unchanged.
- Failure proves: Recovery can leave a mixed graph or invalidate registered v2 work.
- Evidence artifact: `evidence/m5-v2-activation.md`
- Automation location: lifecycle transaction, release/adapter, and broad-smoke fixtures.
- Required by milestone: M5.

### TS-015. Lifecycle and validation diagnostics

- Covers: observability contract, RTS-R18, RTS-R19, RTS-R21, RTS-R22.
- Level: contract
- Command IDs: CMD-01, CMD-03, CMD-04, CMD-05, CMD-06
- Fixture/setup: Valid, stale, removed-active, accepted-historical, wholly unknown, mixed-package, and activation-blocked records.
- Steps: Request status, context, validation, routing, and package review in human and JSON forms where supported.
- Expected result: Diagnostics name active stage, permitted operation, exact members and identities, stale evidence, compatibility class, unknown value, or blocking change ID without guessing.
- Failure proves: Operators cannot distinguish repairable history from invalid active state.
- Evidence artifact: M1, M2, and M5 evidence.
- Automation location: lifecycle read/output and repository validator tests.
- Required by milestone: M1, M2, M5.

### TS-016. Published usability, privacy, and bounded execution

- Covers: accessibility, security/privacy, and performance expectations; RTS-R12, RTS-R18, RTS-R24.
- Level: contract and smoke
- Command IDs: CMD-07, CMD-08, CMD-09, CMD-10, CMD-13, CMD-14
- Fixture/setup: Canonical and clean-installed skill text, ordinary plan invocation, and repository command execution logs.
- Steps: Check definition of TG, readable tables/text, absence of maintainer-only path assumptions in published guidance, conditional resource loading, no new credential/network/data store, and reported command timing regressions.
- Expected result: Text remains self-contained and accessible; ordinary context is smaller in lifecycle surface; no hosted service, background index, secret, or privacy surface is introduced.
- Failure proves: Retirement worsens usability, portability, or operational exposure.
- Evidence artifact: M3-M5 evidence.
- Automation location: skill/prose/build checks plus evidence inspection.
- Required by milestone: M3-M5.

### TS-017. New v2 workflow end to end

- Covers: RTS-R1-RTS-R19, RTS-R24, RTS-R25, RTS-AC1, RTS-AC2, RTS-AC3, RTS-AC4, RTS-AC5, RTS-AC6, RTS-AC7, RTS-AC10, RTS-AC12.
- Level: end-to-end
- Command IDs: CMD-01 through CMD-16
- Fixture/setup: Fresh governed change created after activation with several SRs, multiple engineering milestones, local TGs, one change-level TG, concrete checks, and evidence.
- Steps: Progress through Design Review, plan, Delivery Review, implementation milestones, Code Review, explanation, and Verify; traverse traceability in both directions.
- Expected result: No test-spec artifact or stage exists; one readiness decision covers sequence and verification; concrete proof and evidence satisfy approved TGs; downstream authority is unchanged.
- Failure proves: The complete replacement workflow loses rigor, traceability, or stage separation.
- Evidence artifact: `evidence/m5-v2-activation.md` and M6 closeout evidence.
- Automation location: public lifecycle and generated clean-install integration fixture.
- Required by milestone: M5 and M6.

### TS-018. Historical fresh-checkout read

- Covers: RTS-R20-RTS-R22, RTS-AC8, BND-COMPAT-001, EC10.
- Level: end-to-end
- Command IDs: CMD-02, CMD-03, CMD-04, CMD-09, CMD-11, CMD-12, CMD-13, CMD-15, CMD-16
- Fixture/setup: Clean checkout or temporary package containing the frozen manifest and a completed historical test-spec change, with network disabled and no regeneration step.
- Steps: Install or invoke supported tooling, read status and evidence, validate history, and compare tracked historical bytes.
- Expected result: The historical record is readable, valid, and unchanged without network, migration, synthesis, or active legacy authority.
- Failure proves: Compatibility depends on mutable external state or damages history.
- Evidence artifact: `evidence/m5-v2-activation.md` and M6 closeout evidence.
- Automation location: adapter clean-install and lifecycle compatibility fixture.
- Required by milestone: M5 and M6.

## Fixtures and data

- Contract fixtures: explicit v2, manifest-matched v1, manifest-matched legacy-unversioned, absent entry, duplicate entry, raw-UTF-8 disorder, class mismatch, unknown contract, and v2-with-active-test-spec.
- Lifecycle fixtures: new v2 path, post-Delivery-Review v1 continuation, pre-gate activation blocker, historical terminal record, stale revision, interrupted transaction, mixed package, and first-v2-record recovery boundary.
- Plan fixtures: many SRs to one TG, one SR across milestones, non-SR packaging work, safe intermediate state, missing local verification, missing change-level verification, and test-spec substitution.
- Package fixtures: canonical, missing specialist resource, escaped resource, extra retired entrypoint, old route with new skills, and new route with old package membership.
- Historical fixture bytes are treated as immutable test input; tests compare them before and after compatibility operations.

## Mocking/stubbing policy

Use temporary repositories, change roots, adapter output directories, and deterministic local filesystem fault injection already owned by repository tests. Stub Git or network availability only to prove those inputs cannot affect classification. Do not mock lifecycle package composition when the public CLI path can exercise it, and do not replace supported-adapter generation with string-only assertions.

## Migration or compatibility tests

The first implementation intentionally omits optional in-place migration. Compatibility proof therefore covers exact manifest-bound reading, post-gate v1 continuation, activation blocking for pre-gate v1 work, rejection of implicit conversion, historical byte preservation, and the pre-/post-first-v2 recovery boundary. A future explicit migration operation would require a new approved proof map.

## Observability verification

TS-015 verifies lifecycle status, context, validation, review-package, and activation diagnostics. Evidence must include representative structured output for accepted v2, accepted historical v1, removed active test-spec, wholly unknown value, stale identity, mixed package, and exact activation blocker. No hosted telemetry is required.

## Security/privacy verification

TS-011 and TS-016 verify authority boundaries and absence of new credentials, secrets, network dependencies, personal-data stores, or external actors. Compatibility fixtures must prove that historical classification cannot escalate authority or bypass validation. Adapter generation runs in temporary local output and must not publish or contact external services.

## Performance checks

No numeric threshold is imposed. M3 evidence records that ordinary plan invocation loads compact inline guidance without all specialist references or a test-spec skill. M4-M5 evidence records material timing or memory regressions in skill validation, adapter generation tests, lifecycle tests, and broad smoke; any unexplained material regression is a Delivery Review, Code Review, or Verify concern.

## Manual QA checklist

Not applicable. Every required behavioral, structural, compatibility, recovery, and package outcome has an automated or review-owned proof path. Human semantic judgment occurs in Delivery Review, Code Review, and Verify rather than as a separate manual test procedure.

## What not to test and why

- Do not test one-to-one SR, TG, test-function, or evidence identity because the specification explicitly permits many-to-many traceability.
- Do not test every Cartesian combination of boundary partitions; stop after every approved boundary and selected interaction has direct outcome proof.
- Do not test a v1-to-v2 migration operation because the approved first implementation omits it and activation blocks pre-gate prior work instead.
- Do not rewrite historical artifacts to prove compatibility; byte preservation is the required outcome.
- Do not add semantic validators for requirement or verification adequacy; formal reviews own those decisions.
- Do not publish adapter archives or mutate external systems while running this proof map.

## Uncovered gaps

None. The plan's initial reference to nonexistent `packages/rigorloop/test/new-change.test.js` was corrected to the existing `packages/rigorloop/test/cli.test.js` owner before this proof map was registered.

## Next artifacts

- Delivery Review of the exact plan and this legacy-path test specification under approved Design Review `design-review-r2`.

## Follow-on artifacts

None yet

## Readiness

Ready for independent Delivery Review. This legacy-path artifact exists only because the implementing change is registered under the prior lifecycle contract; it does not authorize implementation until the exact delivery package is approved and settled.
