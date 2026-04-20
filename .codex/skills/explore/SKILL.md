---
name: explore
description: >
  Expand and challenge an idea before proposal, specification, or planning. Use at the early ideation stage when the problem, user value, scope, architecture direction, or product strategy is not settled.
argument-hint: [idea, feature request, product goal, bug theme, or vague project direction]
---

# Exploration and option generation

You are the divergence engine. Your job is to make the idea better before the team commits to a direction.

Do not write an execution plan. Do not implement. Do not freeze requirements. Explore first.

## Goals

- Understand the real problem behind the request.
- Generate multiple plausible solution directions.
- Challenge assumptions and weak framing.
- Identify risks, unknowns, and decision criteria.
- Produce a discussion artifact that helps humans debate tradeoffs.

## Inputs to read

Read, if present:

- `AGENTS.md`
- `CONSTITUTION.md`
- `docs/project-map.md`
- related specs
- related architecture docs or ADRs
- related plans or proposals
- product docs, issues, support notes, incidents, or user feedback

If context is missing, still proceed with explicit assumptions.

## Output path

Prefer:

```text
docs/proposals/YYYY-MM-DD-slug.explore.md
```

If the repo prefers one proposal file, place exploration as a section in the later proposal.

## Process

1. Restate the problem in one paragraph.
2. Identify stakeholders and affected user journeys.
3. Separate facts, assumptions, and unknowns.
4. Generate at least five options:
   - `O0`: do nothing or defer;
   - `O1`: minimal safe change;
   - `O2`: incremental product improvement;
   - `O3`: architectural or platform-oriented option;
   - `O4`: high-risk/high-upside option.
5. For each option, describe:
   - core idea;
   - user value;
   - implementation complexity;
   - architecture impact;
   - testing burden;
   - rollout and rollback implications;
   - risks;
   - what would make the option wrong.
6. Compare options against decision criteria.
7. Recommend one option or a staged sequence.
8. List research questions that must be answered before proposal or spec.

## Debate prompts

Use these prompts to strengthen ideation:

- What problem would remain unsolved after this change?
- What is the smallest thing that proves value?
- What would a skeptical engineer object to?
- What would a skeptical user object to?
- What would fail at 10x scale?
- What would make support, operations, or QA harder?
- What are we assuming because it is convenient?
- What behavior should explicitly remain unchanged?

## Rules

- Do not collapse to one idea too early.
- Include at least one option you do not recommend.
- Include a “do nothing” option honestly.
- Do not hide risks under vague words like “complexity.”
- Do not choose architecture without showing alternatives.
- Do not produce requirements with `MUST` language yet; save that for `spec`.

## Expected output

- exploration artifact path or inline exploration report;
- options table with tradeoffs;
- assumptions and unknowns;
- recommendation and why;
- research questions;
- readiness statement for `research` or `proposal`.
