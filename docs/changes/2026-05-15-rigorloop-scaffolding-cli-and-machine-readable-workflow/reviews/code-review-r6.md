# Code Review R6

Review ID: code-review-r6
Stage: code-review
Round: 6
Reviewer: Codex code-review skill
Target: commit `8951ff0` (`M3: install verified codex adapter archives`)
Reviewed artifact: packages/rigorloop; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `git show 8951ff0 -- packages/rigorloop docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- Tracked governing branch state: commit `8951ff0`
- Governing artifacts:
  - `specs/rigorloop-cli-package-and-codex-init.md` R46-R61c and R68-R75
  - `specs/rigorloop-cli-package-and-codex-init.test.md` T15-T19, T29-T44
  - `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md` M3 and Current Handoff Summary
  - `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
  - `docs/architecture/system/architecture.md` CLI package and Codex init boundaries
- Validation evidence recorded in the active plan and change metadata:
  - `npm test --prefix packages/rigorloop` passed after M3 implementation.
  - Temporary-project smoke for the real `v0.1.3` Codex archive with `init --adapter codex --from-archive` passed.
  - `python scripts/test-select-validation.py` passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.3.json --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md` passed.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
  - `git diff --check --` passed.

## Diff Summary

M3 adds package-bundled Codex adapter metadata, release metadata and archive fetch paths, local `--from-archive` verification, ZIP parsing, SHA-256 and size checks, install-root and symlink checks, `rigorloop-tree-hash-v1`, adapter file extraction, planned lockfile hash output, and tests for success, missing metadata, incompatible releases, metadata rejection, archive traversal, symlinks, checksum/size/tree mismatches, overwrite conflicts, and no durable lockfile writes.

## Findings

### CR6-F1: Runtime metadata source overrides bypass the official and bundled metadata trust boundary

Finding ID: CR6-F1
Severity: blocker
Location: packages/rigorloop/dist/bin/rigorloop.js:211; packages/rigorloop/dist/bin/rigorloop.js:220; packages/rigorloop/test/cli.test.js:433; packages/rigorloop/test/cli.test.js:467

Evidence: The approved architecture says network mode fetches release metadata and archives from the official GitHub release source, while local mode verifies archives against bundled adapter metadata shipped with the installed CLI package version (`docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md:31`, `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md:32`). The spec likewise requires official release metadata for network mode and bundled adapter metadata for local archive mode (`specs/rigorloop-cli-package-and-codex-init.md:255`, `specs/rigorloop-cli-package-and-codex-init.md:257`). The implementation instead lets `RIGORLOOP_RELEASE_METADATA_URL` replace the official release metadata URL (`packages/rigorloop/dist/bin/rigorloop.js:211`) and lets `RIGORLOOP_METADATA_FILE` replace the bundled metadata path (`packages/rigorloop/dist/bin/rigorloop.js:220`). The M3 tests exercise successful install through those overrides, including a `data:` metadata URL for network mode and arbitrary fixture metadata for local mode (`packages/rigorloop/test/cli.test.js:433`, `packages/rigorloop/test/cli.test.js:467`). A caller can therefore supply metadata that claims `source_repository: xiongxianfei/rigorloop`, matching hashes, and `validation.result: pass`, and the CLI will trust it despite it not being the official release source or package-bundled metadata.

Required outcome: Runtime user environment must not be able to replace the official network metadata source or package-bundled local metadata source in production command paths.

Safe resolution path: Remove the production `RIGORLOOP_RELEASE_METADATA_URL` and `RIGORLOOP_METADATA_FILE` overrides, or guard them behind a package-internal test-only mode that cannot be used by ordinary CLI execution. Keep package tests fixture-backed through a non-shipped seam, subprocess fixture package, or local helper function that does not alter the public trust boundary. Add regression tests proving ordinary runtime environment variables cannot redirect metadata trust.

### CR6-F2: Metadata-hash verification is not implemented or tested

Finding ID: CR6-F2
Severity: major
Location: packages/rigorloop/dist/bin/rigorloop.js:232; packages/rigorloop/dist/bin/rigorloop.js:281; packages/rigorloop/test/cli.test.js:711; packages/rigorloop/test/cli.test.js:846

Evidence: The spec requires metadata-hash mismatches to produce status `error` and exit code `3` (`specs/rigorloop-cli-package-and-codex-init.md:318`) and lists metadata-hash failures with checksum, size, and tree-hash verification failures (`specs/rigorloop-cli-package-and-codex-init.md:310`). The implementation fetches network metadata through `response.json()` and discards the raw bytes before any hash can be computed (`packages/rigorloop/dist/bin/rigorloop.js:232`). `validateMetadata` only checks that `metadata.metadata.sha256` is syntactically hash-shaped (`packages/rigorloop/dist/bin/rigorloop.js:281`); it never compares fetched metadata bytes with a trusted expected hash. The package tests treat a missing metadata hash as a blocked `metadata-invalid` case (`packages/rigorloop/test/cli.test.js:711`) and T34 covers archive SHA, archive size, and tree hash mismatches but not metadata-hash mismatch (`packages/rigorloop/test/cli.test.js:846`).

Required outcome: Metadata-hash verification must either be implemented according to the approved contract, including status `error` and exit code `3` for mismatches, or the spec must be revised before M3 can close.

Safe resolution path: Define the trusted expected metadata hash source for network metadata, fetch metadata as bytes, verify those bytes against that trusted expected hash before parsing or trusting artifact URLs, and add direct tests for metadata-hash mismatch exit `3`. If the current approved architecture cannot supply a trusted expected hash without a broader decision, stop and revise the spec/architecture instead of silently treating metadata hashes as informational fields.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR6-F1` violates the official/bundled metadata source requirements; `CR6-F2` violates the metadata-hash mismatch contract in R60/R61c. |
| Test coverage | concern | Tests cover many archive failure modes, but they rely on runtime metadata source overrides and do not cover metadata-hash mismatch as required by T34. |
| Edge cases | concern | Path traversal, symlink, install-root, overwrite, checksum, size, tree mismatch, incompatible release, missing bundled metadata, and real archive smoke are covered; metadata-hash mismatch lacks direct proof. |
| Error handling | concern | Archive SHA, size, tree, and path verification failures use exit `3`; invalid metadata hash is not classified as the expected verification failure class. |
| Architecture boundaries | block | The shipped environment overrides let runtime state replace official release metadata and package-bundled metadata, crossing the ADR trust boundary. |
| Compatibility | pass | The package remains private, uses one binary, keeps lockfile output planned-only, and does not add non-Codex adapters. |
| Security/privacy | block | Untrusted metadata source substitution can make the archive verifier trust attacker-controlled archive URLs and hashes. |
| Derived artifact currency | pass | No generated adapter skill bodies are committed; package metadata is a small bundled metadata file, not an adapter archive. |
| Unrelated changes | pass | The M3 diff is scoped to CLI archive verification/install behavior, tests, metadata, and lifecycle state. |
| Validation evidence | concern | Recorded validation is relevant but cannot prove the missing metadata trust-boundary and metadata-hash requirements. |

## Review Status

changes-requested

## Milestone-Aware Handoff

- Reviewed milestone: M3. Codex adapter metadata, archive verification, extraction, and tree hash
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR6-F1` and `CR6-F2`
- Remaining in-scope implementation milestones: M3
- Next stage: review-resolution M3, then implement accepted fixes for M3
- Final closeout readiness: not ready
- Reason final closeout is not ready: M3 has unresolved code-review findings, and downstream explain-change, verify, and PR gates have not run.

## Residual Risks

No additional residual risks beyond `CR6-F1` and `CR6-F2`.
