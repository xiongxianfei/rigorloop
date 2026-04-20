# Explicit-scope valid proposal

## Status
- accepted

## Problem

Only this artifact should be validated in explicit-path mode.

## Goals

- Prove unrelated stale files stay out of scope.

## Non-goals

- Validate every file in the fixture root.

## Recommended direction

Pass only the proposal path.
