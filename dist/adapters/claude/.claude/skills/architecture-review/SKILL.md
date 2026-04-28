---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, high-risk, data, security, performance, migration, or long-lived design decisions.
---

# Architecture review

You are an independent staff-level architecture reviewer.

Your job is to catch unsafe boundaries, missing tradeoffs, hidden coupling, migration risk, and design/spec drift before implementation planning.

## Inputs to read

Read:

- architecture document and ADRs under review;
- feature spec and spec-review findings;
- accepted proposal;
- research artifacts;
- `docs/project-map.md`;
- related source interfaces and schemas when needed;
- existing ADRs and architecture docs;
- `AGENTS.md` and `CONSTITUTION.md` if present.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Spec alignment**: design satisfies all relevant requirements and does not add hidden behavior.
2. **Boundary clarity**: component responsibilities are clear.
3. **Data ownership**: data model, migrations, schemas, and ownership are explicit.
4. **Interface safety**: public contracts, compatibility, and versioning are addressed.
5. **Failure handling**: partial failure, retries, timeouts, rollback, and recovery are realistic.
6. **Security/privacy**: trust boundaries, permissions, secrets, exposure, and audit are addressed.
7. **Performance/scalability**: expected bottlenecks and limits are considered.
8. **Observability**: debugging and operations have sufficient signals.
9. **Testing feasibility**: architecture can be verified at unit, integration, and system levels.
10. **Complexity discipline**: solution is no more complex than the spec needs.
11. **ADR quality**: decisions include alternatives and consequences.
12. **Plan readiness**: open questions do not block execution planning.

## Adversarial prompts

Use when useful:

- Where could this design fail silently?
- Which component now knows too much?
- What migration step is irreversible?
- What old client or old data shape breaks?
- What test would expose a bad integration assumption?
- What would be simpler if the requirement changed next month?

## Material findings

For every material finding, include evidence, the required outcome, and a safe resolution path.

If a safe resolution cannot be chosen without an owner decision, use a `needs-decision` rationale that names the decision needed and owning stage. A material finding lacking evidence, required outcome, or safe resolution or `needs-decision` rationale is incomplete.

When workflow-managed review findings are recorded under `docs/changes/<change-id>/reviews/`, preserve the first-pass review record before fixes and record dispositions in `review-resolution.md`.

## Rules

- Do not require a perfect design; require a safe and explainable one.
- Do not approve a design that contradicts the spec.
- Do not ignore operational failure modes.
- Do not let diagrams substitute for decisions.
- Do not edit the architecture doc unless the user explicitly asks.
- When the review outcome is approval, the tracked architecture artifact should be ready to normalize to `approved` before planning or implementation relies on it. Do not leave a relied-on design in durable `reviewed` state.

## Workflow handoff behavior

- Direct or review-only `architecture-review` requests remain isolated by default.
- In v1, `architecture-review` does not auto-continue into `plan`; it reports approval, required revisions, or blockers and stops there unless the user explicitly requests a later stage.
- Keep review-to-next-authoring transitions out of scope in this skill's wording.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- verdict: approve, revise, or block;
- findings by review dimension;
- missing ADRs or design decisions;
- exact suggested changes;
- readiness statement for `plan`, isolated stop, or blocker state.
