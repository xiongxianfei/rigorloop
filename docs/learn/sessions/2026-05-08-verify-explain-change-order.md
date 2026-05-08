# Learn Session: Verify and Explain-Change Ordering

## Frame

- Date: 2026-05-08
- Status: session-recorded-follow-up-recommended
- Trigger: contributor asked for best practice after `verify` blocked because `docs/changes/2026-05-08-skill-contract-optimization/explain-change.md` was missing, while the documented full-feature sequence places `explain-change` after `verify`.
- Trigger type: explicit contributor observation.
- Scope: ordering and responsibility boundaries between validation evidence, final `verify`, baseline change-local reasoning, `explain-change`, and PR handoff.
- Session path: `docs/learn/sessions/2026-05-08-verify-explain-change-order.md`

## Evidence Reviewed

- `docs/workflows.md`
- `specs/rigorloop-workflow.md`
- `specs/docs-changes-usage-policy.md`
- `skills/verify/SKILL.md`
- `skills/explain-change/SKILL.md`
- `docs/plans/2026-05-08-skill-contract-optimization.md`
- `docs/changes/2026-05-08-skill-contract-optimization/explain-change.md`
- `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
- `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
- `docs/learn/topics/plan-lifecycle-closeout.md`

## Exclusions

- This session does not change workflow order, workflow specs, docs, skills, validators, generated output, or PR readiness rules.
- This session does not update a curated topic file because the fix changes authoritative workflow behavior and should be handled by an action-owning artifact.
- This session does not claim hosted CI, branch readiness, PR readiness, or plan Done state.

## Prior Learnings Reviewed

- `docs/learn/sessions/2026-05-07-plan-readiness-vs-completion.md`
- `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
- `docs/learn/topics/plan-lifecycle-closeout.md`

The prior learning already separates readiness from completion and lifecycle-closeout milestones from implementation milestones. It does not settle the narrower ordering conflict between the final `verify` gate and the downstream `explain-change` artifact.

## Observations

### O1: Current guidance creates a circular dependency

The public workflow summary and stage-autoprogression guidance place `explain-change` after `verify`, but `verify` requires the baseline change-local pack for ordinary non-trivial work. That baseline pack defaults to `change.yaml` plus `explain-change.md`.

Evidence:

- `docs/workflows.md` lists the full-feature sequence as `... verify -> ci-maintenance when triggered -> explain-change -> pr`.
- `skills/verify/SKILL.md` says to confirm the baseline change-local pack exists and treat a missing pack as a blocker.
- `specs/docs-changes-usage-policy.md` requires durable Markdown reasoning for every non-trivial change and defaults that artifact to `docs/changes/<change-id>/explain-change.md`.
- The skill-contract optimization `verify` pass selected CI and review closeout succeeded, then blocked only because `explain-change.md` did not exist yet.

### O2: Validation evidence and final verify are different things

The workflow needs validation evidence before a useful explanation can be written, but the final branch-ready `verify` gate also needs to inspect the explanation artifact after it exists. Treating both as one stage creates ordering pressure.

Evidence:

- `skills/explain-change/SKILL.md` requires verification evidence in the explanation.
- `skills/verify/SKILL.md` owns `branch-ready` and checks touched, referenced, generated, and authoritative artifacts.
- `docs/workflows.md` says final PR text must not add new authoritative references after verify without rerunning verify.

### O3: The best-practice fix is to remove the circular dependency explicitly

Best practice is to choose one explicit lifecycle model instead of letting agents infer it:

1. Preferred model: separate validation evidence collection from the final `verify` gate.
2. Alternate model: keep `verify -> explain-change`, but define the first `verify` result as "ready for explain-change", not final `branch-ready`, and require a second final verify before PR.

The preferred model is less stateful:

```text
implement
-> code-review
-> review-resolution when triggered
-> validation evidence collection
-> explain-change
-> final verify
-> pr
```

In that model, validation commands can run before `explain-change`, but final `verify` happens after the durable explanation exists and is indexed.

### O4: If the current order is retained, the verify skill needs two readiness states

If the repository keeps `verify -> explain-change -> pr`, then `verify` should not block merely because `explain-change.md` is the next downstream artifact. Instead, it should return a narrower result such as "validation passed; ready for explain-change; not branch-ready for PR". After `explain-change`, a final verify rerun would be required before PR handoff.

This preserves the current sequence but makes the workflow more stateful and easier to misuse.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | artifact-update | direction | Candidate proposal/spec update | Contributor observation and current workflow evidence | The conflict spans workflow docs, docs-changes policy, and verify/explain-change skills, so learn should not patch one surface directly. |
| O2 | observation | observation | Context for candidate proposal | Evidence in verify and explain-change skills | The validation-vs-final-verify distinction explains the blocker but does not by itself change policy. |
| O3 | direction | direction | Candidate proposal/spec update | Contributor asked for best practice | The preferred model would change workflow semantics and needs an authoritative artifact. |
| O4 | direction | direction | Candidate proposal/spec update | Contributor asked for best practice | The alternate model is viable but creates two verify states and should be decided in proposal/spec work. |

Contributor confirmation status: confirmed for recording the session and answering the best-practice question. Not confirmed for editing authoritative workflow specs, skills, docs, validators, or generated output.

## Routing Results

- Session record: created.
- Topic update: not routed.
- Action-owning artifact update: not routed.
- Recommended follow-up: create a proposal to decide the lifecycle model and then update `specs/rigorloop-workflow.md`, `docs/workflows.md`, `skills/verify/SKILL.md`, `skills/explain-change/SKILL.md`, and related tests/generated outputs as needed.

## Best Practice

Do not make a final gate require an artifact that is defined as downstream of that gate.

For RigorLoop, the cleaner fix is to treat validation command execution and final `verify` as separate concepts:

- validation evidence can be collected during implementation, code-review closeout, or lifecycle closeout before `explain-change`;
- `explain-change` writes the durable rationale and cites the available validation evidence;
- final `verify` runs after `explain-change` exists and checks that artifacts, generated output, review closeout, validation evidence, plan state, and explanation agree;
- `pr` runs only after that final verify passes.

This avoids the circular "verify requires explain-change, but explain-change comes after verify" failure while keeping `verify` as the real branch-ready gate.

If maintainers prefer not to move final `verify`, the fallback is to rename or split the first result:

```text
verify before explain-change = ready for explain-change, not branch-ready
verify after explain-change = branch-ready for PR
```

That fallback works, but it is more stateful and should be specified carefully because the repository is actively trying to make skills smaller and less stateful.

## No-Durable-Route Rationale

This session records a concrete workflow-design issue and recommends a follow-up, but it does not update curated topic guidance or authoritative workflow policy. The fix changes workflow semantics and belongs in a proposal/spec/skill update, not directly in a learn topic.
