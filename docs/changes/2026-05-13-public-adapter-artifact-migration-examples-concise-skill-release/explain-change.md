# Explain Change: Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release

## Summary

This change prepares `v0.1.2` as the public adapter archive-introduction release without removing the existing repository-tree adapter install path. It adds deterministic per-adapter release archives, validates adapter artifact metadata and checksums, documents the archive install contract, keeps the retained skill-validator proof pack with explicit rationale, records `v0.1.2` token-cost evidence, and proves local release readiness.

The implementation deliberately does not untrack `dist/adapters/**/skills` in `v0.1.2`. That removal remains a later release gate after at least one stable public release has shipped downloadable adapter archives and install guidance.

## Problem

`v0.1.1` kept `dist/adapters/` as the public adapter install path and did not ship downloadable adapter archives. The accepted source-boundary direction wants generated adapter skill bodies to move out of tracked source, but only after users have a stable overlap period where the new release-archive install path exists. The release also needed clearer adapter artifact evidence, release notes, token-cost evidence, and a decision on the active-looking skill-validator proof pack.

## Decision Trail

| Decision source | Decision | Impact on diff |
| --- | --- | --- |
| Proposal | Choose the staged compatibility path: publish archives first, remove tracked adapter skill bodies later. | M1-M3 add archive generation, metadata, and docs while preserving tracked `dist/adapters/**/skills`. |
| Spec `R1`-`R6` | Treat `v0.1.2` as archive-introduction and keep repository-tree adapter install compatibility. | `build-adapters.py --version 0.1.1 --check` remains part of validation; no tracked adapter skill bodies are removed. |
| Spec `R52`-`R60`, `R63` | Release gate validates canonical skills, tracked adapters, archives, metadata, token-cost report, notes, and missing archive failures. | `validate-release.py`, `release-verify.sh`, adapter distribution helpers, and tests were extended. |
| Spec `R64`-`R69` | Move the skill-validator proof pack only if safe; otherwise retain with rationale. | `docs/changes/0001-skill-validator/README.md` records retained-fixture and release non-blocking rationale. |
| Spec `R70`-`R75` | Keep `docs/workflows.md` as artifact-location guide; avoid broad skill rewrite. | `docs/workflows.md` records adapter artifact metadata location; canonical skill text was not changed in M3/M4. |
| Spec `R76`-`R81` | Produce token-cost Markdown/YAML reports using canonical `skills/` statically and public adapter output dynamically. | `docs/reports/token-cost/releases/v0.1.2.*` and sanitized run summaries were added. |
| Spec `R82`-`R85` | Release notes must name archives, retained compatibility, metadata/checksum location, and release gate. | `docs/releases/v0.1.2/release-notes.md` and release metadata were added. |
| Architecture | `skills/` is the only authored skill source; public adapter skill copies remain generated output through the compatibility window; release archives are release assets, not committed files. | Archive output is generated into temporary/release output and not tracked. |
| Plan | M1-M5 implement archive generation, metadata validation, install docs, fixture settlement, and final evidence; M6 is later untracking. | Lifecycle state keeps `v0.1.2` release-ready work separate from the later untracking gate. |

## Diff Rationale by Area

| Area | Files | Why changed | Requirements / plan | Test or evidence |
| --- | --- | --- | --- | --- |
| Lifecycle artifacts | `docs/proposals/...`, `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`, `.test.md`, `docs/architecture/system/architecture.md`, `docs/plans/...`, `docs/plan.md`, `docs/changes/.../change.yaml` | Record the accepted staged release direction, requirements, test mapping, architecture constraints, milestone state, validation evidence, and handoffs. | Proposal, spec `R1`-`R85`, plan M1-M5 | Lifecycle and change metadata validators passed throughout the milestones. |
| Adapter archive generation | `scripts/build-adapters.py`, `scripts/adapter_distribution.py`, `scripts/validate-adapters.py` | Add archive output mode for per-adapter `v0.1.2` archives and validate archive roots without mutating tracked `dist/adapters/` compatibility output. | M1, `R12`-`R22`, `R52`-`R56`, `R59` | Archive generation and `validate-adapters.py --root <release-output-dir> --version v0.1.2` passed. |
| Release metadata and validation | `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, `docs/releases/v0.1.2/release.yaml`, `scripts/validate-release.py`, `scripts/release-verify.sh`, `scripts/adapter_distribution.py` | Record archive checksums, source commit, generator command, validation command, and wire validation into the maintainer release gate. | M2, `R23`-`R42`, `R52`-`R60`, `R63` | `validate-release.py --release-commit 5514ef...` passed; mismatch test for source commit fails as expected. |
| Source-commit review fix | `scripts/validate-release.py`, `scripts/release-verify.sh`, `scripts/test-adapter-distribution.py`, `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, `review-resolution.md` | Resolve code-review finding `PAAM-M2-CR1` by directly validating `release.source_commit` against the release commit input and recording the approved pre-metadata archive-source exception. | M2 review-resolution | `test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch`; negative CLI mismatch proof. |
| Install contract and release notes | `dist/adapters/README.md`, `docs/releases/v0.1.2/release-notes.md`, `docs/workflows.md` | Tell users where archives live, keep `dist/adapters/<adapter>/` as the compatibility path, identify checksums/metadata, and add adapter artifact metadata to the artifact-location map. | M3, `R43`-`R51`, `R57`, `R60`, `R70`-`R75`, `R82`-`R85` | Adapter distribution tests check README, release notes, workflow artifact map, and release-note failure cases. |
| Skill-validator proof pack | `docs/changes/0001-skill-validator/README.md`, `scripts/test-skill-validator.py`, `scripts/test-artifact-lifecycle-validator.py` | Retain the proof pack at the old path because reference inventory showed moving it safely was larger than the release slice; record that retention is non-active lifecycle state and non-blocking for `v0.1.2`. | M4, `R64`-`R69` | Focused fixture rationale tests and selector/lifecycle tests passed. |
| Token-cost evidence | `docs/reports/token-cost/releases/v0.1.2.md`, `docs/reports/token-cost/releases/v0.1.2.yaml`, `docs/reports/token-cost/runs/v0.1.2/*.analysis.yaml` | Record static and dynamic token evidence for `v0.1.2`, with static measurement from canonical `skills/` and dynamic benchmark source from public Codex adapter output rather than `.codex/skills/`. | M5, `R76`-`R81` | `validate-token-cost-report.py`, token-cost tests, and full `release-verify.sh v0.1.2` passed. |
| Review evidence | `docs/changes/.../reviews/*.md`, `review-log.md`, `review-resolution.md` | Record formal reviews, the M2 material finding and resolution, and clean reviews for M1-M5. | Formal review recording rules; plan review and code-review stages | `validate-review-artifacts.py --mode closeout` passed with 11 reviews, 2 findings, and 2 resolution entries. |

## Tests Added or Changed

| Test surface | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `scripts/test-adapter-distribution.py` | Archive creation, archive install roots, archive validation, metadata schema, checksum validation, source-commit mismatch rejection, release notes, README contract, workflow artifact map, and release gate behavior. | Adapter packaging and release validation are repository-owned distribution contracts, so script-level regression coverage is the right level. |
| `scripts/test-skill-validator.py` | Retained skill-validator fixture rationale includes durable release non-blocking wording. | The proof pack is a static/documentation fixture; direct static assertions catch accidental rationale removal. |
| `scripts/test-artifact-lifecycle-validator.py` | Retained fixture README is documented as non-active lifecycle state and does not break lifecycle classification. | Lifecycle routing is the risk; validator regression coverage is targeted. |
| `scripts/test-token-cost-report-validation.py` | Token-cost metadata rules reject invalid sources such as `.codex/skills/`, enforce result-quality evidence, and validate final report shape. | Token-cost evidence is structured YAML, so schema/semantic validation tests are sufficient. |
| `scripts/test-token-cost-measurement.py` | Static and dynamic measurement tooling behavior remains valid. | Measurement correctness is owned by the benchmark tooling. |

## Validation Evidence Before Final Verify

Milestone validation recorded in the active plan includes:

- `python scripts/test-adapter-distribution.py` passed 88 tests.
- `python scripts/test-skill-validator.py` passed 73 tests.
- `python scripts/test-artifact-lifecycle-validator.py` passed 51 tests.
- `python scripts/test-select-validation.py` passed 59 tests.
- `python scripts/test-token-cost-report-validation.py` passed 16 tests.
- `python scripts/test-token-cost-measurement.py` passed 24 tests.
- `python scripts/validate-skills.py` passed for 23 skill files.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>` and `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2` passed.
- `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir> --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537` passed.
- `RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2` passed.
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.2.yaml` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release` passed after M5 code-review recording.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the governing artifacts, review records, retained fixture README, and token-cost reports.
- `git diff --check --` passed.

No hosted CI result is claimed here.

## Review Resolution Summary

Formal review evidence is recorded under `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/` and indexed by `review-log.md`.

Material findings:

- `PR-001`: accepted and resolved by updating M5 to use the existing token benchmark runner shape with `--release`, explicit suite/tool/output arguments, and a public adapter skill source.
- `PAAM-M2-CR1`: accepted and resolved by validating `release.source_commit` against the release commit input, adding a negative source-commit mismatch regression test, and recording the approved `v0.1.2` archive-source policy exception.

`review-resolution.md` has `Closeout status: closed`; no `needs-decision` item remains open. Code-review rounds M1, M2 rerun, M3, M4, and M5 closed with no material findings after the M2 resolution.

## Alternatives Rejected

- Remove tracked `dist/adapters/**/skills` in `v0.1.2`: rejected because it would skip the stable compatibility window after `v0.1.1`.
- Publish archives without metadata/checksum validation: rejected because release artifacts need reproducible evidence.
- Move `docs/changes/0001-skill-validator/` during M4: rejected for this release slice because active references and validators still rely on the old path.
- Broadly rewrite public skills for token reduction: rejected as out of scope for the archive-introduction release; token-cost warnings remain follow-up signals.
- Commit generated archive files: rejected because archives are release assets; tracked metadata and checksums are the repository evidence.

## Scope Control

The change preserves workflow stage order, keeps Codex, Claude Code, and opencode support, avoids hand-editing generated adapter output, avoids changing canonical skill behavior for token reduction, and does not claim final release publication. It keeps `.codex/skills/` as local runtime state and does not use it as release evidence.

## Risks and Follow-Ups

- `v0.1.2` still needs final `verify`, PR handoff, and explicit release-publication handoff before release publication.
- M6 remains a later untracking gate after the stable archive-introduction release ships.
- Token-cost warnings remain for `workflow` and `code-review`; they should be addressed only through a separately reviewed skill-surface optimization slice.
- The retained skill-validator proof pack should move to `docs/examples/changes/skill-validator/` only when references, selectors, validators, docs, and tests can be updated safely in one follow-up slice.

## Readiness

This explanation completes the durable rationale stage for the reviewed M1-M5 implementation. The next workflow stage is `verify`; this artifact does not claim final verification, PR readiness, hosted CI status, or release publication.
