# Code Review R9 - M3 official archive URL rerun

Review ID: code-review-r9
Stage: code-review
Round: 9
Reviewer: Codex code-review skill
Target: commit `8194283` (`Enforce official Codex archive URLs`)
Reviewed artifact: packages/rigorloop; specs/rigorloop-cli-package-and-codex-init.md; specs/rigorloop-cli-package-and-codex-init.test.md; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: clean-with-notes

## Inputs

- Feature spec: `specs/rigorloop-cli-package-and-codex-init.md`
- Test spec: `specs/rigorloop-cli-package-and-codex-init.test.md`
- Architecture/ADR: `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- Active plan: `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md`
- Prior material finding: `CR8-F1`
- Implementation commit: `8194283`

## Scope

This review focused on the `CR8-F1` fix and M3 closeout readiness. It checked that default network adapter installation validates the selected archive URL as the exact official RigorLoop GitHub release archive URL before fetching bytes, while local `--from-archive` remains verified against bundled metadata without making a network fetch.

## Findings

No material findings.

## Review Notes

- `packages/rigorloop/dist/lib/official-archive-url.js:5` defines the canonical expected URL as `https://github.com/xiongxianfei/rigorloop/releases/download/<release>/<archive>`.
- `packages/rigorloop/dist/lib/official-archive-url.js:21` verifies protocol, host, exact pathname, no query, no fragment, no credentials, and no port before accepting a network archive URL.
- `packages/rigorloop/dist/bin/rigorloop.js` calls URL validation in the default network path after bundled metadata validation and before `fetchBytes(artifact.url)`.
- Local archive mode still returns archive work from `--from-archive` before the network URL fetch path, so it keeps the accepted user-facing local command model.
- `packages/rigorloop/test/cli.test.js` now uses a mocked fetch seam for the official GitHub release URL instead of a production-path `data:` URL.
- Negative tests cover `data:`, wrong host, wrong owner/repo, wrong release tag, wrong archive filename, query string, fragment, `http:`, and `raw.githubusercontent.com` cases.
- The spec and test spec now explicitly require official archive URL enforcement for network-mode adapter installation.

## Validation Evidence Reviewed

- `npm test --prefix packages/rigorloop` passed after the `CR8-F1` fix.
- Real default network install smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --json` passed after the `CR8-F1` fix.
- Real local archive smoke with `node packages/rigorloop/dist/bin/rigorloop.js init --adapter codex --from-archive ./rigorloop-adapter-codex-v0.1.3.zip --json` passed after the `CR8-F1` fix.
- `python scripts/test-select-validation.py` passed after the `CR8-F1` fix.
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR8-F1` fix.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow` passed after the `CR8-F1` fix.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed after the `CR8-F1` fix.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after the `CR8-F1` fix for the package, spec, test spec, architecture, plan, change metadata, review log, review-resolution, and `code-review-r8.md`.
- `bash scripts/ci.sh --mode explicit ...` passed after the `CR8-F1` fix for the M3 package and lifecycle surfaces.
- `git diff --check --` passed after the `CR8-F1` fix.

## Decision

M3 is clean with notes. `CR8-F1` is closed, and no new material findings were identified.

## Handoff

- Current milestone state: closed
- Remaining in-scope implementation milestones: none
- Next stage: lifecycle closeout, starting with `explain-change`
- Final closeout readiness: not complete until explain-change, verify, and PR gates run
