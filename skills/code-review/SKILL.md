---
name: code-review
description: >
  Perform an independent implementation review against the spec, architecture, plan, test spec, actual diff, and validation evidence. Use after implementation or before PR readiness decisions.
argument-hint: [branch, diff, plan path, spec path, or feature name]
---

# Independent implementation review

You are reviewing with fresh eyes.

Your job is to determine whether the implementation satisfies the approved contract safely, not whether it merely looks plausible.

## Inputs to read

Read:

- actual diff or changed files;
- feature spec;
- test spec;
- concrete plan;
- architecture doc and ADRs when relevant;
- plan validation notes;
- test and CI results;
- `AGENTS.md` and `CONSTITUTION.md`;
- related code paths and tests when needed.

Prefer a fresh session or intentionally reset assumptions.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Requirement compliance**: every relevant `MUST` is satisfied.
2. **Non-goal protection**: diff does not add excluded behavior.
3. **Architecture alignment**: implementation follows design decisions and boundaries.
4. **Test quality**: tests assert behavior, not implementation trivia.
5. **Coverage completeness**: requirements, examples, edge cases, and regressions are covered.
6. **Error handling**: failures, invalid input, permissions, and partial states are handled.
7. **Security/privacy**: no secrets, leaks, auth bypass, injection, unsafe logging, or exposure.
8. **Compatibility/migration**: old data/clients/configs are handled as specified.
9. **Performance/scalability**: no obvious avoidable bottleneck or unbounded work.
10. **Simplicity/maintainability**: implementation is no more complex than needed.
11. **Observability**: required logs, metrics, traces, or audit events are present.
12. **Validation evidence**: claimed commands/results are present and credible.
13. **Artifact updates**: specs, plans, architecture docs, and learnings are updated when reality changed.

## Severity

Use:

- `blocker`: unsafe to merge or violates a `MUST`.
- `major`: should be fixed before PR approval.
- `minor`: improvement that does not block.
- `nit`: optional style/readability suggestion.
- `positive`: good pattern worth keeping.

## Rules

- Do not confuse passing tests with compliance.
- Do not spot-check only a few requirements.
- Do not review from memory; use the actual diff.
- Do not request broad rewrites when a targeted fix is enough.
- Do not skip positive notes for good patterns.
- Do not approve if verification evidence is missing for critical behavior.

## Workflow handoff behavior

- In a workflow-managed full-feature flow, a satisfied `code-review` hands off to `verify` unless a stop condition applies.
- If findings can be resolved without a new user decision and are accepted for action, enter the `review-resolution` loop, address them, and rerun `code-review` before any downstream handoff.
- If findings require a design, scope, or spec decision, stop and report that blocker instead of auto-looping.
- Direct `code-review` requests remain isolated by default unless the user explicitly asks to continue beyond the review result.

## Expected output

- verdict: approve, request changes, or block;
- requirement-by-requirement compliance summary when useful;
- issues by severity with exact file/path references;
- test coverage findings;
- validation evidence assessment;
- positive notes;
- readiness statement for `verify`, `review-resolution`, isolated stop, or blocker state.
