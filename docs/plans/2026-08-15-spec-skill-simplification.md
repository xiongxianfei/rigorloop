# Spec Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `spec` package without weakening contract quality, portable authoring, boundary-first adoption, governed lifecycle authority, interrupted-authoring recovery, structural composition, or `spec-review` handoff. Freeze semantic and literal ownership first, refactor the canonical package second, and prove loaded-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-15-spec-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-15-spec-skill-simplification.md`
- Spec: `specs/spec-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-15-spec-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/spec-skill-simplification.test.md`

## Context and orientation

`skills/spec/` is the only authored package source. The change adds `references/governed-spec-authoring.md`, retains both existing boundary-first references with their current initial-loading contract, shortens the universal skill, and revises the existing skeleton with one conditional insertion point for the feature-authoring reference's formal boundary block.

Existing skill validators own canonical structure, resource mapping, closed vocabulary, and focused spec behavior. Existing boundary validation owns formal record structure and proof-map links. Existing adapter generation and validation own generated, archived, release-candidate, and temporary installed-tree proof. Change-local ledgers, scenarios, and measurements remain evidence rather than new validator or runtime systems.

## Non-goals

- Change spec purpose, requirement quality, examples, compatibility duties, boundary-first semantics, `spec-review` settlement, workflow order, downstream claims, or customer-project portability.
- Let workflow mutate spec-owned state or let spec settle review, route workflow, or write another stage's state.
- Add another structural asset, runtime classifier, target-agent evaluation, transcript grading, separate manual semantic-review gate, tokenizer dependency, or permanent simplicity validator.
- Change package roots, lifecycle schema, adapter transformation, publication behavior, or historical specifications.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R57-R65; BND-COMPAT-001, BND-ENV-001; INT-004 | M1 preservation inventories, scenarios, negative fixtures, and baseline measurement |
| R1-R62; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001-INT-003 | M2 canonical package, operations, recovery, structural composition, and focused validation |
| R63-R67; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004 | M3 measurement, semantic preservation, and canonical-through-installed proof |
| R21-R42, R43-R56, R57-R67 | M4 final holistic review, explanation, verification, and PR-boundary evidence |

## Milestones

### M1. Freeze spec rule, literal, and scenario ownership

- Milestone kind: implementation
- Goal: Account for every behaviorally significant rule and compatibility-sensitive literal and establish deterministic scenarios before moving procedure or structure.
- Requirements: R57-R65; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: none; architecture assessment is `architecture-not-required`.
- Files/components likely touched:
  - `docs/changes/2026-08-15-spec-skill-simplification/spec-rule-disposition.yaml`
  - `docs/changes/2026-08-15-spec-skill-simplification/spec-literal-compatibility.yaml`
  - `docs/changes/2026-08-15-spec-skill-simplification/fixtures/`
  - `docs/changes/2026-08-15-spec-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved spec and recorded `architecture-not-required` assessment
  - complete current `skills/spec/` package and exact literal consumers
- Tests and proof:
  - scenarios for both assemblies, tri-state governed signals, portable operations, governed transactions, exact retry, stale restart, partial-content states, formal boundary-block transitions, missing resources, and forbidden writes
  - unknown disposition and classification values fail before consistency checks
  - deterministic LF-normalized profile and package baselines
- Implementation steps:
  - inventory semantic rules with stable IDs, sources, requirements, profiles, dispositions, destinations, and proof
  - inventory exact-string consumers separately as normative, parser/package, incidental, obsolete, or historical
  - serialize ledgers and scenarios as JSON-compatible YAML and validate shape and closed values
  - record SA0 and SA1 baselines, representative output, duplicate clusters, resource counts, and total package size
- Validation commands:
  - run the exact M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-15-spec-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, duplicate cluster, and required scenario has one closed treatment before canonical skill prose moves.
- Completion criteria: M1 artifacts validate, unknown values fail first, and the canonical skill package remains unchanged.
- Required evidence: `docs/changes/2026-08-15-spec-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence and completeness.
- Optional commit boundary: `M1: freeze spec rule and literal ownership`
- Risks:
  - similar passages may encode different portable, boundary, or lifecycle behavior
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged

### M2. Separate universal spec policy from governed procedure

- Milestone kind: implementation
- Goal: Shorten `SKILL.md`, add the governed reference, and give the skeleton one conditional formal-block insertion point while preserving portable completeness and exact lifecycle authority.
- Requirements: R1-R62; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; INT-001-INT-003.
- Architecture decisions: existing published-skill package, stage-owned lifecycle, and boundary-first decisions; no new ADR.
- Files/components likely touched:
  - `skills/spec/SKILL.md`
  - `skills/spec/references/governed-spec-authoring.md`
  - `skills/spec/references/boundary-first-method-v1.md`
  - `skills/spec/references/boundary-first-feature-authoring-v1.md`
  - `skills/spec/assets/spec-skeleton.md`
  - `scripts/test-skill-validator.py`
  - directly coupled resource registrations and literal consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - exact SA0 and SA1 loads, forbidden loads, invalid-signal stops, and missing-resource failures
  - portable file-state operations and governed candidate-versus-authority validation
  - creation, revision, exact retry, commit points, collisions, stale detection, explicit restart authority, partial-content preservation, and concurrent writes
  - absent, empty, matching nonempty, unrelated, and unpreservable partial-file outcomes
  - all formal block and anchor states, adoption, preservation, deactivation, full rewrite, malformed structure, and no placeholders
- Implementation steps:
  - add failing focused assertions before changing canonical package text
  - retain universal contract, signal classification, stop, claim, and trigger rules inline while moving only governed procedure
  - author the governed reference with exact operations, retry identities, restart authority, preservation, write limits, and handoff
  - retain the two boundary references and their initial-loading behavior without semantic edits unless a true contract correction is required
  - revise the skeleton with one structural insertion point and migrate true literal consumers atomically
- Validation commands:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/test-skill-validator.py SpecSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: portable spec judgment remains complete from a shorter common path, governed procedure loads precisely, recovery preserves content and authority, and the existing asset owns ordinary layout plus one insertion point.
- Completion criteria: focused and broad skill tests pass, resource maps are valid, no universal rule is hidden, formal block ownership remains with the feature reference, and output contains no placeholders.
- Required evidence: `docs/changes/2026-08-15-spec-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the canonical package and validator changes.
- Optional commit boundary: `M2: simplify spec package paths`
- Risks:
  - a universal spec rule may move behind the governed trigger
  - restart logic may overwrite unattributable content or cross workflow and review ownership
  - skeleton changes may duplicate formal boundary structure
- Rollback/recovery:
  - restore the prior canonical skill and skeleton, remove the governed reference and focused assertions, and regenerate derived output atomically

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove loaded-profile reduction, semantic preservation, complete boundary proof, and canonical-through-installed integrity without target-agent execution or another semantic-review gate.
- Requirements: R63-R67; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: existing generated-package and resource-integrity architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct `spec` coverage is absent
  - `docs/changes/2026-08-15-spec-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-15-spec-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-15-spec-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - generated, packed, archived, release-candidate, and installed targets contain the governed reference, both boundary references, and skeleton at exact paths and bytes
  - missing, escaped, transformed, stale, additional, or mixed resources fail
  - every profile, resource, representative output, and total package measurement uses the approved deterministic convention
  - the approved proof map gives every applicable boundary and selected interaction direct proof
- Implementation steps:
  - extend only existing adapter proof where direct `spec` selection is absent
  - generate packages in a temporary directory and validate archive and clean-install parity
  - report before and after profiles, resources, representative output, total package, duplicate clusters, and mapped-resource counts
  - review the final package against both M1 ledgers and all 67 requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python -c 'exec("""import subprocess, sys, tempfile\nversion = "v0.4.0"\nwith tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:\n    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)\n    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "spec"], check=True)""")'`
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/spec-skill-simplification.md`
- Expected observable result: both procedural profiles shrink, semantics remain complete, every boundary has direct proof, and supported packages carry byte-identical resources.
- Completion criteria: measurements, preservation review, boundary validation, canonical validation, builds, archives, and clean-install parity pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of M3 evidence and the final package chain.
- Optional commit boundary: `M3: prove spec simplification`
- Risks:
  - generic adapter tests may pass without selecting `spec`
  - the main file may shrink while the real loaded profiles do not
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R21-R42, R43-R56, R57-R67.
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
- Optional commit boundary: `closeout: verify spec simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library ledger and fixture proof owns closed values, fields, unique IDs, scenarios, and unknown-value-first behavior.
- `python scripts/validate-skills.py skills/spec/SKILL.md` owns normalized package structure and resource maps.
- `python scripts/test-skill-validator.py SpecSkillSimplificationTests` owns focused package, classification, transaction, recovery, structure, and failure behavior.
- `python scripts/test-skill-validator.py`, `python scripts/test-build-skills.py`, and `python scripts/build-skills.py --check` own broad skill and generated-resource regression proof.
- `python scripts/test-adapter-distribution.py` and a temporary clean-installed `spec` selection own adapter package proof.
- `python scripts/validate-boundary-first.py --check --path specs/spec-skill-simplification.md` owns final boundary-to-proof structure after the test spec exists.
- Change metadata, review artifacts, ordinary code review, and human PR review own lifecycle structure and semantic judgment.

## Risks and recovery

- Risk: conditional extraction hides universal policy. Recovery: block on M1 disposition, portable scenarios, focused assertions, and review; restore the prior package atomically.
- Risk: stale restart exceeds stage authority or loses user-authored bytes. Recovery: prove exact current authorization, identity, attribution, snapshot, and write limits and stop on reliance, mismatch, or preservation failure.
- Risk: structural deduplication emits an incomplete or misplaced formal boundary block. Recovery: validate the insertion point and all block and anchor states while retaining semantic ownership in the feature reference.
- Risk: relocation appears as deletion. Recovery: report both loaded profiles, every resource, representative output, and total package.
- Risk: a derived target omits or transforms a reference. Recovery: block acceptance on archive and clean-install proof and regenerate from the last complete canonical revision.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing skill resource, boundary-first, spec-family asset, stage-owned lifecycle, and workflow-routing contracts.
- Existing skill validation, boundary validation, adapter generation, archive validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-15 | Use three implementation milestones plus lifecycle closeout. | Preservation, canonical package mutation, and derived-package proof have independent rollback and review boundaries. | One large rewrite; many tiny prose milestones. |
| 2026-08-15 | Freeze semantic and literal inventories before canonical edits. | Behavioral ownership and exact compatibility are different evidence classes. | Infer preservation after editing; freeze every asserted phrase. |
| 2026-08-15 | Implement governed procedure and skeleton insertion together. | Trigger, recovery, and output composition must remain internally consistent while both boundary references remain stable. | Partial package milestones; separate formal-block rewrite. |
| 2026-08-15 | Preserve nonempty stale content before same-entry restart. | Recovery must remain reviewable and non-destructive without a new persistence model. | Silent overwrite; workflow-owned spec mutation; new reset schema. |
| 2026-08-15 | Extend existing validators and measure loaded plus total content. | Durable invariants already have owners and simplification evidence is change-local. | New validator family; main-file-only metric; target-runtime journey. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code-review milestones, explanation, verification, and PR handoff remain.
