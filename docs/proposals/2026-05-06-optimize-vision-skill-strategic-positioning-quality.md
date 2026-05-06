# Optimize Vision Skill Strategic Positioning Quality

## Status

accepted

## Problem

The current `vision` skill is strong at safe editing, artifact authority, README synchronization, and consistent Markdown structure. It is weaker at the most important vision task: identifying the project's strategic center before writing.

That gap produced a legacy RigorLoop vision that framed the project as a "Git-first starter kit." The phrase was not wrong as an implementation constraint, but it made the substrate the headline. The better framing is that RigorLoop is a rigorous software engineering workflow for AI coding agents, using specification-driven development, test-driven development, human-in-the-loop review, requirements traceability, and design-implementation consistency verification.

The skill needs to optimize for positioning quality, not only document shape.

## Goals

- Make generated and revised visions name the true project category, not merely the repository or tooling substrate.
- Preserve the current skill's edit authorization, README front-matter safety, canonical `VISION.md` handling, security boundaries, and concise Markdown discipline.
- Add explicit guidance for methodology, workflow, protocol, and operating-model projects.
- Improve pitch, differentiator, commitments, refusals, and falsifiability quality.
- Add validation coverage so future skill edits do not regress to low-level framing when a higher-level category is present.
- Retire lowercase `vision.md` handling across active user-facing guidance and repository validation now that root `VISION.md` is the canonical project-vision artifact.
- Preserve strategic-positioning rationale in an ordinary project artifact at `docs/vision/strategic-positioning.md` when the positioning pass materially shapes the vision.

## Non-goals

- Do not turn `VISION.md` into a proposal, spec, architecture document, roadmap, or task tracker.
- Do not remove repository-state, existing-vision, security, research, or README marker safety rules.
- Do not make `vision` a normal lifecycle stage.
- Do not require external research for ordinary vision drafting.
- Do not force every project into the RigorLoop methodology pattern.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not make `docs/vision/strategic-positioning.md` independently authoritative over `VISION.md`.

## Vision fit

fits the current vision

The proposal directly supports the current vision by improving the skill that maintains project identity. It strengthens RigorLoop's commitment to durable context, proposal-fit review, source-of-truth clarity, and reviewable rationale without changing the vision itself.

## Context

`VISION.md` is the canonical project-vision artifact. README front-matter is derived from it, and `CONSTITUTION.md` outranks it for governance. The `vision` skill is upstream of the normal per-change lifecycle and is used at project genesis or when accumulated evidence shows that the current vision no longer reflects the project.

The old lowercase `vision.md` path was temporary migration state. This proposal retires that handling across active user-facing guidance and repo-owned validation, including `vision`, `proposal`, and `proposal-review` skill instructions, active specs and tests, selector classification, conflict validation, and fixtures. Historical records may still mention lowercase path text, but active behavior should no longer treat lowercase `vision.md` as migration input, a supported project-vision surface, or a no-vision gate exception.

The current skill already defines strong safety mechanics: state-based edit authorization, README marker boundaries, privacy and research boundaries, section shape, word count, and required reporting. Existing specs and tests cover those mechanics in `specs/vision-skill.md`, `specs/vision-skill.test.md`, and `scripts/test-skill-validator.py`.

The observed gap is strategic positioning. The skill has drafting heuristics, but they do not force a pre-drafting answer to category, audience, pain, promise, mechanism, alternatives, tradeoff, compatibility surfaces, refusals, and falsifiability. That allowed a compatibility surface, Git, to become the headline instead of the higher-level project category.

For RigorLoop's own skill-development repository, `specs/vision-skill.md` and `specs/vision-skill.test.md` are the right places to define and verify `vision` skill behavior. For ordinary projects using RigorLoop, those files may not exist. The strategic-positioning pass therefore needs a durable project-local location under `docs/` instead of living only in final assistant output or in RigorLoop's skill-development specs.

## Options considered

### Option 0: Keep the skill unchanged

This preserves stability, but it leaves the quality gap unresolved. Future visions can remain structurally valid while strategically weak.

### Option 1: Only add more examples

Examples help, but they are easy to overfit and do not enforce a general reasoning method. The skill needs a process for discovering the strategic center, not only sample prose.

### Option 2: Replace the whole skill

This is unnecessary and risky. The current skill's state-based editing, README synchronization, security boundaries, and output reporting rules are useful and should remain.

### Option 3: Add a strategic-positioning layer to the existing skill

This is the recommended option. Keep the current safety and artifact controls, but add a mandatory pre-drafting positioning pass, anti-anchor rule, methodology-as-product carve-out, pitch-quality check, calibrated word budget, optional methodology sections, and final quality gates.

## Recommended direction

Adopt Option 3.

The optimized skill should first identify the strategic center of the project, then write or update `VISION.md`. The generated prose should make compatibility surfaces visible without mistaking them for the core promise.

`VISION.md` should normally stay at or under 750 words. For methodology, protocol, workflow, or operating-model projects, the owner may explicitly allow up to 900 words when needed to explain the project category, methodology pillars, tradeoff, refusals, and falsifiability. The skill should still avoid feature lists, architecture, roadmap content, implementation detail, and requirements language.

For initial visions and materially repositioned visions, the strategic-positioning pass should be written to `docs/vision/strategic-positioning.md` as a supporting rationale artifact. `VISION.md` remains the canonical public-facing vision. The positioning artifact explains the category, user, pain, promise, mechanism, alternatives, tradeoff, compatibility surfaces, refusals, and falsifiability used to draft or revise the vision.

Authority rule: `VISION.md` is the canonical project-vision artifact. `docs/vision/strategic-positioning.md` is supporting rationale. If they conflict, update the positioning rationale or revise `VISION.md` through a substantive vision update; do not treat the rationale as independently authoritative.

For RigorLoop-style inputs, the skill should naturally converge on this kind of framing:

> RigorLoop is a rigorous software engineering workflow for AI coding agents. It turns product intent into traceable requirements, tests, architecture, plans, implementation, and verification evidence so humans can review agent-produced changes with confidence.

Git, CI, and pull requests can remain in the vision, but as compatibility surfaces rather than the headline.

The intended artifact split is:

- `VISION.md`: canonical concise project identity and public-facing vision.
- `docs/vision/strategic-positioning.md`: durable positioning rationale behind the vision and review aid.
- README vision front-matter: short derived summary from `VISION.md`.
- `docs/changes/<change-id>/explain-change.md`: change-local rationale when a substantive repositioning occurs.
- `specs/vision-skill.md`: RigorLoop-internal contract for developing the `vision` skill itself.

## Expected behavior changes

- Before drafting or materially revising `VISION.md`, the `vision` skill identifies project category, primary user, primary pain, primary promise, core mechanism, alternatives, tradeoff, compatibility surfaces, refusals, and falsifiability.
- The first sentence is checked against the highest-level project category implied by the inputs.
- Repository layout, Git, CI, pull requests, runtime, package format, hosting platform, language, and template mechanics are treated as compatibility surfaces unless the owner explicitly chooses them as the project category or they are genuinely the product.
- Methodology, workflow, protocol, and operating-model pillars are allowed in the vision when they define the product identity.
- The pitch and differentiator answer category, audience, outcome, mechanism, alternative class, and tradeoff across the opening sections.
- `VISION.md` normally stays at or under 750 words.
- Methodology, protocol, workflow, or operating-model visions may go up to 900 words only when the owner explicitly allows it and the extra space is needed for category, methodology pillars, tradeoff, refusals, or falsifiability.
- The skill still avoids feature lists, architecture, roadmap content, implementation detail, and requirements language.
- For initial visions, the skill creates `VISION.md` and `docs/vision/strategic-positioning.md`, and optionally creates or syncs README front-matter when marker rules allow it.
- For materially repositioned visions, the skill updates both `VISION.md` and `docs/vision/strategic-positioning.md`.
- For substantive repositioning in repositories that use change-local packs, `docs/changes/<change-id>/explain-change.md` summarizes the positioning delta and links to `docs/vision/strategic-positioning.md`.
- For initial visions and materially repositioned visions, the skill reports a concise strategic-positioning summary in final output and points to the durable positioning artifact.
- For editorial updates, README sync, or narrow section edits, the strategic-positioning pass remains internal and `docs/vision/strategic-positioning.md` is not updated unless strategic assumptions changed or a conflict is revealed.
- For methodology, workflow, protocol, or operating-model projects, the skill may add one optional methodology-oriented section when available inputs identify concrete methodology pillars or an operating loop.
- If the owner has not supplied enough detail for methodology structure, the skill keeps the standard sections and reports an open vision-level question instead of inventing that structure.
- Active user-facing guidance and repository validation no longer preserve lowercase `vision.md` migration behavior; root `VISION.md` remains the only supported project-vision artifact.
- Final quality gates catch weak positioning before the skill reports completion.

## Architecture impact

The canonical implementation target is `skills/vision/SKILL.md`. Generated Codex runtime output under `.codex/skills/vision/SKILL.md` and public adapter output under `dist/adapters/` should be refreshed only through repository generators.

The change likely touches:

- `skills/vision/SKILL.md`
- `skills/proposal/SKILL.md`
- `skills/proposal-review/SKILL.md`
- `docs/vision/strategic-positioning.md` behavior in the skill contract and tests
- `.codex/skills/vision/SKILL.md`, generated from canonical skills
- `dist/adapters/*/.../skills/vision/SKILL.md`, generated adapter output
- `specs/vision-skill.md`
- `specs/vision-skill.test.md`
- `scripts/validation_selection.py`
- `scripts/test-skill-validator.py`
- `scripts/test-select-validation.py`
- possibly `scripts/validate-skills.py` or related fixtures if lightweight quality checks become script-owned instead of test-only assertions

No runtime data flow, storage, network boundary, or deployment boundary is expected.

## Testing and verification strategy

Use static assertions, contract tests, and existing generator drift checks. This slice should not add a prompt-output evaluation harness.

Candidate coverage:

- Static skill-validator assertions for the strategic-positioning pass, anti-anchor rule, methodology-as-product rule, pitch-quality check, word-budget policy, optional-section rule, reporting behavior, and final quality gates.
- Static RigorLoop-style methodology assertions proving the skill tells agents to lead with the AI-agent software engineering workflow or methodology category, treat Git and CI as compatibility surfaces, include methodology pillars as the core mechanism, and avoid "Git-first starter kit" as the category.
- Static ordinary-product assertions proving implementation substrates such as WinUI, MSIX, and Shell APIs should not be over-centered when the user-facing product category is a Windows-native file manager.
- Static true-substrate assertions proving Git can be the lead category when the project is actually a Git extension.
- Static assertions proving active `vision`, `proposal`, and `proposal-review` skill guidance does not preserve lowercase `vision.md` migration handling.
- Selector regression assertions proving lowercase `vision.md` is no longer classified as a supported root vision surface, no longer participates in root vision conflict blocking, and no longer serves as a no-vision gate exception.
- Static assertions for `docs/vision/strategic-positioning.md` creation and update triggers, authority wording, expected worksheet sections, editorial no-update behavior, and change-local link behavior for substantive repositioning.
- README marker and generated-output drift checks to preserve existing safety behavior.

Expected validation includes focused skill tests, skill validation, generated skill drift checks, adapter drift checks, artifact lifecycle validation, and selector-selected CI for changed paths.

## Rollout and rollback

Roll out as a normal workflow-governance change. Update the proposal-driven spec and test spec first, then amend the canonical `vision` skill, add regression coverage, regenerate derived skill and adapter outputs through repository generators, and run selector-selected validation.

Rollback is straightforward: revert the skill/spec/test changes and regenerated outputs. Existing `VISION.md` files remain valid because the proposal changes drafting guidance and supporting rationale behavior, not the canonical vision path or README marker contract. Any generated `docs/vision/strategic-positioning.md` artifact can be kept as historical rationale or removed in the same rollback if it was created only by the reverted behavior.

## Risks and mitigations

- Risk: the skill may produce visions that are too long. Mitigation: keep the normal cap at 750 words, require explicit owner permission for the 900-word methodology cap, and require concise sections.
- Risk: methodology sections could become feature lists. Mitigation: allow at most one optional methodology-oriented section, require concrete methodology pillars or an operating loop from inputs, and keep the content high-level.
- Risk: the anti-anchor rule may hide important substrate commitments. Mitigation: allow substrates in the vision as compatibility surfaces or differentiators when they are genuinely strategic.
- Risk: examples could overfit to RigorLoop. Mitigation: include fixtures where the substrate is and is not the true category.
- Risk: quality gates become subjective and hard to test. Mitigation: encode the durable checks as static skill contract assertions and leave judgment-heavy quality assessment to proposal/spec review rather than building a prompt-output harness in this slice.
- Risk: the positioning rationale could be mistaken for a second vision source of truth. Mitigation: require explicit authority wording that `VISION.md` remains canonical and the rationale only explains derivation.
- Risk: the positioning artifact becomes stale after editorial edits. Mitigation: do not update it for editorial work, and update it only when strategic assumptions change or conflict with `VISION.md`.
- Risk: removing lowercase path handling could break a repository still mid-migration. Mitigation: this repository has completed the migration and ordinary user-facing guidance should point to `VISION.md`; any historical lowercase references remain archival only, not active behavior.

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-06 | Recommend adding a strategic-positioning layer to the existing `vision` skill. | Preserves current safety and source-of-truth mechanics while addressing the actual positioning failure. | Keep unchanged; add examples only; replace the whole skill. |
| 2026-05-06 | Set the normal vision cap to 750 words, with owner-authorized 900-word allowance for methodology, protocol, workflow, and operating-model projects. | Gives strategic visions enough room for category, pillars, tradeoff, refusals, and falsifiability while preserving concision. | Keep the 500-word cap; allow 900 words by default. |
| 2026-05-06 | Report a concise strategic-positioning summary only for initial or materially repositioned visions by default. | Makes strategic assumptions reviewable when they matter without adding noise to editorial updates or README sync. | Always report the positioning pass; never report it unless asked. |
| 2026-05-06 | Allow at most one optional methodology-oriented section when inputs identify concrete methodology pillars or an operating loop. | Supports methodology-as-product without encouraging invented structure or feature-list visions. | Always add methodology sections; never allow optional sections. |
| 2026-05-06 | Use static assertions for the first regression slice. | Keeps validation lightweight and reviewable while covering the strategic-positioning contract. | Add a prompt-output quality harness in this slice. |
| 2026-05-06 | Retire lowercase `vision.md` handling across active user-facing guidance and repository validation. | The temporary migration path is no longer the project-vision source of truth; retaining active instructions and validation exceptions around it adds noise and weakens the canonical `VISION.md` model. | Retire it only from the `vision` skill; preserve temporary migration-path behavior as a permanent safety rule. |
| 2026-05-06 | Preserve strategic-positioning rationale in `docs/vision/strategic-positioning.md` for initial and materially repositioned visions. | Final assistant output is not durable enough for the rationale that materially shapes `VISION.md`; ordinary RigorLoop user projects need a project-local review aid outside RigorLoop's internal skill specs. | Store the worksheet inside `VISION.md`; rely only on final assistant output; rely on `specs/vision-skill.md` in user projects. |

## Next artifacts

- Feature spec update for the `vision` skill strategic-positioning contract.
- Matching test-spec update covering strategic-positioning fixtures, `docs/vision/strategic-positioning.md` behavior, and generated-output drift.
- Execution plan if the accepted spec touches canonical skills, generated outputs, specs, tests, and validation scripts.

## Follow-on artifacts

- `proposal-review`: approved on 2026-05-06 after `PR-1` clarified lowercase `vision.md` retirement scope.
- Proposal-review record: [review-log](../changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-log.md) and [review-resolution](../changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-resolution.md).
- Feature spec update: [Vision Skill](../../specs/vision-skill.md).

## Readiness

Accepted after proposal-review. Ready for feature spec review once the downstream spec update is drafted.
