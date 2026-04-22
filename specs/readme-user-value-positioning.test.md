# README User Value Positioning test spec

## Status
- active

## Related spec and plan

- Spec: `specs/readme-user-value-positioning.md`
- Plan: `docs/plans/2026-04-22-readme-user-value-positioning.md`
- Architecture: none. The approved spec and active plan both state that no separate architecture artifact is expected for this slice.

## Testing strategy

- Use manual contract review as the primary proof method because this feature changes contributor-facing documentation behavior rather than executable runtime behavior.
- Use focused repository command checks to support manual review:
  - explicit-path lifecycle validation for touched lifecycle-managed artifacts;
  - `rg` checks for required headings, links, and banned stale wording;
  - `git diff --check` for patch hygiene;
  - `bash scripts/ci.sh` as the repo-owned final validation wrapper.
- Treat README ordering, audience priority, help-pointer truthfulness, and stale-rollout removal as manual acceptance checks over real repository files.
- Reuse the existing `specs/rigorloop-workflow.test.md` surface only if narrow wording or proof-ownership adjustments become necessary; otherwise keep this focused test spec as the primary proof surface for the new README-positioning contract.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R6` | `T1`, `T2` | manual | README acts as public overview and follows the required opening order before mechanics/reference content |
| `R2`, `R2a`, `R2b`, `R2c` | `T1`, `T3` | manual | value-first opening and lead-audience priority are visible in the first audience-defining sentence or bullet |
| `R3`, `R3a`, `R3b` | `T2` | manual | near-top `When to use / When not to use` section and placement rules |
| `R4`, `R4a`, `R4b` | `T1`, `T4` | manual | user outcomes are concrete and truthful, without unsupported claims |
| `R5`, `R5a`, `R5b` | `T5` | manual | quick-start or adoption checklist exists, is placed correctly, and links to the required workflow/example surfaces |
| `R5c`, `R5d`, `R5e`, `R5f`, `R10` | `T6`, `T7` | manual | help/contribution pointer answers all three discovery questions with active, non-placeholder links and truthful destinations |
| `R7`, `R7a` | `T4`, `T8` | manual | README remains faithful to accepted project direction and rejects unsupported positioning |
| `R8`, `R8a` | `T8` | manual | stale rollout phrasing is removed and shipped proof surfaces use durable present-state wording |
| `R9`, `R9a` | `T7`, `T9` | manual | linked summary alignment does not change workflow rules or validation requirements |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T2`, `T5` | first-time contributor can understand value, fit, and next steps before mechanics |
| `E2` | `T3` | maintainer visibility remains secondary to the lead individual-contributor framing |
| `E3` | `T4` | unsupported “replaces PR/CI/human review” positioning is explicitly rejected |
| `E4` | `T8` | stale rollout framing such as `Current Focus` is removed or replaced with durable wording |

## Edge case coverage

- The README may keep workflow summary and repository-layout sections, but only after all required opening sections: `T2`
- Maintainers and small teams may be mentioned prominently later, but not before or equal to individual contributors in the first audience-defining sentence or bullet: `T3`
- The README may link to `docs/changes/0001-skill-validator/` as a shipped example, but it must not imply that the example pack is universal: `T5`, `T8`
- Existing repo surfaces may satisfy the help/contribution pointer without a new `CONTRIBUTING.md`, but if they are missing, stale, or placeholder-only the change must stop rather than guess: `T6`, `T7`
- If `docs/workflows.md` or other linked summary surfaces need alignment, those changes must remain summary-only and must not drift from `specs/rigorloop-workflow.md`: `T9`
- The placeholder security contact in `.github/ISSUE_TEMPLATE/config.yml` must not become a README help link: `T7`

## Test cases

### T1. README opens as a value-first public project overview

- Covers: `R1`, `R1a`, `R1b`, `R2`, `R4`, `E1`
- Level: manual
- Fixture/setup:
  - `README.md`
- Steps:
  - Review the opening of `README.md`.
  - Confirm it starts with the project title, a short tagline or equivalent opening line, and an opening overview paragraph.
  - Confirm the opening overview explains what RigorLoop is, why it is useful, that it is a Git-first starter kit for AI-assisted software delivery, and that it does not replace pull requests, CI, or human review.
- Expected result:
  - A first-time visitor can understand the project value from the top of the README before reaching mechanics-heavy content.
- Failure proves:
  - The README still behaves like a mechanics-first repository memo instead of a public entrypoint.
- Automation location:
  - Manual review plus `rg -n '^# |^## ' README.md`

### T2. README ordering satisfies the required opening sequence

- Covers: `R1a`, `R1b`, `R3`, `R3b`, `R5b`, `R6`, `E1`
- Level: manual
- Fixture/setup:
  - `README.md`
- Steps:
  - Inspect the README section order.
  - Confirm the order is: title/tagline, opening overview paragraph, `When to use / When not to use`, quick-start or adoption checklist, help/contribution pointer, then mechanics/reference content.
  - Confirm no mechanics/reference section appears before those required opening sections.
- Expected result:
  - The README follows the approved opening order exactly enough that a reviewer does not have to guess.
- Failure proves:
  - The README still front-loads workflow mechanics or reference material too early.
- Automation location:
  - Manual review supported by `rg -n '^# |^## ' README.md`

### T3. Audience priority names individual contributors first

- Covers: `R2a`, `R2b`, `R2c`, `E2`
- Level: manual
- Fixture/setup:
  - `README.md`
- Steps:
  - Identify the first audience-defining sentence or bullet in the README.
  - Confirm individual contributors are named first.
  - Confirm any maintainer or small-team mention appears only in a secondary clause after contributors or in a later sentence/section.
  - Confirm the README does not use an equal-priority audience phrase such as “contributors, maintainers, and teams” in that first audience-defining sentence or bullet.
- Expected result:
  - Lead-audience priority is observable and unambiguous.
- Failure proves:
  - The README no longer expresses the approved first-release audience decision clearly enough for reviewers or implementers.
- Automation location:
  - Manual contract review

### T4. User outcomes are concrete and unsupported positioning is absent

- Covers: `R4`, `R4a`, `R4b`, `R7`, `R7a`, `E3`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/proposals/2026-04-19-rigorloop-project-direction.md`
- Steps:
  - Review the README outcome statements.
  - Confirm they are grounded in current repository reality such as reviewability, explicit artifacts, safer AI-assisted delivery, or traceable change rationale.
  - Confirm the README does not rely on unsupported social proof, adoption claims, production-readiness claims, hosted-platform claims, or language claiming to replace Git, PRs, CI, or human review.
- Expected result:
  - The README is persuasive because it is truthful, not because it overclaims.
- Failure proves:
  - The change traded accuracy for marketing language or drifted from accepted project direction.
- Automation location:
  - Manual contract review

### T5. Quick-start or adoption checklist points to required deeper workflow/example surfaces

- Covers: `R5`, `R5a`, `R5b`, `E1`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `docs/changes/0001-skill-validator/`
- Steps:
  - Review the quick-start path or adoption checklist.
  - Confirm it appears after `When to use / When not to use` and before the help/contribution pointer.
  - Confirm it links to `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `docs/changes/0001-skill-validator/`.
  - Confirm the linked surfaces exist and are active repository guidance or shipped example material.
- Expected result:
  - A reader can go from overview to the right deeper workflow/example surfaces without hunting around the repo.
- Failure proves:
  - The README promises a next step but does not route readers to the required deeper surfaces.
- Automation location:
  - Manual review supported by `rg -n 'docs/workflows.md|specs/rigorloop-workflow.md|docs/changes/0001-skill-validator' README.md`

### T6. Help/contribution pointer answers all three R5d discovery questions

- Covers: `R5c`, `R5d`, `R5e`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/plans/2026-04-22-readme-user-value-positioning.md`
- Steps:
  - Review the README’s help/contribution pointer.
  - Confirm it explicitly answers:
    - where to learn the workflow in more detail;
    - where to find artifact and skill documentation;
    - where to learn how to contribute or report issues.
  - Confirm the pointer is concise rather than a long support section.
  - Confirm it follows the R5d help/contribution surface map recorded in the active plan.
- Expected result:
  - A new individual contributor can find all three discovery paths from one compact README section or link group.
- Failure proves:
  - The README still leaves core help/contribution discovery implicit or scattered.
- Automation location:
  - Manual contract review

### T7. R5d links use active, non-placeholder surfaces and stop on insufficient coverage

- Covers: `R5f`, `R10`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `specs/README.md`
  - `skills/`
  - `.github/ISSUE_TEMPLATE/bug.yml`
  - `.github/ISSUE_TEMPLATE/feature.yml`
  - `.github/pull_request_template.md`
  - `.github/ISSUE_TEMPLATE/config.yml`
- Steps:
  - Inspect the actual README link targets used for the three R5d discovery questions.
  - Confirm workflow detail points to `docs/workflows.md` or another active workflow guide.
  - Confirm artifact/skill discovery points to `skills/` and/or another active non-placeholder skill/artifact documentation surface.
  - Confirm contribution or issue reporting points to `.github/ISSUE_TEMPLATE/` and/or `.github/pull_request_template.md`, not to an implied nonexistent `CONTRIBUTING.md`.
  - Confirm the README does not surface the placeholder security contact from `.github/ISSUE_TEMPLATE/config.yml`.
  - If any required discovery need cannot be truthfully satisfied by current surfaces, record that implementation must stop and revisit scope rather than guessing.
- Expected result:
  - Every help/contribution link is active, truthful, and non-placeholder.
- Failure proves:
  - The README is routing users to weak, stale, or invented contributor-help surfaces.
- Automation location:
  - Manual contract review supported by `rg -n 'docs/workflows.md|skills/|specs/README.md|ISSUE_TEMPLATE|pull_request_template|CONTRIBUTING' README.md .github/ISSUE_TEMPLATE .github/pull_request_template.md specs/README.md`

### T8. Stale rollout wording is removed and shipped example language is durable

- Covers: `R8`, `R8a`, `E4`
- Level: manual
- Fixture/setup:
  - `README.md`
- Steps:
  - Review the README for rollout-era wording.
  - Confirm it does not use `Current Focus` or equivalent active-rollout framing for the already-shipped proof-of-value example.
  - Confirm shipped proof surfaces are described in durable present-state language.
- Expected result:
  - The README reflects current repository state rather than frozen rollout status.
- Failure proves:
  - The entrypoint still reads like an implementation-status memo instead of a stable project overview.
- Automation location:
  - Manual review supported by `! rg -n '^## Current Focus$|^Active implementation work is tracked in' README.md`

### T9. Linked summary alignment does not change workflow rules or validation requirements

- Covers: `R9`, `R9a`
- Level: manual
- Fixture/setup:
  - touched linked summary surfaces, especially `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - If any linked summary surfaces are edited, compare their changed wording against the normative workflow spec.
  - Confirm the changes are wording or link-alignment changes only.
  - Confirm no workflow-rule, validation-command, or source-of-truth-order change was introduced.
  - If no linked summary surfaces were edited, record that no further proof was needed beyond the README review.
- Expected result:
  - README alignment does not smuggle in a workflow-contract change.
- Failure proves:
  - A documentation-positioning slice accidentally altered normative contributor behavior.
- Automation location:
  - Manual contract review

## Fixtures and data

- Real repository surfaces, not synthetic fixtures:
  - `README.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `specs/README.md`
  - `skills/`
  - `.github/ISSUE_TEMPLATE/bug.yml`
  - `.github/ISSUE_TEMPLATE/feature.yml`
  - `.github/pull_request_template.md`
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `docs/changes/0001-skill-validator/`
- The active plan acts as a review fixture for the R5d surface map and the stop-if-insufficient rule:
  - `docs/plans/2026-04-22-readme-user-value-positioning.md`

## Mocking/stubbing policy

- No mocks or stubs are needed.
- Use the real repository files as the proof surface because the contract is about contributor-visible documentation behavior and link truthfulness.

## Migration or compatibility tests

- Manual verification that the rewritten README preserves compatibility with the current repository baseline:
  - required deeper links still resolve to active repo surfaces;
  - no existing normative workflow rule is changed;
  - existing deep-mechanics sections may move, but remain truthful if retained.

## Observability verification

- Manual review must be able to determine from the README top section:
  - what the project does;
  - why it is useful;
  - who it is for;
  - when to use it;
  - when not to use it;
  - where to go for workflow, artifact, skill, and contribution guidance.
- `rg` checks should confirm presence of required headings/links and absence of banned stale wording.

## Security/privacy verification

- Confirm the README and any touched summary surfaces do not introduce secrets, private operational details, fake CI status, hosted-capability claims, or placeholder-only support links.
- Confirm the placeholder security contact in `.github/ISSUE_TEMPLATE/config.yml` is not elevated as a README help path.

## Performance checks

- Not applicable. This change is documentation behavior, not runtime behavior.

## Manual QA checklist

- [ ] The README opens with title, tagline, and overview paragraph before any mechanics/reference section.
- [ ] The first audience-defining sentence or bullet names individual contributors first.
- [ ] `When to use / When not to use` appears before quick start, help pointer, and mechanics/reference sections.
- [ ] The `When to use / When not to use` section includes at least one good-fit and one bad-fit case.
- [ ] The README includes a quick-start path or adoption checklist linking to `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `docs/changes/0001-skill-validator/`.
- [ ] The README includes a concise help/contribution pointer that answers all three R5d questions.
- [ ] The README does not imply a nonexistent `CONTRIBUTING.md`.
- [ ] The README does not surface the placeholder security contact.
- [ ] The README no longer contains `Current Focus` or equivalent rollout-era active-state wording.
- [ ] Any touched summary surfaces remain summary-only and do not alter workflow rules or validation requirements.

## What not to test

- Do not create executable product tests; this feature is intentionally documentation-contract driven.
- Do not test unrelated wording polish outside the approved scope.
- Do not test broader docs-site, branding, or tutorial behavior because those are non-goals.
- Do not treat GitHub rendering details beyond heading order and link presence as a contract requirement.

## Uncovered gaps

- None. The approved spec and active plan are specific enough to support manual contract verification without returning to spec or architecture.

## Next artifacts

- `pr`
- downstream merge-closeout lifecycle updates if later stages continue

## Follow-on artifacts

None yet.

## Readiness

This test spec remained aligned through implementation, first-pass `code-review`, `verify`, and `explain-change`.

The next stage is `pr`.
