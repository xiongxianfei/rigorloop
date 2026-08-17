# Test-Spec Revision R1 Evidence

- Stage: test-spec
- Operation: `revise-primary-test-spec`
- Test specification: `specs/learn-skill-simplification.test.md`
- Prior identity: `sha256:046e20536ac6358854ccd962fba165a12d838d9498ac0bf608253eb77b452bb3`
- Revised identity: `sha256:7618bdbfd88a5cdc7fe9e4c8fd77b65baba495f040ad6df1c53e0933c807819d`
- Authorizing findings: `LRNSIM-TSR1`, `LRNSIM-TSR2`
- Governing spec review: `spec-review-r2`
- Governing plan review: `plan-review-r2`
- Completion status: complete
- Review request: `test-spec-review-r2`

## Result

The revision restricts M1 to CMD1-runnable preservation, measurement, caller, scenario, and architecture-trigger proof; gives R46 its own M1 proof obligation and case; and leaves package behavior in M2. It also adds direct compact-result proof for both learn operations, idempotent replay, blocked outcomes, all R37 result concepts, and narrow claim limits.

Boundary-first validation passes. The revision changes no approved behavior, architecture decision, implementation sequence, or production code.

The revised test specification returns to `review-required` and claims no approving rereview or implementation readiness.
