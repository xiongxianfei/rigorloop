---
name: architecture
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or update technical architecture after Proposal Review and before the specification is finalized.
argument-hint: [feature spec path, proposal path, architecture question, or change name]
---

# Architecture authoring

## Workflow role

### Compact current-state contract

For `compact-current-state-v1`, start from the bounded CLI projection and read only its required paths plus the approved proposal constraints needed for architecture. Author canonical architecture or ADR content, then submit the transient authoring operation through the CLI; never edit `change.yaml` directly. The CLI validates consistency but grants no permission. The artifact becomes review-ready for the stable current review owned by Design Review. Do not create routine request, authoring-evidence, correction-return, or review-log artifacts.

- role_name: architecture
- stage: authoring
- upstream: accepted proposal and embedded feasibility evidence
- downstream: spec reconciliation, then design-review
- summary: Author the smallest architecture package that establishes the technical design envelope.
- ownership: Architecture artifacts and authorized architecture authoring evidence only.
- must_not_claim: Design Review approval, plan readiness, implementation readiness, verification, branch readiness, release readiness, or PR readiness.

Portable work is isolated. Workflow-managed execution does not enlarge the architecture write set.

## Evidence and upstream settlement

Read current guidance, the accepted proposal and feasibility evidence, draft specification when present, canonical architecture, relevant ADRs, project map, and affected system surfaces. Rank governing artifacts above history and inference; upstream artifacts and state are read-only.

Require an accepted current proposal and feasibility evidence without later contradiction or open resolution. Route unsettled direction to `proposal` and behavior needing reconciliation to `spec`.

## Classification and loaded assemblies

Classify before mutation. Authoring mode is `portable` or `governed`; authoring action is `canonical-update`, `adr-only`, `canonical-update-with-adr`, `no-change-required`, or `blocked`.

| Assembly | Use | Loaded procedure |
| --- | --- | --- |
| `AA1-portable-authoring` | portable architecture authoring | `SKILL.md` plus package method |
| `AA2-governed-authoring` | governed authoring | AA1 plus governed authoring |

Loading selects procedure, not authority.

## Scope and routing

Treat specification requirements as SRs and architecture as their technical realization, not as another requirement level.

Use architecture for cross-component structure, data flow, persistence, APIs, deployment, packaging, adapters, security, quality targets, cross-cutting rules, or durable decisions. Use the smallest surface: canonical truth, ADR decision history, or both.

For a focused change with no new architectural decision, confirm the current architecture envelope with `no-change-required`; the current architecture remains the package member. Never create temporary architecture to resolve product or behavioral uncertainty.

Portable authoring repeats current applicability, writes only resolved architecture or ADR files, and never writes lifecycle, review, routing, or automation state.

## Governed signals and targets

Governed signals are `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. Any explicit change ID, workflow identity, owning-change field, or governed entry counts even when malformed. Only no signal permits portable authoring; invalid, stale, conflicting, duplicated, escaped, unsafe, or ambiguous signals stop without portable fallback.

Target operations are `create`, `revise`, `supersede`, and `deprecate`. Canonical architecture and each ADR are distinct manifest targets. Never rewrite accepted history as though a prior decision never existed.

## Universal write and handoff boundaries

Author only accepted design required by the spec. Exclude milestones, secrets, review settlement, unsupported claims, and mutable state. Preserve history and identify replacement or supersession.

Governed authoring ends each completed target at `review-required` and hands off to specification reconciliation, then `design-review`. It never approves ADRs, settles supersession, or advances workflow. Report partial targets and blockers.

## Stop conditions and claims

Stop on missing or unreadable required resources, unresolved placement, invalid signals, stale basis, illegal state, ambiguity, conflicts, changed baseline, unsafe dependencies, unrecorded files, concurrency, incomplete recovery, or placeholders. The common path must not reconstruct missing procedure.

Never claim Design Review approval, ADR settlement, plan or implementation readiness, validation, verification, branch readiness, release, deployment, publication, or PR readiness.

## Resource map

- READ `references/requirement-to-delivery-model.md` when relating system requirements to technical realization or downstream allocation.
- READ `references/architecture-package-method.md` for `AA1-portable-authoring` and `AA2-governed-authoring` before package judgment or writes.
- READ `references/governed-architecture-authoring.md` only for `AA2-governed-authoring`; validate exact authority before governed reads or writes.
- COPY `assets/architecture-skeleton.md` when creating or fully rewriting canonical architecture. Fill applicable sections and remove placeholders.
- COPY `assets/adr-skeleton.md` when creating a new ADR. Fill every applicable field.
- COPY `assets/diagram-styles.mmd` when Mermaid flowchart or graph diagrams need the standard role styles.

Require readable, contained, same-version resources. Missing triggered resources stop dependent work.

## Evidence collection efficiency

Use summary and stable-ID first reasoning. Prefer check IDs, requirement IDs, file paths, line citations, diffs, and targeted excerpts.

## When full-file read is required

Read fully when the whole file is the review target, bounded searches disagree, isolation is unsafe, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
COPY `<applicable mapped asset>` to `<resolved target>` and replace every placeholder.
```

Use mapped assets only for applicable authoring output; `no-change-required` uses the compact result below.

## Expected output

Return a concise result without unfilled placeholders.

## Result

Report authoring mode, action, assembly, targets, changed sections or ADRs, blockers, recording state, claim limitations, and next stage.
