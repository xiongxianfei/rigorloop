# ADR-20260523-release-process-contract: Standing Release Process and Evidence Boundary

## Status

accepted

## Context

RigorLoop already has lifecycle contracts for proposing, specifying, planning, reviewing, verifying, and publishing specific package versions. It also has release-specific architecture for public adapter releases and the first public npm publication.

What was missing was a standing release-process architecture: a durable boundary for routine publish operations after code, package, adapter, or release-artifact changes are already reviewed and merged. Without that boundary, each publish could be reconstructed from memory, prior PRs, or ad hoc notes, and release evidence could vary by maintainer.

The approved release-process spec defines release publishing as an operation when no new decision is introduced, and as normal lifecycle-managed work when the process, release surface, authentication/provenance path, package identity, adapter target, or publish mechanics change.

## Decision

Adopt a standing release-process boundary for RigorLoop.

Routine publishes execute the standing process and record version-scoped release evidence under:

```text
docs/releases/v<version>.md
```

Routine release evidence is linked from related change records when applicable. It does not update `docs/plan.md` unless the release is part of an active lifecycle plan.

The standing process requires a pre-publish release gate covering source identity, version and dist-tag, release notes or not-required rationale, generated-output currency, package preview, validation, packed install smoke, publish path, and blocker state. Generated-output currency is proven by repository-owned drift or generated-output checks such as `skills.drift`, `adapters.drift`, or current equivalents.

npm publication prefers trusted publishing/OIDC. Manual fallback is allowed for first rollout or approved emergency paths, but it does not relax package preview, evidence, registry verification, or the non-deferred release gate.

Emergency release deferrals are narrow exceptions. A deferral record names the gate item, approving owner or owning stage, rationale, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage. Release evidence creation, secret suppression, source/package/version/dist-tag recording, publish path recording, registry verification, and recovery/follow-up recording are non-deferrable.

Bad published package content recovers through fix-forward, dist-tag correction, or deprecation. Published npm versions are not overwritten.

## Alternatives considered

### Keep releases ad hoc

Rejected. It preserves short-term maintainer speed but leaves release gates, version decisions, package preview, registry verification, and recovery evidence dependent on memory.

### Require full proposal/spec/plan for every publish

Rejected for routine publishes. A routine publish is an operation on already-reviewed work, not a new product or implementation decision. Lifecycle treatment remains required when the release itself introduces a new decision.

### Fully automate releases immediately

Rejected for the first slice. Automation is valuable, but the release contract and evidence boundary must be approved before automation publishes immutable public artifacts.

### Store release evidence only under change records

Rejected. Change-local links are useful when a release is tied to a lifecycle change, but the durable release record is version-scoped and belongs under `docs/releases/`.

## Consequences

- Routine publish operations have a stable architecture boundary and durable evidence record.
- Release-process changes and package-surface changes remain normal lifecycle-managed work.
- The npm registry is treated as a public delivery boundary whose result must be verified after publish.
- Release evidence becomes a security-sensitive artifact and must avoid credentials, OTPs, raw environment dumps, private hostnames, usernames, and machine-local paths.
- Emergency releases have a testable deferral contract instead of a vague gate-bypass label.
- Trusted publishing can be added or hardened without changing the standing release-process shape, as long as auth/provenance policy changes continue through lifecycle review.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Write the test spec for the release-process contract after architecture review.
- Plan implementation slices for release evidence checklist validation, release gate commands, manual fallback documentation, and trusted publishing configuration.
