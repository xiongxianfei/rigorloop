# ADR-20260728: Portable Boundary-First Release Manifest and Package Rollback

## Status

accepted

## Context

The portable boundary-first method is published as skill instructions and one
shared packaged reference. The earlier activation design expanded recovery
into repository state transitions, rollback receipts, transaction writers, and
historical content identities. Those mechanisms are unnecessary for publishing
skills and conflict with the approved two-state, release-scoped contract.

## Decision

Keep the existing canonical reference and deterministic skill-local
projections.

Use `specs/boundary-first-activation.yaml` as one small reviewed release
manifest. It records:

- contract version and `pending` or `active` state;
- immutable activating and rollback release tags;
- the ten governed skills;
- canonical reference and projection identities;
- the full parent commit identity used as the grandfathering baseline; and
- the sorted grandfathered feature-spec path inventory.

Pending state uses `-` for the two release tags and baseline revision. Active
state requires all three values.

The activating change derives grandfathered paths only from its parent
revision. Source control owns that historical identity; the manifest does not
copy historical file hashes or maintain an attestation log.

Activation is an ordinary reviewed source change after the existing reference,
skill, generated-package, adapter, and clean-install checks pass. No activation
writer is introduced.

Rollback validation selects the manifest's rollback release and reads the
existing adapter artifact metadata at
`docs/reports/adapter-artifacts/releases/<version>.yaml`. It verifies one
passing archive identity for every adapter in `dist/adapters/manifest.yaml`.
The validation is read-only. An authorized release operator owns any external
installation or publication.

No rollback state, transaction receipt, rollback writer, historical
attestation store, or repository mutation protocol is part of this
architecture.

## Alternatives considered

### Repository rollback transaction

Rejected because it adds state, recovery, and evidence machinery beyond the
published-skill capability.

### Infer historical specs from the activating worktree

Rejected because specs introduced by the activating change could incorrectly
grandfather themselves.

### Maintain historical file hashes in the activation manifest

Rejected because the immutable source-control baseline already owns historical
content identity.

### Perform external rollback from repository validation

Rejected because package validation and release operation authority are
different trust boundaries.

## Consequences

- The user capability remains the published skill text and packaged reference.
- Activation evidence is one small manifest settled through review.
- Existing source control and release metadata remain the evidence owners.
- Rollback readiness is deterministic without external mutation.
- Older accepted feature specs remain valid without migration.
- Architecture, plan, test spec, and M3 implementation must remove assumptions
  about `rolled-back` state, receipts, writers, and historical attestation.

## Follow-up

- Align the canonical architecture package.
- Revise and review the execution plan and test spec.
- Replace the existing activation validator with the two-state release-manifest
  contract and focused package-rollback validation.
