# Vision Skill Simplification and VISION.md Migration

## Status

- accepted

## Problem

RigorLoop now has a dedicated `vision` skill, but the current design carries two kinds of avoidable complexity.

First, the canonical project-vision artifact is named `vision.md`, while other root-level public or governance documents use uppercase names such as `README.md`, `AGENTS.md`, and `CONSTITUTION.md`. The lowercase path works, but it stands apart from the root-document convention used for the repository's most visible governing files.

Second, the `vision` skill exposes `create`, `revise`, and `mirror` as user-facing modes. Those modes were useful because they protected important safety boundaries: no silent overwrite, bounded README front-matter edits, and explicit handling for substantive vision changes. The cost is that users must choose mode names that are mostly implementation detail, and the skill must explain a small state machine before it can do project-governance work.

The repository should simplify the interface without weakening the safety model. The durable direction is: make `VISION.md` canonical, retire lowercase `vision.md` through an explicit migration, remove user-facing create/revise/mirror modes, and preserve the safety gates those modes were protecting.

## Goals

- Rename the canonical root project-vision artifact from `vision.md` to `VISION.md`.
- Make `VISION.md` the canonical project-vision and proposal-fit reference.
- Remove user-facing `create`, `revise`, and `mirror` modes from the `vision` skill.
- Preserve safe behavior:
  - no silent overwrite of an existing vision;
  - no silent README marker insertion when updating or syncing an existing vision;
  - explicit confirmation before substantive vision changes;
  - README front-matter remains generated from the vision artifact.
- Update proposal and proposal-review guidance to use `VISION.md`.
- Update governance and workflow summaries that name the canonical vision path.
- Update selector routing and focused validator coverage for `VISION.md`.
- Regenerate generated `.codex/skills/` and public adapter output when canonical skill guidance changes.
- Avoid changing the content of the current project vision unless explicitly requested.

## Non-goals

- Rewriting the approved project vision content.
- Turning `vision` into a normal per-change workflow stage.
- Adding a README sync helper script in this proposal.
- Creating a separate `vision-review` skill.
- Rewriting old proposals solely to change `vision.md` references.
- Changing README content outside the vision marker block except when inserting the block during initial vision creation.
- Changing the meaning of proposal, spec, architecture, plan, test-spec, review, verification, or PR artifacts.
- Changing the 500-word cap, required vision sections, drafting heuristics, privacy rules, or research boundaries except where wording must refer to `VISION.md`.

## Vision fit

fits the current vision

This proposal strengthens project identity and reviewability by making the project vision easier to find, easier to reference, and safer to use in proposal review. It does not change the approved vision content.

## Context

The current `vision` skill produces or updates root `vision.md` and README front-matter. It uses explicit `create`, `revise`, and `mirror` modes. Those modes protect real boundaries, but they also make the skill feel like a state machine rather than a simple project-governance tool.

Root repository documents already use uppercase names for public or governance entrypoints:

- `README.md`
- `AGENTS.md`
- `CONSTITUTION.md`

Renaming the project vision artifact to `VISION.md` aligns with that root-document convention.

This is a real source-of-truth migration. It affects:

- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/workflows.md`
- `README.md`
- `VISION.md`
- legacy `vision.md`
- `skills/vision/SKILL.md`
- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `specs/vision-skill.md`
- `specs/vision-skill.test.md`
- selector routing and selector tests
- skill validator coverage
- README marker validation expectations
- generated `.codex/skills/`
- generated public adapters under `dist/adapters/`

## Options considered

### Option 1: Keep `vision.md` and keep explicit modes

Advantages:

- no migration;
- current skill behavior already exists;
- lowest implementation cost.

Disadvantages:

- root naming remains inconsistent;
- mode vocabulary remains heavier than necessary;
- future proposals must keep reasoning about `create`, `revise`, and `mirror`;
- the skill remains harder for contributors to invoke casually.

### Option 2: Rename to `VISION.md` but keep explicit modes

Advantages:

- solves root naming consistency;
- preserves the current safety model.

Disadvantages:

- keeps mode complexity;
- does not simplify the skill;
- still requires users to choose between mode names that are mostly implementation detail.

### Option 3: Keep `vision.md` but simplify the skill

Advantages:

- reduces skill complexity;
- avoids source-of-truth migration.

Disadvantages:

- leaves root naming inconsistency;
- likely creates a second later migration;
- proposal and proposal-review guidance would continue referencing lowercase `vision.md`.

### Option 4: Rename to `VISION.md` and remove user-facing modes

Advantages:

- aligns the root project-vision artifact with root-document naming convention;
- simplifies the skill interface;
- preserves safety through state-based edit rules;
- makes proposals and proposal-review check one canonical artifact path;
- creates a cleaner long-term governance model.

Disadvantages:

- requires coordinated migration;
- requires selector, validator, skill, README, governance, spec, and generated-output updates;
- must avoid leaving both `vision.md` and `VISION.md` as competing canonical files.

## Recommended direction

Choose Option 4.

The repository should make `VISION.md` the canonical project-vision artifact and simplify the `vision` skill by removing user-facing `create`, `revise`, and `mirror` modes. The simplified skill should operate from repository state and user intent instead of explicit mode names.

### Source-of-truth rule

`VISION.md` becomes the canonical project-vision and proposal-fit reference.

Source-of-truth relationship:

1. `CONSTITUTION.md` owns repository governance, source boundaries, and workflow principles.
2. `VISION.md` owns project identity, target users, commitments, refusals, and proposal-fit framing.
3. `specs/` own behavior, workflow, schema, and other durable contracts.
4. Proposals own change-level direction and tradeoff selection.
5. README front-matter mirrors `VISION.md` and is not independently authoritative.

`VISION.md` does not replace specs, proposals, architecture documents, plans, or test specs. If README front-matter conflicts with `VISION.md`, `VISION.md` wins.

### Simplified skill behavior

The skill should no longer expose `create`, `revise`, or `mirror` as user-facing modes.

Instead, it should follow state-based behavior:

| Repository state and user intent | Behavior |
| --- | --- |
| No `VISION.md` exists and the user explicitly asks to establish project vision | Create root `VISION.md`, generate README front-matter, insert README vision markers if missing using deterministic placement, and report assumptions and open questions. |
| No `VISION.md` exists and the user does not ask to establish project vision | Stop and ask whether to create `VISION.md`. |
| `VISION.md` exists and the user asks to update vision | Update only the requested section or clearly related sections; ask or confirm whether the change is `substantive` or `editorial` before finalizing; require a causal link in the change-local pack for substantive changes that are part of a non-trivial change; update README front-matter only inside an existing valid marker block. |
| `VISION.md` exists and the user asks to sync README | Leave `VISION.md` unchanged; update README front-matter only inside an existing valid marker block; report whether README changed or already matched. |
| README markers are missing or malformed during an update or sync | Stop unless the user explicitly authorizes marker insertion or skipping README synchronization. |
| Lowercase `vision.md` exists and uppercase `VISION.md` does not | Treat `vision.md` as a legacy artifact and migrate it to `VISION.md` in the migration change. |
| Both `vision.md` and `VISION.md` exist | Stop, require an owner decision, and do not merge or overwrite automatically. |

After migration, lowercase `vision.md` is not canonical.

### README front-matter rule

README front-matter remains bounded by:

```markdown
<!-- vision:start -->
...
<!-- vision:end -->
```

Generated README front-matter includes only:

- the pitch;
- the differentiator;
- the target audience;
- a link to `VISION.md`.

README marker insertion is automatic only when creating the initial `VISION.md`. When updating an existing `VISION.md` or syncing README from it, missing or malformed markers require explicit handling. The skill should not edit README content outside the marker block except during initial marker insertion.

### Proposal integration

When `VISION.md` exists, every new or substantively revised proposal includes `Vision fit` using the existing allowed values:

- `fits the current vision`
- `may conflict with the current vision`
- `intentionally proposes a vision revision`
- `no vision exists yet`

When no canonical project-vision artifact exists, proposal must use `no vision exists yet`.

A proposal must not claim it fits, conflicts with, or revises a vision when no canonical vision artifact exists. Proposal-review should request revision if `VISION.md` exists and `Vision fit` is missing, if `VISION.md` does not exist and the proposal does not say `no vision exists yet`, or if the proposal silently redefines project vision.

### Migration rules

The migration must not leave two competing canonical vision files.

Valid states:

| State | Meaning |
| --- | --- |
| only `vision.md` exists | legacy state before migration |
| only `VISION.md` exists | valid migrated state |
| both exist | invalid; requires owner decision |
| neither exists | allowed only before project vision is established |

Case-only renames can be unreliable on case-insensitive filesystems. The implementation plan should use a safe Git rename strategy when needed, such as:

```bash
git mv vision.md .vision.tmp
git mv .vision.tmp VISION.md
```

The final branch should not contain both `vision.md` and `VISION.md`.

## Expected behavior changes

- Root project vision is referenced as `VISION.md`.
- The `vision` skill no longer exposes `create`, `revise`, or `mirror` mode names to users.
- The skill remains safe:
  - no silent overwrite;
  - no silent README marker insertion during updates or sync;
  - no unclassified substantive vision changes;
  - no automatic merge between lowercase and uppercase vision files.
- README front-matter links to `VISION.md`.
- Proposals and proposal-review check `VISION.md`.
- Selectors and validators classify `VISION.md` and README marker behavior.
- Generated skills and adapters reflect the new artifact path and simplified skill interface.

## Architecture impact

This is a workflow-governance and source-of-truth migration, not a runtime architecture change.

Affected surfaces:

- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/workflows.md`
- `README.md`
- `VISION.md`
- legacy `vision.md`
- `skills/vision/SKILL.md`
- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `specs/vision-skill.md`
- `specs/vision-skill.test.md`
- selector routing
- selector regression tests
- skill validator tests
- README marker tests
- generated `.codex/skills/`
- generated public adapters under `dist/adapters/`

No service boundary, storage layer, network integration, or deployment architecture changes are expected.

## Testing and verification strategy

Focused proof should cover:

- `VISION.md` is the canonical vision artifact path;
- `vision.md` is no longer referenced as canonical after migration;
- both `vision.md` and `VISION.md` cannot coexist as valid canonical artifacts;
- skill guidance no longer exposes `create`, `revise`, or `mirror` as user-facing modes;
- skill guidance still preserves safe creation, update, and README synchronization behavior;
- proposal requires `Vision fit`;
- proposal-review enforces absent-vision wording;
- README front-matter links to `VISION.md`;
- selector classifies `VISION.md`;
- generated `.codex/skills/` and `dist/adapters/` match canonical skill sources.

Likely checks:

```bash
python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path VISION.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md
bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path README.md --path VISION.md --path skills/vision/SKILL.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md --path specs/vision-skill.md --path specs/vision-skill.test.md
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/test-select-validation.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
git diff --check --
```

If the migration touches change-local artifacts, validation should use selector-selected checks or explicit lifecycle and metadata checks for the touched files.

## Rollout and rollback

Rollout:

1. Accept this proposal.
2. Write a focused spec for the `VISION.md` migration and skill simplification.
3. Update the matching test spec.
4. Plan the migration.
5. Update governance docs, workflow docs, and skill docs.
6. Rename `vision.md` to `VISION.md` if the legacy file exists.
7. Update README links and front-matter.
8. Update proposal and proposal-review guidance.
9. Update selector and validator coverage.
10. Regenerate `.codex/skills/` and public adapters.
11. Run focused validation.
12. Complete code review, verify, explain-change, and PR.

Rollback:

- avoid leaving both `vision.md` and `VISION.md`;
- restore lowercase `vision.md` as the only canonical vision artifact if the migration is reverted;
- update README links and marker-bounded front-matter;
- update proposal and proposal-review guidance;
- update selector routing;
- regenerate generated skill and adapter output;
- rerun validation.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Both `vision.md` and `VISION.md` exist. | Treat coexistence as invalid and require owner decision. |
| Removing modes removes safety. | Preserve safety through state-based behavior and explicit confirmation gates. |
| README marker insertion becomes unsafe. | Allow automatic marker insertion only during initial vision creation. |
| Proposal-review loses vision-fit clarity. | Require explicit `Vision fit` and absent-vision wording. |
| Generated adapters drift. | Regenerate and validate generated outputs. |
| Case-only rename fails on local filesystems. | Use a safe two-step Git rename if needed. |
| Historical references become noisy to update. | Update active governance, skill, spec, README, selector, and generated surfaces; do not rewrite old proposals solely for path text. |

## Open questions

None.

The approved spec resolves the lower-level compatibility questions for legacy mode words, lowercase `vision.md` migration routing, proposal `Vision fit` status values, and both-file coexistence handling. The execution plan owns the remaining implementation sequencing.

## Decision log

- 2026-05-01: Proposed `VISION.md` as the canonical root project-vision artifact for consistency with root governance and public entry files.
- 2026-05-01: Proposed removing user-facing `create`, `revise`, and `mirror` modes from the `vision` skill.
- 2026-05-01: Kept README marker safety and substantive/editorial confirmation as required behavior after removing mode names.
- 2026-05-01: Chose to treat coexistence of `vision.md` and `VISION.md` as invalid.
- 2026-05-01: Scoped this as a separate proposal instead of bundling it into the broader workflow refactor.
- 2026-05-01: Proposal-review approved the direction with no material findings. The proposal is accepted for focused spec work.

## Next artifacts

- `proposal-review`
- focused spec
- focused test spec
- execution plan
- implementation
- generated-output validation
- explain-change

## Follow-on artifacts

- Spec: [Vision Skill Simplification and VISION.md Migration](../../specs/vision-skill-simplification-and-vision-md-migration.md)
- Plan: [2026-05-01 Vision Skill Simplification and VISION.md Migration](../plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)
- Test spec: [Vision Skill Simplification and VISION.md Migration Test Spec](../../specs/vision-skill-simplification-and-vision-md-migration.test.md)

## Readiness

Accepted. The focused spec is approved, the execution plan passed `plan-review`, and the focused test spec is active for implementation.

The proposal resolves the main direction: `VISION.md` becomes the canonical root project-vision artifact, the `vision` skill loses user-facing `create`, `revise`, and `mirror` modes, and safety boundaries are preserved through state-based edit rules.
