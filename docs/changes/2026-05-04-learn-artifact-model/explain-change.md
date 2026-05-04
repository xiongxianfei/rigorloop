# Learn Artifact Model Change Explanation

## Summary

This change implements the approved learn artifact model across the workflow contract, governance summaries, selector behavior, canonical `learn` skill guidance, the lightweight `docs/learn/` index, generated Codex skill output, generated public adapter output, and change-local lifecycle evidence.

The model gives `learn` one canonical session-record namespace, optional curated topic guidance, contributor-confirmed classification before routing, and explicit action routing into authoritative artifacts. It also keeps `learn` periodic or explicitly triggered rather than making it a mandatory final step for every change.

First-pass implementation, direct code-review follow-up, `$verify`, and this final explanation closeout are complete. The next workflow stage is `pr`; this direct `$explain-change` request stops before preparing or opening the PR.

## Problem

The prior workflow treated final learn artifact handling as deferred and mixed several possible recording surfaces: temporary no-learn rationale, scheduled follow-up notes, old retrospective paths, and future learn refactor language. The accepted proposal and approved spec narrowed that into a single process: run a learn session only when triggered, record any session that reaches Frame, keep durable topic guidance curated and non-authoritative, and route behavior changes to the affected authoritative artifact.

The implementation needed to align contributor-facing guidance, validation selection, generated skill mirrors, and change evidence without adding templates, empty topic files, a prebuilt taxonomy, or mandatory per-change learn work.

## Decision Trail

- Proposal: `docs/proposals/2026-05-03-optimize-learn-skill.md`
- Proposal decision: use a light first slice with `docs/learn/sessions/**`, `docs/learn/topics/**`, affected authoritative artifacts, ADRs/proposals when warranted, no templates, no archive infrastructure, and no roadmap fallback for untracked follow-ups.
- Spec: `specs/learn-artifact-model.md`, requirements `R1`-`R47`.
- Workflow spec update: `specs/rigorloop-workflow.md`, requirements `R7ba`-`R7bf`.
- Test spec: `specs/learn-artifact-model.test.md`, tests `T1`-`T14`, plus `specs/rigorloop-workflow.test.md` `T23`.
- Architecture/ADR decision: no separate architecture or ADR was required. The accepted scope changes repository workflow, documentation, selector routing, skill guidance, and generated output; it does not introduce runtime architecture, persistence, deployment, external integration, or a durable architecture decision.
- Plan: `docs/plans/2026-05-04-learn-artifact-model.md`.
- Milestones completed: M1 workflow and governance alignment; M2 learn path selector recognition; M3 learn skill, learn index, and generated output; M4 final validation and lifecycle closeout.

## Diff Rationale By Area

| File or area | Change | Reason | Source and evidence |
| --- | --- | --- | --- |
| `docs/proposals/2026-05-03-optimize-learn-skill.md` | Captures the accepted direction for session files, topic guidance, action-owning artifacts, light structure, and follow-up routing. | Establishes the decision basis before the spec and implementation. | Proposal accepted; plan source artifact. |
| `specs/learn-artifact-model.md` | Adds the final learn contract, including canonical paths, phases, classifications, routing, topic authority, bounded evidence, selector recognition, and generated-output refresh. | Provides the authoritative behavior contract for `R1`-`R47`. | `specs/learn-artifact-model.test.md` `T1`-`T14`; lifecycle validation. |
| `specs/learn-artifact-model.test.md` | Maps every requirement group and edge case to manual, integration, selector, skill-validator, generated-output, and final CI checks. | Makes the human-readable workflow and executable selector/skill behavior testable. | Test spec coverage table; lifecycle validation. |
| `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md` | Replaces temporary learn closeout wording with final trigger, session-record, pre-session no-record, topic-file, and authoritative-artifact routing rules. | Satisfies `R45`, `R46`, and workflow `R7ba`-`R7bf` without turning `learn` into a default final per-change stage. | `T23`; stale-term scan; explicit CI. |
| `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` | Aligns operational and governance guidance with triggered learn sessions, `docs/learn/` surfaces, no-learn closeout boundaries, and durable lesson routing. | Prevents lower-level contributor guidance from preserving the deferred or temporary model. | `T1`, `T6`; stale-term scan; explicit CI. |
| `scripts/validation_selection.py` | Classifies `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**` as lightweight known learn artifact paths. | Satisfies `R44` and keeps raw session/topic records out of lifecycle validation. | `scripts/test-select-validation.py`; selector regression. |
| `scripts/test-select-validation.py` | Adds representative learn namespace regression coverage. | Proves the selector recognizes the new paths before any `docs/learn/**` artifact is created. | `test_learn_artifact_paths_are_known_lightweight_paths`; `python scripts/test-select-validation.py`. |
| `skills/learn/SKILL.md` | Rewrites the canonical learn skill around Frame, Observe, Classify, and Route; requires evidence-bound observations, contributor confirmation, one primary classification, secondary routes, bounded evidence, and R29 maintainer-rule-adoption handling. | Implements the operator guidance for `R2`-`R43`, including the rule that maintainer requests alone route to proposal work rather than durable learn capture. | `scripts/test-skill-validator.py`; `python scripts/validate-skills.py`. |
| `docs/learn/README.md` | Adds a lightweight namespace index for `sessions/` and `topics/`. | Makes the new paths discoverable without adding templates, empty topic files, or a taxonomy. | `T2`, `T8`, selector-selected CI. |
| `scripts/test-skill-validator.py` | Adds stable wording checks for canonical paths, phases, classification model, confirmation, bounded evidence, generated-output boundaries, and R29 rule adoption. | Protects the durable parts of the skill guidance while leaving session/topic shapes template-free. | `test_learn_skill_final_artifact_model_and_bounded_process`. |
| `.codex/skills/learn/SKILL.md` | Regenerated from canonical `skills/learn/SKILL.md`. | Keeps the local Codex runtime mirror generated rather than hand-edited. | `python scripts/build-skills.py --check`. |
| `dist/adapters/claude/.claude/skills/learn/SKILL.md`, `dist/adapters/codex/.agents/skills/learn/SKILL.md`, `dist/adapters/opencode/.opencode/skills/learn/SKILL.md` | Regenerated public adapter learn skills. | Keeps Claude Code, Codex adapter, and opencode outputs aligned with the canonical skill. | `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| `docs/plan.md` and `docs/plans/2026-05-04-learn-artifact-model.md` | Tracks milestone completion, validation notes, review/verify/explain-change status, and remaining PR handoff. | Keeps the active plan index and plan body synchronized while the initiative remains Active until PR closeout. | Artifact lifecycle validation. |
| `docs/changes/2026-05-04-learn-artifact-model/change.yaml` | Records requirements, tests, changed files, validation evidence, review status, verification status, and explanation status. | Provides machine-readable traceability for the non-trivial workflow-governance change. | `python scripts/validate-change-metadata.py`. |
| `docs/changes/2026-05-04-learn-artifact-model/review-log.md`, `review-resolution.md`, and `reviews/code-review-*.md` | Records the tracked M1-M3 review rounds and closes all material findings. | Preserves review traceability without duplicating detailed review transcripts in this explanation. | Review artifact validation in structure and closeout modes. |

## Tests Added Or Changed

- `specs/learn-artifact-model.test.md`
  - `T1` covers workflow/governance alignment and temporary-surface retirement.
  - `T2` covers the lightweight canonical namespace.
  - `T3` covers session fields, phases, empty outcomes, and periodic windows.
  - `T4` covers one primary classification, secondary routes, and confirmation before routing.
  - `T5` and `T6` cover routing destinations, follow-up tracking, and no-record boundaries.
  - `T7` covers trigger types, single-event evidence, and `R29` maintainer-driven rule adoption.
  - `T8` covers topic authority and curated topic lifecycle.
  - `T9` covers bounded evidence collection.
  - `T10` covers selector recognition.
  - `T11` and `T12` cover skill-validator and generated-output checks.
  - `T13` covers private incident detail handling.
  - `T14` covers final explicit-path validation across the full change surface.
- `specs/rigorloop-workflow.test.md`
  - `T23` now proves the workflow-level learn contract points to the final model and preserves the nonblocking trigger boundary.
- `scripts/test-select-validation.py`
  - `test_learn_artifact_paths_are_known_lightweight_paths` proves `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**` are recognized without selecting lifecycle validation.
- `scripts/test-skill-validator.py`
  - `test_learn_skill_final_artifact_model_and_bounded_process` proves the stable skill guidance for paths, phases, classifications, confirmation, bounded evidence, generated boundaries, and R29.

These test levels are intentionally mixed. Human-readable process contracts are covered by spec/test-spec review and explicit artifact validation; executable repository behavior is covered by selector, skill-validator, generated-output drift, adapter validation, and selected CI checks.

## Review And Verification Outcomes

- Tracked code-review evidence:
  - `review-log.md` contains seven tracked review entries for M1-M3.
  - Three material findings were recorded and accepted: `CR-M1-F1`, `CR-M2-F1`, and `CR-M3-R2-F1`.
  - All material findings are closed in `review-resolution.md`.
  - No `needs-decision` dispositions remain and no review-log entry lists open findings.
- Direct final code-review:
  - The M4 direct `code-review` request completed with no blocking or required-change findings.
  - Because it produced no material findings, it did not require a new review-resolution entry.
- `$verify`:
  - Verdict: pass.
  - Result: no blockers, no generated-output drift, no lifecycle drift, no missing review closeout, and local PR-mode CI passed.
  - Hosted CI was not observed from this environment.
  - Broad smoke was not required by the active plan or selector-selected validation.

## Review Resolution Summary

`docs/changes/2026-05-04-learn-artifact-model/review-resolution.md` is closed.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| `CR-M1-F1` | accepted | Added incident response and contributor observation trigger coverage to `docs/workflows.md` and `specs/rigorloop-workflow.test.md`. |
| `CR-M2-F1` | accepted | Updated stale M2 plan outcome wording after selector implementation. |
| `CR-M3-R2-F1` | accepted | Added explicit R29 maintainer-driven rule-adoption guidance, skill-validator coverage, and regenerated skill/adapter output. |

Clean tracked rounds required no resolution entries: `code-review-m1-r2`, `code-review-m2-r2`, `code-review-m3-r1`, and `code-review-m3-r3`.

## Validation Evidence

Milestone validation evidence is recorded in `docs/plans/2026-05-04-learn-artifact-model.md` and `change.yaml`. Final validation included:

- `bash scripts/ci.sh --mode explicit --path <full M4 changed surface>` - passed; selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` - passed locally.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-04-learn-artifact-model` - passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-04-learn-artifact-model` - passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml` - passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths <authoritative artifact set>` - passed.
- `git diff --check origin/main..HEAD` - passed.
- `git diff --check --` - passed.
- Stale learn-surface scan over workflow, governance, README, and learn skill surfaces - passed after the corrected single-quoted pattern rerun.

Post-verify explain-change closeout validation is recorded in the plan and `change.yaml`.

## Alternatives Rejected

- Keeping both `docs/learn/` and `docs/learnings/`: rejected because similar path names would confuse raw session records with curated topic guidance.
- Using topic files as policy: rejected because topic files are curated guidance and must not override specs, ADRs, workflow docs, skill files, accepted proposals, plans, or other authoritative artifacts.
- Adding session or topic templates in the first slice: rejected because the approved proposal defers templates until actual usage reveals a stable shape worth codifying.
- Adding empty topic files, a prebuilt taxonomy, or archive infrastructure: rejected because the first implementation should use the lightest structure that solves the current problem.
- Falling back to `docs/roadmap.md` for untracked learn follow-ups: rejected because unowned roadmap accumulation weakens prioritization; use an issue, active plan, or proposal instead.
- Treating maintainer-requested rule adoption as durable learn capture without accumulated evidence: rejected by `R29`; route that work to proposal deliberation.
- Hand-editing generated `.codex/skills/` or `dist/adapters/`: rejected because generated outputs must remain reproducible from canonical skill source and generator commands.
- Creating a top-level `docs/explain/` artifact: rejected because this ordinary non-trivial change already has the required change-local explanation surface.

## Scope Control

- This change does not make `learn` mandatory for every change.
- It does not make `learn` own plan lifecycle, review-resolution closeout, verification readiness, PR readiness, or CI status.
- It does not create session templates, topic templates, empty topic files, a fixed topic taxonomy, historical-note migration, issue-tracker automation, or background lesson triage.
- It does not change product runtime behavior, deployment, persistence, external APIs, or release packaging.
- It does not add structural validation for session/topic file content; selector support is intentionally lightweight.
- It does not move the active plan to Done. The plan remains Active until PR or merge lifecycle closeout updates it.

## Risks And Follow-Ups

- Hosted CI remains external and unobserved until the PR runs in GitHub Actions.
- Session and topic file shapes are intentionally not templated yet; a later proposal can add templates or validators if usage shows a stable shape.
- The direct M4 code-review was clean but not added as a tracked review record because the direct request produced no material findings. The tracked review-resolution surface remains closed and complete for all material findings.
- PR body preparation and PR opening remain owned by the `pr` stage.

## Readiness

M1-M4 implementation, tracked review-resolution closeout, direct final code-review, `$verify`, and final `$explain-change` are complete. The change is ready for PR handoff after this closeout diff is committed. Direct `$explain-change` execution stops before preparing or opening the PR.
