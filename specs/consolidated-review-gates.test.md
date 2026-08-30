# Consolidated Review Gates Test Specification

## Owning change record

`docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`

## Related spec and plan

- Spec: `specs/consolidated-review-gates.md`
- Plan: `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md`
- Architecture/ADRs: `docs/adr/ADR-20260828-consolidated-review-package-topology.md`

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Specification | `specs/consolidated-review-gates.md` | `spec` | `spec-review-r5`; `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/spec-review-r5.md` |
| Execution plan | `docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md` | `plan` | `plan-review-r5`; `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/plan-review-r5.md` |
| Architecture decision | `docs/adr/ADR-20260828-consolidated-review-package-topology.md` | `adr-consolidated-review-package-topology` | `architecture-review-adr-r4`; `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/architecture-review-adr-r4.md` |

## Testing strategy

Use contract and integration fixtures for cutover admission, visible package membership, governed invalidation, review outcomes, finding ownership, atomic settlement, routing, historical-authority rejection, and rollback. Use repository validator suites for closed schemas and generated parity, skill-validator fixtures for public responsibility boundaries, and one broad smoke run only at the cutover milestone. Tests exercise public CLI and generated-package paths where those paths are the contract; helper-only proof does not substitute for an admitted public path.

Boundary model version: boundary-first-v1
Boundary model scope: CRG-R1, CRG-R2, CRG-R3, CRG-R4, CRG-R5, CRG-R6, CRG-R7, CRG-R8, CRG-R9, CRG-R10, CRG-R11, CRG-R12, CRG-R13, CRG-R14, CRG-R15, CRG-R16, CRG-R17, CRG-R18, CRG-R19, CRG-R20, CRG-R21, CRG-R22, CRG-R23, CRG-R24, CRG-R25, CRG-R26, CRG-R27, CRG-R28, CRG-R29, CRG-R30, CRG-R31, CRG-R32, CRG-R33, CRG-R34, CRG-R35, CRG-R36, CRG-R37, CRG-R38, CRG-R39, CRG-R40, CRG-R41, CRG-R42, CRG-R43, CRG-R44, CRG-R45

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| CRG-R1–CRG-R5 | CRG-T01, CRG-T11, CRG-T16 | contract, integration | One consolidated graph, retired old gates, and atomic cutover. |
| CRG-R6 | CRG-T13, CRG-T15 | contract | Canonical and generated review entrypoints. |
| CRG-R7–CRG-R11 | CRG-T03, CRG-T13 | contract | Embedded feasibility and Proposal Review authority. |
| CRG-R12–CRG-R16 | CRG-T04, CRG-T07, CRG-T09 | integration | Exact design membership, coherence, and atomic authority. |
| CRG-R17–CRG-R21 | CRG-T05, CRG-T07, CRG-T09 | integration | Exact delivery membership, traceability, and implementation authorization. |
| CRG-R22–CRG-R24 | CRG-T04, CRG-T05, CRG-T09 | contract | Visible member maps and governed invalidation without package hashes. |
| CRG-R25–CRG-R28 | CRG-T02, CRG-T06, CRG-T07, CRG-T10 | contract, integration | Bounded context, checked mutation, atomic failure, and unknown vocabularies. |
| CRG-R29–CRG-R34 | CRG-T07, CRG-T08, CRG-T09 | integration | Outcomes, finding attribution, corrections, and rereview. |
| CRG-R35–CRG-R40 | CRG-T01, CRG-T10, CRG-T16 | integration, end-to-end | No dual-mode metadata, cutover blocking, and rollback. |
| CRG-R41–CRG-R42 | CRG-T11, CRG-T12, CRG-T16 | integration, end-to-end | Preserved downstream gates and Verify inputs. |
| CRG-R43–CRG-R45 | CRG-T13, CRG-T14, CRG-T15, CRG-T17 | contract, smoke | Canonical surfaces, generated parity, and semantic-review limits. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | CRG-T03 | Feasibility remains embedded and jointly reviewed. |
| E2, E3 | CRG-T04, CRG-T08 | Coherent design approves atomically; contradiction blocks the package. |
| E4 | CRG-T05 | Delivery trace is evaluated as one package. |
| E5 | CRG-T09 | A governed member revision makes package authority review-required. |
| E6, E7 | CRG-T01, CRG-T16 | Legacy-dependent work blocks cutover; historical evidence is not package authority. |
| E8 | CRG-T08, CRG-T13 | Reviewer independence and owner routing are preserved. |
| E9 | CRG-T06, CRG-T07 | Existing lifecycle family exposes and performs package operations. |

## Edge case coverage

| Edge cases | Covered by |
| --- | --- |
| EC1–EC2 | CRG-T03, CRG-T09 |
| EC3–EC5 | CRG-T04, CRG-T08, CRG-T09 |
| EC6–EC8 | CRG-T05, CRG-T08 |
| EC9–EC10 | CRG-T01, CRG-T16 |
| EC11 | CRG-T09 |
| EC12 | CRG-T15, CRG-T17 |
| EC13 | CRG-T13 |
| EC14 | CRG-T05, CRG-T13 |

## Proof map

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | CRG-R1, CRG-R7, CRG-R8, CRG-R9, CRG-R10, CRG-R12, CRG-R17, CRG-R22, CRG-R28 | BND-INPUT-001 | CRG-T01, CRG-T02, CRG-T03, CRG-T04, CRG-T05 | contract | automated | CMD-002, CMD-003, CMD-010, CMD-011 | M1/M2/M4 evidence | M1 | - | - |
| PRF-002 | covered | CRG-R2, CRG-R12, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R24, CRG-R29, CRG-R34, CRG-R35 | BND-STATE-001 | CRG-T04, CRG-T05, CRG-T07, CRG-T09, CRG-T11 | integration | automated | CMD-001, CMD-004, CMD-012, CMD-014, CMD-015, CMD-016, CMD-017 | M2/M3 evidence | M2 | - | - |
| PRF-003 | covered | CRG-R5, CRG-R13, CRG-R14, CRG-R18, CRG-R22, CRG-R29, CRG-R31, CRG-R33, CRG-R35, CRG-R37 | BND-AUTH-001 | CRG-T01, CRG-T04, CRG-T05, CRG-T08, CRG-T13 | contract | automated | CMD-001, CMD-005, CMD-006, CMD-010, CMD-012, CMD-018 | M1/M2/M4 evidence | M1 | - | - |
| PRF-004 | covered | CRG-R12, CRG-R14, CRG-R15, CRG-R16, CRG-R17, CRG-R19, CRG-R21, CRG-R31, CRG-R33, CRG-R42 | BND-COMPOSE-001 | CRG-T04, CRG-T05, CRG-T08, CRG-T12 | integration | automated | CMD-001, CMD-012, CMD-014 | M2/M3 evidence | M2 | - | - |
| PRF-005 | covered | CRG-R23, CRG-R24, CRG-R25, CRG-R26, CRG-R27, CRG-R34 | BND-TEMPORAL-001 | CRG-T09 | integration | automated | CMD-012, CMD-013 | M2 evidence | M2 | - | - |
| PRF-006 | covered | CRG-R10, CRG-R13, CRG-R18, CRG-R20, CRG-R26, CRG-R33, CRG-R39 | BND-RECOVERY-001 | CRG-T08, CRG-T10, CRG-T16 | integration | automated | CMD-009, CMD-012, CMD-013 | M2/M6 evidence | M2 | - | - |
| PRF-007 | covered | CRG-R1, CRG-R5, CRG-R35, CRG-R36, CRG-R37, CRG-R38, CRG-R39, CRG-R40 | BND-COMPAT-001 | CRG-T01, CRG-T11, CRG-T16 | end-to-end | automated | CMD-009, CMD-010, CMD-011, CMD-014 | M1/M3/M6 evidence | M1 | - | - |
| PRF-008 | covered | CRG-R25, CRG-R26, CRG-R27, CRG-R38, CRG-R43, CRG-R44 | BND-ENV-001 | CRG-T06, CRG-T15, CRG-T17 | smoke | automated | CMD-007, CMD-008, CMD-009 | M5/M6 evidence | M5 | - | - |
| PRF-009 | covered | CRG-R14, CRG-R16, CRG-R31 | INT-001 | CRG-T04, CRG-T08 | integration | automated | CMD-012, CMD-013 | M2 evidence | M2 | - | - |
| PRF-010 | covered | CRG-R20, CRG-R21, CRG-R31 | INT-002 | CRG-T05, CRG-T08 | integration | automated | CMD-012, CMD-013 | M2 evidence | M2 | - | - |
| PRF-011 | covered | CRG-R24, CRG-R26, CRG-R34 | INT-003 | CRG-T09 | integration | automated | CMD-012, CMD-013 | M2 evidence | M2 | - | - |
| PRF-012 | covered | CRG-R26, CRG-R39 | INT-004 | CRG-T10, CRG-T16 | integration | automated | CMD-009, CMD-012, CMD-014 | M2/M6 evidence | M2 | - | - |
| PRF-013 | covered | CRG-R35, CRG-R37 | INT-005 | CRG-T01, CRG-T16 | integration | automated | CMD-009, CMD-010, CMD-011, CMD-014 | M1/M6 evidence | M1 | - | - |
| PRF-014 | covered | CRG-R38, CRG-R44 | INT-006 | CRG-T15, CRG-T17 | smoke | automated | CMD-007, CMD-008, CMD-009 | M5/M6 evidence | M5 | - | - |
| PRF-015 | covered | CRG-R29, CRG-R31, CRG-R33 | INT-007 | CRG-T08 | integration | automated | CMD-003, CMD-004, CMD-012, CMD-013, CMD-014, CMD-015, CMD-016, CMD-017 | M2/M3 evidence | M2 | - | - |
| PRF-016 | covered | CRG-R35, CRG-R38, CRG-R39 | INT-008 | CRG-T01, CRG-T16 | end-to-end | automated | CMD-009, CMD-010, CMD-011, CMD-014 | M1/M6 evidence | M1 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD-001 | `npm test --prefix packages/rigorloop` | existing/configured | implementation | M2, M6 | M2 | Any failing test blocks the milestone. | Node test runner must report executed tests. | milestone evidence | Local tests only. |
| CMD-002 | `python scripts/test-change-metadata-validator.py` | existing/configured | implementation | M1, M5 | M1 | Nonzero blocks the milestone. | Harness must execute its fixture inventory. | milestone evidence | Local fixture writes only. |
| CMD-003 | `python scripts/test-review-artifact-validator.py` | existing/configured | implementation | M2, M5 | M2 | Nonzero blocks the milestone. | Harness must execute its fixture inventory. | milestone evidence | Local fixture writes only. |
| CMD-004 | `python scripts/test-workflow-automation.py` | existing/configured | implementation | M3 | M3 | Nonzero blocks routing work. | Harness must execute its fixture inventory. | M3 evidence | Local fixture writes only. |
| CMD-005 | `python scripts/validate-skills.py && python scripts/test-skill-validator.py` | existing/configured | implementation | M4, M6 | M4 | Either nonzero result blocks the owning milestone. | Both commands must execute applicable checks. | M4/M6 evidence | Reads canonical skills and local fixtures. |
| CMD-006 | `python scripts/build-skills.py --check` | existing/configured | implementation | M4 | M4 | Drift blocks M4. | Not applicable; parity check has an explicit result. | M4 evidence | Check mode does not publish. |
| CMD-007 | `python scripts/test-adapter-distribution.py` | existing/configured | implementation | M5, M6 | M5 | Nonzero blocks M5 and cutover. | Harness must execute all supported-target fixtures. | M5/M6 evidence | Local temporary archives only. |
| CMD-008 | `python scripts/build-adapters.py --version v0.4.1 --output-dir release-output/v0.4.1 && python scripts/validate-adapters.py --root release-output/v0.4.1 --version v0.4.1` | planned-for-implementation | implementation | M5 | M5 | Build or validation failure blocks cutover. | Validation must inspect every declared adapter. | M5 evidence | Writes only the declared local output directory; no publication. |
| CMD-009 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | verification | M6, M7 | M6 | Any failure blocks cutover or closeout. | Broad smoke must report selected checks; empty selection fails. | M6/M7 evidence | Repository-local checks; no release or deployment. |
| CMD-010 | `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js` | existing/configured | implementation | M1 | M1 | Any failing focused lifecycle test blocks M1. | Node test runner must report executed tests. | M1 evidence | Local focused tests only. |
| CMD-011 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | implementation | M1, M5 | M1 | Nonzero blocks the owning milestone. | Harness must execute its fixture inventory. | M1/M5 evidence | Local fixture writes only. |
| CMD-012 | `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-transaction.test.js` | existing/configured | implementation | M2 | M2 | Any failing package-lifecycle test blocks M2. | Node test runner must report executed tests. | M2 evidence | Local focused tests only. |
| CMD-013 | `python scripts/test-governed-lifecycle-cli-validator.py` | existing/configured | implementation | M2, M6 | M2 | Nonzero blocks the owning milestone. | Harness must execute its fixture inventory. | M2/M6 evidence | Local fixture writes only. |
| CMD-014 | `node --test packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-read.test.js` | existing/configured | implementation | M3 | M3 | Any failing routing test blocks M3. | Node test runner must report executed tests. | M3 evidence | Local focused tests only. |
| CMD-015 | `python scripts/test-workflow-automation-policy.py` | existing/configured | implementation | M3 | M3 | Nonzero blocks routing work. | Harness must execute its fixture inventory. | M3 evidence | Local fixture writes only. |
| CMD-016 | `python scripts/test-workflow-automation-state.py` | existing/configured | implementation | M3 | M3 | Nonzero blocks routing work. | Harness must execute its fixture inventory. | M3 evidence | Local fixture writes only. |
| CMD-017 | `python scripts/test-workflow-code-state.py` | existing/configured | implementation | M3 | M3 | Nonzero blocks downstream authority work. | Harness must execute its fixture inventory. | M3 evidence | Local fixture writes only. |
| CMD-018 | `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md` | existing/configured | implementation | M4 | M4 | Nonzero blocks M4. | Not applicable; the audit reports an explicit result. | M4 evidence | Reads only the declared canonical guidance. |
| CMD-019 | `python scripts/test-lifecycle-cli-conformance.py` | existing/configured | implementation | M6 | M6 | Nonzero blocks cutover. | Harness must execute its fixture inventory. | M6 evidence | Local fixture writes only. |
| CMD-020 | `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-28-consolidate-rigorloop-review-gates` | existing/configured | verification | M7 | M7 | Nonzero blocks closeout. | Not applicable; closeout validation has an explicit result. | M7 evidence | Reads the owning change root only. |
| CMD-021 | `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml` | existing/configured | verification | M7 | M7 | Nonzero blocks closeout. | Not applicable; metadata validation has an explicit result. | M7 evidence | Reads the owning change record only. |
| CMD-022 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md --path specs/consolidated-review-gates.md --path docs/adr/ADR-20260828-consolidated-review-package-topology.md` | existing/configured | verification | M7 | M7 | Nonzero blocks closeout. | Not applicable; lifecycle validation has an explicit result. | M7 evidence | Reads only the declared governed artifacts and owning change state. |
| CMD-023 | `node --test packages/rigorloop/test/result-renderer.test.js` | existing/configured | implementation | M1 | M1 | Any failing public-output fixture blocks M1. | Node test runner must report executed tests. | M1 correction evidence | Local public-output regression only. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | CRG-T01, CRG-T02 | none | CMD-002, CMD-010, CMD-011, CMD-023 | M1 correction evidence | M1 code review | No manifest or topology marker exists. |
| M2 | CRG-T04–CRG-T10 | none | CMD-001, CMD-003, CMD-012, CMD-013 | M2 implementation evidence | M2 code review | Includes visible-map, invalidation, owner-mapping, outcome, and fault-injection proof. |
| M3 | CRG-T08, CRG-T11, CRG-T12 | none | CMD-004, CMD-014, CMD-015, CMD-016, CMD-017 | M3 implementation evidence | M3 code review | Covers the consolidated graph and downstream authority. |
| M4 | CRG-T03, CRG-T13 | none | CMD-005, CMD-006, CMD-018 | M4 implementation evidence | M4 code review | Semantic review remains independent. |
| M5 | CRG-T02, CRG-T14, CRG-T15 | none | CMD-002, CMD-003, CMD-007, CMD-008, CMD-011 | M5 implementation evidence | M5 code review | Generated parity precedes cutover. |
| M6 | CRG-T16, CRG-T17 | none | CMD-001, CMD-005, CMD-007, CMD-009, CMD-013, CMD-019 | M6 cutover and rollback evidence | M6 code review | Cutover is one atomic reviewed slice. |
| M7 | CRG-T12, CRG-T17 | none | CMD-009, CMD-020, CMD-021, CMD-022 | explain-change, final review, and verify evidence | Verify and PR handoff | Lifecycle closeout adds no implementation scope. |

## Test cases

### CRG-T01. Reject dual-mode activation machinery

- Covers: CRG-R1–CRG-R5, CRG-R35–CRG-R40, E6, E7, EC9, EC10, BND-INPUT-001, BND-AUTH-001, BND-COMPAT-001, INT-005, INT-008
- Level: integration
- Command IDs: CMD-002, CMD-010, CMD-011, CMD-023
- Fixture/setup: New-change, lifecycle status/context, schemas, validators, and repository paths with no topology marker or activation manifest; stale dual-mode fixture variants.
- Steps: Create and read governed changes, validate metadata, run the public-output fixture, and scan owned runtime/schema surfaces for abandoned activation machinery.
- Expected result: New changes contain no topology field, reads infer no topology or baseline, no activation document is required, and stale dual-mode fields or files are absent from the supported contract.
- Failure proves: Hidden coexistence or activation authority remains in the implementation.
- Evidence artifact: M1 and M6 evidence
- Automation location: lifecycle, new-change, and metadata-validator tests
- Required by milestone: M1

### CRG-T02. Reject every remaining unknown closed-vocabulary value first

- Covers: CRG-R1, CRG-R28–CRG-R30, CRG-R45, CRG-AC10, BND-INPUT-001
- Level: contract
- Command IDs: CMD-002, CMD-003, CMD-011
- Fixture/setup: One fixture per new package kind, role, outcome, finding scope, artifact kind, and settlement state with an unknown value.
- Steps: Submit each fixture before any dependent consistency condition is evaluated.
- Expected result: Each supported closed vocabulary produces an explicit error and no state mutation; no topology or activation vocabulary exists.
- Failure proves: A closed set can silently fall through consistency logic.
- Evidence artifact: M1, M2, and M5 evidence
- Automation location: lifecycle and repository validator tests
- Required by milestone: M1

### CRG-T03. Enforce embedded proposal feasibility

- Covers: CRG-R7–CRG-R11, E1, EC1, EC2, BND-INPUT-001
- Level: contract
- Command IDs: CMD-005, CMD-006, CMD-018
- Fixture/setup: Proposal templates and proposals with complete, missing, duplicate, unsupported, contradicted, stale, and blocking Feasibility sections.
- Steps: Validate authoring shape and run Proposal Review criteria fixtures.
- Expected result: Exactly one complete embedded section is accepted for review; inadequate evidence routes to proposal revision; no standalone feasibility artifact or gate is introduced.
- Failure proves: Feasibility ownership or Proposal Review authority is incomplete.
- Evidence artifact: M4 evidence
- Automation location: skill-validator fixtures
- Required by milestone: M4

### CRG-T04. Compose and identify the design package

- Covers: CRG-R12–CRG-R16, CRG-R22–CRG-R24, E2, E3, EC3–EC5, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, INT-001
- Level: integration
- Command IDs: CMD-001, CMD-003, CMD-012, CMD-013
- Fixture/setup: Primary architecture/spec, ordered ADRs, accepted proposal binding, and missing, duplicate, extra-role, unsafe-path, and contradictory variants.
- Steps: Request design context, inspect the explicit member ID-to-path map, and attempt each review outcome.
- Expected result: Exact coherent membership exposes the architecture, specification, and applicable ADR paths directly; invalid membership fails; contradiction records a cross-artifact finding; no component-only approval grants progression.
- Failure proves: Design package composition or atomic authority is unsound.
- Evidence artifact: M2 evidence
- Automation location: package lifecycle and review-validator tests
- Required by milestone: M2

### CRG-T05. Compose delivery and prove the full trace

- Covers: CRG-R17–CRG-R21, CRG-R22–CRG-R24, E4, EC6, EC14, BND-STATE-001, BND-COMPOSE-001, INT-002
- Level: integration
- Command IDs: CMD-001, CMD-003, CMD-012, CMD-013
- Fixture/setup: Current plan/test-spec pair and variants with missing ownership, wrong order, wrong proof boundary, missing risk evidence, or incompatible proof sequence.
- Steps: Request delivery context and evaluate every trace from requirement through architecture, milestone, proof, and command.
- Expected result: Only a complete compatible trace can approve atomically and authorize implementation; every gap produces an attributable package finding.
- Failure proves: Delivery approval can hide sequencing or proof gaps.
- Evidence artifact: M2 evidence
- Automation location: package lifecycle and review-validator tests
- Required by milestone: M2

### CRG-T06. Expose bounded package context and status

- Covers: CRG-R25, CRG-R27, E9, BND-ENV-001
- Level: contract
- Command IDs: CMD-001, CMD-012, CMD-013
- Fixture/setup: Current, review-required, incomplete, blocked, and settled design/delivery packages.
- Steps: Run public lifecycle status and both review contexts.
- Expected result: Output names each member ID and exact path, upstream review ID, review ID and round, package status, blockers, correction targets, and next operation without aggregate or member hashes.
- Failure proves: Contributors must infer package authority or maintain redundant identities.
- Evidence artifact: M2 evidence
- Automation location: lifecycle read tests
- Required by milestone: M2

### CRG-T07. Record outcomes and settle packages atomically

- Covers: CRG-R15, CRG-R21, CRG-R26, CRG-R29, E9, BND-STATE-001, BND-RECOVERY-001
- Level: integration
- Command IDs: CMD-001, CMD-012, CMD-013
- Fixture/setup: Approved, changes-requested, blocked, and inconclusive records for both package kinds.
- Steps: Record and settle through the public lifecycle operations, including dry run and exact replay.
- Expected result: Approved settles the complete package; other outcomes remain visible with no authority; dry run writes nothing; exact replay is idempotent.
- Failure proves: Outcome authority or atomic settlement is incorrect.
- Evidence artifact: M2 evidence
- Automation location: lifecycle evidence and transaction tests
- Required by milestone: M2

### CRG-T08. Attribute findings and route corrections without self-approval

- Covers: CRG-R29–CRG-R34, E3, E8, EC7, EC8, BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, INT-001, INT-002, INT-007
- Level: integration
- Command IDs: CMD-001, CMD-003, CMD-004, CMD-012, CMD-013, CMD-014, CMD-015, CMD-016, CMD-017
- Fixture/setup: Artifact-local, cross-artifact, upstream-direction, multi-owner, unresolved, and insufficient-evidence findings.
- Steps: Record review results, resolve when required, route each correction, revise through owners, and attempt rereview.
- Expected result: Findings retain stable IDs, exact scopes and affected artifacts; reviewers do not edit components; workflow routes every necessary owner; resolution never substitutes for changed-package rereview.
- Failure proves: Consolidation weakens attribution, independence, or correction safety.
- Evidence artifact: M2/M3/M4 evidence
- Automation location: lifecycle correction, review-validator, and skill-validator tests
- Required by milestone: M2

### CRG-T09. Invalidate governed package revisions and reject stale mutations

- Covers: CRG-R23–CRG-R26, CRG-R34, E5, EC4, EC11, BND-STATE-001, BND-TEMPORAL-001, INT-003
- Level: integration
- Command IDs: CMD-001, CMD-012, CMD-013
- Fixture/setup: Record a member revision, replace the upstream review ID, change membership, use a stale lifecycle revision, mismatch the explicit map or review data, and make one unrecorded direct edit.
- Steps: Inspect invalidation after governed events; attempt stale record, mismatched settlement, identical replay with refreshed lifecycle context, and current rereview.
- Expected result: Governed member or upstream-review changes set approval to `review-required`; stale lifecycle or mismatched review data fails unchanged; identical refreshed replay is idempotent; an unrecorded direct edit does not trigger hashing or automatic invalidation in this slice.
- Failure proves: Package invalidation or retry authority is inconsistent with the lightweight contract.
- Evidence artifact: M2 evidence
- Automation location: lifecycle package and transaction tests
- Required by milestone: M2

### CRG-T10. Recover from interrupted package mutation and pre-adoption revert

- Covers: CRG-R26, CRG-R39, INT-004, BND-RECOVERY-001
- Level: integration
- Command IDs: CMD-001, CMD-009, CMD-012, CMD-013
- Fixture/setup: Fault injection before replacement, after replacement, during validation, and during a pre-adoption release revert.
- Steps: Interrupt record and settlement transactions, then exercise the reviewed pre-adoption code-revert fixture and inspect recovery.
- Expected result: Only the prior or complete candidate state is authoritative; partial projection grants no authority; recovery is deterministic.
- Failure proves: Atomicity or recovery can expose partial package state.
- Evidence artifact: M2/M6 evidence
- Automation location: lifecycle transaction and cutover tests
- Required by milestone: M2

### CRG-T11. Enforce the consolidated stage graph

- Covers: CRG-R2–CRG-R5, CRG-R15, CRG-R21, CRG-R36–CRG-R41, BND-STATE-001, BND-AUTH-001, BND-COMPAT-001
- Level: integration
- Command IDs: CMD-004, CMD-014, CMD-015, CMD-016, CMD-017
- Fixture/setup: Completed and incomplete source stages for every adjacent consolidated edge, skipped and retired edges, stale authority, correction paths, and active automation projections.
- Steps: Request normal advancement and correction routing through public operations.
- Expected result: Only an adjacent consolidated edge with exact completion authority advances; settlement remains isolated; automation synchronizes; retired, invalid, or stale requests write nothing.
- Failure proves: Workflow routing can bypass or mix review authority.
- Evidence artifact: M3 evidence
- Automation location: lifecycle stage-advance and workflow-automation tests
- Required by milestone: M3

### CRG-T12. Preserve downstream assurance and Verify inputs

- Covers: CRG-R41–CRG-R42, CRG-AC8, BND-COMPOSE-001
- Level: integration
- Command IDs: CMD-004, CMD-009, CMD-014, CMD-015, CMD-016, CMD-017, CMD-020, CMD-021, CMD-022
- Fixture/setup: Current and stale proposal, design, delivery, implementation, code-review, explanation, and validation evidence, plus historical individual-review evidence.
- Steps: Build Code Review and Verify contexts and attempt final readiness.
- Expected result: Existing downstream responsibilities remain separate; current package evidence is required; stale, partial, or historical-only authority blocks.
- Failure proves: Consolidation bypasses downstream assurance.
- Evidence artifact: M3/M4/M7 evidence
- Automation location: downstream context, skill-validator, and broad-smoke tests
- Required by milestone: M3

### CRG-T13. Publish independent review responsibilities and retire old entrypoints

- Covers: CRG-R3–CRG-R11, CRG-R13–CRG-R21, CRG-R29–CRG-R34, CRG-R41–CRG-R45, E8, EC13, EC14, BND-AUTH-001
- Level: contract
- Command IDs: CMD-005, CMD-006, CMD-018
- Fixture/setup: Canonical skills, templates, reciprocal ownership maps, direct invocation, retired-entrypoint inventory, and repository-maintainer leakage fixtures.
- Steps: Validate proposal feasibility, new Design/Delivery skills, absence of four retired progression skills from the post-cutover inventory, isolation, claims, and generated local mirrors.
- Expected result: Responsibilities are independently invocable; retired progression entrypoints are absent rather than aliases; review never edits authorship; direct review remains isolated; canonical skill contracts validate.
- Failure proves: Public workflow responsibilities are ambiguous or unsafe.
- Evidence artifact: M4 evidence
- Automation location: skill-validator and build-skills checks
- Required by milestone: M4

### CRG-T14. Enforce structural invariants without semantic overclaim

- Covers: CRG-R28, CRG-R35, CRG-R43, CRG-R45, CRG-AC9–CRG-AC11
- Level: contract
- Command IDs: CMD-002, CMD-003, CMD-007, CMD-011
- Fixture/setup: Valid and invalid package, finding, lifecycle, cutover-prerequisite, and generated-manifest records.
- Steps: Run each existing validator owner and compare its accepted claims with CRG-R45.
- Expected result: Structure, references, identities, parity, and closed vocabularies are enforced; no validator claims feasibility, coherence, adequacy, fidelity, or readiness.
- Failure proves: Validation is incomplete or improperly replaces semantic review.
- Evidence artifact: M5 evidence
- Automation location: repository validator suites
- Required by milestone: M5

### CRG-T15. Prove generated adapter and release parity

- Covers: CRG-R6, CRG-R38, CRG-R43–CRG-R44, EC12, BND-ENV-001, INT-006
- Level: smoke
- Command IDs: CMD-007, CMD-008
- Fixture/setup: Canonical skills plus Codex, Claude, and OpenCode archive descriptors with missing, stale, extra, drifted, and correct inventories.
- Steps: Build temporary archives and validate skill inventory, aliases, responsibilities, manifests, checksums, and portability.
- Expected result: Every supported adapter matches the canonical consolidated responsibilities and omits retired progression entrypoints; any drift blocks cutover and packaging.
- Failure proves: Installable workflow differs from canonical governance.
- Evidence artifact: M5/M6 evidence
- Automation location: adapter distribution and validation tests
- Required by milestone: M5

### CRG-T16. Cut over atomically and preserve evidence on rollback

- Covers: CRG-R1–CRG-R45, CRG-AC1–CRG-AC11, E6, E7, EC9, EC10, BND-COMPAT-001, BND-RECOVERY-001, INT-004–INT-006, INT-008
- Level: end-to-end
- Command IDs: CMD-001, CMD-005, CMD-007, CMD-009, CMD-013, CMD-019
- Fixture/setup: Current canonical/generated prerequisites, zero nonterminal legacy-dependent changes, consolidated public flow, historical-authority misuse, partial cutover, and pre-adoption code-revert fixture.
- Steps: Validate prerequisites, cut over once, run the consolidated flow, reject historical and partial authority, and prove the pre-adoption revert without rewriting records.
- Expected result: Cutover is atomic; old progression entrypoints are absent; historical evidence remains readable but non-authorizing; pre-adoption revert restores the prior release without rewriting records.
- Failure proves: Cutover or rollback violates single-mechanism authority or evidence preservation.
- Evidence artifact: M6 cutover and rollback evidence
- Automation location: cutover integration and broad-smoke tests
- Required by milestone: M6

### CRG-T17. Prove complete composition before release handoff

- Covers: CRG-R38, CRG-R43–CRG-R45, CRG-AC9–CRG-AC11, EC12, BND-ENV-001, INT-006
- Level: smoke
- Command IDs: CMD-008, CMD-009, CMD-020, CMD-021, CMD-022
- Fixture/setup: The complete candidate revision after M1–M6 reviews and generated archive construction.
- Steps: Run repository broad smoke, archive validation, consolidated and historical-authority flows, and rollback proof at one revision.
- Expected result: All canonical, runtime, validator, cutover, and generated surfaces agree; any missing or stale owner blocks cutover or closeout.
- Failure proves: Integrated release evidence is incomplete.
- Evidence artifact: M6/M7 evidence
- Automation location: repository broad smoke and release validation
- Required by milestone: M6

## Fixtures and data

Use repository-local temporary fixture roots. Package fixtures declare package kind, ordered artifact ID-to-path members, upstream review ID, review ID, outcome, and status. Cutover fixtures declare the nonterminal legacy-dependent inventory and expected public gate inventory. Fault fixtures inject failures only through the existing lifecycle transaction test adapter. No fixture may depend on network access, machine-local paths, aggregate hashes, or member content hashes.

## Mocking/stubbing policy

Mock only filesystem transaction faults, generated archive inputs, and unavailable external boundaries already abstracted by repository test adapters. Do not mock member-map resolution, governed invalidation, cutover admission, public lifecycle dispatch, validator admission, or workflow completion authority in tests claiming those outcomes.

## Migration or compatibility tests

CRG-T01, CRG-T11, and CRG-T16 prove absence of dual-mode metadata, rejection of retired progression and historical-only authority, legacy-dependent cutover blocking, atomic cutover, and pre-adoption rollback. No test migrates active legacy changes in place.

## Observability verification

CRG-T06 asserts stable status/context fields and actionable invariant errors. CRG-T07–CRG-T11 assert mutation results distinguish success, blocked, stale, idempotent, recovered, and unchanged outcomes. Existing privacy-bounded CLI diagnostic tests must continue passing.

## Security/privacy verification

Fixtures assert repository-relative paths, safe artifact resolution, reviewer/author separation, authority-checked operations, and absence of machine-local or private runtime data in package and review records. Existing path traversal, symlink, and request-envelope checks remain mandatory.

## Performance checks

No numeric latency target applies. Contract tests assert package context reads only registered members and the accepted upstream binding rather than repository history or external services. Broad smoke must remain bounded by the existing repository command.

## Manual QA checklist

Not applicable. All first-slice observable outcomes have automated contract, integration, end-to-end, or smoke proof. Independent semantic reviews remain lifecycle gates rather than manual QA procedures owned by this test specification.

## What not to test and why

- Do not test merged architecture/spec or plan/test-spec artifacts because merging is a non-goal.
- Do not test automatic semantic or byte-equivalence detection for unrecorded direct edits because that behavior and content hashing are outside the first slice.
- Do not test in-place legacy migration, runtime old/new coexistence, multiple workflow profiles, external services, deployment, or publication because they are outside scope.
- Do not treat validators as proof of feasibility credibility, design coherence, delivery adequacy, implementation fidelity, or final readiness; those remain independent semantic decisions.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review` under the implementing change's pre-cutover contract.
- M1 implementation only after clean test-spec settlement.

## Follow-on artifacts

None yet.

## Readiness

Ready for `test-spec-review`. This proof map does not authorize implementation, claim validation results, or establish verification, branch, release, or PR readiness.
