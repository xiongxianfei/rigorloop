# Code Review R3 - M2 CR2-F1 Rerun

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: M2 package-content validation CR2-F1 fix
Reviewed artifact: scripts/npm_package_validation.py; scripts/test-npm-package-publication.py; docs/plans/2026-05-16-rigorloop-npm-publication.md; docs/changes/2026-05-16-first-public-npm-release/review-resolution.md; docs/changes/2026-05-16-first-public-npm-release/change.yaml
Review date: 2026-05-16
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Reviewed milestone: M2. Package-Content Validation And Packed-Package Smoke
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4, M5
- Required review-resolution: none
- Next stage: implement M3

## Review inputs

- Diff/review surface: current workspace diff for the CR2-F1 validator fix, validator tests, active plan handoff, review-resolution, and change metadata.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Prior finding: `CR2-F1` from `reviews/code-review-r2.md`.
- Validation evidence: M2 validation notes in the active plan and `docs/changes/2026-05-16-first-public-npm-release/change.yaml`.

## Diff summary

The CR2-F1 fix replaces fragile recursive `fnmatch`-based forbidden-path detection with explicit normalized package-relative checks in `scripts/npm_package_validation.py`. The tests now directly cover root-level and nested `.zip`, `.tgz`, `.env`, `.pem`, and `.key` paths, generated adapter bodies under `dist/adapters/**`, local state under `.codex` and `.agents`, and allowed runtime files. The plan and change metadata hand M2 back to code-review after the fix.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R17-R27 and TNP-003/TNP-021 require deterministic tarball allowlist/forbidden-path checks. `is_forbidden_path` now rejects forbidden content by package-relative meaning rather than glob shape. |
| Test coverage | pass | `test_forbidden_path_detection_rejects_root_and_nested_sensitive_files` and `test_inspector_rejects_forbidden_paths` prove root-level and nested forbidden archive and secret-like paths fail. |
| Edge cases | pass | The reviewed failure classes from CR2-F1 are directly covered: root `.zip`, `.tgz`, `.env`, `.pem`, `.key`, plus nested variants. |
| Error handling | pass | `inspect_package_tarball` raises `NpmPackageValidationError` when a forbidden path is present, blocking publication validation. |
| Architecture boundaries | pass | npm remains a CLI delivery artifact; adapter archives and generated adapter bodies remain outside the package tarball. |
| Compatibility | pass | The selector continues to route package changes to existing CLI tests and the new npm package publication tests. |
| Security/privacy | pass | The fix blocks root and nested archive/secret-like leakage before publication. |
| Derived artifact currency | pass | No generated public adapter skill bodies were edited or bundled. |
| Unrelated changes | pass | The CR2-F1 fix is scoped to package validation, tests, and lifecycle evidence. |
| Validation evidence | pass | Recorded validation includes `python scripts/test-npm-package-publication.py`, selector regression, package tests, selected CI, review artifact validation, metadata validation, lifecycle validation, and diff check after the fix. |

## No-finding rationale

The previous blocker was that `package/**/*.zip`-style patterns missed root-level forbidden paths. The implementation now normalizes tarball paths and rejects forbidden classes by suffix and package-relative prefixes. The regression tests prove both the helper and the tarball inspector reject root-level and nested forbidden files, so CR2-F1 is closed.

## Residual risks

- M3 through M5 still need implementation and review before repository-side publication readiness.
- Public npm publication, post-publication `npx` smoke, and real non-dry-run Codex adapter install proof remain future lifecycle work and are not claimed by this M2 review.
