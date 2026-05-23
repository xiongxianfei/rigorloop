# Code Review M1 R2 - CRM-M1-CR1 Re-review

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `e0ca12b`
Status: clean-with-notes

## Review inputs

- Review surface: commit `e0ca12b` (`Resolve M1 registered evidence affected roots`).
- Reviewed milestone: M1. Evidence class registry and registered selector routing.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Prior finding under re-review: `CRM-M1-CR1`.
- Implementation files reviewed: `scripts/validation_selection.py` and `scripts/test-select-validation.py`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, and the M1 validation notes in the active plan.

## Diff summary

The resolution commit adds the governing change root from `_change_root(path)` to `affected_roots` in the `registered-change-evidence` selector branch. It also extends `test_registered_change_evidence_selects_declared_checks_and_governing_metadata` to assert that the registered evidence route includes the governing `docs/changes/<change-id>/` root. Lifecycle artifacts record the accepted finding resolution and return M1 to code-review rerun without claiming M2 or final readiness.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. CRM-R9 requires registered evidence to route to declared selector check IDs and affected roots; the registered evidence branch now adds the governing change root to `affected_roots`.
- Test coverage: pass. CRM-T004 requires selected check IDs, affected root, and governing `change.yaml`; the registered evidence test now asserts all three.
- Edge cases: pass. The fix is limited to paths already classified as `registered-change-evidence`; broad-pattern, ambiguity, and unregistered evidence behavior are not changed.
- Error handling: pass. The existing `len(matches) != 1` manual-routing diagnostic remains unchanged, and root attribution is only added after the evidence class resolves.
- Architecture boundaries: pass. The selector remains the owner of registered evidence routing and uses the existing repository-relative `_change_root()` helper.
- Compatibility: pass. Existing selected check IDs, registry patterns, selector categories, and lifecycle validation paths are unchanged.
- Security/privacy: pass. Affected root output remains repository-relative and contains no local filesystem, host, or user-specific path.
- Derived artifact currency: pass. No generated adapters or generated skill outputs are in scope for M1.
- Unrelated changes: pass. The code diff is scoped to affected-root output and its regression assertion; lifecycle edits only record the finding resolution and handoff.
- Validation evidence: pass. Recorded validation includes direct selector proof for `behavior-preservation.md`, selector regression, selected CI over implementation and lifecycle paths, metadata validation, lifecycle validation, review artifact structure validation, and whitespace.

## No-finding rationale

The R1 finding was specifically that registered evidence selected checks and governing `change.yaml` but omitted the governing change root from `affected_roots`. The resolution commit addresses that exact gap with the existing `_change_root()` helper and adds a direct assertion in the CRM-T004 test path. Direct selector evidence now shows `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/` in `affected_roots`, and selected CI reran the relevant selector and lifecycle checks.

## Handoff

Reviewed milestone: M1. Evidence class registry and registered selector routing
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M2
Remaining implementation milestones: M2, M3, M4, M5
Verify readiness: not-claimed
