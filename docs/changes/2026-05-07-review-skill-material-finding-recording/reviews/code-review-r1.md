# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: working tree diff for M1-M3 review skill material-finding recording implementation
Status: changes-requested

## Review inputs

- Diff surface: working tree diff and untracked files for the review skill material-finding recording change.
- Spec: `specs/formal-review-recording.md`
- Spec: `specs/review-finding-resolution-contract.md`
- Spec: `specs/rigorloop-workflow.md`
- Test specs: `specs/formal-review-recording.test.md`, `specs/review-finding-resolution-contract.test.md`, `specs/rigorloop-workflow.test.md`
- Plan: `docs/plans/2026-05-07-review-skill-material-finding-recording.md`
- Validation evidence: commands recorded in `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`

## Diff summary

The implementation adds the canonical shared `Isolation and Recording`
subsection, copies it into the five formal review skills, adds static
assertions for shared-block equality and broad material-finding wording,
adds scan-first review-resolution template coverage, refreshes generated
skill and adapter output, and updates plan/change-local evidence.

## Findings

### CR1-F1 - Shared timing rule weakens a MUST to should

Finding ID: CR1-F1
Severity: major
Evidence: `templates/shared/review-isolation-and-recording.md` says "The durable record should be created before review-driven edits begin." `specs/formal-review-recording.md` `R6` says material findings "MUST be recorded before review-driven fixes proceed", and `specs/review-finding-resolution-contract.md` `R2m` says material review findings "MUST be recorded before fixes begin."
Required outcome: The canonical shared review block and copied/generated review-skill guidance must use mandatory wording for the before-fix recording rule, matching the approved spec.
Safe resolution: Change the canonical shared block to say the durable record `must` be created before review-driven edits begin; recopy the byte-identical block into all five formal review skills; regenerate `.codex/skills/` and public adapter output; tighten or add static assertion coverage for the mandatory timing wording; rerun the selected skill, review-artifact, adapter, lifecycle, metadata, selector, whitespace, and explicit CI validation.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | The shared skill guidance weakens a spec-level MUST for timing. |
| Test coverage | concern | Static coverage checks broad wording but does not assert mandatory timing strength. |
| Edge cases | concern | The first-pass timing edge case is present but not enforced strongly enough in skill text. |
| Error handling | pass | No runtime error-handling change is involved. |
| Architecture boundaries | pass | The implementation reuses existing skill/template/generator boundaries. |
| Compatibility | concern | Generated outputs mirror the same weakened guidance. |
| Security/privacy | pass | No sensitive data exposure found in reviewed surfaces. |
| Generated output drift | pass | Drift checks passed, but generated output correctly mirrors the flawed canonical wording. |
| Unrelated changes | pass | Reviewed changes align with the active review-recording initiative. |
| Validation evidence | concern | Validation ran, but it did not catch the timing-strength regression. |

## Recommended next stage

Enter review-resolution and fix `CR1-F1` before `verify`.
