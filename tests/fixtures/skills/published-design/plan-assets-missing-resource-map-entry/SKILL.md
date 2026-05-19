---
name: plan
description: Use this fixture for the plan asset pilot missing resource-map entry check.
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

## Expected output

- Compact output summary: Status, Purpose / big picture, Milestones, Validation plan, Decision log, Current Handoff Summary.
