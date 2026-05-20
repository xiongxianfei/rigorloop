# Skill Contract

## Status

- approved

## Related proposal

- [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md)
- [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md)
- [RigorLoop Published Skill Design Contract](../docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md)
- [Assets-First Progressive Disclosure Pilot for Published Skills](../docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md)
- [Spec and Test-Spec Structural Hygiene](../docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md)

## Goal and context

This spec defines the contributor-visible contract for RigorLoop skill guidance. A skill is an operational guide for one agent capability or workflow stage. It should be small enough to scan, explicit about local ownership, and clear about what it can and cannot claim.

The problem this spec addresses is recurring state and handoff confusion. Skills can accidentally blur progress, readiness, closeout, final Done state, review outcome, validation proof, branch readiness, and PR readiness. The skill contract prevents those overclaims by standardizing core sections, result output, claim boundaries, shared-policy blocks, evidence-reading rules, public skill surface boundaries, generated-output handling, and minimum viable skill creation rules.

Skills are also a published user-facing interface. Repository-maintainer guidance for authoring, generating, validating, or packaging this repository's skills belongs in contributor and governance surfaces, not inside shipped skill text.

This spec owns skill-contract behavior. `specs/rigorloop-workflow.md` continues to own stage order, stage obligation, handoff, and downstream-blocking semantics.

This amendment tightens the published skill portability contract with exact allowed project-portable surfaces, blocked RigorLoop repository-internal surfaces, and static-check scope.

This amendment also tightens token-cost discipline for normalized skills. Token-cost discipline is part of normalized skill behavior. It teaches agents to select the smallest evidence surface that can answer the current question while preserving correctness, validation coverage, review obligations, artifact obligations, and workflow gates.

This amendment defines the published-skill design contract for portable operating documentation. It makes `description` the routing source, distinguishes repository-root internals from packaged skill-local resources, requires resource maps when packaged resources exist, defines published-skill design pilot routing-test evidence, and constrains the published-skill design pilot to an audit plus a `proposal` and `proposal-review` pilot.

This amendment defines the assets-first progressive disclosure pilot for published skills. It adds a follow-on `plan` pilot that ships exactly four normative structural templates under `skills/plan/assets/`, keeps rules in `skills/plan/SKILL.md`, requires deterministic asset resource-map validation, proves adapter packaging for non-empty skill-local assets, and requires both behavior parity and measurable common-path improvement.

This amendment defines structural hygiene for this spec and its matching test spec. It adds slice navigation and grouping while preserving existing R-clause IDs, clause text, acceptance-criterion text, test-case IDs, and cross-references.

## Spec growth strategy

This spec amends through accretion: each accepted amendment adds a clause band to a single file rather than splitting the file. Accretion is sustainable while ownership remains clear and the file remains navigable.

Structural hygiene MUST be applied per amendment when this spec exceeds about 1200 lines or has absorbed more than about 6 slice families. Hygiene work groups clauses by slice, adds navigation aids, and prunes stale cross-references. Hygiene work MUST NOT change clause text, IDs, or numbering.

Splitting this spec into multiple files MUST be pursued through a separate proposal that defends the ownership boundary along which the split occurs. Splits MUST NOT happen as part of a content amendment.

## Glossary

- `skill`: a `SKILL.md` operational guide that tells an agent when and how to perform a repository capability.
- `published skill text`: skill instructions shipped to users through local skill mirrors or public adapter packages.
- `contributor-maintenance guidance`: instructions for contributors maintaining this repository's canonical skill source, generated mirrors, adapter output, validators, and release packaging.
- `canonical skill source`: an authored skill file under `skills/<skill>/SKILL.md`.
- `generated skill mirror`: derived local Codex runtime output under `.codex/skills/`.
- `adapter output`: derived public adapter package output under `dist/adapters/`.
- `normalized skill`: a skill that has been updated to satisfy this spec's required core sections, claim boundaries, and result-output contract.
- `required core section`: a section every normalized skill must include.
- `conditional section`: a section used only when relevant to a skill's artifact, proof, review, milestone, generated-output, or failure behavior.
- `skill type`: a broad category such as authoring, review, execution, periodic, on-demand, or support.
- `claim boundary`: the set of outcomes a skill may state as proven and the outcomes it must leave to another stage or owning artifact.
- `overclaim`: a statement that implies a downstream stage, proof, or lifecycle state has passed when the current skill does not own that proof.
- `result block`: the compact `## Result` summary at the start of a skill's expected output.
- `shared skill policy block`: canonical wording under `templates/shared/<block-name>.md` that is copied verbatim into consuming skills and checked for drift.
- `minimum viable skill`: the smallest justified new skill that owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.
- `ci-maintenance`: the visible workflow stage label for CI infrastructure maintenance. The existing `ci` skill remains the skill entrypoint for that stage label unless a later approved spec changes it.
- `token-cost discipline`: selecting the smallest evidence surface that can answer the current question before broadening.
- `bounded evidence`: a small evidence surface such as a changed-path list, inventory, heading list, stable ID, count, matching line number, or targeted excerpt.
- `high-volume surface`: a file set, artifact, log, generated output tree, or historical record set likely to produce large output.
- `output cap`: a tool or command setting that truncates returned text. Output caps are safety rails, not evidence-selection strategy.
- `routing description`: the frontmatter `description` field that must contain portable skill-selection guidance.
- `workflow role`: a short section that states a lifecycle skill's stage role, received input, produced output, and downstream claim boundary.
- `packaged skill resource`: a file shipped inside the installed skill package, such as `<skill>/references/`, `<skill>/scripts/`, or `<skill>/assets/`.
- `packaged asset`: a structural template shipped under a skill-local `assets/` directory and copied into an output artifact when the resource map says to use it.
- `normative asset`: a packaged asset whose structure is part of the reviewed output contract for the skill.
- `structural fingerprint`: a validator-recomputed digest of normalized asset structure used to detect unacknowledged asset drift.
- `reference corpus`: contract-era artifacts used as strict behavior-parity references.
- `historical corpus`: pre-contract artifacts used for coverage gap analysis rather than strict structural parity.
- `repository-root internal path`: a RigorLoop maintainer-only path such as root `specs/`, root `schemas/`, root `scripts/`, root `dist/`, root `benchmarks/`, or maintainer-only docs.
- `routing fixture`: a representative prompt used to evaluate description coverage and transcript behavior without claiming deterministic model auto-selection.

## Spec navigation

This spec covers four current concerns, organized by slice:

| Slice | Clause band | Examples | Parent proposal |
|---|---|---|---|
| Foundational | R1-R7 | E1, E3 | [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md) |
| Baseline normalization first slice | R8-R26 | E1, E2, E4, E5, E6, E7 | [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md) |
| Published-skill design pilot | R27-R36 | E8-E12 | [RigorLoop Published Skill Design Contract](../docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md) |
| Assets-first plan pilot | R37-R45 | E13-E16 | [Assets-First Progressive Disclosure Pilot for Published Skills](../docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md) |

The Examples section remains a single sequence because some examples are cross-cutting. The Requirement and Acceptance criteria sections use slice headers for direct navigation.

Cross-cutting glossary entries appear in the Glossary section. Slice terminology disambiguation appears in the Slice terminology section.

## Slice terminology

This spec uses two rollout labels:

- `baseline normalization first slice`: the historical skill-contract optimization slice covering `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`.
- `published-skill design pilot`: the R27 through R36 amendment slice covering `proposal`, `proposal-review`, validator changes needed for the pilot, and generated adapter validation for changed skills.
- `assets-first plan pilot`: the R37 through R45 amendment slice covering `skills/plan/SKILL.md`, exactly four normative assets under `skills/plan/assets/`, validator and adapter proof for packaged assets, token-cost measurement, and plan behavior-parity evidence.

Do not use the unqualified phrase `first implementation slice` when the intended slice could be ambiguous.

## Examples first

### Example E1: baseline normalization execution skill avoids review overclaim

Given `skills/implement/SKILL.md` is normalized in the baseline normalization first slice
When the skill reports successful implementation for a milestone
Then its output may state implementation work and targeted validation are complete
And it may state the next stage is `code-review`
But it must not claim review passed, branch-ready, PR-ready, or ready-for-final-closeout.

### Example E2: non-baseline-slice skill is not blocked immediately

Given `skills/proposal/SKILL.md` has not yet been normalized
When the baseline normalization first slice normalizes `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`
Then the baseline normalization first slice remains valid
And `proposal` is normalized in the later core-lifecycle wave.

### Example E3: shared block is copied and checked

Given `templates/shared/review-isolation-and-recording.md` is the shared review recording block
When a formal review skill adopts that block
Then the skill copies the block verbatim
And validator checks compare the copied subsection to the shared source.

### Example E4: generated skill output is not edited directly

Given `skills/code-review/SKILL.md` changes
When generated Codex and adapter skill outputs are refreshed
Then `.codex/skills/code-review/SKILL.md` and affected `dist/adapters/**/code-review/SKILL.md` are derived outputs
And contributors do not hand-edit those generated copies
But the published `code-review` skill text does not expose repository-local generation paths, selector path constraints, or shared-block implementation details.

### Example E5: baseline validator uses narrow overclaim checks

Given the baseline normalization first slice adds validation checks for `skills/verify/SKILL.md`
When the validator checks overclaim wording
Then it prefers required positive wording such as `branch-ready`
And it blocks narrow historically dangerous PR-readiness claims
But it does not perform broad natural-language quality scoring.

### Example E6: one-off helper behavior does not create a skill

Given a contributor wants a one-time formatting checklist
When the behavior does not own a distinct artifact, gate, review responsibility, recurring action, or approved operational process
Then the contributor updates an existing skill, template, or docs surface instead of adding a new skill.

### Example E7: CI stage label and skill entrypoint differ

Given the workflow stage label is `ci-maintenance`
When contributors invoke the current skill entrypoint
Then they use the existing `ci` skill for CI infrastructure maintenance
And the spec does not require a `skills/ci-maintenance/SKILL.md` path.

### Example E8: description carries portable routing

Given a published `proposal-review` skill
When an adapter lists available skills before loading skill bodies
Then the `description` contains the review capability, trigger contexts, and important near-miss boundaries
And no required routing logic exists only in `SKILL.md` or optional `when_to_use` metadata.

### Example E9: packaged scripts are allowed when mapped

Given a skill ships `scripts/validate_review_artifact.py` inside the skill package
When `SKILL.md` includes a `Resource map`
Then the resource map states when to run the script, what input it expects, how to interpret output or exit code, and what to do on failure
And the published-skill portability check does not reject the packaged script merely because its path contains `scripts/`.

### Example E10: repository-root scripts are not customer dependencies

Given a published skill tells a customer project to run root `scripts/build-adapters.py`
When that script is not packaged with the skill and is not project-local
Then published-skill portability validation fails because the skill requires a RigorLoop repository-root internal path.

### Example E11: published-skill design pilot routing fixtures are not model-selection proof

Given a pilot skill includes positive, casual positive, edge positive, near negative, competing-skill, and should-not-trigger prompts
When the published-skill design pilot validates those fixtures
Then validation may prove fixture coverage and support transcript review
But it must not claim deterministic runtime skill auto-selection unless an approved routing harness exists.

### Example E12: audit records but does not retire skills

Given the published-skill design pilot audit identifies a weak skill candidate
When the audit records the candidate
Then it records the skill name, reason, affected artifacts or gates, likely owner, and whether separate approval is required
But it does not merge, retire, rename, remove, or change ownership of that skill in the published-skill design pilot.

### Example E13: plan asset resource map copies templates

Given the assets-first plan pilot ships `assets/milestone.md`
When `skills/plan/SKILL.md` includes a `Resource map`
Then the resource map uses the literal verb `COPY`
And it states when to copy `assets/milestone.md`
And it names the fields the agent must fill.

### Example E14: plan skeleton owns section layout

Given `assets/plan-skeleton.md` is normative
When `skills/plan/SKILL.md` describes expected output
Then `SKILL.md` includes only a compact output expectation summary
And `assets/plan-skeleton.md` owns canonical section order, headers, and placeholders
And the full section layout is not duplicated in both files.

### Example E15: handoff asset is not hidden lifecycle policy

Given the assets-first plan pilot ships `assets/current-handoff-summary.md`
When an agent copies that asset
Then the asset provides headings, labels, and placeholders only
And lifecycle status values, transition rules, claim ownership, readiness semantics, and validation requirements remain in `SKILL.md` or governing workflow artifacts.

### Example E16: historical plans are coverage evidence only

Given a historical plan was written before the published-skill design contract era
When the assets-first plan pilot uses it as evidence
Then strict structural parity is not required
And gap analysis records whether the new `plan` skill can cover the same planning concerns.

## Requirements

### Foundational (R1-R7)

R1. The normative skill contract MUST live in `specs/skill-contract.md`.

R1a. `specs/skill-contract.md` MUST own standard skill shape, claim boundaries, result output expectations, shared-block rules, public skill surface boundaries, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules.

R1b. `specs/rigorloop-workflow.md` MUST continue to own stage order, stage obligation, handoff, and downstream-blocking semantics.

R1c. `docs/workflows.md` and `AGENTS.md` MAY summarize this contract but MUST NOT override it.

R1d. `skills/*/SKILL.md` MUST implement local operating guidance that is consistent with this spec after each skill is normalized.

R2. Canonical skill source MUST remain under `skills/<skill>/SKILL.md`.

R2a. Generated skill mirrors under `.codex/skills/` MUST be treated as derived output.

R2b. Adapter output under `dist/adapters/` MUST be treated as derived output.

R2c. Contributors MUST NOT hand-edit `.codex/skills/` or `dist/adapters/` to satisfy this spec.

R2d. When canonical skill source changes, generated skill mirrors and adapter output MUST be regenerated or checked according to the active plan and validation commands.

R3. A normalized skill MUST include these required core sections:
- `Purpose`
- `When to use`
- `When not to use`
- `Inputs to read`
- `Outputs`
- `Handoff`
- `Stop conditions`
- `Claims this skill must not make`

R3a. A normalized skill MAY keep or add conditional sections when relevant, including:
- `Preconditions`
- `Workflow`
- `Validation / proof`
- `Failure modes`
- `Examples`
- `Required artifact sections`
- `Review finding format`
- `Milestone state rules`

R3b. Normalization MUST preserve skill-specific guidance that changes behavior, artifact shape, review format, validation, or stop conditions.

R3c. Normalization MUST NOT flatten useful domain-specific sections into generic prose when those sections make the skill safer or easier to review.

R3d. Published skill text MUST NOT include repository-maintainer-only source, generation, packaging, selector-path, or shared-block implementation instructions.

R3e. Published skill text MUST NOT direct end users to this repository's internal spec path for full routing rules. It MUST route full workflow questions through the `workflow` skill or another user-facing workflow instruction surface.

R3f. Published skill text MAY reference portable project surfaces such as:
- `AGENTS.md`;
- `docs/workflows.md`;
- `VISION.md`;
- `docs/changes/<change-id>/`;
- `docs/plans/<plan>.md`;
- local workflow contract, if the adopting project has one;
- project validation command, when supplied by the adopting project.

R3g. Published skill text MUST NOT reference RigorLoop repository-internal surfaces such as:
- `specs/rigorloop-workflow.md`;
- `specs/skill-contract.md`;
- `.codex/skills/`;
- `dist/adapters/`;
- `scripts/select-validation.py`;
- `scripts/build-adapters.py`;
- `templates/shared/`;
- RigorLoop-local examples;
- selector path constraints;
- drift-check mechanics;
- shared-block implementation mechanics.

R3h. Published skill text MUST use project-portable wording such as project workflow guide, local workflow contract, project validation command, generated skill output, and adapter output when this project uses adapters.

R3i. Published skill portability checks MUST apply to canonical skill files shipped to users, generated public skill copies, and public adapter skill copies.

R3j. Published skill portability checks MUST NOT apply to internal specs, plans, tests, generator scripts, maintainer docs, or repository-only contributor docs.

R3k. Internal RigorLoop repository details MAY remain in specs, tests, plans, maintainer docs, generator code, and repository-only contributor docs.

R3l. Static validation for published skill portability MUST be narrow and phrase- or path-based. It MUST fail on unqualified references to RigorLoop repository-internal paths or commands in published skill text, while allowing the project-portable surfaces listed in `R3f`.

R3m. Body `When to use` and `When not to use` sections MUST NOT replace frontmatter `description` as the portable routing source.

R3n. Body `When to use` and `When not to use` sections MAY summarize invocation scope, local stop conditions, or competing RigorLoop skills after the skill has loaded, but required selection logic MUST remain present in `description`.

R3o. Validators SHOULD check that `description` is independently sufficient for routing and SHOULD NOT require body sections to restate every trigger.

R4. Normalized authoring skills MUST define the artifact they produce or update and the required artifact sections or quality checklist that make the output reviewable.

R4a. Authoring skills include `proposal`, `spec`, `architecture`, `plan`, `test-spec`, `explain-change`, and other skills that create or revise durable authoring artifacts.

R5. Normalized review skills MUST define review status vocabulary, checklist coverage, finding format, material finding recording behavior, and artifact-local or change-local closeout expectations.

R5a. Review skills include `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.

R5b. Review skills MUST preserve the governing formal review recording rules when they apply.

R6. Normalized execution skills MUST define proof expectations, state updates, stop conditions, and claims they must not make.

R6a. Execution skills include `implement`, `verify`, `pr`, and `ci`.

R6b. The `ci` skill MUST be treated as the skill entrypoint for the visible `ci-maintenance` workflow stage label unless a later approved spec renames the skill path.

R6c. A skill contract implementation MUST NOT require a `skills/ci-maintenance/SKILL.md` path in this slice.

R7. Normalized periodic, on-demand, or support skills MUST define trigger, output, handoff, stop conditions, and claim boundaries appropriate to their obligation.

R7a. Periodic, on-demand, and support skills include `learn`, `explore`, `research`, `vision`, `project-map`, and `bugfix` when those skills are normalized.

### Baseline normalization first slice (R8-R26)

R8. The baseline normalization first slice MUST normalize only these canonical skills:
- `skills/workflow/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/pr/SKILL.md`
- `skills/learn/SKILL.md`

R8a. The baseline normalization first slice MUST add or align required core sections where missing.

R8b. The baseline normalization first slice MUST add or align do-not-overclaim guidance.

R8c. The baseline normalization first slice MUST add or align compact result output expectations.

R8d. The baseline normalization first slice MUST align milestone, progress, readiness, and closeout wording where relevant.

R8e. The baseline normalization first slice MUST add or align targeted evidence-reading guidance.

R8f. The baseline normalization first slice MUST include generated-output drift checks when canonical skill changes produce generated output changes.

R8g. The baseline normalization first slice MUST NOT normalize every skill.

R8h. The baseline normalization first slice MUST keep repository-maintainer generated-output handling out of published skill text.

R9. Later-phase normalization MUST proceed in the order approved by the proposal unless a later approved proposal changes the order.

R9a. Phase 2 MUST normalize core lifecycle authoring and review skills: `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `explain-change`, and the `ci` skill for the `ci-maintenance` stage label.

R9b. Phase 3 MUST normalize on-demand and standing or living-reference skills: `explore`, `research`, `vision`, `project-map`, and `bugfix`.

R9c. Phase 4 MUST normalize newly adopted optional skills only when those skills exist and own approved artifacts or gates.

R9d. Phase 4 candidate names include `ui-design`, `ui-design-review`, `workflow-contract`, and `adopt-rigorloop`; this spec does not create those skills.

R10. A normalized skill MUST include `Claims this skill must not make`.

R10a. `implement` MUST NOT claim review passed, clean review, branch-ready, PR-ready, or ready-for-final-closeout.

R10b. `code-review` MUST NOT claim branch-ready, PR-ready, CI passed, or verification passed.

R10c. `verify` MUST NOT claim PR-ready, PR body ready, or review passed.

R10d. `pr` MUST NOT claim implementation, review, verification, or tests passed unless the claim is linked to owning evidence.

R10e. `plan` MUST distinguish Done, complete, ready for PR, and ready for final closeout from remaining-gates wording.

R10f. `learn` MUST NOT create new workflow policy unless the lesson is routed to an authoritative artifact.

R11. Skill result output MUST be summary-first.

R11a. A normalized skill's expected output MUST start with or require a compact `## Result` block unless the skill has a reviewed, equivalent summary format.

R11b. The common result block MUST include:
- `Skill`
- `Status`
- `Artifacts changed`
- `Open blockers`
- `Next stage`

R11c. A skill MAY add optional result fields when relevant, including:
- `Validation`
- `Review status`
- `Finding IDs`
- `Milestone state`
- `Readiness`
- `Follow-ups`
- `Recommended direction`
- `Next artifacts`
- `Session path`
- `Lessons captured`

R12. Skill handoff sections MUST stay local.

R12a. A normalized skill's `Handoff` section MUST name the normal next stage, conditional next stages, and stop conditions that are local to the skill.

R12b. A normalized published skill MUST route full workflow questions through the `workflow` skill or another user-facing workflow instruction surface instead of pointing to this repository's internal workflow spec path.

R12c. A skill MUST NOT imply automatic downstream continuation when the governing workflow treats the invocation as isolated.

R13. Planning and execution skills MUST distinguish progress, readiness, closeout, and Done when those concepts appear.

R13a. `Progress` MUST mean work that has happened so far.

R13b. `Readiness` MUST mean the next stage that can happen.

R13c. `Closeout` MUST mean the current artifact or stage satisfied its checklist.

R13d. `Done` MUST mean final lifecycle state after required gates are complete.

R13e. `Ready for final closeout` MUST NOT be represented as Done, PR-ready, or branch-ready.

R13f. Plans that mention `Ready for final closeout` SHOULD pair it with remaining completion gates when ambiguity is possible.

R14. Shared skill policy blocks MUST live under `templates/shared/<block-name>.md`.

R14a. Shared skill policy blocks MUST be treated as canonical authored sources for copied skill subsections.

R14b. In v1, consuming skills MUST copy adopted shared blocks verbatim.

R14c. `scripts/test-skill-validator.py` or another repo-owned validation script MUST compare copied shared blocks to the shared source when drift checking is adopted.

R14d. Shared blocks MUST NOT replace or outrank the workflow spec or this skill-contract spec.

R14e. Shared-block generation into skills MUST NOT be added in the baseline normalization first slice.

R15. The first published-skill shared-block set MUST include only stable rules approved for v1:
- `review-isolation-and-recording`
- `evidence-collection-efficiency`

R15b. The following shared blocks MUST remain deferred until a later approved change stabilizes them:
- `vision-fit`
- `plan-readiness-vs-completion`
- `milestone-aware-review-handoff`
- `first-pass-completeness`
- `material-finding-requirements`, if still under active simplification

R15c. `generated-output-handling` is contributor-maintenance guidance, not a v1 shared block. Do not keep an unused `templates/shared/generated-output-handling.md` source unless a later approved change adopts it for an actual contributor-facing consumer.

R16. Evidence-reading guidance in normalized skills MUST prefer targeted evidence before broad reads.

R16a. Normalized skills SHOULD start from summaries, stable IDs, headings, targeted sections, check IDs, file paths, counts, or line citations.

R16b. Normalized skills MUST allow full-file reads when the whole file is the review target, relevant sections cannot be isolated safely, surrounding context can change the conclusion, bounded searches conflict or are incomplete, or behavior-changing edits depend on the whole source-of-truth artifact.

R16c. Evidence-reading guidance MUST NOT weaken exact artifact review obligations when exact wording matters.

R17. Examples in normalized skills MUST be optional and bounded.

R17a. A skill MAY include one minimal valid example and one invalid example when those examples prevent recurring errors.

R17b. Long examples MUST live in `examples/`, templates, or another appropriate artifact rather than inside skill files.

R18. Forbidden-overclaim validation MUST be narrow and incident-based.

R18a. Validators SHOULD prefer positive required wording checks over forbidden phrase checks.

R18b. Validators MAY check a small list of historically dangerous phrases for `implement`, `code-review`, `verify`, `pr`, `plan`, and `learn`.

R18c. Validators MUST NOT perform broad semantic quality scoring in the baseline normalization first slice.

R18d. Forbidden phrase checks MUST avoid blocking explicit negative guidance such as "Do not set Ready for final closeout from implement."

R19. A new skill SHOULD be added only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.

R19a. Contributors SHOULD NOT add a skill for one-off helper behavior, a tiny formatting rule, or a checklist that belongs inside an existing skill.

R19b. `docs/workflows.md` and `AGENTS.md` MAY summarize the minimum viable skill rule.

R19c. Detailed examples and templates for creating skills SHOULD live in skill-creator guidance, such as `templates/skill.md` or `docs/skills/creating-skills.md`.

R20. The skill contract implementation MUST preserve source-of-truth order.

R20a. If a skill, generated output, adapter output, contributor summary, or shared block conflicts with this spec on skill-contract behavior, this spec wins unless a higher-priority artifact applies.

R20b. If this spec conflicts with `specs/rigorloop-workflow.md` on stage order, stage obligation, handoff, or downstream blocking, `specs/rigorloop-workflow.md` wins for those workflow-routing semantics.

R21. Token-cost discipline MUST be part of normalized skill behavior.

R21a. Token-cost discipline MUST be implemented as an amendment to this skill contract, not as a new workflow stage.

R21b. Token-cost discipline MUST NOT reduce required validation coverage, review obligations, artifact obligations, or workflow stage gates.

R22. Normalized skills that collect evidence from high-volume surfaces MUST prefer bounded evidence before broad reads.

R22a. Bounded evidence includes inventories, changed paths, headings, stable IDs, requirement IDs, test IDs, check IDs, path lists, counts, matching line numbers, diffs, and targeted excerpts.

R22b. Skills MUST guide agents to broaden from bounded evidence to neighboring context or full-file reads only when bounded evidence is insufficient for the current decision.

R22c. Skills MUST NOT present a broad recursive search, generated-output dump, validation-log dump, or full-file read as the default first step for high-volume surfaces.

R23. Output caps MUST be treated as safety rails, not evidence-selection strategy.

R23a. Skill guidance MUST NOT imply that setting an output cap makes a broad query acceptable as the normal first pass.

R23b. Skill guidance SHOULD name low-volume query strategies such as filename-first searches, count-first searches, precise globs, stable IDs, and targeted range reads when those examples fit the skill.

R24. Summary-first and failure-focused output MUST preserve validation semantics.

R24a. Normal output budgets MAY reduce routine output volume.

R24b. Normal output budgets MUST NOT change selected check coverage, command exit behavior, failure detection, or required validation evidence.

R24c. When a command or skill output omits detail for readability, it MUST say how to request or obtain the omitted detail when the omission affects reviewability.

R25. Static validation for token-cost discipline MUST be narrow and reviewable.

R25a. Static validation MUST check token-cost guidance through stable sections, phrases, examples, or requirement coverage.

R25b. Static validation MUST preserve full-file-read escape conditions.

R25c. Static validation MUST check the output-cap distinction where the implementation adds that wording to skill-contract surfaces.

R25d. Static validation MUST NOT perform broad natural-language quality scoring.

R26. Reviewers MAY report broad, noisy evidence collection as a process defect when it materially affects a workflow artifact, review, implementation, or verification result.

R26a. A process-defect finding MUST identify the noisy evidence surface and the safer bounded evidence strategy.

R26b. A process-defect finding MUST NOT require reducing correctness checks, skipping required artifacts, or ignoring full-file-read escape conditions.

### Published-skill design pilot (R27-R36)

R27. Published skills MUST be portable operating documentation for capable agents.

R27a. A published skill MUST teach a specialized workflow, artifact contract, quality gate, validation behavior, tool sequence, or trust boundary that the base model would not reliably perform unaided.

R27b. A published skill MUST NOT rely on maintainers having this repository's internal specs, schemas, scripts, reports, change-local proof packs, or generated adapter output unless those resources are packaged with the skill, supplied by the user, present as project-local artifacts, or the RigorLoop repository itself is the target.

R27c. A published skill MUST NOT hide side effects or authority beyond its name and `description`.

R28. Skill names SHOULD be short, concrete, lowercase, hyphenated, and action- or artifact-oriented.

R28a. A new or retained skill SHOULD be justified by at least one of: repeatable lifecycle procedure, durable artifact contract, domain-specific risk judgment, tool or command sequence, deterministic helper script, output shape the model often gets wrong, or safety or trust boundary.

R28b. Contributors SHOULD reject, merge, or keep out of skill form candidates that are only generic summarization, generic writing advice, generic code help, simple Q&A, one-step tasks, or preferences better handled by project instructions.

R29. The frontmatter `description` MUST be the portable routing source.

R29a. `description` MUST state the skill capability and trigger contexts.

R29b. `description` MUST include important near-miss boundaries when competing skills or common false positives exist.

R29c. `description` MUST NOT be a synonym dump.

R29d. `description` MUST be `<= 1024` characters.

R29e. Optional adapter-specific metadata such as `when_to_use` MAY exist, but required routing logic MUST still be present in `description`.

R29f. Validators MUST evaluate routing coverage against `description`, not require `when_to_use`.

R30. A lifecycle skill MUST include `Workflow role` when it produces or closes a lifecycle artifact, gates a stage, participates in stage handoff, or claims downstream readiness.

R30a. `Workflow role` MUST state the lifecycle role, received input, produced output or status, and downstream claims the skill must not make.

R30b. Non-lifecycle skills MAY omit `Workflow role` when they do not produce or close lifecycle artifacts, gate stages, participate in handoff, or claim downstream readiness.

R31. A skill's body MUST contain execution guidance for the normal workflow path.

R31a. A skill body MUST NOT rely on essential trigger logic that is absent from `description`.

R31b. A skill body SHOULD use imperative instructions for procedure, resource routing, stop conditions, output expectations, and validation.

R31c. A skill body SHOULD explain the rationale for judgment-affecting rules when the rationale helps prevent over-application or under-application.

R31d. Hard-constraint language SHOULD be reserved for security boundaries, privacy constraints, destructive actions, required output formats, claim ownership, formal review recording, schema requirements, and validation requirements.

R32. A skill that ships packaged `references/`, `scripts/`, or `assets/` resources MUST include a `Resource map`.

R32a. The `Resource map` MUST name every packaged resource and state the condition under which the agent should load or use it.

R32b. A skill that ships no packaged resources MUST NOT include a required "No bundled resources" line solely to state absence.

R32c. A skill that references a packaged script MUST state when to run it, what input it expects, what output or exit code means, and what to do on failure.

R32d. Packaged skill-local `<skill>/scripts/` resources MUST NOT be treated as forbidden repository-root `scripts/` dependencies.

R33. Published-skill self-containment validation MUST distinguish repository-root internal paths from packaged skill-local resources.

R33a. Published skills MUST NOT require unavailable repository-root internal paths such as root `specs/`, root `schemas/`, maintainer-only root `docs/`, root `benchmarks/`, root `scripts/`, or root `dist/` as normal customer-project dependencies.

R33b. Published skills MAY use project-local docs when present and relevant, user-provided paths, packaged skill resources, and internal RigorLoop paths when operating inside the RigorLoop repository or when those paths are the target artifact.

R33c. Validators MUST NOT use a blunt path deny-list that rejects every mention of `scripts/`; they MUST distinguish packaged skill scripts from repository-root internal scripts.

R34. Artifact-producing skills MUST include a compact fenced output skeleton or a reviewed equivalent template.

R34a. Examples and counterexamples MAY clarify behavior, but examples MUST NOT replace normative output skeletons.

R34b. Long examples SHOULD live in packaged references, assets, or other appropriate artifacts instead of the common-path `SKILL.md` body.

R35. First-slice routing tests MUST be prompt fixtures and transcript-review inputs unless a dedicated routing harness is approved.

R35a. First-slice routing fixture sets SHOULD include obvious positives, casual positives, edge positives, near negatives, competing-skill prompts, and should-not-trigger prompts for each changed skill.

R35b. Published-skill design pilot routing evidence MAY prove description trigger coverage, near-miss coverage, fixture coverage, and transcript observations about under-triggering, over-triggering, or unnecessary resource loading.

R35c. First-slice routing tests MUST NOT claim deterministic runtime skill auto-selection in CI unless a dedicated, approved routing harness defines that oracle.

R35d. Published-skill design pilot routing validation MUST NOT add broad semantic scoring of skill prose as a required CI gate.

R35e. For each changed published-skill design pilot skill, the implementation MUST provide a routing coverage table in the plan, test spec, or fixture file.

R35f. The routing coverage table MUST identify positive triggers, near misses when relevant, competing skills when relevant, and should-not-trigger prompt classes.

R35g. Static checks MAY validate routing coverage table presence and bounded phrase coverage, but MUST NOT use broad semantic scoring unless a later approved routing harness defines that oracle.

R36. The published-skill design pilot MUST be audit-first and pilot-scoped.

R36a. The published-skill design pilot MUST audit current RigorLoop skills and classify findings such as description routing gaps, missing near-miss boundaries, hidden trigger logic, missing workflow role, missing output template, unavailable internal dependency, missing resource map, validation over-application, under-specified validation, generic skill candidate, script candidate, reference split candidate, example or counterexample candidate, and token-cost risk.

R36b. The published-skill design pilot MUST limit skill body changes to `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, validator changes needed for the pilot, and generated adapter validation for changed skills.

R36c. The published-skill design pilot MUST NOT rewrite all skills.

R36d. The published-skill design pilot audit MAY record merge or retire candidates but MUST NOT merge, retire, rename, remove, or change ownership of any skill.

R36e. Each merge or retire candidate recorded by the audit MUST include skill name, reason it may not earn its existence, affected artifacts or gates, likely owner, and whether a separate proposal or spec amendment is required.

R36f. The pilot token-cost budget target is zero token regression for `proposal` and `proposal-review`; up to `+5%` is tolerated only with recorded rationale, and above `+10%` blocks the pilot unless this spec is revised.

R36g. For each changed published-skill design pilot skill, implementation MUST record a behavior-preservation note.

R36h. The behavior-preservation note MUST identify removed or rewritten behavior-significant wording, why the change is safe, and where the essential rule is preserved.

R36i. The published-skill design pilot MUST include behavior-parity evidence for representative proposal and proposal-review artifacts showing that material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries were not weakened.

R36j. A structural validation pass alone is insufficient to close the published-skill design pilot when a touched skill changed behavior-significant wording.

### Assets-first plan pilot (R37-R45)

R37. The assets-first plan pilot MUST be a follow-on packaged-resource pilot and MUST NOT change the current published-skill design pilot scope unless this spec is explicitly amended and approved.

R37a. Implementation MUST NOT begin while `plan` is part of another active or unresolved skill-contract change unless the active plan or change-local evidence records why the overlap is safe.

R37b. The assets-first plan pilot MUST modify `plan` as the only skill in its asset pilot implementation slice.

R37c. The assets-first plan pilot MUST NOT modify `proposal`, `proposal-review`, `spec`, `spec-review`, `code-review`, `verify`, or `pr`.

R37d. The assets-first plan pilot MUST NOT introduce packaged `references/`, packaged `scripts/`, build-time partials, adapter install-root changes, lockfile changes, or CLI behavior changes.

R38. The assets-first plan pilot MUST ship exactly these four normative assets under `skills/plan/assets/`:
- `plan-skeleton.md`;
- `milestone.md`;
- `current-handoff-summary.md`;
- `decision-log-row.md`.

R38a. The assets-first plan pilot MUST NOT ship optional, example, deprecated, or fifth asset files unless this spec is amended.

R38b. The four normative assets MUST contain structural templates copied and filled by the agent, not paragraph-length workflow procedure, filled example narratives, hidden trigger logic, or policy text that belongs in `SKILL.md` or governing specs.

R38c. The four normative assets MUST NOT require repository-root internal paths as normal customer-project dependencies.

R39. `skills/plan/SKILL.md` MUST include a `Resource map` for the four normative assets.

R39a. Each assets-first plan pilot resource-map entry MUST use the literal verb `COPY`.

R39b. Each assets-first plan pilot resource-map entry MUST name the asset path, state the trigger condition, and name the fields or structures the agent must fill.

R39c. `COPY` is the only allowed verb for `assets/` in this pilot. `READ` is reserved for future `references/`, and `RUN` is reserved for future `scripts/`.

R39d. The `Resource map` MUST instruct the agent not to emit unfilled placeholders.

R40. `assets/plan-skeleton.md` MUST be the reviewed equivalent full output template for the `plan` artifact in the assets-first plan pilot.

R40a. `assets/plan-skeleton.md` MUST own canonical plan section order, headers, and placeholders.

R40b. `skills/plan/SKILL.md` MUST retain a compact output expectation summary that names the expected output shape and points to `assets/plan-skeleton.md` through the `Resource map`.

R40c. `skills/plan/SKILL.md` and `assets/plan-skeleton.md` MUST NOT duplicate the full plan section layout.

R41. `assets/current-handoff-summary.md` MUST contain only section headings, field labels, and placeholders.

R41a. `assets/current-handoff-summary.md` MUST NOT define lifecycle status values, next-stage transition rules, claim ownership, branch-ready semantics, PR-ready semantics, or validation requirements.

R41b. `skills/plan/SKILL.md` MUST retain the rule that the Current Handoff Summary stays consistent with the active plan, plan index, and change metadata.

R41c. If `current-handoff-summary.md` cannot satisfy `R41` through `R41b`, the handoff summary template MUST remain inline in `skills/plan/SKILL.md` for this pilot.

R42. Every assets-first plan pilot asset MUST include metadata comments for template name and version, skill name, template status, structural fingerprint, and maintained-alongside path.

R42a. Asset template status MUST use one of: `normative`, `optional`, `example`, `deprecated`.

R42b. The assets-first plan pilot assets MUST use `normative` status.

R42c. Static validation MUST recompute the structural fingerprint for each normative asset and fail when the recomputed fingerprint differs from the recorded fingerprint without a template-version update.

R42d. Static validation MUST compare the section set for normative assets against the section set referenced by `skills/plan/SKILL.md` resource-map and operating-procedure text when the asset is a full-artifact skeleton.

R42e. Drift MUST be resolved by reverting the structural change or bumping the template version and updating the recorded fingerprint.

R43. Assets-first plan pilot validation MUST be deterministic.

R43a. Static validation MAY check asset count, approved asset paths, required metadata comments, matching `Resource map` entries, literal `COPY`, fields-to-fill wording, visible placeholders, forbidden repository-root required paths, structural fingerprints, section-set parity, and generated adapter asset presence.

R43b. Static validation MUST NOT use broad semantic scoring to decide whether asset prose is too explanatory.

R43c. Prose-heavy asset review MUST use a bounded heuristic declared in the spec, test spec, or plan, or code-review judgment.

R43d. Behavior parity MUST be fixture-based or review-recorded and MUST NOT rely on an unbounded claim that the new plan is similar enough.

R44. The assets-first plan pilot MUST prove both no regression and demonstrated improvement.

R44a. The no-regression gate MUST include behavior-parity evidence showing that required plan sections, milestone shape, decision log shape, current handoff summary, validation evidence, implementation and review handoff, claim boundaries, and recording discipline are not weakened.

R44b. The demonstrated-improvement gate MUST show that `skills/plan/SKILL.md` common-path body token count decreases by at least 15 percent compared with the pre-pilot baseline.

R44c. Total packaged skill content, measured as `skills/plan/SKILL.md` plus assets, MAY grow by up to 5 percent with recorded rationale.

R44d. Total packaged skill content growth above 10 percent MUST block rollout unless this spec is amended.

R44e. The assets-first plan pilot MUST record supporting evidence that `assets/milestone.md` is used once per milestone across the behavior-parity reference corpus.

R45. The assets-first plan pilot behavior-parity corpus MUST separate contract-era reference plans from historical plans.

R45a. The reference corpus MUST include at least three contract-era, contract-compliant plans and MUST use strict structural parity.

R45b. The reference corpus SHOULD include `docs/plans/2026-05-18-skill-readability-self-containment.md`, `docs/plans/2026-05-19-published-skill-design-spec-family.md`, and `docs/plans/2026-05-19-published-skill-design-plan-family.md`.

R45c. The historical corpus MUST include 3 to 5 pre-contract-era plans and MUST use coverage parity, not strict structural parity.

R45d. Historical corpus gaps MUST be recorded in change-local evidence such as `docs/changes/<change-id>/historical-coverage.md`.

R45e. Follow-on packaged-resource proposals MUST choose resource patterns by skill type: constructive skills SHOULD treat `assets/` as the primary pattern for repeated structures, while deliberative skills SHOULD treat `references/` as the primary pattern for rule-heavy judgment guidance.

## Inputs and outputs

Inputs:

- accepted skill-contract proposal;
- accepted assets-first progressive disclosure pilot proposal;
- accepted structural hygiene proposal;
- canonical skill files under `skills/`;
- shared policy blocks under `templates/shared/`;
- generated skill mirrors under `.codex/skills/`;
- generated adapter output under `dist/adapters/`;
- workflow contract in `specs/rigorloop-workflow.md`;
- contributor summaries in `docs/workflows.md` and `AGENTS.md`;
- skill validator and generated-output drift validation scripts.

Outputs:

- `specs/skill-contract.md`;
- structural navigation in `specs/skill-contract.md`;
- normalized canonical skill source for the in-scope slice;
- a skill existence audit for the pilot pair and recorded follow-ons for any merge or retire candidates;
- a routing coverage table for each changed published-skill design pilot skill;
- a behavior-preservation note for each changed published-skill design pilot skill;
- behavior-parity evidence for representative proposal and proposal-review artifacts;
- four normative `plan` assets and their resource-map entries for the assets-first plan pilot;
- structural fingerprint and section-set drift evidence for normative `plan` assets;
- behavior-parity reference and historical corpus evidence for the assets-first plan pilot;
- common-path body token reduction and total packaged content measurements for the assets-first plan pilot;
- copied shared policy blocks where adopted;
- regenerated `.codex/skills/` output when canonical skills change;
- regenerated `dist/adapters/` output when canonical skills change;
- validator checks for required sections, description length and routing coverage, resource-map coverage, self-containment, shared-block drift, generated-output drift, and narrow overclaim assertions;
- contributor summary updates when root or workflow guidance is affected.
- grouped test-spec coverage in `specs/skill-contract.test.md` during the matching test-spec stage.

## State and invariants

- `specs/skill-contract.md` is the normative skill-contract spec.
- `specs/rigorloop-workflow.md` remains the normative workflow-routing spec.
- Canonical skill source lives under `skills/`.
- `.codex/skills/` and `dist/adapters/` are generated outputs.
- A normalized skill owns only its local claims.
- A skill's readiness statement is not proof that downstream gates have passed.
- Public shared blocks are copied and checked in v1, not generated into skills.
- Published skill text does not expose repository-local source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation details, or RigorLoop-local examples.
- Published skill portability checks apply only to shipped skill text and generated public skill copies, not internal maintainer surfaces.
- The baseline normalization first slice is limited to seven canonical skills.
- The `ci` skill remains the entrypoint for the `ci-maintenance` stage label.
- `description` remains the portable routing source for published skills.
- Packaged skill-local resources are allowed only when included in adapter output and mapped in `SKILL.md`.
- Repository-root internal paths are not normal customer-project dependencies.
- The published-skill design pilot does not merge, retire, rename, remove, or change ownership of skills.
- The assets-first plan pilot is limited to `plan`, exactly four normative `assets/` templates, and deterministic validator and adapter proof.
- The assets-first plan pilot keeps workflow rules and lifecycle handoff semantics in `SKILL.md` or governing workflow artifacts, not hidden in assets.
- Normative asset structure is checked for drift through metadata, structural fingerprints, and section-set parity.
- Structural hygiene amendments preserve R-clause IDs, clause text, acceptance-criterion text, test-case IDs, and cross-references.

## Error and boundary behavior

- If a required shared-block source is missing, validation MUST fail or the consuming skill MUST not claim shared-block conformance.
- If a copied shared block drifts from its shared source, validation MUST fail when drift checking is adopted.
- If generated `.codex/skills/` or `dist/adapters/` output drifts from canonical skills, generated-output drift validation MUST fail.
- If a normalized skill cannot satisfy a required core section without creating misleading content, the implementation MUST stop for spec review or owner decision rather than inventing a hollow section.
- If a proposed forbidden phrase check blocks explicit negative guidance, the check MUST be narrowed before it is relied on.
- If the workflow stage label `ci-maintenance` is used in a normalization list, spec and plan authors MUST map it to the existing `ci` skill entrypoint unless a later approved spec renames the skill path.
- If a new optional skill does not yet exist or lacks approved artifact or gate ownership, it MUST NOT be included in implementation scope solely because it is named as a Phase 4 candidate.
- If `description` exceeds 1024 characters, validation MUST fail.
- If a skill ships packaged resources without a `Resource map`, validation MUST fail for that skill.
- If a published skill requires an unavailable repository-root internal path as a customer-project dependency, portability validation MUST fail.
- If a validator cannot distinguish repository-root `scripts/` from packaged skill-local scripts, the validator MUST be narrowed before it is relied on.
- If routing fixtures are used without an approved routing harness, review output MUST NOT claim deterministic model auto-selection.
- If the published-skill design pilot audit identifies a merge or retire candidate, implementation MUST record it as a follow-on instead of acting on it.
- If a changed published-skill design pilot skill lacks a routing coverage table, the pilot MUST NOT claim routing coverage validation is complete.
- If a changed published-skill design pilot skill lacks a behavior-preservation note, the pilot MUST NOT claim behavior-significant wording was safely preserved.
- If behavior-parity evidence shows weakened material review status, finding format, recording obligations, stop conditions, validation obligations, or claim boundaries, the pilot MUST stop for revision before closeout.
- If the assets-first plan pilot ships more or fewer than four assets, validation MUST fail unless this spec is amended.
- If a `plan` asset lacks required metadata comments, validation MUST fail.
- If a normative `plan` asset structural fingerprint drifts without a template-version update, validation MUST fail.
- If the `plan` resource map omits an asset, uses a verb other than `COPY` for an asset, omits trigger conditions, or omits fields to fill, validation MUST fail.
- If `assets/current-handoff-summary.md` defines lifecycle transition rules or readiness semantics, the pilot MUST stop for revision or keep that template inline in `SKILL.md`.
- If `skills/plan/SKILL.md` common-path body token count does not decrease by at least 15 percent, the assets-first plan pilot MUST NOT roll out unless this spec is amended.
- If behavior-parity evidence treats historical plans as strict structural references, the pilot evidence MUST be revised before closeout.
- If a structural hygiene amendment changes existing R-clause text, clause IDs, acceptance-criterion text, test-case IDs, or cross-references, the amendment MUST stop for revision before spec-review approval.
- If a clause is grouped under a slice header that conflicts with the Slice terminology clause band, the amendment MUST stop for revision before spec-review approval.

## Compatibility and migration

- Existing unnormalized skills remain valid until their approved normalization phase.
- The baseline normalization first slice does not require all skills to adopt the required core sections at once.
- Existing contributor generated-output policy remains unchanged: edit canonical skill source, regenerate generated output, and validate drift. That policy is contributor-maintenance guidance and is not copied into published skill text.
- Existing `skills/ci/` path remains valid for `ci-maintenance`.
- Existing formal review recording rules remain authoritative for review records; this spec only defines how shared review guidance is copied and checked in skills.
- Rollback for wording-only skill changes may revert the affected canonical skills, shared blocks, validator checks, and generated output together.
- Existing skills are not invalid solely because their `description` exceeds 1024 characters or lacks the new routing structure until the approved implementation slice brings them into scope.
- Optional `when_to_use` metadata remains compatible when an adapter supports it, but it is not required and does not replace `description`.
- Existing packaged skill resources may remain until their owning skill is in scope, but once the skill is changed for this contract, resource-map coverage applies to packaged resources in that skill.
- Existing `plan` behavior remains the compatibility baseline. Moving structure into assets MUST NOT weaken plan section requirements, handoff consistency, validation evidence, review handoff, or claim boundaries.
- Rollback for the assets-first plan pilot is to reinline asset skeletons into `skills/plan/SKILL.md`, remove `skills/plan/assets/`, and keep validator improvements only when they remain valid for flat skills.
- Structural hygiene rollback is to remove the added navigation aids and slice headers while preserving unchanged clause IDs and cross-references.

## Observability

- Validation output SHOULD identify which required core section, shared block, generated output, or overclaim check failed.
- Selector-selected validation SHOULD classify touched spec, skill, template, generated, adapter, change-local, and review-artifact paths without unclassified paths.
- Review and verification artifacts SHOULD cite validation commands and results rather than generic success claims.
- No runtime logs, metrics, traces, or audit events are required because this is repository guidance behavior, not runtime product behavior.
- Validation output SHOULD identify description-length failures, missing trigger contexts, missing near-miss boundaries, missing resource-map entries, unavailable repository-root dependencies, and routing fixture coverage gaps by stable check ID when those checks are implemented.
- Assets-first plan pilot validation output SHOULD identify asset metadata, resource-map coverage, `COPY` verb, structural fingerprint, section-set parity, adapter asset presence, and token-budget failures by stable check ID when those checks are implemented.
- Structural hygiene validation SHOULD identify any slice-band mismatch, changed clause ID, changed acceptance criterion, changed test-case ID, or broken cross-reference by stable location.

## Security and privacy

- Skill normalization MUST NOT require committing secrets, credentials, tokens, private keys, machine-local paths, or private user data.
- Generated output refreshes MUST preserve the existing security boundary that derived adapter packages do not become independent sources of truth.
- Evidence-reading guidance MUST NOT encourage pasting sensitive logs or secrets into skill output.
- Published skills MUST NOT instruct users to expose secrets, credentials, proxy URLs, private hostnames, tokens, private keys, or raw environment values while using packaged resources or scripts.
- Packaged assets MUST NOT include secrets, credentials, tokens, private keys, machine-local paths, or private user data.

## Accessibility and UX

This change has no user-interface surface. The relevant user experience is contributor readability of skill files and validation output.

## Performance expectations

- Skill validation SHOULD remain static and repository-local in the baseline normalization first slice and published-skill design pilot.
- The baseline normalization first slice and published-skill design pilot MUST NOT add broad natural-language quality scoring.
- Evidence-reading guidance SHOULD reduce unnecessary broad reads by preferring targeted summaries, IDs, headings, line citations, and path lists first.
- Generated-output checks SHOULD use existing build and adapter validation paths unless the approved plan names a narrower or broader proof scope.
- Token-cost static validation MUST stay narrow, phrase-based, and reviewable rather than scoring prose quality.
- `description` length validation MUST be deterministic.
- Routing fixture validation MUST remain deterministic unless a dedicated routing harness defines a stable oracle.
- The pilot token-cost budget MUST be measured for `proposal` and `proposal-review` before rollout expands.
- Behavior-parity evidence for the published-skill design pilot MUST be concrete enough for review without running broad natural-language scoring.
- The assets-first plan pilot common-path body token reduction MUST be measured with a deterministic repository-owned script before rollout.
- Assets-first plan pilot validation MUST remain static and repository-local except for human review of bounded qualitative evidence.

## Edge cases

1. If a skill already has a domain-specific section that overlaps a required core section, normalization may keep both only when the overlap remains clear and non-duplicative.
2. If a skill is both authoring and execution oriented, it must satisfy the required core sections and the relevant conditional sections for both roles.
3. If a clean review skill output has no material findings, formal review recording rules may allow artifact-local settlement; this spec does not require an empty review record.
4. If a shared block is adopted by only one skill initially, the block may still live under `templates/shared/` when the approved plan expects later consumers.
5. If a normalized skill needs an example to prevent a recurring error, the example must remain short enough not to turn the skill into a tutorial.
6. If a generated adapter path changes because adapter packaging changes, the active plan or validation command must list the concrete changed generated paths instead of relying on an unclassified directory path.
7. If `ready for final closeout` appears inside a negative instruction, validators must not treat that occurrence as an implementation overclaim.
8. If a contributor proposes a new optional skill named in Phase 4, that proposal still must prove artifact or gate ownership before the skill is added.
9. If a skill has no packaged resources, it does not need a `Resource map` or "No bundled resources" statement.
10. If a skill ships a packaged script but the script is rarely used, the `Resource map` still must name the script and its load condition.
11. If a project-local `docs/workflows.md` exists in a customer project, a published skill may consult it when relevant; that does not authorize requiring this repository's maintainer-only workflow docs in customer projects.
12. If a prompt fixture suggests a competing skill, the expected evidence is that the changed skill's `description` contains a near-miss boundary or that transcript review records the routing issue; it is not automatic CI proof of model selection.
13. If the published-skill design pilot audit finds a candidate for retirement, it is a follow-on decision and does not change adapter contents in the pilot.
14. If a body `When to use` section is useful after a skill has loaded, it may summarize scope or competing skills, but missing routing details in `description` remain a defect.
15. If routing coverage depends on a phrase table, static validation may check table and phrase presence, but transcript review still owns qualitative under-trigger or over-trigger observations.
16. If a touched pilot skill removes wording because the rule moved to another section, the behavior-preservation note must cite the destination section.
17. If `plan-skeleton.md` changes only placeholder names without changing section structure, structural fingerprint policy still applies because placeholders affect copied output shape.
18. If a historical plan lacks Current Handoff Summary, that absence is not a strict parity failure; the historical corpus checks whether the new skill can cover the same planning concern.
19. If a future `code-review` packaged-resource proposal is created, it should justify `references/` as the primary pattern unless repeated output structures dominate the proposed change.
20. If an asset contains a negative example of a forbidden repository-root path, validation must distinguish negative examples from required customer-project dependencies.
21. If an example applies to more than one slice, the Examples section may remain flat while the navigation index lists the example under each relevant slice.
22. If a future amendment adds a new slice family, the amendment must update the navigation index and grouping headers in the same change.

## Non-goals

- Do not change lifecycle stage order.
- Do not replace `specs/rigorloop-workflow.md`.
- Do not normalize every skill in the baseline normalization first slice.
- Do not add a standalone `review-resolution` skill.
- Do not add a standalone `token-budget` skill.
- Do not add a `skills/ci-maintenance/SKILL.md` path in this slice.
- Do not add broad semantic quality scoring for skill prose.
- Do not generate shared blocks into skills in v1.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not expose repository-maintainer source, generation, adapter, selector-path, shared-block implementation details, or RigorLoop-local examples in published skill text.
- Do not replace proposal, spec, architecture, plan, review, verification, explain-change, or PR artifacts with skill prose.
- Do not require `when_to_use` frontmatter.
- Do not require a `Resource map` when a skill ships no packaged resources.
- Do not claim published-skill design pilot routing fixtures prove deterministic model auto-selection.
- Do not merge, retire, rename, remove, or change ownership of skills in the published-skill design pilot.
- Do not let body `When to use` or `When not to use` sections become the primary routing source.
- Do not close the published-skill design pilot on structural validation alone when behavior-significant skill wording changed.
- Do not treat the assets-first plan pilot as authorization to roll out assets to every skill.
- Do not use packaged assets for hidden workflow rules, lifecycle transition policy, or claim ownership.
- Do not add packaged `references/` or `scripts/` in the assets-first plan pilot.
- Do not require historical plans to satisfy current plan structure for strict behavior parity.
- Do not change existing R-clause IDs, R-clause text, acceptance-criterion text, test-case IDs, or cross-references during structural hygiene.
- Do not split this spec or its matching test spec into multiple files as part of a content amendment.
- Do not group the Examples section when doing so would obscure cross-cutting examples.

## Acceptance criteria

### Foundational (R1-R7)

- A reviewer can identify `specs/skill-contract.md` as the normative skill-contract source.
- A reviewer can distinguish skill-contract behavior from workflow-routing behavior owned by `specs/rigorloop-workflow.md`.
- A contributor can identify the required core sections for a normalized skill.
- A contributor can see that `ci` is the skill entrypoint for `ci-maintenance`.

### Baseline normalization first slice (R8-R26)

- A contributor can identify which skills belong to the baseline normalization first slice.
- A contributor can identify the later normalization phases without guessing.
- A reviewer can confirm that normalized skills include local do-not-overclaim guidance.
- A reviewer can confirm that skill outputs are summary-first and include the common result fields or an approved equivalent.
- A reviewer can confirm that shared blocks adopted in v1 are copied from `templates/shared/` and checked for drift.
- A reviewer can confirm that generated `.codex/skills/` and `dist/adapters/` output are regenerated rather than hand-edited.
- A reviewer can confirm that published baseline normalization first-slice skills do not expose repository-maintainer generated-output handling, internal workflow spec paths, adapter package paths, selector path constraints, or shared-block implementation details.
- A reviewer can identify the exact published-skill allowlist and blocklist for project-portable wording.
- A reviewer can confirm that public skill portability checks apply to shipped skill text and generated public copies, not internal specs, plans, tests, generator scripts, maintainer docs, or repository-only contributor docs.
- A reviewer can confirm that validator checks are positive-first, narrow, and not broad semantic scoring.
- A contributor can determine when a new skill is justified and when an existing skill or template should be updated instead.

### Published-skill design pilot (R27-R36)

- A reviewer can confirm that `description` is the required portable routing source and is capped at 1024 characters.
- A reviewer can confirm that optional `when_to_use` metadata is not required and does not replace `description`.
- A reviewer can confirm that lifecycle skills with handoff, gate, artifact closeout, or downstream readiness responsibilities require `Workflow role`.
- A reviewer can confirm that skills with packaged resources include a resource map naming every packaged resource with a load condition.
- A reviewer can confirm that packaged skill-local scripts are distinguished from forbidden repository-root scripts.
- A reviewer can confirm that published-skill design pilot routing tests are bounded fixture and transcript evidence unless an approved harness exists.
- A reviewer can confirm that the published-skill design pilot audit results do not directly merge, retire, rename, remove, or change ownership of skills.
- A reviewer can confirm that pilot token-cost measurement uses the zero target, `+5%` rationale tolerance, and `+10%` hard cap.
- A reviewer can confirm that body `When to use` and `When not to use` sections do not replace `description` as the portable routing source.
- A reviewer can inspect a routing coverage table for each changed published-skill design pilot skill.
- A reviewer can inspect a behavior-preservation note for each changed published-skill design pilot skill.
- A reviewer can confirm behavior-parity evidence shows no weakening of material review status, finding format, recording obligations, stop conditions, validation obligations, or claim boundaries.

### Assets-first plan pilot (R37-R45)

- A reviewer can confirm the assets-first plan pilot is a follow-on slice limited to `plan` and exactly four normative assets.
- A reviewer can confirm `skills/plan/SKILL.md` uses a `Resource map` with literal `COPY` entries for every asset.
- A reviewer can confirm `assets/plan-skeleton.md` owns canonical plan section order while `SKILL.md` keeps only a compact output expectation summary.
- A reviewer can confirm `assets/current-handoff-summary.md` contains no lifecycle transition rules or readiness semantics.
- A reviewer can confirm every `plan` asset has metadata comments, normative status, and structural fingerprint coverage.
- A reviewer can confirm deterministic validation covers asset count, approved paths, metadata, resource-map coverage, `COPY`, placeholders, repository-root path exclusion, structural fingerprint, section-set parity, and adapter asset presence.
- A reviewer can confirm the assets-first plan pilot records behavior parity, at least 15 percent common-path body token reduction, total packaged content budget evidence, and milestone substructure reuse evidence.
- A reviewer can confirm behavior-parity evidence separates a strict contract-era reference corpus from a historical coverage corpus.

### Structural hygiene

No acceptance criteria are added in this amendment. Structural hygiene is reviewed by preserving the existing acceptance-criterion text while adding navigation headers.

## Open questions

- None. Spec-stage decisions resolved the proposal's open questions as follows: use about 1200 lines or more than about 6 slice families as the hygiene trigger; group the test spec Requirement coverage map during the matching test-spec amendment; keep the navigation index focused on R-clause bands; apply the growth strategy to this spec only; keep Examples flat because examples can be cross-cutting.

## Next artifacts

- Current amendment: plan for the audit-first `proposal` and `proposal-review` pilot.
- Current draft amendment: spec-review for the assets-first `plan` progressive disclosure pilot.
- Current draft amendment: spec-review for the spec and test-spec structural hygiene amendment.
- After plan: `plan-review`.
- Historical carried context: `code-review M2` under [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md) after M2 implementation handoff.
- Historical carried context: `implement M3` consumes the public skill portability proof.
- Historical carried context: `code-review M3` after M3 implementation handoff.

## Follow-on artifacts

- Spec-review: approved on 2026-05-08 with no material findings; clean review settled artifact-locally.
- Execution plan: [Skill Contract Optimization Execution Plan](../docs/plans/2026-05-08-skill-contract-optimization.md).
- Test spec: [Skill Contract Test Spec](skill-contract.test.md).
- Proposal: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md).
- Spec-review: approved in [spec-review-r5](../docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md).
- Plan: [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md).
- Current amendment: public skill surface boundary allow/block policy approved in this spec.
- Current amendment proposal: [RigorLoop Published Skill Design Contract](../docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md).
- Current amendment proposal-review: [proposal-review-r2](../docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r2.md).
- Current amendment spec-review: [spec-review-r3](../docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/spec-review-r3.md).
- Current amendment plan: [RigorLoop Published Skill Design Contract Execution Plan](../docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md).
- Current draft amendment proposal: [Assets-First Progressive Disclosure Pilot for Published Skills](../docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md).
- Current draft amendment proposal-review: [proposal-review-r2](../docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/proposal-review-r2.md).
- Current amendment spec-review: [spec-review-r1](../docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/spec-review-r1.md).
- Current draft amendment plan: [Assets-First Progressive Disclosure Pilot Execution Plan](../docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md).
- Current amendment proposal: [Spec and Test-Spec Structural Hygiene](../docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md).
- Current amendment proposal-review: [proposal-review-r1](../docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/proposal-review-r1.md).
- Current amendment spec-review: [spec-review-r1](../docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/reviews/spec-review-r1.md).

## Readiness

Approved structural hygiene amendment. Current downstream stage: plan for the spec and test-spec structural hygiene amendment.
