# Review Resolution: Activate Boundary-First v1 in RigorLoop v0.4.0

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: proposal-review-r4

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `proposal-review-r4`
- Findings resolved: 3
- Unresolved findings: 3
- Final result: Proposal revision is approved; specification R2 awaits review of the three remaining findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| BFA-PR1-001 | accepted | resolved | Added pre-tag candidate validation while preserving strict tag-context activation proof. |
| BFA-PR2-001 | accepted | resolved | Separated final reviewed branch head from the activation transition tag target and required tagged-tree self-containment. |
| BFA-SR1-001 | accepted | open | Separate remote publication base P from transition parent/grandfathering baseline B. |
| BFA-SR1-002 | accepted | resolved | Replaced patch v0.3.7 with contract-compliant minor v0.4.0 through proposal revision. |
| BFA-SR1-003 | accepted | open | Replace invalid unpublished transition histories with a fresh branch and rereview. |
| BFA-SR1-004 | accepted | open | Complete formal boundary ownership for identity, self-containment, strict composition, drift, and replacement. |

## Finding Details

### proposal-review-r1

#### BFA-PR1-001 - Pre-tag PR and strict activation validation are circular

Finding ID: BFA-PR1-001
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the proposal to define a candidate-validation bridge and strict release-owned tag validation.
Rationale: This preserves reviewed PR readiness, immutable tag authority, the existing rollback rule, and the user's stable-release objective without publishing before review.
Validation target: proposal-review-r2
Validation evidence: Proposal-review R2 confirms explicit candidate and strict tag-context phases resolve the circular gate.

### proposal-review-r2

#### BFA-PR2-001 - Reviewed branch head and activation tag target are conflated

Finding ID: BFA-PR2-001
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the proposal to publish `main` at the final reviewed head and `v0.3.7` at the earlier reviewed transition commit, with tagged-tree release self-containment.
Rationale: The activation tag contract binds the pending-to-active transition, while durable lifecycle evidence can validly follow that transition on the same first-parent branch.
Validation target: proposal-review-r3
Validation evidence: Proposal-review R3 confirms the two-identity first-parent model, tagged-tree self-containment, candidate/strict authority split, compare-and-swap, and atomic publication are coherent.

### spec-review-r1

#### BFA-SR1-001 - Publication base and grandfathering baseline are conflated

Finding ID: BFA-SR1-001
Disposition: accepted
Status: open
Owner: spec author
Owning stage: spec
Chosen action: Introduce publication base P and preserve B as T's first parent.
Rationale: Candidate preparation can occur between the remote fork point and activation transition.
Validation target: spec-review-r2
Validation evidence: pending

#### BFA-SR1-002 - Patch version violates release classification

Finding ID: BFA-SR1-002
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the release target to stable minor v0.4.0 and retain v0.3.6 rollback.
Rationale: REL-R9 and REL-R10 classify new backward-compatible public skill behavior as a minor release.
Validation target: proposal-review-r4 then spec-review-r2
Validation evidence: Proposal-review R4 approves stable minor v0.4.0 under REL-R10 and confirms v0.3.6 rollback plus prior sequencing remain intact.

#### BFA-SR1-003 - Invalid transition recovery lacks a legal history

Finding ID: BFA-SR1-003
Disposition: accepted
Status: open
Owner: spec author
Owning stage: spec
Chosen action: Define replacement-branch regeneration from the authorized publication base.
Rationale: Appending another transition violates uniqueness and force-pushing would rewrite reviewed history.
Validation target: spec-review-r2
Validation evidence: pending

#### BFA-SR1-004 - Formal boundary ownership is incomplete

Finding ID: BFA-SR1-004
Disposition: accepted
Status: open
Owner: spec author
Owning stage: spec
Chosen action: Extend exact boundary and interaction ownership for the missing requirements and hazards.
Rationale: Downstream proof must consume requirement-owned semantic rows rather than infer them.
Validation target: spec-review-r2
Validation evidence: pending

## Clean review receipts

### proposal-review-r3

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-PR1-001 and BFA-PR2-001 closure
Evidence: reviews/proposal-review-r3.md

### proposal-review-r4

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-SR1-002 closure
Evidence: reviews/proposal-review-r4.md

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [ ] Validation evidence is recorded.
- [x] Closeout status is correct.
