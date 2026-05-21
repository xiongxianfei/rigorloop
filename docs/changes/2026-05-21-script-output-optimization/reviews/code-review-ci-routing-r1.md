# Code Review CI Routing R1

Review ID: code-review-ci-routing-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: selector-routing maintenance fix at commit `8def5ae`
Status: clean-with-notes

## Review inputs

- Review surface: commit `8def5ae` (`Route script output evidence artifacts`).
- Governing artifacts: `specs/script-output-optimization.md` R32 and AC14, `specs/script-output-optimization.test.md` TSRO-014, active plan handoff state, and the final verify blocker that showed PR-mode CI blocked on change-local evidence files.
- Reviewed files: `scripts/validation_selection.py` and `scripts/test-select-validation.py`.
- Validation evidence: `python scripts/test-select-validation.py`, `bash scripts/ci.sh --mode pr --base $(git merge-base HEAD main) --head HEAD --jobs 1`, lifecycle validation, review-artifact closeout validation, change metadata validation, and `git diff --check --`.

## Diff summary

The patch adds four script-output evidence filenames to the existing `change-local-lifecycle` selector allowlist:

- `output-contract-red-test.md`
- `script-output-audit.md`
- `selected-tests-baseline.txt`
- `selected-tests-m3.txt`

It also extends the selector regression fixture in `scripts/test-select-validation.py` to prove those filenames classify as `change-local-lifecycle` and select `artifact_lifecycle.validate`.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. AC14 normally excludes selector changes, but the post-verify CI blocker required a narrow routing maintenance fix so lifecycle evidence created by this approved change can run through PR-mode CI. The patch does not alter output formatting, selected validation checks, failure detection, or wrapper execution semantics.
- Test coverage: pass. `scripts/test-select-validation.py` now includes exact fixture paths for all four filenames and expects `artifact_lifecycle.validate`.
- Edge cases: pass. The previously blocked PR-mode path for all branch changes now reports selector status `ok`; no manual-routing blocker remains for the four evidence files.
- Error handling: pass. Unsupported change-local paths still fall through to `change-local-unsupported`; only the four approved evidence filenames are added.
- Architecture boundaries: pass. The change is limited to repository-owned validation routing and its regression test. It does not touch `scripts/ci.sh`, generated adapters, public skill files, workflow specs, or lifecycle validator behavior.
- Compatibility: pass. Existing change-local lifecycle filenames remain unchanged; the patch only expands deterministic routing for evidence files already validated manually in earlier milestones.
- Security/privacy: pass. The diff adds static filenames and no logging of secrets, environment values, or private paths.
- Derived artifact currency: pass. No generated artifacts changed.
- Unrelated changes: pass. The diff is scoped to selector classification and selector regression coverage.
- Validation evidence: pass. PR-mode selected CI passed after the patch and included `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`.

## No-finding rationale

The original verify blocker was deterministic: PR-mode CI classified four required evidence files as `change-local-unsupported`. The implementation fixes exactly that classifier gap and proves the four filenames through the existing selector regression fixture. The passing PR-mode CI run demonstrates that the supported branch diff now reaches the intended checks instead of blocking before validation.

## Residual risks

This review closes only the selector-routing maintenance patch. Because the patch happened after `explain-change`, the durable rationale and active handoff state still need to be refreshed before final verify can claim branch readiness.

## Handoff

Reviewed milestone: CI routing maintenance after final verify blocker
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: explain-change refresh, then verify
Remaining implementation milestones: none
Verify readiness: not-claimed
