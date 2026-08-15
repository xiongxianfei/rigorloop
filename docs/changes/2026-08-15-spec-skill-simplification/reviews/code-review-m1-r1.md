# Code Review M1 R1: Spec Preservation Inventories

Review ID: code-review-M1-r1

Stage: code-review

Round: r1

Reviewer: Codex independent code-review context

Target: implementation milestone M1 diff `88455f4e..d8fa87cc`

Reviewed milestone: M1

Reviewed artifact: commit `d8fa87cc`

Reviewed revision: `d8fa87cc`

Review date: 2026-08-15

Recording status: recorded

Status: changes-requested

Review status: changes-requested

Material findings: SPSIM-M1-CR1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review-resolution entry, and workflow review state
- Open blockers: none; the finding is mechanically correctable within M1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPSIM-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-15-spec-skill-simplification/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-15-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-spec-skill-simplification/review-resolution.md#code-review-M1-r1`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: SPSIM-M1-CR1
- Verify readiness: not-claimed

## Actual diff summary

M1 adds only change-local semantic and literal ledgers, deterministic scenarios, two invalid closed-vocabulary fixtures, baseline measurements, and milestone evidence. It does not alter canonical skill prose, boundary references, the structural skeleton, validators, generated output, or package behavior.

## Finding SPSIM-M1-CR1

Finding ID: SPSIM-M1-CR1

Severity: major

Location: `spec-rule-disposition.yaml` row `SRULE-014` and `spec-literal-compatibility.yaml` after `SLIT-026`

Evidence: R57 requires exactly one disposition and destination per semantic rule or duplicate cluster, but `SRULE-014` assigns one rule row to two reference destinations even though the common skill owns initial loading and each boundary reference owns different procedure. R59 separately requires every exact heading consumed by contracts, fixtures, or tests to receive one classification and disposition, but the ledger classifies only the two insertion anchors and omits the other exact universal skeleton headings.

Required outcome: Split initial loading, compact boundary procedure, and feature-record procedure into independently owned rule rows, and classify every exact universal skeleton heading separately without freezing incidental prose.

Safe resolution path: Replace `SRULE-014` with one inline resource-loading row while retaining the two reference-owned procedure rows, add one literal row for every remaining skeleton heading, update the evidence counts, rerun CMD1 and the named M1 checks, and return M1 for context-reset rereview.

needs-decision rationale: none

auto_fix_class: mechanical

deterministic_authority: R57 and R59 define exact one-owner and one-literal-treatment obligations.

affected_paths: `docs/changes/2026-08-15-spec-skill-simplification/spec-rule-disposition.yaml`, `docs/changes/2026-08-15-spec-skill-simplification/spec-literal-compatibility.yaml`, `docs/changes/2026-08-15-spec-skill-simplification/evidence/m1-preservation-inventories.md`

required_validation: CMD1, documentation prose validation, change metadata validation, and `git diff --check`

## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R57 and R59 are not fully satisfied because one semantic row has two destinations and multiple exact skeleton headings are absent. |
| Test coverage | concern | CMD1 proves closed values, shape, and uniqueness but cannot detect omitted current literals or a composite destination. |
| Edge cases | pass | Scenarios cover profiles, signals, transactions, retries, restart authority, partial content, formal-block states, resources, parity, and acceptance. |
| Error handling | pass | Unknown dispositions and classifications fail before required-field and consistency checks. |
| Architecture boundaries | pass | M1 records evidence only and leaves package, lifecycle, and adapter ownership unchanged. |
| Compatibility | concern | Exact insertion anchors are covered, but remaining universal skeleton headings lack explicit treatment. |
| Security/privacy | pass | Every artifact is repository-local static evidence with no external access or secrets. |
| Derived artifact currency | pass | Canonical and generated resources are unchanged by M1. |
| Unrelated changes | pass | The implementation commit contains only the seven planned M1 evidence files. |
| Validation evidence | pass | CMD1, change metadata, readability, documentation prose, and diff checks passed for the authored shape. |

## Requirement-fidelity receipt

The review began from R57-R62 and T16. Unknown-value ordering, unique identities, scenarios, and baseline arithmetic match the approved properties. The one-owner rule and exhaustive exact-literal inventory remain incomplete for the reasons recorded in `SPSIM-M1-CR1`.

## Handoff

M1 requires resolution and rereview of `SPSIM-M1-CR1` before it can close or hand off to M2. This review does not claim later package behavior, generated-resource currency, final holistic review, verification, branch readiness, or PR readiness.
