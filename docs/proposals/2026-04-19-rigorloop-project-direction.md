# RigorLoop Project Direction

## Status
- accepted

## Problem

AI-assisted software delivery is often fast to draft but hard to review, audit, and trust. Requirements, architecture decisions, tests, verification evidence, and change rationale frequently end up scattered across chats, commits, pull requests, and human memory. That makes it harder for contributors to collaborate safely and harder for maintainers to understand why a change exists.

This repository is still positioned as a generic Codex-ready template. It has the structure for plans, specs, test specs, workflows, and validation, but it does not yet state a concrete public purpose. That leaves contributors without a clear answer to what RigorLoop is, who it serves, and why its workflow should exist instead of a lighter generic template or a heavier AI platform.

Without an explicit direction, follow-on specs and plans are likely to drift between incompatible goals: repository template, workflow documentation set, agent framework, or automation product.

## Goals

- Define RigorLoop as a public open-source AI engineering workflow rather than a generic starter template.
- Make the user value explicit: help teams build software with AI using specs, tests, architecture, review gates, and explainable change history.
- Preserve the repository's current strengths: explicit artifacts, small reviewable diffs, and auditable engineering decisions.
- Establish a direction that can be turned into concrete specs, test specs, and plans without prematurely locking implementation details.
- Keep adoption practical for ordinary Git-based software projects.

## Non-goals

- Building a hosted SaaS product, centralized control plane, or agent runtime as part of this initiative.
- Replacing GitHub, CI systems, or existing code review tools.
- Mandating a single model vendor, editor, or agent interface.
- Defining the full normative workflow contract in this proposal.
- Requiring the full artifact stack for trivial fixes, docs-only edits, or other low-risk maintenance work.
- Solving every process need for every software team.

## Context

- `README.md` is still a placeholder for a generic repository template.
- `docs/workflows.md` and `AGENTS.md` describe process mechanics, but not the product-level identity of the repository.
- The repository already contains the skeleton needed for an artifact-driven workflow: plans, specs, test specs, scripts, and Codex skills.
- There is no existing project map, proposal set, architecture document, or approved feature spec that defines what this repository should become.
- The user direction is that RigorLoop is "an open-source AI engineering workflow for building software with specs, tests, architecture, review gates, and explainable change history."

## Options considered

### Option 1: Keep the repository as a generic Codex-ready template

This keeps the current scope small and flexible.

- Advantages:
  - Lowest immediate effort.
  - Broad reuse across unrelated repositories.
  - Fewer opinionated decisions to defend.
- Disadvantages:
  - Weak public identity.
  - Little differentiation from other AI-assisted repository templates.
  - Does not turn the stated RigorLoop idea into a reviewable product direction.

### Option 2: Position RigorLoop as a broad AI engineering platform

This would frame the project as a runtime or orchestration layer for AI-driven software delivery.

- Advantages:
  - Ambitious vision with large long-term surface area.
  - Could eventually include execution, coordination, and governance features.
- Disadvantages:
  - Misaligned with the current repository, which is mostly workflow artifacts and templates.
  - High architecture and maintenance burden before the core workflow is proven.
  - Risks collapsing product strategy into premature implementation ambitions.

### Option 3: Position RigorLoop as an opinionated open-source workflow with artifact-driven review gates

This treats the repository as the home of a disciplined AI engineering workflow that organizes proposals, specs, test specs, architecture, plans, verification, review, and explainable change history.

- Advantages:
  - Fits the current repository structure and strengths.
  - Makes the value proposition concrete without overcommitting to a platform build.
  - Supports incremental delivery: docs, templates, verification scripts, and examples can evolve in small steps.
- Disadvantages:
  - Can feel process-heavy if the minimum required artifact set is not clearly bounded.
  - Requires careful separation between workflow contract and optional automation.

### Option 4: Narrow the project to one workflow slice, such as spec generation or explainable history

This would produce a tighter first message, but at the cost of fragmenting the intended workflow.

- Advantages:
  - Easier to message and spec initially.
  - Lower surface area for early implementation.
  - Could still be useful as a sequencing tactic inside a broader Option 3 rollout.
- Disadvantages:
  - Undersells the broader workflow described by the user.
  - Creates a risk that the repository evolves around one feature instead of a coherent engineering loop.
  - Works better as a staged entry point than as the whole product position.

## Recommended direction

Choose Option 3.

RigorLoop should be defined as an opinionated open-source AI engineering workflow for people who want AI-assisted software delivery to remain explicit, reviewable, and auditable. The first release should optimize for individual contributors, while still remaining usable by maintainers and small teams. The repository should remain a reusable starter kit rather than a hosted platform, and the workflow should stay as generic as possible so model- or tool-specific guidance can live in optional adapters instead of the core contract.

The core value is not a single automation feature. The value is the loop: teams and contributors move from early framing through explicit review gates, implementation, verification, explanation, and pull request readiness with durable artifacts along the way. That makes the resulting change history explainable instead of opaque.

This direction matches the repository's existing artifact layout while staying small enough to ship incrementally. The reference workflow should be:

- constitution / project-map when needed
- explore
- research when needed
- proposal
- proposal-review
- spec
- spec-review
- architecture
- architecture-review when needed
- plan
- plan-review
- test-spec
- implement
- code-review
- verify
- ci when GitHub workflow automation needed for a material risk is missing or stale
- explain-change
- pr
- learn

The first proof-of-value example should be a skill metadata validator with fixtures and CI. It is small, objective, immediately useful to contributors, and concrete enough to demonstrate the workflow end to end without introducing a larger product feature first.

Later specs should define which stages are mandatory, which are conditional, and what reduced path applies to trivial or low-risk changes so the workflow does not become ceremonial. The intended fast lane is spec -> implement -> verify -> pr for trivial work only.

## Expected behavior changes

- The repository will stop presenting itself as a generic template and start presenting itself as RigorLoop.
- Public documentation will describe a concrete workflow and a first-release audience centered on individual contributors.
- Future repository artifacts will define when exploration, research, proposals, specs, architecture docs, plans, reviews, verification, explanation, and learning are expected.
- The project will publish a first golden-path example based on a skill metadata validator with linked artifacts and verification evidence.
- Trivial and low-risk work will be able to use a reduced fast-lane path instead of the full lifecycle.
- Explain-change information will be split across PR summary, durable artifacts, and machine-readable metadata rather than forced into one place.
- Example flows and templates will increasingly show traceable movement from idea to verified change.
- Automation, if added, will support the workflow rather than redefine it.
- Git, pull requests, CI, and human review will remain the source of truth rather than being replaced by agent orchestration.

## Architecture impact

The expected impact is mostly on repository structure, documentation contracts, and verification helpers rather than application runtime code.

- Primary components affected:
  - `README.md` and public project documentation
  - `docs/workflows.md`
  - `docs/proposals/`, `docs/plans/`, and `specs/`
  - workflow templates, change artifacts, and structured change metadata
  - repository-local skills, helper scripts, and generated distribution output
  - CI checks that validate artifact presence or consistency
- Expected boundary decisions:
  - workflow contract versus optional automation
  - tool-agnostic artifacts versus Codex-specific guidance
  - lightweight adoption path versus stricter governance modes
  - canonical source directories versus generated compatibility output
- Expected high-level flow:
  - constitution / project-map when needed
  - explore
  - research when needed
  - proposal
  - proposal-review
  - spec
  - spec-review
  - architecture
  - architecture-review when needed
  - plan
  - plan-review
  - test-spec
  - implement
  - code-review
  - verify
  - ci when GitHub workflow automation needed for a material risk is missing or stale
  - explain-change
  - pr
  - learn

The initial source-of-truth split should keep generic workflow content separate from Codex-specific guidance. Generic methodology, templates, schemas, and core skills should be edited as the canonical source. Codex-specific instructions should live in an adapter layer, and generated output should be treated as derived distribution rather than authored source.

## Testing and verification strategy

This proposal itself is reviewed as documentation, but the follow-on work should be backed by lightweight verification.

- Documentation review to ensure the project description, workflow terms, and artifact relationships are internally consistent.
- Spec-to-test mapping for any workflow behavior that becomes normative.
- Example-based verification so the documented loop can be followed from artifact to artifact.
- A proof-of-value example should show one individual contributor taking a non-trivial change from explore through PR and learn, including the relevant review gates and an explain-change artifact, using only the repository's documented workflow.
- Early CI should focus on structural correctness rather than subjective quality scoring.
- The first automated checks should validate skills, validate validator fixtures, and detect generated-output drift.
- CI checks for broader repository conventions can expand once the workflow contract is stable.
- Regression checks for scripts or templates that encode workflow rules.

## Rollout and rollback

Rollout should be documentation-first.

- Introduce the project direction through proposal, spec, and public docs before broader automation changes.
- Keep the existing file layout where possible so early adoption does not require repository migration.
- Phase in stricter validation only after the workflow contract is explicit.

Rollback is straightforward because the early changes are artifact and documentation oriented.

- If the direction proves too opinionated, the repository can fall back to a generic template posture.
- If specific workflow elements create friction, they can be kept optional in the spec instead of being enforced in automation.

## Risks and mitigations

- Risk: The workflow becomes too ceremonial for small changes.
  - Mitigation: Define explicit thresholds for when each artifact is required versus optional.
- Risk: The project appears locked to Codex or a single model provider.
  - Mitigation: Keep workflow artifacts tool-agnostic and treat agent-specific guidance as an adapter layer.
- Risk: A starter kit that tries to encode the entire workflow at once becomes hard for individual contributors to adopt.
  - Mitigation: Ship the full reference loop, but explicitly define optional stages, reduced paths for low-risk changes, and concrete examples for common work sizes.
- Risk: Early automation becomes brittle by trying to judge writing quality or workflow philosophy instead of structural correctness.
  - Mitigation: Start with high-value structural validation and drift detection, not subjective scoring.
- Risk: Documentation and automation drift apart.
  - Mitigation: Add example-driven verification and small CI checks once the contract is stable.
- Risk: The scope expands into a platform before the workflow is validated.
  - Mitigation: Keep this initiative focused on workflow definition and repository behavior, not runtime orchestration.
- Risk: Explainable change history remains too vague to implement consistently.
  - Mitigation: Turn that concept into a later spec with concrete artifact expectations and examples.

## Open questions

- What exact change-classification rules should distinguish fast-lane work from full-lifecycle work?

These questions are now implementation-shaping details rather than unresolved product-direction decisions. They should be resolved in the spec and architecture work rather than by reopening the overall direction.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-19 | Frame RigorLoop as an opinionated open-source AI engineering workflow with artifact-driven review gates. | This best matches the repository's current structure and the user-stated value of specs, tests, architecture, review gates, and explainable change history. | A generic template was too weak, a broad platform was too premature, and a single-slice workflow product was too narrow. |
| 2026-04-19 | Optimize the first release for individual contributors. | This gives the project a concrete initial user while still allowing maintainers and teams to benefit later. | Targeting all user segments equally would keep the value proposition vague. |
| 2026-04-19 | Keep RigorLoop as a reusable starter kit with generic core workflow artifacts. | This aligns with the current repository shape and reduces vendor or tool lock-in. | A hosted platform or a tightly vendor-specific workflow would be too constraining. |
| 2026-04-19 | Treat explainable change history as a combination of PR narrative, repository artifacts, and structured metadata. | No single representation is sufficient on its own for clarity, reuse, and automation. | PR-only, artifact-only, or metadata-only approaches were too incomplete. |
| 2026-04-19 | Use a full lifecycle that runs from optional constitution/project-map work through explore, proposal, spec, architecture, plan, implementation, review, verification, explain-change, PR, and learn. | This captures the project vision as a coherent engineering loop with explicit quality gates and post-change learning rather than a collection of isolated practices. | Defining only one slice would underrepresent the intended workflow, and omitting review checkpoints would weaken rigor. |
| 2026-04-19 | Use a skill metadata validator with fixtures and CI as the first proof-of-value example. | It provides immediate contributor value, objective validation, and a compact demonstration of the workflow. | Starting with a new skill or a larger feature would be harder to verify objectively. |
| 2026-04-19 | Use a fast lane of spec -> implement -> verify -> pr for trivial work. | This preserves trust while avoiding full-lifecycle overhead on low-risk changes. | Requiring the full lifecycle for every change would make adoption too heavy, and using no structured path would reduce trust. |
| 2026-04-19 | Phase workflow enforcement from structure and validation first to artifact presence and traceability later. | This keeps early adoption practical while leaving room for stronger rigor after the contract stabilizes. | Enforcing full traceability immediately would likely create brittle process before the workflow proves value. |
| 2026-04-19 | Separate generic workflow content from Codex-specific adapters and generated distribution. | This keeps the core method portable while still supporting Codex-specific installation and compatibility output. | Mixing methodology, adapters, and generated output would increase drift and vendor coupling. |
| 2026-04-19 | Require visible review disposition for every review item, but require a standalone review-resolution artifact only when the review has durable value. | The durable invariant is the decision record, not the file shape, which keeps trust without adding unnecessary ceremony to small reviews. | Requiring `review-resolution.md` for every reviewed change would be too heavy for early adoption. |
| 2026-04-19 | Leave exact repository layout details to the architecture artifact while preserving source-of-truth separation in the workflow contract. | The workflow spec should define invariants and required paths, while architecture should define the concrete repository layout for authored sources, adapters, and generated output. | Hardcoding the entire directory layout into the workflow contract would make early evolution harder without improving the core methodology. |
| 2026-04-19 | Treat the `ci` stage as creating or updating GitHub workflows for material-risk changes, not routine CI execution. | This keeps the lifecycle aligned with the `ci` skill's purpose while leaving routine PR CI enforcement to verification and repository rules. | Treating `ci` as routine CI execution would blur the difference between automation maintenance and normal PR validation. |

## Follow-on artifacts

- `specs/rigorloop-workflow.md`
- `specs/rigorloop-workflow.test.md`
- `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
- `docs/plans/2026-04-19-rigorloop-first-release-implementation.md`

## Readiness

Proposal review is complete. This proposal was accepted and is now part of the merged first-release baseline.

No further proposal-stage action is pending for this artifact.
