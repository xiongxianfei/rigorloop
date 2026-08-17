# Learn Skill Simplification Execution Plan

## Purpose / big picture

Simplify the published `learn` package without weakening trigger safety, evidence quality, contributor confirmation, durable session recording, topic ownership, owner-bound derivative routing, or claim boundaries. Freeze semantic and literal ownership first, align the authoritative learn contract and canonical package second, and prove real-profile reduction and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-16-learn-skill-simplification/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-16-learn-skill-simplification.md`
- Spec: `specs/learn-skill-simplification.md`
- Architecture: not required; recorded in `docs/changes/2026-08-16-learn-skill-simplification/architecture-assessment.md`
- Test spec: pending at `specs/learn-skill-simplification.test.md`

## Context and orientation

`skills/learn/` is the sole authored package source. The change shortens the universal skill, adds `references/session-method.md`, adds no asset or script, removes the unsupported trigger-assessment surface, and introduces a narrow `record-learn-route-result` operation for prospective stable route IDs. Existing learn sessions and topics remain Markdown evidence under `docs/learn/`; historical sessions are not migrated. The existing package builders and adapter checks own derived-resource parity.

The approved focused spec amends legacy direct-write wording: learn records confirmed routes and exact owner-result backlinks, while destination owners perform authoritative mutations under their own contracts. The implementation must align `specs/learn-artifact-model.md` and its proof map atomically so two active writer rules do not remain.

## Non-goals

- Change the four-phase learning method, trigger cadence, seven primary classifications, contributor-confirmation standard, learn namespace, topic authority, or destination review gates.
- Add trigger assessment, phase-resume state, a route registry, background polling, a cross-stage coordinator, external integration, templates, scripts, a learning engine, or a new lifecycle owner.
- Migrate historical sessions, infer route IDs, or treat route completion as destination approval, acceptance, implementation, release, or workflow settlement.
- Optimize another skill except for directly coupled caller and contract compatibility.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R36-R47; BND-COMPAT-001, BND-ENV-001; INT-005 | M1 semantic and literal ledgers, legacy disposition inventory, architecture-trigger inspection, deterministic scenarios, and profile baselines |
| R1-R35, R47; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001-INT-004 | M2 focused learn-contract alignment, canonical package split, stable routes, and bounded result recording |
| R37-R45; BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001; INT-005 | M3 both-profile reduction, semantic preservation, boundary proof, and canonical-through-installed parity |

## Milestones

### M1. Freeze learn rules, literals, scenarios, and measurement baselines

- Milestone kind: implementation
- Goal: Account for every behaviorally significant learn rule, compatibility-sensitive literal, legacy cross-spec disposition, route scenario, and real loaded profile before moving procedure.
- Requirements: R36-R47; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: none; architecture assessment is `architecture-not-required` because existing Markdown sessions can carry stable routes without new persistence ownership.
- Files/components likely touched:
  - `docs/changes/2026-08-16-learn-skill-simplification/learn-rule-disposition.yaml`
  - `docs/changes/2026-08-16-learn-skill-simplification/learn-literal-compatibility.yaml`
  - `docs/changes/2026-08-16-learn-skill-simplification/fixtures/`
  - `docs/changes/2026-08-16-learn-skill-simplification/evidence/profile-size-baseline.md`
- Dependencies:
  - approved specification, approving spec rereview, and recorded architecture assessment
  - complete current learn skill, artifact-model contract and proof map, trigger callers, and package consumers
- Tests and proof:
  - rule and literal vocabularies reject unknown values before consistency checks
  - exact dispositions cover legacy R21-R24, R33, Example E3, affected output and acceptance surfaces, and every current direct-write phrase
  - the inventory proves whether persistent phase or effect state, polling, external integration, a new state owner, or cross-owner mutation is required and records the no-trigger result before M2
  - scenarios cover both operations, trigger-owner closeout, same-day collisions, partial files, complete reruns, confirmation, topic effects, stable routes, completion-kind mismatch, exact backlinks, historical sessions, missing resources, and forbidden writes
  - LF-normalized baseline words and UTF-8 bytes are recorded for LR0, LR1, each resource, and total package
- Implementation steps:
  - inventory universal, session-method, topic, route, result-recording, stop, claim, and exact-literal ownership with one disposition per item
  - inventory every current caller and contract surface affected by removal of trigger assessment or direct learn destination writes
  - compare the required session, topic, route, retry, and owner-result behavior with R46's reassessment triggers before authorizing canonical mutation
  - serialize deterministic positive and negative scenarios, including unknown operation, settlement, completion-kind, and classification values
  - record canonical input identities and deterministic profile assemblies
- Validation commands:
  - run the M1 standard-library ledger and fixture command defined by the test spec
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-16-learn-skill-simplification/change.yaml`
- Expected observable result: every current rule, literal, caller, scenario, and measurement surface has one closed treatment before canonical procedure moves.
- Completion criteria: ledgers and fixtures validate, unknown values fail first, cross-spec dispositions are complete, baselines are reproducible, no R46 architecture trigger is present, and the canonical learn package remains unchanged.
- Required evidence: `docs/changes/2026-08-16-learn-skill-simplification/evidence/m1-preservation-inventories.md`
- Review handoff: independent `code-review` of M1 evidence.
- Optional commit boundary: `M1: freeze learn simplification ownership`
- Risks:
  - legacy routing prose may encode direct mutation in examples or outputs outside numbered requirements
  - literal fixtures may accidentally freeze incidental wording
  - implementation evidence may reveal persistent recovery or coordination needs excluded by the assessment
- Rollback/recovery:
  - revert M1 evidence only; canonical package remains unchanged, any unresolved authority conflict returns to `spec`, and any R46 trigger stops the plan and returns to architecture assessment before M2

### M2. Align the learn contract and split the canonical package

- Milestone kind: implementation
- Goal: Align authoritative routing language, shorten `SKILL.md`, add the session-method reference, and implement prospective stable routes plus bounded owner-result recording.
- Requirements: R1-R35, R47; BND-INPUT-001; BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; INT-001-INT-004.
- Architecture decisions: existing published-skill package and learn Markdown artifact model; no new ADR.
- Files/components likely touched:
  - `specs/learn-artifact-model.md`
  - `specs/learn-artifact-model.test.md`
  - `skills/learn/SKILL.md`
  - `skills/learn/references/session-method.md`
  - `scripts/test-skill-validator.py`
  - directly coupled workflow guidance or caller assertions identified by M1
- Dependencies:
  - M1 and its code review are closed with an explicit no-R46-trigger result
- Tests and proof:
  - exact LR0 and LR1 resource loading, one-time reference loading, and missing-resource stops
  - explicit direct invocation, no public assessment operation, trigger-owner pre-session closeout, and unknown-operation failure
  - unique session paths, lowest available suffix, absence recheck, partial-file no-resume, complete-session idempotency, changed basis, and concurrency stops
  - confirmation-gated topic and route effects with no destination mutation authority
  - `ROUTE-NNN` assignment, complete route fields, closed completion kinds and settlements, valid and mismatched owner results, idempotent backlink, conflicting backlink, and historical-session rejection
  - exact prospective alignment of the legacy artifact-model contract and proof map
- Implementation steps:
  - add failing focused assertions and contract fixtures before canonical package edits
  - amend legacy routing requirements and affected prose to name destination owners while retaining mandatory authoritative outcomes
  - keep universal trigger, evidence, confirmation, ownership, sensitive-data, stop, claim, and resource-selection rules inline
  - author `session-method.md` from the detailed four-phase method, evidence selection, classification, topic curation, and route construction rules
  - implement the narrow route-result operation and prospective route structure without polling, recovery state, or cross-owner mutation
  - update only directly coupled callers and validators identified by M1
- Validation commands:
  - `python scripts/validate-skills.py skills/learn/SKILL.md`
  - `python scripts/test-skill-validator.py LearnSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: ordinary route-result recording loads only the universal skill, every real session loads one complete method reference, and learn-owned writes remain limited to sessions, confirmed topic guidance, and exact route backlinks.
- Completion criteria: focused and broad skill tests pass, legacy writer conflict is removed, every operation and route boundary has one loaded owner, and no new persistence or destination authority appears.
- Required evidence: `docs/changes/2026-08-16-learn-skill-simplification/evidence/m2-package-implementation.md`
- Review handoff: independent `code-review` of the focused contract, canonical package, and validator changes.
- Optional commit boundary: `M2: simplify learn package paths`
- Risks:
  - universal confirmation or sensitive-data safety may move behind the session trigger
  - legacy direct-write wording may survive in a sibling contract surface
  - completion may overclaim destination lifecycle state
- Rollback/recovery:
  - restore the prior contract and canonical package atomically and regenerate derived output; do not rewrite historical learn artifacts

### M3. Prove both-profile reduction and package parity

- Milestone kind: implementation
- Goal: Prove LR0 and LR1 reduction, semantic preservation, complete boundary proof, and canonical-through-installed resource integrity.
- Requirements: R37-R45; BND-COMPOSE-001; BND-COMPAT-001; BND-ENV-001; INT-005.
- Architecture decisions: existing resource-integrity and adapter-package architecture; no new ADR.
- Files/components likely touched:
  - `scripts/test-adapter-distribution.py` only if direct learn-resource selection coverage is absent
  - `docs/changes/2026-08-16-learn-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-16-learn-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-16-learn-skill-simplification/evidence/m3-package-proof.md`
- Dependencies:
  - M2 and its code review are closed
- Tests and proof:
  - LR0 and LR1 each decrease in words and bytes from the 1,712-word and 12,375-byte baseline; resources and total package are reported separately
  - every semantic rule, legacy disposition, and exact literal has one classified final treatment
  - generated, archived, release-candidate, and clean-installed packages contain byte-identical required resources
  - missing, escaped, transformed, stale, extra, or mixed resources fail
  - the approved proof map gives every applicable boundary and selected interaction direct proof
- Implementation steps:
  - extend only existing package proof when direct learn-resource selection is absent
  - build and validate temporary package and installation trees
  - report before and after assemblies, resources, duplicate ownership, and total package without presenting relocation as deletion
  - compare the final package and amended artifact-model contract with the M1 ledgers and all approved requirements
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-skills.py skills/learn/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-boundary-first.py --check --path specs/learn-skill-simplification.md`
- Expected observable result: both real loaded profiles shrink and every supported package carries the exact required reference and semantics.
- Completion criteria: measurement, preservation, boundary, canonical, build, archive, release-candidate, and clean-install proof pass with no unexplained profile growth or unresolved literal.
- Required evidence: simplification measurements, semantic preservation review, and M3 package proof.
- Review handoff: independent `code-review` of final package-chain evidence.
- Optional commit boundary: `M3: prove learn simplification`
- Risks:
  - generic adapter tests may omit direct learn-reference selection
  - a smaller session profile may hide route-result common-path growth
- Rollback/recovery:
  - restore the prior package, regenerate every derived target, and discard temporary trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Obtain final holistic review, close findings, explain the change, verify branch readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R47.
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
- Optional commit boundary: `closeout: verify learn simplification`
- Risks:
  - a late cross-milestone contract or package inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 standard-library proof owns closed ledgers, legacy dispositions, static scenarios, unknown-value-first behavior, and deterministic baselines.
- Focused skill validation owns operation selection, universal ownership, route structure, completion-kind matching, and reference mapping.
- Existing artifact-model proof owns the amended authoritative-output obligations and learn/destination ownership split.
- Build and adapter validation own generated, archived, release-candidate, and installed parity.
- Boundary validation owns final requirement-to-proof structure after the test spec exists.
- Change metadata, review artifacts, code review, verification, and PR review own lifecycle and semantic judgment.

## Risks and recovery

- Risk: extraction hides universal learn safety. Recovery: block on M1 ownership, LR0 scenarios, focused assertions, and review.
- Risk: cross-spec clarification weakens mandatory authoritative updates. Recovery: prove both the owner-produced result and exact learn backlink while forbidding direct learn mutation.
- Risk: route result recording expands into coordination. Recovery: require explicit identities, one matching route write, and negative proof for polling, discovery, workflow, topic, and destination changes.
- Risk: relocation appears as deletion. Recovery: report both profiles, the reference, duplicate ownership, and total package.

## Dependencies

- Accepted proposal, approved spec, clean reviews, closed findings, and recorded `architecture-not-required` assessment.
- Existing published-skill resource, learn artifact model, stage-owned lifecycle, workflow-routing, and adapter-package contracts.
- Existing skill validation, adapter generation, archive validation, release-candidate validation, and clean-install owners.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-17 | Use three implementation milestones plus lifecycle closeout. | Ownership, contract/package mutation, and distribution proof have independent rollback and review boundaries. | One large rewrite; many prose-only milestones. |
| 2026-08-17 | Align legacy writer wording in the package milestone. | The canonical skill and authoritative learn contract must change atomically so no competing writer rule survives. | Defer contract alignment; let learn mutate destinations. |
| 2026-08-17 | Keep interruption fail-closed and route results explicit. | This preserves traceability without persistent phase state, polling, or coordination architecture. | Transaction recovery; route reconciliation engine. |
| 2026-08-17 | Measure both real profiles and total package separately. | Moving procedure to a reference is useful only if both actual paths shrink. | Main-file-only or LR1-only acceptance. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
