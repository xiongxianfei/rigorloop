# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M4. `test-spec` assets
Reviewed artifact: commit `ab59028` (`M4: add test-spec assets`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: SFA-M4-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/reviews/code-review-m4-r1.md
- Review log: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-log.md
- Review resolution: docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md
- Reviewed milestone: M4. `test-spec` assets
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5
- Required review-resolution: yes
- Finding IDs: SFA-M4-CR1
- Verify readiness: not-claimed

## Scope

Reviewed the M4 `test-spec` asset extraction against the actual diff, approved
spec and test spec, active plan M4 scope, changed `test-spec` skill/assets,
behavior-preservation evidence, and recorded validation evidence.

## Review inputs

- Diff/review surface: `git show ab59028 -- skills/test-spec/SKILL.md skills/test-spec/assets docs/changes/2026-05-20-spec-family-assets-progressive-disclosure docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md docs/plan.md`
- Tracked governing branch state: commit `ab59028` on `proposal/spec-family-assets-progressive-disclosure`
- Governing artifacts:
  - `specs/spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
- Validation evidence:
  - `python scripts/validate-skills.py skills/test-spec/SKILL.md`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `git diff --check -- .`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md --path docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md --path docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md --path docs/plan.md`

## Diff summary

- Added `skills/test-spec/assets/test-spec-skeleton.md`,
  `skills/test-spec/assets/test-case.md`,
  `skills/test-spec/assets/coverage-map-row.md`, and
  `skills/test-spec/assets/edge-case-row.md`.
- Added `skills/test-spec/SKILL.md` resource-map entries for those assets.
- Replaced the inline full output skeleton with compact guidance pointing to
  the full skeleton and repeated-structure assets.
- Recorded M4 preservation, behavior-parity, token, cold-read, lifecycle, and
  validation evidence, and moved M4 to `review-requested`.

## Findings

### SFA-M4-CR1 - Coverage-map row extraction does not preserve table row shapes

Finding ID: SFA-M4-CR1
Severity: major

Location:

- `skills/test-spec/assets/test-spec-skeleton.md`, lines 24-32
- `skills/test-spec/assets/coverage-map-row.md`, line 6
- `skills/test-spec/SKILL.md`, lines 77-79
- `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`, M4 preservation matrix coverage-map row

Evidence:

The approved spec requires source-to-asset field parity and representative
behavior parity for `test-spec` structures (`SFA-R28`, `SFA-R29`, `SFA-R31`).
The pre-extraction output skeleton had concrete table rows matching each table
shape:

- requirement coverage map: four cells, `Requirement ID`, `Covered by`,
  `Level`, and `Notes`;
- example coverage map: three cells, `Example`, `Covered by`, and `Notes`;
- edge case coverage: list row shape, now separately represented by
  `edge-case-row.md`.

The extracted full skeleton keeps the table headers but replaces row structure
with a single-cell placeholder row:

```md
| <requirement coverage rows> |
| <example coverage rows> |
```

The repeated `coverage-map-row.md` asset has a four-cell row:

```md
| <coverage target> | <covered by test IDs or manual verification> | <coverage map level or notes> | <notes> |
```

That four-cell row does not fit the three-column example coverage table. The
resource map says to copy the same asset for each "requirement, example, or
traceability coverage-map row", so following the installed skill can produce a
malformed example coverage map or add a new level column where the baseline
did not have one.

Required outcome:

Restore coverage-map structural parity so the full skeleton and repeated
coverage asset preserve the original row shapes and do not instruct agents to
copy a four-cell row into the three-column example coverage table.

Safe resolution path:

- Update `assets/test-spec-skeleton.md` so the requirement coverage map includes
  a four-cell placeholder row and the example coverage map includes a three-cell
  placeholder row.
- Update `assets/coverage-map-row.md` and its `SKILL.md` resource-map entry so
  it has an unambiguous scope that matches its row shape. If one asset must
  cover both requirement and example rows under the approved four-asset cap,
  make the asset explicitly contain both structural variants without adding
  rules or coverage obligations.
- Update M4 behavior-preservation evidence to record the exact preserved row
  shapes.
- Rerun M4 validation and return M4 to code review.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `SFA-R28`, `SFA-R29`, and `SFA-R31` require field and behavior parity; the coverage-map extraction changes row shape for requirement/example coverage rows. |
| Test coverage | concern | Validator tests pass, but they do not catch table cell-count parity for extracted skeleton rows. |
| Edge cases | block | The named M4 proof case requires every extracted field to map to baseline source content; the example coverage row has no direct preserved three-cell structure. |
| Error handling | pass | No runtime error path changed; the issue is structural artifact output drift. |
| Architecture boundaries | pass | No architecture, adapter root, lockfile, CLI, or release trust-boundary changes are introduced. |
| Compatibility | concern | Existing test-spec output readers expecting the example coverage table's three-column shape could receive a four-column row if the shared asset is copied there. |
| Security/privacy | pass | No secrets, credentials, unsafe logging, or security-sensitive behavior is introduced. |
| Derived artifact currency | pass | M4 does not own generated mirror/archive proof; M5 remains responsible for generated output. |
| Unrelated changes | pass | The diff is scoped to M4 `test-spec` assets, evidence, and lifecycle state. |
| Validation evidence | concern | Recorded validation commands passed, but the defect is outside the current deterministic validator coverage. |

## No-finding rationale

Not applicable. One material finding requires changes before M4 can close.

## Residual risks

M5 remains open. Generated skill mirror and temporary adapter archive proof are
still planned for M5 and are not claimed by this review.

## Handoff

- Reviewed milestone: M4. `test-spec` assets
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5
- Required review-resolution: yes, for `SFA-M4-CR1`
- Recommended next stage: review-resolution / implement M4 fix
- Final closeout readiness: not ready; M4 has an open finding, and M5, explain-change, verify, and PR handoff remain open.
- Automatic downstream handoff: none from this isolated code-review invocation.
