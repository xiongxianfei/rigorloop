---
name: plan
description: Use this fixture when validating the assets-first plan pilot resource map.
---

# Plan

## Resource map

- COPY `assets/plan-skeleton.md` when creating a new plan.
  Fill: Status, Purpose, Milestones, Validation plan, Decision log, Current Handoff Summary.
  Sections: Status; Purpose / big picture; Milestones; Validation plan; Decision log; Current Handoff Summary.
  Do not emit unfilled placeholders.
- COPY `assets/milestone.md` when adding each milestone.
  Fill: milestone id, goal, requirements, tests, validation commands, rollback.
  Do not emit unfilled placeholders.
- COPY `assets/current-handoff-summary.md` when updating the active handoff section.
  Fill: current milestone, milestone state, review status, next stage, final closeout readiness.
  Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` when recording a planning decision.
  Fill: date, decision, rationale, alternatives rejected.
  Do not emit unfilled placeholders.

## Expected output

- Compact output summary: Status, Purpose / big picture, Milestones, Validation plan, Decision log, Current Handoff Summary.

