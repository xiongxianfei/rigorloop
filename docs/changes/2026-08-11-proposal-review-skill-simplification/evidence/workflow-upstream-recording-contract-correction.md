# Workflow Upstream Correction: Review-Recording Root Authority

Stage: workflow
Date: 2026-08-11
Change: `2026-08-11-proposal-review-skill-simplification`
Detected while routing: spec authoring
Owning correction stage: proposal

## Conflict

The accepted proposal prohibits an advisory review from creating `docs/changes/<new-change-id>/` or `change.yaml` when material recording is required and no existing root is available.

The higher-priority approved `specs/formal-review-recording.md` contract requires every material finding to have change-local review files, requires change-ID selection to fall back to `YYYY-MM-DD-<topic>-review-recording`, and requires creating or updating the selected review-record root when safe. `AGENTS.md` likewise states that isolation stops handoff rather than recording.

The proposal also lists recording-obligation changes as a non-goal, so specification cannot silently choose the conflicting proposal behavior.

## Route

Workflow routes the narrow contradiction to proposal authoring. The correction must distinguish a generated recording-only root from governed lifecycle continuation: creating required review evidence does not settle the reviewed proposal, activate workflow, or authorize downstream work.

After the substantive correction, formal proposal review must approve the revised artifact before workflow returns to spec authoring. The `test-spec-review` automation target remains active.
