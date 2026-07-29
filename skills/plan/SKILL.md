---
name: plan
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or revise a stable execution plan after proposal, spec, and architecture are settled enough to implement. Use for multi-file, multi-component, risky, migration-heavy, or milestone-based work that needs reviewable implementation slices, validation commands, recovery paths, and dependencies. Use spec, test-spec, implement, code-review, verify, or pr for those stages; do not use plan to choose product direction, write code, review diffs, update workflow routing or existing planned work, verify branch readiness, or open PRs.
argument-hint: [feature name, spec path, architecture path, or implementation goal]
---

# Stable execution plan

Sequence approved behavior and architecture into reviewable implementation. Do not decide product direction.

## Purpose

Create or revise a concrete execution plan with milestones, validation commands, recovery paths, and lifecycle readiness.

## Workflow role

- role_name: plan
- stage: authoring
- upstream: accepted proposal, approved or reviewed spec, architecture records or ADRs when relevant, test-spec when already present, and project-local workflow evidence
- downstream: plan-review
- summary: Create or revise the stable execution intent, milestone sequence, validation strategy, and recovery path.
- must_not_claim: implementation completion, review approval, verification, branch readiness, PR readiness, final closeout readiness, or Done while downstream gates remain.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant: `AGENTS.md`, `CONSTITUTION.md`, `docs/plan.md`, accepted proposals, approved specs, test specs, architecture records, ADRs, review findings, `docs/project-map.md`, `docs/workflows.md`, source files, tests, CI, and workflow files.

Do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects. Use portable defaults where safe, and block on ambiguity.

## Resource map

- READ `references/boundary-first-method-v1.md` when cited approved boundary or interaction rows are missing, stale, unknown, ambiguous, conflicting, or insufficient for planning.
- COPY `assets/plan-skeleton.md` when creating a new plan or replacing the full plan structure.
  Fill: sections, placeholders, and the stable owning change-record pointer.
  Sections: Purpose / big picture; Current Handoff Summary; Source artifacts; Context and orientation; Non-goals; Requirements covered; Milestones; Validation plan; Risks and recovery; Dependencies; Decision log; Readiness.
  Do not emit unfilled placeholders.
- COPY `assets/milestone.md` when adding each reviewable implementation milestone.
  Fill: ID, state, goal, requirements, files, tests, steps, validation, result, risks, rollback.
  Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` when recording a material planning or sequencing decision.
  Fill: date, decision, reason, and rejected alternatives.
  Do not emit unfilled placeholders.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Use semantic source lines for human-facing prose; one sentence or natural clause per source line when practical.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## When to use

Use after proposal, spec, and architecture are stable enough to sequence multi-file, risky, milestone-based, migration-heavy, or cross-component work.

## When not to use

Do not choose product direction, replace missing specs, implement code, claim review or verification outcomes, or mark work Done while downstream lifecycle gates remain.

## Inputs to read

Read needed project-local evidence: `AGENTS.md`, `CONSTITUTION.md` if present, `docs/plan.md`, accepted proposal, approved or reviewed spec, architecture or ADRs when relevant, test-spec if present, `docs/project-map.md`, code, tests, CI, and workflows.

Use bounded evidence first. Use broader-section or full-file reading when the target file is the artifact, relevant sections cannot be isolated safely, or surrounding context can change the plan.

## Upstream settlement check

Before relying on a spec, architecture package, or ADR, read each matching `change.yaml` artifact entry and formal review evidence.
Require the artifact-specific settled state, no later contradictory review, no open findings, and closed review resolution when required.

Treat every upstream artifact and lifecycle entry as read-only.
Do not normalize embedded status or settle an upstream entry.
If settlement is missing, contradictory, unknown, or unmapped, record the blocker and route to the matching review stage.

## Change-record authoring transition

For a governed change, read the complete `change.yaml` before writing.
Require `lifecycle_contract: stage-owned-change-local-v1`; route a missing marker to `workflow` for creation or migration instead of inventing state.
Resolve exactly one plan entry by artifact ID, `kind`, and normalized `path`.
For a new plan, create only that entry with a unique stable ID, `kind: plan`, normalized path, and explicit role. Before creating or substantively revising the plan, set only that entry to `authoring`, remove any prior `review`, and set `authoring_evidence` to the plan-authoring record path.
When registering a new primary plan and `planned_work` is absent, initialize `workflow_state.planned_work` exactly once from the plan's ordered milestones: set every implementation milestone to `planned`, set `current_milestone` to the first implementation milestone, list all implementation milestones in `remaining_implementation_milestones`, use `latest_review.status: not-started` with its required empty identity fields and evidence, and use `final_closeout.readiness: not-ready` with the applicable open-gate reasons. The plan must not replace or update existing `planned_work`; workflow owns every later `planned_work` transition.
After the plan and authoring record are complete, set the same entry to `review-required`. Preserve every other entry and every other `workflow_state` field. Stop on an ambiguous entry, illegal transition, or failed available change-metadata validation.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Plan surfaces:

- Workflow map: `docs/workflows.md` describes project-local workflow and artifact-location customizations.
- Plan index: `docs/plan.md` is a stable navigation index.
- Plan body: `docs/plans/YYYY-MM-DD-slug.md` carries stable execution intent for a planned initiative.
- Change metadata: `docs/changes/<change-id>/change.yaml` is the sole owner of mutable workflow and milestone state.
- Change-local evidence: `docs/changes/<change-id>/` contains review, rationale, verification, and related lifecycle evidence.

Lookup order: explicit user path or change ID; change metadata; reviewed artifact path; plan body; known governing spec or schema constraint when directly relevant; `docs/workflows.md` artifact-location table; this skill's portable default path; block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Use `docs/workflows.md` only for artifact types it specifies. If it is present but silent for a plan surface, use this skill's portable default path.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Change-record bounded reads

For planned change records when present, read current workflow and milestone state from `docs/changes/<change-id>/change.yaml`.
Use the plan body only for stable milestone intent.
When the project provides a query helper, use it as a bounded view of the change record, not as a second state owner.

Escalate from bounded helper output to full `change.yaml` when planning depends on forensic reconstruction, unsupported-shape diagnostics, disputed evidence, migration compatibility, or whole-record review.

## Expected output

Output a compact result plus a plan artifact. Copy `assets/plan-skeleton.md` for section order and other assets for repeated structures. Do not duplicate full layout here.

## Outputs

Produce or update the stable plan body and, when needed, its navigation entry in `docs/plan.md`.
Name milestones, validation, recovery, and dependencies.
The plan stage may record its own authoring transition and one-time deterministic initialization of missing primary-plan `planned_work`; it must not write review settlement, routing, or later planned-work transitions.

## Result

- Skill: plan
- Status: <created | updated | blocked>
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: <plan-review | test-spec after plan-review | blocked>

## Boundary-first method

Map applicable boundaries to independently closeable milestones, dependencies, affected surfaces, rollback units, and proof timing.

Use only approved boundary and interaction IDs. Stop planning when an applicable boundary lacks an owning milestone, dependency, rollback unit, affected surface, or timed proof obligation; route a contract gap upstream instead of repairing it in the plan.

## Handoff

- Normal next stage: `plan-review`.
- Conditional next stages: return to `spec` or `architecture` when planning exposes a blocking gap; proceed to `test-spec` only after plan-review when the workflow allows it.
- In a workflow-managed flow, successful `plan` completion hands off to `plan-review` when that review is next.
- Only a clean `plan-review` can satisfy that review gate in an automated `bounded-review-fix` run; this skill does not mark the run target reached and does not invoke `test-spec`.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Claims this skill must not make

Do not claim:

- code is implemented, review passed, verification passed, branch-ready, or PR-ready;
- the plan is Done because it is ready for the next stage;
- ready for PR or ready for final closeout without remaining gates and owning evidence;
- derived artifacts are current unless validation evidence proves it.

Use `Readiness is not Done` as the default interpretation for handoff lines. Keep Remaining completion gates visible whenever readiness could be confused with completion.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done.

## Plan authoring rules

- Derive work from spec requirements and architecture decisions.
- Do not add behavior not in the spec.
- Do not hide risky work in vague milestones.
- Do not omit validation commands.
- Keep `docs/plan.md` as stable navigation, not a lifecycle-state owner or second long-form plan body.
- In `docs/plan.md` and `docs/plan-archive.md`, write plan references as clickable Markdown links relative to the index file, for example `[Title](plans/YYYY-MM-DD-slug.md)`; do not leave bare `docs/plans/...` text as the index entry.
- Do not put mutable lifecycle state, current milestone state, review status, progress, routing, blockers, or final closeout state in the plan body or navigation index.
- Preserve plan revisions as changes to execution intent and send the revised artifact through `plan-review`; do not use plan edits as workflow-state updates.
- `implement`, reviews, `verify`, and `pr` treat the plan as read-only.
- `verify` challenges any mutable workflow state embedded in a governed plan.
- If completion depends on a true downstream completion event, keep the plan `Active` and name that event; merge itself is not that event.
- Do not create a plan that only the current chat context can understand.
- Do not proceed to implementation until `plan-review` and `test-spec` are ready unless an isolated manual invocation is requested and recorded.
- If planning reveals spec or architecture gaps, update those artifacts first.

## Milestone-aware plans

The plan defines ordered milestone IDs and stable intent.
`change.yaml` gives each implementation milestone exactly one current `Milestone state`: `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.

For a final `verify` automation target, record target selection separately from implementation and verification authorization; neither owns live next-stage state. Plans must keep ordered implementation milestones, approved validation commands, promotion evidence expectations, separate verification authority, and stop-before-PR boundaries explicit.

Use `review-requested` after implementation and validation. Use `resolution-needed` for review-resolution, fixes, owner decision, or re-review. `implementation-complete` and `review-clean` are evidence descriptions, not milestone state values.

Normal loop:

```text
implement M<n>
-> code-review M<n>
-> review-resolution M<n>, when triggered
-> implement fixes for M<n>, when needed
-> code-review M<n> rerun, when needed
-> close M<n>
-> implement M<n+1>, when another in-scope implementation milestone remains
```

Do not hand off to final closeout until all in-scope implementation milestones are `closed` or removed and required review-resolution is closed. Do not postpone milestones to make final closeout available.

Use `lifecycle-closeout` for a milestone or section that tracks only downstream gates such as `ci-maintenance`, `explain-change`, `verify`, PR handoff, release, deploy, or final plan closeout.

## Change-local handoff rules

The plan identifies its owning change record.
Current milestone, milestone state, last reviewed milestone, review status, remaining milestones, next stage, blockers, and final-closeout readiness live only in that record.
Plan and review stages write their scoped evidence; workflow consumes that evidence and owns routing updates.

## Stop conditions

Stop when source artifacts are missing or contradictory, lifecycle status is not approved enough, architecture/security/release boundaries are unclear, validation commands cannot be identified, a milestone would rely on chat-only context, or the plan would hide open work behind `Ready for final closeout`, Done, or PR readiness wording.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

Use this compact response shape; copy `assets/plan-skeleton.md` for the full plan artifact.

```md
Result

- Skill: plan
- Status: <created | updated | blocked>
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: <plan-review | test-spec after plan-review | blocked>
- Readiness: <ready for plan-review | blocked with reason>

Plan

- Plan file: <docs/plans/YYYY-MM-DD-slug.md>
- Plan navigation: <docs/plan.md updated | not-needed with rationale>
- Owning change record: <docs/changes/<change-id>/change.yaml>
- Remaining completion gates: <gates>
```
