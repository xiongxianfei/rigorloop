# Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release

- Status: active
- Owner: maintainer
- Start date: 2026-05-13
- Last updated: 2026-05-13
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan sequences the implementation work for the `v0.1.2` public adapter archive-introduction release and records the later untracking gate.

The immediate release must publish downloadable adapter archives while keeping tracked `dist/adapters/**/skills` available for the stable compatibility window. The later untracking release can remove tracked generated adapter skill bodies only after one stable release has shipped archives and install docs.

## Source artifacts

- Proposal: `docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
- Spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Architecture: `docs/architecture/system/architecture.md`
- Related ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
- Change metadata: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
- Review log: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md`
- Proposal review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md`
- Spec review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md`
- Architecture review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md`
- Plan reviews: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r1.md`, `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md`
- Test spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md`

## Context and orientation

No `docs/project-map.md` exists in this checkout, so this plan uses direct source inspection and the approved artifacts above rather than project-map reliance.

Relevant implementation surfaces:

- `skills/` is the only authored skill source.
- `dist/adapters/manifest.yaml` is the adapter support matrix.
- `dist/adapters/README.md` is the repository-tree adapter install-contract surface.
- `dist/adapters/**/skills` remains tracked during `v0.1.2`.
- `scripts/build-adapters.py` currently generates tracked adapter output and must gain archive-output support if it does not already provide it.
- `scripts/validate-adapters.py` validates public adapter package structure and must validate generated archive output.
- `scripts/adapter_distribution.py` and `scripts/test-adapter-distribution.py` own most adapter and release-distribution checks.
- `scripts/validate-release.py` owns structured release validation and is delegated from `scripts/release-verify.sh`.
- `scripts/release-verify.sh <version>` is the maintainer-facing final release gate.
- `scripts/measure-skill-tokens.py`, `scripts/run-token-cost-benchmarks.py`, and `scripts/validate-token-cost-report.py` own token-cost evidence.
- `docs/reports/adapter-artifacts/releases/<version>.yaml` will be the tracked adapter artifact metadata surface.
- `docs/releases/<version>/release-notes.md` is the tracked release-notes surface.
- `docs/workflows.md` owns the project artifact-location map.
- `docs/changes/0001-skill-validator/` is a retained validator fixture and historical proof pack unless it can safely move to `docs/examples/changes/skill-validator/` in one slice.

Current known implementation shape before work begins:

- `v0.1.2` must introduce archives and keep repository-tree adapter installation available.
- The first untracking release is not part of the `v0.1.2` release-ready implementation unless a later plan revision makes it current after the stable compatibility release ships.
- The skill-validator proof pack move is conditional and cannot block archive publication.
- Public skill simplification is bounded to artifact-location lookup wording, portable defaults, and obsolete generated-output references.

## Non-goals

- Do not remove tracked generated public adapter skill bodies from `dist/adapters/**/skills` in `v0.1.2`.
- Do not shorten the compatibility window without an accepted policy exception.
- Do not remove support for Codex, Claude Code, or opencode.
- Do not commit generated archive files by default.
- Do not make `.codex/skills/` a public adapter install source.
- Do not require a combined all-adapters archive.
- Do not make the skill-validator proof pack move a release blocker.
- Do not perform broad progressive-loading optimization as release-critical work.
- Do not remove safety-critical review, verification, material-finding, security, or release guidance from public skills.
- Do not tag, publish, merge, or deploy as part of implementation milestones unless a later explicit release handoff authorizes it.

## Requirements covered

- R1-R6: M1, M3, M5 keep `v0.1.2` as the archive-introduction release with tracked adapter skills preserved.
- R7-R11: M6 records the later untracking gate after the stable archive release ships.
- R12-R22: M1 implements archive generation, archive names, install roots, and optional combined archive behavior.
- R23-R42: M2 implements and validates adapter artifact metadata and checksum behavior.
- R43-R51: M3 updates `dist/adapters/README.md` as the install-contract surface.
- R52-R63: M1, M2, M3, and M5 update release validation and final release-gate behavior; M6 records later untracking validation.
- R64-R69: M4 either moves the proof pack with references updated or records retained-fixture rationale.
- R70-R75: M3 and M4 update the artifact-location guide and bounded skill wording only where needed.
- R76-R81: M5 produces and validates `v0.1.2` token-cost evidence.
- R82-R85: M3 and M5 produce `v0.1.2` release notes for archive introduction and compatibility.
- R86-R87: M6 records later untracking release-note requirements.

## Current Handoff Summary

- Current milestone: M5. Produce token-cost and final release-readiness evidence
- Current milestone state: planned
- Last reviewed milestone: M4 code-review r1 found no material findings and closed M4.
- Review status: proposal-review, spec-review, architecture-review, and plan-review are approved; plan-review r1 finding PR-001 is closed in review-resolution; M1 code-review r1 found no material findings; M2 code-review r2 found no material findings after PAAM-M2-CR1 resolution; M3 code-review r1 found no material findings; M4 code-review r1 found no material findings.
- Remaining in-scope implementation milestones: M5
- Next stage: implement M5
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M5 is not implemented or reviewed, and final release validation has not run. M6 is a tracked later-release gate and is not part of `v0.1.2` implementation closeout until the stable archive release has shipped and a plan revision makes untracking current.

## Milestones

### M1. Generate adapter archives without removing tracked adapter skills

- Milestone state: closed
- Goal: Add deterministic per-adapter archive generation for `v0.1.2` while preserving tracked repository-tree adapter packages.
- Requirements: R1-R6, R12-R22, R52-R56, R59, R63
- Files/components likely touched:
  - `scripts/build-adapters.py`
  - `scripts/adapter_distribution.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - temporary release-output directory only for generated archives
- Dependencies:
  - Plan-review and test-spec complete.
  - Existing adapter manifest remains the supported-adapter source.
- Tests to add/update:
  - Archive generation creates `rigorloop-adapter-codex-v0.1.2.zip`, `rigorloop-adapter-claude-v0.1.2.zip`, and `rigorloop-adapter-opencode-v0.1.2.zip`.
  - Each archive contains the adapter's expected install root: `.agents/skills/`, `.claude/skills/`, or `.opencode/skills/`.
  - Archive generation does not delete or modify tracked `dist/adapters/**/skills`.
  - Combined archive behavior is optional and explicit.
- Implementation steps:
  - Add an output-dir archive mode if `build-adapters.py` does not already support it.
  - Generate archives from canonical skills and adapter templates, not by hand-editing generated output.
  - Keep normal tracked adapter drift checks intact.
  - Make archive generation deterministic enough for stable checksum validation.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>`
  - `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `git diff --check -- scripts/build-adapters.py scripts/adapter_distribution.py scripts/validate-adapters.py scripts/test-adapter-distribution.py`
- Expected observable result: Required per-adapter archives validate from generated release output, and tracked `dist/adapters/**/skills` remains present for the compatibility window.
- Commit message: `M1: generate public adapter release archives`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Archive mode could accidentally change tracked adapter output.
  - Zip timestamps or ordering could make checksums unstable.
- Rollback/recovery:
  - Revert archive mode and keep repository-tree adapter installation as the only public path until archive generation is ready.

### M2. Validate adapter artifact metadata and checksums

- Milestone state: closed
- Goal: Add tracked metadata for `v0.1.2` adapter archives and make release validation fail on missing, malformed, inconsistent, or checksum-mismatched evidence.
- Requirements: R23-R42, R52-R56, R59, R63
- Files/components likely touched:
  - `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`
  - `scripts/adapter_distribution.py`
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`
  - `scripts/test-adapter-distribution.py`
- Dependencies:
  - M1 archive generation produces the files metadata describes.
- Tests to add/update:
  - Required YAML fields are enforced for schema version 1.
  - Required adapters are exactly present unless support policy changes.
  - Non-pass artifact or validation results fail release validation.
  - SHA-256 mismatch fails validation.
  - `combined_artifact.required: false` permits omitting the combined archive.
- Implementation steps:
  - Implement a parser/validator for `docs/reports/adapter-artifacts/releases/<version>.yaml`.
  - Record source commit, generator command, source skills path, manifest path, artifacts, optional combined archive data, and validation result.
  - Wire structured metadata validation into `scripts/validate-release.py`.
  - Delegate metadata validation from `scripts/release-verify.sh`.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir> --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `git diff --check -- docs/reports/adapter-artifacts/releases/v0.1.2.yaml scripts/adapter_distribution.py scripts/validate-release.py scripts/release-verify.sh scripts/test-adapter-distribution.py`
- Expected observable result: Release validation accepts valid `v0.1.2` adapter artifact metadata and rejects missing archives, invalid results, and checksum mismatches.
- Commit message: `M2: validate adapter artifact release metadata`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - Metadata schema could drift from the approved spec.
  - Validation could require locally committed archives instead of release-output artifacts.
- Rollback/recovery:
  - Disable archive metadata validation only by reverting M2 and blocking `v0.1.2` publication; do not publish archives without checksum evidence.

### M3. Update install contract, release notes, and artifact-location guidance

- Milestone state: closed
- Goal: Make user-facing release and install docs describe the archive-introduction release, retained repository-tree compatibility path, metadata/checksum location, and artifact-location map.
- Requirements: R3-R6, R43-R51, R57, R60, R70-R75, R82-R85
- Files/components likely touched:
  - `dist/adapters/README.md`
  - `docs/releases/v0.1.2/release-notes.md`
  - `docs/releases/v0.1.2/release.yaml` if release metadata exists for this version
  - `docs/workflows.md`
  - selected `skills/*/SKILL.md` only for bounded artifact-location lookup wording or obsolete generated-output references
  - generated adapter output only if canonical skills change and the compatibility window requires refresh
- Dependencies:
  - M1 and M2 clarify archive names, metadata path, and validation commands.
- Tests to add/update:
  - README validation checks required install-contract content.
  - Release-note validation checks archive availability, retained compatibility path, checksum/metadata location, and release gate command.
  - Skill-surface tests or static assertions ensure `.codex/skills/` is not described as a public install source.
- Implementation steps:
  - Update `dist/adapters/README.md` with canonical source, support matrix, archive names, install roots, compatibility window, later untracking behavior, and checksum metadata location.
  - Add tracked `v0.1.2` release notes.
  - Add adapter artifact metadata location to `docs/workflows.md`.
  - Update only directly affected public skills for concise artifact-location lookup wording if stale duplicated path guidance is present.
  - Regenerate public adapters only if canonical skill text changes.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir> --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `git diff --check -- dist/adapters/README.md docs/releases/v0.1.2 docs/workflows.md skills scripts/test-adapter-distribution.py`
- Expected observable result: Users can see both `v0.1.2` install paths and the forward archive path, and contributor-facing artifact locations include adapter artifact metadata.
- Commit message: `M3: document adapter archive install contract`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
  - [x] code-review closed
- Risks:
  - Docs could imply generated skill bodies are already untracked in `v0.1.2`.
  - Skill simplification could grow beyond the release slice.
- Rollback/recovery:
  - Restore prior docs and block release publication until archive docs and release notes match the spec.
  - Split non-essential skill wording into a later plan if it becomes broad.

### M4. Settle skill-validator proof pack and bounded skill wording

- Milestone state: closed
- Goal: Either move the retained skill-validator proof pack safely into `docs/examples/` or record retained-fixture rationale, then finish any bounded artifact-location wording that did not belong in M3.
- Requirements: R64-R75
- Files/components likely touched:
  - `docs/changes/0001-skill-validator/`
  - `docs/examples/changes/skill-validator/`
  - `docs/examples/README.md`
  - `scripts/select-validation.py`
  - `scripts/validation_selection.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/test-skill-validator.py`
  - `docs/workflows.md`
  - selected `skills/*/SKILL.md`
- Dependencies:
  - M3 docs and artifact-location map changes should be known.
- Tests to add/update:
  - If moved, selector and lifecycle tests classify `docs/examples/changes/skill-validator/` as example or fixture content.
  - If retained, a tracked or review-visible rationale is present and does not block release validation.
  - Public skill wording keeps safety-critical review, verification, material-finding, security, and release guidance.
- Implementation steps:
  - Search references to `docs/changes/0001-skill-validator/`.
  - Move the proof pack only if all references, selectors, validators, docs, and tests can be updated in the same slice.
  - If unsafe, retain the old path and add explicit retained-fixture rationale with a follow-up.
  - Keep skill wording changes limited to lookup wording, portable defaults, and obsolete generated-output references.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path docs/examples/changes/skill-validator/change.yaml` if moved
  - `git diff --check -- docs/changes/0001-skill-validator docs/examples docs/workflows.md skills scripts`
- Expected observable result: The proof pack is either safely moved and reclassified as example content, or retained with rationale and no release blocker.
- Commit message: `M4: settle skill-validator example surface`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
  - [x] code-review closed
- Risks:
  - Hidden tests or validators may depend on the old fixture path.
  - Skill wording changes could remove behavior under the label of token reduction.
- Rollback/recovery:
  - Revert the proof-pack move and record retained-fixture rationale.
  - Restore any removed safety-critical skill text and split broader optimization into the existing progressive-loading track.

### M5. Produce token-cost and final release-readiness evidence

- Milestone state: planned
- Goal: Produce `v0.1.2` token-cost reports, run final release validation, and update lifecycle evidence for downstream explain-change, verify, PR, and release handoff.
- Requirements: R1-R6, R52-R60, R63, R76-R85
- Files/components likely touched:
  - `docs/reports/token-cost/releases/v0.1.2.md`
  - `docs/reports/token-cost/releases/v0.1.2.yaml`
  - `docs/releases/v0.1.2/release-notes.md`
  - `docs/releases/v0.1.2/release.yaml` if used
  - `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`
  - this plan file and `docs/plan.md`
  - change-local evidence under `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/`
- Dependencies:
  - M1-M4 closed or explicitly removed by plan revision.
  - Token-cost tooling can use public adapter release output or generated temporary public adapter output.
- Tests to add/update:
  - Token-cost report metadata validation for `v0.1.2`.
  - Release validation coverage for token-cost report, release notes, archives, metadata, canonical skills, and tracked adapters.
- Implementation steps:
  - Record baseline from `docs/reports/token-cost/releases/v0.1.1.md`.
  - Run static measurement against canonical `skills/`.
  - Run dynamic benchmarks against public adapter release output or generated temporary public adapter output, not `.codex/skills/`.
  - Create `v0.1.2` Markdown and YAML token-cost reports.
  - Run full release verification.
  - Update plan progress, validation notes, and change metadata.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>`
  - `python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2`
  - `python scripts/measure-skill-tokens.py`
  - `python scripts/run-token-cost-benchmarks.py --release v0.1.2 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`
  - `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.2.yaml`
  - `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir> --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `git diff --check --`
- Expected observable result: `v0.1.2` release readiness is locally proven with archive validation, adapter metadata checksums, token-cost evidence, release notes, canonical skill validation, and tracked adapter validation.
- Commit message: `M5: validate archive-introduction release evidence`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - Token-cost dynamic tooling may require environment support not present locally.
  - Full release verification may reveal stale generated adapter output.
- Rollback/recovery:
  - Use the existing token-cost waiver contract only if it applies and is recorded.
  - Regenerate tracked adapter output from canonical skills if drift is found.
  - Do not publish `v0.1.2` until full release validation passes or an approved release policy records a waiver.

### M6. Later untracking release gate

- Milestone state: lifecycle-closeout
- Goal: Keep the future untracking release visible without making it part of `v0.1.2` implementation closeout.
- Requirements: R7-R11, R61-R62, R86-R87
- Files/components likely touched:
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/**/skills`
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`
  - `docs/releases/<untracking-version>/release-notes.md`
  - a follow-up plan or plan revision after `v0.1.2` ships
- Dependencies:
  - A stable public release has shipped downloadable adapter archives and archive-install documentation.
- Tests to add/update:
  - Untracking release validation fails when generated public adapter skill bodies remain tracked.
  - Untracking release validation fails when `dist/adapters/README.md` or `dist/adapters/manifest.yaml` is missing.
  - Release notes identify release-archive installation as the active path.
- Implementation steps:
  - Do not start this milestone during `v0.1.2` implementation.
  - After `v0.1.2` is published, decide whether to revise this plan or create a follow-up untracking plan.
  - Remove tracked generated adapter skill bodies only in that later release slice.
- Validation commands:
  - `git ls-files 'dist/adapters/**/skills/**'`
  - `python scripts/validate-release.py --version <untracking-version>`
  - `bash scripts/release-verify.sh <untracking-version>`
  - `git diff --check -- dist/adapters scripts docs/releases`
- Expected observable result: The later release validates that generated public adapter skill bodies are no longer tracked while manifest and README remain tracked.
- Commit message: `M6: remove tracked generated adapter skill bodies`
- Milestone closeout:
  - [ ] stable archive release has shipped
  - [ ] follow-up plan or plan revision exists
  - [ ] validation passed
  - [ ] progress updated
  - [ ] validation notes updated
- Risks:
  - Removing tracked skill bodies before users have an archive-install migration path.
  - Treating `v0.1.2` readiness as permission to untrack generated skills immediately.
- Rollback/recovery:
  - Restore tracked generated adapter skill bodies if archive installation or metadata is not release-ready before the untracking release.

## Validation plan

Before implementation:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
- `git diff --check -- docs/plan.md docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`

During implementation, run each milestone's targeted commands before code-review handoff.

Before PR handoff, run the M5 final validation pack plus any commands added by the test spec, plan-review, code-review, or verify.

## Risks and recovery

- Risk: The implementation removes tracked adapter skill bodies in `v0.1.2`. Recovery: restore `dist/adapters/**/skills`, keep repository-tree install compatibility, and move untracking work to M6 after the stable archive release ships.
- Risk: Archive metadata validates files from a developer's private local path. Recovery: validate only generated release-output artifacts and tracked metadata, and block publication when ordinary maintainers cannot reproduce the evidence.
- Risk: Adapter archive generation is not deterministic enough for checksum validation. Recovery: normalize archive file order and timestamps or block release until deterministic generation is solved.
- Risk: Skill-validator fixture movement breaks selectors or validators. Recovery: revert the move, retain the fixture at `docs/changes/0001-skill-validator/`, record rationale, and schedule a follow-up.
- Risk: Skill simplification removes safety-critical guidance. Recovery: restore the guidance and split broader token optimization into a separate reviewed slice.
- Risk: Token-cost benchmark tooling is unavailable. Recovery: use the existing token-cost waiver contract only if it applies and is recorded; otherwise block publication.

## Dependencies

- Plan-review must approve this plan before test-spec and implementation.
- Test-spec must map spec requirements and edge cases to concrete tests before implementation.
- M1 archive output is the input for M2 metadata and M5 release validation.
- M2 metadata validation must be in place before release notes claim checksums are recorded.
- M3 install docs and release notes depend on archive naming and metadata path decisions from M1-M2.
- M4 is conditional and must not block archive publication when it cannot be completed safely.
- M5 depends on all current `v0.1.2` implementation milestones being closed or explicitly removed by plan revision.
- M6 depends on the true downstream event of a stable archive-introduction release being published.
- Final GitHub release publication and artifact attachment are outside normal implementation commits and require explicit release handoff.

## Progress

- [x] 2026-05-13: Proposal accepted, spec approved, canonical architecture updated, and architecture-review approved.
- [x] 2026-05-13: Execution plan created and added to `docs/plan.md`.
- [x] Plan-review completed.
- [x] Test-spec created.
- [x] M1 implemented and handed to code-review.
- [x] M1 code-review completed with no material findings.
- [x] M2 implemented and reviewed once.
- [x] M2 review-resolution completed and returned to code-review.
- [x] M2 rerun code-review closed.
- [x] M3 implemented and handed to code-review.
- [x] M3 code-review closed.
- [x] M4 implemented and handed to code-review.
- [x] M4 code-review closed.
- [ ] M5 final release-readiness evidence completed and reviewed.
- [ ] Final explain-change, verify, and PR handoff completed.
- [ ] `v0.1.2` release publication handoff completed or explicitly deferred.
- [ ] M6 follow-up untracking plan or plan revision created after `v0.1.2` ships.

## Decision log

- 2026-05-13: Keep `v0.1.2` focused on archive introduction and compatibility; do not untrack generated public adapter skill bodies until a later release.
- 2026-05-13: Use five current implementation milestones for archive generation, metadata validation, docs/release guidance, conditional example/skill cleanup, and final release evidence.
- 2026-05-13: Track the later untracking release as M6 with an external dependency instead of hiding it inside `v0.1.2` readiness.
- 2026-05-13: Treat per-adapter archives as required and the combined archive as optional unless later planning changes the release contract.
- 2026-05-13: Use direct source inspection because `docs/project-map.md` is absent.
- 2026-05-13: Resolve plan-review PR-001 by using the existing token benchmark runner shape with `--release`, explicit suite/tool/output arguments, and a public adapter skill source rather than `.codex/skills/`.
- 2026-05-13: Test spec created as the active proof-planning surface; proceed to implement M1.
- 2026-05-13: During M1, keep tracked `dist/adapters` at the current `0.1.1` compatibility version and validate it with `build-adapters.py --version 0.1.1 --check`; archive generation uses `v0.1.2` release output without mutating tracked adapter packages.
- 2026-05-13: M1 implements per-adapter release archives only; adapter artifact metadata and final `v0.1.2` release validation remain M2 and M5 work.
- 2026-05-13: Code-review M1 R1 found no material findings and closed M1; proceed to M2 metadata and checksum validation.
- 2026-05-13: M2 treats `v0.1.2` as an archive-introduction release while keeping the tracked repository-tree adapter compatibility matrix at `0.1.1`; release validation checks generated `v0.1.2` archives through `--release-output-dir`.
- 2026-05-13: M2 added minimal `v0.1.2` release metadata and notes so the adapter artifact metadata gate can run end to end. M3 remains responsible for refining install-contract documentation and release-note wording.
- 2026-05-13: Code-review M2 R1 found PAAM-M2-CR1: source-commit mismatch is accepted instead of rejected. M2 is in review-resolution before rerun code-review.
- 2026-05-13: Resolved PAAM-M2-CR1 by validating `release.source_commit` against the release/source commit input. For `v0.1.2`, the approved policy exception is that metadata names the archive source commit `5514ef14ce5f310787f464ea78bd777838cb5537`; validation commands must pass that commit explicitly when validating the tracked metadata and generated archives.
- 2026-05-13: Code-review M2 R2 found no material findings and closed M2. Proceed to M3 install contract, release notes, and artifact-location guidance.
- 2026-05-13: M3 did not change canonical skill text, so generated adapter output was not refreshed. Tracked adapter compatibility validation remains on manifest version `0.1.1`; `v0.1.2` is validated through generated release archive output and release metadata.
- 2026-05-13: Code-review M3 R1 found no material findings and closed M3. Proceed to M4 skill-validator proof-pack settlement and bounded skill wording.
- 2026-05-13: M4 retained `docs/changes/0001-skill-validator/` rather than moving it. The reference inventory found active README, workflow, selector, lifecycle, change-metadata, test, and historical references to the old path; retaining it with explicit v0.1.2 release non-blocking rationale is the scope-complete path for this release slice.
- 2026-05-13: M4 did not change canonical skill text because existing public skills already carry the bounded artifact-location lookup wording and safety-critical guidance validated by `scripts/test-skill-validator.py`; generated adapter output was not refreshed.
- 2026-05-13: Code-review M4 R1 found no material findings and closed M4. Proceed to M5 token-cost and final release-readiness evidence.

## Surprises and discoveries

- `docs/project-map.md` is absent, so no project-map context was used.
- M1 validation showed that refreshing tracked `dist/adapters` to `0.1.2` during archive generation breaks historical `v0.1.1` repository-artifact validation. M1 now validates archive release output for `v0.1.2` while proving tracked adapter output remains at the current `0.1.1` compatibility version.

## Validation notes

- Plan creation validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`

- Test-spec creation validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-resolution.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md`
  - `git diff --check -- specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md docs/plan.md docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`

- M1 targeted validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_adapter_archives_install_under_target_project_roots AdapterDistributionTests.test_validate_adapter_archives_rejects_missing_required_archive AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir"; python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.2`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `git diff --check -- scripts/build-adapters.py scripts/adapter_distribution.py scripts/validate-adapters.py scripts/test-adapter-distribution.py`
  - `git ls-files 'dist/adapters/**/skills/**' | wc -l` returned `69`.
  - `git ls-files '*.zip' '*.tar.gz' | rg 'rigorloop-adapter|rigorloop-adapters' || true` returned no tracked adapter archives.

- M1 code-review validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_adapter_archives_install_under_target_project_roots AdapterDistributionTests.test_validate_adapter_archives_rejects_missing_required_archive AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir"; python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.2`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `git show --check HEAD -- scripts/adapter_distribution.py scripts/build-adapters.py scripts/validate-adapters.py scripts/test-adapter-distribution.py`
  - `git ls-files 'dist/adapters/**/skills/**' | wc -l` returned `69`.
  - `git ls-files '*.zip' '*.tar.gz' | rg 'rigorloop-adapter|rigorloop-adapters' || true` returned no tracked adapter archives.
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-resolution.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m1-r1.md`
  - `git diff --check -- docs/plan.md docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`

- M2 targeted validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined AdapterDistributionTests.test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_release_verify_script_supports_v0_1_2_archive_metadata_gate`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir"; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `git diff --check -- docs/reports/adapter-artifacts/releases/v0.1.2.yaml docs/releases/v0.1.2 scripts/adapter_distribution.py scripts/validate-release.py scripts/release-verify.sh scripts/test-adapter-distribution.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-resolution.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m1-r1.md`
  - `git diff --check --`

- M2 code-review r1 validation evidence:
  - `git show --stat --oneline --decorate --name-only HEAD`
  - `git show -- scripts/adapter_distribution.py scripts/validate-release.py scripts/release-verify.sh scripts/test-adapter-distribution.py docs/reports/adapter-artifacts/releases/v0.1.2.yaml docs/releases/v0.1.2/release.yaml docs/releases/v0.1.2/release-notes.md`
  - `git rev-parse HEAD` returned `a4efaca61f7c84a8f1fc7c2976bf7428a07e7d53`.
  - `docs/reports/adapter-artifacts/releases/v0.1.2.yaml` records `source_commit: 5514ef14ce5f310787f464ea78bd777838cb5537`.
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir"` passed despite the source-commit mismatch.

- M2 review-resolution validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_artifact_metadata_validation_accepts_schema_and_optional_combined AdapterDistributionTests.test_adapter_artifact_metadata_validation_rejects_bad_results_checksums_and_source_commit_mismatch AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata AdapterDistributionTests.test_validate_release_cli_passes_changed_surface_inputs AdapterDistributionTests.test_release_verify_script_supports_v0_1_2_archive_metadata_gate` first failed before CLI and release-gate plumbing, then passed after the fix.
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` failed with `release.source_commit mismatch`.
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.md --path specs/public-adapter-artifact-migration-examples-concise-skill-release.test.md --path docs/architecture/system/architecture.md --path docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md --path docs/plan.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-log.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/review-resolution.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/plan-review-r2.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m1-r1.md --path docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m2-r1.md`
  - `git diff --check --`

- M2 code-review r2 found no material findings and closed M2. Review record: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m2-r2.md`.

- M3 targeted validation passed:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_2_release_notes_document_archive_introduction_contract AdapterDistributionTests.test_v0_1_2_release_validation_rejects_notes_without_archives_or_compatibility AdapterDistributionTests.test_workflows_records_adapter_artifact_metadata_location AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata` failed before the M3 docs and validation updates, then passed after the fix.
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output RELEASE_COMMIT=5514ef14ce5f310787f464ea78bd777838cb5537 bash scripts/release-verify.sh v0.1.2`
  - `git diff --check -- dist/adapters/README.md docs/releases/v0.1.2 docs/workflows.md scripts/adapter_distribution.py scripts/test-adapter-distribution.py`

- M3 code-review r1 found no material findings and closed M3. Review evidence:
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_2_release_notes_document_archive_introduction_contract AdapterDistributionTests.test_v0_1_2_release_validation_rejects_notes_without_archives_or_compatibility AdapterDistributionTests.test_workflows_records_adapter_artifact_metadata_location AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - Review record: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m3-r1.md`

- M4 retained-fixture validation passed:
  - `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_project_artifact_location_m1_retained_fixture_has_durable_rationale` failed after adding the M4 rationale assertions and before updating the fixture README, then passed after the README update.
  - `python scripts/test-artifact-lifecycle-validator.py ArtifactLifecycleValidatorFixtureTests.test_retained_skill_validator_fixture_readme_documents_non_active_status` failed after adding the v0.1.2 non-blocking assertion and before updating the fixture README, then passed after the README update.
  - `python scripts/test-select-validation.py ValidationSelectionTests.test_retained_skill_validator_fixture_rationale_has_deterministic_routing`
  - `python scripts/test-select-validation.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/select-validation.py --mode explicit --path docs/changes/0001-skill-validator/README.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/0001-skill-validator/README.md`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - `git diff --check -- docs/changes/0001-skill-validator docs/examples docs/workflows.md skills scripts`

- M4 code-review r1 found no material findings and closed M4. Review evidence:
  - `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_project_artifact_location_m1_retained_fixture_has_durable_rationale`
  - `python scripts/test-artifact-lifecycle-validator.py ArtifactLifecycleValidatorFixtureTests.test_retained_skill_validator_fixture_readme_documents_non_active_status`
  - `python scripts/test-select-validation.py ValidationSelectionTests.test_retained_skill_validator_fixture_rationale_has_deterministic_routing`
  - `tmpdir=$(mktemp -d); python scripts/build-adapters.py --version v0.1.2 --output-dir "$tmpdir" >/dev/null; python scripts/validate-release.py --version v0.1.2 --release-output-dir "$tmpdir" --release-commit 5514ef14ce5f310787f464ea78bd777838cb5537`
  - Review record: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/code-review-m4-r1.md`

## Outcome and retrospective

Not completed. M4 is closed after clean code-review; M5 remains open.

## Readiness

See `Current Handoff Summary`.

## Remaining completion gates

- M1-M5 implementation, targeted validation, and code-review loops.
- Required review-resolution if code-review records material findings.
- Explain-change, verify, and PR handoff.
- Explicit release handoff for publishing `v0.1.2` and attaching archives.
- Later M6 follow-up after the stable archive release ships.
