# ADR-20260902: Route Context and Skill Identity

## Owning change record

`docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`

## Context

The published `workflow` skill currently combines semantic routing and bounded automation with authoring and reading `docs/workflows.md`. The lifecycle CLI already owns deterministic state interpretation and guarded mutation, but agents still reconstruct artifact placement, project workflow configuration, and portions of current lifecycle context from Markdown and skill text.

The accepted proposal removes `docs/workflows.md`, renames the skill to `route`, and makes the CLI authoritative for deterministic project-local workflow facts without making it a semantic router. The design must also avoid disrupting already-active v3 automation merely because a public skill name changes.

## Decision

Add one read-only public command, `rigorloop workflow-context`, that projects deterministic project workflow facts. It has two phases:

1. Without `--change`, it returns the active governed-change candidates, effective lifecycle contract, configuration provenance, and any deterministic selection or configuration blockers. It never chooses among multiple candidates.
2. With `--change <change-id>`, it returns that change's current stage, artifact identities and resolved locations, package and milestone state, structural blockers, permitted lifecycle operations, automation projection, and effective project workflow configuration.

The command returns versioned human and JSON representations from one result model. It is read-only, performs no lifecycle mutation, does not classify the user's semantic intent, does not select a correction owner, and does not decide whether an allowed transition is the correct transition.

Use bundled v3 workflow defaults as the base configuration and allow one optional repository-root `rigorloop.workflow.yaml` to provide supported project-local overrides. Its first schema contains a closed schema version and an `artifact_locations` map whose entries use supported artifact kinds and repository-relative path templates or an explicitly supported non-path surface. Configuration precedence is bundled defaults followed by the tracked repository override; explicit user artifact identity or path remains request input checked against governance and safety, not hidden configuration. Unknown keys, kinds, placement forms, unsafe paths, contradictory ownership, and ambiguous template resolution fail closed. `docs/workflows.md`, repository prose, prior chat, filename guessing, and remembered conventions are not configuration inputs.

Rename the canonical and published skill package from `workflow` to `route`. Current skill inventories and adapter archives contain `route` and do not contain a `workflow` alias or tombstone skill. Installer, validation, and upgrade diagnostics detect an installed or requested obsolete current `workflow` package and identify `route` as its replacement. A host that resolves skills before RigorLoop runs may report the old invocation as unavailable; migration documentation must make the replacement explicit.

Retain `workflow` as the stable lifecycle authority value and retain existing `workflow.automation` stored namespaces. These are protocol-role and persistence names, not published skill identities. The `route` skill exercises the `workflow` authority. Existing active or resumable v3 automation therefore resumes under `route` without rewriting `change.yaml`, changing target identity, or losing receipts. New user-facing commands and skill references use `route`; stored authority and automation compatibility fields remain unchanged until a separately approved schema migration has independent value.

Remove `docs/workflows.md` from current routing authority and delete guide authoring, guide resources, guide invocation assemblies, and guide lookup fallbacks. Historical copies remain ordinary Git history or project documentation and are never consulted by current RigorLoop routing.

## Alternatives considered

- Extend `rigorloop lifecycle context <stage>` only: rejected because route discovery also needs a project-level phase before an exact change or stage is known.
- Put project workflow configuration in `rigorloop.yaml`: rejected because that file is installation target state and does not currently own governed workflow configuration.
- Keep `docs/workflows.md` as generated compatibility output: rejected because it preserves a second projection and refresh obligation that the proposal explicitly retires.
- Rename stored authority and automation keys with the skill: rejected because those stable protocol names do not grant skill identity and changing them would force unnecessary active-run migration.
- Keep a current `workflow` alias skill: rejected because it creates two public entry points and weakens the clean rename.
- Let the CLI choose the next semantic stage: rejected because structural permission does not establish correction ownership or engineering meaning.

## Consequences

- Route invocations gain one bounded authoritative context source and stop reconstructing deterministic facts from Markdown.
- The CLI package gains a closed project-workflow configuration parser, a project/change context projection, stable diagnostics, and direct tests for unknown values, unsafe paths, ambiguity, and non-mutation.
- The repository gains optional `rigorloop.workflow.yaml`; repositories using only bundled defaults need no file.
- Current docs, governance, specs, skills, validators, fixtures, adapter manifests, release metadata, and examples must migrate coherently from `workflow` invocation naming to `route` and from Markdown lookup to CLI context.
- Existing v3 automation remains resumable because persisted role and namespace identifiers do not change.
- Removing the human-authored workflow map makes readable CLI human output and configuration provenance part of acceptance.

## Follow-up

- Review this ADR with the change-owned architecture and specification as one Design package.
- Allocate implementation across the CLI context/config boundary, route skill migration, guide retirement, validation, generated adapters, documentation, and release proof.

