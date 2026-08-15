# Architecture Assessment: Proposal Skill Simplification

Assessment: architecture-not-required

## Rationale

The approved specification adds two mapped procedure references inside the existing `proposal` skill root and revises one existing structural asset without changing the published-skill package model. Canonical source remains under `skills/`; references remain package-owned procedure; the asset remains a structural leaf; and canonical, generated, packed, archived, release-candidate, and installed resources retain the existing path and raw-byte parity contract.

The change preserves the existing lifecycle ownership model. Workflow owns stale-attempt validation, no-reliance judgment, authorization evidence, and routing while proposal remains the only writer of its proposal entry and proposal-authored evidence. `authoring-reset-required` is a transaction result rather than a lifecycle state, and the authorization handshake reuses workflow-owned transition evidence rather than adding a persistence mechanism or evidence type.

The change introduces no runtime, service, API, dependency, deployment topology, security boundary, package transformation, lifecycle state, persistence owner, or validator family. No canonical architecture document, diagram, ADR, architecture artifact, or architecture review is required.

## Reassessment triggers

Reassess as `architecture-required` if implementation proposes direct workflow mutation of proposal-owned state, a new lifecycle state, a new persisted authorization or reset record type, independent policy ownership for either reference, another structural asset, a package transformation, a runtime classifier, or a new validator family.

## Result

Proceed directly to `plan` and `plan-review`. Architecture authoring and `architecture-review` are not applicable to the approved scope.
