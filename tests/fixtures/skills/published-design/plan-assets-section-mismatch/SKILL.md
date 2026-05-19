---
name: plan
description: Use this fixture when validating plan skeleton section-set parity.
---

# Plan

## Resource map

- COPY `assets/plan-skeleton.md` when creating a new plan. Fill: Status. Sections: Status; Purpose / big picture. Do not emit unfilled placeholders.
- COPY `assets/milestone.md` when adding each milestone. Fill: milestone id. Do not emit unfilled placeholders.
- COPY `assets/current-handoff-summary.md` when updating handoff. Fill: current milestone. Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` when recording decisions. Fill: date. Do not emit unfilled placeholders.

## Expected output

- Compact output summary: Status, Purpose / big picture.

