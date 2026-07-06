# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. Validation and fixtures
Reviewed artifact: commit a30d412d
Review date: 2026-07-06
Reviewed commit: a30d412d
Status: changes-requested
Review status: changes-requested
Material findings: SUBCR-M2-CR1
Recording status: recorded
Recording blocker: none
Reviewed milestone: M2
Milestone closeout: open
Required review-resolution: yes
Immediate next stage: review-resolution
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-07-06-subagent-assisted-code-review/reviews/code-review-m2-r1.md; docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md; docs/changes/2026-07-06-subagent-assisted-code-review/review-resolution.md; docs/plans/2026-07-06-subagent-assisted-code-review.md; docs/plan.md; docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml
- Open blockers: SUBCR-M2-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SUBCR-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-06-subagent-assisted-code-review/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md
- Review resolution: docs/changes/2026-07-06-subagent-assisted-code-review/review-resolution.md#code-review-m2-r1
- Reviewed milestone: M2
- Milestone closeout: open
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: SUBCR-M2-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `a30d412d M2: validate subagent review packets and coverage`.
- Governing artifacts inspected: `specs/subagent-assisted-code-review.md` R3-R14, `specs/subagent-assisted-code-review.test.md` T7-T12, active plan M2.
- Validation evidence reviewed: M2 validation notes in `docs/plans/2026-07-06-subagent-assisted-code-review.md`, validation ledger in `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`, and direct review proof of malformed packet aggregation behavior.

## Findings

Finding ID: SUBCR-M2-CR1
Severity: major
Location: scripts/skill_validation.py:183
Evidence: `validate_subagent_review_packet` rejects an invalid packet with `unknown packet schema version: bogus` and `unknown specialist role: style-reviewer`, but `aggregate_subagent_review_packets` iterates over the same raw packet and returns an accepted finding sourced from `style-reviewer`.
Required outcome: Aggregation must reject malformed subagent packets before any finding can be accepted, deduplicated, conflict-resolved, or promoted toward canonical material findings.
Safe resolution path: Validate each packet inside `aggregate_subagent_review_packets` before processing, or change the aggregation boundary to accept only prevalidated packet objects that cannot represent unknown schema versions, unknown roles, unknown statuses, missing required fields, malformed findings, or unverifiable reviewed scope. Add a regression proving a malformed or unknown-role packet cannot produce `accepted_findings`.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | fail | R8d requires unknown packet schema versions and unknown roles to fail closed. R10a requires the aggregator to reject malformed packets. The current aggregator does not enforce that boundary. |
| Test coverage | fail | T7 says malformed advisory output must fail closed, and T10 covers R10a-R10d aggregation behavior. Existing tests prove packet validation separately but do not prove aggregation rejects malformed packets before promotion. |
| Edge cases | fail | A malformed packet with a high-confidence major finding can bypass packet validation if passed directly to aggregation. |
| Error handling | fail | The aggregation path does not surface packet validation errors or mark malformed packet coverage as rejected or missing. |
| Lifecycle boundaries | pass | The implementation does not let subagents directly own canonical review status, verify readiness, or PR readiness. |
| Security/privacy | pass | No secret, external-network, or publication surface changed in M2. |
| Derived artifact currency | pass | M2 does not change tracked generated adapter output. Generated-output proof remains scoped to M3. |
| Unrelated changes | pass | The implementation diff is scoped to M2 validator helpers, review-artifact validation, tests, and lifecycle bookkeeping. |

## Review proof

The reviewer ran a focused Python probe against the M2 helper API:

```text
packet_errors= ['unknown packet schema version: bogus', 'unknown specialist role: style-reviewer']
accepted_findings= ({'title': 'Promoted despite malformed packet', 'severity': 'major', 'location': 'scripts/skill_validation.py', 'evidence': 'evidence text', 'required_outcome': 'reject malformed packets', 'safe_resolution_path': 'validate before aggregate', 'confidence': 'high', 'source_subagents': ('style-reviewer',)},)
```

This proves the packet validator and aggregator disagree on the same malformed packet.

## Milestone handoff state

- Reviewed milestone: M2. Validation and fixtures
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M2, M3
- Next stage: review-resolution
- Final closeout readiness: not ready; SUBCR-M2-CR1 is open, M2 is not closed, M3 remains open, and final holistic review, explain-change, verify, and PR handoff remain open.
- Verify readiness: not-claimed
