# Code Review R3

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: M2. Successful lockfile creation and update after verified Codex install
Status: changes-requested

## Review inputs

- Diff/review surface: unstaged M2 lockfile implementation changes, including `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/lockfile.js`, and `packages/rigorloop/test/cli.test.js`
- Prior review: `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r2.md`
- Plan: `docs/plans/2026-05-16-rigorloop-cli-lockfile.md`
- Spec: `specs/rigorloop-cli-lockfile.md`
- Test spec: `specs/rigorloop-cli-lockfile.test.md`
- Validation evidence reviewed:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
  - Manual review probe: run package-local `init --adapter codex --json` in a temporary project containing a pre-existing `.agents/skills/custom/NOTE.md`

## Diff summary

The M2 implementation adds durable lockfile creation and update after verified Codex init. It writes `rigorloop.lock` for successful network and local archive installs, records `source: release-archive` or `source: local-archive`, removes the old `lockfile-spec-not-approved` warning, updates JSON actions/artifacts, and adds tests for successful creation, local archive portability, failed archive verification no-write behavior, and source-mode updates.

## Findings

### CR3-F1 - Installed tree hash can include unrelated pre-existing files

Finding ID: CR3-F1
Severity: major

Location: `packages/rigorloop/dist/bin/rigorloop.js`

Evidence:

- The spec says a lockfile entry may claim generated output only after verification succeeds and requires tree hashes for generated adapter output (`specs/rigorloop-cli-lockfile.md` R24-R32, R45e, and state invariant "A lockfile entry may claim generated output only after verification succeeds").
- The M2 plan requires computing lockfile tree hash from installed filesystem state after extraction and says failed tree-hash verification must not create or update `rigorloop.lock`.
- The implementation verifies the archive tree before extraction in `inspectArchive`, then after writing files computes `treeHashForFilesystem(INSTALL_ROOT)` over every regular file currently under `.agents/skills`.
- The implementation writes that filesystem hash into `rigorloop.lock` without comparing it to the trusted adapter metadata tree hash after extraction.
- Direct review probe: in a temporary project with pre-existing `.agents/skills/custom/NOTE.md`, `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` exited `0`, returned `status: success`, and wrote `rigorloop.lock` with `file_count: 24` and tree hash `0c9703cd7894f9bdbdffd706744cc549312608e04b1e195586f4b9bc88ff86ac`, while bundled metadata expects the Codex adapter tree hash `6f6bc739ca20b29844773dd1b7295475ccd53827d68e0784cc1636f6435669c5`.

Required outcome:

Successful M2 lockfile creation or update must record only verified Codex generated adapter output state. If the installed filesystem tree does not match the trusted expected tree after extraction, the command must not write or update `rigorloop.lock`.

Safe resolution path:

After extraction, compute the installed tree using the same generated-output file set represented by the verified archive metadata, or compare the full installed-root tree to the trusted expected tree and fail with a tree-hash verification error before lockfile write when extra or modified files are present. Add a regression test with a pre-existing extra file under `.agents/skills` proving the command exits with validation failure and leaves `rigorloop.lock` absent or unchanged.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | M2 writes a lockfile even when the installed root tree differs from trusted metadata, violating tree verification and no-update-on-failed-verification requirements. |
| Test coverage | concern | Current tests prove normal success and archive-metadata failure paths, but do not cover pre-existing extra files in the installed root before lockfile creation. |
| Edge cases | block | The named failed tree-hash verification no-write behavior is not proven for installed filesystem state after extraction. |
| Error handling | concern | Archive verification failures map correctly, but post-extraction filesystem tree mismatch is not converted to a validation failure. |
| Architecture boundaries | pass | The implementation still uses package-bundled metadata and does not introduce a new metadata trust root. |
| Compatibility | concern | Existing first-slice projects with incidental `.agents/skills` files can receive a lockfile that claims unrelated files as generated output. |
| Security/privacy | pass | No secret or path leakage was observed in the reviewed lockfile fields for covered paths. |
| Derived artifact currency | pass | No generated workflow artifacts are involved. |
| Unrelated changes | pass | Package and lifecycle changes remain scoped to the lockfile initiative. |
| Validation evidence | concern | Recorded validation passed, but it does not exercise the failing installed-tree mismatch case. |

## Handoff

- Reviewed milestone: M2. Successful lockfile creation and update after verified Codex install
- Milestone state after review: resolution-needed
- Required review-resolution: required for `CR3-F1`
- Remaining implementation milestones: M2 resolution, M3
- Next stage: review-resolution for `CR3-F1`, then implement the accepted M2 fix
- Final closeout readiness: not ready; M2 has an unresolved material finding and M3 remains open
