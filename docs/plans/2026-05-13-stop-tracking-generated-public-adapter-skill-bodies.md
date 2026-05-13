# Stop tracking generated public adapter skill bodies for v0.1.3

- Status: active
- Owner: maintainer
- Start date: 2026-05-13
- Last updated: 2026-05-13
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

This plan turns the approved `v0.1.3` adapter untracking contract into reviewable implementation slices.

The release completes the compatibility-window migration started by `v0.1.2`: generated public adapter package bodies leave tracked Git state, release archives become the active public install surface, `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain the tracked support surface, and validation proves generated adapter output from temporary or release-output directories.

Readiness is not Done. This plan remains active until implementation, milestone reviews, explain-change, verify, PR handoff, and the release publication handoff are complete.

## Source artifacts

- Proposal: [2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md](../proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md)
- Spec: [stop-tracking-generated-public-adapter-skill-bodies.md](../../specs/stop-tracking-generated-public-adapter-skill-bodies.md)
- Architecture: [architecture.md](../architecture/system/architecture.md)
- ADR: [ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md](../adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md)
- Test spec: [stop-tracking-generated-public-adapter-skill-bodies.test.md](../../specs/stop-tracking-generated-public-adapter-skill-bodies.test.md)
- Change metadata: [change.yaml](../changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml)
- Review evidence:
  - proposal-review: [proposal-review-r2.md](../changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/proposal-review-r2.md)
  - spec-review: [spec-review-r2.md](../changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/spec-review-r2.md)
  - architecture-review: [architecture-review-r1.md](../changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/architecture-review-r1.md)

## Context and orientation

Primary implementation surfaces:

- `dist/adapters/README.md`
- `dist/adapters/manifest.yaml`
- `dist/adapters/codex/`
- `dist/adapters/claude/`
- `dist/adapters/opencode/`
- `scripts/build-adapters.py`
- `scripts/adapter_distribution.py`
- `scripts/validate-adapters.py`
- `scripts/validate-release.py`
- `scripts/release-verify.sh`
- `scripts/run-token-cost-benchmarks.py`
- `scripts/validate-token-cost-report.py`
- `scripts/test-adapter-distribution.py`
- `scripts/test-token-cost-report-validation.py`
- `scripts/test-select-validation.py`
- `scripts/test-skill-validator.py`
- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/workflows.md`
- `docs/releases/v0.1.3/release.yaml`
- `docs/releases/v0.1.3/release-notes.md`
- `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`
- `docs/reports/token-cost/releases/v0.1.3.md`
- `docs/reports/token-cost/releases/v0.1.3.yaml`
- `docs/reports/token-cost/runs/v0.1.3/`

Current script interfaces to preserve or use:

```bash
python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>
python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3
python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <commit>
python scripts/run-token-cost-benchmarks.py --release v0.1.3 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>
bash scripts/release-verify.sh v0.1.3
```

The token-cost `--skill-source` value must point to generated public adapter release output or temporary public adapter output, not `.codex/skills/`.

## Non-goals

- Do not remove support for Codex, Claude Code, or opencode.
- Do not change workflow stage order.
- Do not move `docs/changes/0001-skill-validator/`.
- Do not optimize high-cost public skills.
- Do not add new token-cost threshold gates.
- Do not change public skill behavior beyond removing obsolete generated-output or install-path references.
- Do not rewrite Git history.
- Do not commit generated adapter archives.
- Do not make `.codex/skills/` a public install source.
- Do not retain partial tracked adapter packages under `dist/adapters/` after the migration.

## Requirements covered

- Release phase/source ownership: R0-R7.
- Tracked/untracked adapter surfaces: R8-R15d.
- Public install contract: R16-R25.
- Root guidance alignment: R26-R32.
- Adapter generation and validation: R33-R41g.
- Adapter artifact metadata and release evidence: R42-R51.
- Token-cost evidence: R52-R57.
- Deferred scope: R58-R61.
- Test-spec coverage: R62-R68.

## Current Handoff Summary

- Current milestone: M1. Validation model migration and regression tests
- Current milestone state: review-requested
- Last reviewed milestone: none
- Review status: M1 implementation complete; awaiting code-review
- Remaining in-scope implementation milestones: M1 review closeout, M2, M3, M4
- Next stage: code-review M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: M1 is implemented but not reviewed, M2-M4 are not implemented, release validation has not run against final release evidence, explain-change and verify are missing, and PR/release handoff is not prepared.

## Milestones

### M1. Validation model migration and regression tests

- Milestone state: review-requested
- Goal: Make adapter and release validation use generated temporary or release-output adapter packages instead of tracked `dist/adapters/<adapter>/` package trees.
- Requirements: R33-R41g, R62-R68.
- Files/components likely touched:
  - `scripts/build-adapters.py`
  - `scripts/adapter_distribution.py`
  - `scripts/validate-adapters.py`
  - `scripts/validate-release.py`
  - `scripts/release-verify.sh`
  - `scripts/test-adapter-distribution.py`
  - `scripts/test-select-validation.py`
  - `specs/stop-tracking-generated-public-adapter-skill-bodies.test.md`
- Dependencies: approved plan-review and active test spec.
- Tests to add/update:
  - positive tests proving generated temporary output validates without tracked `dist/adapters/**/skills`;
  - negative tests proving release validation fails if it still requires tracked adapter skill bodies;
  - negative tests proving tracked generated adapter skill bodies are rejected for `v0.1.3`;
  - tests proving release validation still requires generated adapter output, archive structure, metadata, checksums, and release proof.
- Implementation steps:
  1. Add or update tests first for the new validation target and tracked-body rejection.
  2. Update adapter validation to validate `--root <release-output-dir>` output for all adapters.
  3. Update release validation and release verify so `v0.1.3` release readiness depends on generated output and archives, not tracked package trees.
  4. Retire or version-gate tracked-output drift checks for `v0.1.3` and later.
- Validation commands:
  ```bash
  python scripts/test-adapter-distribution.py
  python scripts/validate-skills.py
  python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>
  python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3
  python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <commit>
  ```
- Expected observable result: validation passes against generated output and fails when `v0.1.3` relies on tracked generated adapter package trees.
- Commit message: `M1: validate adapters from generated release output`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: validation may have implicit assumptions that `dist/adapters/<adapter>/` exists.
- Rollback/recovery: keep tracked adapter output until validation is migrated; if migration cannot be completed, stop before M2 and revise the spec or plan.
- Implementation result: `v0.1.3` release validation now supports the release-output/archive validation model, requires only the tracked adapter support surface under `dist/adapters/`, rejects tracked adapter package fragments for `v0.1.3`, and keeps archive/metadata validation required for the release.

### M2. Repository tree untracking and guidance alignment

- Milestone state: planned
- Goal: Remove tracked generated adapter package fragments and align root/install guidance with the archive-install model.
- Requirements: R8-R32, R58-R61.
- Files/components likely touched:
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - `dist/adapters/codex/`
  - `dist/adapters/claude/`
  - `dist/adapters/opencode/`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
- Dependencies: M1 validation path available.
- Tests to add/update:
  - tracked-path absence check for `dist/adapters/**/skills`;
  - check that only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked under `dist/adapters/`;
  - root-guidance audit check or release-validation coverage for stale active install wording.
- Implementation steps:
  1. Remove tracked generated adapter skill bodies, generated adapter instruction entrypoints, and generated opencode command wrappers from `dist/adapters/`.
  2. Keep `dist/adapters/README.md` and `dist/adapters/manifest.yaml`.
  3. Update `dist/adapters/README.md` as the install-contract surface with archive names/patterns, install roots, support matrix, and metadata/checksum location.
  4. Update `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` or record explicit unaffected rationale if any listed surface is already compatible.
  5. Ensure historical `v0.1.2` compatibility wording is version-qualified.
- Validation commands:
  ```bash
  git ls-files 'dist/adapters/**/skills/**'
  git ls-files 'dist/adapters/**'
  python scripts/select-validation.py --mode explicit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path dist/adapters/README.md --path dist/adapters/manifest.yaml
  python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <commit>
  ```
- Expected observable result: no generated adapter package fragments are tracked, active guidance points to release archives or `dist/adapters/README.md`, and `dist/adapters/` has only approved tracked support files.
- Commit message: `M2: retire tracked adapter package fragments`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: root guidance could keep stale compatibility-window text that looks active.
- Rollback/recovery: restore generated adapter output from canonical `skills/` and stop release preparation if guidance or validation cannot be aligned.

### M3. v0.1.3 release evidence and token-cost reports

- Milestone state: planned
- Goal: Produce `v0.1.3` release evidence for adapter archives, metadata/checksums, release notes, and token-cost reports using generated public adapter output.
- Requirements: R42-R57.
- Files/components likely touched:
  - `docs/releases/v0.1.3/release.yaml`
  - `docs/releases/v0.1.3/release-notes.md`
  - `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`
  - `docs/reports/token-cost/releases/v0.1.3.md`
  - `docs/reports/token-cost/releases/v0.1.3.yaml`
  - `docs/reports/token-cost/runs/v0.1.3/`
  - `scripts/validate-token-cost-report.py`
  - `scripts/test-token-cost-report-validation.py`
- Dependencies: M1 generated-output validation and M2 install guidance.
- Tests to add/update:
  - source-commit match validation for `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`;
  - checksum validation against generated or published archives;
  - token-cost source validation that rejects `.codex/skills/`;
  - release notes validation that records archive install path and retired repository-tree skill-body path.
- Implementation steps:
  1. Generate adapter release output for `v0.1.3`.
  2. Record adapter metadata and SHA-256 checksums.
  3. Create `v0.1.3` release metadata and release notes.
  4. Run static skill token measurement from `skills/`.
  5. Run or dry-run the dynamic token-cost benchmark suite using generated public adapter output or release archive output as `--skill-source`.
  6. Write token-cost Markdown and YAML release evidence.
- Validation commands:
  ```bash
  python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>
  python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3
  python scripts/measure-skill-tokens.py
  python scripts/run-token-cost-benchmarks.py --release v0.1.3 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>
  python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.3.yaml
  python scripts/validate-release.py --version v0.1.3 --release-output-dir <release-output-dir> --release-commit <commit>
  ```
- Expected observable result: `v0.1.3` release evidence exists and validates without referencing `.codex/skills/` as the public adapter source.
- Commit message: `M3: add v0.1.3 release evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: dynamic benchmark execution may be blocked by local tool availability.
- Rollback/recovery: use the existing token-cost waiver or exception process only if approved; otherwise stop release readiness until benchmark evidence is available.

### M4. Release verification and lifecycle closeout

- Milestone state: planned
- Goal: Prove the full `v0.1.3` release gate locally and prepare downstream closeout without claiming publication prematurely.
- Requirements: all acceptance criteria, especially R50-R51.
- Files/components likely touched:
  - `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/explain-change.md`
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/verify-report.md`
- Dependencies: M1-M3 closed or removed by approved plan revision.
- Tests to add/update:
  - no new implementation tests expected unless final release verification exposes a coverage gap.
- Implementation steps:
  1. Run targeted release verification.
  2. Run selected or broad repository validation required by the test spec and active plan.
  3. Record explain-change evidence.
  4. Run verify and update verify evidence.
  5. Prepare PR handoff.
  6. After PR readiness and publication authorization, route to the release stage for tag/publication and archive upload.
- Validation commands:
  ```bash
  bash scripts/release-verify.sh v0.1.3
  python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies
  python scripts/validate-change-metadata.py docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml
  python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md --path specs/stop-tracking-generated-public-adapter-skill-bodies.md --path specs/stop-tracking-generated-public-adapter-skill-bodies.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md --path docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md
  git diff --check --
  ```
- Expected observable result: `bash scripts/release-verify.sh v0.1.3` passes, lifecycle artifacts are synchronized, and the branch is ready for explain-change, verify, PR, and release publication handoff.
- Commit message: `M4: verify v0.1.3 release readiness`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: release verification may expose stale validation assumptions or missing release artifacts.
- Rollback/recovery: keep the plan active, restore tracked adapter output if necessary before publication, or revise the plan/spec if the release boundary changes.

## Validation plan

Plan-stage validation:

```bash
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies
python scripts/validate-change-metadata.py docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md --path specs/stop-tracking-generated-public-adapter-skill-bodies.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md --path docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md --path docs/plan.md
git diff --check -- docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md docs/plan.md docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies
```

Implementation validation is milestone-specific and culminates in:

```bash
bash scripts/release-verify.sh v0.1.3
```

## Risks and recovery

- Validation migration risk: existing checks may assume tracked `dist/adapters/<adapter>/` package trees. Recovery is to stop before untracking, keep generated trees tracked, and update validation first.
- User install confusion: root guidance or install docs may still point to the retired repository-tree path. Recovery is to block release readiness until guidance is updated or a valid unaffected rationale is recorded.
- Partial package risk: leaving generated entrypoints or opencode command wrappers tracked could look like a valid installable package. Recovery is to remove all generated package fragments or amend the spec before implementation.
- Token-cost benchmark availability: dynamic benchmark execution may be unavailable in a local environment. Recovery is to use the approved waiver/exception process; do not replace the full `v0.1.3` report with a scoped check unless policy allows it.
- Metadata mismatch: `release.source_commit` may not match the validation input. Recovery is to update metadata to the accepted source commit model or record an approved policy exception before release readiness.
- Publication rollback: before publishing, regenerate and restore tracked adapter output if the migration is unsafe; after publishing, use a later recovery release rather than mutating published assets.

## Dependencies

- `v0.1.2` must remain the published compatibility-window release with adapter archives and metadata.
- Proposal, spec, architecture, ADR, and architecture-review are accepted/approved.
- Plan-review must approve this plan before implementation.
- Test spec must be created and active before implementation.
- Release publication depends on completed PR readiness and maintainer authorization.
- Ordinary contributors do not need every supported adapter tool installed locally; repository-owned generation, validation, metadata, and release verification provide non-smoke proof.

## Progress

- [x] 2026-05-13: proposal accepted.
- [x] 2026-05-13: spec approved.
- [x] 2026-05-13: architecture package and ADR updated.
- [x] 2026-05-13: architecture-review approved with no material findings.
- [x] 2026-05-13: execution plan created.
- [x] 2026-05-13: plan-review approved with no material findings.
- [x] 2026-05-13: test spec created and active.
- [x] 2026-05-13: test spec approved by maintainer.
- [x] M1 started.
- [x] 2026-05-13: M1 implementation completed and handed to code-review.
- [ ] M1 implemented and reviewed.
- [ ] M2 implemented and reviewed.
- [ ] M3 implemented and reviewed.
- [ ] M4 release verification closeout completed.
- [ ] explain-change recorded.
- [ ] verify passed.
- [ ] PR handoff completed.
- [ ] release publication completed.

## Decision log

- 2026-05-13: Use a four-milestone release plan: validation migration, repository/guidance untracking, release/token-cost evidence, and final release verification. This keeps generated-output validation safe before removing tracked package fragments.
- 2026-05-13: Keep release publication as a downstream handoff after PR readiness rather than claiming it inside planning. The plan prepares `v0.1.3` release evidence and release gate proof.
- 2026-05-13: Use the active test spec as the implementation proof map before M1 starts.
- 2026-05-13: Treat maintainer test-spec approval as the handoff that unblocks implementation of M1.
- 2026-05-13: For `v0.1.3`, treat `generated_sync` as proof that the tracked adapter support surface is clean while adapter package correctness is proved by release-output archive validation and artifact metadata validation.

## Surprises and discoveries

- Existing script interfaces already support generated release-output validation and benchmark skill-source injection through `--output-dir`, `--root`, `--release-output-dir`, `--release-commit`, and `--skill-source`.
- Release validation needed a version-gated notes and tracked-surface branch so the old `dist/adapters/<adapter>/` drift check remains active for compatibility releases but does not require retired package trees for `v0.1.3`.

## Validation notes

- 2026-05-13: `python scripts/test-adapter-distribution.py -k v0_1_3` passed: 2 tests.
- 2026-05-13: `python scripts/test-adapter-distribution.py` passed: 90 tests. The suite emitted an expected negative-fixture token-cost validation message while still completing `OK`.
- 2026-05-13: `python scripts/validate-skills.py` passed: validated 23 skill files.
- 2026-05-13: `python scripts/build-adapters.py --version v0.1.3 --output-dir <tmp>/release-output && python scripts/validate-adapters.py --root <tmp>/release-output --version v0.1.3` passed.

## Outcome and retrospective

- Not started. Fill this only after the implementation and downstream release handoff finish.

## Readiness

- See `Current Handoff Summary`.

## Remaining completion gates

- implementation and code-review for M1-M4
- review-resolution if material findings are raised
- explain-change
- verify
- pr
- release publication
