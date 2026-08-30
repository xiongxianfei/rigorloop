# Lightweight Requirement-to-Delivery Model Specification

## Owning change record

`docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml`

## Related proposal

[Introduce a Lightweight Requirement-to-Delivery Model](../docs/proposals/2026-08-30-lightweight-requirement-delivery-model.md)

## Goal and context

RigorLoop must explain how an incoming need becomes an approved direction, system requirements, architecture realization, allocated work, implementation, and evidence without introducing a parallel requirements-management lifecycle. The contract defines a lightweight requirement-refinement model, keeps work decomposition separate and proportional, and makes existing artifact responsibilities easier to trace.

The observable product surface is the guidance, templates, examples, and review criteria shipped through RigorLoop's supported skill packages. Existing lifecycle stages and artifacts remain authoritative.

## Glossary

- **RR — Raw Requirement:** The incoming need before RigorLoop clarification, normally represented by the existing issue, prompt, report, or referenced source.
- **IR — Initial Requirement:** The accepted proposal-level clarification of the challenge, goals, scope, principle, direction, feasibility, and material impact.
- **SR — System Requirement:** A stable, observable, testable requirement owned by the specification.
- **AR — Allocated Requirement:** The conceptual assignment of an SR to a realization boundary or delivery work package; it is not a mandatory persisted entity.
- **Requirement refinement:** The conceptual `RR → IR → SR → AR` relationship.
- **Work decomposition:** Optional structuring of effort into Epic, Feature, Story, Task, Milestone, or Subtask levels.
- **Realization:** Architecture's explanation of how technical boundaries can satisfy SRs.
- **Allocation:** Planning's assignment of SR and architecture responsibilities to executable work.

## Examples first

Example E1: Small change avoids empty hierarchy
Given one accepted proposal and two system requirements
When Delivery prepares one implementation milestone with two tasks
Then RigorLoop does not require separate RR, IR, AR, Epic, Feature, or Story records

Example E2: Requirement explains delivery work
Given `SR-08` requires rejected mutations to preserve governed state
And architecture assigns validation before mutation commit
When a plan defines milestone `M2` for lifecycle mutation guards
Then the milestone cites `SR-08` and the relevant architecture boundary as its reason for existing

Example E3: Requirement and work hierarchies remain many-to-many
Given `SR-01` and `SR-02` are realized by Story A
And `SR-02` is also realized by Story B
When plan traceability is reviewed
Then both mappings are valid without forcing one SR per Story or one Story per SR

Example E4: Shared vocabulary does not grant authority
Given a shared model describes Design Review as checking `IR → SR ↔ Architecture`
When a design package is reviewed
Then the existing Design Review contract still owns package membership, findings, outcome, and settlement

Example E5: Mixed published package is rejected
Given a consuming skill maps the requirement-to-delivery reference
When its packaged reference is missing or differs from the canonical shared source
Then existing skill-package validation fails before publication

## Requirements

| ID | Requirement |
| --- | --- |
| RTD-R1 | RigorLoop MUST define requirement refinement as `RR → IR → SR → AR` and MUST define work decomposition as a separate `Epic → Feature → Story → Task` view. |
| RTD-R2 | An existing incoming issue, prompt, report, idea, or referenced source MUST be sufficient to represent RR; RigorLoop MUST NOT require a separate RR artifact or RR identifier. |
| RTD-R3 | The accepted proposal MUST serve as the durable IR-level clarification; RigorLoop MUST NOT require a separate IR artifact or identifier. |
| RTD-R4 | The specification MUST own SR-level behavior, and SR identities MUST remain the primary durable requirement references used by architecture, planning, review, implementation evidence, and verification. |
| RTD-R5 | Architecture MUST describe realization of SRs within technical constraints and MUST NOT be presented as another requirement-refinement level. |
| RTD-R6 | Planning MUST be the primary allocation surface that connects SRs and architecture boundaries to executable work; AR MUST remain conceptual in the first slice and MUST NOT require a separate entity or identifier. |
| RTD-R7 | Requirement refinement and work decomposition MUST remain distinct and MUST permit many-to-many mappings between SRs and milestones, stories, or tasks. |
| RTD-R8 | Epic, Feature, Story, Task, Milestone, and Subtask levels MUST be optional and proportional; a change MUST NOT add an otherwise unnecessary level merely to complete the taxonomy. |
| RTD-R9 | Each delivery milestone or equivalent work package MUST be able to identify why it exists, which SRs it realizes, which architecture boundary it affects, its dependencies, and the work included within it. |
| RTD-R10 | Every important SR MUST be able to identify its architecture realization and allocated delivery work, while every lower-level work item MUST be able to trace to an SR or an explicitly justified non-requirement obligation. |
| RTD-R11 | Proposal Review MUST interpret its existing direction decision as RR-to-IR refinement; Design Review MUST interpret its existing package decision as `IR → SR ↔ Architecture` coherence; Delivery Review MUST interpret its existing decision as allocation and delivery coherence; Code Review MUST trace implementation to allocated work and governing SRs; Verify MUST trace evidence backward to implementation, SRs, and the accepted proposal. |
| RTD-R12 | The conceptual model MUST NOT change review-gate order, package membership, settlement authority, correction ownership, or approval meaning. |
| RTD-R13 | The first slice MUST express the model through a canonical shared reference, selected skill-local guidance, applicable templates, bounded examples, review criteria, and supported adapter packages. |
| RTD-R14 | Stage skills MUST expose only terminology relevant to their responsibility and MUST load the complete shared model only under an explicit resource-map condition. |
| RTD-R15 | The shared model MUST NOT own stage transitions, artifact placement, lifecycle mutation, settlement, readiness claims, or stage-specific stop conditions. |
| RTD-R16 | The first slice MUST NOT add RR, IR, or AR lifecycle state; mandatory Epic, Feature, Story, or Task records; a requirements database; external tracker integration; or machine-readable traceability state. |
| RTD-R17 | The first slice MUST NOT remove test-spec, redistribute proof-design responsibility, or change Delivery Review authority. |
| RTD-R18 | Canonical shared text, mapped skill-local references, generated supported adapter packages, and clean installed skill trees MUST remain consistent through existing package and parity validation. |
| RTD-R19 | Historical settled artifacts MUST remain valid without retrofitted RR, IR, or AR labels. New or substantively revised guidance after activation MUST use the new model coherently. |
| RTD-R20 | Deterministic validation MAY check structure, mapped-resource presence, copied-source parity, generated-package parity, and stable identifiers; semantic adequacy of refinement, realization, allocation, and evidence closure MUST remain review-owned. |

## Inputs and outputs

Inputs are an incoming need, an accepted proposal and Proposal Review identity, specification requirements, architecture boundaries, planning work packages, implementation evidence, and the existing review and verification artifacts relevant to the current stage.

Outputs remain the existing artifacts. The model adds explanatory relationships and traceability references; it does not add a required RR, IR, or AR file, database row, lifecycle entry, or CLI response.

Published skill output may use the terms RR, IR, SR, and AR only as defined here. Where ordinary wording is clearer, a skill may say raw need, approved direction, system requirement, realization, or allocation without emitting acronyms solely for completeness.

## State and invariants

- Existing lifecycle state remains solely in the current owning change record.
- Proposal acceptance remains the only governed event that establishes the IR-level direction.
- Design Review remains the only gate that grants authority to the architecture/specification package.
- Delivery Review remains the only gate that grants implementation authority to the plan/test-specification package.
- SR identities remain stable across approved downstream references unless specification ownership explicitly revises them.
- RR, IR, and AR add no independent lifecycle, settlement, freshness, or retry state.
- Omitted optional hierarchy levels are valid and do not represent missing artifacts.

## Error and boundary behavior

- If a raw need is unavailable or cannot be responsibly reconstructed, Proposal Review blocks direction approval rather than inventing RR content.
- If a proposed SR cannot be traced to the accepted direction, Design Review routes the gap to specification or proposal ownership according to whether behavior or direction is wrong.
- If architecture cannot realize an SR, Design Review withholds package authority and names the owning artifact or cross-artifact inconsistency.
- If delivery work lacks SR or architecture rationale, Delivery Review withholds implementation authority and routes the allocation gap to planning ownership.
- If a lower-level work item is justified by migration, maintenance, validation, documentation, or another non-SR obligation, the plan must state that obligation explicitly rather than create a false SR.
- If a mapped shared reference is missing or drifted, existing package validation fails closed before publication.
- If model terminology conflicts with an owning stage contract, the governing spec and owning stage contract win; the package must be corrected before reliance.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: RTD-R1, RTD-R2, RTD-R3, RTD-R4, RTD-R5, RTD-R6, RTD-R7, RTD-R8, RTD-R9, RTD-R10, RTD-R11, RTD-R12, RTD-R13, RTD-R14, RTD-R15, RTD-R16, RTD-R17, RTD-R18, RTD-R19, RTD-R20

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | RTD-R2, RTD-R3, RTD-R4, RTD-R9, RTD-R10 | BND-INPUT-001 | - |
| state-lifecycle | not-applicable | - | - | RTD-R12 and RTD-R16 forbid new model-owned lifecycle state; existing lifecycle behavior is unchanged. |
| identity-authority | applicable | RTD-R3, RTD-R4, RTD-R5, RTD-R6, RTD-R11, RTD-R12, RTD-R15 | BND-AUTH-001 | - |
| composition-path | applicable | RTD-R10, RTD-R11, RTD-R13, RTD-R14, RTD-R15, RTD-R18 | BND-COMPOSE-001 | - |
| temporal-retry | not-applicable | - | - | The model introduces no operation, transaction, retry, replay, or concurrency behavior. |
| failure-recovery | applicable | RTD-R10, RTD-R18, RTD-R20 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | RTD-R12, RTD-R16, RTD-R17, RTD-R18, RTD-R19 | BND-COMPAT-001 | - |
| external-environment | applicable | RTD-R13, RTD-R14, RTD-R18 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | RTD-R2, RTD-R3, RTD-R4, RTD-R9, RTD-R10 | raw need present or unavailable; accepted direction present or unsettled; SR mapped, unmapped, or falsely inferred; work rationale SR-backed or explicitly non-SR | The model never invents missing intent, requirements, or false traceability. | Valid inputs refine or allocate through existing artifacts; missing or contradictory inputs stop at the owning review boundary. | RTD-R10 |
| BND-AUTH-001 | identity-authority | RTD-R3, RTD-R4, RTD-R5, RTD-R6, RTD-R11, RTD-R12, RTD-R15 | proposal direction, SR identity, architecture realization, plan allocation, shared terminology | Existing artifact and review owners retain authority; SR is the durable downstream requirement identity; shared text grants no authority. | Correct ownership permits normal review; ownership conflicts or unauthorized model claims block reliance. | RTD-R12 |
| BND-COMPOSE-001 | composition-path | RTD-R10, RTD-R11, RTD-R13, RTD-R14, RTD-R15, RTD-R18 | canonical shared source, skill-local reference, stage-local instruction, generated package, installed skill, artifact trace | Every consumer applies one coherent model while retaining stage-local semantics and conditional loading. | Coherent composition supports forward and reverse traceability; missing or contradictory composition fails package validation or semantic review. | RTD-R13 |
| BND-RECOVERY-001 | failure-recovery | RTD-R10, RTD-R18, RTD-R20 | semantic trace gap; missing mapped resource; copied-source drift; generated or installed drift | Deterministic tooling repairs no semantic content; owning author or reviewer resolves semantic gaps. | Structural drift fails closed and is regenerated or recopied; semantic gaps route to the owning stage and require rereview when governed members change. | RTD-R20 |
| BND-COMPAT-001 | compatibility-migration | RTD-R12, RTD-R16, RTD-R17, RTD-R18, RTD-R19 | historical artifact, new artifact, substantively revised guidance, coherent package, mixed package | Historical artifacts need no retrofit; activated published surfaces must agree; existing review and test-spec authority remains unchanged. | History remains readable; new work uses the model; mixed activation blocks publication. | RTD-R19 |
| BND-ENV-001 | external-environment | RTD-R13, RTD-R14, RTD-R18 | canonical repository, generated adapter archive, clean target installation, customer repository without RigorLoop internals | Published references are self-contained within each installed skill root and do not require canonical repository paths. | Supported clean installs resolve mapped references; missing or escaped resources fail package validation. | RTD-R18 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | RTD-R11, RTD-R12, RTD-R15 | BND-AUTH-001, BND-COMPOSE-001 | Shared terminology is interpreted as new stage authority or changed review semantics. | Stage contracts retain authority, and the shared model remains explanatory only. |
| INT-002 | RTD-R13, RTD-R18, RTD-R19 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | Canonical skills, generated adapters, and installed targets expose different models during activation. | Existing parity checks fail mixed publication; supported package surfaces activate coherently while historical artifacts remain valid. |
| INT-003 | RTD-R9, RTD-R10, RTD-R20 | BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001 | Tooling invents an SR or allocation merely to make a traceability check pass. | Semantic gaps route to the owning author or review gate; deterministic tooling reports structure only. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | RTD-R2, RTD-R3, RTD-R6, RTD-R8, RTD-R16 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E2 | illustration | RTD-R4, RTD-R5, RTD-R6, RTD-R9, RTD-R10 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E3 | illustration | RTD-R7, RTD-R10 | BND-INPUT-001 | - | - |
| E4 | illustration | RTD-R11, RTD-R12, RTD-R15 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E5 | illustration | RTD-R13, RTD-R18 | BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | - | - |

## Compatibility and migration

Settled historical proposals, specifications, architecture records, plans, tests, reviews, and verification evidence remain valid without RR, IR, or AR labels. No historical artifact rewrite, document-version marker, compatibility interpreter, or lifecycle migration is required.

Activation must update canonical shared text, selected canonical skills, mapped skill-local resources, affected templates and examples, generated supported adapter packages, and existing parity expectations as one coherent implementation. A mixed published package is invalid.

The change preserves stage order, package membership, review authority, lifecycle schema, CLI operations, test-spec ownership, and existing SR identities. Rollback may revert the new shared source and consumer guidance together while preserving already-authored artifacts as ordinary historical text.

## Observability

Skill and review outputs should make the current relationship visible through existing identifiers and artifact paths: accepted proposal, SR IDs, architecture boundaries, milestone or work-package IDs, implementation evidence, and review or verification records.

Validation diagnostics must identify the exact missing mapped reference, parity mismatch, invalid stable ID, or structural trace field. They must not claim that a semantic allocation or verification chain is adequate.

No new runtime logs, metrics, tracing system, audit database, or CLI response fields are required.

## Security and privacy

The model introduces no authentication, authorization, secret, network, or private-data boundary. Raw requirements may contain sensitive stakeholder context, so published guidance must not require copying unnecessary private input into durable artifacts. Existing repository privacy and secret-handling rules continue to apply.

## Accessibility and UX

The model is text-first and must remain understandable without diagrams. Acronyms must be expanded at first use in the shared reference, and skills should prefer ordinary stage-local wording when the acronym adds no value. Tables and hierarchy diagrams must have equivalent explanatory prose.

## Performance expectations

The shared reference must remain concise enough for conditional loading. Skills must not load it unconditionally merely because it is packaged. Implementation must reuse existing build and parity validation rather than add a repository-wide semantic scan, background index, database, or hosted service.

## Edge cases

EC1. A maintenance milestone exists only to update generated adapter expectations; it may cite an explicit packaging obligation rather than inventing an SR.

EC2. One SR requires changes in two milestones; both allocations are valid and both cite the same SR.

EC3. One milestone realizes three related SRs; a single work package is valid when the plan remains reviewable.

EC4. A small documentation correction needs no Epic, Feature, Story, RR ID, IR ID, or AR ID.

EC5. Architecture reveals that a proposed SR cannot be realized; Design Review routes the contradiction to specification or proposal ownership rather than weakening the requirement silently.

EC6. A historical plan does not use AR terminology; it remains valid and requires no migration.

EC7. A shared reference is present but a skill resource map never loads it; package review treats the unused resource or missing load condition as a design defect rather than relying on its mere presence.

EC8. An installed adapter has the mapped reference but its wording differs from the canonical source; package parity fails before publication.

## Non-goals

- Creating mandatory RR, IR, or AR artifacts or identifiers.
- Requiring every change to use Epic, Feature, Story, and Task.
- Enforcing one-to-one mappings between requirements and work.
- Introducing a requirements database, hosted service, or external tracker integration.
- Adding machine-readable traceability state or new lifecycle schema.
- Removing test-spec or reallocating proof-design ownership.
- Changing review-gate order, package authority, CLI operations, or settlement behavior.
- Retrofitting historical artifacts.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| RTD-AC1 | A new raw need can proceed through proposal, specification, architecture, and planning without any mandatory RR, IR, or AR artifact. |
| RTD-AC2 | Proposal, specification, architecture, and plan guidance consistently describe their RR/IR, SR, realization, and allocation responsibilities. |
| RTD-AC3 | Review guidance checks the appropriate forward or reverse traceability relationship without changing existing review authority. |
| RTD-AC4 | A small-change example omits unnecessary hierarchy, and a larger example demonstrates optional many-to-many decomposition. |
| RTD-AC5 | Plans can cite SRs and architecture boundaries for milestones while permitting explicitly justified non-SR obligations. |
| RTD-AC6 | Shared-source, skill-local, generated-package, and clean-install parity pass for every selected consumer and supported adapter. |
| RTD-AC7 | No new lifecycle field, RR/IR/AR state, CLI operation, database, external integration, or mandatory work entity is introduced. |
| RTD-AC8 | Historical artifacts remain valid without rewrite, and mixed current package surfaces fail before publication. |
| RTD-AC9 | Deterministic checks remain structural while formal review owns semantic sufficiency. |
| RTD-AC10 | Design Review can map every requirement to a compatible architecture responsibility without unresolved contradiction. |

## Open questions

None. Exact consumer wording, template edits, and validation command selection belong to Delivery planning within the approved architecture and this contract.

## Next artifacts

- Design Review of this specification with `docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md`.
- Execution plan and test specification after Design Review approval.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review reconciliation with the architecture. This specification does not authorize delivery planning until the exact design package is approved.
