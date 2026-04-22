# README User Value Positioning

## Status
- approved

## Related proposal

- [README User Value Positioning](../docs/proposals/2026-04-22-readme-user-value-positioning.md)
- [RigorLoop Project Direction](../docs/proposals/2026-04-19-rigorloop-project-direction.md)

## Goal and context

This spec defines the contributor-visible contract for how `README.md` presents RigorLoop to first-time repository visitors.

The goal is to make the root README explain what RigorLoop does, why it is useful, who it is for, when it fits, and where to start before it dives into workflow mechanics, repository layout, or rollout-era detail. The change is positioning-only: it does not alter workflow rules, validation requirements, or the repository's source-of-truth order.

## Glossary

- `public entrypoint`: the root `README.md` that GitHub shows to repository visitors.
- `value-first`: README structure that explains user problem, value, fit, and next steps before detailed mechanics.
- `qualification guidance`: the near-top `When to use / When not to use` section that helps a reader decide whether RigorLoop fits their needs.
- `opening overview paragraph`: the first explanatory paragraph after the project title and tagline that tells a visitor what RigorLoop is and why it matters.
- `mechanics/reference section`: a section focused on installation details, complete workflow tables, skill catalogs, file layout details, schema references, long examples, or similar reference-heavy content.
- `linked summary surface`: a contributor-facing summary document linked from the README, such as `docs/workflows.md`.

## Examples first

### Example E1: first-time contributor qualifies the project quickly

Given a visitor lands on the repository root page on GitHub
When they read the title, introduction, and first few sections of `README.md`
Then they can tell what RigorLoop is, why it is useful, that it is for AI-assisted software delivery with explicit reviewable artifacts, and whether it fits their workflow before they encounter the full lifecycle stage list.

### Example E2: maintainer remains visible without displacing the lead audience

Given a maintainer evaluates the repository for team use
When they read the README
Then they can see that the starter kit remains useful to maintainers and small teams, while the first-release entrypoint still speaks primarily to individual contributors.

### Example E3: unsupported positioning is rejected

Given a README draft claims that RigorLoop replaces pull requests, CI, or human review
When the draft is reviewed against this spec
Then the draft is rejected because it contradicts the accepted project direction and the existing workflow contract.

### Example E4: stale rollout framing is removed

Given the first proof-of-value example is already shipped
When the README is rewritten under this spec
Then it does not present that rollout as if it were still the current active implementation focus, and it instead describes shipped artifacts in durable language.

## Requirements

R1. The root `README.md` MUST act as the repository's public project overview for first-time visitors rather than as a compact restatement of repository-internal mechanics.

R1a. The README MUST open in the following order:
- project title;
- short tagline or equivalent opening line;
- opening overview paragraph.

R1b. The opening overview paragraph MUST appear before any audience-fit section, quick-start or adoption-checklist section, help or contribution pointer, or mechanics/reference section.

R2. Before any mechanics/reference section, the README MUST explain all of the following in plain language:
- what RigorLoop is;
- why it is useful;
- that it is a Git-first starter kit for AI-assisted software delivery;
- that it does not replace pull requests, CI, or human review.

R2a. In the first audience-defining sentence or bullet in the README, the README MUST name individual contributors first as the primary audience.

R2b. Maintainers and small teams MAY be mentioned only:
- in a secondary clause after individual contributors; or
- in a later sentence or later section.

R2c. The README MUST NOT open with an audience phrase that gives equal priority to contributors, maintainers, and teams.

R3. After the opening overview paragraph and before the first mechanics/reference section, the README MUST include a section titled exactly:
- `When to use / When not to use`

R3a. The `When to use / When not to use` section MUST include at least:
- one good-fit case grounded in AI-assisted software delivery with explicit proposals, specs, plans, tests, review gates, verification, or explainable change history;
- one bad-fit case grounded in a repository need that RigorLoop does not serve well, such as replacing Git-based review, replacing CI or human review, acting as a hosted orchestration platform, or acting as a zero-process scratchpad.

R3b. The `When to use / When not to use` section MUST appear before any quick-start or adoption-checklist section, help or contribution pointer, or mechanics/reference section.

R4. Before any mechanics/reference section, the README MUST communicate concrete user outcomes from adopting RigorLoop.

R4a. Those outcomes MUST be grounded in current repository reality, such as clearer reviewability, explicit artifact history, safer AI-assisted delivery, or traceable change rationale.

R4b. The README MUST NOT rely on unsupported social proof, adoption claims, or production-readiness claims to create value.

R5. The README MUST include a short quick-start path or adoption checklist that helps a reader go deeper after the overview and audience-fit sections.

R5a. That quick-start path or adoption checklist MUST point readers to all of the following existing surfaces:
- `docs/workflows.md` for the short workflow summary;
- `specs/rigorloop-workflow.md` for the normative workflow contract;
- `docs/changes/0001-skill-validator/` for the shipped proof-of-value example.

R5b. The quick-start path or adoption checklist MUST appear after the `When to use / When not to use` section and before the help or contribution pointer and any mechanics/reference section.

R5c. After the quick-start path or adoption checklist and before any mechanics/reference section, the README MUST include a concise help or contribution pointer.

R5d. The help or contribution pointer MUST help a new individual contributor answer all of the following:
- where to learn the workflow in more detail;
- where to find artifact and skill documentation;
- where to learn how to contribute or report issues.

R5e. A short `Learn more / contribute` section or compact link group MAY satisfy `R5c` and `R5d`.

R5f. The help or contribution pointer MUST point to active repository surfaces that truthfully satisfy the linked need.

R6. The README MAY still include workflow summary, source-of-truth guidance, validation commands, repository layout, and example references, but those sections MUST appear after the value-first overview, qualification guidance, quick-start or adoption-checklist section, and help or contribution pointer required by `R2` through `R5`.

R7. The README MUST remain faithful to the accepted product direction.

R7a. The README MUST NOT present RigorLoop as any of the following:
- a generic repository template with no opinionated workflow value;
- a hosted SaaS product;
- a centralized control plane or agent runtime;
- a replacement for Git, pull requests, CI, or human review.

R8. The README MUST NOT use stale rollout-state wording that implies the already-shipped first proof-of-value rollout is still the current active implementation focus.

R8a. If the README mentions shipped proof surfaces, it MUST describe them in durable present-state language rather than as an in-progress rollout.

R9. This initiative MUST NOT change workflow rules, validation requirements, or source-of-truth ordering.

R9a. If linked summary surfaces such as `docs/workflows.md` are updated for alignment, those edits MUST remain wording or link-alignment changes only and MUST NOT alter the normative workflow contract defined elsewhere.

R10. When the README links to deeper guidance, those links MUST remain truthful to the current repository baseline and MUST NOT send readers to stale or contradictory active guidance.

## Inputs and outputs

Inputs:

- the root `README.md`
- the accepted README positioning proposal
- the accepted project-direction proposal
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- the shipped proof-of-value example under `docs/changes/0001-skill-validator/`

Outputs:

- a value-first root README that helps visitors qualify the project quickly
- a near-top `When to use / When not to use` section
- a short deeper-reading path to the workflow summary, normative spec, and shipped example
- any minimal linked-summary alignment needed to keep public guidance truthful

## State and invariants

- `README.md` remains the public project overview.
- `docs/workflows.md` remains the short operational summary.
- `specs/rigorloop-workflow.md` remains the normative workflow contract.
- This spec changes entrypoint positioning, not workflow behavior.
- The README continues to describe the project truthfully according to the accepted project direction and current repository baseline.

## Error and boundary behavior

- If the README does not follow the required opening order of title and tagline, opening overview paragraph, `When to use / When not to use`, quick-start or adoption checklist, help or contribution pointer, and only then mechanics/reference content, it does not satisfy this spec.
- If the README includes `When to use / When not to use` but omits either a good-fit or bad-fit case, it does not satisfy this spec.
- If the first audience-defining sentence or bullet does not name individual contributors first, it does not satisfy this spec.
- If the README omits a concise help or contribution pointer that answers the required discovery questions, it does not satisfy this spec.
- If the README claims that RigorLoop replaces Git-based review, CI, or human review, it does not satisfy this spec.
- If the README claims hosted-platform or orchestration behavior that the repository does not provide, it does not satisfy this spec.
- If linked deeper guidance is stale or contradictory, the README change is incomplete until the touched summary surfaces are made truthful.
- If no linked summary surface needs wording or link alignment, implementation MAY leave those files unchanged.

## Compatibility and migration

- Existing workflow rules, validation commands, and source-of-truth ordering remain unchanged.
- Existing deep-mechanics sections may be renamed, moved downward, condensed, or retained as long as they remain truthful and follow the required value-first sections.
- Existing links to the workflow summary, normative spec, and proof-of-value example should remain discoverable after the rewrite.
- This spec does not require a separate documentation site, tutorial series, or branding overhaul.
- Rollback, if needed, is a restoration of earlier README structure and copy, but any truthfully improved references to shipped artifacts may be preserved.

## Observability

- Manual review MUST be able to determine from the top portion of the README:
  - what the project does;
  - why it is useful;
  - who it is for;
  - when to use it;
  - when not to use it;
  - where to go next for deeper workflow, artifact, skill, and contribution guidance.
- Diff review MUST be able to confirm that the README follows the required opening order and introduces value and fit before mechanics/reference content.
- Review of touched summary surfaces MUST be able to confirm that no workflow-rule drift was introduced.

## Security and privacy

- The README and any aligned summary surfaces MUST NOT introduce secrets, credentials, tokens, or private operational details.
- Positioning copy MUST NOT fake adoption, maturity, CI status, or hosted capabilities.

## Accessibility and UX

- The README MUST use clear headings and scannable section ordering suitable for GitHub readers who skim before they read deeply.
- The required `When to use / When not to use` heading MUST remain easy to find near the top of the document.
- Essential meaning MUST remain available in text. Images, badges, or external visuals MAY support the README, but they MUST NOT be required to understand the project's value or fit.

## Edge cases

1. The README may keep a lifecycle summary and repository layout, but only after the value-first overview, qualification guidance, quick-start or adoption-checklist section, and help or contribution pointer.
2. The README may mention maintainers and small teams prominently, but it may not displace individual contributors as the lead audience for the first-release entrypoint.
3. The README may link to `docs/changes/0001-skill-validator/` as a shipped example, but it must not imply that the example's full artifact pack is universal for every non-trivial change.
4. If only `README.md` requires wording changes to satisfy this spec, no broader doc rewrite is required.
5. If a touched public summary surface would need normative workflow edits to align with the new README, that broader change is out of scope for this spec and must be handled separately.

## Non-goals

- Changing workflow rules, stage order, or autoprogression behavior.
- Changing validation command requirements.
- Changing the repository's source-of-truth order.
- Rebranding the project name, logo, or repository structure.
- Creating a project website, hosted product, tutorial suite, or broader docs information-architecture overhaul.
- Adding unsupported maturity, adoption, or production-readiness claims.

## Acceptance criteria

- A first-time visitor can read the top of `README.md` and understand what RigorLoop is, why it is useful, who it is for, and whether it fits their needs before encountering detailed workflow mechanics.
- `README.md` includes a near-top section titled `When to use / When not to use` with at least one good-fit and one bad-fit case.
- The first audience-defining sentence or bullet names individual contributors first, and any maintainer or small-team mention appears only in a secondary clause or later sentence/section.
- The README includes a quick-start path or adoption checklist and a concise help or contribution pointer before any mechanics/reference section.
- The README points readers to active deeper surfaces for workflow, artifact and skill documentation, and contribution or issue reporting, including `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `docs/changes/0001-skill-validator/` where those needs apply.
- The README no longer presents the first proof-of-value rollout as if it were still active implementation focus.
- Any touched linked summary surfaces remain truthful and do not alter workflow rules, validation requirements, or source-of-truth ordering.

## Open questions

None.

## Next artifacts

- implementation under `docs/plans/2026-04-22-readme-user-value-positioning.md`
- change-local artifacts under `docs/changes/2026-04-22-readme-user-value-positioning/`

## Follow-on artifacts

- `docs/plans/2026-04-22-readme-user-value-positioning.md`
- `specs/readme-user-value-positioning.test.md`

## Readiness

Spec review feedback is incorporated.

This spec is approved.

No separate architecture artifact is expected for this slice.

The active execution plan now exists.

The active test spec now exists.

Implementation may proceed under the active plan and active test spec.
