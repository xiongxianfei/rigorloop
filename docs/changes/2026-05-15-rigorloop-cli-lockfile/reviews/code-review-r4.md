# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: M2. Successful lockfile creation and update after verified Codex install
Status: approved

## Review inputs

- Diff/review surface: unstaged M2 lockfile implementation and CR3-F1 fix, including `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`, and `specs/rigorloop-cli-lockfile.test.md`
- Prior M2 review: `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r3.md`
- Review resolution: `docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`
- Plan: `docs/plans/2026-05-16-rigorloop-cli-lockfile.md`
- Spec: `specs/rigorloop-cli-lockfile.md`
- Test spec: `specs/rigorloop-cli-lockfile.test.md`
- Validation evidence:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'CR3-F1|T26 adapter file|TLF-020|TLF-021'`
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-cli-lockfile`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path specs/rigorloop-cli-lockfile.test.md --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`
  - `git diff --check -- packages/rigorloop/dist/bin/rigorloop.js packages/rigorloop/test/cli.test.js specs/rigorloop-cli-lockfile.test.md docs/plans/2026-05-16-rigorloop-cli-lockfile.md docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml docs/changes/2026-05-15-rigorloop-cli-lockfile/review-log.md docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`

## Diff summary

The M2 rerun-reviewed implementation now verifies the installed Codex adapter root before lockfile writes. `verifyInstalledTree` computes expected rows from the verified archive entries, computes actual rows from `.agents/skills`, compares both row sets and the trusted metadata tree hash, and returns `installed-tree-mismatch` before lockfile creation or update when the root contains extra, modified, or partial files. Successful lockfile writes record the trusted metadata tree hash and verified file count. Tests now cover extra-file mismatch, modified-file mismatch, partial-tree mismatch, exact existing tree success, unchanged existing lockfile on mismatch, and the updated installed-tree verification test-spec expectations.

## Findings

No material findings.

## Prior finding closeout

### CR3-F1

Status: resolved by implementation

Evidence:

- `packages/rigorloop/dist/bin/rigorloop.js` now calls `verifyInstalledTree` before archive action planning and again before `rigorloop.lock` serialization.
- `verifyInstalledTree` compares actual installed rows from `.agents/skills` with expected rows from the verified archive entries and rejects mismatches with `installed-tree-mismatch`.
- Lockfile serialization receives `archiveWork.artifact.tree_sha256`, so successful writes record the trusted metadata tree hash rather than a new hash that can include unrelated files.
- Regression tests prove extra, modified, and partial installed trees exit `3`, do not write a new lockfile, and leave existing lockfile bytes unchanged on mismatch.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | M2 now satisfies R36-R39 and R45a-R45e for successful verified writes and no-write behavior on archive, tree-hash, manifest, and mutation-safety failures. |
| Test coverage | pass | Package tests cover network and local lockfile writes, local archive basename portability, failed archive verification no-write, CR3-F1 installed-tree mismatch cases, exact-tree success, and existing-lockfile unchanged behavior. |
| Edge cases | pass | Direct CR3-F1 tests cover extra file, modified expected file, partial installed tree, exact existing tree, and mismatch with an existing lockfile. |
| Error handling | pass | Installed-tree mismatch returns `status: error` through the validation-failed exit class, while directory/file conflicts still use mutation-conflict handling. |
| Architecture boundaries | pass | The trust root remains package-bundled metadata and verified archive entries; npm package contents are not treated as authored adapter source. |
| Compatibility | pass | Existing first-slice projects without `rigorloop.lock` remain valid, and exact existing Codex adapter trees can receive a lockfile without rewriting adapter files. |
| Security/privacy | pass | Local archive lockfile tests assert absolute archive paths and machine-local data are not serialized. |
| Derived artifact currency | pass | No generated workflow or adapter release artifacts are modified by M2. |
| Unrelated changes | pass | Reviewed package/test/spec-test changes are scoped to durable lockfile creation/update and CR3-F1 coverage. |
| Validation evidence | pass | Focused CR3-F1 tests, full package tests, review artifact validation, change metadata validation, artifact lifecycle validation, selected CI, and diff check are recorded as passed. |

## No-finding rationale

The rerun-reviewed implementation closes the CR3-F1 gap without expanding M2 into full M3 drift reporting. It allows absent or empty install roots to proceed, allows exact existing verified adapter content to create/update the lockfile, rejects non-empty mismatched installed roots before writes, records trusted metadata tree state, and leaves existing lockfiles unchanged when installed-tree verification fails.

## Residual risks

M3 still needs to implement the explicit drift/conflict contract for existing lockfile-recorded generated output, including drift-specific blocker reporting and missing-root behavior. This clean review closes only M2.

## Handoff

- Reviewed milestone: M2. Successful lockfile creation and update after verified Codex install
- Milestone state after review: closed
- Required review-resolution: closed for M2
- Remaining implementation milestones: M3
- Next stage: implement M3
- Final closeout readiness: not ready; M3 implementation, code-review, explain-change, verify, and PR handoff remain open
