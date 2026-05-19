# Published Skill Design Implement And Code-Review Behavior Parity

Change: `2026-05-19-published-skill-design-implement-code-review`

## Representative Artifacts

| Artifact class | Representative surface | Why it matters |
|---|---|---|
| Active plan | `docs/plans/2026-05-19-published-skill-design-implement-code-review.md` | Exercises planned milestone handoff, plan progress updates, validation notes, and state-sync expectations. |
| Implementation handoff | M1/M2/M3 milestone sections in the active plan | Exercises `implement` milestone state, validation evidence, and `code-review` handoff boundaries. |
| Clean code-review receipt | `docs/changes/2026-05-19-published-skill-design-spec-family/reviews/code-review-m3-r1.md` | Representative clean review shape with checklist, no-finding rationale, and next-stage routing. |
| Material finding review | `docs/changes/2026-05-19-published-skill-design-spec-family/reviews/code-review-m2-r1.md` | Representative material finding with evidence, required outcome, safe resolution, and review-resolution routing. |
| Review resolution | `docs/changes/2026-05-19-published-skill-design-spec-family/review-resolution.md` | Representative accepted finding disposition and closeout behavior. |
| Review log | `docs/changes/2026-05-19-published-skill-design-spec-family/review-log.md` | Representative clean receipt and material finding ledger behavior. |

## Parity Checks

M3 must confirm the rewrite preserves these outcomes:

| Area | Required parity result | M3 result |
|---|---|---|
| Implementation handoff state | `implement` still moves implemented milestones to `review-requested`, not `closed`. | Pending M3. |
| Validation obligations | `implement` still names and records targeted validation before handoff. | Pending M3. |
| Plan update ownership | `implement` still owns active-plan progress, decisions, discoveries, and validation notes during execution. | Pending M3. |
| First-pass completeness | `implement` still requires same-slice completeness before code-review handoff. | Pending M3. |
| Review status taxonomy | `code-review` still uses exactly one first-pass status from the approved set. | Pending M3. |
| Finding format | `code-review` still requires evidence, required outcome, and safe resolution or `needs-decision` for material findings. | Pending M3. |
| Recording obligations | `code-review` still records clean formal reviews and material findings, and does not create empty review-resolution for clean reviews. | Pending M3. |
| Stop conditions | Both skills still stop on missing or contradictory governing artifacts, failing validation, or unresolved owner decisions. | Pending M3. |
| Claim boundaries | Neither skill claims verification, CI, branch-ready, PR-ready, or downstream completion without owning evidence. | Pending M3. |
| Milestone routing | `code-review` still routes clean non-final reviews to the next implementation milestone and final clean reviews to final closeout only when all implementation milestones are closed. | Pending M3. |

## M1 No-Change Evidence

M1 creates parity scope only. No behavior-significant skill wording changes are
made in M1.
