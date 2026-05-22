# Code Review M2 R2 - CRM-M2-CR1 Re-review

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `4ea2570`
Status: clean-with-notes

## Review inputs

- Review surface: commit `4ea2570` (`Resolve M2 evidence deferral contract`).
- Reviewed milestone: M2. Registration debt and actual changed-path proof.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Prior finding under re-review: `CRM-M2-CR1`.
- Implementation files reviewed: `scripts/validation_selection.py` and `scripts/test-select-validation.py`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/selector-routing-proof.md`, and the M2 validation notes in the active plan.

## Diff summary

The resolution commit adds a selector-owned owner-approved deferral model for deterministic unregistered change-local evidence. Selector output now keeps unregistered evidence visible as `manual-routing-required` and `debt: evidence-registration`; unresolved or incomplete deferrals remain blocking, while complete deferrals move to review-visible `registration_debt` with `verify_readiness: owner-deferred`. The selector tests now cover no deferral, complete deferral, incomplete deferral, and mismatched-path deferral cases.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. CRM-R17 through CRM-R19 require registration debt to resolve before verify unless CRM-R18's owner-approved deferral shape is satisfied; the implementation now distinguishes no, incomplete, invalid, and complete deferral states.
- Test coverage: pass. CRM-T009 has direct selector tests for unresolved debt, complete deferral unblocking, incomplete deferral blocking, and mismatched-path deferral blocking.
- Edge cases: pass. Complete deferrals do not convert unregistered evidence into registered routing, and mismatched paths do not unblock the reviewed evidence path.
- Error handling: pass. Missing fields are reported through `missing_deferral_fields`; invalid or duplicate matching deferrals remain blocking rather than silently routing.
- Architecture boundaries: pass. The selector owns the routing/debt diagnostic and reads only the governing change-local metadata needed for the deferral decision.
- Compatibility: pass. Registered evidence classes, selector categories, selected check IDs, registry patterns, query-helper behavior, and stage-skill guidance are unchanged.
- Security/privacy: pass. Deferral `path` and `follow_up` values are validated as repository-relative values; selector output remains repository-relative.
- Derived artifact currency: pass. No generated adapters or generated skill outputs are in scope for M2.
- Unrelated changes: pass. The code diff is scoped to the accepted deferral contract and its tests; lifecycle edits record only the finding resolution and handoff.
- Validation evidence: pass. Recorded validation includes selector regression, direct unregistered-evidence proof, local changed-path proof from the implementation state, selected CI, metadata validation, lifecycle validation, review-artifact structure validation, and whitespace.

## No-finding rationale

The R1 finding was that M2 emitted registration debt but had no implemented or tested owner-approved deferral path. The resolution commit adds the required five-field deferral shape, keeps unresolved or incomplete deferrals blocking, and proves that complete deferrals remain visible as registration debt while unblocking verify readiness through explicit owner deferral. Review reran `python scripts/test-select-validation.py` and the direct unregistered-evidence selector proof; the current clean worktree makes `--mode local` report no changed paths during re-review, so the implementation's recorded pre-commit local changed-path proof remains the actual M2 changed-set evidence.

## Handoff

Reviewed milestone: M2. Registration debt and actual changed-path proof
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M3
Remaining implementation milestones: M3, M4, M5
Verify readiness: not-claimed
