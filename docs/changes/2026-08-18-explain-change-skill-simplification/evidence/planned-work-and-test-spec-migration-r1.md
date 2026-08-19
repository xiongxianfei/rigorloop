# Planned-Work and Test-Spec Migration R1

Stage: workflow
Result: complete
Date: 2026-08-18

## Planned-work reconciliation

The activated R2 plan baseline initialized M1-M4 without inferring prior execution. Workflow reconciles M1-M3 to `closed` only from their existing milestone implementation evidence and clean code-review records:

- M1: `reviews/code-review-m1-r1.md`
- M2: `reviews/code-review-m2-r2.md`, after resolution of EXCSIM-CR1
- M3: `reviews/code-review-m3-r1.md`

M4 remains `planned` and becomes the sole remaining implementation milestone. The earlier blocked final review is not reused as M4 review evidence.

## Test-spec registration

The canonical test specification exists and its prior R2 review remains historical evidence, but the approved spec revision, ADR-20260818, and plan M4 make its evidence-tail proof stale. The current change record has no test-spec artifact entry. Workflow registers the exact existing path as primary `test-spec` in `authoring` solely to permit governed revision; it does not infer approval, mutate the test specification, or settle its review.

This migration routes to test-spec authoring and claims no implementation, verification, branch, or PR readiness.
