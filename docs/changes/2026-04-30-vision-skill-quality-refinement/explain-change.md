# Vision Skill Quality Refinement Explain Change

## Summary

This change refines the already-shipped `vision` skill so future project-vision drafts are sharper on the first pass, while preserving the approved vision contract and README marker behavior.

The implementation adds focused drafting heuristics, consolidates edit-authorization guidance, moves workflow-fit guidance before mode mechanics, converts create/revise/mirror behavior into one comparison table, and makes substantive revision traceability enforceable. It also refreshes generated Codex and public adapter outputs from the canonical skill, records review findings and resolutions, creates the approved root `vision.md` plus README front-matter, and fixes validation selector coverage so root `vision.md` no longer blocks PR-mode CI as `unclassified-path`.

## Problem

The first real use of the `vision` skill produced a valid `vision.md`, but the draft needed repeated review cycles to add a comparative differentiator, embedded pain points, checkable commitments, and observable falsifiability. The existing skill prevented bad output but did not actively steer authors toward strong output.

The workflow also exposed a validation gap after root `vision.md` was created: PR-mode validation treated the root project-vision file as unclassified. That made the approved project-vision artifact a CI blocker even though the vision-skill contract already made it a first-class surface.

## Decision Trail

- Proposal: `docs/proposals/2026-04-30-vision-skill-quality-refinement.md` chose contract refinement over a wording-only patch.
- Requirements: `specs/vision-skill.md` `R19`, `R79`-`R80`, `R81`-`R94`, and `AC9`, `AC13`-`AC19`.
- Test spec: `specs/vision-skill.test.md` maps the refinement to `T1`-`T11`, with selector-specific coverage in `T10`.
- Architecture / ADR: none required; the work changes skill guidance, validation routing, generated text output, and lifecycle artifacts without adding runtime, persistence, deployment, service, or dependency boundaries.
- Plan: `docs/plans/2026-04-30-vision-skill-quality-refinement.md` split implementation into canonical skill/test updates, generated output refresh, lifecycle closeout, review-resolution, and selector follow-up.
- Review: `code-review-r1` found CR1-F1; `code-review-r2` and `code-review-r3` returned `clean-with-notes`.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/vision/SKILL.md` | Added drafting heuristics, moved workflow fit near the top, consolidated edit authorization, converted mode behavior to one table, and made substantive revise-mode traceability a gate. | Addresses the observed quality gap and removes repeated, drift-prone guidance while preserving approved modes. | `R19`, `R81`-`R94`, `AC13`-`AC18` | `scripts/test-skill-validator.py`; `python scripts/validate-skills.py` |
| `scripts/test-skill-validator.py` | Added focused assertions for the refined skill contract and the CR1-F1 ask-or-confirm gate. | The implementation surface is Markdown skill guidance, so contract assertions need to inspect the text directly. | `T1`-`T4`, `T8`, `T11` | Test failed before the skill update, then passed after the fix. |
| `.codex/skills/vision/SKILL.md`, `dist/adapters/*/skills/vision/SKILL.md` | Regenerated derived skill outputs. | Keeps runtime and public adapter packages synchronized without hand-editing generated output. | `R43`-`R45`, `AC6`-`AC7` | `build-skills.py --check`, adapter regression, adapter drift, adapter validation |
| `vision.md` | Added the approved root project vision. | Establishes the canonical project-vision artifact produced by the accepted skill practice. | `R21`-`R26`, `R46`-`R47`, `R61`-`R66` | Word count check by review, README marker validation |
| `README.md` | Added marker-bounded generated front-matter derived from `vision.md`. | Makes the public entrypoint summarize the canonical vision while keeping README front-matter non-authoritative. | `R25`-`R26`, `R54`-`R55`, `AC8`-`AC11` | `python scripts/validate-readme.py README.md --vision-markers` |
| `scripts/validation_selection.py` | Classified root `vision.md` as `vision` and selected `readme.vision_markers` for root vision changes. | Prevents approved root vision changes from blocking selected CI as `unclassified-path`. | `R79`-`R80`, `AC9` | selector focused tests and PR-mode CI |
| `scripts/test-select-validation.py` | Added explicit and PR-mode regression coverage for root `vision.md`; adjusted README lightweight test setup to avoid accidental marker selection. | Proves the exact failure path found by verify and keeps README marker selection deterministic. | `T10`, `T11` | `ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block`; `ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block` |
| `specs/vision-skill.md`, `specs/vision-skill.test.md` | Added requirements and proof mapping for root `vision.md` selector coverage and the approved refinement details. | Keeps executable behavior, skill guidance, and validation routing under an approved contract. | `R79`-`R94`, `AC9`, `AC13`-`AC19` | artifact lifecycle validation |
| `docs/plans/...`, `docs/plan.md` | Added the active plan and kept the initiative active until verify, PR handoff, and final closeout complete. | Preserves lifecycle state and prevents stale branch-readiness claims. | plan policy, workflow contract | artifact lifecycle validation |
| `docs/changes/...` | Added `change.yaml`, this explanation, review log, review-resolution, and three review records. | Provides durable reasoning, review findings, dispositions, and validation evidence for a non-trivial workflow change. | docs-changes baseline pack, review rules | review artifact validation and change metadata validation |

## Tests Added Or Changed

- `scripts/test-skill-validator.py` now proves the refined `vision` skill contract: workflow-fit placement, drafting heuristics, one mode table, consolidated edit authorization, substantive revision traceability, and the revise-mode `substantive` versus `editorial` ask-or-confirm gate.
- `scripts/test-select-validation.py` now proves root `vision.md` is classified as `vision`, does not appear in `unclassified_paths`, selects `readme.vision_markers`, and works in PR-mode diff selection.
- `specs/vision-skill.test.md` now maps selector behavior for README and root `vision.md` to `T10` and final closeout to `T11`.

These are the right levels because the skill behavior is expressed as repository-owned Markdown guidance, generated outputs are deterministic build products, and the selector behavior is executable Python logic.

## Verification Evidence

Key validation evidence is recorded in `docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` and the active plan. The most relevant commands include:

- `python scripts/test-skill-validator.py` failed before the skill guidance update, then passed after the canonical skill was refined.
- `python scripts/validate-skills.py` passed.
- `python scripts/build-skills.py --check` passed after generated Codex skill output was refreshed.
- `python scripts/test-adapter-distribution.py` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed after adapter output was refreshed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block` failed before the selector fix, then passed after root `vision.md` classification was added.
- `python scripts/test-select-validation.py` passed.
- `python scripts/select-validation.py --mode explicit ... --path vision.md` passed and selected `readme.validate`, `readme.vision_markers`, `selector.regression`, and the expected lifecycle, skill, adapter, review, and metadata checks.
- `bash scripts/ci.sh --mode pr --base 28f1736 --head HEAD` passed before `code-review-r3` was recorded.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-30-vision-skill-quality-refinement` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the plan, proposal, spec, test spec, change metadata, and this explanation.
- `bash scripts/ci.sh --mode explicit ...code-review-r3...` passed after recording the third review.
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-30-vision-skill-quality-refinement/explain-change.md --path docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml --path docs/plans/2026-04-30-vision-skill-quality-refinement.md` passed after refreshing this explanation.

Hosted CI has not been observed from this local environment. A fresh `verify` rerun is still required after `code-review-r3` before PR readiness can be claimed.

## Review Resolution Summary

Material findings: one.

- `code-review-r1`: one accepted finding, CR1-F1. The canonical `vision` skill did not explicitly ask or confirm whether revise mode was `substantive` or `editorial` before finalizing. The fix updated `skills/vision/SKILL.md`, focused skill-validator assertions, and generated outputs.
- `code-review-r2`: no material findings.
- `code-review-r3`: no material findings for the post-r2 selector and lifecycle diff.

Review closeout is recorded in `docs/changes/2026-04-30-vision-skill-quality-refinement/review-resolution.md`, with `Closeout status: closed` and no open findings in `review-log.md`.

## Alternatives Rejected

- Leaving the `vision` skill unchanged was rejected because the first real use showed avoidable review churn even though the output was structurally valid.
- Patching only the skill wording was rejected because the approved contract, proof map, generated outputs, and lifecycle artifacts would have drifted.
- Requiring named competitors in every differentiator was rejected because naming a tool can date the vision and create unnecessary positioning risk; the heuristic allows either an alternative class or a specific tool.
- Extracting shared evidence-collection boilerplate was rejected as out of scope and too costly for this refinement.
- Adding a README mirror helper script was rejected because the approved contract only required marker-bounded behavior and guidance, not new automation.

## Scope Control

- The skill refinement preserves create, revise, and mirror as the only `vision` edit modes.
- The approved root `vision.md` keeps the 500-word cap and required section order.
- README content outside `<!-- vision:start -->` and `<!-- vision:end -->` remains author-owned.
- Generated `.codex/skills/` and `dist/adapters/` output was refreshed through repository generators, not hand-edited.
- Proposal and proposal-review behavior stayed inside the existing `Vision fit` contract.
- `vision` remains upstream of the normal per-change lifecycle and is not added as a normal stage.

## Risks And Follow-Ups

- `verify` must rerun after tracked `code-review-r3` before branch-ready or PR handoff can be claimed.
- Hosted CI has not been observed.
- `docs/plan.md` remains active until verify, PR handoff, and final Done closeout complete.

## Readiness

This explanation is current through the tracked `code-review-r3` record. It is not a PR-ready claim. The next required stage is `verify`; PR handoff remains blocked until verify reports branch-ready. If verify changes readiness evidence, refresh this explanation before PR handoff.
