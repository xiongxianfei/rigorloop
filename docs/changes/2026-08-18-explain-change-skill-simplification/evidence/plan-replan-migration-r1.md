# Plan Replan Migration R1

Stage: workflow
Operation: governed replan migration
Result: complete
Date: 2026-08-18

## Basis

The canonical plan exists at `docs/plans/2026-08-18-explain-change-skill-simplification.md` and its prior authoring, review, initialization, and settlement evidence remains linked from the change record. The approved specification revision and accepted ADR-20260818 add implementation work that the historical M1-M3 baseline does not contain. The current change record has no plan artifact entry and no `workflow_state.planned_work`, so ordinary plan revision would encounter file-entry asymmetry.

## Migration

Workflow registers the exact existing canonical path as primary plan ID `plan` in `authoring` solely to permit `revise-primary-plan`. It does not infer milestone completion from the plan body, restore the historical `planned_work` projection, settle the plan, or route beyond plan authoring.

The revised plan must preserve M1-M3 as historical execution intent, add the newly required implementation milestone and closeout ordering, return the plan entry to `review-required`, receive fresh plan review, and initialize a new exact planned-work projection only through the approved plan initialization protocol.

This migration changes no proposal, specification, architecture, test specification, implementation, review verdict, verification result, branch state, or PR state.
