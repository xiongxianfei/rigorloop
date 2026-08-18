# Code Review M4 R1: Ordered Final-Review Evidence Tail

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M4 range `d3e1766a..970ef3ed`
Reviewed milestone: M4
Reviewed artifact: commit `970ef3ed`
Review date: 2026-08-18
Status: changes-requested
Material findings: EXCSIM-CR3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: EXCSIM-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: EXCSIM-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-18-explain-change-skill-simplification/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-08-18-explain-change-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-18-explain-change-skill-simplification/review-resolution.md#code-review-m4-r1`
- Reviewed milestone: M4
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4
- Required review-resolution: yes
- Finding IDs: EXCSIM-CR3
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact risks were self-referential identities, acceptance of reordered or broader commits, path-only acceptance of shared metadata, recovery from an inexact partial tail, and a synthetic-only end-to-end proof. Review inspected the M4 diff, approved spec and ADR, plan/test proof, production resolver and workflow predicate, temporary-Git tests, scenario fixture, shipped reference, and recorded validation.

## Material finding

Finding ID: EXCSIM-CR3
Severity: major
Location: `scripts/workflow_code_state.py:123-158,277-313,506-516`
Evidence: `_changed_fields` represents any list change as the owning list path, while both stage allowlists admit whole `workflow_state.evidence`, `workflow.automation.evidence`, and `changed_files` lists. An `R` or `E` commit can therefore delete prior evidence, reorder the list, or insert another stage's evidence and still pass. Post-handoff commits likewise accept any caller-supplied lifecycle path without verifying that the commit and shared metadata are verify-owned. This contradicts R27-R29 and the ADR's closed per-revision path-and-field contract.
Required outcome: Preserve prior shared-list values and admit only the exact stage-owned append operations for `R`, `E`, and later verify evidence; reject deletion, replacement, reordering, duplicates, unrelated entries, and unknown sibling fields before verify reuse.
Safe resolution path: Add a semantic list-delta validator bound to the exact stage manifest, narrow post-handoff validation to one verify-owned evidence commit and its closed `change.yaml` fields, add positive and negative real-Git regressions, rerun M4 validation, and rereview M4.
needs-decision rationale: none; R27-R29 already determine the required behavior.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | Scalar and mapping fields fail closed, but shared list mutations are broader than R27-R29. |
| Test coverage | concern | Real Git ancestry is covered; destructive and unrelated list deltas are not. |
| Edge cases | block | Evidence deletion, substitution, and later caller-supplied paths can bypass stage ownership. |
| Error handling | pass | Invalid ancestry, dirty state, unknown mapping fields, and path mismatches stop. |
| Architecture boundaries | pass | The correction stays in the accepted parser and evidence-owner model. |
| Compatibility | pass | Reviewed product identity remains stable across derived stage revisions. |
| Security/privacy | pass | No external credentials or sensitive content are introduced. |
| Derived artifact currency | pass | Skill, build, and adapter checks pass for the reviewed package. |
| Unrelated changes | pass | The implementation is scoped to M4 surfaces. |
| Validation evidence | concern | All commands pass because the missing semantic list-delta cases are not exercised. |

## Claim limitations

M4 remains open until EXCSIM-CR3 is corrected and rereviewed. No final verification, branch readiness, or PR readiness is claimed.
