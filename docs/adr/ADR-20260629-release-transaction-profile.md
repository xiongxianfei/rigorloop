# ADR-20260629-release-transaction-profile: Release Transaction Profile Source of Truth

## Status

accepted

## Context

RigorLoop's standing release process already treats routine publish work as an operation with durable release evidence, but recent routine releases exposed avoidable human cost. Version-specific release state was duplicated across package metadata, release evidence, adapter metadata, validation allowlists, tests, shell cases, and Markdown evidence. Missing or stale copies caused repeated release loops, and manually written post-publication evidence failed validator shape requirements such as command strings and hash prefixes.

The approved release transaction automation proposal and spec define a routine-release model: a typed release transaction profile owns routine release state, generated release-prep surfaces derive from that profile, preflight catches cheap deterministic drift before broad verification, and public closeout generates validator-compatible evidence after publication.

This is a durable architecture decision because it changes release source-of-truth ownership, generated-output flow, validation layering, release evidence shape, CI/local release-gate parity, and the boundary between cheap preflight and the full release gate.

## Decision

Use a version-scoped release transaction profile as the source of truth for routine release state:

```text
docs/releases/profiles/<tag>.yaml
```

The profile owns routine release version state, package identity, target set, adapter artifact expectations, publication requirements, evidence classes, validator expectations, generated release-prep surfaces, and timing requirements. Release tooling may read and validate the profile, but scripts are not the source of truth for routine release state.

Release-prep surfaces are classified as:

- profile-owned generated surfaces;
- human-authored profile-checked surfaces;
- historical immutable surfaces.

`prepare-release` generates profile-owned surfaces and marked generated regions from the active profile. It must not overwrite human-authored narrative outside generated regions, generate or rewrite test logic, publish, tag, push, or rewrite historical release evidence.

`release-preflight` owns cheap deterministic local/profile/schema checks before broad release verification. It checks profile completeness, package/profile version agreement, generated metadata pointer drift, unauthorized current-version literals, pending evidence shape, local tag conflicts, reachable remote tag conflicts, and release-output state. It is side-effect-light and is not a substitute for full release verification.

`scripts/release-verify.sh <tag>` remains the authoritative full local release gate. GitHub Actions release workflow behavior should invoke the same repository-owned release verification command set for a given profile. The full gate remains responsible for generated outputs, archive integrity, adapter metadata, package contents, and full validation.

`close-release-publication` is a deterministic rerunnable closeout command. It reads public GitHub release asset metadata and npm registry metadata, runs fresh public `npx` smoke for version and supported target init commands, writes validator-compatible command strings and hash shapes, and fails clearly while public evidence is unavailable.

Routine release timing evidence is recorded as release evidence. First-slice duration targets are warnings or observations, not release-failing budgets.

Special releases remain explicit owner decisions. A release outside the routine boundary must not be forced through routine automation without recorded handling.

## Alternatives considered

### Keep hand-edited release checklists

Rejected because the release retrospective showed that hand-synchronized version literals and evidence fields are the avoidable defect class. More checklist discipline would not remove duplicated state.

### Put profiles under implementation-owned script paths

Rejected for the first slice because the profile is durable release transaction evidence. Keeping it under `docs/releases/profiles/` places the authority next to release evidence and keeps it reviewable without treating scripts as the release state owner.

### Add only release preflight

Rejected as incomplete. Preflight would catch some cheap drift but would still leave routine release surfaces manually duplicated and evidence shape manually drafted.

### Add only evidence templates

Rejected as incomplete. Templates would reduce post-publication evidence-shape loops but would not solve release-version allowlist drift, metadata pointer drift, target fixture drift, or local/CI release gate ownership.

### Parallelize release verification first

Rejected for this decision. Parallelism may reduce wall-clock time later, but it does not remove duplicated release state or late evidence-shape discovery. Timing evidence should be collected before proposing hard runtime optimization.

## Consequences

- Routine releases gain a single durable source of truth for version-specific release state.
- Generated release-prep diffs remain reviewable tracked changes, but their routine content derives from the profile.
- Validators and generators must stay schema-compatible; evidence generation must be tested against pending and published validation.
- Current-version literal auditing becomes part of release drift prevention.
- Preflight reduces fix-and-rerun loops but does not weaken the full release gate.
- Historical release evidence remains immutable by routine release prep.
- Special releases require explicit owner decision rather than implicit generator behavior.
- Timing evidence creates a basis for later parallelism or budget proposals without turning first-slice timing targets into release failures.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Plan implementation slices for release profile schema, generated-surface ownership, `prepare-release`, release preflight, public closeout, local/CI gate parity, and timing evidence.
- Write a test spec after plan-review maps requirements to proof cases.
