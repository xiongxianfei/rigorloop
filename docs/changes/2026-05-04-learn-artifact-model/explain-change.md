# Learn Artifact Model Change Explanation

## Status

M3 implemented and code-review clean; M4 not started.

## Summary

This change aligns the workflow contract, selector behavior, learn skill guidance, learn namespace index, and generated outputs with the approved final learn artifact model.

The workflow spec no longer treats learn output as a temporary follow-up or no-learn rationale surface. A learn invocation that reaches Frame now records a tracked session under `docs/learn/sessions/YYYY-MM-DD-<slug>.md`; durable topic guidance is under `docs/learn/topics/<topic>.md` only when confirmed durable lessons justify it; behavior-changing lessons route to the authoritative action-owning artifact.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-03-optimize-learn-skill.md`
- Spec: `specs/learn-artifact-model.md`
- Test spec: `specs/learn-artifact-model.test.md`
- Plan: `docs/plans/2026-05-04-learn-artifact-model.md`
- Workflow contract: `specs/rigorloop-workflow.md`

## M1 Diff Rationale

| File or area | Change | Reason | Proof |
| --- | --- | --- | --- |
| `specs/rigorloop-workflow.test.md` | Updated `T23` and related coverage language before the implementation docs changed. | Establishes the M1 proof expectation that workflow guidance links to the final learn artifact model and no longer treats final learn modeling as deferred. | Manual contract proof in `T23`; stale-term scan. |
| `specs/rigorloop-workflow.md` | Replaced temporary learn closeout wording with final session-record, pre-session no-record, topic-file, and action-owning artifact rules. | Makes the workflow spec point contributors to the approved learn model while preserving nonblocking default behavior. | `R7ba`-`R7bf`; artifact lifecycle validation. |
| `docs/workflows.md` | Added the short operational version of session-record and pre-session closeout rules. | Keeps the workflow summary aligned with the canonical contract without duplicating all learn skill details. | Selector-selected CI. |
| `AGENTS.md` | Updated practical agent guidance for triggered learn closeout after Frame versus pre-session closeout. | Prevents agent guidance from sending learn output back to temporary surfaces. | Selector-selected CI. |
| `CONSTITUTION.md` | Added the durable learn-output principle under documentation rules. | Keeps governance-level guidance aligned for durable lessons without expanding into a template. | Selector-selected CI. |
| `README.md` | Reviewed and left unchanged. | It mentions periodic learning as a lifecycle category but does not define or conflict with learn artifact surfaces. | Unaffected rationale in `change.yaml`. |
| `docs/changes/2026-05-04-learn-artifact-model/` | Added baseline change metadata and this explanation. | Required durable reasoning and traceability pack for ordinary non-trivial work. | Change metadata validation. |

## Scope Control

- M1 does not edit `skills/learn/SKILL.md`; that is M3.
- M1 does not create `docs/learn/README.md`; that is M3 after selector recognition in M2.
- M1 does not add selector path recognition; that is M2.
- M1 does not refresh generated `.codex/skills/` or public adapter output; that follows canonical skill changes in M3.
- M1 does not add session or topic templates, empty topic files, fixed taxonomy, issue tracker integration, or historical-note migration.

## Validation Evidence

- `rg -n 'temporary learn|future learn refactor|final learn artifact model is deferred|docs/learnings|docs/retrospectives|Until a focused \`learn\` refactor|scheduled \`learn\` follow-ups and explicit no-learn rationales|temporary recording surfaces|Future focused \`learn\` refactor' specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/workflows.md AGENTS.md CONSTITUTION.md README.md` - passed.
- `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md` - passed; selected `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-learn-artifact-model/change.yaml` - passed.
- `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/learn-artifact-model.md --path specs/learn-artifact-model.test.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/plan.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md` - passed.
- `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md README.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md specs/learn-artifact-model.md specs/learn-artifact-model.test.md docs/plans/2026-05-04-learn-artifact-model.md docs/plan.md docs/changes/2026-05-04-learn-artifact-model` - passed.

Additional M1 validation is recorded in the active plan and `change.yaml`.

## Review State

`code-review` round 1 requested one targeted fix, `CR-M1-F1`, because `docs/workflows.md` and `specs/rigorloop-workflow.test.md` omitted the incident response and contributor observation trigger classes required by the workflow contract and learn artifact spec.

The finding was accepted in `review-resolution.md`. The fix adds those trigger classes to the operational workflow summary and `T23`; review-resolution validation passed with review artifact validation, lifecycle validation, selector-selected explicit CI, change metadata validation, stale-term scan, and whitespace validation.

`code-review` round 2 found no blocking or required-change findings for the M1 slice. M2-M4 remain unimplemented by design.

## Verification State

M1 verification passed for the committed M1 slice. The verifier checked review closeout, stale learn-surface wording, whitespace across the two M1 commits, selector-selected validation for the full touched surface, and explicit-path CI. The selector chose `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.

This is not full initiative `branch-ready`: M2 selector recognition, M3 learn skill/index/generated output, and M4 final lifecycle closeout remain open.

## M2 Diff Rationale

| File or area | Change | Reason | Proof |
| --- | --- | --- | --- |
| `scripts/test-select-validation.py` | Added `test_learn_artifact_paths_are_known_lightweight_paths`. | Proves `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**` are known paths and are not lifecycle-validated as specs, plans, ADRs, or architecture docs. | Test failed before selector implementation, then passed after M2. |
| `scripts/validation_selection.py` | Added `learn-artifact` classification for the lightweight learn namespace. | Satisfies `R44` without creating `docs/learn/**` content before M3 and without over-validating raw session/topic records. | `python scripts/test-select-validation.py`; representative explicit selector run. |
| `docs/plans/2026-05-04-learn-artifact-model.md` and `change.yaml` | Recorded M2 progress, validation, and scope boundary. | Keeps implementation-owned plan state and change metadata aligned with the real milestone. | Selector-selected explicit CI. |

## M2 Scope Control

- M2 does not create `docs/learn/README.md`; M3 owns that after selector recognition.
- M2 does not edit `skills/learn/SKILL.md` or generated skill/adapter output; M3 owns those surfaces.
- M2 does not add structural validators or templates for learn session/topic content.

## M2 Review Resolution

`code-review` round 1 found `CR-M2-F1`: the active plan's `Outcome And Retrospective` section still said M2 had not started after M2 was implemented. The finding was accepted, and the plan now records M1-M2 as implemented with M3-M4 still not started.

`code-review` round 2 found no blocking or required-change findings for the M2 slice.

## M2 Verification

M2 verification passed for the committed M2 slice. The verifier checked selector regression coverage, representative learn-path selector output, review closeout, whitespace across the three M2 commits, selector-selected validation for the full M2 touched surface, and explicit-path CI. The selector chose `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression` for the full touched surface.

This is not full initiative `branch-ready`: M3 review and M4 final lifecycle closeout remain open.

## M3 Diff Rationale

| File or area | Change | Reason | Proof |
| --- | --- | --- | --- |
| `scripts/test-skill-validator.py` | Added `test_learn_skill_final_artifact_model_and_bounded_process` before changing the skill. | Locks the approved Frame, Observe, Classify, Route process; canonical `docs/learn/` paths; one primary classification; secondary routes; confirmation; bounded evidence; and lightweight index boundaries. | Test failed before implementation because the index was absent and old learn guidance remained; passed after M3. |
| `skills/learn/SKILL.md` | Rewrote the learn operator guidance around Frame, Observe, Classify, and Route. | Makes `learn` a guided evidence process instead of a retrospective template, with contributor-confirmed routing into session records, topic guidance, action-owning artifacts, ADRs, proposals, or no-learn rationales. | `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`. |
| `docs/learn/README.md` | Added a lightweight namespace index for `sessions/` and `topics/`. | Gives contributors the canonical path model without introducing templates, empty topic files, or a prebuilt taxonomy. | M3 selector-selected CI. |
| Generated skill and adapter output | Refreshed `.codex/skills/learn/SKILL.md` and public adapter learn skill files through repository generators. | Keeps generated runtime mirrors and public adapter packages aligned with canonical `skills/learn/SKILL.md`. | `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| Plan and change metadata | Recorded M3 progress, validation, and the adapter portability discovery. | Keeps implementation-owned lifecycle evidence aligned with the actual milestone. | `python scripts/validate-change-metadata.py`; selector-selected explicit CI. |

## M3 Scope Control

- M3 does not add session templates, topic templates, empty topic files, or a fixed topic taxonomy.
- M3 does not migrate historical notes into `docs/learn/`.
- M3 does not make `learn` mandatory for every change.
- M3 does not start M4 lifecycle closeout.

## M3 Validation

- `python scripts/test-skill-validator.py` - failed before implementation for the expected missing-index and stale-guidance reasons, then passed after M3.
- `python scripts/validate-skills.py` - passed.
- `python scripts/build-skills.py` - passed.
- `python scripts/build-adapters.py --version 0.1.1` - passed after the generated-output boundary named public adapter alternatives alongside `.codex/skills/`.
- `python scripts/build-skills.py --check` - passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` - passed.
- `python scripts/validate-adapters.py --version 0.1.1` - passed.
- `bash scripts/ci.sh --mode explicit --path skills/learn/SKILL.md --path docs/learn/README.md --path scripts/test-skill-validator.py --path .codex/skills/learn/SKILL.md --path dist/adapters/claude/.claude/skills/learn/SKILL.md --path dist/adapters/codex/.agents/skills/learn/SKILL.md --path dist/adapters/opencode/.opencode/skills/learn/SKILL.md --path docs/plans/2026-05-04-learn-artifact-model.md --path docs/changes/2026-05-04-learn-artifact-model/change.yaml --path docs/changes/2026-05-04-learn-artifact-model/explain-change.md` - passed; selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.
- `git diff --check -- skills/learn/SKILL.md docs/learn/README.md scripts/test-skill-validator.py .codex/skills/learn/SKILL.md dist/adapters/claude/.claude/skills/learn/SKILL.md dist/adapters/codex/.agents/skills/learn/SKILL.md dist/adapters/opencode/.opencode/skills/learn/SKILL.md docs/plans/2026-05-04-learn-artifact-model.md docs/changes/2026-05-04-learn-artifact-model` - passed.

## M3 Review State

`code-review` round 1 found no blocking or required-change findings for the M3 slice. The review record is `docs/changes/2026-05-04-learn-artifact-model/reviews/code-review-m3-r1.md`.
