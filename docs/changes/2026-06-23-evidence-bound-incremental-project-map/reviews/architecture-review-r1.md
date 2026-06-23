# Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review
Target: docs/architecture/system/architecture.md; docs/architecture/system/diagrams/container.mmd
Reviewed artifact: docs/architecture/system/architecture.md
Review date: 2026-06-23
Recording status: recorded
Status: changes-requested

## Result

- Review surface: canonical-architecture-update
- Review status: changes-requested
- Material findings: PMAP-AR1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md`
- Review resolution: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md#architecture-review-r1`
- Open blockers: PMAP-AR1-F1
- Required canonical updates: align the Building Block View and C4 container diagram treatment of `Project maps`
- Required ADR updates: none
- Next stage: architecture

## Scope

Reviewed the canonical architecture update for the approved `project-map` contract. The review covered the accepted proposal, approved spec, clean spec-review record, architecture method, canonical architecture package, C4 context and container diagrams, and current `docs/project-map.md` orientation state.

This review is isolated. It does not automatically hand off to planning.

## Review Surface

Review surface: `canonical-architecture-update`.

No ADR is under review. The canonical architecture package records that no additional ADR is required because the change applies existing generated-output, published skill resource-integrity, and living-reference workflow decisions to one skill and one packaged skeleton asset.

## Findings

Finding ID: PMAP-AR1-F1
Finding: The Building Block View introduces `Project maps` as a Level 1 container, but the C4 container diagram has no matching container or explicit aggregation.
Location: `docs/architecture/system/architecture.md:242`; `docs/architecture/system/diagrams/container.mmd:9`
Severity: material
Evidence: The Building Block View table adds `Project maps` as a peer container with its own responsibility and source path. The C4 container diagram's repository subgraph lists governance, lifecycle artifacts, token benchmarks, CLI, architecture, change-local evidence, validation cache, templates, skills, scripts, generated runtime mirrors/adapters, release evidence, and legacy architecture archive, but it does not include `Project maps` or state that project maps are intentionally folded into another container.
Required outcome: The canonical architecture package must make the prose and C4 container view agree before downstream planning relies on this architecture update.
Safe resolution path: In the architecture stage, choose one representation and update the canonical package accordingly: either add a `Project maps` container and relevant relationships to `docs/architecture/system/diagrams/container.mmd`, or fold project-map ownership into an existing container row in `architecture.md` with enough rationale that the diagram remains accurate. Then rerun architecture-review.
Recommendation: Treat this as a C4 sufficiency fix, not a new ADR. The owner decision is only whether `Project maps` is first-class at the container level or intentionally represented inside an existing repository container.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Spec alignment | pass | The architecture update reflects the approved `project-map` spec: observation-only role, metadata/freshness, evidence classes, root/area registration, correction notes, command evidence, skeleton packaging, generated adapter inclusion, and deferred artifact-validator scope are represented. |
| Package shape | concern | The review surface is correctly a direct canonical architecture update with no change-local delta and no ADR, but PMAP-AR1-F1 leaves the Building Block View and C4 container diagram inconsistent. |
| Boundary clarity | block | PMAP-AR1-F1 makes it unclear whether project maps are a distinct repository container or an artifact inside an existing container. |
| Data ownership | pass | The update keeps project maps as living references and preserves source/config/schema/test/CI precedence over project-map summaries. |
| Interface safety | pass | The architecture preserves the published skill/customer-project boundary and keeps skeleton policy in `SKILL.md` rather than the copied asset. |
| Runtime and failure handling | pass | Runtime View covers mode classification, placement lookup, dirty baselines, command safety, configured-versus-executed evidence, correction notes, area overlap, and downstream direct-source escalation. |
| Deployment and execution boundaries | pass | The update ties the skeleton asset to existing skill resource-integrity and generated adapter inclusion paths without changing release archive or install architecture. |
| Security/privacy | pass | The update preserves user go-ahead for mutation, network, build, and test-suite commands and does not add secrets, telemetry, or remote indexing. |
| Quality and operations | pass | Quality and risk entries cover downstream reliance safety, source-of-truth confusion, area-map fragmentation, and natural-language validator overfit. |
| Testing feasibility | pass | The first-slice validation boundary maps to contract checks, resource-map/skeleton proof, generated adapter inclusion, representative outputs, behavior-preservation evidence, and cold-read proof. |
| Complexity discipline | pass | The architecture avoids automatic graph generation, runtime tracing, broad fixture requirements, and a dedicated project-map artifact validator before drift evidence exists. |
| ADR quality | pass | No new durable decision requiring an ADR is introduced; the no-ADR rationale correctly points to existing generated-output and resource-integrity decisions. |
| Plan readiness | block | Planning should wait until PMAP-AR1-F1 is resolved and architecture-review reruns cleanly. |

## C4 And arc42 Checks

- Lifecycle metadata and all 12 arc42 section headings remain present.
- The context and container diagrams remain separate `.mmd` source files with C4 role classes and intent-labeled relationships.
- No component diagram is required; the changed behavior is skill/artifact workflow and packaging guidance, not internal component collaboration needing a lower-level view.
- No deployment diagram is required; existing Deployment View prose covers canonical skills, generated output, release archives, and installed target roots affected by the skeleton asset.
- Section 9 states that no ADR is required for the evidence-bound `project-map` update.
- PMAP-AR1-F1 blocks C4 sufficiency until the Building Block View and container diagram agree on the `Project maps` boundary.

## Readiness

Changes requested.

No automatic downstream handoff is performed because this was a direct `architecture-review` request.

Immediate next repository stage: architecture

Stop condition: PMAP-AR1-F1
