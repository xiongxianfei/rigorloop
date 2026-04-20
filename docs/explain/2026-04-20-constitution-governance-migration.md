# Constitution governance migration rationale

## Summary

This explanation covers the constitution-governance migration branch range `8dcc4d3..a4d1056`.

The change promotes repository-wide governance from an untracked, tool-scoped draft path to tracked root [`CONSTITUTION.md`](../../CONSTITUTION.md), makes [`AGENTS.md`](../../AGENTS.md) a concise operating guide that points upward to that constitution, updates canonical [`skills/`](../../skills) to the new best-practice reference pattern, regenerates tracked [`.codex/skills/`](../../.codex/skills), and normalizes the active plan surfaces in [`docs/plan.md`](../plan.md).

This artifact explains the reviewed M1 migration only. It does not justify the unrelated untracked proposal [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md), which remains outside this diff.

## Problem

The repository had a governance draft only in local working state at `.codex/CONSTITUTION.md`, which created the wrong signal about ownership and scope:

- the highest-level governance artifact looked Codex-specific instead of repository-wide;
- `AGENTS.md`, skills, and plan surfaces disagreed about where durable governance lived;
- canonical [`skills/`](../../skills) and generated [`.codex/skills/`](../../.codex/skills) both carried stale path references;
- the active plan index still treated the finished first-release plan as active guidance.

If left alone, future contributors would keep learning the wrong source-of-truth model: governance under `.codex/`, active-plan drift in `docs/plan.md`, and adapter-facing paths treated as canonical.

## Decision trail

| Artifact | Decision carried into the diff | How it shaped the change |
| --- | --- | --- |
| [`2026-04-20-constitution-governance-surface.md`](../proposals/2026-04-20-constitution-governance-surface.md) | Root `CONSTITUTION.md` should be the only canonical governance source; no `.codex/CONSTITUTION.md` shim; skills are the primary migration surface. | The diff adds root `CONSTITUTION.md`, removes the old path, updates canonical skills first, and regenerates generated skills from them. |
| [`constitution-governance-surface.md`](../../specs/constitution-governance-surface.md) | Define the contract in `R1-R12`: substantive root constitution, defer-or-reproduce behavior in `AGENTS.md`, one coherent migration, active-vs-historical boundary, and visible validation evidence. | The diff includes the constitution artifact, `AGENTS.md` alignment, active-plan normalization, skill-path migration, and the validation notes recorded in the plan. |
| [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md) | Use manual review plus real path scans and `python scripts/build-skills.py --check` instead of synthetic tests. | The implementation relies on real repository proof surfaces rather than adding low-value unit tests for a documentation and path migration. |
| [`2026-04-19-rigorloop-first-release-repository-architecture.md`](../architecture/2026-04-19-rigorloop-first-release-repository-architecture.md) and [`ADR-20260419-repository-source-layout.md`](../adr/ADR-20260419-repository-source-layout.md) | `skills/` stays canonical, `.codex/skills/` stays generated and must not be hand-edited. | The migration updates canonical skills first and uses the generator to refresh `.codex/skills/` instead of editing generated output directly. |
| [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Land the migration as one milestone with explicit closeout gates. | The implementation is a single coherent M1 slice, followed by one small review-driven correction commit. |

## Diff rationale by area

| Area | Files | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- | --- |
| Root governance surface | [`CONSTITUTION.md`](../../CONSTITUTION.md) | Added a tracked, substantive constitution with project purpose, source-of-truth order, governance rules, verification rules, and fast-lane boundaries. | The repository needed a real root governance artifact, not a local draft or redirect. | Proposal decision; spec `R1`, `R1a`, `R1b` | Manual review `T1`; code-review and verify both confirmed it is substantive and ordered. |
| Concise operational guide | [`AGENTS.md`](../../AGENTS.md) | Repointed `AGENTS.md` to `CONSTITUTION.md`, added the constitution to precedence, and updated required-reading order to defer to the constitution consistently. | `AGENTS.md` needed to become a concise operational guide instead of a conflicting governance surface. | Spec `R3-R5`; test `T3` | Initial code review found a contradiction; follow-up commit `a4d1056` closed that gap. |
| Canonical skill migration | [`skills/`](../../skills) | Replaced `.codex/CONSTITUTION.md` references with `CONSTITUTION.md` in the canonical skill corpus. | Skills were the primary migration surface, so canonical updates had to happen before any generated refresh. | Proposal skill-first decision; spec `R6-R7` | `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills`; manual review `T4` |
| Generated compatibility refresh | [`.codex/skills/`](../../.codex/skills) | Regenerated Codex compatibility skills from canonical `skills/` so the generated tree matches the new constitution path. | The architecture forbids direct ownership of generated skill output. | Architecture and ADR; spec `R7-R8`, `R12` | `python scripts/build-skills.py --check`; generated-skill path scan `T5` |
| Plan lifecycle normalization | [`docs/plan.md`](../plan.md), [`2026-04-19-rigorloop-first-release-implementation.md`](../plans/2026-04-19-rigorloop-first-release-implementation.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Moved the finished first-release plan to `Done`, made the constitution migration the only active plan, and recorded M1 progress, validation, and review follow-up. | Active guidance had to be internally consistent so `R9a` and `T6` could pass. | Migration spec `R9-R12`; plan-review findings | Manual review of active guidance; `docs/plan.md` now indexes only the constitution migration as active. |
| Migration contract artifacts | [`2026-04-20-constitution-governance-surface.md`](../proposals/2026-04-20-constitution-governance-surface.md), [`constitution-governance-surface.md`](../../specs/constitution-governance-surface.md), [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md), [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) | Added the proposal/spec/test-spec/plan trail that defines and verifies this migration. | This change is governance and compatibility work; the durable reasoning had to be tracked, not left in chat only. | Proposal, spec, test spec, plan | Proposal-review, spec-review, plan-review, code-review, verify |

## Tests added or changed

No new executable tests were added for this migration. That was intentional and matches the approved test spec.

The proof surface is defined by [`constitution-governance-surface.test.md`](../../specs/constitution-governance-surface.test.md), which maps the migration to:

- `T1`: manual review that root `CONSTITUTION.md` is substantive and ordered;
- `T2`: git/path checks proving `.codex/CONSTITUTION.md` is gone as an active governance file;
- `T3`: manual review that `AGENTS.md` points upward without contradiction;
- `T4`: canonical skill path scans and spot review;
- `T5`: generated skill drift check through `python scripts/build-skills.py --check`;
- `T6`: focused active-guidance review through `docs/plan.md`, `AGENTS.md`, and the active migration plan;
- `T7`: repository-wide scan showing remaining old-path references are historical only;
- `T8`: manual diff review confirming this landed as one coherent migration.

This test level is appropriate because the change is about repository-visible governance state, path ownership, and artifact coherence, not new runtime logic.

## Verification evidence

Verification was run against the current committed M1 state.

Commands run during review and verify:

- `git ls-files --error-unmatch CONSTITUTION.md`
  - pass
- `! git ls-files --error-unmatch .codex/CONSTITUTION.md >/dev/null 2>&1 && ! test -e .codex/CONSTITUTION.md`
  - pass
  - important output: `old-path-absent`
- `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md docs/workflows.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md README.md`
  - pass
- `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills .codex/skills`
  - pass
- `rg -n "\\.codex/CONSTITUTION\\.md" AGENTS.md README.md docs specs skills .codex/skills`
  - pass
  - remaining hits were historical or proof artifacts, not active guidance
- `python scripts/build-skills.py --check`
  - pass
  - important output: generated skills are in sync
- `git diff --check 8dcc4d3..HEAD`
  - pass
- `bash scripts/ci.sh`
  - pass
  - validated canonical skills, ran 9 existing skill-validator fixture tests, and rechecked generated drift

CI boundary:

- local repo-owned CI passed through [`scripts/ci.sh`](../../scripts/ci.sh);
- the hosted workflow at [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) remains the expected thin wrapper;
- hosted GitHub Actions CI for `c401bf6` and `a4d1056` was not observed from this environment, so this artifact does not claim remote CI passed.

## Alternatives rejected

These were the meaningful rejected paths for this migration:

- Keep `.codex/CONSTITUTION.md` as the canonical governance file.
  - Rejected because it keeps the highest-level governance artifact tool-scoped and weakens portability.
- Keep both `CONSTITUTION.md` and `.codex/CONSTITUTION.md` as long-lived duplicates.
  - Rejected because it creates two constitutions and invites split-brain drift.
- Edit `.codex/skills/` directly and backfill canonical `skills/` later.
  - Rejected because it violates the architecture and ADR boundary that makes `skills/` canonical and `.codex/skills/` generated.
- Leave the stale first-release plan active in `docs/plan.md`.
  - Rejected because it makes active guidance ambiguous and breaks the migration’s `R9a` target.

## Scope control

This change intentionally did not:

- redesign the governance policy beyond what was needed to establish root `CONSTITUTION.md`;
- rewrite every historical artifact to erase all mention of `.codex/CONSTITUTION.md`;
- broaden into unrelated CI, release, or workflow-behavior changes;
- weaken the canonical-versus-generated boundary for skills;
- pull the separate plan-index lifecycle ownership proposal into this migration.

## Risks and follow-ups

The migration is verified, but a few follow-up concerns remain visible:

- [`2026-04-20-constitution-governance-migration.md`](../plans/2026-04-20-constitution-governance-migration.md) still says M1 is ready for `code-review`; after verify, that wording is stale.
- Hosted CI has not been observed yet for the two local migration commits.
- The working tree still has one unrelated untracked file outside this explained diff:
  - [`2026-04-20-plan-index-lifecycle-ownership.md`](../proposals/2026-04-20-plan-index-lifecycle-ownership.md)

## PR-ready summary

- Added tracked root `CONSTITUTION.md` as the repository-wide governance source.
- Reduced `AGENTS.md` to a concise operating guide that points to and defers to the constitution.
- Updated canonical `skills/` first, then regenerated `.codex/skills/` to preserve the authored-versus-generated boundary.
- Removed `.codex/CONSTITUTION.md` instead of keeping a compatibility shim.
- Normalized `docs/plan.md` so the constitution migration is the only active plan and the finished first-release plan is historical.
- Verified the migration with git path checks, repo path scans, `python scripts/build-skills.py --check`, and `bash scripts/ci.sh`.
