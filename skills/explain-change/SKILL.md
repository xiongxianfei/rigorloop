---
name: explain-change
description: >
  Explain why the agent made each meaningful change by linking the actual diff to the problem, proposal, requirements, architecture decisions, plan milestones, tests, review outcomes, and available validation evidence. Use after implementation and review-resolution, before final verify and PR, or whenever the user asks why code changed.
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
- code-review findings and prior verification evidence when it exists;
- `review-resolution.md` when material review findings exist;
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

For isolated manual skill invocations that are not used to claim complete workflow delivery, inline explanation in the final response or PR body may be enough when the governing workflow contract allows it.

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
6. **Validation evidence available before final verify**:
   - commands run;
   - CI status if known;
   - manual checks.
7. **Review resolution summary** when material findings exist:
   - concise counts by disposition;
   - link to `review-resolution.md`;
   - do not duplicate transcript details from review records.
8. **Alternatives rejected**: what was not done and why.
9. **Scope control**: non-goals preserved.
10. **Risks and follow-ups**.

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
- Do not claim final `verify`, `branch-ready`, `pr-body-ready`, `pr-open-ready`, or hosted CI-final status before the owning stage has produced that evidence.
- Explain-change is scoped evidence and must not own the active plan's current next stage.
- Use the active plan `Current Handoff Summary` when summarizing current planned-initiative state.
- Material finding closeout must not proceed at `Closeout status: open`; `Closeout status: closed` requires final dispositions, no `needs-decision`, and no stale `review-log.md` open findings.
- A stage-owned non-approval outcome that blocks downstream progress or requires revision needs a same-stage later review round or explicit reviewer or owner closeout naming the original Review ID; `review-resolution.md` alone is not a silent substitute.
- For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.
- Do not proceed when `review-resolution.md` is missing, open, still contains `needs-decision`, or `review-log.md` still lists open findings for material findings that must close before handoff.
- Do not duplicate transcript content from detailed reviews; summarize review-resolution counts from the scan-first summary or overview and link the durable artifact.
- Do not invent alternatives that were never considered; mark them as hindsight if added.
- Keep explanations readable for a human reviewer.
- For planned initiatives, do not claim PR readiness unless lifecycle state made true by this PR is recorded before the PR opens for review. If completion depends on a true downstream completion event, say why the plan remains `Active`; merge itself is not that event.

## Workflow handoff behavior

- In a workflow-managed standard workflow, successful `explain-change` completion hands off to `verify` unless a stop condition applies.
- Direct `explain-change` requests remain isolated by default unless the user explicitly asks to continue beyond the explanation.
- If explanation work surfaces a validation gap, stale artifact, or other blocker, stop and report it instead of implying the change is ready for `verify` or `pr`.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- explanation artifact path or inline explanation;
- trace from problem to diff;
- file-by-file rationale;
- tests and available validation evidence;
- alternatives rejected;
- remaining risks;
- readiness statement for `verify` or blocker state.
