# Design Review R1: Lightweight Requirement-to-Delivery Model

Review ID: design-review-r1
Stage: design-review
Round: r1
Reviewer: Independent Codex design-review context
Reviewer authority: design-review
Target: design package `architecture`, `spec`
Reviewed artifact: design package `architecture`, `spec`
Review date: 2026-08-30
Package kind: design
Package members: architecture=docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md, spec=specs/lightweight-requirement-delivery-model.md
Upstream review ID: proposal-review-r1
Status: changes-requested
Material findings: RTD-DR1
Correction targets: spec
Recording status: recorded

## Result

- Skill: design-review
- Review status: changes-requested
- Package members: architecture=`docs/architecture/2026-08-30-lightweight-requirement-delivery-model.md`, spec=`specs/lightweight-requirement-delivery-model.md`
- Upstream review ID: proposal-review-r1
- Review ID and round: design-review-r1, r1
- Material findings: RTD-DR1
- Correction targets: spec owned by spec
- Recording status: recorded
- Settlement status: withheld pending exact-package CLI settlement of the changes-requested outcome
- Open blockers: RTD-DR1
- Immediate next stage: specification authoring owner
- Claim limitations: approval grants authority only to this exact design package; it does not authorize implementation or claim verification, branch, PR, release, or deployment readiness

### Finding RTD-DR1

Finding ID: RTD-DR1
Severity: medium
Location: `specs/lightweight-requirement-delivery-model.md`, document preamble before `## Goal and context`
Evidence: The specification contains `Boundary model version: boundary-first-v1` inside its boundary record but omits the required active `boundary_contract: boundary-first-v1` marker near the top of a new feature spec. `python scripts/validate-boundary-first.py --check --path specs/lightweight-requirement-delivery-model.md` fails closed with `BFR-NEW-SPEC-MARKER` and reports that `boundary-first-v1` was expected.
Required outcome: Add the active `boundary_contract: boundary-first-v1` marker in the specification's canonical preamble so the complete boundary record is explicitly activated and the focused validator passes.
Safe resolution path: The specification owner should add only the required marker, record the revised artifact through the lifecycle CLI, run the focused boundary and artifact-lifecycle validators, record the finding disposition and correction return, and request a fresh Design Review of the changed exact package.
needs-decision rationale: none
Finding scope: artifact-local
Affected artifact IDs: spec
Owning stages: spec

## Design coherence

The architecture and specification form one coherent realization of the accepted proposal direction. They keep requirement refinement separate from work decomposition, preserve the many-to-many relationship between system requirements and delivery work, and use existing artifacts without introducing RR, IR, or AR lifecycle entities.

The architecture supports all specified behavior and failure outcomes. Stable SR identities remain the durable traceability join points; the canonical shared reference and skill-local copies preserve package portability; stage-local skills retain authority, routing, correction, and readiness semantics; and existing validation owns structural and package parity while semantic sufficiency remains review-owned.

The specification respects the architecture's repository, packaging, compatibility, privacy, and progressive-disclosure constraints. Its boundary model classifies all eight core dimensions exactly once, defines each applicable boundary once, and selects only requirement-grounded composed hazards. No example creates normative behavior.

## Proposal preservation

The package preserves the accepted challenge, goals, scope, governing principle, and direction. It does not add mandatory hierarchy, lifecycle state, external integrations, machine-readable traceability, or changes to test-specification and Delivery Review authority.

## ADR assessment

No applicable ADR is missing. The package applies the existing skill-local resource and adapter packaging architecture without introducing a new runtime component, deployment boundary, external dependency, persistence mechanism, or irreversible platform decision.

## Independence statement

This reviewer did not author or edit the proposal, architecture, specification, authoring evidence, or workflow routing state.
