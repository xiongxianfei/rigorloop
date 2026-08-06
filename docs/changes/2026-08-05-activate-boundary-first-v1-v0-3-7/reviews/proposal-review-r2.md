# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: independent Codex proposal-review peer
Target: docs/proposals/2026-08-05-activate-boundary-first-v1-v0-3-7.md
Status: changes-requested
Material findings: BFA-PR2-001
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: workflow-owned after recording

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: BFA-PR2-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-log.md`
- Review resolution: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-resolution.md`
- Open blockers: BFA-PR2-001
- Immediate next stage: proposal revision

## Finding reconciliation

`BFA-PR1-001` is resolved narrowly. The proposal now separates explicit
pre-tag candidate validation from strict release-context tag validation and
keeps candidate evidence from claiming an active published release.

## Material Findings

## Finding BFA-PR2-001

Finding ID: BFA-PR2-001
Severity: major
Location: Recommended direction; rollout and rollback
Evidence: The proposal requires `main` and `v0.3.7` to resolve to the same reviewed activation commit. Formal review, resolution, explanation, and verification evidence may be committed after the pending-to-active transition, so the final reviewed branch head can differ from that transition commit. `scripts/boundary_first_validation.py` requires the tag to resolve to the transition commit, not final `HEAD`.
Required outcome: Define the atomic publication with two explicit identities and prove release verification at the tagged transition does not depend on later lifecycle-evidence commits.
Safe resolution path: Fast-forward `main` to the exact final reviewed branch head and create `v0.3.7` at the exact pending-to-active transition commit in that head's first-parent history. Retain unchanged-parent compare-and-swap, atomic two-ref push, strict tag validation, and regeneration/rereview on drift. Require tagged-tree release verification to be self-contained.
needs-decision rationale: none; separating the two identities is required by the existing activation contract and preserves the selected release direction.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The remaining pending capability is clear. |
| User value | pass | Stable activation delivers the requested default behavior. |
| Option diversity | pass | Deferral, repository-only activation, stable release, release candidate, and runtime activation are compared. |
| Decision rationale | pass | Stable patch activation remains justified. |
| Scope control | pass | Candidate validation is narrow and broad redesign remains excluded. |
| Architecture awareness | concern | Branch-head and tag-target identities are conflated. |
| Testability | concern | Tagged-tree self-containment is not yet an explicit proof obligation. |
| Risk honesty | concern | Drift is covered, but post-transition evidence commits are not. |
| Rollout realism | block | The proposed same-commit two-ref target conflicts with lifecycle evidence sequencing. |
| Readiness for spec | block | BFA-PR2-001 must be resolved and rereviewed. |

## Scope Preservation Review

- Scope-preservation result: pass. The revision preserves activation,
  publication, concise scope, rollback, and explicit external-action control.

## Recommended Proposal Edits

- Recommended edits: Distinguish final reviewed branch head from the activation
  transition tag target in recommended direction, rollout, risks, decision log,
  and proof strategy. Require the tagged transition tree to contain every input
  needed by strict release verification.

## Recommendation

- Recommendation: changes-requested. Resolve BFA-PR2-001 without reopening the
  stable-release or candidate-mode decisions, then run proposal-review R3.
