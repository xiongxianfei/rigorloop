# Code Review M1 R1 - Change Evidence Registry Routing

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `8fe07bb`
Status: changes-requested

## Review inputs

- Review surface: commit `8fe07bb` (`M1: add change evidence registry routing`).
- Reviewed milestone: M1. Evidence class registry and registered selector routing.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Implementation files reviewed: `scripts/validation_selection.py`, `scripts/test-select-validation.py`, and `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md`.
- Validation evidence reviewed: M1 entries in `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml` and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.

## Diff summary

M1 adds a selector-owned `EvidenceClassRegistration` table, registry validation helper, registered evidence path classification, registered evidence routing through selector checks, selector regression coverage for registry shape/pattern behavior, and behavior-preservation evidence. The commit also contains the upstream proposal, spec, architecture, plan, test-spec, and formal review artifacts for this initiative.

## Findings

### CRM-M1-CR1: Registered evidence routing omits affected root output

Finding ID: CRM-M1-CR1
Severity: major
Location: `scripts/validation_selection.py:752`

Evidence: The approved spec requires registered evidence files to route to declared selector check IDs and affected roots (`CRM-R9`). The test spec's CRM-T004 expected registered evidence output to include "declared selected check IDs, affected root, and governing `change.yaml`." The implementation branch for `registered-change-evidence` adds selected check paths for the evidence file and governing `change.yaml`, but it never adds the governing change root to `affected_roots`. Direct selector proof confirms the gap: `python scripts/select-validation.py --mode explicit --path docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/behavior-preservation.md` returns `"affected_roots": []`. The test added for registered evidence asserts selected checks and paths but does not assert `affected_roots`, so the specified proof gap is not caught.

Required outcome: Registered evidence routing must populate the affected change root in selector output, and the registered-evidence test must assert that affected root so CRM-T004 directly proves the requirement.

Safe resolution path: In the `registered-change-evidence` selection branch, add the governing change root to `affected_roots` when present. Extend `test_registered_change_evidence_selects_declared_checks_and_governing_metadata` or an equivalent M1 test to assert `docs/changes/<change-id>/` appears in `payload["affected_roots"]`. Rerun M1 selector tests, explicit registered-evidence routing, selected CI for the implementation paths, lifecycle validation, change metadata validation, and whitespace checks.

## Checklist coverage

- Spec alignment: concern. Registry shape, bounded patterns, and lifecycle check routing align with M1, but CRM-R9 affected-root routing is incomplete.
- Test coverage: concern. Registry completeness, pattern routing, broad-pattern rejection, ambiguity rejection, and selector-regression selection are covered; affected-root output for registered evidence is not asserted.
- Edge cases: concern. Broad and ambiguous patterns have direct tests, but CRM-T004's affected-root edge is missing direct proof.
- Error handling: pass. Invalid registry entries, broad patterns, and ambiguous sample matches fail closed in tests.
- Architecture boundaries: pass. The registry remains selector-owned for the first slice, matching the ADR and CRM-R55.
- Compatibility: pass. Existing recurring evidence still selects `artifact_lifecycle.validate`; category names changed to `registered-change-evidence` as expected.
- Security/privacy: pass. The reviewed selector output and diagnostics use repository-relative paths.
- Derived artifact currency: pass. No generated artifacts are in scope for M1.
- Unrelated changes: pass. The implementation diff and lifecycle artifacts are tied to the approved change-record catalog initiative.
- Validation evidence: concern. The recorded commands are relevant and passed, but they did not catch the affected-root omission.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M1. Evidence class registry and registered selector routing
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `CRM-M1-CR1`
Remaining implementation milestones: M1 resolution, M2, M3, M4, M5
Verify readiness: not-claimed
