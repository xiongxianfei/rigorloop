# README user value positioning plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-22
- Last updated: 2026-04-22
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved README positioning contract as a narrow documentation change that makes RigorLoop's value, fit, and next steps clear to first-time visitors without changing workflow rules or widening into a broader documentation overhaul.

This initiative should make the public entrypoint do five things before it dives into mechanics:

- explain what RigorLoop is and why it matters;
- make individual contributors the explicit lead audience;
- help a reader qualify fit through `When to use / When not to use`;
- provide a short quick-start or adoption path; and
- point readers to deeper workflow, artifact, skill, and contribution/reporting surfaces.

The implementation must stay inside the approved slice:

- no workflow-rule changes;
- no validation-rule changes;
- no source-of-truth-order changes;
- no separate docs site, branding overhaul, or tutorial suite;
- no new standalone contributor portal unless existing surfaces prove insufficient and the scope is explicitly revisited.

## Source artifacts

- Proposal: `docs/proposals/2026-04-22-readme-user-value-positioning.md`
- Spec: `specs/readme-user-value-positioning.md`
- Spec-review findings carried into this plan:
  - the first audience-defining sentence or bullet must name individual contributors first;
  - the README must include a concise help or contribution pointer that helps a new contributor find workflow detail, artifact/skill docs, and contribution or issue-reporting paths;
  - the README opening order is concrete: title/tagline, opening overview, `When to use / When not to use`, quick start or adoption checklist, help / contribution pointer, then mechanics/reference content.
- Architecture: none. The approved spec says no separate architecture artifact is expected for this slice.
- Architecture-review findings: none.
- Test spec: `specs/readme-user-value-positioning.test.md` is now active and owns the manual contract proof for README ordering, audience priority, fit guidance, help/contribution discovery, link truthfulness, and stale-rollout removal.
- Related workflow and proof surfaces:
  - `README.md`
  - `docs/workflows.md`
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `specs/README.md`
  - `.github/ISSUE_TEMPLATE/bug.yml`
  - `.github/ISSUE_TEMPLATE/feature.yml`
  - `.github/pull_request_template.md`
  - `docs/changes/0001-skill-validator/`
  - `skills/`

## Context and orientation

- The current `README.md` is accurate about workflow mechanics, but it still opens with structure and lifecycle detail before it clearly communicates user value, fit, and next steps.
- The current README still contains rollout-era framing under `Current Focus`, even though the first proof-of-value example already shipped.
- The approved spec requires a specific opening order and a near-top `When to use / When not to use` section before mechanics-heavy or reference-heavy content.
- The approved spec also requires help and contribution discovery, but the repository does not currently have a standalone `CONTRIBUTING.md`.
- Existing contributor-help surfaces that can satisfy the approved spec without creating a new guide are:
  - `docs/workflows.md` for the short workflow summary;
  - `specs/rigorloop-workflow.md` for the normative workflow contract;
  - `specs/README.md` and `skills/` for artifact and skill documentation discovery;
  - `.github/ISSUE_TEMPLATE/bug.yml` and `.github/ISSUE_TEMPLATE/feature.yml` for issue reporting;
  - `.github/pull_request_template.md` as a contributor-visible PR expectation surface;
  - `docs/changes/0001-skill-validator/` as the shipped proof-of-value example.
- R5d help and contribution surface map:

| R5d question | Required README answer | Current repository surface | Decision |
| --- | --- | --- | --- |
| Where can I learn the workflow in more detail? | Link to the workflow guide. | `docs/workflows.md` | Use this surface if it exists and contains active workflow guidance. |
| Where can I find artifact and skill documentation? | Link to active skill/artifact documentation. | `skills/` and/or the closest active skill/artifact documentation surface in the repo | Use only if the linked surface contains non-placeholder documentation. |
| Where can I learn how to contribute or report issues? | Link to active issue/PR contribution entry points. | `.github/ISSUE_TEMPLATE/` and `.github/pull_request_template.md` | Use these current surfaces because the repo does not yet have `CONTRIBUTING.md`. Do not imply a standalone contributor guide exists. |
- If any mapped surface is missing, placeholder-only, stale, or not truthful, stop implementation and revisit scope instead of guessing.
- Do not invent a link to `CONTRIBUTING.md` unless that file is created in the same change.
- `.github/ISSUE_TEMPLATE/config.yml` contains a placeholder security contact URL. Do not elevate that link into the README as a recommended help path for this slice.
- The repository currently has no `docs/project-map.md`. The change is narrow enough that a project map is not required for planning.
- This is ordinary non-trivial work. Implementation must carry the baseline change-local pack:
  - `docs/changes/2026-04-22-readme-user-value-positioning/change.yaml`
  - `docs/changes/2026-04-22-readme-user-value-positioning/explain-change.md`

## Non-goals

- Changing workflow rules, stage order, autoprogression behavior, validation commands, or source-of-truth order.
- Creating a separate documentation site, tutorial suite, or branding overhaul.
- Rebranding the project name, logo, or repository structure.
- Adding unsupported maturity, adoption, or production-readiness claims.
- Creating a new standalone `CONTRIBUTING.md` or support page unless implementation proves the approved help-pointer contract cannot be satisfied with existing active surfaces.
- Surfacing the placeholder security contact from `.github/ISSUE_TEMPLATE/config.yml` as a recommended README help link.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R4b`, `R8`-`R8a`, accessibility and acceptance criteria for value-first ordering | `README.md` |
| `R5`-`R5f`, `R10`, observability for deeper guidance and contribution discovery | `README.md`, existing linked surfaces such as `docs/workflows.md`, `specs/README.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, `.github/pull_request_template.md` if a narrow truthfulness fix is needed |
| `R6`-`R7a`, `R9`-`R9a`, compatibility and invariant boundaries | `README.md`, `docs/workflows.md` only if alignment wording is needed, plus manual contract review against `specs/rigorloop-workflow.md` |
| lifecycle truthfulness for this initiative | `docs/proposals/2026-04-22-readme-user-value-positioning.md`, `specs/readme-user-value-positioning.md`, `docs/plans/2026-04-22-readme-user-value-positioning.md`, `docs/plan.md`, explicit-path artifact validation |

## Milestones

### M1. Rewrite the public README entrypoint and align linked summary surfaces

- Goal:
  - Make the root README satisfy the approved value-first contract and update only the minimal linked summary surfaces needed to keep public guidance truthful.
- Requirements:
  - `R1`-`R10`
- Files/components likely touched:
  - `README.md`
  - `docs/workflows.md` only if wording or link alignment is needed
  - `specs/README.md` only if a narrow wording clarification is needed as a linked help surface
  - `.github/ISSUE_TEMPLATE/bug.yml` and `.github/ISSUE_TEMPLATE/feature.yml` only if a narrow truthfulness or readability fix is needed for README-linked issue reporting
  - `.github/pull_request_template.md` only if a narrow wording clarification is needed as a linked contribution surface
  - `docs/changes/2026-04-22-readme-user-value-positioning/change.yaml`
  - `docs/changes/2026-04-22-readme-user-value-positioning/explain-change.md`
- Dependencies:
  - approved proposal
  - approved spec
  - `plan-review`
  - active test spec now exists and remains the required proof surface for implementation
- Tests to add/update:
  - use the active `specs/readme-user-value-positioning.test.md` as the manual proof surface for `R1`-`R10`
  - update `specs/rigorloop-workflow.test.md` only if its existing README-facing proof needs a narrow ownership or wording adjustment after the new focused test spec is introduced
- Implementation steps:
  - rewrite `README.md` to follow the approved opening order exactly;
  - make the first audience-defining sentence or bullet name individual contributors first;
  - add a near-top `When to use / When not to use` section with at least one good-fit and one bad-fit case grounded in the approved spec;
  - add a short quick-start path or adoption checklist that points to `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `docs/changes/0001-skill-validator/`;
  - add a concise `Learn more / contribute` style pointer that tells readers where to learn the workflow, where to find artifact and skill documentation, and where to contribute or report issues using existing active surfaces;
  - apply the recorded R5d help/contribution surface map and stop if any required discovery need cannot be truthfully satisfied by current active repository surfaces;
  - remove rollout-era phrasing such as `Current Focus` and replace it with durable shipped-state wording;
  - inspect `docs/workflows.md`, `specs/README.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, and `.github/pull_request_template.md` as possible link targets;
  - edit those linked surfaces only if a narrow truthfulness fix is required to support the README's new help or contribution pointers;
  - explicitly check whether `AGENTS.md` or `CONSTITUTION.md` are affected; if not, record the no-change decision in validation notes instead of leaving the omission implicit;
  - create the baseline change-local pack for this initiative.
- Validation commands:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-readme-user-value-positioning.md --path specs/readme-user-value-positioning.md --path specs/readme-user-value-positioning.test.md --path docs/plans/2026-04-22-readme-user-value-positioning.md`
  - `rg -n '^# |^## ' README.md`
  - `rg -n 'When to use / When not to use|docs/workflows.md|specs/rigorloop-workflow.md|docs/changes/0001-skill-validator|skills/|specs/README.md|ISSUE_TEMPLATE|pull_request_template' README.md docs/workflows.md specs/README.md .github/ISSUE_TEMPLATE .github/pull_request_template.md`
  - `! rg -n '^## Current Focus$|^Active implementation work is tracked in' README.md`
  - `git diff --check -- README.md docs/workflows.md specs/readme-user-value-positioning.test.md docs/plan.md docs/plans/2026-04-22-readme-user-value-positioning.md docs/changes/2026-04-22-readme-user-value-positioning .github/ISSUE_TEMPLATE/bug.yml .github/ISSUE_TEMPLATE/feature.yml .github/pull_request_template.md specs/README.md`
  - `bash scripts/ci.sh`
  - manual contract review that:
    - the first audience-defining sentence or bullet names individual contributors first;
    - the README opening order matches the approved spec;
    - the README answers all three R5d discovery questions with active, non-placeholder links:
      - workflow detail -> `docs/workflows.md`
      - artifact/skill documentation -> `skills/` and/or another active non-placeholder skill/artifact documentation surface
      - contribution or issue reporting -> `.github/ISSUE_TEMPLATE/` and `.github/pull_request_template.md`
    - the help/contribution pointer uses truthful active repository surfaces and does not elevate the placeholder security contact or imply a standalone `CONTRIBUTING.md` exists when it does not.
- Expected observable result:
  - the top of `README.md` tells first-time visitors what RigorLoop is, why it is useful, who it is for, when to use it, when not to use it, and where to go next before any mechanics/reference section appears;
  - stale rollout wording is gone from the README;
  - any touched linked summary surfaces remain truthful and do not alter workflow rules or validation requirements.
- Commit message:
  - `M1: implement README user-value positioning`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - the README becomes more promotional than truthful;
  - the help/contribution pointer forces scope creep because there is no standalone `CONTRIBUTING.md`;
  - a touched linked surface introduces workflow drift;
  - a README link accidentally points to a placeholder or stale surface.
- Rollback/recovery:
  - revert to the previous README wording if the new copy overstates capabilities;
  - keep link targets limited to existing active surfaces instead of inventing new docs mid-slice;
  - if satisfying the approved help-pointer contract would require a new contributor guide or workflow-rule change, stop and revisit scope through spec/proposal rather than expanding implementation silently.

## Validation plan

- Planning-stage validation:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-readme-user-value-positioning.md --path specs/readme-user-value-positioning.md --path docs/plans/2026-04-22-readme-user-value-positioning.md`
  - `git diff --check -- docs/plan.md docs/proposals/2026-04-22-readme-user-value-positioning.md specs/readme-user-value-positioning.md docs/plans/2026-04-22-readme-user-value-positioning.md`
- Milestone validation:
  - use the commands listed under `M1`
- Review-time validation expectations:
  - `plan-review` should confirm the milestone remains one coherent docs slice and that the help/contribution pointer does not smuggle in a new contributor-doc project;
  - the active test spec now owns the opening-order, audience-priority, fit guidance, help-pointer, and stale-rollout-removal manual contract checks;
  - final implementation should rerun milestone-targeted checks and `bash scripts/ci.sh`.

## Risks and recovery

- Risk: the README over-corrects into marketing language that is not grounded in visible repository behavior.
  - Recovery: anchor copy to approved positioning and existing proof surfaces; reject unsupported claims during code review.
- Risk: the absence of `CONTRIBUTING.md` pushes implementation into an unplanned contributor-doc creation effort.
  - Recovery: use existing active surfaces first; if those prove insufficient, stop and revisit scope rather than widening the milestone silently.
- Risk: README-linked issue or contribution surfaces are technically present but not good public entrypoints.
  - Recovery: make only small truthfulness/readability fixes to the linked surfaces that are already in scope as potential targets; do not redesign GitHub intake flows.
- Risk: editing `docs/workflows.md` accidentally changes workflow meaning instead of only aligning wording.
  - Recovery: keep `specs/rigorloop-workflow.md` as the normative contract and treat any needed wording change in `docs/workflows.md` as summary-only.

## Dependencies

- `plan-review` must complete before implementation starts.
- the active test spec must remain current before production doc changes begin.
- No separate architecture artifact is planned; if implementation expands beyond README positioning and narrow linked-summary alignment, stop and revisit scope before coding.
- The baseline change-local pack for this ordinary non-trivial change is required during implementation.

## Progress

- [x] 2026-04-22: proposal accepted and focused spec approved.
- [x] 2026-04-22: plan created and indexed in `docs/plan.md`.
- [x] 2026-04-22: `specs/readme-user-value-positioning.test.md` created and activated.
- [x] 2026-04-22: `M1` rewritten `README.md` into the approved value-first order and created the baseline change-local pack under `docs/changes/2026-04-22-readme-user-value-positioning/`.

## Decision log

- 2026-04-22: No separate architecture artifact is planned. Rationale: the approved spec is limited to public-entrypoint positioning and narrow linked-summary alignment, not system-shape or workflow-design changes.
- 2026-04-22: Start with one implementation milestone. Rationale: the expected authored surfaces are small enough for one coherent docs review loop and one milestone commit.
- 2026-04-22: Use existing active repository surfaces for help and contribution discovery instead of planning a new standalone contributor guide. Rationale: the approved spec requires discoverability, not a new documentation program.
- 2026-04-22: Do not elevate `.github/ISSUE_TEMPLATE/config.yml` in the README. Rationale: its security contact URL is still a placeholder and would be misleading as a public help path.
- 2026-04-22: Do not update `AGENTS.md` or `CONSTITUTION.md` in `M1`. Rationale: the README rewrite changes public positioning only; it does not change governance, practical agent behavior, or validation expectations.
- 2026-04-22: Leave `docs/workflows.md`, `specs/README.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, and `.github/pull_request_template.md` unchanged in `M1`. Rationale: they are already truthful link targets for the approved quick-start and help/contribution pointer, so editing them would widen scope without improving contract fidelity.

## Surprises and discoveries

- 2026-04-22: The repository currently has no `docs/project-map.md`; the slice is narrow enough that no project map is needed.
- 2026-04-22: The repository currently has no standalone `CONTRIBUTING.md`; existing active surfaces must carry the approved help/contribution discovery requirement unless scope is revisited.
- 2026-04-22: `.github/ISSUE_TEMPLATE/config.yml` still contains a placeholder security contact URL and should not be surfaced as recommended user help.
- 2026-04-22: The existing issue templates and PR template were sufficient to satisfy the approved contribution/reporting pointer without inventing a new contributor guide.

## Validation notes

- 2026-04-22: `test-spec` created `specs/readme-user-value-positioning.test.md` as the active manual proof surface for `R1`-`R10`, including the R5d surface map, required opening order, and stale-rollout-removal checks.
- 2026-04-22: `M1` validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-readme-user-value-positioning.md --path specs/readme-user-value-positioning.md --path specs/readme-user-value-positioning.test.md --path docs/plans/2026-04-22-readme-user-value-positioning.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-readme-user-value-positioning/change.yaml`
  - `rg -n '^# |^## ' README.md`
  - `rg -n 'When to use / When not to use|docs/workflows.md|specs/rigorloop-workflow.md|docs/changes/0001-skill-validator|skills/|specs/README.md|ISSUE_TEMPLATE|pull_request_template' README.md docs/workflows.md specs/README.md .github/ISSUE_TEMPLATE .github/pull_request_template.md`
  - `! rg -n '^## Current Focus$|^Active implementation work is tracked in' README.md`
  - `git diff --check -- README.md docs/workflows.md specs/readme-user-value-positioning.test.md docs/plan.md docs/plans/2026-04-22-readme-user-value-positioning.md docs/changes/2026-04-22-readme-user-value-positioning .github/ISSUE_TEMPLATE/bug.yml .github/ISSUE_TEMPLATE/feature.yml .github/pull_request_template.md specs/README.md`
  - `bash scripts/ci.sh`

## Outcome and retrospective

- This plan is active. Outcome notes and retrospective lessons will be recorded after implementation and verification are complete.

## Readiness

- `plan-review` feedback is incorporated.
- The active test spec now exists.
- Ready for `implement`.
