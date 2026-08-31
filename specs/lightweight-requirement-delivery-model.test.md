# Lightweight Requirement-to-Delivery Model Test Specification

## Owning change record

`docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml`

## Related spec and plan

- Spec: `specs/lightweight-requirement-delivery-model.md`
- Plan: `docs/plans/2026-08-30-lightweight-requirement-delivery-model.md`
- Architecture/ADRs: `docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md`; no new ADR

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Specification | `specs/lightweight-requirement-delivery-model.md` | `spec` | `design-review-r2`; `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/design-review-r2.md` |
| Architecture | `docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md` | `architecture` | `design-review-r2`; `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/design-review-r2.md` |
| Execution plan | `docs/plans/2026-08-30-lightweight-requirement-delivery-model.md` | `plan` | pending Delivery Review |

## Testing strategy

Use focused contract tests for the canonical shared source, all nine resource maps, stage-local responsibility, proportional examples, authority exclusions, and shared-copy drift. Use existing skill build and adapter-distribution suites for generated archive and clean-install parity. Deterministic checks prove structure, mapping, and byte identity; Delivery Review, Code Review, and Verify retain semantic judgment over meaningful refinement, allocation, implementation fidelity, and evidence closure.

Boundary model version: boundary-first-v1
Boundary model scope: RTD-R1, RTD-R2, RTD-R3, RTD-R4, RTD-R5, RTD-R6, RTD-R7, RTD-R8, RTD-R9, RTD-R10, RTD-R11, RTD-R12, RTD-R13, RTD-R14, RTD-R15, RTD-R16, RTD-R17, RTD-R18, RTD-R19, RTD-R20

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| RTD-R1-RTD-R3 | RTD-T01, RTD-T02 | contract | Model vocabulary, raw-input handling, and Proposal/IR responsibility. |
| RTD-R4-RTD-R6 | RTD-T02, RTD-T03 | contract | Stable SR ownership, architecture realization, and plan allocation. |
| RTD-R7-RTD-R10 | RTD-T03, RTD-T04 | contract | Many-to-many work, proportional hierarchy, milestone rationale, and forward traceability. |
| RTD-R11-RTD-R12 | RTD-T05, RTD-T06 | contract | Gate-local traceability judgment with unchanged authority. |
| RTD-R13-RTD-R15 | RTD-T02, RTD-T05, RTD-T07 | integration | Canonical source, conditional skill-local loading, and no shared lifecycle authority. |
| RTD-R16-RTD-R17 | RTD-T04, RTD-T06 | contract | No new lifecycle entities and unchanged test-spec/Delivery authority. |
| RTD-R18 | RTD-T07, RTD-T08 | integration, smoke | Canonical, local, generated, and clean-install parity. |
| RTD-R19 | RTD-T06, RTD-T08 | contract | Historical readability and coherent activation without retrofit. |
| RTD-R20 | RTD-T05, RTD-T07 | contract | Deterministic structure versus semantic-review ownership. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | RTD-T04 | A small change omits RR/IR/AR records and empty Epic/Feature/Story levels. |
| E2 | RTD-T03 | A milestone cites its governing SR and architecture boundary. |
| E3 | RTD-T03 | Many-to-many SR and Story allocation remains valid. |
| E4 | RTD-T05 | Shared vocabulary does not grant Design Review authority. |
| E5 | RTD-T07, RTD-T08 | Missing or drifted packaged guidance fails before publication. |

## Edge case coverage

| Edge cases | Covered by |
| --- | --- |
| EC1-EC4 | RTD-T03, RTD-T04 |
| EC5 | RTD-T05 |
| EC6 | RTD-T06 |
| EC7-EC8 | RTD-T07, RTD-T08 |

## Proof map

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | RTD-R2, RTD-R3, RTD-R4, RTD-R9, RTD-R10 | BND-INPUT-001 | RTD-T02, RTD-T03 | contract | automated | CMD-001, CMD-002 | M1 evidence | M1 | - | - |
| PRF-002 | covered | RTD-R3, RTD-R4, RTD-R5, RTD-R6, RTD-R11, RTD-R12, RTD-R15 | BND-AUTH-001 | RTD-T02, RTD-T05, RTD-T06 | contract | automated | CMD-001, CMD-002 | M1/M2 evidence | M1, M2 | - | - |
| PRF-003 | covered | RTD-R10, RTD-R11, RTD-R13, RTD-R14, RTD-R15, RTD-R18 | BND-COMPOSE-001 | RTD-T05, RTD-T07, RTD-T08 | integration | automated | CMD-001, CMD-003, CMD-004, CMD-005 | M2/M3 evidence | M2, M3 | - | - |
| PRF-004 | covered | RTD-R10, RTD-R18, RTD-R20 | BND-RECOVERY-001 | RTD-T05, RTD-T07, RTD-T08 | integration | automated | CMD-001, CMD-004, CMD-005 | M2/M3 evidence | M2, M3 | - | - |
| PRF-005 | covered | RTD-R12, RTD-R16, RTD-R17, RTD-R18, RTD-R19 | BND-COMPAT-001 | RTD-T06, RTD-T08 | integration | automated | CMD-001, CMD-003, CMD-004, CMD-005 | M2/M3 evidence | M2, M3 | - | - |
| PRF-006 | covered | RTD-R13, RTD-R14, RTD-R18 | BND-ENV-001 | RTD-T07, RTD-T08 | smoke | automated | CMD-003, CMD-004, CMD-005 | M3 evidence | M3 | - | - |
| PRF-007 | covered | RTD-R11, RTD-R12, RTD-R15 | INT-001 | RTD-T05 | contract | automated | CMD-001, CMD-002 | M2 evidence | M2 | - | - |
| PRF-008 | covered | RTD-R13, RTD-R18, RTD-R19 | INT-002 | RTD-T07, RTD-T08 | integration | automated | CMD-003, CMD-004, CMD-005 | M3 evidence | M3 | - | - |
| PRF-009 | covered | RTD-R9, RTD-R10, RTD-R20 | INT-003 | RTD-T03, RTD-T05 | contract | automated | CMD-001, CMD-002 | M1/M2 evidence | M1, M2 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD-001 | `python scripts/test-skill-validator.py` | existing/configured | implementation | M1, M2, M3 | M1 | Any failed contract fixture blocks the owning milestone. | The harness must report executed tests; an empty run fails. | milestone evidence | Local fixture and temporary-file activity only. |
| CMD-002 | `python scripts/validate-skills.py skills/proposal/SKILL.md skills/proposal-review/SKILL.md skills/architecture/SKILL.md skills/spec/SKILL.md skills/design-review/SKILL.md skills/plan/SKILL.md skills/delivery-review/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md` | existing/configured | implementation | M1, M2 | M1 | Any invalid skill or resource map blocks review. | All nine declared skill paths must be processed. | M1/M2 evidence | Reads authored skill packages only. |
| CMD-003 | `python scripts/build-skills.py --check` | existing/configured | implementation | M1, M2, M3 | M1 | Drift or invalid generated projection blocks the owning milestone. | Not applicable; check mode returns an explicit result. | milestone evidence | Temporary build/check only; no publication. |
| CMD-004 | `python scripts/test-build-skills.py` | existing/configured | implementation | M3 | M3 | Any failed build or resource-copy case blocks M3. | The harness must report executed cases; an empty run fails. | M3 evidence | Temporary output only. |
| CMD-005 | `python scripts/test-adapter-distribution.py` | existing/configured | implementation | M3 | M3 | Any archive or clean-install parity failure blocks M3. | Every supported adapter fixture must execute. | M3 evidence | Temporary archives and installations only; no publication. |
| CMD-006 | `python scripts/validate-boundary-first.py --check --path specs/lightweight-requirement-delivery-model.md --path specs/lightweight-requirement-delivery-model.test.md` | existing/configured | test-spec | M1-M3 | Delivery Review | Any feature/proof-map structural error blocks Delivery authority. | Not applicable; the validator returns an explicit result. | test-spec authoring and review evidence | Reads the exact design and proof-map paths. |
| CMD-007 | `python scripts/validate-documentation-prose.py --mode audit --path templates/shared/requirement-to-delivery-model.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path skills/architecture/SKILL.md --path skills/spec/SKILL.md --path skills/design-review/SKILL.md --path skills/plan/SKILL.md --path skills/delivery-review/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md` | existing/configured | implementation | M1, M2 | M1 | Prose errors block the owning milestone. | Not applicable; the audit returns an explicit result. | M1/M2 evidence | Reads only declared authored guidance. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | RTD-T01, RTD-T02, RTD-T03, RTD-T04 | none | CMD-001, CMD-002, CMD-003, CMD-007 | `evidence/m1-authoring-model.md` | M1 code review | Proves vocabulary, authoring ownership, allocation, proportionality, and initial package validity. |
| M2 | RTD-T05, RTD-T06 | none | CMD-001, CMD-002, CMD-003, CMD-007 | `evidence/m2-review-traceability.md` | M2 code review | Proves gate-local semantic questions and unchanged authority. |
| M3 | RTD-T07, RTD-T08 | none | CMD-001, CMD-003, CMD-004, CMD-005 | `evidence/m3-package-parity.md` | M3 code review | Proves fail-closed shared-copy and supported installed-package parity. |
| M4 | RTD-T01-RTD-T08 | none | CMD-001-CMD-007 | final review, explanation, and verification evidence | Verify and PR handoff | Lifecycle closeout adds no implementation behavior. |

## Test cases

### RTD-T01. Define one concise and stable shared model

- Covers: RTD-R1, RTD-R7, RTD-R8, RTD-R16, RTD-AC1, RTD-AC4
- Level: contract
- Command IDs: CMD-001, CMD-002, CMD-007
- Fixture/setup: Canonical shared reference plus variants that conflate requirement and work hierarchies, require all work levels, or introduce RR/IR/AR records.
- Steps: Validate the canonical vocabulary, separation rule, proportionality rule, and explicit no-new-entity boundaries.
- Expected result: The source defines `RR → IR → SR → AR`, keeps work decomposition separate and optional, and requires no additional artifact or lifecycle entity.
- Failure proves: The conceptual model is incomplete or has become mandatory ceremony.
- Evidence artifact: `evidence/m1-authoring-model.md`
- Automation location: `scripts/test-skill-validator.py`
- Required by milestone: M1

### RTD-T02. Map authoring stages to existing artifact responsibilities

- Covers: RTD-R2-RTD-R6, RTD-R13-RTD-R15, RTD-AC2, E1, BND-INPUT-001, BND-AUTH-001
- Level: contract
- Command IDs: CMD-001, CMD-002, CMD-003
- Fixture/setup: Proposal, spec, architecture, and plan skills with exact local resource maps and missing, unconditional, escaped, or responsibility-swapped variants.
- Steps: Validate each stage-local instruction, load condition, packaged reference, and artifact/output contract.
- Expected result: proposal refines raw need into IR-level direction, spec owns SRs, architecture realizes SRs, and plan allocates them without creating new artifacts or authority.
- Failure proves: An authoring responsibility is missing, misplaced, or loaded unsafely.
- Evidence artifact: `evidence/m1-authoring-model.md`
- Automation location: skill-validator resource-map and focused responsibility fixtures
- Required by milestone: M1

### RTD-T03. Preserve meaningful and many-to-many allocation

- Covers: RTD-R6, RTD-R7, RTD-R9, RTD-R10, RTD-AC5, E2, E3, EC1-EC3, BND-INPUT-001, INT-003
- Level: contract
- Command IDs: CMD-001, CMD-002
- Fixture/setup: Plan guidance and structure for one SR across multiple work items, multiple SRs in one milestone, and justified non-SR maintenance work.
- Steps: Validate requirement and architecture references, dependencies, included work, and explicit non-SR obligation handling.
- Expected result: milestones can explain why they exist without forced one-to-one mappings or invented SRs.
- Failure proves: Allocation is untraceable, falsely normalized, or too rigid for approved work.
- Evidence artifact: `evidence/m1-authoring-model.md`
- Automation location: focused plan-skill contract fixtures
- Required by milestone: M1

### RTD-T04. Keep work hierarchy proportional

- Covers: RTD-R7, RTD-R8, RTD-R16, E1, E3, EC2-EC4
- Level: contract
- Command IDs: CMD-001, CMD-002
- Fixture/setup: Small one-milestone change, larger many-to-many initiative, and invalid empty Epic/Feature/Story placeholders.
- Steps: Validate that omitted levels are accepted and empty taxonomy emitted only for completeness is rejected by semantic criteria or focused fixture expectations.
- Expected result: small changes remain small while larger initiatives may add useful hierarchy.
- Failure proves: Taxonomy completeness has become an approval requirement.
- Evidence artifact: `evidence/m1-authoring-model.md`
- Automation location: shared-reference and authoring-skill fixtures
- Required by milestone: M1

### RTD-T05. Ask stage-local traceability questions without granting authority

- Covers: RTD-R11, RTD-R12, RTD-R15, RTD-R20, RTD-AC3, RTD-AC9, RTD-AC10, E4, EC5, BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, INT-001, INT-003
- Level: contract
- Command IDs: CMD-001, CMD-002, CMD-007
- Fixture/setup: Five review/verification skills with current authority text plus variants where shared guidance claims settlement, transition, artifact ownership, or semantic automation.
- Steps: Validate each stage's traceability question and the continued ownership of findings, outcomes, corrections, and readiness.
- Expected result: Proposal Review, Design Review, Delivery Review, Code Review, and Verify traverse the appropriate chain while retaining their existing authority.
- Failure proves: The shared model changes a review decision or lets deterministic tooling replace judgment.
- Evidence artifact: `evidence/m2-review-traceability.md`
- Automation location: focused review-family and verify skill fixtures
- Required by milestone: M2

### RTD-T06. Preserve lifecycle, proof-design, and historical contracts

- Covers: RTD-R12, RTD-R16, RTD-R17, RTD-R19, RTD-AC7, EC6, BND-AUTH-001, BND-COMPAT-001
- Level: contract
- Command IDs: CMD-001, CMD-002
- Fixture/setup: Existing lifecycle and test-spec authority claims, untouched historical examples, and invalid variants adding model-specific state, stages, or mandatory backfill.
- Steps: Validate that existing stage order and proof ownership remain unchanged and historical artifacts require no retrofit.
- Expected result: the model activates through guidance only and leaves settled history readable.
- Failure proves: The first slice has introduced an unapproved migration or lifecycle behavior.
- Evidence artifact: `evidence/m2-review-traceability.md`
- Automation location: skill-contract and negative phrase fixtures
- Required by milestone: M2

### RTD-T07. Fail closed on missing or drifted shared resources

- Covers: RTD-R13, RTD-R14, RTD-R18, RTD-R20, E5, EC7-EC8, BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001, INT-002
- Level: integration
- Command IDs: CMD-001, CMD-003, CMD-004
- Fixture/setup: Canonical source and nine skill-local copies with missing, altered, unmapped, escaped, and extra stale variants.
- Steps: Run existing shared-resource, skill-build, and resource-map validation over each variant.
- Expected result: exact coherent mappings pass; every missing, drifted, unsafe, or mixed copy fails with an actionable owning path.
- Failure proves: A published skill can silently diverge from the canonical model.
- Evidence artifact: `evidence/m3-package-parity.md`
- Automation location: existing skill-validator and build-skill test suites
- Required by milestone: M3

### RTD-T08. Preserve supported adapter and clean-install parity

- Covers: RTD-R18, RTD-R19, RTD-AC6, RTD-AC8, E5, EC7-EC8, BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001, INT-002
- Level: smoke
- Command IDs: CMD-003, CMD-004, CMD-005
- Fixture/setup: Temporary generated archives and clean target installations for every supported adapter and each selected consuming skill.
- Steps: Build temporary packages, inspect mapped resources, install into clean temporary roots, and validate byte parity and path containment.
- Expected result: all supported packages resolve the same self-contained model without canonical repository access or historical artifact rewrites.
- Failure proves: The canonical change does not reach a supported public package coherently.
- Evidence artifact: `evidence/m3-package-parity.md`
- Automation location: existing build and adapter-distribution suites
- Required by milestone: M3

## Fixtures and data

Use temporary canonical/local resource trees, all nine selected skill roots, small-change and many-to-many allocation examples, authority-conflict variants, and existing supported-adapter fixtures. No private stakeholder input, external tracker, network service, or persisted requirements database is required.

## Mocking/stubbing policy

Do not mock semantic review. Filesystem package fixtures may isolate canonical copies, generated archives, and clean installations. Tests must exercise existing public validator/build entrypoints rather than helper-only functions when claiming package behavior.

## Migration or compatibility tests

Prove that settled historical artifacts remain readable without RR, IR, or AR labels and that current mapped skill packages activate coherently. Do not rewrite historical proposal, spec, plan, review, release, or adapter evidence.

## Observability verification

No runtime logs, metrics, or traces are introduced. Validation diagnostics must identify the exact missing, drifted, escaped, or invalid mapped resource; semantic review evidence must cite existing SR, architecture, milestone, and review identities.

## Security/privacy verification

Confirm the shared guidance does not require copying unnecessary private raw-request content into durable artifacts and that packaged references cannot escape the installed skill root. Existing secret and repository-path checks remain authoritative.

## Performance checks

No runtime performance benchmark is applicable. Focused tests confirm conditional loading and concise stage-local instructions; existing build and distribution suites bound packaging overhead.

## Manual QA checklist

Not applicable. Every structural and package claim is automated; semantic sufficiency is owned by the required independent reviews rather than an additional manual checklist.

## What not to test and why

- Do not test new RR, IR, or AR lifecycle entities, because the approved contract forbids them.
- Do not require every change to emit Epic, Feature, Story, or Task levels.
- Do not grade prose semantics with a new automated traceability engine; formal review owns meaning.
- Do not invoke external trackers, publish packages, or require installed Codex, Claude Code, or OpenCode runtimes.
- Do not rewrite or revalidate settled historical artifacts against the new terminology.

## Uncovered gaps

None.

## Next artifacts

- Independent Delivery Review of this proof map with the exact execution plan.
- Implementation milestones only after Delivery authority is granted and the plan is initialized.

## Follow-on artifacts

None yet

## Readiness

Ready for Delivery Review reconciliation with `docs/plans/2026-08-30-lightweight-requirement-delivery-model.md`. This test specification does not authorize implementation.
