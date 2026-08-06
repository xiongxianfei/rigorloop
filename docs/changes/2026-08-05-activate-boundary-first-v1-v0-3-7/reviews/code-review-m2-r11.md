# Code Review: M2 R11

Review ID: code-review-m2-r11
Stage: code-review
Round: 11
Reviewer: two independent L2 Codex reviewers
Target: 22451c8c..0bd4a06c
Reviewed artifact: M2 R10 simplification range
Reviewed milestone: M2
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m2-review-resolution-r10
Reviewer context ID: m2-r11-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Risk tier: elevated
Risk-tier triggers: ambiguous external mutation; temporary-hook lifecycle
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M2 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@0bd4a06c#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@0bd4a06c#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@0bd4a06c#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@0bd4a06c#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:22451c8c..0bd4a06c.diff@0bd4a06c#sha256:4dedc4d74288244c1a42817959f89983b2ae3991c9089860a27befcb76a5d836
Initial packet hash: sha256:4dedc4d74288244c1a42817959f89983b2ae3991c9089860a27befcb76a5d836
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: guarded-push failure classification and temporary-hook lifecycle
Highest-impact failure modes: completed publication reported as retryable; local cleanup suppresses confirmation
Changed boundaries: BND-RECOVERY-001; BND-ENV-001
Evidence expected: joint main/tag state classification and phase-safe hook cleanup
Areas requiring direct inspection: failure pair state, setup, cleanup, confirmation
Areas intentionally out of scope: release payload; actual publication; final verify
Risk classes considered: external mutation; recovery guidance; local privacy; atomicity
Falsifiable review questions: can exact H/T suggest rerun; can hook cleanup suppress confirmation
Material findings: BFA-M2-R11-001, BFA-M2-R11-002
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Diff summary

The correction removed the diagnostic result transport, inherited descriptors,
nonce channel, and endpoint cleanup machinery. The pre-push hook now returns a
boolean allow/reject result, and the parent classifies a failed push from a
fresh remote advertisement.

## Findings

### BFA-M2-R11-001 — Fresh-ref classification mishandles ambiguous success and combined races

Finding ID: BFA-M2-R11-001
Severity: major
Location: `scripts/boundary_activation_release.py:398-421`; `scripts/test-boundary-activation-release.py:357-406`
Evidence: classification checks main drift before tag existence. Exact remote
`main == H` and `tag == T` after a client-side failure is therefore reported as
retryable main drift even though atomic publication may have completed. A
simultaneous main drift plus existing immutable tag also suppresses the stronger
tag reconciliation state. The existing matrix omits both pair states.
Required outcome: classify main and tag jointly; exact H/T in publish mode must
proceed to confirmation or stop-and-reconcile, any other tag must take
precedence, and main-drift regeneration is allowed only when the tag is absent.
Safe resolution path: replace ordered single-ref checks with an explicit pair
classifier and cover exact H/T, base/tag, drift/tag, drift-only, unchanged, and
advertisement failure in check and publish modes.

### BFA-M2-R11-002 — Temporary-hook lifecycle errors escape bounded phase handling

Finding ID: BFA-M2-R11-002
Severity: major
Location: `scripts/boundary_activation_release.py:354-421`
Evidence: temporary-directory creation, hook write, chmod, and cleanup surround
the bounded subprocess handler. Setup errors can escape with private local
diagnostics, while cleanup failure after a successful push can prevent fresh
confirmation and recreate post-publication uncertainty.
Required outcome: bound private setup failures, preserve the primary result when
cleanup also fails, and ensure successful real pushes still reach confirmation
or stop-and-reconcile handling.
Safe resolution path: separate setup, push, cleanup, and confirmation states and
add setup, combined failure/cleanup, dry-run cleanup, and publish-success cleanup
fault tests.

## Checklist coverage

- Spec alignment: concern; ambiguous success violates the approved recovery contract.
- Test coverage: block; joint ref states and hook-lifecycle faults are absent.
- Edge cases: block; exact H/T and combined drift/tag states are uncovered.
- Error handling: block; setup and cleanup errors can escape or suppress confirmation.
- Architecture boundaries: pass; removal of the diagnostic transport is appropriately simplifying.
- Compatibility: concern; retry guidance is unsafe after possible publication.
- Security/privacy: concern; raw local setup diagnostics can escape.
- Derived artifact currency: pass for the reviewed range.
- Unrelated changes: pass; the range stays within M2.
- Validation evidence: concern; 17 tests and selector validation pass but omit the reproduced states.

## Prior-finding reconciliation

BFA-M2-R7-001, BFA-M2-R8-001, BFA-M2-R8-002, BFA-M2-R9-001, and
BFA-M2-R10-001 are resolved by transport removal. BFA-M2-R10-002 remains open
through both new findings. Earlier safe-context findings remain open through
the incomplete joint-state and hook-lifecycle handling.

## Milestone handoff

M2 requires review resolution. M2, M3, and M4 remain in scope under the existing
plan, but the owner has since selected a replacement usability-first direction;
workflow routing owns any cancellation or supersession decision.
