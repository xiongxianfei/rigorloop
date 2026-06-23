# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `697701a`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r1.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M4-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M4. Generated Package and Archive Resource Parity
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4 resolution, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M4-CR1
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `697701a` (`M4: validate generated resource parity`).
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 through M3 reviews, active plan M4 review-requested state, and M4 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R50-R51a; `specs/skill-contract.test.md` T45; active plan M4.
- Validation evidence: M4 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml` and active plan validation notes.
- Implementation files reviewed: `scripts/skill_validation.py`, `scripts/build-skills.py`, `scripts/adapter_distribution.py`, `scripts/validate-release-ci.py`, `scripts/test-build-skills.py`, `scripts/test-adapter-distribution.py`, active plan state, and change metadata.

## Diff summary

M4 adds mapped-resource identity collection as skill-root relative path plus raw-byte SHA-256, validates generated local mirrors, generated adapter output, and release archives for missing or stale mapped resources, and adds stale and missing resource regressions for those surfaces. It also changes the recorded-source release CI wrapper so historical release checks rebuild archives from the recorded source and call only tracked adapter artifact metadata validation on the rebuilt output.

## Findings

## Finding SRI-M4-CR1

Finding ID: SRI-M4-CR1
Severity: major
Location: `scripts/validate-release-ci.py:79`
Evidence: `validate_from_recorded_source()` now materializes the recorded source, builds adapter archives, and validates only `validate_adapter_artifact_metadata(...)`. Before this change, the recorded-source path called `validate_release_output(...)`, which validates the release metadata and notes surface in addition to adapter artifact metadata. The M4 change avoids retroactively applying current canonical skill lint to historical source, but it also drops release metadata, release-notes, required validation-key status, security-scanning, token-cost, npm-publication, and related release-surface checks for the recorded-source CI path.

This weakens release CI beyond the M4 parity scope. M4 may need a recorded-source compatibility mode because current post-M3 skill lint should not be applied to historical v0.1.5 source, but that mode must not reduce recorded-source release validation to checksum metadata only.

Required outcome: Preserve recorded-source compatibility without dropping release metadata and release-surface validation. The recorded-source path must skip only the current canonical skill or archive-content checks that are invalid for historical sources, while retaining release metadata, release notes, required validation evidence, security, npm-publication, and adapter artifact metadata checks that are still applicable to the recorded release.

Safe resolution path: Add an explicit recorded-source release-validation mode, or split release metadata validation from current canonical archive-content validation, so `scripts/validate-release-ci.py` can validate historical release metadata and locally rebuilt recorded-source artifacts without applying current post-M3 skill lint to historical source. Add a regression proving a release metadata error still fails in recorded-source mode, and keep the historical v0.1.5 recorded-source compatibility case green. Rerun `python scripts/test-adapter-distribution.py`, the selected release-CI validation tests, `python scripts/select-validation.py --mode explicit --path scripts/validate-release-ci.py --path scripts/adapter_distribution.py --path scripts/test-adapter-distribution.py`, M4 lifecycle validation, review artifact validation, change metadata validation, and `git diff --check --`.

needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. The generated and archive mapped-resource parity work aligns with R50-R51a, but the recorded-source release-CI behavior change drops unrelated release-surface validation that remains part of the release contract.
- Test coverage: concern. M4 has useful stale and missing mapped-resource tests, but no regression proves recorded-source release CI still rejects invalid release metadata after narrowing the historical-source path.
- Edge cases: concern. Historical source compatibility is a real edge case, but the implementation handles it by bypassing more validation than necessary.
- Error handling: concern. Invalid or incomplete release metadata can now avoid recorded-source CI failure because only adapter artifact metadata is checked on the rebuilt output.
- Architecture boundaries: pass. The parity helpers live in existing skill validation, build, adapter generation, and release validation surfaces.
- Compatibility: concern. The release-CI wrapper is a contributor and release workflow surface; narrowing it to artifact metadata changes release validation expectations for recorded-source checks.
- Security/privacy: concern. Release security-scanning validation previously performed through `validate_release_output(...)` is no longer reached by the recorded-source path.
- Derived artifact currency: pass. Generated local mirror, adapter output, and release archive resource parity are now checked with path and raw-byte SHA-256 diagnostics.
- Unrelated changes: concern. The recorded-source compatibility fix is related to making M4 validation pass, but the current implementation changes broader release-CI semantics beyond the mapped-resource parity contract.
- Validation evidence: concern. The named M4 commands are relevant for mapped-resource parity, but they do not prove retained release metadata validation for recorded-source CI.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M4. Generated Package and Archive Resource Parity
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Remaining implementation milestones: M4 resolution, M5, M6, M7
Next stage: review-resolution for SRI-M4-CR1
Final closeout readiness: not ready; M4 remains open and later implementation milestones remain.
