# Architecture Revision Evidence R1: Governed Lifecycle CLI

Stage: architecture
Transaction ID: architecture-revision-r1
Change ID: `2026-08-24-governed-lifecycle-cli`
Revision authority: accepted findings `RLCLI-AR1`, `RLCLI-AR2`, and `RLCLI-AR3` from `architecture-review-r1`
Evidence state: complete
Batch result: complete

## Target manifest

| Order | Artifact ID | Kind | Path | Operation | Prior identity | Revised identity | Dependencies | Commit group | Entry result |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `adr-lifecycle-cli` | `adr` | `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` | revise | `sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa` | `sha256:9e2ed53a513fe7d1d04c69cfd5044a3aa4f2199e39695849ac7a5d638d6fb78e` | none | `lifecycle-cli-architecture-r2` | `review-required` |
| 2 | `architecture` | `architecture` | `docs/architecture/system/architecture.md` | revise | `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2` | `sha256:911aafdbec7f124d92705dd0364183c7a4a805f8963a359553e17d343d2b3c95` | `adr-lifecycle-cli` | `lifecycle-cli-architecture-r2` | `review-required` |

## Resolution scope

- `RLCLI-AR1`: qualified all current no-hash statements and made ADR-20260824 the narrow successor for activated freshness identities.
- `RLCLI-AR2`: selected the pinned package-local `yaml` dependency, closed the admitted YAML domain, and defined deterministic schema-ordered serialization without formatting-preservation claims.
- `RLCLI-AR3`: fixed lock and recovery filenames, modes, exclusive-create behavior, phases, startup order, refusal behavior, cleanup order, and named orphan-lock repair.

No command, semantic-authority, workflow-routing, deployment, hosted-service, or diagram scope changed. Both coupled targets are ready for independent architecture-review r2.
