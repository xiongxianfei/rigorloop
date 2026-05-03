# Workflow Refactor Change Explanation

## Status

Verify complete; branch-ready; ready for final `explain-change`.

## Source artifacts

- Proposal: `docs/proposals/2026-05-01-workflow-refactor.md`
- Spec: `specs/rigorloop-workflow.md`
- Test spec: `specs/rigorloop-workflow.test.md`
- Plan: `docs/plans/2026-05-03-workflow-refactor.md`

## M1 changes

M1 aligns root and contributor-facing workflow guidance with the approved workflow category model. The changed guidance distinguishes standing artifacts, living references, workflow infrastructure, on-demand artifacts, the per-change chain, and periodic learning.

The root guidance now treats `docs/project-map.md` as a living reference that cannot be relied on when absent, stale, contradicted, or missing the relied-on area. This change records a no-map rationale in the plan because M1 relies on approved workflow artifacts and bounded root guidance, not on repository-shape claims from a project map.

The M1 guidance also separates `ci-maintenance` from validation execution, keeps `review-resolution` as closeout for material review findings rather than a review stage, and describes `learn` as periodic or explicitly invoked rather than part of the default per-change chain.

## M2 changes

M2 aligns canonical stage skills with the approved workflow contract. `skills/workflow/SKILL.md` now routes by categories, obligation values, triggers, `review-resolution`, and `ci-maintenance` instead of the old overloaded chain.

`skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` now state the standing-artifact gates for first substantive proposals, bootstrap exceptions, and governance/source-of-truth proposals. `skills/ci/SKILL.md` now presents CI work as `ci-maintenance` and separates CI infrastructure from validation execution, test design, and validation-command ownership.

`skills/learn/SKILL.md` now treats `learn` as periodic or explicitly invoked and records the approved temporary closeout options: immediate capture, scheduled follow-up, or explicit no-learn rationale. `skills/verify/SKILL.md` had stale downstream handoff wording, so M2 updates it to hand off to `ci-maintenance` only when hosted workflow automation or related CI infrastructure is triggered.

M2 also adds focused skill-validator assertions for these skill-contract guarantees and regenerates `.codex/skills/` plus generated public adapters under `dist/adapters/` from canonical skill sources.

## M3 changes

M3 adds repository-owned regression coverage for the refactored workflow proof map. `scripts/test-select-validation.py` now covers the workflow-refactor surface set across root guidance, lifecycle artifacts, canonical skill sources, generated skill output, generated adapter output, selector tests, lifecycle tests, skill-validator tests, change metadata, explain-change, review log, and review-resolution.

The selector coverage also proves that broad smoke remains trigger-based: ordinary workflow-refactor paths do not require broad smoke, while active plan, test-spec, and review-resolution trigger contexts can elevate it when they explicitly require broad smoke.

`scripts/test-artifact-lifecycle-validator.py` now covers plan-context expansion to authoritative proposal, spec, test-spec, and architecture artifacts. It also proves that an invalid referenced workflow authority, such as a spec left in transitional `reviewed` status, blocks lifecycle validation when reached through the plan context.

## M4 closeout evidence

M4 closes the change-local evidence slice. The active change-local pack now links the accepted proposal, approved spec, active test spec, active plan, explain-change artifact, review-resolution ledger, touched files, validation records, and current review state through `change.yaml` and this Markdown rationale.

No additional project-map reliance was introduced. `docs/project-map.md` remains absent, and this change continues to rely on the approved proposal, approved workflow spec, active test spec, active plan, root guidance, affected skills, generated-output checks, and bounded file inventories rather than repository-shape claims from a map.

No `learn` trigger was raised during M4. The only material review finding was the already-closed M1 stale-plan wording defect, and later M2/M3 code reviews were clean-with-notes. There was no repeated review pattern, blocker or major workflow-process finding, failed release or adapter smoke, postmortem action, cadence run, or maintainer request requiring immediate learn capture or a scheduled learn follow-up.

No standalone `verify-report.md` was added. The M4 validation evidence remains concise enough to record in `change.yaml` and the active plan; the later `verify` stage still owns the branch-ready conclusion.

## Affected surfaces

- `CONSTITUTION.md`: updated where current wording conflicted with the approved workflow contract.
- `AGENTS.md`: updated for the practical execution chain, project-map no-reliance, learning, autoprogression, and `ci-maintenance` wording.
- `README.md`: updated to present the category model and the per-change chain without implying that `explore`, `research`, `learn`, or CI infrastructure maintenance are default per-change stages.
- `docs/workflows.md`: updated as the short operating summary for categories, obligations, handoffs, and stage boundaries.
- `docs/plan.md` and `docs/plans/2026-05-03-workflow-refactor.md`: updated as lifecycle and execution-plan surfaces for the active refactor.
- `skills/workflow/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/ci/SKILL.md`, `skills/learn/SKILL.md`, and `skills/verify/SKILL.md`: updated in M2 where local skill guidance was affected.
- `.codex/skills/` and `dist/adapters/`: regenerated in M2 from canonical skill sources after the skill guidance changed.
- `scripts/test-select-validation.py` and `scripts/test-artifact-lifecycle-validator.py`: updated in M3 to cover the selector and lifecycle proof required by the active test spec.

## Deferred surfaces

No affected operating or governance surface remains deferred for this refactor. `docs/project-map.md` is intentionally absent and not relied on.

The final learn artifact model is deferred to a later learn refactor. M1 records only the temporary workflow behavior required by the approved workflow spec: capture immediately, schedule follow-up, or record a no-learn rationale when a trigger occurs.

## Validation

Validation evidence is recorded in `change.yaml` and the active plan. The final M4 proof covers change metadata validation, skill validation, skill regression fixtures, generated Codex skill drift, public adapter regression, adapter drift, adapter validation, selector regression, artifact lifecycle regression, explicit lifecycle validation over proposal/spec/test-spec/plan/change-local artifacts, and explicit-path CI over the changed authoritative surfaces.

The verify pass reran the final repository-owned proof over the tracked branch state after `code-review-m4-r1`. It confirmed generated skill and adapter output are in sync, review-resolution is closed, lifecycle-managed artifacts are coherent, the baseline change-local pack exists, and explicit-path CI passes without a broad-smoke trigger. Hosted CI was not observed locally; `.github/workflows/ci.yml` delegates pull-request and main-branch runs to `scripts/ci.sh`.

## Review closeout

`code-review-m1-r1` found one stale-plan wording defect. `review-resolution.md` records the accepted disposition and the plan now states that `specs/rigorloop-workflow.test.md` is active and was updated by the `test-spec` stage before M1.

`code-review-m2-r1`, `code-review-m3-r1`, and `code-review-m4-r1` returned `clean-with-notes` with no material findings. The verify pass found no blockers and marked the branch ready for final `explain-change`.
