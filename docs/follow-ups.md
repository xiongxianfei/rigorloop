# Follow-ups

This file tracks deferred work that is not owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session.

Do not use this file for normal active milestone tracking.

## Open follow-ups

| ID | Title | Source | Owner stage | Owner surface | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| FU-001 | Improve token-friendliness for remaining skills | docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md | proposal | proposal | open | Create a proposal identifying remaining skills, optimization criteria, and validation evidence. |
| FU-002 | Decide RigorLoop CLI package architecture and command contracts | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | First-slice CLI spec created at `specs/rigorloop-cli-package-and-codex-init.md`; after spec review, create architecture/ADR coverage for package boundaries, release metadata lookup, local archive verification, extraction safety, and publication boundary. |
| FU-003 | Implement first Codex init CLI slice | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance plus CLI spec and architecture approval, plan a slice for package skeleton, local command execution, `rigorloop --help`, `rigorloop version`, `rigorloop init --adapter codex`, and `rigorloop init --adapter codex --dry-run --json`. |
| FU-004 | Implement `rigorloop init` adapter archive model | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance, specify verified Codex release archive metadata, pinned package-to-adapter version behavior, `--from-archive`, checksum verification, `rigorloop-tree-hash-v1`, planned lockfile output, manifest behavior, backup, no-overwrite rules, and generated-output boundaries before implementation planning; durable `rigorloop.lock` writes wait for an accepted lockfile spec. |
| FU-005 | Implement `rigorloop new-change` artifact pack scaffolding | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance and CLI contract settlement, define profile-aware change scaffolding in the spec, then plan a slice for `docs/changes/<change-id>/change.yaml` and related templates. |
| FU-006 | Implement `rigorloop status` workflow inspection | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance and state-contract specification, define inspection, blockers, JSON output, and no-overclaim rules before implementation planning. |
| FU-007 | Implement `rigorloop validate` as the public validation facade | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance, specify facade behavior over repository-owned or project-configured validators using `selected`, `ci`, `change_metadata`, `review_artifacts`, `artifact_lifecycle`, and `skills` before reporting and mapping selected validators to stable exit codes. |
| FU-008 | Add machine-readable workflow schema and semantic validator | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance, create a follow-on proposal or spec for `workflow/rigorloop.workflow.yaml`, canonicality, `schemas/workflow.schema.json`, claims, transitions, blockers, and validator bindings. |
| FU-009 | Generate workflow docs, diagrams, validator tables, and frozen drift checks | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After workflow schema canonicality is settled, plan generation from workflow YAML and `rigorloop validate --workflow --frozen`. |
| FU-010 | Harden npm release pipeline for RigorLoop CLI package | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | Required before public npm publication: create release-policy artifacts for trusted publishing, provenance, pinned Actions, CODEOWNERS, `@xiongxianfei/rigorloop` package contents, dependency policy, lifecycle-script policy, and publish validation. |

## Closed follow-ups

| ID | Title | Closed by | Notes |
| --- | --- | --- | --- |
