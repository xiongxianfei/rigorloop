# Canonical System Architecture

## Status

- approved

## Introduction and Goals

Define the current system architecture in the canonical package.

## Architecture Constraints

- Keep architecture artifacts reviewable as repository text.

## Context and Scope

The repository contains authored workflow artifacts, validation scripts, and generated adapter output.

## Solution Strategy

Use concise arc42 sections with C4 diagrams and ADR links.

## Building Block View

- Authored artifacts
- Validation scripts
- Generated outputs

## Runtime View

Validation commands inspect repository artifacts and report lifecycle findings.

## Deployment View

Repository packaging is the deployment boundary for this documentation method.

## Crosscutting Concepts

Lifecycle status is tracked inside lifecycle-managed artifacts.

## Architecture Decisions

No ADRs are required for this lifecycle compatibility fixture.

## Quality Requirements

Reviewability and traceability are the primary qualities.

## Risks and Technical Debt

This fixture is intentionally small and does not model the whole repository.

## Glossary

- canonical package: the current system architecture source.

## Readiness

- Architecture review is complete. The next stage should be `plan`.
