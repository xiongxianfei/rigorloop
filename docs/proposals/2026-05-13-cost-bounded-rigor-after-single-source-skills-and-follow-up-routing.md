# Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing

## Status

accepted

## Problem

RigorLoop has completed two structural improvements that remove prior sources of workflow cost and confusion:

1. Single authored skill source.
2. Follow-up ownership routing.

After [PR #52], generated public adapter skill bodies are no longer ordinary tracked source. `skills/` is the single authored skill source, while public adapter packages are release-generated output. The constitution now reflects this model: `skills/` is the only authored skill source, and generated public adapter skill bodies for `v0.1.3` and later are release archives rather than tracked source under `dist/adapters/`.

After [PR #53], deferred work has a routing model: workflow routes, project-map orients when present, action-owning artifacts track work, and unowned cross-change follow-ups use the follow-up ownership surface instead of being hidden in chat or project-map notes.

Those changes remove two completed cleanup tracks. The remaining cost problem is workflow amplification:

```text
large proposal scope
-> many spec/plan/test/review surfaces
-> broad evidence collection
-> multiple review findings
-> repeated validation
-> repeated state reconciliation
```

The next improvement should optimize workflow operating behavior now that single-source skills and follow-up ownership are in place.

Core goal:

```text
Preserve rigor.
Reduce waste.
Make every stage prove the smallest sufficient thing with the smallest sufficient evidence.
```

## Goals

- Reduce proposal-to-implementation token cost without weakening RigorLoop rigor.
- Use the completed single-authored-skill-source model as the baseline.
- Use the completed follow-up ownership model as the routing surface for deferred work.
- Keep `docs/workflows.md` as the artifact-location and follow-up routing guide.
- Ask broad proposals to separate core scope from deferrable follow-ups.
- Make stage evidence collection bounded by default.
- Reduce broad authoritative-document searches for path discovery.
- Keep high-cost public skills progressively loadable.
- Record lifecycle token-cost evidence for large workflow-governance or release changes.
- Keep safety-critical review, verification, material-finding, and release rules intact.

## Non-goals

- Do not reintroduce tracked generated adapter skill bodies.
- Do not move deferred-work ownership into `project-map`.
- Do not weaken formal review, verify, PR, or material-finding rules.
- Do not turn token thresholds into hard blockers before enough comparable reports exist.
- Do not rewrite every skill in one change.
- Do not remove safety-critical guidance solely because it is long.
- Do not replace proposal/spec/plan/review artifacts with chat summaries.
- Do not use `docs/follow-ups.md` as a dumping ground for current-change work.
- Do not update adapter packaging surfaces unless this proposal directly changes release evidence or benchmark source behavior.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to rigorous, traceable, AI-assisted delivery. It makes the workflow more efficient while preserving durable artifacts, explicit evidence, and human-reviewable change history.

## Context

[PR #52] changed the repository source model: generated public adapter skill bodies are no longer ordinary tracked source, `skills/` is the authored source, and adapter packages are validated/generated release output. The current constitution reflects that only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are the tracked adapter support surface.

[PR #53] changed follow-up routing: `workflow` owns routing guidance, `project-map` does not own deferred execution, and unowned cross-change follow-ups have an explicit route. `docs/workflows.md` now records the follow-up placement model.

The remaining cost problem is therefore not duplicated generated skill sources or unclear follow-up ownership. It is workflow amplification through broad proposals, broad searches, oversized stage guidance, repeated loops, and validation scopes that are larger than the stage actually owns.

The token-cost learning already says token optimization should diagnose static size, runtime reads, command output, full-file reads, broad searches, and context-base effects separately before deleting guidance.

The context-budget learning also identifies unbounded evidence collection as a concrete issue: broad searches returned large output, while the better practice is bounded extraction first.

No `docs/project-map.md` file was present during proposal authoring. This proposal relies on `docs/workflows.md` for artifact location and follow-up routing.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Account for [PR #52] single-skill-source completion. | in scope | Context; Non-goals; Workstream F |
| Account for [PR #53] follow-up routing completion. | in scope | Context; Workstream E |
| Reduce proposal-to-implementation token cost. | in scope | Goals; Recommended direction |
| Keep rules simple and concise. | in scope | Goals; Scope budget; Risks and mitigations |
| Preserve RigorLoop rigor. | in scope | Goals; Non-goals; Recommended direction |
| Avoid re-solving completed cleanup. | in scope | Non-goals; Scope budget; Workstreams E and F |
| Generate updated proposal. | in scope | This document |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Proposal scope budget guidance for broad or multi-part proposals | first-slice candidate | This is the primary mechanism for stopping broad proposal amplification before downstream stages rely on it. |
| Bounded evidence and path-search guidance | first-slice candidate | This directly targets the remaining token-cost driver after single-source skills and follow-up routing. |
| Stage validation-budget guidance | separate implementation slice | This is important, but selector behavior and validation contracts need their own focused slice if executable behavior changes. |
| Lifecycle token-cost summaries for large workflow-governance or release changes | deferred or conditional follow-up | This can provide comparable evidence, but it should not add routine artifact overhead before tight triggers exist. |
| Use the PR #53 follow-up ownership model | same-slice dependency | Deferred items discovered by this change need the accepted routing model instead of project-map or chat. |
| Treat PR #52 single-source skills as completed context | same-slice dependency | The proposal should not reopen generated adapter source cleanup. |
| Full progressive-loading implementation for `workflow`, `implement`, and `code-review` | separate proposal | The accepted progressive-loading proposal already owns the larger skill restructuring direction; this proposal should align with it rather than duplicate it. |
| Rewriting every public skill | out of scope | Broad skill churn would undermine the cost-bounded premise. |
| Hard token thresholds in CI | deferable follow-up | More comparable lifecycle reports are needed before token totals become blockers. |
| Adapter archive or release validation changes | out of scope unless touched by later spec | Adapter packaging is already handled by the single-source release model. |

Scope budget treatment values:

```text
core to this proposal:
  needed for this change to satisfy its goal

first-slice candidate:
  likely belongs in the first implementation slice, subject to proposal-review and spec/plan shaping

same-slice dependency:
  needed in the same implementation slice because the main change cannot pass without it

separate implementation slice:
  belongs in this initiative, but should be implemented and reviewed separately

deferable follow-up:
  real future work, but not required for this change

separate proposal:
  related but independently valuable or risky enough to use its own proposal

out of scope:
  explicitly not part of this change
```

## First implementation slice

The first implementation slice covers only:

- scope-budget guidance for broad or multi-workstream proposals;
- proposal-review checks for missing scope-budget classification;
- concise bounded-evidence and path-search wording in `docs/workflows.md`.

Out of first-slice scope:

- selector or validation-budget behavior changes;
- lifecycle token-cost summary artifacts;
- dynamic benchmark changes;
- broad progressive-loading implementation;
- edits to `implement` or `code-review` unless the plan explicitly scopes them;
- release validation changes;
- adapter packaging changes;
- rewriting every public skill.

Later slices can handle:

```text
M2: bounded evidence wording in selected skill surfaces, limited to `proposal`, `proposal-review`, and `workflow`
M3: validation-budget guidance
M4: lifecycle token-cost summary
M5: progressive-loading follow-through
```

## Options considered

### Option 1: Keep the workflow unchanged after PR #52 and PR #53

Advantages:

- No new process changes.
- Avoids further skill churn.

Disadvantages:

- Leaves proposal-to-implementation cost high.
- Does not address broad evidence collection.
- Does not prevent multi-workstream proposal amplification.
- Does not improve stage validation budgeting.

### Option 2: Add hard token budgets now

Advantages:

- Easy to measure.
- Makes cost visible.

Disadvantages:

- Premature hard gates can block useful rigorous work.
- Token totals are still affected by runtime behavior, tool output, and prompt/context base.
- May incentivize deleting safety-critical guidance.

### Option 3: Add cost-bounded rigor rules

Advantages:

- Preserves engineering rigor.
- Targets known waste patterns.
- Uses completed single-source and follow-up-routing foundations.
- Avoids hard token gates too early.
- Keeps skill guidance concise and operational.

Disadvantages:

- Requires careful stage-skill wording.
- Requires measurement discipline.
- Does not instantly reduce all token costs.

## Recommended direction

Choose Option 3.

Adopt cost-bounded rigor:

```text
Smallest sufficient decision.
Smallest sufficient evidence.
Smallest sufficient artifact set.
Smallest sufficient validation set.
```

This does not mean weaker workflow. It means each stage should avoid unnecessary expansion before proving what it actually owns.

## Workstream A: Proposal scope budget

Broad proposals should classify work items before downstream stages rely on them.

### Scope-budget trigger

A proposal requires a scope budget when any of these are true:

- the user request contains two or more independent work items;
- the change touches more than one lifecycle family, such as release packaging plus skill wording plus examples migration;
- the change could reasonably require more than one spec or implementation plan;
- the proposal includes release policy, workflow policy, generated output, public skill behavior, or validation policy;
- the proposal-reviewer identifies silent narrowing or hidden follow-up risk.

Small single-decision proposals may omit the scope budget.

Scope-budget applicability is a proposal/proposal-review judgment in the first implementation slice.

Validators may check table shape when a `Scope budget` table exists, but they must not fail a proposal solely because they infer that the proposal is broad. A proposal-review finding may require a scope budget when silent narrowing, hidden follow-up risk, or multi-workstream scope is evident.

Add or preserve this section for broad or multi-part proposals:

```md
## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| <work item> | core to this proposal / first-slice candidate / same-slice dependency / separate implementation slice / deferable follow-up / separate proposal / out of scope | <why> |
```

Deferred follow-ups should route through the accepted follow-up model from PR #53:

```text
current-change follow-up -> active plan/change artifact
review finding follow-up -> review-resolution
repeated lesson -> learn
new policy/product direction -> proposal
unowned cross-change follow-up -> docs/follow-ups.md / follow-up ownership surface
```

## Workstream B: Evidence budget

Stages should use bounded evidence before broad reads.

Default evidence sequence:

```text
1. exact user-provided path or change ID
2. current handoff summary / active plan state
3. change.yaml, review-log, review-resolution, or release metadata
4. docs/workflows.md artifact-location map
5. targeted headings, stable IDs, line ranges, counts, or diffs
6. full-file read only when the whole file is the target or bounded evidence is insufficient
```

Public skills should include concise wording:

```md
Use bounded evidence before broad reads, but do not under-read.

Start from active state, metadata, `docs/workflows.md`, headings, and targeted excerpts. Expand to a broader section or full file when narrower evidence is incomplete, contradictory, or insufficient to support the claim being made.
```

`docs/workflows.md` owns the full evidence-budget rule. Skills that directly need the behavior should get only a short operational reminder, not a repeated shared template.

## Workstream C: Validation budget

Each stage should validate what it owns.

Validation-budget behavior is owned by:

- `docs/workflows.md` for operational guidance;
- validation-selection scripts and specs for executable check selection;
- stage skills only for concise local reminders.

If implementation changes selector behavior, the spec and test spec should cover it. If implementation only changes wording, skill-validator coverage is sufficient.

Examples:

```text
proposal-only change:
  validate proposal lifecycle and diff cleanliness

spec change:
  validate spec/test-spec surfaces and affected validators

skill wording change:
  validate canonical skills and skill-validator checks

release packaging change:
  validate release metadata, adapter artifacts, token-cost report, and release notes

review artifact change:
  validate review artifacts and change metadata
```

Broad release validation should not run for draft proposal-only changes unless the proposal changes release validation itself.

## Workstream D: Lifecycle token-cost summary

Lifecycle token-cost summaries are conditional, not routine.

They are required only for:

- large workflow-governance changes;
- release changes;
- changes where dynamic benchmark warnings or broad-search incidents occur;
- explicit maintainer request.

They are optional for ordinary feature, docs, proposal, or small skill edits.

Do not expand these triggers yet. After 3-5 completed lifecycle token-cost summaries exist, review whether they found actionable cost drivers before expanding the trigger set.

Lifecycle token-cost summaries are deferred. A later proposal or spec should define the exact report path and schema.

The intended field groups are:

- identity
- trigger
- scope
- source artifacts
- observed cost drivers
- largest observed event
- result/rationale

Detailed numeric comparisons, exact model usage, run-to-run variance, threshold regression results, hard-gate recommendations, and before/after dynamic benchmark comparison remain advisory unless a benchmark actually ran or a later plan/test-spec requires them.

This report is diagnostic, not a hard gate, and it is out of scope for the first implementation slice.

## Workstream E: Follow-up routing after PR #53

This proposal should no longer say "create a follow-up ownership model" as future work. That model is now completed.

Instead, this change should use the model:

```text
workflow routes
project-map orients when present
action-owning artifacts track work
unowned cross-change follow-ups use the follow-up ownership surface
```

If a future work item is discovered during this proposal, classify it in the scope budget and place it in the correct owner artifact.

## Workstream F: Single-source skills after PR #52

This proposal should no longer treat generated adapter skill bodies as an active source problem to solve. That cleanup is completed by PR #52.

New wording for downstream artifacts:

```text
The repository now has one authored skill source under `skills/`.

Do not search generated adapter output for skill truth.

Do not add generated adapter skill bodies back to tracked source.

Release and benchmark work should use generated release-output archives or the accepted public adapter release surface.
```

## Workstream G: Progressive-loading alignment

This proposal should align with the accepted progressive-loading direction without absorbing that separate proposal's full implementation scope.

Priority skills remain:

```text
workflow
implement
code-review
```

Reason: the `v0.1.1` token-friendliness report identified `workflow` as a high-warning static-size skill, `code-review` as a warning static-size skill, whole-skill reads in dynamic benchmarks, and `implement-handoff` as the largest command-output cost driver.

Required direction for any skill touched by this change:

- quick operating guide or equivalent targeted entry point when the skill is high-cost
- targeted reading first
- concise result output
- no broad path discovery
- no deletion of safety-critical review or verification guidance

This proposal may add concise bounded-evidence wording to high-cost skills when those skills are touched. It does not implement the full progressive-loading proposal unless a later plan explicitly scopes that as a separate milestone.

## Expected behavior changes

Before:

```text
A broad proposal can carry many workstreams into every downstream stage.
```

After:

```text
The proposal classifies each workstream as core scope, first-slice candidate, separate slice, dependency, follow-up, separate proposal, or out of scope.
```

Before:

```text
Agents may broad-search specs, docs, and skills to find paths or state.
```

After:

```text
Agents start from current state, docs/workflows.md, metadata, headings, counts, and targeted excerpts.
```

Before:

```text
Deferred work can be hidden in chat or project-map notes.
```

After:

```text
Deferred work uses the PR #53 follow-up routing model.
```

Before:

```text
Generated adapter skill bodies were a repeated review and benchmark surface.
```

After:

```text
PR #52 completed single-authored-source cleanup; this proposal does not reintroduce generated skill bodies as tracked source.
```

## Architecture impact

No runtime architecture change is expected.

This is a workflow-operation, skill-guidance, validation-selection, and token-measurement improvement.

Affected surfaces may include:

```text
docs/workflows.md
skills/proposal/SKILL.md
skills/proposal-review/SKILL.md
skills/workflow/SKILL.md
scripts/test-skill-validator.py
docs/reports/token-cost/
```

First-slice skill surfaces are limited to `proposal`, `proposal-review`, and `workflow` when the plan proves a skill edit is necessary. `implement` and `code-review` are deferred unless a later plan explicitly scopes progressive-loading alignment.

Adapter packaging surfaces are unaffected unless a later spec directly changes release evidence or benchmark source behavior.

## Testing and verification strategy

For this proposal-only artifact, use targeted lifecycle and diff checks.

Suggested proposal validation:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md
python scripts/select-validation.py --mode explicit --path docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md
git diff --check -- docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md
```

If the later implementation changes skill wording:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/select-validation.py --mode explicit --path <changed-skill-path>
python scripts/measure-skill-tokens.py
git diff --check --
```

If token-cost scripts change:

```bash
python scripts/test-token-cost-measurement.py
python scripts/test-token-cost-report-validation.py
```

If workflow docs change:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md
```

Adapter archive or release validation is not part of this proposal unless a later spec or plan touches release/adapter packaging.

## Measurement expectation

After implementation, record:

- static skill token total before/after when skills changed;
- whether broad-search or full-skill-read warnings changed for affected benchmark prompts;
- largest observed command-output event if a dynamic benchmark was run;
- qualitative explanation if no dynamic benchmark was run.

This measurement is diagnostic and warning-only. It does not set a hard token target.

When a change only updates proposal or evidence wording, before/after dynamic benchmark comparison is not required. The plan or test spec decides whether dynamic benchmark comparison is required; `implement` or the release benchmark process runs it when planned, `explain-change` summarizes why it was or was not run, and `verify` checks that required evidence matches the accepted plan.

## Rollout and rollback

### Rollout

Use reviewable slices:

1. M1: add the scope-budget trigger and table guidance to proposal and proposal-review surfaces, plus concise bounded evidence/path-search wording in `docs/workflows.md`.
2. M2: add minimal selected skill wording for `proposal`, `proposal-review`, and `workflow`, plus static checks only if M1/M2 require them.
3. M3: add validation-budget guidance so stage validation remains targeted unless release, test-spec, review-resolution, broad-smoke, or plan triggers apply.
4. M4: define conditional lifecycle token-cost summary support for large workflow-governance or release changes.
5. M5: align any touched high-cost skills with progressive-loading guidance without duplicating the full accepted progressive-loading proposal.

### Rollback

If scope-budget guidance creates too much proposal overhead:

```text
limit it to broad or multi-workstream proposals only
```

If evidence-budget wording causes under-reading:

```text
restore stronger full-file-read escape conditions while preserving bounded-first lookup
```

If lifecycle token-cost reports become noisy:

```text
make them optional and trigger them only for large workflow-governance or release work
```

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Agents under-read important context. | Preserve full-file-read escape conditions. |
| Cost reduction weakens rigor. | Keep validation semantics and formal review rules unchanged. |
| Scope budget becomes bureaucracy. | Trigger it for broad or multi-workstream proposals. |
| Follow-up register becomes a dumping ground. | Use action-owning artifacts first. |
| Token reports add overhead. | Require them only for tightly triggered workflow-governance, release, benchmark-warning, broad-search-incident, or maintainer-request cases. |
| Skills become vague. | Keep exact blockers, default paths, and result formats. |

## Acceptance criteria

- Broad proposals include a scope-budget table or equivalent classification when the trigger applies.
- Small single-decision proposals may omit the scope budget.
- Scope-budget applicability is proposal/proposal-review judgment in the first slice; validators do not infer broadness.
- `docs/workflows.md` remains the path, follow-up-routing, and full bounded-evidence guide.
- The proposal records validation-budget ownership as a later slice and does not change selector behavior in the first implementation.
- When M3 is implemented, validation-budget guidance distinguishes `docs/workflows.md` guidance, selector behavior, and skill-local reminders.
- `workflow`, `implement`, and `code-review` preserve progressive-loading boundaries when they are touched.
- Deferred work routes through the PR #53 follow-up ownership model.
- The proposal does not reintroduce tracked generated adapter skill bodies.
- Token-cost measurement remains category-based, not a premature hard gate.
- Measurement expectations are diagnostic and warning-only.
- Safety-critical review, verification, material-finding, and release guidance is preserved.

## Resolved decisions

No open questions block spec or plan.

| Question | Decision |
|---|---|
| Should future slices expand lifecycle token-cost summaries beyond the initial conditional triggers? | Not yet. Keep summaries conditional until several examples prove they reduce cost more than they add overhead. |
| Should the scope-budget table become part of the proposal validator? | Not as a hard validator in the first slice. Keep it as proposal/proposal-review guidance first; validators may check table shape when present. |
| Which token-cost report fields should be required versus advisory first? | Intended required groups are identity, trigger, scope, source artifacts, observed cost drivers, largest observed event, and result/rationale. The exact report path and schema belong in a later proposal or spec. Keep detailed numeric comparisons advisory unless a benchmark actually ran. |
| Who owns before/after dynamic benchmark comparison for a first slice that changes only proposal/evidence wording? | No required dynamic benchmark comparison. The active plan/test spec decides whether one is needed; `explain-change` records the rationale, and `verify` checks required evidence. |

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-13 | Treat PR #52 as completed context. | The repository now has one authored skill source under `skills/`; generated adapter skill bodies are not ordinary tracked source. |
| 2026-05-13 | Treat PR #53 as completed context. | Follow-up ownership routing now exists; project-map does not own deferred execution. |
| 2026-05-13 | Focus this proposal on cost-bounded rigor. | Remaining waste comes from scope, evidence, validation, and review-loop amplification. |
| 2026-05-13 | Avoid hard token gates for now. | More comparable lifecycle cost data is needed before blocking releases on totals. |
| 2026-05-13 | Narrow the first implementation slice. | Cost-bounded rigor should first prevent broad proposal scope and broad evidence reads before adding reporting or high-cost skill restructuring. |
| 2026-05-13 | Keep lifecycle token-cost summaries conditional. | Measurement should earn its place by finding actionable cost drivers instead of becoming routine artifact overhead. |
| 2026-05-13 | Keep scope-budget validation guidance-first. | Broadness is semantic; first-slice validators should check table shape only when present rather than infer broad scope. |
| 2026-05-13 | Keep first-slice token-cost field groups small. | Identity, trigger, scope, observed drivers, largest event, and result/rationale are enough to sketch why the summary exists and what it found; exact schema belongs in a later artifact. |
| 2026-05-13 | Do not require dynamic benchmark comparison for proposal/evidence wording changes. | The active plan or test spec owns the benchmark decision; explain-change records the rationale and verify checks required evidence. |
| 2026-05-13 | Keep first-slice implementation narrow. | M1 should cover proposal/proposal-review scope-budget guidance and concise workflow evidence wording before skill, validator, or reporting work expands. |

## Next artifacts

```text
proposal-review
spec, if the scope/evidence/validation budget becomes normative
plan
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Proposal-review receipt: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r1.md`
- Proposal-review findings: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r2.md`
- Proposal-review approval: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/proposal-review-r3.md`
- Review-resolution closeout: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/review-resolution.md`
- First-slice spec: `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`
- Spec-review approval: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md`
- Execution plan: `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md`
- M2 selected skill reminders spec: `specs/cost-bounded-rigor-m2-selected-skill-reminders.md`
- M2 selected skill reminders plan: `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md`
- M3 validation-budget guidance spec: `specs/cost-bounded-rigor-m3-validation-budget-guidance.md`
- Plan-review approval: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/plan-review-r1.md`
- Test spec: `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`

## Readiness

Accepted after clean proposal-review evidence. The approved spec, active plan, and active test spec now own the implementation handoff.

## Core invariant

```text
Rigor is non-negotiable.
Waste is optional.

Use the smallest sufficient decision, evidence, artifact set, and validation set.
```

[PR #52]: https://github.com/xiongxianfei/rigorloop/pull/52
[PR #53]: https://github.com/xiongxianfei/rigorloop/pull/53
