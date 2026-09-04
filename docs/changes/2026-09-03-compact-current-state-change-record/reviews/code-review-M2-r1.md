# Code Review M2 R1: Recoverable compact transactions

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: current M2 working-tree slice
Reviewed artifact: compact candidate evaluator, transaction and recovery adapter, focused tests, ignore rule, and M2 evidence
Reviewed milestone: M2
Review date: 2026-09-04
Status: approved
Review status: approved
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Open blockers: none
- Next stage: Workflow may close M2 after exact validation and review registration
- Review status: approved
- Material findings: none
- Recording status: recorded
- Review record: `docs/changes/2026-09-03-compact-current-state-change-record/reviews/code-review-M2-r1.md`
- Reviewed milestone: M2
- Milestone closeout: eligible after lifecycle registration
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: closed
- Verify readiness: not-claimed

## Review inputs

- Actual diff: `compact-transaction.js`, three focused transaction/recovery/concurrency suites, the machine-local transaction ignore rule, the closed-milestone validation-registration handoff correction, and M2 evidence.
- Approved Design package: `design-review-r4`.
- Approved Delivery package: `delivery-review-r4` for plan identity `sha256:6a27b852d9e803c3e226d8e01aed413a612f340e815da397ec333702f6f7149c`.
- Accepted dependency: M1 closed against `code-review-m1-r3`.
- Direct proof: 16 focused M2 tests; 413 passing package tests with 2 historical skips; 42 focused lifecycle evidence and milestone tests; npm package validation and diff validation.

## Review judgment

The pure evaluator and filesystem adapter remain separate. The evaluator validates exact expected-file membership, prior identities, affected candidates, lifecycle revision inputs, and complete prior/resulting sets without performing I/O. The adapter owns containment, exclusive locking, reread, private staging, recovery metadata, deterministic replacement, persisted validation, durability barriers, restoration, cleanup, and bounded result classification.

The final slice closes the durability and recovery risks found during review. Transaction directory creation is synchronized through its parent; every authoritative parent must share the transaction filesystem and support directory synchronization before replacement. Recovery refuses authoritative bytes outside both recorded states, validates phase/status consistency, uses the canonical complete-set reader before accepting either prior or candidate state, and releases a failed recovery attempt's lock so an exact retry remains possible. Prepared recovery cleanup does not rewrite untouched files.

Content writes handle partial writes, authoritative replacement temporaries are retry-unique, and unexpected filesystem errors are normalized rather than exposing private paths or bytes. Competing writers cannot remove another writer's lock. Request, file, and aggregate limits are enforced before replacement. Transaction-private files use owner-only modes and are excluded from ordinary version-control selection.

No public compact writer is activated. The implementation does not use repository history, pull-request state, network access, hosted services, local diagnostic logs, or raw command output for correctness or recovery.

The lifecycle handoff correction is narrowly scoped: current validation evidence may move to a different path only when the prior path is already bound into a closed non-current milestone completion. Same-milestone and unrelated conflicting registrations remain rejected.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | SR-22–SR-33 and SR-43–SR-45 transaction responsibilities are represented without activating M3 semantic operations. |
| Concurrency | pass | A deterministic competing writer receives `busy`; stale and conflicting retries preserve authoritative bytes. |
| Recovery | pass | Prepared, mixed replacing, persisted, tampered, unknown-identity, and failed-recovery retry cases are covered. |
| Durability | pass | File flush, directory sync, same-filesystem checks, read-back, and cleanup synchronization occur at explicit boundaries. |
| Containment/privacy | pass | Normalized repository paths, ancestor checks, symlink refusal, private modes, size bounds, and redacted unexpected failures are enforced. |
| Result consistency | pass | Success, already-applied, rejected, busy, and recovery-required paths use `compact-result-v1`. |
| Compatibility | pass | Existing package behavior remains green and public compact activation is withheld. |
| Validation evidence | pass | Focused, package-wide, packaging, and diff validations pass. |

## Independence statement

This review inspected the current M2 diff, approved contracts, lifecycle projection, exact fault behavior, and validation results without modifying implementation or lifecycle state.

## No-finding statement

No material finding remains against the exact M2 R1 candidate.
