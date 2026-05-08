# Skill Contract

## Status

- approved

## Related proposal

- [Skill Contract Optimization](../docs/proposals/2026-05-08-skill-contract-optimization.md)

## Goal and context

This spec defines the contributor-visible contract for RigorLoop skill guidance. A skill is an operational guide for one agent capability or workflow stage. It should be small enough to scan, explicit about local ownership, and clear about what it can and cannot claim.

The problem this spec addresses is recurring state and handoff confusion. Skills can accidentally blur progress, readiness, closeout, final Done state, review outcome, validation proof, branch readiness, and PR readiness. The skill contract prevents those overclaims by standardizing core sections, result output, claim boundaries, shared-policy blocks, evidence-reading rules, public skill surface boundaries, generated-output handling, and minimum viable skill creation rules.

Skills are also a published user-facing interface. Repository-maintainer guidance for authoring, generating, validating, or packaging this repository's skills belongs in contributor and governance surfaces, not inside shipped skill text.

This spec owns skill-contract behavior. `specs/rigorloop-workflow.md` continues to own stage order, stage obligation, handoff, and downstream-blocking semantics.

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

## Examples first

### Example E1: first-slice execution skill avoids review overclaim

Given `skills/implement/SKILL.md` is normalized in the first implementation slice
When the skill reports successful implementation for a milestone
Then its output may state implementation work and targeted validation are complete
And it may state the next stage is `code-review`
But it must not claim review passed, branch-ready, PR-ready, or ready-for-verify.

### Example E2: non-first-slice skill is not blocked immediately

Given `skills/proposal/SKILL.md` has not yet been normalized
When the first implementation slice normalizes `workflow`, `plan`, `implement`, `code-review`, `verify`, `pr`, and `learn`
Then the first slice remains valid
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

### Example E5: validator uses narrow overclaim checks

Given the first validation slice adds checks for `skills/verify/SKILL.md`
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

## Requirements

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

R8. The first implementation slice MUST normalize only these canonical skills:
- `skills/workflow/SKILL.md`
- `skills/plan/SKILL.md`
- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`
- `skills/verify/SKILL.md`
- `skills/pr/SKILL.md`
- `skills/learn/SKILL.md`

R8a. The first implementation slice MUST add or align required core sections where missing.

R8b. The first implementation slice MUST add or align do-not-overclaim guidance.

R8c. The first implementation slice MUST add or align compact result output expectations.

R8d. The first implementation slice MUST align milestone, progress, readiness, and closeout wording where relevant.

R8e. The first implementation slice MUST add or align targeted evidence-reading guidance.

R8f. The first implementation slice MUST include generated-output drift checks when canonical skill changes produce generated output changes.

R8g. The first implementation slice MUST NOT normalize every skill.

R8h. The first implementation slice MUST keep repository-maintainer generated-output handling out of published skill text.

R9. Later-phase normalization MUST proceed in the order approved by the proposal unless a later approved proposal changes the order.

R9a. Phase 2 MUST normalize core lifecycle authoring and review skills: `proposal`, `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan-review`, `test-spec`, `explain-change`, and the `ci` skill for the `ci-maintenance` stage label.

R9b. Phase 3 MUST normalize on-demand and standing or living-reference skills: `explore`, `research`, `vision`, `project-map`, and `bugfix`.

R9c. Phase 4 MUST normalize newly adopted optional skills only when those skills exist and own approved artifacts or gates.

R9d. Phase 4 candidate names include `ui-design`, `ui-design-review`, `workflow-contract`, and `adopt-rigorloop`; this spec does not create those skills.

R10. A normalized skill MUST include `Claims this skill must not make`.

R10a. `implement` MUST NOT claim review passed, clean review, branch-ready, PR-ready, or ready-for-verify.

R10b. `code-review` MUST NOT claim branch-ready, PR-ready, CI passed, or verification passed.

R10c. `verify` MUST NOT claim PR-ready, PR body ready, or review passed.

R10d. `pr` MUST NOT claim implementation, review, verification, or tests passed unless the claim is linked to owning evidence.

R10e. `plan` MUST distinguish Done, complete, ready for PR, and ready for verify from remaining-gates wording.

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

R13e. `Ready for verify` MUST NOT be represented as Done, PR-ready, or branch-ready.

R13f. Plans that mention `Ready for verify` SHOULD pair it with remaining completion gates when ambiguity is possible.

R14. Shared skill policy blocks MUST live under `templates/shared/<block-name>.md`.

R14a. Shared skill policy blocks MUST be treated as canonical authored sources for copied skill subsections.

R14b. In v1, consuming skills MUST copy adopted shared blocks verbatim.

R14c. `scripts/test-skill-validator.py` or another repo-owned validation script MUST compare copied shared blocks to the shared source when drift checking is adopted.

R14d. Shared blocks MUST NOT replace or outrank the workflow spec or this skill-contract spec.

R14e. Shared-block generation into skills MUST NOT be added in the first implementation slice.

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

R18c. Validators MUST NOT perform broad semantic quality scoring in the first validation slice.

R18d. Forbidden phrase checks MUST avoid blocking explicit negative guidance such as "Do not set Ready for verify from implement."

R19. A new skill SHOULD be added only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.

R19a. Contributors SHOULD NOT add a skill for one-off helper behavior, a tiny formatting rule, or a checklist that belongs inside an existing skill.

R19b. `docs/workflows.md` and `AGENTS.md` MAY summarize the minimum viable skill rule.

R19c. Detailed examples and templates for creating skills SHOULD live in skill-creator guidance, such as `templates/skill.md` or `docs/skills/creating-skills.md`.

R20. The skill contract implementation MUST preserve source-of-truth order.

R20a. If a skill, generated output, adapter output, contributor summary, or shared block conflicts with this spec on skill-contract behavior, this spec wins unless a higher-priority artifact applies.

R20b. If this spec conflicts with `specs/rigorloop-workflow.md` on stage order, stage obligation, handoff, or downstream blocking, `specs/rigorloop-workflow.md` wins for those workflow-routing semantics.

## Inputs and outputs

Inputs:

- accepted skill-contract proposal;
- canonical skill files under `skills/`;
- shared policy blocks under `templates/shared/`;
- generated skill mirrors under `.codex/skills/`;
- generated adapter output under `dist/adapters/`;
- workflow contract in `specs/rigorloop-workflow.md`;
- contributor summaries in `docs/workflows.md` and `AGENTS.md`;
- skill validator and generated-output drift validation scripts.

Outputs:

- `specs/skill-contract.md`;
- normalized canonical skill source for the in-scope slice;
- copied shared policy blocks where adopted;
- regenerated `.codex/skills/` output when canonical skills change;
- regenerated `dist/adapters/` output when canonical skills change;
- validator checks for required sections, shared-block drift, generated-output drift, and narrow overclaim assertions;
- contributor summary updates when root or workflow guidance is affected.

## State and invariants

- `specs/skill-contract.md` is the normative skill-contract spec.
- `specs/rigorloop-workflow.md` remains the normative workflow-routing spec.
- Canonical skill source lives under `skills/`.
- `.codex/skills/` and `dist/adapters/` are generated outputs.
- A normalized skill owns only its local claims.
- A skill's readiness statement is not proof that downstream gates have passed.
- Public shared blocks are copied and checked in v1, not generated into skills.
- Published skill text does not expose repository-local source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, or shared-block implementation details.
- The first implementation slice is limited to seven canonical skills.
- The `ci` skill remains the entrypoint for the `ci-maintenance` stage label.

## Error and boundary behavior

- If a required shared-block source is missing, validation MUST fail or the consuming skill MUST not claim shared-block conformance.
- If a copied shared block drifts from its shared source, validation MUST fail when drift checking is adopted.
- If generated `.codex/skills/` or `dist/adapters/` output drifts from canonical skills, generated-output drift validation MUST fail.
- If a normalized skill cannot satisfy a required core section without creating misleading content, the implementation MUST stop for spec review or owner decision rather than inventing a hollow section.
- If a proposed forbidden phrase check blocks explicit negative guidance, the check MUST be narrowed before it is relied on.
- If the workflow stage label `ci-maintenance` is used in a normalization list, spec and plan authors MUST map it to the existing `ci` skill entrypoint unless a later approved spec renames the skill path.
- If a new optional skill does not yet exist or lacks approved artifact or gate ownership, it MUST NOT be included in implementation scope solely because it is named as a Phase 4 candidate.

## Compatibility and migration

- Existing unnormalized skills remain valid until their approved normalization phase.
- The first implementation slice does not require all skills to adopt the required core sections at once.
- Existing contributor generated-output policy remains unchanged: edit canonical skill source, regenerate generated output, and validate drift. That policy is contributor-maintenance guidance and is not copied into published skill text.
- Existing `skills/ci/` path remains valid for `ci-maintenance`.
- Existing formal review recording rules remain authoritative for review records; this spec only defines how shared review guidance is copied and checked in skills.
- Rollback for wording-only skill changes may revert the affected canonical skills, shared blocks, validator checks, and generated output together.

## Observability

- Validation output SHOULD identify which required core section, shared block, generated output, or overclaim check failed.
- Selector-selected validation SHOULD classify touched spec, skill, template, generated, adapter, change-local, and review-artifact paths without unclassified paths.
- Review and verification artifacts SHOULD cite validation commands and results rather than generic success claims.
- No runtime logs, metrics, traces, or audit events are required because this is repository guidance behavior, not runtime product behavior.

## Security and privacy

- Skill normalization MUST NOT require committing secrets, credentials, tokens, private keys, machine-local paths, or private user data.
- Generated output refreshes MUST preserve the existing security boundary that derived adapter packages do not become independent sources of truth.
- Evidence-reading guidance MUST NOT encourage pasting sensitive logs or secrets into skill output.

## Accessibility and UX

This change has no user-interface surface. The relevant user experience is contributor readability of skill files and validation output.

## Performance expectations

- Skill validation SHOULD remain static and repository-local in the first implementation slice.
- The first validation slice MUST NOT add broad natural-language quality scoring.
- Evidence-reading guidance SHOULD reduce unnecessary broad reads by preferring targeted summaries, IDs, headings, line citations, and path lists first.
- Generated-output checks SHOULD use existing build and adapter validation paths unless the approved plan names a narrower or broader proof scope.

## Edge cases

1. If a skill already has a domain-specific section that overlaps a required core section, normalization may keep both only when the overlap remains clear and non-duplicative.
2. If a skill is both authoring and execution oriented, it must satisfy the required core sections and the relevant conditional sections for both roles.
3. If a clean review skill output has no material findings, formal review recording rules may allow artifact-local settlement; this spec does not require an empty review record.
4. If a shared block is adopted by only one skill initially, the block may still live under `templates/shared/` when the approved plan expects later consumers.
5. If a normalized skill needs an example to prevent a recurring error, the example must remain short enough not to turn the skill into a tutorial.
6. If a generated adapter path changes because adapter packaging changes, the active plan or validation command must list the concrete changed generated paths instead of relying on an unclassified directory path.
7. If `ready for verify` appears inside a negative instruction, validators must not treat that occurrence as an implementation overclaim.
8. If a contributor proposes a new optional skill named in Phase 4, that proposal still must prove artifact or gate ownership before the skill is added.

## Non-goals

- Do not change lifecycle stage order.
- Do not replace `specs/rigorloop-workflow.md`.
- Do not normalize every skill in the first implementation slice.
- Do not add a standalone `review-resolution` skill.
- Do not add a `skills/ci-maintenance/SKILL.md` path in this slice.
- Do not add broad semantic quality scoring for skill prose.
- Do not generate shared blocks into skills in v1.
- Do not hand-edit generated `.codex/skills/` or `dist/adapters/` output.
- Do not expose repository-maintainer source, generation, adapter, selector-path, or shared-block implementation details in published skill text.
- Do not replace proposal, spec, architecture, plan, review, verification, explain-change, or PR artifacts with skill prose.

## Acceptance criteria

- A reviewer can identify `specs/skill-contract.md` as the normative skill-contract source.
- A reviewer can distinguish skill-contract behavior from workflow-routing behavior owned by `specs/rigorloop-workflow.md`.
- A contributor can identify the required core sections for a normalized skill.
- A contributor can identify which skills belong to the first implementation slice.
- A contributor can identify the later normalization phases without guessing.
- A contributor can see that `ci` is the skill entrypoint for `ci-maintenance`.
- A reviewer can confirm that normalized skills include local do-not-overclaim guidance.
- A reviewer can confirm that skill outputs are summary-first and include the common result fields or an approved equivalent.
- A reviewer can confirm that shared blocks adopted in v1 are copied from `templates/shared/` and checked for drift.
- A reviewer can confirm that generated `.codex/skills/` and `dist/adapters/` output are regenerated rather than hand-edited.
- A reviewer can confirm that published first-slice skills do not expose repository-maintainer generated-output handling, internal workflow spec paths, adapter package paths, selector path constraints, or shared-block implementation details.
- A reviewer can confirm that validator checks are positive-first, narrow, and not broad semantic scoring.
- A contributor can determine when a new skill is justified and when an existing skill or template should be updated instead.

## Open questions

- None.

## Next artifacts

- Plan-review for the execution plan.
- Matching test spec after plan-review.

## Follow-on artifacts

- Spec-review: approved on 2026-05-08 with no material findings; clean review settled artifact-locally.
- Execution plan: [Skill Contract Optimization Execution Plan](../docs/plans/2026-05-08-skill-contract-optimization.md).
- Test spec: [Skill Contract Test Spec](skill-contract.test.md).

## Readiness

Approved after spec-review. Follow-on execution plan and matching test spec are recorded; the active plan owns the current execution handoff.
