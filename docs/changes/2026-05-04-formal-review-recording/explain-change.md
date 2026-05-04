# Formal Review Recording Change Explanation

## Summary

This change implements the first milestone of the approved formal review recording work. M1 aligns the governing workflow and review-resolution contracts so detailed review records are stage-neutral across proposal, spec, architecture, plan, and code review, while keeping clean reviews proportional and artifact-local when no detailed-record trigger applies.

The implementation is intentionally limited to contract and governance alignment. Validator fixture work, review-stage skill guidance, generated-output refresh, final verification, and PR closeout remain in later milestones.

## Source Artifacts

- Proposal: `docs/proposals/2026-05-04-formal-review-recording.md`
- Spec: `specs/formal-review-recording.md`
- Test spec: `specs/formal-review-recording.test.md`
- Plan: `docs/plans/2026-05-04-formal-review-recording.md`

No architecture artifact was required for M1. The approved spec reuses the existing `docs/changes/<change-id>/reviews/`, `review-log.md`, `review-resolution.md`, and review-artifact validator model without introducing new storage, parser, deployment, or integration architecture.

## M1 Changes

| File or area | Change | Reason |
| --- | --- | --- |
| `specs/review-finding-resolution-contract.md` | Added stage-neutral detailed-record triggers, material and no-material initial review-record root rules, artifact-local clean review settlement, and the rule that symbolic `Resolution:` fields do not by themselves require `review-resolution.md`. | Makes the existing review-resolution contract match the approved formal review recording spec. |
| `specs/review-finding-resolution-contract.test.md` | Added `T17` coverage for formal review recording trigger policy, no-material detailed records without empty `review-resolution.md`, material initial roots, and clean artifact-local settlement. | Keeps the paired test spec aligned with the governing contract changes. |
| `specs/rigorloop-workflow.md` | Added workflow requirements `R12an`-`R12av` for detailed-record triggers, supported formal review stages, no-material roots, and artifact-status authority boundaries. | Makes the lifecycle workflow enforce the same stage-neutral policy. |
| `specs/rigorloop-workflow.test.md` | Added `T27` coverage for workflow-level formal review recording behavior and related edge cases. | Keeps workflow proof aligned with the new requirements. |
| `docs/workflows.md`, `CONSTITUTION.md`, and `AGENTS.md` | Added concise operational and governance wording for detailed formal review record triggers, clean review settlement, and no-material review records without empty `review-resolution.md`. | Prevents contributor-facing guidance from preserving the old code-review-centered behavior. |
| `docs/plan.md` and this plan | Kept the initiative active and documented M1 progress and validation evidence. | Maintains lifecycle traceability while later milestones remain open. |
| `docs/changes/2026-05-04-formal-review-recording/` | Added the baseline change-local `change.yaml` and this durable explanation. | Satisfies the non-trivial change-local artifact baseline for M1. |

## Scope Boundaries

- M1 does not change `scripts/review_artifact_validation.py` or validator fixtures.
- M1 does not update review-stage skills or generated `.codex/skills/` and `dist/adapters/` output.
- M1 does not create `review-resolution.md` because no material review findings exist for this milestone.
- M1 does not add a dedicated `pr-review` stage.
- M1 does not make review files authoritative for proposal, spec, architecture, ADR, or plan status.

## Validation

M1 validation passed with the plan's explicit scope:

- `python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-04-formal-review-recording/change.yaml`
- `bash scripts/ci.sh --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path docs/proposals/2026-05-04-formal-review-recording.md --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/plan.md --path docs/plans/2026-05-04-formal-review-recording.md --path docs/changes/2026-05-04-formal-review-recording/change.yaml --path docs/changes/2026-05-04-formal-review-recording/explain-change.md`
- `git diff --check -- CONSTITUTION.md AGENTS.md docs/workflows.md docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`
- `rg -n '[[:blank:]]$|\\t' CONSTITUTION.md AGENTS.md docs/workflows.md docs/proposals/2026-05-04-formal-review-recording.md specs/formal-review-recording.md specs/formal-review-recording.test.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/plan.md docs/plans/2026-05-04-formal-review-recording.md docs/changes/2026-05-04-formal-review-recording`

The first metadata validation attempt failed because `validation: []` was rejected by the repository metadata validator. The placeholder was replaced with explicit validation records and the metadata validator passed afterward.

## Readiness

M1 is a milestone slice, not full feature completion. The next implementation milestone is M2 validator coverage.
