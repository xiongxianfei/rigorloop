# Spec-Family Assets Progressive Disclosure Behavior Preservation

## Status

active

This artifact records source-to-asset preservation proof for the spec-family
assets pass. M1 establishes the baseline and validator foundation before skill
text changes; M2 through M4 will add per-skill extraction rows when assets are
created.

## M1. Baseline Summary And Validator Foundation

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md` | Created before skill edits; maps PR #79 baseline structures to planned assets and records rules that remain in `SKILL.md`. |
| `scripts/skill_validation.py` | Adds deterministic spec-family asset checks for approved asset paths, asset-only scope, metadata, allowed statuses, visible placeholders, filler text, repository-root dependencies, literal `COPY`, fill-field wording, no-placeholder instructions, and review-class policy prose. |
| `scripts/test-skill-validator.py` | Adds positive and negative fixture coverage for spec-family asset layouts plus a baseline-summary presence check. |
| Canonical spec-family skill text | Unchanged in M1. |

### Proof-route decision

| Decision | Evidence | Result |
| --- | --- | --- |
| Existing `specs/skill-contract.md` plus `specs/spec-family-assets-progressive-disclosure.md` is sufficient for implementation to proceed. | `baseline.md` records existing packaged-resource coverage and the spec-family-specific contract. | No skill-contract spec amendment is needed before skill edits. |
| `spec-review` remains capped at two assets. | Approved spec requirements `SFA-R9` and `SFA-R10`; baseline asset count table. | No `review-dimension-row.md` asset is allowed. |

### Preservation matrix scaffold

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `spec` | Full spec output skeleton section set | `skills/spec/SKILL.md`, `## Output skeleton`, lines 211-258 | `skills/spec/assets/spec-skeleton.md` | Baseline section set recorded in `baseline.md`; extraction proof pending M2. |
| `spec` | Requirement row fields | `skills/spec/SKILL.md`, `## Requirements`, lines 228-229, and required-section guidance | `skills/spec/assets/requirement-row.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M2. |
| `spec` | Acceptance-criterion row fields | `skills/spec/SKILL.md`, `## Acceptance criteria`, lines 250-251, and required-section guidance | `skills/spec/assets/acceptance-criterion-row.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M2. |
| `spec` | Decision-log row fields | Existing proposal decision-log pattern and spec readiness/open-question guidance | `skills/spec/assets/decision-log-row.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M2. |
| `spec-review` | Review result skeleton fields | `skills/spec-review/SKILL.md`, `## Output skeleton`, lines 175-201 | `skills/spec-review/assets/review-result-skeleton.md` | Baseline field set recorded in `baseline.md`; extraction proof pending M3. |
| `spec-review` | Material-finding fields | `skills/spec-review/SKILL.md`, `## Material findings`, lines 85-94, and output skeleton findings block | `skills/spec-review/assets/review-finding.md` | Baseline field set recorded in `baseline.md`; extraction proof pending M3. |
| `test-spec` | Full test-spec output skeleton section set | `skills/test-spec/SKILL.md`, `## Output skeleton`, lines 152-245 | `skills/test-spec/assets/test-spec-skeleton.md` | Baseline section set recorded in `baseline.md`; extraction proof pending M4. |
| `test-spec` | Test-case fields | `skills/test-spec/SKILL.md`, `## Test case format`, lines 93-105, and output skeleton lines 187-198 | `skills/test-spec/assets/test-case.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M4. |
| `test-spec` | Coverage-map row fields | `skills/test-spec/SKILL.md`, output skeleton lines 171-181 | `skills/test-spec/assets/coverage-map-row.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M4. |
| `test-spec` | Edge-case row fields | `skills/test-spec/SKILL.md`, output skeleton lines 183-185 | `skills/test-spec/assets/edge-case-row.md` | Baseline repeated fields recorded in `baseline.md`; extraction proof pending M4. |

### M1 behavior parity

M1 does not edit canonical skill text or generated output. Behavior parity for
`spec`, `spec-review`, and `test-spec` therefore remains unchanged from the
approved PR #79 baseline. Representative behavior parity for each extracted
skill structure will be recorded in the milestone that changes that skill.
