---
name: plan
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or revise a living execution plan after proposal, spec, and architecture are stable enough to implement. Use for multi-file, multi-component, risky, migration-heavy, or milestone-based work that needs reviewable implementation slices, validation commands, recovery paths, dependencies, and current handoff state. Use spec, test-spec, implement, code-review, verify, or pr for those stages; do not use plan to choose product direction, write code, review diffs, verify branch readiness, or open PRs.
argument-hint: [feature name, spec path, architecture path, or implementation goal]
---

# Living execution plan

Sequence approved behavior and architecture into reviewable implementation. Do not decide product direction.

## Purpose

Create or revise a concrete execution plan with milestones, validation commands, recovery paths, and lifecycle readiness.

## Workflow role

- role_name: plan
- stage: authoring
- upstream: accepted proposal, approved or reviewed spec, architecture records or ADRs when relevant, test-spec when already present, and project-local workflow evidence
- downstream: plan-review
- summary: Create or revise the execution plan artifact, milestone sequence, validation strategy, recovery path, current handoff summary, and lifecycle readiness.
- must_not_claim: implementation completion, review approval, verification, branch readiness, PR readiness, final closeout readiness, or Done while downstream gates remain.

## Project-local evidence

Public skills operate in customer-project mode by default.

Use project-local artifacts when present and relevant: `AGENTS.md`, `CONSTITUTION.md`, `docs/plan.md`, accepted proposals, approved specs, test specs, architecture records, ADRs, review findings, `docs/project-map.md`, `docs/workflows.md`, source files, tests, CI, and workflow files.

Do not require RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects. Use portable defaults where safe, and block on ambiguity.

## Resource map

- COPY `assets/plan-skeleton.md` when creating a new plan or replacing the full plan structure.
  Fill: sections and placeholders.
  Sections: Status; Purpose / big picture; Source artifacts; Context and orientation; Non-goals; Requirements covered; Current Handoff Summary; Milestones; Validation plan; Risks and recovery; Dependencies; Progress; Decision log; Surprises and discoveries; Validation notes; Outcome and retrospective; Readiness.
  Do not emit unfilled placeholders.
- COPY `assets/milestone.md` when adding each reviewable implementation milestone.
  Fill: ID, state, goal, requirements, files, tests, steps, validation, result, risks, rollback.
  Do not emit unfilled placeholders.
- COPY `assets/current-handoff-summary.md` when creating or updating the current handoff summary in a milestone-based plan.
  Fill: milestone, state, review status, remaining milestones, next stage, readiness, reason.
  Do not emit unfilled placeholders.
- COPY `assets/decision-log-row.md` when recording a material planning or sequencing decision.
  Fill: date, decision, reason, and rejected alternatives.
  Do not emit unfilled placeholders.

## When to use

Use after proposal, spec, and architecture are stable enough to sequence multi-file, risky, milestone-based, migration-heavy, or cross-component work.

## When not to use

Do not choose product direction, replace missing specs, implement code, claim review or verification outcomes, or mark work Done while downstream lifecycle gates remain.

## Inputs to read

Read needed project-local evidence: `AGENTS.md`, `CONSTITUTION.md` if present, `docs/plan.md`, accepted proposal, approved or reviewed spec, architecture or ADRs when relevant, test-spec if present, `docs/project-map.md`, code, tests, CI, and workflows.

Use bounded evidence first. Use broader-section or full-file reading when the target file is the artifact, relevant sections cannot be isolated safely, or surrounding context can change the plan.

## Upstream status settlement

Before relying on a spec, architecture package, or ADR in workflow-managed downstream execution, check tracked status against clear review evidence. Skip review-only, no-edit, and manual inspection requests.

During normal workflow-managed downstream execution, do not ask whether edits are allowed; the downstream invocation permits minimal settlement.

Settle only lifecycle/status/readiness/follow-on/closeout metadata. Do not rewrite substantive artifact content.

Evidence needs durable review evidence, an approving or clean outcome, no later contradictory review record, no open findings in `review-log.md` when present, closed `review-resolution.md` when required, and explicit mapping.

Mappings:

- spec-review approved with no unresolved material findings -> spec `Status: approved`;
- architecture-review approved for an architecture package with no unresolved material findings -> architecture `Status: approved`;
- architecture-review approved for an ADR with no unresolved material findings -> ADR status `accepted` or `active` only when the ADR lifecycle vocabulary clearly supports that target.

If evidence is missing, contradictory, unresolved, unknown, or unmapped, block instead of guessing. If the artifact type, lifecycle field, next status, or target status is unknown or unmapped, block instead of inferring a settlement. Report `## Upstream status settlement` when settlement was updated, blocked, or stale status was detected, with `Settlement result: updated | blocked | not-needed`, `New status`, `not-applicable`, and `Settlement blocker`. Name blocked settlement with a deterministic target, blocked settlement with no deterministic target, known target blocked by evidence/state, unknown target blocked by missing mapping or lifecycle vocabulary, and unknown lifecycle vocabulary.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order: explicit user path or change ID; active plan, change metadata, reviewed artifact path, or current artifact metadata; known governing spec or schema constraint when directly relevant; `docs/workflows.md` artifact-location table; this skill's portable default path; block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Expected output

Output a compact result plus a plan artifact. Copy `assets/plan-skeleton.md` for section order and other assets for repeated structures. Do not duplicate full layout here.

## Outputs

Produce or update the plan body and, when starting or replanning, the `docs/plan.md` lifecycle index. Name milestones, validation, recovery, current handoff summary, and Remaining completion gates.

## Result

- Skill: plan
- Status: <created | updated | blocked>
- Artifacts changed: <paths or none>
- Open blockers: <blockers or none>
- Next stage: <plan-review | test-spec after plan-review | blocked>

## Handoff

- Normal next stage: `plan-review`.
- Conditional next stages: return to `spec` or `architecture` when planning exposes a blocking gap; proceed to `test-spec` only after plan-review when the workflow allows it.
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
- Keep `docs/plan.md` as an index, not a second long-form plan body.
- Keep `docs/plan.md` bounded: Active and Blocked first, at most the recent completed window in `Done (recent)`, and older terminal history in `docs/plan-archive.md`.
- Use the plan body's explicit `## Status` lifecycle marker fields `Plan lifecycle state` and `Terminal disposition`; do not infer terminal state from prose.
- Update the plan index surfaces and the plan body together when starting, replacing, transitioning, archiving older terminal history, or before the PR opens for review.
- Keep superseded entries in `docs/plan.md` only while they include `superseded by:` and non-empty `active-context:`; move terminal superseded history without active context to `docs/plan-archive.md`.
- If completion depends on a true downstream completion event, keep the plan `Active` and name that event; merge itself is not that event.
- Do not create a plan that only the current chat context can understand.
- Do not proceed to implementation until `plan-review` and `test-spec` are ready unless an isolated manual invocation is requested and recorded.
- If planning reveals spec or architecture gaps, update those artifacts first.

## Milestone-aware plans

Each implementation milestone has exactly one `Milestone state`: `planned`, `implementing`, `review-requested`, `resolution-needed`, or `closed`.

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

The active plan `Readiness` section points to `Current Handoff Summary` for current live state. Do not duplicate the current next stage outside `Current Handoff Summary` unless the statement is explicitly historical.

## Current Handoff Summary rules

Update a current handoff summary whenever implementation or review changes milestone readiness. The active plan `Current Handoff Summary` owns current milestone, milestone state, last reviewed milestone, review status, remaining in-scope implementation milestones, next stage, final closeout readiness, and reason.

Keep it consistent with the active plan, `docs/plan.md`, and change metadata. It must not claim branch readiness, PR readiness, final verification, final closeout readiness, or Done while downstream gates remain.

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
- Plan index surfaces: <docs/plan.md updated | docs/plan-archive.md updated | not-needed with rationale>
- Current milestone: <milestone or not-started>
- Remaining completion gates: <gates>
```
