# Architecture authoring manifest

Assessment basis: accepted proposal `proposal-review-r1`, active `stage-owned-change-local-v3` context, current governed lifecycle CLI transaction and correction-routing ADRs, current canonical workflow skill/package architecture, and direct inspection of the authored workflow package and CLI context boundary.
Commit group: refocus-workflow-into-route-design-v1
Authoring result: complete

## Target 1

Target ID: adr-route-context-and-skill-identity
Kind: adr
Role: supporting
Prior identity: absent
Path and identity: docs/adr/ADR-20260902-route-context-and-skill-identity.md sha256:f09d242c3d65fc4fd8fcc412d30a880554786fa4b22edd1ec6fff9c329773d5c
Dependencies: accepted proposal and retained lifecycle CLI ADRs
Commit point: complete durable decision covering workflow-context projection, repository configuration, public skill identity, stored-protocol compatibility, alternatives, and consequences
Evidence state: complete

## Target 2

Target ID: architecture
Kind: architecture
Role: primary
Prior identity: absent
Path and identity: docs/architecture/2026-09-02-refocus-workflow-into-route.md sha256:9fc1bd38151f710c036a6466661927c28681f83fe90cea5a8ffcbcb8d7a06a73
Dependencies: accepted proposal and Target 1 decision content
Commit point: independently valid arc42 package covering CLI/route authority, configuration and result boundaries, package migration, active automation continuity, guide retirement, failure behavior, validation, deployment, and rollback
Evidence state: complete

No C4 diagram target is needed because this change modifies a repository protocol and published skill package rather than adding a service, deployable container, network relationship, or runtime process boundary.
