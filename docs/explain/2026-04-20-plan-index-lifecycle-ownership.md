# Plan index lifecycle ownership rationale

## Summary

This explanation covers the plan-index lifecycle ownership feature range `155be39..903394b`.

The change adds a full proposal/spec/test-spec/plan trail for lifecycle-closeout ownership, updates the governing workflow docs and stage skills so contributors can discover the ownership split without chat history, normalizes the plan template and already-known stale plan surfaces, and closes the feature itself to `Done` during verify once the on-branch outcome was known.

This feature is mostly documentation, workflow-contract, and repository-state work rather than new runtime logic. The diff is therefore large in artifact count but narrow in behavioral scope: it changes how contributors record and review lifecycle state for planned initiatives, not how the product runs.

## Problem

The repository had already demonstrated the failure mode this feature addresses:

- a completed initiative remained listed under `## Active` in `docs/plan.md`;
- later work had to reason around stale active guidance;
- ownership of lifecycle closeout was too implicit across `plan`, `implement`, `verify`, `pr`, and `learn`;
- the plan template and touched historical plan bodies did not teach or model the intended lifecycle vocabulary consistently.

If left unchanged, contributors could keep claiming PR readiness while `docs/plan.md` and plan bodies disagreed about whether an initiative was still active.

## Decision trail

| Artifact | Decision carried into the change | How it shaped the diff |
| --- | --- | --- |
| [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md) | Reject implicit ownership, reject `learn` as lifecycle authority, and reject early automation; make final closeout own lifecycle state while `verify` enforces drift detection. | The diff changes workflow docs, skills, and plan surfaces instead of adding automation or retrospective bookkeeping rules. |
| [`plan-index-lifecycle-ownership.md`](../../specs/plan-index-lifecycle-ownership.md) | Define the contract in `R1`-`R9`: `docs/plan.md` is an index, plan bodies stay synchronized with it, `implement` owns ongoing plan-body updates, `verify` blocks stale lifecycle state, and adoption should correct already-known stale state. | The diff updates governance/workflow docs, stage skills, plan template guidance, and touched plan/index state to reflect those rules. |
| [`plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md) | Use manual and structural proof surfaces (`T1`-`T10`) rather than synthetic runtime tests. | The implementation records path scans, lifecycle-state scans, manual plan/index comparisons, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, and `bash scripts/ci.sh` instead of adding low-value executable tests for prose. |
| [`2026-04-19-rigorloop-first-release-repository-architecture.md`](../architecture/2026-04-19-rigorloop-first-release-repository-architecture.md) and [`ADR-20260419-repository-source-layout.md`](../adr/ADR-20260419-repository-source-layout.md) | Keep `skills/` canonical, `.codex/skills/` generated, and `docs/plans/0000-00-00-example-plan.md` as the canonical plan template. | The feature edits canonical `skills/` first, regenerates `.codex/skills/`, and teaches lifecycle-aware plan behavior in the canonical plan example rather than adding a second plan surface. |
| [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Implement in three milestones: core workflow docs, stage skills, and plan-surface migration. Close the feature to `Done` before PR when the outcome is already known. | The branch history splits into M1 (`99907da`), M2 (`6d507c1`), M3 (`0a24fe3`), and a verify-stage closeout commit (`903394b`). |
| Code-review and verify findings | Keep the active plan body current during the feature, and do not defer a known `Done` transition until after PR. | Review fixups updated stale plan metadata after M1, and verify performed the final lifecycle closeout for this initiative itself before `pr`. |

## Milestone map

| Milestone or stage | Commits | Outcome |
| --- | --- | --- |
| M1 | `99907da` | Made lifecycle-closeout ownership, stale-state blocking, and index-versus-body semantics explicit in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `specs/rigorloop-workflow.md`. |
| M2 | `6d507c1` | Aligned canonical `plan`, `implement`, `verify`, `pr`, `learn`, and `workflow` skills with the ownership split and regenerated `.codex/skills/`. |
| M3 | `0a24fe3` | Normalized `docs/plan.md`, the canonical plan example, and already-known stale historical plan surfaces. |
| Verify closeout | `903394b` | Closed the feature itself to `Done` after verify confirmed the on-branch outcome was already known and no merge-dependent exception applied. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Governing workflow contract | [`CONSTITUTION.md`](../../CONSTITUTION.md), [`AGENTS.md`](../../AGENTS.md), [`docs/workflows.md`](../workflows.md), [`specs/rigorloop-workflow.md`](../../specs/rigorloop-workflow.md) | Added explicit lifecycle-index versus plan-body semantics, `implement` ownership during execution, verify-stage stale-state blocking, and the done-before-PR default with a merge-dependent exception. | Contributors needed one clear rule for when and how lifecycle state changes, not scattered implicit expectations. | Proposal decision; spec `R1`, `R2`, `R4`, `R6`-`R8a`; plan M1 | `T1`, `T3`, `T4`, `T5`; focused doc scans recorded in the plan and rerun during verify |
| Durable feature artifacts | [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md), [`plan-index-lifecycle-ownership.md`](../../specs/plan-index-lifecycle-ownership.md), [`plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md), [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Added the proposal/spec/test-spec/plan trail and kept the active plan’s progress, decisions, surprises, validation notes, and later stage-readiness state current. | The workflow change needed tracked decision memory and test mapping, not chat-only approval context. | Proposal, spec, test spec, plan; `CONSTITUTION.md` active-plan rule | Proposal-review, plan-review, code-review, and verify findings are all reflected in the plan history |
| Stage skill alignment | [`skills/plan/SKILL.md`](../../skills/plan/SKILL.md), [`skills/implement/SKILL.md`](../../skills/implement/SKILL.md), [`skills/verify/SKILL.md`](../../skills/verify/SKILL.md), [`skills/pr/SKILL.md`](../../skills/pr/SKILL.md), [`skills/learn/SKILL.md`](../../skills/learn/SKILL.md), [`skills/workflow/SKILL.md`](../../skills/workflow/SKILL.md), matching [`.codex/skills/`](../../.codex/skills/) files | Clarified that `plan` owns startup and replanning, `implement` owns ongoing plan-body updates, `verify` blocks stale lifecycle state, `pr` expects lifecycle closeout when final state is known, and `learn` is retrospective only. | Updating docs without runtime guidance would have left the repository teaching contradictory behavior. | Spec `R4`, `R7`, `R7a`, `R8`, `R8a`; architecture/ADR generated-boundary rule; plan M2 | `T2`, `T3`, `T5`, `T6`; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`; lifecycle wording scan across canonical and generated skills |
| Plan template and historical plan normalization | [`docs/plan.md`](../plan.md), [`0000-00-00-example-plan.md`](../plans/0000-00-00-example-plan.md), [`2026-04-19-rigorloop-first-release-implementation.md`](../plans/2026-04-19-rigorloop-first-release-implementation.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Made the template model lifecycle-aware closeout, moved known-done historical plans under `Done`, and removed stale active-state wording from touched plan bodies. | Adoption needed to start from a truthful baseline and teach contributors how to keep the plan index and plan body synchronized. | Spec `R3`, `R3a`, `R3b`, `R5`, `R9`; plan M3 | `T7`, `T8`, `T9`; index-section scan, per-slug uniqueness loop, lifecycle wording scan, and manual review of touched plans |
| Verify-stage closeout | [`docs/plan.md`](../plan.md), [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md) | Closed the feature itself to `Done` during verify, recorded the verify finding that the plan was still stale after code review, and updated readiness from `explain-change` plus `pr` to `pr` only after this explanation artifact was created. | Once implementation, code review, and verify all passed on-branch, deferring `Done` until after PR would have violated the very rule this feature introduced. | Spec `R5`, `R6`, `R6a`, `R7`, `R7a`; workflow spec `R8g`-`R8ja`; verify finding | Final verify reruns plus lifecycle-state manual review; closeout commit `903394b` |

## Tests added or changed

No new executable application tests were added. That was intentional.

The feature added the dedicated test spec [`specs/plan-index-lifecycle-ownership.test.md`](../../specs/plan-index-lifecycle-ownership.test.md), which maps the contract to the following proof surfaces:

- `T1`: manual review of governing workflow docs;
- `T2`: canonical/generated skill alignment plus structural validation and drift checks;
- `T3` and `T4`: manual proof of done-transition timing and immediate blocked/superseded handling;
- `T5`: verify-stage stale-state blocking and lifecycle-evidence expectations;
- `T6`: confirmation that `learn` remains non-authoritative;
- `T7` through `T9`: structural plan-index checks, lifecycle-wording scans, and manual plan-body comparisons;
- `T10`: confirmation that the change does not imply new heavyweight automation.

This test level is appropriate because the feature changes contributor-visible workflow and repository-state contracts, not executable runtime behavior. The best proof surfaces are tracked docs, plan/index state, canonical/generated skill trees, and repo-owned validation commands.

## Verification evidence

Final verification was run against the committed branch state through `903394b`.

Commands run:

- `rg -n "docs/plan\.md|plan body|lifecycle closeout|Blocked|Done|Superseded|stale lifecycle|learn|verify" CONSTITUTION.md AGENTS.md docs/workflows.md specs/rigorloop-workflow.md`
  - pass
- `python scripts/validate-skills.py`
  - pass
  - important output: validated 22 skill files
- `python scripts/build-skills.py --check`
  - pass
  - important output: generated skills are in sync
- `rg -n "docs/plan\.md|plan body|lifecycle|closeout|stale|learn|verify|merge-dependent|post-merge|Blocked|Superseded|authoritative" skills .codex/skills`
  - pass
- `rg -n "^## (Active|Blocked|Done|Superseded)$" docs/plan.md`
  - pass
- `for slug in 2026-04-19-rigorloop-first-release-implementation 2026-04-20-constitution-governance-migration 2026-04-20-plan-index-lifecycle-ownership; do test "$(rg -c "${slug}\\.md" docs/plan.md)" -eq 1; done`
  - pass
- `rg -n "Status|Outcome and retrospective|Readiness|ready for PR|ready for code-review|complete and now belongs|blocked|superseded" docs/plans/0000-00-00-example-plan.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md docs/plans/2026-04-20-constitution-governance-migration.md docs/plans/2026-04-20-plan-index-lifecycle-ownership.md`
  - pass
- `git diff --check 155be39..HEAD`
  - pass
- `bash scripts/ci.sh`
  - pass
  - important output: 9 skill-validator fixture tests passed and generated-skill drift check passed

Manual checks:

- reviewed the `Done` section in [`docs/plan.md`](../plan.md);
- reviewed the active feature plan’s `Status`, `Outcome and retrospective`, and `Readiness` surfaces after closeout;
- confirmed the full diff range changes only the planned workflow, skill, spec, and plan surfaces for this initiative.

CI boundary:

- local repo-owned validation passed through [`scripts/ci.sh`](../../scripts/ci.sh);
- [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) remains the intended thin wrapper over that script;
- hosted GitHub Actions CI was not observed from this environment, so this explanation does not claim remote CI passed.

Evidence note:

- the shell loop text in commit bodies `0a24fe3` and `903394b` was shell-expanded when the commits were created, so the authoritative command text is the validation record in [`2026-04-20-plan-index-lifecycle-ownership.md`](../plans/2026-04-20-plan-index-lifecycle-ownership.md), not those commit bodies.

## Alternatives rejected

These alternatives were explicitly rejected by the proposal or later stage findings:

- Keep lifecycle-closeout ownership implicit.
  - Rejected because the repository had already produced stale active-plan state in practice.
- Make `learn` the owner of plan-index closeout.
  - Rejected because `learn` is optional and retrospective, while lifecycle bookkeeping is operational state.
- Add automation or CI enforcement before the ownership rule was stable.
  - Rejected because the problem was a workflow-contract gap first, not a missing automation system.
- Redesign the full internal structure of every historical plan file.
  - Rejected because the feature only needed lifecycle-status, readiness, and closeout normalization on touched plans.
- Defer this feature’s own `Done` transition until after PR or merge.
  - Rejected during verify because the outcome was already known on-branch and no merge-dependent exception applied.

## Scope control

This feature intentionally did not:

- add lifecycle automation that infers plan state from git or PR status;
- redesign the repository layout or create a new planning system;
- turn `learn` into required bookkeeping;
- rewrite archival proposals, explain artifacts, or review notes beyond the touched stale plan surfaces;
- broaden into unrelated governance, CI, or release-process cleanup beyond lifecycle-closeout ownership.

## Risks and follow-ups

The feature is verified and locally ready for PR, but a few follow-ups remain visible:

- hosted CI has not been observed from this environment;
- commit bodies `0a24fe3` and `903394b` contain shell-expanded loop text, so readers should rely on the plan’s validation notes for the exact command wording;
- the working tree still contains two unrelated untracked proposal drafts outside this explained diff:
  - [`2026-04-20-docs-changes-usage-policy.md`](../proposals/2026-04-20-docs-changes-usage-policy.md)
  - [`2026-04-20-workflow-stage-handoff-clarity.md`](../proposals/2026-04-20-workflow-stage-handoff-clarity.md)

## PR-ready summary

- Added a full proposal/spec/test-spec/plan trail for lifecycle-closeout ownership.
- Made lifecycle ownership explicit in the governing workflow docs and in the canonical and generated stage skills.
- Normalized the plan template and the already-known stale plan/index surfaces to a truthful `Done` baseline.
- Closed the feature itself to `Done` during verify because the final outcome was already known before PR.
- Verified the full feature with focused lifecycle scans, skill validation and drift checks, `git diff --check`, and `bash scripts/ci.sh`.
