# Vision Skill Simplification and VISION.md Migration

## Status

- approved

## Related proposal

- [Vision Skill Simplification and VISION.md Migration](../docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)

## Goal and context

This spec defines the contract for migrating the canonical project-vision artifact from root `vision.md` to root `VISION.md` and simplifying the `vision` skill from explicit user-facing modes to state-based behavior. It preserves the existing safety guarantees around overwrite protection, substantive vision changes, README marker boundaries, proposal `Vision fit`, and generated skill or adapter output.

This spec is focused on the `VISION.md` migration and vision-skill interface. It does not change the approved project vision content or make `vision` part of the normal per-change lifecycle.

When approved, this spec supersedes the mode and lowercase-path portions of [specs/vision-skill.md](vision-skill.md). The implementation must update the active vision contract surfaces so no approved spec, active test spec, or canonical skill continues to require the old lowercase-path or user-facing mode model. Existing requirements in `specs/vision-skill.md` that govern vision content quality, privacy, research boundaries, drafting heuristics, workflow fit, generated-output ownership, and README marker safety remain in force unless this spec explicitly replaces their path or mode wording.

## Glossary

- `VISION.md`: the canonical project-vision document at the repository root after migration.
- `vision.md`: the legacy lowercase root project-vision path before migration.
- canonical vision artifact: the single root file that governs project identity, target users, commitments, refusals, and proposal-fit framing.
- README front-matter: the README section between `<!-- vision:start -->` and `<!-- vision:end -->`, generated from the canonical vision artifact.
- marker pair: the exact `<!-- vision:start -->` and `<!-- vision:end -->` comments that bound generated README front-matter.
- state-based behavior: `vision` skill behavior determined by repository state and user intent, not by explicit `create`, `revise`, or `mirror` modes.
- establish project vision: create the initial canonical vision artifact.
- update vision: change canonical project-vision content.
- sync README: regenerate README front-matter from the canonical vision artifact without changing the artifact.
- substantive vision change: a project-meaning change caused by a proposal, incident, learning, or project-direction drift.
- editorial vision change: a typo, wording cleanup, or formatting-only change that does not change project meaning.
- legacy mode words: old invocation words such as `create`, `revise`, and `mirror` that may appear in user requests but are no longer user-facing operating modes.
- coexistence: a repository state where both root `vision.md` and root `VISION.md` exist.
- `Vision fit`: a proposal section that states how the proposed direction relates to the canonical vision artifact.

## Examples first

### Example E1: migration creates one canonical uppercase vision

Given root `vision.md` exists
And root `VISION.md` does not exist
When the migration is implemented
Then the repository has root `VISION.md`
And root `vision.md` is absent
And the project vision content is unchanged except for path-sensitive links or generated front-matter.

### Example E2: both vision paths exist

Given root `vision.md` exists
And root `VISION.md` exists
When the `vision` skill or repository validation evaluates the state
Then the state is invalid
And no automatic merge or overwrite happens
And an owner decision is required.

### Example E3: establish project vision without mode names

Given neither `VISION.md` nor `vision.md` exists
When the user explicitly asks to establish the project vision
Then the `vision` skill creates root `VISION.md`
And inserts deterministic README front-matter markers when needed
And reports assumptions and open vision-level questions.

### Example E4: missing canonical vision without establishment intent

Given no canonical vision artifact exists
When the user invokes the `vision` skill without asking to establish project vision
Then the skill stops
And asks whether to create `VISION.md`
And does not edit README.

### Example E5: existing vision update is explicit and bounded

Given root `VISION.md` exists
When the user asks to update one vision section
Then the skill updates only the requested section or clearly related sections
And asks or confirms whether the change is `substantive` or `editorial` before finalizing
And updates README front-matter only inside an existing valid marker block.

### Example E6: substantive update needs traceability

Given root `VISION.md` exists
And a substantive vision update is part of a non-trivial change with a change-local pack
When the causal link is missing from the required change-local artifacts
Then the skill stops before finalizing
And reports the missing traceability record.

### Example E7: README sync leaves vision unchanged

Given root `VISION.md` exists
And README contains one valid marker pair
When the user asks to sync README
Then `VISION.md` remains unchanged
And only README content between the marker pair changes
And the skill reports whether README changed or already matched.

### Example E8: malformed README markers stop update or sync

Given root `VISION.md` exists
And README has missing, malformed, nested, or multiple vision marker pairs
When the user asks to update vision or sync README
Then the skill stops before modifying files
Unless the user explicitly authorizes marker insertion or skipping README synchronization.

### Example E9: old mode words are not required modes

Given root `VISION.md` exists
When the user says `vision mirror`
Then the skill may interpret the request as a README sync intent
But it must apply state-based behavior
And it must not report `mirror` as a mode used.

### Example E10: proposals use uppercase vision reference

Given root `VISION.md` exists
When a new proposal is created
Then it includes `Vision fit`
And it must not use `no vision exists yet`.

### Example E11: no canonical vision is explicit

Given neither root `VISION.md` nor root `vision.md` exists
When a new proposal is created
Then it includes `Vision fit`
And the section states `no vision exists yet`.

## Requirements

### Canonical artifact and source of truth

R1. The canonical project-vision artifact MUST be root `VISION.md`.

R2. Root `VISION.md` MUST own project identity, target users, commitments, refusals, and proposal-fit framing.

R3. Root `VISION.md` MUST be subordinate to `CONSTITUTION.md`.

R4. Root `VISION.md` MUST NOT replace specs, proposals, architecture documents, ADRs, plans, test specs, review artifacts, verification evidence, or PR summaries.

R5. README front-matter between `<!-- vision:start -->` and `<!-- vision:end -->` MUST be generated from `VISION.md` and MUST NOT be independently authoritative.

R6. If README front-matter conflicts with `VISION.md`, `VISION.md` MUST be treated as the source of truth.

R7. After migration completes, root `vision.md` MUST NOT be described as canonical in active governance, workflow, skill, proposal, proposal-review, README, selector, or validation guidance.

R8. Historical proposals and change-local artifacts MUST NOT be rewritten solely to update old `vision.md` path references.

### Migration states

R9. For this repository migration, the final migrated state MUST contain root `VISION.md` and MUST NOT contain root `vision.md`.

R10. The pre-migration state with only root `vision.md` MAY be treated as legacy input for this migration because this repository already has an established project-vision artifact.

R11. The state where both root `vision.md` and root `VISION.md` exist MUST be invalid.

R12. When both root `vision.md` and root `VISION.md` exist, the `vision` skill and repository validation MUST require an owner decision before either file is merged, deleted, or overwritten.

R13. The migration MUST preserve the approved project vision content except for path-sensitive references, generated README front-matter, or explicit owner-approved wording changes.

R14. The implementation plan SHOULD use a safe two-step Git rename for case-only path migration when the filesystem or Git configuration may not reliably record a case-only rename.

R15. Rollback MUST restore exactly one canonical vision artifact path and MUST NOT leave both root `vision.md` and root `VISION.md` in the repository.

### Vision skill interface

R16. The `vision` skill MUST remain named `vision`.

R17. The `vision` skill description MUST describe producing or updating the project vision and matching README front-matter without requiring user-facing `create`, `revise`, or `mirror` modes.

R18. The `vision` skill MUST NOT present `create`, `revise`, and `mirror` as required user-facing operating modes.

R19. The `vision` skill MUST NOT include a required mode-selection table for `create`, `revise`, and `mirror`.

R20. The `vision` skill MUST use state-based behavior based on repository state and user intent.

R21. The `vision` skill MAY interpret legacy mode words as natural-language intent, but it MUST apply the state-based behavior in this spec and MUST NOT report those words as modes used.

R22. The `vision` skill output MUST NOT include a required `Mode used` field.

R23. Every `vision` skill run MUST report changed files.

R24. Every `vision` skill run MUST report whether README front-matter was created, replaced, unchanged, skipped, or blocked.

R25. When the skill creates the initial `VISION.md`, it MUST report assumptions and open vision-level questions.

R26. When the skill updates `VISION.md`, it MUST report sections changed and whether the revision is `substantive` or `editorial`.

R27. When the skill syncs README only, it MUST report that `VISION.md` was unchanged.

### Vision establishment behavior

R28. If neither root `VISION.md` nor root `vision.md` exists and the user explicitly asks to establish project vision, the `vision` skill MUST create root `VISION.md`.

R29. The `vision` skill MUST NOT create root `VISION.md` merely because the skill is installed or invoked for ordinary README maintenance.

R30. If no canonical vision artifact exists and the user does not clearly ask to establish project vision, the skill MUST stop and ask whether to create `VISION.md`.

R31. Initial `VISION.md` content generated by the skill MUST continue to follow the approved 500-word cap, required section order, plain-language rule, no requirements-vocabulary rule, no implementation-detail rule, drafting heuristics, privacy boundary, research boundary, and plain-Markdown readability rules from `specs/vision-skill.md`.

### Vision update behavior

R32. If root `VISION.md` exists and the user asks to update vision content, the skill MUST update only the requested section or clearly related sections.

R33. If a requested vision update necessarily affects sections beyond the requested section, the skill MUST state why before finalizing.

R34. If the requested section or update intent is unclear, the skill MUST stop and ask for clarification before editing `VISION.md`.

R35. Before finalizing any `VISION.md` update, the skill MUST ask or confirm whether the update is `substantive` or `editorial`.

R36. If an update changes project scope, target users, commitments, refusals, proposal-fit framing, or falsifiability, the skill MUST treat it as substantive unless an owner explicitly records a contrary rationale.

R37. For substantive updates tied to an existing or required change-local pack, the skill MUST require the causal link to be recorded in the relevant `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing.

R38. Editorial updates and README-sync-only changes MUST NOT require a new change-local pack solely because the `vision` skill ran.

R39. The skill MUST NOT silently overwrite an existing `VISION.md`.

R40. The skill MUST NOT merge legacy `vision.md` into `VISION.md` automatically when both files exist.

### README front-matter behavior

R41. README front-matter MUST remain bounded by the exact marker pair `<!-- vision:start -->` and `<!-- vision:end -->`.

R42. Generated README front-matter MUST include only the pitch, differentiator, target audience, and a link to `VISION.md`.

R43. README front-matter MUST be derived from `VISION.md`.

R44. Automatic README marker insertion MUST be allowed only when creating the initial `VISION.md`.

R45. If README contains an existing valid marker block, the skill MUST replace only content inside the marker block and preserve all content outside the markers.

R46. When updating an existing `VISION.md` or syncing README from it, missing, malformed, nested, or multiple README marker pairs MUST stop the skill before file modification unless the user explicitly authorizes marker insertion or skipping README synchronization.

R47. If README marker insertion is explicitly authorized, the skill MUST preserve existing README content order and insert one marker-bounded front-matter block at the deterministic README location already defined by `specs/vision-skill.md`.

R48. The skill MUST NOT edit README content outside the marker block except to insert the marker block when initial vision creation or explicit owner authorization allows insertion.

R49. This change MUST NOT add a required README synchronization helper script.

### Proposal and proposal-review behavior

R50. The `proposal` skill MUST read root `VISION.md` when present as the canonical project-vision reference.

R51. The `proposal` skill MUST require a `Vision fit` section in every new proposal it creates after this spec is approved.

R52. The `proposal` skill MUST require a `Vision fit` section when it substantively revises an existing proposal after this spec is approved.

R53. Legacy proposals that are not substantively revised after this spec is approved MUST NOT be considered invalid solely because they reference `vision.md` or lack `Vision fit`.

R54. A proposal's `Vision fit` section MUST begin with exactly one allowed status value on the first non-empty line:

- `fits the current vision`;
- `may conflict with the current vision`;
- `proposes a vision revision`;
- `no vision exists yet`.

A short explanatory paragraph MAY follow the status line.

R55. If root `VISION.md` exists, `Vision fit` MUST NOT use `no vision exists yet`.

R56. If neither root `VISION.md` nor migration-recognized legacy root `vision.md` exists, `Vision fit` MUST use `no vision exists yet`. During this repository migration, proposals MUST NOT use `no vision exists yet` solely because `VISION.md` has not yet replaced legacy `vision.md`.

R57. A proposal MUST NOT silently redefine project vision outside the `Vision fit` section and normal proposal rationale.

R58. The `proposal-review` skill MUST check a proposal's `Vision fit` section against root `VISION.md` when it exists.

R59. If a proposal created or substantively revised after this spec is approved lacks `Vision fit`, proposal-review MUST request revision.

R60. If proposal-review finds a conflict with `VISION.md`, the review MUST classify the required outcome as revise proposal, revise vision, or record explicit exception.

R61. A proposal-review explicit exception MUST include approving owner or owning stage, evidence for the conflict, why proposal revision is not chosen, why vision revision is not chosen, where the exception is recorded, and whether the exception is one-time or establishes a future vision-revision trigger.

R62. An explicit vision-conflict exception MUST be recorded in both the proposal's `Vision fit` section and the proposal-review output.

### Governance, validation, and generated output

R63. `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and README ownership guidance MUST be updated when they name the canonical vision path.

R64. Active governance, workflow, README, proposal, proposal-review, and vision-skill guidance MUST state that `VISION.md` is the canonical project-vision artifact.

R65. Active governance, workflow, README, proposal, proposal-review, and vision-skill guidance MUST state that README front-matter is generated from `VISION.md`.

R66. Selector routing MUST classify root `VISION.md` as a supported vision surface.

R67. During the `vision.md` to `VISION.md` migration, selector routing MUST classify legacy root `vision.md` so a deletion, rename, or migration check does not fail PR-mode or explicit-mode validation as `unclassified-path`.

R68. Selector-selected validation for root `VISION.md` changes MUST include README vision marker validation or an equivalent repository-owned vision/README consistency check.

R69. Repository-owned validation MUST block or fail when both root `vision.md` and root `VISION.md` exist.

R70. Focused skill-validator coverage MUST assert that the `vision` skill no longer exposes `create`, `revise`, or `mirror` as user-facing modes while preserving state-based safety behavior.

R71. Focused selector coverage MUST prove root `VISION.md` explicit-path selection and PR-mode selection are classified and select the expected vision/README checks.

R72. Generated `.codex/skills/` output MUST be refreshed only through `scripts/build-skills.py`.

R73. Generated public adapter output under `dist/adapters/` MUST be refreshed only through `scripts/build-adapters.py`.

R74. Generated skill and adapter output MUST match canonical skill sources after generation.

R75. The normal per-change lifecycle MUST NOT add `vision` as a required stage.

### Legacy contract retirement, pre-vision state, and migration routing

R76. When this spec is approved, the repository MUST update active vision contract surfaces so no approved spec, active test spec, or canonical skill requires the old lowercase-path or user-facing mode model.

R77. The implementation MUST update `specs/vision-skill.md`, `specs/vision-skill.test.md`, `skills/vision/SKILL.md`, generated `.codex/skills/`, and generated public adapters under `dist/adapters/`.

R78. The updates required by R77 MUST retire or rewrite requirements that require root `vision.md` as the canonical project-vision artifact.

R79. The updates required by R77 MUST retire or rewrite requirements that require user-facing `create`, `revise`, or `mirror` operating modes.

R80. The updates required by R77 MUST preserve still-valid safety and quality rules, including no silent overwrite of an existing vision, deterministic README marker handling, no silent README marker insertion during update or sync unless explicitly authorized, substantive/editorial confirmation for meaning-changing updates, plain Markdown readability, sensitive information exclusion, and bounded-read behavior.

R81. For repositories before project vision has been established, neither root `VISION.md` nor root `vision.md` MAY exist.

R82. In a pre-vision repository state, proposal and proposal-review behavior MUST follow the no-vision rules: proposals use `Vision fit` status `no vision exists yet`, and substantive proposals stop unless they are bootstrap work to create project vision or the workflow explicitly permits proceeding without one.

R83. After migration, root `vision.md` MUST NOT be treated as canonical if it reappears; selector behavior MUST classify it as a legacy or conflict case rather than silently ignoring it.

## Inputs and outputs

Inputs:

- user request to establish project vision, update vision, or sync README;
- root `VISION.md`, when present;
- legacy root `vision.md`, when present during migration;
- README front-matter, when present;
- project context from `CONSTITUTION.md`, `AGENTS.md`, README, project map, recent proposals, research, and exploration artifacts when present;
- change-local pack when a substantive update is part of a non-trivial change.

Outputs:

- root `VISION.md` when the skill establishes or updates project vision;
- deletion or rename of legacy root `vision.md` during migration;
- README front-matter between the marker pair when generated or synchronized;
- updated governance, workflow, README, proposal, proposal-review, vision-skill, spec, and test-spec guidance when they name the canonical path or mode model;
- selector and validator coverage for root `VISION.md`;
- generated `.codex/skills/` and `dist/adapters/` output after canonical skill changes and generator runs;
- user-facing `vision` skill output that reports changed files, README front-matter action, assumptions or open questions when relevant, sections changed when relevant, and substantive/editorial classification when relevant.

## State and invariants

- `VISION.md` is the only canonical project-vision artifact after migration.
- For this repository migration, the final state is not a no-vision state because the repository already has an established project-vision artifact.
- Repositories before project vision has been established may have neither root `VISION.md` nor root `vision.md`.
- `VISION.md` remains subordinate to `CONSTITUTION.md`.
- `VISION.md` does not replace specs, proposals, architecture artifacts, ADRs, execution plans, test specs, review artifacts, verification evidence, or PR summaries.
- README front-matter is generated from `VISION.md` and is not independently authoritative.
- Content outside README vision markers remains author-owned.
- The `vision` skill remains upstream of the per-change workflow.
- Adding or updating the skill and establishing project vision remain separate actions unless the user explicitly asks to establish project vision.
- Generated skill and adapter output remains derived from canonical authored skill sources.
- Drafting heuristics guide authoring quality but do not change the required vision sections, 500-word cap, README marker behavior, or source-of-truth order except for the path migration from `vision.md` to `VISION.md`.

## Error and boundary behavior

- Existing `VISION.md` plus unclear update intent stops for clarification before editing.
- Missing `VISION.md` plus no establishment intent stops for clarification before editing.
- Missing `VISION.md` plus sync request stops because there is no canonical source to sync from.
- Both root `vision.md` and root `VISION.md` existing stops skill behavior and blocks validation until an owner decision resolves the state.
- Missing or malformed README markers outside initial establishment or explicit owner authorization stop the skill before file modification.
- A generated or revised `VISION.md` over 500 words is invalid and must be shortened before completion.
- A proposal with stale or missing `Vision fit` after this spec applies must be revised before proposal-review can approve it.
- A substantive vision update tied to an existing or required change-local pack stops before finalization when the causal link is missing from the required change-local artifacts.
- Generated output drift blocks completion until generator output matches canonical sources.

## Compatibility and migration

Existing proposals, specs, plans, reviews, change-local artifacts, and PR records remain historically valid when they mention `vision.md`. They are not rewritten solely for path text.

The migration from `vision.md` to `VISION.md` must be atomic within the implementing branch: the final branch state contains exactly one canonical vision file.

For this repository, the final migrated branch state is not allowed to be a no-vision state.

For repositories before project vision has been established, neither root vision file may exist. In that state, proposals must use `Vision fit` status `no vision exists yet`, and substantive proposals stop unless they are bootstrap work to create project vision or the workflow explicitly permits proceeding without one.

The implementation plan should use a two-step Git rename when needed to make the case-only path change reliable across filesystems:

```bash
git mv vision.md .vision.tmp
git mv .vision.tmp VISION.md
```

Legacy user requests that contain `create`, `revise`, or `mirror` may be interpreted as plain-language intent during a compatibility period, but those words are not operating modes and are not reported as modes.

Rollback must restore exactly one canonical root vision artifact, update all active path references, refresh generated skill and adapter output, and rerun validation.

## Observability

The `vision` skill's user-facing response must report:

- changed files;
- README front-matter action: created, replaced, unchanged, skipped, or blocked;
- assumptions and open vision-level questions when establishing project vision;
- sections changed when updating vision;
- revision classification when updating vision;
- whether a substantive update's causal link was recorded or not required;
- why the skill stopped when a boundary condition blocks editing.

Validation output remains the repository-owned skill, generated-output, adapter, lifecycle, README, selector, and metadata validation output selected for touched paths.

## Security and privacy

`VISION.md` and generated README front-matter must not include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication.

If sensitive or private content is present in inputs, the `vision` skill must omit it or ask for explicit confirmation before including it.

The `vision` skill must not fetch external information unless the user explicitly requests research or the workflow invokes a research-backed mode before vision drafting.

If external research is used, the `vision` skill output must distinguish researched facts from project assumptions.

## Accessibility and UX

No application UI is involved.

`VISION.md` must be readable as plain Markdown and must not require rendered tables, diagrams, HTML layout, or generated assets to understand the project vision.

The simplified skill interface should be understandable from ordinary user intent such as establishing vision, updating vision, or syncing README, without requiring users to choose internal mode names.

## Performance expectations

No runtime performance behavior is introduced.

Evidence collection behavior remains bounded by the existing summary-first and full-file-read guidance. Full-file reads remain required when creating or replacing the canonical vision artifact, when README marker placement depends on the whole README structure, or when the whole source-of-truth artifact is the review target.

## Edge cases

1. Root `vision.md` exists and root `VISION.md` does not: migration treats lowercase as legacy input and produces uppercase as the only canonical file.
2. Root `VISION.md` exists and root `vision.md` also exists: skill behavior stops and validation blocks until an owner decision resolves coexistence.
3. Neither root vision file exists and README already has vision markers: establishing project vision may replace the marker content after creating `VISION.md`.
4. Root `VISION.md` exists and README lacks markers: update or sync stops unless the user explicitly authorizes marker insertion or skipping README synchronization.
5. README contains two `<!-- vision:start -->` markers: update or sync stops for explicit handling.
6. A proposal created after approval says `fits the current vision` while neither root `VISION.md` nor migration-recognized legacy root `vision.md` exists: proposal-review requests revision to `no vision exists yet`.
7. A proposal created after approval omits `Vision fit`: proposal-review requests revision.
8. A vision update changes project scope but is labeled editorial: the skill surfaces the mismatch and treats it as substantive or asks for owner clarification.
9. A user asks to update vision but names no section or direction: the skill asks for clarification before editing.
10. A user asks to sync README and README front-matter already matches `VISION.md`: the skill reports no content changes.
11. A generated adapter omits the updated `vision` skill even though portability rules include it: adapter validation or drift checking fails through existing generated-output checks.
12. A historical proposal references `vision.md`: no update is required solely because the reference is historical.
13. A request says `vision mirror`: the skill may treat it as README sync intent, but it does not require or report `mirror` mode.
14. A case-only rename is not recorded by Git on a local filesystem: the implementation uses a two-step rename before final validation.
15. This repository migration ends with neither root vision file: validation fails because this repository already has an established project-vision artifact.
16. A different repository has not established project vision yet: neither root vision file may exist, proposals use `Vision fit` status `no vision exists yet`, and substantive proposals stop unless they are bootstrap or explicitly permitted.
17. After migration, root `vision.md` reappears: selector behavior classifies it as a legacy or conflict case rather than ignoring it.

## Non-goals

- Rewrite the approved project vision content.
- Make `vision` a normal per-change workflow stage.
- Add validator enforcement for vision prose quality.
- Add a README synchronization helper script.
- Create a separate `vision-review` skill.
- Rewrite old proposals, specs, plans, reviews, change-local artifacts, or PR records solely to replace historical `vision.md` text.
- Turn the vision into a roadmap, feature list, status tracker, requirements spec, architecture document, or project-management system.
- Change adapter portability rules beyond refreshing generated output for changed canonical skill guidance.
- Require specific competitor names in generated or revised vision text.
- Extract or consolidate shared evidence-collection guidance across skills.
- Change the 500-word cap, required vision sections, drafting heuristics, privacy rules, or research boundaries except where wording must refer to `VISION.md`.

## Acceptance criteria

- AC1. Root `VISION.md` is the only canonical project-vision artifact after migration.
- AC2. Root `vision.md` is absent from the final migrated branch state.
- AC3. Active governance, workflow, README, proposal, proposal-review, and vision-skill guidance name `VISION.md` as canonical.
- AC4. README front-matter links to `VISION.md` and remains marker-bounded.
- AC5. The `vision` skill validates as a canonical skill and no longer exposes `create`, `revise`, or `mirror` as user-facing modes.
- AC6. The `vision` skill preserves safe state-based establishment, update, and README sync behavior.
- AC7. The `vision` skill preserves substantive/editorial confirmation and causal-link gating for substantive changes.
- AC8. Proposal guidance requires `Vision fit` against `VISION.md` for new and substantively revised proposals.
- AC9. Proposal-review checks `Vision fit` against `VISION.md` and preserves explicit exception requirements.
- AC10. Repository-owned validation classifies root `VISION.md` as a supported vision surface.
- AC11. Repository-owned validation blocks or fails when both root `vision.md` and root `VISION.md` exist.
- AC12. Selector regression coverage proves explicit and PR-mode routing for root `VISION.md`.
- AC13. Generated `.codex/skills/` output is synchronized through `scripts/build-skills.py`.
- AC14. Generated `dist/adapters/` output is synchronized through `scripts/build-adapters.py`.
- AC15. Historical artifacts are not rewritten solely for lowercase `vision.md` references.
- AC16. The normal lifecycle chain does not include `vision` as a required stage.
- AC17. `specs/vision-skill.md`, `specs/vision-skill.test.md`, and `skills/vision/SKILL.md` no longer require root `vision.md` as canonical or user-facing `create`, `revise`, and `mirror` operating modes.
- AC18. The still-valid vision safety and quality rules remain present after retiring the old path and mode model.
- AC19. Selector routing classifies both root `VISION.md` and legacy root `vision.md` during migration, and a deletion, rename, or migration of root `vision.md` does not fail PR-mode or explicit-mode validation as `unclassified-path`.
- AC20. After migration, reintroduced root `vision.md` is classified as a legacy or conflict case.
- AC21. Proposal `Vision fit` accepts exactly one allowed status on the first non-empty line and permits a short explanatory paragraph after the status line.

## Open questions

None.

## Next artifacts

- `code-review` for M2 authored-surface implementation
- `verify`
- `implement` M3 generated-output refresh after M2 review and verification
- final `code-review`, `verify`, `explain-change`, and `pr`

## Follow-on artifacts

- Plan: [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)
- Test spec: [Vision Skill Simplification and VISION.md Migration Test Spec](vision-skill-simplification-and-vision-md-migration.test.md)
- M1 implementation: selector and validation support committed.
- M2 implementation: authored-surface migration ready for code-review.

## Readiness

Approved after `spec-review`. The linked execution plan and focused test spec track downstream implementation and review state for the migration.
