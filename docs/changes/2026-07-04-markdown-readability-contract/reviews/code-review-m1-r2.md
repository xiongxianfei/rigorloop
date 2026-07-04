# Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1. Readability Validator and Deterministic Fixtures
Reviewed artifact: commit `34d4aaf8`
Review date: 2026-07-04
Reviewed commit: `34d4aaf8`
Status: changes-requested
Review status: changes-requested
Material findings: MDREAD-M1-CR2
Recording status: recorded
Recording blocker: none
Reviewed milestone: M1
Milestone closeout: resolution-needed
Required review-resolution: yes
Immediate next stage: review-resolution M1
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-07-04-markdown-readability-contract/reviews/code-review-m1-r2.md
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: MDREAD-M1-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-04-markdown-readability-contract/reviews/code-review-m1-r2.md
- Review log: docs/changes/2026-07-04-markdown-readability-contract/review-log.md
- Review resolution: docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md#code-review-m1-r2
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2
- Required review-resolution: yes
- Finding IDs: MDREAD-M1-CR2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: commit `34d4aaf8 M1: resolve readability selector changed sections`, compared against prior M1 implementation commit `7426647f`.
- Tracked governing branch state: proposal, approved spec, active test spec, active plan, code-review R1 record, and accepted `MDREAD-M1-CR1` resolution are tracked through commit `34d4aaf8`.
- Governing artifacts: `specs/markdown-readability-contract.md`, `specs/markdown-readability-contract.test.md`, `docs/plans/2026-07-04-markdown-readability-contract.md`, `docs/changes/2026-07-04-markdown-readability-contract/reviews/code-review-m1-r1.md`, `docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md`.
- Validation evidence: M1 validation notes in `docs/plans/2026-07-04-markdown-readability-contract.md` and `docs/changes/2026-07-04-markdown-readability-contract/change.yaml`.

## Diff summary

The resolution commit adds `changed_sections` metadata to selector-selected checks, renders `--changed-section` arguments into `markdown_readability.validate` commands, derives README and `VISION.md` ranges from PR/main and local git diffs, falls back to a whole-file range when no hunks are available, and adds selector tests for README/`VISION.md` command shape plus a PR-mode README hard-wrap command failure regression.
It also records the R1 review finding, its accepted resolution, validation evidence, and the M1 rerun handoff state.

## Findings

### MDREAD-M1-CR2 - No-hunk fallback over-enforces historical README and VISION content

Finding ID: MDREAD-M1-CR2
Severity: major
Location: `scripts/validation_selection.py:1033`, `scripts/validation_selection.py:1035`, `scripts/test-select-validation.py:2532`
Evidence: The approved spec requires first-slice README and `VISION.md` semantic source-line checks to apply only to changed sections, and untouched historical README/`VISION.md` sections must remain audit-only. The R2 selector derives git hunks when available, but `_resolve_changed_sections` replaces an empty hunk set with `_whole_file_section`, so explicit path selection without git hunks emits `--changed-section README.md:1:N` or `--changed-section VISION.md:1:N`. The new README selector test asserts `README.md:1:3`, making this over-broad fallback intentional test behavior. Direct reproduction against an explicit README path with an old split `proposal to` / `spec` phrase shows the selected command shape as `python scripts/validate-markdown-readability.py README.md --changed-section README.md:1:6`, and running that command fails with `ERROR MDREAD-001` for the historical split even though no actual changed-section range identifies those lines.
Required outcome: Selector-composed README and `VISION.md` readability validation must not treat an unknown or unavailable changed-section range as whole-file enforcement for existing historical content. It must either derive exact changed ranges, restrict whole-file changed-section fallback to genuinely new/untracked files where the whole file is the change, or avoid claiming changed-section enforcement when exact ranges are unavailable.
Safe resolution path: Replace the unconditional `_whole_file_section` fallback with a bounded policy. For PR/main and local modes, use git hunk ranges and add regression coverage for an untouched historical split outside the changed hunk. For explicit/non-git cases, either require caller-supplied changed-section ranges, omit changed-section enforcement with a clear non-enforcement/audit-only command shape, or apply whole-file fallback only when the file is newly added/untracked and therefore the whole file is actually changed. Update selector tests so explicit existing-file fixtures do not assert whole-file enforcement, and rerun selector, readability, metadata, review-artifact, lifecycle, and whitespace validation.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `MDREAD-M1-CR2`: R32/R33 require changed-section-only enforcement and historical audit-only behavior, but no-hunk fallback enforces the whole file. |
| Test coverage | concern | The PR-mode README regression proves the selected command can fail a changed hard-wrap, but the explicit README test now locks in over-broad whole-file changed-section behavior. |
| Edge cases | block | T3/EC6 require untouched historical sections to remain audit-only or out of scope; direct reproduction shows explicit path selection can fail an untouched historical split. |
| Error handling | concern | Git hunk derivation failure silently broadens scope to whole-file enforcement instead of surfacing unavailable changed-section information or using audit-only behavior. |
| Architecture boundaries | pass | The change remains inside repository-owned validation selector and test scripts; no architecture artifact was required. |
| Compatibility | concern | Existing explicit-path validation workflows can become stricter than the approved first slice and fail historical README/`VISION.md` text without a migration decision. |
| Security/privacy | pass | The diff reads local git diffs and local Markdown paths only; no secrets, network state, or external data are introduced. |
| Derived artifact currency | pass | No generated adapter or derived skill output is changed in this M1 resolution slice. |
| Unrelated changes | pass | The implementation diff is scoped to selector support, selector tests, and lifecycle/review evidence. |
| Validation evidence | concern | Recorded validation commands passed, but they do not include a negative regression proving historical hard-wrap text outside the changed hunk remains audit-only for selector-composed commands. |

## Recommended next stage

`review-resolution M1` for `MDREAD-M1-CR2`, followed by targeted implementation fixes and rerun `code-review`.

## Milestone handoff

- Reviewed milestone: M1
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2
- Next stage: review-resolution M1
- Final closeout readiness: not ready; M1 has an open material finding and M2 remains unimplemented.
