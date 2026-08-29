# Execution Plan: Consolidated RigorLoop Review Gates

## Purpose / big picture

Implement consolidated review gates as the single supported workflow after one reviewed release cutover. The implementation keeps proposal, architecture, specification, plan, and test-specification authorship separate; introduces atomic Design Review and Delivery Review package authority; adds embedded proposal feasibility evaluation; preserves downstream Code Review and Verify responsibilities; and retires old progression only after canonical sources, lifecycle behavior, generated adapters, legacy-work inventory, and rollback proof agree.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-28-consolidate-rigorloop-review-gates.md`
- Spec: `specs/consolidated-review-gates.md`
- Architecture: `docs/adr/ADR-20260828-consolidated-review-package-topology.md`
- Test spec: pending downstream authoring

## Context and orientation

The governed lifecycle runtime is the Node package under `packages/rigorloop/dist/lib/`, with request validation in `lifecycle-contract.js`, interpretation and status in `lifecycle-read.js`, semantic mutations in `lifecycle-operations.js`, atomic persistence in `lifecycle-transaction.js`, new-change creation in `new-change.js`, and regression tests under `packages/rigorloop/test/`. Repository-side lifecycle, workflow, review-record, skill, and adapter enforcement lives under `scripts/`, `schemas/`, and their fixture trees.

Canonical public skills are authored only under `skills/`. Generated local mirrors and public adapter archives derive from those sources through `scripts/build-skills.py` and `scripts/build-adapters.py`; generated public skill bodies are not tracked source. Workflow and governance explanations span `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/rigorloop-workflow.md`, with the consolidated-gates spec taking precedence for behavior changed at cutover.

The implementation must preserve one mutable state owner in each change-local `change.yaml`, one existing lifecycle CLI command family, stage-owned artifact editing, review/author separation, and workflow-owned routing. The current partially implemented `advance-stage` operation is treated as unfinished work inside M3: it must be brought into full consolidated-graph conformance rather than accepted as a separate or already-complete milestone.

## Non-goals

- Do not merge architecture with specification or plan with test specification.
- Do not add combined design-authoring or delivery-authoring skills.
- Do not create a standalone feasibility artifact, skill, state, or review gate.
- Do not migrate active legacy changes in place or infer package approval from old individual reviews.
- Do not introduce cross-change canonical revision ownership, automatic path succession, a generic lifecycle status setter, a new top-level CLI family, external services, or new production dependencies.
- Do not remove milestone Code Review, final holistic Code Review when required, review-resolution, `explain-change`, Verify, or PR preparation.
- Do not cut over before legacy-dependent work is closed and generated-output parity and rollback proof are current.

## Requirements covered

- CRG-R1 through CRG-R6: M1 establishes the single-cutover contract; M3 enforces the consolidated progression graph; M4 establishes and retires the public review entrypoints.
- CRG-R7 through CRG-R11: M4 adds and evaluates embedded proposal feasibility without a separate artifact or gate.
- CRG-R12 through CRG-R21: M2 implements exact design and delivery package composition and atomic authority; M4 supplies the independent review responsibilities.
- CRG-R22 through CRG-R28: M2 implements aggregate identity, read context, atomic package recording and settlement, staleness, idempotency, and fail-closed vocabularies.
- CRG-R29 through CRG-R34: M2 records closed outcomes, findings, affected artifacts, and correction targets; M3 integrates workflow-owned correction routing; M4 preserves reviewer independence and review-resolution ownership.
- CRG-R35 through CRG-R40: M1 removes dual-topology activation machinery; M6 performs the atomic cutover only after legacy-dependent work is closed and proves the pre-adoption revert boundary.
- CRG-R41 and CRG-R42: M3 and M4 preserve downstream stage semantics and make Verify consume current package authority.
- CRG-R43 through CRG-R45: M4 updates canonical guidance, M5 proves validators and generated distribution parity, and M6 blocks cutover until the complete integrated surface is current.
- BND-INPUT-001 and BND-AUTH-001: M1 and M2 own cutover authority, package input, role, authority, and upstream-binding admission.
- BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001, and BND-RECOVERY-001: M2 and M3 own atomic authority, cross-artifact composition, stale/retry behavior, interruption recovery, and correction paths.
- BND-COMPAT-001 and BND-ENV-001: M1, M5, and M6 own single-mechanism cutover, historical-evidence boundaries, generated adapters, and rollback.
- INT-001 through INT-008: M2 proves package contradictions, stale settlement, and atomic recovery; M3 proves correction routing; M5 and M6 prove historical-authority rejection, generated parity, legacy-dependent cutover blocking, and rollback.

## Milestones

### M1. Establish the single-cutover foundation

- Milestone kind: implementation
- Goal: Remove dual-topology activation machinery and establish that the consolidated workflow replaces old progression only at one complete reviewed cutover.
- Requirements: CRG-R1 through CRG-R5, CRG-R35 through CRG-R40, CRG-AC7, CRG-AC10, BND-INPUT-001, BND-AUTH-001, BND-COMPAT-001, INT-005, INT-008
- Architecture decisions: Release cutover; Stage-owned artifact editing
- Files/components likely touched:
  - approved proposal, specification, ADR, plan, and test specification
  - `specs/cli-observability-and-token-efficient-results.md`
  - `packages/rigorloop/dist/lib/new-change.js`, lifecycle read/rendering, schema, and validator surfaces touched by the abandoned topology marker
  - lifecycle, new-change, change-metadata, artifact-lifecycle, and public-output fixtures and tests
- Dependencies:
  - Accepted proposal, approved consolidated-gates spec, and accepted ADR.
  - The exact current test specification must map all eight approved boundaries, INT-001 through INT-008, and milestone proof, and must retain its explicitly owner-approved status while this correction is applied.
  - The release-cutover milestone must later identify any nonterminal change that still depends on legacy progression.
- Tests and proof:
  - `new-change` writes no topology marker and reads no activation manifest.
  - Lifecycle status and context do not infer topology or baseline authority.
  - Existing public-output fixtures remain stable after removal of the abandoned M1 output additions.
  - Governing artifacts agree that only one progression mechanism is shipped after cutover.
- Implementation steps:
  - Remove topology-marker and activation-manifest tests before removing their implementation.
  - Remove the manifest, schema, parser, baseline inventory, new-change assignment, lifecycle inference, and output fields.
  - Amend the approved cutover, compatibility, architecture, plan, and proof contracts without changing their recorded approval status, as explicitly authorized by the owner.
  - Clarify that approved feature changes may supersede obsolete exact-output fixtures without introducing legacy rendering modes.
- Validation commands:
  - `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js`
  - `node --test packages/rigorloop/test/result-renderer.test.js`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: Current lifecycle behavior has no activation document or topology metadata, and the approved design requires one complete future cutover rather than coexistence.
- Completion criteria: Manifest, parser, schema, marker, inference, and output additions are absent; focused lifecycle, metadata, artifact-lifecycle, and public-output suites pass; authored contracts agree on one cutover.
- Required evidence: M1 correction evidence naming removed surfaces, revised contract identities, and exact focused test results.
- Review handoff: Code review of complete activation-machinery removal, public-output behavior, and cross-artifact cutover coherence.
- Optional commit boundary: `M1: simplify consolidated gate cutover`
- Risks:
  - A stale topology reference could preserve hidden dual-mode behavior.
  - Cutover wording could retire old progression before generated and runtime surfaces are complete.
- Rollback/recovery:
  - Revert the M1 correction while the implementing change remains pre-cutover; no released workflow transition occurs.

### M2. Implement aggregate review packages and atomic lifecycle authority

- Milestone kind: implementation
- Goal: Calculate exact design and delivery package revisions and record or settle one package decision atomically through the existing lifecycle transaction boundary.
- Requirements: CRG-R12 through CRG-R34, CRG-AC2 through CRG-AC6, CRG-AC10, BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, INT-001 through INT-005, INT-007
- Architecture decisions: Package membership and identity; Package lifecycle and CLI boundary
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`
  - `packages/rigorloop/dist/lib/lifecycle-read.js`
  - `packages/rigorloop/dist/lib/lifecycle-operations.js`
  - `packages/rigorloop/dist/lib/lifecycle-transaction.js`
  - package-review request, status, transaction, and recovery tests under `packages/rigorloop/test/`
  - `schemas/change.schema.json`, lifecycle validators, and review-record validation
- Dependencies:
  - M1 single-cutover contract and removal of dual-mode metadata.
  - Existing artifact registrations, safe-path checks, review logs, finding resolution, transaction locking, and recovery behavior.
- Tests and proof:
  - Design membership is primary architecture, primary spec, and applicable ADRs in deterministic order; delivery membership is primary plan then primary test spec.
  - Duplicate, missing, unsafe, extra-role, wrong-stage, unknown-kind, and unknown-outcome inputs fail closed.
  - `review-package-sha256-v1` is stable for identical canonical inputs and changes for every member-byte, membership, package-kind, or upstream-binding change.
  - Durable package projections store member IDs, upstream binding, and one aggregate revision without durable per-member hashes.
  - Approved settlement is atomic; changes-requested, blocked, and inconclusive remain visible but grant no authority.
  - Exact replay is idempotent; stale revision, stale member, stale binding, interrupted replacement, and post-validation failure preserve the prior complete authority.
- Implementation steps:
  - Write the package composition, identity, outcome, stale-input, interruption, and unknown-vocabulary regression fixtures first.
  - Add `review_packages.design` and `review_packages.delivery` projections with closed states and compact durable fields.
  - Implement transient member resolution and canonical aggregate calculation inside the lifecycle engine.
  - Add `context design-review` and `context delivery-review` package views and bounded status fields.
  - Add `record-package-review` and `settle-review-package` mutations using the common envelope, pure evaluator, lock, recovery, and single-file transaction.
  - Integrate finding scopes, affected artifact IDs, correction targets, review logs, and review-resolution without creating partial component authority.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-evidence.test.js packages/rigorloop/test/lifecycle-transaction.test.js`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
- Expected observable result: Contributors can inspect, record, retry, and atomically settle one exact design or delivery package using one CLI-calculated aggregate identity and precise findings, without maintaining member-document hashes.
- Completion criteria: Every package input, outcome, staleness, retry, authority, finding, interruption, and recovery partition has direct proof and no partial or component-only progression path remains.
- Required evidence: M2 evidence containing aggregate-identity vectors, atomic transaction fault results, outcome/authority matrix results, and exact package status examples.
- Review handoff: Code review of package composition, canonical identity, state projection, atomic settlement, finding attribution, and recovery behavior.
- Optional commit boundary: `M2: add atomic design and delivery package authority`
- Risks:
  - Package identity could drift across readers, validators, or generated evidence.
  - Sequential internal writes could accidentally expose partial authority.
- Rollback/recovery:
  - Revert package operations and projections together before cutover; the released workflow remains unchanged.

### M3. Complete consolidated workflow routing and downstream authority consumption

- Milestone kind: implementation
- Goal: Make normal progression, correction routing, automation projections, and downstream evidence consumption use the consolidated graph and exact settled authority.
- Requirements: CRG-R2 through CRG-R5, CRG-R15, CRG-R21, CRG-R25 through CRG-R29, CRG-R33 through CRG-R42, CRG-AC5 through CRG-AC8, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, INT-003 through INT-005, INT-007, INT-008
- Architecture decisions: Normal workflow progression; Package lifecycle and CLI boundary
- Files/components likely touched:
  - `packages/rigorloop/dist/lib/lifecycle-contract.js`
  - `packages/rigorloop/dist/lib/lifecycle-read.js`
  - `packages/rigorloop/dist/lib/lifecycle-operations.js`
  - `packages/rigorloop/test/lifecycle-stage-advance.test.js`
  - `scripts/workflow_automation.py`, `scripts/workflow_automation_state.py`, and related policy/validation tests
  - lifecycle correction, milestone, Verify-input, and workflow fixtures
- Dependencies:
  - M1 single-cutover contract.
  - M2 settled design and delivery package authority.
  - Existing correction, milestone, lock, recovery, and automation-state contracts.
- Tests and proof:
  - The closed consolidated stage graph admits only adjacent authorized edges.
  - Authoring completion, package settlement, and milestone completion are distinguished exactly.
  - The existing partial `advance-stage` code is extended to support the consolidated graph, package authority, exact replay, invalid-edge rejection, and active automation synchronization without a topology request field.
  - Settlement remains isolated; only workflow calls advancement or correction operations.
  - Artifact-local, cross-artifact, and upstream-direction package findings route to the required owners and return only after exact rereview.
  - Code Review, explanation, Verify, and PR inputs reject stale, mixed, or partial package authority.
- Implementation steps:
  - Expand stage-advance tests before changing the existing implementation, including retired-edge rejection, stale completion, package completion, automation contradiction, and replay.
  - Centralize the stage graph and source-stage completion checks so read permissions and mutations share one decision.
  - Extend correction routing to exact package findings and multiple correction targets without granting partial authority.
  - Update automation policy/state and downstream context consumers to require current package evidence.
  - Preserve milestone operations and final holistic Code Review triggers without treating package settlement as implementation completion.
- Validation commands:
  - `node --test packages/rigorloop/test/lifecycle-stage-advance.test.js packages/rigorloop/test/lifecycle-correction-route.test.js packages/rigorloop/test/lifecycle-milestone.test.js packages/rigorloop/test/lifecycle-read.test.js`
  - `python scripts/test-workflow-automation.py`
  - `python scripts/test-workflow-automation-policy.py`
  - `python scripts/test-workflow-automation-state.py`
  - `python scripts/test-workflow-code-state.py`
- Expected observable result: Workflow can advance or correct changes through one closed consolidated graph, while manual settlement remains isolated and downstream stages consume only exact current authority.
- Completion criteria: The consolidated graph, retired-edge rejection, package corrections, automation synchronization, stale/historical rejection, milestone preservation, and downstream authority consumption have direct public-path regression proof.
- Required evidence: M3 stage-transition matrix, correction-route evidence, automation-state results, and downstream stale/mixed authority results.
- Review handoff: Code review of graph closure, completion authority, routing separation, correction targeting, automation synchronization, and downstream evidence selection.
- Optional commit boundary: `M3: complete consolidated workflow routing`
- Risks:
  - Read-side permissions and mutation-side validation could diverge.
  - Package corrections could accidentally authorize one component or lose multi-owner findings.
- Rollback/recovery:
  - Revert consolidated routing and consumers together before cutover; the released workflow remains unchanged.

### M4. Publish canonical feasibility, Design Review, and Delivery Review responsibilities

- Milestone kind: implementation
- Goal: Update canonical skills, templates, and governance so public authoring and review responsibilities match the consolidated workflow and retire old progression entrypoints at cutover.
- Requirements: CRG-R3 through CRG-R21, CRG-R29 through CRG-R34, CRG-R41 through CRG-R45, CRG-AC1 through CRG-AC3, CRG-AC6, CRG-AC8 through CRG-AC10, BND-AUTH-001, BND-COMPOSE-001, BND-ENV-001, INT-001, INT-002, INT-006, INT-007
- Architecture decisions: Review and distribution boundaries; Stage-owned artifact editing
- Files/components likely touched:
  - `skills/design-review/` and `skills/delivery-review/`
  - `skills/proposal/`, `skills/proposal-review/`, and the canonical proposal template asset
  - `skills/spec-review/`, `skills/architecture-review/`, `skills/plan-review/`, and `skills/test-spec-review/`
  - `skills/workflow/`, `skills/code-review/`, `skills/explain-change/`, `skills/verify/`, and `skills/pr/`
  - `specs/skill-contract.md`, `specs/rigorloop-workflow.md`, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and affected examples
- Dependencies:
  - M2 package context and settlement request contracts.
  - M3 consolidated routing, correction, and downstream authority semantics.
- Tests and proof:
  - Proposal assets contain exactly one Feasibility section with assessment, basis, constraints, and blockers; Proposal Review rejects missing or inadequate feasibility.
  - `design-review` and `delivery-review` are independently invocable, record precise findings, do not edit reviewed artifacts, settle only exact packages, and remain isolated when invoked directly.
  - Old review skills are absent from the post-cutover public progression inventory and are not aliases.
  - Workflow, Code Review, Explain Change, Verify, and PR guidance consumes package authority without changing their preserved semantic responsibilities.
  - Published skill validation catches missing reciprocal ownership, unsupported claims, repository-maintainer leakage, and unknown stage vocabulary.
- Implementation steps:
  - Add failing skill-validator fixtures for the two new skills, retired-entrypoint exclusion, feasibility ownership, isolation, finding scopes, and generated asset requirements.
  - Add the Feasibility section to canonical proposal authoring assets and make Proposal Review evaluate it without creating another artifact.
  - Author distinct `design-review` and `delivery-review` skills with package-specific inputs, criteria, evidence, findings, settlement, stops, and claim limits; share only mapped review-method resources where appropriate.
  - Remove the four old review skills from post-cutover progression and adapter inventories rather than retaining compatibility aliases.
  - Update workflow and downstream skills, then amend governing specs and operational guidance with explicit cutover ownership and retirement language.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md`
- Expected observable result: Canonical public guidance exposes one embedded feasibility evaluation, distinct Design and Delivery review skills, retired old progression entrypoints, precise finding ownership, and unchanged downstream assurance responsibilities.
- Completion criteria: Canonical skill inventory, templates, reciprocal stage ownership, isolation, review recording, claim boundaries, governing specs, and operational guidance agree and pass skill and prose validation.
- Required evidence: M4 canonical skill inventory, validator output, generated local-mirror check, feasibility fixture results, and retired/new entrypoint authority matrix.
- Review handoff: Code review of public skill contracts, stage ownership, review independence, compatibility wording, and governance alignment.
- Optional commit boundary: `M4: publish consolidated review responsibilities`
- Risks:
  - Shared review text could turn old entrypoints into ambiguous aliases.
  - Governance wording could cut over before runtime and package parity exist.
- Rollback/recovery:
  - Revert canonical skill and guidance changes as one slice before cutover; retain authored review records as history.

### M5. Enforce structural invariants and generated adapter parity

- Milestone kind: implementation
- Goal: Make repository validators, fixtures, adapter manifests, generated archives, and release checks agree with the complete consolidated public surface before cutover.
- Requirements: CRG-R28, CRG-R35 through CRG-R45, CRG-AC7, CRG-AC9 through CRG-AC11, BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPAT-001, BND-ENV-001, INT-004 through INT-008
- Architecture decisions: Release cutover; Review and distribution boundaries
- Files/components likely touched:
  - `scripts/artifact_lifecycle_validation.py`, `scripts/change_metadata_semantics.py`, and `scripts/review_artifact_validation.py`
  - validator tests and fixtures under `scripts/test-*.py` and `tests/fixtures/`
  - `dist/adapters/manifest.yaml`
  - `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and adapter fixtures
  - release validation metadata and checks owned by existing release scripts
- Dependencies:
  - M1 single-cutover contract and absence of topology schemas.
  - M2 package state and review-record shapes.
  - M3 routing and compatibility behavior.
  - M4 complete canonical skill inventory.
- Tests and proof:
  - Every new closed vocabulary has an explicit unknown-value regression that fails before consistency checks.
  - Validators prove package shape, aggregate identity consistency, finding scope, atomic settlement consistency, stale authority, cutover prerequisites, and recovery invariants without attempting semantic review.
  - Generated Codex, Claude Code, and opencode archives contain the two new skills and omit the four retired progression skills.
  - Drift, missing skills, unexpected files, wrong gate inventory, and release-archive mismatch block generation or validation.
  - Historical-evidence and interruption fixtures preserve old records and prior complete state without granting old progression authority.
- Implementation steps:
  - Extend existing validator owners and fixtures rather than adding standalone validator CLIs.
  - Add package and cutover paths to validation selection and lifecycle governance where existing check ownership requires them.
  - Update adapter descriptors and manifests from canonical skill sources, then regenerate only temporary/release output through repository scripts.
  - Add archive parity, portability, drift, retired-entrypoint, and rollback-support tests for every supported adapter.
  - Integrate cutover prerequisites into existing release validation without making structural checks claim semantic review quality.
- Validation commands:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version v0.4.1 --output-dir release-output/v0.4.1`
  - `python scripts/validate-adapters.py --root release-output/v0.4.1 --version v0.4.1`
- Expected observable result: Repository governance and every generated adapter surface expose the same gate inventory, package record shape, and cutover behavior, with drift and unknown values failing closed.
- Completion criteria: Validator and adapter suites prove all structural and distribution invariants, generated archives are reproducible from canonical skills, and cutover prerequisites report no parity gap.
- Required evidence: M5 validator matrix, unknown-vocabulary results, generated archive inventories and checksums, adapter drift results, and compatibility fixture results.
- Review handoff: Code review of validator ownership, fail-closed ordering, generated-source boundaries, adapter parity, and release-gate composition.
- Optional commit boundary: `M5: enforce lifecycle and adapter parity`
- Risks:
  - Validators could duplicate semantic reviewer judgment or introduce a new validation framework.
  - Generated output could be hand-edited or checked against the wrong source boundary.
- Rollback/recovery:
  - Revert validators and adapter descriptors together before cutover and regenerate temporary output from the restored sources.

### M6. Cut over atomically and prove the release boundary

- Milestone kind: implementation
- Goal: Retire old progression and ship the consolidated workflow only after all canonical, runtime, legacy-work, validation, and generated-package prerequisites pass together.
- Requirements: CRG-R1 through CRG-R45, CRG-AC1 through CRG-AC11, all eight boundary IDs, INT-001 through INT-008
- Architecture decisions: Release cutover; Package membership and identity; Package lifecycle and CLI boundary; Normal workflow progression; Review and distribution boundaries
- Files/components likely touched:
  - cutover and pre-adoption-revert integration fixtures and repository validation evidence
  - legacy-dependent change inventory validation
  - any tracked release metadata required by the selected release profile
- Dependencies:
  - M1 through M5 accepted implementation slices and current code-review evidence.
  - No nonterminal governed change depends on legacy progression, plus reproducible generated-adapter parity.
- Tests and proof:
  - The checked cutover revision removes old progression entrypoints and exposes the complete consolidated graph and package authority together.
  - A new fixture completes proposal feasibility, Design Review, Delivery Review, implementation authorization, downstream review, and Verify-input selection through public paths.
  - Nonterminal legacy-dependent work, historical individual evidence presented as package authority, partial cutover, stale package state, and missing generated parity block.
  - A pre-adoption code-revert fixture restores the prior release without rewriting historical evidence; after adoption begins, recovery is forward-only unless separately specified.
- Implementation steps:
  - Run the complete cutover prerequisite graph and fail without changing released behavior if any owner is stale or legacy-dependent work remains.
  - Remove old progression entrypoints and publish consolidated routing, skills, validators, and generated packages in the same reviewed release slice.
  - Run end-to-end consolidated flow, historical-authority rejection, interruption, generated-parity, and pre-adoption-revert fixtures.
  - Record exact cutover and rollback evidence without rewriting historical review or change records.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/test-lifecycle-cli-conformance.py`
  - `python scripts/test-governed-lifecycle-cli-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: New and resumed governed work uses consolidated review gates; old progression entrypoints are absent; historical evidence remains readable; and no canonical/generated parity gap exists.
- Completion criteria: Cutover prerequisites, consolidated public flow, legacy-work blocker, historical-authority rejection, pre-adoption revert fixture, validators, canonical skills, generated adapters, and full repository proof agree at one revision.
- Required evidence: M6 cutover revision identity, legacy-dependent inventory result, end-to-end consolidated result, rollback result, generated archive checksums, and broad-smoke result.
- Review handoff: Final implementation-milestone code review covering cutover atomicity, old-entrypoint retirement, rollback, complete public-path behavior, and cross-milestone interactions.
- Optional commit boundary: `M6: cut over to consolidated review gates`
- Risks:
  - Cutover could expose consolidated routing before one consumer or adapter is current.
  - A late code revert could strand work already started under consolidated gates.
- Rollback/recovery:
  - Permit a reviewed code revert only before consolidated work begins; afterward use a forward correction or separately approved migration and do not rewrite change history.

### M7. Complete lifecycle closeout evidence

- Milestone kind: lifecycle-closeout
- Goal: Assemble final cross-milestone rationale and verification evidence after all implementation milestones and required code reviews close.
- Requirements: CRG-R41 through CRG-R45, CRG-AC8 through CRG-AC11
- Architecture decisions: Package lifecycle and CLI boundary; Review and distribution boundaries
- Files/components likely touched:
  - `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/explain-change.md`
  - conditional review-resolution, CI-maintenance, and verify evidence under the owning change root
- Dependencies:
  - M1 through M6 implementation milestones closed with required code-review evidence.
  - Matching test specification approved and its required proof complete.
- Tests and proof:
  - Explain-change traces the actual final diff to CRG-R1 through CRG-R45, ADR decisions, milestones, tests, reviews, cutover, and rollback evidence.
  - Final holistic Code Review covers cross-milestone interactions when milestone reviews cannot prove them in isolation.
  - Verify consumes current proposal, design, delivery, implementation, code-review, explanation, validation, and generated-package evidence and rejects stale or mixed authority.
- Implementation steps:
  - Resolve or explicitly disposition every material review finding before explanation or verification.
  - Produce the durable change explanation from the actual diff and exact evidence identities.
  - Run required final holistic Code Review, CI-maintenance if triggered, and Verify through their owning stages.
  - Prepare PR handoff only after Verify establishes current readiness.
- Validation commands:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-28-consolidate-rigorloop-review-gates`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md --path specs/consolidated-review-gates.md --path docs/adr/ADR-20260828-consolidated-review-package-topology.md`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: The complete current evidence set supports the downstream Verify decision without stale, partial, historical-authority, generated-parity, or unresolved-finding gaps.
- Completion criteria: Required implementation and holistic reviews are closed, explanation is current, validation evidence is complete, Verify has an exact evidence basis, and no lifecycle-closeout work is hidden in an implementation milestone.
- Required evidence: Final code-review record when required, explain-change artifact, conditional CI-maintenance evidence, verify report or receipt, and exact command results.
- Review handoff: `explain-change`, final `verify`, and then `pr` under their existing owners; this plan milestone does not perform or claim those outcomes.
- Optional commit boundary: `M7: assemble consolidated-gate closeout evidence`
- Risks:
  - Cross-milestone drift or generated-output staleness could escape focused milestone reviews.
- Rollback/recovery:
  - Keep closeout not-ready, route stale or contradictory evidence to its owning milestone or stage, and rerun only the affected review and verification chain.

## Validation plan

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js`: fast lifecycle contract, read-model, and progression loop.
- `npm test --prefix packages/rigorloop`: complete lifecycle CLI and public package regression suite.
- `python scripts/test-change-metadata-validator.py`: package, cutover, and compact change-state schema regression proof.
- `python scripts/test-artifact-lifecycle-validator.py`: artifact/package lifecycle and stale-state consistency proof.
- `python scripts/test-review-artifact-validator.py`: package-review findings, records, logs, and resolution-shape proof.
- `python scripts/test-workflow-automation.py`: consolidated workflow routing behavior.
- `python scripts/test-skill-validator.py`: canonical public skill inventory, ownership, isolation, and contract proof.
- `python scripts/build-skills.py --check`: generated local skill-mirror parity from canonical sources.
- `python scripts/test-adapter-distribution.py`: deterministic public adapter archive, manifest, alias, and portability proof.
- `bash scripts/ci.sh --mode broad-smoke`: final repository-wide composition required by cutover and generated-distribution risk.
- Manual semantic review remains required for feasibility credibility, design coherence, delivery adequacy, implementation fidelity, and final readiness because CRG-R45 prohibits structural validation from replacing those judgments.

## Risks and recovery

- Risk: historical individual-review evidence may be mistaken for current package authority.
  - Recovery: Block cutover until historical-authority fixtures and every public entrypoint enforce the single consolidated graph.
- Risk: aggregate identity may diverge across context, recording, settlement, validators, or Verify.
  - Recovery: Use one lifecycle-engine canonicalization owner and shared fixed vectors; fail closed on every mismatch and retain the last complete settlement.
- Risk: package review may weaken artifact-level traceability or reviewer independence.
  - Recovery: Persist member IDs and aggregate revision, keep findings scoped to artifacts/relationships, and route every correction to authoring owners before rereview.
- Risk: stage advancement may become a generic status setter or collapse settlement with continuation.
  - Recovery: Admit only closed graph edges with exact source completion and workflow authority; keep settlement isolated and test direct invocation.
- Risk: generated adapters may lag canonical skills at cutover.
  - Recovery: Make archive parity a cutover prerequisite and keep released behavior unchanged until all supported adapters validate.
- Risk: the broad change could become unreviewable.
  - Recovery: Preserve M1 through M6 as independently revertible implementation slices with focused proof and code review before integration cutover.

## Dependencies

- The exact current test specification must map all eight approved boundaries, INT-001 through INT-008, and milestone proof, and must receive a clean `test-spec-review` settlement before M1 implementation begins. Every implementation milestone inherits this gate through the ordered dependency chain.
- A substantive change to requirement mappings, boundary or interaction coverage, validation commands, fixtures, pass/fail criteria, or milestone proof in the test specification requires current `test-spec-review` settlement before affected implementation continues.
- M1 single-cutover contract precedes package state, routing, skills, validators, and cutover.
- M2 package authority precedes workflow consumption and public review-skill settlement.
- M3 runtime routing precedes canonical skill claims that consolidated continuation is supported.
- M4 canonical skills precede adapter generation; generated outputs are never hand-edited.
- M5 parity and legacy-retirement proof precede M6 cutover.
- M6 cutover must remain one reviewed slice; pre-adoption rollback is a normal code revert, and later recovery is forward-only unless separately specified.
- Each implementation milestone receives focused tests and independent code review before its dependent milestone begins.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-29 | Use one release cutover instead of runtime topology admission. | The old mechanism is retired after the consolidated surface is complete, so per-change topology metadata and a legacy baseline add no durable value. | Activation manifest, runtime coexistence, or inferred topology. |
| 2026-08-29 | Implement package identity and atomic settlement before publishing new review skills. | Public skills must describe executable lifecycle behavior and exact evidence contracts. | Publishing aspirational skills first or letting skills emulate settlement in prose. |
| 2026-08-29 | Treat the existing `advance-stage` work as incomplete M3 scope. | The approved ADR requires the consolidated graph, package completion authority, replay, and automation synchronization beyond the current partial slice. | Declaring the partial CLI fix complete or creating a separate generic status operation. |
| 2026-08-29 | Make generated adapter parity a prerequisite to cutover. | CRG-R38 and CRG-R44 prohibit release cutover while installable packages expose a different gate inventory. | Changing canonical sources first and repairing adapters afterward. |
| 2026-08-29 | Isolate cutover in M6 after all implementation surfaces are reviewed. | The release boundary must retire old progression atomically and allow a normal revert before adoption begins. | Incremental activation, runtime coexistence, or automatic migration of active legacy changes. |

## Readiness

- See the owning change record for current workflow state.
