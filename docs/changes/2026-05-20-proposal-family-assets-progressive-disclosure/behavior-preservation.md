# Proposal-Family Assets Progressive Disclosure Behavior Preservation

## Status

active

This artifact records source-to-asset preservation proof for the proposal-family
assets pass. M1 established the pinned baseline and validator foundation before
skill text changes. M2 added the `proposal` skeleton asset. M3 adds the narrow
`proposal-review` structural assets and records the behavior-preservation
evidence for that extraction.

## M1. Baseline And Validator Foundation

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md` | Created before skill edits; records source commit, source hashes, existing skeleton sections, conditional sections, closed enums, rule ownership, review dimensions, recording obligations, and planned asset destinations. |
| `scripts/skill_validation.py` | Adds deterministic proposal-family asset checks for approved asset paths, asset-only scope, metadata, allowed statuses, visible placeholders, filler text, repository-root dependencies, literal `COPY`, fill-field wording, no-placeholder instructions, generated-output presence helpers, and proposal-review review-class policy boundaries. |
| `scripts/test-skill-validator.py` | Adds positive and negative fixture coverage for proposal-family asset layouts plus baseline-summary presence and review-class label checks. |
| Canonical proposal-family skill text | Unchanged in M1. |

### M1 behavior parity

M1 did not edit canonical skill text or generated output. Behavior parity for
`proposal` and `proposal-review` therefore remained unchanged from the pinned
baseline. Per-skill extraction evidence is recorded in the milestone that
changes each skill.

### Skill-contract sufficiency reassessment before M2

Existing `specs/skill-contract.md` packaged-resource rules, the approved
proposal-family spec, the active test spec, and the M1 validator foundation are
sufficient for the M2 `proposal` full-skeleton asset extraction. No
skill-contract amendment is required before M2 because the M2 scope uses the
approved `assets/proposal-skeleton.md` inventory, keeps rules and conditional
triggers in `SKILL.md`, and does not change generated-output mechanics.

## M2. Proposal Skeleton Asset

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/proposal/SKILL.md` | Added a `Resource map`, kept routing, evidence access, artifact placement, required section guidance, closed enums, Vision fit rules, standing artifact gates, scope-preservation rules, scope-budget rules, decision-quality checks, workflow handoff, and output obligations in `SKILL.md`, and replaced the full inline skeleton with compact asset-copy guidance. |
| `skills/proposal/assets/proposal-skeleton.md` | Added the full proposal output skeleton with the same section set as the pinned baseline. |
| Inline row formats | Initial-intent rows, scope-budget rows, decision-log rows, risk rows, and similar small table rows remain in `SKILL.md`; no row-only assets are added in M2. |
| Conditional proposal sections | `Initial intent preservation` and `Scope budget` remain trigger-based and governed by `SKILL.md`; the `Resource map` and compact output guidance instruct insertion only when triggers apply. |

### Preservation matrix

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `proposal` | Full proposal output skeleton section set | `skills/proposal/SKILL.md`, previous `## Output skeleton` | `skills/proposal/assets/proposal-skeleton.md` | Same section headings are present: `Status`, `Problem`, `Goals`, `Non-goals`, `Vision fit`, `Context`, `Options Considered`, `Recommended Direction`, `Expected Behavior Changes`, `Architecture Impact`, `Testing and Verification Strategy`, `Rollout and Rollback`, `Risks and Mitigations`, `Open Questions`, `Decision Log`, `Next Artifacts`, `Follow-on Artifacts`, and `Readiness`. |
| `proposal` | Conditional `Initial intent preservation` section | `skills/proposal/SKILL.md`, `## Scope preservation` | `SKILL.md` trigger guidance plus resource-map insertion instruction | Preserves the trigger for broad, multi-part, or materially revised requests. The section is not made mandatory for every proposal and remains available when triggered. |
| `proposal` | Conditional `Scope budget` section | `skills/proposal/SKILL.md`, `## Scope budget for broad proposals` | `SKILL.md` trigger guidance plus resource-map insertion instruction | Preserves the trigger for broad or multi-workstream proposals. The section is not made mandatory for every proposal and remains available when triggered. |
| `proposal` | Initial-intent, scope-budget, decision-log, and risk row formats | Inline format guidance and required-section guidance | `SKILL.md` inline guidance | Preserves row shapes inline and avoids metadata-heavy one-line assets. |

### Behavior parity

| Baseline surface | M2 result |
| --- | --- |
| Required sections | Same required proposal sections remain listed in `SKILL.md`; `assets/proposal-skeleton.md` carries the same full skeleton section set from the pinned baseline. |
| Closed enums | Proposal status, Vision fit, initial goal treatment, and scope budget treatment enum blocks remain unchanged in `SKILL.md`. |
| Vision fit and standing gates | Vision fit rules, root `VISION.md` behavior, root `CONSTITUTION.md` behavior, and bootstrap exception behavior remain in `SKILL.md`. |
| Scope preservation | Initial-goal extraction, traceability, no-silent-drop guidance, and intentional narrowing guidance remain in `SKILL.md`. |
| Scope budget | Scope-budget triggers, treatment values, and follow-up ownership routing remain in `SKILL.md`. |
| Rules and handoff | Proposal rules, evidence guidance, artifact placement, full-file-read guidance, workflow handoff behavior, and claim boundaries remain in `SKILL.md`. |
| Output obligation | `SKILL.md` still exposes `Output skeleton` and `Expected output`; the full copy-and-fill structure is copied from `assets/proposal-skeleton.md` rather than duplicated inline. |
| Placeholder behavior | The asset contains visible placeholders as a template. M2 does not create a final representative proposal artifact, so no final output placeholder leak is introduced in this slice. |

### Asset contract check

| Asset | Metadata | Resource-map entry | Placeholder | Hidden-rule check |
| --- | --- | --- | --- | --- |
| `assets/proposal-skeleton.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, conditional section insertion behavior, and no-placeholder instruction. | Visible placeholders present. | Structural skeleton only; rules, gates, enums, conditional triggers, and handoff behavior remain in `SKILL.md`. |

## M3. Proposal-Review Structural Assets

### Same-slice scope

| Surface | Treatment |
| --- | --- |
| `skills/proposal-review/SKILL.md` | Added a `Resource map`, kept routing, evidence access, artifact placement, review dimensions, review dimension result enum, Vision fit review, vision conflict outcome enum, standing artifact gate review, scope preservation, scope-budget review, material-finding sufficiency, recording status enum, review status enum, isolation and recording rules, workflow handoff, and expected output obligations in `SKILL.md`, and replaced the full inline skeleton with compact asset-copy guidance. |
| `skills/proposal-review/assets/review-result-skeleton.md` | Added the approved review result skeleton structure with the preserved `## Result` heading, literal `Skill` field, result fields, material findings, review dimensions, scope-preservation result, recommended edits, and recommendation fields only. |
| `skills/proposal-review/assets/material-finding.md` | Added the approved material-finding structure with finding ID, severity, location, evidence, required outcome, safe resolution path, and needs-decision rationale fields only. |
| Review judgment and policy | Remain in `SKILL.md`; no review dimensions, status values, sufficiency rules, scope rules, Vision fit rules, standing artifact gate rules, recording rules, handoff rules, architecture guidance, testability guidance, risk guidance, security examples, privacy examples, or rollout examples were moved into assets. |

### Preservation matrix

| Skill | Source content | Existing location | Asset destination | Preservation proof |
| --- | --- | --- | --- | --- |
| `proposal-review` | Result block heading | `skills/proposal-review/SKILL.md`, previous `## Output skeleton`, `## Result` block | `skills/proposal-review/assets/review-result-skeleton.md` | Preserves the baseline `## Result` heading. |
| `proposal-review` | Skill field | `skills/proposal-review/SKILL.md`, previous `## Output skeleton`, `## Result` block | `skills/proposal-review/assets/review-result-skeleton.md` | Preserves the literal `- Skill: proposal-review` field. |
| `proposal-review` | Review result fields | `skills/proposal-review/SKILL.md`, previous `## Output skeleton`, `## Result` block | `skills/proposal-review/assets/review-result-skeleton.md` | Preserves Skill, review status, material findings, recording status, recording blocker, review record, review log, review resolution, open blockers, and immediate next stage fields as structural labels. |
| `proposal-review` | Review dimensions result area | `skills/proposal-review/SKILL.md`, previous `## Output skeleton`, `## Review Dimensions` block | `skills/proposal-review/assets/review-result-skeleton.md` | Preserves the review dimensions output slot as a structural placeholder while the review dimensions table and result enum remain in `SKILL.md`. |
| `proposal-review` | Scope preservation, recommended edits, and recommendation areas | `skills/proposal-review/SKILL.md`, previous `## Output skeleton` | `skills/proposal-review/assets/review-result-skeleton.md` | Preserves structural placeholders for scope-preservation result, recommended edits, and recommendation while all review rules remain in `SKILL.md`. |
| `proposal-review` | Material finding fields | `skills/proposal-review/SKILL.md`, `## Material findings` and previous `## Output skeleton`, `## Material Findings` block | `skills/proposal-review/assets/material-finding.md` | Preserves finding ID, severity, location, evidence, required outcome, safe resolution path, and needs-decision rationale fields. |

### Behavior parity

| Baseline surface | M3 result |
| --- | --- |
| Review dimensions | The dimension table and `pass`, `concern`, `block` result enum remain unchanged in `SKILL.md`. The asset includes only a `Review dimensions` structural placeholder. |
| Vision fit and standing gates | Vision fit review, Vision fit enum, vision conflict outcome enum, bootstrap exception behavior, and standing artifact gate review remain unchanged in `SKILL.md`. |
| Scope preservation and scope budget | Initial-goal treatment enum, scope-preservation failure behavior, scope-budget treatment enum, broad-proposal checks, and no-silent-narrowing behavior remain unchanged in `SKILL.md`. |
| Material findings | Sufficiency rules and required field obligations remain unchanged in `SKILL.md`; `assets/material-finding.md` provides only the copy-and-fill field structure. |
| Recording and review statuses | Recording status and review status enum blocks remain unchanged in `SKILL.md`. |
| Isolation and handoff | Isolation, formal recording behavior, no automatic downstream handoff, and proposal-review gate behavior remain unchanged in `SKILL.md`. |
| Output obligation | `SKILL.md` still exposes `Output skeleton` and `Expected output`; the structural copy-and-fill blocks are copied from the two approved assets rather than duplicated inline. |
| Placeholder behavior | The assets contain visible placeholders as templates. M3 does not create a final representative proposal-review artifact, so no final output placeholder leak is introduced in this slice. |

### Asset contract check

| Asset | Metadata | Resource-map entry | Placeholder | Hidden-rule check |
| --- | --- | --- | --- | --- |
| `assets/review-result-skeleton.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names trigger, fill structures, and no-placeholder instruction. | Visible placeholders present. | Contains headings, approved field labels, and placeholders only; no review policy, rules, enums, dimensions guidance, recording rules, or handoff behavior. |
| `assets/material-finding.md` | Template, Skill, Template status, and Maintained alongside present. | `COPY` entry names per-finding trigger, fill fields, and no-placeholder instruction. | Visible placeholders present. | Contains headings, approved field labels, and placeholders only; no material-finding sufficiency rule, severity policy, or safe-resolution decision rule. |
