# Constitution governance migration plan

- Status: done
- Owner: maintainer + Codex
- Start date: 2026-04-20
- Last updated: 2026-04-20
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Migrate repository-wide governance from the draft Codex-scoped path to a general root `CONSTITUTION.md` without leaving split-brain guidance behind.

This plan exists because the reviewed spec and test spec now define a compatibility-sensitive migration with a broad guidance blast radius. The migration touches the root governance artifact, `AGENTS.md`, canonical `skills/`, generated `.codex/skills/`, and active guidance surfaces that currently teach contributors what to read.

The spec requires one coherent change rather than a long-lived staged rollout. This plan therefore uses one milestone that lands the full active-surface migration in one reviewable unit, with generated-skill sync and path-scan validation treated as required closeout gates rather than follow-up cleanup.

## Source artifacts

- Proposal: `docs/proposals/2026-04-20-constitution-governance-surface.md`
- Spec: `specs/constitution-governance-surface.md`
- Spec-review findings: 2026-04-20 review cycle in conversation approved the spec after three tightening passes:
  - root `CONSTITUTION.md` must define the source-of-truth order;
  - root `CONSTITUTION.md` must contain substantive repository-wide governance rules;
  - active guidance must be explicitly scoped for the migration and `AGENTS.md` must either reproduce or defer to the constitution order.
- Test spec: `specs/constitution-governance-surface.test.md`
- Related repository architecture context:
  - `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - `docs/adr/ADR-20260419-repository-source-layout.md`
  - These remain background context only; no new architecture artifact is planned because the existing canonical-versus-generated boundary already covers `skills/` and `.codex/skills/`.

## Context and orientation

- Current working state now contains:
  - tracked root `CONSTITUTION.md` as the canonical governance path in this branch
  - an updated `AGENTS.md` that points to `CONSTITUTION.md`
  - reviewed proposal, spec, and test spec artifacts for this migration
  - canonical `skills/` updated to the root constitution path and regenerated `.codex/skills/`
  - no `.codex/CONSTITUTION.md` file in the working tree
- The canonical-versus-generated boundary already exists:
  - canonical skills live under `skills/`
  - generated Codex compatibility output lives under `.codex/skills/`
  - `python scripts/build-skills.py --check` is the existing sync proof surface
- At plan creation, the active guidance set that named the governance path included at minimum:
  - `AGENTS.md`
  - the then-active plan indexed in `docs/plan.md`, `docs/plans/2026-04-20-constitution-governance-migration.md`
  - canonical skill files under `skills/`
  - generated skill files under `.codex/skills/`
- `docs/workflows.md` does not currently name the constitution path, so it is in scope only if implementation adds or changes governance-path wording there.
- Historical artifacts such as the accepted proposal for this migration are expected to keep old-path references where they describe prior state. They are not rewrite targets unless they still instruct contributors what to read today.
- The first-release implementation plan is now indexed under `Done` in `docs/plan.md`. It is a historical artifact for this migration unless it still instructs contributors what to read today.
- The largest blast radius is the skill corpus:
  - `skills/` contains the canonical guidance that must be updated first
  - `.codex/skills/` must be regenerated from those canonical changes in the same change

## Non-goals

- Rewriting governance policy beyond what is required to establish root `CONSTITUTION.md` as the governing surface.
- Refactoring unrelated workflow docs, CI behavior, release automation, or skill behavior beyond constitution-reference updates.
- Removing every historical mention of `.codex/CONSTITUTION.md` from proposals, review notes, explain-change artifacts, or other archival surfaces.
- Introducing a compatibility shim or redirect at `.codex/CONSTITUTION.md`.
- Turning this migration into a broader documentation cleanup initiative.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`, `R1a`, `R1b` | root `CONSTITUTION.md` |
| `R2` | removal of tracked `.codex/CONSTITUTION.md` |
| `R3`, `R4`, `R5` | `AGENTS.md` |
| `R6`, `R7`, `R8` | canonical `skills/`, generated `.codex/skills/`, and `python scripts/build-skills.py --check` |
| `R9`, `R9a` | `AGENTS.md`, this active plan file as indexed in `docs/plan.md`, and any other in-scope active guidance file naming the governance path |
| `R10` | no required edits to historical artifacts beyond confirming remaining references are historical |
| `R11`, `R12` | one coherent branch diff plus explicit validation evidence in this plan |

## Milestones

### M1. Land the root-constitution governance migration

- Goal:
  - Complete the full active-surface migration in one reviewable change so root `CONSTITUTION.md` becomes canonical, canonical skills adopt the new best-practice reference pattern, generated skills are regenerated, in-scope active guidance is accurate, and `.codex/CONSTITUTION.md` is removed.
- Requirements:
  - `R1`-`R12`
- Files/components likely touched:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `specs/constitution-governance-surface.test.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
  - canonical `skills/*/SKILL.md`
  - generated `.codex/skills/*/SKILL.md`
  - `.codex/CONSTITUTION.md` (deletion)
  - `docs/workflows.md` and other root or `docs/` guidance files only if they currently name the governance path or detailed governance source
- Dependencies:
  - reviewed spec: `specs/constitution-governance-surface.md`
  - test spec: `specs/constitution-governance-surface.test.md`
  - existing generated-skill sync command: `python scripts/build-skills.py --check`
  - normalized active plan index in `docs/plan.md`
- Tests to add/update:
  - no new executable tests are expected
  - update `specs/constitution-governance-surface.test.md` to reflect that a dedicated execution plan now exists for this migration
  - use the reviewed path-scan and generated-sync proof surfaces from `specs/constitution-governance-surface.test.md`
- Implementation steps:
  - revise and promote the current governance draft into tracked root `CONSTITUTION.md` so it satisfies `R1a` and `R1b`, including replacing internal `.codex/CONSTITUTION.md` authority claims and tool-scoped documentation rules
  - update `AGENTS.md` so it points to `CONSTITUTION.md` and either reproduces or defers to the constitution order
  - update canonical `skills/` first so any governance-path reference uses `CONSTITUTION.md`
  - regenerate `.codex/skills/` from canonical `skills/`
  - update this active plan if it still names the old path or states stale governance-path facts
  - update any other in-scope active guidance surface that names the constitution path or detailed governance source
  - remove `.codex/CONSTITUTION.md`
  - confirm remaining repository references to `.codex/CONSTITUTION.md` are historical only
- Validation commands:
  - `git ls-files --error-unmatch CONSTITUTION.md`
  - `! git ls-files --error-unmatch .codex/CONSTITUTION.md`
  - `! test -e .codex/CONSTITUTION.md`
  - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills .codex/skills AGENTS.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md docs/workflows.md README.md`
  - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md README.md docs specs skills .codex/skills`
  - `python scripts/build-skills.py --check`
  - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md docs/workflows.md specs/constitution-governance-surface.test.md skills .codex/skills`
  - manual review: `CONSTITUTION.md` is substantive and defines the required source-of-truth order
  - manual review: `AGENTS.md` points to `CONSTITUTION.md` and either reproduces or defers to that order without contradiction
- Expected observable result:
  - contributors find substantive governance at root `CONSTITUTION.md`
  - `AGENTS.md` points to the root constitution without contradicting it
  - canonical and generated skill corpora no longer present `.codex/CONSTITUTION.md` as current authority
  - `.codex/CONSTITUTION.md` is removed as an active tracked governance path
  - any remaining old-path references are historical only
- Commit message: `M1: migrate governance to root constitution`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - stale old-path references may remain in active guidance outside the initially expected file set
  - canonical skill updates may be broader than expected because many skills reference the old path
  - generated `.codex/skills/` may drift if canonical skills are edited without a same-change regeneration
- Rollback/recovery:
  - revert the migration commit as one unit if review finds unacceptable governance drift
  - if only generated output is stale, rerun canonical-to-generated sync before re-review
  - do not reintroduce a shim at `.codex/CONSTITUTION.md` as a partial recovery

## Validation plan

- Treat the skill corpus as the primary migration proof surface:
  - canonical `skills/` must be correct first
  - generated `.codex/skills/` must then be synchronized from those canonical changes
- Use focused path scans for active guidance:
  - `AGENTS.md`
  - `docs/plan.md`
  - this active plan file
  - `docs/workflows.md` only if it names the governance path
- Use repository-wide search only to classify remaining old-path references as historical rather than to force broad rewrites.
- Use manual review to confirm:
  - `CONSTITUTION.md` is substantive and defines the required source-of-truth order
  - `AGENTS.md` points to `CONSTITUTION.md` and either reproduces or defers to that order without contradiction
- Record the exact commands run in `Validation notes`.

## Risks and recovery

- Risk: implementation quietly expands into historical-artifact cleanup unrelated to the contract.
  - Recovery: stop after active guidance and skill surfaces are correct; defer historical cleanup unless a file is still instructing contributors what to read today.
- Risk: `AGENTS.md` and `CONSTITUTION.md` drift on precedence wording.
  - Recovery: prefer explicit defer-or-reproduce behavior in `AGENTS.md`; use manual comparison during validation.
- Risk: the active first-release plan remains stale and keeps teaching the old path or a wrong absence claim.
  - Recovery: keep the active-plan index accurate in `docs/plan.md`; treat completed plans as historical unless they still instruct contributors what to read today.
- Risk: reviewers challenge the lack of a multi-milestone rollout.
  - Recovery: point to `R11`; if the migration must expand beyond one coherent change, stop and replace this plan with a broader milestone plan before further implementation.

## Dependencies

- Internal:
  - reviewed proposal, spec, and test spec for this migration
  - existing generated-skill sync tooling
  - current active plan index in `docs/plan.md`
- External:
  - none

## Progress

- [x] M1. Land the root-constitution governance migration
- 2026-04-20: plan created
- 2026-04-20: M1 implemented. Added root `CONSTITUTION.md`, updated `AGENTS.md` and canonical `skills/`, regenerated `.codex/skills/`, removed `.codex/CONSTITUTION.md`, and aligned active plan surfaces.
- 2026-04-20: M1 code-review follow-up fixed `AGENTS.md` required-reading order so it explicitly follows the constitution without contradiction.
- 2026-04-20: M1 verify passed on the current committed branch state using path checks, focused scans, `python scripts/build-skills.py --check`, and `bash scripts/ci.sh`.

## Decision log

- 2026-04-20: Use one milestone for the migration. Rationale: the spec requires one coherent change and staged partial rollout would create temporary governance drift across active guidance and generated skills.
- 2026-04-20: Treat the active plan currently indexed in `docs/plan.md` as in-scope active guidance when it names the governance path. Rationale: `R9a` makes active guidance a migration target even when the plan is otherwise unrelated to the new initiative.
- 2026-04-20: With the first-release plan moved to `Done`, treat this migration plan as the only active plan surface. Rationale: `docs/plan.md` should not keep completed execution plans under `Active`, and the constitution migration should validate against the normalized active-guidance set.

## Surprises and discoveries

- 2026-04-20: The local constitution draft could not be promoted verbatim because it still asserted `.codex/CONSTITUTION.md` as the governing path and still treated governance documentation as tool-scoped.

## Validation notes

- 2026-04-20:
  - pre-change proof:
    - `! git ls-files --error-unmatch CONSTITUTION.md >/dev/null 2>&1`
    - `rg -n "\\.codex/CONSTITUTION\\.md" AGENTS.md skills`
  - milestone validation:
    - `git ls-files --error-unmatch CONSTITUTION.md`
    - `! git ls-files --error-unmatch .codex/CONSTITUTION.md`
    - `! test -e .codex/CONSTITUTION.md`
    - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills .codex/skills AGENTS.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md docs/workflows.md README.md`
    - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md README.md docs specs skills .codex/skills`
    - `python scripts/build-skills.py --check`
    - `git diff --check -- CONSTITUTION.md AGENTS.md README.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md docs/workflows.md specs/constitution-governance-surface.test.md skills .codex/skills`
  - result: pass
  - manual review:
    - `CONSTITUTION.md` is substantive and defines the required source-of-truth order
    - `AGENTS.md` points to `CONSTITUTION.md` and reproduces an order consistent with it
- 2026-04-20 code-review follow-up:
  - validation:
    - `python scripts/build-skills.py --check`
    - `git diff --check -- AGENTS.md docs/plans/2026-04-20-constitution-governance-migration.md`
  - manual review:
    - `AGENTS.md` required-reading order now defers to `CONSTITUTION.md` and follows the same artifact order for implementation work
  - result: pass
- 2026-04-20 verify:
  - validation:
    - `git ls-files --error-unmatch CONSTITUTION.md`
    - `! git ls-files --error-unmatch .codex/CONSTITUTION.md >/dev/null 2>&1 && ! test -e .codex/CONSTITUTION.md`
    - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md docs/workflows.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md README.md`
    - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills .codex/skills`
    - `rg -n "\\.codex/CONSTITUTION\\.md" AGENTS.md README.md docs specs skills .codex/skills`
    - `python scripts/build-skills.py --check`
    - `git diff --check 8dcc4d3..HEAD`
    - `bash scripts/ci.sh`
  - manual review:
    - `CONSTITUTION.md` remains substantive and ordered
    - `AGENTS.md` continues to defer to the constitution without contradiction
    - remaining `.codex/CONSTITUTION.md` references are historical or proof artifacts only
  - result: pass with concerns limited to hosted CI not yet observed and unrelated untracked files outside the reviewed diff

## Outcome and retrospective

- M1 is complete, verified, and explained. This migration work is done and now belongs in `docs/plan.md` under `Done`.

## Readiness

This plan is done.

It remains a historical record for the constitution-governance migration rather than an active execution plan.

## Historical closeout rationale

Retained from `docs/explain/2026-04-20-constitution-governance-migration.md` when the legacy explanation directory was retired during the 2026-09-07 repository cleanup. The quoted text preserves the original account, commands and paths; it is historical evidence, not current plan state or a fresh verification result. New work uses the owning change’s contract-selected Verify report.

> # Constitution governance migration rationale
>
> ## Summary
>
> This explanation covers the constitution-governance migration branch range `8dcc4d3..a4d1056`.
>
> The change promotes repository-wide governance from an untracked, tool-scoped draft path to tracked root [`CONSTITUTION.md`](../../CONSTITUTION.md), makes [`AGENTS.md`](../../AGENTS.md) a concise operating guide that points upward to that constitution, updates canonical [`skills/`](../../skills) to the new best-practice reference pattern, regenerates tracked [`.codex/skills/`](../../.codex/skills), and normalizes the active plan surfaces in [`docs/plan.md`](../plan.md).
>
> This artifact explains the reviewed M1 migration only. It does not justify the unrelated untracked proposal [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md), which remains outside this diff.
>
> ## Problem
>
> The repository had a governance draft only in local working state at `.codex/CONSTITUTION.md`, which created the wrong signal about ownership and scope:
>
> - the highest-level governance artifact looked Codex-specific instead of repository-wide;
> - `AGENTS.md`, skills, and plan surfaces disagreed about where durable governance lived;
> - canonical [`skills/`](../../skills) and generated [`.codex/skills/`](../../.codex/skills) both carried stale path references;
> - the active plan index still treated the finished first-release plan as active guidance.
>
> If left alone, future contributors would keep learning the wrong source-of-truth model: governance under `.codex/`, active-plan drift in `docs/plan.md`, and adapter-facing paths treated as canonical.
>
> ## Decision trail
>
> | Artifact | Decision carried into the diff | How it shaped the change |
> | --- | --- | --- |
> | [`2026-04-20-constitution-governance-surface.md`](../proposals/2026-04-20-constitution-governance-surface.md) | Root `CONSTITUTION.md` should be the only canonical governance source; no `.codex/CONSTITUTION.md` shim; skills are the primary migration surface. | The diff adds root `CONSTITUTION.md`, removes the old path, updates canonical skills first, and regenerates generated skills from them. |
> | [`constitution-governance-surface.md`](../../specs/constitution-governance-surface.md) | Define the contract in `R1-R12`: substantive root constitution, defer-or-reproduce behavior in `AGENTS.md`, one coherent migration, active-vs-historical boundary, and visible validation evidence. | The diff includes the constitution artifact, `AGENTS.md` alignment, active-plan normalization, skill-path migration, and the validation notes recorded in the plan. |
> | [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md) | Use manual review plus real path scans and `python scripts/build-skills.py --check` instead of synthetic tests. | The implementation relies on real repository proof surfaces rather than adding low-value unit tests for a documentation and path migration. |
> | [`2026-04-19-rigorloop-first-release-repository-architecture.md`](../architecture/2026-04-19-rigorloop-first-release-repository-architecture.md) and [`ADR-20260419-repository-source-layout.md`](../adr/ADR-20260419-repository-source-layout.md) | `skills/` stays canonical, `.codex/skills/` stays generated and must not be hand-edited. | The migration updates canonical skills first and uses the generator to refresh `.codex/skills/` instead of editing generated output directly. |
> | [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Land the migration as one milestone with explicit closeout gates. | The implementation is a single coherent M1 slice, followed by one small review-driven correction commit. |
>
> ## Diff rationale by area
>
> | Area | Files | Change | Reason | Source artifact | Test or evidence |
> | --- | --- | --- | --- | --- | --- |
> | Root governance surface | [`CONSTITUTION.md`](../../CONSTITUTION.md) | Added a tracked, substantive constitution with project purpose, source-of-truth order, governance rules, verification rules, and fast-lane boundaries. | The repository needed a real root governance artifact, not a local draft or redirect. | Proposal decision; spec `R1`, `R1a`, `R1b` | Manual review `T1`; code-review and verify both confirmed it is substantive and ordered. |
> | Concise operational guide | [`AGENTS.md`](../../AGENTS.md) | Repointed `AGENTS.md` to `CONSTITUTION.md`, added the constitution to precedence, and updated required-reading order to defer to the constitution consistently. | `AGENTS.md` needed to become a concise operational guide instead of a conflicting governance surface. | Spec `R3-R5`; test `T3` | Initial code review found a contradiction; follow-up commit `a4d1056` closed that gap. |
> | Canonical skill migration | [`skills/`](../../skills) | Replaced `.codex/CONSTITUTION.md` references with `CONSTITUTION.md` in the canonical skill corpus. | Skills were the primary migration surface, so canonical updates had to happen before any generated refresh. | Proposal skill-first decision; spec `R6-R7` | `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills`; manual review `T4` |
> | Generated compatibility refresh | [`.codex/skills/`](../../.codex/skills) | Regenerated Codex compatibility skills from canonical `skills/` so the generated tree matches the new constitution path. | The architecture forbids direct ownership of generated skill output. | Architecture and ADR; spec `R7-R8`, `R12` | `python scripts/build-skills.py --check`; generated-skill path scan `T5` |
> | Plan lifecycle normalization | [`docs/plan.md`](../plan.md), [`2026-04-19-rigorloop-first-release-implementation.md`](../plans/2026-04-19-rigorloop-first-release-implementation.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Moved the finished first-release plan to `Done`, made the constitution migration the only active plan, and recorded M1 progress, validation, and review follow-up. | Active guidance had to be internally consistent so `R9a` and `T6` could pass. | Migration spec `R9-R12`; plan-review findings | Manual review of active guidance; `docs/plan.md` now indexes only the constitution migration as active. |
> | Migration contract artifacts | [`2026-04-20-constitution-governance-surface.md`](../proposals/2026-04-20-constitution-governance-surface.md), [`constitution-governance-surface.md`](../../specs/constitution-governance-surface.md), [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Added the proposal/spec/test-spec/plan trail that defines and verifies this migration. | This change is governance and compatibility work; the durable reasoning had to be tracked, not left in chat only. | Proposal, spec, test spec, plan | Proposal-review, spec-review, plan-review, code-review, verify |
>
> ## Tests added or changed
>
> No new executable tests were added for this migration. That was intentional and matches the approved test spec.
>
> The proof surface is defined by [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md), which maps the migration to:
>
> - `T1`: manual review that root `CONSTITUTION.md` is substantive and ordered;
> - `T2`: git/path checks proving `.codex/CONSTITUTION.md` is gone as an active governance file;
> - `T3`: manual review that `AGENTS.md` points upward without contradiction;
> - `T4`: canonical skill path scans and spot review;
> - `T5`: generated skill drift check through `python scripts/build-skills.py --check`;
> - `T6`: focused active-guidance review through `docs/plan.md`, `AGENTS.md`, and the active migration plan;
> - `T7`: repository-wide scan showing remaining old-path references are historical only;
> - `T8`: manual diff review confirming this landed as one coherent migration.
>
> This test level is appropriate because the change is about repository-visible governance state, path ownership, and artifact coherence, not new runtime logic.
>
> ## Verification evidence
>
> Verification was run against the current committed M1 state.
>
> Commands run during review and verify:
>
> - `git ls-files --error-unmatch CONSTITUTION.md`
>   - pass
> - `! git ls-files --error-unmatch .codex/CONSTITUTION.md >/dev/null 2>&1 && ! test -e .codex/CONSTITUTION.md`
>   - pass
>   - important output: `old-path-absent`
> - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md docs/workflows.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md README.md`
>   - pass
> - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills .codex/skills`
>   - pass
> - `rg -n "\\.codex/CONSTITUTION\\.md" AGENTS.md README.md docs specs skills .codex/skills`
>   - pass
>   - remaining hits were historical or proof artifacts, not active guidance
> - `python scripts/build-skills.py --check`
>   - pass
>   - important output: generated skills are in sync
> - `git diff --check 8dcc4d3..HEAD`
>   - pass
> - `bash scripts/ci.sh`
>   - pass
>   - validated canonical skills, ran 9 existing skill-validator fixture tests, and rechecked generated drift
>
> CI boundary:
>
> - local repo-owned CI passed through [`scripts/ci.sh`](../../scripts/ci.sh);
> - the hosted workflow at [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) remains the expected thin wrapper;
> - hosted GitHub Actions CI for `c401bf6` and `a4d1056` was not observed from this environment, so this artifact does not claim remote CI passed.
>
> ## Alternatives rejected
>
> These were the meaningful rejected paths for this migration:
>
> - Keep `.codex/CONSTITUTION.md` as the canonical governance file.
>   - Rejected because it keeps the highest-level governance artifact tool-scoped and weakens portability.
> - Keep both `CONSTITUTION.md` and `.codex/CONSTITUTION.md` as long-lived duplicates.
>   - Rejected because it creates two constitutions and invites split-brain drift.
> - Edit `.codex/skills/` directly and backfill canonical `skills/` later.
>   - Rejected because it violates the architecture and ADR boundary that makes `skills/` canonical and `.codex/skills/` generated.
> - Leave the stale first-release plan active in `docs/plan.md`.
>   - Rejected because it makes active guidance ambiguous and breaks the migration’s `R9a` target.
>
> ## Scope control
>
> This change intentionally did not:
>
> - redesign the governance policy beyond what was needed to establish root `CONSTITUTION.md`;
> - rewrite every historical artifact to erase all mention of `.codex/CONSTITUTION.md`;
> - broaden into unrelated CI, release, or workflow-behavior changes;
> - weaken the canonical-versus-generated boundary for skills;
> - pull the separate plan-index lifecycle ownership proposal into this migration.
>
> ## Risks and follow-ups
>
> The migration is verified, but a few follow-up concerns remain visible:
>
> - [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) still says M1 is ready for `code-review`; after verify, that wording is stale.
> - Hosted CI has not been observed yet for the two local migration commits.
> - The working tree still has one unrelated untracked file outside this explained diff:
>   - [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md)
>
> ## PR-ready summary
>
> - Added tracked root `CONSTITUTION.md` as the repository-wide governance source.
> - Reduced `AGENTS.md` to a concise operating guide that points to and defers to the constitution.
> - Updated canonical `skills/` first, then regenerated `.codex/skills/` to preserve the authored-versus-generated boundary.
> - Removed `.codex/CONSTITUTION.md` instead of keeping a compatibility shim.
> - Normalized `docs/plan.md` so the constitution migration is the only active plan and the finished first-release plan is historical.
> - Verified the migration with git path checks, repo path scans, `python scripts/build-skills.py --check`, and `bash scripts/ci.sh`.
