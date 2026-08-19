# Test-Spec Revision R2

Stage: test-spec
Operation: revise-primary-test-spec
Result: review-required
Date: 2026-08-18

## Governing basis

- Approved specification and review: `spec-review-r2`
- Accepted architecture and ADR: `architecture-review-r1`, `ADR-20260818`
- Active plan and review: `plan-review-r2`
- Authorizing upstream change: ordered final-review evidence-tail amendment

## Revision summary

The proof map replaces the obsolete one explanation-only direct-child model with distinct reviewed-subject S, final-review-recording R, explanation-recording E, and handoff E identities. T09-T11 now cover exact identities, closed path-and-field ownership, partial `S -> R` retry, and fail-closed broader tails. T19 adds a real temporary-Git `S -> R -> E -> verify` journey, and CMD-12 makes the existing workflow code-state test suite a first-class M4 command.

Coverage, acceptance, example, boundary, interaction, edge-case, command, and milestone mappings now bind R24-R29 and ADR-20260818 to M4. No manual acceptance, target-agent runtime, network, live PR, new persistence service, or new identity owner is introduced.

This evidence records no peer approval, implemented test, validation pass, implementation authorization, verification, branch readiness, or PR readiness.
