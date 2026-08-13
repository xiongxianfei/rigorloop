# Architecture Assessment: Plan Skill Simplification

Assessment date: 2026-08-13
Result: architecture-required
Owner: workflow
Change: `2026-08-12-plan-skill-simplification`

The package split reuses the existing published-skill package model, but the evidence-initialization-settlement transaction changes ADR-owned lifecycle ordering, legal primary-plan state combinations, review settlement behavior, validator invariants, and recovery. Canonical architecture and a narrow successor ADR are required before planning.

Required architecture surfaces are `docs/architecture/system/architecture.md` and a successor to `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`. Independent `architecture-review` is required.
