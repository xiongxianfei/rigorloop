# Architecture Authoring Evidence: Project-Map Skill Simplification

Stage: architecture
Date: 2026-08-14
Artifact ID: `architecture`
Artifact: `docs/architecture/system/architecture.md`
Architecture surface: canonical-update
Completion status: complete

## Upstream settlement

`spec-review-r1` approved the amended `specs/project-map.md` contract at commit `45c71958`, with no material findings and a required bounded architecture update.

## Updated architecture surfaces

- Section 2 records the mapped project-map package, independent operation/scope axes, bounded coordination preflight, PMA0/PMA1 selection, and missing-resource stop.
- Section 5 adds the project-map package responsibility split and the recoverable root-registration-last area transaction.
- Section 6 replaces the old four-mode flow with target-state-bound operation, assembly selection, area commit ordering, and retry behavior.
- Section 8 aligns structural, universal, and conditional procedure ownership.
- Sections 9 and 11 record the no-ADR rationale and the new coordination and partial-write mitigations.

## Architecture decision

No ADR or diagram change is required. The change uses the existing published-skill mapped-resource model, generated package parity, and project-map artifact container; it introduces no new runtime, persistence owner, deployment topology, system container, or independent policy owner.

## Result

The canonical package is ready for independent `architecture-review`. This evidence does not claim architecture approval, planning readiness, test-spec readiness, implementation readiness, verification, or PR readiness.
