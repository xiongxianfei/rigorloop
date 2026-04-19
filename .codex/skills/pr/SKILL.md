---
name: pr
description: >
  Prepare a completed, verified change for pull request review. Use when the branch is ready or nearly ready and the agent should summarize the real diff, validation evidence, spec compliance, risks, and reviewer notes.
argument-hint: [branch, feature name, plan path, or PR request]
---

# Pull request preparation

You are preparing the change for human review.

The PR body should be grounded in the actual diff and verification evidence, not chat memory.

## Inputs to read

Read:

- actual diff and git status;
- proposal;
- feature spec;
- test spec;
- architecture doc and ADRs when relevant;
- concrete plan and validation notes;
- explain-change artifact if present;
- verification report;
- CI status when available;
- `AGENTS.md` and `.codex/CONSTITUTION.md` if relevant.

## Readiness checks

Before drafting or opening a PR, check:

1. working tree status;
2. branch and base branch;
3. commits are present and scoped;
4. tests and validation commands passed or gaps are documented;
5. CI status is known when available;
6. artifacts are updated;
7. no secrets, credentials, local paths, or debug-only changes are included;
8. generated files and migrations are intentional;
9. reviewers have enough context.

## PR body structure

Use this template:

```markdown
## Summary
- ...

## Why
- ...

## Spec / plan / architecture
- Proposal: ...
- Spec: ...
- Test spec: ...
- Architecture / ADRs: ...
- Plan: ...

## What changed
- ...

## Tests and verification
- [x] `command` — result
- [ ] CI — pending / not available / passed

## Requirement coverage
- R1 → T1, T2 → files/evidence
- R2 → T3 → files/evidence

## Risks and rollback
- ...

## Reviewer notes
- ...

## Follow-ups
- ...
```

## Title guidance

Use a concise title:

```text
<type>: <user-visible outcome>
```

Examples:

- `feat: add resumable import validation`
- `fix: preserve filters after dashboard refresh`
- `refactor: isolate billing provider adapter`

## Rules

- Do not open or claim to open a PR unless the tool/action actually did it.
- Do not say CI passed unless it passed.
- Do not omit failed or unrun validation.
- Do not summarize from memory when a diff is available.
- Do not bury known risks.
- Do not include massive internal detail that obscures review.

## Expected output

- readiness check results;
- PR title;
- PR body;
- blockers if not ready;
- explicit validation and CI status;
- recommended reviewers or review focus when useful.
