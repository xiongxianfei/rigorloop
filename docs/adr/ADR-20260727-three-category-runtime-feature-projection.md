# ADR-20260727: Three-Category Runtime Feature Projection

## Status

accepted

## Context

The accepted capability-projected file-change-control ADR modeled each runtime
feature as either a permitted tool or required-disabled behavior.

M2 preflight against the exact reviewed Codex 0.145.0 implementation disproved
that binary partition. The runtime reports three permitted command tools, four
enabled behaviors already classified as permitted non-tool runtime behavior,
and 89 disabled tool-bearing features. Treating the four non-tool behaviors as
tools would widen child capability; treating them as required-disabled would
reject the safe observed runtime.

The approved R53 workflow specification resolves the contract gap without
weakening the read-only child or parent-only materialization boundary.

## Decision

This ADR supersedes only the binary feature-partition clauses of
[`ADR-20260727-capability-projected-file-change-control`](ADR-20260727-capability-projected-file-change-control.md).
All runtime-byte binding, capability-state, handler-conformance, evidence-v3,
opaque-v1, and unsupported-v2 decisions in that ADR remain accepted.

Every runtime projection contains three pairwise-disjoint exhaustive feature
collections:

```text
permitted_tool_features
permitted_non_tool_features
required_disabled_features
```

Each collection equals its corresponding complete feature-classification
category. Count-preserving category swaps fail before `thread/start`.

The first projection is an eleven-field row containing three permitted tools,
four permitted non-tool behaviors, and 89 required-disabled tool-bearing
features. Its canonical identity is:

```text
sha256:ab6416627d461e3f11a2bc0d16d465ae8601478a8d085b64e86a6945931a4624
```

Permitted non-tool behaviors may remain enabled but never enter the
effective-tool projection. That projection contains only
`permitted-built-in-tool` and
`must-be-disabled-tool-bearing-behavior` rows. Every required-disabled feature
must be disabled, every permitted tool required by the projection must be
enabled, and any observed file-change event under
`not-exposed-projection` remains projection drift.

Current attestations and manifests remain v3. Adding the third collection
changes the runtime-projection identity but does not reinterpret historical
evidence created under another identity.

## Consequences

- Runtime compatibility is based on exact implementation and capability
  projection, not Codex version alone.
- Safe enabled non-tool behavior no longer causes false blocking.
- Non-tool behavior cannot be mislabeled as executable tool authority.
- The typed registry and proof map require pairwise category-swap regressions.
- Architecture, plan, test-spec, implementation, and evidence identities must
  synchronize before M2 resumes.

## Alternatives considered

- Keep the binary partition and disable the four non-tool behaviors: rejected
  because the exact runtime reports them enabled despite the generated
  configuration, producing false blocking without reducing tool authority.
- Classify the four behaviors as permitted tools: rejected because that would
  widen the executable-tool claim beyond the runtime-owned inventory.
- Trust the Codex version and special-case the four names in behavior code:
  rejected because version is not an implementation identity and hidden
  exceptions would bypass the normative projection.
- Rewrite the accepted predecessor ADR: rejected because accepted decision
  history is append-only evidence.

## Supersession

This ADR supersedes only the binary-partition clauses of
`ADR-20260727-capability-projected-file-change-control`.

## Follow-up

- Accept this ADR only after a clean architecture review.
- On approval, normalize this ADR from `proposed` to `accepted` and the
  canonical architecture from `draft` to `approved` in the same handoff.
- Preserve the predecessor ADR as accepted historical evidence; do not rewrite
  its binary-partition decision.
- Synchronize the active plan and test spec to approved spec-review R53, this
  ADR, the approved architecture identity, and the eleven-field projection
  identity.
- Synchronize implementation and v3 evidence selectors to those identities
  before M2 resumes.
