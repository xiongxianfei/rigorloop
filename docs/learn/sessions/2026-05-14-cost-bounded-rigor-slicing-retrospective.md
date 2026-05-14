# Learn Session: Cost-Bounded Rigor Slicing Retrospective

## Frame

- Trigger: maintainer invoked `$learn` and asked whether excessive token usage has been resolved, why the cost-bounded-rigor effort was split into five plans, and what best practice should be.
- Trigger type: explicit maintainer retrospective / contributor observation.
- Scope: accepted cost-bounded-rigor proposal, M1-M5 cost-bounded-rigor plan evidence, prior token-cost learn records, and current PR #58 state.
- Session path: `docs/learn/sessions/2026-05-14-cost-bounded-rigor-slicing-retrospective.md`
- Evidence in scope:
  - `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `docs/plan.md`
  - `docs/learn/topics/token-cost-measurement.md`
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
  - `docs/learn/sessions/2026-05-11-dynamic-token-cost-root-cause.md`
  - `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-slicing-retrospective.md`
- Explicit exclusions:
  - This session does not claim exact token savings from M1-M5 because no comparable end-to-end dynamic lifecycle benchmark was required or run for the full five-plan effort.
  - This session does not mark PR #58 merged; `gh pr view 58` showed PR #58 open with passing hosted CI at the time of this session.
  - This session does not create new workflow policy, hard token thresholds, or a new required planning rule.
  - This session does not update topic files without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/topics/token-cost-measurement.md`
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
  - `docs/learn/sessions/2026-05-11-dynamic-token-cost-root-cause.md`
  - `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`

## Observe

### O1: Excessive token usage is mitigated, not proven fully resolved

The M1-M5 cost-bounded-rigor effort implemented several controls that should reduce workflow amplification: scope-budget guidance, bounded-evidence guidance, selected skill reminders, validation-budget guidance, conditional lifecycle token-cost summaries, and high-cost skill follow-through. That is real mitigation.

The evidence does not prove that excessive token usage is fully resolved as a measured end state. The accepted proposal made measurement diagnostic and warning-only, and it explicitly did not require before/after dynamic benchmark comparison for proposal or evidence wording changes. M2 recorded static token measurement as diagnostic evidence and did not run a dynamic benchmark. M5 made no skill or validator edits and did not run static token measurement or dynamic benchmarks because no runtime behavior changed.

Evidence:

- The proposal says measurement is diagnostic and warning-only, with no hard token target.
- The proposal says the plan or test spec decides whether dynamic benchmark comparison is required.
- M1 delivered scope-budget and bounded-evidence guidance, then left later slices deferred.
- M2 recorded diagnostic static skill token measurement only: 23 skills, total estimated tokens 57,587, and `workflow/SKILL.md` estimated at 5,296 tokens.
- M5 audit found no concrete skill or proof gap and did not run dynamic benchmarks because it made no runtime behavior change.

### O2: The five-plan split was intentional scope control

The five plans were not accidental fragmentation. The accepted proposal first narrowed the first implementation slice to proposal/proposal-review scope-budget guidance and concise workflow evidence wording, then named M2-M5 as later slices. That split prevented validation-budget behavior, lifecycle reporting, and progressive-loading follow-through from being pulled into the first PR.

Evidence:

- The proposal's first implementation slice excludes selector or validation-budget behavior changes, lifecycle token-cost summary artifacts, dynamic benchmark changes, broad progressive-loading implementation, release validation changes, adapter packaging changes, and rewriting every public skill.
- The proposal's rollout lists M1 through M5 as reviewable slices.
- M2's plan decision log says to plan M2 separately from M3-M5 because the proposal intentionally split selected skill reminders, validation-budget guidance, lifecycle token-cost summaries, and progressive-loading follow-through into reviewable slices.
- M3 completed without changing selector behavior, release behavior, adapter packaging, lifecycle token-cost summaries, dynamic benchmark requirements, hard token gates, or progressive-loading work.
- M4 completed conditional lifecycle-summary support without hard token gates, release packaging changes, adapter packaging changes, benchmark-suite expansion, or progressive-loading work.
- M5 kept progressive-loading follow-through to an audit/no-change result instead of reopening the earlier full progressive-loading proposal.

### O3: Splitting reduced scope risk, but it also added lifecycle overhead

The five-plan approach reduced the chance that one broad workflow-governance change would carry unrelated surfaces through the same spec, test spec, review, validation, and PR. It also created more formal artifact overhead: each slice needed its own spec, review, plan, test spec, implementation record, review evidence, explain-change, verification, and PR handoff.

That tradeoff was justified here because each slice had different ownership and validation boundaries: proposal/proposal-review guidance, selected skill wording, validation ownership, lifecycle token-cost reporting, and high-cost skill audit. A single plan would likely have repeated the exact amplification problem the proposal was trying to solve.

Evidence:

- M1 owned proposal/proposal-review and `docs/workflows.md` evidence guidance.
- M2 owned selected skill reminders and static proof.
- M3 owned validation-budget owner-surface guidance while preserving selector behavior.
- M4 owned conditional lifecycle report shape and warning-only boundaries.
- M5 owned high-cost skill audit and no-change rationale against the already completed progressive-loading baseline.

### O4: Broad-search behavior is still not eliminated

The repository now has stronger bounded-evidence guidance, but practice still needs discipline. During this learn session, the first evidence query was too broad and returned 7,076 lines before the search was narrowed. That mirrors prior learn evidence that broad searches returned 511 lines and then 2,118 lines in earlier token/context work.

Evidence:

- Prior learn evidence records broad searches of 511 lines and 2,118 lines, with the lesson that `max_output_tokens` is a safety rail, not a search design.
- The current learn session's initial broad query scanned `docs/plan.md`, `docs/plans`, `specs`, `docs/changes`, and `docs/learn`, returning 7,076 lines.
- A lifecycle token-cost summary was created for this session's broad-search incident: `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-slicing-retrospective.md`.

### O5: Best practice is slice-by-owner, not always-one-plan or always-many-plans

The best practice is not "always use one plan" and not "always split into many plans." Use one accepted proposal when the direction is shared, then split implementation into separate plans or PRs when the work has distinct owners, validation surfaces, risk profiles, or review gates. Keep one plan when the change is cohesive, has one implementation surface, and can be reviewed and validated as a single unit.

Evidence:

- The accepted proposal used one decision artifact for the overall direction.
- The rollout split implementation into M1-M5 because the work crossed proposal guidance, workflow guidance, skill wording, validation policy, lifecycle reporting, and progressive-loading follow-through.
- M5 demonstrates the other side of the rule: when the remaining slice was only audit/no-change rationale, it stayed one small plan with one implementation milestone.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Recorded proposal, plan, and benchmark-scope evidence | The repository has mitigation evidence, but not comparable dynamic proof that excessive token use is fully resolved. |
| O2 | observation | observation | None | Accepted proposal and M1-M5 plan evidence | The five-plan split is explained by accepted scope boundaries and plan decision logs. |
| O3 | observation | observation | None | Plan outcomes and affected-surface differences | The overhead tradeoff is observable; this session does not quantify whether five plans used fewer total tokens than one broad plan would have. |
| O4 | process-follow-up | process-follow-up | Lifecycle token-cost summary | Existing M4 trigger plus current broad-search incident | A broad-search incident occurred during this learn session, so a compact lifecycle token-cost summary was created under the existing M4 contract. |
| O5 | durable-lesson | candidate durable-lesson | Candidate topic update after confirmation | Contributor confirmation pending | The slice-by-owner rule appears reusable, but `learn` must not update topic guidance without contributor confirmation. |

## Route

- Created session record: `docs/learn/sessions/2026-05-14-cost-bounded-rigor-slicing-retrospective.md`
- Created lifecycle token-cost summary: `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-slicing-retrospective.md`
- No topic entry was created because O5 needs contributor confirmation before durable topic routing.
- No proposal, spec, ADR, skill, workflow, or plan update was created from this session.

## Answer

The excessive-token issue is not fully resolved in the sense of "we have measured an end-to-end reduction and can stop thinking about it." It is better described as mitigated by several workflow controls. The repository now has scope-budget guidance, bounded-evidence guidance, selected skill reminders, validation-budget guidance, conditional lifecycle summaries, and high-cost skill follow-through. But the evidence remains category-based and warning-only; dynamic benchmark comparison was not required for these wording/audit slices.

The work was split into five plans because the accepted proposal intentionally separated distinct implementation surfaces:

- M1: proposal/proposal-review scope budget and workflow bounded-evidence guidance.
- M2: selected skill reminders.
- M3: validation-budget owner-surface guidance.
- M4: conditional lifecycle token-cost summary support.
- M5: progressive-loading follow-through against the already completed baseline.

That split was the practical application of cost-bounded rigor. A single broad plan would have bundled proposal behavior, skill wording, validation policy, lifecycle reporting, and progressive-loading audit into one large review and validation surface.

Best practice in this context is:

- Use one proposal for the shared decision and scope budget.
- Split into separate plans when slices have different owners, tests, risks, or review gates.
- Keep one plan when the implementation is cohesive and can be validated through one narrow proof path.
- Do not split merely for ceremony; each split must reduce review ambiguity, validation breadth, or scope coupling.
- Measure enough to find waste, but do not create measurement work that becomes the new waste.

## No-Durable-Route Rationale

This session records the retrospective and one candidate durable lesson. It does not update a topic file because contributor confirmation is still required for durable guidance routing.

## Follow-Ups

- Candidate durable lesson, pending contributor confirmation: add a concise learn topic entry that says workflow-governance efforts should use one proposal for the shared decision and separate plans only when implementation slices have distinct owners, tests, risks, or review gates.
- No new proposal is recommended from this session because the relevant cost-bounded-rigor controls have already been implemented or are represented by PR #58.
