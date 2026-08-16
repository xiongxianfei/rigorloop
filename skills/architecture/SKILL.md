---
name: architecture
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Create or update technical architecture after the spec is stable and before execution planning.
argument-hint: [feature spec path, proposal path, architecture question, or change name]
---

# Architecture assessment and authoring

## Workflow role

- role_name: architecture
- stage: authoring
- upstream: approved spec and current spec review
- downstream: architecture-review
- summary: Assess architecture impact and author the smallest justified package.
- ownership: Architecture artifacts and authorized architecture authoring evidence only.
- must_not_claim: architecture-review approval, plan readiness, implementation readiness, verification, branch readiness, release readiness, or PR readiness.

Portable work is isolated. Workflow-managed execution does not enlarge the architecture write set.

## Evidence and upstream settlement

Read current guidance, proposal, approved spec/review, canonical architecture, relevant ADRs, project map, and affected system surfaces. Rank governing artifacts above history and inference; upstream artifacts and state are read-only.

Require an approved current spec without later contradiction or open resolution. Route unsettled direction to `proposal`, unclear behavior to `spec`, and missing settlement to `spec-review`.

## Classification and loaded assemblies

Classify before mutation. Assessment mode is `isolated` or `workflow-managed`; applicability judgment is `required`, `not-required`, or `ambiguous`; route result is `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`; authoring action is `assessment-only`, `canonical-update`, `adr-only`, `canonical-update-with-adr`, or `blocked`.

| Assembly | Use | Loaded procedure |
| --- | --- | --- |
| `AA0-assessment` | assessment only | `SKILL.md` |
| `AA1-portable-authoring` | portable architecture authoring | AA0 plus package method |
| `AA2-governed-authoring` | governed authoring | AA1 plus governed authoring |

Loading selects procedure, not authority.

## Applicability and routing

Use architecture for cross-component structure, data flow, persistence, APIs, deployment, packaging, adapters, security, quality targets, cross-cutting rules, or durable decisions. Use the smallest surface: canonical truth, ADR decision history, or both.

For a leaf change without those effects, return `architecture-not-required` with rationale and write no artifact. Unresolved applicability returns `architecture-ambiguous` and blocks. Never create temporary architecture to resolve product or behavioral uncertainty.

Portable authoring repeats current applicability, writes only resolved architecture or ADR files, and never writes lifecycle, review, routing, or automation state.

Workflow-managed assessment records `Stage: architecture-assessment`, `Applicability: required | not-required`, and exact `Spec identity`; ambiguity pauses without completion. Isolated assessment writes only to an explicit valid user-provided evidence path.

## Governed signals and targets

Governed signals are `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`. Any explicit change ID, workflow identity, owning-change field, or governed entry counts even when malformed. Only no signal permits portable authoring; invalid, stale, conflicting, duplicated, escaped, unsafe, or ambiguous signals stop without portable fallback.

Target operations are `create`, `revise`, `supersede`, and `deprecate`. Canonical architecture and each ADR are distinct manifest targets. Never rewrite accepted history as though a prior decision never existed.

## Universal write and handoff boundaries

Author only accepted design required by the spec. Exclude milestones, secrets, review settlement, unsupported claims, and mutable state. Preserve history and identify replacement or supersession.

Governed authoring ends each completed target at `review-required` and hands off to `architecture-review`. It never approves ADRs, settles supersession, or advances workflow. Report partial targets and blockers.

## Stop conditions and claims

Stop on missing or unreadable required resources, unresolved placement, invalid signals, stale basis, illegal state, ambiguity, conflicts, changed baseline, unsafe dependencies, unrecorded files, concurrency, incomplete recovery, or placeholders. The common path must not reconstruct missing procedure.

Never claim architecture-review approval, ADR settlement, plan or implementation readiness, validation, verification, branch readiness, release, deployment, publication, or PR readiness.

## Resource map

- READ `references/architecture-package-method.md` for `AA1-portable-authoring` and `AA2-governed-authoring` before package judgment or writes.
- READ `references/governed-architecture-authoring.md` only for `AA2-governed-authoring`; validate exact authority before governed reads or writes.
- COPY `assets/architecture-skeleton.md` when creating or fully rewriting canonical architecture. Fill applicable sections and remove placeholders.
- COPY `assets/adr-skeleton.md` when creating a new ADR. Fill every applicable field.
- COPY `assets/diagram-styles.mmd` when Mermaid flowchart or graph diagrams need the standard role styles.

Require readable, contained, same-version resources. Missing triggered resources stop dependent work; untriggered references do not block assessment.

## Evidence collection efficiency

Use summary and stable-ID first reasoning. Prefer check IDs, requirement IDs, file paths, line citations, diffs, and targeted excerpts.

## When full-file read is required

Read fully when the whole file is the review target, bounded searches disagree, isolation is unsafe, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
COPY `<applicable mapped asset>` to `<resolved target>` and replace every placeholder.
```

Use mapped assets only for applicable authoring output; assessment-only results use the compact result below.

## Expected output

Return a concise result without unfilled placeholders.

## Result

Report assessment mode, applicability judgment, route, action, assembly, targets, changed sections or ADRs, blockers, recording state, claim limitations, and next stage.
