# Proposal Revision Evidence R5: Proposal-Review Skill Simplification

Stage: proposal
Date: 2026-08-11
Artifact: `docs/proposals/2026-08-11-proposal-review-skill-simplification.md`
Trigger: `docs/changes/2026-08-11-proposal-review-skill-simplification/evidence/workflow-upstream-recording-contract-correction.md`

## Revision scope

Specification routing exposed a conflict between the accepted proposal's prohibition on new advisory recording roots and the approved formal-review-recording contract's generated fallback root. The proposal lists recording-obligation changes as a non-goal, so this revision follows the higher-priority existing contract.

## Correction

- Clean non-formal explicit durable requests may use an allowed standalone path without formal lifecycle artifacts.
- Material, non-approval, and formal recording use the governing change-ID selection order.
- When no existing identity is available, an unambiguous generated `YYYY-MM-DD-<topic>-review-recording` root carries the minimal required review evidence.
- A generated recording-only root never settles the reviewed proposal, activates workflow, or grants continuation authority.
- Ambiguous, colliding, or unwritable identities produce blocked recording with the complete finding and smallest corrective action.
- Static scenarios, acceptance criteria, risks, and the decision log now reflect the existing contract.

## Authoring result

The correction removes the upstream conflict without changing the selected two-reference design, operational modes, result groups, target-runtime exclusion, or architecture expectation. The substantively revised proposal is ready for formal rereview and does not claim acceptance until that review settles it.
