# Spec-Family Assets Progressive Disclosure Baseline

## Status

active

PR #79 remains the authoritative behavior baseline. This change-local baseline
is a review aid for the asset extraction pass and does not redefine behavior.

## Proof-route assessment

`specs/skill-contract.md` is sufficient for this rollout when combined with
`specs/spec-family-assets-progressive-disclosure.md` and its active test spec.
The existing contract already defines packaged skill resources, skill-local
assets, resource maps, `COPY` for assets, generated-output boundaries,
repository-root dependency limits, and the prior `plan` assets-first pilot.

No skill-contract spec amendment is required before M1 continues. This change's
approved spec owns the narrower spec-family decisions: the three-skill scope,
full-skeleton boundaries for `spec` and `test-spec`, the two-asset cap for
`spec-review`, and the review-class asset restrictions.

## Baseline Summary

| Skill | Source skill | Existing full skeleton section set | Repeated substructure fields to extract | Closed enums that remain in `SKILL.md` | Stop conditions that remain in `SKILL.md` | Review dimensions or coverage obligations that remain in `SKILL.md` | Source location for each extracted asset |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `spec` | `skills/spec/SKILL.md` | `Status`; `Related proposal`; `Goal and context`; `Glossary`; `Examples first`; `Requirements`; `Inputs and outputs`; `State and invariants`; `Error and boundary behavior`; `Compatibility and migration`; `Observability`; `Security and privacy`; `Accessibility and UX`; `Performance expectations`; `Edge cases`; `Non-goals`; `Acceptance criteria`; `Open questions`; `Next artifacts`; `Follow-on artifacts`; `Readiness` | Requirement ID and statement; examples and edge-case links; acceptance-criterion ID and statement; decision date, decision, reason, and alternatives rejected | Spec status and settlement result from `## Closed enums`, lines 161-179 | Upstream status settlement blockers and normal authoring boundaries remain in `SKILL.md`, lines 39-79 and rules after the output skeleton | Required-section obligations remain summarized in `SKILL.md`, lines 108-159 | `assets/spec-skeleton.md` from `## Output skeleton`, lines 211-258; `assets/requirement-row.md` from `## Requirements`, lines 228-229 plus requirement guidance; `assets/acceptance-criterion-row.md` from `## Acceptance criteria`, lines 250-251 plus required-section guidance; `assets/decision-log-row.md` from proposal decision-log pattern and spec open-question/readiness guidance |
| `spec-review` | `skills/spec-review/SKILL.md` | Result block with skill, review status, material findings, recording status, review record/log/resolution fields, open blockers, immediate next stage, eventual test-spec readiness, and stop condition | Review result fields; material-finding fields: ID, severity, location, evidence, required outcome, and safe resolution path or needs-decision rationale | Review dimension verdict from `## Closed enums`, lines 67-75 | Missing input and inconclusive-review boundaries remain in `SKILL.md`, lines 145-159 and rules after the output skeleton | Ten review dimensions remain in `SKILL.md`, lines 48-65; finding severity, material-finding sufficiency, and recording obligations remain in `SKILL.md`, lines 77-143 | `assets/review-result-skeleton.md` from `## Output skeleton`, lines 175-201; `assets/review-finding.md` from `## Material findings`, lines 85-94 and the output skeleton findings block |
| `test-spec` | `skills/test-spec/SKILL.md` | `Status`; `Related spec and plan`; `Testing strategy`; `Requirement coverage map`; `Example coverage map`; `Edge case coverage`; `Test cases`; `Fixtures and data`; `Mocking/stubbing policy`; `Migration or compatibility tests`; `Observability verification`; `Security/privacy verification`; `Performance checks`; `Manual QA checklist`; `What not to test`; `Uncovered gaps`; `Next artifacts`; `Follow-on artifacts`; `Readiness` | Test ID, title, covered requirements/examples, level, fixture/setup, steps, expected result, failure proof, automation location; coverage-map requirement/example/edge-case row fields; edge-case ID and test mapping | Test spec status, test case level, and coverage map level from `## Closed enums`, lines 118-150 | Unreviewed or unstable source-spec stop conditions remain in `SKILL.md`, lines 25-30 | Required-section obligations remain in `SKILL.md`, lines 69-91; coverage rules remain in `SKILL.md`, lines 108-116 | `assets/test-spec-skeleton.md` from `## Output skeleton`, lines 152-245; `assets/test-case.md` from `## Test case format`, lines 93-105 and output skeleton lines 187-198; `assets/coverage-map-row.md` from output skeleton lines 171-181; `assets/edge-case-row.md` from required sections and output skeleton lines 183-185 |

## Asset Count Baseline

| Skill | Approved asset cap | M1 result |
| --- | ---: | --- |
| `spec` | 4 | Cap recorded; no assets created in M1. |
| `spec-review` | 2 | Cap recorded; `review-dimension-row.md` remains excluded. |
| `test-spec` | 4 | Cap recorded; no assets created in M1. |

## M1 Outcome

M1 creates the proof route, baseline summary, behavior-preservation scaffold,
and deterministic validator coverage before skill text changes. Canonical
skill text remains unchanged in M1.
