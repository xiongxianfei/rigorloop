# Review Resolution: Simplify Architecture Skill Surfaces

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `architecture-review-r1`, `plan-review-r1`, `plan-review-r2`
- Findings resolved: 2
- Unresolved findings: 0
- Final result: proposal-review R1 requested revision for one material finding. The proposal wording was revised to require a new ADR amending or narrowing the existing architecture-package-method ADR, so the finding is closed. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 approved the draft architecture-package-method amendment with no material findings. Architecture-review R1 approved the canonical architecture update and new ADR with no material findings. Plan-review R1 requested changes for PR-F1; the plan now requires per-milestone code-review handoff and review closeout for M1-M4 before final lifecycle closeout. Plan-review R2 approved the revised plan with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| PASS-F1 | accepted | resolved | Proposal now requires a new ADR amending or narrowing `ADR-20260428-architecture-package-method` and preserves the existing accepted ADR as decision history. |
| PR-F1 | accepted | resolved | Plan now adds per-implementation-milestone code-review handoff and review closeout before M1-M4 can close or final lifecycle closeout can begin. |

## Resolution Entries

### proposal-review-r1

#### PASS-F1 - ADR amendment path is ambiguous

Finding ID: PASS-F1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Chosen action: Revised the proposal's architecture impact, decision log, and next artifacts to require a new ADR amending or narrowing `ADR-20260428-architecture-package-method`, while preserving the existing accepted ADR as history and allowing only an explicit lifecycle cross-reference if the later spec or ADR contract requires it.
Rationale: Accepted ADRs should remain decision history. This change narrows one decision inside the architecture-package method, not the whole C4 plus arc42 plus ADR method.
Validation target: Proposal wording explicitly says the later architecture work creates a new ADR that amends/narrows the existing architecture-package-method ADR and does not fully supersede the whole C4 plus arc42 plus ADR method.
Validation evidence: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-simplify-architecture-skill-surfaces` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/proposal-review-r1.md` passed; `git diff --check -- docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces` passed.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

#### PR-F1 - Implementation milestones bypass per-milestone code-review

Finding ID: PR-F1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: plan author
Chosen action: Revised the plan so M1, M2, M3, and M4 each require targeted validation, handoff to milestone-specific code-review, completed code-review, material finding resolution or explicit disposition, and milestone state update before the next implementation milestone starts. M5 now starts final lifecycle closeout only after M1-M4 review loops are complete.
Rationale: Milestone-based implementation work needs reviewable slices. The current plan defers code-review until after M1-M4 are closed, which makes the milestone loop less reviewable than the repository workflow requires.
Validation target: Revised plan requires code-review handoff and review closeout for M1, M2, M3, and M4 before starting the next implementation milestone or entering M5 lifecycle closeout.
Validation evidence: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml` passed; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-09-simplify-architecture-skill-surfaces` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md --path docs/plan.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/plan-review-r1.md` passed with existing warning in `docs/plan.md` line 17; `git diff --check -- docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md docs/changes/2026-05-09-simplify-architecture-skill-surfaces docs/plan.md` passed.

### plan-review-r2

No material findings.
