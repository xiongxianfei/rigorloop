# Retire the Standalone Test-Spec Stage Specification

## Owning change record

`docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Retire the Standalone Test-Spec Stage](../docs/proposals/2026-08-31-retire-standalone-test-spec-stage.md)

## Goal and context

RigorLoop must remove test specification as a mandatory standalone lifecycle artifact and stage without reducing pre-implementation verification rigor. Observable behavior must be owned by stable system requirements, verification responsibility must be allocated with delivery work, and Delivery Review must decide implementation and verification readiness together.

The observable product surface includes canonical skills and references, workflow routing, governed lifecycle state and CLI behavior, review-package membership, templates, validation diagnostics, examples, documentation, and generated packages for supported adapters. This specification supersedes the predecessor model's deliberate first-slice constraint against redistributing proof-design responsibility, but does not otherwise redesign the Lightweight Requirement-to-Delivery Model.

## Glossary

- **System requirement (SR):** A stable, observable, testable behavior owned by the specification and used as the durable downstream requirement reference.
- **Verification group (TG):** A lightweight plan-local identity for one related verification objective and its important scenarios.
- **Milestone verification:** What one allocated implementation milestone must demonstrate before completion.
- **Change-level verification:** What the integrated change must demonstrate when correctness spans milestones or system boundaries.
- **Concrete proof:** An implementation-owned automated test, manual check, analysis, inspection, or operational exercise that demonstrates an approved verification expectation.
- **Active contract:** The lifecycle vocabulary, routing, artifacts, and package rules applied to newly governed changes after activation.
- **Historical compatibility:** Read-only acceptance and interpretation of artifacts and evidence valid under a prior lifecycle contract.
- **Explicit migration:** A workflow-owned, validated transition of an in-flight governed change to the new active contract.

## Examples first

Example E1: Specification owns rejected-transition behavior
Given `SR-12` requires a rejected governed transition not to modify governed state
And its important scenarios include stale revision, unresolved material finding, unauthorized operation, and invalid predecessor state
When delivery planning begins
Then the plan consumes those outcomes without prescribing test filenames, frameworks, fixtures, or mocks in the specification

Example E2: Milestone carries allocated verification
Given milestone `M2` realizes `SR-07` and `SR-12` at the transition boundary
When the plan defines `TG-02 — Rejected mutation preserves state`
Then `TG-02` identifies the rejection scenarios and unchanged-state outcome that M2 must demonstrate before completion

Example E3: Complete-change proof is not inferred from milestone proof
Given separate milestones implement migration, new-state mutation, and compatibility reads
When correctness depends on an old-to-new end-to-end lifecycle
Then the plan includes change-level verification covering migration and the integrated workflow even if each milestone has its own verification

Example E4: Delivery Review rejects incomplete verification planning
Given a plan safely sequences implementation but omits authority and recovery verification required by approved SRs and architecture
When Delivery Review evaluates the package
Then it records a material finding, withholds implementation authority, and routes correction to plan ownership

Example E5: Historical test-spec remains valid but inactive
Given a completed pre-activation change contains an accepted `test-spec.md` and test-spec review evidence
When current tooling reads that historical change
Then the records remain valid and readable without making test-spec an allowed stage or required artifact for a newly governed change

Example E6: Unknown lifecycle value fails closed
Given a new change record contains an unrecognized artifact kind that is neither active nor explicitly historical
When lifecycle validation runs
Then it reports an unknown-value error before attempting package-consistency interpretation

Example E7: In-flight work does not migrate implicitly
Given a governed change registered the prior lifecycle contract before activation
When Workflow resumes it after activation
Then it continues its registered test-spec path unless an explicit migration validates and records the new target state

## Requirements

| ID | Requirement |
| --- | --- |
| RTS-R1 | After activation, a newly governed change MUST NOT require or permit `test-spec` as an active artifact, authoring stage, review stage, settlement state, or Delivery Review package member. |
| RTS-R2 | The normal post-Design delivery route MUST be `plan → delivery-review → implement`; it MUST NOT insert another mandatory verification artifact, proof-obligation stage, or verification authoring skill. |
| RTS-R3 | The specification MUST own stable SR-level observable behavior and MUST express relevant normal behavior, invalid input, failure behavior, state transitions, authority, compatibility, migration, retries, concurrency, recovery, system boundaries, important scenarios, and acceptance conditions sufficiently for downstream verification planning. |
| RTS-R4 | Specification guidance MUST NOT normally prescribe test filenames, test frameworks, fixtures, mocks, exact validation commands, implementation-specific test mechanics, or milestone allocation. |
| RTS-R5 | Architecture MUST identify realization responsibilities and verification-relevant technical boundaries without becoming the owner of concrete verification allocation or mechanics. |
| RTS-R6 | The plan MUST remain primarily a safe engineering and dependency sequence shaped by dependencies, safe intermediate states, migration order, reversibility, integration boundaries, implementation risk, and reviewability. |
| RTS-R7 | Every implementation milestone MUST identify its purpose, governing SRs or explicitly justified non-SR obligations, relevant architecture responsibilities, dependencies, implementation scope, completion criteria, required verification, and evidence expectations. |
| RTS-R8 | Milestone verification MUST state what behavior and important scenarios the milestone must demonstrate, while permitting implementation to choose concrete test and check mechanics within the approved contract. |
| RTS-R9 | A plan MUST include change-level verification whenever end-to-end, cross-milestone, cross-component, compatibility, migration, concurrency, failure-recovery, security, authority, generated-output parity, or other integrated behavior cannot be demonstrated adequately within one milestone. |
| RTS-R10 | Milestone completion MUST NOT by itself imply complete-change correctness; final readiness MUST account for every required change-level verification group and its evidence. |
| RTS-R11 | Plans MUST support the trace `SR → allocated milestone or work → verification group → concrete proof → evidence` without requiring one SR per group, one group per test, or RigorLoop identities for individual test functions. |
| RTS-R12 | `plan` MUST provide compact inline verification guidance and conditionally loaded specialist references for boundary and negative cases, state machines, concurrency and retry, migration and compatibility, failure and recovery, security and authority, cross-milestone integration, and manual or operational evidence. |
| RTS-R13 | Delivery Review MUST approve one exact plan-centered delivery package under one approved Design Review identity and MUST assess implementation readiness and verification adequacy in the same independent decision. |
| RTS-R14 | Delivery Review MUST withhold implementation authority when SR allocation, milestone verification, change-level verification, important normal or negative scenarios, applicable compatibility, migration, recovery, concurrency, security or authority concerns, or realistic evidence expectations are materially insufficient. |
| RTS-R15 | Delivery Review MUST route missing or inadequate verification planning to `plan`; it MUST NOT author the missing plan content, accept a standalone test-spec substitute, or defer material pre-implementation coverage to final Verify. |
| RTS-R16 | Implementation MUST own concrete tests and checks and stage-owned evidence; Code Review and Verify MUST retain their existing downstream responsibilities and MUST NOT become substitutes for pre-implementation verification planning. |
| RTS-R17 | Canonical test-spec and test-spec-review authoring packages MUST be removed from the active published skill inventory, and specialist methodology worth retaining MUST move under the plan skill's progressive-disclosure package. |
| RTS-R18 | Workflow routing, lifecycle schemas and engine behavior, CLI operations, review-package calculation, validators, templates, examples, guidance, and supported adapter output MUST express the same active contract and MUST reject a mixed old/new package before publication or downstream authority. |
| RTS-R19 | Every changed closed vocabulary MUST reject unknown values explicitly before consistency checks, and each newly changed vocabulary MUST have an unknown-value regression test. |
| RTS-R20 | Settled historical test-spec artifacts, review records, and lifecycle evidence MUST remain valid read-only records without rewrite, conversion, or retroactive invalidation. |
| RTS-R21 | A change governed under the prior contract MUST continue its registered lifecycle by default; adoption of the new contract MUST require an explicit workflow-owned migration that validates exact current state, artifact identities, target state, and ambiguity-free compatibility. |
| RTS-R22 | Historical compatibility MUST NOT make test-spec valid for a newly governed change, silently repair active state from historical evidence, or treat unknown values as legacy values. |
| RTS-R23 | Activation and rollback MUST each operate on a complete compatible contract across canonical sources, executable lifecycle behavior, validation, documentation, and generated adapter packages; neither path may partially remove or restore the stage. |
| RTS-R24 | The change MUST preserve existing proposal, architecture, specification, Design Review, implementation, Code Review, Verify, and PR authority boundaries and MUST NOT merge specification and plan. |
| RTS-R25 | Deterministic validation MAY judge structure, known vocabulary, exact package membership, references, stable IDs, resource mapping, identities, compatibility fixtures, and generated parity; semantic adequacy of requirements, sequencing, verification, and evidence MUST remain owned by the applicable formal review. |

## Inputs and outputs

Inputs to the new delivery boundary are an accepted proposal, approved architecture and specification with stable SRs and boundary identities, applicable ADRs, and the Design Review identity authorizing that exact package.

The plan outputs ordered implementation milestones, SR and architecture allocation, milestone completion criteria, verification groups, change-level verification where applicable, validation or evidence expectations, dependencies, and recovery intent. A verification group may cite several SRs and scenarios; concrete implementation may realize one group through several tests or checks.

Delivery Review outputs its existing durable review evidence and package settlement for exactly the approved plan-centered package. Implementation outputs code, concrete tests or checks, and evidence through existing stage-owned surfaces. No test-spec artifact, proof-obligation artifact, replacement lifecycle row, or per-test RigorLoop identity is output for a newly governed change.

## State and invariants

- Specification remains the sole owner of SR behavior; plan and implementation may not redefine an SR outcome.
- Plan remains the sole owner of delivery allocation and pre-implementation verification allocation.
- Delivery Review remains the sole pre-implementation readiness gate and grants no authority until both sequence and verification are adequate.
- A verification group is plan-local stable intent, not mutable lifecycle state or a new governed artifact kind.
- `change.yaml` remains the sole mutable governed-state snapshot for a governed change.
- Active and historical contract interpretation are distinguishable; historical compatibility never expands the active vocabulary.
- In-flight migration is explicit, workflow-owned, identity-bound, and fail-closed.
- Concrete proof and evidence cannot replace missing approved pre-implementation expectations for material behavior.
- Generated packages remain derived from canonical authored sources.

## Error and boundary behavior

- If an SR lacks enough observable behavior to allocate verification responsibly, plan authoring stops and routes the behavior gap to specification ownership.
- If architecture leaves a verification-relevant realization boundary ambiguous, plan authoring stops and routes the gap through the design correction path.
- If a safe engineering milestone cannot be verified independently, the plan states the limitation and allocates the behavior to a later milestone or change-level group; it does not split work solely to manufacture test isolation.
- If required verification spans milestones, omission of change-level coverage is a Delivery Review finding even when all milestones have local checks.
- If a plan uses a test-spec attachment as required package authority, Delivery Review rejects the package and routes the content into the plan.
- If an in-flight prior-contract change lacks enough state or identity evidence for migration, Workflow leaves it on the registered contract and reports the migration blocker.
- If active and historical vocabulary cannot be distinguished, lifecycle interpretation blocks rather than guessing.
- If a canonical skill, mapped resource, generated adapter, schema, validator, or workflow route reflects a different ownership model, validation blocks activation or publication.
- If a removed closed-vocabulary value or a wholly unknown value reaches a current-only path, validation reports the exact invalid value before dependent consistency errors.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: RTS-R1, RTS-R2, RTS-R3, RTS-R4, RTS-R5, RTS-R6, RTS-R7, RTS-R8, RTS-R9, RTS-R10, RTS-R11, RTS-R12, RTS-R13, RTS-R14, RTS-R15, RTS-R16, RTS-R17, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23, RTS-R24, RTS-R25

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | RTS-R3, RTS-R4, RTS-R6, RTS-R7, RTS-R8, RTS-R9, RTS-R10, RTS-R11, RTS-R13, RTS-R14, RTS-R15, RTS-R18 | BND-INPUT-001 | - |
| state-lifecycle | applicable | RTS-R1, RTS-R2, RTS-R13, RTS-R18, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-STATE-001 | - |
| identity-authority | applicable | RTS-R3, RTS-R4, RTS-R5, RTS-R6, RTS-R13, RTS-R14, RTS-R15, RTS-R16, RTS-R18, RTS-R21, RTS-R24, RTS-R25 | BND-AUTH-001 | - |
| composition-path | applicable | RTS-R2, RTS-R11, RTS-R12, RTS-R13, RTS-R15, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | RTS-R3, RTS-R6, RTS-R8, RTS-R9, RTS-R10, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | RTS-R3, RTS-R9, RTS-R14, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | RTS-R1, RTS-R17, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-COMPAT-001 | - |
| external-environment | applicable | RTS-R12, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | RTS-R3, RTS-R4, RTS-R6, RTS-R7, RTS-R8, RTS-R9, RTS-R10, RTS-R11, RTS-R13, RTS-R14, RTS-R15, RTS-R18 | SR behavior sufficient or insufficient; milestone-local or cross-change behavior; verification group present, missing, or falsely substituted; coherent or mixed delivery member set | Requirements own behavior, plans own allocation, and package inputs never invent missing behavior or verification. | Sufficient inputs permit review; missing behavior routes to spec, missing allocation routes to plan, and mixed members are rejected. | RTS-R13 |
| BND-STATE-001 | state-lifecycle | RTS-R1, RTS-R2, RTS-R13, RTS-R18, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | new pre-activation, new post-activation, registered in-flight prior contract, explicitly migrated, completed historical; authoring, review-required, accepted, revision-required, or invalid state | One governed change follows one explicit contract; historical acceptance cannot authorize active test-spec behavior. | New changes use the plan-only route; prior in-flight changes continue or migrate explicitly; completed records remain readable; invalid transitions block. | RTS-R21 |
| BND-AUTH-001 | identity-authority | RTS-R3, RTS-R4, RTS-R5, RTS-R6, RTS-R13, RTS-R14, RTS-R15, RTS-R16, RTS-R18, RTS-R21, RTS-R24, RTS-R25 | specification behavior, architecture realization, plan allocation, Delivery Review verdict, implementation mechanics, Verify evidence closure, Workflow migration | Every decision remains with its named owner; no downstream stage silently repairs an upstream contract. | Authorized actions proceed within their write sets; ownership conflicts withhold authority and route to the owner. | RTS-R24 |
| BND-COMPOSE-001 | composition-path | RTS-R2, RTS-R11, RTS-R12, RTS-R13, RTS-R15, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | canonical skill, mapped reference, template, workflow route, CLI engine, validator, generated adapter, installed package | Every active consumer expresses the same responsibility split and route; specialist guidance is plan-owned and conditional. | Coherent composition publishes the new route; missing, stale, additional, or mixed surfaces fail validation. | RTS-R18 |
| BND-TEMPORAL-001 | temporal-retry | RTS-R3, RTS-R6, RTS-R8, RTS-R9, RTS-R10, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | milestone order, cross-milestone behavior, interrupted activation, resume before or after activation, repeated migration request | Safe engineering order remains primary; complete-change proof is explicit; lifecycle mutation remains identity-bound and idempotent where already recorded. | Ordered work and explicit final groups proceed; interrupted or stale activation and migration stop or reconcile through named lifecycle behavior. | RTS-R10 |
| BND-RECOVERY-001 | failure-recovery | RTS-R3, RTS-R9, RTS-R14, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | missing proof allocation, validator failure, unknown vocabulary, partial generated package, failed migration, rollback | Semantic content is never repaired by validation; unknown values fail first; rollback restores one complete contract without rewriting history. | Gaps route to owners, partial activation blocks, failed migration preserves prior authority, and coherent rollback restores serviceable workflow guidance. | RTS-R23 |
| BND-COMPAT-001 | compatibility-migration | RTS-R1, RTS-R17, RTS-R18, RTS-R19, RTS-R20, RTS-R21, RTS-R22, RTS-R23 | active new record, prior-contract in-flight record, settled historical record, known legacy value in historical context, removed value in active context, unknown value | Compatibility is read-only and contextual; active removal does not invalidate history or admit new legacy artifacts. | Historical evidence remains valid; new test-spec use fails; explicit migration may succeed when exact; ambiguity and unknown values block. | RTS-R22 |
| BND-ENV-001 | external-environment | RTS-R12, RTS-R17, RTS-R18, RTS-R19, RTS-R23 | canonical repository, generated temporary package, release archive, clean supported-adapter installation, customer repository without canonical source paths | Published plan methodology is self-contained under the installed skill root and every adapter derives from canonical sources. | All supported packages expose the same route and references; escaped, missing, transformed without contract, or divergent resources fail package validation. | RTS-R18 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | RTS-R1, RTS-R18, RTS-R20, RTS-R22 | BND-STATE-001, BND-COMPAT-001 | Historical compatibility is implemented by leaving test-spec in the active vocabulary. | Historical records remain readable through a bounded legacy path while new active test-spec state is rejected. |
| INT-002 | RTS-R13, RTS-R15, RTS-R18 | BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | Delivery Review accepts a separate test-spec as compensation for an incomplete plan. | The exact plan owns required verification, and Delivery Review routes inadequate content to plan before granting authority. |
| INT-003 | RTS-R6, RTS-R8, RTS-R9, RTS-R10 | BND-INPUT-001, BND-TEMPORAL-001 | Verification concerns reshape milestones into unsafe or dependency-inverted slices, or milestone checks are mistaken for complete-change proof. | Engineering dependencies determine sequence; verification attaches to those milestones and separate change-level groups close integrated behavior. |
| INT-004 | RTS-R18, RTS-R19, RTS-R23 | BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | A partial implementation publishes old routing with new skills or lets removed and unknown values fall through. | Closed-vocabulary tests and package parity block partial publication; activation or rollback operates on one coherent revision. |
| INT-005 | RTS-R20, RTS-R21, RTS-R22, RTS-R23 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001 | Resume or migration silently changes the authority of an in-flight prior-contract package. | Workflow preserves the registered path unless an exact, validated, identity-bound migration records the new state; failure leaves prior authority intact. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | RTS-R3, RTS-R4 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E2 | illustration | RTS-R7, RTS-R8, RTS-R11 | BND-INPUT-001 | - | - |
| E3 | illustration | RTS-R9, RTS-R10 | BND-INPUT-001, BND-TEMPORAL-001 | - | - |
| E4 | illustration | RTS-R13, RTS-R14, RTS-R15 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E5 | illustration | RTS-R1, RTS-R20, RTS-R22 | BND-STATE-001, BND-COMPAT-001 | - | - |
| E6 | regression | RTS-R19, RTS-R22 | BND-RECOVERY-001, BND-COMPAT-001 | AGENTS-CLOSED-VOCABULARY | - |
| E7 | illustration | RTS-R21 | BND-STATE-001, BND-TEMPORAL-001, BND-COMPAT-001 | - | - |

## Compatibility and migration

Completed historical changes keep their test specifications, review records, and lifecycle evidence unchanged. Tooling may recognize those values only in a bounded historical context and must not convert them into active authority or rewrite them into plan sections.

In-flight changes registered under the prior contract continue the prior stage graph by default. An optional migration is valid only when Workflow owns the operation, the exact lifecycle revision and relevant artifact identities are current, the destination state is unambiguous, required verification content already exists in the plan, and the transition preserves or explicitly invalidates affected review authority. Failed or stale migration leaves the prior state unchanged.

Activation must update canonical sources, lifecycle implementation, validation fixtures, docs, and supported generated adapters as one release-compatible revision. The existing `skills/`-to-generated-package pipeline remains authoritative. Rollback restores the last complete standalone-test-spec package and active graph together; it neither deletes post-activation plans nor rewrites historical records.

The predecessor `RTD-R17` remains historical evidence of the Lightweight Requirement-to-Delivery Model's first-slice scope. This specification intentionally supersedes that constraint for newly governed behavior after activation.

## Observability

Lifecycle context and validation must expose the exact active stage, permitted operation, package membership, artifact identities, stale evidence, unknown value, compatibility classification, or migration blocker needed to explain an outcome. Diagnostics must distinguish a removed active test-spec value, an accepted historical value, and a wholly unknown value.

Plan and review artifacts expose verification through existing Markdown identities: SR IDs, milestone IDs, TG IDs, concrete check references, evidence paths, and review IDs. No new hosted telemetry, audit database, or per-test lifecycle event is required.

## Security and privacy

Authority boundaries are material: only specification may define behavior, only plan may allocate verification, only Delivery Review may grant pre-implementation package authority, and only Workflow may migrate governed stage state. Historical compatibility must not become an authority-escalation or validation-bypass path.

Specialist security and authority verification guidance must remain available to plan authors when applicable. The change introduces no new credential, secret, network, personal-data, or external actor store; existing repository privacy and secret-handling rules continue to apply.

## Accessibility and UX

No interactive UI is introduced. Published guidance must remain usable as text without diagrams, define verification-group terminology on first use, use tables with clear headings, and avoid requiring users to understand internal generator or canonical-source paths. Removing the standalone stage should reduce ordinary workflow choices and context loads.

## Performance expectations

An ordinary change must not load every specialist verification reference or a standalone test-spec skill. Conditional plan resources should make initial planning context smaller than the prior plan-plus-test-spec path. Validation and generation must reuse repository-owned mechanisms and must not add a hosted service, background index, or repository-wide semantic inference engine.

No numeric runtime target is imposed because the change is predominantly authored guidance and bounded lifecycle validation; implementation evidence must report any material regression in existing repository validation or package-generation commands.

## Edge cases

EC1. One milestone realizes several SRs and one verification group demonstrates their shared outcome; this is valid when traceability remains explicit.

EC2. One SR is realized across three milestones; each milestone states its local verification and the plan adds a final group when the integrated SR cannot be proven locally.

EC3. A milestone contains only packaging or documentation work; it may cite an explicit non-SR obligation and suitable structural evidence rather than inventing a behavioral SR.

EC4. A safe migration milestone intentionally leaves a supported intermediate state that is not user-complete; its completion criteria prove that state, while change-level verification proves the final workflow.

EC5. A manual recovery exercise is the only realistic proof for an operational boundary; the plan may require that evidence without forcing an automated test or standalone test-spec.

EC6. A historical review record cites `test-spec-review`; it remains readable when tied to a pre-activation contract but is rejected as a review kind for a new change.

EC7. A user attempts to attach an optional `test-spec.md` to a new Delivery Review package; the content may be relocated to plan, but the artifact is not accepted as package authority.

EC8. A plan mentions a concrete validation command for a known repository check; this is permitted as evidence planning, but the specification remains free of that implementation mechanic.

EC9. A specialist plan reference is present in canonical source but omitted from one generated adapter; package parity fails before release.

EC10. An already-completed change is opened from a fresh checkout; historical interpretation does not require network access, migration, or regeneration of its test-spec artifact.

## Non-goals

- Removing test design, automated tests, manual checks, operational exercises, or evidence.
- Making the specification responsible for implementation-level test mechanics or milestone allocation.
- Making milestone decomposition primarily test-driven.
- Requiring each SR, verification group, or test to map one-to-one.
- Introducing a proof-obligation artifact, verification database, replacement mandatory skill, or renamed test-spec stage.
- Merging specification and plan.
- Changing Code Review or Verify into pre-implementation planning gates.
- Defining every concrete test before implementation.
- Redesigning the Lightweight Requirement-to-Delivery Model beyond this ownership change.
- Rewriting, deleting, or retroactively migrating completed historical test-spec records.
- Selecting exact filenames, reference organization, implementation modules, or validation commands before delivery planning.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| RTS-AC1 | A newly governed change progresses from approved Design Review to plan and one plan-centered Delivery Review without creating or settling a test-spec artifact. |
| RTS-AC2 | Specification guidance and templates make relevant SR behavior, boundaries, failures, and important scenarios explicit without requiring test mechanics. |
| RTS-AC3 | Plan guidance and skeleton require SR and architecture allocation, milestone verification, evidence expectations, and applicable change-level verification while preserving engineering-led sequencing. |
| RTS-AC4 | Delivery Review approves or rejects implementation sequence and verification adequacy in one exact package decision and routes deficiencies to plan. |
| RTS-AC5 | Lightweight TG identities connect SRs and milestones to concrete proof and evidence without creating lifecycle state or per-test identity requirements. |
| RTS-AC6 | Specialist verification methods are available through conditionally loaded plan-owned references, and ordinary planning does not load all specialist content. |
| RTS-AC7 | New lifecycle state and package validation reject test-spec as active, reject unknown vocabulary before consistency checks, and include unknown-value regression coverage for every changed closed set. |
| RTS-AC8 | Completed historical test-spec artifacts and evidence remain valid and readable without mutation, while their vocabulary does not authorize new artifacts. |
| RTS-AC9 | A prior-contract in-flight change resumes its registered route or uses an explicit identity-bound Workflow migration; ambiguous or failed migration preserves prior state and reports a blocker. |
| RTS-AC10 | Canonical skills, references, workflow docs, schemas, CLI behavior, validators, templates, examples, and all supported generated adapters pass coherent-package and mixed-package rejection checks. |
| RTS-AC11 | Rollback can restore the last complete prior contract without rewriting historical records or leaving a mixed stage graph. |
| RTS-AC12 | Proposal, Design Review, Implementation, Code Review, Verify, PR, and stage-owned lifecycle authority remain unchanged except for the approved removal and Delivery Review package adjustment. |
| RTS-AC13 | Design Review can map every requirement to a compatible architecture responsibility and finds no unresolved contradiction with the accepted proposal or ADR. |

## Open questions

None. Exact edited-file inventory, specialist-reference grouping, compatibility-fixture structure, implementation slices, release boundary, and validation commands belong to Delivery planning within the approved design.

## Next artifacts

- Design Review of this specification with `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md` and `docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md`.
- Execution plan and, because this self-hosting change remains governed by the prior contract, its required historical-path test specification after Design Review approval.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review reconciliation with the architecture and ADR. This specification does not authorize delivery planning or implementation until the exact design package is approved.
