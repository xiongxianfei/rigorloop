# Design refinement: CLI trust boundary

Authoring result: complete

## Target 1

Artifact path: specs/compact-current-state-change-record.md
Artifact identity: sha256:225b54dedb662f8485b0c9db1870048126704c7defa0d7fc1e86ab6f8e68eda7
Result: `compact-operation-v1` no longer accepts caller identity or authority fields; operation eligibility is derived from current state, target, active work, and exact identities. Authority-named durable v1 fields are explicitly responsibility/provenance metadata only.

## Target 2

Artifact path: docs/architecture/2026-09-03-compact-current-state-change-record.md
Artifact identity: sha256:511ad9b51619c38cc874d9aff9efcd0c1a4470e6a5514fa700983cde355e0c13
Result: the evaluator and local trust boundary now distinguish structural eligibility from authenticated permission.

## Target 3

Artifact path: docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md
Artifact identity: sha256:089519c8ae5604a07e3c90d2506045a0eed1b02d5f556216cff1625cbfdc007a
Result: the decision excludes request-level authority claims and records external execution controls as the actual permission boundary.

## Validation

- Compact contract, projection, transaction, concurrency, and recovery tests: 36 passed.
- The design retains independent semantic responsibility without claiming caller authentication.

## Handoff

The revised exact Design package requires fresh Design Review. This evidence does not claim approval.
