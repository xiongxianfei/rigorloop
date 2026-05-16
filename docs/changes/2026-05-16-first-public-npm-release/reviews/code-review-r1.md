# Code Review R1 - M1 Package Metadata

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1 package metadata implementation
Reviewed artifact: packages/rigorloop package metadata and bundled adapter metadata changes
Review date: 2026-05-16
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Reviewed milestone: M1. Package Metadata And Runtime Tarball Contract
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: none
- Next stage: implement M2

## Review inputs

- Diff/review surface: current workspace diff for `packages/rigorloop/package.json`, `packages/rigorloop/README.md`, `packages/rigorloop/LICENSE`, `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/metadata/releases.json`, `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.4.json`, deletion of `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json`, `packages/rigorloop/test/cli.test.js`, active plan updates, and change metadata updates.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Validation evidence: M1 validation notes in the active plan and `docs/changes/2026-05-16-first-public-npm-release/change.yaml`.

## Diff summary

M1 changes the package identity from candidate `0.1.3` with `private: true` to publishable `@xiongxianfei/rigorloop@0.1.4`, adds package-local `LICENSE` to the `files` allowlist, updates README wording away from candidate-only publication blocking, aligns bundled release metadata to `v0.1.4`, removes the package-local `v0.1.3` bundled metadata file, and updates package tests and fixtures to assert the `v0.1.4` package-to-adapter mapping.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `packages/rigorloop/package.json` now names `@xiongxianfei/rigorloop` at `0.1.4`, has no `private: true`, exposes only the `rigorloop` binary, and uses a `files` allowlist including `dist/`, `package.json`, `README.md`, and `LICENSE`, matching R1-R2, R8, R10-R18, and AC1-AC3. |
| Test coverage | pass | `packages/rigorloop/test/cli.test.js` adds direct package policy assertions for TNP-001, TNP-002, TNP-004, and bundled metadata assertions for TNP-005. Existing CLI tests were updated to the `0.1.4` package identity and passed in full package validation. |
| Edge cases | pass | The direct tests cover absence of `private`, forbidden lifecycle scripts, runtime dependencies, extra binaries, adapter archive names, official GitHub archive URL shape, and release-index metadata hash alignment for `v0.1.4`. |
| Error handling | pass | The only runtime code change makes the missing bundled metadata error message use the computed package-compatible release instead of a hard-coded `v0.1.3`; no error class or exit-code behavior changed. |
| Architecture boundaries | pass | npm remains the CLI delivery channel only. Adapter archives are still external GitHub release artifacts selected by bundled metadata; no adapter ZIPs or generated adapter skill bodies were added to package contents in M1. |
| Compatibility | pass | Package version, manifest output, lockfile fixtures, official archive URL tests, and package fixture helpers were updated consistently to `0.1.4`. Historical `v0.1.3` release evidence outside `packages/rigorloop` was not rewritten. |
| Security/privacy | pass | The package policy test asserts no install lifecycle scripts and no runtime dependencies. The README preserves the adapter archive trust boundary and no secrets, credentials, local paths, or token material were added. |
| Derived artifact currency | pass | No generated public adapter skill bodies were edited. Bundled metadata hash in `releases.json` matches the new `adapter-artifacts-v0.1.4.json` bytes by direct test. |
| Unrelated changes | pass | The reviewed M1 diff is scoped to package metadata/runtime metadata, package tests, and lifecycle evidence. Other existing initiative artifacts are upstream proposal/spec/architecture/plan surfaces for the active npm publication change. |
| Validation evidence | pass | Recorded evidence includes expected proof-first targeted test failure and pass, `npm test --prefix packages/rigorloop`, change metadata validation, artifact lifecycle validation, selected CI with `rigorloop_cli.test`, and `git diff --check`. |

## No-finding rationale

The M1 implementation satisfies the approved milestone's package-level contract without entering M2 tarball inspection, M3 release verification, M4 publish workflow, or M5 publication evidence scope. The tests directly prove the package identity, one-binary surface, publish blocker removal, package-local license requirement, lifecycle-script/dependency policy, and `v0.1.4` bundled metadata mapping. Remaining publication proof requirements are explicitly deferred in the active plan and are not claimed by M1.

## Residual risks

- M2 must still inspect the actual packed tarball and prove forbidden files are absent from the package artifact.
- M3/M5 must still generate and verify real `v0.1.4` release assets and actual non-dry-run Codex install proof before FU-010 can close.
