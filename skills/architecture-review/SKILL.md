---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, hard-to-reverse, data, security, performance, migration, or long-lived design decisions.
argument-hint: [architecture doc path, ADR path, or feature name]
---

# Architecture review

You are an independent staff-level architecture reviewer.

Your job is to catch unsafe boundaries, missing tradeoffs, hidden coupling, missing C4 or arc42 reasoning, unrecorded durable decisions, migration risk, and design/spec drift before implementation planning.

## Inputs to read

Read:

- `AGENTS.md` and `CONSTITUTION.md` if present;
- the project's architecture method guidance when C4, arc42, canonical package, review-surface, or ADR method compliance is in scope;
- the project's canonical architecture package;
- ADRs under review and related existing ADRs;
- no-architecture-impact rationale when that is the review surface;
- feature spec and spec-review findings;
- accepted proposal;
- research artifacts;
- `docs/project-map.md`;
- related source interfaces and schemas when needed;
- legacy architecture docs when their status or supersession affects the change.

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, arc42 section numbers, ADR IDs, diagram paths, file paths, and line citations. Expand from targeted sections only when the narrower evidence is insufficient.

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. `docs/workflows.md` artifact-location table;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in `docs/workflows.md` when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Review Surface

Classify the review surface before reviewing:

- `canonical-architecture-update`
- `ADR`
- `no-architecture-impact-rationale`
- `proposal-or-spec-gap`

### canonical-architecture-update

Review the changed canonical architecture sections, diagrams, and ADR links directly.

Do not require a change-local architecture delta for a canonical architecture update.

Check the changed package content against arc42 structure, relevant C4 views, ADR links, quality concerns, risks, and compatibility with the approved spec.

### ADR

Review the ADR for context, decision, alternatives, consequences, and compatibility with the canonical architecture.

Confirm the ADR records a durable decision rather than duplicating current architecture structure that belongs in the canonical package.

### no-architecture-impact-rationale

Check whether the no-architecture-impact rationale is credible.

Reject the rationale when the change affects architecture boundaries, data flow, generated-output flow, deployment, packaging, adapters, quality targets, cross-cutting rules, security boundaries, or durable decisions.

### proposal-or-spec-gap

If the design direction is unresolved, return a finding that routes back to `proposal` or proposal revision.

If behavior is unsettled, route to `spec` or spec revision.

Do not use architecture-review to settle product direction.

## C4, arc42, and ADR Review Checklist

Check the approved package model before broader design critique:

- Canonical source: current architecture truth belongs in the project's canonical architecture package.
- arc42 completeness: lifecycle metadata appears before all 12 official arc42 sections, and the section names remain in order.
- Core sections: Introduction and Goals, Architecture Constraints, Context and Scope, Solution Strategy, and Building Block View contain current-system content for real architecture work.
- Runtime View: updated when behavior, orchestration, failure paths, command flow, generated-output flow, or operational flow changes.
- Deployment View: updated when environments, packaging, generated outputs, adapters, release layout, infrastructure, or execution boundaries change.
- Crosscutting Concepts: updated when validation, security, caching, portability, generation, observability, or similar cross-cutting rules change.
- Architecture Decisions: section 9 links relevant ADRs or states that no ADRs are required for the update.
- Quality Requirements, Risks and Technical Debt, and Glossary are present and explicit enough for review.
- C4 sufficiency: context and container diagrams exist as reviewable source text; component or deployment diagrams are required only when the change needs that level of explanation.
- ADR completeness: durable decisions have ADRs with status, context, decision, alternatives considered, consequences, and follow-up.
- Legacy status: older `docs/architecture/` documents are not implied to be normalized unless the legacy normalization artifact classifies them.

## Package Quality Checks

Treat these as common architecture-review finding triggers:

- embedded or duplicated diagram source in `architecture.md` instead of one linked authored diagram source file;
- generic non-C4 flowchart that does not distinguish people, system under review, external systems, and containers;
- wrong C4 level, such as internal containers shown in the system context diagram or component detail forced into the container diagram;
- missing C4 role classes in Mermaid flowchart or graph diagrams;
- missing technology labels where relevant for containers;
- unlabeled relationships or relationships that mix classification with runtime or dependency flow without explanation;
- flat Building Block View that is only a folder or source-path catalog when multiple responsibilities or containers are involved;
- duplicated ADR rationale in arc42 section 9 instead of concise ADR links and one-line summaries;
- weak quality-scenario content that names qualities without stimulus, environment, response, or measure;
- Deployment View repeats source layout instead of explaining packaging, execution, generated output, release, or distribution boundaries.

Add or request a component diagram only when the refined container view and Building Block View still cannot explain important internal responsibilities, boundaries, or interactions.

## Finding Format

Use this simple shape for architecture-review findings:

```text
Finding: <one-sentence problem>
Location: <file path and section/line, or diagram name>
Severity: <blocker | material | minor>
Recommendation: <what should change>
```

Severity MUST use `blocker`, `material`, or `minor`. Do not require mandatory C4-level classification; location provides the traceability when a finding is diagram-specific.

This simple architecture-review format does not replace the repository-wide material-finding contract. Material findings still require evidence, required outcome, and a safe resolution path or `needs-decision` rationale.

## Review dimensions

Evaluate each with `pass`, `concern`, or `block`:

1. **Spec alignment**: design satisfies all relevant requirements and does not add hidden behavior.
2. **Package shape**: the classified review surface matches the approved C4, arc42, and ADR method.
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

## Isolation and Recording

Isolation governs handoff. Recording follows formal review triggers.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every formal lifecycle review result must be recorded or explicitly blocked.

Use:

- `Recording status: recorded` when the required review evidence was created
  or updated.
- `Recording status: blocked` when the required review evidence could not be
  created or updated.

`not-required` is reserved for non-formal review-like requests outside the
formal lifecycle review model.

For a clean review, create the lightweight review receipt required by the
formal review recording spec and index it in `review-log.md`. Do not create an
empty `review-resolution.md` solely for a clean review.

For material findings or blocking outcomes, create the required detailed review
record and disposition artifacts.
Use a detailed review record for material or blocking review outcomes.

Material findings must include:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

Do not merely tell the user that review artifacts should be created. Create
or update them before final output, or report `Recording status: blocked` with
the blocker and smallest next action.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed


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

Read the full file when the whole file is the review target, when checking all 12 arc42 headings or lifecycle metadata, when an ADR supersession or legacy lifecycle status affects the verdict, when the relevant section cannot be isolated safely, when surrounding context can change the conclusion, when bounded searches disagree, or when a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

Start with:

```md
## Result

- Review surface: canonical-architecture-update | ADR | no-architecture-impact-rationale | proposal-or-spec-gap
- Review status: approved | changes-requested | blocked | inconclusive
- Material findings:
- Recording status:
- Recording blocker:
- Review record:
- Review log:
- Review resolution: <path | not-required | blocked>
- Open blockers:
- Required canonical updates:
- Required ADR updates:
- Next stage:
```

Then include:

- findings by review dimension with evidence, required outcome, and safe resolution;
- missing C4 views, arc42 sections, legacy status, ADRs, or design decisions;
- exact suggested changes;
- readiness statement for `plan`, isolated stop, or blocker state.
