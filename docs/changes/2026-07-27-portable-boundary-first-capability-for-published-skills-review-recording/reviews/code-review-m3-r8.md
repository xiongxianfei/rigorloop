# Boundary-First M3 Code Review R8

Review ID: code-review-m3-r8
Stage: code-review
Round: 8
Reviewer: two independent Codex code reviewers
Target: commit 82592456
Reviewed artifact: commit 82592456
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-M3-CR23
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: PBF-M3-CR23
- Recording status: recorded
- Reviewed milestone: M3
- Milestone closeout: not-allowed
- Remaining implementation milestones: M3, M4
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Verify readiness: not claimed

## Packet integrity and independence

Pass. Both reviewers used the exact R8 packet. Every pinned artifact and the
full `15b5f69f..82592456` diff identity matched. The required second review is
satisfied.

## Finding

### PBF-M3-CR23

Finding ID: PBF-M3-CR23
Severity: blocker
Location: `scripts/boundary_first_validation.py`, activation transition and tag binding
Evidence: Transition discovery follows path-simplified history and skips
multi-parent commits, so a merge can bind to the activation branch parent
instead of the integration commit's first parent and omit target-branch
historical specs. Separately, tag validation proves only tag existence and
ordering: the activating tag can be moved to a pending commit, and a later
active-to-active edit can replace the recorded release fields without failing.
Required outcome: Treat the first pending-to-active edge on first-parent
integration history as the activation transition; bind the baseline to that
commit's first parent, bind the activating tag to that transition commit, and
require current release fields to equal the transition snapshot.
Safe resolution path: Inspect first-parent history without path
simplification, return transition commit/parent/manifest values, and add merge,
misdirected-tag, and active-to-active rewrite regressions.
needs-decision rationale: none

## Prior finding reconciliation

PBF-M3-CR18 through PBF-M3-CR22 are resolved for linear parent binding, release
adjacency, removal of adapter-manifest authority, raw Unicode tree paths, and
regular-blob modes. PBF-M3-CR23 covers the remaining merge and immutable
transition-identity seam.

## Recommendation

Apply one validator-and-test-only correction, then run code-review M3 R9. M4
remains blocked.
