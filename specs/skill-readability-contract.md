# Skill Readability and Self-Containment Contract

## Status

approved

## Related proposal

- [Optimize Skills for User-Facing Readability and Self-Containment](../docs/proposals/2026-05-18-skill-readability-self-containment.md)
- Builds on [Customer-Portable Public Skills and Token-Friendly Local Guidance](../docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md)

## Goal and context

This spec defines the user-facing readability and self-containment contract for installed RigorLoop skill text. Installed skills are the contract a user sees after adapter installation, so each skill must preserve output quality, expose its rules clearly, avoid unresolved repository-internal dependencies, and provide fillable output skeletons where the skill produces durable artifacts or formal review evidence.

This spec extends the existing `specs/skill-contract.md` and `specs/customer-portable-public-skill-evidence.md` contracts. It does not change workflow stage order, normative review verdicts, adapter archive format, generated-output ownership, or release packaging.

Priority order:

```text
1. high-quality skill output
2. clear and concise skills
3. token cost
```

Token cost is a constraint, not the driver. A smaller skill body is not acceptable if it weakens output quality, required-rule coverage, artifact completeness, or cold-read clarity.

## Glossary

- `installed skill`: a skill file delivered to a user through an adapter install, such as `.claude/skills/`, `.agents/skills/`, or `.opencode/skills/`.
- `canonical skill source`: the authored skill source under `skills/<skill>/SKILL.md`.
- `generated adapter output`: adapter package output derived from canonical skill source.
- `artifact-producing skill`: a skill whose expected output creates or updates a durable artifact, review record, report, handoff text, or user-facing command artifact.
- `closed enum`: a finite value set where spelling and membership are part of the contract.
- `workflow role block`: a short top-of-skill section that states the skill's lifecycle role, stage class, inputs from upstream stages, outputs to downstream stages, and role summary.
- `output skeleton`: a fenced, fillable template showing the durable artifact or result shape the skill should produce.
- `workflow-wide rule`: a rule that applies beyond one skill and constrains lifecycle behavior, evidence, review recording, validation, or handoff.
- `skill-local rule`: a rule that applies only to the current skill's artifact, output, or stop conditions.
- `cold-read verification`: inspection of installed skill text in a clean project without RigorLoop repository context to confirm the skill is self-contained and scannable.
- `quality regression`: a rewrite outcome that weakens verdicts, rationale, required-section coverage, scope preservation, handoff clarity, stop conditions, rule ownership, or formal recording behavior compared with the baseline skill.

## Examples first

### Example E1: proposal skill exposes the artifact shape

Given an installed `proposal` skill
When a user opens the skill without access to RigorLoop repository specs or docs
Then the skill shows its workflow role near the top
And its required proposal sections are in a scannable table
And its valid status and Vision fit values are in fenced closed-enum blocks
And the bottom of the skill includes a fenced fillable proposal skeleton.

### Example E2: proposal-review preserves review quality

Given a baseline `proposal-review` skill and a rewritten `proposal-review` skill
When both review the same representative proposal fixture
Then the rewritten skill must not miss a material finding that the baseline skill would report
And it must preserve formal review recording obligations
And any wording improvement must not weaken review status, finding format, or review-resolution boundaries.

### Example E3: cold-read catches a dangling internal reference

Given an installed skill references `specs/skill-contract.md` as required runtime context
When cold-read verification inspects the skill in a clean adapter-installed project
Then the reference is a defect unless it is explicitly framed as maintainer-only context unavailable to adopters
And the skill must instead carry the needed user-facing contract directly or route to project-local guidance when present.

### Example E4: token reduction cannot override clarity

Given a rewrite removes repeated prose and reduces token count
When the same rewrite removes the only fenced enum block for a review verdict set
Then the rewrite fails this spec
And the token reduction must be reverted or revised until the closed enum is again discoverable.

### Example E5: workflow-wide rule is marked

Given a review skill includes formal review recording behavior
When the rule applies to all formal review skills rather than only that skill
Then the skill marks it as a workflow-wide rule
And any skill-local exception or stop condition remains separately labeled.

## Requirements

R1. Canonical skill source for installed skills MUST remain under `skills/<skill>/SKILL.md`.

R2. Generated adapter output MUST be derived from canonical skill source and MUST NOT be hand-edited to satisfy this spec.

R3. Implementations of this spec MUST preserve the existing normative behavior of each rewritten skill.

R4. A rewritten skill MUST NOT weaken skill output quality, including required artifact coverage, verdict quality, rationale quality, scope preservation, handoff clarity, stop conditions, or formal review recording behavior.

R5. Rewrites MUST optimize in this priority order: high-quality skill output first, clear and concise skill text second, token cost third.

R6. Token-cost reduction MUST NOT justify a quality regression or clarity regression.

R7. Each rewritten installed skill MUST be self-contained for normative user-facing behavior.

R8. A rewritten installed skill MUST NOT require unavailable RigorLoop repository-internal files as runtime context for an adopter.

R9. A rewritten installed skill MAY use project-local artifacts when those artifacts exist and are relevant, including local `AGENTS.md`, `VISION.md`, `docs/workflows.md`, specs, plans, architecture records, validation commands, and change artifacts.

R10. A rewritten installed skill MUST use portable defaults where safe and MUST block on ambiguity where no safe default exists.

R11. Each rewritten installed skill MUST include a workflow role block near the top of the skill body.

R12. The workflow role block MUST include `role_name`, `stage`, `upstream`, `downstream`, and a plain-language summary.

R13. The `role_name` field MUST match the skill name.

R14. The workflow role block `stage` value MUST be exactly one of:

```text
authoring
review
execution
verification
handoff
support
periodic
```

R15. The workflow role block summary MUST be no more than two lines when rendered as normal prose in canonical skill source.

R16. Every closed enum used by a rewritten skill MUST appear in a fenced block or table exactly once in that skill.

R17. A rewritten skill MUST NOT restate the same closed enum values in multiple prose locations.

R18. Valid closed enum values MUST preserve existing spelling, capitalization, and membership unless a separate approved spec changes the enum.

R19. Long enumerative content in rewritten skills MUST use a table when the list has named fields, comparisons, review dimensions, required sections, or classification values.

R20. Long enumerative content MAY remain a list when order is the contract and table fields would reduce clarity.

R21. Each rule, lookup order, and guideline SHOULD appear once per skill, in the earliest location where a reader needs it.

R22. If a rule is intentionally repeated for safety, the repeated instance MUST identify itself as a reminder and MUST not introduce conflicting wording.

R23. Workflow-wide rules in rewritten skills MUST be labeled as workflow-wide rules.

R24. Skill-local rules in rewritten skills MUST be distinguishable from workflow-wide rules by section placement, label, or wording.

R25. Each artifact-producing skill in scope MUST include a fenced output skeleton near the bottom of the skill.

R26. An output skeleton MUST include every required top-level section or field that the skill expects the output artifact to contain.

R27. An output skeleton MUST use fillable placeholders rather than prose-only description.

R28. An output skeleton MUST preserve existing required result blocks for review skills, including formal review recording fields when applicable.

R29. The pilot implementation MUST cover `proposal` and `proposal-review`.

R30. The full rollout scope after the pilot MUST include these artifact-producing skills unless the plan records a justified exclusion:

```text
proposal
proposal-review
spec
spec-review
architecture
architecture-review
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
project-map
vision
learn
bugfix
ci
workflow
```

R31. Skills outside the full rollout list MAY adopt the same formatting pattern when they produce durable user-facing output, but they are not required by this spec unless added by a later accepted artifact.

R32. Rewritten skills SHOULD include front matter fields `version` and `schema-version`.

R33. The initial `schema-version` value for this contract MUST be `skill-readability-v1`.

R34. The initial `version` value MUST be determined by the implementation plan and applied consistently to the pilot pair.

R35. Existing consumers MUST be able to ignore `version` and `schema-version` without behavior change.

R36. Static validation MUST check that rewritten in-scope skills include a workflow role block.

R37. Static validation MUST check that rewritten artifact-producing skills include a fenced output skeleton.

R38. Static validation MUST check for unqualified required references to unavailable RigorLoop repository-internal paths in installed skill text.

R39. Static validation SHOULD check that each known closed enum appears in only one authoritative fenced block or table per rewritten skill.

R40. Static validation MUST NOT reject legitimate project-local references that are clearly conditional or project-local.

R41. Cold-read verification MUST be performed for the pilot pair before expanding to the full rollout.

R42. Cold-read verification MUST inspect installed adapter output, not only canonical source.

R43. Cold-read verification MUST confirm that every normative reference resolves to installed skill text or project-local artifacts visible to an adopter.

R44. Cold-read verification MUST confirm that workflow role, valid enums, required sections, output skeleton, handoff, stop conditions, and workflow-wide versus skill-local rule boundaries are discoverable without repository-internal context.

R45. Behavior-parity verification MUST compare rewritten pilot skill outputs against baseline outputs on representative proposal and review fixtures.

R46. Behavior-parity verification MUST classify each observed output difference as `equivalent`, `improvement`, or `regression`.

R47. Any `regression` classification MUST block rollout for that skill until resolved or explicitly accepted by a later approved spec change.

R48. Token-cost measurement MUST compare each rewritten skill against its baseline.

R49. The default token-cost target is zero regression versus the prior skill body.

R50. A token-cost increase up to five percent MAY be accepted only when readability gain is demonstrated and recorded in the change-local pack.

R51. A token-cost increase greater than ten percent MUST block rollout unless this spec is revised.

R52. Token-cost thresholds MUST NOT override the quality floor or clarity floor.

R53. The forbidden-path lint enforcement mode during rollout, such as warning or CI-blocking, MUST be decided by the execution plan.

R54. This spec MUST NOT introduce build-time partials, include mechanisms, adapter packaging changes, manifest format changes, release archive contract changes, or retroactive legacy archive rewrites.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-05-18-skill-readability-self-containment.md`;
- current canonical skill source under `skills/`;
- generated installed adapter output used for cold-read verification;
- representative proposal and review fixtures for behavior-parity checks;
- existing skill validation and token-cost measurement tooling.

Outputs:

- rewritten canonical skill source for the pilot pair and later rollout skills;
- generated adapter output validation evidence;
- cold-read verification evidence;
- behavior-parity evidence with `equivalent`, `improvement`, or `regression` classifications;
- static validation coverage for workflow role blocks, output skeletons, forbidden paths, and known closed enums;
- token-cost comparison evidence.

## State and invariants

- Installed skill text remains the user-facing contract.
- Skill output quality is the primary success criterion.
- Clarity and concision are secondary success criteria.
- Token cost is a tertiary constraint.
- Normative skill behavior remains unchanged unless a separate approved spec changes it.
- Canonical skill source remains under `skills/`.
- Generated adapter output remains derived.
- Repository-maintainer implementation details stay out of installed skill text unless they are directly user-facing contract.

## Error and boundary behavior

R55. If a rewritten skill omits a required workflow role block, validation MUST fail or the plan MUST record why the skill is out of scope.

R56. If a rewritten artifact-producing skill omits its output skeleton, validation MUST fail or the plan MUST record why the skill is out of scope.

R57. If cold-read verification finds an unresolvable normative reference, rollout for that skill MUST stop until the reference is removed, reframed as project-local, or made self-contained.

R58. If behavior-parity fixtures show a regression, rollout for that skill MUST stop until the regression is resolved.

R59. If token-cost measurement exceeds the hard cap, rollout for that skill MUST stop until this spec is revised or the skill body is reduced without breaching quality or clarity floors.

R60. If the implementation cannot identify whether a rule is workflow-wide or skill-local, it MUST keep the rule and record the ambiguity for spec or plan resolution rather than deleting or weakening it.

## Compatibility and migration

- Existing skill invocation behavior remains compatible because the rewrite changes presentation and self-containment, not workflow stage semantics.
- Existing consumers that ignore new front matter fields remain compatible.
- Adapter package format and release archive format remain unchanged.
- Existing generated adapter output is not retroactively rewritten; future adapter output is regenerated from canonical source after skill changes.
- Rollback is file-based: reverting the affected canonical skill source and regenerated validation evidence restores prior skill text.

## Observability

- Static validation output must name each failed skill and missing readability/self-containment contract element.
- Cold-read evidence must name the adapter output inspected, skills inspected, and any unresolved references or missing skeletons.
- Behavior-parity evidence must name each fixture, compared skill, and difference classification.
- Token-cost evidence must name baseline tokens, after-change tokens, percentage delta, and any rationale for accepted regression.
- Change-local evidence must record any accepted token increase, quality improvement claim, or rollout-blocking defect.

## Security and privacy

- Installed skill text must not require adopters to expose secrets, private keys, tokens, private repository metadata, or unrelated machine-local paths.
- Cold-read test projects and behavior-parity fixtures should use synthetic or public-safe data.
- Generated adapter output must not expose repository-maintainer-only implementation mechanics as user-facing instructions.

## Accessibility and UX

No graphical UI is involved. The user experience requirement is text scanability: users must be able to locate workflow role, closed enums, required sections, output skeletons, stop conditions, and rule scope without reading unrelated repository context.

## Performance expectations

Skill token cost must stay within the thresholds in R49-R52. Performance optimization is subordinate to output quality and clarity.

## Edge cases

1. A skill has no durable output artifact: it still needs a workflow role block but may omit an output skeleton if the plan records it as non-artifact-producing.
2. A skill has a closed enum embedded in an output skeleton: the enum block or table remains the authoritative value set, and the skeleton should reference the enum without restating all values.
3. A skill must mention `docs/workflows.md`: it may do so as project-local guidance when present, but it must not require the RigorLoop repository's internal `docs/workflows.md` in adopter projects.
4. A table would make an ordered procedure harder to follow: the ordered list may remain when order is the contract.
5. A safety-critical rule appears in multiple skills: each skill may carry the rule if needed for self-containment, but the same rule should not be repeated multiple times within one skill.
6. A rewritten review skill is shorter but misses a material finding in parity fixtures: this is a regression and blocks rollout.
7. A rewritten skill exceeds the five percent token tolerance but improves clarity: rollout remains blocked unless the increase is at or below the hard cap and the change-local pack records the readability justification.
8. A front matter consumer rejects unknown fields: implementation must resolve compatibility before shipping `version` or `schema-version` to that consumer.

## Non-goals

- Do not change workflow stage order, handoff semantics, review verdict meanings, or formal review recording requirements.
- Do not introduce build-time partials or include mechanisms.
- Do not change adapter packaging, manifest format, or release archive contracts.
- Do not retroactively rewrite legacy adapter archives.
- Do not move normative behavior out of installed skill text into inaccessible repository specs.
- Do not use token-cost reduction as a reason to weaken output quality or clarity.
- Do not edit generated adapter output by hand.

## Acceptance criteria

- The pilot `proposal` and `proposal-review` skills include workflow role blocks, fenced closed enums, tabulated enumerative contracts where appropriate, clear workflow-wide versus skill-local rule boundaries, and fenced output skeletons.
- The pilot pair passes cold-read verification against installed adapter output.
- The pilot pair passes behavior-parity verification with no `regression` classifications.
- Static validation covers workflow role blocks, output skeleton presence, forbidden unqualified repository-internal references, and known closed enum placement for the pilot pair.
- Token-cost comparison is recorded for the pilot pair and stays within R49-R52.
- Any accepted token-cost increase includes recorded readability justification and no quality or clarity regression.
- Generated adapter output is validated from canonical skill source.
- No adapter package format, manifest format, release archive contract, or workflow stage behavior changes occur.

## Open questions

- Should the full rollout include all skills listed in R30, or should the plan record justified exclusions for non-artifact-producing support skills?
- Should forbidden-path lint be warning-only during the rollout window or CI-blocking immediately?
- What exact initial `version` value should the pilot pair use?

These questions do not block spec review because the contract defines safe defaults and delegates rollout policy to the plan.

## Next artifacts

- `spec-review` for this spec.
- `plan` covering pilot implementation, validation additions, cold-read procedure, rollout sequencing, and lint enforcement mode.
- `test-spec` mapping requirements to static validation, cold-read, behavior parity, token-cost, and adapter validation checks.

## Follow-on artifacts

- Spec review: `docs/changes/2026-05-18-skill-readability-self-containment/reviews/spec-review-r1.md`
- Plan: `docs/plans/2026-05-18-skill-readability-self-containment.md`

## Readiness

Approved and ready for planning.
