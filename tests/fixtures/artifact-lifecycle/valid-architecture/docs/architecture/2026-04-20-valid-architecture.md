# Valid Architecture

## Status
- approved

## Related artifacts

- Spec: `specs/valid-spec.md`

## Introduction and Goals

Keep the design small and deterministic.

## Architecture Constraints

Use repository-local deterministic validation.

## Context and Scope

The validator and its governed Markdown inputs are in scope.

## Solution Strategy

Use one parser and one executable contract registry.

## Building Block View

The lifecycle validator reads artifact contracts and Markdown sections.

## Runtime View

Validation reads an artifact and reports structural findings.

## Deployment View

The validator runs as a repository-local Python command.

## Crosscutting Concepts

Required sections fail closed.

## Architecture Decisions

No ADR is required for this fixture.

## Quality Requirements

Validation is deterministic.

## Risks and Technical Debt

None for this fixture.

## Glossary

None for this fixture.

## Next artifacts

- Architecture review.

## Follow-on artifacts

- None yet.

## Readiness

- Architecture review is complete. The next stage should be `plan`.
