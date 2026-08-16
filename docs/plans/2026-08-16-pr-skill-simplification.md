# PR Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `pr` package without weakening verification binding, external-action authority, branch safety, existing-PR preservation, hosted-CI truthfulness, retry, or result claims. Freeze semantic and literal ownership first, implement the canonical `pr` package and directly coupled verify-evidence amendment second, and prove loaded-profile reduction plus package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-16-pr-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-16-pr-skill-simplification.md`
- Spec: `specs/pr-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-16-pr-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/pr-skill-simplification.test.md`

## Context and orientation

`skills/pr/` is the sole authored PR-skill package source. The change shortens its universal file, adds `references/governed-pr-readiness.md`, and adds `assets/pr-body-skeleton.md`. `skills/verify/` remains the sole owner of `branch-ready` and receives only the directly coupled normalized verification-basis result/report amendment and focused fixtures. Existing skill validation and adapter distribution tooling own resource mapping, generation, archive, release-candidate, and installed parity. No live PR or target-agent runtime is part of acceptance.

## Non-goals

- Change lifecycle routing, artifact settlement, merge, release, publication, reviewer, label, or deployment ownership.
- Add a PR provider engine, CLI, managed Markdown section parser, body-ownership protocol, persistent PR transaction schema, or new verify evidence owner.
- Optimize `verify` beyond the normalized immutable basis required by `pr`.
- Open a live acceptance PR or execute a target-agent runtime.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R42-R45; BND-COMPAT-001, BND-ENV-001; INT-003, INT-007, INT-008 | M1 rule, literal, verify-basis, scenario, and measurement baselines |
| R1-R41, R48-R49; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001-INT-008 | M2 canonical PR package, verify amendment, focused fixtures, and external-operation proof |
| R42-R47, R49; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | M3 profile reduction, semantic preservation, boundary proof, and package parity |
| R1-R49 | M4 lifecycle closeout after implementation |

## Milestones

### M1. Freeze PR rules, literals, verification basis, scenarios, and baselines

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule, compatibility-sensitive literal, existing verify-evidence representation, external-operation scenario, and measurement surface before canonical prose moves.
- Requirements: R42-R45; BND-COMPAT-001; BND-ENV-001; INT-003; INT-007; INT-008.
- Architecture decisions: none; architecture assessment is `architecture-not-required` while existing verify result/report evidence remains sufficient.
- Files/components likely touched:
  - `docs/changes/2026-08-16-pr-skill-simplification/pr-rule-disposition.yaml`
  - `docs/changes/2026-08-16-pr-skill-simplification/pr-literal-compatibility.yaml`
  - `docs/changes/2026-08-16-pr-skill-simplification/verify-basis-disposition.yaml`
  - `docs/changes/2026-08-16-pr-skill-simplification/fixtures/`
  - `docs/changes/2026-08-16-pr-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved specification and recorded architecture-not-required assessment
  - complete current `pr` and relevant `verify` contract surfaces and consumers
- Tests and proof:
  - every closed vocabulary rejects an unknown value before consistency checks
  - fixtures cover intent, independent authority, remote ancestry, PR state, CI, basis compatibility, evidence tail, reread, retry, concurrent creation, read-back, and forbidden mutation
  - current verify result/report and consumer forms have one classified migration to the normalized basis
  - LF-normalized baseline words and UTF-8 bytes are recorded for PR0, PR1, planned resources, representative body composition, and total package
- Implementation steps:
  - inventory universal, governed, structure, external-operation, CI, verify-basis, stop, claim, and exact-literal ownership
  - serialize deterministic positive and negative scenarios, including unknown-value fixtures
  - classify current portable and governed verify evidence and every incidental legacy representation
  - record deterministic baseline assemblies and content identities
- Validation commands:
  - run the M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-16-pr-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, verification representation, scenario, and measurement surface has one closed treatment before canonical edits.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, exact legacy compatibility is classified, and canonical skill packages remain unchanged.
- Required evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze pr simplification ownership`
- Risks:
  - similar wording may encode distinct opening, refresh, CI, or lifecycle authority
  - historical verify prose may be accidentally promoted to exact identity evidence
- Rollback/recovery:
  - revert M1 evidence only; canonical packages remain unchanged and route to architecture if existing evidence ownership is insufficient

### M2. Implement the PR package and normalized verify basis

- Milestone kind: implementation
- Goal: Shorten `pr/SKILL.md`, add the governed reference and structural asset, amend verify-owned result/report evidence, and close deterministic external-operation behavior.
- Requirements: R1-R41, R48-R49; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001; INT-001-INT-008.
- Architecture decisions: existing published-skill resource and verify evidence ownership; no new ADR.
- Files/components likely touched:
  - `skills/pr/SKILL.md`
  - `skills/pr/references/governed-pr-readiness.md`
  - `skills/pr/assets/pr-body-skeleton.md`
  - directly coupled `skills/verify/` result/report wording or existing reference
  - `specs/skill-contract.md` or another current owner only where the normalized verify basis requires an explicit contract amendment
  - `scripts/test-skill-validator.py`
  - focused fixtures and literal consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - tri-state governed signals, exact resource loading, and missing-resource stops
  - `prepare-only` zero writes; independent submission, refresh, and existing-state transition authority
  - all remote branch, PR, operation-result, and CI states, including unknown-value-first failures
  - exact normalized verify basis, legacy preparation-only compatibility, and one permitted evidence tail
  - base/head rereads, remote containment, concurrent matching PR creation, idempotent reuse, title-only and whole-body refresh, body-byte preservation, and final read-back
  - no force, delete, overwrite, duplicate PR, lifecycle mutation, section parser, or external-ready overclaim
- Implementation steps:
  - add failing focused assertions and fixtures before canonical package edits
  - keep universal target, verification, branch, PR, CI, operation, stop, claim, and read-back policy inline
  - author the governed-readiness reference from lifecycle aggregation rules only
  - author the structural PR-body asset without policy text or unfilled placeholders
  - amend the current verify-owned result/report contract with immutable repository, remote, base, merge-base, head, and subject identities
  - migrate exact consumers atomically and preserve historical evidence as preparation-only input
- Validation commands:
  - `python scripts/validate-skills.py skills/pr/SKILL.md skills/verify/SKILL.md`
  - run the focused PR simplification test class named by the test spec
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: portable PR work remains self-sufficient and smaller, governed evidence loads one read-only reference, body layout has one asset owner, and opening is bound to an exact current verify basis and safe remote state.
- Completion criteria: focused and broad skill tests pass, every operation and authority combination has one result, no new architecture owner appears, and existing unsafe or legacy evidence fails closed.
- Required evidence: `docs/changes/2026-08-16-pr-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of canonical PR/verify contract and focused tests.
- Optional commit boundary: `M2: simplify pr package and bind verify basis`
- Risks:
  - universal submission safety may move behind the governed trigger
  - the verify amendment may accidentally transfer branch-ready ownership to `pr`
  - external writes may occur from stale preflight evidence
- Rollback/recovery:
  - restore the prior flat PR package and prior verify wording and regenerate derived output atomically

### M3. Prove real-profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove semantic preservation, complete boundary coverage, PR0 and PR1 reduction, and canonical-through-installed resource integrity.
- Requirements: R42-R47, R49; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct PR/verify resource selection coverage is absent
  - `docs/changes/2026-08-16-pr-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-16-pr-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-16-pr-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - PR0 and PR1 words and bytes decrease from the flat baseline; asset, representative composition, and total package are reported separately
  - every rule, literal, and verify-basis representation has one final disposition
  - every applicable boundary and interaction has direct proof in the approved test spec
  - generated, archived, release-candidate, and clean-installed packages contain byte-identical mapped resources
- Implementation steps:
  - extend only existing package proof when direct PR selection coverage is absent
  - build and validate temporary package and installed trees
  - report before/after assemblies, resources, duplicates, and total package without presenting relocation as deletion
  - compare the final package with M1 ledgers, R1-R49, and AC-PRSIM-001 through AC-PRSIM-020
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/pr/SKILL.md skills/verify/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/pr-skill-simplification.md`
- Expected observable result: both real PR procedural profiles shrink and every supported generated or installed package carries exact required resources.
- Completion criteria: measurement, preservation, boundary, canonical, build, archive, release-candidate, and clean-install proof pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove pr skill simplification`
- Risks:
  - generic adapter tests may omit direct PR package selection
  - a smaller main file may hide governed or representative growth
- Rollback/recovery:
  - restore the prior package and verify wording, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R49.
- Architecture decisions: none.
- Files/components likely touched:
  - final review records, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M3 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and the complete approved test-spec command ledger
- Implementation steps:
  - run final holistic `code-review`, resolve and rereview findings, record rationale, and run final `verify`
- Validation commands:
  - use the complete approved test-spec commands
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports truthful PR handoff state.
- Completion criteria: final review is clean, rationale is current, verification is recorded, and no blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate authority.
- Optional commit boundary: `closeout: verify pr skill simplification`
- Risks:
  - late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library proof owns closed ledgers, compatibility classifications, scenarios, baselines, and unknown-value-first behavior.
- Focused skill validation owns canonical structure, resource mapping, intent and authority matrices, verify-basis compatibility, remote state, read-back, CI, and forbidden mutation.
- Build and adapter validation own generated, archived, release-candidate, and installed parity.
- Boundary validation owns final requirement-to-proof structure after the test spec exists.
- Change metadata, review artifacts, code review, verification, and PR review own lifecycle and semantic judgment.

## Risks and recovery

- Risk: extraction hides universal submission safety. Recovery: block on M1 ownership, PR0 scenarios, focused assertions, and review.
- Risk: normalized verify evidence becomes a new state owner. Recovery: keep it on existing result/report surfaces and return to architecture if a new schema is required.
- Risk: stale remote evidence causes destructive or duplicate writes. Recovery: require directional ancestry, repeated base/head/PR reads, exact read-back, and non-force fixtures.
- Risk: relocation appears as deletion. Recovery: report all assemblies, resources, duplicate ownership, and total package.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing published-skill resource, verify evidence, stage-owned lifecycle, and workflow-routing contracts.
- Existing skill validation, adapter generation, archive validation, release-candidate validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-16 | Use three implementation milestones plus lifecycle closeout. | Preservation, canonical mutation, and package proof have independent rollback and review boundaries. | One large rewrite; many prose-only milestones. |
| 2026-08-16 | Freeze verify-basis compatibility before edits. | Historical prose must not be silently promoted to immutable identity evidence. | Infer the basis during PR opening; migrate after implementation. |
| 2026-08-16 | Implement PR and directly coupled verify changes in one milestone. | Producer and consumer contracts must remain atomic. | Split producer and consumer across milestones. |
| 2026-08-16 | Exclude section-level body mutation. | Whole-body preservation avoids a new parser and ownership architecture. | Hidden markers; heading-based parsing. |
| 2026-08-16 | Measure both real procedural profiles and total package separately. | Relocation must not be presented as deletion. | Main-file-only or fixed-percentage acceptance. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
