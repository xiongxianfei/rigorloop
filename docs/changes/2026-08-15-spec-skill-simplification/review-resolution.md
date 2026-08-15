# Review Resolution: Spec Skill Simplification

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 2
- Current result: proposal revision required before specification

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `SPSIM-PR1` | accepted | open | Select and fully define a stale-authoring recovery contract owned for `spec`. |
| `SPSIM-PR2` | accepted | open | Define the skeleton and formal boundary-record composition interface. |

## Finding details

### proposal-review-r1

#### SPSIM-PR1

Finding ID: SPSIM-PR1
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Replace the unowned reset-authorization assumption with an executable recovery contract.
Chosen action: Prefer a spec-owned same-entry restart unless an exact approved workflow authorization contract is identified and amended in scope.
Rationale: Proposal-specific reset authorization and test-spec-specific same-entry restart do not automatically grant a recovery mechanism to `spec`.
Required outcome: Define exact owner, authority, operation, identity, partial-content treatment, permitted writes, resulting state, and architecture effect.
Safe resolution path: Adopt the same-entry restart recommended by `proposal-review-r1` or explicitly broaden the governing workflow contract with architecture reassessment.
Validation target: revised recovery, ownership, architecture, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.

#### SPSIM-PR2

Finding ID: SPSIM-PR2
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the interface between ordinary skeleton structure and the formal boundary-record block.
Chosen action: Add one conditional insertion point while preserving the feature-authoring reference as the block owner.
Rationale: Initial resource loading does not determine output applicability or the block's location in the ordinary spec structure.
Required outcome: Define exact insertion location, applicability, omission, unresolved-data behavior, and non-duplication.
Safe resolution path: Adopt the conditional insertion point and applicability matrix recommended by `proposal-review-r1`.
Validation target: revised structural ownership, behavior, missing-resource rules, scenarios, risks, and acceptance criteria plus independent rereview.
Validation evidence: pending proposal revision.
