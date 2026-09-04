# M2 implementation evidence: Recoverable compact transactions

Milestone: M2
Subject path: `docs/plans/2026-09-03-compact-current-state-change-record.md`
Subject identity: `sha256:6a27b852d9e803c3e226d8e01aed413a612f340e815da397ec333702f6f7149c`
Validation result: passed

## Result

- Skill: implement
- Status: M2 implementation complete and handed to Code Review
- Completed scope: pure expected-file and candidate evaluator; one private change-local writer lock; same-filesystem prior and candidate staging; versioned recovery metadata; deterministic multi-file replacement; exact restoration and candidate acceptance; current-set validation; bounded result envelopes; retry, contention, size, containment, permission, durability, and recovery guards
- Public activation: withheld; no public compact mutation or recovery command is wired
- Current dependency: accepted M1 implementation and Code Review R3
- Next stage: Code Review M2 R1
- Claim limitations: this evidence does not claim semantic operation coverage, public compact CLI readiness, workflow activation, final verification, release, or external readiness

## Test-first evidence

The focused baseline failed because `compact-transaction.js` did not exist. The transaction, recovery, and concurrency suites were then implemented against explicit prior/candidate bytes and fault points. Review-driven strengthening added recovery-state identity checks, prepared-state no-rewrite cleanup, complete-set reader coupling, safe unexpected-error normalization, partial-write handling, recovery-lock retry, parent-directory durability, nested-filesystem rejection, and random retry-safe replacement temporaries.

## Validation results

- `node --test packages/rigorloop/test/compact-transaction.test.js packages/rigorloop/test/compact-recovery.test.js packages/rigorloop/test/compact-concurrency.test.js` — passed, 16 tests.
- `npm test --prefix packages/rigorloop` — passed, 413 tests and 2 historical skips.
- `python scripts/validate-npm-package.py` — passed.
- `git diff --check` — passed.

## Transaction and recovery evidence

- The evaluator validates the versioned operation, binds every declared current file, rejects unbound affected paths and unchanged candidate entries, validates both prior and candidate complete sets against their expected lifecycle revisions, and performs no filesystem access.
- The adapter acquires a `0600` exclusive lock under a `0700` `.rigorloop/transactions/<change-id>/` directory before reading mutation inputs.
- Prior and candidate bytes are flushed under `prior/` and `candidate/`; `compact-recovery-v1` records sorted paths, identities, lifecycle revisions, phases, and replacement status.
- Every affected parent is checked for containment, regular-file semantics, same-filesystem placement, and directory-sync support before authoritative replacement.
- Each replacement uses a private flushed sibling temporary, atomic rename or removal, file read-back, and parent-directory synchronization.
- Ordinary failure at every tested boundary restores the exact prior set and removes transaction state before returning. Simulated interruption leaves reader-visible `recovery-required` state.
- Recovery rejects malformed, missing, unsafe, tampered, contradictory, or identity-unknown state. An untouched prepared transaction is discarded without rewriting authoritative files; mixed replacement restores prior bytes; a fully persisted candidate may be accepted only after canonical complete-set validation.
- A live competing writer receives `busy`; an identical uncertain retry returns `already-applied` only when every declared current file and the complete candidate set match; a conflicting retry rejects stale unchanged.
- Request, per-file, and combined transaction limits reject before replacement. Unexpected filesystem diagnostics are normalized and do not echo private recovery content.
- Recovery has no repository-history, pull-request, network, hosted-service, diagnostic-log, or raw-command-output dependency.
- The governed handoff regression is fixed: after one milestone closes, its completion registration archives the prior validation path so the next active milestone may replace the plan's current validation registration without weakening same-target refresh checks.

## Recovery

The M2 module and its three focused suites can be removed together while retaining M1's read-only compact model. Public compact writers remain disabled, so no repository state depends on this test-only adapter.
