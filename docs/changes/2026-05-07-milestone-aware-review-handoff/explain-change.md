# Milestone-Aware Review Handoff Explain Change

## Summary

This change makes clean code review of a milestone aware of whether more in-scope implementation milestones remain. A clean non-final milestone review closes that milestone and routes to the next implementation milestone; only a clean final implementation milestone can route to `verify`.

Status: implementation evidence is current through M4. Final verification and PR-facing explanation still run in the lifecycle-closeout stage.

## Problem

The old workflow guidance treated a clean `code-review` result as a direct handoff to `verify`. That was correct for single-slice or final-milestone work, but it could skip planned implementation milestones in a milestone-based full-feature plan.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Use a milestone loop and reserve `verify` for after all implementation milestones are closed. |
| Spec | Use one `Milestone state` field with `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`. |
| Test spec | Prove the first slice with static wording checks and generated-output drift checks, not executable plan-state validation. |
| Plan | Split proof, authoritative contracts, authored guidance, and generated output into M1 through M4. |
| Architecture | Not required because no runtime boundary, storage, parser, API, or deployment behavior changed. |

## Diff Rationale By Area

| Area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| Static proof | Added and activated skill-validator assertions for milestone-aware state, handoff, and stale shortcut removal. | Proves the guidance cannot retain the unconditional clean-review-to-verify shortcut. | `python scripts/test-skill-validator.py` |
| Workflow contracts | Updated `specs/workflow-stage-autoprogression.md` and `specs/rigorloop-workflow.md`. | Makes the normative full-feature autoprogression contract milestone-aware. | M2 validation notes |
| Operating guidance | Updated `docs/workflows.md`, `AGENTS.md`, and authored `skills/*/SKILL.md` guidance. | Makes contributor and agent routing match the approved milestone loop. | M3 validation notes |
| Generated output | Regenerated `.codex/skills/` and `dist/adapters/` from canonical `skills/`. | Keeps runtime skill mirrors and adapter packages derived instead of stale. | M4 drift checks |
| Change-local evidence | Updated `change.yaml`, this explanation, and the active plan. | Keeps traceability, validation evidence, and handoff state reviewable. | Change metadata validation |

## Tests Added Or Changed

- `scripts/test-skill-validator.py` now runs the milestone-aware guidance checks as ordinary passing tests.
- Existing adapter and generated-output checks prove generated mirrors match canonical skill sources.
- No executable plan-state validator was added.

## Verification Evidence

Implementation validation is recorded in the active plan and `change.yaml`.

Key M4 commands:

- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`

Final lifecycle `verify` is still pending until M4 is reviewed and closed.

## Review Resolution Summary

The plan-review finding `PLR1-F1` was recorded and resolved before implementation. M1, M2, and M3 implementation reviews were clean with no material findings.

## Alternatives Rejected

- Keeping `implementation-complete` or `review-clean` as milestone states was rejected because it creates a parallel or ambiguous state model.
- Adding executable plan-state validation was rejected for this first slice because the approved scope is guidance and static wording checks.
- Adding a standalone `review-resolution` skill was rejected; same-milestone resolution guidance is local to the existing workflow and stage skills.

## Scope Control

This change does not alter fast-lane, bugfix, isolated review, direct `pr`, merge, release, deploy, destructive Git, runtime data flow, persistence, APIs, schemas, or hosted automation behavior.

## Risks And Follow-Ups

- Generated outputs must remain in sync with canonical `skills/`; M4 drift checks cover that.
- Final verify, explain-change closeout, and PR handoff remain lifecycle-closeout work after all implementation milestones are closed.
