# Bugfix Skill Simplification Execution Plan

## Purpose / big picture

Replace the small but ambiguous published bugfix workflow with a truthful one-file contract that deterministically separates diagnosis, commands, writes, proof authoring, production correction, validation, owner routing, results, and handoff. Freeze semantic compatibility first, implement the compact contract second, and prove truthful measurements and package parity third.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`

Mutable lifecycle state, milestone progress, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-08-20-bugfix-skill-simplification.md`
- Spec: `specs/bugfix-skill-simplification.md`
- Architecture: `docs/changes/2026-08-20-bugfix-skill-simplification/architecture-assessment.md`; not required
- Test spec: `specs/bugfix-skill-simplification.test.md`, pending

## Context and orientation

`skills/bugfix/SKILL.md` is the only authored package source and has no references, assets, or scripts. The change is a semantic compression, not progressive disclosure. Existing skill validation, build, adapter distribution, archive, release-candidate, and clean-install tooling remains authoritative for package integrity.

The principal hazards are behavioral loss during compression, circular regression-test gating, authority broadening, overlapping action rows, proof identity drift, cross-owner mutation, and misleading completion claims. The approved boundary record gives each hazard stable ownership and direct proof requirements.

## Non-goals

- Add a reference, asset, template, packaged script, diagnosis skill, runtime engine, issue integration, or persistent bug state.
- Execute a live repair, target agent, external system, hosted CI, or PR operation.
- Change workflow autoprogression, upstream artifact ownership, or unrelated skills.
- Rewrite historical bugfix evidence merely to adopt the new wording.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| R1, R21, R25-R27; BND-COMPAT-001, BND-ENV-001; INT-005, INT-006 | M1 preservation inventory, literal consumers, scenario fixtures, package baseline, and architecture-trigger check |
| R2-R22, R24-R25; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001 through INT-005 | M2 focused contract tests and canonical one-file rewrite |
| R1, R23-R27; all boundaries and interactions | M3 full proof, measurements, semantic reconciliation, and package parity |
| R1-R27 | M4 lifecycle closeout after all implementation milestones |

## Milestones

### M1. Freeze semantic, literal, scenario, and size baselines

- Milestone kind: implementation
- Goal: Account for every current rule and consumer-sensitive literal, serialize the approved state machines, and capture reproducible package measurements before editing the canonical skill.
- Requirements: R1, R21, R25-R27; BND-COMPAT-001; BND-ENV-001; INT-005; INT-006.
- Architecture decisions: architecture-not-required assessment; stop and reassess on any recorded trigger.
- Files/components likely touched:
  - `docs/changes/2026-08-20-bugfix-skill-simplification/bugfix-rule-disposition.yaml`
  - `docs/changes/2026-08-20-bugfix-skill-simplification/bugfix-literal-compatibility.yaml`
  - `docs/changes/2026-08-20-bugfix-skill-simplification/fixtures/`
  - `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/profile-size-baseline.md`
  - `scripts/test-skill-validator.py`
- Dependencies:
  - approved spec, clean spec review, and architecture assessment
  - current skill, skill contract, workflow contract, validators, package builders, and adapter consumers
- Tests and proof:
  - every meaningful legacy rule has exactly one retained, amended, relocated, removed-duplicate, or incidental disposition and one current owner
  - every parser- or documentation-sensitive literal has one preserved or atomically migrated consumer treatment
  - fixtures cover every closed value, action row, proof row, boundary, interaction, negative state, owner route, and forbidden claim
  - normalized word and byte baselines reproduce the current root and complete package
- Implementation steps:
  - inventory the current skill line by line and search direct consumers
  - build deterministic scenario fixtures from the approved requirements and boundaries
  - add failing unknown-value, overlap, reachability, authority, proof, write-boundary, routing, and claim tests before canonical edits
  - record exact measurement inputs and formulas
  - stop for architecture if any persistent or external owner becomes necessary
- Validation commands:
  - `python scripts/test-skill-validator.py BugfixSkillSimplificationTests`
  - `python scripts/validate-change-metadata.py docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`
- Expected observable result: compatibility, scenario, and size baselines are deterministic while `skills/bugfix/SKILL.md` remains unchanged.
- Completion criteria: inventories have no unknown dispositions, fixtures cover every approved row, unknown values fail first, measurements reproduce, and no architecture trigger is present.
- Required evidence: `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/m1-preservation-and-baseline.md`
- Review handoff: independent `code-review` of M1 inventories, fixtures, tests, and baseline evidence.
- Optional commit boundary: `M1: freeze bugfix simplification behavior`
- Risks:
  - incidental prose becomes a false compatibility requirement
  - a meaningful stop or claim boundary is missed because no parser consumes it
- Rollback/recovery:
  - revert M1 evidence and focused tests only; return normative gaps to spec and architecture triggers to architecture assessment

### M2. Implement the compact bugfix contract

- Milestone kind: implementation
- Goal: Rewrite the one-file skill so every operation, authority, evidence, phase, action, result, owner, write, and handoff decision follows the approved closed contract.
- Requirements: R2-R22, R24-R25; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-001 through INT-005.
- Architecture decisions: preserve the existing one-file package and invocation-local evidence model.
- Files/components likely touched:
  - `skills/bugfix/SKILL.md`
  - `scripts/test-skill-validator.py`
  - directly coupled active documentation consumers identified by M1
- Dependencies:
  - M1 and its code review close without architecture reassessment
- Tests and proof:
  - explicit diagnosis, explicit fix, bare concrete `$bugfix`, absent defect, conflicting intent, and late expansion
  - command authority, side effects, portable and governed write scope, malformed governed signals, and missing evidence placement
  - reproduction, basis, feasibility, proof, cause, proof-action, current-action, terminal-result, and unknown-value cross-products
  - bounded proof authoring before correction, unchanged proof identity after correction, completed-state precedence, and deterministic owner routing
  - code-review-only immediate handoff and forbidden downstream claims
- Implementation steps:
  - run the focused failing contract tests
  - replace repeated narrative with compact closed tables and exact ordering
  - keep all safety rules inline because every fix loads the complete file
  - preserve only one semantic owner for each retained legacy rule and literal
  - update directly coupled documentation only when M1 proves it necessary
- Validation commands:
  - `python scripts/validate-skills.py skills/bugfix/SKILL.md`
  - `python scripts/test-skill-validator.py BugfixSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: supported bugfix requests select one safe action and terminal result without speculative mutation or downstream overclaim.
- Completion criteria: focused and broad skill tests pass, all closed values and rows are represented, no forbidden owner is mutated, and no resource is added.
- Required evidence: `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/m2-contract-implementation.md`
- Review handoff: independent `code-review` of the canonical skill, focused tests, and coupled consumer changes.
- Optional commit boundary: `M2: simplify bugfix control contract`
- Risks:
  - compression removes a legacy safety rule
  - a broad phase row shadows blocked or complete states
  - request-bound authority is read as repository-wide permission
- Rollback/recovery:
  - restore the previous canonical skill and directly coupled consumers together, then rerun the full skill and build suites

### M3. Prove measurements, boundary coverage, and package parity

- Milestone kind: implementation
- Goal: Reconcile every frozen rule and literal, prove every boundary outcome, report exact size deltas, and validate a byte-identical package through all supported projections without sacrificing required behavior to a metric.
- Requirements: R1, R23-R27; all approved boundaries and interactions.
- Architecture decisions: existing build and adapter-package architecture; no ADR.
- Files/components likely touched:
  - `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/simplification-measurements.md`
  - `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/semantic-preservation-review.md`
  - `docs/changes/2026-08-20-bugfix-skill-simplification/evidence/m3-package-proof.md`
  - existing adapter distribution tests only if direct bugfix parity coverage is absent
- Dependencies:
  - M2 and its code review close
- Tests and proof:
  - original reproduction, identity-equal regression proof, blast-radius checks, and failure claims remain distinct
  - every requirement, example, edge case, boundary, interaction, legacy rule, and sensitive literal has final proof or disposition
  - before/after normalized words and UTF-8 bytes are reported for the root and complete package; any token estimate identifies its tokenizer or model basis
  - semantic completeness, deterministic interpretation, safety, and parity pass regardless of whether a measured count decreases
  - canonical, generated, packed, archived, release-candidate, and clean-installed bugfix packages are byte-identical
- Implementation steps:
  - run the focused and broad contract suites
  - reconcile final text against M1 inventories and the approved test spec
  - measure the exact before and after inputs using the approved formula
  - build and validate temporary package, archive, release-candidate, and install trees
  - record commands, identities, counts, and limitations
- Validation commands:
  - `python scripts/test-skill-validator.py BugfixSkillSimplificationTests`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py skills/bugfix/SKILL.md`
  - `python scripts/validate-boundary-first.py --check --path specs/bugfix-skill-simplification.md`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: the complete shipped package is semantically complete, truthfully measured, and identical through every supported projection.
- Completion criteria: all focused, broad, boundary, build, distribution, measurement, and reconciliation proof passes with no unresolved rule, literal, gap, or growth.
- Required evidence: measurement, semantic-preservation, and M3 package-proof records.
- Review handoff: independent `code-review` of final proof and package-chain evidence.
- Optional commit boundary: `M3: prove bugfix simplification`
- Risks:
  - a measured root change hides a changed generated or installed copy
  - a word, byte, or token target masks semantic loss or causes required behavior to move outside the published contract
- Rollback/recovery:
  - restore the prior skill and consumer set, rebuild projections, and discard temporary package trees

### M4. Close implementation lifecycle evidence

- Milestone kind: lifecycle-closeout
- Goal: Perform final holistic review, close findings, explain the change, verify readiness, and prepare PR handoff after implementation milestones close.
- Requirements: R1-R27.
- Architecture decisions: architecture-not-required assessment.
- Files/components likely touched:
  - final review records, `explain-change.md`, and `verify-report.md` under the owning change root
- Dependencies:
  - M1-M3 and required review resolution are closed
- Tests and proof:
  - final holistic diff review and the complete approved test-spec command ledger
- Implementation steps:
  - run final holistic `code-review`
  - resolve every material finding through owned correction and rereview
  - create the durable change explanation
  - run final `verify` and hand off to `pr` only under separate authority
- Validation commands:
  - use the complete approved test-spec command ledger
  - `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`
- Expected observable result: implementation evidence is coherent and final verification reports truthful PR handoff state.
- Completion criteria: final review is clean, rationale is current, verification is recorded, and no blocker remains.
- Required evidence: final review, closed resolution when required, explanation, and verify report.
- Review handoff: `verify`, then `pr` only under separate authority.
- Optional commit boundary: `closeout: verify bugfix simplification`
- Risks:
  - late cross-milestone inconsistency invalidates earlier proof
- Rollback/recovery:
  - return to the owning implementation milestone, correct and rereview it, then repeat closeout

## Validation plan

- M1 owns rule, literal, scenario, unknown-value, baseline, and architecture-trigger proof.
- M2 owns the executable closed contract, authority, state-machine, routing, write-boundary, and claim proof.
- M3 owns final boundary coverage, semantic reconciliation, truthful size reporting, metric-gaming prevention, and canonical-through-installed parity.
- Formal code review, review resolution, explanation, verify, and PR review own later lifecycle judgment.

## Risks and recovery

- Risk: compact tables become less readable than the original narrative. Recovery: preserve plain-language classification and result summaries while removing duplicate prose.
- Risk: proof authoring accidentally grants production permission. Recovery: keep the two gates separate in both text and tests.
- Risk: a new durable owner becomes necessary. Recovery: stop and return to architecture before canonical mutation.
- Risk: lifecycle or contract files are treated as bugfix evidence destinations. Recovery: test the exact read-only list and missing-placement stop.

## Dependencies

- Approved focused spec, clean spec review, architecture-not-required assessment, and approved portable proposal direction.
- Existing published-skill, workflow, lifecycle, boundary-first, build, adapter, archive, and release-candidate contracts.
- Existing skill validation, package build, adapter distribution, and token-measurement tools.
- Approved test specification and test-spec review before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-20 | Use three implementation milestones plus lifecycle closeout. | Preservation, contract mutation, and distribution proof have distinct rollback and review boundaries. | One large rewrite; prose-only milestones. |
| 2026-08-20 | Keep the package flat. | Every real fix needs the complete compact procedure and no measured conditional profile justifies another resource. | Conditional fix reference; separate diagnosis skill. |
| 2026-08-20 | Establish fixtures and ledgers before editing the skill. | Compression is safe only when every current rule and consumer-sensitive literal has an owner. | Rewrite first and reconstruct compatibility afterward. |
| 2026-08-20 | Prove size and package parity only after semantic closure. | A smaller count is not success when behavior or a shipped projection drifts. | Size-first acceptance; root-only measurement. |
| 2026-08-20 | Treat word, byte, and tokenizer-specific token counts as diagnostic evidence rather than mandatory reductions. | The complete published contract must reflect the truth even when required deterministic wording increases a count. | Retain the legacy ceiling; omit required inline behavior; hide cost in contributor-only evidence. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done; plan review, test-spec authoring and review, implementation and code review, explanation, verification, and PR handoff remain.
