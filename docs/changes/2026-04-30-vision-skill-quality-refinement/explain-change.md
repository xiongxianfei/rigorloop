# Vision Skill Quality Refinement Explain Change

## Summary

M1 refines the canonical `vision` skill and focused skill-validator assertions so the skill pushes stronger first-pass vision drafts instead of only blocking bad outputs.

M2 refreshes generated `.codex/skills/` and `dist/adapters/` output through the existing generators. M3 synchronizes lifecycle state and final implementation proof. CR1-F1 fixes the missing revise-mode ask-or-confirm gate found by code review. `code-review-r2` returned `clean-with-notes`. A later verification pass exposed that root `vision.md` was not classified by the validation selector, so the selector now routes root `vision.md` to README vision-marker validation.

## Source Artifacts

- Proposal: `docs/proposals/2026-04-30-vision-skill-quality-refinement.md`
- Spec: `specs/vision-skill.md` (`R19`, `R81`-`R94`, `AC13`-`AC19`)
- Test spec: `specs/vision-skill.test.md`
- Plan: `docs/plans/2026-04-30-vision-skill-quality-refinement.md`

## Diff Rationale

| Area | Change | Reason |
| --- | --- | --- |
| `scripts/test-skill-validator.py` | Added focused assertions for workflow-fit placement, drafting heuristics, consolidated edit authorization, mode-table shape, and enforceable revise-mode traceability. | The implementation surface is skill text, so tests need stable contract assertions that fail before the guidance exists. |
| `skills/vision/SKILL.md` | Moved workflow fit near the top, consolidated source-of-truth and overwrite rules into edit authorization, converted mode behavior to one table, added drafting heuristics, and made substantive revise-mode traceability explicit. | Matches the approved refinement while preserving create/revise/mirror behavior, README marker rules, and source-of-truth order. |
| `skills/vision/SKILL.md` and `scripts/test-skill-validator.py` | Added explicit revise-mode wording to ask or confirm whether a revision is `substantive` or `editorial` before finalizing, plus focused assertion coverage. | Resolves CR1-F1 against R18 and T2 without changing the approved spec. |
| `.codex/skills/vision/SKILL.md` and `dist/adapters/*/skills/vision/SKILL.md` | Refreshed the generated vision skill copies through `scripts/build-skills.py` and `scripts/build-adapters.py --version 0.1.1`. | Keeps generated Codex runtime and public adapter packages synchronized with the canonical refined skill without hand edits. |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Classified root `vision.md` as a supported `vision` selector surface and added explicit plus PR-mode regressions. | Prevents root project vision creation from blocking selector-selected CI as `unclassified-path`. |
| Lifecycle artifacts | Updated proposal, spec, test spec, plan, and change-local evidence to point at first-pass `code-review` after M3 instead of earlier implementation stages, then synchronized post-review readiness after `code-review-r2` and `verify`. | Prevents stale handoff state before review and verify inspect lifecycle-managed artifacts. |
| Review artifacts | Added `reviews/code-review-r1.md`, `reviews/code-review-r2.md`, `review-log.md`, and `review-resolution.md`. | Preserves the first-pass finding, records the accepted fix, and makes the clean review rerun durable before downstream handoff. |
| Change-local evidence | Added this artifact pack during M1. | Implementation-stage changes are non-trivial, so the causal link should be durable before later generated-output and closeout milestones. |

## Scope Control

- The approved root `vision.md` content remains separate from the skill-quality refinement; this follow-up only adds selector coverage for the root path.
- README front-matter content is not changed by the selector fix.
- Generated `.codex/skills/` and `dist/adapters/` files are updated only through repository generators.
- Shared evidence-collection boilerplate extraction remains out of scope.
- Proposal, proposal-review, and governance behavior are not broadened in M1.
- `docs/plan.md` remains active and unchanged because the initiative has not completed the new code-review rerun, verify rerun, explain-change, PR handoff, or Done closeout.

## Validation Evidence

- `python scripts/test-skill-validator.py` failed before the skill revision for the new M1 assertions.
- `python scripts/test-skill-validator.py` passed after the skill revision.
- `python scripts/validate-skills.py skills/vision/SKILL.md` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.test.md` passed.
- `python scripts/test-change-metadata-validator.py` passed.
- `python scripts/validate-readme.py README.md --vision-markers` passed.
- `git diff --check -- specs/vision-skill.test.md scripts/test-skill-validator.py skills/vision/SKILL.md docs/plans/2026-04-30-vision-skill-quality-refinement.md docs/changes/2026-04-30-vision-skill-quality-refinement` passed.

Selector inspection passed and selected generated skill and adapter drift checks. Those checks are deferred to M2 because generated output refresh is the next milestone, not part of M1.

M2 validation:

- `python scripts/build-skills.py --check` failed before M2 generation because `.codex/skills/vision/SKILL.md` was stale.
- `python scripts/build-adapters.py --version 0.1.1 --check` failed before M2 generation because three generated adapter vision skill copies were stale.
- `python scripts/build-skills.py` passed.
- `python scripts/build-adapters.py --version 0.1.1` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/select-validation.py --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md` selected `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, and `readme.vision_markers`.
- `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md` passed.
- `bash scripts/ci.sh --mode explicit --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md` passed.

M3 validation:

- `python scripts/validate-skills.py` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`.
- `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md` passed.
- `git diff --check -- .` passed.

CR1-F1 review-resolution validation:

- `python scripts/test-skill-validator.py` failed before the canonical skill fix for the new ask-or-confirm assertion.
- `python scripts/test-skill-validator.py` passed after the fix.
- `python scripts/build-skills.py` passed.
- `python scripts/build-adapters.py --version 0.1.1` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-04-30-vision-skill-quality-refinement` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md` passed.
- `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`.
- `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md` passed.
- `bash scripts/ci.sh --mode broad-smoke` passed.
- `git diff --check -- .` passed.

Post-review lifecycle sync and verification:

- `code-review-r2` returned `clean-with-notes` with no blocking or required-change findings.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md` passed.
- `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md` selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `readme.vision_markers`.
- `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/proposals/2026-04-30-vision-skill-quality-refinement.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md --path scripts/test-skill-validator.py --path .codex/skills/vision/SKILL.md --path dist/adapters/codex/.agents/skills/vision/SKILL.md --path dist/adapters/claude/.claude/skills/vision/SKILL.md --path dist/adapters/opencode/.opencode/skills/vision/SKILL.md --path docs/plans/2026-04-30-vision-skill-quality-refinement.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r1.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/reviews/code-review-r2.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-log.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md` passed.
- `git diff --check -- docs/changes/2026-04-30-vision-skill-quality-refinement docs/plans/2026-04-30-vision-skill-quality-refinement.md` passed.

Root vision selector fix:

- `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block` failed before the selector fix because root `vision.md` was unclassified.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block` passed after classifying root `vision.md`.
- `python scripts/test-select-validation.py` passed.
- `python scripts/select-validation.py --mode explicit --path ... --path vision.md` passed and selected `readme.vision_markers` plus the expected selector, skill, adapter, review, lifecycle, metadata, and README checks.
- `bash scripts/ci.sh --mode explicit --path ... --path vision.md` passed the full selected check set, including `selector.regression`.

## Readiness

CR1-F1 review-resolution has closed, `code-review-r2` is clean, and the root `vision.md` selector blocker is fixed with regression coverage. The new selector change is ready for `code-review` rerun before verify and downstream PR handoff.
