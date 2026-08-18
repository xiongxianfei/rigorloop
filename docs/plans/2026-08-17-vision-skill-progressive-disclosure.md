# Vision Skill Progressive Disclosure Execution Plan

## Purpose / big picture

Simplify the published `vision` package without weakening canonical vision ownership, state-based behavior, strategic positioning, README marker safety, identity-bound multi-file recovery, or truthful output. Freeze semantic and literal ownership first, refactor the canonical package second, and prove real-profile reduction plus package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md`
- Spec: `specs/vision-skill-progressive-disclosure.md`
- Architecture: not required; recorded in `docs/changes/2026-08-17-vision-skill-progressive-disclosure/architecture-assessment.md`
- Test spec: pending at `specs/vision-skill-progressive-disclosure.test.md`

## Context and orientation

`skills/vision/` is the sole authored package source and currently contains one flat `SKILL.md`. The change adds two conditional references and two copied structural assets. Existing skill validators own normalized structure and resource maps; build and adapter validation own derived package parity; current `specs/vision-skill.test.md` and focused consumers contain compatibility-sensitive exact phrases that must be classified before movement. Operation manifests remain invocation-local or ordinary change-local Markdown evidence rather than a new parsed schema.

## Non-goals

- Change project vision, strategic-positioning content, README front-matter, canonical paths, word limits, marker literals, public result vocabulary, or proposal-fit behavior.
- Add a runtime router, synchronization script, persistence surface, lifecycle state, authority owner, tokenizer, prose classifier, target-agent evaluation, or separate manual semantic-review gate.
- Rewrite historical vision artifacts or optimize another skill.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R58-R63; BND-COMPAT-001, BND-ENV-001; INT-004 | M1 ownership ledgers, scenarios, and baseline measurements |
| R1-R60; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-003 | M2 canonical package, resources, actions, manifests, recovery, and focused proof |
| R61-R66; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-004 | M3 profile reduction, preservation, boundary proof, and package parity |

## Milestones

### M1. Freeze vision rule, literal, scenario, and measurement ownership

- Milestone kind: implementation
- Goal: Account for every behavioral rule, compatibility-sensitive literal, required scenario, and baseline measurement before moving procedure or structure.
- Requirements: R58-R63; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: none; architecture assessment is `architecture-not-required`.
- Files/components likely touched:
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/vision-rule-disposition.yaml`
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/vision-literal-compatibility.yaml`
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/fixtures/`
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/profile-size-baseline.md`
- Dependencies:
  - approved focused spec and recorded no-architecture assessment
  - complete current vision package and exact consumers
- Tests and proof:
  - all six assemblies, operation and action vocabularies, pre-resolved and late skips, marker states, manifests, partial retry, assets, missing resources, and forbidden writes
  - unknown values fail before consistency checks
  - normalized baseline words and bytes for procedural resources and total package
- Implementation steps:
  - inventory semantic rules and duplicate clusters with stable owners and dispositions
  - classify exact headings, labels, paths, enums, markers, verbs, parser-sensitive phrases, and incidental assertions
  - serialize deterministic scenarios and negative unknown-value fixtures
  - record the flat baseline and six expected loaded-profile formulas
- Validation commands:
  - `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureLedgerTests`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-17-vision-skill-progressive-disclosure/change.yaml`
- Expected observable result: every current rule, literal, scenario, and measurement input has one closed treatment before canonical skill prose moves.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, and the canonical vision package remains unchanged.
- Required evidence: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze vision skill ownership`
- Risks:
  - similar marker or authority text may encode different universal and reference-owned behavior
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged

### M2. Separate universal, strategic, README, and structural ownership

- Milestone kind: implementation
- Goal: Shorten `SKILL.md`, add both references and assets, and preserve exact operations, authority, marker evidence, manifests, write order, and retry behavior.
- Requirements: R1-R60; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-003.
- Architecture decisions: existing mapped-resource and stage-owned evidence architecture; no new ADR.
- Files/components likely touched:
  - `skills/vision/SKILL.md`
  - `skills/vision/references/strategic-vision-authoring.md`
  - `skills/vision/references/readme-vision-sync.md`
  - `skills/vision/assets/vision-skeleton.md`
  - `skills/vision/assets/strategic-positioning-skeleton.md`
  - `scripts/test-skill-validator.py`
  - directly coupled consumers classified by M1
- Dependencies:
  - M1 and its code review are closed
- Tests and proof:
  - exact VA0, VA0S, VA1, VA1S, VA2, and VA2S loading plus missing-resource stops
  - repository-state and operation classification, significance escalation, independent secondary actions and assets
  - pre-resolved skip versus late skip, uninspected marker value, exact authority, zero-write result, and unknown values
  - manifest preparation, exact canonical and README transitions, source-first writes, interruption points, retries, lost context, and concurrency
  - skeleton composition, prospective adoption, no policy leakage, and no placeholders
- Implementation steps:
  - add failing focused assertions before canonical package edits
  - keep universal operation, authority, safety, stops, claims, triggers, and results inline
  - author strategic and README references from their M1-owned rules
  - create both structural-only assets and preserve narrow historical edits
  - migrate true literal consumers atomically
- Validation commands:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: normal sync and editorial paths load only applicable procedure, strategic paths retain full quality, and every skip or multi-target action remains authority- and identity-bound.
- Completion criteria: focused and broad skill tests pass, resource mappings and assets validate, and every universal or conditional rule has one loaded owner.
- Required evidence: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of canonical package and validators.
- Optional commit boundary: `M2: simplify vision package paths`
- Risks:
  - universal authority may move behind a trigger
  - no-reference skip may accidentally parse markers or omit settlement evidence
  - multi-file recovery may imply an unapproved state model
- Rollback/recovery:
  - restore the prior canonical package and focused assertions, remove new resources, and regenerate derived output atomically

### M3. Prove profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove six-profile reduction, semantic and literal preservation, complete boundary proof, and canonical-through-installed integrity.
- Requirements: R61-R66; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-004.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct vision selection is absent
  - `specs/vision-skill.test.md` only for directly coupled consolidated proof that must move with package ownership
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-17-vision-skill-progressive-disclosure/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - all six assemblies shrink from baseline and total package growth remains visible
  - generated, archived, release-candidate, and clean-installed targets contain byte-identical references and assets
  - missing, escaped, stale, extra, transformed, or mixed resources fail
  - approved proof map gives every applicable boundary and selected interaction direct proof
- Implementation steps:
  - extend only existing package proof when direct vision selection is absent
  - build and validate temporary package and installation trees
  - report before and after profiles, resources, assets, total package, and duplicate removal
  - compare the final package against M1 ledgers and every approved requirement
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/vision-skill-progressive-disclosure.md`
- Expected observable result: every supported procedural assembly shrinks and every supported package carries exact required resources without behavior loss.
- Completion criteria: measurement, preservation, boundary, canonical, build, archive, and clean-install proof pass with no unexplained profile growth.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove vision simplification`
- Risks:
  - generic adapter tests may omit direct vision selection
  - main-file reduction may hide loaded-profile or total-package growth
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R66.
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
- Optional commit boundary: `closeout: verify vision simplification`
- Risks:
  - a late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library proof owns closed ledgers, scenarios, unknown-value-first behavior, and baseline measurement.
- Skill validation owns canonical structure, resource mappings, and focused behavior.
- Build and adapter validation own generated, archived, release-candidate, and installed parity.
- Boundary validation owns final requirement-to-proof structure after the test spec exists.
- Change metadata, review artifacts, code review, and final PR-mode CI own lifecycle and holistic closeout.

## Risks and recovery

- Risk: extraction hides universal authority. Recovery: block on M1 ownership, all six assembly scenarios, focused assertions, and review.
- Risk: pre-resolved skip becomes a bypass. Recovery: bind exact owner instruction, whole README identity, uninspected marker state, and zero-write manifest proof.
- Risk: operation recovery becomes a hidden transaction system. Recovery: keep governed state in Markdown evidence, keep portable recovery fail-closed, and return to architecture if a new owner is required.
- Risk: relocation appears as deletion. Recovery: report all profiles, resources, assets, and total package separately.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing consolidated vision, skill-resource, lifecycle, workflow, build, adapter, and package-integrity contracts.
- Existing skill validation, adapter generation, archive validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-17 | Use three implementation milestones plus lifecycle closeout. | Ownership, canonical mutation, and package proof have independent rollback and review boundaries. | One large rewrite; many prose-only milestones. |
| 2026-08-17 | Freeze semantic and literal ownership before edits. | Behavioral meaning and exact compatibility are different evidence classes. | Infer ownership after editing; freeze every sentence. |
| 2026-08-17 | Implement both references and both assets together. | Resource triggers, skip evidence, strategic quality, and structure must remain coherent. | Partial package rollout; several narrow references. |
| 2026-08-17 | Keep operation manifests in invocation context or Markdown authoring evidence. | Existing ownership is sufficient and avoids new architecture. | Parsed transaction schema; silent cross-session adoption. |
| 2026-08-17 | Measure six real assemblies and total package separately. | Relocation must not be presented as deletion or hidden behind compact skip paths. | Main-file-only or primary-only metrics. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
