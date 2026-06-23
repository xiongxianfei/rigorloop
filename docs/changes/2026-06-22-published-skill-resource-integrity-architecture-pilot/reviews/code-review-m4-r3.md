# Code Review M4 R3

Review ID: code-review-m4-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: commit `866523a7`
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r3.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: implement M5
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r3.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M4. Generated Package and Archive Resource Parity
- Milestone closeout: closed
- Remaining implementation milestones: M5, M6, M7
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `866523a7` (`Resolve recorded-source archive validation`).
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 through M3 reviews, active plan M4 review-requested state, SRI-M4-CR2 review-resolution evidence, and M4 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R50-R51a; `specs/skill-contract.test.md` T45; active plan M4; SRI-M4-CR2 detailed review.
- Validation evidence: focused recorded-source profile bundle, full `python scripts/test-adapter-distribution.py`, selector-selected adapter regression command, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --` recorded in the active plan and change metadata.
- Implementation files reviewed: `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, active plan state, and change metadata.

## Diff summary

The SRI-M4-CR2 resolution replaces the recorded-source archive-validation empty-list shortcut with a structured archive-validation profile result.

Recorded-source release validation now inspects rebuilt archives for archive presence, archive structure, required recorded-source skill roots, and mapped-resource relative-path plus raw-byte SHA-256 parity when the recorded source declares a valid `Resource map`.

The release validator fails closed if archive validation returns no executed checks. Current-source archive validation remains routed through the existing current policy path.

The test suite adds recorded-source regressions for missing mapped resources, stale mapped-resource bytes with regenerated outer metadata, missing archives when no Resource map exists, malformed recorded Resource maps, and no-check archive-validation results.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R50-R50b require skill-root relative path plus raw-byte SHA-256 parity across release candidates; `validate_adapter_archives_for_profile(... RECORDED_SOURCE ...)` now compares recorded-source mapped resources against archive entries and hashes. |
| Test coverage | pass | `test_recorded_source_profile_rejects_missing_mapped_resource_in_archive`, `test_recorded_source_profile_rejects_stale_mapped_resource_even_with_current_metadata`, and the focused 10-test recorded-source bundle directly cover the CR2 regression surface. |
| Edge cases | pass | Tests cover no Resource map with real archive validation, malformed Resource map failure, missing archive failure, stale inner bytes despite regenerated adapter metadata, current-source policy enforcement, and no-check fail-closed behavior. |
| Error handling | pass | Missing archives, invalid/malformed recorded maps, missing resources, stale hashes, and no executed archive checks produce validation errors instead of vacuous pass results. |
| Architecture boundaries | pass | The change stays in adapter distribution/release validation and tests. It does not alter architecture resources, clean-install M5 scope, or current canonical skill lint policy. |
| Compatibility | pass | Recorded-source mode continues to skip current post-M3 canonical skill-content policy for historical source while preserving release metadata, adapter artifact metadata, and archive integrity checks. |
| Security/privacy | pass | No secret, credential, network, authentication, or privacy-sensitive behavior changed; release security evidence remains handled by the shared release-output validator. |
| Derived artifact currency | pass | No generated adapter output or historical archives were hand-edited. The reviewed changes validate temporary rebuilt archives from source. |
| Unrelated changes | pass | The diff is scoped to recorded-source archive validation, its regression tests, and lifecycle state/evidence updates for M4 CR2. |
| Validation evidence | pass | The change record lists the requested focused recorded-source tests, full adapter suite, selector-selected checks, lifecycle validation, metadata validation, review-artifact validation, and whitespace check as passing. |

## No-finding rationale

The finding in SRI-M4-CR2 was that recorded-source validation reported `adapter_archives: pass` without running archive inspection. The reviewed commit removes that empty-list path and routes both current and recorded source through a closed validation-profile helper.

For recorded source, the helper records executed archive checks, validates the archive structure enough to require target entrypoints and skill roots, checks every recorded-source skill `SKILL.md` under each adapter skill root, and compares mapped resource entries and raw-byte SHA-256 when a valid `Resource map` exists.

The named CR2 edge cases have direct tests: missing mapped resources, stale mapped-resource bytes after regenerating outer adapter metadata, no Resource map with missing archive, malformed Resource map, historical v0.1.5 compatibility, current-source policy enforcement, and fail-closed no-check behavior.

## Residual risk

M5 clean-installed target-tree parity, M6 repository-wide audit/enforcement, and M7 final evidence closeout remain open and are not claimed by this review.

## Handoff

Reviewed milestone: M4. Generated Package and Archive Resource Parity
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Remaining implementation milestones: M5, M6, M7
Next stage: implement M5
Final closeout readiness: not ready; later implementation milestones remain.

Do not claim final closeout, verify readiness, branch readiness, or PR readiness from this review.
