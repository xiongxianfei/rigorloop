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

## M2. `spec` Assets

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/spec/SKILL.md` | Added a `Resource map`, kept rules, stop/status-settlement boundaries, closed enums, routing, claim boundaries, and validation guidance in `SKILL.md`, and replaced the full inline skeleton with compact output guidance that points to `assets/spec-skeleton.md`. |
| `skills/spec/assets/spec-skeleton.md` | Added the full spec output skeleton with the same required section set as the PR #79 baseline. |
| `skills/spec/assets/requirement-row.md` | Added the repeated requirement row structure while preserving the full requirement statement field and leaving modal guidance in `SKILL.md`. |
| `skills/spec/assets/acceptance-criterion-row.md` | Added the repeated acceptance-criterion row structure matching the existing output skeleton acceptance-criterion format. |
| `skills/spec/assets/decision-log-row.md` | Added the capped structural decision-log row asset recorded in the approved plan. |
| `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md` | Refined the `spec` repeated-substructure wording so examples and edge cases remain required full-skeleton sections rather than per-requirement row fields. |

### Preservation matrix

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `spec` | Full spec output skeleton section set | `skills/spec/SKILL.md`, previous `## Output skeleton` | `skills/spec/assets/spec-skeleton.md` | Same 21 section headings are present: `Status`, `Related proposal`, `Goal and context`, `Glossary`, `Examples first`, `Requirements`, `Inputs and outputs`, `State and invariants`, `Error and boundary behavior`, `Compatibility and migration`, `Observability`, `Security and privacy`, `Accessibility and UX`, `Performance expectations`, `Edge cases`, `Non-goals`, `Acceptance criteria`, `Open questions`, `Next artifacts`, `Follow-on artifacts`, `Readiness`. |
| `spec` | Requirement row fields | Previous output skeleton `Requirements` row and requirement-format guidance | `skills/spec/assets/requirement-row.md` | Preserves requirement ID plus full requirement statement field: `<requirement ID>. <requirement statement>.` Requirement modal guidance, rules, and testability obligation remain in `SKILL.md`. |
| `spec` | Acceptance-criterion row fields | Previous output skeleton `Acceptance criteria` row | `skills/spec/assets/acceptance-criterion-row.md` | Preserves acceptance-criterion ID plus observable outcome shape: `<acceptance criterion ID>. <observable acceptance outcome>.` |
| `spec` | Decision-log row fields | Approved plan per-asset justification and proposal decision-log pattern | `skills/spec/assets/decision-log-row.md` | Preserves structural row fields: date, decision, reason, alternatives rejected. |

### Behavior parity

| Baseline surface | M2 result |
| --- | --- |
| Required sections | Same 21 required sections remain listed in `SKILL.md`; `assets/spec-skeleton.md` carries the same full section set. |
| Closed enums | Spec status and settlement-result enum blocks remain unchanged in `SKILL.md`. |
| Rules and stop conditions | Upstream status settlement blockers, artifact placement, authoring rules, evidence guidance, full-file-read guidance, workflow handoff behavior, and claim boundaries remain in `SKILL.md`. |
| Output obligation | `SKILL.md` still exposes an `Output skeleton` section and `Expected output`; the full skeleton structure is copied from `assets/spec-skeleton.md` rather than duplicated inline. |
| Placeholder behavior | Assets contain visible placeholders as templates; M2 does not create a final representative output artifact, so no final output placeholder leak is introduced in this slice. |

#### Requirement modal preservation

The asset `assets/requirement-row.md` now uses:

```text
<requirement ID>. <requirement statement>.
```

This preserves all representative requirement statement forms owned by
`skills/spec/SKILL.md`:

- `R1. The system MUST ...`
- `R2. The API MUST NOT ...`
- `R3. The UI SHOULD ... because ...`

No modal value is added, removed, or made preferred by the asset.

### Asset contract check

| Asset | Metadata | Resource-map entry | Placeholder | Hidden-rule check |
| --- | --- | --- | --- | --- |
| `assets/spec-skeleton.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural skeleton only; rules and enums remain in `SKILL.md`. |
| `assets/requirement-row.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural row only; requirement rules remain in `SKILL.md`. |
| `assets/acceptance-criterion-row.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural row only. |
| `assets/decision-log-row.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural row only. |

### Token and cold-read evidence

| Measurement | Baseline `spec/SKILL.md` | M2 `spec/SKILL.md` | M2 packaged assets |
| --- | ---: | ---: | ---: |
| Lines | 264 | 238 | 111 |
| Bytes | 10,686 | 10,573 | 2,005 |
| Estimated tokens | 2,672 | 2,641 | 502 |

Common-path `SKILL.md` size decreased by 26 lines, 113 bytes, and 31
estimated tokens. Packaged asset footprint is recorded separately from the
common path.

Cold-read result: the installed `spec` skill body names every packaged asset in
`Resource map`, states when each asset is copied, names the fields or
structures to fill, and instructs the agent not to emit unfilled placeholders.
The `Output skeleton` and `Expected output` sections tell the agent to use the
full skeleton asset and repeated row assets without needing repository-internal
paths or generated-output knowledge.

## M3. `spec-review` Assets

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/spec-review/SKILL.md` | Added a `Resource map`, kept review dimensions, verdict enum, severity policy, material-finding sufficiency rules, recording obligations, lifecycle boundaries, routing, claim boundaries, and validation guidance in `SKILL.md`, and replaced the inline result skeleton with compact asset-copy guidance. |
| `skills/spec-review/assets/review-result-skeleton.md` | Added the structural review result scaffold with result fields, findings area, eventual test-spec readiness, and stop condition placeholders. |
| `skills/spec-review/assets/review-finding.md` | Added the structural material-finding block with the same field labels as the existing material-finding contract. |
| `scripts/skill_validation.py` | Tightened the review-class policy-prose detector so allowed field-label lines remain valid while policy prose is still rejected. |
| `scripts/test-skill-validator.py` | Updated the valid spec-family asset fixture to prove review-class field labels such as `Recording status` are accepted. |

### Preservation matrix

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `spec-review` | Review result fields | Previous `skills/spec-review/SKILL.md` output skeleton | `skills/spec-review/assets/review-result-skeleton.md` | Preserves result fields for skill, review status, material findings, recording status, recording blocker, review record, review log, review resolution, open blockers, immediate next stage, eventual test-spec readiness, and stop condition. Review outcome rules and recording obligations remain in `SKILL.md`. |
| `spec-review` | Material-finding fields | `skills/spec-review/SKILL.md`, `## Material findings`, and previous output skeleton finding block | `skills/spec-review/assets/review-finding.md` | Preserves structural fields for finding ID, summary, severity, location, evidence, required outcome, and safe resolution path or needs-decision rationale. Finding sufficiency rules and severity policy remain in `SKILL.md`. |

### Behavior parity

| Baseline surface | M3 result |
| --- | --- |
| Review dimensions | Same ten review dimensions remain listed in `SKILL.md`; no review-dimension asset was created. |
| Closed enums | Review dimension verdict enum remains unchanged in `SKILL.md`. |
| Review rules and stop conditions | Review judgment, vague/untestable requirement rules, finding sufficiency, isolation/recording obligations, handoff boundaries, and inconclusive stop conditions remain in `SKILL.md`. |
| Material-finding shape | `assets/review-finding.md` preserves the same material-finding fields while adding no review policy prose. |
| Recording behavior | Recording obligations remain in `SKILL.md`; `assets/review-result-skeleton.md` preserves the result fields for review record, review log, review resolution, recording status, and recording blocker. |
| Placeholder behavior | Assets contain visible placeholders as templates; M3 does not create a final representative output artifact, so no final output placeholder leak is introduced in this slice. |

### Review-class asset boundary

| Asset | Metadata | Resource-map entry | Placeholder | Hidden-rule check |
| --- | --- | --- | --- | --- |
| `assets/review-result-skeleton.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural result scaffold only; review dimensions, verdicts, recording rules, and review policy remain in `SKILL.md`. |
| `assets/review-finding.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Structural finding block only; severity policy and material-finding sufficiency rules remain in `SKILL.md`. |

### Token and cold-read evidence

| Measurement | Baseline `spec-review/SKILL.md` | M3 `spec-review/SKILL.md` | M3 packaged assets |
| --- | ---: | ---: | ---: |
| Lines | 205 | 196 | 43 |
| Bytes | 9,206 | 9,077 | 1,210 |
| Estimated tokens | 2,302 | 2,269 | 302 |

Common-path `SKILL.md` size decreased by 9 lines, 129 bytes, and 33
estimated tokens. Packaged asset footprint is recorded separately from the
common path.

Cold-read result: the installed `spec-review` skill body names both packaged
assets in `Resource map`, states when each asset is copied, names the fields or
structures to fill, and instructs the agent not to emit unfilled placeholders.
The `Output skeleton` and `Expected output` sections tell the agent to use the
result asset and material-finding asset while keeping review dimensions,
verdicts, finding sufficiency, severity policy, and recording obligations in
`SKILL.md`.
