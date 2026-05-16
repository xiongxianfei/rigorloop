# Follow-ups

This file tracks deferred work that is not owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session.

Do not use this file for normal active milestone tracking.

## Open follow-ups

| ID | Title | Source | Owner stage | Owner surface | Status | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| FU-005 | Implement `rigorloop new-change` artifact pack scaffolding | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | Implementation milestones are closed in `docs/plans/2026-05-16-rigorloop-cli-new-change.md`; explain-change is recorded, final local verify passed, and the next action is PR handoff. |
| FU-006 | Implement `rigorloop status` workflow inspection | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance and state-contract specification, define inspection, blockers, JSON output, and no-overclaim rules before implementation planning. |
| FU-007 | Implement `rigorloop validate` as the public validation facade | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance, specify facade behavior over repository-owned or project-configured validators using `selected`, `ci`, `change_metadata`, `review_artifacts`, `artifact_lifecycle`, and `skills` before reporting and mapping selected validators to stable exit codes. |
| FU-008 | Add machine-readable workflow schema and semantic validator | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After proposal acceptance, create a follow-on proposal or spec for `workflow/rigorloop.workflow.yaml`, canonicality, `schemas/workflow.schema.json`, claims, transitions, blockers, and validator bindings. |
| FU-009 | Generate workflow docs, diagrams, validator tables, and frozen drift checks | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | After workflow schema canonicality is settled, plan generation from workflow YAML and `rigorloop validate --workflow --frozen`. |
| FU-010 | Harden npm release pipeline for RigorLoop CLI package | docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md | proposal | proposal | open | Required before public npm publication: create release-policy artifacts for trusted publishing, provenance, pinned Actions, CODEOWNERS, `@xiongxianfei/rigorloop` package contents, dependency policy, lifecycle-script policy, and publish validation. |

## Closed follow-ups

| ID | Title | Closed by | Notes |
| --- | --- | --- | --- |
| FU-001 | Improve token-friendliness for remaining skills | Maintainer decision on 2026-05-15 | Closed by maintainer request; no active proposal needed. |
| FU-002 | Decide RigorLoop CLI package architecture and command contracts | PR #62 | First-slice CLI spec, architecture, ADR, plan, implementation, review, verify, and merge completed. Remaining CLI work is tracked by narrower follow-ups. |
| FU-003 | Implement first Codex init CLI slice | PR #62 | Implemented `@xiongxianfei/rigorloop`, `rigorloop` binary, help/version, `init --adapter codex`, dry-run JSON, safe manifest scaffolding, verified Codex adapter install, and planned lockfile output only. |
| FU-004 | Implement `rigorloop init` adapter archive model | PR #63 | Durable `rigorloop.lock` writes for verified Codex init, local/archive source recording, strict lockfile schema handling, generated-output tree hashing, and drift blocking merged with the lockfile follow-up. |
