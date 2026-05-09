# Learn Session: Implement Review-Fix Handoff Drift

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking what is wrong with the implement stage after another lifecycle-readiness problem.
- Trigger type: explicit maintainer request / contributor observation / repeated implementation handoff drift.
- Scope:
  - `skills/implement/SKILL.md` and `.codex/skills/implement/SKILL.md`
  - `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r1.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/code-review-r2.md`
  - `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`
- Evidence in scope:
  - implement skill wording that accepted review findings return to the same milestone and must update plan progress, validation notes, and milestone state before handoff;
  - code-review R1 finding `CR1-F1`, which required the active plan to stop routing to plan-review and return M1 to `review-requested` after the fix;
  - code-review R2 finding `CR2-F1`, which found that the partial correction still left plan Readiness and change metadata out of sync with open review-resolution;
  - the active plan state where Current Handoff Summary says M1 is in review-resolution while Readiness still says `Next stage: code-review M1`.
- Explicit exclusions:
  - this session does not fix `CR1-F1` or `CR2-F1`;
  - this session does not update implement skill behavior, workflow specs, plan templates, validators, or topic files;
  - this session does not claim review-resolution closeout, branch readiness, verification readiness, or PR readiness.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `docs/learn/sessions/2026-05-09-plan-readiness-state-drift.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
- Session record path: `docs/learn/sessions/2026-05-09-implement-review-fix-handoff-drift.md`

## Observe

### O1 - The implement-stage miss is incomplete review-fix closeout, not only stale wording

Evidence:

- Code-review R1 required replacing stale plan-review wording and then rerunning M1 plan/change metadata validation before returning M1 to `review-requested`.
- The active plan's Current Handoff Summary was updated to `resolution-needed`, but its Readiness section still says `Next stage: code-review M1` and `Implementation readiness: M1 is implemented and ready for code-review`.
- Code-review R2 found the same state drift and also identified stale change metadata review status.

Observation:

The implementation response to `CR1-F1` handled only part of the accepted finding. It updated some plan text and review bookkeeping, but did not complete the full review-fix handoff: all affected state surfaces synchronized, finding disposition updated, targeted validation rerun, and milestone returned to `review-requested` only when the fix was actually complete.

### O2 - The implement skill already contains the needed invariant

Evidence:

- The implement skill says accepted review findings return to the same milestone.
- It says after fixes and targeted validation evidence are complete, that same milestone returns to `review-requested` before rerun `code-review`.
- It says implementation owns keeping the active plan body current during execution.
- It says a slice must meet the `first-pass acceptable result` bar and must not leave a known in-scope defect for later review.

Observation:

The contract is present, but execution did not apply it to review-resolution fixes. The fix was approached as patching a sentence, not as implementing an accepted review finding with a same-slice completeness set.

### O3 - Review fixes need their own same-slice completeness set

Evidence:

- `CR1-F1` named the active plan as the primary affected surface, but its safe resolution also required rerunning validation and returning M1 to `review-requested`.
- `CR2-F1` found adjacent surfaces that should have been part of the same fix: plan Readiness, change metadata review status, review-resolution state, and review-log/open findings.
- The learn session `2026-05-09-plan-readiness-state-drift.md` identified the exact stale Readiness line before the R2 review, but the implement-stage state was still not reconciled.

Observation:

For accepted review findings, the same-slice completeness set is the finding's required outcome plus every touched state surface needed to make that outcome truthful. If the fix changes review state, that set includes Current Handoff Summary, Readiness, milestone state, progress, review-resolution, review-log, change metadata, and validation evidence.

### O4 - The immediate implement-stage stop condition should have fired

Evidence:

- The active plan still contains contradictory next-stage state.
- Review-resolution still records open findings.
- The milestone should not be handed to rerun code-review while accepted findings remain only partially resolved.

Observation:

The correct implement-stage behavior is to stop before handoff until the accepted findings are fully resolved or explicitly dispositioned, targeted validation passes, and the plan state is changed back to `review-requested`. A partial review-resolution patch is not implementation handoff evidence.

## What's Wrong

The implement stage failed to treat accepted review findings as a same-milestone implementation loop.

It should have read `CR1-F1` as an implementation task with a clear completion contract: fix every state surface affected by the finding, update review-resolution, update change metadata, rerun selected validation, then return M1 to `review-requested` for re-review. Instead, it performed a local correction and left stale sibling readiness and metadata behind.

## Best Practices

1. When implementing a review finding, start from the finding's required outcome and safe resolution, not from the most visible sentence.
2. Build a review-fix completeness set before editing.
3. Include all state surfaces touched by the finding: plan Current Handoff Summary, milestone state, Progress, Outcome, Readiness, review-log, review-resolution, change metadata, and validation notes.
4. Keep the milestone `resolution-needed` while any accepted finding is still open or only partially fixed.
5. Return the milestone to `review-requested` only after fixes are complete, targeted validation passes, and review-resolution records validation evidence.
6. Search for stale pre-fix state terms before re-review handoff.
7. Do not use a learn session or code-review record as a substitute for implement-stage review-resolution work.
8. Treat a later review finding on adjacent stale state as a preventable first-pass miss when it was named by the prior finding or by an existing learn observation.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Active review-resolution context | Code-review R1/R2 evidence | This explains the immediate active-plan failure. |
| O2 | observation | observation | None | Implement skill text | The needed rule already exists in the skill contract. |
| O3 | process-follow-up | pending confirmation | Possible implement skill checklist or validator follow-up | Not yet confirmed | The pattern is reusable, but any behavior change belongs in action-owning artifacts. |
| O4 | process-follow-up | pending confirmation | Possible review-resolution/implement handoff checklist | Not yet confirmed | The implement stop condition needs stronger execution support, but routing needs confirmation. |

Contributor confirmation status: unavailable for derivative updates. This session records candidate classifications and stops before routing.

## Route

No routing performed.

Candidate follow-up: add a concrete review-fix completeness checklist to the action-owning implement/review-resolution guidance, or add a validation check that compares open review-resolution findings against plan Readiness and `change.yaml.review`.

## No Durable Route Rationale

The evidence supports a process gap in how implement handles accepted review findings, but the corrective behavior would affect implementation, review-resolution, plan template, or validation contracts. This session captures the diagnosis and best practices without making new policy authoritative.
