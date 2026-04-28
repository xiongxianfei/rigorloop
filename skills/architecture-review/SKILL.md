---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, high-risk, data, security, performance, migration, or long-lived design decisions.
argument-hint: [architecture doc path, ADR path, or feature name]
---

# Architecture review

You are an independent staff-level architecture reviewer.

Your job is to catch unsafe boundaries, missing tradeoffs, hidden coupling, missing C4 or arc42 reasoning, unrecorded durable decisions, migration risk, and design/spec drift before implementation planning.

## Inputs to read

Read:

- `AGENTS.md` and `CONSTITUTION.md` if present;
- `specs/architecture-package-method.md` when C4, arc42, canonical package, change-local delta, or ADR method compliance is in scope;
- canonical architecture package under `docs/architecture/system/`;
- change-local architecture delta and diagrams under `docs/changes/<change-id>/`;
- ADRs under review and related existing ADRs;
- feature spec and spec-review findings;
- accepted proposal;
- research artifacts;
- `docs/project-map.md`;
- related source interfaces and schemas when needed;
- legacy architecture docs when their status or supersession affects the change.

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, arc42 section numbers, ADR IDs, diagram paths, file paths, and line citations. Expand from targeted sections only when the narrower evidence is insufficient.

## C4, arc42, and ADR Review Checklist

Check the approved package model before broader design critique:

- Canonical source: current architecture truth belongs in `docs/architecture/system/architecture.md` and default diagrams under `docs/architecture/system/diagrams/`.
- Change-local delta: `docs/changes/<change-id>/architecture.md` is working evidence only and must not compete with the canonical package after merge-back.
- arc42 completeness: lifecycle metadata appears before all 12 official arc42 sections, and the section names remain in order.
- Core sections: Introduction and Goals, Architecture Constraints, Context and Scope, Solution Strategy, and Building Block View contain current-system content for real architecture work.
- Runtime View: updated when behavior, orchestration, failure paths, command flow, generated-output flow, or operational flow changes.
- Deployment View: updated when environments, packaging, generated outputs, adapters, release layout, infrastructure, or execution boundaries change.
- Crosscutting Concepts: updated when validation, security, caching, portability, generation, observability, or similar cross-cutting rules change.
- Architecture Decisions: section 9 links relevant ADRs or states that no ADRs are required for the update.
- Quality Requirements, Risks and Technical Debt, and Glossary are present and explicit enough for review.
- C4 sufficiency: context and container diagrams exist as reviewable source text; component or deployment diagrams are required only when the change needs that level of explanation.
- ADR completeness: durable decisions have ADRs with status, context, decision, alternatives considered, consequences, and follow-up.
- Merge-back: accepted durable content from a change-local delta is represented in the canonical package before completion.
- Legacy status: older `docs/architecture/` documents are not implied to be normalized unless the legacy normalization artifact classifies them.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Spec alignment**: design satisfies all relevant requirements and does not add hidden behavior.
2. **Package shape**: canonical or change-local artifact usage matches the approved C4, arc42, and ADR method.
3. **Boundary clarity**: C4 views and Building Block View make component responsibilities clear.
4. **Data ownership**: data model, migrations, schemas, and ownership are explicit when relevant.
5. **Interface safety**: public contracts, compatibility, and versioning are addressed.
6. **Runtime and failure handling**: runtime scenarios, partial failure, retries, timeouts, rollback, and recovery are realistic.
7. **Deployment and execution boundaries**: packaging, adapters, generated output, environments, and release layout are covered when affected.
8. **Security/privacy**: trust boundaries, permissions, secrets, exposure, and audit are addressed.
9. **Quality and operations**: quality requirements, performance, scalability, observability, and maintainability are considered.
10. **Testing feasibility**: architecture can be verified at unit, integration, and system levels.
11. **Complexity discipline**: solution is no more complex than the spec needs.
12. **ADR quality**: durable decisions include alternatives and consequences.
13. **Plan readiness**: open questions do not block execution planning.

## Adversarial prompts

Use when useful:

- Where could this design fail silently?
- Which component now knows too much?
- Which arc42 section would a maintainer need but not find?
- Is the chosen C4 level enough to see the affected boundary?
- What migration step is irreversible?
- What old client or old data shape breaks?
- What test would expose a bad integration assumption?
- What would be simpler if the requirement changed next month?
- Which decision will be impossible to recover six months from now without an ADR?

## Material findings

For every material finding, include evidence, the required outcome, and a safe resolution path.

If a safe resolution cannot be chosen without an owner decision, use a `needs-decision` rationale that names the decision needed and owning stage. A material finding lacking evidence, required outcome, or safe resolution or `needs-decision` rationale is incomplete.

When workflow-managed review findings are recorded under `docs/changes/<change-id>/reviews/`, preserve the first-pass review record before fixes and record dispositions in `review-resolution.md`.

## Rules

- Do not require a perfect design; require a safe and explainable one.
- Do not approve a design that contradicts the spec.
- Do not ignore operational failure modes.
- Do not let diagrams substitute for decisions.
- Do not let ADRs substitute for current structure.
- Do not require component, code-level, or deployment diagrams unless the change needs them.
- Do not require architecture updates for leaf changes with no architecture impact.
- Do not edit the architecture doc unless the user explicitly asks.
- When the review outcome is approval, the tracked architecture artifact should be ready to normalize to `approved` before planning or implementation relies on it. Do not leave a relied-on design in durable `reviewed` state.
- When spec-review or architecture-review identifies required changes, the artifact must not remain in `approved` state until the required changes are resolved and re-reviewed.

## Workflow handoff behavior

- Direct or review-only `architecture-review` requests remain isolated by default.
- In v1, `architecture-review` does not auto-continue into `plan`; it reports approval, required revisions, or blockers and stops there unless the user explicitly requests a later stage.
- Keep review-to-next-authoring transitions out of scope in this skill's wording.

## When full-file read is required

Read the full file when the whole file is the review target, when checking all 12 arc42 headings or lifecycle metadata, when merge-back from a change-local delta may affect multiple sections, when ADR supersession or legacy lifecycle status affects the verdict, when the relevant section cannot be isolated safely, when surrounding context can change the conclusion, when bounded searches disagree, or when a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- verdict: approve, revise, or block;
- findings by review dimension with evidence, required outcome, and safe resolution;
- missing C4 views, arc42 sections, merge-back, legacy status, ADRs, or design decisions;
- exact suggested changes;
- readiness statement for `plan`, isolated stop, or blocker state.
