# ADR-20260726: Stage-Authored Artifact Envelope Transport

## Status

accepted

## Accepted scoped successor

`ADR-20260727-capability-projected-file-change-control` supersedes
only this ADR's unconditional live file-change-probe and v2 current-evidence
clauses. Architecture-review R22 accepted that scoped successor.
This record remains accepted for its read-only child, deny-only handler,
workspace-integrity, stage-authored envelope, and parent-only materialization
decisions.

## Context

The accepted boundary-first behavior architecture assumed that an isolated
stage agent would write its completed lifecycle artifacts directly into the
scenario workspace. Live M2 feasibility work against the pinned Codex
app-server disproved that assumption: the runtime returns schema-constrained
agent messages but does not expose the assumed stage-agent workspace-write
surface.

Restoring harness-authored lifecycle renderers would make examples and
transport code a competing semantic source. Requiring an unavailable direct
write would make the approved proof harness unrealizable. The approved R45
workflow-spec amendment instead separates semantic authorship from physical
materialization and removes all child workspace-write authority.

## Decision

Use `boundary-stage-artifact-envelope-v1` as the only stage-output transport
contract for the boundary behavior harness.

- Child commands and detached descendants receive read-only workspace access
  and no writable root. The parent exact-byte materializer is the sole
  workspace writer.
- One identity-bound `stage-file-change-authorization-policy-v1` configures the
  app-server request handler for the denial probe, materialization canary,
  lifecycle stages, and fresh retries. Every file-change approval request
  receives `decline`; accept decisions and missing or substituted handlers
  fail closed. Reconciliation performs no child turn.
- Preflight and generation independently prove a cause-specific
  request/decline/terminal-`declined` file-change trace plus unchanged
  workspace, in addition to direct and detached-descendant command denial.
- The stage-owning skill authors every semantic byte and returns one
  schema-constrained envelope through the agent-message channel.
- The parent selects and identity-binds the exact artifact policy before the
  turn. The behavior manifest carries `lifecycle-stage-artifacts-v1`; runtime
  preflight separately attests `materialization-canary-v1`.
- The child-runtime adapter captures a bounded candidate-message set, including
  candidates observed before timeout. Raw bytes remain transient and are
  retained only for the sole complete candidate through materialization and
  snapshot capture.
- Before every canary or lifecycle turn, the workspace-integrity guard retains
  one root descriptor and captures a bounded, no-follow baseline. After normal
  completion, or after the exact timed-out child is confirmed stopped and
  reaped, it performs the complete bounded post-turn scan before
  materialization.
- Changed or overflowing workspaces route to `stage-workspace-mutated`;
  unstable, unreadable, raced, unsupported, or otherwise invalid scans route
  to `stage-workspace-inspection-failed`. Both stop before materialization,
  lifecycle publication, or retry and retain only bounded value-free evidence.
- The transport reconciler validates the parent policy, closed envelope shape,
  stage and occurrence, artifact-set variant, exact ordered paths and roles,
  UTF-8, per-artifact and aggregate limits, raw candidate-message byte limit,
  canonical-envelope byte limit, and candidate cardinality. It does not
  interpret or rewrite semantic content.
- Only a complete unchanged workspace observation and one complete valid
  candidate may reach the exact-byte materializer. It writes accepted
  `content_utf8` bytes unchanged
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
  using a separate noncanonical policy and the same workspace-integrity guard.
  Its workspace and semantic bytes are discarded after parent-only exact-byte
  equality is proved; only the bounded pass result and permitted runtime
  observations survive.
- New evidence uses `boundary-runtime-attestation-v2`,
  `boundary-runtime-preflight-v2`, and
  `boundary-behavior-implementation-v2`. The sole supported historical v1
  manifest is an opaque read-only registry entry selected by exact path,
  regular-file kind, and raw-byte identity; it cannot satisfy a current role.
- Immutable publication, publisher locking, lease/receipt recovery, current
  pointer replacement, boundary aggregation, and release activation remain
  unchanged.

The approved workflow specification remains normative. The harness and typed
model are executable projections and fail closed on missing, unknown,
additional, stale, or inconsistent values.

## Alternatives considered

- Keep direct stage filesystem writes: rejected because the supported pinned
  runtime does not expose that capability to stage agents.
- Keep the workspace writable and detect mutation afterward: rejected because
  terminal turn state cannot prove that detached child writers are quiescent
  during the post-turn scan or parent materialization.
- Treat command denial as proof for file-change/apply-patch: rejected because
  the app-server file-change protocol is a distinct authorization surface and
  requires its own cause-specific decline trace.
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
- The standalone harness gains candidate collection, envelope validation, a
  shared deny-only request handler, root-anchored workspace integrity
  inspection, exact-byte materialization, structural content validation, and
  additional value-free observations.
- Feasibility now proves the actual semantic-output-to-byte-materialization
  path, not merely a generic command-level workspace write.
- Tests must cover all artifact variants, raw and canonical equality/overflow
  boundaries, direct/descendant/file-change denial, scan limits and races,
  candidate cardinality and overflow, timeout reconciliation, materialization
  mismatch, content-state mismatch, v2-only current selection, opaque v1
  history, and correction-budget terminal branches.
- No new lifecycle stage, workflow engine, normative renderer, persistence
  surface, or external authority is introduced.

## Relationship

This ADR supersedes:

- only the direct stage-filesystem-write clause in
  `ADR-20260725-boundary-first-proof-modeling`; and
- only the writable-workspace, behavior-output-write-success, and
  isolated-workspace-file-change-permission clauses in
  `ADR-20260726-codex-permission-profile-boundary-harness`.

The replacement is a read-only child profile, deny-only file-change handling,
parent-only materialization, and bounded workspace-integrity inspection.
All other decisions in those ADRs remain accepted.

Architecture-review R18 accepted this decision and activated only the scoped
clause replacements above. This ADR strengthens the runtime permission profile
without changing credential isolation, identity binding, publication,
recovery, or release-activation boundaries.

## Acceptance conditions

- Architecture review confirms the stage owns all semantic bytes.
- Architecture review confirms the adapter owns only bounded capture,
  validation, integrity inspection, exact materialization, and value-free
  observations.
- Architecture review confirms child commands, descendants, and file-change
  protocol handling cannot obtain workspace-write authority.
- Architecture review confirms v2-only current evidence and exact opaque v1
  historical recognition.
- The C4 component view separates candidate collection, transport
  reconciliation, materialization, and lifecycle structure validation.
- The plan and test spec bind every new policy and failure boundary before
  implementation resumes.
