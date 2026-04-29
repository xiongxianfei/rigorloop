# Vision Skill

## Status

- approved

## Related proposal

- [Vision Skill](../docs/proposals/2026-04-29-vision-skill.md)

## Goal and context

This spec defines the contributor-visible contract for a new `vision` skill and the related proposal and proposal-review guidance. The change gives RigorLoop a safe way to create or revise a root `vision.md`, mirror a short generated README front-matter section, and make proposal fit against the project vision explicit.

The vision skill is upstream of the normal per-change workflow. It is not a new lifecycle stage between proposal, spec, architecture, planning, implementation, review, verification, and PR.

The first implementation of this spec adds the skill and routing guidance. It does not create the initial `vision.md`; that project-level content is created later by explicitly invoking the accepted skill in `create` mode.

## Glossary

- `vision.md`: the canonical project vision document at the repository root.
- README front-matter: the README section between `<!-- vision:start -->` and `<!-- vision:end -->`, generated from `vision.md`.
- marker pair: the exact `<!-- vision:start -->` and `<!-- vision:end -->` comments that bound generated README front-matter.
- create mode: the `vision` skill mode that creates `vision.md` and README front-matter when no current vision exists.
- revise mode: the `vision` skill mode that updates a named part of an existing `vision.md` and mirrors README front-matter.
- mirror mode: the `vision` skill mode that leaves `vision.md` unchanged and regenerates README front-matter from it.
- substantive revision: a vision change caused by a proposal, incident, learning, or project-direction drift.
- editorial revision: a typo, wording, or README mirror-only change that does not change project meaning.
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

R19. For substantive revisions, the `vision` skill MUST remind the contributor to record the causal link in the relevant `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` when a change-local pack exists.

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

## Inputs and outputs

Inputs:

- user invocation argument: project idea, `create`, `revise <section>`, or `mirror`;
- root `vision.md`, when present;
- README front-matter, when present;
- project context from `AGENTS.md`, `CONSTITUTION.md`, README, project map, recent proposals, research, and exploration artifacts when present.

Outputs:

- `vision.md` in create and revise mode;
- README front-matter between the marker pair in create, revise, and mirror mode;
- `skills/vision/SKILL.md` as the canonical authored skill;
- updated `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` guidance;
- generated `.codex/skills/` and `dist/adapters/` output after the existing generators run.

## State and invariants

- `vision.md` is the canonical project vision.
- `vision.md` is subordinate to `CONSTITUTION.md` and does not replace specs, proposals, architecture artifacts, or execution plans.
- README front-matter is generated from `vision.md` and is not independently authoritative.
- The vision skill is upstream of the per-change workflow.
- Adding the skill and creating the initial vision are separate actions.
- Content outside README vision markers remains author-owned.
- Generated skill and adapter output remains derived from canonical authored skill sources.

## Error and boundary behavior

- Existing `vision.md` plus unclear mode stops for clarification.
- Missing `vision.md` plus a mirror request stops because there is no canonical source to mirror.
- Missing `vision.md` plus a revise request stops because there is no existing section to revise.
- Missing or malformed README markers outside create-mode marker insertion require explicit handling.
- A generated or revised `vision.md` over 500 words is invalid and must be shortened before completion.
- A proposal with a stale or missing `Vision fit` section after this spec applies must be revised before proposal-review can approve it.

## Compatibility and migration

Existing proposals, README content, and workflow artifacts remain valid when this spec is adopted. Existing proposals are grandfathered until they are substantively revised.

The repository currently has no root `vision.md`. The first skill implementation therefore changes skill and guidance surfaces only. The initial `vision.md` and README front-matter are created later through explicit `vision create` use and review.

When canonical skills change, generated `.codex/skills/` and `dist/adapters/` output must be refreshed through existing generators so adapter packages remain deterministic.

Rollback removes the canonical `vision` skill, reverts proposal/proposal-review guidance, reruns existing generators, and either keeps or removes any later `vision.md` according to the rollback decision for that separate vision-authoring change.

## Observability

The skill's normal response follows R56 through R60. For revise mode, the response states whether the revision was substantive or editorial when that classification was determined.

Validation output remains the existing repository-owned skill, generated-output, adapter, lifecycle, and selector validation output.

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

## Non-goals

- Create the initial project `vision.md` as part of adding the skill.
- Make `vision` a normal per-change workflow stage.
- Add validator enforcement for vision prose quality in the first implementation.
- Add a README mirror helper script in the first implementation.
- Rewrite existing proposals to add `Vision fit`.
- Turn the vision into a roadmap, feature list, status tracker, requirements spec, architecture document, or project-management system.
- Change adapter portability rules beyond adding the new canonical skill source.

## Acceptance criteria

- AC1. `skills/vision/SKILL.md` exists, validates as a canonical skill, and documents create, revise, and mirror mode behavior.
- AC2. The first implementation does not create root `vision.md`.
- AC3. `skills/proposal/SKILL.md` requires `Vision fit` for new and substantively revised proposals after adoption.
- AC4. `skills/proposal-review/SKILL.md` checks `Vision fit` and classifies confirmed conflicts.
- AC5. `docs/workflows.md` or other workflow guidance updated by the implementation does not add `vision` to the normal lifecycle chain.
- AC6. Generated `.codex/skills/` output is synchronized through `scripts/build-skills.py`.
- AC7. Generated `dist/adapters/` output is synchronized through `scripts/build-adapters.py`.
- AC8. README marker ownership is documented in the skill without requiring a helper script.
- AC9. Existing validation selectors identify the changed skill, generated-output, lifecycle, and workflow surfaces without requiring broad smoke unless an authoritative trigger adds it.
- AC10. `CONSTITUTION.md`, `AGENTS.md`, and applicable workflow or README ownership guidance document the `vision.md` source-of-truth boundary.
- AC11. README marker insertion behavior is deterministic and preserves content outside the generated marker block.
- AC12. Proposal-review explicit exceptions for vision conflicts include owner or stage, evidence, rationale against proposal and vision revision, recording location, and future-trigger classification.

## Open questions

- None.

## Next artifacts

- execution plan
- test spec after plan approval

## Follow-on artifacts

- None yet.

## Readiness

This spec is approved. The immediate next repository stage is `plan`; eventual `test-spec` readiness is conditional on plan approval.
