# Architecture Review R1 - Validation Idempotency and Cache-Hit Safety

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review
Target: docs/architecture/system/architecture.md; docs/architecture/system/diagrams/container.mmd; docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md
Reviewed artifact: docs/architecture/system/architecture.md
Review date: 2026-05-23
Recording status: recorded
Status: approved

## Result

- Review surface: canonical-architecture-update and ADR
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md`
- Review resolution: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md#architecture-review-r1`
- Open blockers: none
- Required canonical updates: none
- Required ADR updates: none
- Next stage: plan

## Scope

Reviewed the canonical architecture update, container diagram update, and ADR for the approved validation idempotency and cache-hit safety spec.

Review inputs:

- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- `specs/validation-idempotency-and-cache-hit-safety.md`
- `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/spec-review-r2.md`
- `docs/architecture/system/architecture.md`
- `docs/architecture/system/diagrams/container.mmd`
- `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`

This review is isolated. It does not automatically hand off to planning.

## Review Surface

Review surface: `canonical-architecture-update` plus `ADR`.

The change updates the canonical arc42 package, container diagram, and durable ADR for first-slice validation cache hits on unchanged explicit-path lifecycle validation inputs. No change-local architecture delta is required because current architecture truth is recorded directly in the canonical package.

## Findings

No material findings.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Spec alignment | pass | The architecture matches the approved spec: first-slice caching is limited to `validate-artifact-lifecycle.py --mode explicit-paths`; cache hits require previous pass plus matching command, input, implementation, and policy hashes; Workstream B remains gated. |
| Package shape | pass | Current architecture truth is in the canonical architecture package, the diagram remains separate Mermaid source, and the durable validation-cache decision is recorded in an accepted ADR. |
| Boundary clarity | pass | The Building Block View keeps cache-key computation and validation idempotency inside validation/generation scripts while separating untracked local cache state from tracked change-local evidence. |
| Data ownership | pass | The architecture distinguishes local execution cache, `validation-cache-evidence.yaml`, `validation-cache-measurement.yaml`, compact `change.yaml` evidence kinds, and closeout validation ownership. |
| Interface safety | pass | The design preserves validator semantics, selected checks, exit codes, selector routing, and closeout requirements; cache hits are evidence that a prior pass still applies, not new passes. |
| Runtime and failure handling | pass | Runtime flow covers command/path normalization, unsafe/duplicate path rejection, missing or changed cache components, non-passing prior results, unsupported manifests, and closeout actual-run fallback. |
| Deployment and execution boundaries | pass | The local execution cache is explicitly untracked, branch-local, worktree-local, change-local, non-portable, and not reused in CI or remote/shared cache contexts. |
| Security/privacy | pass | Tracked cache-hit and measurement evidence are constrained to repository-relative paths and exclude secrets, credentials, usernames, hostnames, absolute local paths, and environment dumps. |
| Quality and operations | pass | Quality scenarios and risks cover stale input surfaces, cache evidence mistaken for closeout, local cache leakage, and Workstream B starting without measurement evidence. |
| Testing feasibility | pass | The design maps to cache-key, invalidation, metadata evidence-kind, closeout rejection, measurement file, and actual-run behavior tests named by the approved spec. |
| Complexity discipline | pass | The design adds one bounded cacheable command family and avoids remote cache, fleet-wide cache rollout, changed-path narrowing, and component diagram expansion. |
| ADR quality | pass | The ADR includes status, context, decision, alternatives, consequences, and follow-up; it records a durable decision without duplicating the full canonical package. |
| Plan readiness | pass | No architecture questions block execution planning. |

## C4 And arc42 Checks

- Lifecycle metadata and all 12 arc42 section headings remain present in the canonical package.
- The container diagram remains separate `.mmd` source and now shows the local validation execution cache as untracked local state related to validation scripts and change-local evidence.
- The C4 container level is sufficient because the affected boundary is between validation scripts, local cache state, and change-local evidence, not a new deployment unit or external system.
- No component diagram is required because the Building Block View and Runtime View explain cache helper responsibilities, manifest hashing, formal evidence, closeout behavior, and measurement flow at the needed level.
- No deployment diagram is required because execution remains local repository scripts and existing CI wrapper delegation; the local cache is explicitly non-portable.
- Section 9 links the new ADR with a concise summary.
- Quality, risk, and glossary sections include cache-hit safety, closeout gate safety, local execution cache, formal cache-hit evidence, and validation cache measurement.

## Readiness

Approved for architecture-review purposes.

Immediate next repository stage: plan.

Stop condition: none.
