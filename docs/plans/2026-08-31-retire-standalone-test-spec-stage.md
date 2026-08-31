# Execution Plan: Retire the Standalone Test-Spec Stage

## Purpose / big picture

Retire standalone test-specification authoring and review for newly governed changes while preserving pre-implementation verification rigor, historical evidence, and fail-closed lifecycle interpretation. The implementation will introduce the `stage-owned-change-local-v2` contract behind an inactive compatibility boundary, make specification and plan the owners of verification intent, make Delivery Review the joint implementation-and-verification readiness gate, and activate the new route only after canonical sources, lifecycle behavior, validators, documentation, and supported adapter packages agree.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-31-retire-standalone-test-spec-stage.md`
- Specification: `specs/retire-standalone-test-spec-stage.md`
- Architecture: `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md`
- ADR: `docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md`
- Approved Design package: `design-review-r2`
- Legacy-path test specification: pending downstream authoring at `specs/retire-standalone-test-spec-stage.test.md`

## Context and orientation

The governed lifecycle runtime is the Node package under `packages/rigorloop/dist/lib/`. Contract parsing, package composition, stage routing, mutation, status, and new-change scaffolding are exercised under `packages/rigorloop/test/`. Repository-side lifecycle, workflow, review, skill, schema, and adapter enforcement lives under `scripts/`, `schemas/`, and their fixture trees.

Canonical public skills are authored only under `skills/`; generated local mirrors and public adapter archives derive from those sources. Current governance and workflow behavior is expressed in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, skill contracts, templates, and adapter metadata. Historical feature artifacts and settled review evidence are records and are not bulk-rewritten merely because they describe the previous workflow.

This change is self-hosting under `stage-owned-change-local-v1`. It must author and settle its legacy test specification and Delivery Review package before implementation. The implementation then adds v2 without making it the default, proves both classifications, and activates v2 only when every manifest-listed nonterminal prior-contract change has already passed its legacy test-spec and Delivery Review gate. Prior-contract work at implementation or later can then finish through the unchanged downstream stages without retaining the retired authoring entrypoints. The first implementation omits optional in-place migration.

## Non-goals

- Remove test design, automated or manual checks, operational exercises, evidence, Code Review, or Verify.
- Make specification own test mechanics or make milestone sequencing primarily test-driven.
- Require one SR per milestone, verification group, test case, or evidence item.
- Introduce a proof-obligation artifact, replacement verification skill, renamed test-spec stage, per-test lifecycle identity, or semantic traceability engine.
- Merge specification with plan or change existing author/reviewer write boundaries.
- Migrate, rewrite, or delete completed historical test-spec artifacts and review evidence.
- Implement optional in-place v1-to-v2 migration in the first slice.
- Infer a lifecycle contract from dates, artifact presence, stage names, Git reachability, network state, or current repository contents.
- Hand-edit generated adapter skill bodies or treat historical feature specs as current mutable routing state.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| RTS-R20-RTS-R23; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-005 | M1 frozen classification and compatibility foundation |
| RTS-R1, RTS-R2, RTS-R13-RTS-R16, RTS-R18, RTS-R19, RTS-R21-RTS-R24; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-002, INT-004, INT-005 | M2 dual lifecycle and plan-centered Delivery Review authority |
| RTS-R3-RTS-R12, RTS-R14-RTS-R17, RTS-R25; BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-002, INT-003 | M3 authoring, review, and specialist verification methodology |
| RTS-R17-RTS-R20, RTS-R22-RTS-R25; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-001, INT-004 | M4 governance, validator, template, and adapter preactivation parity |
| RTS-R1, RTS-R2, RTS-R17-RTS-R23; all eight boundaries; INT-001-INT-005 | M5 atomic v2 activation and legacy-entrypoint retirement |
| RTS-AC1-RTS-AC13 | Legacy-path test specification, milestone evidence, change-level verification, and M6 closeout |

## Milestones

### M1. Establish frozen contract classification and compatibility

- Milestone kind: implementation
- Goal: Add the schema-validated activation-manifest model and fail-closed contract classifier without changing the default lifecycle of newly created changes.
- Requirements: RTS-R20-RTS-R23, RTS-AC7, RTS-AC8, RTS-AC10, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, INT-001, INT-005.
- Architecture decisions: explicit lifecycle discriminator; frozen manifest eligibility; no heuristic inference; optional migration omitted.
- Files/components likely touched:
  - one tracked activation manifest and its schema under the existing lifecycle contract owners
  - `schemas/change.schema.json`
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`, lifecycle readers, and new-change fixtures
  - `scripts/artifact_lifecycle_contracts.py`, `scripts/change_metadata_semantics.py`, and focused validator fixtures
- Dependencies:
  - approved Design package `design-review-r2`
  - settled legacy test specification and approved Delivery Review package for this change
  - current v1 and legacy-unversioned readers
- Tests and proof:
  - TG-01 classifies explicit v2, manifest-matched v1, and manifest-matched legacy-unversioned records deterministically.
  - TG-02 rejects v1 or unversioned records absent from the manifest, class mismatches, duplicate or unsorted manifest entries, unknown contract values, and v2 records carrying active test-spec state.
  - TG-03 proves dates, current stage, artifact presence, Git state, and network state cannot select a contract.
  - Unknown contract and manifest-class values fail before dependent consistency checks, with named unknown-value regressions.
- Implementation steps:
  - Add failing classifier, schema, ordering, mismatch, and unknown-vocabulary fixtures first.
  - Define the manifest schema and deterministic raw-UTF-8 ordering rules under existing lifecycle validation ownership.
  - Add pure classification shared by runtime readers and repository validators.
  - Keep new-change scaffolding on v1 and keep the manifest preactivation state non-authoritative until M5.
  - Record that no in-place migration operation is implemented; prior records remain on their registered contract.
- Validation commands:
  - `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: Runtime and repository validators can distinguish v2, manifest-bound v1, and manifest-bound legacy records without changing current creation or routing behavior.
- Completion criteria: Classification is deterministic and shared; every changed closed set rejects unknown values first; new changes still scaffold as v1; no migration path or active v2 transition is exposed.
- Required evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m1-contract-classification.md`
- Review handoff: Code Review of schema closure, manifest determinism, compatibility boundaries, and unchanged new-change behavior.
- Optional commit boundary: `M1: add lifecycle contract classification`
- Risks:
  - The manifest could become mutable state or a permissive allowlist.
  - Runtime and Python validators could classify the same record differently.
- Rollback/recovery:
  - Revert the inactive manifest and classifier together; v1 remains the only creation and routing contract.

### M2. Implement the inactive v2 lifecycle and plan-centered package

- Milestone kind: implementation
- Goal: Add the v2 no-test-spec graph, plan-only Delivery Review membership, and exact routing behavior behind the contract discriminator while retaining v1 behavior for manifest-bound records.
- Requirements: RTS-R1, RTS-R2, RTS-R13-RTS-R16, RTS-R18, RTS-R19, RTS-R21-RTS-R24, RTS-AC1, RTS-AC4, RTS-AC7, RTS-AC8, RTS-AC11, BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, INT-001, INT-002, INT-004, INT-005.
- Architecture decisions: v2 `plan -> delivery-review -> implement`; exact primary-plan package; v1 continuity; no manufactured approval.
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`, lifecycle package/read/operation modules, and transaction-aware stage tests
  - `scripts/lifecycle_state_sync.py`, `scripts/workflow_automation.py`, `scripts/workflow_automation_policy.py`, and `scripts/workflow_automation_state.py`
  - `scripts/review_artifact_validation.py`, artifact lifecycle validation, schemas, and fixtures
- Dependencies:
  - accepted M1 implementation and Code Review
  - existing package identity, settlement, correction-route, and lifecycle revision behavior
- Tests and proof:
  - TG-04 proves v2 permits only `design-review -> plan -> delivery-review -> implement`, composes Delivery Review from the exact primary plan and approved Design package, and has no test-spec authoring, review, settlement, or member state.
  - TG-05 proves manifest-bound v1 retains its registered package, stage, status, and downstream route without v2 authority leakage.
  - TG-06 rejects a v2 test-spec artifact, active test-spec stage, test-spec review kind, test-spec package member, removed known value in an active path, mixed v1/v2 package, stale lifecycle revision, and every wholly unknown value before consistency interpretation.
  - TG-07 proves plan corrections return to plan and that settlement alone does not advance workflow.
- Implementation steps:
  - Add a contract-keyed closed stage and package matrix, starting with public-path negative tests.
  - Implement v2 package composition and permissions through existing lifecycle operations rather than a parallel CLI.
  - Make read context and workflow automation expose the active contract, exact plan member, permitted operation, and compatibility blocker.
  - Preserve v1 behavior only for exact manifest-matched records and keep new-change on v1 until M5.
  - Extend existing review and lifecycle validators with contract-aware structural rules; do not make them judge semantic verification adequacy.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-transaction.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-workflow-automation-policy.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-review-artifact-validator.py`
- Expected observable result: Explicit v2 fixtures use one plan-centered readiness gate while exact v1 fixtures continue the old contract; new repositories still default to v1 before activation.
- Completion criteria: Closed graph, package, correction, replay, unknown-value, mixed-contract, and compatibility matrices pass through runtime and repository-owned paths with no v2 default creation.
- Required evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m2-dual-lifecycle.md`
- Review handoff: Code Review of contract-keyed graph closure, package authority, correction ownership, compatibility isolation, and transaction behavior.
- Optional commit boundary: `M2: add inactive plan-centered lifecycle`
- Risks:
  - Read-side permissions and mutation-side checks could select different graphs.
  - Compatibility handling could authorize a newly added legacy artifact.
- Rollback/recovery:
  - Revert v2 routing and package behavior together; retain M1 only if its inactive classifier remains internally consistent.

### M3. Publish specification, plan, and Delivery Review verification ownership

- Milestone kind: implementation
- Goal: Strengthen the three owning skills and their assets, add proportional plan-owned specialist methods, and stage retirement of standalone test-spec entrypoints without activating the new public route.
- Requirements: RTS-R3-RTS-R17, RTS-R25, RTS-AC2-RTS-AC6, RTS-AC9, RTS-AC12, BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001, INT-002, INT-003.
- Architecture decisions: SR behavior remains specification-owned; engineering-led milestones carry verification groups; Delivery Review judges both dimensions; specialist methods use progressive disclosure.
- Files/components likely touched:
  - `skills/spec/` and its specification assets and references
  - `skills/plan/SKILL.md`, `skills/plan/assets/plan-skeleton.md`, milestone assets, and new plan-owned verification references
  - `skills/delivery-review/` and its result/finding resources
  - `skills/workflow/` only for contract-keyed routing and preactivation wording
  - `skills/test-spec/` and `skills/test-spec-review/` retirement inventory, removed only at M5
  - `templates/shared/boundary-first-compact-scan.md` and mapped boundary-first resources where proof ownership changes for v2
- Dependencies:
  - accepted M2 implementation and Code Review
  - existing requirement-to-delivery shared model and skill resource-map rules
- Tests and proof:
  - TG-08 proves specification guidance owns observable normal, invalid, failure, state, authority, compatibility, migration, retry, concurrency, recovery, boundary, scenario, and acceptance behavior when relevant, while excluding implementation test mechanics.
  - TG-09 proves each implementation milestone records engineering purpose, SR and architecture allocation, dependencies, implementation scope, completion criteria, TG-based required verification, and evidence expectations; change-level groups are required when behavior spans milestones or boundaries.
  - TG-10 proves Delivery Review independently evaluates safe sequencing and verification adequacy for the exact plan, rejects substitution by a test-spec attachment, and routes gaps to specification or plan ownership.
  - TG-11 proves ordinary plans load compact inline guidance while risk-triggered plans can conditionally load boundary/negative, state-machine, concurrency/retry, migration/compatibility, failure/recovery, security/authority, cross-milestone integration, and manual/operational evidence methods.
  - TG-12 proves TG IDs remain plan-local trace identities and do not create lifecycle state, mandatory per-test identities, or a replacement artifact or skill.
- Implementation steps:
  - Add failing skill and asset assertions for ownership, required plan fields, conditional loading, review criteria, and forbidden replacement surfaces.
  - Strengthen specification prompts and examples without adding filenames, frameworks, fixtures, mocks, or commands to SR ownership.
  - Extend plan skeleton and milestone structure, then add the smallest coherent set of specialist references covering all approved method families.
  - Update Delivery Review inputs, method, findings, and outputs to the plan-only package while retaining reviewer independence and exact settlement behavior.
  - Stage contract-aware workflow text so v1 remains executable until M5 and v2 guidance cannot be selected before activation.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/spec/SKILL.md skills/plan/SKILL.md skills/delivery-review/SKILL.md skills/workflow/SKILL.md`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: Canonical owning skills fully express the no-test-spec verification contract, and complex methods are available proportionally, while the active default workflow remains v1 pending parity and activation.
- Completion criteria: Skill and asset tests prove authority separation, complete milestone and change-level verification structure, conditional specialist coverage, and no substitute artifact or lifecycle identity.
- Required evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m3-verification-ownership.md`
- Review handoff: Code Review of published authority, plan usability, verification-method completeness, reviewer independence, and progressive disclosure.
- Optional commit boundary: `M3: colocate verification ownership`
- Risks:
  - Plan structure could become a renamed test specification or let verification reshape safe engineering order.
  - Specialist resources could all load by default and erase the intended context reduction.
- Rollback/recovery:
  - Restore the prior owning-skill assets and mappings as one unit; do not leave partial authority language across specification, plan, and Delivery Review.

### M4. Assemble governance, validation, and adapter parity before activation

- Milestone kind: implementation
- Goal: Make every canonical governance, template, validator, example, generator, and supported adapter surface capable of publishing one coherent v2 contract, while retaining v1 as the active default until cutover.
- Requirements: RTS-R17-RTS-R20, RTS-R22-RTS-R25, RTS-AC6-RTS-AC10, RTS-AC12, RTS-AC13, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001, INT-001, INT-004.
- Architecture decisions: coherent publication boundary; generated output derives from `skills/`; semantic adequacy remains review-owned.
- Files/components likely touched:
  - `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and current governing workflow/specification surfaces
  - current templates and examples that prescribe lifecycle routing or delivery-package shape
  - `scripts/skill_validation.py`, lifecycle/review validators, selector coverage, and their fixtures
  - `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, adapter generation/validation tests, and temporary release output
- Dependencies:
  - accepted M3 implementation and Code Review
  - stable v2 runtime behavior and final canonical skill resource map
- Tests and proof:
  - TG-13 inventories active normative references and proves they agree on spec behavior ownership, plan verification allocation, plan-only Delivery Review, unchanged downstream gates, and historical compatibility.
  - TG-14 proves every changed closed vocabulary rejects unknown values before consistency checks and retains known legacy values only in manifest-bound contexts.
  - TG-15 proves generated Codex, Claude Code, and opencode packages resolve every plan-owned specialist resource, expose no active standalone test-spec entrypoint in the staged v2 inventory, and contain no escaped canonical paths or mixed routing.
  - TG-16 proves historical artifacts, release archives, and review evidence remain untouched and readable; active examples and templates create no new test-spec artifact.
- Implementation steps:
  - Produce an explicit current-surface removal inventory, separating normative active content from immutable historical records.
  - Update governing workflow specs, documentation, templates, and examples with preactivation-safe language and contract-keyed fixtures.
  - Extend existing validators and selection logic rather than adding a semantic verifier or new validation CLI.
  - Stage adapter descriptors and generate only temporary archives for v2 parity, drift, clean-install, and resource-resolution proof.
  - Add the activation prerequisite that every manifest-listed nonterminal prior-contract change is at implementation or later with a settled legacy Delivery Review package.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
- Expected observable result: A complete v2 release candidate can be generated and validated without mixed ownership, while released/default behavior remains v1 and historical artifacts remain unchanged.
- Completion criteria: Normative-surface inventory is closed; unknown-value, historical, mixed-package, generated-resource, and supported-adapter tests pass; activation prerequisite is executable and reports exact blocking change IDs.
- Required evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m4-preactivation-parity.md`
- Review handoff: Code Review of normative-versus-historical scope, validator ownership, fail-closed ordering, adapter parity, and activation prerequisites.
- Optional commit boundary: `M4: stage no-test-spec publication parity`
- Risks:
  - Historical documents could be rewritten unnecessarily or active guidance could remain hidden in an overlooked template.
  - Temporary generated output could be mistaken for tracked authored source.
- Rollback/recovery:
  - Revert staged governance, validator, and adapter descriptors together and regenerate temporary output from restored canonical sources.

### M5. Activate v2 atomically and retire standalone entrypoints

- Milestone kind: implementation
- Goal: Freeze the pre-activation inventory, switch new-change scaffolding and active routing to v2, remove standalone test-spec entrypoints from current packages, and prove the complete release boundary in one reviewed slice.
- Requirements: RTS-R1, RTS-R2, RTS-R17-RTS-R23, RTS-AC1, RTS-AC4, RTS-AC7-RTS-AC11, RTS-AC13, all eight boundary IDs, INT-001-INT-005.
- Architecture decisions: coherent activation; exact manifest-bound compatibility; rollback only before the first v2 record; forward recovery afterward.
- Files/components likely touched:
  - frozen activation manifest and activation metadata
  - `packages/rigorloop/dist/lib/new-change.js` and active graph/package selectors
  - canonical `skills/test-spec/` and `skills/test-spec-review/` entrypoints and current skill inventory
  - adapter manifest/release metadata and integrated activation fixtures
- Dependencies:
  - accepted M1-M4 implementation slices and Code Reviews
  - every pre-activation governed change inventoried exactly as v1 or legacy-unversioned
  - every nonterminal prior-contract change at implementation or later with settled legacy Delivery Review authority; otherwise activation blocks
  - reproducible staged adapter parity and no unresolved material findings
- Tests and proof:
  - TG-17 proves a newly scaffolded v2 change reaches plan-centered Delivery Review and implementation without creating, registering, reviewing, settling, or packaging test-spec.
  - TG-18 proves manifest-bound historical and post-Delivery-Review v1 records remain readable and can continue through unchanged downstream stages without active test-spec entrypoints.
  - TG-19 proves a pre-Delivery-Review prior-contract record blocks activation with its exact change ID; a missing, extra, reordered, duplicated, or class-mismatched manifest entry blocks.
  - TG-20 proves current skill inventories and supported adapter archives omit standalone test-spec and test-spec-review entrypoints, include plan specialist resources, and reject mixed old/new packages.
  - TG-21 proves pre-first-v2 rollback restores the last complete v1 package and that a recorded v2 change makes silent default rollback invalid, requiring forward compatibility correction.
- Implementation steps:
  - Run the activation prerequisite without mutating released behavior and stop on any inventory, review, validation, or generated-package gap.
  - Freeze the sorted manifest against the reviewed activation baseline and validate every entry and class.
  - In one slice, switch new-change to v2, select the v2 active graph and package, remove standalone skill entrypoints and active old vocabulary, and publish matching adapter metadata.
  - Run new-v2, post-gate-v1 continuation, historical read, mixed-package rejection, rollback-boundary, and clean-install adapter scenarios through public paths.
  - Record the activation revision and first-v2-record boundary needed to explain recovery behavior; do not rewrite historical records.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-lifecycle-cli-conformance.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: New governed work uses specification, plan, and one plan-centered Delivery Review; prior exact records remain intelligible; standalone test-spec entrypoints are absent from every supported current package.
- Completion criteria: Frozen inventory, v2 public flow, v1 post-gate continuation, historical interpretation, entrypoint retirement, unknown/mixed rejection, generated parity, and rollback-boundary proof pass at one reviewed revision.
- Required evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m5-v2-activation.md`
- Review handoff: Final implementation-milestone Code Review of activation atomicity, exact compatibility, active removal, generated parity, and cross-milestone interactions.
- Optional commit boundary: `M5: activate plan-centered verification workflow`
- Risks:
  - Activation could strand a prior change that still needs legacy authoring or publish one mixed adapter.
  - A rollback after v2 use could silently impose invalid legacy obligations.
- Rollback/recovery:
  - Before any v2 change record exists, restore the last complete v1 graph, skills, and generated packages together. After a v2 record exists, keep its contract valid and ship a forward compatible correction; do not silently return to v1-by-default.

### M6. Complete lifecycle closeout evidence

- Milestone kind: lifecycle-closeout
- Goal: Assemble cross-milestone rationale, final review, and verification evidence after all implementation milestones close.
- Requirements: RTS-R24, RTS-R25, RTS-AC1-RTS-AC13.
- Architecture decisions: unchanged downstream Code Review, Explain Change, Verify, and PR responsibilities.
- Files/components likely touched:
  - `docs/changes/2026-08-31-retire-standalone-test-spec-stage/explain-change.md`
  - conditional review-resolution, CI-maintenance, and verification evidence under the owning change root
- Dependencies:
  - M1-M5 implementation milestones closed with required Code Review evidence
  - every required verification group and change-level group from the approved legacy-path test specification has current evidence
- Tests and proof:
  - TG-FINAL-01 traverses SR to milestone to TG to concrete checks and evidence for the complete new v2 workflow.
  - TG-FINAL-02 proves historical and post-gate prior-contract behavior without mutation or active-vocabulary leakage.
  - TG-FINAL-03 proves activation, mixed-version rejection, supported-package parity, and recovery boundaries across M1-M5.
  - TG-FINAL-04 proves the actual diff matches approved authority and that Code Review and Verify retain their original responsibilities.
- Implementation steps:
  - Resolve or disposition every material implementation-review finding through its owning stage.
  - Produce durable change rationale from the actual final diff and exact artifact and evidence identities.
  - Run final holistic Code Review when cross-milestone interactions are not fully covered by milestone reviews.
  - Run Verify against current canonical, runtime, historical, generated, and review evidence; prepare PR handoff only after readiness passes.
- Validation commands:
  - run every required command from `specs/retire-standalone-test-spec-stage.test.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-31-retire-standalone-test-spec-stage`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: Current evidence demonstrates the no-test-spec workflow, exact legacy compatibility, and coherent package publication without unresolved findings or stale authority.
- Completion criteria: All implementation reviews are closed, explanation and verification are current, complete-change groups pass, and no lifecycle-closeout work is hidden in an implementation milestone.
- Required evidence: final holistic review receipt when required, closed review resolution when triggered, explain-change artifact, conditional CI evidence, and Verify receipt or report.
- Review handoff: `explain-change`, then `verify`, then `pr` under their unchanged owners.
- Optional commit boundary: `closeout: verify test-spec retirement`
- Risks:
  - Focused milestone proof may miss a contract interaction or stale generated projection.
- Rollback/recovery:
  - Keep closeout not-ready, return the gap to its owning milestone or stage, and rerun only the invalidated review and proof chain.

## Change-level verification

### TG-FINAL-01 — New v2 delivery lifecycle

- Covers: RTS-R1-RTS-R19, RTS-R24, RTS-R25; M2-M5.
- Demonstrate:
  - a newly scaffolded change uses v2 and progresses from approved Design Review through plan, plan-centered Delivery Review, implementation authorization, concrete tests/checks, evidence, Code Review, and Verify without a test-spec artifact or stage;
  - SR, architecture responsibility, milestone, TG, concrete proof, and evidence trace in both directions;
  - milestone completion does not substitute for required complete-change verification.

### TG-FINAL-02 — Prior-contract and historical compatibility

- Covers: RTS-R20-RTS-R23; M1, M2, M4, M5.
- Demonstrate:
  - manifest-matched completed records remain readable and unchanged;
  - a manifest-matched nonterminal v1 record already past Delivery Review continues through common downstream stages;
  - pre-gate prior-contract work blocks activation, and removed or unknown active values never obtain authority.

### TG-FINAL-03 — Coherent activation, publication, and recovery

- Covers: RTS-R17-RTS-R23, RTS-AC6-RTS-AC11, RTS-AC13; M1-M5.
- Demonstrate:
  - canonical skills, mapped resources, lifecycle runtime, schemas, validators, workflow guidance, templates, generated adapters, and release metadata express one contract;
  - partial, mixed, drifted, escaped, unknown, and class-mismatched surfaces fail before publication;
  - rollback is coherent before first v2 use and forward-only afterward.

### TG-FINAL-04 — Preserved downstream assurance and authority

- Covers: RTS-R13-RTS-R16, RTS-R24, RTS-R25; M2-M6.
- Demonstrate:
  - Delivery Review alone grants pre-implementation readiness for the exact plan-centered package;
  - Implementation chooses concrete test mechanics and produces evidence;
  - Code Review judges the actual diff and Verify judges complete current evidence without becoming substitutes for pre-implementation planning.

## Validation plan

- Lifecycle Node tests own public request, stage, package, transaction, read-context, replay, and new-change behavior for both explicit contracts.
- Repository Python tests own schema, manifest, workflow automation, review evidence, artifact lifecycle, closed-vocabulary, selection, and compatibility fixtures.
- Skill validation owns resource maps, stage authority, conditional loading, required plan structure, retired entrypoint inventory, and published claim boundaries.
- Build and adapter-distribution checks own canonical-to-generated projection, supported archive inventory, clean-install resolution, portability, and drift.
- Delivery Review and later semantic reviews own whether verification groups, scenarios, engineering sequence, and evidence are actually sufficient; structural validators do not claim that judgment.
- Focused milestone commands run first. `npm test --prefix packages/rigorloop` and `bash scripts/ci.sh --mode broad-smoke` provide integrated proof at activation and closeout.

## Risks and recovery

- Risk: plan grows into a second test-spec artifact. Recovery: keep TGs as milestone-attached objectives, keep mechanics implementation-owned, and reject a separate mandatory hierarchy.
- Risk: historical compatibility reopens removed active vocabulary. Recovery: require exact manifest membership and contract class, separate active and historical paths, and fail unknown values before consistency.
- Risk: a prior change is stranded at activation. Recovery: block activation until every nonterminal prior-contract change has settled Delivery Review and reached implementation or later; do not activate on an incomplete inventory.
- Risk: skill, validator, docs, runtime, or adapter surfaces disagree. Recovery: stage v2 behind the inactive discriminator, require M4 parity, and make M5 one reviewed activation slice.
- Risk: specialist methodology increases ordinary context. Recovery: keep basic guidance inline and validate risk-triggered conditional resource maps.
- Risk: rollback invalidates created v2 records. Recovery: allow whole-package rollback only before first v2 record and use forward compatible correction afterward.

## Dependencies

- Accepted proposal and approved Design package `design-review-r2`.
- This change's legacy-path test specification and one exact legacy Delivery Review package must be settled before M1 implementation.
- M1 contract classification precedes v2 lifecycle state; M2 runtime behavior precedes public authority claims; M3 canonical skills precede adapter and governance parity; M4 complete parity precedes M5 activation.
- Each implementation milestone receives focused tests and independent Code Review before its dependent milestone begins.
- M5 activation blocks if any manifest-listed nonterminal prior-contract change is earlier than implementation or lacks settled Delivery Review authority.
- Optional v1-to-v2 migration is omitted. Any later migration capability requires its own approved design and identity-bound proof.
- Generated skill bodies and adapter archives are derived and never hand-edited.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-31 | Build v2 behind an inactive discriminator and activate only after parity. | Every checked implementation slice remains serviceable, and public routing cannot outrun runtime or package support. | Immediate default switch; mixed incremental publication. |
| 2026-08-31 | Omit in-place v1-to-v2 migration from the first implementation. | Exact migration is optional in the approved design and would expand lifecycle risk without being needed for this cutover. | Automatic migration; heuristic conversion; a new migration stage. |
| 2026-08-31 | Block activation until all nonterminal prior-contract changes have passed legacy Delivery Review. | Retired authoring entrypoints are then unnecessary for continuation, while v1 work can finish through unchanged downstream stages. | Keep a hidden standalone test-spec skill; strand pre-gate work; rewrite prior plans. |
| 2026-08-31 | Use plan-local TG identities and four change-level groups. | This provides reviewable traceability and integrated proof without another governed artifact or per-test identity scheme. | One TG per test; a proof-obligation hierarchy; milestone-only proof. |
| 2026-08-31 | Separate semantic adequacy from deterministic validation. | Delivery Review must judge whether verification is sufficient; validators can only enforce structure, vocabulary, identity, and parity. | Semantic inference engine; structural checks that claim readiness. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. The legacy-path test specification and Delivery Review remain mandatory before implementation begins.
