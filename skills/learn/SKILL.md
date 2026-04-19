---
name: learn
description: >
  Capture durable lessons after implementation, review, verification, or incidents. Use when the workflow revealed recurring mistakes, spec gaps, architecture discoveries, testing improvements, CI gaps, or process changes that should guide future agents.
argument-hint: [feature name, completed plan, incident, review findings, or retrospective]
---

# Learning and retrospective capture

You are preserving useful lessons so future work improves.

Do not fabricate lessons. Capture what was actually learned from evidence.

## Inputs to read

Read, if present:

- completed plan and validation notes;
- explain-change artifact;
- PR summary;
- code-review and verify findings;
- incident or bugfix notes;
- relevant spec and test spec;
- architecture docs and ADRs;
- `AGENTS.md`, `.codex/CONSTITUTION.md`, and `docs/workflows.md`;
- CI failures or flaky test evidence.

## Where lessons go

Choose the narrowest durable home:

- **Feature-specific behavior** → feature spec.
- **Feature-specific testing** → feature test spec.
- **Design decision** → architecture doc or ADR.
- **Implementation convention** → `AGENTS.md` or constitution.
- **Workflow/handoff lesson** → `docs/workflows.md`.
- **Architecture orientation** → `docs/project-map.md`.
- **Plan outcome** → completed plan’s outcome/retrospective section.
- **General retrospective** → `docs/retrospectives/YYYY-MM-DD-slug.md`.

## Retrospective sections

For a completed feature, include:

1. **What changed**.
2. **What went well**.
3. **What was harder than expected**.
4. **Spec accuracy**: where the spec helped or missed reality.
5. **Test effectiveness**: which tests caught problems or were missing.
6. **Architecture accuracy**: where design matched or drifted.
7. **Process issues**: sequencing, handoff, context, review, CI.
8. **Durable updates made**.
9. **Follow-up actions** with owners or artifact paths.

## Rules

- Do not rewrite history; add a clear note.
- Do not put project-wide rules into a feature-only artifact.
- Do not turn one-off trivia into policy.
- Do not blame; describe conditions and fixes.
- Do not leave verified workflow changes undocumented.
- If nothing durable was learned, say so and make no edits.

## Expected output

- documents updated;
- lessons captured;
- follow-up actions;
- what future agents should do differently;
- confirmation if no durable lesson existed.
