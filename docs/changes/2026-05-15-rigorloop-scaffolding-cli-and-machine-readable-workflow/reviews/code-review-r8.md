# Code Review R8

Review ID: code-review-r8
Stage: code-review
Round: 8
Reviewer: Codex code-review skill
Target: commit `5cc5b34` (`Resolve M3 bundled metadata install path`)
Reviewed artifact: packages/rigorloop; specs/rigorloop-cli-package-and-codex-init.md; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `git show 5cc5b34 -- packages/rigorloop specs/rigorloop-cli-package-and-codex-init.md specs/rigorloop-cli-package-and-codex-init.test.md docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md docs/architecture/system docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow`
- Tracked governing branch state: commit `5cc5b34`
- Governing artifacts:
  - `specs/rigorloop-cli-package-and-codex-init.md` R49-R61c, Security and privacy, AC4-AC11
  - `specs/rigorloop-cli-package-and-codex-init.test.md` T15-T19, T29-T44
  - `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
  - `docs/architecture/system/architecture.md`
  - `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md` M3 and Current Handoff Summary
- Validation evidence reviewed:
  - `npm test --prefix packages/rigorloop` passed after the `CR7-F1` fix.
  - Real default network install smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` passed after the `CR7-F1` fix.
  - Real local archive smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed after the `CR7-F1` fix.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-package-and-codex-init.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/context.mmd --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-log.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/review-resolution.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/reviews/code-review-r7.md` passed after the `CR7-F1` fix.

## Diff Summary

The `CR7-F1` fix changes the first-slice default install trust model so both default network install and local `--from-archive` install load bundled adapter metadata, verify its bytes against `bundled_metadata_sha256` from `releases.json`, parse metadata only after hash verification, and then either download the archive URL named by the trusted metadata or verify the local archive. It updates the spec, test spec, ADR, architecture package, tests, release index, review-resolution, and plan evidence accordingly.

## Findings

### CR8-F1: Network install does not enforce that bundled metadata names an official adapter archive URL

Finding ID: CR8-F1
Severity: major
Location: packages/rigorloop/dist/bin/rigorloop.js:358; packages/rigorloop/dist/bin/rigorloop.js:913; packages/rigorloop/test/cli.test.js:496; specs/rigorloop-cli-package-and-codex-init.md:255; specs/rigorloop-cli-package-and-codex-init.md:443

Evidence: The revised spec says networked adapter installation must use bundled official adapter metadata and then download the official adapter archive URL named by that metadata (`specs/rigorloop-cli-package-and-codex-init.md:255`), and the security boundary says network access must be limited to fetching official adapter archives for the requested adapter (`specs/rigorloop-cli-package-and-codex-init.md:443`). The implementation validates only that the artifact URL is a non-empty string as part of metadata completeness (`packages/rigorloop/dist/bin/rigorloop.js:358`) and then fetches `artifact.url` directly in default network mode (`packages/rigorloop/dist/bin/rigorloop.js:913`). The updated T15 test proves the command succeeds with a `data:application/octet-stream` artifact URL (`packages/rigorloop/test/cli.test.js:496`), which is useful as a fixture seam but also demonstrates that production validation does not reject non-official archive URLs in bundled metadata.

Required outcome: Before M3 closes, the CLI must enforce that network-mode artifact URLs are official RigorLoop GitHub release archive URLs for the expected release and archive filename, or the approved spec/security boundary must be revised to allow arbitrary package-bundled archive URLs in first-slice network install.

Safe resolution path: Add a package-local URL validator for network archive URLs, such as requiring `https://github.com/xiongxianfei/rigorloop/releases/download/<release>/<archive>` with `<release>` matching the package-compatible release and `<archive>` matching the selected Codex artifact filename. Run this validation before `fetchBytes(artifact.url)` in default network mode. Keep tests deterministic by either using a fixture package with the official URL plus a test fetch seam, or by structuring tests so production URL validation is unit-tested separately and the real network smoke proves the official URL path. Add a negative test where bundled metadata names a non-official archive URL and the command returns `status: error`, exit code `3`, with a clear metadata/archive URL error code.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR8-F1` conflicts with R49 and the security requirement that network access is limited to official adapter archives. |
| Test coverage | concern | Tests cover bundled metadata hashing and real archive smoke, but T15 also proves a non-official `data:` archive URL can drive default network install. |
| Edge cases | concern | Metadata hash mismatch, missing trust root, local archive verification, checksum, size, tree hash, traversal, symlink, install root, overwrite, and missing metadata cases are covered; non-official archive URL rejection is not. |
| Error handling | concern | Metadata schema and hash failures map to exit `3`, but there is no classified failure for invalid network archive URL. |
| Architecture boundaries | concern | The bundled metadata trust-root model is respected, but the network egress boundary is not enforced independently. |
| Compatibility | pass | The one-package CLI shape, no durable lockfile write, Codex-only scope, and public npm publication block remain intact. |
| Security/privacy | block | A malformed bundled metadata file could make default network install fetch from a non-official URL despite the security boundary. |
| Derived artifact currency | pass | `releases.json` matches the bundled metadata hash model and no adapter archive is bundled into npm source. |
| Unrelated changes | pass | The diff is scoped to CR7 metadata trust behavior, tests, specs, architecture, and lifecycle evidence. |
| Validation evidence | concern | Existing validation is relevant but does not prove official archive URL enforcement. |

## Review Status

changes-requested

## Milestone-Aware Handoff

- Reviewed milestone: M3. Codex adapter metadata, archive verification, extraction, and tree hash
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR8-F1`
- Remaining in-scope implementation milestones: M3
- Next stage: review-resolution M3, then implement accepted fix or approved contract revision for M3
- Final closeout readiness: not ready
- Reason final closeout is not ready: M3 has unresolved code-review finding `CR8-F1`, and downstream explain-change, verify, and PR gates have not run.

## Residual Risks

No additional residual risks beyond `CR8-F1`.
