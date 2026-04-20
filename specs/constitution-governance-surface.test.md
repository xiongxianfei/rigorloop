# Constitution Governance Surface Test Spec

## Status

- complete

## Related spec and plan

- Spec: `specs/constitution-governance-surface.md`
- Related proposal: `docs/proposals/2026-04-20-constitution-governance-surface.md`
- Plan: `docs/plans/2026-04-20-constitution-governance-migration.md`
- Related governance surfaces:
  - `AGENTS.md`
  - `.codex/CONSTITUTION.md`
  - `docs/workflows.md`
  - `docs/plan.md`
  - the plan file currently indexed as active in `docs/plan.md`
  - `skills/`
  - `.codex/skills/`

## Testing strategy

- Use manual contract review for root governance content, `AGENTS.md` behavior, active-versus-historical scope, and one-change migration shape.
- Use the dedicated execution plan to define the named validation commands, active-guidance review surface, and one-milestone migration shape for implementation.
- Use repository path scans to prove that active guidance and skill surfaces no longer present `.codex/CONSTITUTION.md` as the current governing path.
- Use git-tracked-path checks to prove root `CONSTITUTION.md` exists as the tracked canonical artifact and `.codex/CONSTITUTION.md` no longer exists as a tracked active file.
- Use the existing generated-skill sync surface with `python scripts/build-skills.py --check` to prove generated `.codex/skills/` remains in sync with canonical `skills/`.
- Prefer real repository files and real git state over mocks, snapshots, or synthetic adapters.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b` | `T1` | manual | Root constitution exists, is substantive, and defines the governing order |
| `R2` | `T2` | integration, manual | Old path is removed as a tracked active governance file |
| `R3`, `R4`, `R5` | `T3` | manual | `AGENTS.md` points upward, stays operational, and does not contradict the constitution |
| `R6` | `T4` | integration, manual | Canonical skills use the best-practice root constitution reference pattern |
| `R7`, `R8` | `T5`, `T8` | integration, manual | Generated skills are regenerated from canonical changes and stay derived |
| `R9`, `R9a` | `T6` | integration, manual | Active guidance surfaces are updated and in-scope files are reviewed explicitly |
| `R10` | `T7` | manual | Historical artifacts may retain the old path only as history |
| `R11` | `T8` | manual | Migration lands as one coherent change |
| `R12` | `T5`, `T6`, `T8` | integration, manual | Verification evidence covers active guidance, skill surfaces, and generated sync |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T5`, `T8` | Canonical skills update first, generated skills regenerate from them, and the change is reviewable as one migration |
| `E2` | `T3` | `AGENTS.md` becomes concise and either reproduces or defers to the constitution order |
| `E3` | `T7` | Historical references to `.codex/CONSTITUTION.md` remain allowed only as prior-state context |
| `E4` | `T2`, `T8` | No compatibility shim or duplicate constitution remains after the migration |

## Edge case coverage

- A tracked historical artifact may keep `.codex/CONSTITUTION.md` only if it is clearly describing prior state: `T7`
- A skill that previously referenced repository governance must update even if no other content in that skill changes: `T4`
- A skill that never referenced repository governance does not need a new constitution reference solely for this migration: `T4`
- `AGENTS.md` may defer to `CONSTITUTION.md` instead of restating the full order, but if it restates one it must match: `T3`
- A regeneration-only `.codex/skills/` edit is insufficient if canonical `skills/` were not the primary migration surface: `T8`
- The active plan currently indexed in `docs/plan.md` is part of active guidance review if it names the governance path or detailed governance source: `T6`

## Test cases

### T1. Root constitution is canonical, substantive, and ordered

- Covers: `R1`, `R1a`, `R1b`
- Level: manual
- Fixture/setup:
  - `CONSTITUTION.md`
- Steps:
  - Confirm `CONSTITUTION.md` exists at the repository root.
  - Review `CONSTITUTION.md` and confirm it contains substantive repository-wide governance rules rather than only a redirect or placeholder.
  - Confirm it defines the repository source-of-truth order.
  - Confirm that order places `CONSTITUTION.md` above specs, architecture or ADR guidance, active plans, matching test specs, workflow summaries, and `AGENTS.md`.
- Expected result:
  - Root `CONSTITUTION.md` is the real governing artifact, not just a renamed pointer.
- Failure proves:
  - The migration changed the path without establishing the intended governance surface.
- Automation location:
  - Manual review of `CONSTITUTION.md`

### T2. Old constitution path is removed as an active tracked governance file

- Covers: `R2`, `E4`
- Level: integration
- Fixture/setup:
  - git index
  - `CONSTITUTION.md`
  - `.codex/CONSTITUTION.md`
- Steps:
  - Run `git ls-files --error-unmatch CONSTITUTION.md`.
  - Run `git ls-files --error-unmatch .codex/CONSTITUTION.md` and confirm it fails.
  - Confirm no tracked redirect or duplicate constitution remains under `.codex/`.
- Expected result:
  - Root `CONSTITUTION.md` is tracked and `.codex/CONSTITUTION.md` is not tracked as an active governance file.
- Failure proves:
  - The migration left a shim, duplicate, or stale tracked path in place.
- Automation location:
  - direct git path checks during migration verification

### T3. AGENTS.md points to or defers to the root constitution without contradiction

- Covers: `R3`, `R4`, `R5`, `E2`, `EC4`
- Level: manual
- Fixture/setup:
  - `AGENTS.md`
  - `CONSTITUTION.md`
- Steps:
  - Review `AGENTS.md`.
  - Confirm it identifies `CONSTITUTION.md` as the detailed governance source.
  - If `AGENTS.md` restates instruction precedence or required reading, confirm it either reproduces the ordered list from `CONSTITUTION.md` or explicitly defers to it.
  - Confirm `AGENTS.md` does not point to `.codex/CONSTITUTION.md` or present a conflicting order.
  - Confirm `AGENTS.md` remains an operational guide rather than a second full constitution.
- Expected result:
  - `AGENTS.md` stays concise, points upward, and does not compete with the constitution.
- Failure proves:
  - Contributors could still get conflicting governance from `AGENTS.md`.
- Automation location:
  - Manual review of `AGENTS.md`

### T4. Canonical skills use the best-practice root constitution reference pattern

- Covers: `R6`, `E1`, `EC2`, `EC3`
- Level: integration, manual
- Fixture/setup:
  - canonical skills under `skills/`
- Steps:
  - Run `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" skills`.
  - Confirm no canonical skill still points to `.codex/CONSTITUTION.md`.
  - Review the skills that mention constitution guidance and confirm they use root `CONSTITUTION.md` as the governing path.
  - Confirm skills that do not mention repository-wide governance are not forced to add new constitution references solely for this migration.
- Expected result:
  - Canonical skills that discuss repository governance follow the new best-practice root-constitution pattern.
- Failure proves:
  - The primary migration surface was not actually migrated or was migrated inconsistently.
- Automation location:
  - repository path scan plus manual review of matching canonical skills

### T5. Generated skills are regenerated and in sync with canonical skills

- Covers: `R7`, `R8`, `R12`, `E1`, `EC5`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - `scripts/build-skills.py`
- Steps:
  - Run `python scripts/build-skills.py --check`.
  - Run `rg -n "\\.codex/CONSTITUTION\\.md" .codex/skills`.
  - Confirm the drift check passes and generated skills no longer point to `.codex/CONSTITUTION.md`.
- Expected result:
  - Generated skills are synchronized with canonical skills and reflect the migrated root constitution path.
- Failure proves:
  - Generated output was not regenerated from canonical changes or still carries stale governance references.
- Automation location:
  - `python scripts/build-skills.py --check` plus generated-skill path scan

### T6. All in-scope active guidance surfaces are migrated

- Covers: `R9`, `R9a`, `R12`
- Level: integration, manual
- Fixture/setup:
  - `AGENTS.md`
  - `docs/workflows.md`
  - `docs/plan.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
  - root guidance files that mention the constitution path or detailed governance source
- Steps:
  - Review `docs/plan.md` and confirm `docs/plans/2026-04-20-constitution-governance-migration.md` is the active plan indexed for this migration.
  - Run a focused scan such as:
    - `rg -n "\\.codex/CONSTITUTION\\.md|CONSTITUTION\\.md" AGENTS.md docs/workflows.md docs/plan.md docs/plans/2026-04-20-constitution-governance-migration.md README.md`
  - Review matching active-guidance files and confirm any current governance-path reference points to `CONSTITUTION.md`.
  - Confirm no active guidance file still presents `.codex/CONSTITUTION.md` as current authority.
- Expected result:
  - The in-scope active guidance set is migrated coherently, not partially.
- Failure proves:
  - Contributors could still learn the wrong governance path from an active repo surface.
- Automation location:
  - focused repo path scan plus manual review of active-guidance hits

### T7. Historical artifacts keep old-path references only as history

- Covers: `R10`, `E3`, `EC1`
- Level: manual
- Fixture/setup:
  - proposals
  - explain-change artifacts
  - review notes
  - ADRs
  - superseded plans, when present
- Steps:
  - Run a repository-wide scan for `.codex/CONSTITUTION.md`.
  - Inspect remaining matches outside the active-guidance set.
  - Confirm each remaining match is clearly historical, explanatory, or review-related rather than instructing contributors what to read today.
- Expected result:
  - Old-path references remain only where they describe prior state or review history.
- Failure proves:
  - The migration erased useful history or left stale active instructions in the wrong places.
- Automation location:
  - repository-wide search plus manual review of out-of-scope matches

### T8. The migration lands as one coherent reviewable change

- Covers: `R7`, `R11`, `R12`, `E1`, `E4`
- Level: manual
- Fixture/setup:
  - migration branch or PR diff
- Steps:
  - Review the change set.
  - Confirm the same change adds root `CONSTITUTION.md`, updates canonical `skills/`, regenerates `.codex/skills/`, updates in-scope active guidance, and removes `.codex/CONSTITUTION.md`.
  - Confirm the change does not rely on a long-lived compatibility shim or a later cleanup PR to become correct.
- Expected result:
  - Reviewers can approve one coherent migration without guessing what a later cleanup will fix.
- Failure proves:
  - The migration is split in a way that creates temporary governance drift or breaks the canonical-versus-generated contract.
- Automation location:
  - manual diff review in code review or PR review

## Fixtures and data

- Real repository files only:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `docs/plan.md`
  - `docs/plans/2026-04-20-constitution-governance-migration.md`
  - canonical skills under `skills/`
  - generated skills under `.codex/skills/`
  - historical artifact samples that still mention `.codex/CONSTITUTION.md`
- Command surfaces:
  - `git ls-files --error-unmatch ...`
  - `rg -n ...`
  - `python scripts/build-skills.py --check`

## Mocking/stubbing policy

- Do not mock repository files, git state, or generated-skill output.
- Do not rely on snapshots as the primary proof.
- Use real path scans, real tracked-file checks, and the real generated-skill drift check.

## Migration or compatibility tests

- `T2` verifies that the old tracked constitution path is removed rather than shimmed.
- `T6` verifies that active guidance is migrated coherently.
- `T7` verifies that historical references remain allowed only as history.
- `T8` verifies that the migration lands as one coherent compatibility-sensitive change.

## Observability verification

- Use focused path scans to make remaining governance-path references reviewable.
- Use `python scripts/build-skills.py --check` as the generated-output observability surface.
- Use manual review of `CONSTITUTION.md` and `AGENTS.md` to confirm the ordered governance model is visible to contributors.

## Security/privacy verification

- Review the migration diff for machine-local paths, host-specific command workarounds, or debug artifacts.
- Confirm the migration does not weaken the canonical-versus-generated ownership boundary by hand-editing `.codex/skills/` as if it were authoritative.

## Performance checks

- No dedicated performance benchmark is required for this migration.
- The required proof surfaces are limited to repository path scans, git path checks, and the existing generated-skill drift check, which should stay practical for normal contributor workflows.

## Manual QA checklist

- [ ] `CONSTITUTION.md` reads as the substantive governing document, not as a redirect.
- [ ] `CONSTITUTION.md` defines the source-of-truth order with root constitution above the required artifact classes.
- [ ] `AGENTS.md` points to `CONSTITUTION.md` and either reproduces or defers to its order.
- [ ] Canonical `skills/` no longer point to `.codex/CONSTITUTION.md`.
- [ ] Generated `.codex/skills/` is in sync and no longer points to `.codex/CONSTITUTION.md`.
- [ ] The active plan currently indexed in `docs/plan.md` does not present the old path as current authority.
- [ ] Any remaining `.codex/CONSTITUTION.md` references are clearly historical.
- [ ] `.codex/CONSTITUTION.md` is not left behind as a tracked active governance file.

## What not to test

- Do not test unrelated workflow behavior, CI policy, or release automation changes beyond the generated-skill sync surface used by this migration.
- Do not require every historical artifact to be rewritten to remove all mention of `.codex/CONSTITUTION.md`.
- Do not test exact prose wording in the constitution or `AGENTS.md` beyond the observable contract defined in the spec.
- Do not add UI, network, or external-service tests; this migration is repository-structure and guidance behavior only.

## Uncovered gaps

- No uncovered contract gaps remain for the current one-milestone migration shape.
- If implementation expands beyond one coherent change or broadens into unrelated governance cleanup, return to `plan` or `spec` before `implement`.

## Readiness

This test spec is complete. Its coverage now describes the merged governance migration baseline.

No further implementation-stage action is pending for this artifact.
