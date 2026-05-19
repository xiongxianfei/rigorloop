# Spec Review R1: Assets-First Progressive Disclosure Pilot for Published Skills

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/skill-contract.md
Status: approved
Reviewed artifact: specs/skill-contract.md
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: spec-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/spec-review-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md
- Open blockers: none for spec review
- Immediate next stage: plan

## Summary

The draft `specs/skill-contract.md` amendment is precise enough for downstream planning and test-spec work. It defines the assets-first plan pilot as a follow-on slice, gives stable requirement IDs for the asset set, resource-map verbs, output-template boundary, handoff boundary, metadata and drift checks, deterministic validator boundaries, improvement gates, corpus split, compatibility, rollback, observability, security, and non-goals.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | pass | R37 through R45 state concrete obligations for scope, assets, resource-map behavior, templates, validation, improvement proof, and corpus selection. |
| Normative language | pass | The amendment uses testable `MUST` requirements for required behavior and scoped `SHOULD` guidance for follow-on pattern preferences. |
| Completeness | pass | Normal behavior, boundary behavior, migration, rollback, observability, security, performance, edge cases, non-goals, and acceptance criteria are covered. |
| Testability | pass | Requirements are observable through static validation, adapter packaging checks, token measurement, behavior-parity evidence, and review-recorded corpus evidence. |
| Examples | pass | E13 through E16 cover resource-map copying, skeleton ownership, handoff-policy exclusion, and historical-corpus use. |
| Compatibility | pass | Existing `plan` behavior remains the baseline, rollback is defined, and historical plans are not forced into current structural parity. |
| Observability | pass | Validation output expectations name asset metadata, resource-map coverage, `COPY`, fingerprints, section parity, adapter presence, and token-budget failures. |
| Security/privacy | pass | Assets are barred from containing secrets, credentials, tokens, machine-local paths, and private data. |
| Non-goals | pass | The spec excludes broad assets rollout, hidden workflow rules in assets, `references/` or `scripts/` in this pilot, and strict historical-plan structural parity. |
| Acceptance criteria | pass | Acceptance criteria map to the new slice boundaries, four assets, resource-map entries, skeleton and handoff boundaries, deterministic validation, improvement gates, and corpus split. |

## Eventual Test-Spec Readiness

ready

The spec has stable requirement IDs and observable proof surfaces. Test-spec should map R37 through R45 to concrete static validator tests, adapter packaging checks, token measurement evidence, behavior-parity fixtures, and review-recorded historical coverage.

## Stop Condition

None.
