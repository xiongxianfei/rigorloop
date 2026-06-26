# Requirement-Fidelity Gate for Spec-Canonical Reviews Execution Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews
- Owner: maintainer
- Start date: 2026-06-26
- Last updated: 2026-06-26
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the first slice of the requirement-fidelity gate for spec-canonical automated reviews. The work should prevent requirement compression by making automated review handoff depend on deterministic applicability evidence, spec-first packet ordering, requirement-property decomposition, property-by-surface checks, structurally valid fidelity receipts, spec-derived validator matrices for selected changed contracts, and compression-defect calibration.

This plan preserves the independent adversarial review gates. The fidelity gate is an additive sibling layer: independence answers whether the review is procedurally unanchored, while fidelity answers whether the review compares artifacts against the full normative spec.

## Source artifacts

- Proposal: [Requirement-Fidelity Gate for Spec-Canonical Reviews](../proposals/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md)
- Proposal-review: [proposal-review-r1](../changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/proposal-review-r1.md)
- Spec: [Requirement-Fidelity Gate for Spec-Canonical Reviews](../../specs/requirement-fidelity-gate.md)
- Spec-review: [spec-review-r2](../changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r2.md)
- Architecture: [canonical system architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260626-requirement-fidelity-gate](../adr/ADR-20260626-requirement-fidelity-gate.md)
- Architecture-review: [architecture-review-r1](../changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/architecture-review-r1.md)
- Test spec: [Requirement-Fidelity Gate Test Spec](../../specs/requirement-fidelity-gate.test.md)
- Change metadata: [change.yaml](../changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml)

## Context and orientation

This is workflow-governance and validator work inside the repository-local RigorLoop system. It does not add a hosted service, database, background worker, external control plane, deployment target, or network dependency.

Important implementation surfaces:

- `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, and related review skills own reviewer-facing and workflow-facing instructions.
- `scripts/review_artifact_validation.py`, `scripts/validate-review-artifacts.py`, and `scripts/test-review-artifact-validator.py` own formal review record structure.
- `scripts/artifact_lifecycle_validation.py`, `scripts/validate-artifact-lifecycle.py`, and `scripts/test-artifact-lifecycle-validator.py` own workflow-state and autoprogression checks.
- `scripts/change_metadata_semantics.py`, `scripts/validate-change-metadata.py`, and `scripts/test-change-metadata-validator.py` own change metadata shape and semantic checks.
- `scripts/validation_selection.py`, `scripts/select-validation.py`, `scripts/ci.sh`, and `scripts/test-select-validation.py` own changed-path routing.
- `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/build-skills.py`, `scripts/test-build-skills.py`, `scripts/build-adapters.py`, and `scripts/validate-adapters.py` own canonical skill validation and generated adapter proof when skill behavior changes.
- `tests/fixtures/review-artifacts/`, `tests/fixtures/artifact-lifecycle/`, `tests/fixtures/change-metadata/`, and any new calibration fixture location own regression coverage.

The implementation should favor structured fields and closed vocabularies where the spec defines them. Prose remains bounded evidence, not the source of truth for closed sets.

## Non-goals

- Do not replace or weaken independent adversarial review gates.
- Do not require every review to produce a finding.
- Do not add mandatory manual-review applicability classification in the first slice.
- Do not rewrite all historical reviews, all existing validators, or all existing specs.
- Do not implement full automatic extraction of requirement properties from arbitrary prose.
- Do not expose private chain-of-thought in review records.
- Do not add a hosted review service, database, external queue, or network dependency.
- Do not proceed to implementation until `plan-review` and the matching test spec are complete.

## Requirements covered

- `R1`-`R3`: M1, M2
- `R4`-`R13`: M1, M2
- `R14`-`R23`: M1, M2
- `R24`-`R29`: M3
- `R30`-`R34`: M1, M2
- `R35`-`R40`: M1, M2
- `R41`-`R45c`: M4
- `R46`-`R50`: M1, M2, M3, M4, M5
- `AC-RFG-001`-`AC-RFG-008`: M1, M2
- `AC-RFG-009`-`AC-RFG-012`: M3, M4
- `AC-RFG-013`-`AC-RFG-020`: M2, M4, M5
- `RFG-T017`-`RFG-T022`: M4, M5
- `RFG-022`-`RFG-024`: M1, M2, M3

## Current Handoff Summary

- Current milestone: M4. Compression calibration corpus and sampling records
- Current milestone state: planned
- Latest review evidence: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r4.md
- Last reviewed milestone: M3
- Review status: approved; stage=code-review; round=r4
- Remaining in-scope implementation milestones: M4, M5
- Next stage: implement M4
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, explain-change-pending, verify-pending, pr-handoff-pending — M1 through M3 are closed; M4 and M5 remain open.

## Milestones

### M1. Requirement-fidelity review contract and guidance

- Milestone state: closed
- Goal: Add reviewer-facing and workflow-facing guidance for deterministic applicability, spec-first packet ordering, requirement-property decomposition, property-by-surface verification, fidelity receipts, requirement-compression findings, and AND semantics with the independent-review gate.
- Requirements: `R1`-`R3`, `R9`-`R13`, `R14`-`R23`, `R27`-`R40`, `R46`-`R50`, `AC-RFG-001`-`AC-RFG-008`, `AC-RFG-013`, `AC-RFG-016`-`AC-RFG-019`
- Files/components likely touched:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Dependencies:
  - Approved test spec must define the exact skill and workflow assertions before implementation.
  - M1 should not change generated adapter output directly; generation validation belongs to M5 if canonical skill text changes.
- Tests to add/update:
  - Skill-validator checks for spec-canonical packet order, decomposition before artifact comparison, property-by-surface checks, no global-substring sufficiency for multi-surface contracts, requirement-fidelity receipt fields, compression-finding guidance, no finding quota, and independent-gate preservation.
  - Workflow guidance checks for AND semantics when both review contracts apply.
  - Manual-review first-slice scope checks for voluntary opt-in without mandatory manual applicability classification.
- Implementation steps:
  - Update canonical guidance so automated `code-review` is the first full pilot surface.
  - Add bounded applicability and packet-order instructions without making reviewers the authority for computed applicability.
  - Add fidelity receipt and material-finding guidance while preserving existing clean-review and material-finding recording duties.
  - Keep public skill text user-facing and avoid repository-maintainer implementation internals that belong in specs or docs.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: Canonical review and workflow guidance teaches the requirement-fidelity gate as a spec-canonical sibling to the independent-review gate without changing direct manual review obligations.
- Commit message: `M1: add requirement-fidelity review guidance`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Skill text could become too long or leak maintainer-only implementation details.
  - Guidance-only changes could appear complete before validators enforce the gate.
- Rollback/recovery:
  - Revert the affected canonical skill and workflow guidance while leaving the approved spec and architecture artifacts intact.

### M2. Applicability, receipt, and autoprogression validators

- Milestone state: closed
- Goal: Add structured validation for applicability manifests, closed vocabularies, receipt completeness, packet-order evidence, not-applicable reasons, reviewer overrides, and autoprogression blocking when applicable fidelity evidence is missing or invalid.
- Requirements: `R3`-`R13`, `R14`-`R23`, `R30`-`R40`, `R46`, `R48`, `R50`, `AC-RFG-002`-`AC-RFG-008`, `AC-RFG-013`, `AC-RFG-016`, `AC-RFG-018`-`AC-RFG-020`
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/review-artifacts/`
  - `tests/fixtures/artifact-lifecycle/`
  - `tests/fixtures/change-metadata/`
- Dependencies:
  - M1 should define the author-facing evidence vocabulary before validator diagnostics depend on it.
  - Test spec must define valid and invalid fixture shapes.
- Tests to add/update:
  - Valid applicability manifest with affected paths, path triggers, category triggers, `applicable`, review stage, and no override.
  - Invalid manifests for unknown applicability result, unknown override direction, missing override justification, free-form not-applicable reason, missing matched trigger evidence, and packet ordering that does not put the relevant spec clause first.
  - Clean review receipt fixtures that fail without decomposition evidence or validator/spec comparison when the manifest is `applicable`.
  - Autoprogression fixture proving independent-review receipt alone is insufficient when fidelity also applies.
  - Historical clean review fixture proving old records are not retroactively invalidated solely for missing fidelity receipt.
  - Unknown-value regression tests for every new closed vocabulary.
- Implementation steps:
  - Add shared constants for applicability results, override directions, not-applicable reasons, receipt fields, compression severity defaults, and packet-order evidence.
  - Extend review artifact validation to fail closed for malformed gate evidence while preserving existing profile-off and historical review behavior.
  - Extend lifecycle validation so workflow-managed continuation requires both independent-review and fidelity receipts when both gates apply.
  - Extend change metadata checks only as needed to record the new evidence without making change metadata the owner of live plan state.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
- Expected observable result: Invalid fidelity gate records fail closed, applicable clean automated reviews require valid fidelity evidence, and legacy reviews remain historical evidence.
- Commit message: `M2: validate requirement-fidelity review evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - New validation could accidentally make historical clean reviews fail current lifecycle checks.
  - Closed-vocabulary checks could be added after consistency checks and allow unknown values to pass silently.
- Rollback/recovery:
  - Revert the new fidelity-specific validator paths and fixtures while preserving existing review artifact, lifecycle, and change metadata validators.

### M3. Spec-derived validator matrix pilot

- Milestone state: closed
- Goal: Pilot property-list by surface-list assertions for one selected high-value multi-surface contract, using the M2 missing-`recorded` R26 case as the canonical regression.
- Requirements: `R24`-`R29`, `R43`, `R46`-`R49`, `AC-RFG-009`-`AC-RFG-012`, `AC-RFG-016`-`AC-RFG-018`
- Files/components likely touched:
  - `specs/test-spec-review-gate.md`
  - `skills/implement/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/`
  - `scripts/validate-skills.py` if the matrix requires reusable validation support
- Dependencies:
  - M1 should define the reviewer guidance and M2 should define the closed-list validation style before the pilot hardens one contract.
  - Test spec must identify the exact R26 surfaces and expected properties.
- Tests to add/update:
  - Shared constants for `approved`, `current`, and `recorded` with a source annotation for `specs/test-spec-review-gate.md` R26.
  - Shared constants for the required `implement` skill surfaces.
  - Matrix assertion that each property appears on each required surface or equivalent surface-specific semantic representation.
  - Negative fixture or equivalent proof where removing `recorded` from one surface fails validation.
  - Regression proof that implementation and validator agreement on `approved + current` without `recorded` still fails.
- Implementation steps:
  - Identify the existing R26 wording and the exact authored skill surfaces that project that requirement.
  - Replace hand-listed phrase checks with a single property list multiplied by a surface list.
  - Update `skills/implement/SKILL.md` only as needed to carry the full `approved + current + recorded` evidence contract.
  - Avoid extending the pilot to unrelated validators in this slice.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: The canonical R26 compression case fails validation if any required R26 property is missing from any required `implement` skill surface.
- Commit message: `M3: add R26 property matrix validation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - The validator could overfit exact prose where the spec requires semantic properties.
  - Surface names could drift if no accepted vocabulary exists for skill sections.
- Rollback/recovery:
  - Revert the R26-specific matrix and skill text changes while preserving broader requirement-fidelity gate infrastructure.

### M4. Compression calibration corpus and sampling records

- Milestone state: planned
- Goal: Add the `requirement-compression` seeded-defect family, named rotating corpus iterations, Phase B sampling floors, not-applicable sampling records, and soft-normative regression checks.
- Requirements: `R17`-`R17d`, `R41`-`R45c`, `R48`, `AC-RFG-012`, `AC-RFG-014`, `AC-RFG-015`, `AC-RFG-020`, `RFG-T017`-`RFG-T022`
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - `tests/fixtures/review-artifacts/`
  - `tests/fixtures/artifact-lifecycle/`
  - `tests/fixtures/change-metadata/`
  - `specs/requirement-fidelity-gate.md` only if the approved spec exposes an implementation-blocking gap
- Dependencies:
  - M2 should establish review artifact and lifecycle validator extension points.
  - M3 should supply the canonical R26 missing-`recorded` regression seed or a fixture equivalent.
- Tests to add/update:
  - Six seed-type coverage for A+B+C compressed to A+B, N surfaces compressed to N-1, closed enum compressed, normative verbs compressed, multi-surface asymmetry, and validator mirrors implementation.
  - Corpus iteration validation requiring at least six defects across at least four seed types.
  - Rotation trigger fixtures for complete defect-set exposure, recall above 95 percent across two cycles, and scheduled two-cycle rotation.
  - Sampling records for 10 percent baseline applicable receipts, 30 percent reviewer-authored decomposition receipts, 5 percent not-applicable receipts, and steady-state floors of 5 percent and 15 percent.
  - Closed-enum tests for sampling reasons, audit outcomes, and rotation triggers.
  - Soft-normative wording meta-test for undefined or unquantified safety claims in `MUST` requirements.
- Implementation steps:
  - Choose the smallest repository-owned representation for corpus iterations and sampling records that existing validators can check.
  - Add public fixture examples without making the public examples the entire protected calibration corpus.
  - Add selector coverage so calibration fixture changes route to the right validator tests.
  - Keep calibration evidence as a measurement layer; do not make it a finding quota.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
- Expected observable result: Calibration data can prove sampling floors, named corpus iterations, rotation triggers, and the canonical compression defect family without relying on reviewer memory or static public examples.
- Commit message: `M4: add requirement-compression calibration fixtures`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - A fully public corpus could make recall metrics easy to game.
  - Calibration validation could be mistaken for runtime review gating.
- Rollback/recovery:
  - Revert calibration-specific fixtures and sampling validators while keeping the core fidelity gate checks in place.

### M5. Generated guidance, behavior preservation, and lifecycle closeout

- Milestone state: planned
- Goal: Refresh generated outputs after canonical guidance changes, record behavior-preservation evidence, run selected and broad-enough validation, and prepare downstream lifecycle evidence for final code-review, explain-change, verify, and PR handoff.
- Requirements: `R46`-`R50`, all acceptance criteria as final integration proof
- Files/components likely touched:
  - generated skill or adapter outputs produced by existing build scripts
  - `docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/behavior-preservation.md`
  - `docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md`
  - `docs/plan.md`
- Dependencies:
  - M1 through M4 must be implemented and reviewed or ready for final integration review.
  - Generated outputs must be produced only through existing generation commands.
- Tests to add/update:
  - Build-skill and adapter validation for any canonical skill changes.
  - Selected validation routing for all touched source, fixture, skill, plan, and change-record surfaces.
  - Behavior-preservation matrix proving independent review gates, historical reviews, manual review opt-in, and no finding quota remain intact.
- Implementation steps:
  - Run normal skill and adapter generation checks after all canonical guidance changes settle.
  - Add behavior-preservation evidence under the change root.
  - Run selected CI against the full changed-path set and targeted validators named by the test spec.
  - Update the plan body, plan index, change metadata, validation notes, and review handoff status before code-review.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `bash scripts/ci.sh --mode explicit --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `git diff --check -- docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md docs/plan.md docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
- Expected observable result: Generated outputs are current where required, behavior preservation is recorded, selected validation passes, and the change is ready for final code-review before explain-change and verify.
- Commit message: `M5: refresh fidelity gate generated evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Generated-output drift could be missed if skill changes are validated without build checks.
  - Lifecycle state could drift between the plan body, plan index, and change metadata.
- Rollback/recovery:
  - Regenerate from canonical sources or revert generated-output changes first, then rerun selected CI and lifecycle validation.

## Validation plan

- `python scripts/test-skill-validator.py`: validates canonical skill guidance and selected phrase/contract fixtures.
- `python scripts/validate-skills.py`: validates canonical skill structure.
- `python scripts/test-review-artifact-validator.py`: validates formal review record and fidelity receipt fixtures.
- `python scripts/test-artifact-lifecycle-validator.py`: validates workflow-state and autoprogression fixtures.
- `python scripts/test-change-metadata-validator.py`: validates change metadata semantics and closed vocabulary behavior where applicable.
- `python scripts/test-select-validation.py`: validates changed-path routing for new fixture and validator surfaces.
- `python scripts/test-build-skills.py`: validates skill generation behavior.
- `python scripts/build-skills.py --check`: proves generated local skill mirrors are current when canonical skills change.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`: proves adapter output remains valid when public skill behavior changes.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`: validates change-local review evidence.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`: validates change metadata.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path specs/requirement-fidelity-gate.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260626-requirement-fidelity-gate.md --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/proposal-review-r1.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r1.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r2.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/architecture-review-r1.md`: validates lifecycle state synchronization for current planning evidence.
- `bash scripts/ci.sh --mode explicit --path <changed paths>`: final selected validation after implementation determines the exact touched files.
- `git diff --check -- <changed paths>`: whitespace and patch hygiene.

## Risks and recovery

- Risk: The fidelity gate duplicates or weakens the independent-review gate instead of composing with it.
  - Recovery: Keep AND semantics in validators and tests; rollback fidelity-specific autoprogression while preserving independent-review behavior.
- Risk: Applicability remains discretionary despite the spec.
  - Recovery: Treat affected-path and category triggers as closed constants with unknown-value and missing-trigger regression tests.
- Risk: Decomposition evidence becomes boilerplate.
  - Recovery: Keep structural receipt checks in M2 and calibration sampling plus seeded compression defects in M4.
- Risk: Validator matrices overfit exact wording.
  - Recovery: Use semantic property IDs except where exact public wording is normative under `R28`.
- Risk: Generated skill or adapter output drifts after canonical skill edits.
  - Recovery: Run existing generation and adapter validation commands in M5 and regenerate only from canonical sources.

## Dependencies

- `plan-review` must approve this execution plan before test-spec authoring.
- The matching test spec must map every `MUST`, acceptance criterion, and planned test ID before implementation starts.
- M1 should precede M2 because validators need stable guidance and evidence vocabulary.
- M2 should precede M3 and M4 because the validator extension points should exist before the pilot matrix and calibration records rely on them.
- M5 runs only after M1 through M4 have produced stable changed-path evidence.

## Progress

- 2026-06-26: Proposal accepted, spec approved after spec-review R2, canonical architecture and ADR approved after architecture-review R1.
- 2026-06-26: Execution plan authored and indexed for plan-review.
- 2026-06-26: Test spec authored as the active proof-planning surface; next stage is `test-spec-review`.
- 2026-06-26: Test-spec-review R1 requested changes for `TSR1-F1`; next stage is `review-resolution`.
- 2026-06-26: Resolved `TSR1-F1` by adding structured manual proof cases, converting two manual bullets to automated tests, and updating coverage references; next stage is `test-spec-review-r2`.
- 2026-06-26: Test-spec-review R2 approved the revised active test spec with no material findings; next stage is `implement` for M1.
- 2026-06-26: M1 implementation started; current focus is skill-validator coverage and canonical guidance for requirement-fidelity review behavior.
- 2026-06-26: M1 implementation completed. Added skill-validator coverage for requirement-fidelity guidance; updated `code-review`, `workflow`, `implement`, adjacent review skills, and `docs/workflows.md`; next stage is `code-review`.
- 2026-06-26: Code-review R1 returned clean-with-notes for M1, closed M1, and handed off to implement M2.
- 2026-06-26: M2 implementation started. Added tests and validator support for requirement-fidelity applicability manifests, clean-review fidelity receipts, lifecycle AND semantics, optional change-metadata fidelity fields, and the approved-and-recorded test-spec-review implementation precondition.
- 2026-06-26: M2 implementation completed. Requirement-fidelity review artifact, lifecycle, and change-metadata validators pass targeted and full-suite validation; next stage is `code-review`.
- 2026-06-26: Code-review R2 requested changes for M2. Finding `RFG-M2-CR1` is open; next stage is `review-resolution`.
- 2026-06-26: Resolved `RFG-M2-CR1` by making missing fidelity applicability fail closed, canonicalizing clean-review fixtures as complete by default, and adding lifecycle plus review-artifact regressions; next stage is `code-review-r3`.
- 2026-06-26: Code-review R3 returned clean-with-notes for M2, confirmed `RFG-M2-CR1` is resolved, closed M2, and handed off to implement M3.
- 2026-06-26: M3 implementation completed. Added source-annotated R26 property and surface constants plus a property-list by surface-list skill-validator matrix; added a missing-`recorded` negative regression for the canonical compression case; next stage is `code-review-r4`.
- 2026-06-26: Code-review R4 returned clean-with-notes for M3, closed the R26 matrix pilot milestone, and handed off to implement M4.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-26 | Split implementation into guidance, validators, matrix pilot, calibration, and closeout milestones. | The spec spans review guidance, structured records, validator behavior, calibration, and generated outputs; separating these keeps review surfaces bounded. | One broad implementation milestone that mixes skills, validators, fixtures, and generated output. |
| 2026-06-26 | Make `code-review` the full first pilot and keep other review families scoped to compatible evidence behavior. | The motivating M2 miss occurred in code review, and the spec says all-review-family rollout follows the pilot. | Immediate mandatory rollout across every review family. |
| 2026-06-26 | Put generated output and behavior preservation in the final implementation milestone. | Generated outputs should reflect stable canonical guidance after the earlier milestones settle. | Regenerate after every intermediate skill edit. |

## Surprises and discoveries

- None yet.

## Validation notes

- 2026-06-26: Upstream status settlement result: not-needed. Proposal, spec, architecture, and ADR statuses already match durable clean review evidence.
- 2026-06-26: M1 validation passed:
  - `python scripts/test-skill-validator.py -k requirement_fidelity_m1_guidance_surfaces`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- 2026-06-26: M2 validation passed:
  - `python scripts/test-review-artifact-validator.py -k requirement_fidelity`
  - `python scripts/test-artifact-lifecycle-validator.py -k requirement_fidelity`
  - `python scripts/test-change-metadata-validator.py -k requirement_fidelity`
  - `python scripts/test-artifact-lifecycle-validator.py -k test_spec_review`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
- 2026-06-26: M2 review-resolution validation passed:
  - `python scripts/test-artifact-lifecycle-validator.py -k requirement_fidelity`
  - `python scripts/test-review-artifact-validator.py -k requirement_fidelity`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r2.md`
  - `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/invalid-workflow-managed-missing-fidelity-applicability` failed as expected with `fidelity-applicability-missing`
  - `git diff --check -- scripts/lifecycle_state_sync.py scripts/test-artifact-lifecycle-validator.py scripts/review_artifact_validation.py scripts/test-review-artifact-validator.py tests/fixtures/review-artifacts/invalid-workflow-managed-missing-fidelity-applicability docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md docs/plan.md`
- 2026-06-26: Code-review R3 evidence validation passed:
  - `python scripts/test-artifact-lifecycle-validator.py -k requirement_fidelity`
  - `python scripts/test-review-artifact-validator.py -k requirement_fidelity`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r3.md`
- 2026-06-26: M3 validation passed:
  - `python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads`
  - `python scripts/test-skill-validator.py -k requirement_fidelity_m3`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
- 2026-06-26: Code-review R4 evidence validation passed:
  - `python scripts/test-skill-validator.py -k requirement_fidelity_m3`
  - `python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md --path docs/plan.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md --path docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r4.md`
  - `git diff --check -- docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md docs/plan.md`

## Outcome and retrospective

- Pending implementation and downstream lifecycle closeout.

## Readiness

- See `Current Handoff Summary`.
- The `Current Handoff Summary` is the single live owner for next-stage and closeout state.
