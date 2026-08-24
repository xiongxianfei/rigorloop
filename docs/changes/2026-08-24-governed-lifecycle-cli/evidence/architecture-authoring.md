# Architecture Authoring Evidence: Governed Lifecycle CLI

Stage: architecture
Transaction ID: architecture-authoring-r1
Change ID: `2026-08-24-governed-lifecycle-cli`
Assessment basis: `architecture-assessment-r1`
Spec identity: `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Approving review identity: `sha256:c004c71183fae1589599952235a8a72a37b93e346e8909d3c21dd24a2de01826`
Evidence state: complete
Batch result: complete

## Prepared target manifest

| Order | Artifact ID | Kind | Path | Operation | Prior identity | Intended identity | Dependencies | Commit group | Independently valid after commit | Commit point | Entry transition |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `adr-lifecycle-cli` | `adr` | `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` | create | absent | `sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa` | none | `lifecycle-cli-architecture-r1` | no; canonical architecture must reference the decision | ADR file | `authoring` to `review-required` |
| 2 | `architecture` | `architecture` | `docs/architecture/system/architecture.md` | revise | `sha256:8b367791fb90aacd81005c761cc252bcb982e2ef7d48fef436d93c197a254abe` | `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2` | `adr-lifecycle-cli` | `lifecycle-cli-architecture-r1` | yes | canonical Markdown | `authoring` to `review-required` |

Governing inputs: accepted proposal `RL-PROP-CLI-001`, approved spec at the identity above, spec-review r2, architecture assessment r1, canonical architecture baseline, ADR-20260729, ADR-20260810, and ADR-20260515.

The two targets are coupled in one commit group. No diagram target is required because the existing CLI package and repository containers remain structurally accurate; the new responsibility is a Level 2 component and runtime flow inside the existing CLI container.

## Completion

- `adr-lifecycle-cli`: created at its intended identity; entry moved to `review-required`.
- `architecture`: canonical owner pointer, related-artifact registry, Level 2 component, runtime flow, cross-cutting boundary, and ADR index updated at the intended identity; entry moved to `review-required`.
- Preserved partial state: none; both coupled targets completed.
- Blockers: none.
- Next stage: independent `architecture-review`.
