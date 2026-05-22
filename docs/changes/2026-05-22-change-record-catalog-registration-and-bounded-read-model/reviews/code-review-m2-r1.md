# Code Review M2 R1 - Registration Debt and Actual Changed-Path Proof

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `99159c3`
Status: changes-requested

## Review inputs

- Review surface: commit `99159c3` (`M2: surface change evidence registration debt`).
- Reviewed milestone: M2. Registration debt and actual changed-path proof.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Implementation files reviewed: `scripts/validation_selection.py`, `scripts/test-select-validation.py`, and `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`.
- Validation evidence reviewed: M2 entries in `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml` and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.

## Diff summary

M2 adds `unregistered-change-evidence` classification for immediate child files under `docs/changes/<change-id>/` that do not match a registered evidence class or lifecycle artifact. Those paths now produce `manual-routing-required` with `debt: evidence-registration`, `verify_readiness: blocked`, and an owner-approved deferral next-action message. The milestone also registers `selector-routing-proof.md` as routing-coverage evidence, adds selector tests for unregistered evidence and actual local changed-path discovery, and records the local selector proof for this branch.

## Findings

### CRM-M2-CR1: Owner-approved deferral shape is not implemented or tested

Finding ID: CRM-M2-CR1
Severity: major
Location: `scripts/test-select-validation.py:953`; `scripts/validation_selection.py:813`; `specs/change-record-catalog-registration-and-bounded-read-model.test.md:207`

Evidence: The M2 spec scope includes CRM-R17 through CRM-R19. CRM-R18 says an owner-approved deferral for deterministic evidence must name owner, path, reason, validation impact, and follow-up location, and CRM-R19 says unresolved `manual-routing-required` blocks verify unless CRM-R18 is satisfied. The test spec also defines CRM-T009, expecting a complete owner-approved deferral to unblock readiness while incomplete deferrals fail. The implementation only embeds the required field names in the `next_action` string for blocked selector output and asserts that wording in `test_unregistered_change_evidence_produces_registration_debt`. There is no parser, evidence shape, or test fixture for a complete deferral, and no test proving an incomplete deferral fails while a complete one satisfies CRM-R18. As implemented, `verify_readiness` is always `blocked` for unregistered deterministic evidence, so the approved exception path cannot be exercised or reviewed.

Required outcome: M2 must include a review-visible owner-approved deferral shape, with tests proving complete deferrals can satisfy CRM-R18 and incomplete deferrals fail without making unregistered evidence silently route.

Safe resolution path: Add the smallest deferral mechanism consistent with the current architecture, preferably selector-local test fixtures or a change-local evidence/plan shape if no schema-owned storage exists yet. Extend selector tests for CRM-T009: complete deferral includes owner, path, reason, validation impact, and follow-up; incomplete deferrals remain blocking; unregistered evidence without deferral remains `manual-routing-required`. Rerun M2 selector tests, direct unregistered evidence proof, local changed-path proof, selected CI, lifecycle/metadata/review artifact validation, and whitespace checks.

## Checklist coverage

- Spec alignment: concern. CRM-R7, CRM-R8, CRM-R12 through CRM-R16 are covered, but CRM-R17 through CRM-R19 require an owner-approved deferral path that is not implemented.
- Test coverage: concern. CRM-T006, CRM-T007, and CRM-T008 have direct tests/proof; CRM-T009 is missing.
- Edge cases: concern. EC3, EC6, and EC8 are covered; EC7 complete owner-approved unsupported status is not.
- Error handling: pass for unresolved debt. Unregistered evidence fails closed and selected CI reports the blocking selector result.
- Architecture boundaries: pass. The selector remains the owner of routing diagnostics and does not introduce query helper or skill guidance behavior.
- Compatibility: pass. Existing registered evidence routes and selected check IDs remain unchanged.
- Security/privacy: pass. Diagnostics and proof use repository-relative paths only.
- Derived artifact currency: pass. No generated artifacts are in scope for M2.
- Unrelated changes: pass. The diff is scoped to selector routing, tests, proof evidence, and plan/change metadata.
- Validation evidence: concern. The recorded commands are relevant and passed, but they do not exercise the owner-approved deferral shape required by CRM-T009.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Registration debt and actual changed-path proof
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `CRM-M2-CR1`
Remaining implementation milestones: M2 resolution, M3, M4, M5
Verify readiness: not-claimed
