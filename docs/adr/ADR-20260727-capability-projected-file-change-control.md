# ADR-20260727: Capability-Projected File-Change Control

## Status

proposed

## Context

The accepted stage-envelope architecture required every supported runtime to
produce a live app-server file-change request, receive a parent decline, and
finish the item as declined.

M2 feasibility proved that Codex 0.145.0 exposes only the three approved
command features under the identity-bound read-only configuration. Enabling
candidate apply-patch flags did not enable those feature rows or expose a
file-change operation. A prompt cannot prove an unavailable operation by
failing to invoke it.

Removing the file-change control would weaken the parent-only materialization
boundary. Pinning only a runtime version would also be insufficient because
different implementation bytes can retain the same declared version, schemas,
and feature rows.

## Decision

Use one immutable typed runtime-projection registry as the executable
projection of the approved workflow specification.

Each projection binds:

- projection ID and exact runtime version;
- exact launcher and runtime-package byte identities;
- generated-schema identity;
- complete protocol-item and feature-classification identities;
- the exhaustive permitted-tool and required-disabled feature sets; and
- one closed file-change capability state.

The complete row has a canonical content identity. Selection requires one
unique exact match across all implementation and declaration identities.
Unknown fields, duplicate IDs or selection keys, identity disagreement, or
changed launcher/package bytes fail before `thread/start`.

File-change proof is capability-state-specific:

- `exposed-live-probe-required` requires the correlated
  request/decline/terminal-`declined` trace and unchanged workspace;
- `not-exposed-projection` forbids asking the model to invoke an absent
  operation and instead requires the exact reviewed runtime projection, every
  required-disabled feature disabled, a complete invocation-owned
  effective-tool projection, a fresh invocation-owned deny-handler
  conformance result, and rejection of any observed file-change event as
  projection drift.

The same identity-bound deny-only handler remains installed before every
canary, lifecycle, and retry thread. Its conformance policy proves the matching
decline and the complete missing, malformed, mismatched, widened, accepted,
and session-accepted negative set against the actual dispatch and validation
functions.

New evidence uses:

- `boundary-runtime-attestation-v3`;
- `boundary-runtime-preflight-v3`; and
- `boundary-behavior-implementation-v3`.

The exact registered v1 manifest remains opaque read-only history.
No durable v2 evidence was published, so all v2-labeled data is unsupported
historical evidence and cannot satisfy a current role or be upgraded.

The workflow specification remains normative. The typed Python registry,
effective-tool projection, handler-conformance runner, and diagnostic maps are
immutable executable projections with exhaustive conformance tests.

## Alternatives considered

- Keep retrying prompts until a file-change event appears: rejected because
  model behavior cannot make an unavailable tool exist and event absence is
  not enforcement proof.
- Remove file-change handling: rejected because a later or drifting runtime
  could expose a path around parent-only materialization.
- Select by version only: rejected because version declarations do not bind
  implementation bytes.
- Select by schemas and feature flags without runtime bytes: rejected because
  tool-exposure code may change without changing those declarations.
- Treat repository unit tests as runtime proof: rejected because the proof
  must be fresh and invocation-owned.
- Add a runtime-specific branch directly in orchestration code: rejected
  because reviewed immutable projections provide a closed compatibility
  boundary and make future support additive.

## Consequences

- A runtime upgrade, reinstall with different package bytes, or changed
  launcher requires a separately reviewed projection row before canonical
  behavior generation can proceed.
- The first projection is intentionally exact rather than portable across
  unreviewed package or platform variants.
- Non-exposure proof is more expensive than checking feature flags alone but
  remains bounded and does not depend on model compliance.
- The handler remains deny-only even when the selected runtime exposes no
  file-change operation; a contradictory event stops the turn.
- Architecture, plan, test spec, code, and durable evidence must move together
  from v2 assumptions to v3.

## Supersession

On acceptance, this ADR supersedes only:

- the unconditional live file-change-probe clause in
  `ADR-20260726-stage-authored-artifact-envelope-transport`; and
- that ADR's v2 current-evidence clauses.

It preserves the accepted read-only child boundary, deny-only policy,
workspace-integrity gate, stage-authored envelope, parent-only exact-byte
materialization, and scoped relationship to predecessor ADRs.

Until architecture review accepts this ADR, the predecessor clauses remain the
accepted architecture and implementation remains blocked.

## Acceptance conditions

- Architecture review confirms the registry row binds exact runtime bytes and
  all capability declarations.
- Architecture review confirms neither feature flags nor event absence alone
  can prove non-exposure.
- Architecture review confirms handler conformance is fresh,
  invocation-owned, bounded, value-free, and exercises the live dispatch
  implementation.
- Architecture review confirms all v3 identity and migration surfaces are
  consistent.
- Plan and test-spec revisions must map runtime-byte drift, projection
  ambiguity, capability-state proof, handler cases, event drift, and v1/v2/v3
  compatibility before implementation resumes.
