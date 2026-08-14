# Code Review M1 R1: Proposal Preservation Inventories

Review ID: code-review-M1-r1

Stage: code-review

Round: r1

Reviewer: Codex independent code-review context

Target: implementation milestone M1 diff `aad470a7..64fc3022`

Reviewed milestone: M1

Reviewed artifact: commit `64fc3022`

Reviewed revision: `64fc3022`

Review date: 2026-08-14

Recording status: recorded

Status: changes-requested

Review status: changes-requested

Material findings: PRSIM-M1-CR1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review-resolution entry, and workflow review state
- Open blockers: none; the recorded finding is mechanically correctable within M1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PRSIM-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-14-proposal-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-proposal-skill-simplification/review-resolution.md#code-review-M1-r1`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: PRSIM-M1-CR1
- Verify readiness: not-claimed

## Actual diff summary

M1 adds only change-local semantic and literal ledgers, 25 deterministic scenarios, two invalid closed-vocabulary fixtures, baseline measurements, and milestone evidence. It does not alter canonical skill prose, the structural skeleton, validators, generated output, or package behavior.

## Finding PRSIM-M1-CR1

Finding ID: PRSIM-M1-CR1

Severity: major

Location: `docs/changes/2026-08-14-proposal-skill-simplification/proposal-literal-compatibility.yaml`, rows `PLIT-017` and `PLIT-019`

Evidence: R42 and T16 require each exact heading, label, path, enum, or consumed phrase to receive one literal classification. `PLIT-017` stores five enum values as one comma-joined string, and `PLIT-019` stores seven values the same way. Neither composite string is an exact literal consumed by the skill or validators, so the ledger does not provide one independently reviewable treatment per enum value.

Required outcome: Represent each initial-goal-treatment and scope-budget-treatment value as its own literal row with one exact value, source, consumer set, classification, semantics, disposition, and replacement field.

Safe resolution path: Split `PLIT-017` into five stable rows and `PLIT-019` into seven stable rows, preserve the existing classifications and semantics, update M1 evidence counts, rerun CMD1, and return the same milestone for rereview.

needs-decision rationale: none

auto_fix_class: mechanical

auto_fix_kind: split-composite-literal-ledger-rows

deterministic_authority: R42 and T16 require one separate classification for every exact consumed enum value.

affected_paths: `docs/changes/2026-08-14-proposal-skill-simplification/proposal-literal-compatibility.yaml`, `docs/changes/2026-08-14-proposal-skill-simplification/evidence/m1-preservation-inventories.md`

required_validation: CMD1, documentation prose validation, change metadata validation, and `git diff --check`

## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Semantic rules and most literals map to R41-R44, but two composite literal rows do not satisfy R42's exact-value granularity. |
| Test coverage | concern | CMD1 proves shape, closed values, uniqueness, and loading but does not reject composite literal strings. |
| Edge cases | pass | The scenarios cover assemblies, operations, retry, stale reset, predicates, resource failure, parity, and acceptance boundaries. |
| Error handling | pass | Unknown dispositions and classifications fail before required-field and consistency checks. |
| Architecture boundaries | pass | M1 records evidence only and preserves canonical package, lifecycle, and generated-package ownership. |
| Compatibility | concern | Twelve closed enum values currently have only two composite classifications rather than one exact treatment each. |
| Security/privacy | pass | Every M1 artifact is repository-local static evidence with no external access or secret requirement. |
| Derived artifact currency | pass | Canonical and generated package resources are unchanged by M1. |
| Unrelated changes | pass | The implementation commit contains only the seven planned M1 evidence files. |
| Validation evidence | pass | CMD1, documentation prose validation, and diff checking passed for the authored shape. |

## Requirement-fidelity receipt

The review began with R41-R44 and T16. Semantic rule ownership, unknown-value-first behavior, scenario identities, and baseline accounting match the approved properties. Literal classification fails one property: each compatibility-sensitive enum value must be independently represented as the exact consumed literal rather than compressed into a non-source composite string.

## Handoff

M1 requires resolution and rereview of `PRSIM-M1-CR1` before it can close or hand off to M2. This review does not claim later package behavior, generated-resource currency, final holistic review, verification, branch readiness, or PR readiness.
