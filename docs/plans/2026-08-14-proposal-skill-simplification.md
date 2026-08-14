# Proposal Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `proposal` package without weakening decision quality, intent preservation, standing gates, governed authoring, stale recovery, structural composition, or lifecycle ownership. Freeze semantic and literal ownership first, refactor the package second, and prove loaded-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-14-proposal-skill-simplification.md`
- Spec: `specs/proposal-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-14-proposal-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/proposal-skill-simplification.test.md`

## Context and orientation

`skills/proposal/` is the only authored package source. The change adds `references/governed-proposal-authoring.md` and `references/strategic-and-scope-gates.md`, shortens the universal skill, and revises the existing skeleton so core and four conditional groups have one layout owner.

Existing skill validators own canonical structure, resource mapping, closed vocabulary, and focused proposal behavior. Existing adapter generation and validation own generated, archived, release-candidate, and temporary installed-tree proof. Change-local ledgers, scenarios, and measurements remain evidence rather than new validator or runtime systems.

## Non-goals

- Change proposal purpose, vision or scope vocabularies, proposal-review settlement, workflow order, downstream claims, or customer-project portability.
- Let workflow mutate proposal-owned state or let proposal create a change root, settle review, route workflow, or write another stage's state.
- Add another template, result asset, runtime classifier, target-agent evaluation, separate manual semantic-review gate, or permanent simplicity validator.
- Change package roots, lifecycle schema, adapter transformation, publication behavior, or historical proposals.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R41-R47; BND-COMPAT-001, BND-ENV-001; INT-004 | M1 preservation inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R40, R44; all input, state, authority, composition, temporal, and recovery boundaries; INT-001-INT-003 | M2 canonical package, transactions, recovery, structural composition, and focused validation |
| R45-R49; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004 | M3 measurement, semantic preservation, and canonical-through-installed proof |
| R21, R25-R32, R41-R49 | M4 final holistic review, explanation, verification, and PR-boundary evidence |

## Milestones

### M1. Freeze proposal rule, literal, and scenario ownership

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal and establish deterministic scenarios before moving procedure or structure.
- Requirements: R41-R47; BND-COMPAT-001; BND-ENV-001; INT-004.
- Files/components likely touched:
  - `docs/changes/2026-08-14-proposal-skill-simplification/proposal-rule-disposition.yaml`
  - `docs/changes/2026-08-14-proposal-skill-simplification/proposal-literal-compatibility.yaml`
  - `docs/changes/2026-08-14-proposal-skill-simplification/fixtures/`
  - `docs/changes/2026-08-14-proposal-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec and recorded `architecture-not-required` assessment
  - complete current `skills/proposal/` package and exact literal consumers
- Tests and proof:
  - scenarios for all four assemblies, portable operations, governed transactions, stale reset, downstream reliance, group composition, resource failure, and forbidden writes
  - unknown disposition and classification values fail before consistency checks
  - deterministic LF-normalized profile and package baselines
- Implementation steps:
  - inventory semantic rules with stable IDs, sources, requirements, assemblies, dispositions, destinations, and proof
  - inventory exact-string consumers separately as normative, parser/package, incidental, obsolete, or historical
  - serialize ledgers and scenarios as JSON-compatible YAML and validate shape and closed values
  - record PA0, PA0G, PA1, PA1G-equivalent baselines, representative output, duplicate clusters, and total package size
- Validation commands:
  - run the exact M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-14-proposal-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, duplicate cluster, and required scenario has one closed treatment before canonical skill prose moves.
- Completion criteria: M1 artifacts validate, unknown values fail first, and the canonical skill package remains unchanged.
- Required evidence: `docs/changes/2026-08-14-proposal-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence and completeness.
- Optional commit boundary: `M1: freeze proposal rule and literal ownership`
- Risks:
  - similar passages may encode different standing-gate or lifecycle behavior
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged

### M2. Separate universal proposal policy from conditional procedure

- Milestone kind: implementation
- Goal: Shorten `SKILL.md`, create both independently triggered references, and make the existing skeleton the sole structural owner while preserving exact lifecycle authority.
- Requirements: R1-R40, R44; BND-INPUT-001; BND-INPUT-002; BND-STATE-001; BND-STATE-002; BND-AUTH-001; BND-AUTH-002; BND-COMPOSE-001; BND-COMPOSE-002; BND-TEMPORAL-001; BND-RECOVERY-001; BND-RECOVERY-002; INT-001-INT-003.
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal/references/governed-proposal-authoring.md`
  - `skills/proposal/references/strategic-and-scope-gates.md`
  - `skills/proposal/assets/proposal-skeleton.md`
  - `scripts/test-skill-validator.py`
  - directly coupled resource registrations and literal consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - exact PA0, PA0G, PA1, and PA1G loads, forbidden loads, late triggers, and resource failures
  - portable file-state operations and governed candidate-versus-authority validation
  - creation, revision, exact retry, commit points, collisions, and concurrent writes
  - workflow authorization, proposal-owned reset, idempotent consumption, changed reliance, and forbidden cross-owner writes
  - every specialized predicate combination, explicit blockers, omitted groups, and no placeholders
- Implementation steps:
  - add failing focused assertions before changing canonical package text
  - retain universal decision, stop, claim, and trigger rules inline while moving only conditional procedure
  - author the governed reference with exact operations, retry identities, authorized reset, write limits, and handoff
  - author the strategic reference with all four predicate procedures and independent composition
  - revise the skeleton so it owns layout only and migrate true literal consumers atomically
- Validation commands:
  - `python scripts/validate-skills.py skills/proposal/SKILL.md`
  - `python scripts/test-skill-validator.py ProposalSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: portable proposal judgment remains complete from a shorter common path, conditional procedure loads precisely, recovery preserves ownership, and one asset owns layout.
- Completion criteria: focused and broad skill tests pass, resource maps are valid, no universal rule is hidden, and output contains no policy-bearing asset text or placeholders.
- Required evidence: `docs/changes/2026-08-14-proposal-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the canonical package and validator changes.
- Optional commit boundary: `M2: simplify proposal package paths`
- Risks:
  - a universal proposal rule may move behind a trigger
  - reset logic may cross workflow or review ownership
- Rollback/recovery:
  - restore the prior canonical skill and skeleton, remove both references and focused assertions, and regenerate derived output atomically

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove loaded-profile reduction, semantic preservation, and canonical-through-installed integrity without target-agent execution or another manual review gate.
- Requirements: R45-R49; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct `proposal` coverage is absent
  - `docs/changes/2026-08-14-proposal-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-14-proposal-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-14-proposal-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - generated, packed, archived, release-candidate, and installed targets contain both references and the skeleton at exact paths and bytes
  - missing, escaped, transformed, stale, or mixed resources fail
  - every profile, resource, representative output, and total package measurement uses the approved deterministic convention
- Implementation steps:
  - extend only existing adapter proof where direct `proposal` selection is absent
  - generate packages in a temporary directory and validate archive and clean-install parity
  - report before and after profiles, resources, representative output, total package, duplicate clusters, and mapped-resource counts
  - review the final package against both M1 ledgers and all 49 requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - temporary `build-adapters.py` plus `validate-adapters.py --clean-install-smoke --skill proposal`
  - `python scripts/validate-skills.py skills/proposal/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/proposal-skill-simplification.md`
- Expected observable result: all procedural profiles shrink or carry an approved exception, semantics remain complete, and supported packages carry byte-identical resources.
- Completion criteria: measurements, semantic review, canonical validation, builds, archives, and clean-install parity pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of M3 evidence and the final package chain.
- Optional commit boundary: `M3: prove proposal simplification`
- Risks:
  - generic adapter tests may pass without selecting `proposal`
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R21, R25-R32, R41-R49.
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
- Optional commit boundary: `closeout: verify proposal simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library ledger and fixture proof owns closed values, fields, unique IDs, scenarios, and unknown-value-first behavior.
- `python scripts/validate-skills.py skills/proposal/SKILL.md` owns normalized package structure and resource maps.
- `python scripts/test-skill-validator.py ProposalSkillSimplificationTests` owns focused package, transaction, structure, and failure behavior.
- `python scripts/test-skill-validator.py`, `python scripts/test-build-skills.py`, and `python scripts/build-skills.py --check` own broad skill and generated-resource regression proof.
- `python scripts/test-adapter-distribution.py` and a temporary clean-installed `proposal` selection own adapter package proof.
- `python scripts/validate-boundary-first.py --check --path specs/proposal-skill-simplification.md` owns final boundary-to-proof structure after the test spec exists.
- Change metadata, review artifacts, ordinary code review, and human PR review own lifecycle structure and semantic judgment.

## Risks and recovery

- Risk: conditional extraction hides universal policy. Recovery: block on M1 disposition, portable scenarios, focused assertions, and review; restore the prior package atomically.
- Risk: reset or revision exceeds stage authority. Recovery: prove exact authorization and writes and stop on reliance, identity, or concurrency mismatch.
- Risk: structural deduplication emits an incomplete proposal. Recovery: require core and applicable groups and reject placeholders.
- Risk: relocation appears as deletion. Recovery: report every loaded profile, representative output, and total package.
- Risk: a derived target omits a reference. Recovery: block acceptance on archive and clean-install proof and regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing skill resource, proposal-family asset, stage-owned lifecycle, and workflow-routing contracts.
- Existing skill validation, adapter generation, archive validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-14 | Use three implementation milestones plus lifecycle closeout. | Preservation, package mutation, and derived-package proof have independent rollback and review boundaries. | One large rewrite; many tiny prose milestones. |
| 2026-08-14 | Freeze semantic and literal inventories before canonical edits. | Behavioral ownership and exact compatibility are different evidence classes. | Infer preservation after editing; freeze every asserted phrase. |
| 2026-08-14 | Implement both references and skeleton composition together. | Trigger, ownership, and output applicability must remain internally consistent. | Partially functional package milestones. |
| 2026-08-14 | Test workflow authorization and proposal reset as one slice. | Recovery safety depends on both sides without crossing write ownership. | Direct workflow reset; unbounded proposal reset. |
| 2026-08-14 | Extend existing validators and measure loaded plus total content. | Durable invariants already have owners and simplification evidence is change-local. | New validator family; main-file-only metric; target-runtime journey. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
