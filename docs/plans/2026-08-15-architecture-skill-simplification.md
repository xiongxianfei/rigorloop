# Architecture Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `architecture` package without weakening applicability, C4 plus arc42 plus ADR method, governed authority, prepared recovery, dependency-safe commits, or review handoff. Freeze ownership first, refactor the canonical package second, and prove real-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-15-architecture-skill-simplification.md`
- Spec: `specs/architecture-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-15-architecture-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/architecture-skill-simplification.test.md`

## Context and orientation

`skills/architecture/` is the sole authored package source. The change adds `references/architecture-package-method.md` and `references/governed-architecture-authoring.md`, shortens the universal skill, and retains exactly three assets after classifying policy-bearing prompts. Existing skill validators own structure and mappings, while adapter generation and validation own derived package parity. Prepared manifests remain Markdown authoring evidence rather than a new parsed schema.

## Non-goals

- Change architecture applicability, C4, arc42, ADR semantics, canonical paths, architecture-review settlement, workflow order, or customer-project portability.
- Add runtime routing, new persistence, lifecycle states, state owners, assets, tokenizer dependencies, prose classifiers, target-agent evaluation, or a separate manual semantic-review gate.
- Optimize `architecture-review`.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R43-R51; BND-COMPAT-001, BND-ENV-001; INT-004 | M1 ownership ledgers, scenarios, and baseline measurement |
| R1-R48; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-003 | M2 canonical package, prepared transaction, dependencies, assets, and focused proof |
| R49-R54; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004 | M3 profile reduction, semantic preservation, and canonical-through-installed proof |

## Milestones

### M1. Freeze architecture rule, literal, asset, and scenario ownership

- Milestone kind: implementation
- Goal: Account for every behavioral rule, compatibility-sensitive literal, asset instruction, and required scenario before moving procedure.
- Requirements: R43-R51; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: none; architecture assessment is `architecture-not-required`.
- Files/components likely touched:
  - `docs/changes/2026-08-15-architecture-skill-simplification/architecture-rule-disposition.yaml`
  - `docs/changes/2026-08-15-architecture-skill-simplification/architecture-literal-compatibility.yaml`
  - `docs/changes/2026-08-15-architecture-skill-simplification/architecture-asset-disposition.yaml`
  - `docs/changes/2026-08-15-architecture-skill-simplification/fixtures/`
  - `docs/changes/2026-08-15-architecture-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved specification and recorded no-architecture assessment
  - complete current architecture package and exact consumers
- Tests and proof:
  - all three assemblies, assessment outcomes, signal classifications, target operations, prepared evidence, dependencies, commit groups, retries, asset composition, missing resources, and forbidden writes
  - unknown values fail before consistency checks
  - LF-normalized baseline words and bytes
- Implementation steps:
  - inventory semantic rules, duplicates, literals, and every non-heading asset instruction with stable owners and dispositions
  - serialize deterministic scenarios and negative unknown-value fixtures
  - record AA0, AA1, AA2, resource, asset, representative output, and total-package baselines
- Validation commands:
  - run the M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, asset prompt, and required scenario has one closed treatment before canonical prose moves.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, and the canonical package remains unchanged.
- Required evidence: `docs/changes/2026-08-15-architecture-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze architecture skill ownership`
- Risks:
  - similar text may encode different universal, method, or governed behavior
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged

### M2. Separate universal, method, and governed architecture procedure

- Milestone kind: implementation
- Goal: Shorten `SKILL.md`, add both references, correct asset ownership, and preserve exact prepared and dependency-safe transaction behavior.
- Requirements: R1-R48; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-003.
- Architecture decisions: existing published-skill package and stage-owned lifecycle decisions; no new ADR.
- Files/components likely touched:
  - `skills/architecture/SKILL.md`
  - `skills/architecture/references/architecture-package-method.md`
  - `skills/architecture/references/governed-architecture-authoring.md`
  - `skills/architecture/assets/architecture-skeleton.md`
  - `skills/architecture/assets/adr-skeleton.md`
  - `skills/architecture/assets/diagram-styles.mmd`
  - `scripts/test-skill-validator.py`
  - directly coupled resource registrations and literal consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - exact AA0, AA1, and AA2 loads and missing-resource stops
  - assessment recording, current-basis binding, invalid signals, portable isolation, and governed authority
  - manifest preparation before writes, interruption points, exact retries, changed manifests, concurrency, dependencies, commit groups, canonical commit order, ADR supersession, and all batch results
  - asset composition, no duplicate policy, and no placeholders
- Implementation steps:
  - add failing focused assertions before canonical package edits
  - keep universal applicability, classifications, stops, claims, and triggers inline
  - author the method reference from method-owned rules and the governed reference from authority and transaction rules
  - revise policy-bearing asset prompts according to M1 without changing literal Mermaid styles
  - migrate true literal consumers atomically
- Validation commands:
  - `python scripts/validate-skills.py skills/architecture/SKILL.md`
  - `python scripts/test-skill-validator.py ArchitectureSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: assessment stays self-sufficient, portable authoring loads only method detail, governed authoring loads exact mutation procedure, and interrupted combined work remains recoverable and dependency-safe.
- Completion criteria: focused and broad skill tests pass, resource maps and assets validate, and all universal and transaction rules have one loaded owner.
- Required evidence: `docs/changes/2026-08-15-architecture-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of canonical package and validators.
- Optional commit boundary: `M2: simplify architecture package paths`
- Risks:
  - universal applicability may move behind a trigger
  - shared evidence or commit groups may imply an unapproved schema
  - partial commits may expose broken references
- Rollback/recovery:
  - restore the prior canonical package and focused assertions and regenerate derived output atomically

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove real-profile reduction, semantic preservation, complete boundary proof, and canonical-through-installed integrity.
- Requirements: R49-R54; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct architecture coverage is absent
  - `docs/changes/2026-08-15-architecture-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-15-architecture-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-15-architecture-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - generated, archived, release-candidate, and clean-installed targets contain exact references and assets
  - missing, escaped, transformed, stale, extra, or mixed resources fail
  - approved proof map gives every applicable boundary and interaction direct proof
- Implementation steps:
  - extend only existing package proof when direct architecture selection is absent
  - build and validate temporary package and installation trees
  - report before and after assemblies, resources, assets, representative output, total package, and duplicates
  - compare final package against M1 ledgers and all requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/architecture/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/architecture-skill-simplification.md`
- Expected observable result: all three procedural assemblies shrink and every supported package carries byte-identical required resources.
- Completion criteria: measurement, preservation, boundary, canonical, build, archive, and clean-install proof pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove architecture simplification`
- Risks:
  - generic adapter tests may omit direct architecture selection
  - main-file reduction may hide real-profile growth
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R54.
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
- Optional commit boundary: `closeout: verify architecture simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library proof owns closed ledgers, scenarios, and unknown-value-first behavior.
- Skill validation owns canonical structure, mappings, and focused behavior.
- Build and adapter validation own generated, archived, release-candidate, and installed parity.
- Boundary validation owns final requirement-to-proof structure after the test spec exists.
- Change metadata, review artifacts, code review, and PR review own lifecycle and semantic judgment.

## Risks and recovery

- Risk: extraction hides universal applicability. Recovery: block on M1 ownership, AA0 scenarios, focused assertions, and review.
- Risk: prepared recovery becomes a new hidden state model. Recovery: keep it Markdown evidence, stop on schema expansion, and return to architecture assessment if a new owner is required.
- Risk: dependent commits expose broken references. Recovery: validate dependencies and commit groups before canonical Markdown and preserve only independently valid targets.
- Risk: relocation appears as deletion. Recovery: report all loaded assemblies, resources, assets, representative output, and total package.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing skill resource, architecture method, stage-owned lifecycle, and workflow-routing contracts.
- Existing skill validation, adapter generation, archive validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-15 | Use three implementation milestones plus lifecycle closeout. | Ownership, canonical mutation, and package proof have independent rollback and review boundaries. | One large rewrite; many prose-only milestones. |
| 2026-08-15 | Freeze semantic, literal, and asset ownership before edits. | Behavior, exact compatibility, and copied structure are different evidence classes. | Infer ownership after editing; freeze every sentence. |
| 2026-08-15 | Implement method and governed references together. | Loading, assessment, prepared recovery, dependencies, and assets must remain coherent. | Partial package rollout; several narrow references. |
| 2026-08-15 | Keep prepared manifests in Markdown authoring evidence. | Existing stage ownership is sufficient and avoids new architecture. | Parsed transaction schema; in-memory-only recovery. |
| 2026-08-15 | Measure real profiles and total package separately. | Relocation must not be presented as deletion. | Main-file-only or fixed-percentage acceptance. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
