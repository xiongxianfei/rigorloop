# Usability-First Boundary-First v0.4.0 Architecture Review R2

Review ID: architecture-review-r2
Stage: architecture-review
Round: 2
Reviewer: Codex independent architecture-review peer
Target: docs/architecture/system/architecture.md;
docs/architecture/system/diagrams/component-boundary-guidance.mmd;
docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md
Review date: 2026-08-06
Status: approved
Material findings: none
Immediate next stage: plan
Automatic downstream handoff: none

## Result

- Review surface: `canonical-architecture-update`, `ADR`
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r2.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#architecture-review-r2`
- Open blockers: none
- Required canonical updates: none
- Required ADR updates: none
- Next stage: plan, without automatic handoff from this isolated review.

## Review inputs

- Constitution: `CONSTITUTION.md`
- Repository instructions: `AGENTS.md`
- Architecture method: `specs/architecture-package-method.md`
- Accepted proposal: `docs/proposals/2026-08-06-usability-first-boundary-release.md`
- Approved specification: `specs/usability-first-boundary-release.md`
- Approved spec review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r3.md`
- Architecture authoring evidence: `docs/changes/2026-08-06-usability-first-boundary-release/evidence/architecture-authoring.md`
- Canonical architecture: `docs/architecture/system/architecture.md`
- Component diagram: `docs/architecture/system/diagrams/component-boundary-guidance.mmd`
- Proposed ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
- Prior architecture review: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r1.md`
- Related ADRs: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`, `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`, and `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`

## Findings

None.

## Prior finding reconciliation

### UBR-AR1-001 - resolved

The revised architecture names `scripts/boundary_first_validation.py` as the owner of the repository-internal `derive_grandfathered_specs(root, baseline_revision)` function. The callable accepts a repository root and exact 40-character lowercase reviewed commit identity and returns `(sorted_paths, issues)`. The package and ADR define successful output, raw-UTF-8-byte ordering, bounded invalid/unavailable/malformed/unreadable failures, no-write behavior, one-time activation implementation use, regression-fixture ownership, and the prohibition on normal `--check` invocation.

This closes the R1 ambiguity without adding a CLI, writer, script, lifecycle stage, state store, release path, or recurring user action. Planning can now treat placement and invocation as settled rather than making an architecture decision.

## Review dimensions

| Review dimension | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | UBR-R001 through UBR-R020 map to automatic concise skill behavior, declarative activation snapshots, explicit one-time baseline derivation, exact custom-path retirement, routine release, and immutable rollback. |
| Package shape | pass | Lifecycle metadata precedes all 12 arc42 sections, canonical truth remains in the package, the focused component diagram is linked source, and the durable decision is recorded in ADR-20260806. |
| Boundary clarity | pass | Skill instructions, resource projection, authoring-only inventory derivation, current-file validation, routine release, and public services have distinct owners and flows. |
| Data ownership | pass | The activation YAML owns the frozen snapshot; the internal function only derives one authoring value; projection and release state remain with their established owners. |
| Interface safety | pass | The internal callable has exact inputs, outputs, ordering, bounded failure behavior, no-write semantics, and no public CLI compatibility obligation. |
| Runtime and failure handling | pass | Invalid authoring input returns bounded issues; checked-revision failures identify current-file divergence; partial publication retains rerunnable closeout and immutable fix-forward recovery. |
| Deployment and execution boundaries | pass | No new runtime or infrastructure is introduced; derived packages remain proof, and trusted GitHub/npm publication stays in the routine release workflow. |
| Security/privacy | pass | The helper reads local Git objects without credentials or network access, local validation emits bounded identities, and public credentials remain in trusted release execution. |
| Quality and operations | pass | Scenarios cover concision, package parity, baseline reproducibility, local/public claim separation, routine release, partial failure, and rollback. |
| Testing feasibility | pass | Unit fixtures can exercise the callable contract, integration proof can freeze its successful result, and system validation can prove that normal `--check` succeeds without history or baseline reachability. |
| Complexity discipline | pass | The design reuses one module and one existing validator while adding no command, writer, service, schema, or custom publication mechanism. |
| ADR quality | pass | Context, decision, exact callable contract, alternatives, consequences, supersession, and follow-up are complete and consistent with the canonical package. |
| Plan readiness | pass | No unresolved product, behavior, placement, interface, migration, security, or release-ownership decision remains. |

## Package sufficiency

The unchanged system context and container views remain credible because actors, external systems, credentials, and top-level repository containers do not change. The focused component diagram is the correct lowest affected C4 level and now shows the read-only inventory helper separately from activation authoring and checked-revision validation. No deployment diagram is needed because the design removes a custom publication path and reuses the existing release deployment boundary.

The canonical package retains every required arc42 section in order. Runtime, deployment, crosscutting, decisions, quality scenarios, risks, and glossary all describe the changed behavior at an appropriate level without turning architecture into an execution plan.

## Decision and ADR reconciliation

- `ADR-20260806` supersedes the unpublished custom candidate/atomic-publication decision without rewriting `ADR-20260805`.
- Checked-revision snapshots amend only the transition/tag-derived local activation semantics of `ADR-20260728`; the single manifest, frozen compatibility inventory, immutable rollback, and external release boundary remain intact.
- Instruction-owned automatic behavior and projection parity remain compatible with `ADR-20260729`.
- The internal derivation function is an implementation-owned read-only authoring interface, not a new public CLI or competing state owner.

## Routing and readiness

The canonical architecture is approved and ADR-20260806 is accepted. The design is ready for plan authoring. This direct architecture review is isolated and does not start planning automatically.
