# Architecture Revision: Milestone Authority and Replay Persistence

Stage: architecture-assessment
Applicability: required
Spec identity: sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82
Assessment mode: workflow-managed
Route result: architecture-required
Authoring action: canonical-update

## Authoring manifest

Artifact ID: architecture
Artifact kind: architecture
Artifact role: primary
Artifact path: docs/architecture/system/architecture.md
Prior artifact identity: sha256:427828a44dd25d63f18e07c99eb4055330a26961f5de8d8297545a7d6455c6e7
Artifact identity: sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67
Evidence state: complete
Dependency: specs/governed-lifecycle-cli.md at sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82
Commit group: canonical-architecture
Commit point: docs/architecture/system/architecture.md

## Design result

- Workflow owns route selection and the continuation decision; the CLI validates and atomically applies only a closed workflow-selected operation.
- `complete-milestone` closes and reports eligibility without changing routing; `start-milestone` is the separate workflow-selected operation that synchronizes milestone and routing projections.
- `lifecycle_cli.milestones.<milestone-id>` stores a normalized completion-evidence record and fingerprint covering proof, receipt, canonical review-log occurrence, complete packet inventory, review facts, milestone, and authority.
- Replay reconstructs every stored constituent; unrelated review-log appends remain valid because the canonical occurrence, not the whole log, is identity-bearing.
- No ADR revision is required because ADR-20260824 already owns the routing, closed-operation, exact-identity, replay, and transaction boundaries.

## Validation

- `git diff --check -- docs/architecture/system/architecture.md`: passed.
- `python3 scripts/validate-documentation-prose.py --mode audit --path docs/architecture/system/architecture.md`: reported the file's existing broad mechanical-wrap debt; no claim of prose-audit conformance is made by this correction.

This revision is ready for architecture-review and does not claim architecture approval, implementation readiness, verification, branch readiness, or PR readiness.
