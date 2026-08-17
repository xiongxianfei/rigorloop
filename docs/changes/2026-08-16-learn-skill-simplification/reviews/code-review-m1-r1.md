# Code Review M1 R1: Learn Skill Simplification

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M1 range `88c7f8c2..224d62aa`
Reviewed milestone: M1
Reviewed artifact: commit `224d62aa`
Review date: 2026-08-17
Status: changes-requested
Material findings: LRNSIM-CR-M1-R1-F1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: M1 caller and disposition closure is not directly validated
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: LRNSIM-CR-M1-R1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: LRNSIM-CR-M1-R1-F1
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact M1 risks were a self-declared caller inventory that did not prove current repository call sites, ledger fields accepted without closed-vocabulary validation, an inaccurate baseline, and an architecture gate that could be satisfied by prose alone. Direct inspection covered the actual implementation range, ledger schemas, invalid fixtures, validator assertions, baseline bytes and words, scenario families, current caller surfaces, and the unchanged canonical skill.

## Findings

## Finding LRNSIM-CR-M1-R1-F1

Finding ID: LRNSIM-CR-M1-R1-F1
Severity: major
Location: `fixtures/learn-simplification-scenarios.yaml`, both disposition ledgers, and `LearnSkillSimplificationLedgerTests`
Evidence: The caller rows contain descriptive labels but no repository path or consumed phrase, so the test proves only that four self-authored rows exist rather than inventorying current callers. The validator checks rule owners and literal classifications but never checks either ledger's `disposition` against a closed set or an unknown-value fixture. M1 therefore cannot establish its plan requirement that every current caller, rule, and literal has one closed treatment before canonical mutation.
Required outcome: Bind every caller row to a current repository path and exact identifying phrase, verify those paths and phrases, validate rule and literal dispositions against closed vocabularies before consistency checks, and add unknown-disposition regression fixtures.
Safe resolution path: Declared-safe correction limited to the M1 ledgers, M1 fixtures, `LearnSkillSimplificationLedgerTests`, and M1 evidence. Add deterministic fields and assertions, rerun CMD1, metadata validation, and diff checks, then obtain M1 rereview.
needs-decision rationale: none
auto_fix_class: declared-safe
allowed paths: `docs/changes/2026-08-16-learn-skill-simplification/learn-*.yaml`, `docs/changes/2026-08-16-learn-skill-simplification/fixtures/*`, `docs/changes/2026-08-16-learn-skill-simplification/evidence/m1-preservation-inventories.md`, `scripts/test-skill-validator.py`
forbidden paths: `skills/learn/**`, `specs/**`, `docs/plans/**`, and lifecycle state outside workflow-owned routing
required validation: CMD1, change-metadata validation, and `git diff --check`

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | Intended ownership matches R38-R40 and R47, but the inventory is not evidence-closed. |
| Test coverage | block | Unknown owners and literal classifications are tested, but dispositions and actual caller bindings are not. |
| Edge cases | pass | Scenario families cover operation, interruption, retry, authority, result, compatibility, and architecture stops. |
| Error handling | concern | Two closed ledger fields can accept arbitrary values. |
| Architecture boundaries | pass | No R46 trigger or new persistent owner is introduced. |
| Compatibility | concern | Literal rows exist but their dispositions are not validated. |
| Security/privacy | pass | All proof is repository-local and contains no sensitive data. |
| Derived artifact currency | pass | Canonical and derived packages are intentionally unchanged in M1. |
| Unrelated changes | pass | The implementation range is limited to M1 evidence and its validator. |
| Validation evidence | block | Passing CMD1 does not prove the missing caller and disposition properties. |

## Requirement-fidelity receipt

R38 and R39 require every rule and compatibility-sensitive literal to receive a disposition, and the M1 plan requires current caller inventory before mutation. The current validator establishes identity uniqueness and partial vocabulary closure but omits those properties. R46 remains satisfied because the slice adds no recovery, polling, integration, schema owner, or cross-owner mutation.

## Claim limitations

This review does not close M1, authorize M2, or claim verification, branch, CI, or PR readiness.
