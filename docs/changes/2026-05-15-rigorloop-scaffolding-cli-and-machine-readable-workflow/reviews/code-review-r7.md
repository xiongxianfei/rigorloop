# Code Review R7

Review ID: code-review-r7
Stage: code-review
Round: 7
Reviewer: Codex code-review skill
Target: commit `6d100dc` (`Resolve M3 metadata trust findings`)
Reviewed artifact: packages/rigorloop; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `git show 6d100dc -- packages/rigorloop docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md`
- Tracked governing branch state: commit `6d100dc`
- Governing artifacts:
  - `specs/rigorloop-cli-package-and-codex-init.md` R49-R61c and AC4-AC11
  - `specs/rigorloop-cli-package-and-codex-init.test.md` T15-T19, T29-T44
  - `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md` M3 and Current Handoff Summary
  - `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- Validation evidence reviewed:
  - `npm test --prefix packages/rigorloop` passed after the `CR6-F1`/`CR6-F2` fix.
  - Temporary-project smoke for the real `v0.1.3` Codex archive with `init --adapter codex --from-archive` passed after the fix.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md` passed after the fix.
  - Direct review check: `curl -fsSL -o "$tmp/adapter-artifacts-v0.1.3.json" https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/adapter-artifacts-v0.1.3.json` returned HTTP 404.
  - Direct review check: GitHub release API for `v0.1.3` listed only `rigorloop-adapter-claude-v0.1.3.zip`, `rigorloop-adapter-codex-v0.1.3.zip`, and `rigorloop-adapter-opencode-v0.1.3.zip`.

## Diff Summary

The `CR6-F1`/`CR6-F2` fix removes production runtime metadata environment overrides, adds a bundled release trust index under `packages/rigorloop/dist/metadata/releases.json`, changes network metadata loading to fetch raw bytes and verify SHA-256 before parsing, keeps local archive verification on bundled package metadata, adds fixture-package tests for metadata trust behavior, and updates review-resolution and plan state for the accepted findings.

## Findings

### CR7-F1: Bundled network metadata URL points to a release asset that does not exist

Finding ID: CR7-F1
Severity: blocker
Location: packages/rigorloop/dist/metadata/releases.json:6; packages/rigorloop/dist/bin/rigorloop.js:915

Evidence: The M3 spec requires networked adapter installation to fetch release metadata from the official release source (`specs/rigorloop-cli-package-and-codex-init.md:255`) and AC4 says actual `rigorloop init --adapter codex` installs verified Codex adapter files from an approved release archive when metadata, checksum, size, path, and tree-hash checks pass (`specs/rigorloop-cli-package-and-codex-init.md:492`). The implementation now resolves network metadata through the bundled release index (`packages/rigorloop/dist/bin/rigorloop.js:915`) and that index points to `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/adapter-artifacts-v0.1.3.json` (`packages/rigorloop/dist/metadata/releases.json:6`). A direct review check on 2026-05-15 returned HTTP 404 for that URL, and the GitHub release API for `v0.1.3` listed only the three adapter ZIP assets, not an `adapter-artifacts-v0.1.3.json` metadata asset. The package tests exercise network mode with fixture `data:` metadata URLs, so they do not prove the tracked bundled release index can satisfy the real default command path.

Required outcome: The tracked bundled release index must reference an official metadata source that exists and whose raw bytes match the trusted `metadata_sha256`, or the approved spec/architecture must be revised so the first-slice default network install contract no longer depends on an unavailable release metadata asset.

Safe resolution path: Publish the official `adapter-artifacts-v0.1.3.json` metadata asset for the `v0.1.3` release and update `packages/rigorloop/dist/metadata/releases.json` if the URL or SHA-256 differs; then add or record direct proof that `rigorloop init --adapter codex` can fetch metadata from the tracked official URL, verify the metadata hash, download the official archive, and install successfully. If modifying the historical release asset is not acceptable, revise the spec/architecture to make first-slice default install use bundled metadata plus official archive URL, then update tests and the release index accordingly before closing M3.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR7-F1` violates the network metadata availability needed by R49 and AC4 for the default `init --adapter codex` path. |
| Test coverage | concern | Tests prove trust-boundary behavior with fixture package metadata, but no tracked test or validation proves the real bundled `v0.1.3` metadata URL exists. |
| Edge cases | concern | Metadata hash mismatch, missing trust root, and ignored env overrides are covered; the real official metadata source edge case is not. |
| Error handling | pass | Missing network metadata is reported as a blocked release-unavailable path rather than an internal error. |
| Architecture boundaries | concern | The trust-boundary design is now respected, but the trusted source it records is not currently available. |
| Compatibility | block | The public quick-start/default command would block on metadata download for `v0.1.3` unless the release asset is added or the contract changes. |
| Security/privacy | pass | The fix removes runtime env trust-root substitution and verifies network metadata bytes before parsing. |
| Derived artifact currency | concern | The bundled release index is tracked, but it is not synchronized with the actual release asset list. |
| Unrelated changes | pass | The diff is scoped to M3 metadata trust handling, tests, and lifecycle artifacts. |
| Validation evidence | concern | Package tests and selected CI passed, but the direct release URL check failed with HTTP 404. |

## Review Status

changes-requested

## Milestone-Aware Handoff

- Reviewed milestone: M3. Codex adapter metadata, archive verification, extraction, and tree hash
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR7-F1`
- Remaining in-scope implementation milestones: M3
- Next stage: review-resolution M3, then implement accepted fix or approved contract revision for M3
- Final closeout readiness: not ready
- Reason final closeout is not ready: M3 has unresolved code-review finding `CR7-F1`, and downstream explain-change, verify, and PR gates have not run.

## Residual Risks

No additional residual risks beyond `CR7-F1`.
