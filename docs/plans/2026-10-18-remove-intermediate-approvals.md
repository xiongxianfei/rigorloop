# Remove intermediate approval gates

## Purpose / big picture

The maintainer selected: remove intermediate requirement, design and plan approvals; keep final independent review and verification. Requirements, logical behavior, architecture and delivery reasoning remain necessary where relevant, but their authors may establish a usable basis within existing authority without separate stage approval.

## Current Handoff Summary

Owning Change: `2026-10-18-remove-intermediate-approvals`. Mutable progress and assessment evidence belong to its CLI handoff. The direct user decision authorizes the policy change and removes intermediate approval prerequisites for this work; final review and Verify remain required.

## Source artifacts

- Existing IR-009 guided-work and IR-004 assessment needs; refine SR-054, SR-080–083 and affected shared assessment criteria while preserving identities.
- [Workflow](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md), [Assessment](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md) and [Authoring](../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md).
- [Record persistence](../../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md) owns basis admission and closeout prerequisites; CLI exposes the same supported tasks.

## Context and orientation

Use one loop: reconcile the request, refine affected logical behavior and architecture, allocate proportionate work/proof, implement, independently review the whole change, then verify. Optional specialist reviews remain available. Missing authority, unresolved material decisions, failed checks and open findings still prevent unsupported continuation or completion.

The existing v2 request/v4 record shapes already admit a nullable Basis review reference. An owner-selected accepted Basis with no review is not an independent approval. An explicitly linked formal review remains a reliance dependency, including adverse or stale support. Existing stored judgments and completed accounts retain their meaning. No storage migration or automatic rewriting of customer state is required; older executables reject review-free accepted bases and non-code advisory reviews, including reads of active stores containing them. Do not mix writers or claim downgrade compatibility; use an explicit selected-work disposition before changing installed tooling.

## Non-goals

No removal of final review or Verify, external-action permissions, requirement semantics, test obligations or storage. No release, publication, historical cleanup campaign or empirical productivity claim.

## Requirements covered

SR-080/081 govern usable requirement/design bases and distinct authoring responsibilities. SR-054/082 govern continuation and final review. SR-027–029 retain truthful evidence and review reliance; SR-083 governs coherent consumer updates and historical preservation.

## Milestones

1. Reconcile current requirements, affected behavior/allocation, Constitution, Workflow and Assessment with the selected policy. Keep design reasoning with its existing owners; shorten design instructions into locate, refine, challenge and handoff.
2. Update CLI admission and completion, specialist skills and shared resources together. Regenerate projections through existing tools. Demonstrate accepted bases and final completion with no intermediate reviews, while rejecting missing final review, missing/stale final Verify, unresolved findings and unsupported explicitly linked reviews.
3. Run affected repository checks, resolve failures and prepare the complete candidate for one independent whole-change review, followed by separate Verify.

## Final review checkpoint

Independent whole-change Code Review assesses requirement fidelity, combined design, implementation, tests, generated resources and compatibility. Corrections return to their owners and receive proportionate reassessment. Final Verify follows applicable approval; no intermediate approval is substituted for this gate.

## Change-level verification

Exercise the real CLI in an isolated project: select requirement/design bases without intermediate review records, record completed work and the delivery basis, obtain independent code-review approval, record final Verify and complete. Negative variations preserve author/reviewer separation, selected-review dependencies, open findings and stale-support rejection. Existing fully reviewed records must remain readable and keep their original support.

## Validation plan

- Qualified Node: `node --test packages/rigorloop/test/operational-review.test.js packages/rigorloop/test/operational-reliance.test.js` for admission, completion and retained reliance.
- `python3 scripts/project-operational-guidance.py --check` and existing shared-resource projection checks for generated guidance parity.
- `bash scripts/ci.sh --mode local` with the qualified Node and available D2/browser tools for the complete selected scope.
- `git diff --check` and focused prose/link checks for current explanations.

## Risks and recovery

The main risk is leaving an old gate in a consumer or accidentally weakening final assurance. Audit affected current sources and test both successful review-free progression and protected failure paths. Preserve optional review dependencies and historical bytes. Revert source and generated changes together if qualification fails; do not restore old admission code over newly written review-free records without an explicit compatibility disposition.

## Dependencies and material rationale

No new package or service is needed. Tests use the existing SQLite-capable Node toolchain. Final independent assessment requires an actual separate reviewer; this plan grants no permission to spawn agents. The selected change reduces mandatory approvals, not the completeness of the final claim.

## Readiness

See the owning Change for current work, evidence and review standing.
