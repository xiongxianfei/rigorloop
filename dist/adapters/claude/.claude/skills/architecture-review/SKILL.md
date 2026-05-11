---
name: architecture-review
description: >
  Review a proposed architecture/design before execution planning. Use for cross-component, hard-to-reverse, data, security, performance, migration, or long-lived design decisions.
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

Isolation governs handoff. Recording follows material findings.

A direct or review-only request remains isolated by default: it does
not automatically continue into downstream workflow stages.

Isolation does not suppress recording.

Every material finding requires a durable change-local review record
under:

`docs/changes/<change-id>/reviews/<stage>-r<n>.md`

The review record must be indexed in `review-log.md` and resolved in
`review-resolution.md`.

Create the durable record before fixing.

A material finding must include:

- evidence
- required outcome
- safe resolution path, or `needs-decision` rationale

Clean reviews with no material findings remain lightweight and do not
require detailed review files.

For an isolated review with material findings, the final review output
must state:

- no automatic downstream handoff
- material Finding IDs
- required review record path
- whether the record must be created before fixing or reconstructed
- whether owner decision is needed

## Detailed Review Records

Use these detailed review record triggers for formal lifecycle reviews:

- material findings
- stage-owned non-approval outcomes that block downstream progress or require revision
- reconstructed review evidence
- closeout evidence citation
- explicit reviewer or maintainer request

Examples of stage-owned non-approval outcomes include `revise`, `changes-requested`, `blocked`, `rethink`, `inconclusive`, and equivalent blocking stage-specific outcomes.

When a detailed review file is created, `review-log.md` indexes it. Material findings need stable `Finding ID` values and disposition in `review-resolution.md`.

In this contract, clean reviews can settle artifact-locally when no detailed review record triggers apply. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`. Likewise, artifact-local settlement must not replace detailed review records when a trigger applies.

Do not add a dedicated `pr-review` stage. It is an unsupported review stage unless a later approved spec extends the stage set. A material maintainer PR comment that needs disposition must first be promoted into a supported formal lifecycle review record with a stable `Finding ID`.

## Recording status output

`Recording status` is not the review verdict. It reports whether required review-recording artifacts were created, were not required, or are blocked.

Use exactly one:

- `not-required`: no material findings exist and no detailed-record trigger applies.
- `recorded`: every artifact required by the active recording trigger exists or was updated.
- `blocked`: required review-recording artifacts could not be created or updated.

For material findings, `recorded` requires a detailed review record, `review-log.md`, and `review-resolution.md`. For no-material detailed-record triggers, `recorded` requires a detailed review record and `review-log.md`; do not require an empty `review-resolution.md` solely for that no-material review event.

If `Recording status: blocked`, include `Recording blocker` with the blocker and smallest action needed to create or update the required recording artifacts.

Do not merely tell the user that these files should be created. Create or update them before final output, or report `Recording status: blocked`.

Every material finding in final output and durable records must preserve complete finding shape:

- Finding ID
- Severity
- Location
- Evidence
- Required outcome
- Safe resolution path, or `needs-decision` rationale

`Location` may be a file path and section, file path and line, artifact and milestone or requirement ID, missing expected artifact path, or review surface plus not-present rationale. It must be specific enough to find the affected surface without chat history.

When recording is required and no active change root is obvious, choose the change ID in this order:

1. active `docs/changes/<change-id>/change.yaml`
2. active plan or reviewed artifact metadata
3. user-provided change ID
4. generated review-recording change ID: `YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording`

If the change ID remains ambiguous, use `Recording status: blocked`.

## Status sync output

`Status sync` is not the review verdict, is separate from `Recording status`, and is not downstream workflow continuation. It reports whether a clean or approving review result updated the reviewed artifact's owned lifecycle/status/readiness/closeout surface.

Use exactly one:

- `not-required`: the review outcome is not approving or clean, or no lifecycle status change is expected for that review result.
- `updated`: the reviewed artifact's owned lifecycle/status/readiness/closeout surface was updated to the next artifact-specific state.
- `blocked`: an approving or clean review result expected an artifact-status update, but the update could not be made.

For `architecture-review`, an `approved` architecture package targets architecture `Status: approved`. An `approved` ADR targets ADR `Status: accepted` or `Status: active`, according to the ADR's existing lifecycle field.

If `Status sync: updated`, include `Status artifact` with the status artifact path and exact status field or section changed.

If `Status sync: blocked`, include `Status sync blocker` with the intended next status, the blocker, and the smallest manual action needed.

Explicit user instructions that forbid file edits block status sync even when the review result is approving or clean. If the target is ambiguous, do not guess; use `Status sync: blocked`.

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
- Status sync:
- Status artifact:
- Status sync blocker:
- Review record:
- Review log:
- Review resolution:
- Open blockers:
- Immediate next stage:
- Required canonical updates:
- Required ADR updates:
- Next stage:
```

Then include:

- findings by review dimension with evidence, required outcome, and safe resolution;
- missing C4 views, arc42 sections, legacy status, ADRs, or design decisions;
- exact suggested changes;
- readiness statement for `plan`, isolated stop, or blocker state.
