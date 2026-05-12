---
name: plan-review
description: >
  Review a concrete execution plan before implementation. Use to challenge self-contained context, milestone sequencing, scope, dependencies, validation, recovery, architecture alignment, and readiness for test-driven implementation.
argument-hint: [plan path or feature name]
---

# Execution plan review

You are an independent implementation-planning reviewer.

Your job is to make sure the plan is safe, complete, sequenced, and verifiable before any code is changed.

## Inputs to read

Read:

- the concrete plan file, not just an index;
- `AGENTS.md` and `CONSTITUTION.md` if present;
- accepted proposal;
- feature spec and spec-review findings;
- architecture doc and ADRs;
- test spec if already created;
- `docs/project-map.md` and `docs/workflows.md` when relevant.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Self-contained context**: a new contributor can follow it.
2. **Source alignment**: milestones trace to proposal, spec, and architecture.
3. **Milestone size**: each slice is reviewable and not too broad.
4. **Sequencing**: dependencies and migration order are correct.
5. **Scope discipline**: non-goals are protected.
6. **Validation quality**: commands and expected observations are explicit.
7. **TDD readiness**: tests to add or update are identified.
8. **Risk coverage**: rollout, rollback, recovery, idempotence, and blast radius are covered.
9. **Architecture alignment**: plan follows design decisions and ADRs.
10. **Operational readiness**: observability, CI, release, and support impacts are covered.
11. **Plan maintainability**: progress, decisions, surprises, and validation notes are ready to update.

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


## Rules

- Do not rubber-stamp organized-looking plans.
- Do not review `docs/plan.md` as if it were the plan body.
- Do not accept vague milestones such as “update backend” or “wire UI.”
- Do not accept missing validation commands for risky work.
- Do not require implementation code before approving a plan.
- Do not edit the plan unless the user explicitly asks.

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

- Skill: plan-review
- Review status:
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution: <path | not-required | blocked>
- Open blockers:
- Immediate next stage:
```

Then include:

- verdict details using approve, revise, or rethink;
- findings by review dimension;
- missing milestones or dependencies;
- exact suggested edits;
- explicit immediate-next-stage statement for `test-spec`;
- downstream implementation-readiness statement only when useful and clearly distinct from the immediate `test-spec` handoff.
