# Proposal-Family Assets Progressive Disclosure

- Status: done
Plan lifecycle state: done
Terminal disposition: merged
- Owner: maintainers
- Start date: 2026-05-20
- Last updated: 2026-05-26
- Related issue or PR: PR #81
- Supersedes: none

## Purpose / big picture

Implement the approved proposal-family assets progressive-disclosure contract for `proposal` and `proposal-review` in small reviewable slices. The change extracts substantial output structures into packaged `assets/` while preserving skill behavior, keeping rules in `SKILL.md`, proving generated-output packaging, and recording behavior-parity, token-cost, and cold-read evidence.

## Source artifacts

- Proposal: `docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md`
- Spec: `specs/proposal-family-assets-progressive-disclosure.md`
- Architecture: not-required; the approved spec preserves adapter roots, lockfile semantics, CLI behavior, and runtime architecture.
- Test spec: `specs/proposal-family-assets-progressive-disclosure.test.md`

## Context and orientation

- Canonical authored skill sources are under `skills/proposal/` and `skills/proposal-review/`.
- Generated local skill mirrors and public adapter archives are derived output. Do not hand-edit generated output.
- The existing skill-contract and prior assets-first work already define packaged assets, resource maps, `COPY`, metadata, placeholder policy, generated-output proof, and token-cost measurement expectations.
- This change is behavior-preserving. Review should compare extracted structures against the pinned baseline summary before accepting any skill text changes.
- `proposal` is constructive and may use one full skeleton asset.
- `proposal-review` is deliberative and may use only narrow result and material-finding assets.

## Non-goals

- Do not add packaged `references/`, packaged `scripts/`, build-time partials, or include syntax.
- Do not change routing descriptions for `proposal` or `proposal-review`.
- Do not change proposal status values, Vision fit values, initial-goal treatment values, scope-budget treatment values, review status values, recording status values, review-dimension results, or vision-conflict outcomes.
- Do not change required proposal sections, proposal-review dimensions, material-finding requirements, standing artifact gate rules, scope-preservation rules, recording rules, or handoff behavior.
- Do not touch `spec`, `spec-review`, `test-spec`, `plan`, `code-review`, `verify`, or `pr` assets in this initiative.
- Do not change adapter install roots, lockfile semantics, CLI behavior, release archive trust boundaries, or canonical skill source location.
- Do not retroactively rewrite legacy adapter archives.

## Requirements covered

- PFA-R1-PFA-R4: M2, M3
- PFA-R5-PFA-R6: M2, M3, M4
- PFA-R7-PFA-R16: M2
- PFA-R17-PFA-R22: M2
- PFA-R23-PFA-R28: M1, M3
- PFA-R29-PFA-R32: M1, M2, M3
- PFA-R33-PFA-R39: M1, M2, M3
- PFA-R40-PFA-R45: M4
- PFA-R46-PFA-R50: M4
- PFA-R51-PFA-R52: M1
- PFA-R53-PFA-R55: plan-review and test-spec gates before M1

## Current Handoff Summary

- Current milestone: final closeout
- Current milestone state: done
- Last reviewed milestone: M4. Generated Output, Token, Cold-Read, and Lifecycle Evidence
- Review status: code-review M4 R1 clean-with-notes; no material findings
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: done
- Reason final closeout is or is not ready: PR #81 merged into `main` on 2026-05-21.

## Milestones

### M1. Baseline and Validator Foundation

- Milestone state: closed
- Goal: Create the pinned behavior baseline and deterministic validator/test coverage needed before changing skill text.
- Requirements: PFA-R23-PFA-R28, PFA-R29-PFA-R32, PFA-R33-PFA-R39, PFA-R51-PFA-R52
- Files/components likely touched:
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - validator fixtures under `tests/` or script-owned fixture areas, if needed
- Dependencies:
  - Plan-review approved.
  - `specs/proposal-family-assets-progressive-disclosure.test.md` approved.
  - Source commit or branch point selected for baseline identity.
- Tests to add/update:
  - Positive and negative asset metadata, `COPY`, placeholder, and baseline-summary checks.
  - Positive and negative `proposal-review` structural-label allowlist checks.
  - Negative forbidden-label checks for `Recording-status rules`, `Material-finding sufficiency`, `Vision fit review`, `Scope-preservation rules`, `Severity policy`, and related policy labels.
  - Generated-output presence helper coverage if not already sufficient.
- Implementation steps:
  - Create the baseline summary before editing `skills/proposal/` or `skills/proposal-review/`.
  - Record source commit or branch point, canonical source paths, source hashes or section hashes, existing skeleton fields, conditional sections, enum/rule ownership, review dimensions, recording obligations, and planned asset destinations.
  - Add or extend deterministic validator helpers and tests for proposal-family asset constraints.
  - Keep semantic or broad-language scoring out of validators.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check --`
- Expected observable result: Baseline evidence exists and validator tests fail for policy-shaped review asset labels while accepting approved structural labels.
- Implementation evidence:
  - Created `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md` before editing `skills/proposal/` or `skills/proposal-review/`.
  - Added proposal-family asset inventory, metadata, resource-map, placeholder, forbidden resource-class, generated-output presence, and baseline-summary fixture coverage.
  - Added deterministic `proposal-review` structural-label allowlist and forbidden review-policy label checks.
  - Extended generated asset presence mapping to include proposal-family skills.
  - Created `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml`.
- Commit message: `M1: add proposal-family asset validator foundation`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - result: closed by code-review M1 R2 after `PFA-M1-CR1` resolution
- Risks:
  - Validator may overblock legitimate field labels.
  - Baseline may be too vague for later code review.
- Rollback/recovery:
  - Narrow validator checks to explicit labels and fixtures.
  - Regenerate baseline from pinned source commit or branch point with exact hashes and headings.

### M2. Proposal Skeleton Asset

- Milestone state: closed
- Goal: Extract the `proposal` output skeleton into `assets/proposal-skeleton.md` without changing proposal behavior or conditional section triggers.
- Requirements: PFA-R1-PFA-R5, PFA-R7-PFA-R22, PFA-R29-PFA-R39
- Files/components likely touched:
  - `skills/proposal/SKILL.md`
  - `skills/proposal/assets/proposal-skeleton.md`
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`
  - change-local preservation or parity evidence
- Dependencies:
  - M1 closed.
- Tests to add/update:
  - `skills/proposal/SKILL.md` validates with the new resource map.
  - Asset metadata, placeholder policy, `COPY` mapping, and conditional-section behavior are covered.
- Implementation steps:
  - Add `assets/proposal-skeleton.md` with required metadata comments.
  - Add a `COPY` resource-map entry to `skills/proposal/SKILL.md`.
  - Replace the full inline skeleton with a compact output expectation summary.
  - Preserve `Initial intent preservation` and `Scope budget` as trigger-based sections.
  - Record source-to-asset parity for the extracted proposal skeleton and conditional sections.
- Validation commands:
  - `python scripts/validate-skills.py skills/proposal/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check --`
- Expected observable result: `proposal` ships one mapped skeleton asset, keeps rules in `SKILL.md`, and preserves conditional section behavior.
- Implementation evidence:
  - Added `skills/proposal/assets/proposal-skeleton.md` with required metadata and the same full skeleton section set as the pinned baseline.
  - Added a `COPY` resource-map entry to `skills/proposal/SKILL.md` naming fill structures, conditional section insertion behavior, and no-placeholder guidance.
  - Replaced the full inline skeleton in `skills/proposal/SKILL.md` with compact asset-copy guidance.
  - Preserved `Initial intent preservation` and `Scope budget` as trigger-based sections governed by `SKILL.md`.
  - Recorded M2 source-to-asset preservation, behavior parity, and asset contract evidence in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md`.
- Commit message: `M2: extract proposal skeleton asset`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - result: closed by code-review M2 R1
- Risks:
  - Full skeleton extraction could hide too much contract surface.
  - Conditional sections could become mandatory or disappear.
- Rollback/recovery:
  - Reinline the full skeleton into `skills/proposal/SKILL.md`.
  - Keep validator improvements from M1 if still valid.

### M3. Proposal-Review Structural Assets

- Milestone state: closed
- Goal: Extract narrow `proposal-review` result and material-finding structures into assets without moving review judgment or review policy out of `SKILL.md`.
- Requirements: PFA-R1-PFA-R6, PFA-R10-PFA-R13, PFA-R23-PFA-R39, PFA-R51-PFA-R52
- Files/components likely touched:
  - `skills/proposal-review/SKILL.md`
  - `skills/proposal-review/assets/review-result-skeleton.md`
  - `skills/proposal-review/assets/material-finding.md`
  - validator tests or fixtures from M1 if M3 exposes gaps
  - change-local preservation or parity evidence
- Dependencies:
  - M1 closed.
  - M2 closed or explicitly not in conflict.
- Tests to add/update:
  - `skills/proposal-review/SKILL.md` validates with the new resource map.
  - Positive structural labels such as `Recording status` and `Severity` pass.
  - Forbidden policy labels such as `Recording-status rules`, `Material-finding sufficiency`, `Vision fit review`, `Scope-preservation rules`, and `Severity policy` fail.
- Implementation steps:
  - Add `review-result-skeleton.md` and `material-finding.md` with required metadata comments.
  - Add `COPY` resource-map entries to `skills/proposal-review/SKILL.md`.
  - Replace inline output skeleton material with a compact output expectation summary.
  - Keep review dimensions, policies, rules, statuses, recording obligations, and handoff behavior in `SKILL.md`.
  - Record source-to-asset parity for review result fields and material-finding fields.
- Validation commands:
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check --`
- Expected observable result: `proposal-review` ships only the two approved structural assets and remains self-contained for review judgment.
- Implementation evidence:
  - Added `skills/proposal-review/assets/review-result-skeleton.md` with required metadata and only the approved result, review-dimensions placeholder, scope-preservation result, recommended edits, and recommendation structural fields.
  - Added `skills/proposal-review/assets/material-finding.md` with required metadata and only finding ID, severity, location, evidence, required outcome, safe resolution path, and needs-decision rationale fields.
  - Added `COPY` resource-map entries to `skills/proposal-review/SKILL.md` for the review result skeleton and one material-finding block per material finding.
  - Replaced the full inline output skeleton in `skills/proposal-review/SKILL.md` with compact asset-copy guidance.
  - Preserved review dimensions, policies, rules, statuses, recording obligations, and handoff behavior in `SKILL.md`.
  - Recorded M3 source-to-asset preservation, behavior parity, and review-class asset boundary evidence in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md`.
- Commit message: `M3: extract proposal-review structural assets`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
  - result: closed by code-review M3 R2 after `PFA-M3-CR1` resolution
- Risks:
  - Review-class asset field labels could allow hidden policy.
  - `SKILL.md` could lose review judgment during skeleton compression.
- Rollback/recovery:
  - Reinline review result and material-finding structures into `skills/proposal-review/SKILL.md`.
  - Keep deterministic review-class validator fixes if still valid.

### M4. Generated Output, Token, Cold-Read, and Lifecycle Evidence

- Milestone state: review-requested
- Goal: Prove generated skill mirrors and temporary adapter packages include proposal-family assets, record token-cost and cold-read evidence, and prepare final lifecycle evidence.
- Requirements: PFA-R40-PFA-R50
- Files/components likely touched:
  - generated local skill mirror check output or evidence records
  - temporary adapter output outside tracked source
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/`
  - `docs/plan.md`
  - this plan body
- Dependencies:
  - M2 and M3 closed.
- Tests to add/update:
  - Generated skill mirror asset presence proof.
  - Temporary adapter output asset presence proof.
  - Adapter validation proof.
  - Token-cost evidence with common-path size, total packaged footprint, and P.
  - Cold-read proof from installed skill output alone.
- Implementation steps:
  - Run generated skill mirror check or build command.
  - Build temporary adapter output using the repository version.
  - Validate generated adapter output.
  - Record generated-output proof and no-hand-edit evidence.
  - Run token measurement and record P for each asset.
  - Record cold-read proof and representative no-placeholder output proof.
  - Update plan progress, validation notes, and lifecycle state before downstream handoff.
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"`
  - `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md`
  - `git diff --check --`
- Expected observable result: Generated outputs include mapped assets, adapter validation passes or records a blocker, token/cold-read evidence is recorded, and lifecycle state is ready for explain-change and verify after all implementation reviews close.
- Commit message: `M4: record proposal-family asset generated-output evidence`
- Implementation evidence:
  - Recorded `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/generated-output-proof.md`.
  - Proved generated skill mirror asset presence under `/tmp/rigorloop-pfa-m4-skills-final-wybuIX/skills`.
  - Built and validated temporary `v0.1.5` adapter archives under `/tmp/rigorloop-pfa-m4-adapters-final-bT9gTu`.
  - Inspected Codex, Claude, and opencode archive contents with Python `zipfile`; all three proposal-family assets were present under each adapter root.
  - Ran tracked-tree adapter check and recorded the known expanded-adapter-layout deferral after temporary generated proof passed.
  - Recorded common-path token deltas, total packaged deltas, P estimates, cold-read evidence, representative no-placeholder evidence, and no-hand-edit evidence.
  - Trimmed duplicated `proposal/SKILL.md` output/resource-map wording so both touched common-path skill bodies are smaller than the pinned baseline while keeping asset usage and conditional-section guidance intact.
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Temporary adapter validation may expose unrelated tracked-tree debt.
  - Total packaged footprint may grow for `proposal-skeleton.md`.
- Rollback/recovery:
  - Record tracked-tree debt deferral only when generated mirror proof, temporary adapter proof, and adapter validation evidence are complete or explicitly blocked.
  - Reinline assets and rerun generated-output validation if packaging cannot be proven.

- Code-review closeout: closed by code-review M4 R1.

## Validation plan

- `python scripts/test-skill-validator.py`: deterministic validator and fixture coverage.
- `python scripts/validate-skills.py`: canonical skill contract validation.
- `python scripts/validate-skills.py skills/proposal/SKILL.md`: focused proposal skill validation.
- `python scripts/validate-skills.py skills/proposal-review/SKILL.md`: focused proposal-review skill validation.
- `python scripts/build-skills.py --check`: generated skill mirror proof.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"`: temporary adapter generation.
- `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`: temporary adapter validation.
- `python scripts/measure-skill-tokens.py`: common-path, total packaged footprint, and P evidence.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`: review closeout validation.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md`: lifecycle validation.
- `git diff --check --`: whitespace and patch hygiene.

## Risks and recovery

- Risk: Full skeleton extraction hides too much visible contract surface.
  - Recovery: Reinline the skeleton and record fallback evidence.
- Risk: Conditional proposal sections change behavior.
  - Recovery: Restore trigger wording in `SKILL.md` and preserve optional/labeled conditional blocks only.
- Risk: Review-class assets admit hidden policy labels.
  - Recovery: Tighten structural allowlist and forbidden-label fixtures.
- Risk: Generated adapter proof misses assets.
  - Recovery: Fix generation or packaging from canonical skill source; do not hand-edit generated output.
- Risk: Token-cost evidence is misread as total-token optimization.
  - Recovery: Record common-path size, total packaged footprint, and P separately.

## Dependencies

- Plan-review must approve this plan before implementation.
- Matching test spec must be created and approved before implementation.
- If the existing skill-contract rules are insufficient, a skill-contract spec amendment packet must be created before skill edits.
- Repository version value is needed for temporary adapter generation and validation.
- Temporary directory for adapter output is needed during M4.

## Progress

- 2026-05-20: Plan created after proposal acceptance, spec approval, and clean spec-review R1.
- 2026-05-20: Clean plan-review R1 recorded; matching test spec created as the active proof surface for implementation.
- 2026-05-20: M1 implemented and set to `review-requested` after validator and skill validation passed.
- 2026-05-20: Code-review M1 R1 recorded `PFA-M1-CR1`; M1 moved to `resolution-needed`.
- 2026-05-20: Accepted and resolved `PFA-M1-CR1` by making the `proposal-review` asset structural-label allowlist closed for field-label-shaped lines, adding neutral non-allowlisted label fixtures, and returning M1 to `review-requested` for code-review rerun.
- 2026-05-20: code-review M1 R2 returned clean-with-notes; M1 closed and next stage is implement M2.
- 2026-05-20: M2 implementation started for `skills/proposal/SKILL.md`, `skills/proposal/assets/proposal-skeleton.md`, and proposal preservation evidence only.
- 2026-05-20: M2 extracted `assets/proposal-skeleton.md`, updated `skills/proposal/SKILL.md` resource-map and compact output guidance, recorded preservation evidence, and moved to `review-requested`.
- 2026-05-20: code-review M2 R1 returned clean-with-notes; M2 closed and next stage is implement M3.
- 2026-05-20: M3 extracted `assets/review-result-skeleton.md` and `assets/material-finding.md`, updated `skills/proposal-review/SKILL.md` resource-map and compact output guidance, recorded preservation evidence, and moved to `review-requested`.
- 2026-05-20: code-review M3 R1 recorded `PFA-M3-CR1`; M3 moved to `resolution-needed`.
- 2026-05-20: Accepted and resolved `PFA-M3-CR1` by restoring the pinned `## Result` heading and literal `Skill` field, adding direct validator coverage, and returning M3 to `review-requested` for code-review rerun.
- 2026-05-20: code-review M3 R2 returned clean-with-notes; M3 closed and next stage is implement M4.
- 2026-05-20: M4 recorded generated skill mirror proof, temporary adapter archive proof, adapter validation, tracked-tree adapter deferral, token/P evidence, cold-read evidence, and no-hand-edit evidence; M4 moved to `review-requested`.
- 2026-05-20: code-review M4 R1 returned clean-with-notes; all implementation milestones are closed and the next stage is final closeout sequence starting with explain-change.
- 2026-05-20: Explain-change recorded durable rationale in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/explain-change.md`; next stage is verify.
- 2026-05-20: Final local verify passed, `verify-report.md` was recorded, and the branch is ready for PR handoff.
- 2026-05-20: Opened PR #81 for hosted CI and human review.
- 2026-05-21: PR #81 merged into `main` at `cbac052bd4baffedeae28d50a8569cbf4759195c`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-20 | No architecture package required. | The approved spec preserves adapter roots, lockfile semantics, CLI behavior, generated-output trust boundaries, and runtime architecture; the work is a skill asset extraction and validation slice. | Create architecture or ADR for unchanged architecture surfaces. |
| 2026-05-20 | Keep test-spec as a pre-implementation gate. | PFA-R53 requires the matching test spec to be approved before implementation begins. | Start M1 immediately after plan-review. |
| 2026-05-20 | Split `proposal` and `proposal-review` into separate implementation milestones. | Separate milestones reduce review risk across constructive and deliberative skill asset boundaries. | Extract both skills in one milestone. |
| 2026-05-20 | No skill-contract amendment is required before M1. | Existing `specs/skill-contract.md` asset rules plus the approved proposal-family spec and active test spec are sufficient for baseline and deterministic validator work. | Stop M1 for a spec amendment before any skill text is changed. |

## Surprises and discoveries

- M1 did not require edits to canonical skill text. The baseline captured the pinned source state before any `skills/proposal/` or `skills/proposal-review/` edits.
- Existing spec-family validator helpers were close enough to reuse as a bounded pattern, but proposal-review needed a separate allowlist and forbidden-label set because its review-policy surfaces differ.
- Code-review found that the allowlist is not yet enforced for otherwise neutral non-allowlisted labels; M1 must resolve `PFA-M1-CR1` before M2.
- Resolution for `PFA-M1-CR1` keeps the stricter closed allowlist scoped to `proposal-review` assets only; constructive assets such as `proposal-skeleton.md` are unaffected.
- M2 keeps token-cost, P, cold-read, generated mirror, and temporary adapter proof in M4. M2 records preservation and behavior-parity evidence for the `proposal` extraction only.
- M3 keeps generated mirror, temporary adapter proof, token-cost, P, cold-read, and representative no-placeholder proof in M4. M3 records preservation and behavior-parity evidence for the `proposal-review` structural extraction only.
- Code-review found that `review-result-skeleton.md` did not preserve the pinned `Skill` result field or `## Result` heading shape; M3 must resolve `PFA-M3-CR1` before M4.
- Resolution for `PFA-M3-CR1` adds direct validator coverage for the pinned proposal-review result skeleton heading and `Skill` field, so a future extraction cannot silently drop that baseline field while preserving only allowed-label checks.
- M4 confirmed that packaged totals grow while common-path bodies shrink. `proposal-skeleton.md` keeps a high P estimate, so the asset is justified by common-path readability and maintainability instead of total-token reduction.
- `proposal/SKILL.md` needed a small duplicate-wording trim during M4 because the initial M2 extraction reduced lines but left the local token estimate slightly above the pinned baseline. The final estimate is 3308 tokens versus the 3368-token baseline.
- The tracked-tree adapter check still reports known expanded-layout debt for `dist/adapters/` with `total=112`, `missing=111`, and `manifest-error=1`; temporary adapter archive generation, validation, and archive inspection passed.

## Aligned-surface audit

- `skills/proposal/`: unaffected in M1; baseline captured the source state for M2 before skill edits.
- `skills/proposal/`: M2 adds only `assets/proposal-skeleton.md` and compact `SKILL.md` resource-map/output guidance; rules, enums, gates, scope preservation, scope budget, decision-quality checks, artifact placement, and handoff behavior remain in `SKILL.md`.
- `skills/proposal-review/`: unaffected in M1; baseline captured the source state for M3 before skill edits.
- `skills/proposal-review/`: M3 adds only `assets/review-result-skeleton.md`, `assets/material-finding.md`, and compact `SKILL.md` resource-map/output guidance; review dimensions, review statuses, recording statuses, material-finding sufficiency, scope preservation, scope budget, Vision fit review, standing gates, isolation, recording, artifact placement, and handoff behavior remain in `SKILL.md`.
- Generated skill mirrors and adapter packages: M4 generated mirror, temporary adapter archive, and archive inspection proof passed; tracked-tree expanded adapter check is deferred as known debt.
- `specs/skill-contract.md`: unaffected in M1; no amendment needed before validator foundation work.
- `docs/plan.md`: updated only as the active plan index; milestone journal details remain in this plan body.
- `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/explain-change.md`: records rationale only and does not own final verify or PR readiness.
- `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/verify-report.md`: records branch-ready verification and hands off to `pr`; it does not claim PR-body readiness or hosted CI success.

## Validation notes

- 2026-05-20: Plan-review handoff validation passed before test-spec authoring:
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md`
  - `git diff --check --`
- 2026-05-20: Test-spec handoff validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md`
  - `git diff --check --`
- 2026-05-20: M1 validation passed:
  - `python scripts/test-skill-validator.py` - pass, 150 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass, reviews=4, findings=4, log_entries=4, resolution_entries=4
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md` - pass, validated 3 artifact files
  - `git diff --check --` - pass
- 2026-05-20: M1 review-resolution validation for `PFA-M1-CR1` passed:
  - `python scripts/test-skill-validator.py` - pass, 151 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md` - pass
  - `git diff --check --` - pass
- 2026-05-20: M2 validation passed:
  - `python scripts/validate-skills.py skills/proposal/SKILL.md` - pass, validated 1 skill file
  - `python scripts/test-skill-validator.py` - pass, 151 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md` - pass
  - `git diff --check --` - pass
- 2026-05-20: M3 validation passed:
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md` - pass, validated 1 skill file
  - `python scripts/test-skill-validator.py` - pass, 151 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass, reviews=7, findings=5, log_entries=7, resolution_entries=5
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m2-r1.md` - pass, validated 3 artifact files
  - `git diff --check --` - pass
- 2026-05-20: M3 review-resolution validation for `PFA-M3-CR1` passed:
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md` - pass, validated 1 skill file
  - `python scripts/test-skill-validator.py` - pass, 152 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass, reviews=8, findings=6, log_entries=8, resolution_entries=6
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m2-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md` - pass, validated 3 artifact files
  - `git diff --check --` - pass
- 2026-05-20: code-review M3 R2 recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass, reviews=9, findings=6, log_entries=9, resolution_entries=6
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m2-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r2.md` - pass, validated 3 artifact files
  - `git diff --check --` - pass
- 2026-05-20: M4 generated-output and token proof passed:
  - `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-pfa-m4-skills-final-wybuIX/skills` - pass, generated proposal-family assets present
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` - pass, built Codex, Claude, and opencode adapter archives
  - `python scripts/validate-adapters.py --root /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu --version v0.1.5` - pass
  - Python `zipfile` inspection against `/tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` - pass, all three proposal-family assets present in all three adapter archives
  - `python scripts/build-adapters.py --check --version v0.1.5 --verbose` - expected tracked-tree deferral, `total=112`, `missing=111`, `manifest-error=1`
  - `python scripts/measure-skill-tokens.py` - pass, 23 skills, 250084 bytes, 62509 estimated tokens
  - `python scripts/validate-skills.py skills/proposal/SKILL.md` - pass after final `proposal` wording trim
  - `python scripts/test-skill-validator.py` - pass, 152 tests
  - `python scripts/validate-skills.py` - pass, validated 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass, reviews=9, findings=6, log_entries=9, resolution_entries=6
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.md --path specs/proposal-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/generated-output-proof.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/proposal-review-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/spec-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/plan-review-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m2-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md --path docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r2.md` - pass, validated 3 artifact files
  - `git diff --check --` - pass

## Outcome and retrospective

- PR #81 merged into `main`.

## Readiness

- Done. PR #81 merged and no downstream lifecycle gates remain.
