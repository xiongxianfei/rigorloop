# Architecture Assessment: Workflow Skill Simplification

Assessment: architecture-required

## Rationale

The approved specification keeps the existing published-skill package model, lifecycle state model, and automation persistence schema, but it changes the canonical location and composition of workflow orchestration procedure.

The canonical architecture currently assigns public `$workflow auto` and stage-handoff semantics to `skills/workflow/SKILL.md` alone.
The approved design instead keeps universal classification and safety in `SKILL.md` while placing governed lifecycle, automation, and guide-authoring procedure in mapped package-local references with exact dependency direction and fail-safe loading.

That responsibility-location change crosses canonical skill structure, conditional policy loading, package composition, generated adapter parity, and runtime failure boundaries already owned by `docs/architecture/system/architecture.md`.
The owning architecture document must therefore be updated by this change before planning.

The existing resource-integrity architecture can be specialized rather than replaced.
No new ADR, diagram, runtime, state store, dependency, validation family, or deployment topology is required unless architecture authoring discovers a new durable decision beyond the approved specification.

## Required architecture scope

- Correct the workflow-automation component responsibility from one file to one skill-owned package.
- Record the universal-before-conditional ownership boundary.
- Record the one-way automation-to-governed transition dependency.
- Record stateless commands and transient bootstrap without changing persistence architecture.
- Record required-resource failure and atomic package rollout or rollback.
- Preserve existing generated, archived, and installed mapped-resource parity.

## Result

Proceed through `architecture` and `architecture-review` before planning.
