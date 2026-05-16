# Code Review R2 - M2 Package Content And Packed Smoke

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2 package-content validation and packed-package smoke implementation
Reviewed artifact: scripts/npm_package_validation.py; scripts/validate-npm-package.py; scripts/test-npm-package-publication.py; scripts/validation_selection.py; scripts/test-select-validation.py; docs/plans/2026-05-16-rigorloop-npm-publication.md; docs/changes/2026-05-16-first-public-npm-release/change.yaml
Review date: 2026-05-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR2-F1
- Blocking findings: CR2-F1
- Reviewed milestone: M2. Package-Content Validation And Packed-Package Smoke
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: required
- Next stage: review-resolution for CR2-F1, then implement M2 fix

## Review inputs

- Diff/review surface: current workspace diff for M2 package-content validator, validator tests, selector routing, active plan, and change metadata.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Validation evidence: M2 validation notes in the active plan and `docs/changes/2026-05-16-first-public-npm-release/change.yaml`.

## Diff summary

M2 adds `scripts/npm_package_validation.py` and `scripts/validate-npm-package.py` for package policy and tarball content validation; adds `scripts/test-npm-package-publication.py` for actual `npm pack`, tarball inspection, and installed-binary smoke; and updates validation selection so package changes select both `rigorloop_cli.test` and `npm_package_publication.test`.

## Findings

### CR2-F1 - Root-level forbidden archive and secret-like files are not rejected

Finding ID: CR2-F1
Severity: blocker
Location: `scripts/npm_package_validation.py`
Evidence: `FORBIDDEN_PATH_PATTERNS` includes patterns such as `package/**/*.zip`, `package/**/*.tgz`, `package/**/*.pem`, `package/**/*.key`, and `package/**/*.env`, and `is_forbidden_path` evaluates them with `fnmatch.fnmatchcase`. Python `fnmatch` does not treat `**` as matching zero or more directories. Direct review check showed:

  ```text
  package/evil.zip -> False
  package/.env -> False
  package/secret.key -> False
  package/nested/evil.zip -> True
  ```

  The current negative tarball test only injects `package/dist/adapters/codex/skills/proposal/SKILL.md`, so it does not prove root-level forbidden archive, env, key, or pem files are rejected.
Required outcome: Package-content validation must reject forbidden tarball paths at package root and nested paths, including adapter/archive/secrets patterns required by R22-R26 and TNP-003/TNP-021.
Safe resolution path: Add direct tests for root-level and nested forbidden paths such as `package/rigorloop-adapter-codex-v0.1.4.zip`, `package/archive.tgz`, `package/.env`, `package/secret.pem`, and `package/secret.key`. Update `is_forbidden_path` to implement the spec's intended recursive semantics explicitly, for example by checking exact forbidden prefixes and suffixes in addition to path-glob patterns, or by adding root-level patterns like `package/*.zip`, `package/*.tgz`, `package/*.pem`, `package/*.key`, and `package/*.env`.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R22-R26 require package-content validation to fail before publication if any forbidden tarball path is present. CR2-F1 shows root-level forbidden files can pass. |
| Test coverage | block | `scripts/test-npm-package-publication.py` tests one `dist/adapters/**` forbidden path but lacks direct proof for root-level archive and secret-like forbidden paths named by the spec. |
| Edge cases | block | Root-level `.zip`, `.tgz`, `.pem`, `.key`, and `.env` paths are named forbidden classes but are not covered by the current matching behavior. |
| Error handling | pass | When paths are detected as forbidden, `inspect_package_tarball` raises `NpmPackageValidationError` before publication. The issue is incomplete detection. |
| Architecture boundaries | pass | The design keeps npm as CLI delivery and does not bundle adapter archives in the actual current tarball. |
| Compatibility | pass | Selector routing adds the new package publication check alongside existing package tests without removing existing checks. |
| Security/privacy | block | Root-level `.env`, key, pem, archive, and nested tarball files are a public package leakage risk if accidentally included. |
| Derived artifact currency | pass | No generated public adapter skill bodies were edited. |
| Unrelated changes | pass | M2 diff is scoped to package validation, selector routing, and lifecycle evidence. |
| Validation evidence | concern | Recorded validation proves the current package tarball and one forbidden path fixture, but not the full named forbidden path set required for clean M2 review. |

## No-finding rationale

Not applicable; material finding CR2-F1 requires a fix before M2 can close.

## Residual risks

- After CR2-F1 is fixed, rerun `python scripts/test-npm-package-publication.py`, selector regression, selected CI, and diff check before returning M2 to code-review.
