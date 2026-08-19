# Code Review M1 R1: Preservation Inventories

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M1 range `5fd2cb0b..33e7dd4a`
Reviewed milestone: M1
Reviewed artifact: range `5fd2cb0b..33e7dd4a`
Review date: 2026-08-19
Status: changes-requested
Material findings: CIMSIM-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, invocation manifest, review log, and review resolution
- Open blockers: CIMSIM-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CIMSIM-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/review-resolution.md#code-review-m1-r1`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CIMSIM-CR1
- Verify readiness: not-claimed

## Blind-first risk map

The primary risks were incomplete semantic inventory, incidental literals becoming compatibility contracts, missing regression scenarios, non-reproducible baselines, and premature architecture-not-required claims. The review inspected the M1 diff, R45-R54, the M1 plan slice, T12-T15, and direct focused validation.

## Finding CIMSIM-CR1

Finding ID: CIMSIM-CR1
Severity: major
Location: `ci-maintenance-rule-disposition.yaml` and `ci-maintenance-literal-compatibility.yaml`
Evidence: The rule ledger contains five broad ownership groups and the literal ledger contains seven examples, while M1 and R45 require every behaviorally significant current rule and consumed literal to receive one disposition and owner. The ledgers do not enumerate R1-R54, the complete legacy clause range, assemblies, result values, paths, headings, placeholders, or parser consumers, so M2 could move or delete unaccounted behavior without detection.
Required outcome: Expand the ledgers into exhaustive requirement and literal-consumer inventories, with closed dispositions and owner checks that fail for missing, duplicate, or unknown entries.
Safe resolution path: Generate explicit R1-R54 rows, enumerate legacy CIM-R1 through CIM-R65 with the five amendment exceptions, enumerate all closed vocabularies, assembly families, resources, placeholders, headings, and directly coupled consumers, then strengthen the focused test and rerun M1 validation.
needs-decision rationale: none; the approved M1 contract determines the correction.
Auto-fix class: declared-safe
Allowed paths: the two M1 ledgers, M1 focused tests, and M1 evidence
Forbidden paths: canonical skill package, approved spec, plan, and test spec

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | R45 is not exhaustively represented. |
| Test coverage | concern | Tests check examples rather than completeness. |
| Edge cases | pass | Named T1-T15 scenarios exist. |
| Error handling | concern | Missing and duplicate ledger entries do not fail. |
| Architecture boundaries | pass | No R53 trigger is introduced. |
| Compatibility | block | Legacy and parser-consumer coverage is incomplete. |
| Security/privacy | pass | No external or sensitive surface changes. |
| Derived artifact currency | pass | No generated output changes in M1. |
| Unrelated changes | pass | The diff is milestone-scoped. |
| Validation evidence | concern | Passing focused tests do not prove exhaustive ownership. |
