# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Target: branch diff `origin/main...HEAD`
Reviewed milestone: M1. Selected skill reminder audit and implementation
Reviewed artifact: commits `400fb3a` and `fd0406a`
Review date: 2026-05-14
Reviewer: Codex code-review
Recording status: recorded
Status: changes-requested

## Review status

changes-requested

## Review inputs

- Diff/review surface: `git diff origin/main...HEAD`
- Tracked governing branch state: branch `feat/cost-bounded-rigor-m2-skill-wording` is clean and two commits ahead of `origin/main`.
- Governing artifacts:
  - `specs/cost-bounded-rigor-m2-selected-skill-reminders.md`
  - `specs/cost-bounded-rigor-m2-selected-skill-reminders.test.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md`
- Validation evidence:
  - `python scripts/test-skill-validator.py` passed after the workflow reminder edit.
  - `python scripts/validate-skills.py` passed.
  - `python scripts/build-skills.py --check` passed.
  - `python scripts/measure-skill-tokens.py` completed as diagnostic-only evidence.
  - `bash scripts/ci.sh --mode explicit ...` passed for selected skill, lifecycle, review-artifact, and change-metadata paths.

## Diff summary

The branch adds the focused M2 spec, test spec, plan, change-local review evidence, and one implementation edit for selected skill reminders.

`skills/workflow/SKILL.md` gains a short path/state lookup reminder that starts from active plan state, current artifact metadata, `docs/workflows.md`, default paths, and targeted headings before broader searches, with an expansion escape when narrower evidence is incomplete, contradictory, or insufficient.

`scripts/test-skill-validator.py` adds `test_cost_bounded_rigor_m2_selected_skill_reminders` for selected skill boundaries, existing proposal/proposal-review lookup wording, workflow path/state lookup wording, and absence of duplicated full workflow sequence text.

The plan records `proposal` and `proposal-review` as unchanged with rationale and records `workflow` as edited. Prior `code-review-m1-r1` closed cleanly, and this second review covers the current branch state including the review/state-sync commit.

## Material findings

### CBR-M2-CR2-1 - Static proof freezes an exact full sentence

Finding ID: CBR-M2-CR2-1

Severity: major

Location: `scripts/test-skill-validator.py`

Evidence: The approved M2 spec says `R14. Static proof MUST NOT require a selected skill to use one exact sentence when equivalent concise wording satisfies the contract.` The active M2 test spec `T5` repeats that static proof must not require one exact sentence. The new `test_cost_bounded_rigor_m2_selected_skill_reminders` requires every selected skill body to contain the exact full sentence `Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.` A selected skill could preserve bounded-first and do-not-under-read behavior with equivalent concise wording, but this test would fail solely because the sentence changed.

Required outcome: The M2 static proof must keep narrow, stable checks without requiring one exact full sentence where equivalent concise wording would satisfy the approved contract.

Safe resolution path: Replace the exact full-sentence assertion with smaller stable behavior cues or section-presence checks, such as separate checks for exact ranges, narrower evidence, and insufficient evidence, or rely on the existing section/full-file escape checks plus the workflow-specific path/state terms. Keep the selected-surface and forbidden-sequence checks. Rerun `python scripts/test-skill-validator.py` and the selected CI command for the changed paths.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | The implementation scope is narrow, but the static proof conflicts with M2 `R14` by requiring one exact full sentence. |
| Test coverage | concern | `test_cost_bounded_rigor_m2_selected_skill_reminders` covers real M2 boundaries, but one assertion is too brittle for the approved proof contract. |
| Edge cases | concern | Edge case `EC7` says a proposed static test enforcing exact prose must be rejected or narrowed; the current test enforces exact prose for one sentence. |
| Error handling | pass | No runtime or parser error behavior changes are introduced. |
| Architecture boundaries | pass | No runtime, persistence, API, release, adapter packaging, selector, or architecture boundary changes are included. |
| Compatibility | concern | Future equivalent selected-skill wording could satisfy the spec but fail validation because of a full-sentence assertion. |
| Security/privacy | pass | The skill wording continues to prefer targeted evidence over broad dumps and does not introduce secret-handling risk. |
| Derived artifact currency | pass | `build-skills.py --check` and adapter archive regression passed; generated public adapter skill bodies were not edited. |
| Unrelated changes | pass | The branch stays within M2 selected skill reminders, focused proof, and lifecycle/review evidence. |
| Validation evidence | concern | The selected validation passed, but passing validation includes the brittle assertion identified above. |

## No-finding rationale

Not applicable; one material finding requires a targeted fix before M1 can return to clean code-review.

## Residual risks

- Hosted CI has not been observed for this branch.
- Final explain-change, verify, and PR handoff remain blocked until this finding is resolved and code-review reruns cleanly.

## Milestone-aware handoff

- Reviewed milestone: M1. Selected skill reminder audit and implementation.
- Review status: changes-requested.
- Milestone state after review: resolution-needed.
- Required review-resolution: required for `CBR-M2-CR2-1`.
- Remaining implementation milestones: M1 requires targeted review-resolution/fix; no later implementation milestones are in scope.
- Next stage: review-resolution for `CBR-M2-CR2-1`, then targeted implementation fix and rerun code-review.
- Final closeout readiness: not ready; material finding remains open, and explain-change, verify, and PR are not complete.
