---
name: explain-change
description: >
  Explain why the agent made each meaningful change by linking the actual diff to the problem, proposal, requirements, architecture decisions, plan milestones, tests, and verification evidence. Use after implementation and verification, before PR, or whenever the user asks why code changed.
argument-hint: [branch, diff, feature name, plan path, or question]
---

# Change rationale explanation

You are making the implementation understandable.

This skill exists because users should never have to reverse-engineer why an agent changed code.

## Inputs to read

Read:

- actual diff or changed files;
- proposal;
- feature spec;
- test spec;
- architecture doc and ADRs;
- concrete plan and validation notes;
- code-review and verify findings;
- test and CI output;
- `AGENTS.md` and `CONSTITUTION.md` if relevant.

## Output path

Prefer:

```text
docs/changes/<change-id>/explain-change.md
```

For new ordinary non-trivial work, use `docs/changes/<change-id>/explain-change.md` unless an approved equivalent durable reasoning surface already applies under the workflow contract.

Use:

```text
docs/explain/YYYY-MM-DD-slug.md
```

only when the governing workflow contract explicitly allows that top-level explain artifact class for the change.

For small fast-lane or otherwise exempt changes, inline explanation in the final response or PR body is enough.

## Required sections

1. **Summary**: what changed and why.
2. **Problem**: original issue or goal.
3. **Decision trail**:
   - exploration option selected;
   - proposal decision;
   - requirement IDs;
   - architecture/ADR decisions;
   - plan milestones.
4. **Diff rationale by area**:
   - files changed;
   - why each file changed;
   - which requirement/test/design decision it supports.
5. **Tests added or changed**:
   - test IDs;
   - what each test proves;
   - why the test level is appropriate.
6. **Verification evidence**:
   - commands run;
   - CI status if known;
   - manual checks.
7. **Alternatives rejected**: what was not done and why.
8. **Scope control**: non-goals preserved.
9. **Risks and follow-ups**.

## File rationale format

Use a table when useful:

```text
File | Change | Reason | Source artifact | Test/evidence
```

## Rules

- Explain from the actual diff, not memory.
- For ordinary non-trivial work, do not treat PR text alone as the durable reasoning surface.
- For new ordinary non-trivial work, do not default to a new top-level `docs/explain/` artifact when `docs/changes/<change-id>/explain-change.md` should exist.
- Do not justify unrelated changes; flag them.
- Do not claim a requirement drove a change unless the link is real.
- Do not hide validation gaps.
- Do not invent alternatives that were never considered; mark them as hindsight if added.
- Keep explanations readable for a human reviewer.

## Workflow handoff behavior

- In a workflow-managed full-feature flow, successful `explain-change` completion hands off to `pr` unless a stop condition applies.
- Direct `explain-change` requests remain isolated by default unless the user explicitly asks to continue beyond the explanation.
- If explanation work surfaces a validation gap, stale artifact, or other blocker, stop and report it instead of implying the change is ready for `pr`.

## Expected output

- explanation artifact path or inline explanation;
- trace from problem to diff;
- file-by-file rationale;
- tests and verification evidence;
- alternatives rejected;
- remaining risks;
- PR handoff summary bullets plus a readiness statement for `pr` or blocker state.
