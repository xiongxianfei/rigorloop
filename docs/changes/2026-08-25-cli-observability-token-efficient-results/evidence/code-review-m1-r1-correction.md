# Code review M1 R1 correction implementation

## Result

## Core result

- Skill: implement
- Status: completed
- Completed scope: Implemented corrections for `CLIOBS-M1-CR1` through `CLIOBS-M1-CR5`; expanded direct proof and corrected evidence for `CLIOBS-M1-CR6`.
- Artifacts changed: CLI invocation controller and entrypoint, logging configuration and sink, observability tests, executable token measurement and fixtures, validation selector ownership, compact validation-layering skill guidance, installed-package observability smoke, immutable baseline identity, and M1-M4 evidence.
- Tests added or updated: unsafe and disabled configuration, event-construction and completion-sink failures, semantic exit parity, read-only absent and corrupt lookup, platform defaults, symlink and permission refusal, lock exhaustion, partial-write rollback, real concurrent writers, real six-profile measurement, fixture-identity rejection, and installed-package logging/result/documentation paths.
- Validation performed: focused Node observability tests; lifecycle ownership/withdrawal tests; package tests; measurement command and regression; governed wrapper tests; exact selector command; selector regression; boundary validation; and the focused installed-package observability smoke.
- Validation result: 22 focused observability tests, 6 ownership/withdrawal tests, 201 Node package tests, 3 measurement regressions, all measurement gates, 3 governed-wrapper regressions, the exact C07 selector command, all 154 C04 selector regressions, boundary validation, and C08 packed-package observability smoke passed.
- Open blockers: none in the correction implementation; review-resolution, same-stage code rereview, milestone sequencing, final broad smoke, and verify remain separate gates.
- Next stage: code-review M1 R2 after durable finding resolution
- Claim limitations: This evidence does not claim clean review, milestone closeout, final verification, package readiness, release readiness, or PR readiness.

## Planned milestone

- Change ID: `2026-08-25-cli-observability-token-efficient-results`
- Plan identity: `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`, `sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2`
- Milestone ID: `M1`
- Milestone state: `resolution-needed`
- Baseline or change-pack status: plan and test-spec proof-command corrections are approved and settled; the duplicate architecture registration is withdrawn with the canonical artifact unchanged; accepted implementation findings are ready for durable resolution and same-stage rereview.
- Milestone validation evidence: `evidence/m1-result-model.md`, `evidence/m2-logging-core.md`, `evidence/m3-invocation-integration.md`, and `evidence/m4-token-and-package-proof.md`
- Commit status: not committed; workflow closeout is still in progress.
- Code-review handoff: ready after review-resolution registers the six exact finding dispositions.

## Finding disposition evidence

| Finding | Implemented correction | Direct result |
| --- | --- | --- |
| `CLIOBS-M1-CR1` | Unsafe paths and event construction now degrade diagnostics without suppressing semantic dispatch. | Focused failure regressions pass. |
| `CLIOBS-M1-CR2` | Read validation no longer calls writer initialization or creates an absent store. | Missing-store and corrupt-store lookup regressions pass. |
| `CLIOBS-M1-CR3` | Command output is buffered behind one controller and new projections render after terminal observability with the semantic exit code. | Completion-failure and exit-parity regressions pass. |
| `CLIOBS-M1-CR4` | Locked writes verify full length, sync, and truncate to the pre-append boundary on failure. | Partial-write rollback and six-process concurrency regressions pass. |
| `CLIOBS-M1-CR5` | The six-profile gate executes subprocess interactions and derives bytes, fields, exits, and follow-ups. | Median reduction is 73.04%; all gates pass; defaults remain unchanged. |
| `CLIOBS-M1-CR6` | Added boundary and failure proof, registered selector ownership, added installed-package observability proof, corrected the plan/test-spec gate ownership, and replaced overstated milestone evidence with exact pass/fail records. | C01-C04 and C06-C10 applicable implementation proof pass; C05 runs after durable finding closeout and C11 remains final-verification proof. |

## Validation results and remaining blockers

### C04 — selector regression

`python scripts/test-select-validation.py` passed all 154 tests. `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` each received one compact sentence preserving the approved targeted-proof, selected-check, triggered-broad-smoke, and manual-proof contract without moving detailed mechanics into published skill text.

### C05 — governed lifecycle validation

This command is intentionally rerun by review-resolution after the six exact findings are durably closed. Implementation does not own review closeout or workflow routing.

### C08 — focused packed-package verification

`python scripts/test-npm-package-publication.py NpmPackagePublicationTests.test_packed_package_observability_surface_matches_documentation` passed. It packs and installs the package in a disposable directory and exercises the documented logging, lookup, and result projection surface. Immutable tag verification remains release preparation under approved plan review `plan-review-r3` and test-spec review `test-spec-review-r4`.

### Lifecycle ownership recovery

The canonical governed-lifecycle CLI change was migrated through the CLI to schema v2. The observability change's duplicate registration for `docs/architecture/system/architecture.md` was then withdrawn through the guarded workflow operation. The semantic architecture file remains byte-identical, and ownership/withdrawal regressions passed 6 tests.

## Unchanged surfaces

- Feature specification, architecture, and ADR behavior remain unchanged. The execution plan and test specification changed only proof-command ownership and upstream identity references through governed correction routes.
- Published skills: only compact validation-layering reminders were added; lifecycle settlement procedure and repository-maintainer mechanics were not added.
- Package README: unchanged because supported commands, defaults, privacy boundary, and recovery guidance did not change.
- Production Python wrapper: unchanged because exit-code and single-consumption parity are enforced at the shared controller and existing wrapper regression passed.
- Lifecycle routing and review resolution: unchanged by implementation authority; workflow and rereview own those transitions.
