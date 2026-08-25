# Workflow-Routed Upstream Corrections Architecture

## Owning change record

- `docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

## Related artifacts

- Proposal: `docs/proposals/2026-08-25-workflow-routed-upstream-corrections.md`
- Spec: `specs/workflow-routed-upstream-corrections.md`
- Plan: pending
- ADR: `docs/adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md`

## Summary

This design extends the local governed lifecycle engine with three workflow-authorized operations: start one exact upstream correction route, return from that route after a current approving review, and withdraw one provably duplicate architecture or ADR registration. It also prevents new cross-change artifact-path collisions and scopes settlement blockers to the exact registered review occurrence.

The design preserves one Git-contained mutable snapshot per change, keeps route choice with workflow, keeps semantic revision with the artifact owner, and adds only bounded route facts to agent context.

## Requirements covered

This architecture covers specification requirements R1-R32, including the public operation contract, guarded state transitions, cross-change ownership, migration, diagnostics, recovery, and compatibility boundaries.

## Architecture Constraints

- `change.yaml` remains the sole mutable governed lifecycle snapshot.
- New mutation uses the existing lock, recovery bundle, canonical revision, serializer, post-validation, and rollback transaction.
- Semantic Markdown and historical review evidence are never changed by the new operations.
- Unknown stored and request vocabularies fail before consistency checks.
- Old clients must reject state they cannot preserve.

## Proposed architecture

### Context and scope

Workflow selects a correction destination from durable findings and requests the route. The lifecycle CLI validates the supplied decision against the current snapshot and canonical workflow order. The destination authoring and review skills then use their existing artifact-revision, review-recording, and settlement operations. Workflow requests return only after the engine proves the exact revised identity and review occurrence. CI consumes the same read model.

Cross-change ownership discovery is local and read-only. It scans supported `docs/changes/*/change.yaml` records, never Git history, generated packages, or external state.

### Solution strategy

### Stored schema

Introduce lifecycle CLI schema version 2. The existing `migrate` operation upgrades a selected version-1 record before a correction route or withdrawal can be recorded. Version 2 adds these closed surfaces beneath `lifecycle_cli`:

- `active_correction`: either absent or one mapping containing route ID, prior lifecycle revision, source snapshot, destination facts, reason, evidence identity, route-start artifact identity, and status `active`;
- `correction_history`: a deterministic route-ID-keyed mapping of returned route receipts containing the captured facts and return evidence identity;
- `withdrawals`: a deterministic withdrawal-ID-keyed mapping containing the selected registration facts, canonical owner, prior lifecycle revision, evidence identity, and status `withdrawn`.

Route and withdrawal IDs are SHA-256 identities over a versioned canonical encoding of their durable request facts and prior lifecycle revision. Resulting lifecycle revisions remain only in the common result envelope so stored data is not self-referential.

The version-2 reader accepts version 1 and version 2. Version-1 records remain valid for existing operations, but the three new operations require explicit migration. A version-1 client rejects version 2 through its existing unsupported-schema path and therefore cannot silently drop new coordination state.

The structural v1-to-v2 migration is admissible whenever the selected record has no active lock or recovery condition, even when semantic findings or a workflow blocker remain open. It preserves every existing artifact, review, finding, milestone, and routing fact. This prevents migration from becoming a prerequisite deadlock for the recovery operation.

### Correction projection

`route-correction` first validates current routing, source fields, exact current findings, destination settlement and identity, canonical predecessor order, evidence, and workflow authority. It copies current stage, next stage, lifecycle state, blocker, active milestone and its state, and selected finding IDs into the source snapshot. It then sets current stage to the destination authoring stage, next stage to its review peer, and current blocker to null. The active route, not a blocker string, explains why this temporary routing is valid.

The interpreter admits `route-correction` while the cited source findings or blocker are active, because those facts are route inputs rather than reasons to suppress the workflow-owned recovery operation. It admits guarded withdrawal despite unrelated findings for the same reason, while retaining every R23 activity and ownership refusal.

The interpreter overlays one narrow permission while the route is active: only `record-artifact-revision` for the exact destination artifact and owning authoring authority is added. Existing unrelated open findings and the suspended blocker remain visible in route context but are non-fatal only to that exact operation. All other permission logic is unchanged.

When the destination revision is registered, existing invalidation removes its prior review, validation, and resolution registrations. Review recording binds a new review occurrence to the revised hash. Settlement reads material findings from the exact registered `lifecycle_cli.reviews[artifact_id]` occurrence; the global review log remains a status ledger but no longer substitutes unrelated findings for the target occurrence.

`return-correction` validates the route, expected revision, return evidence, changed destination hash, derived review authority, approving outcome, exact registered review identity, and chronology. It moves the active record to history and restores the source snapshot fields exactly. It does not close findings or advance milestones.

### Cross-change ownership

Before creating a new artifact entry, the snapshot reader builds a normalized ownership index from supported active `lifecycle_cli.artifacts` entries. It validates agreement with the corresponding `artifact_states` and `artifacts` projections and fails closed on unreadable, unsupported, escaped, or contradictory records. The selected change is excluded only for its existing exact artifact ID. A different change owning the same normalized path produces `RL_ARTIFACT_PATH_OWNED`.

Withdrawal parses the selected Markdown artifact's first normalized `Owning change record` pointer, requires it to identify the supplied different change, and requires exactly one matching active artifact entry there. It rejects active dependencies and non-architecture kinds. The transaction removes only the duplicate change's active artifact projections and artifact-keyed lifecycle registrations, then stores the withdrawal receipt. Semantic files, review records, logs, resolution text, authoring evidence, and canonical-owner state remain byte-identical.

### Diagnostics and agent context

The interpreter returns immediate `permitted_operations` separately from `available_after_workflow_route`. A context request for a legal non-current upstream authoring stage returns `RL_WORKFLOW_ROUTE_REQUIRED` with the current stage, requested stage, workflow owner, relevant finding IDs, and deferred operation. Concise human output leads with the owner and next action; JSON carries the same facts without absolute paths.

Published authoring skills keep their existing semantic guidance and registration call. They do not gain settlement or routing procedure. Workflow guidance gains only the three operation requests and evidence schemas.

## Building Block View

The implementation extends existing package-local boundaries:

1. `lifecycle-contract.js` owns version-2 stored and request vocabularies, stage/review mappings, route reasons, and diagnostic codes.
2. `lifecycle-read.js` parses selected coordination state and derives active-route status, exact immediate permissions, deferred route guidance, and route/withdrawal diagnostics.
3. `lifecycle-operations.js` builds the bounded cross-change ownership index, parses the owning-change pointer, and evaluates route, return, withdrawal, scoped settlement, and collision prevention as candidate-state transitions.
4. The existing transaction adapter performs the only write and recovery protocol.
5. The CLI parser and renderers expose the three public operations and bounded human/JSON results.

No second transition engine, database, daemon, or workflow runner is introduced.

## Runtime View

### Start correction

Workflow writes route evidence, reads current context, and submits the exact route request. The engine validates version 2, stale-operation identity, source snapshot parity, finding membership, destination order and settlement, then atomically stores the route and destination routing. Failure leaves prior bytes.

### Revise and review

The destination authoring skill receives minimal context and writes the exact artifact plus authoring evidence. Existing registration invalidates stale target evidence. The matching review skill records one occurrence. Settlement considers that occurrence's finding set even though downstream findings remain open.

### Return

Workflow writes exact return evidence and submits the route ID. The engine compares every artifact and review identity, then atomically restores the captured source fields and stores history. Any stale or mismatched fact rejects without mutation.

### Withdraw duplicate

Workflow writes withdrawal evidence after read-only ownership diagnostics. The engine proves canonical ownership and inactivity, removes only selected active projections, stores a receipt, and post-validates both selected state and repository-wide ownership.

## Interfaces and contracts

The public interface remains `rigorloop lifecycle <operation> --request <path>`. Requests use the version-1 JSON envelope and current lifecycle revision; the stored coordination representation is version 2 for correction and withdrawal operations. Human and JSON responses derive from the same result, and all paths and evidence identities are repository-contained.

## Deployment View

The capability ships inside the existing Node `@xiongxianfei/rigorloop` package and uses the existing `yaml` dependency. Generated adapter archives consume compatible workflow and skill text only after package and repository validation pass. No service, credential, network call, or new production dependency is added.

## Crosscutting Concepts

- Canonicalization: repository-relative normalized paths and versioned canonical request encodings.
- Authority: workflow requests route, return, and withdrawal; stage owners retain revision and review operations.
- Freshness: every mutation carries current lifecycle revision and exact content identities.
- Recovery: one selected `change.yaml` mutation under the existing recovery protocol.
- Privacy: diagnostics omit absolute paths and file contents.
- Token economy: deferred routing guidance is one bounded object; skills do not embed lifecycle mechanics.

## Architecture Decisions

- [ADR-20260825 Workflow-Routed Correction and Artifact Ownership](../adr/ADR-20260825-workflow-routed-correction-and-artifact-ownership.md) - adopt schema version 2, one active correction snapshot, read-time ownership indexing, exact review-occurrence settlement, and guarded duplicate withdrawal.
- [ADR-20260824 Governed Lifecycle CLI Transaction Boundary](../adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md) - retained transaction, interpreter, and semantic-operation boundary amended by the new workflow-requested operations.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| integrity | route or return facts are stale or mismatched | stable rejection and byte-identical prior `change.yaml` |
| recoverability | an exact duplicate architecture registration exists | one guarded withdrawal removes only active duplicate projections and leaves semantic files unchanged |
| compatibility | an old CLI reads version-2 route state | fail closed as unsupported schema without rewrite |
| explainability | an agent asks for a blocked upstream stage | bounded owner, reason, finding IDs, and deferred operation in human and JSON output |
| efficiency | cross-change ownership is evaluated | one bounded scan of supported change records with no Git or network access |

## Risks and Technical Debt

- Repository-wide scans grow with change count. The first release favors correctness; a cache is deferred until measurement shows need.
- Owning-change pointers are Markdown structure. Parsing is deliberately narrow and fail-closed; a future schema-owned artifact manifest may replace it.
- Historical review logs remain broader than registered review occurrences. Settlement uses exact registrations; validators must retain ledger visibility without restoring global blocking.
- Version-2 migration increases rollout coordination but prevents old clients from silently deleting new state.

## Glossary

- Active correction: one temporary workflow route plus an immutable downstream source snapshot.
- Active owner: a current artifact registration, excluding withdrawal receipts.
- Scoped settlement: settlement based on the exact registered review occurrence for the target artifact revision.

## Next artifacts

- Independent architecture review.

## Follow-on artifacts

- None yet.

## Readiness

Ready for architecture review after CLI registration; not plan-ready, implementation-ready, verified, or PR-ready.
