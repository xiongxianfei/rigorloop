# Code Review M4 R2

Review ID: code-review-m4-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `f3634b11`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r2.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M4-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r2.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M4. Generated Package and Archive Resource Parity
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M4-CR2
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `f3634b11` (`Resolve M4 release validation profile`).
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 through M3 reviews, SRI-M4-CR1 review-resolution evidence, active plan M4 review-requested rerun state, and M4 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R50-R51a; `specs/skill-contract.test.md` T45; active plan M4; SRI-M4-CR1 review-resolution entry.
- Validation evidence: SRI-M4-CR1 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml` and active plan validation notes.
- Implementation files reviewed: `scripts/adapter_distribution.py`, `scripts/validate-release-ci.py`, `scripts/test-adapter-distribution.py`, active plan state, review log, review resolution, and change metadata.

## Diff summary

The SRI-M4-CR1 resolution adds a closed `ReleaseValidationProfile` enum, routes recorded-source release CI through `validate_release_output(..., profile=ReleaseValidationProfile.RECORDED_SOURCE)`, and keeps release metadata, notes, security, npm-publication, and adapter artifact metadata checks active for recorded-source validation. Tests now prove the real `v0.1.5` recorded-source route stays green, invalid release metadata fails in recorded-source mode, current-source content policy still fails for malformed current skill content, and invalid profile values fail closed.

## Findings

## Finding SRI-M4-CR2

Finding ID: SRI-M4-CR2
Severity: major
Location: `scripts/adapter_distribution.py:3505`
Evidence: `validate_release_output()` now skips `validate_adapter_archives(...)` whenever `profile` is `ReleaseValidationProfile.RECORDED_SOURCE`, setting `adapter_archive_errors` to `[]`. Later, `actual_validation["adapter_archives"]` is derived from that empty list, so a recorded-source release can satisfy `validation.adapter_archives: pass` without any release-archive content or mapped-resource parity validation running. Adapter artifact metadata still checks archive presence and full-archive SHA-256, but that is not the same as the M4/T45 resource parity check that proves mapped resources inside archives preserve skill-root relative path and raw-byte SHA-256.

SRI-M4-CR1 required historical compatibility to skip only current canonical skill/archive-content policy checks that cannot validly apply to historical source. It did not allow recorded-source mode to bypass applicable archive integrity checks. The requested CR1 acceptance criteria also explicitly kept adapter artifact metadata and mapped-resource parity active. The new tests cover release metadata preservation and current policy skipping, but none corrupts or removes a mapped resource inside a recorded-source rebuilt archive and proves recorded-source validation fails.

Required outcome: Recorded-source validation must retain archive-content integrity for the rebuilt recorded-source artifacts, including mapped-resource parity when the recorded source contains mapped resources, without applying incompatible current canonical skill lint to historical source.

Safe resolution path: Split archive validation into current-source policy checks and recorded-source archive parity checks, or add a `validate_recorded_source_adapter_archives(...)` helper that validates rebuilt archives against the recorded source without calling current canonical skill validation that is invalid for historical releases. Keep `ReleaseValidationProfile.RECORDED_SOURCE` from running current post-M3 resource lint against old skills, but do not set `adapter_archive_errors` to `[]` before inspecting the rebuilt archives. Add regressions showing a recorded-source profile fails for a stale or missing mapped resource inside a rebuilt archive when the recorded source has a valid resource map, while the historical `v0.1.5` compatibility case remains green. Rerun `python scripts/test-adapter-distribution.py`, selector-selected validation for `scripts/validate-release-ci.py`, `scripts/adapter_distribution.py`, and `scripts/test-adapter-distribution.py`, lifecycle validation, review artifact validation, change metadata validation, and `git diff --check --`.

needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. R50-R50b and T45 require release archive mapped-resource path and raw-byte SHA-256 parity; recorded-source mode currently skips the archive validator that owns that check.
- Test coverage: concern. The added tests prove release metadata and current policy boundaries, but there is no recorded-source stale or missing mapped-resource archive fixture.
- Edge cases: concern. A recorded-source archive with stale mapped-resource bytes can pass if its adapter artifact metadata is regenerated to match the stale archive.
- Error handling: pass. Invalid profile values fail closed, and recorded-source build/materialization failures still return nonzero.
- Architecture boundaries: pass. The profile split remains in the existing release validation surfaces.
- Compatibility: concern. Historical-source compatibility is improved, but the implementation overcorrects by treating `adapter_archives` as passing without archive inspection.
- Security/privacy: pass. Release security evidence remains active through the shared release validator.
- Derived artifact currency: concern. Current-source archive resource parity remains active, but recorded-source rebuilt archive content is not inspected for mapped-resource parity.
- Unrelated changes: pass. The diff is scoped to the SRI-M4-CR1 release-validation profile resolution and lifecycle bookkeeping.
- Validation evidence: concern. The recorded commands are relevant and pass, but they do not include direct proof that recorded-source archive mapped-resource parity remains active.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M4. Generated Package and Archive Resource Parity
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Remaining implementation milestones: M4 resolution, M5, M6, M7
Next stage: review-resolution for SRI-M4-CR2
Final closeout readiness: not ready; M4 remains open and later implementation milestones remain.
