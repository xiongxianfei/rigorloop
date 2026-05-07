# Learn Session: Plan Readiness vs Completion

## Frame

- Date: 2026-05-07
- Status: session-recorded-routed
- Trigger: contributor asked for best practices because the active plan is not over while readiness remains `verify`.
- Trigger type: explicit contributor observation.
- Scope: planned-initiative lifecycle wording, especially the difference between plan lifecycle state, milestone progress, and immediate next-stage readiness.
- Session path: `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`

## Evidence Reviewed

- `docs/learn/README.md`
- `docs/learn/topics/plan-lifecycle-closeout.md`
- `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`
- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `docs/plan.md`
- `docs/plans/2026-05-07-review-skill-material-finding-recording.md`
- Contributor correction: the correct handover process sends code to `verify` only after all planned implementation milestones are complete and code review has been conducted.

## Exclusions

- This session does not change plan lifecycle state.
- This session does not update `docs/workflows.md`, `specs/rigorloop-workflow.md`, skills, validators, or generated output.
- This session updates topic guidance only after the contributor correction confirmed the reusable handoff invariant.

## Prior Learnings Reviewed

- `docs/learn/topics/plan-lifecycle-closeout.md`
- `docs/learn/sessions/2026-05-05-recurring-plan-closeout-misses.md`

The prior topic already captures the closeout rule: implementation plans move to Done before PR review when implementation, review-resolution, verification, explain-change, and PR handoff are complete. If completion depends on a true downstream event, the plan stays Active and names that event.

## Observations

### O1: Active plan state and `Ready for verify` can be compatible

An active plan can still say `Ready for verify` only when the planned implementation milestones are complete, review-resolution is closed when triggered, and code review has been conducted. In that case, the remaining active work is downstream lifecycle gates, not unfinished implementation scope.

Evidence:

- `docs/plans/2026-05-07-review-skill-material-finding-recording.md` says the clean `code-review` rerun completed with no blocking or required-change findings.
- The same plan says M4 remains pending until `verify`, `explain-change`, and PR handoff complete.
- The same plan says readiness is `Ready for verify`.
- `docs/workflows.md` lists the full-feature execution path as `implement -> code-review -> review-resolution when triggered -> verify -> ci-maintenance when triggered -> explain-change -> pr`.
- Contributor correction: code should hand over to verification only after all planned implementation milestones are complete and code review has been conducted.

### O2: Readiness should describe the immediate next gate after prerequisites

`Readiness` is useful when it answers "what can happen next?" after prerequisite gates are satisfied. It should not be overloaded to mean "the plan is done", and it should not skip unfinished planned implementation milestones. Plan completion belongs in `Status`, `Progress`, `Outcome`, and the plan index.

Evidence:

- `docs/workflows.md` says `code-review` owns review findings, `verify` owns `branch-ready`, and `pr` owns PR readiness.
- `specs/rigorloop-workflow.md` defines `branch-ready` as a `verify` conclusion.
- `.codex/skills/verify/SKILL.md` treats plan completion as a verification dimension: milestones are complete or intentionally deferred.
- The active plan separates progress, outcome, and readiness sections.

### O3: The useful wording pattern is state plus next action

Best practice is to pair a next-stage readiness statement with explicit unfinished plan state:

```text
Status: Active.
Progress: implementation milestones are complete; code-review is complete.
Readiness: Ready for verify.
Remaining completion gates: verify, explain-change, PR handoff, then Done if no true downstream event remains.
```

This avoids two failure modes: marking a plan Done too early, or making "Ready for verify" sound like branch or PR readiness.

### O4: Verify is the right next gate only after planned implementation milestones and code-review are complete

The plan should not move to Done at this point because verification, explanation, and PR handoff are not complete. It also should not stay "ready for code-review" after a clean code-review rerun. The current best state is Active plus `Ready for verify` only because the implementation milestones have completed and code-review has been conducted.

Evidence:

- `docs/plans/2026-05-07-review-skill-material-finding-recording.md` records clean code-review evidence.
- `docs/workflows.md` says first-pass clean code-review in a workflow-managed full-feature run continues to `verify`.
- `docs/workflows.md` says `verify` blocks PR readiness on stale lifecycle state.

### O5: Plan structure should not make verify handoff circular

If a plan includes a final milestone that itself contains verification, explanation, and PR handoff, that milestone should be treated as a lifecycle-closeout milestone rather than an unfinished implementation milestone blocking verify. If the milestone still contains implementation tasks, `Ready for verify` is premature.

Evidence:

- `docs/plans/2026-05-07-review-skill-material-finding-recording.md` names M4 "Final Lifecycle Closeout and Verification" and lists `verify`, `explain-change`, and PR handoff as dependencies and remaining work.
- `docs/workflows.md` places `verify` after `code-review` and before `explain-change` and `pr`.
- Contributor correction requires all planned implementation milestones and code-review to finish before verify handoff.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | Topic context | Evidence in active plan, workflow summary, and contributor correction | Active plus `Ready for verify` is coherent only when remaining active work is downstream lifecycle gates. |
| O2 | durable-lesson | durable-lesson | Topic update | Contributor correction | The distinction is reusable and prevents readiness from skipping unfinished planned implementation work. |
| O3 | durable-lesson | durable-lesson | Topic update; candidate plan-template follow-up | Contributor correction | The wording pattern is reusable and makes state plus next action explicit. |
| O4 | observation | observation | Topic context | Evidence in active plan, workflow summary, and contributor correction | The next gate is `verify` only because implementation milestones and code-review are complete. |
| O5 | durable-lesson | durable-lesson | Topic update; candidate plan-template follow-up | Contributor correction plus current plan shape | Plans should distinguish implementation milestones from lifecycle-closeout gates to avoid circular verify handoff. |

Contributor confirmation status: confirmed for curated topic guidance by the explicit correction. Not confirmed for workflow, skill, validator, or template changes.

## Routing Results

- Session record: created.
- Topic update: updated `docs/learn/topics/plan-lifecycle-closeout.md`.
- Action-owning artifact update: not routed.
- Proposal, ADR, issue, or process follow-up: not created. A plan-template or workflow wording follow-up remains candidate only.

## Best Practices

1. Keep lifecycle state and next-stage readiness separate.
2. Use `Active` while any in-PR completion gate remains unfinished.
3. Use `Ready for <next stage>` to name the immediate next gate only after prerequisite milestones and gates are satisfied.
4. Hand over to `verify` only after planned implementation milestones are complete and code-review has been conducted.
5. After clean `code-review`, `Ready for verify` is correct only when no planned implementation milestone remains unfinished.
6. Do not mark a plan Done until implementation, review-resolution when triggered, verification, explain-change, and PR handoff are complete, unless a true downstream completion event keeps it Active.
7. Add a short remaining-gates line when ambiguity is likely.
8. Avoid broad readiness terms like `ready` or `PR-ready` until the owning stage has produced that result.
9. If a final milestone includes verification and PR handoff, label it as lifecycle closeout or split it so `verify` handoff is not blocked by a milestone that contains `verify`.

## No-Durable-Route Rationale

The current workflow already contains the core rule. This session routes a curated topic update after contributor confirmation, but does not change authoritative workflow, skill, validator, or template artifacts without a separate approved change.
