---
name: pr
description: >
  Prepare a completed, verified change for pull request review. Use when the branch is ready or nearly ready and the agent should summarize the real diff, validation evidence, spec compliance, risks, and reviewer notes.
argument-hint: [branch, feature name, plan path, or PR request]
---

# Pull request preparation

You are preparing the change for human review.

The PR body should be grounded in the actual diff and verification evidence, not chat memory.

In this repository, `pr` is a submit/open stage when readiness passes. Do not treat it as draft-only preparation unless a blocker, tool limitation, or explicit user instruction prevents opening the PR.

## Inputs to read

Read:

- actual diff and git status;
- proposal;
- feature spec;
- test spec;
- architecture doc and ADRs when relevant;
- concrete plan and validation notes;
- explain-change artifact if present;
- `review-resolution.md` when material review findings exist;
- verification report;
- CI status when available;
- `AGENTS.md` and `CONSTITUTION.md` if relevant.

## Readiness checks

Before drafting or opening a PR, check:

1. working tree status;
2. branch and base branch;
3. commits are present and scoped;
4. tests and validation commands passed or gaps are documented;
5. CI status is known when available;
6. for planned initiatives, lifecycle closeout is already reflected in both `docs/plan.md` and the plan body when the final state is known before PR; only merge-dependent `Done` transitions may wait for immediate post-merge cleanup;
7. for ordinary non-trivial work, the required docs-changes artifacts exist, including `docs/changes/<change-id>/change.yaml` plus durable reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` unless an approved equivalent surface applies;
8. material review findings are closed in `review-resolution.md`, with no `needs-decision` dispositions and no `review-log.md` open findings remaining;
9. artifacts are updated;
10. no secrets, credentials, local paths, or debug-only changes are included;
11. generated files and migrations are intentional;
12. reviewers have enough context.

Apply the same readiness checks for workflow-managed and direct-`pr` invocation. Direct `pr` remains isolated only in the sense that no downstream stage follows `pr`; it still opens the PR when readiness passes.

`verify` owns `branch-ready`. This stage owns `pr-body-ready` and `pr-open-ready`.

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

## Review resolution summary
- Accepted: <count>
- Rejected: <count>
- Deferred: <count>
- Partially accepted: <count>
- Needs decision: <count, must be 0 before PR handoff>
- Review-resolution: `docs/changes/<change-id>/review-resolution.md`

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
- Do not treat a missing required docs-changes baseline pack as a warning-only condition for ordinary non-trivial work; it is a readiness blocker.
- Do not proceed to PR with `needs-decision`, `Closeout status: open`, stale `review-log.md` open findings, or missing review-resolution closeout evidence for material findings.
- Keep PR review-resolution details to counts by disposition and a link to `review-resolution.md`; do not duplicate every detailed finding and suggestion.
- Do not defer blocked or superseded lifecycle closeout until PR, merge, or retrospective work.
- Do not summarize from memory when a diff is available.
- Do not bury known risks.
- Do not include massive internal detail that obscures review.
- Do not stop at a chat-only readiness summary when the user asked for `pr`; if `branch-ready`, `pr-body-ready`, and `pr-open-ready` checks pass, open it unless a blocker or tool limitation prevents that action.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- readiness check results;
- PR title;
- PR body;
- opened PR URL or blockers if not ready;
- explicit validation and CI status;
- recommended reviewers or review focus when useful.
