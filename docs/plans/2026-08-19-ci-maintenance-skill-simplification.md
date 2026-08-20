# CI-Maintenance Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `ci-maintenance` package without weakening command ownership, semantic risk coverage, least privilege, privileged-design authority, concurrent file safety, dependency-aware batch behavior, or hosted-CI truthfulness. Freeze semantic and literal ownership first, split the canonical package second, and prove every real assembly plus package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md`
- Spec: `specs/ci-maintenance-skill-simplification.md`
- Architecture: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/architecture-assessment.md`; not required
- Test spec: `specs/ci-maintenance-skill-simplification.test.md`, pending

## Context and orientation

`skills/ci-maintenance/` is the only authored package source. Its current root mixes universal safety, GitHub authoring mechanics, risk placement, and output structure. The change adds `references/github-workflow-authoring.md`, narrows the existing risk map to semantic coverage placement, and makes `assets/github-workflow-skeleton.yml` minimally safe and structural.

The focused specification amends only five clauses in the existing approved CI-maintenance contract. Existing skill validation and adapter distribution tooling remain the owners of resource mapping and canonical-through-installed parity. Conditional file safety remains an invocation-local contract and must use available transient filesystem primitives; no persistent transaction system is planned.

## Non-goals

- Run validation, wait for hosted CI, debug checks, design tests, verify a branch, or open a PR.
- Design privileged workflows, mutate external platform state, or add provider-neutral authoring.
- Add a workflow generator, managed YAML parser, persistent lock, mutation receipt, multi-file transaction, or runtime engine.
- Bulk-migrate historical workflows or optimize unrelated skills beyond directly coupled contracts, validators, fixtures, mappings, and package surfaces.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R45-R54; BND-COMPAT-001, BND-ENV-001; INT-006 | M1 rule/literal ledgers, compatibility inventory, scenario fixtures, baselines, and architecture-trigger check |
| R1-R28, R42-R44; BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001; INT-001, INT-002, INT-003 | M2 focused contract alignment, package split, assemblies, privilege, risk ownership, skeleton, and result claims |
| R29-R41; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-004, INT-005 | M3 conditional one-file commits, dependency batches, partial results, and retry proof |
| R45-R52, R54; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-006 | M4 semantic preservation, all-assembly reduction, boundary proof, and canonical-through-installed parity |
| R1-R54 | M5 lifecycle closeout after all implementation milestones |

## Milestones

### M1. Freeze rules, literals, scenarios, and baselines

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, consumed literal, compatibility overlap, boundary scenario, and real loaded assembly before canonical procedure moves.
- Requirements: R45-R54; BND-COMPAT-001; BND-ENV-001; INT-006.
- Architecture decisions: architecture-not-required assessment; stop and reassess if R53 triggers.
- Files/components likely touched:
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/ci-maintenance-rule-disposition.yaml`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/ci-maintenance-literal-compatibility.yaml`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/fixtures/`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/profile-size-baseline.md`
  - focused validator fixtures identified by the inventories
- Dependencies:
  - approved specification, closed `CIMSIM-SR1`, and recorded architecture assessment
  - current skill, legacy focused contract, skill contract, parser consumers, validators, package mappings, and generated-resource owners
- Tests and proof:
  - every semantic rule and parser-sensitive literal receives exactly one retained, relocated, amended, removed, or incidental treatment and one owner
  - the five amended legacy clauses and every unlisted retained clause are represented
  - fixtures cover closed classifications, assemblies and variants, resource failure, privilege authority, risk ownership, conditional commits, dependency batches, result claims, and unknown values
  - LF-normalized word and UTF-8 byte baselines reproduce the current root, resources, fixed assemblies, conditional variants, and complete package
  - the inventory confirms no R53 architecture trigger before package mutation
- Implementation steps:
  - inventory current root, reference, asset, focused specification, validators, fixtures, and package consumers
  - separate semantic ownership from exact literal compatibility and structural asset ownership
  - serialize deterministic positive and negative scenarios, including every named proposal/spec regression
  - record exact measurement formulas and canonical input identities
  - stop and return to architecture if safe conditional commits or batch proof require persistent coordination, parsing, provider abstraction, or external mutation
- Validation commands:
  - `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, scenario, compatibility overlap, and measurement input has one closed treatment before canonical package mutation.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, baselines are reproducible, no R53 trigger is present, and `skills/ci-maintenance/SKILL.md` remains unchanged.
- Required evidence: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 inventories, fixtures, and baseline evidence.
- Optional commit boundary: `M1: freeze ci-maintenance simplification ownership`
- Risks:
  - old skeleton assertions may be mistaken for still-authoritative behavior after R54
  - incidental prose may be frozen as a parser contract
- Rollback/recovery:
  - revert M1 evidence and fixtures only; return normative gaps to spec and architecture triggers to architecture assessment before M2

### M2. Align the contract and split the canonical package

- Milestone kind: implementation
- Goal: Shorten the universal skill, add the GitHub authoring reference, narrow the risk map, simplify the skeleton, and implement exhaustive classification and assembly behavior.
- Requirements: R1-R28, R42-R44; BND-INPUT-001; BND-AUTH-001; BND-COMPOSE-001; INT-001; INT-002; INT-003.
- Architecture decisions: existing mapped-resource and adapter-package architecture; no ADR.
- Files/components likely touched:
  - `skills/ci-maintenance/SKILL.md`
  - `skills/ci-maintenance/references/github-workflow-authoring.md`
  - `skills/ci-maintenance/references/risk-to-check-map.md`
  - `skills/ci-maintenance/assets/github-workflow-skeleton.yml`
  - `specs/ci-maintenance-skill.md`
  - `specs/ci-maintenance-skill.test.md`
  - `scripts/test-skill-validator.py`
  - directly coupled fixture or package mapping surfaces identified by M1
- Dependencies:
  - M1 and its code review close without architecture reassessment
- Tests and proof:
  - closed independent operation, concern, target, provider, privilege, and structure axes plus unknown-value-first failure
  - exact target/provider compatibility and external-state read-only behavior
  - sole semantic risk-placement ownership and GitHub serialization without policy overlap
  - ordinary, project-native, structural, coverage-sensitive, and privileged approved-design assemblies and late loading
  - minimal skeleton contents and absence of built-in privileged, boundary, push, schedule, or manual behavior
  - fixed hosted observation and forbidden readiness claims
- Implementation steps:
  - add failing focused assertions and scenario fixtures before canonical edits
  - amend the legacy contract and its tests according to R54 without weakening unlisted clauses
  - keep universal safety, authority, stops, claims, and resource triggers inline
  - move only GitHub composition and exact approved-design realization mechanics to the new reference
  - narrow the risk map to semantic coverage selection and reduce the skeleton to structural safe defaults
  - update only directly coupled active consumers identified by M1
- Validation commands:
  - `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`
  - `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: each invocation selects its exact resources and external evidence, policy ownership is singular, privileged choices remain design-bound, and review/external/hosted claims remain bounded.
- Completion criteria: focused and broad tests pass, every rule and structure has one owner, amended literals migrate atomically, and no new architecture owner appears.
- Required evidence: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the focused contract, canonical package, and coupled consumers.
- Optional commit boundary: `M2: simplify ci-maintenance package paths`
- Risks:
  - universal command or security safety may move behind conditional loading
  - the authoring reference may silently regain semantic check-placement authority
  - the skeleton may imply privileged or boundary behavior through examples
- Rollback/recovery:
  - restore the prior canonical package and legacy contract atomically, remove the new mapped reference, and rebuild generated packages

### M3. Implement conditional commits and dependency-aware batches

- Milestone kind: implementation
- Goal: Close single-file concurrency and multi-target partial-state behavior without introducing persistent coordination.
- Requirements: R29-R41; BND-STATE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001; INT-004; INT-005.
- Architecture decisions: architecture-not-required only while primitives remain transient and manifests invocation-local.
- Files/components likely touched:
  - `skills/ci-maintenance/SKILL.md`
  - `skills/ci-maintenance/references/github-workflow-authoring.md`
  - `scripts/test-skill-validator.py`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/fixtures/`
  - existing repository helper surfaces only when M1 proves a directly coupled reusable primitive already owns the behavior
- Dependencies:
  - M2 and its code review close with the complete resource model stable
- Tests and proof:
  - atomic no-clobber creation rejects a target that appears after preflight
  - identity-guarded revision rejects a target that changes after validation
  - read-back confirms bytes but never substitutes for commit-time protection
  - unsupported conditional capability and uncertain output return `blocked`
  - exact intended content plus unchanged evidence is idempotent; every other retry reclassifies current state
  - independent, ordered-dependent, and atomic-group-required batches prepare fully, validate references, order safely, and report complete, partial-blocked, or blocked-before-write exactly
  - retry reconstructs the current graph and never adopts stale or unrelated partial state
- Implementation steps:
  - add failing deterministic filesystem and manifest scenarios first
  - document or use existing transient conditional file primitives without adding persistence
  - implement the complete single-target commit sequence in published procedure
  - implement invocation-local batch classification, provider-first ordering, intermediate-validity checks, and exact aggregate results
  - stop and return to architecture if the supported environment cannot satisfy the contract without a new persistent owner
- Validation commands:
  - `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests`
  - `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: concurrent work is never overwritten, safe dependent batches expose exact partial state, and unsupported atomic grouping stops before mutation.
- Completion criteria: every concurrency, retry, dependency, partial-failure, and unsupported-environment scenario passes without persistent coordination or external mutation.
- Required evidence: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/m3-conditional-commit-and-batch-proof.md`
- Review handoff: independent `code-review` of conditional-write, batch, retry, and architecture-boundary behavior.
- Optional commit boundary: `M3: close ci-maintenance mutation safety`
- Risks:
  - a nominally atomic rename may still overwrite concurrent work
  - batch ordering may expose an invalid wrapper or provider state
- Rollback/recovery:
  - revert M3 procedure and fixtures as one unit; retain the fail-closed prior behavior and do not weaken the approved concurrency contract

### M4. Prove all-assembly reduction and package parity

- Milestone kind: implementation
- Goal: Prove semantic preservation, every real assembly's reduction, boundary coverage, and canonical-through-installed integrity.
- Requirements: R45-R52, R54; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-006.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct resource-selection proof is absent
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-19-ci-maintenance-skill-simplification/evidence/m4-package-proof.md`
- Dependencies:
  - M2-M3 and their code reviews are closed
- Tests and proof:
  - every fixed assembly and conditional `CIM5`, `CIM6`, and `CIM8` variant decreases in words and UTF-8 bytes from its frozen equivalent
  - external design and project-contract evidence is disclosed but excluded from packaged totals
  - every semantic rule, literal, amended legacy clause, boundary, and interaction has verified final treatment and proof
  - generated, archived, release-candidate, and clean-installed packages contain exact mapped resources and reject drift
- Implementation steps:
  - extend only existing package proof when direct CI-maintenance selection coverage is absent
  - build and validate temporary package and installation trees
  - report before/after assemblies, resources, duplicate ownership, and complete package
  - compare the final package and coupled consumers with M1 inventories and approved requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/ci-maintenance-skill-simplification.md`
  - `python scripts/build-skills.py --check`
- Expected observable result: every real assembly shrinks and every supported package carries byte-identical required resources and preserved semantics.
- Completion criteria: measurement, preservation, boundary, canonical, generated, archive, release-candidate, and clean-install proof pass with no unexplained growth or unresolved literal.
- Required evidence: simplification measurements, semantic preservation review, and M4 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M4: prove ci-maintenance simplification`
- Risks:
  - generic adapter tests may omit a conditional assembly or external-evidence disclosure
  - a smaller root may hide growth in coverage-sensitive or privileged paths
- Rollback/recovery:
  - restore the prior package, regenerate derived output, and discard temporary package trees

### M5. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R54.
- Architecture decisions: architecture-not-required assessment.
- Files/components likely touched:
  - final review records, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M4 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and the complete approved test-spec command ledger
- Implementation steps:
  - run final holistic `code-review`
  - close every material finding through owned correction and rereview
  - create or refresh the durable change explanation
  - run final `verify` and hand off to `pr` only under separate authority
- Validation commands:
  - use the complete approved test-spec command ledger
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports truthful PR handoff state.
- Completion criteria: final review is clean, rationale is current, verification is recorded, and no blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate authority.
- Optional commit boundary: `closeout: verify ci-maintenance simplification`
- Risks:
  - late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 focused skill-validator proof owns closed ledgers, compatibility, scenario inventory, unknown-value-first behavior, architecture triggers, and baselines.
- M2 focused and broad skill/package validation owns classifications, resource selection, policy ownership, privileged design realization, skeleton structure, and claims.
- M3 deterministic filesystem and batch scenarios own no-clobber, identity guards, read-back, retry, dependency ordering, intermediate validity, and partial results.
- M4 adapter, build, boundary, and measurement proof owns generated-resource parity and semantic preservation.
- Change metadata, formal reviews, code review, verify, and PR review own lifecycle and human judgment.

## Risks and recovery

- Risk: extraction hides command, coverage, or security safety. Recovery: block M2 on M1 ownership and narrow-review proof.
- Risk: conditional replacement overwrites concurrency. Recovery: require commit-time predicates and block unsupported environments.
- Risk: dependency batches expose invalid intermediate state. Recovery: prove provider-first ordering or classify atomic-group-required before writes.
- Risk: relocation appears as deletion. Recovery: report all assemblies, resources, duplicate ownership, and complete package.
- Risk: a new persistent owner becomes necessary. Recovery: stop and return to architecture before canonical mutation.

## Dependencies

- Approved focused spec, clean spec review, closed review resolution, architecture-not-required assessment, and accepted proposal direction.
- Existing legacy CI-maintenance, published-skill resource, stage-owned lifecycle, and adapter-package contracts.
- Existing skill validation, package generation, archive validation, release-candidate validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-19 | Use four implementation milestones plus lifecycle closeout. | Ownership inventory, package composition, mutation safety, and distribution proof have distinct rollback and review boundaries. | One large rewrite; prose-only milestones. |
| 2026-08-19 | Keep semantic placement in the risk map and serialization in the GitHub reference. | One owner for each decision prevents policy drift while preserving conditional loading. | Duplicate placement rules; one catch-all reference. |
| 2026-08-19 | Use transient conditional file primitives and invocation-local batch manifests only. | This satisfies concurrency and partial-state safety without creating a new architecture owner. | Plain overwrite; persistent transaction service. |
| 2026-08-19 | Measure every fixed assembly and conditional variant separately. | Root-only or complete-package totals cannot prove user-visible simplification. | Root-only measurement; privileged-path omission. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
