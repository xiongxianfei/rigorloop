# README User Value Positioning Explain Change

## Summary

This change turns the repository root `README.md` into a value-first public entrypoint for first-time visitors. It moves user value, fit guidance, quick-start links, and contribution discovery ahead of workflow mechanics, removes stale rollout framing, and keeps the change inside the approved documentation-only slice with no workflow-rule or validation-rule changes.

## Problem

The previous README was accurate but mechanics-first. It explained lifecycle structure, artifact locations, and validation commands before it clearly answered the questions a new visitor actually needs first: what RigorLoop is, why it is useful, who it is for, when it fits, and where to go next.

That mismatch mattered because the accepted proposal explicitly chose a README-led positioning fix rather than a broader documentation rewrite. The contract for this initiative required the entrypoint to lead with value, individual contributors as the primary audience, an exact `When to use / When not to use` section, a quick-start path, and a truthful help/contribution pointer.

## Decision trail

- Exploration: none; the problem statement was already concrete enough to move directly into proposal/spec work.
- Proposal: [2026-04-22-readme-user-value-positioning.md](/home/xiongxianfei/data/20260419-rigorloop/docs/proposals/2026-04-22-readme-user-value-positioning.md:1)
- Proposal decision:
  - choose a README-led, value-first rewrite with only minimal linked-summary alignment if needed
  - lead for individual contributors first, keep maintainers and small teams secondary
  - use a near-top `When to use / When not to use` section
  - keep the slice out of workflow-rule, validation, and source-of-truth-order changes
- Spec: [readme-user-value-positioning.md](/home/xiongxianfei/data/20260419-rigorloop/specs/readme-user-value-positioning.md:1)
- Test spec: [readme-user-value-positioning.test.md](/home/xiongxianfei/data/20260419-rigorloop/specs/readme-user-value-positioning.test.md:1)
- Requirements:
  - `R1`-`R10`
- Architecture:
  - none; the approved spec and plan both kept this slice below the architecture threshold
- Plan milestone:
  - `M1. Rewrite the public README entrypoint and align linked summary surfaces`

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `README.md` | rewrote the opening into title, tagline, overview paragraph, exact `When to use / When not to use`, `Quick Start`, and `Learn More / Contribute` before mechanics-heavy sections | satisfy the approved value-first entrypoint contract and make user fit and next steps obvious before lifecycle detail | spec `R1`-`R8a`, proposal recommended direction, plan `M1` | `T1`-`T8`, heading/link/stale-wording checks, manual contract review |
| `README.md` | named individual contributors first and kept maintainers/small teams secondary in the opening overview | make the lead-audience rule reviewable rather than implied | spec `R2a`-`R2c`, spec-review feedback | `T3`, manual audience-priority review |
| `README.md` | added quick-start links to `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `docs/changes/0001-skill-validator/` | provide the required deeper-evaluation path without forcing mechanics into the opening overview | spec `R5`-`R5b`, plan `M1` | `T5`, required-link grep |
| `README.md` | added a concise help/contribution pointer to `docs/workflows.md`, `specs/README.md`, `skills/`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, and `.github/pull_request_template.md` | answer all three `R5d` discovery questions with active, truthful current surfaces and without inventing `CONTRIBUTING.md` | spec `R5c`-`R5f`, plan R5d surface map | `T6`, `T7`, manual link-truthfulness review |
| `README.md` | removed the `Current Focus` section and the active-rollout pointer to the older implementation plan | stop presenting a shipped example as if it were still active implementation work | spec `R8`, `R8a` | `T8`, banned-wording grep |
| `docs/proposals/2026-04-22-readme-user-value-positioning.md` | captured the accepted direction, audience decision, scope guardrails, and readiness for implementation | settle the product-positioning decision before contract and implementation work | proposal stage | lifecycle validation |
| `specs/readme-user-value-positioning.md` | defined the README contract as reviewable requirements, ordering rules, link obligations, and non-goals | make the docs behavior explicit enough to implement and review safely | spec stage | spec review, lifecycle validation |
| `specs/readme-user-value-positioning.test.md` | mapped the README contract into manual proof surfaces and focused command checks | prove the documentation behavior at the right level without inventing runtime tests | test-spec stage, `T1`-`T9` | active test spec, validation notes |
| `docs/plans/2026-04-22-readme-user-value-positioning.md`, `docs/plan.md` | created and maintained the one-milestone execution plan, recorded validation, first-pass review, and verify outcomes, and kept lifecycle readiness truthful | keep initiative state durable and reviewable rather than chat-only | active plan policy, plan `M1` | lifecycle validation, `git diff --check` |
| `docs/changes/2026-04-22-readme-user-value-positioning/change.yaml`, `docs/changes/2026-04-22-readme-user-value-positioning/explain-change.md` | created the baseline change-local pack and recorded the decision trail, validation, and downstream review/verify results | make this non-trivial documentation slice comply with the repository’s docs-changes baseline policy | docs-changes baseline policy, plan `M1` | change-metadata validation, lifecycle validation |

## Tests added or changed

- [readme-user-value-positioning.test.md](/home/xiongxianfei/data/20260419-rigorloop/specs/readme-user-value-positioning.test.md:1)
  - `T1`, `T2`, `T3`, and `T4` prove the README now opens as a value-first project overview, names individual contributors first, and avoids unsupported positioning.
  - `T5`, `T6`, and `T7` prove the quick-start and help/contribution pointers answer the required discovery questions with truthful repo surfaces.
  - `T8` proves stale rollout framing is removed.
  - `T9` protects the invariant that no linked summary surface may drift into workflow-rule changes.
- Test level rationale:
  - manual contract review is the right level because this feature changes contributor-facing documentation behavior rather than executable runtime behavior
  - focused `rg`, lifecycle, metadata, patch-hygiene, and repo-owned CI wrapper commands provide concrete evidence around that manual proof surface

## Review and verification outcomes

- First-pass `code-review`
  - Status: `clean-with-notes`
  - Result: no blocking or required-change findings; the clean result was grounded in the actual diff, the approved artifacts, checklist coverage, and recorded validation evidence
  - Durable location: [the active plan](/home/xiongxianfei/data/20260419-rigorloop/docs/plans/2026-04-22-readme-user-value-positioning.md:237)
- `verify`
  - Verdict: `ready`
  - Result: no blockers, no stale lifecycle drift, and no missing baseline change-local artifacts or validation evidence
  - Durable location: [the active plan](/home/xiongxianfei/data/20260419-rigorloop/docs/plans/2026-04-22-readme-user-value-positioning.md:265)

## Verification evidence

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-readme-user-value-positioning.md --path specs/readme-user-value-positioning.md --path specs/readme-user-value-positioning.test.md --path docs/plans/2026-04-22-readme-user-value-positioning.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-readme-user-value-positioning/change.yaml`
- `rg -n '^# |^## ' README.md`
- `rg -n 'When to use / When not to use|docs/workflows.md|specs/rigorloop-workflow.md|docs/changes/0001-skill-validator|skills/|specs/README.md|ISSUE_TEMPLATE|pull_request_template' README.md docs/workflows.md specs/README.md .github/ISSUE_TEMPLATE .github/pull_request_template.md`
- `! rg -n '^## Current Focus$|^Active implementation work is tracked in' README.md`
- `git diff --check -- README.md docs/workflows.md specs/readme-user-value-positioning.test.md docs/plan.md docs/plans/2026-04-22-readme-user-value-positioning.md docs/changes/2026-04-22-readme-user-value-positioning .github/ISSUE_TEMPLATE/bug.yml .github/ISSUE_TEMPLATE/feature.yml .github/pull_request_template.md specs/README.md`
- `bash scripts/ci.sh`
- manual contract review over:
  - README opening order
  - audience priority
  - required good-fit and bad-fit cases
  - truthful help/contribution pointer coverage for all three `R5d` questions
  - unchanged linked summary surfaces
- Hosted CI status: unobserved from this environment

## Alternatives rejected

- Small wording polish on the old README structure
  - Rejected because it would leave the mechanics-first opening intact and would not solve the actual positioning problem.
- Broader documentation or branding overhaul
  - Rejected because the approved slice was a narrow README-led public-entrypoint improvement, not a docs IA or marketing initiative.
- Inventing a standalone `CONTRIBUTING.md`
  - Rejected because the approved plan required using truthful existing repo surfaces first and stopping if they were insufficient.
- Editing `docs/workflows.md`, `specs/README.md`, issue templates, or the PR template anyway
  - Rejected because those surfaces were already truthful link targets, so changing them would widen scope without improving contract fidelity.

## Scope control

- `docs/workflows.md` was left unchanged because the README’s new quick-start and help links already matched the existing workflow summary truthfully.
- `specs/README.md`, `.github/ISSUE_TEMPLATE/bug.yml`, `.github/ISSUE_TEMPLATE/feature.yml`, and `.github/pull_request_template.md` were left unchanged because they already satisfied the approved help/contribution surface map.
- `AGENTS.md` was left unchanged because this slice did not change practical agent behavior or validation expectations.
- `CONSTITUTION.md` was left unchanged because this slice did not introduce a new governance principle.
- No workflow rule, validation requirement, or source-of-truth-order change was introduced.
- No placeholder security contact was elevated into the README.

## Risks and follow-ups

- Hosted CI still needs to be observed on the eventual PR.
- The README now makes a stronger first impression, but future edits should keep value claims anchored to visible repository behavior and shipped proof surfaces rather than drifting toward unsupported marketing language.
- If later contributor feedback shows that the current issue/PR templates are not enough for “how to contribute” discovery, that follow-up should go through a new proposal/spec slice rather than silently widening this completed change.

## PR-ready summary

- `README.md` now explains RigorLoop’s value, fit, and next steps before workflow mechanics.
- The entrypoint explicitly leads with individual contributors, includes exact fit guidance, and routes readers to the workflow summary, normative workflow spec, shipped example, artifact docs, and contribution/reporting surfaces.
- The change stays documentation-only: no workflow rules, validation requirements, or source-of-truth ordering changed.
- The initiative carries its own accepted proposal, approved spec, active test spec, active plan, change metadata, clean review record, verify result, and durable explanation.

## Readiness

- `explain-change` is complete for this initiative.
- The next stage is `pr`.
- This invocation was a direct `explain-change` request, so no automatic handoff to `pr` was performed here.
