# ADR-20260825: Workflow-Routed Correction and Artifact Ownership

## Owning change record

`docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

## Context

The governed lifecycle CLI prevents unsupported state mutation, but its first release intentionally does not route workflow. A downstream review can therefore identify a defect in an already settled upstream test spec or architecture while the CLI admits neither upstream revision nor workflow return. The current artifact registration path also checks collisions only inside one change, allowing two changes to claim the same shared Markdown path. Finally, settlement consults global open findings instead of the exact registered review occurrence, so unrelated findings can block a corrected upstream artifact.

The approved specification requires workflow to choose the route while the CLI validates and records it, exact downstream state restoration, occurrence-scoped settlement, cross-change collision prevention, and guarded recovery for duplicate architecture or ADR registration.

## Decision

Amend ADR-20260824 with three workflow-authorized semantic operations: `route-correction`, `return-correction`, and `withdraw-artifact-registration`. The CLI validates the supplied route but never chooses it.

Adopt lifecycle CLI schema version 2 for persisted correction and withdrawal state. A selected version-1 change must use the existing explicit migration operation before a new operation. That structural migration remains available despite semantic findings or workflow blockers and preserves them exactly; only lock or recovery conditions block it. Version 2 stores at most one active correction with an immutable source snapshot, deterministic returned-route history, and deterministic withdrawal receipts. It stores prior lifecycle revisions only; resulting revisions stay in result envelopes. This makes old clients fail closed instead of silently dropping unknown coordination state.

During correction, current routing points to the exact destination owner and the source blocker exists only inside the source snapshot. Workflow may start that route while its cited blocker or findings are active, and only the exact destination artifact revision operation gains permission afterward. Guarded withdrawal is likewise available despite unrelated findings but retains every activity and ownership refusal. Return requires a changed artifact identity and one exact current approving review occurrence, then restores every source routing and milestone field without resolving findings or advancing work.

Build a bounded read-time ownership index from supported active change records before new artifact creation or withdrawal. Reject new cross-change collisions. Permit withdrawal only for an architecture or ADR registration whose Markdown owning-change pointer and canonical owner's exact entry prove that the selected change is a duplicate. Remove only the duplicate's active projections and artifact-keyed lifecycle registrations; retain semantic and historical evidence bytes plus a non-owning receipt.

Settle artifacts from the exact current registered review occurrence and target identity. Global review logs remain durable status ledgers, but unrelated open findings do not become settlement preconditions for another artifact occurrence.

Use the existing pure evaluator and single-file transaction adapter. No operation writes another change's record, semantic Markdown, or multiple files atomically.

## Alternatives considered

- Allow direct workflow edits for exceptional correction routes: rejected because it recreates the unsupported transition boundary and stale-write risk.
- Let the CLI select the upstream destination: rejected because route choice is a semantic workflow decision.
- Add a generic reopen or deregister command: rejected because it expands authority beyond the exact defect and cannot prove safe ownership.
- Keep schema version 1 with ignored additive fields: rejected because older clients may serialize away coordination state.
- Make the canonical owner transaction participate in withdrawal: rejected because it creates an unnecessary multi-file transaction; canonical state is already proof and remains unchanged.
- Treat every global open finding as settlement-blocking: rejected because findings belong to review occurrences and unrelated findings create correction deadlocks.

## Consequences

- Downstream proof and contract gaps gain a deterministic recovery path without weakening review findings or milestone state.
- Workflow guidance gains narrow evidence and operation calls; stage skills do not absorb settlement or routing mechanics.
- Version-2 migration and mixed-version validation become required before using the new operations.
- Artifact creation performs a bounded repository scan, increasing local read cost with change count.
- Existing duplicate architecture or ADR registrations can be repaired without deleting audit evidence.
- The operation and validator suites must cover schema migration, path normalization, owning-pointer parsing, scoped findings, exact restoration, retry, and transaction faults.

## Follow-up

- Review this ADR with the change-owned architecture document.
- Plan implementation as proof-first slices for schema/read model, correction route, ownership recovery, diagnostics, and skill/workflow migration.
- Apply the verified withdrawal and correction capability to the blocked CLI observability change in a separate governed consumption slice.
