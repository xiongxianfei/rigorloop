# README User Value Positioning

## Status
- accepted

## Problem

RigorLoop already has a clear internal workflow contract, but the repository entrypoint still describes the project more as a process container than as a useful product for users.

The current `README.md` is accurate about lifecycle stages, artifact locations, and validation commands, yet it undersells the user-facing value:

- it explains the workflow before it clearly explains the user problem;
- it does not quickly tell a new visitor who RigorLoop is for and when they should use it;
- it emphasizes repository mechanics more than outcomes such as clearer reviews, safer AI-assisted delivery, and traceable change history;
- it still carries rollout-era framing such as `Current Focus`, which reads as project-internal status rather than a strong public entrypoint.

That makes it harder for potential users to decide, within the first screen or two, whether this project solves a real problem for them.

## Goals

- Make the repository entrypoint explain what RigorLoop does, why it matters, and who it serves before diving into workflow detail.
- Reframe `README.md` around user value and outcomes rather than mostly around internal artifact structure.
- Preserve the repository's existing rigor and honesty without sounding like an internal process memo.
- Give users a clear "start here" path that points to the right next step for evaluation, adoption, and contribution.
- Align public-facing messaging with accepted project direction and current repository behavior.

## Non-goals

- Redesigning the full workflow contract or changing lifecycle rules.
- Creating a separate project website, docs site, or marketing funnel in this slice.
- Rebranding the project name, logo, or repository structure.
- Adding claims about maturity, adoption, or production readiness that the repository cannot support.
- Rewriting every repository document to match a new voice beyond the small set of public entrypoints affected by the change.
- Changing workflow rules, validation requirements, or the repository's source-of-truth order.

## Context

- The accepted project-direction proposal already defines RigorLoop as an opinionated open-source AI engineering workflow focused on explicit artifacts, reviewability, and auditable change history: [2026-04-19-rigorloop-project-direction.md](/home/xiongxianfei/data/20260419-rigorloop/docs/proposals/2026-04-19-rigorloop-project-direction.md:1).
- `README.md` is the repository's public entrypoint and is explicitly owned as the public project overview in [docs/workflows.md](/home/xiongxianfei/data/20260419-rigorloop/docs/workflows.md:122).
- The current README already explains the workflow accurately, but it opens with mechanics and structure before it clearly answers the visitor's first questions: what the project does, why it is useful, how to get started, and where to get help.
- Current public messaging still contains rollout-stage language under `Current Focus`, even though the first proof-of-value example has already shipped.
- External README guidance from GitHub and Open Source Guides is directionally consistent with the repo need here: a README should explain what the project does, why it is useful, how to get started, and where to get help, and it should present important information in priority order for scanning readers.
  - GitHub Docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
  - GitHub Docs writing guidance: https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs
  - Open Source Guides: https://opensource.guide/starting-a-project/

## Options considered

### Option 1: Do nothing and keep the current README structure

This would keep the current README as-is because it is already mostly accurate about the repository workflow and artifact model.

- Advantages:
  - No review or implementation cost.
  - No risk of wording drift introduced by a rewrite.
  - Preserves the current contributor-facing explanation exactly as shipped.
- Disadvantages:
  - Leaves the core problem unsolved because new visitors still encounter mechanics before value.
  - Preserves rollout-era framing such as `Current Focus`, which now reads as stale public positioning.
  - Assumes accuracy alone is enough, even though the entrypoint still does a weak job of helping users decide whether RigorLoop is for them.

### Option 2: Make only small wording edits to the existing README

This would preserve the current structure and simply tighten a few sentences.

- Advantages:
  - Lowest effort.
  - Minimal review surface.
  - Low risk of wording drift against current specs.
- Disadvantages:
  - Does not fix the core issue that the README leads with mechanics instead of user value.
  - Likely leaves the first-time visitor without a strong reason to keep reading.
  - Preserves the stale rollout-era emphasis and weak "why this matters" framing.

### Option 3: Rewrite the README as a value-first public entrypoint and lightly align adjacent public docs

This would keep the current project scope and workflow intact, but restructure the README so it starts with problem, audience, outcomes, and adoption path, then links deeper workflow detail to `docs/workflows.md` and specs.

- Advantages:
  - Best match for the real problem.
  - Improves first impression without needing a bigger documentation program.
  - Keeps detailed mechanics available without forcing them into the opening sections.
  - Can correct stale rollout wording and make the shipped proof surfaces easier to discover.
- Disadvantages:
  - Requires deliberate copywriting and section reordering, not just cleanup.
  - May require small supporting edits in nearby public docs so linked expectations stay consistent.

### Option 4: Build a broader documentation and branding overhaul

This would go beyond README changes into tutorials, visual assets, a docs IA refresh, and stronger project-brand presentation.

- Advantages:
  - Highest upside for polish and discoverability.
  - Could support multiple user journeys in more depth.
  - Could eventually strengthen adoption and contributor onboarding.
- Disadvantages:
  - Too large for the immediate problem.
  - Risks mixing product positioning, information architecture, and workflow changes into one initiative.
  - Would likely need architecture and planning depth that is not justified by the current request.

## Recommended direction

Choose Option 3.

The repo should treat `README.md` as a value-first entrypoint for new users, not as a compact restatement of the workflow internals.

The revised README should lead with:

- the problem RigorLoop solves;
- the promise it makes to users;
- who it is for and who it is not for, with individual contributors as the lead audience and maintainers and small teams as secondary beneficiaries;
- a near-top `When to use / When not to use` section;
- the concrete outcomes users get from adopting it;
- a short "how to evaluate or get started" path;
- links to deeper workflow, artifact, and contributor documentation.

The core positioning should stay faithful to the accepted project direction:

- RigorLoop helps teams and contributors use AI to build software in a way that remains explicit, reviewable, and auditable.
- It does not replace Git, pull requests, CI, or human review.
- Its power is the disciplined loop from idea to reviewed change with durable artifacts and explainable history.

In practice, the README should stop trying to front-load every workflow detail. It should instead use an inverted-pyramid structure:

1. outcome and audience first;
2. quick understanding and quick-start path second;
3. workflow summary and repository layout after that;
4. deeper operational or normative detail by link, not by overloading the entrypoint.

Supporting public entrypoints such as `docs/workflows.md` may need light alignment if section names, links, or contributor expectations change, but this slice should remain primarily a README-led messaging improvement.

This initiative is positioning-only. It does not change workflow rules, validation requirements, source-of-truth ordering, or any normative behavior contract in `specs/`.

## Expected behavior changes

- Repository visitors will understand the user value of RigorLoop earlier in the README.
- The top of the README will answer why the project matters before listing internal structure.
- The README will more clearly separate "why use this" from "how the workflow works."
- New users will have a clearer path to evaluate the project, find the golden-path example, and decide whether the workflow fits their needs.
- Historical rollout wording such as the current-focus framing will be removed or replaced with more durable project-overview language.
- Adjacent public docs may receive small wording or link updates so the public entrypoint and deeper workflow summary do not drift.

## Architecture impact

Expected impact is limited and documentation-centered.

- Primary surfaces likely affected:
  - `README.md`
  - `docs/workflows.md`
  - possibly other small public entrypoints if they repeat the old positioning
- Boundaries that should remain unchanged:
  - workflow rules and stage policy
  - normative workflow behavior in `specs/`
  - validation requirements and command expectations
  - generated output rules
  - source-of-truth ordering
  - repository scripts and CI behavior

No dedicated architecture artifact is expected unless the change expands into a broader documentation-information-architecture redesign.

## Testing and verification strategy

- Manual review against the accepted product-direction proposal and current workflow contract.
- Manual README quality review against the scoped best-practice questions:
  - Does it explain what the project does?
  - Does it explain why it is useful?
  - Does it tell users how to get started?
  - Does it tell users where to get more help?
- Diff review to confirm the README leads with value and audience before deeper mechanics.
- Targeted drift review of any touched public entrypoints so they do not contradict the README.
- Standard repository validation only if touched files participate in existing repo-owned checks.

## Rollout and rollback

Rollout should be documentation-first and low risk.

- Start with README restructuring and copy changes.
- Make only the minimal adjacent-doc edits required to keep linked guidance truthful.
- Avoid claiming new product capabilities that are not already supported by the repository.

Rollback is straightforward:

- restore the previous README structure and wording if the new entrypoint is judged misleading, too promotional, or inconsistent with the actual workflow.

## Risks and mitigations

- Risk: The README becomes more marketable but less truthful.
  - Mitigation: anchor every claim to existing repository behavior, accepted direction, and visible proof surfaces.
- Risk: The README becomes too abstract and stops helping contributors start.
  - Mitigation: keep a short quick-start or evaluation path near the top and link directly to concrete repo artifacts.
- Risk: Messaging drift appears between `README.md` and deeper workflow docs.
  - Mitigation: scope the implementation to README-first plus any necessary adjacent summary-surface alignment.
- Risk: The change expands into a broad docs rewrite.
  - Mitigation: keep this initiative limited to user-value positioning and entrypoint structure, not full docs IA or branding.
- Risk: The project overstates maturity or readiness.
  - Mitigation: keep wording explicit about what RigorLoop is today, what example it ships, and what it does not replace.

## Open questions

None at proposal stage.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-22 | Treat the problem as user-value positioning, not as a generic docs refresh. | The current issue is not lack of words; it is that the repository entrypoint does not quickly communicate why the project matters to users. | A general cleanup proposal would be too vague to guide a meaningful README rewrite. |
| 2026-04-22 | Keep the recommended slice centered on a README-led entrypoint rewrite with only light adjacent-doc alignment. | This is the smallest change that can materially improve first-contact understanding without widening into a docs-platform effort. | A minimal wording polish would be too weak, and a full docs/branding overhaul would be too broad. |
| 2026-04-22 | Keep detailed workflow mechanics in deeper docs and use the README as an outcome-first entrypoint. | Scanning readers need problem, usefulness, audience, and start path before implementation detail. | Reusing the current README structure would continue to front-load internal mechanics. |
| 2026-04-22 | Lead the README primarily for individual contributors while keeping maintainers and small teams visible as secondary beneficiaries. | The accepted project direction already optimized the first release for individual contributors, so the entrypoint should not reopen that audience decision. | Treating audience as unresolved would invite spec drift in the headline, examples, and quick-start path. |
| 2026-04-22 | Keep this slice strictly out of workflow-contract and validation-rule changes. | The user request is about public positioning, and widening into workflow-rule edits would exceed the smallest truthful change. | Folding normative workflow or validation changes into a README-positioning effort would blur scope and weaken reviewability. |
| 2026-04-22 | Use a near-top `When to use / When not to use` section instead of a short adoption checklist. | This gives scanning readers a fast qualification path without expanding the entrypoint into a setup guide. | A checklist would push the README toward procedural onboarding before readers know whether the project fits their needs. |

## Next artifacts

- `proposal-review`
- likely a focused spec for README-led public positioning and public-entrypoint alignment
- plan and test-spec only if the approved scope expands beyond a small documentation slice

## Follow-on artifacts

- `specs/readme-user-value-positioning.md`
- `docs/plans/2026-04-22-readme-user-value-positioning.md`
- `specs/readme-user-value-positioning.test.md`

## Readiness

- This proposal is accepted.
- The focused follow-on spec now exists and is approved.
- No separate architecture artifact is expected for this slice.
- The active execution plan now exists.
- The active test spec now exists.
- The next stage is `implement`.
