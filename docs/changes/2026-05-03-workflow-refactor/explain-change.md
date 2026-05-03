# Workflow Refactor Change Explanation

## Status

Explain-change complete; ready for `pr`.

## Summary

This change refactors RigorLoop workflow guidance around lifecycle categories instead of one overloaded linear chain. Standing artifacts, living references, workflow infrastructure, on-demand artifacts, per-change stages, and periodic learning now have distinct rules and handoff behavior.

The branch updates the approved workflow proposal, workflow spec, test spec, root guidance, operational workflow summary, affected stage skills, generated skill and adapter output, selector and lifecycle regression coverage, and change-local review and verification evidence.

The implementation keeps `specs/rigorloop-workflow.md` as the canonical workflow contract, keeps `docs/workflows.md` as the short operating summary, separates `ci-maintenance` from validation execution, treats `review-resolution` as closeout rather than a review stage, and records that `docs/project-map.md` is absent and not relied on for this refactor.

## Problem

The old workflow summary mixed fundamentally different lifecycle concepts into one chain: standing governance, project-map context, exploration, research, proposal/spec stages, implementation, validation, CI, learning, and PR. That made it unclear what is mandatory, what is conditional, what is on demand, what can go stale, and what blocks downstream work.

The refactor needed to make those categories explicit, preserve the already-landed `VISION.md` source-of-truth migration, move `explore` and `research` out of the default per-change chain, move `learn` to periodic or explicit retrospective work, define the `project-map` no-reliance rule without implementing the full project-map lifecycle, and align the affected docs, skills, generated outputs, and validation proof.

## Decision Trail

- Exploration: no separate `explore` artifact was created. The accepted proposal records the options and tradeoffs directly.
- Proposal decision: `docs/proposals/2026-05-01-workflow-refactor.md` selected the category-model refactor and deferred the root vision rename, full project-map lifecycle, and final learn artifact model.
- Spec: `specs/rigorloop-workflow.md` was approved with the category table, stage obligation metadata, standing-artifact gates, project-map no-reliance rule, learn closeout rule, `review-resolution` gate, `ci-maintenance` boundary, targeted proof rules, durable reasoning rules, and generated-output/source-of-truth boundaries.
- Test spec: `specs/rigorloop-workflow.test.md` is active and maps the approved requirements to root guidance checks, skill assertions, selector regressions, lifecycle validation, generated-output checks, change metadata validation, and manual reviewable evidence.
- Architecture / ADRs: none required. This is workflow-governance and artifact-routing work, not a runtime architecture, storage, API, deployment, or service-boundary change.
- Plan: `docs/plans/2026-05-03-workflow-refactor.md` split the work into M1 root guidance, M2 skill/generated-output alignment, M3 validator coverage, and M4 change-local closeout and verification.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-01-workflow-refactor.md` | Added the accepted workflow-refactor proposal and updated it to build on canonical `VISION.md`. | Records the selected category-model direction and removes the superseded future vision-rename follow-up. | Proposal, `VISION.md` migration state | Artifact lifecycle validation |
| `specs/rigorloop-workflow.md` | Added category rules, stage-obligation metadata, standing-artifact gates, project-map no-reliance, learn closeout, `review-resolution`, `ci-maintenance`, targeted proof, durable reasoning, and generated-output boundaries. | Makes the workflow definition inspectable and testable from one canonical contract. | R1-R12f, R20-R27 | `validate-artifact-lifecycle`, selector-selected CI |
| `specs/rigorloop-workflow.test.md` | Expanded the proof map with T20-T28 and related manual checks. | Turns the approved workflow requirements into concrete tests and reviewable evidence. | Test-spec stage | `test-select-validation`, `test-artifact-lifecycle-validator`, `test-skill-validator` |
| `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md` | Rewrote operating guidance around the category model, obligation values, no-map rule, periodic `learn`, `review-resolution`, and `ci-maintenance`. | Keeps contributor-facing guidance aligned with the canonical workflow contract. | M1, R6-R9, R12, R24 | README validation, lifecycle validation, explicit CI |
| `skills/workflow/SKILL.md` | Updated routing guidance to use categories, triggers, obligation values, and stage-owned readiness. | Prevents the workflow skill from reintroducing the old overloaded chain. | M2, R6-R7w | `test-skill-validator`, `validate-skills` |
| `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md` | Added standing-artifact gates, first-substantive-proposal handling, bootstrap exceptions, and review checks. | Ensures proposal creation and proposal-review enforce `VISION.md` and `CONSTITUTION.md` gates consistently. | R6a, R6e-R6h | `test-skill-validator` |
| `skills/ci/SKILL.md` | Clarified the user-visible action as `ci-maintenance` and excluded validation execution, test design, and validation-command ownership. | Removes ambiguity between hosted CI infrastructure work and `verify`. | R9-R9b | `test-skill-validator`, explicit CI |
| `skills/learn/SKILL.md` | Reframed `learn` as periodic or explicitly invoked, with immediate capture, scheduled follow-up, or no-learn rationale. | Keeps retrospective learning available without making it a default per-change stage. | R7ba-R7be | `test-skill-validator`; no-learn rationale in plan/explain-change |
| `skills/verify/SKILL.md` | Updated downstream handoff wording so verify routes to `ci-maintenance` only when CI infrastructure is actually triggered. | Preserves `verify` as the branch-ready gate and avoids treating CI maintenance as routine validation execution. | R7rc, R9 | `test-skill-validator` |
| `.codex/skills/` and `dist/adapters/` | Regenerated local Codex mirrors and public adapter skill copies from canonical skills. | Keeps generated runtime and adapter outputs in sync after canonical skill changes. | R20-R24a, R26-R27 | `build-skills --check`, `test-adapter-distribution`, `build-adapters --check`, `validate-adapters` |
| `scripts/test-select-validation.py` | Added workflow-refactor surface coverage, generated-output routing coverage, broad-smoke trigger coverage, and active plan/test-spec/review-resolution trigger cases. | Proves the validation selector chooses targeted checks and does not require broad smoke without an authoritative trigger. | R8l-R8s, T25 | `python scripts/test-select-validation.py` |
| `scripts/test-artifact-lifecycle-validator.py` | Added plan-context expansion and invalid workflow-authority regressions. | Proves touched plan context reaches authoritative proposal/spec/test-spec surfaces and blocks stale lifecycle states. | R8f-R8kg, T25 | `python scripts/test-artifact-lifecycle-validator.py` |
| `scripts/test-skill-validator.py` | Added focused assertions for workflow-refactor skill guidance. | Prevents affected canonical skills from drifting back to old-chain, advice-only, or ambiguous CI wording. | M2, T21-T24, T26 | Red/green `python scripts/test-skill-validator.py` during M2 |
| `docs/changes/2026-05-03-workflow-refactor/` | Added `change.yaml`, review records, review-resolution, and this explanation. | Provides durable traceability, review closeout, validation evidence, and reviewer-facing rationale for a non-trivial workflow-governance change. | R10-R12f, R25-R25h | Metadata, review-artifact, lifecycle, and CI validation |
| `docs/plan.md`, `docs/plans/2026-05-03-workflow-refactor.md` | Added and maintained the active plan, milestone progress, decisions, validation notes, and PR readiness. | Keeps planned initiative state synchronized and reviewable before PR. | R8f-R8j | Lifecycle validation |

## Tests Added Or Changed

- `scripts/test-select-validation.py`
  - Adds workflow-refactor surface selection coverage for root guidance, lifecycle artifacts, canonical skill sources, generated skill output, generated adapter output, selector tests, lifecycle tests, skill-validator tests, change metadata, explanation, review log, and review-resolution.
  - Adds broad-smoke source coverage so ordinary workflow-refactor paths stay targeted while active plan, test-spec, and review-resolution trigger contexts can require broad smoke.
- `scripts/test-artifact-lifecycle-validator.py`
  - Adds plan-context expansion coverage to proposal, spec, test spec, and architecture authority surfaces.
  - Adds a regression proving invalid referenced workflow authority blocks validation when reached through a plan.
- `scripts/test-skill-validator.py`
  - Adds assertions that workflow, proposal, proposal-review, CI, learn, and verify skill guidance matches the refactored category, gate, handoff, `ci-maintenance`, and learn behavior.
- `specs/rigorloop-workflow.test.md`
  - Adds or expands T20-T28 for category visibility, standing-artifact gates, project-map no-reliance, stage obligations, triggered learn, handoff authority, selector/lifecycle proof, CI-maintenance, review-resolution, and change metadata traceability.

## Requirement Coverage

| Requirement group | Test coverage | Implementation evidence |
| --- | --- | --- |
| R1-R7be | T1, T20, T21, T22, T23 | `specs/rigorloop-workflow.md`, root guidance, `docs/workflows.md`, workflow/proposal/learn skills |
| R7c-R7w | T3, T24 | Workflow-facing skill handoffs, stage-owned readiness wording, verify/pr authority split |
| R8-R8s | T2, T13, T17, T25 | Active plan/index, selector-selected proof, lifecycle validator coverage, explicit CI wrapper behavior |
| R9-R9b | T13, T14, T26 | `ci-maintenance` wording in workflow docs and `skills/ci/SKILL.md`; validation remains under `verify` |
| R10-R12f | T3, T16, T27 | `explain-change.md`, `review-log.md`, closed `review-resolution.md`, concise review summary |
| R20-R24a, R26-R27 | T4, T11, T12, T17 | Canonical/generated boundaries, generated skill and adapter drift checks, Git/PR/CI/human-review authority |
| R25-R25h | T5, T6, T7, T28 | `change.yaml` with artifacts, requirements, tests, validation records, changed files, and review state |

## Verification Evidence

Validation evidence is recorded in `docs/changes/2026-05-03-workflow-refactor/change.yaml` and the active plan. The final verify pass ran after code review and after generated outputs were refreshed.

- `python scripts/validate-change-metadata.py docs/changes/2026-05-03-workflow-refactor/change.yaml` - passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-03-workflow-refactor` - passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-03-workflow-refactor` - passed.
- `python scripts/validate-skills.py` - passed.
- `python scripts/test-skill-validator.py` - passed.
- `python scripts/build-skills.py --check` - passed.
- `python scripts/test-adapter-distribution.py` - passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` - passed.
- `python scripts/validate-adapters.py --version 0.1.1` - passed.
- `python scripts/test-select-validation.py` - passed.
- `python scripts/test-artifact-lifecycle-validator.py` - passed.
- `python scripts/test-change-metadata-validator.py` - passed.
- `python scripts/select-validation.py --mode explicit ...` over the full workflow-refactor changed surface - passed; selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `readme.validate`, `readme.vision_markers`, and `selector.regression`.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` over proposal, spec, test spec, plan, change metadata, explain-change, review log, review-resolution, and final code-review record - passed.
- `bash scripts/ci.sh --mode explicit ...` over the full workflow-refactor changed surface - passed with the same selector-selected checks.
- `git diff --check --` - passed.

Hosted CI was not observed locally. The repository GitHub workflow is a thin wrapper that delegates pull-request and main-branch runs to `scripts/ci.sh`; local explicit CI passed.

## Review Resolution Summary

- Code-review rounds: 4.
- Material findings: 1.
- Accepted: 1.
- Rejected: 0.
- Deferred: 0.
- Partially accepted: 0.
- Needs decision: 0.
- Unresolved findings: 0.
- Review-resolution: `docs/changes/2026-05-03-workflow-refactor/review-resolution.md`.

`code-review-m1-r1` found stale plan wording that still described `specs/rigorloop-workflow.test.md` as archived even though the test-spec stage had activated it before M1. The finding was accepted, fixed in the plan, and validated. `code-review-m2-r1`, `code-review-m3-r1`, and `code-review-m4-r1` returned `clean-with-notes` with no material findings.

## Alternatives Rejected

- Keep the current workflow chain: rejected because it keeps standing artifacts, living references, on-demand aids, per-change stages, and retrospective learning visually conflated.
- Rewrite only `docs/workflows.md`: rejected because the real contract would still be scattered across the spec, skills, and generated outputs.
- Bundle the full project-map lifecycle: rejected as too broad; this change keeps only the minimal no-reliance rule and defers freshness markers and revision workflow.
- Bundle the final learn artifact model: rejected as too broad; this change records temporary allowed closeout surfaces and defers the three-surface learn model.
- Rename `skills/ci/`: rejected because `ci-maintenance` is the contributor-visible action label, while the existing skill path can remain stable.
- Run broad smoke by default: rejected because the approved workflow uses targeted selector-selected proof unless an authoritative source triggers broad smoke.

## Scope Control

- The completed `VISION.md` migration is not reopened.
- The approved project vision content is not changed.
- `docs/project-map.md` is not created because this refactor does not rely on repository-shape claims from a project map.
- Project-map freshness markers, calendar thresholds, and skill behavior are deferred.
- The final `learn` artifact model is deferred.
- Generated `.codex/skills/` and `dist/adapters/` output was refreshed through repository generators, not hand-edited.
- No runtime code, API, storage, deployment, or release packaging behavior is changed.

## Risks And Follow-Ups

- Hosted CI is not observed locally; local repository-owned explicit CI passed and `.github/workflows/ci.yml` delegates to the same wrapper.
- The full project-map lifecycle remains a follow-up proposal.
- The final learn artifact model remains a follow-up proposal.
- Workflow wording is now more structured; future changes should avoid duplicating the whole routing table inside every stage skill.

## PR Handoff Summary

- Refactor workflow guidance around standing artifacts, living references, workflow infrastructure, on-demand artifacts, per-change stages, and periodic learning.
- Align root guidance, workflow summary, stage skills, generated skill output, public adapter output, selectors, lifecycle tests, and change-local artifacts with the approved workflow spec.
- Preserve targeted selector-selected proof as the default and keep broad smoke trigger-based.
- Close the only material review finding and verify the branch with explicit repository-owned validation.
- Branch is ready for PR review.
