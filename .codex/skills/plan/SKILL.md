---
name: plan
description: >
  Create or revise a living execution plan after proposal, spec, and architecture are stable enough to implement. Use for multi-file, multi-component, risky, or milestone-based work that should be split into reviewable milestone slices.
argument-hint: [feature name, spec path, architecture path, or implementation goal]
---

# Living execution plan

You are turning approved behavior and architecture into a safe, reviewable implementation path.

Planning happens after the spec defines behavior and architecture defines the design direction. Do not use this skill to decide what the product should be.

## Purpose

Create or revise a concrete execution plan that turns approved artifacts into reviewable implementation milestones, validation commands, recovery paths, and lifecycle readiness.

## When to use

Use this skill after proposal, spec, and architecture are stable enough to sequence implementation, especially for multi-file, risky, milestone-based, migration-heavy, or cross-component work.

## When not to use

Do not use this skill to choose product direction, replace missing specs, perform implementation, claim review or verification outcomes, or mark work Done when downstream lifecycle gates remain.

## Inputs to read

Read:

- `AGENTS.md`
- `CONSTITUTION.md` if present
- `docs/plan.md` if present
- accepted proposal
- approved or reviewed feature spec
- spec-review findings
- architecture doc and ADRs when relevant
- architecture-review findings when available
- test-spec if already created
- `docs/project-map.md`
- relevant code, tests, CI, and workflows

## Upstream status settlement

In workflow-managed downstream execution, before relying on a spec, architecture package, or ADR, check whether its tracked status matches clear formal review evidence.

Do not run upstream status settlement for review-only, no-edit, or manual inspection requests. Those requests remain isolated.

During normal workflow-managed downstream execution, do not ask whether edits are allowed; the downstream invocation permits minimal settlement.

Settle only lifecycle/status/readiness/follow-on/closeout metadata. Do not rewrite substantive artifact content.

The clear review evidence check requires:

- durable formal review evidence for the upstream artifact;
- an approving or clean review outcome;
- no later contradictory review record;
- no open findings in `review-log.md` when present;
- closed `review-resolution.md` for material findings when required;
- an explicit settlement mapping for this skill.

Mappings for this skill:

- spec-review approved with no unresolved material findings -> spec `Status: approved`.
- architecture-review approved for an architecture package with no unresolved material findings -> architecture `Status: approved`.
- architecture-review approved for an ADR with no unresolved material findings -> ADR status `accepted` or `active` only when the ADR lifecycle vocabulary clearly supports that target.

If review evidence is missing, contradictory, unresolved, the status surface is absent, the artifact type is unmapped, or the ADR has unknown lifecycle vocabulary, block instead of guessing.

If the artifact type, lifecycle field, next status, or target status is unknown or unmapped, block instead of inferring a settlement.

Report `## Upstream status settlement` when settlement was updated, blocked, or stale status was detected:

```md
## Upstream status settlement

- Upstream artifact:
- Review evidence:
- Previous status:
- New status:
- Settlement result: updated | blocked | not-needed
- Settlement blocker:
```

For blocked settlement with a deterministic target, report that intended target in `New status`. For blocked settlement with no deterministic target, report `New status: not-applicable`. `Settlement blocker` is required for blocked settlement and must distinguish a known target blocked by evidence/state from an unknown target blocked by missing mapping or lifecycle vocabulary.

## Output paths

Prefer:

```text
docs/plans/YYYY-MM-DD-slug.md
docs/plan.md
```

Create a new dated plan for new initiatives. Update `docs/plan.md` as the lifecycle index of active, blocked, done, and superseded plans.
For planned initiatives, `docs/plan.md` remains the lifecycle index while files under `docs/plans/` remain the plan bodies. `plan` owns creating or revising those surfaces when an initiative starts or is re-planned, not every later execution-time update.

## Outputs

Produce or update the concrete plan body and, when starting or replanning an initiative, the `docs/plan.md` lifecycle index. The plan must name the milestone sequence, validation commands, recovery path, current handoff summary, and remaining completion gates.

## Handoff

- Normal next stage: `plan-review`.
- Conditional next stages: return to `spec` or `architecture` when planning exposes a blocking gap; proceed to `test-spec` only after plan-review when the workflow allows it.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Claims this skill must not make

Do not claim:

- code is implemented, review passed, verification passed, branch-ready, or PR-ready;
- the plan is Done merely because it is ready for the next stage;
- ready for PR or ready for final closeout without explicit remaining gates and the owning review/verification evidence;
- derived artifacts are current unless validation evidence proves it.

Use `Readiness is not Done` as the default interpretation for handoff lines. Keep `Remaining completion gates` visible whenever readiness could be confused with completion.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. A plan may remain `Active` while it is ready for the next gate.

## Required sections

1. **Status**: draft, reviewed, active, blocked, done, superseded.
2. **Purpose / big picture**: why this implementation plan exists.
3. **Source artifacts**: proposal, spec, architecture, test spec.
4. **Context and orientation**: files, modules, flows, and constraints a new contributor needs.
5. **Non-goals**: scope guardrails from proposal/spec.
6. **Requirements covered**: list requirement IDs and where they will be implemented.
7. **Milestones**: small reviewable slices.
8. **Validation plan**: commands and manual checks per milestone.
9. **Risks and recovery**: rollback, feature flags, migration recovery, idempotence.
10. **Dependencies**: internal and external sequencing constraints.
11. **Progress**: checkboxes or status per milestone.
12. **Decision log**: implementation decisions made during planning.
13. **Surprises and discoveries**: updated during implementation.
14. **Validation notes**: evidence from implementation.
15. **Outcome and retrospective**: filled after completion.

## Milestone format

Each milestone should include:

```text
M1. Title
- Milestone state:
- Goal:
- Requirements:
- Files/components likely touched:
- Dependencies:
- Tests to add/update:
- Implementation steps:
- Validation commands:
- Expected observable result:
- Commit message: `M1: <completed milestone outcome>`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
- Rollback/recovery:
```

Milestones should be small enough for one review loop and one coherent commit. A PR may contain one or more completed milestones when that is the clearest review boundary.

## Milestone-aware plans

For milestone-based plans, each implementation milestone has exactly one `Milestone state`.

Allowed values:

- `planned`
- `implementing`
- `review-requested`
- `resolution-needed`
- `closed`

Use `review-requested` after implementation and targeted validation complete and the slice has been handed to `code-review`. Use `resolution-needed` when review findings require review-resolution, fixes, owner decision, or re-review. `implementation-complete` and `review-clean` are evidence descriptions, not milestone state values.

Each implementation milestone normally follows this loop:

```text
implement M<n>
-> code-review M<n>
-> review-resolution M<n>, when triggered
-> implement fixes for M<n>, when needed
-> code-review M<n> rerun, when needed
-> close M<n>
-> implement M<n+1>, when another in-scope implementation milestone remains
```

Do not hand off to final closeout until all in-scope implementation milestones are `closed` or explicitly removed by plan revision and required review-resolution is closed.

Milestones are not postponed to make final closeout available. If a planned implementation milestone no longer belongs in the current change, revise the plan before handoff.

Use `lifecycle-closeout` for a milestone or section that tracks only downstream gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or final plan closeout. A mixed milestone that still contains implementation work remains an implementation milestone for final-closeout readiness decisions.

For milestone-based plans, include and update a current handoff summary whenever implementation or review changes milestone readiness:

```text
Current milestone:
Current milestone state:
Last reviewed milestone:
Review status:
Remaining in-scope implementation milestones:
Next stage:
Final closeout readiness:
Reason final closeout is or is not ready:
```

The active plan `Readiness` section points to `Current Handoff Summary` for current live state. Do not duplicate the current next stage outside `Current Handoff Summary` unless the statement is explicitly historical.

## Planning rules

- Derive work from spec requirements and architecture decisions.
- Do not add behavior not in the spec.
- Do not hide risky work in vague milestones.
- Do not omit validation commands.
- Keep `docs/plan.md` as an index, not a second long-form plan body.
- When planning starts a new initiative or replaces an older one, update the relevant `docs/plan.md` entry and plan body in the same planning change.
- When a plan lifecycle transition is performed by a PR, plan the synchronized `docs/plan.md` and plan-body update before the PR opens for review.
- If completion depends on a true downstream completion event, keep the plan `Active` and name that event; merge itself is not that event.
- Do not create a plan that only the current chat context can understand.
- Do not proceed to implementation until `plan-review` and `test-spec` are ready unless the user explicitly requests an isolated manual skill invocation and the limitation is recorded.
- If planning reveals spec or architecture gaps, update those artifacts first.

## Stop conditions

Stop before handoff when:

- required source artifacts are missing, contradictory, or not approved enough for the workflow state;
- architecture, migration, security, or release boundaries are too unclear to sequence safely;
- validation commands cannot be identified;
- a milestone would rely on chat-only context;
- the plan would hide open implementation work behind `Ready for final closeout`, Done, or PR readiness wording.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Skill: plan
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
- Readiness:
```

Then include:

- concrete plan file path;
- updated `docs/plan.md` index when applicable;
- milestone-by-milestone plan;
- validation and recovery strategy;
- readiness statement for `plan-review` and `test-spec`.
