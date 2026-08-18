---
name: explain-change
description: >
  Trace meaningful changes from the actual diff to decisions, requirements, tests, reviews, and validation. Use after implementation or for a change-rationale question.
argument-hint: [branch, diff, change ID, artifact path, or question]
---

# Change rationale explanation

## Purpose

Explain the implementation without overstating evidence or owning another stage.

## When to use

Use after review closeout or for a direct rationale request. Direct requests remain isolated.

## Inputs and evidence

Resolve the actual diff first. Read the smallest decision-bearing proposal, spec, test spec, design, plan, review, tests, and validation evidence. Distinguish observed, inferred, and unknown facts. Flag unrelated changes, non-goals, risks, sensitive data, and evidence gaps; never explain from memory.

Resolve paths from the request, active metadata, project guidance, then the portable default. Portable durable output requires one exact path and never creates governed state.

Use `change.yaml` for current state and treat the plan and upstream artifacts as read-only.

## Generated Markdown readability

Write normal Markdown paragraphs with stable IDs. Do not split a sentence across physical source lines. Diagrams are optional. Do not require manual-proof contracts from readability alone.

## Classification and resources

Classify the governed signal as `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. A malformed, duplicated, escaped, unsafe, stale, missing-root, mismatched, or conflicting signal stops without portable fallback.

Independently select `inline-explanation`, `create-durable-explanation`, or `refresh-durable-explanation`. Create requires an exact absent target. Refresh requires an exact existing target, current identity, and explicit user authority or a validated governed stale route. A missing refresh target routes to creation without silent reclassification.

Use exactly these assemblies:

- `EC0-portable-inline`: `SKILL.md`.
- `EC1-portable-durable`: `SKILL.md` plus skeleton.
- `EC2-governed-inline`: `SKILL.md` plus governed reference.
- `EC3-governed-durable`: `SKILL.md` plus governed reference and skeleton.

For a single candidate, READ `references/governed-workflow-explanation.md`. For durable output, COPY `assets/explain-change-skeleton.md`. Loading does not grant mutation, lifecycle, routing, automation, or readiness authority. A missing, unreadable, escaped, stale, contradictory, or mixed-version resource blocks; must not reconstruct it. Load late-discovered resources before dependent work.

## Durable writes

Create and refresh compose a complete whole-file artifact from the current skeleton. No section-level refresh, mixed-ownership preservation, managed-region editing, or historical-layout parsing. Leave untargeted history unchanged.

Resolve action, target, prior identity, reviewed basis, and content; validate and re-read decision identities; atomically replace one file; then read back. Unavailable, failed, uncertain, or concurrent replacement blocks. A retry must classify current state afresh and never adopt unknown or changed content.

## Content and claims

Trace decisions to changes and tests. Include pre-verify evidence, alternatives, scope, risks, and disposition counts with a resolution link.

Never claim final verify, branch readiness, `pr-body-ready`, `pr-open-ready`, hosted-CI completion, release, deployment, lifecycle completion, artifact settlement, milestone state, routing, or external mutation. Only workflow decides whether verify is next.

## Stop conditions

Stop on ambiguous diff, target, authority, identity, signal, resource, open finding, unsafe content, or failed read-back. Name the blocker and owner.

## Evidence collection efficiency

Use summary and stable-ID first reasoning. Prefer check IDs, requirement IDs, file paths, and line citations before broad reads.

## When full-file read is required

Read fully when the whole file is the review target, bounded searches disagree, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Report classification, action, assembly, output, basis, gaps, commands, blockers, claim limits, and handoff owner.

## Resource map

- READ `references/governed-workflow-explanation.md` only for `single-governed-candidate`.
- COPY `assets/explain-change-skeleton.md` only for durable create or refresh.
