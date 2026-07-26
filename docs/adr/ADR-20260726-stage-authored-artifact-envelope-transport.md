# ADR-20260726: Stage-Authored Artifact Envelope Transport

## Status

proposed

## Context

The accepted boundary-first behavior architecture assumed that an isolated
stage agent would write its completed lifecycle artifacts directly into the
scenario workspace. Live M2 feasibility work against the pinned Codex
app-server disproved that assumption: the runtime returns schema-constrained
agent messages but does not expose the assumed stage-agent workspace-write
surface.

Restoring harness-authored lifecycle renderers would make examples and
transport code a competing semantic source. Requiring an unavailable direct
write would make the approved proof harness unrealizable. The approved
workflow-spec amendment instead separates semantic authorship from physical
materialization.

## Decision

Use `boundary-stage-artifact-envelope-v1` as the only stage-output transport
contract for the boundary behavior harness.

- The stage-owning skill authors every semantic byte and returns one
  schema-constrained envelope through the agent-message channel.
- The parent selects and identity-binds the exact artifact policy before the
  turn. The behavior manifest carries `lifecycle-stage-artifacts-v1`; runtime
  preflight separately attests `materialization-canary-v1`.
- The child-runtime adapter captures a bounded candidate-message set, including
  candidates observed before timeout. Raw bytes remain transient and are
  retained only for the sole complete candidate through materialization and
  snapshot capture.
- The transport reconciler validates the parent policy, closed envelope shape,
  stage and occurrence, artifact-set variant, exact ordered paths and roles,
  UTF-8, per-artifact and aggregate limits, raw candidate-message byte limit,
  canonical-envelope byte limit, and candidate cardinality. It does not
  interpret or rewrite semantic content.
- The exact-byte materializer writes accepted `content_utf8` bytes unchanged
  below the isolated output root, rereads the complete leaf set, and records a
  value-free identity/count/entry-kind comparison.
- The harness then runs its closed structural lifecycle projections against the
  materialized bytes and records a value-free content-validation observation.
  These checks may reject inconsistent review, finding, resolution, occurrence,
  or content-state records, but may not create or alter judgment.
- Timeout reconciliation uses the retained candidate observation after the
  exact child is confirmed stopped and reaped. One complete valid candidate is
  reconciled without reinvocation; only zero candidates with no independent
  non-output failure permits one fresh-runtime retry. Partial, extra,
  contradictory, malformed, oversized, overflowing, or policy-incompatible
  evidence fails closed.
- The preflight materialization canary executes through `workflow` and `spec`
  using a separate noncanonical policy. Its workspace and semantic bytes are
  discarded after exact-byte equality is proved; only the bounded pass result
  and permitted runtime observations survive.
- Immutable publication, publisher locking, lease/receipt recovery, current
  pointer replacement, boundary aggregation, and release activation remain
  unchanged.

The approved workflow specification remains normative. The harness and typed
model are executable projections and fail closed on missing, unknown,
additional, stale, or inconsistent values.

## Alternatives considered

- Keep direct stage filesystem writes: rejected because the supported pinned
  runtime does not expose that capability to stage agents.
- Have the harness render lifecycle artifacts from stage summaries: rejected
  because transport code would become a competing semantic author.
- Parse unconstrained prose and infer files: rejected because candidate
  identity, completeness, boundaries, and recovery would be ambiguous.
- Let the adapter normalize or repair returned content: rejected because exact
  stage ownership and replayable byte identity would be lost.
- Persist raw failed candidate content: rejected because bounded value-free
  observations provide replayable diagnostics without retaining potentially
  sensitive or untrusted prose.

## Consequences

- Stage skills must support one closed schema output in the isolated behavior
  harness while preserving their normal public artifact responsibilities.
- The standalone harness gains candidate collection, envelope validation,
  exact-byte materialization, structural content validation, and additional
  value-free observations.
- Feasibility now proves the actual semantic-output-to-byte-materialization
  path, not merely a generic command-level workspace write.
- Tests must cover all artifact variants, raw and canonical equality/overflow
  boundaries, candidate cardinality and overflow, timeout reconciliation,
  materialization mismatch, content-state mismatch, and correction-budget
  terminal branches.
- No new lifecycle stage, workflow engine, normative renderer, persistence
  surface, or external authority is introduced.

## Relationship

On acceptance, this ADR supersedes only the direct stage-filesystem-write
clause in `ADR-20260725-boundary-first-proof-modeling`. All other decisions in
that ADR remain accepted.

This ADR refines the child-runtime transport selected by
`ADR-20260726-codex-permission-profile-boundary-harness`. It does not weaken
the runtime permission profile, credential isolation, identity binding,
publication, recovery, or release-activation boundaries.

## Acceptance conditions

- Architecture review confirms the stage owns all semantic bytes.
- Architecture review confirms the adapter owns only bounded capture,
  validation, exact materialization, and value-free observations.
- The C4 component view separates candidate collection, transport
  reconciliation, materialization, and lifecycle structure validation.
- The plan and test spec bind every new policy and failure boundary before
  implementation resumes.
