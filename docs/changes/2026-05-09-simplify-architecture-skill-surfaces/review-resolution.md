# Review Resolution: Simplify Architecture Skill Surfaces

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5
Review closeout: code-review-r6
Review closeout: code-review-r7
Review closeout: code-review-r8
Review closeout: code-review-r9

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `architecture-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`, `code-review-r6`, `code-review-r7`, `code-review-r8`, `code-review-r9`
- Findings resolved: 6
- Unresolved findings: 0
- Final result: proposal-review R1 requested revision for one material finding. The proposal wording was revised to require a new ADR amending or narrowing the existing architecture-package-method ADR, so the finding is closed. Proposal-review R2 approved the revised proposal with no material findings. Spec-review R1 approved the draft architecture-package-method amendment with no material findings. Architecture-review R1 approved the canonical architecture update and new ADR with no material findings. Plan-review R1 requested changes for PR-F1; the plan now requires per-milestone code-review handoff and review closeout for M1-M4 before final lifecycle closeout. Plan-review R2 approved the revised plan with no material findings. Code-review R1 requested changes for CR1-F1 and code-review R2 requested changes for CR2-F1. Both findings are resolved. Code-review R3 found no new material findings for the CR1/CR2 open-state alignment. Code-review R4 requested changes for CR4-F1, which is resolved. Code-review R5 requested changes for CR5-F1; the owner rejected that lifecycle review finding for this plan implementation review, so it is closed without the requested wording fix. Code-review R6 found no material findings and closed M1. Code-review R7 found no material findings and closed M2. Code-review R8 found no material findings and closed M3. Code-review R9 found no material findings and closed M4.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| PASS-F1 | accepted | resolved | Proposal now requires a new ADR amending or narrowing `ADR-20260428-architecture-package-method` and preserves the existing accepted ADR as decision history. |
| PR-F1 | accepted | resolved | Plan now adds per-implementation-milestone code-review handoff and review closeout before M1-M4 can close or final lifecycle closeout can begin. |
| CR1-F1 | accepted | resolved | M1 plan Outcome and Readiness now route to code-review rerun after CR1/CR2 review-resolution validation. |
| CR2-F1 | accepted | resolved | M1 review-resolution state is aligned across the plan, review-resolution, review-log, and change metadata before re-review. |
| CR4-F1 | accepted | resolved | Active plan Source Artifacts now says the test spec was revised for the 2026-05-09 simplification in M1. |
| CR5-F1 | rejected | resolved | Owner rejected the lifecycle review finding for this plan implementation review; no Outcome wording fix is required. |

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

### code-review-r1

#### CR1-F1 - Plan outcome still routes to plan-review after M1 handoff

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: code-review
Decision owner: implementation author
Chosen action: Aligned the active plan's Outcome and Readiness sections with the completed M1 review-resolution state and returned M1 to `review-requested`.
Rationale: The active plan body must stay current during implementation and review-resolution. Stale plan-review or code-review readiness wording can misroute the next implementer or reviewer while accepted findings remain open.
Validation target: Plan Current Handoff Summary, Outcome, Readiness, review-resolution, review-log, and `change.yaml.review` consistently state that CR1-F1 and CR2-F1 are resolved, no material findings remain open, targeted validation passed, and M1 is deliberately returned to `review-requested`.
Validation evidence: Review-resolution closeout validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/test-change-metadata-validator.py`; `git diff --check` passed; whitespace scan returned no matches; parsed `change.yaml.review` has `status: review_requested_after_cr1_cr2_resolution` and `unresolved_items: 0`.

### code-review-r2

#### CR2-F1 - M1 review-resolution state remains inconsistent across plan and change metadata

Finding ID: CR2-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: code-review
Decision owner: implementation author
Chosen action: Aligned the plan Readiness section, review-resolution, review-log, and `change.yaml.review` with the completed M1 review-resolution state.
Rationale: The active plan's Current Handoff Summary, Readiness section, and change metadata must expose the same current state so downstream work cannot mistake an open review-resolution loop for code-review readiness or approval.
Validation target: Active plan Readiness, Current Handoff Summary, review-resolution, review-log, and `change.yaml.review` consistently state that CR1-F1 and CR2-F1 are resolved, no material findings remain open, targeted validation passed, and M1 is returned to `review-requested`.
Validation evidence: Review-resolution closeout validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/test-change-metadata-validator.py`; `git diff --check` passed; whitespace scan returned no matches; parsed `change.yaml.review` has `status: review_requested_after_cr1_cr2_resolution` and `unresolved_items: 0`.

### code-review-r3

No material findings.

### code-review-r4

#### CR4-F1 - Plan Source Artifacts still says the test spec is not revised

Finding ID: CR4-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: code-review
Decision owner: implementation author
Chosen action: Updated the active plan Source Artifacts test-spec wording so it matches M1 progress, implementation result, and readiness.
Rationale: The active plan must not contain contradictory source-artifact readiness statements before M2 relies on the revised test spec.
Validation target: Active plan Source Artifacts, Progress, Outcome, Readiness, review-resolution, review-log, and `change.yaml.review` consistently state that CR4-F1 is resolved, no material findings remain open, targeted validation passed, and M1 returns to `review-requested`.
Validation evidence: CR4-F1 resolution validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/test-change-metadata-validator.py`; `git diff --check` passed; whitespace scan returned no matches; stale CR4 open-state scan returned no matches.

### code-review-r5

#### CR5-F1 - Plan outcome still says M1 is in review-resolution

Finding ID: CR5-F1
Disposition: rejected
Status: resolved
Owner: implementation author
Owning stage: code-review
Decision owner: maintainer
Chosen action: Reject the lifecycle review finding for this plan implementation review and return M1 to `review-requested`.
Rationale: Owner decision: "We don't accept the lifecycle review in this plan implent." The finding is therefore not accepted as a required implementation fix for M1.
Validation target: Active plan Current Handoff Summary, Readiness, review-resolution, review-log, and `change.yaml.review` consistently state that CR5-F1 is rejected, no material findings remain open, targeted validation passed, and M1 returns to `review-requested`.
Validation evidence: CR5-F1 rejection validation passed: `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`; `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`; `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-log.md --path docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md --path docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`; `python scripts/test-change-metadata-validator.py`; `git diff --check` passed; whitespace scan returned no matches; parsed `change.yaml.review` has `status: review_requested_after_cr5_rejection` and `unresolved_items: 0`.

### code-review-r6

No material findings.

### code-review-r7

No material findings.

### code-review-r8

No material findings.

### code-review-r9

No material findings.
