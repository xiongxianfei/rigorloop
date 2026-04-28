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

When workflow-managed review findings are recorded under `docs/changes/<change-id>/reviews/`, preserve the first-pass review record before fixes and record dispositions in `review-resolution.md`.

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
