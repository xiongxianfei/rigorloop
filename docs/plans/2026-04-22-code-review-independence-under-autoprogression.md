# Code review independence under autoprogression plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-22
- Last updated: 2026-04-22
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved code-review independence contract as a small workflow-and-skill change that keeps the existing v1 autoprogression boundaries intact.

This initiative should make `code-review` credible when it is entered automatically after `implement` by requiring:

- independent-review mode;
- a first-pass review record before review-driven fixes begin;
- explicit `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive` status handling;
- checklist coverage plus no-finding rationale for clean reviews; and
- optional rather than mandatory positive notes.

The implementation must stay inside the approved first slice:

- no executable workflow router;
- no hard fresh-session enforcement;
- no mandatory human reviewer or second-pass reviewer for every change;
- no fast-lane or bugfix autoprogression expansion; and
- no new standalone `review-resolution.md` requirement created solely by this feature.

## Source artifacts

- Proposal: `docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md`
- Spec: `specs/code-review-independence-under-autoprogression.md`
- Spec-review findings carried into this plan:
  - no separate architecture artifact is expected for the first slice;
  - issues that are clearly fixable within current approved scope use `changes-requested`, not `blocked`;
  - clean reviews require checklist coverage and no-finding rationale, while positive notes remain optional.
- Architecture: none. The approved spec says no separate architecture artifact is expected for the first slice.
- Architecture-review findings: none.
- Test spec: `specs/code-review-independence-under-autoprogression.test.md` is now active and owns first-pass review record, status mapping, clean-review validity, and sensitive-change coverage for this initiative.
- Related workflow and proof surfaces:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/code-review/SKILL.md`
  - generated `.codex/skills/`

## Context and orientation

- The focused approved spec is additive to the existing workflow-stage autoprogression contract. Implementation must preserve the current `implement -> code-review -> review-resolution/code-review -> verify` chain while tightening how the first review pass is recorded and justified.
- The main authored surfaces likely to change are:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md` only if adjacent handoff wording would otherwise contradict the approved spec
  - `AGENTS.md` if the approved contract changes practical agent behavior or validation expectations
  - `CONSTITUTION.md` only if implementation reveals a governance or principle change rather than a lower-level workflow or skill update
- Generated `.codex/skills/` output remains derived. Regenerate it; do not hand-edit it.
- The repository currently has no `docs/project-map.md`. The change is narrow enough that a project map is not required for planning.
- Existing proof ownership is split:
  - the new focused test spec will own the first-pass record, status mapping, clean-review validity, and optional-positive-note coverage;
  - `specs/workflow-stage-autoprogression.test.md` already owns overlapping proof for the `code-review <-> review-resolution` loop, isolated-stage behavior, and bounded v1 autoprogression. Update it only where the new feature would otherwise make those existing proof cases drift.
- This is ordinary non-trivial work. Implementation must carry the baseline change-local pack:
  - `docs/changes/2026-04-22-code-review-independence-under-autoprogression/change.yaml`
  - `docs/changes/2026-04-22-code-review-independence-under-autoprogression/explain-change.md`

## Non-goals

- Reverting `implement -> code-review` autoprogression.
- Requiring hard fresh-session enforcement.
- Requiring a human reviewer or mandatory second-pass reviewer for every non-trivial change.
- Expanding autoprogression into fast-lane or bugfix execution.
- Redefining when standalone `review-resolution.md` is required.
- Requiring generic praise or positive-note boilerplate in every clean review.
- Building a repo-owned workflow router, persistent state store, or review queue.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R3e`, `R6`-`R7`, observability section, acceptance criteria | `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md`, generated `.codex/skills/` |
| `R4`-`R5`, `R8`-`R8d`, state/invariants, edge cases | `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `skills/implement/SKILL.md` only if adjacent handoff wording needs alignment, generated `.codex/skills/` |
| clean-review template and optional-positive-note rule | `skills/code-review/SKILL.md`, generated `.codex/skills/`, targeted workflow summary wording in `docs/workflows.md` |
| change-local durability and lifecycle truthfulness for this initiative | `docs/changes/2026-04-22-code-review-independence-under-autoprogression/`, `docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`, `docs/plan.md`, explicit-path artifact validation |
| overlapping autoprogression proof ownership | `specs/code-review-independence-under-autoprogression.test.md` plus targeted updates to `specs/workflow-stage-autoprogression.test.md` during `test-spec` |

## Milestones

### M1. Implement the independent first-pass code-review contract

- Goal:
  - Align canonical workflow guidance, `code-review` stage behavior, and generated skill output with the approved first-pass review contract without broadening v1 autoprogression scope.
- Requirements:
  - `R1`-`R8d`
- Files/components likely touched:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md` if adjacent wording needs a narrow consistency fix
  - `AGENTS.md` if the recorded guidance-impact check shows practical agent behavior or validation expectations changed
  - `CONSTITUTION.md` only if the same check shows a governance or principle change rather than lower-level workflow guidance
  - `docs/changes/2026-04-22-code-review-independence-under-autoprogression/change.yaml`
  - `docs/changes/2026-04-22-code-review-independence-under-autoprogression/explain-change.md`
  - generated `.codex/skills/`
- Dependencies:
  - approved proposal
  - approved spec
  - `plan-review`
  - active test spec created after `plan-review`
- Tests to add/update:
  - create `specs/code-review-independence-under-autoprogression.test.md`
  - update `specs/workflow-stage-autoprogression.test.md` only where its existing proof ownership for `code-review` loop and isolated-stage behavior would otherwise drift
- Implementation steps:
  - update `skills/code-review/SKILL.md` to require independent-review mode, first-pass review record contents, explicit status mapping, clean-review validity rules, optional-positive-note guidance, and the recommended clean-review template;
  - update `skills/workflow/SKILL.md` so workflow-managed versus isolated `code-review` behavior matches the approved spec and preserves the current autoprogression boundary;
  - update `docs/workflows.md` only where the short operational summary needs to mention the first-pass review record, `inconclusive`, or optional positive notes to avoid stale contributor guidance;
  - touch `skills/implement/SKILL.md` only if its handoff wording would otherwise contradict the approved `code-review` contract;
  - explicitly check whether the approved contract affects `AGENTS.md` or `CONSTITUTION.md`;
  - if `AGENTS.md` is affected because practical agent behavior or validation expectations changed, update it in this milestone;
  - if `CONSTITUTION.md` is affected because the change rises to a governance or principle change, update it in this milestone;
  - if neither file is affected, record that no-change decision in the plan validation notes instead of leaving the omission implicit;
  - create the baseline change-local pack for this initiative;
  - regenerate `.codex/skills/` after canonical skill changes.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md --path docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
  - `rg -n 'independent-review|first-pass review record|clean-with-notes|changes-requested|blocked|inconclusive|no-finding rationale|positive note|review-resolution' skills/code-review/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md`
  - `rg -n 'code-review|verify|validation|workflow-managed|isolated|review-resolution' AGENTS.md CONSTITUTION.md docs/workflows.md`
  - `git diff --check -- skills/code-review/SKILL.md skills/workflow/SKILL.md skills/implement/SKILL.md docs/workflows.md specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md docs/changes/2026-04-22-code-review-independence-under-autoprogression .codex/skills`
  - `bash scripts/ci.sh`
- Expected observable result:
  - canonical and generated workflow guidance describe a credible first-pass `code-review`, clean reviews require checklist coverage plus no-finding rationale, positive notes are optional, workflow-managed fixable findings still auto-enter `review-resolution`, and isolated requests still stop after review.
- Commit message: `M1: implement code-review independence contract`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - canonical `skills/` and generated `.codex/skills/` may drift;
  - wording may accidentally imply hard session enforcement or mandatory human review;
  - workflow summary wording may blur the boundary between `changes-requested` and `blocked`;
  - implementation may duplicate proof already owned by `specs/workflow-stage-autoprogression.test.md`.
- Rollback/recovery:
  - revert canonical and generated skill changes together;
  - revert the workflow summary wording together with the skill changes if contributor guidance becomes inconsistent;
  - if the scope expands beyond the expected surfaces, stop and split a new milestone instead of widening M1 silently.

## Validation plan

- Before implementation:
  - complete `plan-review`;
  - rely on active `specs/code-review-independence-under-autoprogression.test.md`;
  - update `specs/workflow-stage-autoprogression.test.md` during `test-spec` only where overlap requires it.
- During implementation:
  - run the narrow skill/generation checks first:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
  - run the explicit-path artifact validator for the touched lifecycle-managed artifacts once the test spec exists;
  - record the explicit `AGENTS.md` / `CONSTITUTION.md` impact decision in validation notes;
  - use targeted `rg` and `git diff --check` commands before the repo-wide smoke pass.
- Final milestone proof:
  - run `bash scripts/ci.sh`;
  - record the exact commands and results in this plan body's validation notes.

## Risks and recovery

- Risk: implementation weakens the approved autoprogression boundary.
  - Recovery: revert workflow and skill wording together and re-check against `specs/workflow-stage-autoprogression.md`.
- Risk: clean reviews become template-shaped but not evidence-backed.
  - Recovery: tighten the `code-review` skill wording rather than adding generic positive-note boilerplate.
- Risk: adjacent stage wording in `skills/implement/SKILL.md` or `docs/workflows.md` drifts from the focused spec.
  - Recovery: keep the change narrow, update only the contradicting adjacent wording, and rerun the targeted `rg` proof.
- Risk: proof ownership overlaps between the new test spec and `specs/workflow-stage-autoprogression.test.md`.
  - Recovery: keep the new test spec focused on the new contract and update the older test spec only where its existing coverage would drift.

## Dependencies

- `plan-review` must complete before implementation starts.
- `test-spec` must create the active test spec before production guidance changes begin.
- No separate architecture artifact is planned; if implementation expands beyond guidance-and-skill alignment or requires new orchestration behavior, stop and create architecture before implementation.
- The baseline change-local pack for this ordinary non-trivial change is required during implementation.
- Generated `.codex/skills/` output must stay synchronized with canonical `skills/`.

## Progress

- [x] 2026-04-22: proposal accepted and focused spec approved.
- [x] 2026-04-22: plan created and indexed in `docs/plan.md`.
- [x] 2026-04-22: plan-review feedback incorporated.
- [x] 2026-04-22: `specs/code-review-independence-under-autoprogression.test.md` created and activated.
- [x] 2026-04-22: M1 implemented, validated, and prepared for `code-review`.

## Decision log

- 2026-04-22: No separate architecture artifact is planned for the first slice. Rationale: the approved spec limits the implementation to workflow summary and skill guidance, not a new orchestration subsystem.
- 2026-04-22: Start with one implementation milestone. Rationale: the expected authored surfaces are narrow enough for one coherent review loop and one coherent commit; split later only if implementation expands.
- 2026-04-22: Treat `specs/workflow-stage-autoprogression.test.md` as an overlapping proof owner rather than replacing it. Rationale: the existing test spec already owns the `code-review` loop and isolated-stage scenarios that this feature refines.
- 2026-04-22: Plan-review required early `python scripts/test-skill-validator.py` coverage and an explicit `AGENTS.md` / `CONSTITUTION.md` impact check. Rationale: skill-regression failures should be caught before the final `bash scripts/ci.sh` pass, and guidance-surface omission must be an explicit recorded decision rather than an implicit assumption.
- 2026-04-22: Left `AGENTS.md`, `CONSTITUTION.md`, and `skills/implement/SKILL.md` unchanged during M1. Rationale: the approved slice only required stage-local `code-review` and workflow guidance alignment; governance principles, practical repo-wide agent rules, and `implement` handoff wording already remained consistent with the approved contract.

## Surprises and discoveries

- 2026-04-22: `python scripts/validate-skills.py` counts raw `# ` lines anywhere in a skill body, including fenced examples. The clean-review example in `skills/code-review/SKILL.md` had to avoid a literal top-level heading inside the fenced template to satisfy the validator.

## Validation notes

- 2026-04-22: `test-spec` created `specs/code-review-independence-under-autoprogression.test.md`, updated `specs/workflow-stage-autoprogression.test.md` only to clarify proof ownership, and refreshed proposal/spec/plan lifecycle references.
- 2026-04-22: M1 updated `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md`, created the baseline change-local pack under `docs/changes/2026-04-22-code-review-independence-under-autoprogression/`, and regenerated `.codex/skills/`.
- 2026-04-22: M1 targeted validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-independence-under-autoprogression/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md --path docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
  - `rg -n 'independent-review|first-pass review record|clean-with-notes|changes-requested|blocked|inconclusive|no-finding rationale|positive note|review-resolution' skills/code-review/SKILL.md skills/workflow/SKILL.md docs/workflows.md .codex/skills specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md`
  - `rg -n 'code-review|verify|validation|workflow-managed|isolated|review-resolution' AGENTS.md CONSTITUTION.md docs/workflows.md`
  - `git diff --check -- skills/code-review/SKILL.md skills/workflow/SKILL.md skills/implement/SKILL.md docs/workflows.md specs/code-review-independence-under-autoprogression.test.md specs/workflow-stage-autoprogression.test.md docs/changes/2026-04-22-code-review-independence-under-autoprogression .codex/skills`
  - `bash scripts/ci.sh`
  - Result: passed.
- 2026-04-22: No `docs/plan.md` lifecycle update was needed during M1. The initiative remained active, and the existing active-plan index entry stayed truthful while implementation moved the plan body from `implement` readiness to `code-review` readiness.

## Outcome and retrospective

- This initiative is active. M1 is implemented and awaits independent `code-review`; downstream lifecycle closeout remains pending until later stages settle the branch.

## Readiness

- The next stage is `code-review`.
- M1 is complete and ready for the first independent review pass.

## Risks and follow-ups

- If implementation shows that `skills/verify/SKILL.md` or other adjacent stage skills also need alignment, add that work explicitly instead of widening the scope silently.
- If later execution shows that guidance alone cannot preserve independence, open a separate architecture/proposal track for stronger enforcement rather than broadening this change ad hoc.
