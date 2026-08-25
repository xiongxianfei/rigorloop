# Governed architecture authoring

Load only for `AA2-governed-authoring`. The parent and package method own architecture judgment; this reference owns governed registration.

## Basis and manifest

Run `rigorloop lifecycle context architecture --change <change-id> --format json`. Require a current `architecture-required` assessment, exact approved spec identity, legal authority, and no blocker. Prepare one ordered authoring-evidence manifest covering each canonical or ADR target, its kind, role, path, prior digest or absence, dependencies, commit group, and independently valid commit point. Capture every prior target digest before writing.

If context returns `RL_WORKFLOW_ROUTE_REQUIRED`, do not author or mutate state. Return its route facts to workflow and resume only after context makes `record-artifact-revision` immediately available.

Write stage-owned diagrams, ADRs, canonical Markdown, and manifest evidence in dependency order. For each target, evidence names its artifact path, SHA-256 identity, and `Evidence state: complete`. Preserve architecture history. A partial batch may retain only targets the manifest proves independently valid; otherwise stop and route recovery.

For each complete target, refresh context and submit `record-artifact-revision` using the returned lifecycle revision, exact target ID, kind (`architecture` or `adr`), role, path, shared evidence path, `stage_authority: architecture`, and prior digest for revision. Register targets in manifest order. The CLI derives `review-required` and invalidates replaced evidence; never edit lifecycle fields or routing directly.

Stop on drift, dependency failure, conflicting target, rejected registration, unsafe partial group, or ambiguous retry. `already-recorded` is success only for the identical target and evidence.

## Result

Report assessment basis, manifest, each target and CLI result, preserved partial state, blockers, and architecture-review eligibility. Do not claim approval or continuation.
