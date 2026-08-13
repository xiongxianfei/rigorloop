# Workflow Automation Target: Test-Spec Review

Stage: workflow
Date: 2026-08-13
Change: `2026-08-12-plan-skill-simplification`
Mechanism: `bounded-review-fix`
Target: `test-spec-review`
Occurrence: singleton

## Authorization

The explicit `$workflow auto: test-spec-review` invocation authorizes the governed lifecycle to continue through the first clean recorded `test-spec-review` result for this change. It does not authorize implementation, PR creation, push, publication, release, deployment, merge, credentials, destructive Git, or another external mutation.

## Canonical starting position

The primary proposal is accepted through `proposal-review-r4`, all proposal findings are closed, and the next valid authoring stage is `spec`.

## Architecture applicability

The accepted proposal selects `architecture-required`. After clean `spec-review`, workflow must record that assessment and route through architecture authoring and architecture-review before plan authoring.

## Stop conditions

Pause on any non-clean review, open material finding, failed recording, ambiguous or stale identity, invalid transition, missing required resource, failed required validation, owner decision, target non-applicability, or transition-budget exhaustion.
