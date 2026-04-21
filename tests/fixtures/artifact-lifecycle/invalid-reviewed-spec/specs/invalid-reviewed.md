# Invalid reviewed spec

## Status
- reviewed

## Goal and context

This fixture should fail because `reviewed` is not a durable relied-on state.

## Requirements

R1. The validator MUST reject reviewed specs.

## Acceptance criteria

- Validation fails.
