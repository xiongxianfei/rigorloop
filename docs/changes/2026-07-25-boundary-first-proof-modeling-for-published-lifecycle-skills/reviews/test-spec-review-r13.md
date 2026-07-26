# Boundary-First Proof Modeling Test-Spec Review R13

Review ID: test-spec-review-r13
Stage: test-spec-review
Round: 13
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: focused R28y proof map after spec-review R36 and architecture-review R15
Reviewed artifact: specs/rigorloop-workflow.test.md at 14af42f9
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR13-1, BFP-TSR13-2
Immediate next stage: test-spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Initial packet inventory: approved R36 spec, approved R15 architecture, accepted ADR, approved R14 plan, draft test spec
Manifest owner: workflow orchestrator

## Result

The focused upstream specification and architecture are approved, but the test
spec still identifies itself as draft and retains stale readiness text that
claims upstream approval is pending. Its controlled transport-failure proof
also lacks the exact fixture owner, root, record fields, canonical-evidence
eligibility, and command binding required by the approved contract.

## Findings

### BFP-TSR13-1 — Test-spec lifecycle and readiness are stale

Finding ID: BFP-TSR13-1
Severity: blocker

Evidence:

- `specs/rigorloop-workflow.test.md` declares `draft`.
- The architecture summary still describes the approved architecture and
  accepted ADR as draft or proposed.
- Readiness still says spec approval precedes focused test-spec review.

Required outcome:

- Set the proof surface to `active`.
- Synchronize its governing-artifact and readiness text with spec-review R36,
  architecture-review R15, the accepted ADR, and plan-review R14.
- State that approval of the revised test spec is the remaining gate before M2
  implementation resumes.

Safe resolution:

- Make a lifecycle-only correction without changing approved upstream
  semantics, then rerun independent test-spec review.

### BFP-TSR13-2 — Controlled transport-failure fixtures lack an executable contract

Finding ID: BFP-TSR13-2
Severity: major

Evidence:

- T52 names a test-owned failure-fixture schema but does not bind its owner or
  root.
- The test spec does not enumerate the required fixture fields:
  `fixture_id`, `event_key`, `transport_attempts`,
  `expected_terminal_decision`, `expected_diagnostic_id`,
  `expected_diagnostic_ids`, and `canonical_evidence_eligible`.
- T52 is not bound to `CMD-BFP-1`.
- M2 ownership and expected evidence omit the transport-fixture root.

Required outcome:

- Bind controlled transport fixtures to owner
  `scripts/test-boundary-proof.py` and root
  `tests/fixtures/boundary-proof/transport/`.
- Declare the exact fields, reject invalid fixtures fail closed, and require
  `canonical_evidence_eligible: false` for controlled failures.
- Bind T52 and M2 proof to `CMD-BFP-1`.
- Add the fixture root to the global fixture declaration and M2 ownership and
  expected evidence.

Safe resolution:

- Project the already approved transport-fixture contract exactly into the
  test spec and plan, without inventing new runtime behavior.
