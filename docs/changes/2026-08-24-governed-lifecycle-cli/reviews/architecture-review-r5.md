# Architecture Review R5: Milestone Authority and Replay Persistence

Review ID: architecture-review-r5
Stage: architecture-review
Round: r5
Target: canonical architecture at `sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67`
Reviewed artifact: `docs/architecture/system/architecture.md` at `sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67`
Reviewed artifact path: docs/architecture/system/architecture.md
Reviewed artifact identity: sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67
Governing spec: `specs/governed-lifecycle-cli.md` at `sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82`
Decision basis: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` at `sha256:5917887bf347c2346f7667c38d1763fca2c656e6586538fd0898224c405e3f81`
Reviewer: Codex same-context fresh-assumption formal reviewer
Review date: 2026-08-27
Recording status: recorded
Status: approved
Review status: approved
Material findings: none
Open findings: none

## Result

- Review surface: canonical-architecture-update
- Review status: approved
- Recording mode: formal-lifecycle
- Settlement: exact-target-set
- Execution: manual
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/architecture-review-r5.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: not-required for this no-finding review; the existing resolution remains open for `RLCLI-DEADLOCK-CR1` and `RLCLI-DEADLOCK-CR2`
- Next stage: return control to workflow; implementation only after the correction route returns
- Claim limitation: no implementation, validation, verification, branch, or PR readiness is claimed

## Prepared settlement manifest

Subject: milestone completion/start authority and completion-replay persistence
Basis: approved governed lifecycle CLI specification at `sha256:06e8856209816c1692cc3baab4a41b3936b8118f6be4c668de7a80665f0c1b82`
Target order: architecture
Target architecture kind: architecture
Target architecture role: primary
Target architecture path: docs/architecture/system/architecture.md
Target architecture identity: sha256:78e708c76b5f787e4f54e55d16d7abc827dd16f90ea578b4dec11f06cf93ff67
Target architecture authoring evidence: docs/changes/2026-08-24-governed-lifecycle-cli/evidence/architecture-deadlock-correction-r1.md
Target architecture disposition: approved
Target architecture expected result: approved
Settlement progress: review evidence prepared; CLI recording and settlement pending

## Findings

None.

## Review assessment

- Specification alignment: the two-step completion/start protocol implements R16 and R31 without moving route selection into the CLI.
- Ownership: workflow decides whether to continue; the CLI validates and applies only the selected closed operation; skills retain semantic ownership.
- Persistence: one normalized milestone completion record under the existing `lifecycle_cli.milestones` coordination surface keeps Git-contained reconstruction and does not introduce a second state owner.
- Replay: constituent-level revalidation prevents status-only idempotence while canonical-occurrence hashing avoids false staleness from unrelated review-log appends.
- Failure handling: contradictory routing projections and drifted evidence reject the complete candidate before the transaction adapter persists it.
- Compatibility: existing command names and the single `change.yaml` transaction boundary remain stable; legacy completion records require an explicit deterministic compatibility path in implementation and proof rather than implicit routing repair.
- Testability: the approved T09 proof map directly covers completion without routing, workflow-selected start, synchronized projections, exact replay, evidence omission, constituent drift, unrelated append, and legacy behavior.
- ADR decision: no new ADR is needed because ADR-20260824 already owns closed lifecycle operations, workflow routing ownership, exact evidence identities, deterministic replay, and atomic single-record mutation.

The architecture is coherent and proportionate for the correction. This receipt makes no independent-review claim and does not itself settle the target or advance workflow.
