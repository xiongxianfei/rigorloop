# Lightweight Requirement-to-Delivery Model Execution Plan

## Purpose / big picture

Introduce one concise requirement-to-delivery model across RigorLoop's existing published skills without adding lifecycle entities, mandatory hierarchy, or machine-readable traceability. The implementation will make Proposal/IR, Specification/SR, architecture realization, plan allocation, implementation, and evidence traceable through existing artifacts and stable SR identities.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-30-lightweight-requirement-delivery-model.md`
- Spec: `specs/lightweight-requirement-delivery-model.md`
- Architecture: `docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md`
- Test spec: `specs/lightweight-requirement-delivery-model.test.md`
- Approved Design package: `design-review-r2`

## Context and orientation

The implementation boundary is authored Markdown plus existing deterministic packaging checks. One canonical shared source will live at `templates/shared/requirement-to-delivery-model.md`; nine selected skills will carry byte-identical local copies and short stage-specific loading guidance. Existing skill validation, build, adapter archive, and clean-install paths remain the only deterministic publication mechanisms.

The shared model explains relationships but grants no stage authority. Stable SR IDs remain the downstream join point. RR, IR, and AR remain conceptual, work hierarchy remains optional, and semantic traceability remains review-owned.

## Non-goals

- Add RR, IR, or AR artifacts, identifiers, lifecycle state, schemas, CLI operations, databases, or tracker integrations.
- Require Epic, Feature, Story, or Task levels or a one-to-one mapping between requirements and work.
- Change review-gate order, package authority, test-spec ownership, or settlement behavior.
- Hand-edit generated adapter packages or retrofit settled historical artifacts.
- Add a standalone validator, semantic traceability engine, or repository-wide index.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| RTD-R1-RTD-R10, RTD-R13-RTD-R16; BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | M1 shared model, authoring skills, proportional examples, and artifact structures |
| RTD-R11-RTD-R12, RTD-R15, RTD-R20; BND-AUTH-001, BND-RECOVERY-001; INT-001, INT-003 | M2 review and verification guidance with unchanged authority and semantic ownership |
| RTD-R13-RTD-R14, RTD-R17-RTD-R20; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-002 | M3 shared-copy validation and supported package parity |
| RTD-AC1-RTD-AC10 | Matching test specification and evidence across M1-M3 |

## Milestones

### M1. Publish the shared model through authoring stages

- Milestone kind: implementation
- Goal: Add the concise canonical model and integrate it proportionally into proposal, specification, architecture, and planning guidance and structures.
- Requirements: RTD-R1-RTD-R10, RTD-R13-RTD-R16; BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001.
- Architecture decisions: one canonical shared source, byte-identical skill-local copies, conditional loading, stable SR join points, and no new lifecycle state.
- Files/components likely touched:
  - `templates/shared/requirement-to-delivery-model.md`
  - `skills/proposal/`, `skills/spec/`, `skills/architecture/`, and `skills/plan/`
  - their existing artifact assets or references only where traceability prompts are needed
- Dependencies:
  - approved Design package `design-review-r2`
  - existing shared-resource and skill-resource-map contracts
- Tests and proof:
  - focused skill validation for resource mapping, stage-local responsibility, and conditional loading
  - examples for a small change without empty hierarchy and a many-to-many SR/work allocation
  - checks that artifact structures expose existing SR and architecture references without RR/IR/AR fields
- Implementation steps:
  - add focused failing assertions for the canonical source and four authoring consumers
  - author the compact shared model and copy it byte-for-byte into the selected skill roots
  - add short stage-local responsibility and exact resource-map load conditions
  - refine existing assets only where an existing field must make allocation or traceability explicit
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/proposal/SKILL.md skills/spec/SKILL.md skills/architecture/SKILL.md skills/plan/SKILL.md`
  - `python scripts/build-skills.py --check`
- Expected observable result: authoring guidance consistently explains RR-to-IR refinement, SR ownership, architecture realization, and proportional allocation while producing only existing artifact types.
- Completion criteria: the shared wording and four authoring integrations agree, focused tests pass, and no new lifecycle or mandatory taxonomy field exists.
- Required evidence: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/evidence/m1-authoring-model.md`
- Review handoff: independent code review of M1 shared-source, authoring-skill, and structure changes.
- Optional commit boundary: `M1: integrate requirement model into authoring`
- Risks:
  - stage guidance may copy the full model into common context or make optional terminology mandatory
- Rollback/recovery:
  - revert the shared source, four copies, and their focused assertions as one unit; do not leave partially mapped consumers

### M2. Integrate traceability judgment into review and verification

- Milestone kind: implementation
- Goal: Make existing review and verification skills traverse the requirement-to-delivery chain at their owned boundaries without changing any decision or settlement authority.
- Requirements: RTD-R11-RTD-R12, RTD-R15, RTD-R20; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001; INT-001, INT-003.
- Architecture decisions: shared vocabulary is explanatory; existing review contracts own findings and authority; deterministic checks do not judge semantic sufficiency.
- Files/components likely touched:
  - `skills/proposal-review/`, `skills/design-review/`, `skills/delivery-review/`, `skills/code-review/`, and `skills/verify/`
  - their existing result or finding assets only when an existing trace field needs clarification
- Dependencies:
  - M1 and its independent code review are closed
- Tests and proof:
  - focused validation for all five mapped review/verification consumers
  - semantic criteria covering RR-to-IR, IR-to-SR/architecture, allocation, implementation fidelity, and reverse evidence trace
  - negative assertions that shared wording grants no stage transition, settlement, or readiness authority
- Implementation steps:
  - add focused failing assertions for the five remaining consumers
  - copy the canonical reference and add exact conditional resource-map entries
  - add concise stage-local traceability criteria without duplicating the shared model
  - preserve precise finding ownership and existing review-result vocabulary
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md skills/design-review/SKILL.md skills/delivery-review/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md`
  - `python scripts/build-skills.py --check`
- Expected observable result: each gate asks the correct traceability question while retaining its existing package, outcome, correction, and settlement contract.
- Completion criteria: all five consumers load the shared reference only when relevant, semantic judgment remains review-owned, and focused validation passes.
- Required evidence: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/evidence/m2-review-traceability.md`
- Review handoff: independent code review of M2 review and verification integration.
- Optional commit boundary: `M2: integrate requirement traceability reviews`
- Risks:
  - explanatory vocabulary may be interpreted as additional approval authority or mandatory review ceremony
- Rollback/recovery:
  - restore the prior stage-local text and remove the five mappings together, preserving M1 only if all surviving package mappings remain coherent

### M3. Enforce shared-resource and publication parity

- Milestone kind: implementation
- Goal: Extend the existing skill-resource validation owner so every selected consumer, generated adapter archive, and clean installation carries the same self-contained model.
- Requirements: RTD-R13-RTD-R14, RTD-R17-RTD-R20; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-002.
- Architecture decisions: existing validator and build pipeline own structural parity; generated output remains derived; historical artifacts remain untouched.
- Files/components likely touched:
  - `scripts/skill_validation.py` and `scripts/test-skill-validator.py`
  - existing build and adapter-distribution tests only where selection of the new mapped resource is not already proved
- Dependencies:
  - M1-M2 and their independent code reviews are closed
- Tests and proof:
  - canonical-to-nine-consumer byte parity and missing/drifted-resource failures
  - unknown mapping or escaped packaged-resource failures through existing owners
  - generated supported adapter archive and clean-install resolution for every mapped consumer
  - unchanged historical lifecycle, release, and artifact surfaces
- Implementation steps:
  - add a failing canonical-copy parity regression under the existing shared-resource validator owner
  - extend existing build/distribution selection only where generic coverage does not exercise the mapped resource
  - generate into temporary output and validate supported adapter archives and clean installs
  - avoid committing generated skill bodies or changing recorded historical release identities
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
- Expected observable result: a missing, drifted, escaped, or mixed model resource fails through existing validation, and every supported installed skill resolves its local copy.
- Completion criteria: canonical, local, generated, and clean-install parity pass for all nine consumers with no new validator CLI or publication mechanism.
- Required evidence: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/evidence/m3-package-parity.md`
- Review handoff: independent code review of M3 validation and complete cross-milestone publication behavior.
- Optional commit boundary: `M3: validate requirement model package parity`
- Risks:
  - generic package tests may pass without selecting all nine consumers or may encourage hand-edited generated output
- Rollback/recovery:
  - correct the canonical source, mapped copies, or existing validator map and rerun temporary generation; never patch derived archives directly

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Complete final holistic review, rationale, verification, and PR handoff after all implementation milestones close.
- Requirements: RTD-AC1-RTD-AC10.
- Architecture decisions: no additional design decision.
- Files/components likely touched:
  - final review evidence, `explain-change.md`, and verification evidence under the owning change root
- Dependencies:
  - M1-M3 and any required review resolution are closed
- Tests and proof:
  - final holistic diff review and every required command from the matching test specification
- Implementation steps:
  - obtain final holistic code review, resolve and rereview findings when required, explain the actual diff, and run final verification
- Validation commands:
  - run every required command from `specs/lightweight-requirement-delivery-model.test.md`
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: the complete implementation and current evidence support truthful PR handoff.
- Completion criteria: final review is clean, rationale and verification are current, and no lifecycle blocker remains.
- Required evidence: final review receipt, closed review resolution when required, explanation, and verification report.
- Review handoff: `verify`, then `pr` only when requested or workflow-authorized.
- Optional commit boundary: `closeout: verify requirement delivery model`
- Risks:
  - a cross-milestone interaction may invalidate earlier focused evidence
- Rollback/recovery:
  - return to the owning milestone, correct and rereview it, then repeat holistic closeout

## Validation plan

- Skill validation owns resource maps, local references, structural assets, closed vocabularies, and canonical-copy parity.
- Build and adapter-distribution validation own generated archive and clean-install projection.
- Formal reviews own whether the model is proportionate, allocation is meaningful, and evidence genuinely traces to the approved direction.
- The matching test specification will map every requirement, boundary, interaction, example, edge case, and acceptance criterion to milestone-local proof.

## Risks and recovery

- Risk: terminology adds context instead of reducing inference. Recovery: keep the shared source concise, load it conditionally, and retain short ordinary stage-local wording.
- Risk: optional hierarchy becomes mandatory ceremony. Recovery: keep small-change and many-to-many examples explicit and reject empty taxonomy fields.
- Risk: shared guidance changes authority. Recovery: retain stage contracts as authoritative and test the absence of new lifecycle or settlement claims.
- Risk: canonical and installed resources drift. Recovery: fail existing parity checks, correct authored sources, and regenerate temporary outputs.

## Dependencies

- Accepted proposal and approved Design package `design-review-r2`.
- Existing skill contract, shared-resource validation, build, adapter archive, and clean-install mechanisms.
- Matching test specification and independent Delivery Review before implementation.
- No new runtime dependency, service, lifecycle field, CLI operation, or publication mechanism.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-30 | Use three implementation milestones plus lifecycle closeout. | Authoring guidance, review semantics, and package parity have distinct implementation and review boundaries. | One broad milestone; one milestone per skill. |
| 2026-08-30 | Integrate authoring consumers before review consumers. | Reviews should judge a coherent authored model, and each milestone remains independently reviewable. | Update all nine consumers in one slice; review consumers first. |
| 2026-08-30 | Extend existing shared-resource and distribution checks. | The approved architecture forbids a new validator or traceability engine. | Add a standalone model validator; rely on semantic review for byte parity. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; test-spec authoring, Delivery Review, implementation, code review, explanation, verification, and PR handoff remain.
