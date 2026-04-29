# Architecture Title

## Status

- draft

## Related artifacts

- Proposal:
- Spec:
- Plan:
- ADRs:

## Introduction and Goals

State the architecture goal, scope, stakeholders, and what this package must make clear.

## Architecture Constraints

List binding constraints such as workflow rules, runtime limits, compatibility requirements, security boundaries, tooling limits, or dependency limits.

## Context and Scope

Describe the system boundary, primary actors, external systems, and relevant dependencies.

See [diagrams/context.mmd](diagrams/context.mmd) for the C4 system context view.

Package diagrams live as separate authored source files under `diagrams/`. Reference them with relative Markdown links, not image embeds or inline Mermaid blocks. Default Mermaid diagrams use `.mmd` source files; flowchart or graph diagrams should use the shared role classes from `templates/diagram-styles.mmd` or an explicitly equivalent copied block.

## Solution Strategy

Summarize the selected architecture approach and the main tradeoffs.

## Building Block View

Describe the system as a hierarchy. Start with a system-level white-box view, then decompose important containers, modules, artifact groups, or responsibilities only where the extra detail affects review.

See [diagrams/container.mmd](diagrams/container.mmd) for the C4 container view.

Add `diagrams/component-<name>.mmd` only when the refined container view and this section cannot explain important internal responsibilities, boundaries, or interactions.

## Runtime View

Describe important runtime scenarios, command flows, generation flows, failure paths, or operational sequences. Use `Not applicable` with rationale when no runtime flow is relevant.

## Deployment View

Describe environments, packaging, generated outputs, adapters, release layout, infrastructure, publication or distribution flow, release evidence, and execution boundaries when relevant. Avoid repeating source layout already covered in the Building Block View unless the source location is part of the deployment or packaging boundary.

Use `Not applicable` with rationale when no deployment or packaging concern is relevant.

## Crosscutting Concepts

Describe cross-cutting architecture rules such as validation strategy, security boundary, portability rule, generation policy, caching pattern, or observability pattern. Use `Not applicable` with rationale when none apply.

## Architecture Decisions

Summarize and link relevant ADRs with one concise line per decision, or state that no ADRs are required for this package or update. Keep detailed rationale in the ADR.

- [ADR-YYYYMMDD-short-title](../../adr/ADR-YYYYMMDD-short-title.md) - one-line decision summary.

## Quality Requirements

<!--
Quality scenarios use stimulus / environment / response / measure.
Example:

| Quality | Scenario | Measure |
| --- | --- | --- |
| Reviewability | A reviewer opens a PR that changes the canonical architecture package | All affected arc42 sections and diagram source files are visible as reviewable text in the PR |
| Performance | A contributor runs the required validation command for this package | Validation completes within the budget defined by the active plan or CI contract |

Delete this comment and replace it with real scenarios, or write `Not applicable` with a one-line rationale.
-->

## Risks and Technical Debt

Record known risks, deferred cleanup, and technical debt that affect this package or update.

## Glossary

Define architecture terms used in this package, or use `Not applicable` with rationale when no special terms need definition.

## Next artifacts

- Architecture review.

## Follow-on artifacts

- None yet.

## Readiness

State the truthful next repository stage and any conditions before downstream work relies on this package.
