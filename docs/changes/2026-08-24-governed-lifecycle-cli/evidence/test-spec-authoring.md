# Test-Spec Authoring Evidence: Governed Lifecycle CLI

- Operation: `create-primary-test-spec`
- Change ID: `2026-08-24-governed-lifecycle-cli`
- Artifact ID: `test-spec`
- Canonical path: `specs/governed-lifecycle-cli.test.md`
- Governing basis: approved `spec` through `spec-review-r2`, approved architecture and accepted ADR through `architecture-review-r2`, and active `plan` through `plan-review-r1`
- Coverage: R1-R34, E1-E4, EC1-EC10, BND-INPUT-001 through BND-ENV-001, INT-001 through INT-004, AC1-AC10, and M1-M7
- Proof design: 25 automated cases, 16 direct boundary/interaction obligations, 14 versioned command entries, no uncovered gaps
- Authoring result: primary test spec created and matching entry moved to `review-required`
- Downstream authority: independent `test-spec-review` only
