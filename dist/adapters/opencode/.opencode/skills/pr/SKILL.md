---
name: pr
description: >
  Prepare a completed, verified change for pull request review. Use when the branch is ready or nearly ready and the agent should summarize the real diff, validation evidence, spec compliance, risks, and reviewer notes.
---

# Pull request preparation

You are preparing the change for human review.

The PR body should be grounded in the actual diff and verification evidence, not chat memory.

In this repository, `pr` is a submit/open stage when readiness passes. Do not treat it as draft-only preparation unless a blocker, tool limitation, or explicit user instruction prevents opening the PR.

## Purpose

Prepare and, when readiness passes, open a pull request grounded in the actual diff, verification evidence, lifecycle artifacts, risks, and reviewer needs.

## When to use

Use this skill after `verify` has established branch readiness, or when the user directly invokes `pr` and the branch is ready or nearly ready for review.

## When not to use

Do not use this skill to claim implementation, review, verification, tests, or CI passed without owning evidence; do not use it to bypass unresolved blockers or create PR text from memory.

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
6. for planned initiatives, lifecycle closeout is already reflected in both `docs/plan.md` and the plan body before the PR opens for review when final state is known; if completion depends on a true downstream completion event, the plan remains `Active` and names it; merge itself is not that event;
7. for ordinary non-trivial work, the required docs-changes artifacts exist, including `docs/changes/<change-id>/change.yaml` plus durable reasoning, defaulting to `docs/changes/<change-id>/explain-change.md` unless an approved equivalent surface applies;
8. material review findings are closed in `review-resolution.md`, with no `needs-decision` dispositions and no `review-log.md` open findings remaining;
8a. `Closeout status: open` blocks PR handoff, and `Closeout status: closed` requires final dispositions for all material findings;
8b. a stage-owned non-approval outcome that blocks downstream progress or requires revision has a same-stage later review round or explicit reviewer or owner closeout naming the original Review ID; `review-resolution.md` alone is not a silent substitute;
8c. for no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`;
9. artifacts are updated;
10. no secrets, credentials, local paths, or debug-only changes are included;
11. generated files and migrations are intentional;
12. reviewers have enough context.

Apply the same readiness checks for workflow-managed and direct-`pr` invocation. Direct `pr` remains isolated only in the sense that no downstream stage follows `pr`; it still opens the PR when readiness passes.

`verify` owns `branch-ready`. This stage owns `pr-body-ready` and `pr-open-ready`.

## Outputs

Produce a PR readiness check, title, body, reviewer notes, risks, follow-ups, and the opened PR URL when the repository/tooling permits opening the PR.

## Handoff

- Normal next stage: open the PR when `branch-ready`, `pr-body-ready`, and `pr-open-ready` pass.
- Conditional next stages: return to `verify`, `explain-change`, review-resolution, implementation, or artifact updates when readiness blockers remain; stop when tooling or permissions prevent opening.
- For full stage order and downstream-blocking semantics, route through the `workflow` skill.

## Claims this skill must not make

Do not claim:

- implementation passed, review passed, verification passed, or tests passed unless the statement links to owning evidence;
- CI passed unless the hosted or local CI evidence was actually observed and named;
- branch-ready without citing `verify` evidence;
- derived artifacts are current unless validation evidence proves it.

Use owning evidence when summarizing implementation passed, review passed, verification passed, or tests passed.

## Progress, readiness, closeout, and Done

- Progress means work that has happened so far.
- Readiness means the next stage that can happen.
- Closeout means the current artifact or stage satisfied its checklist.
- Done means final lifecycle state after required gates are complete.
- Readiness is not Done. PR body/open readiness is not proof that earlier stages passed unless linked to evidence.

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
- Keep PR review-resolution details to counts by disposition from the scan-first summary or overview and a link to `review-resolution.md`; do not duplicate every detailed finding and suggestion.
- Do not defer blocked or superseded lifecycle closeout until PR, merge, or retrospective work.
- Do not summarize from memory when a diff is available.
- Do not bury known risks.
- Do not include massive internal detail that obscures review.
- Do not stop at a chat-only readiness summary when the user asked for `pr`; if `branch-ready`, `pr-body-ready`, and `pr-open-ready` checks pass, open it unless a blocker or tool limitation prevents that action.

## Stop conditions

Stop before opening or claiming a PR when:

- `verify` has not established branch readiness;
- required review-resolution, lifecycle closeout, derived-artifact refresh, validation, CI, or docs-change evidence is missing or failing;
- the working tree or commits include unrelated or unreviewed changes;
- the PR body would need to cite evidence that does not exist;
- tooling, permissions, remote state, or explicit user instructions prevent opening.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, derived artifacts, or validation output.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Skill: pr
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
- Readiness:
```

Then include:

- readiness check results;
- PR title;
- PR body;
- opened PR URL or blockers if not ready;
- explicit validation and CI status;
- recommended reviewers or review focus when useful.
