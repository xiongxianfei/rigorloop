# Vision Skill

## Status

- approved

## Related proposal

- [Vision Skill](../docs/proposals/2026-04-29-vision-skill.md)
- [Vision Skill Quality Refinement](../docs/proposals/2026-04-30-vision-skill-quality-refinement.md)
- [Vision Skill Simplification and VISION.md Migration](../docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)

## Goal and context

This spec defines the contributor-visible contract for the `vision` skill and adjacent proposal and proposal-review guidance. The skill gives RigorLoop a safe way to establish or update root `VISION.md`, synchronize short generated README front-matter, and make proposal fit against the project vision explicit.

The vision skill is upstream of the normal per-change workflow. It is not a lifecycle stage between proposal, spec, architecture, planning, implementation, review, verification, and PR.

This active contract has been updated by the approved `VISION.md` migration. It retires the old lowercase canonical path and the old user-facing mode model while preserving the still-valid quality and safety rules from the original vision skill.

## Glossary

- `VISION.md`: the canonical project vision document at the repository root.
- legacy root `vision.md`: the lowercase root project-vision path recognized only as migration input or a legacy/conflict case after migration.
- README front-matter: the README section between `<!-- vision:start -->` and `<!-- vision:end -->`, generated from `VISION.md`.
- marker pair: the exact `<!-- vision:start -->` and `<!-- vision:end -->` comments that bound generated README front-matter.
- state-based behavior: `vision` skill behavior determined by repository state and ordinary user intent rather than by required user-facing modes.
- establish project vision: create the initial canonical `VISION.md`.
- update vision: change canonical project-vision content in `VISION.md`.
- sync README: regenerate README front-matter from `VISION.md` without changing `VISION.md`.
- substantive revision: a vision change caused by a proposal, incident, learning, or project-direction drift.
- editorial revision: a typo, wording cleanup, or formatting-only change that does not change project meaning.
- drafting heuristics: non-normative authoring questions in the `vision` skill that help produce sharper vision text before finalizing generated or revised content.
- `Vision fit`: a proposal section that states how the proposed direction relates to `VISION.md`.
- explicit exception: a proposal-review outcome that allows a proposal to proceed despite a vision conflict without revising the proposal or vision.

## Examples first

### Example E1: establishing the first vision is explicit

Given neither root `VISION.md` nor legacy root `vision.md` exists
When the user explicitly asks to establish project vision
Then the skill creates root `VISION.md`
And it inserts deterministic README front-matter markers when needed
And it reports assumptions and open vision-level questions.

### Example E2: skill installation does not create vision

Given the `vision` skill exists
When it is installed, regenerated, or invoked for ordinary README maintenance
Then no root `VISION.md` is created without explicit project-vision establishment intent.

### Example E3: existing vision updates are bounded

Given root `VISION.md` exists
When the user asks to update one vision section
Then the skill updates only the requested section or clearly related sections
And asks or confirms whether the update is `substantive` or `editorial` before finalizing.

### Example E4: README sync leaves vision unchanged

Given root `VISION.md` exists
And README contains one valid marker pair
When the user asks to sync README
Then `VISION.md` remains unchanged
And only README content between the marker pair changes.

### Example E5: proposals expose vision fit

Given root `VISION.md` exists
When the proposal skill creates a new proposal
Then the proposal includes a `Vision fit` section
And the first non-empty line is one allowed status value.

### Example E6: no vision exists yet is explicit

Given neither root `VISION.md` nor migration-recognized legacy root `vision.md` exists
When the proposal skill creates a new proposal
Then `Vision fit` states `no vision exists yet`.

### Example E7: proposal-review classifies a vision conflict

Given root `VISION.md` exists
And a proposal says `may conflict with the current vision`
When proposal-review confirms the conflict
Then the review outcome identifies whether the next action is revise proposal, revise vision, or record explicit exception.

### Example E8: legacy mode words are intent hints only

Given root `VISION.md` exists
When the user says `vision mirror`
Then the skill may treat that wording as README sync intent
But the skill applies state-based behavior and does not report a mode.

## Requirements

### Canonical artifact and source of truth

R1. The canonical project-vision artifact MUST be root `VISION.md`.

R2. `VISION.md` MUST own project identity, target users, commitments, refusals, and proposal-fit framing.

R3. `CONSTITUTION.md` MUST outrank `VISION.md`.

R4. `VISION.md` MUST NOT replace specs, proposals, architecture artifacts, ADRs, plans, test specs, review artifacts, verification evidence, or PR summaries.

R5. README front-matter between `<!-- vision:start -->` and `<!-- vision:end -->` MUST be generated from `VISION.md` and MUST NOT be independently authoritative.

R6. If README front-matter conflicts with `VISION.md`, `VISION.md` MUST be treated as the source of truth.

R7. Active governance, workflow, README, proposal, proposal-review, and vision-skill guidance MUST NOT describe root `vision.md` as canonical after migration.

R8. Historical proposals, specs, plans, reviews, change-local artifacts, and PR records MUST NOT be rewritten solely to update old `vision.md` references.

### Vision skill interface

R9. The repository MUST keep a canonical authored `vision` skill under `skills/vision/SKILL.md`.

R10. The `vision` skill metadata MUST use `name: vision`.

R11. The `vision` skill description MUST state that it produces or updates the project vision and matching README front-matter.

R12. The `vision` skill no longer exposes `create`, `revise`, or `mirror` as user-facing modes.

R13. The `vision` skill MUST use state-based behavior based on repository state and ordinary user intent.

R14. The skill MAY interpret legacy words such as `create`, `revise`, and `mirror` as natural-language intent hints, but it MUST NOT require users to choose those words and MUST NOT report them as modes used.

R15. Every `vision` skill run MUST report changed files.

R16. Every `vision` skill run MUST report whether README front-matter was created, replaced, unchanged, skipped, blocked, or not applicable.

R17. Establishment output MUST report assumptions and open vision-level questions.

R18. Update output MUST report sections changed and whether the update is `substantive` or `editorial`.

R19. README-only sync output MUST report that `VISION.md` was unchanged.

### Establishment, update, and sync behavior

R20. If neither root `VISION.md` nor legacy root `vision.md` exists and the user explicitly asks to establish project vision, the skill MUST create root `VISION.md`.

R21. The skill MUST NOT create root `VISION.md` merely because the skill is installed or invoked for ordinary README maintenance.

R22. If no canonical vision artifact exists and the user does not clearly ask to establish project vision, the skill MUST stop and ask whether to create `VISION.md`.

R23. If root `VISION.md` exists and the user asks to update vision content, the skill MUST update only the requested section or clearly related sections.

R24. If a requested update necessarily affects sections beyond the requested section, the skill MUST state why before finalizing.

R25. If update intent is unclear, the skill MUST stop and ask for clarification before editing `VISION.md`.

R26. Before finalizing any `VISION.md` update, the skill MUST ask or confirm whether the update is `substantive` or `editorial`.

R27. Updates that change project scope, target users, commitments, refusals, proposal-fit framing, or falsifiability MUST be treated as substantive unless an owner explicitly records a contrary rationale.

R28. For substantive updates tied to an existing or required change-local pack, the skill MUST require the causal link to be recorded in `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing.

R29. Editorial updates and README-only sync MUST NOT require a new change-local pack solely because the `vision` skill ran.

R30. The skill MUST NOT silently overwrite an existing `VISION.md`.

R31. If both root `vision.md` and root `VISION.md` exist, the skill MUST stop and require an owner decision before either file is merged, deleted, or overwritten.

### Vision content and drafting quality

R32. `VISION.md` generated or revised by the skill MUST be no more than 500 words.

R33. `VISION.md` generated or revised by the skill MUST use plain language and MUST NOT use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary.

R34. `VISION.md` generated or revised by the skill MUST NOT include implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, priority columns, or feature lists.

R35. `VISION.md` generated or revised by the skill MUST include sections, in order, covering pitch, differentiator, target audience, non-audience, commitments, refusals, falsifiability, and optional open questions.

R36. `VISION.md` MUST be readable as plain Markdown and MUST NOT require rendered tables, diagrams, HTML layout, or generated assets to understand the project vision.

R37. Drafting heuristics MUST be phrased as authoring questions or checks, not as additional required `VISION.md` sections.

R38. Drafting heuristics MUST ask about differentiator comparison, tradeoffs, embedded pain points, checkable commitments, observable falsifiability, audience non-fit, and concrete refusals.

R39. Drafting heuristics MUST allow either an alternative class or a specific tool for differentiator comparison and MUST NOT require naming a specific competitor.

### README front-matter

R40. README front-matter MUST be bounded by the exact marker pair:

```markdown
<!-- vision:start -->
<!-- vision:end -->
```

R41. README front-matter generated by the skill MUST include only the pitch, differentiator, target audience, and a link to `VISION.md` for goals, non-goals, and falsifiability.

R42. README front-matter generated by the skill MUST be derived from `VISION.md`.

R43. Automatic README marker insertion MUST be allowed only when creating the initial `VISION.md`.

R44. If README contains an existing valid marker block, the skill MUST replace only content inside the marker block and preserve all content outside the markers.

R45. When updating an existing `VISION.md` or syncing README, missing, malformed, nested, or multiple README marker pairs MUST stop the skill before file modification unless the user explicitly authorizes marker insertion or skipping README synchronization.

R46. If marker insertion is authorized, the skill MUST preserve existing README content order and insert one marker-bounded front-matter block at the deterministic README location defined by the skill.

R47. The skill MUST NOT edit README content outside the marker block except to insert the marker block when initial vision creation or explicit owner authorization allows insertion.

R48. The implementation MUST NOT add a required README synchronization helper script.

### Proposal and proposal-review behavior

R49. The `proposal` skill MUST read root `VISION.md` when present as the canonical project-vision reference.

R50. The `proposal` skill MUST require a `Vision fit` section in every new proposal it creates after this contract is adopted.

R51. The `proposal` skill MUST require a `Vision fit` section when it substantively revises an existing proposal after this contract is adopted.

R52. Legacy proposals that are not substantively revised MUST NOT be considered invalid solely because they reference `vision.md` or lack `Vision fit`.

R53. A proposal's `Vision fit` section MUST begin with exactly one allowed status value on the first non-empty line:

- `fits the current vision`;
- `may conflict with the current vision`;
- `proposes a vision revision`;
- `no vision exists yet`.

A short explanatory paragraph MAY follow the status line.

R54. If root `VISION.md` exists, `Vision fit` MUST NOT use `no vision exists yet`.

R55. If neither root `VISION.md` nor migration-recognized legacy root `vision.md` exists, `Vision fit` MUST use `no vision exists yet`.

R56. During this repository migration, proposals MUST NOT use `no vision exists yet` solely because `VISION.md` has not yet replaced migration-recognized legacy root `vision.md`.

R57. A proposal MUST NOT silently redefine project vision outside the `Vision fit` section and normal proposal rationale.

R58. The `proposal-review` skill MUST check a proposal's `Vision fit` section.

R59. If a proposal created or substantively revised after this contract is adopted lacks `Vision fit`, proposal-review MUST request revision.

R60. If proposal-review finds a conflict with `VISION.md`, the review MUST classify the required outcome as revise proposal, revise vision, or record explicit exception.

R61. A proposal-review explicit exception MUST include the approving owner or owning stage, evidence for the conflict, why proposal revision is not chosen, why vision revision is not chosen, where the exception is recorded, and whether the exception is one-time or establishes a future vision-revision trigger.

R62. An explicit vision-conflict exception MUST be recorded in both the proposal's `Vision fit` section and the proposal-review output.

### Workflow, validation, and safety boundaries

R63. The `vision` skill MUST remain upstream of the per-change workflow and MUST NOT be added to the normal lifecycle chain.

R64. Generated `.codex/skills/` output MUST be refreshed only through `scripts/build-skills.py`.

R65. Generated public adapter output under `dist/adapters/` MUST be refreshed only through `scripts/build-adapters.py`.

R66. Selector routing MUST classify root `VISION.md` and migration-time legacy root `vision.md` as supported validation surfaces.

R67. Repository-owned validation MUST block or fail when both root `vision.md` and root `VISION.md` exist.

R68. `VISION.md` and generated README front-matter MUST NOT include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication.

R69. If sensitive or private content is present in inputs, the `vision` skill MUST omit it or ask for explicit confirmation before including it.

R70. The `vision` skill MUST NOT fetch external information unless the user explicitly requests research or the workflow invokes a research-backed mode before vision drafting.

R71. If external research is used, the `vision` skill output MUST distinguish researched facts from project assumptions.

R72. The `vision` skill SHOULD start from compact project inputs when available and SHOULD escalate to full-file reads only when compact inputs are missing, conflicting, or insufficient to determine project-level framing.

## Inputs and outputs

Inputs:

- user request to establish project vision, update vision, or sync README;
- root `VISION.md`, when present;
- legacy root `vision.md`, when present during migration or conflict resolution;
- README front-matter, when present;
- project context from `CONSTITUTION.md`, `AGENTS.md`, README, project map, recent proposals, research, and exploration artifacts when present;
- change-local pack when a substantive update is part of a non-trivial change.

Outputs:

- root `VISION.md` when the skill establishes or updates project vision;
- README front-matter between the marker pair when generated or synchronized;
- updated proposal and proposal-review guidance when proposal-fit behavior changes;
- generated `.codex/skills/` and `dist/adapters/` output after canonical skill changes and generator runs;
- user-facing `vision` skill output that reports changed files, README front-matter action, assumptions or open questions when relevant, sections changed when relevant, and substantive/editorial classification when relevant.

## State and invariants

- `VISION.md` is the canonical project vision.
- Legacy root `vision.md` is not canonical after migration.
- `VISION.md` is subordinate to `CONSTITUTION.md` and does not replace specs, proposals, architecture artifacts, ADRs, plans, test specs, review artifacts, verification evidence, or PR summaries.
- README front-matter is generated from `VISION.md` and is not independently authoritative.
- The vision skill is upstream of the per-change workflow.
- Adding or updating the skill and establishing project vision remain separate actions unless the user explicitly asks to establish project vision.
- Generated skill and adapter output remains derived from canonical authored skill sources.
- Drafting heuristics guide authoring quality but do not change the required vision sections, 500-word cap, README marker behavior, or source-of-truth order.

## Error and boundary behavior

- Existing `VISION.md` plus unclear update intent stops for clarification.
- Missing `VISION.md` plus no establishment intent stops for clarification.
- Missing `VISION.md` plus sync request stops because there is no canonical source to sync from.
- Both root `vision.md` and root `VISION.md` existing stops skill behavior and blocks validation until an owner decision resolves the state.
- Missing or malformed README markers outside initial establishment or explicit owner authorization stop the skill before file modification.
- A generated or revised `VISION.md` over 500 words is invalid and must be shortened before completion.
- A proposal with stale or missing `Vision fit` after this contract applies must be revised before proposal-review can approve it.
- A substantive vision update tied to an existing or required change-local pack stops before finalization when the causal link is missing from the required change-local artifacts.

## Compatibility and migration

Existing proposals, specs, plans, reviews, change-local artifacts, and PR records remain historically valid when they mention `vision.md`. They are not rewritten solely for path text.

For this repository migration, the final branch state must contain root `VISION.md` and must not contain root `vision.md`.

For repositories before project vision has been established, neither root vision file may exist. In that state, proposals use `Vision fit` status `no vision exists yet`, and substantive proposals stop unless they are bootstrap work to create project vision or the workflow explicitly permits proceeding without one.

Legacy user requests that contain `create`, `revise`, or `mirror` may be interpreted as plain-language intent during compatibility, but those words are not operating modes and are not reported as modes.

Rollback must restore exactly one canonical root vision artifact, update all active path references, refresh generated skill and adapter output, and rerun validation.

## Observability

The `vision` skill's user-facing response must report changed files, README front-matter action, assumptions or open questions when establishing project vision, sections changed and revision classification when updating vision, whether a substantive update's causal link was recorded or not required, and why the skill stopped when a boundary condition blocks editing.

Validation output remains the repository-owned skill, generated-output, adapter, lifecycle, README, selector, and metadata validation output selected for touched paths.

## Security and privacy

Sensitive information and external research boundaries are governed by R68 through R71.

## Accessibility and UX

No application UI is involved. Plain Markdown readability is governed by R36.

## Performance expectations

No runtime performance behavior is introduced. Evidence collection behavior is governed by R72.

## Edge cases

1. Root `vision.md` exists and root `VISION.md` does not: migration treats lowercase as legacy input and produces uppercase as the only canonical file.
2. Root `VISION.md` exists and root `vision.md` also exists: skill behavior stops and validation blocks until an owner decision resolves coexistence.
3. Neither root vision file exists and README already has vision markers: establishing project vision may replace the marker content after creating `VISION.md`.
4. Root `VISION.md` exists and README lacks markers: update or sync stops unless the user explicitly authorizes marker insertion or skipping README synchronization.
5. README contains two `<!-- vision:start -->` markers: update or sync stops for explicit handling.
6. A proposal created after adoption says `fits the current vision` while neither root `VISION.md` nor migration-recognized legacy root `vision.md` exists: proposal-review requests revision to `no vision exists yet`.
7. A proposal created after adoption omits `Vision fit`: proposal-review requests revision.
8. A vision update changes project scope but is labeled editorial: the skill surfaces the mismatch and treats it as substantive or asks for owner clarification.
9. A user asks to update vision but names no section or direction: the skill asks for clarification before editing.
10. A user asks to sync README and README front-matter already matches `VISION.md`: the skill reports no content changes.
11. A historical proposal references `vision.md`: no update is required solely because the reference is historical.
12. A request says `vision mirror`: the skill may treat it as README sync intent, but it does not require or report `mirror` mode.

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

- AC1. Root `VISION.md` is the canonical project-vision artifact.
- AC2. The `vision` skill validates as a canonical skill and uses state-based behavior.
- AC3. The `vision` skill preserves safe establishment, update, and README sync behavior.
- AC4. The `vision` skill preserves substantive/editorial confirmation and causal-link gating for substantive changes.
- AC5. README front-matter links to `VISION.md` and remains marker-bounded.
- AC6. Proposal guidance requires `Vision fit` against `VISION.md` for new and substantively revised proposals.
- AC7. Proposal-review checks `Vision fit` against `VISION.md` and preserves explicit exception requirements.
- AC8. The normal lifecycle chain does not include `vision` as a required stage.
- AC9. Active guidance no longer requires root `vision.md` as canonical or user-facing `create`, `revise`, and `mirror` operating modes.
- AC10. Still-valid vision safety and quality rules remain present after retiring the old path and mode model.

## Open questions

None.

## Next artifacts

- code-review for the completed M1-M3 implementation
- verify
- explain-change
- pr

## Follow-on artifacts

- `spec-review`: approved on 2026-04-30 after R81 workflow-fit placement and R91 mode-table wording were made directly testable.
- `spec-review`: approved on 2026-05-01 after the no-vision and migration-recognized legacy `vision.md` behavior was clarified for the `VISION.md` migration.
- Execution plan: [2026-05-01 Vision Skill Simplification and VISION.md Migration](../docs/plans/2026-05-01-vision-skill-simplification-and-vision-md-migration.md)
- Test spec update: [Vision Skill Test Spec](vision-skill.test.md) is active for the consolidated vision skill contract.
- Focused migration test spec: [Vision Skill Simplification and VISION.md Migration Test Spec](vision-skill-simplification-and-vision-md-migration.test.md)
- M3 implementation: generated-output refresh and lifecycle evidence updates completed.

## Readiness

Approved after `spec-review`; the linked execution plan and matching test specs track downstream implementation and review state for the consolidated vision skill contract.
