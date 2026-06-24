# Code Review M3 R2 - Review Evidence and Change Metadata Consistency

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `ab2af875`
Status: changes-requested

## Review inputs

- Review surface: commit `ab2af875` (`Resolve WSS-CR2 review closure predicate`).
- Reviewed milestone: M3. Review Evidence and Change Metadata Consistency.
- Governing artifacts: `specs/single-source-of-workflow-state.md`, `specs/single-source-of-workflow-state.test.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`.
- Implementation files reviewed: `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py`, `scripts/test-change-metadata-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, `specs/single-source-of-workflow-state.md`, and `specs/single-source-of-workflow-state.test.md`.
- Review-resolution evidence reviewed: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/review-resolution.md`.
- Validation evidence reviewed: current runs of `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/validate-review-artifacts.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/`, `python scripts/validate-change-metadata.py docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`, and explicit-path artifact lifecycle validation.

## Diff summary

The WSS-CR2 resolution introduces `finding_closure_state()` in `scripts/review_artifact_validation.py`, routes `summarize_review_evidence()` through that predicate, and refactors closeout-mode review artifact validation to call the same closure helper. The tests add missing-validation, missing-action, reopen, lifecycle-blocking, and parity fixtures. The spec and test spec add the shared-derived-predicate invariant required by WSS-CR2.

## Findings

### WSS-CR3 - Invalid or missing disposition is counted closed by the shared closure predicate

Finding ID: WSS-CR3
Severity: major
Location: `scripts/review_artifact_validation.py:1379`

Evidence: `_parse_resolution_entries()` records a structural finding when a resolution entry has no `Disposition` or an unsupported disposition, but it still appends a `ResolutionRecord` with `disposition=None` or the unsupported value. `_finding_closure_findings()` then accepts the single matching entry and delegates to `_validate_resolution_entry_closeout()`. That function immediately returns no closure findings for `entry.disposition is None or entry.disposition not in APPROVED_DISPOSITIONS`, so `finding_closure_state()` reports the finding as `closed`.

This violates R65 and R65a because an unparseable or non-final disposition is not a final disposition and must fail closed anywhere the derived open/closed predicate is consumed. The gap also leaves `summarize_review_evidence()` able to compute `open_count == 0` for a material finding whose only resolution entry has no supported disposition, which means `change.yaml` count validation and lifecycle owner-state blocking can inherit a false closed verdict.

Required outcome: The shared closure predicate must treat missing, unsupported, or otherwise unparseable disposition state as open. Summary, closeout-mode review validation, change metadata counts, and lifecycle owner-state blocking must all observe the same open verdict.

Safe resolution path: Add a closure-predicate branch that emits a closure finding for `entry.disposition is None` or unsupported dispositions instead of returning an empty finding list. Add regression coverage proving `summarize_review_evidence()` reports the finding open and that change metadata and lifecycle validation block when the resolution entry has a missing or unsupported disposition.

## Checklist coverage

- Spec alignment: block. R65 requires a material finding to stay open until final disposition and validation evidence are all present; R65a requires shared derived predicates to fail consistently.
- Test coverage: concern. The new missing-validation, missing-action, reopen, and parity fixtures are useful, but no fixture exercises a missing or unsupported disposition through `summarize_review_evidence()`.
- Edge cases: block. The parser-critical unparseable-disposition path is a named WSS-CR2 requirement and currently yields a false closed summary.
- Error handling: block. The implementation already detects invalid disposition structurally, but the shared closure predicate does not fail closed on that invalid parsed state.
- Architecture boundaries: pass. The closure predicate is centralized in `review_artifact_validation.py` and consumed by summary and closeout validation rather than duplicated elsewhere.
- Compatibility: pass. The intended fix can be local to the predicate and tests without changing artifact ownership or workflow stage order.
- Security/privacy: pass. The diff handles repository-local Markdown validation only and adds no sensitive logging or external calls.
- Derived artifact currency: block. Derived review counts in `change.yaml` can remain synchronized to a false closed summary when the resolution disposition is invalid.
- Unrelated changes: pass. The implementation diff is scoped to review artifact validation, related tests, spec/test-spec text, and lifecycle evidence.
- Validation evidence: concern. The cited commands pass, but they do not cover the invalid-disposition closure path.

## No-finding rationale

Not applicable. This review has one material finding.

## Residual risks

The same false-closed shape may exist for other parse errors that are represented as structural validation findings but not reflected in `finding_closure_state()`. The WSS-CR3 resolution should audit the predicate for other parse-invalid states that still produce a `ResolutionRecord`.

## Handoff

Reviewed milestone: M3. Review Evidence and Change Metadata Consistency
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution
Remaining implementation milestones: M3, M4, M5
Finding IDs: WSS-CR3
Verify readiness: not-claimed
