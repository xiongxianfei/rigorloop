# Constitution governance migration plan

- Status: active
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
- Current active guidance that names the governance path includes at minimum:
  - `AGENTS.md`
  - the active plan indexed in `docs/plan.md`, currently `docs/plans/2026-04-20-constitution-governance-migration.md`
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

- M1 is complete and verified. It is ready for PR once the branch-scoped explain artifact is committed and unrelated untracked work remains excluded.
