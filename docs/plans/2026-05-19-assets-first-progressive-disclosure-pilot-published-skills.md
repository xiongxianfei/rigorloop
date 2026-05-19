# Assets-First Progressive Disclosure Pilot Execution Plan

- Status: active
- Owner: maintainers
- Start date: 2026-05-19
- Last updated: 2026-05-19
- Related proposal: [Assets-First Progressive Disclosure Pilot for Published Skills](../proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md)
- Related spec: [Skill Contract](../../specs/skill-contract.md)
- Related test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active and owner-approved for R37-R45 after plan-review
- Related proposal-review: [proposal-review-r2](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/proposal-review-r2.md)
- Related spec-review: [spec-review-r1](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/spec-review-r1.md)
- Change root: [docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml)
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the accepted assets-first progressive disclosure pilot for the published `plan` skill.

The pilot proves that a published skill can ship non-empty skill-local `assets/`, map those assets from `SKILL.md`, preserve installed-skill self-containment, and improve the common-path body rather than only adding packaging machinery.

## Source artifacts

- Proposal: [Assets-First Progressive Disclosure Pilot for Published Skills](../proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md), accepted.
- Proposal review: [proposal-review-r2](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/proposal-review-r2.md), approved.
- Spec: [Skill Contract](../../specs/skill-contract.md), approved after [spec-review-r1](../changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/spec-review-r1.md).
- Test spec: [Skill Contract Test Spec](../../specs/skill-contract.test.md), active for prior slices and to be amended for R37-R45 after plan-review.
- Architecture: not required. This initiative changes canonical skill text, packaged Markdown assets, repository validators, deterministic test fixtures, adapter packaging proof, and change-local evidence. It does not add runtime services, persistence, APIs, deployment boundaries, or hard-to-reverse data flow.
- Project map: [RigorLoop Project Map](../project-map.md), available as orientation only.

## Context and orientation

- `skills/` is the only authored skill source.
- Generated public adapter skill bodies are release archives for `v0.1.3` and later; do not hand-edit generated adapter package output.
- The only skill body in scope is `skills/plan/SKILL.md`.
- The only new packaged resources in scope are:
  - `skills/plan/assets/plan-skeleton.md`
  - `skills/plan/assets/milestone.md`
  - `skills/plan/assets/current-handoff-summary.md`
  - `skills/plan/assets/decision-log-row.md`
- Existing validator entrypoints are `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/build-skills.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and `scripts/measure-skill-tokens.py`.
- Behavior-parity evidence should separate contract-era reference plans from historical coverage plans.
- Change-local evidence for this initiative lives under `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/`.

## Non-goals

- Do not modify `proposal`, `proposal-review`, `spec`, `spec-review`, `code-review`, `verify`, or `pr`.
- Do not introduce packaged `references/` or `scripts/`.
- Do not introduce build-time partials or include syntax.
- Do not change adapter install roots, lockfile semantics, release archive trust boundaries, or CLI behavior.
- Do not hand-edit generated adapter skill bodies or generated adapter assets.
- Do not use assets for hidden workflow rules, lifecycle transition policy, or claim ownership.
- Do not require historical plans to satisfy current plan structure for strict parity.
- Do not claim branch readiness, PR readiness, verification readiness, final closeout, or Done from this plan.

## Requirements covered

| Requirement | Planned coverage |
| --- | --- |
| R37-R37d | Keep the pilot as a follow-on `plan` slice only; block overlap with unresolved `plan` work unless an owner decision records safety. |
| R38-R38c | Create exactly four normative structural assets and validate no extra asset classes or root internal dependencies are introduced. |
| R39-R39d | Add a `Resource map` to `skills/plan/SKILL.md` with literal `COPY`, trigger conditions, fields to fill, and no-unfilled-placeholder guidance. |
| R40-R40c | Make `plan-skeleton.md` the reviewed equivalent full output template while preserving compact output expectations in `SKILL.md`. |
| R41-R41c | Keep current handoff lifecycle semantics in `SKILL.md` or workflow artifacts, not in `current-handoff-summary.md`. |
| R42-R42e | Add asset metadata, normative status, structural fingerprints, section-set parity, and drift-resolution behavior. |
| R43-R43d | Add deterministic validator and review boundaries without broad semantic scoring. |
| R44-R44e | Prove no behavior regression and at least 15 percent common-path body token reduction, with total package budget and milestone reuse evidence. |
| R45-R45e | Separate strict contract-era reference corpus from historical coverage corpus and preserve follow-on pattern guidance. |

## Current Handoff Summary

- Current milestone: M1. Asset Contract Validation And Test Spec Support
- Current milestone state: review-requested
- Last reviewed milestone: M1. Asset Contract Validation And Test Spec Support
- Review status: APD-CR1 resolved; ready for M1 code-review rerun
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: code-review for M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 code-review rerun, remaining implementation milestones, code-review loops, explain-change, verify, and PR handoff have not run.

## Pre-implementation prerequisites

- A clean follow-up plan-review must happen before `test-spec`. Done by `plan-review-r2`.
- After a clean plan-review, the immediate next stage is `test-spec`. Done by the R37-R45 amendment to `specs/skill-contract.test.md`.
- `specs/skill-contract.test.md` must be amended for R37-R45 and owner-approved during the `test-spec` stage before any implementation milestone starts. Done; the test spec is active and owner-approved for M1.
- M1 implements the tests and fixtures defined by the approved test-spec amendment; it does not author that test-spec amendment.

## Milestones

### M1. Asset Contract Validation And Test Spec Support

- Milestone state: review-requested
- Goal: make R37-R45 testable before changing the `plan` skill body or adding assets.
- Requirements: R37-R39, R42-R43, R45.
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/published-design/`
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml`
- Dependencies:
  - clean plan-review
  - owner-approved test-spec amendment before implementation starts
- Tests to add/update:
  - validator tests defined by the approved test-spec amendment for R37-R45
  - failing and passing fixtures defined by the approved test-spec amendment for asset count, approved asset paths, metadata comments, literal `COPY`, fields-to-fill, missing resource-map entries, structural fingerprints, section-set parity, and forbidden root dependencies
- Implementation steps:
  - Implement the tests defined by the approved test-spec amendment.
  - Extend `scripts/skill_validation.py` only for deterministic asset-resource checks required by the test spec.
  - Add fixtures under `tests/fixtures/skills/published-design/` for valid and invalid asset pilots.
  - Keep validation static and phrase/path/structure based.
  - Record no-change rationale if adapter packaging already preserves assets without code changes.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml`
  - `git diff --check -- scripts tests docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md`
- Expected observable result: deterministic tests can distinguish valid `plan` packaged assets from missing, unmapped, malformed, or drifted assets.
- Commit message: `M1: validate plan asset contract`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - structural fingerprint checks may become too brittle if they hash non-structural prose
  - section-set parity may overreach if `SKILL.md` intentionally keeps only compact output expectations
- Rollback/recovery:
  - revert validator and fixture changes
  - keep the approved test-spec amendment for replanning if only implementation shape is wrong

### M2. Plan Skill Asset Split

- Milestone state: planned
- Goal: move the plan output structure into exactly four normative assets while preserving `SKILL.md` execution rules and common-path readability.
- Requirements: R37-R42, R44.
- Files/components likely touched:
  - `skills/plan/SKILL.md`
  - `skills/plan/assets/plan-skeleton.md`
  - `skills/plan/assets/milestone.md`
  - `skills/plan/assets/current-handoff-summary.md`
  - `skills/plan/assets/decision-log-row.md`
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/behavior-preservation.md`
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/token-cost.md`
- Dependencies:
  - M1 closed or explicitly revised
  - current `skills/plan/SKILL.md` baseline token measurement recorded before editing
- Tests to add/update:
  - update `scripts/test-skill-validator.py` expectations if the real `plan` skill exposes a same-class edge case absent from fixtures
  - no broad semantic prose scoring
- Implementation steps:
  - Record before-change `skills/plan/SKILL.md` byte and token measurements.
  - Add the four assets with required metadata, normative status, structural fingerprints, and structural placeholders.
  - Make `plan-skeleton.md` own plan section order, headers, and placeholders.
  - Keep `current-handoff-summary.md` to labels and placeholders only.
  - Add a `Resource map` to `skills/plan/SKILL.md` with literal `COPY` entries for all assets.
  - Keep handoff consistency, milestone state, upstream settlement, readiness-vs-Done, validation, and claim-boundary rules in `SKILL.md`.
  - Remove duplicated full-plan section layout from `SKILL.md`.
  - Record behavior-preservation notes for any moved or rewritten behavior-significant wording.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml`
  - `git diff --check -- skills/plan specs/skill-contract.test.md scripts tests docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md docs/plan.md`
- Expected observable result: `skills/plan/SKILL.md` is shorter, all four assets validate, and no lifecycle rule moves into assets.
- Commit message: `M2: split plan skeleton into packaged assets`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - `SKILL.md` may become too terse to expose the output contract
  - placeholder or fingerprint policy may create noisy churn
  - moving handoff structure may accidentally move lifecycle semantics into the asset
- Rollback/recovery:
  - reinline asset skeletons into `skills/plan/SKILL.md`
  - remove `skills/plan/assets/`
  - keep validator improvements only if they still correctly support flat skills

### M3. Adapter, Token, And Behavior-Parity Proof

- Milestone state: planned
- Goal: prove the asset split ships through adapters, improves the common path, preserves behavior, and handles historical coverage.
- Requirements: R43-R45.
- Files/components likely touched:
  - `scripts/build-adapters.py` or `scripts/adapter_distribution.py`, only if packaged assets are not already preserved
  - `scripts/validate-adapters.py` or `scripts/adapter_distribution.py`, only if adapter validation cannot prove asset presence
  - `scripts/measure-skill-tokens.py`, only if separate common-path and asset measurement is missing
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/behavior-parity.md`
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/historical-coverage.md`
  - `docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/token-cost.md`
- Dependencies:
  - M2 closed
  - selected reference and historical corpora recorded before final parity claims
- Tests to add/update:
  - adapter distribution test proving `skills/plan/assets/*` reaches generated archives if existing tests do not cover non-empty asset directories
  - token measurement test if common-path body versus asset measurement requires script behavior changes
- Implementation steps:
  - Build generated skills and adapter archives from canonical `skills/`.
  - Validate the generated adapter output includes all four `plan` assets.
  - Measure after-change `SKILL.md` common-path body tokens and total `SKILL.md` plus assets tokens.
  - Record whether common-path body tokens decreased by at least 15 percent.
  - Record whether total packaged content stayed within the +5 percent rationale tolerance or below the +10 percent hard cap.
  - Record strict behavior parity against the contract-era reference corpus:
    - `docs/plans/2026-05-18-skill-readability-self-containment.md`
    - `docs/plans/2026-05-19-published-skill-design-spec-family.md`
    - `docs/plans/2026-05-19-published-skill-design-plan-family.md`
  - Record historical coverage parity against 3 to 5 pre-contract plans and any gaps.
  - Record milestone asset reuse evidence showing `assets/milestone.md` is used once per milestone in reference outputs.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
  - `python scripts/measure-skill-tokens.py --skills-root skills`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml`
  - `git diff --check -- skills/plan scripts tests specs docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md docs/plan.md`
  - `bash scripts/ci.sh --mode explicit --path skills/plan/SKILL.md --path skills/plan/assets --path scripts --path tests --path specs/skill-contract.test.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md`
- Expected observable result: generated adapter archives contain the assets, the common-path body shrinks by at least 15 percent, behavior parity is preserved, and historical coverage gaps are explicit.
- Commit message: `M3: prove plan asset packaging and parity`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - adapter archive validation may need deterministic asset inventory support
  - token measurement may need a new mode to distinguish `SKILL.md` body from assets
  - behavior-parity evidence could become too narrative unless the corpus checks are structured
- Rollback/recovery:
  - revert adapter/token script changes if unnecessary or too broad
  - keep behavior evidence as review input for a smaller asset split

## Validation plan

- Plan-stage validation:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path specs/skill-contract.md --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/spec-review-r1.md`
  - `git diff --check -- docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md specs/skill-contract.md docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md docs/plan.md docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills`
- Implementation validation is listed per milestone above.
- Final validation after all implementation milestones close should run selected CI on touched paths, then `explain-change`, `verify`, and `pr` stages own their normal proof.

## Risks and recovery

- Risk: the four-asset split fails the 15 percent common-path body reduction gate.
  - Recovery: reinline the assets, remove `skills/plan/assets/`, and record the pilot as not beneficial unless the spec is amended.
- Risk: structural fingerprint validation is too noisy.
  - Recovery: revise the normalization algorithm through test-spec and validator changes before relying on it.
- Risk: adapter generation already omits skill-local assets.
  - Recovery: update adapter distribution code and tests in M3, or stop before claiming adapter proof.
- Risk: behavior parity weakens plan handoff ownership.
  - Recovery: move any hidden lifecycle rule back into `SKILL.md` and rerun parity checks.

## Dependencies

- `spec-review-r1` is clean and has been used to settle `specs/skill-contract.md` to `approved`.
- `plan-review` must pass before test-spec.
- `specs/skill-contract.test.md` must be amended and owner-approved before implementation.
- Each implementation milestone requires code-review before it can close.
- Review-resolution is required if material code-review findings occur.
- Final closeout requires explain-change, verify, and PR handoff after all implementation milestones close.

## Progress

- 2026-05-19: plan created and `docs/plan.md` updated; ready for plan-review.
- 2026-05-19: plan-review-r1 requested changes for APD-PLR1; revised M1 to keep `test-spec` authoring outside implementation and make the approved test-spec amendment a pre-implementation prerequisite.
- 2026-05-19: plan-review-r2 approved the revised plan; `specs/skill-contract.test.md` amended with T33-T36 for R37-R45; ready for M1 implementation.
- 2026-05-19: owner approved the active R37-R45 test-spec amendment; M1 implementation prerequisite is satisfied.
- 2026-05-19: M1 implemented deterministic plan asset-pilot validator support and fixtures; validation passed; ready for M1 code-review.
- 2026-05-19: APD-CR1 review-resolution added direct missing resource-map-entry fixture coverage for the `plan` asset pilot; ready for M1 code-review rerun.

## Decision log

- 2026-05-19: split implementation into validator/test support, asset rewrite, and adapter/token/parity proof -> keeps risky validation mechanics separate from skill text and final proof.
- 2026-05-19: architecture stage marked not required -> the change affects Markdown contracts, static validators, generated adapter packaging proof, and evidence files, not runtime architecture.
- 2026-05-19: implemented assets-first validation as a scoped `plan` plus `assets/` contract -> keeps flat skills valid while allowing M2 to introduce the real packaged assets.
- 2026-05-19: structural fingerprints normalize asset body text after removing metadata comments and normalizing visible placeholders -> catches template drift without treating the metadata header itself as template content.

## Surprises and discoveries

- Initial placeholder validation counted HTML metadata comments as placeholders; the validator now checks asset body text after metadata comments are removed.

## Validation notes

- M1 tests were written before validator implementation. Initial `python scripts/test-skill-validator.py` failed for the new negative plan asset fixtures because the generic packaged-resource validator accepted malformed assets.
- `python scripts/test-skill-validator.py` passed after adding scoped plan asset-pilot validation.
- `python scripts/validate-skills.py` passed.
- `python scripts/test-skill-validator.py` passed with 128 tests after adding the APD-CR1 missing resource-map-entry fixture.
- `python scripts/validate-skills.py` passed after the APD-CR1 fixture addition.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml` passed after APD-CR1 resolution.
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills` passed after APD-CR1 resolution.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/code-review-m1-r1.md` passed after APD-CR1 resolution.
- `git diff --check --` passed after APD-CR1 resolution.
- `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md` passed after APD-CR1 resolution with selected checks `skills.regression`, `skills.generation_regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml` passed.
- `git diff --check -- scripts tests docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md docs/plan.md` passed.
- `bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design --path docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml --path docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md --path docs/plan.md` passed with selected checks `skills.regression`, `skills.generation_regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.

## Outcome and retrospective

- Pending downstream implementation and final closeout.

## Readiness

- See `Current Handoff Summary`.
- Ready for M1 code-review rerun. Readiness is not Done; all remaining implementation and downstream gates remain open.
