# ADR-20260824: Governed Lifecycle CLI Transaction Boundary

## Prospective supersession

After coherent activation of `compact-current-state-v1`, ADR-20260903 supersedes this decision where it limits persistence to `change.yaml`, requires committed procedural evidence, or treats Git, branches, or PR state as a correctness dependency. Registered non-compact changes continue under this ADR. The compact successor retains the pure semantic engine, exact identities, optimistic concurrency, fail-closed parsing, local lock and recovery boundary, and the rule that the CLI validates responsibility but grants no permission.

## Owning change record

`docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`

## Context

RigorLoop's stage-owned lifecycle model makes `change.yaml` the sole mutable governed-state snapshot and assigns narrow transition authority to stage peers. Today, skills and workflow instructions also implement the mechanics of discovering state, checking evidence, selecting fields, serializing YAML, and settling transitions. Existing Python validators detect invalid combinations, while the Node `rigorloop` package exposes scaffolding and installation commands. No executable boundary yet owns guarded lifecycle mutation across humans, skills, adapters, workflow, and CI.

The approved governed-lifecycle CLI specification requires semantic operations, exact artifact and evidence identities, effective-state interpretation, optimistic concurrency, deterministic output, crash recovery, migration, and phased enforcement. It also requires skills to retain semantic judgment and authority limits while removing mechanical lifecycle procedure.

This decision revises the no-hash and direct-peer-write details of ADR-20260729 only for supported governed lifecycle operations after activation. It retains that ADR's single `change.yaml` state owner, stage authority partition, workflow routing ownership, repository-local operation, evidence-first review, and external-action boundary.

## Decision

Extend the existing `@xiongxianfei/rigorloop` package with a `rigorloop lifecycle` command family backed by one pure lifecycle engine. The engine is the canonical interpreter for supported governed state. CLI handlers perform repository discovery, request parsing, filesystem transaction work, and human or JSON rendering; they do not reimplement transition policy.

Place the engine in package-local modules with four inward-facing boundaries:

1. A repository snapshot reader normalizes one selected change record, referenced artifact identities, review and resolution facts, schema compatibility, and explicit dependency edges into immutable input.
2. A pure interpreter derives recorded, evidence, and effective state, blockers, permitted operations, context, lifecycle revision, and stable diagnostics from that snapshot.
3. A pure transition evaluator accepts a versioned semantic request plus the expected lifecycle revision and returns either a rejected result or a deterministic candidate `change.yaml`. It has no filesystem access and no arbitrary field setter.
4. A transaction adapter validates the candidate, persists a same-directory recovery bundle, replaces only `change.yaml`, verifies the persisted result, restores prior bytes on failure, and exposes only the named interrupted-replace reconciliation path when recovery cannot complete automatically.

Use the maintained `yaml` npm package as the package-local parser dependency and pin its resolved version through the npm lockfile. This dependency is justified because governed records already use nested YAML mappings and sequences, and a bespoke parser would create an incomplete schema and unsafe ambiguity around duplicate keys, aliases, tags, and scalar typing. The snapshot reader accepts only the documented lifecycle-schema subset: string-key mappings, sequences, booleans, null, finite numbers where the schema admits them, and strings. Duplicate keys, aliases, anchors, merge keys, custom tags, non-finite numbers, multiple documents, unsafe paths, and unsupported node kinds fail before interpretation. The engine normalizes parsed data into a closed internal model and uses one explicit schema-ordered serializer for deterministic UTF-8/LF block YAML; it does not promise to preserve comments, quoting, key order outside the schema, or other source formatting during mutation. Read-only diagnostics do not rewrite files.

The lifecycle revision is SHA-256 over a versioned canonical serialization of mutation-relevant `change.yaml` data plus the sorted repository-relative path and SHA-256 identity of every referenced artifact or evidence item that can change effective state. Provenance fields explicitly excluded by the schema are omitted. The exact canonicalization and exclusion list are versioned test fixtures and part of compatibility.

`change.yaml` remains the only Git-tracked mutable lifecycle snapshot. Each change directory uses the fixed transient siblings `.rigorloop-lifecycle.lock` and `.rigorloop-lifecycle-recovery.json`; neither is Git-tracked truth or needed after a fresh checkout. Lock acquisition is an atomic exclusive file create with mode `0600`. The lock records schema version, change ID, process ID, random transaction nonce, and start time for diagnostics, but elapsed time never authorizes automatic lock theft. A demonstrably live owner yields `RL_OPERATION_BUSY`; an absent or unverifiable owner yields `RL_RECOVERY_REQUIRED` and requires the named `clear-orphaned-lock` repair after current-revision validation and recovery reconciliation.

Mutation acquires the lock before recovery inspection. The recovery bundle is then created exclusively with mode `0600`, contains the prior bytes, prior and candidate identities, transaction nonce, and exactly `prepared` or `replaced`, and is durably synced before replacement. A `prepared` bundle plus prior bytes is abandoned safely; a bundle plus candidate bytes is treated as replaced even if the phase update was interrupted. After replacement the adapter records `replaced`, verifies the complete state, and either removes the bundle on success or restores and verifies prior bytes before cleanup. Unknown identities, failed restoration, malformed transient state, or nonce disagreement remain blocked. Cleanup removes the recovery bundle before the lock. `validate` may inspect transient state without mutation; normal mutation and reconciliation require the lock. `clear-orphaned-lock` never changes `change.yaml`, refuses a demonstrably live owner, and runs only after a separate explicit dry-run has shown the exact lock path and recovery condition. Git remains responsible for branch divergence and merge conflicts.

Existing Python lifecycle validators become compatibility consumers of the same versioned conformance fixtures and machine contract during migration. The Node engine is the mutation-time authority; CI invokes `rigorloop lifecycle validate` as the public governance entry point after parity is proven. Python validators remain available behind that entry point or as temporary dual-run proof, but no independent implementation may define a conflicting transition outcome. Retirement requires a ledger of protected failures and equivalent proof under ADR-20260810.

Skills continue to author semantic Markdown and make semantic judgments. Governed skills request minimal CLI context, write only their stage-owned artifact or evidence, and request registration or settlement through the CLI. `record-artifact-revision` is the sole first-release authoring registration operation: it verifies an already-written stage-owned artifact and authoring evidence, binds creation or revision to the matching artifact entry and prior identity, invalidates registrations for the replaced identity, and derives `review-required`. It never authors content or changes workflow routing. The operation schema names the requested stage authority, and the CLI validates that claim against the closed operation, current state, artifact identity, and durable evidence. This is a structural integrity check, not caller authentication; trusted CI, branch protection, and filesystem authority remain outside the local threat boundary. The CLI does not grant a broader role, choose workflow routing, invoke another skill, or infer approval. Workflow alone requests routing operations and remains the continuation owner.

Adopt enforcement in five reversible gates: read-only interpretation; guarded mutation; skill and adapter migration; CI dual-run and parity; mandatory enforcement. Until the final gate is recorded, current validated direct mutation remains the compatibility path. After activation, supported governed mutations outside the CLI are invalid and rollback requires a coordinated compatibility release, never undocumented YAML editing.

## Alternatives considered

- Keep lifecycle rules in skills and direct YAML edits: rejected because it duplicates mechanics, consumes agent context, and leaves guarded transitions probabilistic.
- Keep Python validators as a separate mutation engine called by Node: rejected because two language-level policy owners would drift. Python may remain a compatibility adapter or fixture consumer, not an independent transition authority.
- Rewrite all validation in Node immediately: rejected because a big-bang retirement risks losing protected failures. Migration uses shared conformance fixtures and ledger-backed retirement.
- Store an append-only event log or external database: rejected because the first release needs one readable Git-tracked snapshot and repository-contained reconstruction.
- Let the CLI route stages or author semantic artifacts: rejected because it would collapse structural enforcement, semantic authority, and workflow continuation.
- Use only Git locks or branch protection for concurrency: rejected because they do not prevent stale local operations or provide deterministic operation-level diagnostics.

## Consequences

- Humans, skills, workflow, adapters, and CI gain one operation-oriented lifecycle contract and effective-state interpretation.
- Governed skills can remove artifact discovery, review-round calculation, field mutation, serialization, settlement, freshness, and retry mechanics while retaining semantic criteria, artifact output, authority, stop, and portable-mode guidance.
- The Node package gains security-sensitive repository parsing, hashing, canonicalization, lock, recovery, and migration code with substantial conformance and fault-injection proof obligations.
- The package gains one pinned production dependency for YAML parsing; dependency updates become compatibility-sensitive and must rerun parser-domain, duplicate-key, alias/tag, canonicalization, and security fixtures.
- Existing Python validation remains temporarily duplicated, but only as explicitly measured migration proof; conflicting outcomes block enforcement.
- Content hashes become lifecycle identity inputs, revising ADR-20260729's first-version no-hash choice while preserving repository-contained truth and avoiding actor attribution claims.
- A local lock and recovery bundle improve worktree concurrency and crash handling but do not provide distributed transactions across branches or repositories.
- Machine schemas, error codes, lifecycle-revision canonicalization, and compatibility matrices become versioned public contracts for skills and adapters.
- Mandatory enforcement can occur only after skill migration, generated-package parity, CI validation, recovery proof, compatibility documentation, and token measurement pass.

## Follow-up

- Architecture review this ADR with the canonical architecture update.
- Plan the engine, read-only CLI, guarded transaction, migration, skill/adapter conversion, CI enforcement, and token-measurement slices separately.
- Build the boundary-first proof map before implementation and include transition, unknown-value, invalidation, stale-revision, retry, fault-injection, migration, repair, and package-integration fixtures.
- Amend operating guidance only in the enforcement slice, recording intentionally unaffected surfaces.
