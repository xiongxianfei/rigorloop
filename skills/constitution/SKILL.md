---
name: constitution
description: >
  Create or update the repository's governing AI-development principles. Use when starting a project, adopting this skill pack, onboarding a brownfield codebase, or when recurring mistakes show that project rules are unclear.
argument-hint: [project purpose, repo conventions, quality bar, or change request]
---

# Project constitution

You are defining the durable rules that every agentic workflow must follow.

The constitution is the highest-level project context. It should be concise, enforceable, and stable. It is not a feature plan.

## Goals

Create or update project governance so future work has clear answers for:

- what quality means;
- what must be specified before implementation;
- what testing discipline is required;
- which architecture boundaries matter;
- how changes are reviewed and verified;
- what documentation must stay current;
- what the agent must never do silently.

## Inputs to read

Read, if present:

- `AGENTS.md`
- `.codex/CONSTITUTION.md`
- `README.md`
- `CONTRIBUTING.md`
- `docs/workflows.md`
- `docs/project-map.md`
- existing specs under `specs/`
- CI workflows under `.github/workflows/`
- package, build, and test config files

If key files are absent, infer carefully from the repo and document assumptions.

## Artifact choices

Prefer this structure:

```text
AGENTS.md                  # concise agent-facing operating rules
.codex/CONSTITUTION.md     # detailed governance and lifecycle rules
```

If the repo already uses only `AGENTS.md`, update it without adding another file unless more detail is needed.

## Required constitution sections

Include these sections unless the repo already has equivalent guidance:

1. **Project purpose**: what this repo is for and who it serves.
2. **Source of truth order**: constitution, specs, architecture, plans, tests, code, chat.
3. **Spec-driven rules**: when specs are required and how requirements are identified.
4. **Test-driven rules**: tests first, regression tests for bugs, no unverifiable claims.
5. **Architecture rules**: boundaries, dependencies, data ownership, migration discipline.
6. **Security and privacy rules**: secrets, logging, user data, dependency risk.
7. **Compatibility rules**: API, schema, config, migration, versioning, deprecation.
8. **Verification rules**: local commands, CI expectations, evidence needed before completion.
9. **Review rules**: when to run proposal/spec/architecture/plan/code review.
10. **Documentation rules**: which changes update specs, architecture docs, workflows, or learnings.
11. **Agent behavior rules**: no silent assumptions, no unrelated refactors, no fake CI claims.
12. **Fast-lane exceptions**: what small changes can skip the full lifecycle and what they still require.

## Normative language

Use precise terms:

- `MUST` for non-negotiable rules.
- `SHOULD` for strong defaults with documented exceptions.
- `MAY` for optional practices.
- `MUST NOT` for forbidden behavior.

Avoid vague advice such as “write good tests” unless accompanied by concrete criteria.

## Process

1. Identify current explicit rules and implicit conventions.
2. Identify gaps that caused or could cause poor agent decisions.
3. Draft or update the constitution with concise, enforceable rules.
4. Add examples only when they clarify a rule.
5. Cross-link to workflow and artifact locations.
6. Keep project-specific rules separate from temporary feature details.
7. If a rule conflicts with existing practice, call out the conflict and recommend a resolution.

## Gotchas

- Do not turn the constitution into a giant tutorial.
- Do not encode one-off implementation details as universal rules.
- Do not duplicate a detailed architecture document; link to it.
- Do not create rules that cannot be checked in review.
- Do not silently remove existing governance.

## Expected output

- files created or updated;
- a short list of new or changed rules;
- unresolved governance questions;
- recommended next skill, usually `project-map`, `explore`, or `workflow`.
