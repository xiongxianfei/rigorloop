# Vision Skill

## Status

- approved

## Related proposal

- [Vision Skill](../docs/proposals/2026-04-29-vision-skill.md)
- [Vision Skill Quality Refinement](../docs/proposals/2026-04-30-vision-skill-quality-refinement.md)

## Goal and context

This spec defines the contributor-visible contract for a new `vision` skill and the related proposal and proposal-review guidance. The change gives RigorLoop a safe way to create or revise a root `vision.md`, mirror a short generated README front-matter section, and make proposal fit against the project vision explicit.

The vision skill is upstream of the normal per-change workflow. It is not a new lifecycle stage between proposal, spec, architecture, planning, implementation, review, verification, and PR.

The first implementation of this spec adds the skill and routing guidance. It does not create the initial `vision.md`; that project-level content is created later by explicitly invoking the accepted skill in `create` mode.

This revision defines a quality refinement for the already-shipped skill. The refinement keeps the approved vision contract intact while adding drafting heuristics, consolidating overlapping edit-authorization guidance, moving workflow-fit guidance before detailed mode behavior, and replacing advisory substantive-revision traceability with an enforceable causal-link rule.

The approved root `vision.md` is not revised by this spec update.

## Glossary

- `vision.md`: the canonical project vision document at the repository root.
- README front-matter: the README section between `<!-- vision:start -->` and `<!-- vision:end -->`, generated from `vision.md`.
- marker pair: the exact `<!-- vision:start -->` and `<!-- vision:end -->` comments that bound generated README front-matter.
- create mode: the `vision` skill mode that creates `vision.md` and README front-matter when no current vision exists.
- revise mode: the `vision` skill mode that updates a named part of an existing `vision.md` and mirrors README front-matter.
- mirror mode: the `vision` skill mode that leaves `vision.md` unchanged and regenerates README front-matter from it.
- substantive revision: a vision change caused by a proposal, incident, learning, or project-direction drift.
- editorial revision: a typo, wording, or README mirror-only change that does not change project meaning.
- drafting heuristics: non-normative authoring questions in the `vision` skill that help produce sharper vision text before finalizing generated or revised content.
- edit authorization: the skill guidance that says which source is canonical and which modes may edit `vision.md` or README front-matter.
- `Vision fit`: a proposal section that states how the proposed direction relates to `vision.md`.
- explicit exception: a proposal-review outcome that allows a proposal to proceed despite a vision conflict without revising the proposal or vision.

## Examples first

### Example E1: create mode creates the first vision only when invoked

Given the repository has no `vision.md`
And the accepted `vision` skill exists
When the user invokes `vision create`
Then the skill creates root `vision.md`
And the skill inserts or regenerates README front-matter between the marker pair
And the skill summarizes assumptions and open vision-level questions.

### Example E2: adding the skill does not create the initial vision

Given this spec is implemented
When `skills/vision/SKILL.md` and generated skill output are added
Then no root `vision.md` is created unless the user separately invokes the accepted skill in create mode.

### Example E3: existing vision with unclear mode is protected

Given `vision.md` exists
When the user invokes the `vision` skill without `revise` or `mirror` intent
Then the skill stops and asks which mode applies
And it does not overwrite `vision.md`.

### Example E4: mirror mode edits only README front-matter

Given `vision.md` exists
And README contains one valid marker pair
When the user invokes `vision mirror`
Then `vision.md` remains unchanged
And only content between the marker pair changes in README.

### Example E5: proposals expose vision fit

Given `vision.md` exists
When the proposal skill creates a new proposal
Then the proposal includes a `Vision fit` section
And the section states one of the approved vision-fit values.

### Example E6: no vision exists yet is explicit

Given no root `vision.md` exists
When the proposal skill creates a new proposal after this spec is adopted
Then the proposal includes `Vision fit`
And the section states `no vision exists yet`.

### Example E7: proposal-review classifies a vision conflict

Given `vision.md` exists
And a proposal says `may conflict with the current vision`
When proposal-review confirms the conflict
Then the review outcome identifies whether the next action is revise proposal, revise vision, or record explicit exception.

### Example E8: drafting heuristics catch weak first drafts

Given the user invokes `vision create`
When the skill drafts the initial vision
Then the skill uses drafting questions for differentiator, pain points, checkable commitments, observable falsifiability, audience fit, and scope refusals before finalizing the vision text.

### Example E9: competitor naming remains optional

Given the skill asks how the project differs from alternatives
When naming a specific competitor would date the vision or create unnecessary positioning risk
Then the skill may name an alternative class instead of a specific tool.

### Example E10: substantive revision traceability is enforced

Given `vision.md` exists
And a substantive revise-mode invocation is tied to an existing or required change-local pack
When the causal link is absent from the required change-local artifacts
Then the skill stops before finalizing and reports the missing traceability record.

### Example E11: workflow fit is visible before mechanics

Given a contributor opens the `vision` skill
When they read the opening guidance
Then they see that the skill is upstream of the per-change workflow before detailed mode behavior.

## Requirements

R1. The repository MUST add a canonical authored `vision` skill under `skills/vision/SKILL.md`.

R2. The `vision` skill metadata MUST use `name: vision`.

R3. The `vision` skill description MUST state that it produces or updates the project vision and matching README front-matter.

R4. The `vision` skill MUST define exactly these operating modes: `create`, `revise`, and `mirror`.

R5. If no root `vision.md` exists and the user does not specify a mode, the `vision` skill MUST treat the request as create mode only when the request is clearly asking to produce the project vision.

R6. If root `vision.md` exists and the user does not clearly specify `revise` or `mirror`, the `vision` skill MUST stop and ask which mode applies before editing.

R7. Create mode MUST create `vision.md` at the repository root, not under `docs/`.

R8. The first implementation of this spec MUST NOT create root `vision.md` merely because it adds the `vision` skill.

R9. The `vision` skill MUST treat `vision.md` as canonical over README front-matter.

R10. The README front-matter MUST be bounded by the exact marker pair:

```markdown
<!-- vision:start -->
<!-- vision:end -->
```

R11. The `vision` skill MUST NOT edit README content outside the marker pair except for explicit marker insertion in create mode.

R12. If marker insertion is needed in create mode, the skill MUST preserve existing README content order and insert one marker-bounded front-matter block at the deterministic README location defined by R69 through R73.

R13. If README has malformed, nested, or multiple vision marker pairs, the `vision` skill MUST stop and request explicit handling instead of rewriting README broadly.

R14. Mirror mode MUST leave `vision.md` unchanged.

R15. Mirror mode MUST regenerate README front-matter from `vision.md`.

R16. Revise mode MUST update only the named vision section unless the skill states why the requested change necessarily cascades to another section.

R17. Revise mode MUST regenerate README front-matter after changing `vision.md`.

R18. A substantive revise-mode invocation MUST ask or confirm whether the revision is substantive or editorial before finalizing the output.

R19. For substantive revisions tied to an existing or required change-local pack, the `vision` skill MUST require the causal link to be recorded in the relevant `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing.

R20. Editorial revisions and mirror-only changes MUST NOT require a new change-local pack solely because the vision skill ran.

R21. `vision.md` generated or revised by the skill MUST be no more than 500 words.

R22. `vision.md` generated or revised by the skill MUST use plain language and MUST NOT use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary.

R23. `vision.md` generated or revised by the skill MUST NOT include implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, priority columns, or feature lists.

R24. `vision.md` generated or revised by the skill MUST include sections, in order, covering pitch, differentiator, target audience, non-audience, commitments, refusals, falsifiability, and optional open questions.

R25. README front-matter generated by the skill MUST include only the pitch, differentiator, target audience, and a link to `vision.md` for goals, non-goals, and falsifiability.

R26. README front-matter generated by the skill MUST be derived from `vision.md` rather than independently authored.

R27. The `vision` skill MUST report the changed output paths and summarize assumptions or open vision-level questions after create or revise mode.

R28. The `vision` skill MUST report that `vision.md` was unchanged after mirror mode.

R29. The `proposal` skill MUST require a `Vision fit` section in every new proposal it creates after this spec is adopted.

R30. The `proposal` skill MUST require a `Vision fit` section when it substantively revises an existing proposal after this spec is adopted.

R31. Legacy proposals that are not substantively revised after this spec is adopted MUST NOT be considered invalid solely because they lack `Vision fit`.

R32. The `Vision fit` section MUST state exactly one of:

- `fits the current vision`;
- `may conflict with the current vision`;
- `intentionally proposes a vision revision`;
- `no vision exists yet`.

R33. If root `vision.md` exists, `Vision fit` MUST NOT use `no vision exists yet`.

R34. If root `vision.md` does not exist, `Vision fit` MUST use `no vision exists yet`.

R35. A proposal MUST NOT silently redefine project vision outside the `Vision fit` section and normal proposal rationale.

R36. The `proposal-review` skill MUST check a proposal's `Vision fit` section.

R37. If a proposal created or substantively revised after this spec is adopted lacks `Vision fit`, proposal-review MUST request revision.

R38. If proposal-review finds a conflict with `vision.md`, the review MUST classify the required outcome as revise proposal, revise vision, or record explicit exception.

R39. A proposal-review explicit exception MUST include the evidence for the conflict, required outcome, and rationale for why the exception is safer than revising the proposal or vision.

R40. The `vision` skill MUST be described as upstream of the per-change workflow, not as a normal lifecycle stage.

R41. The first implementation MUST NOT add `vision` to the normal full-lifecycle chain between existing workflow stages.

R42. The first implementation MUST NOT add a required helper script for README front-matter mirroring.

R43. Generated `.codex/skills/` output MUST be refreshed only through `scripts/build-skills.py`.

R44. Generated public adapter output under `dist/adapters/` MUST be refreshed only through `scripts/build-adapters.py`.

R45. Generated adapter packages MUST include the `vision` skill when it satisfies existing adapter portability rules.

R46. `vision.md` MUST be the canonical project-vision and proposal-fit reference, subordinate to `CONSTITUTION.md`. It MUST NOT replace specs, proposals, architecture artifacts, or execution plans.

R47. The repository source-of-truth order for the vision surface MUST be:

1. `CONSTITUTION.md` for repository governance, source boundaries, and workflow principles;
2. `vision.md` for project identity, target users, commitments, refusals, and proposal-fit reference;
3. `specs/` for durable behavior and workflow contracts;
4. proposals for change-level direction and tradeoff selection;
5. README front-matter for generated summaries of `vision.md`.

R48. Adding the `vision` skill and `vision.md` contract MUST update `CONSTITUTION.md`.

R49. Adding the `vision` skill and `vision.md` contract MUST update `AGENTS.md`.

R50. Adding the `vision` skill and `vision.md` contract MUST update `docs/workflows.md` if it documents proposal flow or project-start flow.

R51. Adding the `vision` skill and `vision.md` contract MUST update README ownership guidance if README ownership guidance exists.

R52. Governance, workflow, and ownership guidance updated for this change MUST state that `vision.md` is the canonical project-vision artifact.

R53. Governance, workflow, and ownership guidance updated for this change MUST state that proposals created or substantively revised after this spec is adopted include `Vision fit`.

R54. Governance, workflow, and ownership guidance updated for this change MUST state that README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `vision.md`.

R55. Governance, workflow, and ownership guidance updated for this change MUST state that README front-matter is not the source of truth when it conflicts with `vision.md`.

R56. Every `vision` skill run MUST report the mode used: `create`, `revise`, or `mirror`.

R57. Every `vision` skill run MUST report files changed.

R58. Every `vision` skill run MUST report whether README front-matter was created, replaced, or left unchanged.

R59. Create mode output MUST report assumptions made.

R60. Revise mode output MUST report sections changed.

R61. `vision.md` and generated README front-matter MUST NOT include secrets, credentials, private local filesystem paths, private machine names, or personal data not explicitly intended for publication.

R62. If sensitive or private content is present in inputs, the `vision` skill MUST omit it or ask for explicit confirmation before including it.

R63. The `vision` skill MUST NOT fetch external information unless the user explicitly requests research or the workflow invokes a research-backed mode before vision drafting.

R64. If external research is used, the `vision` skill output MUST distinguish researched facts from project assumptions.

R65. `vision.md` MUST be readable as plain Markdown.

R66. `vision.md` MUST NOT require rendered tables, diagrams, HTML layout, or generated assets to understand the project vision.

R67. The `vision` skill SHOULD start from compact project inputs when available: `CONSTITUTION.md`, `AGENTS.md`, README front-matter, existing `vision.md`, and recent proposal summaries.

R68. The `vision` skill SHOULD escalate to full-file reads only when compact inputs are missing, conflicting, or insufficient to determine project-level framing.

R69. When create mode generates README front-matter, the skill MUST insert the marker block deterministically.

R70. If README contains an existing valid `<!-- vision:start -->` and `<!-- vision:end -->` block, the skill MUST replace only content inside the marker block and preserve all content outside the markers.

R71. If README has no marker block and contains a first Markdown H1 heading, the skill MUST insert the marker block immediately after the first H1 block and preserve all existing content after the inserted marker block.

R72. For README marker insertion, the first H1 block MUST be the first line matching `# <title>` plus any immediately following badge/image lines or blank lines directly attached to the heading.

R73. If README has no H1 heading, the skill MUST insert the marker block at the start of the file and preserve all existing content after the inserted marker block.

R74. The skill MUST NOT edit README content outside the marker block except to insert the marker block when it is missing.

R75. If a proposal conflicts with `vision.md`, proposal-review MUST choose one of: revise the proposal, revise `vision.md`, or record an explicit exception.

R76. An explicit vision-conflict exception MUST include approving owner or owning stage, evidence for the conflict, why proposal revision is not chosen, why vision revision is not chosen, where the exception is recorded, and whether the exception is one-time or establishes a future vision-revision trigger.

R77. An explicit vision-conflict exception MUST be recorded in both the proposal's `Vision fit` section and the proposal-review output.

R78. If a proposal with an explicit vision-conflict exception is part of a non-trivial change, the exception SHOULD also be summarized in `explain-change.md`.

R79. `README.md` MUST be classified as a supported `readme` validation surface when it is touched by the vision-skill implementation.

R80. Selector routing MUST select lightweight README validation for changed `README.md`, and MUST select vision marker validation when a standalone vision marker block is present or when the `vision` skill is in scope.

R81. The `vision` skill MUST place workflow-fit guidance immediately after the opening purpose/scope paragraphs and before any Inputs to read, Modes, README behavior, Rules, Output paths, or Failure modes sections. The workflow-fit guidance MUST be visible before detailed mode behavior begins.

R82. The `vision` skill MUST include drafting heuristics after vision content guidance and before README front-matter guidance.

R83. Drafting heuristics MUST be phrased as authoring questions or checks, not as additional required `vision.md` sections.

R84. Drafting heuristics MUST ask how the project differs from an alternative class or specific tool and what tradeoff the project makes.

R85. Drafting heuristics MUST ask whether project pain points are embedded in the differentiator rather than presented as an unrelated complaint list.

R86. Drafting heuristics MUST ask whether commitments are concrete enough for a future reviewer to check.

R87. Drafting heuristics MUST ask whether falsifiability conditions are observable from behavior or artifacts.

R88. Drafting heuristics MUST ask whether the audience statement rules out at least one plausible non-fit.

R89. Drafting heuristics MUST ask whether scope refusals are concrete enough to block misaligned proposals.

R90. Drafting heuristics MUST allow either an alternative class or a specific tool for differentiator comparison; they MUST NOT require naming a specific competitor.

R91. The `vision` skill MUST present `create`, `revise`, and `mirror` mode behavior in one Markdown table. The table MUST include columns for Mode, When it applies, Authorized edits, README behavior, and Stop or clarification conditions. The table MUST include exactly one row for each mode: `create`, `revise`, and `mirror`.

R92. The `vision` skill MUST consolidate source-of-truth, mode authorization, and existing-vision overwrite protection into one edit-authorization section.

R93. The edit-authorization section MUST state that `CONSTITUTION.md` outranks `vision.md`, `vision.md` outranks README front-matter, create/revise/mirror are the only authorized edit paths, and existing visions are not overwritten without clear revise or mirror intent.

R94. Revise-mode output for a substantive revision MUST report whether the required causal link was recorded or not required.

## Inputs and outputs

Inputs:

- user invocation argument: project idea, `create`, `revise <section>`, or `mirror`;
- root `vision.md`, when present;
- README front-matter, when present;
- project context from `AGENTS.md`, `CONSTITUTION.md`, README, project map, recent proposals, research, and exploration artifacts when present.

Outputs:

- `vision.md` in create and revise mode when the skill is invoked for vision authoring;
- README front-matter between the marker pair in create, revise, and mirror mode when the skill is invoked for README mirroring;
- `skills/vision/SKILL.md` as the canonical authored skill;
- updated `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` guidance when proposal-fit behavior changes;
- generated `.codex/skills/` and `dist/adapters/` output after canonical skill changes and existing generator runs.

Quality-refinement outputs are limited to the `vision` skill contract and generated skill or adapter output unless spec review identifies drift in another authoritative surface.

## State and invariants

- `vision.md` is the canonical project vision.
- `vision.md` is subordinate to `CONSTITUTION.md` and does not replace specs, proposals, architecture artifacts, or execution plans.
- README front-matter is generated from `vision.md` and is not independently authoritative.
- The vision skill is upstream of the per-change workflow.
- Adding the skill and creating the initial vision are separate actions.
- Content outside README vision markers remains author-owned.
- Generated skill and adapter output remains derived from canonical authored skill sources.
- `README.md` is a classified validation surface for this implementation, not a PR-mode `unclassified-path` blocker.
- Drafting heuristics guide authoring quality but do not change the required vision sections, 500-word cap, README marker behavior, or source-of-truth order.

## Error and boundary behavior

- Existing `vision.md` plus unclear mode stops for clarification.
- Missing `vision.md` plus a mirror request stops because there is no canonical source to mirror.
- Missing `vision.md` plus a revise request stops because there is no existing section to revise.
- Missing or malformed README markers outside create-mode marker insertion require explicit handling.
- A generated or revised `vision.md` over 500 words is invalid and must be shortened before completion.
- A proposal with a stale or missing `Vision fit` section after this spec applies must be revised before proposal-review can approve it.
- A substantive vision revision tied to an existing or required change-local pack stops before finalization when the causal link is missing from the required change-local artifacts.

## Compatibility and migration

Existing proposals, README content, and workflow artifacts remain valid when this spec is adopted. Existing proposals are grandfathered until they are substantively revised.

The first skill implementation was completed before a root `vision.md` existed. A root `vision.md` now exists and remains out of scope for this refinement.

When canonical skills change, generated `.codex/skills/` and `dist/adapters/` output must be refreshed through existing generators so adapter packages remain deterministic.

Rollback for the quality refinement reverts the touched canonical spec and skill guidance, then reruns existing generators. It does not remove the previously approved `vision` skill or root `vision.md`.

## Observability

The skill's normal response follows R56 through R60 and R94. For revise mode, the response states whether the revision was substantive or editorial when that classification was determined.

Validation output remains the existing repository-owned skill, generated-output, adapter, lifecycle, README, and selector validation output.

## Security and privacy

Sensitive information and external research boundaries are governed by R61 through R64.

## Accessibility and UX

No application UI is involved. Plain Markdown readability is governed by R65 and R66.

## Performance expectations

No runtime performance behavior is introduced. Evidence collection behavior is governed by R67 and R68.

## Edge cases

1. Root `vision.md` exists and README lacks markers: mirror mode stops unless the user explicitly authorizes marker insertion.
2. Root `vision.md` does not exist and README already has markers: create mode may replace the content between the marker pair after creating `vision.md`.
3. README contains two `<!-- vision:start -->` markers: the skill stops for explicit handling.
4. A proposal created after adoption says `fits the current vision` while no `vision.md` exists: proposal-review requests revision to `no vision exists yet`.
5. A proposal created after adoption omits `Vision fit`: proposal-review requests revision.
6. A vision revision changes project scope but is labeled editorial: the skill must surface the mismatch and treat it as substantive or ask for clarification.
7. A user asks to revise an unnamed section: the skill asks which section is being revised before editing.
8. A user asks mirror mode and README front-matter already matches `vision.md`: the skill reports no content changes.
9. A generated adapter omits `vision` even though portability rules include it: adapter validation or drift checking must fail through existing generated-output checks.
10. A legacy proposal without `Vision fit` is read for history only: no revision is required solely for that absence.
11. A first-draft vision names no alternatives and states only abstract values: the drafting heuristics prompt comparative positioning and checkable commitments before finalization.
12. A substantive vision revision has an existing change-local pack but no causal link: the skill stops before finalizing until the link is recorded or the revision is reclassified with rationale.
13. A differentiator can compare against an alternative class without naming a specific competitor: the skill accepts that comparison when it explains the tradeoff.

## Non-goals

- Create the initial project `vision.md` as part of adding the skill.
- Make `vision` a normal per-change workflow stage.
- Add validator enforcement for vision prose quality in the first implementation.
- Add a README mirror helper script in the first implementation.
- Rewrite existing proposals to add `Vision fit`.
- Turn the vision into a roadmap, feature list, status tracker, requirements spec, architecture document, or project-management system.
- Change adapter portability rules beyond adding the new canonical skill source.
- Revise the approved root `vision.md` as part of the quality refinement.
- Require specific competitor names in generated or revised vision text.
- Extract or consolidate shared evidence-collection guidance across skills.
- Change the 500-word cap or required section order for `vision.md`.

## Acceptance criteria

- AC1. `skills/vision/SKILL.md` exists, validates as a canonical skill, and documents create, revise, and mirror mode behavior.
- AC2. The first implementation does not create root `vision.md`.
- AC3. `skills/proposal/SKILL.md` requires `Vision fit` for new and substantively revised proposals after adoption.
- AC4. `skills/proposal-review/SKILL.md` checks `Vision fit` and classifies confirmed conflicts.
- AC5. `docs/workflows.md` or other workflow guidance updated by the implementation does not add `vision` to the normal lifecycle chain.
- AC6. Generated `.codex/skills/` output is synchronized through `scripts/build-skills.py`.
- AC7. Generated `dist/adapters/` output is synchronized through `scripts/build-adapters.py`.
- AC8. README marker ownership is documented in the skill without requiring a helper script.
- AC9. Existing validation selectors identify the changed skill, generated-output, lifecycle, workflow, and README surfaces without requiring broad smoke unless an authoritative trigger adds it; `README.md` must not block PR-mode CI as `unclassified-path`.
- AC10. `CONSTITUTION.md`, `AGENTS.md`, and applicable workflow or README ownership guidance document the `vision.md` source-of-truth boundary.
- AC11. README marker insertion behavior is deterministic and preserves content outside the generated marker block.
- AC12. Proposal-review explicit exceptions for vision conflicts include owner or stage, evidence, rationale against proposal and vision revision, recording location, and future-trigger classification.
- AC13. The `vision` skill contains drafting heuristics covering differentiator comparison, pain points, checkable commitments, observable falsifiability, audience fit, and refusals.
- AC14. The drafting heuristics allow an alternative class or specific tool and do not require naming a specific competitor.
- AC15. The `vision` skill places workflow-fit guidance immediately after the opening purpose/scope paragraphs and before Inputs to read, Modes, README behavior, Rules, Output paths, or Failure modes sections.
- AC16. The `vision` skill presents create, revise, and mirror mode behavior in one Markdown table with exactly the required columns and exactly one row for each mode.
- AC17. The `vision` skill consolidates source-of-truth, mode authorization, and existing-vision overwrite protection into one edit-authorization section.
- AC18. Substantive revise-mode guidance requires the causal link before finalizing when a change-local pack exists or is required.
- AC19. Shared evidence-collection guidance remains outside the refinement scope.

## Open questions

- None.

## Next artifacts

- code-review for the completed M1-M3 implementation

## Follow-on artifacts

- `spec-review`: approved on 2026-04-30 after R81 workflow-fit placement and R91 mode-table wording were made directly testable.
- Execution plan: [2026-04-30 Vision skill quality refinement](../docs/plans/2026-04-30-vision-skill-quality-refinement.md)
- `plan-review`: approved on 2026-04-30 with no material findings.
- Test spec update: [Vision Skill Test Spec](vision-skill.test.md) is active for the 2026-04-30 refinement.
- Implementation: M1-M3 are complete and final implementation proof is recorded in the active plan and change-local evidence.

## Readiness

Approved after `spec-review`; the linked execution plan passed `plan-review`, the matching test spec is active, and implementation closeout is ready for first-pass `code-review`.

Immediate next repository stage: `code-review` for the completed M1-M3 implementation in `docs/plans/2026-04-30-vision-skill-quality-refinement.md`.
