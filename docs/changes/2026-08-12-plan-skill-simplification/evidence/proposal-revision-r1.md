# Proposal Revision R1: Plan Skill Simplification

Stage: proposal
Date: 2026-08-13
Artifact: `docs/proposals/2026-08-12-plan-skill-simplification.md`
Responds to: `proposal-review-r1`

## Changes made

- Resolved `PLSIM-PR1` by separating manual and workflow-managed execution authority from loaded-resource profiles, restricting `plan` to its existing authoring writes, and leaving review evidence, automation receipts, routing, and continuation with `plan-review` and `workflow`.
- Resolved `PLSIM-PR2` by defining stable milestone completion criteria, required evidence, review handoff, and milestone-kind behavior while keeping actual state and progress exclusively in `change.yaml` and stage-owned evidence.
- Resolved `PLSIM-PR3` by defining exact procedural profile assemblies that exclude assets, plus separate per-asset, representative structural assembly, decision-row delta, and total-package measurements.

## Preservation result

The selected package remains one compact `SKILL.md`, one governed reference, the existing boundary reference, and exactly three structural assets. The revision adds no runtime, state model, lifecycle owner, reference, asset, or permanent validator. It preserves the one-time `planned_work` initialization exception, boundary activation ownership, plan-review handoff, and target-agent-runtime exclusion.

## Review request

The proposal is returned to `review-required` for an independent second proposal-review. This authoring revision does not claim that the findings are independently verified or that the proposal is approved.
