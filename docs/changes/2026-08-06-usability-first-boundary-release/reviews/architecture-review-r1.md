# Usability-First Boundary-First v0.4.0 Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex independent architecture-review peer
Target: docs/architecture/system/architecture.md;
docs/architecture/system/diagrams/component-boundary-guidance.mmd;
docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md
Review date: 2026-08-06
Status: changes-requested
Material findings: UBR-AR1-001
Immediate next stage: architecture revision
Automatic downstream handoff: none

## Result

- Review surface: `canonical-architecture-update`, `ADR`
- Review status: changes-requested
- Material findings: `UBR-AR1-001`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#architecture-review-r1`
- Open blockers: `UBR-AR1-001`
- Required canonical updates: define the exact repository-owned, read-only baseline-inventory derivation interface and its ownership.
- Required ADR updates: define the same interface and make clear that checked-revision validation never invokes it.
- Immediate next stage: architecture revision followed by architecture-review R2.

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
- Superseded ADR: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`
- Retained and amended ADRs: `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md` and `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`

## Findings

## Finding UBR-AR1-001

Finding: The architecture requires a pure repository helper to derive the frozen grandfathered-spec inventory from an explicitly supplied baseline revision, but it does not define an exact repeatable interface for that operation.
Finding ID: UBR-AR1-001
Location: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`, Decision paragraph 4 and Alternatives considered; `docs/architecture/system/architecture.md`, Building Block View checked-revision responsibility and Runtime View step 12; `docs/changes/2026-08-06-usability-first-boundary-release/evidence/architecture-authoring.md`, Architecture decision and alternatives
Severity: material
Evidence: UBR-R007 requires activation preparation to receive the exact reviewed pending revision explicitly, derive the complete sorted inventory once, and record both values. Spec-review R3 made the explicit baseline-input mechanism an architecture-readiness condition. The architecture says only that “one pure repository helper” performs derivation and rejects a preparation CLI or writer; it does not name the owning module or callable, define its input and output contract, state its failure behavior, or give a supported read-only invocation. The current validator implementation contains private history-aware derivation behavior, so a plan would have to invent whether to reuse, extract, or replace it. That ambiguity can either reintroduce Git history into ordinary checked-revision validation or produce a one-off manual inventory with no reproducible authoring path.
Required outcome: Define one exact repository-owned, read-only authoring interface that accepts a validated full baseline revision, derives the complete deterministically sorted eligible feature-spec inventory from that revision, performs no writes, reports bounded failures, and is not called by normal `--check` validation. Name its owner and supported invocation or callable contract so planning and tests do not have to choose the mechanism.
Recommendation: Keep the mechanism small by specifying a pure function in the existing boundary-first validation module, with a documented one-time repository invocation recorded in architecture authoring evidence. If maintainers require a stable direct command instead, narrowly permit one read-only derivation command and amend the ADR's blanket rejection of a preparation CLI; do not introduce an activation writer or new lifecycle stage.
Safe resolution path: Amend only the ADR decision and matching canonical Building Block, Runtime, and Crosscutting statements. Preserve the current activation-record shape, current-file-only `--check` behavior, exact custom-path retirement inventory, and routine release ownership.
needs-decision rationale: none; the approved spec already fixes the input, deterministic output, no-write boundary, and later-validation behavior, so architecture only needs to settle placement and invocation.

## Review dimensions

| Review dimension | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Snapshot semantics, checked-revision claims, custom-path retirement, automatic skill behavior, routine release, and rollback align; UBR-R007's exact authoring mechanism remains unsettled. |
| Package shape | pass | The canonical arc42 package retains all 12 sections, uses linked diagram source, records stable ownership, and adds an ADR for the durable decision. |
| Boundary clarity | concern | Runtime validation, activation authoring, and routine release are separated, but the authoring helper boundary is conceptual rather than implementable. |
| Data ownership | pass | The activation record owns the frozen snapshot, resource manifest owns projections, skills own automatic behavior, and release profiles own publication. |
| Interface safety | block | No supported input/output interface exists for the one operation that constructs the frozen compatibility inventory. |
| Runtime and failure handling | pass | Pending and active snapshots validate independently; malformed or divergent current files fail closed; partial public release remains open and rerunnable. |
| Deployment and execution boundaries | pass | No new service or credential boundary is introduced, and routine GitHub/npm publication remains separate from local checked-revision proof. |
| Security/privacy | pass | Local validation needs no credentials or network and evidence excludes secrets and machine-local identity data. |
| Quality and operations | pass | Quality scenarios cover concise skill use, coherent snapshots, local/public claim separation, routine release, partial failure, and immutable rollback. |
| Testing feasibility | block | Tests cannot bind UBR-R007 to a stable authoring interface until architecture names the owner and contract. |
| Complexity discipline | pass | The design removes the custom publisher and candidate protocol while retaining only a declarative record, focused validator, skill instructions, and routine release. |
| ADR quality | concern | Context, selected direction, alternatives, consequences, and supersession are clear; the chosen derivation mechanism is not exact enough to implement. |
| Plan readiness | block | Planning would have to make an architecture decision about helper placement and invocation. |

## Package sufficiency

The unchanged context and container diagrams are justified because actors, external systems, credentials, and top-level repository containers do not change. The updated boundary-guidance component diagram is the lowest affected C4 level and correctly shows baseline input, activation authoring, current-file validation, routine release, and public systems. No deployment diagram is required because the change removes a custom publication path and reuses the documented routine release boundary.

The canonical package is otherwise internally coherent: the activation record is declarative rather than transactional, public claims remain outside local validation, automatic behavior is instruction-owned, frozen inventory preserves historical compatibility, and routine release retains the existing recovery model.

## Decision and ADR reconciliation

- `ADR-20260806` correctly supersedes the unpublished candidate/atomic-publication decision in `ADR-20260805` without rewriting the historical record.
- Its checked-revision snapshot semantics are compatible with the retained single-manifest and immutable rollback parts of `ADR-20260728`.
- Its instruction-owned automatic behavior and projection parity are compatible with `ADR-20260729`.
- The only blocking inconsistency is internal to the new decision: it promises deterministic baseline derivation while rejecting a new command and leaving the surviving interface unnamed.

## Routing and readiness

Architecture and ADR settlement are `revision-required`. The architecture author should resolve UBR-AR1-001, rerun authoring validation, and request architecture-review R2. This direct review is isolated and does not start revision or planning automatically.
