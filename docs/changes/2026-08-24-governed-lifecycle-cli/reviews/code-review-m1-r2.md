# Code Review M1 R2: Corrected Lifecycle Contracts

Review ID: code-review-m1-r2
Stage: code-review
Round: r2
Reviewer: Codex independent code-review context
Target: implementation milestone M1 range `b18fedac..a878ca86`
Reviewed milestone: M1
Reviewed artifact: commit `a878ca86`
Review date: 2026-08-24
Status: changes-requested
Review status: changes-requested
Material findings: RLCLI-CR-M1-3
Recording status: recorded
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Author context ID: root-m1-correction-r1
Reviewer context ID: root-m1-review-r2-context-reset
Context separation mechanism: fresh-assumption-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: public request schema; lifecycle identity contract
Risk-tier classifier: deterministic changed-surface classification
Governing artifacts: `specs/governed-lifecycle-cli.md`; `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`; `docs/plans/2026-08-24-governed-lifecycle-cli.md`; `specs/governed-lifecycle-cli.test.md`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/governed-lifecycle-cli.md@a878ca86#sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405; specs/governed-lifecycle-cli.test.md@a878ca86#sha256:67666e00f314a95058b1399ae723702257e3342781bb2b0acc4d7a81eeb48351; docs/plans/2026-08-24-governed-lifecycle-cli.md@a878ca86#sha256:3db2ac47143f4ad05e78eeeeea0edb8a0228d743319cce16199564f2d5bda485; docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md@a878ca86#sha256:9e2ed53a513fe7d1d04c69cfd5044a3aa4f2199e39695849ac7a5d638d6fb78e; implementation-diff@a878ca86#sha256:4909b9e38f28c56e24433d44bd8e82bdfb702b418f0015d30dd548d62e777687
Prompt template version: code-review-v1
Initial packet hash: sha256:4909b9e38f28c56e24433d44bd8e82bdfb702b418f0015d30dd548d62e777687
Manifest owner: workflow-orchestrator
Affected behavior: lifecycle request and revision contracts
Highest-impact failure modes: supported provenance rejected; incomplete request accepted; excluded provenance changes revision
Changed boundaries: BND-INPUT-001; BND-TEMPORAL-001; BND-COMPAT-001
Evidence expected: T01 and T22 request and revision proof
Areas requiring direct inspection: lifecycle contract module; shared fixture; Node tests
Areas intentionally out of scope: M2 through M7 commands and mutation behavior
Risk classes considered: input; identity; determinism; compatibility
Falsifiable review questions: Can each documented request be represented; do provenance-only variations preserve revision; do mutation fields change it

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, invocation manifest, review log, review resolution, and workflow state
- Open blockers: RLCLI-CR-M1-3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RLCLI-CR-M1-3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-24-governed-lifecycle-cli/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-08-24-governed-lifecycle-cli/review-log.md`
- Review resolution: `docs/changes/2026-08-24-governed-lifecycle-cli/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: RLCLI-CR-M1-3
- Verify readiness: not-claimed

## Finding

### Finding RLCLI-CR-M1-3

Finding ID: RLCLI-CR-M1-3
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js`; request field vocabulary
Evidence: The approved command contract states that mutation requests contain operation-specific data and optional documented provenance. M1 freezes `actor` and `recorded_at` as the version-one provenance vocabulary, yet neither is admitted by `validateLifecycleRequest`; a caller supplying either receives `RL_INVALID_REQUEST` for an unknown field. The implementation therefore cannot represent every supported request shape and the deterministic-provenance exception is one-sided.
Required outcome: Admit only the two version-one provenance fields on every mutation request, validate them as non-empty strings with a deterministic timestamp contract for `recorded_at`, and prove unknown provenance and malformed values fail closed.
Safe resolution path: Add the frozen provenance fields to the common request allowlist, validate `actor` and RFC 3339 `recorded_at`, and add positive, malformed, and unknown-field regressions without changing lifecycle revision exclusions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Optional documented request provenance is rejected. |
| Test coverage | block | No accepted-provenance request regression exists. |
| Edge cases | concern | Unknown fields fail closed, but the closed supported provenance vocabulary is absent from request validation. |
| Error handling | pass | Existing invalid inputs return stable request errors. |
| Architecture boundaries | pass | Revision canonicalization and stage-authority claims follow the ADR. |
| Compatibility | block | A documented request shape is not accepted. |
| Security/privacy | pass | YAML input remains closed and the dependency remains pinned. |
| Derived artifact currency | pass | Shared fixture and Python consumer agree. |
| Unrelated changes | pass | The correction is confined to M1. |
| Validation evidence | concern | 138 package tests pass but do not cover accepted request provenance. |

## Requirement-fidelity receipt

Applicability: applicable. The M1 contract now enforces operation-required fields and revision exclusions, but the common mutation request shape in the approved spec also permits documented provenance. That supported partition remains unimplemented.

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Independence level: L0
Second review: not applicable because this result requests changes
Confidence: high

No clean-review sufficiency receipt is issued because one material finding remains.
