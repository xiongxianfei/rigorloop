# <Model name> Design

Readability contract: Use normal prose paragraphs and complete sentences; use stable IDs and tables for repeated mappings.

Model validation contract: model-document-v1

## Introduction and Goals

<Responsibility, direction and stable owning-change pointer when governed.>

## Architecture Overview

<Required concise graph: model boundary, principal responsibilities, external products/interfaces, labeled relationships and links to detailed owners.>

### Supporting-view decisions

| View | Necessary and why | Owning detail |
| --- | --- | --- |
| Context | <Reasoned decision.> | <Draw if necessary; link to owned detail.> |
| Building Block | <Reasoned decision.> | <Draw if necessary; link to owned detail.> |
| Runtime | <Reasoned decision.> | <Draw if necessary; link to owned detail.> |
| Deployment | <Reasoned decision.> | <Draw if necessary; link to owned detail.> |

## Context and Scope

<External boundaries, inputs/outputs, owner relationships, scope and non-goals. Draw the Context View when necessary.>

## Architecture Constraints

<Applicable authority, technical, compatibility and execution constraints.>

## Requirements

| ID | Required behavior |
| --- | --- |
| <MODEL-SR-01> | <Observable normative outcome and relevant conditions.> |

## Solution Strategy

<Reconciled behavior and technical realization, important dependencies and alternatives.>

## Building Block View

<Coherent local responsibilities and references to shared-contract owners. Draw the Building Block View when necessary.>

## Runtime View

<Representative normal and failure/recovery flows, including affected interactions. Draw the Runtime View when necessary.>

## Deployment View

<Relevant environment, packaging and trust boundaries, or bounded non-applicability. Draw the Deployment View when necessary.>

## Crosscutting Concepts

<Applicable shared concepts, interfaces, data and authority constraints.>

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | <MODEL-SR-01> | <Condition and observable outcome.> |
| State/lifecycle | <MODEL-SR-01> | <Condition and observable outcome.> |
| Identity/authority | <MODEL-SR-01> | <Condition and observable outcome.> |
| Composition/path | <MODEL-SR-01> | <Condition and observable outcome.> |
| Temporal/retry | <MODEL-SR-01> | <Condition and observable outcome.> |
| Failure/recovery | <MODEL-SR-01> | <Condition and observable outcome.> |
| Compatibility/migration | <MODEL-SR-01> | <Condition and observable outcome.> |
| External/environment | <MODEL-SR-01> | <Condition and observable outcome.> |

<Material combined hazards and integrated observation boundaries, linked to requirements.>

### Test design

<Apply the selected requirement-and-proof method: account for every current requirement and section-owned responsibility in scope, including parent interactions. Keep proportionate group reasoning here or link owned test-design/test-design.md and any explicitly selected case index. Reference requirements and the project's shared rules rather than duplicate them. Markdown alone is sufficient; do not require JSON unless the user or project selects it.>

| Group and requirement basis | Risk, target and observation boundary | Conditions, action and independent expected outcome | Fixtures, method and realization gaps |
| --- | --- | --- | --- |
| <Coherent behavior and existing requirement IDs or justified obligation.> | <Plausible violation, consequence, justified depth and actual interface or operation observed.> | <Concrete starting facts, defining action and independently expected values/diagnostics/preserved state.> | <Minimal realistic inputs, fresh mutable resources/cleanup, real/substituted boundaries, inspected test links or proposed review method; distinguish missing protection.> |

<Group equivalent variations while preserving distinct authority, persistence and recovery observations. Explain which faulty candidate the group detects and why another variation would add no distinct detection or useful diagnosis. Account for uncovered obligations and bounded owner dispositions; an unresolved required observation prevents a completeness claim. Several methods may realize one scenario; native discovery owns the method inventory and useful unlisted regressions remain protected. Parent-owned interactions reference child coverage and add the failures that can pass both children. Explain maintenance of identity, group membership, source links and gaps; keep temporary migration acceptance in its change and results in evidence. If a catalog is selected, define its field/reference contract and validation limits in owned detail. Remove unused scaffold text rather than inventing tests.>

### Supporting examples

<Optional index: path, purpose, governing requirements, complete/excerpt scope, synthetic identities and starting assumptions. Remove when no example is justified.>

## Architecture Decisions

| ID | Context and decision | Alternatives and consequences |
| --- | --- | --- |
| <MODEL-DEC-01> | <Important choice, rationale and still-applicable constraints.> | <Meaningful alternatives and consequences.> |

## Quality Requirements

<Important quality conditions, expected response and observation boundary; assessment/feasibility basis for material uncertain claims.>

## Risks and Technical Debt

<Assumptions, unresolved decisions, residual risks and explicitly owned deferred work.>

## Glossary

<Necessary domain terms, or remove when not useful.>
