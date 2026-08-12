# Review Resolution: Plan Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PLSIM-PR1` | needs-decision | open | Proposal author must restrict governed procedure to plan-owned writes and handoff. |
| `PLSIM-PR2` | needs-decision | open | Proposal author must define stable milestone completion structure after mutable-state removal. |
| `PLSIM-PR3` | needs-decision | open | Proposal author must define deterministic procedural and structural measurements. |

## Finding details

### proposal-review-r1

#### PLSIM-PR1

Finding ID: PLSIM-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close the execution-authority and cross-stage ownership model.
Chosen action: pending proposal revision
Rationale: The package shape remains viable, but plan must not own automation receipts or plan-review completion behavior.
Required outcome: Restrict the governed reference to plan-owned authoring and normal review-required handoff.
Safe resolution path: Adopt the authority correction in `proposal-review-r1` and validate it with static manual and automated scenarios.
Validation target: revised reference ownership, execution-authority, handoff, and acceptance sections plus independent proposal rereview.
Validation evidence: pending

#### PLSIM-PR2

Finding ID: PLSIM-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define stable milestone completion structure without mutable progress.
Chosen action: pending proposal revision
Rationale: Mutable state must leave the plan, but stable completion, proof, and review handoff criteria must remain explicit.
Required outcome: Close the replacement milestone field groups and lifecycle-closeout distinction.
Safe resolution path: Adopt the stable completion group recommended by `proposal-review-r1` and reconcile it with the existing asset contract.
Validation target: revised asset ownership, migration, parity, and static fixture sections plus independent proposal rereview.
Validation evidence: pending

#### PLSIM-PR3

Finding ID: PLSIM-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Define deterministic procedural profile and asset measurement assemblies.
Chosen action: pending proposal revision
Rationale: Variable asset applicability and milestone counts currently make the primary reduction gate non-repeatable.
Required outcome: Separate reference-loaded context from output-structure resource measurements.
Safe resolution path: Adopt the measurement convention recommended by `proposal-review-r1`.
Validation target: revised profile, measurement, acceptance, and evidence sections plus independent proposal rereview.
Validation evidence: pending
