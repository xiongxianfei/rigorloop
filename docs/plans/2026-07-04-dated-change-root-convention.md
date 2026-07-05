# Dated Change-Root Convention Plan

## Status

Plan lifecycle state: done
Terminal disposition: closed

- Owner: maintainer
- Change ID: 2026-07-04-dated-change-root-convention
- Start date: 2026-07-04
- Last updated: 2026-07-05
- Related issue or PR: PR #121, https://github.com/xiongxianfei/rigorloop/pull/121
- Supersedes: none

## Purpose / big picture

Clarify the default change ID convention for workflow-managed change roots so agents and users create `docs/changes/YYYY-MM-DD-slug/` instead of undated change roots when no explicit change ID already exists.

## Source artifacts

- Spec: [RigorLoop Workflow](../../specs/rigorloop-workflow.md)
- Test spec: [RigorLoop Workflow test spec](../../specs/rigorloop-workflow.test.md)
- Change metadata: [change.yaml](../changes/2026-07-04-dated-change-root-convention/change.yaml)
- Explain-change: [explain-change.md](../changes/2026-07-04-dated-change-root-convention/explain-change.md)

## Current Handoff Summary

- Current milestone: lifecycle closeout
- Current milestone state: closed
- Latest review evidence: none; lightweight workflow documentation sync
- Last reviewed milestone: none
- Review status: not-required; stage=code-review; round=none
- Remaining in-scope implementation milestones: none
- Next stage: none
- Final closeout readiness: ready
- Reason final closeout is or is not ready: PR #121 merged; implementation, validation evidence, explain-change, and main synchronization are complete.

## Milestones

### M1. Clarify Dated Change-Root Convention

- Milestone state: closed
- Goal: Define `YYYY-MM-DD-slug` as the default new workflow-managed change-root convention and centralize detailed guidance in `docs/workflows.md`.
- Requirements: R25i
- Exit criteria: workflow docs, workflow skill, implement skill, test spec, and static validation align on the dated convention.

## Validation

- `bash scripts/ci.sh --mode explicit --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/implement/SKILL.md --path scripts/test-skill-validator.py --path docs/changes/2026-07-04-dated-change-root-convention/change.yaml --path docs/changes/2026-07-04-dated-change-root-convention/explain-change.md` passed.
