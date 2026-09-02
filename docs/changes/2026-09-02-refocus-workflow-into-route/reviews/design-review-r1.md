# Design Review R1: Refocus Workflow into Route

Review ID: design-review-r1
Stage: design-review
Round: r1
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`, `adr-route-context-and-skill-identity`
Reviewed artifact: design package `architecture`, `spec`, `adr-route-context-and-skill-identity`
Review date: 2026-09-02
Package kind: design
Package members: architecture=docs/architecture/2026-09-02-refocus-workflow-into-route.md, spec=specs/refocus-workflow-into-route.md, adr-route-context-and-skill-identity=docs/adr/ADR-20260902-route-context-and-skill-identity.md
Upstream review ID: proposal-review-r1
Status: approved
Material findings: none
Correction targets: none
Recording status: recorded

## Result

- Skill: design-review
- Review status: approved
- Package members: architecture=`docs/architecture/2026-09-02-refocus-workflow-into-route.md`, spec=`specs/refocus-workflow-into-route.md`, adr-route-context-and-skill-identity=`docs/adr/ADR-20260902-route-context-and-skill-identity.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r1, r1
- Material findings: none
- Correction targets: none
- Recording status: recorded
- Settlement status: pending exact-package CLI settlement
- Open blockers: none
- Immediate next stage: isolated stop after package settlement; Workflow may subsequently route to plan authoring
- Claim limitations: approval grants authority only to this exact Design package and does not authorize implementation or claim final verification, branch, PR, release, or deployment readiness

## Design coherence

The architecture, specification, and ADR form one coherent realization of the accepted proposal. The specification owns observable requirements for the public rename, two-phase read-only workflow context, configuration and path behavior, guide retirement, package migration, active-automation continuity, failure handling, and preserved stage ownership. The architecture realizes them through one CLI projection, bundled defaults plus a closed optional repository override, a route-focused package, stable stored protocol names, coherent adapter migration, and explicit runtime and recovery flows. The ADR records the durable command, configuration, public identity, and persistence-compatibility decisions without settling delivery milestones or internal module decomposition.

The structural/semantic authority split is consistent throughout. Project context exposes bounded candidates without selection; change context exposes exact current facts and structurally permitted operations; route interprets user intent and engineering meaning; the selected stage remains the only semantic artifact owner. Nothing in path resolution or an allowed operation transfers authoring, review, settlement, or repair authority to route or the CLI.

The two-phase command avoids forcing a guessed change identity while preventing the CLI from becoming an autonomous router. Its configuration boundary is deterministic and fail-closed: bundled defaults are explicit, repository overrides are optional and provenance-bearing, and unknown vocabularies, incomplete variables, unsafe paths, collisions, or ambiguity stop without falling back to the retired Markdown guide.

Compatibility is sufficiently resolved for Delivery. The current public package makes a clean `workflow -> route` break with no alias. Installer and validation surfaces diagnose obsolete or mixed current packages. Historical archives and documentation remain unchanged. Stable lifecycle authority `workflow` and persisted `workflow.automation` are explicitly protocol identifiers, so active and resumable v3 occurrences keep their targets, identities, budgets, receipts, and status without a record migration.

The package also preserves progressive disclosure and portability. Governed route uses authoritative CLI facts; automation procedure loads only for its triggered contexts; portable direct use may retain safe explicit paths or published defaults but gains no governed-state claim. Canonical `skills/` ownership and generated-adapter parity remain unchanged.

## Boundary assessment

All eight boundary-first dimensions are classified exactly once. Each applicable dimension defines admitted partitions or transitions, invariants, outcomes, and an owner requirement. The five selected interactions cover the material composed hazards: CLI semantic overreach, unsafe config fallback, rename versus active automation, path resolution versus stage ownership, and stale or partial context. Every behavioral example is governed by linked requirements and boundaries; no example creates normative behavior.

`python scripts/validate-boundary-first.py --check --path specs/refocus-workflow-into-route.md` reports only `BFR-PLAN-PROOF-MISSING`. That is not a Design-package defect: the active v3 order prohibits registering the primary plan until this Design Review is approved. The feature record itself passes the validator's boundary structure and linkage checks. Delivery must allocate correction of this stale validation-order expectation before closeout rather than creating an unauthorized pre-review plan.

## Proposal preservation

The package preserves the accepted clean rename, semantic routing ownership, bounded automation, CLI authority for deterministic facts, removal of `docs/workflows.md` and guide-only resources, stage ownership, Git-native evidence, coherent generated-package migration, obsolete-name diagnostics, and active-run handling. It does not redesign lifecycle stages, create a hosted service, or turn the CLI into a semantic workflow engine.

## ADR assessment

The ADR is necessary because the design creates a new public CLI/configuration boundary and deliberately separates the public skill identity from stable stored protocol identifiers. Its alternatives explain why existing lifecycle context, `rigorloop.yaml`, generated guide compatibility, a public alias, stored-key migration, and autonomous CLI routing were rejected. It agrees with both architecture and specification and leaves implementation allocation to Delivery.

## Independence statement

This review did not author or edit the proposal, architecture, specification, ADR, or authoring evidence after the exact package entered Design Review. It writes only Design Review evidence, the review-log entry, and CLI request artifacts required to record and settle this review.

## No-finding statement

No material finding was identified. The exact package is coherent, bounded, fail-closed, traceable to the accepted proposal, and sufficiently specific to authorize Delivery planning after settlement.

