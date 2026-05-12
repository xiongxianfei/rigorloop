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

Every supported formal lifecycle review invocation requires durable review
recording.

Every material finding requires a durable change-local review record
under:

`docs/changes/<change-id>/reviews/<stage>-r<n>.md`

The review record must be indexed in `review-log.md` and resolved in
`review-resolution.md`.

Create the durable record before fixing.

A material finding must include:

- evidence
- required outcome
- safe resolution path, or `needs-decision` rationale

Every material finding must also preserve complete finding shape:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Use the formal review recording change-ID selection rule. If no change ID can
be selected, report `Recording status: blocked` and state the smallest action
needed.

Clean formal reviews use lightweight review receipts. Material findings use
detailed review records.

### Recording status output

`Recording status` is separate from the review verdict.

For supported formal lifecycle review invocations, use exactly one:

- `recorded`: required review-recording artifacts were created or updated.
- `blocked`: required review-recording artifacts could not be created or updated.

`not-required` is reserved for non-formal review-like requests outside the
formal lifecycle review model.

For material findings, `recorded` requires a detailed review record,
`review-log.md`, and `review-resolution.md`.

For clean formal reviews, `recorded` requires a lightweight review receipt and
`review-log.md`.

For no-material detailed-record triggers, `recorded` requires a detailed review
record and `review-log.md`. Do not require an empty `review-resolution.md` for a
no-material review event.

Formal review output must include `Recording status`, `Recording blocker`,
`Review record`, `Review log`, and `Review resolution` (`path`,
`not-required`, or `blocked`).

If `Recording status: blocked`, include `Recording blocker` and the smallest
action needed.

Do not merely tell the user that review artifacts should be created. Create
or update them before final output, or report `Recording status: blocked`.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Detailed Review Records

Use these detailed review record triggers for formal lifecycle reviews:

- material findings
- stage-owned non-approval outcomes that block downstream progress or require revision
- reconstructed review evidence
- closeout evidence citation
- explicit reviewer or maintainer request

Examples of stage-owned non-approval outcomes include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent blocking stage-specific outcomes.

When a detailed review file is created, `review-log.md` indexes it. Material findings need stable `Finding ID` values and disposition in `review-resolution.md`.

In this contract, clean formal reviews use lightweight review receipts. A clean review receipt proves the review happened and does not by itself settle the reviewed artifact's lifecycle status. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`. Likewise, artifact-local settlement must not replace detailed review records when a trigger applies.

Do not add a dedicated `pr-review` stage. It is an unsupported review stage unless a later approved spec extends the stage set. A material maintainer PR comment that needs disposition must first be promoted into a supported formal lifecycle review record with a stable `Finding ID`.

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
