# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2 orchestration semantics and workflow-state gates implementation diff at commit `13a55915`
Reviewed artifact: M2 implementation diff at commit `13a55915`
Review date: 2026-06-25
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`, `docs/plans/2026-06-25-independent-adversarial-review-gates.md`, `docs/plan.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Open blockers: CR3-F1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR3-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md
- Review resolution: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md
- Reviewed milestone: M2. Orchestration semantics and workflow-state gates
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CR3-F1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `13a55915^..13a55915`, especially `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py`, active plan state, plan index, and change metadata updates.
- Tracked governing branch state: branch `proposal/independent-adversarial-review-gates`; M2 implementation commit is tracked at `13a55915`. One unrelated untracked learn-session file exists and was excluded from the implementation review surface.
- Governing artifacts: `specs/review-independence-and-criticality.md` R10-R14, R18, R20, AC6-AC13, AC15, AC-RAI-018, RAI-021 through RAI-023; `specs/review-independence-and-criticality.test.md` T7, T8, T10, T13, T16, T19; `docs/plans/2026-06-25-independent-adversarial-review-gates.md` M2.
- Validation evidence reviewed: M2 recorded `python scripts/test-artifact-lifecycle-validator.py -k review_gate`, `python scripts/test-artifact-lifecycle-validator.py -k phase_boundaries`, full `python scripts/test-artifact-lifecycle-validator.py`, explicit-path lifecycle validation, change metadata validation, review artifact validation, `git diff --check`, and whitespace scan.

## Diff summary

M2 adds `evaluate_automated_review_gate_route` to project normalized automated review outcomes and profile routing decisions, adds lifecycle tests for clean advance, routable `changes-requested`, blocked/inconclusive pauses, second-review disagreement, and final holistic review preconditions, then updates plan and change metadata handoff state to request `code-review M2`.

## Findings

### CR3-F1 - Clean-status evidence failures cannot produce the required inconclusive gate outcome

Finding ID: CR3-F1
Severity: major
Location: `scripts/lifecycle_state_sync.py:448`
Evidence: `specs/review-independence-and-criticality.md:271`-`273` makes native `approved` and `clean-with-notes` map to `advance` only when independence, evidence, recording, clean receipt, and escalation gates pass. `specs/review-independence-and-criticality.md:296`-`302` also requires an insufficient clean-review receipt to produce `review_gate_outcome: inconclusive`. The M2 helper checks the native-to-derived mapping before the evidence gates: `scripts/lifecycle_state_sync.py:448`-`450` rejects `clean-with-notes` plus `review_gate_outcome: inconclusive` as `review-gate-outcome-mismatch`, then `scripts/lifecycle_state_sync.py:466`-`468` handles an invalid clean receipt only when the supplied outcome was already `advance`. A direct probe with `native_review_status='clean-with-notes'`, `review_gate_outcome='inconclusive'`, and `clean_review_receipt_valid=False` returned `ImplementationAutoprogressionRoute(profile_state='paused', next_stage=None, stop_reason='review-gate-outcome-mismatch')`.
Required outcome: The routing helper and tests must allow clean native statuses to derive `inconclusive` when required clean/evidence gates fail, and must reject or pause based on the actual missing evidence reason without treating the spec-required inconclusive outcome as a native/derived mismatch.
Safe resolution path: Split native verdict mapping from gate validity derivation. Keep direct mappings for `changes-requested -> stop`, `blocked -> blocked`, and `inconclusive -> inconclusive`; for native `approved` and `clean-with-notes`, accept `advance` only after all required gates pass and accept or derive `inconclusive` for missing/insufficient independence, phase, risk, clean receipt, or evidence gates. Add lifecycle tests for `clean-with-notes` plus invalid clean receipt producing/accepting `review_gate_outcome: inconclusive`, and for `approved` or `clean-with-notes` with `review_gate_outcome: advance` failing when the same evidence gates are missing. Rerun `python scripts/test-artifact-lifecycle-validator.py -k review_gate` and the full artifact lifecycle validator suite.
needs-decision rationale: none
auto_fix_class: none

## Checklist coverage

1. Spec alignment: block. CR3-F1 violates R12c, R12d, and R13c by making the native status mapping unconditional before evidence gate evaluation.
2. Test coverage: block. The M2 tests cover clean evidence failure as stop reasons, but do not prove the required `review_gate_outcome: inconclusive` path for materially insufficient clean evidence.
3. Edge cases: block. The named insufficient-clean-receipt edge case is mishandled when the derived outcome is correctly inconclusive.
4. Error handling: concern. Unsupported native/derived values fail closed, but evidence-derived inconclusive outcomes are rejected as mismatches.
5. Architecture boundaries: pass. The implementation stays inside lifecycle-state routing helpers and lifecycle tests.
6. Compatibility: pass. Direct isolated review behavior remains outside the automated workflow-managed gate helper.
7. Security/privacy: pass. The diff does not introduce secret handling, private reasoning recording, or external calls.
8. Derived artifact currency: pass. M2 does not edit canonical `skills/` files, so generated skill or adapter proof is not triggered.
9. Unrelated changes: pass. The reviewed commit contains the expected M2 code, tests, plan, index, and change metadata updates. The unrelated untracked learn file is excluded.
10. Validation evidence: concern. The recorded validation commands are relevant and pass, but they did not catch CR3-F1.

## No-finding rationale

Not applicable. A material finding was found.

## Residual risks

M3-M5 remain planned future milestones and were not reviewed as implemented behavior. The M2 helper is currently a lifecycle-state evaluator; downstream integration into canonical skill guidance and final generated proof remains in later milestones.

## Milestone handoff state

- Reviewed milestone: M2. Orchestration semantics and workflow-state gates
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M2 resolution, M3, M4, M5
- Next stage: review-resolution M2
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, review-resolution-open, explain-change-pending, verify-pending, pr-handoff-pending — M2 has one material code-review finding requiring review-resolution; M3-M5 remain incomplete.
