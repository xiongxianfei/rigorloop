# Plan Replan Migration R2

Stage: workflow
Operation: governed replan migration
Result: prepared-for-plan-review
Date: 2026-08-20

## Basis

The approved specification revision removes strict count reduction as an acceptance gate. The initialized plan's M3 completion criteria and required evidence still require that obsolete outcome, so ordinary plan revision cannot safely coexist with its prior `planned_work.initialization_basis`.

## Preserved live-state snapshot

- Prior initialization review: `plan-review-r1`
- Current milestone: `M2`
- `M1`: `closed`
- `M2`: `resolution-needed`
- `M3`: `planned`
- Remaining implementation milestones: `M2`, `M3`
- Latest review: `code-review-m2-r2`, `changes-requested`
- Final closeout: `not-ready` because lifecycle gates remain open

## Migration

Workflow temporarily removes the prior initialized `planned_work` projection so the exact revised plan can return to `review-required`. It preserves the live-state snapshot above and does not infer progress from plan prose.

After clean `plan-review-r2`, the approved initialization protocol will create a current projection bound to that review. Workflow will then reconcile the preserved snapshot: M1 remains closed, M2 remains the current resolution-needed milestone until its correction and rereview close it, and M3 remains planned. No implementation completion, review approval, or downstream readiness is invented by this migration.
