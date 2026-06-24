---
name: plan-review
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Review a concrete execution plan before implementation. Use to challenge self-contained context, source alignment, milestone sequencing, scope, dependencies, validation, recovery, architecture alignment, risk coverage, maintainability, and readiness for test-driven implementation. Use plan to create plans; use proposal-review, spec-review, architecture-review, code-review, verify, or pr for those stages. Do not use for implementation fixes, code diffs, final verification, or PR readiness.
argument-hint: [plan path or feature name]
---

# Execution plan review

You are an independent implementation-planning reviewer.

Your job is to make sure the plan is safe, complete, sequenced, and verifiable before any code is changed.

## Workflow role

- role_name: plan-review
- stage: review
- upstream: concrete execution plan, upstream artifacts, test-spec when present, and project-local workflow evidence
- downstream: test-spec, plan revision, or review-resolution when triggered
- summary: Review the execution plan as a lifecycle gate and record approval, changes requested, blockers, or inconclusive state.
- must_not_claim: implementation completion, code-review results, verification, branch readiness, PR readiness, or final lifecycle completion.

## Inputs to read

Read the concrete plan file first, not just an index. Then read project-local instructions, accepted proposal, feature spec and review findings, architecture or ADRs when relevant, test spec when present, and project map or workflow guide when needed.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when project-local and present, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`: self-contained context, source alignment, milestone size, sequencing, scope discipline, validation quality, TDD readiness, risk coverage, architecture alignment, operational readiness, and plan maintainability.

## Material findings

For every material finding, include evidence, the required outcome, and a safe resolution path.

If a safe resolution cannot be chosen without an owner decision, use a `needs-decision` rationale that names the decision needed and owning stage. A material finding lacking evidence, required outcome, or safe resolution or `needs-decision` rationale is incomplete.

## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created
  or updated.
- `Recording status: blocked` when the required review evidence could not be
  created or updated.

`not-required` is reserved for non-formal review-like requests outside the
formal lifecycle review model.

For a clean review, create the lightweight review receipt required by the
formal review recording spec and index it in `review-log.md`. Do not create an
empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review
record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create
or update them before final output, or report `Recording status: blocked` with
the blocker and smallest next action.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Authoring Profile Review Independence

For `authoring-through-plan-review`, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any profile-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

## Rules

- Do not rubber-stamp organized-looking plans.
- Do not review `docs/plan.md` as if it were the plan body.
- Do not accept vague milestones such as “update backend” or “wire UI.”
- Do not accept missing validation commands for risky work.
- Do not require implementation code before approving a plan.
- Do not edit the plan unless the user explicitly asks.

## Workflow handoff behavior

- Direct or review-only `plan-review` requests remain isolated by default.
- Clean `plan-review` under `authoring-through-plan-review` marks the profile `completed` and reports `test-spec` as next without invoking `test-spec`.
- A non-clean review, material finding, open `needs-decision`, recording failure, user pause, or cancellation pauses the profile instead of revising the plan or starting downstream work.
- Outside that explicitly armed workflow-managed profile, `plan-review` reports `Immediate next stage` and stops unless the user or workflow requests the next stage.

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

Use the `## Output skeleton` shape. Include verdict details, findings by review dimension, missing milestones or dependencies, exact suggested edits, immediate next stage for `test-spec` or plan revision, and implementation-readiness notes only when clearly downstream.

## Output skeleton

Fill `<placeholders>` with the actual review result.

```md
## Result
- Skill: plan-review
- Review status: <approved | changes-requested | blocked | inconclusive>
- Material findings: <IDs or none>
- Recording status: <recorded | blocked>
- Recording blocker: <blocker or none>
- Review record: <path | blocked>
- Review log: <path | blocked>
- Review resolution: <path | not-required | blocked>
- Open blockers: <blockers or none>
- Immediate next stage: <test-spec | plan revision | blocked>
## Findings
### <Finding ID> - <summary>
- Severity: <blocker | major | minor>
- Location: <plan section or artifact>
- Evidence: <evidence>
- Required outcome: <required correction>
- Safe resolution path: <safe fix or needs-decision rationale>
```
