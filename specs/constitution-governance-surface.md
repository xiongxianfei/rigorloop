# Constitution Governance Surface

## Status
- approved

## Related proposal

- [Constitution Governance Surface](../docs/proposals/2026-04-20-constitution-governance-surface.md)

## Goal and context

This spec defines the repository-visible contract for promoting the constitution from a Codex-scoped draft path to a general repository-wide governance artifact.

The goal is not just to move one file. The goal is to make `CONSTITUTION.md` the single canonical governance source, keep `AGENTS.md` concise and operational, and update the skill corpus to follow the new best-practice governance reference pattern before regenerating derived `.codex/skills/` output.

## Glossary

- `constitution`: the highest-priority repository-wide governance artifact.
- `active guidance`: contributor-facing files that are currently operative for this migration and tell contributors or agents what to read or what path is authoritative.
- `historical artifact`: a tracked file that describes prior state, migration rationale, or review history rather than current governing behavior.
- `canonical skill`: an authored skill file under `skills/`.
- `generated skill`: derived Codex compatibility output under `.codex/skills/`.
- `best-practice constitution reference pattern`: skill guidance that treats root `CONSTITUTION.md` as the repository-wide governance source and never presents `.codex/CONSTITUTION.md` as authoritative.

## Examples first

### Example E1: skill-first constitution migration

Given canonical skills under `skills/` currently instruct contributors to read `.codex/CONSTITUTION.md`
When the constitution migration is performed
Then those canonical skills are updated first to point to `CONSTITUTION.md`, and `.codex/skills/` is regenerated from those canonical changes in the same change.

### Example E2: concise AGENTS surface

Given `AGENTS.md` needs to tell contributors where detailed governance lives
When the migration completes
Then `AGENTS.md` identifies `CONSTITUTION.md` as the detailed governance source, uses the same precedence order if it restates one, and stays an operational guide rather than a second full constitution.

### Example E3: historical reference remains allowed

Given an accepted proposal explains that governance originally lived in `.codex/CONSTITUTION.md`
When that proposal remains in the repository for historical context
Then it may still mention `.codex/CONSTITUTION.md` as past state, provided it does not present that path as the current authoritative governance source.

### Example E4: no compatibility shim

Given the migration introduces root `CONSTITUTION.md`
When the same change updates active guidance and regenerated skills
Then `.codex/CONSTITUTION.md` is removed instead of remaining as a redirect or duplicate.

## Requirements

R1. The repository MUST use root `CONSTITUTION.md` as the single canonical repository-wide governance artifact.

R1a. Root `CONSTITUTION.md` MUST define the repository source-of-truth order for governing artifacts. That order MUST place `CONSTITUTION.md` above specs, architecture or ADR guidance, active plans, matching test specs, workflow summaries, and `AGENTS.md`.

R1b. Root `CONSTITUTION.md` MUST contain the substantive repository-wide governance rules that contributors and agents are expected to follow. It MUST NOT be only a redirect, placeholder, or source-of-truth list.

R2. `.codex/CONSTITUTION.md` MUST NOT remain as a tracked active governance file, compatibility shim, or duplicate constitution after the migration completes.

R3. `AGENTS.md` MUST identify `CONSTITUTION.md` as the detailed governance source.

R4. If `AGENTS.md` restates instruction precedence or required-reading order, it MUST either reproduce the ordered list defined in `CONSTITUTION.md` or explicitly defer to `CONSTITUTION.md`, and it MUST NOT contradict that order.

R5. `AGENTS.md` SHOULD remain concise and operational. It MAY summarize repository-specific working rules, but it MUST NOT present a conflicting governance path or conflicting source-of-truth order.

R6. Canonical skill guidance under `skills/` that instructs contributors or agents to read repository-wide governance MUST use the best-practice constitution reference pattern and MUST NOT point to `.codex/CONSTITUTION.md` as the governing path.

R7. The primary migration surface MUST be canonical skills under `skills/`. Constitution-path changes in `.codex/skills/` MUST be produced by regenerating from canonical skill changes in the same change.

R8. Generated `.codex/skills/` output MUST remain derived content and MUST NOT be hand-edited as the authoritative migration surface.

R9. Active contributor-facing guidance that names the constitution path or detailed governance source MUST point to `CONSTITUTION.md`.

R9a. For this migration, active guidance includes at minimum `AGENTS.md`, the active plan file, `docs/workflows.md`, canonical skills under `skills/`, generated skills under `.codex/skills/`, and any other root or `docs/` guidance file that names the constitution path or detailed governance source. Proposals, explain-change artifacts, review notes, ADRs, and superseded plans are historical unless they still instruct contributors what to read today.

R10. Historical artifacts MAY mention `.codex/CONSTITUTION.md` when describing prior state, migration rationale, or review history, but they MUST NOT present it as the current authoritative governance source.

R11. The migration MUST be performed as one coherent change that:
- adds root `CONSTITUTION.md`;
- updates active guidance surfaces that name the constitution path;
- updates canonical `skills/` to the new best-practice constitution reference pattern;
- regenerates `.codex/skills/` from those canonical changes; and
- removes `.codex/CONSTITUTION.md`.

R12. The migration MUST be verifiable through contributor-visible evidence showing all of the following:
- no canonical skill file under `skills/` still points to `.codex/CONSTITUTION.md` as the governing path;
- no generated skill file under `.codex/skills/` still points to `.codex/CONSTITUTION.md` as the governing path;
- no active guidance file still presents `.codex/CONSTITUTION.md` as the current authoritative constitution path; and
- generated `.codex/skills/` output is in sync with canonical `skills/`.

## Inputs and outputs

### Inputs

- the current governance draft content
- `AGENTS.md`
- canonical skills under `skills/`
- generated skills under `.codex/skills/`
- active contributor-facing guidance that names the constitution path
- historical artifacts that may reference the prior path

### Outputs

- root `CONSTITUTION.md` as the canonical governance artifact
- a concise `AGENTS.md` that points to the constitution
- canonical `skills/` updated to the new constitution reference pattern
- regenerated `.codex/skills/` that matches canonical skills
- removal of `.codex/CONSTITUTION.md`

## State and invariants

- There is exactly one active canonical constitution path: `CONSTITUTION.md`.
- Canonical skills under `skills/` remain the authored source of truth.
- Generated `.codex/skills/` remains derived output.
- Active guidance may describe only the root constitution path as authoritative.
- Historical artifacts may preserve old-path references only as historical context.

## Error and boundary behavior

- If both `CONSTITUTION.md` and `.codex/CONSTITUTION.md` are presented as current governance sources, the migration is incomplete.
- If canonical `skills/` are updated but generated `.codex/skills/` is not regenerated, the migration is incomplete.
- If a historical artifact still mentions `.codex/CONSTITUTION.md`, that is acceptable only when the file clearly describes prior state rather than current authoritative behavior.
- If an active guidance file still points to `.codex/CONSTITUTION.md`, the migration is incomplete even if root `CONSTITUTION.md` exists.
- Skills that do not instruct contributors or agents to consult repository-wide governance are not required to add new constitution references solely because of this migration.

## Compatibility and migration

- The migration is compatibility-sensitive because it changes contributor-visible governance paths and reading order.
- The migration MUST happen in one reviewable change rather than a long-lived split across multiple active governance paths.
- Historical files MAY preserve old-path references when they are clearly archival or explanatory.
- Rollback, if required, is a full reversal of the migration rather than a long-lived dual-path compatibility state.

## Observability

- Contributors MUST be able to verify the migration through repository-visible path scans and the normal generated-skill sync or drift-check surface.
- Manual review MUST be able to confirm that `AGENTS.md` and `CONSTITUTION.md` use a consistent source-of-truth order.
- Manual review MUST treat canonical `skills/` as the primary verification surface before checking regenerated `.codex/skills/`.

## Security and privacy

- The migration MUST NOT introduce machine-local paths, host-specific workarounds, or tool-specific governance ownership claims outside the approved root constitution model.
- The migration MUST NOT weaken the existing canonical-versus-generated ownership boundary for skills.

## Performance expectations

- No special runtime-performance target is defined for this migration.
- Repository-scale validation for path scans and generated-skill sync MUST remain practical for normal contributor workflows.

## Edge cases

EC1. A closed proposal or review note may mention `.codex/CONSTITUTION.md` as the old path without violating the spec if it is clearly historical.

EC2. A skill that previously referenced repository governance must update to the root constitution path even if no other part of that skill changes.

EC3. A skill that never referenced repository governance does not need a new constitution reference solely to satisfy this migration.

EC4. If `AGENTS.md` does not restate full precedence, it still satisfies the spec as long as it points to `CONSTITUTION.md` and does not conflict with it.

EC5. A regeneration-only change in `.codex/skills/` is insufficient if the canonical `skills/` source was not updated first.

## Non-goals

- Rewriting the substantive governance policy beyond what is required to establish the root constitution path.
- Redesigning skill behavior beyond updating constitution-reference guidance.
- Forcing every tracked document to mention `CONSTITUTION.md` when it does not name the governance source today.
- Preserving `.codex/CONSTITUTION.md` as a redirect, duplicate, or long-lived compatibility shim.

## Acceptance criteria

- A tracked root `CONSTITUTION.md` exists, is presented as the canonical governance source, defines the repository source-of-truth order, and contains the substantive repository-wide governance rules.
- `.codex/CONSTITUTION.md` is removed from the active repository surface.
- `AGENTS.md` points to `CONSTITUTION.md` and does not conflict with its precedence model.
- Canonical `skills/` follow the new best-practice constitution reference pattern.
- Generated `.codex/skills/` is regenerated from canonical skills and no longer points to `.codex/CONSTITUTION.md`.
- Active guidance that names the constitution path now uses `CONSTITUTION.md`.
- Historical artifacts, if they mention `.codex/CONSTITUTION.md`, do so only as prior state.

## Open questions

None.
