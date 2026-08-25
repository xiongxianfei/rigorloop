# Architecture Review R1: Governed Lifecycle CLI Transaction Boundary

Review ID: architecture-review-r1
Stage: architecture-review
Round: r1
Reviewer: Codex independent architecture-review context
Review surface: canonical-architecture-update
Target: `docs/architecture/system/architecture.md` and `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
Reviewed artifact: canonical architecture `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2`; ADR `sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa`
Reviewed repository revision: `18a204bb9fa3d6260b19d45896aaa62e89ac0eec`
Review date: 2026-08-24
Recording status: recorded
Status: changes-requested
Material findings: RLCLI-AR1, RLCLI-AR2, RLCLI-AR3

## Result

- Review status: changes-requested
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/architecture-review-r1.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Open blockers: canonical hash-policy contradiction, unspecified YAML parser boundary, and non-deterministic lock/recovery primitive
- Required updates: apply the three bounded architecture corrections and rereview the complete target set
- Next stage after correction: architecture-review

## Review subject

The exact subject is the canonical architecture package at `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2` together with ADR-20260824 at `sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa`. Existing context and container diagrams remain sufficient because the CLI package is already represented and the change adds an internal Level 2 component rather than another container or external system.

## Governing basis

- Specification: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
- Approving spec review: `spec-review-r2` at `sha256:c004c71183fae1589599952235a8a72a37b93e346e8909d3c21dd24a2de01826`
- Architecture assessment: `architecture-assessment-r1` at `sha256:e873a4a49846ff630c42f3847abee494e730d1c8d15228748ddde2e2c36e1c63`
- Architecture method: `specs/architecture-package-method.md` at `sha256:78a8c2da2f40412cfe0e4bf23a5c80d85ce4da53261d52527252fb4a96239582`
- Authoring manifest: `architecture-authoring-r1` at `sha256:c083e18dd961a83e7dde31675452ba3cfbeead0c00dd1cf1095c339a69be5395`

## Findings

### Finding RLCLI-AR1

Finding ID: RLCLI-AR1
Finding: The canonical architecture simultaneously adopts lifecycle content identities and states that lifecycle validation does not hash governed content.
Location: `docs/architecture/system/architecture.md` lifecycle constraints, unified-workflow component, plan baseline, ADR index, and governed lifecycle CLI boundary
Severity: material
Evidence: Lines matching “not use content hashes,” “do not hash governed content,” “governed-document hashes remain outside,” and ADR-20260813's preserved “no-hash boundary” remain current canonical prose. The new boundary says ADR-20260824 amends that rule, leaving consumers with conflicting current instructions.
Required outcome: Make every current canonical hash statement compatible with the new scoped rule: exact identities govern supported CLI freshness and revisions after activation, while actor attribution and unrelated historical plan identity remain excluded.
Safe resolution path: Qualify the legacy validation and plan statements, update the ADR-20260813 summary to note the later amendment, and retain explicit no-attribution and fresh-checkout boundaries.
Recommendation: Treat ADR-20260824 as a narrow successor for hash and direct-write mechanics and make the canonical package unambiguous.
Affected targets: `architecture`

### Finding RLCLI-AR2

Finding ID: RLCLI-AR2
Finding: The design does not choose how the dependency-free Node package safely parses and serializes the repository's YAML lifecycle schema.
Location: ADR-20260824 Decision; canonical `Level 2 White-Box: Governed Lifecycle CLI`
Severity: material
Evidence: The existing package has no YAML dependency, while `change.yaml` includes nested mappings, arrays, scalars, and compatibility forms. The decision assigns snapshot normalization and deterministic candidate serialization to the Node engine but neither chooses a reviewed parser dependency nor defines a supported restricted YAML grammar. Calling Python would also undermine the declared single-engine boundary.
Required outcome: Select one parsing and deterministic serialization boundary, including dependency ownership, supported YAML domain, unknown or unsupported construct behavior, comment/format preservation expectations, and security controls.
Safe resolution path: Adopt one pinned package-local YAML parser justified under the constitution's dependency rule, reject aliases/custom tags/duplicate keys and unsupported constructs, normalize into a closed internal model, and serialize deterministic UTF-8/LF block YAML without promising formatting preservation.
Recommendation: Record this choice in the ADR and canonical component before planning module work.
Affected targets: `architecture`, `adr-lifecycle-cli`

### Finding RLCLI-AR3

Finding ID: RLCLI-AR3
Finding: “Exclusive create or equivalent lock” leaves the transaction and recovery protocol with multiple observably different implementations.
Location: ADR-20260824 Decision; canonical lifecycle component and runtime flow
Severity: material
Evidence: The architecture requires same-worktree serialization and crash recovery but does not fix the lock path, acquisition primitive, stale-lock treatment, recovery-bundle path, phase vocabulary, or ordering between recovery reconciliation and lock acquisition. Those choices determine whether two writers can both proceed and whether a crashed process can be recovered deterministically.
Required outcome: Define one first-release lock and recovery protocol with repository-relative naming, closed phases, acquisition and refusal rules, stale-lock behavior, durable write order, startup order, and cleanup conditions.
Safe resolution path: Use atomic exclusive creation of fixed sibling lock and recovery-bundle paths, never steal a lock based on elapsed time, inspect recovery before normal commands under the acquired lock, define closed `prepared` and `replaced` phases, and require explicit owner action for an unverifiable live-or-stale lock.
Recommendation: Keep cross-branch behavior outside scope but make same-worktree execution deterministic and fault-injectable.
Affected targets: `architecture`, `adr-lifecycle-cli`

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Specification alignment | concern | Core operation and responsibility split aligns, but contradictory canonical hash policy weakens R17-R18 and R27. |
| Ownership and coupling | pass | One engine, CLI transaction adapter, semantic skills, workflow routing, and Git history are distinct. |
| Runtime and recovery | block | The lock and recovery protocol is not uniquely implementable. |
| Data and persistence | block | YAML parsing/serialization and accepted input domain are undecided. |
| Compatibility | concern | Validator convergence is well staged; canonical legacy hash prose is contradictory. |
| Security and privacy | concern | Path and diagnostic constraints are sound, but parser alias/tag/duplicate-key behavior is unspecified. |
| Testability | block | Lock, recovery, and YAML-domain fixtures cannot target one required implementation. |
| Complexity discipline | pass | One engine and staged retirement avoid a second public workflow system. |
| ADR quality | concern | Durable direction is sound; two crucial implementation-boundary alternatives remain unchosen. |

## Prepared settlement manifest

Manifest ID: `architecture-review-r1-settlement`
Manifest state: complete
Review subject identity: `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2+sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa`
Governing basis identity: `architecture-assessment-r1/spec-review-r2/spec-sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`

| Order | Target | Kind | Path | Content identity | Authoring evidence | Pre-state | Disposition | Expected post-state | Progress |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `adr-lifecycle-cli` | ADR | `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md` | `sha256:08cd57ab1198ad0fc4b8de9a1faafc43a0ffa2510fe31dee30cb54469211d6fa` | `architecture-authoring-r1` | `review-required` | changes-requested | `revision-required` | complete |
| 2 | `architecture` | canonical architecture | `docs/architecture/system/architecture.md` | `sha256:badf904a6b8996e3c386a068325fe373715e99fe2d56bf8dc052721bbff00ce2` | `architecture-authoring-r1` | `review-required` | changes-requested | `revision-required` | complete |

Settlement result: `settled`. Both exact targets moved to `revision-required`; workflow routing was unchanged.

## Claim limitations

This review does not approve architecture, settle the ADR as accepted, authorize planning, establish test-spec readiness, or claim implementation, verification, branch, CI, or PR readiness.
