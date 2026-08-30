# Code Review M3 R2: Consolidated Workflow Routing Correction

Review ID: code-review-m3-r2
Stage: code-review
Round: r2
Reviewer: Codex independent code-review with fresh-assumption reset
Review date: 2026-08-30
Target: corrected M3 implementation in commit `5494d2cf`
Reviewed milestone: M3
Reviewed artifact: consolidated routing correction, downstream package-authority assessment, and finding-resolution CLI correction
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CRG-M3-CR3

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m3-r2.md`, `review-log.md`, `review-resolution.md`, and the review summary in `change.yaml`
- Open blockers: CRG-M3-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-M3-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: CRG-M3-CR3
- Verify readiness: not-claimed

## Review inputs and diff summary

The rereview inspected commits `e1a205e8` and `5494d2cf`, M3 of the approved plan, CRG-R35 through CRG-R42, CRG-T11 and CRG-T12, the package-topology ADR, the targeted tests, and the recorded 297-test package result. The JavaScript routing and compact downstream assessment resolve CRG-M3-CR1 and CRG-M3-CR2 as dispositioned. The Python route vocabulary is consolidated, but its formal completion verifier still assumes one scalar reviewed-artifact identity for each combined package.

### Finding CRG-M3-CR3

Finding ID: CRG-M3-CR3
Severity: major
Location: `scripts/workflow_automation_state.py:64-68` and `scripts/workflow_automation_state.py:1045-1122`
Evidence: `design-review` selects input `design-package` and `delivery-review` selects `delivery-package`, then the shared verifier hashes one `Target` file and compares it with that scalar input. Neither scalar exists in the corresponding policy inputs: Design Review requires `proposal-review`, `architecture`, `spec`, and `applicable-adrs`; Delivery Review requires `design-review`, `plan`, and `test-spec`. Direct inspection prints `present=False` for both expected scalars. Therefore a real combined review cannot satisfy the stage-native completion verifier, and the current tests prove routing vocabulary but not combined-review completion.
Required outcome: verify Design Review and Delivery Review completion against their explicit member maps, upstream review IDs, review IDs, outcomes, and canonical review occurrences without aggregate revisions or per-document package hashes, with direct passing and mismatch proof for both stages.
Safe resolution path: add a package-aware formal-review verification branch for the two consolidated review stages, reuse the compact package fields and canonical log occurrence, and add focused state/engine tests for valid design and delivery completion plus member/upstream mismatch rejection.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The scalar verifier contradicts CRG-R22 through CRG-R24 and the no-aggregate package model. |
| Test coverage | block | Routing tests cover stage names, but no test completes either package review through the Python native verifier. |
| Edge cases | concern | Missing or mismatched member/upstream package facts need direct rejection proof. |
| Error handling | pass | Existing lifecycle invalid, stale, and mixed authority partitions fail or remain visibly withheld as governed by the cutover phase. |
| Architecture boundaries | block | Automation completion reads a single artifact while package authority is explicitly multi-artifact. |
| Compatibility | pass | Historical-only authority stays readable and non-authorizing; enforcement activation remains M6-owned under CRG-R35 through CRG-R40. |
| Security/privacy | pass | No new secret, network, personal-data, or external authorization surface. |
| Derived artifact currency | pass | The approved observable fixture was updated with the governing lifecycle change. |
| Unrelated changes | pass | The finding-resolution parser fix is bounded and directly required for the recorded partial disposition. |
| Validation evidence | block | All named suites pass, but none exercises the unsatisfiable package-review completion path. |

## Direct proof

```text
PYTHONPATH=scripts python <policy/verifier inspection>
design-review expected_scalar= design-package present= False required= ['applicable-adrs', 'architecture', 'proposal-review', 'spec']
delivery-review expected_scalar= delivery-package present= False required= ['design-review', 'plan', 'test-spec']
```

## Handoff

The finding is recorded before correction. M3 remains review-requested and M4 must not start. Resolve CRG-M3-CR3, run direct combined-review completion proof for both packages, and return the changed M3 slice for rereview.
