# Canonical-shaped Architecture at Legacy Path

## Status

- approved

## Introduction and Goals

This fixture uses the canonical arc42 shape at a non-canonical legacy architecture path.

## Architecture Constraints

- It should still be checked with the older legacy architecture contract.

## Context and Scope

Legacy path behavior must remain unchanged.

## Solution Strategy

Do not apply the canonical path compatibility outside `docs/architecture/system/architecture.md`.

## Building Block View

- Legacy architecture contract
- Canonical architecture compatibility branch

## Runtime View

Not applicable because this fixture only tests path classification.

## Deployment View

Not applicable because this fixture only tests path classification.

## Crosscutting Concepts

Lifecycle validation remains path-scoped.

## Architecture Decisions

No ADRs are required for this fixture.

## Quality Requirements

Path-scoped compatibility must not weaken legacy validation.

## Risks and Technical Debt

Applying canonical compatibility too broadly would weaken legacy architecture checks.

## Glossary

- legacy path: any architecture Markdown path other than the canonical system package.

## Readiness

- Architecture review is complete. The next stage should be `plan`.
