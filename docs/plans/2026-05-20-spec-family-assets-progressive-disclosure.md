# Spec-Family Assets Progressive Disclosure Plan

- Status: done
- Owner: maintainers
- Start date: 2026-05-20
- Last updated: 2026-05-20
- Related issue or PR: none yet
- Supersedes: none

## Goal

Implement the approved spec-family assets progressive-disclosure contract by adding skill-local structural assets to `spec`, `spec-review`, and `test-spec`, while preserving PR #79 behavior and proving generated skill and adapter output carry the assets.

## Why now

PR #79 completed the spec-family readability pass and left spec-family packaging as the next follow-up. The accepted proposal and approved spec now define the narrower assets-only contract, including review-class boundaries for `spec-review` and generated-output proof requirements.

## Scope

### In scope

- Create the change-local baseline summary before skill edits.
- Add validator and fixture coverage for mapped assets, `COPY`, metadata, statuses, placeholders, review-class boundaries, generated-output presence, and baseline-summary presence.
- Add `assets/` to `skills/spec/`, `skills/spec-review/`, and `skills/test-spec/`.
- Update each touched `SKILL.md` with a resource map and compact output expectation summaries where full skeleton assets are used.
- Record preservation matrices, behavior parity, token-cost evidence, generated mirror proof, temporary adapter archive proof, adapter validation, and cold-read proof.
- Keep the active plan and plan index synchronized through downstream gates.

### Out of scope

- Packaged `references/`.
- Packaged `scripts/`.
- Build-time partials or include syntax.
- Routing-description changes.
- Normative rule, stop-condition, enum, review-dimension, coverage-obligation, lifecycle-boundary, or produced-artifact behavior changes.
- Adapter install-root, lockfile, CLI behavior, or release archive trust-boundary changes.
- Generated adapter hand edits or retroactive legacy archive rewrites.
- Asset work for unrelated lifecycle skills.

## Constraints

- `SKILL.md` remains the installed skill operating contract.
- Assets are copied structures, not hidden rules.
- PR #79 remains the authoritative behavior baseline.
- `spec-review` assets are limited to `review-result-skeleton.md` and `review-finding.md`.
- `spec` is limited to `spec-skeleton.md`; trivial requirement, acceptance-criterion, and decision-log row formats stay inline.
- `test-spec` is limited to `test-spec-skeleton.md`, `test-case.md`, and `coverage-map-row.md`; trivial edge-case row format stays inline.
- Generated mirror proof and temporary adapter archive proof are mandatory.
- Tracked-tree adapter debt may be deferred only with explicit rationale after temporary generated output proof is preserved.
- Implementation must not start until plan-review passes and the matching test spec is approved.

## Source artifacts

- Proposal: `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md`
- Spec: `specs/spec-family-assets-progressive-disclosure.md`
- Proposal review: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/proposal-review-r2.md`
- Spec review: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/spec-review-r1.md`
- Change metadata: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- Related baseline: PR #79 and `docs/changes/2026-05-20-spec-family-readability-pass/`
- Governing contract: `specs/skill-contract.md`

## Context and orientation

`specs/skill-contract.md` already defines generic packaged-resource behavior and the `plan` assets-first pilot. This initiative extends the pattern to the spec family through the focused spec rather than changing the old `plan` pilot clauses.

The work touches canonical skill source under `skills/`, validator and test scripts, change-local evidence, generated mirrors, and temporary adapter archives. Generated public adapter bodies remain derived output and must not be hand-edited.

## Requirements covered

- `SFA-R1` through `SFA-R45`
- `AC-SFA-001` through `AC-SFA-015`
- Proposal acceptance criteria `AC-SFA-001` through `AC-SFA-014`

## Current Handoff Summary

- Current milestone: M6
- Current milestone state: closed
- Last reviewed milestone: M6
- Review status: code-review M6 R1 clean-with-notes; no material findings
- Remaining in-scope implementation milestones: none
- Next stage: done
- Final closeout readiness: done
- Reason final closeout is or is not ready: PR #80 merged on 2026-05-20; hosted CI and human review are complete.

## Milestones

### M1. Baseline summary and validator foundation

- Milestone state: closed
- Goal: Create the change-local baseline summary and deterministic validation coverage before skill text changes.
- Requirements: `SFA-R25` through `SFA-R29`, `SFA-R42`, `SFA-R43`, `AC-SFA-014`, `AC-SFA-015`
- Files expected:
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - validator fixtures as needed
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
- Steps:
  - Record PR #79 baseline structures per skill before skill edits.
  - Assess whether `specs/skill-contract.md` plus this spec is sufficient for multi-skill rollout, full-skeleton boundaries, and review-class restrictions.
  - Add deterministic checks for asset mapping, `COPY`, metadata, status values, placeholders, review-class asset boundaries, generated-output presence, and baseline-summary presence.
  - Record no-spec-amendment rationale or stop for a skill-contract amendment if the sufficiency assessment fails.
- Validation:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/spec-family-assets-progressive-disclosure.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- Result: closed by code-review M1 R2 after `SFA-M1-CR1` resolution.
- Risks:
  - Validator overblocks legitimate assets; keep checks deterministic and use bounded heuristics only where declared.
- Rollback:
  - Revert validator and fixture changes; keep review artifacts intact.

### M2. `spec` assets

- Milestone state: closed
- Goal: Add `spec` structural assets and resource-map guidance without changing behavior.
- Requirements: `SFA-R1` through `SFA-R4`, `SFA-R7`, `SFA-R8`, `SFA-R14` through `SFA-R22`, `SFA-R28` through `SFA-R31`, `SFA-R38` through `SFA-R41`
- Files expected:
  - `skills/spec/SKILL.md`
  - `skills/spec/assets/spec-skeleton.md`
  - change-local preservation, parity, token, and cold-read evidence
- Per-asset justification:
  - `spec-skeleton.md`: used once per new spec; full output skeleton asset to reduce common-path body while keeping compact summary in `SKILL.md`.
- Inline formats: requirement, acceptance-criterion, and decision-log rows stay in `SKILL.md` because they are one-line structures already covered by inline format guidance.
- Validation:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - M2 preservation and behavior-parity evidence inspection
  - `git diff --check -- .`
- Result: closed by code-review M2 R3 after `SFA-M2-CR1` resolution.
- Current correction: M6 removed the three trivial row assets and their resource-map entries.
- Risks:
  - Full skeleton asset hides too much contract surface; fall back to inline skeleton for `spec` if code review finds that risk.
- Rollback:
  - Reinline `spec` skeleton/substructure content and remove `skills/spec/assets/`.

### M3. `spec-review` assets

- Milestone state: closed
- Goal: Add narrow review-class assets for `spec-review` while keeping review judgment in `SKILL.md`.
- Requirements: `SFA-R1` through `SFA-R3`, `SFA-R6`, `SFA-R9`, `SFA-R10`, `SFA-R14`, `SFA-R15`, `SFA-R19` through `SFA-R24`, `SFA-R28` through `SFA-R31`, `SFA-R38` through `SFA-R41`
- Files expected:
  - `skills/spec-review/SKILL.md`
  - `skills/spec-review/assets/review-result-skeleton.md`
  - `skills/spec-review/assets/review-finding.md`
  - change-local preservation, parity, token, and cold-read evidence
- Per-asset justification:
  - `review-result-skeleton.md`: used once per review; structural result scaffold with no review policy.
  - `review-finding.md`: used once per material finding; repeated structural block with stable fields.
- Validation:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - M3 preservation and behavior-parity evidence inspection
  - `git diff --check -- skills/spec-review docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- Result: closed by code-review M3 R2 after `SFA-M3-CR1` resolution.
- Risks:
  - `review-finding.md` accumulates hidden review policy; enforce `SFA-R23` and `SFA-R24` through validator and code review.
- Rollback:
  - Reinline `spec-review` result/finding structures and remove `skills/spec-review/assets/`.

### M4. `test-spec` assets

- Milestone state: closed
- Goal: Add `test-spec` structural assets and resource-map guidance without changing coverage obligations.
- Requirements: `SFA-R1` through `SFA-R3`, `SFA-R5`, `SFA-R11`, `SFA-R12`, `SFA-R14` through `SFA-R22`, `SFA-R28` through `SFA-R31`, `SFA-R38` through `SFA-R41`
- Files expected:
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec/assets/test-spec-skeleton.md`
  - `skills/test-spec/assets/test-case.md`
  - `skills/test-spec/assets/coverage-map-row.md`
  - change-local preservation, parity, token, and cold-read evidence
- Per-asset justification:
  - `test-spec-skeleton.md`: used once per test spec; full output skeleton asset to reduce common-path body while keeping compact summary in `SKILL.md`.
  - `test-case.md`: used once per test case; repeated test case block.
  - `coverage-map-row.md`: used once per requirement or example coverage mapping; preserves separate requirement and example row variants.
- Inline format: edge-case coverage stays in `SKILL.md` because it is a trivial one-line mapping.
- Validation:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - M4 preservation and behavior-parity evidence inspection
  - `git diff --check -- skills/test-spec docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- Result: closed by code-review M4 R2 after `SFA-M4-CR1` resolution.
- Current correction: M6 removed the trivial `edge-case-row.md` asset and its resource-map entry.
- Validation evidence after `SFA-M4-CR1` fix:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/test-skill-validator.py` passed with 142 tests.
  - `git diff --check -- .` passed.
  - Change metadata, explicit-path artifact lifecycle, and review artifact closeout validation passed.
- Risks:
  - Full skeleton asset hides coverage obligations; keep coverage rules in `SKILL.md` and fall back to inline skeleton if needed.
- Rollback:
  - Reinline `test-spec` skeleton/substructure content and remove `skills/test-spec/assets/`.

### M5. Generated output, family proof, and closeout

- Milestone state: closed
- Goal: Prove generated mirrors and temporary adapter packages include all mapped assets, then prepare final lifecycle closeout.
- Requirements: `SFA-R32` through `SFA-R41`, `AC-SFA-008` through `AC-SFA-013`
- Files expected:
  - generated mirror check evidence
  - temporary adapter output evidence
  - token-cost evidence
  - cold-read evidence
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/explain-change.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/verify-report.md`
- Validation:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`
  - `python scripts/validate-adapters.py --root <tmpdir> --version <version>`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `git diff --check -- .`
- Result: closed by code-review M5 R1 after generated mirror proof, temporary adapter archive proof, token evidence, cold-read evidence, and tracked-tree deferral were recorded.
- Validation evidence:
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/build-skills.py --output-dir /tmp/rigorloop-m5-skills-mirror` passed; mirror inspection found all mapped spec-family assets.
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m5-adapters-db7QUP` passed.
  - `python scripts/validate-adapters.py --root /tmp/rigorloop-m5-adapters-db7QUP --version v0.1.5` passed.
  - Python `zipfile` archive inspection found all mapped spec-family assets in Codex, Claude, and opencode temporary adapter archives.
  - `python scripts/build-adapters.py --check --version v0.1.5 --verbose` failed on known missing tracked expanded adapter files under `dist/adapters/`; deferred after temporary archive proof under `SFA-R36`.
  - `python scripts/measure-skill-tokens.py` passed.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/test-skill-validator.py` passed with 142 tests.
- Risks:
  - Tracked-tree adapter debt is confused with temporary archive proof; record separate deferral only when allowed by `SFA-R36`.
- Rollback:
  - Rebuild generated outputs from reverted canonical skills; preserve generic validator changes only when still valid.

### M6. Lean asset correction

- Milestone state: closed
- Goal: Remove low-value row assets and align the contract, validators, generated-output expectations, and evidence with the substantial-template rule.
- Requirements: `SFA-R3A` through `SFA-R3C`, `SFA-R8`, `SFA-R12`, `SFA-R14` through `SFA-R22`, `SFA-R28` through `SFA-R41`
- Files expected:
  - `skills/spec/SKILL.md`
  - `skills/spec/assets/spec-skeleton.md`
  - `skills/test-spec/SKILL.md`
  - `skills/test-spec/assets/test-spec-skeleton.md`
  - `skills/test-spec/assets/test-case.md`
  - `skills/test-spec/assets/coverage-map-row.md`
  - `specs/spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.test.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
  - generated-output presence fixtures
  - change-local preservation, generated-output, token, and cold-read evidence
- Per-asset decision:
  - Keep `spec-skeleton.md`, `test-spec-skeleton.md`, `test-case.md`, `coverage-map-row.md`, `review-result-skeleton.md`, and `review-finding.md`.
  - Drop `requirement-row.md`, `acceptance-criterion-row.md`, `decision-log-row.md`, and `edge-case-row.md`.
- Validation:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/generated-output-proof.md`
  - `git diff --check -- .`
- Result: closed by code-review M6 R1 with no material findings.
- Risks:
  - Historical review records still mention now-removed row assets; keep them as historical evidence and update current governing/evidence surfaces instead.
- Rollback:
  - Restore removed row assets and resource-map entries only if code-review finds a current contract or usability regression.

## Validation plan

Before implementation:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md specs/spec-family-assets-progressive-disclosure.md docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`

During implementation:

- Run milestone-specific validation before each code-review handoff.
- Prefer the smallest relevant validation scope first, then expand to full skill and generated-output proof when milestones touch shared validators or generation.

Final closeout:

- Run the generated mirror and temporary adapter archive proof commands from M5.
- Run final lifecycle, review-artifact, change metadata, skill validation, token, and whitespace checks.

## Risks and recovery

- Asset hides behavior: keep rules in `SKILL.md`, require preservation matrices, and fall back to inline skeletons where needed.
- Review-class asset becomes policy: enforce `SFA-R23` and `SFA-R24` through validation and code review.
- Adapter proof is incomplete: block closeout until temporary generated adapter proof passes or a concrete blocker is recorded.
- Validator overblocks: keep checks deterministic and declare bounded heuristics before use.
- Token reduction is overstated: report common-path and total packaged footprint separately.
- Baseline drift: use PR #79 as authoritative and change-local baseline summary as review aid only.

## Dependencies

- Proposal accepted: complete.
- Spec approved: complete after upstream settlement in this planning stage.
- Spec-review: complete with no material findings.
- Plan-review: complete with no material findings.
- Matching test spec: active.
- Architecture: not required for this change because it does not alter system architecture, data flow, security boundary, deployment boundary, or public adapter roots. Validator and generated-output behavior is covered by the approved spec and test spec.

## Progress

- 2026-05-20: proposal created.
- 2026-05-20: proposal-review R1 recorded five material findings and proposal revised.
- 2026-05-20: proposal-review R2 approved with no material findings.
- 2026-05-20: proposal status settled to `accepted`.
- 2026-05-20: spec created.
- 2026-05-20: spec-review R1 approved with no material findings.
- 2026-05-20: spec status settled to `approved`.
- 2026-05-20: plan created.
- 2026-05-20: plan-review R1 approved with no material findings.
- 2026-05-20: test spec created and marked active.
- 2026-05-20: M1 implemented baseline summary, proof-route assessment, behavior-preservation scaffold, and deterministic validator coverage; milestone moved to review-requested.
- 2026-05-20: code-review M1 R1 requested changes for missing generated-output presence coverage in the validator foundation.
- 2026-05-20: accepted and resolved `SFA-M1-CR1` by adding deterministic generated-output presence helper coverage; M1 returned to review-requested.
- 2026-05-20: code-review M1 R2 returned clean-with-notes; M1 closed and next stage is implement M2.
- 2026-05-20: M2 implementation started for `spec` assets.
- 2026-05-20: M2 added the approved `spec` assets, updated `skills/spec/SKILL.md`, recorded preservation/token/cold-read evidence, and moved to review-requested.
- 2026-05-20: code-review M2 R1 requested changes because `assets/requirement-row.md` narrows requirement rows to `MUST`.
- 2026-05-20: accepted and resolved `SFA-M2-CR1` by changing `assets/requirement-row.md` to preserve the full requirement statement field, updating the `SKILL.md` resource-map entry, and recording modal-preservation evidence; M2 returned to review-requested.
- 2026-05-20: code-review M2 R3 returned clean-with-notes; M2 closed and next stage is implement M3.
- 2026-05-20: M3 added the two approved narrow `spec-review` assets, updated `skills/spec-review/SKILL.md`, tightened the review-class validator to allow structural field labels while rejecting policy prose, recorded preservation/token/cold-read evidence, and moved to review-requested.
- 2026-05-20: code-review M3 R1 requested changes because the review-class validator allows forbidden policy labels when they are shaped as field labels.
- 2026-05-20: accepted and resolved `SFA-M3-CR1` by checking forbidden policy labels before structural field exemptions, adding an explicit `spec-review` structural-label allowlist, and adding fixture coverage for policy-shaped labels; M3 returned to review-requested.
- 2026-05-20: code-review M3 R2 returned clean-with-notes; M3 closed and next stage is implement M4.
- 2026-05-20: M4 added the approved `test-spec` assets, updated `skills/test-spec/SKILL.md`, recorded preservation/token/cold-read evidence, and moved to review-requested.
- 2026-05-20: code-review M4 R1 requested changes because the coverage-map row extraction does not preserve requirement/example table row shapes.
- 2026-05-20: accepted and resolved `SFA-M4-CR1` by restoring requirement/example coverage row-shape parity; M4 returned to review-requested.
- 2026-05-20: code-review M4 R2 returned clean-with-notes; M4 closed and next stage is implement M5.
- 2026-05-20: M5 recorded generated skill mirror proof, temporary adapter archive proof, adapter validation, tracked-tree deferral, token evidence, and cold-read proof; implementation milestones were closed and next stage became final closeout starting with explain-change.
- 2026-05-20: code-review M5 R1 found no blocking or required-change findings; M5 closed.
- 2026-05-20: M6 applied the lean asset correction: dropped trivial row assets, kept substantial skeleton/block assets, updated validators, fixtures, spec, test spec, and evidence, and moved to code-review.
- 2026-05-20: code-review M6 R1 found no blocking or required-change findings; M6 closed and the next stage is final closeout starting with explain-change.
- 2026-05-20: explain-change recorded the problem-to-diff rationale, review-resolution summary, validation evidence, alternatives rejected, scope control, and remaining verify/PR handoff work; next stage is verify.
- 2026-05-20: verify found and fixed a selector routing gap for `baseline.md` and `generated-output-proof.md`, reran selector regression and PR-mode CI, recorded `verify-report.md`, and marked the branch ready for PR handoff.
- 2026-05-20: Opened PR #80 for hosted CI and human review.
- 2026-05-20: PR #80 merged; plan closed.

## Decision log

- 2026-05-20: No separate architecture package for this plan -> the change is constrained to skill text, assets, validators, generated-output proof, and lifecycle evidence; no architecture/data/security/deployment boundary changes are introduced.
- 2026-05-20: Use five implementation milestones -> separates baseline/validator foundation, each skill family member, and generated-output closeout for reviewable slices.
- 2026-05-20: Add M6 lean asset correction -> removes row assets whose template bodies are too small to justify packaged files and keeps the substantial assets.
- 2026-05-20: Test spec comes after plan-review -> follows repository workflow ordering and lets test cases map to concrete milestones.
- 2026-05-20: Existing `specs/skill-contract.md` plus the approved spec-family assets spec is sufficient for implementation -> no skill-contract spec amendment is required before skill edits.

## Surprises and discoveries

- 2026-05-20: M3 showed the review-class policy-prose validator was too broad for allowed structural field labels such as `Recording status`; the validator now exempts only approved structural labels and rejects policy-shaped labels before exemption.
- 2026-05-20: The `spec` row assets and `test-spec` edge-case row asset had a poor metadata-to-content ratio and duplicated inline format guidance, so M6 removed them rather than preserving formalism.

## Validation notes

- Test-spec authoring validation passed:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/plan-review-r1.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `git diff --check -- docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md specs/spec-family-assets-progressive-disclosure.md specs/spec-family-assets-progressive-disclosure.test.md docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- M1 validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
  - `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md specs/spec-family-assets-progressive-disclosure.md specs/spec-family-assets-progressive-disclosure.test.md`
- M1 review-resolution validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- M1 R2 code-review recording validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m1-r2.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- M2 validation passed:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- skills/spec docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
- M2 review-resolution validation passed:
  - `python scripts/validate-skills.py skills/spec/SKILL.md`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- M2 R3 code-review recording validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m2-r3.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- M3 validation passed:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
- M3 R1 code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- M3 review-resolution validation passed:
  - `python scripts/validate-skills.py skills/spec-review/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- M3 R2 code-review recording validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m3-r2.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- M4 validation passed:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
- M4 R1 code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m4-r1.md`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- M6 validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m6-adapters-ohAnao`
  - `python scripts/validate-adapters.py --root /tmp/rigorloop-m6-adapters-ohAnao --version v0.1.5`
  - Python `zipfile` inspection found all current mapped assets and confirmed removed row assets are absent in all three temporary adapter archives.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/generated-output-proof.md`
  - `git diff --check -- .`
- M6 R1 code-review recording validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m6-r1.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- Explain-change recording validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/explain-change.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/explain-change.md docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- Final verify validation passed:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-verify-adapters-MXQ10c`
  - `python scripts/validate-adapters.py --root /tmp/rigorloop-verify-adapters-MXQ10c --version v0.1.5`
  - Python `zipfile` inspection confirmed current mapped assets and removed row asset absence in all three temporary adapter archives.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.md --path specs/spec-family-assets-progressive-disclosure.test.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/generated-output-proof.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/explain-change.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md`
  - `git diff --check -- .`
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode pr --base 88b93f74083042ab6be07a50bed36cab9c49ea8b --head HEAD`

## Outcome and retrospective

- Completed. PR #80 merged on 2026-05-20 after hosted CI and human review.

## Readiness

- See `Current Handoff Summary`.

## Risks and follow-ups

- PR #80 merged; no hosted CI or human review follow-up remains for this plan.
- Follow-up proposals remain separate for packaged `references/`, packaged `scripts/`, produced-artifact readability, and build-time partials.
