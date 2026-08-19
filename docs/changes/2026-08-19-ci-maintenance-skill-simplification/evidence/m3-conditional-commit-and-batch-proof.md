# M3 Conditional Commit and Batch Proof

- Milestone: M3
- Status: implementation complete; review required
- Create: deterministic `O_EXCL` proof shows a target appearing after preflight is preserved and blocks creation.
- Revise: content-identity proof shows a concurrent change invalidates the prior identity and is preserved.
- Read-back: published procedure treats read-back only as confirmation after a successful conditional commit.
- Batch: deterministic graph fixtures order providers before wrappers, detect cycles before writes, report `partial-blocked`, and rebuild retry state.
- Architecture: no persistent lock, receipt, transaction, parser, provider abstraction, or external mutation was added.
- Unchanged with rationale: no runtime helper was added because the approved contract is packaged procedure and deterministic proof, not an executable CI engine.

Validation passed: focused simplification tests, canonical skill validation, complete skill-validator suite, and build check.
