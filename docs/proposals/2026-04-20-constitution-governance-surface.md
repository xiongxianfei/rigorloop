# Constitution Governance Surface

## Status
- accepted

## Problem

RigorLoop now has a draft constitution, but it exists only in local working state at `.codex/CONSTITUTION.md`, which makes the highest-level governance artifact look tool-specific rather than repository-wide.

That creates three problems:

- the constitution is less general and less discoverable than a root-level `CONSTITUTION.md`;
- `AGENTS.md` currently mixes concise operating guidance with source-of-truth rules that should instead point upward to the constitution;
- the repository already has governance drift, because skills, docs, and the active plan disagree about whether `.codex/CONSTITUTION.md` exists and whether it is authoritative.

If this remains unresolved, future agents and contributors will keep learning the wrong lesson: that durable project governance belongs inside one adapter-specific directory instead of at the repository root.

## Goals

- Make the constitution a repository-wide artifact, not a Codex-scoped artifact.
- Keep `AGENTS.md` simple, precise, and subordinate to the constitution.
- Define one clear source-of-truth order for governance artifacts.
- Update canonical skill guidance to follow the constitution best practice first, then regenerate derived skill output.
- Remove path drift across skills, docs, plans, and contributor guidance.
- Keep the governance model general enough to work beyond one agent runtime.

## Non-goals

- Rewriting the substantive governance rules in this proposal.
- Expanding the constitution into a tutorial or feature plan.
- Changing the approved workflow contract in `specs/rigorloop-workflow.md`.
- Redesigning skill behavior beyond updating constitution references.
- Creating two long-lived constitution sources.

## Context

- A draft constitution currently exists only in local working state at `.codex/CONSTITUTION.md`; this proposal decides the canonical repository path before that governance is formalized.
- `AGENTS.md` currently points to `.codex/CONSTITUTION.md` as the detailed governance source.
- Many skill files under both `skills/` and `.codex/skills/` explicitly reference `.codex/CONSTITUTION.md`.
- `docs/plans/2026-04-19-rigorloop-first-release-implementation.md` still says there is no `.codex/CONSTITUTION.md`, which is already stale.
- The repository has already adopted the pattern “root-level practical guide plus one canonical higher-order artifact” for other concerns:
  - `AGENTS.md` plus `docs/workflows.md`
  - top-level workflow specs plus change-local wrapper artifacts
- The user direction is explicit:
  - move the constitution from `.codex/CONSTITUTION.md` to `CONSTITUTION.md`
  - keep `AGENTS.md` concise and precise, pointing to the constitution instead of duplicating it

## Options considered

### Option 1: Keep `.codex/CONSTITUTION.md` as the canonical constitution

- Advantages:
  - smallest immediate change
  - no need to update existing skill references
  - preserves current local layout
- Disadvantages:
  - keeps the highest-level governance artifact tool-scoped
  - weakens portability beyond Codex
  - continues the wrong architectural signal that governance belongs under `.codex/`

### Option 2: Create a root `CONSTITUTION.md` but keep `.codex/CONSTITUTION.md` as a full duplicate

- Advantages:
  - easy migration path for current references
  - root-level discoverability improves immediately
- Disadvantages:
  - creates two governance sources
  - invites drift between duplicate files
  - makes review and precedence weaker instead of stronger

### Option 3: Move to root `CONSTITUTION.md` as the only canonical constitution and reduce `AGENTS.md` to a concise pointer plus operating rules

- Advantages:
  - makes governance general and tool-agnostic
  - matches the user goal directly
  - preserves one clear source of truth
  - keeps `AGENTS.md` short and practical
  - aligns better with future non-Codex adapters or contributor tooling
- Disadvantages:
  - requires a broad path-reference cleanup across skills, docs, and plans
  - may briefly break repository-local expectations if the move and reference updates are split across changes

### Option 4: Keep the constitution in `.codex/` and make `AGENTS.md` the only general governance file

- Advantages:
  - avoids a root `CONSTITUTION.md`
  - reduces the number of governance files
- Disadvantages:
  - overloads `AGENTS.md` again
  - weakens the separation between concise operating guidance and durable governance
  - makes future governance growth harder to manage cleanly

## Recommended direction

Choose Option 3.

RigorLoop should promote the constitution to a root-level `CONSTITUTION.md` and treat that file as the single canonical governance source.

`AGENTS.md` should stay deliberately short. It should:

- point to `CONSTITUTION.md`;
- summarize the repository-specific operating rules agents need most often;
- use the same source-of-truth order as the constitution;
- avoid restating the full governance body unless a short reminder is necessary for daily work.

This change should be done as one coherent governance migration, not as a partial move. The repository should update all tracked references from `.codex/CONSTITUTION.md` to `CONSTITUTION.md` in the same change, including skills, plans, and docs, so the move does not create a temporary split-brain governance surface.

The most important migration surface is the skill corpus. Success is not just moving the constitution file; it is making canonical `skills/` follow the new best-practice constitution reference pattern and then regenerating `.codex/skills/` from that canonical update.

Reference updates MUST be made in canonical `skills/` first, and any generated `.codex/skills/` output MUST be regenerated from those canonical changes in the same migration.

Do not keep a compatibility shim. Remove `.codex/CONSTITUTION.md` in the same change after tracked references are updated.

## Expected behavior changes

- Contributors and agents will find the highest-level governance artifact at `CONSTITUTION.md`.
- `AGENTS.md` will become a concise operating guide instead of a partial governance duplicate.
- Skills and docs will read `CONSTITUTION.md` as the repository-wide governance source.
- Canonical skill instructions will be updated to use the new constitution best practice, and generated skill output will be regenerated from those canonical changes.
- Governance precedence will become easier to explain: user request, constitution, specs, architecture, plans, tests, workflows, then `AGENTS.md`.
- Tool-specific directories such as `.codex/` will no longer appear to own repository-wide governance.

## Architecture impact

The change affects governance layout and reference paths rather than runtime code.

- Primary components affected:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - skill files under `skills/` and `.codex/skills/`
  - plans or docs that reference the constitution path
- Boundary decisions:
  - repository-wide governance belongs at the root
  - concise agent operating guidance stays in `AGENTS.md`
  - adapter-specific directories do not own universal governance
- Expected migration shape:
  - move substantive constitution content to `CONSTITUTION.md`
  - simplify `AGENTS.md` so it points upward
  - update constitution path references everywhere in one change
  - remove the `.codex/CONSTITUTION.md` canonical role

## Testing and verification strategy

- Manual review that `AGENTS.md` is shorter and still useful.
- Repository-wide path scan proving no tracked files still depend on `.codex/CONSTITUTION.md` as the canonical path.
- Treat canonical skill updates as the primary verification surface: review that all tracked `skills/` references follow the new best-practice constitution pattern before regenerating `.codex/skills/`.
- Verify that no tracked canonical or generated skill file still points to `.codex/CONSTITUTION.md` as the governing path.
- Manual review that source-of-truth order is consistent between `CONSTITUTION.md` and `AGENTS.md`.
- If skills or docs are updated, run the repository’s normal structural validation to ensure no unrelated drift is introduced.

## Rollout and rollback

Rollout should be one small governance-focused change:

- update canonical `skills/` to the new constitution best practice;
- review that canonical skill migration as the primary surface;
- regenerate `.codex/skills/`;
- update remaining docs and guidance;
- add `CONSTITUTION.md` at the repository root;
- reduce `AGENTS.md` to concise operating guidance;
- remove `.codex/CONSTITUTION.md`.

Rollback is simple:

- restore `.codex/CONSTITUTION.md` as the canonical location;
- point `AGENTS.md` and skills back to it;
- remove root `CONSTITUTION.md`.

## Risks and mitigations

- Risk: the move leaves stale references across skills and docs.
  - Mitigation: treat the change as a full path migration and verify with repository-wide search.
- Risk: `AGENTS.md` becomes too thin and stops being useful in daily work.
  - Mitigation: keep concise operating rules in `AGENTS.md`, but push durable governance detail into `CONSTITUTION.md`.
- Risk: the repo temporarily has two constitutions.
  - Mitigation: remove `.codex/CONSTITUTION.md` in the same migration after tracked references are updated.
- Risk: existing plans or review artifacts become historically inaccurate.
  - Mitigation: update only the currently active guidance surfaces and note historical path changes where needed instead of rewriting old context indiscriminately.

## Open questions

- Should `docs/workflows.md` explicitly mention `CONSTITUTION.md`, or is it enough for `AGENTS.md` and the skills to point there?

This question does not block writing the spec because the core directional decision is already clear.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-20 | Repository-wide governance should live at root `CONSTITUTION.md`. | Root placement is more general, discoverable, and tool-agnostic than `.codex/CONSTITUTION.md`. | Keeping governance canonical inside `.codex/` weakens portability and clarity. |
| 2026-04-20 | `AGENTS.md` should remain concise and point to the constitution instead of duplicating it. | This keeps daily operating guidance short while preserving one durable governance source. | Making `AGENTS.md` the full governance file would overload it again. |
| 2026-04-20 | Constitution-path updates should be performed as one coherent migration. | Partial updates would create reference drift and split-brain governance. | Keeping both paths live long-term would create ambiguity and drift. |
| 2026-04-20 | Update constitution references in canonical `skills/` first, then regenerate `.codex/skills/` in the same change. | This preserves the repository's canonical-versus-generated ownership model during the migration. | Editing generated skill output directly would break the established source-of-truth boundary. |
| 2026-04-20 | Do not keep a compatibility shim at `.codex/CONSTITUTION.md`. | Removing the old path in the same change avoids duplicate governance surfaces and long-lived ambiguity. | A temporary redirect file would weaken the “single canonical constitution” goal. |

## Follow-on artifacts

- `specs/constitution-governance-surface.md`
- `specs/constitution-governance-surface.test.md`
- `docs/plans/2026-04-20-constitution-governance-migration.md`
- `docs/explain/2026-04-20-constitution-governance-migration.md`

## Readiness

Proposal review is complete. This proposal was accepted and its migration is now part of the merged repository baseline.

No further proposal-stage action is pending for this artifact.
