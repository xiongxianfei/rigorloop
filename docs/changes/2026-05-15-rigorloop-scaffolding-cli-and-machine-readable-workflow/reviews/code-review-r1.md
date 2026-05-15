# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `77c0c0c` (`M1: add rigorloop CLI package skeleton`)
Reviewed artifact: packages/rigorloop; scripts/validation_selection.py; scripts/test-select-validation.py; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `git show 77c0c0c -- packages/rigorloop scripts/validation_selection.py scripts/test-select-validation.py`
- Tracked governing branch state: commit `77c0c0c`
- Governing artifacts:
  - `specs/rigorloop-cli-package-and-codex-init.md`
  - `specs/rigorloop-cli-package-and-codex-init.test.md`
  - `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md`
  - `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- Validation evidence recorded in the active plan:
  - `npm test --prefix packages/rigorloop` passed.
  - `python scripts/test-select-validation.py` passed.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path scripts/validation_selection.py --path scripts/test-select-validation.py` passed.

## Diff Summary

M1 adds the `packages/rigorloop` package candidate with `@xiongxianfei/rigorloop` metadata, one `rigorloop` binary, Node test coverage, a minimal CLI entrypoint for help/version/init dry-run routing, and selector support for package validation through `rigorloop_cli.test`.

The milestone also records the broader proposal/spec/architecture/plan/test-spec artifacts in the same committed branch state.

## Findings

### CR1-F1: Exit-code contract coverage is incomplete for expected error classes

Finding ID: CR1-F1
Severity: major
Location: packages/rigorloop/dist/bin/rigorloop.js:17; packages/rigorloop/test/cli.test.js:174

Evidence: The approved spec requires exit code `3` for validation failures and exit code `1` only for internal or unexpected errors (`specs/rigorloop-cli-package-and-codex-init.md:143`). The same spec later requires expected archive verification failures to use status `error` and exit code `3` (`specs/rigorloop-cli-package-and-codex-init.md:310` and `specs/rigorloop-cli-package-and-codex-init.md:318`). The M1 implementation introduces a shared status-to-exit map where `error` maps to `EXIT.internal` (`packages/rigorloop/dist/bin/rigorloop.js:17`), and the M1 package test named for T11 only asserts exit codes `0`, `2`, and `4` (`packages/rigorloop/test/cli.test.js:174`). The active test spec requires T11 to assert validation/archive failures map to `3`, overwrite refusal maps to `5`, and internal unexpected errors map to `1` (`specs/rigorloop-cli-package-and-codex-init.test.md:226`).

Required outcome: The M1 shared command-result/exit-code layer and tests must represent every public exit-code class required by R12/T11, including expected validation/archive failures as exit `3`, overwrite refusal as exit `5`, and unexpected internal failures as exit `1`, without forcing future M3 archive verification errors through the internal-error path.

Safe resolution path: Add a small package-local command-result or exit-code helper that can be tested directly with table-driven unit tests for all R12 classes, update the CLI to use that helper for current M1 paths, and update `packages/rigorloop/test/cli.test.js` so T11 covers `0`, `2`, `3`, `4`, `5`, and `1`. Keep actual archive verification behavior deferred to M3; the fix only needs the public result mapping layer to be ready for those future command paths.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | Package name, binary, help, version, unsupported adapter, and publication boundary align with R1-R8/R76-R79. Exit-code mapping for R12 is incomplete as recorded in CR1-F1. |
| Test coverage | concern | M1 tests cover package metadata and visible command paths, but T11 does not cover every exit-code class required by the active test spec. |
| Edge cases | concern | Unsupported adapter, quiet/debug/no-color, and no-write unsupported adapter paths are covered. Expected validation/archive error mapping edge cases are not directly covered. |
| Error handling | concern | Unknown command and unsupported adapter paths are safe; the shared `error` mapping currently points at internal-error exit `1`. |
| Architecture boundaries | pass | The implementation keeps one package and one binary, does not bundle adapter archives, and does not install from `.codex/skills`. |
| Compatibility | pass | Existing repository validation remains script-owned, and selector routing is additive for `packages/rigorloop`. |
| Security/privacy | pass | M1 does not handle secrets, network, or archive extraction. No project file contents are sent over the network. |
| Derived artifact currency | pass | No generated adapter output is introduced. |
| Unrelated changes | pass | The code changes are scoped to the CLI package and selector route needed for M1 validation. |
| Validation evidence | pass | The recorded `npm test`, selector regression, and selected CI evidence are relevant, but passing tests do not cover CR1-F1. |

## Review Status

changes-requested

## Milestone-Aware Handoff

- Reviewed milestone: M1. Package skeleton, command discovery, and command contract core
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR1-F1`
- Remaining in-scope implementation milestones: M1, M2, M3
- Next stage: review-resolution M1, then implement the accepted fix for M1
- Final closeout readiness: not ready
- Reason final closeout is not ready: M1 has an unresolved code-review finding, M2 and M3 have not started, and downstream explain-change, verify, and PR gates have not run.

## Residual Risks

No additional residual risks beyond `CR1-F1`.
