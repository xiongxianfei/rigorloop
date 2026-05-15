# RigorLoop Scaffolding CLI and Machine-Readable Workflow Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the scaffolding CLI and machine-readable workflow change.

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: proposal-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5
Review closeout: code-review-r6
Review closeout: code-review-r7
Review closeout: code-review-r8

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`, `code-review-r6`, `code-review-r7`, `code-review-r8`
- Findings resolved: 9
- Unresolved findings: 0
- Final result: spec-review findings have accepted dispositions and the same-stage `spec-review-r2` rerun approved the revised spec. `code-review-r1` finding `CR1-F1` has an accepted implementation fix, `code-review-r2` closed M1 with no material findings, direct `code-review-r3` found no material issues in the current tracked M1 resolution, `code-review-r4` finding `CR4-F1` has an accepted implementation fix, `code-review-r5` closed M2 with no material findings, `code-review-r6` findings `CR6-F1` and `CR6-F2` have accepted implementation fixes, `code-review-r7` finding `CR7-F1` has an accepted implementation fix, `code-review-r8` finding `CR8-F1` has an accepted implementation fix, and `code-review-r9` closed M3 with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SR1-F1 | accepted | resolved | `--from-archive` uses package-bundled official adapter metadata; no first-slice `--metadata` flag. |
| SR1-F2 | accepted | resolved | The first-slice generated `rigorloop.yaml` minimum YAML shape is now defined. |
| SR1-F3 | accepted | resolved | Expected archive verification failures now use status `error` and exit code `3`. |
| CR1-F1 | accepted | resolved | M1 now maps exit codes from internal result class/failure kind and T11 covers every public exit-code class. |
| CR4-F1 | accepted | resolved | M2 now plans `.agents` and `.agents/skills` as first-class directory actions before mutation. |
| CR6-F1 | accepted | resolved | Runtime metadata source overrides were removed from production metadata lookup; tests now use fixture package metadata. |
| CR6-F2 | accepted | resolved | Adapter metadata is verified against a package-bundled release index hash before parsing, with metadata hash mismatch mapped to exit code `3`; `CR7-F1` revised the trust root to bundled metadata for both install paths. |
| CR7-F1 | accepted | resolved | Default network install now uses bundled official adapter metadata as the trust root and fetches only the official archive URL named by that metadata. |
| CR8-F1 | accepted | resolved | Network install now validates that bundled metadata names the exact official GitHub release archive URL before fetching bytes. |

## Common Resolution Metadata

- Owner: spec author
- Owning stage: spec
- Validation target: revise `specs/rigorloop-cli-package-and-codex-init.md`, rerun `spec-review`, then run review artifact, change metadata, artifact lifecycle, and selected CI validation.
- Validation evidence: spec revision completed; same-stage spec-review rerun approved the revised spec. Code-review finding `CR1-F1` fix validation is recorded below.

## Finding Details

### proposal-review-r1

No material findings; no resolution entry required.

### spec-review-r1

#### SR1-F1 - Local archive metadata source is undefined

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Keep the user-facing command simple: `--from-archive <path>` only. Do not require a separate `--metadata` option in the first slice. The CLI verifies local archives against official adapter metadata bundled with the installed `@xiongxianfei/rigorloop` package version.
Rationale: Users should not need to manage a second metadata file for normal local archive installation. The command remains simple while preserving verification through package-bundled release metadata.
Validation target: Add requirements and tests for matching bundled metadata, missing bundled metadata, archive checksum mismatch, size mismatch, tree-hash mismatch, path traversal, and incompatible release version.
Validation evidence: `specs/rigorloop-cli-package-and-codex-init.md` now requires bundled adapter metadata for local archive verification and no first-slice `--metadata` flag. `spec-review-r2` approved the revised spec.

#### SR1-F2 - Generated `rigorloop.yaml` shape is unspecified

Finding ID: SR1-F2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define the exact minimum YAML keys and values generated by first-slice init and omit `validation.commands` by default.
Rationale: `rigorloop.yaml` is a public config surface and tests should not invent its shape.
Validation target: Revised spec requirements and same-stage spec-review rerun.
Validation evidence: `specs/rigorloop-cli-package-and-codex-init.md` now includes a normative minimum `rigorloop.yaml` shape. `spec-review-r2` approved the revised spec.

#### SR1-F3 - Archive verification exit code is inconsistent

Finding ID: SR1-F3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Map checksum, size, tree-hash, metadata-hash, and path-traversal failures to status `error` and exit code `3`.
Rationale: The current spec reserves exit code `1` for internal or unexpected errors, but also assigns expected verification failures to exit code `1`.
Validation target: Revised spec requirements and same-stage spec-review rerun.
Validation evidence: `specs/rigorloop-cli-package-and-codex-init.md` now maps expected archive verification failures to exit code `3`. `spec-review-r2` approved the revised spec.

### spec-review-r2

No material findings; no resolution entry required. The same-stage spec-review rerun approved the revised spec and closed `SR1-F1`, `SR1-F2`, and `SR1-F3`.

### architecture-review-r1

No material findings; no resolution entry required. The architecture-review approved the canonical architecture package update and CLI package/Codex init ADR.

### plan-review-r1

No material findings; no resolution entry required. The plan-review approved the active execution plan for the first CLI package and Codex init slice.

### code-review-r1

#### CR1-F1 - Exit-code contract coverage is incomplete for expected error classes

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Add a package-local command-result or exit-code helper that can be tested directly for every R12 exit-code class, update the CLI to use it for current M1 paths, and update the M1 T11 package test to cover exit codes `0`, `2`, `3`, `4`, `5`, and `1`.
Rationale: M1 introduced the shared command-result surface. It must not encode expected future validation/archive failures as internal errors before M2/M3 build on it.
Validation target: Run `npm test --prefix packages/rigorloop`, `python scripts/test-select-validation.py`, and selected CI for the package, selector, active plan, test spec, and change metadata.
Validation evidence: `packages/rigorloop/dist/lib/command-result.js` now maps exit codes from `exit_class`/failure kind with status fallback only for compatibility; `packages/rigorloop/dist/bin/rigorloop.js` uses the helper for current M1 paths; `packages/rigorloop/test/cli.test.js` T11 covers success, warning, blocked, validation failure, invalid usage, mutation conflict, and internal failure classes. `npm test --prefix packages/rigorloop` passed after the fix.

### code-review-r2

No material findings; no resolution entry required. The code-review rerun closed `CR1-F1` and marked M1 clean with notes.

### code-review-r3

No material findings; no resolution entry required. This direct isolated code-review found no material issues in commit `071df77`.

### code-review-r4

#### CR4-F1 - Write plan omits the parent `.agents` directory that actual init creates

Finding ID: CR4-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Add `.agents` as a first-class `create-dir` action/artifact in dry-run and actual init output, keep `.agents/skills` as its own `create-dir` action/artifact, and apply only planned pending directory actions during actual init.
Rationale: The CLI write plan is a public safety surface. Users and agents must see every filesystem mutation before `init` writes, and recursive parent-directory creation must not hide mutations missing from JSON or human-readable output.
Validation target: Update the M2 write plan and tests so `.agents` is represented whenever it will be created, skipped, or blocked, then rerun package tests, artifact lifecycle validation, change metadata validation, and selected CI for the package and lifecycle surfaces.
Validation evidence: `packages/rigorloop/test/cli.test.js` now asserts `.agents`, `.agents/skills`, and `rigorloop.yaml` action ordering, empty-project dry-run and actual statuses, existing parent and leaf directory statuses, parent-file conflict, and leaf-file conflict. `packages/rigorloop/dist/bin/rigorloop.js` now builds explicit directory actions for `.agents` and `.agents/skills` and creates only pending planned directories. `npm test --prefix packages/rigorloop` passed after the fix.

### code-review-r5

No material findings; no resolution entry required. The code-review rerun closed `CR4-F1` and marked M2 clean with notes.

### code-review-r6

#### CR6-F1 - Runtime metadata source overrides bypass the official and bundled metadata trust boundary

Finding ID: CR6-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Remove production use of `RIGORLOOP_RELEASE_METADATA_URL` and `RIGORLOOP_METADATA_FILE`. Network mode uses the package-bundled release index for the official metadata URL and expected hash. Local `--from-archive` mode uses package-bundled adapter metadata. Tests use temporary fixture package metadata instead of public runtime metadata overrides.
Rationale: Runtime environment variables must not replace the metadata trust root. Archive verification is only meaningful when metadata authority is official or package-bundled, not user-supplied at runtime.
Validation target: Add regression tests proving ordinary runtime environment variables cannot redirect network or local metadata trust, then rerun package tests and selected CI.
Validation evidence: `packages/rigorloop/dist/bin/rigorloop.js` no longer reads `RIGORLOOP_RELEASE_METADATA_URL` or `RIGORLOOP_METADATA_FILE`. `packages/rigorloop/test/cli.test.js` now uses temporary fixture package metadata and includes tests proving those environment variables are ignored during normal CLI execution. `npm test --prefix packages/rigorloop` passed after the fix.

#### CR6-F2 - Metadata-hash verification is not implemented or tested

Finding ID: CR6-F2
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Add a package-bundled release index with trusted expected metadata SHA-256. Verify adapter metadata bytes before parsing, and map metadata SHA-256 mismatch to status `error` with exit code `3`. The later `CR7-F1` resolution changed the first-slice trust root so both default network install and local archive mode use bundled adapter metadata for the installed package version.
Rationale: The CLI must not trust fetched metadata before verifying it. Metadata-hash mismatch is an expected verification failure, not an internal error.
Validation target: Add direct tests for metadata hash mismatch, valid metadata hash, missing trust root, and verification-before-parse behavior, then rerun package tests and selected CI.
Validation evidence: `packages/rigorloop/dist/metadata/releases.json` records the trusted bundled metadata SHA-256 for `v0.1.3`. `packages/rigorloop/dist/bin/rigorloop.js` verifies adapter metadata bytes before parsing. `packages/rigorloop/test/cli.test.js` covers valid metadata hash, metadata hash mismatch, malformed metadata with wrong hash, and missing trust root. `npm test --prefix packages/rigorloop` passed after the fix.

### code-review-r7

#### CR7-F1 - Bundled network metadata URL points to a release asset that does not exist

Finding ID: CR7-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Decision owner: maintainer
Decision needed: None; maintainer accepted the bundled-metadata trust-root model for the first CLI slice.
Chosen action: Revise the first-slice install contract so default network install uses package-bundled official adapter metadata for the installed CLI package version, then downloads and verifies the official adapter archive. Remove the missing release metadata URL as a required trust source for first-slice install.
Rationale: The trusted metadata URL pointed to a non-existent release asset, so the public default install path would block. Bundled official metadata keeps the user command simple, avoids an extra metadata flag or release asset dependency, and still verifies archive SHA, size, install root, and tree hash before writing files.
Validation target: Add tests proving default install uses bundled metadata, bundled metadata hash mismatch exits `3`, missing bundled metadata blocks with exit `2`, and real Codex archive installation succeeds through bundled metadata.
Validation evidence: `packages/rigorloop/dist/metadata/releases.json` now records `bundled_metadata` and `bundled_metadata_sha256` without a required network metadata URL. `packages/rigorloop/dist/bin/rigorloop.js` verifies bundled metadata bytes before parsing for both default and local archive installs. `packages/rigorloop/test/cli.test.js` proves default install ignores legacy metadata URL fields and uses bundled metadata before archive download, bundled metadata hash mismatch exits `3`, missing trust root blocks, and local archive mode still uses bundled metadata. `npm test --prefix packages/rigorloop` passed after the fix. Real default network install and local archive smoke tests both passed with the official `v0.1.3` Codex archive.

### code-review-r8

#### CR8-F1 - Network install does not enforce that bundled metadata names an official adapter archive URL

Finding ID: CR8-F1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Decision owner: maintainer
Decision needed: None; maintainer accepted enforcing the approved official-archive URL boundary.
Chosen action: Add package-local network archive URL validation. Default network install fetches only `https://github.com/xiongxianfei/rigorloop/releases/download/<release>/<archive>` where the release matches the package-compatible release and the archive matches the selected adapter artifact. Non-official URLs return `status: error`, exit code `3`.
Rationale: Bundled metadata is trusted only within the approved security boundary. It must not expand network egress to arbitrary URLs. Tests may use a fetch seam, but production metadata must still name an official release archive URL.
Validation target: Add negative tests for `data:` URLs, wrong host, wrong repo, wrong release, wrong archive, query/hash, and a positive test that uses an official URL with a mocked fetch response.
Validation evidence: `packages/rigorloop/dist/lib/official-archive-url.js` now defines and validates the exact official GitHub release archive URL. `packages/rigorloop/dist/bin/rigorloop.js` validates the URL before default network fetch. `packages/rigorloop/test/cli.test.js` covers the accepted official URL with a fetch seam and rejects `data:`, wrong host, wrong repo, wrong release, wrong archive, query, hash, `http:`, and `raw.githubusercontent.com` URLs. `npm test --prefix packages/rigorloop`, real default network install smoke, real local archive smoke, selected validation, and `git diff --check --` passed after the fix.

### code-review-r9

No material findings; no resolution entry required. The code-review rerun closed `CR8-F1` and marked M3 clean with notes.

## Shared Validation Evidence

| Validation area | Result | Notes |
|---|---|---|
| Review recording | pass | `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` and closeout mode passed after `CR4-F1` resolution recording. |
| Change metadata | pass | Change metadata validation passed after `spec-review-r2` was recorded. |
| Artifact lifecycle | pass | Artifact lifecycle validation passed for the revised spec, review artifacts, active plan, plan index, and M1 test spec. |
| Selected CI | pass | Selector-selected CI passed for the package, selector, active plan, plan index, M1 test spec, change metadata, review log, review-resolution, and code-review record. |

## Closeout Checklist

- [x] Every material finding has a final disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [x] Validation evidence is recorded for `code-review-r1` finding.
- [x] Validation evidence is recorded for `code-review-r4` finding.
- [x] Validation evidence is recorded for `code-review-r7` finding.
- [x] Validation evidence is recorded for `code-review-r8` finding.
- [x] Closeout status is correct.
