# Architecture-Review Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `architecture-review` package without weakening architecture judgment, formal recording, evidence-scoped target settlement, exact retry, reviewer independence, or handoff safety. Freeze semantic and literal ownership first, refactor the canonical package second, and prove real-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-16-architecture-review-skill-simplification.md`
- Spec: `specs/architecture-review-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-16-architecture-review-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/architecture-review-skill-simplification.test.md`

## Context and orientation

`skills/architecture-review/` is the sole authored package source. The change shortens the universal skill, adds `references/architecture-package-review.md` and `references/architecture-review-recording-and-settlement.md`, retains the shared `Isolation and Recording` block byte-identically, and adds no structural asset. Existing validators own normalized skill structure and resource mappings, while adapter build and distribution checks own derived-package parity. The existing formal-review Markdown evidence must carry the exact review subject, governing basis, target dispositions, and prepared settlement manifest without adding a new schema or state owner.

## Non-goals

- Change architecture method, review statuses, lifecycle stages, artifact owners, architecture-review approval authority, workflow order, or customer-project portability.
- Add runtime routing, a new persistence surface, lifecycle state, state owner, structural asset, tokenizer dependency, prose classifier, target-agent evaluation, or a separate manual semantic-review acceptance gate.
- Optimize `architecture` authoring or another review skill.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R47-R54; BND-COMPAT-001, BND-ENV-001; INT-005 | M1 rule and literal ledgers, static scenarios, evidence-capability proof, and baseline measurements |
| R1-R46, R58; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-004 | M2 canonical skill, conditional references, prepared settlement protocol, and focused proof |
| R49-R57; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M3 real-profile reduction, semantic preservation, boundary coverage, and canonical-through-installed parity |

## Milestones

### M1. Freeze review rules, literals, scenarios, and measurement baselines

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, compatibility-sensitive literal, required transaction scenario, and loaded profile before moving procedure.
- Requirements: R47-R54; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: none; architecture assessment is `architecture-not-required` conditional on existing review evidence supporting the prepared manifest.
- Files/components likely touched:
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/architecture-review-rule-disposition.yaml`
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/architecture-review-literal-compatibility.yaml`
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/fixtures/`
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved specification and recorded bounded architecture assessment
  - complete current `architecture-review` package and exact consumers
- Tests and proof:
  - closed scenario vocabularies fail unknown values before consistency checks
  - scenarios cover all four surfaces, all valid authority combinations, record-only subjects, stale bases, scoped dispositions, prepared settlement, interruption, concurrency, missing resources, and forbidden writes
  - the existing review-evidence model is shown capable of representing the full prepared manifest without a new durable schema
  - LF-normalized baseline words and UTF-8 bytes are recorded for ARR0, ARR0M, ARR1, ARR1M, each resource, and the total package
- Implementation steps:
  - inventory universal, method, recording, settlement, retry, automation, and exact-literal ownership with one disposition per item
  - serialize deterministic positive and negative scenarios, including unknown-value fixtures
  - prove that detailed formal-review Markdown can durably record subject, basis, dispositions, expected states, and per-target progress
  - record the deterministic baseline assemblies and identities
- Validation commands:
  - run the M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-16-architecture-review-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, scenario, and measurement surface has one closed treatment before canonical prose moves.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, evidence capability is proven, and the canonical skill package remains unchanged.
- Required evidence: `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze architecture-review ownership`
- Risks:
  - similar recording text may encode different advisory, formal, or automated authority
  - existing Markdown evidence may prove too weak for exact partial recovery
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged and route to architecture if evidence capability fails

### M2. Separate universal judgment, architecture method, and governed settlement

- Milestone kind: implementation
- Goal: Shorten `SKILL.md`, add both references, preserve the shared block exactly, and implement evidence-scoped prepared settlement with exact retry.
- Requirements: R1-R46, R58; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-004.
- Architecture decisions: existing published-skill package and stage-owned formal-review evidence decisions; no new ADR.
- Files/components likely touched:
  - `skills/architecture-review/SKILL.md`
  - `skills/architecture-review/references/architecture-package-review.md`
  - `skills/architecture-review/references/architecture-review-recording-and-settlement.md`
  - `scripts/test-skill-validator.py`
  - directly coupled resource registrations and literal consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - exact ARR0, ARR0M, ARR1, and ARR1M resource loading and missing-resource stops
  - all four review subjects, record-only surfaces without targets, complete governing-basis identity, invalid authority combinations, and advisory isolation
  - one overall status with finding-scoped or blocker-scoped target dispositions and no partial approval
  - durable prepared manifest before target writes, exact pending-write retry, changed basis, changed targets, concurrent state, and no duplicate review evidence
  - byte-identical shared `Isolation and Recording` block and no new structural asset
- Implementation steps:
  - add failing focused assertions before canonical package edits
  - keep universal evidence, classification, judgment, materiality, stops, claims, and resource triggers inline
  - author the architecture-package review reference from method-specific rules
  - author the recording-and-settlement reference from durable recording, prepared manifest, disposition, retry, concurrency, automation, and settlement rules
  - migrate true literal and resource consumers atomically while keeping shared-block bytes exact
- Validation commands:
  - `python scripts/validate-skills.py skills/architecture-review/SKILL.md`
  - `python scripts/test-skill-validator.py ArchitectureReviewSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: ordinary judgment stays self-sufficient, architecture-package review loads only method detail, durable review loads exact recording procedure, and interrupted multi-target settlement remains recoverable without unsupported target mutation.
- Completion criteria: focused and broad skill tests pass, every mode and surface has one loaded owner, shared bytes match, and no new persistence or lifecycle authority appears.
- Required evidence: `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of canonical package and validator changes.
- Optional commit boundary: `M2: simplify architecture-review package paths`
- Risks:
  - universal review safety may move behind a trigger
  - target dispositions may be mistaken for partial semantic approval
  - settlement progress may become reconstructed instead of durably prepared
- Rollback/recovery:
  - restore the prior canonical package and focused assertions and regenerate derived output atomically

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove real-profile reduction, semantic preservation, complete boundary proof, and canonical-through-installed integrity.
- Requirements: R49-R57; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct `architecture-review` selection coverage is absent
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-16-architecture-review-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - ARR1 and ARR1M loaded words and bytes decrease from baseline; ARR0, ARR0M, resources, and total package are reported separately
  - every semantic rule and exact literal has one classified final disposition
  - generated, archived, release-candidate, and clean-installed packages contain byte-identical required resources
  - missing, escaped, transformed, stale, extra, or mixed resources fail
  - the approved proof map gives every applicable boundary and interaction direct proof
- Implementation steps:
  - extend only existing package proof when direct architecture-review selection is absent
  - build and validate temporary package and installation trees
  - report before and after assemblies, resources, duplicates, and total package without presenting relocation as deletion
  - compare the final package with the M1 ledgers and all requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/architecture-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/architecture-review-skill-simplification.md`
- Expected observable result: both real formal review profiles shrink and every supported package carries exact required references.
- Completion criteria: measurement, preservation, boundary, canonical, build, archive, release-candidate, and clean-install proof pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove architecture-review simplification`
- Risks:
  - generic adapter tests may omit direct architecture-review selection
  - a smaller main file may hide real formal-profile growth
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R58.
- Architecture decisions: none.
- Files/components likely touched:
  - final review records, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M3 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and complete approved test-spec command ledger
- Implementation steps:
  - run final holistic `code-review`, resolve and rereview findings, record rationale, and run final `verify`
- Validation commands:
  - use the complete approved test-spec commands
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports truthful PR handoff state.
- Completion criteria: final review is clean, rationale is current, verification is recorded, and no blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate authority.
- Optional commit boundary: `closeout: verify architecture-review simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library proof owns closed ledgers, static scenarios, evidence-capability proof, and unknown-value-first behavior.
- Skill validation owns canonical structure, resource mappings, shared literal compatibility, and focused behavior.
- Build and adapter validation own generated, archived, release-candidate, and installed parity.
- Boundary validation owns final requirement-to-proof structure after the test spec exists.
- Change metadata, review artifacts, code review, verification, and PR review own lifecycle and semantic judgment.

## Risks and recovery

- Risk: extraction hides universal review safety. Recovery: block on M1 ownership, ARR0 scenarios, focused assertions, and review.
- Risk: prepared settlement becomes a hidden new state model. Recovery: keep it in existing formal-review Markdown, stop on schema expansion, and return to architecture assessment if a new owner is required.
- Risk: evidence-scoped settlement over-mutates unaffected targets. Recovery: require explicit finding and blocker scopes, expected pre/post states, and exact retry fixtures.
- Risk: relocation appears as deletion. Recovery: report all assemblies, references, duplicate ownership, and total package.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing published-skill resource, architecture method, stage-owned lifecycle, formal-review evidence, and workflow-routing contracts.
- Existing skill validation, adapter generation, archive validation, release-candidate validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-16 | Use three implementation milestones plus lifecycle closeout. | Ownership, canonical mutation, and package proof have independent rollback and review boundaries. | One large rewrite; many prose-only milestones. |
| 2026-08-16 | Freeze semantic and literal ownership before edits. | Behavior and exact compatibility require different evidence and migration treatment. | Infer ownership after editing; freeze every sentence. |
| 2026-08-16 | Implement both references with the settlement fixtures. | Loading, review identity, prepared recovery, and target dispositions must remain coherent. | Partial package rollout; several narrow references. |
| 2026-08-16 | Reuse formal-review Markdown for the prepared manifest. | Existing evidence ownership is sufficient and avoids new architecture. | Parsed transaction schema; in-memory-only recovery. |
| 2026-08-16 | Measure real formal profiles and total package separately. | Relocation must not be presented as deletion. | Main-file-only or fixed-percentage acceptance. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
