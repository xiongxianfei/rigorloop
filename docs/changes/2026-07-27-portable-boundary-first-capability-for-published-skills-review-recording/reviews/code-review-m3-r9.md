# Boundary-First M3 Code Review R9

Review ID: code-review-m3-r9
Stage: code-review
Round: 9
Reviewer: two independent Codex code reviewers
Target: commit 604306dd
Reviewed artifact: commit 604306dd
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-M3-CR24
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: PBF-M3-CR24
- Recording status: recorded
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Verify readiness: not claimed

## Packet integrity and independence

Pass. Both reviewers used the exact R9 packet and excluded the later invocation
commit. Every pinned artifact and the full `15b5f69f..604306dd` diff identity
matched. The required second review is satisfied.

## Failed remediation

### PBF-M3-CR24

Finding ID: PBF-M3-CR24
Reconciliation: failed-remediation
Severity: blocker
Location: `scripts/boundary_first_validation.py`, activation transition snapshot validation
Evidence: The validator binds the current baseline to the transition's first
parent and the current release fields to the transition snapshot, but does not
validate the transition snapshot's own baseline or grandfathered inventory. A
tagged invalid activation can therefore record a grandparent and incomplete
inventory, then pass after a later active commit repairs only the current
baseline and inventory.
Required outcome: Require the pending-to-active snapshot itself to record its
exact first parent and the exact eligible inventory derived from that parent;
also reject later divergence from that valid snapshot.
Safe resolution path: Compare the transition snapshot baseline with the
transition parent, derive eligible paths from that parent, compare both
transition and current inventories with the derived set, and add a regression
for invalid activation followed by later repair.
needs-decision rationale: none

## Confirmed behavior

First-parent integration ownership, activating-tag binding, release-field
immutability, current false-baseline rejection, raw Unicode path handling, and
regular-blob enforcement are correct. Focused validation passed 51 tests and
selector validation passed 134 tests.

## Recommendation

Apply the validator-and-test-only correction and run code-review M3 R10. M4
remains blocked.
