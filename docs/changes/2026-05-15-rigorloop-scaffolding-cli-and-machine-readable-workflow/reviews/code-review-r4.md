# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review skill
Target: commit `3561f74` (`M2: add codex init planning and manifest scaffold`)
Reviewed artifact: packages/rigorloop; docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface: `git show 3561f74 -- packages/rigorloop docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- Tracked governing branch state: commit `3561f74`
- Governing artifacts:
  - `specs/rigorloop-cli-package-and-codex-init.md` R38-R45, R62-R67
  - `specs/rigorloop-cli-package-and-codex-init.test.md` T12, T20-T24, T26, T41
  - `docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md` M2 and Current Handoff Summary
  - `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- Validation evidence recorded in the active plan and change metadata:
  - `npm test --prefix packages/rigorloop` passed.
  - `python scripts/test-select-validation.py` passed.
  - temporary-project dry-run, actual scaffold, missing archive, and overwrite-refusal smoke checks passed.
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml --path specs/rigorloop-cli-package-and-codex-init.test.md` passed.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-15-rigorloop-cli-package-and-codex-init.md --path docs/plan.md --path specs/rigorloop-cli-package-and-codex-init.test.md --path docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml` passed.
  - `git diff --check --` passed.

## Diff Summary

M2 expands `rigorloop init --adapter codex` beyond the M1 placeholder. It parses `--from-archive` and `--force`, builds planned manifest and planned lockfile JSON, writes a first-slice `rigorloop.yaml`, creates `.agents/skills`, refuses incompatible manifests and `.agents` user-file conflicts, and adds package tests for dry-run, actual scaffold, local-archive planning, no-lockfile behavior, and overwrite refusal.

## Findings

### CR4-F1: Write plan omits the parent `.agents` directory that actual init creates

Finding ID: CR4-F1
Severity: major
Location: packages/rigorloop/dist/bin/rigorloop.js:293; packages/rigorloop/dist/bin/rigorloop.js:459; packages/rigorloop/test/cli.test.js:256

Evidence: The approved spec requires that before mutating, `init` computes a write plan identifying every file and directory it intends to create, update, skip, or block (`specs/rigorloop-cli-package-and-codex-init.md:235`). The M2 implementation plans only one directory action for `.agents/skills` (`packages/rigorloop/dist/bin/rigorloop.js:293`) but actual init calls `mkdirSync(resolve(process.cwd(), INSTALL_ROOT), { recursive: true })` (`packages/rigorloop/dist/bin/rigorloop.js:459`). In an empty project, that recursive write creates both `.agents` and `.agents/skills`. The M2 tests assert the `.agents/skills` action and the resulting install root, but they do not assert that `.agents` is present in the write plan (`packages/rigorloop/test/cli.test.js:256`).

Required outcome: The write plan and JSON/human-visible action list must account for the parent `.agents` directory whenever the command will create, skip, or block it, so dry-run and actual output accurately identify every directory mutation before it happens.

Safe resolution path: Add `.agents` as its own `create-dir` action/artifact in the plan. For an absent parent, dry-run should mark it `planned` and actual init should mark it `done`; for an existing directory, mark it `skipped` or `existing`; for an existing file, keep the current overwrite-refusal blocker. Update M2 tests to assert both `.agents` and `.agents/skills` appear in dry-run and actual action lists.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | Most M2 behavior aligns with R21-R39 and R62-R67, but R40 is incomplete because `.agents` is created implicitly without a plan entry. |
| Test coverage | concern | Tests cover dry-run, manifest creation, local archive path validation, existing manifest handling, overwrite refusal, and no-lockfile behavior, but they do not prove every created directory is listed in the write plan. |
| Edge cases | concern | User-file overwrite conflict with `.agents` is covered; absent `.agents` parent creation is not represented as a first-class planned mutation. |
| Error handling | pass | Missing `--from-archive`, missing archive path, incompatible manifest, and overwrite conflicts map to expected public result classes. |
| Architecture boundaries | pass | The change stays within package-local CLI scaffolding and does not implement archive verification/extraction, durable lockfile writes, public publication, or non-Codex adapters. |
| Compatibility | pass | Existing repository validation remains script-owned; selector-selected package validation continues to run. |
| Security/privacy | pass | M2 does not read secrets, require network access, extract archives, or print project file contents beyond generated scaffold output. |
| Derived artifact currency | pass | No generated public adapter output is introduced. |
| Unrelated changes | pass | The diff is scoped to CLI package code/tests and lifecycle evidence for M2. |
| Validation evidence | pass | The recorded package tests and selected CI are relevant, but passing tests do not cover `CR4-F1`. |

## Review Status

changes-requested

## Milestone-Aware Handoff

- Reviewed milestone: M2. Init dry-run, write planning, and `rigorloop.yaml` scaffold
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR4-F1`
- Remaining in-scope implementation milestones: M2, M3
- Next stage: review-resolution M2, then implement the accepted fix for M2
- Final closeout readiness: not ready
- Reason final closeout is not ready: M2 has an unresolved code-review finding, M3 has not started, and downstream explain-change, verify, and PR gates have not run.

## Residual Risks

No additional residual risks beyond `CR4-F1`.
