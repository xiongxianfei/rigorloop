---
name: plan-review
description: >
  Review a concrete execution plan before implementation. Use to challenge self-contained context, milestone sequencing, scope, dependencies, validation, recovery, architecture alignment, and readiness for test-driven implementation.
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

Isolation governs handoff. Recording follows the finding. These are
independent.

A direct or review-only review request remains isolated by default: it
does not automatically continue into downstream workflow stages.
Isolation does not suppress recording.

A material finding requires a durable change-local review record under
`docs/changes/<change-id>/reviews/`. This applies regardless of whether
the review was workflow-managed or isolated.

The durable record must be created before review-driven edits begin. If
review-driven edits already began before the durable record exists, the
record is reconstructed and must disclose source, timing, available
evidence, stable Finding IDs, and known fidelity loss.

A tracked artifact is any version-controlled repository file whose
change will be committed or reviewed as part of the work. This includes
lifecycle artifacts, governance files, workflow summaries, skills,
specs, schemas, scripts, generated outputs, README content, and
change-local artifacts. Edits to ephemeral chat output, local scratch
files, or unversioned drafts are not tracked artifact edits.

The recording obligation is also a resolution-step gate. A revision
made in response to a material finding is incomplete until the finding
is durably recorded.

Materiality is governed by `CONSTITUTION.md` and is not redefined here.
A material finding requires evidence, required outcome, and a safe
resolution path or `needs-decision` rationale before it drives fixes.

Operational shortcut: if a finding changes or blocks a tracked artifact
edit, changes scope, changes requirements, changes architecture,
changes sequencing, changes validation, creates follow-up work, or
requires disposition, treat it as material unless the reviewer
explicitly records a non-material rationale.

Reconstructed records are governed by `specs/rigorloop-workflow.md`.

Clean reviews with no material findings remain lightweight and may
settle in the reviewed artifact when no detailed-record trigger
applies.

For an isolated review with material findings, final review output names
the isolated handoff status, material Finding IDs, required durable
review record path or reconstruction requirement, confirms
`review-resolution.md` is required, and states the next allowed action:
`create-change-local-record-before-fixing`,
`reconstruct-record-because-fixes-already-began`, or
`stop-for-owner-decision`. Downstream handoff remains stopped unless
explicitly requested.

## Detailed Review Records

Use these detailed review record triggers for formal lifecycle reviews:

- material findings
- stage-owned non-approval outcomes that block downstream progress or require revision
- reconstructed review evidence
- closeout evidence citation
- explicit reviewer or maintainer request

Examples of stage-owned non-approval outcomes include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent blocking stage-specific outcomes.

When a detailed review file is created, `review-log.md` indexes it. Material findings need stable `Finding ID` values and disposition in `review-resolution.md`.

In this contract, clean reviews can settle artifact-locally when no detailed review record triggers apply. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`. Likewise, artifact-local settlement must not replace detailed review records when a trigger applies.

Do not add a dedicated `pr-review` stage. It is an unsupported review stage unless a later approved spec extends the stage set. A material maintainer PR comment that needs disposition must first be promoted into a supported formal lifecycle review record with a stable `Finding ID`.

## Rules

- Do not rubber-stamp organized-looking plans.
- Do not review `docs/plan.md` as if it were the plan body.
- Do not accept vague milestones such as “update backend” or “wire UI.”
- Do not accept missing validation commands for risky work.
- Do not require implementation code before approving a plan.
- Do not edit the plan unless the user explicitly asks.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- verdict: approve, revise, or rethink;
- findings by review dimension;
- missing milestones or dependencies;
- exact suggested edits;
- explicit immediate-next-stage statement for `test-spec`;
- downstream implementation-readiness statement only when useful and clearly distinct from the immediate `test-spec` handoff.
