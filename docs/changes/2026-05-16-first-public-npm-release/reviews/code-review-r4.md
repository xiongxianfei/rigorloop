# Code Review R4 - M3 Release Verification And Evidence

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: M3 release verification and v0.1.4 release evidence implementation
Reviewed artifact: scripts/adapter_distribution.py; scripts/release-verify.sh; scripts/test-adapter-distribution.py; docs/releases/v0.1.4/release.yaml; docs/releases/v0.1.4/release-notes.md; docs/releases/v0.1.4/npm-publication.md; docs/reports/adapter-artifacts/releases/v0.1.4.yaml; packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json; packages/rigorloop/dist/metadata/releases.json; dist/adapters/manifest.yaml; docs/plans/2026-05-16-rigorloop-npm-publication.md; docs/changes/2026-05-16-first-public-npm-release/change.yaml
Review date: 2026-05-16
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Reviewed milestone: M3. Release Verification And v0.1.4 Release Evidence
- Milestone closeout: closed
- Remaining implementation milestones: M4, M5
- Required review-resolution: none
- Next stage: implement M4

## Review inputs

- Diff/review surface: current workspace diff for M3 release target support, release verification script updates, release validation helpers/tests, v0.1.4 release artifacts, bundled adapter metadata, and active plan handoff.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Test-spec focus: TNP-005, TNP-008, TNP-013, TNP-014, TNP-016, TNP-017, and TNP-020.
- Validation evidence: M3 validation notes in the active plan and `docs/changes/2026-05-16-first-public-npm-release/change.yaml`.

## Diff summary

M3 adds `v0.1.4` as a supported release target, extends `release-verify.sh v0.1.4` to run npm package publication validation and build/validate the v0.1.4 adapter release output, and adds release validation for npm publication evidence. The release artifacts under `docs/releases/v0.1.4/` now include release metadata, npm-oriented release notes, and `npm-publication.md` in `pending-publication` state. The v0.1.4 adapter artifact report and bundled package metadata now point the CLI at the v0.1.4 Codex archive metadata and checksums.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R70-R80 require v0.1.4 release metadata, release notes, and publication evidence. The implementation creates those artifacts and keeps `npm-publication.md` pending with `npm.published: false` and `fu_010_closeout_blocked: true`. |
| Test coverage | pass | `test_release_verify_script_supports_v0_1_4_npm_publication_gate`, `test_v0_1_4_release_validation_accepts_pending_publication_evidence`, and `test_v0_1_4_release_validation_requires_publication_evidence_and_closeout_blocker` directly cover the M3 release gate and pending-evidence behavior. |
| Edge cases | pass | The pending publication path is explicitly tested for missing evidence and for an invalid `fu_010_closeout_blocked: false` value. The real install smoke remains pending by design under R69m/TNP-017. |
| Error handling | pass | `validate_release_output` reports missing or invalid publication evidence and marks `npm_publication_evidence` as failed when evidence or v0.1.4 release metadata is incomplete. |
| Architecture boundaries | pass | npm remains CLI delivery only. Release notes state adapter archives remain GitHub release artifacts and are not bundled in npm; package metadata uses bundled adapter metadata for v0.1.4. |
| Compatibility | pass | Existing v0.1.3 untracked-adapter behavior is preserved and v0.1.4 follows the same release-output validation model while adding npm publication evidence checks. |
| Security/privacy | pass | Release validation still runs security path scanning and M3 does not add adapter ZIPs or generated adapter bodies to the npm package. |
| Derived artifact currency | pass | `dist/adapters/manifest.yaml`, `docs/reports/adapter-artifacts/releases/v0.1.4.yaml`, bundled metadata, and release validation are aligned around `v0.1.4`. |
| Unrelated changes | pass | The reviewed M3 diff is scoped to release verification, release evidence, adapter artifact metadata, and active lifecycle state. |
| Validation evidence | pass | Recorded validation includes targeted adapter distribution tests, `bash scripts/release-verify.sh v0.1.4`, package tests, npm package publication tests, selector tests, release/lifecycle validation, selected CI, and diff check. |

## No-finding rationale

The main M3 risk was closing release readiness too early by treating pending npm evidence as final publication proof. The implementation keeps that boundary explicit: pending publication evidence is accepted for repository-side readiness, but it records `npm.published: false`, `adapter_install_smoke.result: pending`, and `fu_010_closeout_blocked: true`. The release gate now knows about `v0.1.4` and validates package publication checks plus adapter release output, while the actual workflow publish gates and post-publication proof remain in M4 through M6b.

## Residual risks

- M4 still needs to implement release workflow publication-mode gates and duplicate-publish protection.
- M5 still needs documentation/follow-up state alignment for final local readiness.
- Public npm publication, post-publication `npm view`/`npx` smoke, and real non-dry-run Codex adapter install proof remain future M6b work and are not claimed by this M3 review.
