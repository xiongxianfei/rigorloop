# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M2. `spec` assets
Reviewed artifact: commit `b8893fd` (`M2: add spec assets`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Scope

Reviewed the M2 implementation slice against the approved spec, active test
spec, active plan, implementation diff, `spec` asset files, preservation
evidence, token/cold-read evidence, and recorded validation evidence.

## Review inputs

- Diff: `git show --unified=80 --no-ext-diff --no-renames b8893fd -- skills/spec/SKILL.md skills/spec/assets docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- Plan: `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
- Spec: `specs/spec-family-assets-progressive-disclosure.md`
- Test spec: `specs/spec-family-assets-progressive-disclosure.test.md`
- Baseline: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`
- Preservation evidence: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
- Validation evidence: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`

## Diff summary

- Added `skills/spec/assets/spec-skeleton.md`,
  `skills/spec/assets/requirement-row.md`,
  `skills/spec/assets/acceptance-criterion-row.md`, and
  `skills/spec/assets/decision-log-row.md`.
- Added a `Resource map` to `skills/spec/SKILL.md` with `COPY` entries for all
  four packaged assets.
- Replaced the full inline `spec` output skeleton with compact output guidance
  that points to `assets/spec-skeleton.md`.
- Updated change-local baseline, preservation, behavior-parity, token, cold-read,
  plan, plan index, and change metadata evidence for M2.

## Findings

### SFA-M2-CR1 - Major: `requirement-row.md` narrows the allowed requirement modal verbs

Finding ID: SFA-M2-CR1
Severity: major
Location: `skills/spec/assets/requirement-row.md:6`; `skills/spec/SKILL.md:153`

Evidence:
`skills/spec/SKILL.md` still defines the requirement format with all three
representative normative forms:

```text
R1. The system MUST ...
R2. The API MUST NOT ...
R3. The UI SHOULD ... because ...
```

The extracted row asset hard-codes only one of those forms:

```text
<requirement ID>. The system MUST <testable behavior>.
```

The M2 preservation evidence also records this hard-coded `MUST` shape as the
preserved row, rather than preserving the broader requirement statement field.

Problem:
This is an asset extraction pass. `SFA-R3`, `SFA-R4`, `SFA-R28`, `SFA-R29`,
`SFA-R30`, and `SFA-R31` require assets to remain structural and preserve
field obligations and behavior. The new asset makes the copy-and-fill
requirement row structurally prefer only `MUST`, which can silently drop the
existing `MUST NOT` and `SHOULD ... because ...` forms that remain part of the
authoritative `spec` skill contract.

Required outcome:
Preserve the requirement row as a structural template for the whole requirement
statement, without narrowing the allowed normative modal forms.

Safe resolution path:
Change `assets/requirement-row.md` to use a neutral requirement-statement
placeholder, for example:

```text
<requirement ID>. <requirement statement>.
```

Then update the `SKILL.md` resource-map fill text and the M2 baseline /
behavior-preservation evidence to say the asset preserves requirement ID and
requirement statement, while the authoritative modal guidance remains in
`SKILL.md`. Rerun the M2 validation commands and return M2 to code review.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `SFA-R3`, `SFA-R28`, `SFA-R29`, `SFA-R30`, and `SFA-R31` require structural extraction and behavior parity, but `requirement-row.md` narrows requirement rows to `MUST`. |
| Test coverage | concern | Validator coverage proves asset metadata, mapping, placeholders, and resource-map shape, but does not catch modal narrowing inside the structural row. |
| Edge cases | concern | `EC1` full-skeleton discoverability is handled, but behavior parity for requirement row variants has a direct proof gap because `MUST NOT` and `SHOULD` are not preserved in the asset shape. |
| Error handling | pass | No runtime error handling is changed; placeholders remain visible and validators reject unfilled-placeholder policy gaps. |
| Architecture boundaries | pass | No architecture, adapter root, lockfile, CLI, or release trust-boundary changes are introduced. |
| Compatibility | concern | Existing spec authors can still read the modal guidance in `SKILL.md`, but the copied asset structure steers generated requirements toward only one modal form. |
| Security/privacy | pass | No secrets, credentials, private data flows, auth behavior, unsafe logging, or external service use is introduced. |
| Derived artifact currency | pass | M2 does not own generated skill mirror or temporary adapter archive proof; those remain assigned to M5. Canonical skill validation passes. |
| Unrelated changes | pass | The diff is scoped to `spec` assets, `spec` skill text, and M2 lifecycle evidence. |
| Validation evidence | pass | Recorded M2 commands are relevant and pass, but passing validation does not prove requirement modal parity. |

## Required review-resolution

Yes. `SFA-M2-CR1` must be resolved before M2 can close or M3 can begin.

## Handoff

- Reviewed milestone: M2. `spec` assets
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Recommended next stage: review-resolution / implement M2 fix
- Final closeout readiness: not ready
- Automatic downstream handoff: none from this isolated code-review invocation.
