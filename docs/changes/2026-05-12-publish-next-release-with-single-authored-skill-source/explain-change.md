# Explain Change: Publish Next Release With Single Authored Skill Source

## Summary

This change prepares the `v0.1.1` transition release so RigorLoop proves the public adapter path works without treating `.codex/skills/` as release evidence.

The implementation keeps `skills/` as the only authored skill source, keeps `dist/adapters/` as the public install path for this release, preserves adapter support for Codex, Claude Code, and opencode, and updates validation and documentation so `.codex/skills/` is only ignored local runtime state.

## Problem

The previous public release contract still described generated `.codex/skills/` checks as part of release verification. After tracked `.codex/skills/` was removed, keeping that path in the release gate would preserve a privileged internal Codex path instead of proving the same public adapter path users receive.

The release needed to preserve three constraints at once:

- contributors author skills once under `skills/`;
- downstream users can still install adapters from `dist/adapters/`;
- release validation proves canonical skills and public adapter output are current, without relying on `.codex/skills/`.

## Decision Trail

The proposal selected a transition release instead of removing all generated adapter copies immediately. That choice keeps repository-tree adapter installation from `dist/adapters/` for `v0.1.1` and defers downloadable adapter archives to a follow-on migration.

The approved spec required:

- `R1`-`R6`: preserve source and release surfaces without changing skill behavior or skill wording;
- `R7`-`R19`: keep `scripts/release-verify.sh` as the maintainer-facing gate, delegate structured validation to `scripts/validate-release.py`, validate public adapter output, and not build or structurally validate `.codex/skills/` as release evidence;
- `R20`-`R25`: document the `v0.1.1` adapter install path and local Codex setup through public Codex adapter output;
- `R26`-`R31`: keep downloadable adapter archives out of required `v0.1.1` scope;
- `R32`-`R35`: keep token-cost evidence on canonical `skills/` and public Codex adapter output, not `.codex/skills/`.

The architecture records the same boundary: release validation for `v0.1.1` checks canonical `skills/`, tracked public adapter output, adapter docs, release notes, token-cost metadata, and ignored/untracked `.codex/skills/` state. It does not build `.codex/skills/` as release evidence.

The plan split implementation into three milestones:

- `M1`: release gate validates public output, not `.codex/skills/`;
- `M2`: release docs and adapter install guidance describe the transition;
- `M3`: release evidence and final validation pack prove the updated contract.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `scripts/release-verify.sh` | Updated `v0.1.1` release verification command selection so it validates canonical skills, public adapter drift, adapter structure, token-cost metadata, and structured release metadata without requiring `build-skills.py --check` as release evidence. | Satisfies the release gate contract while removing `.codex/skills/` generation from required evidence. | Spec `R7`-`R19`; plan `M1`. | `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`; `bash scripts/release-verify.sh v0.1.1`. |
| `scripts/validate-release.py` | Kept the CLI as the structured release validator and made maintainer-facing invocation provide explicit changed-surface context. | Prevents the final release gate from failing because CLI context was missing while preserving stricter helper behavior for changed public skills. | Spec `R8`, `R13`, `R18`, `R19`, `R32`-`R35`; plan `M1`. | `python scripts/validate-release.py --version v0.1.1`; adapter-distribution release validation tests. |
| `scripts/adapter_distribution.py` | Added release validation checks for the `v0.1.1` transition contract, including tracked/ignored `.codex/skills/` state, release-note wording, adapter README expectations, no required archives, and token-cost validation delegation. | Centralizes structured validation for the release surfaces users receive. | Spec `R10`-`R31`; architecture release validation boundary. | `python scripts/test-adapter-distribution.py`; `python scripts/validate-release.py --version v0.1.1`. |
| `scripts/test-adapter-distribution.py` | Added and updated tests for release-gate command selection, ignored/untracked `.codex/skills/`, adapter README guidance, release notes, local Codex setup through public adapter output, optional archive metadata, and token-cost source behavior. | Converts the transition-release requirements into regression coverage. | Test spec `T1`-`T9`, `T11`, `T12`; plan `M1`, `M2`. | `python scripts/test-adapter-distribution.py`. |
| `scripts/test-skill-validator.py` | Replaced stale expectations that contributor docs say to regenerate `.codex/skills/` directly; added assertions for public Codex adapter local setup and negative assertions for stale local-regeneration wording. | M3 validation exposed obsolete test rules that contradicted the approved M2 contract. | Spec `R2`, `R24`, `R25`; test spec `T12`; M3 validation notes. | `python scripts/test-skill-validator.py`. |
| `dist/adapters/README.md` | Made adapter install guidance explicitly version-aware for `v0.1.1`, stated no downloadable archives are required, fixed the artifact metadata path placeholder, and clarified `.codex/skills/` is not a public adapter install source. | Keeps the public adapter install path stable during the compatibility window. | Spec `R20`-`R23`, `R26`, `R27`; plan `M2`. | Adapter README assertions in `python scripts/test-adapter-distribution.py`. |
| `docs/releases/v0.1.1/release-notes.md` | Updated release notes so verification describes public adapter output and no longer says generated `.codex/skills/` is checked as release evidence; stated no adapter archives are introduced. | Release notes are tracked release evidence and must not preserve stale `.codex` release claims. | Spec `R14`, `R16`, `R27`; plan `M2`. | Release-note assertions in `python scripts/test-adapter-distribution.py`; `python scripts/validate-release.py --version v0.1.1`. |
| `README.md`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md` | Simplified local Codex setup guidance: install or copy public Codex adapter output into ignored `.codex/skills/`, keep it untracked, and edit canonical `skills/`. | Resolves stale defensive wording and describes the active path users should follow. | Spec `R24`, `R25`; CR-M2-F1 review resolution. | Focused M2 tests; stale phrase scan; `python scripts/test-skill-validator.py`. |
| `docs/architecture/system/architecture.md` | Updated canonical architecture with the transition-release release-validation boundary, public adapter install path, token-cost source rule, and follow-on adapter archive migration. | Makes the durable architecture match the approved release contract. | Architecture-review R2; ADR `ADR-20260512-generated-skill-output-release-artifacts`. | Architecture reviews recorded clean; lifecycle validation. |
| `docs/proposals/**`, `specs/**`, `docs/plans/**`, `docs/plan.md` | Added proposal, spec, test spec, active execution plan, and plan-index state for the `v0.1.1` transition release. | Provides the governing contract and milestone state for implementation and reviews. | Workflow contract; proposal/spec/plan/test-spec stages. | Lifecycle validation; plan-review and spec-review records. |
| `docs/changes/**` | Added change metadata, review log, review records, review resolution, and this explanation. | Records formal review evidence, material finding disposition, validation evidence, and rationale. | Formal review recording contract; explain-change skill contract. | `python scripts/validate-review-artifacts.py`; `python scripts/validate-change-metadata.py`. |
| `docs/learn/sessions/2026-05-13-defensive-rule-preservation.md` | Recorded the lesson from CR-M2-F1: delete obsolete `.codex/skills/` rules instead of preserving them as defensive warnings. | Prevents the same rule-preservation mistake from recurring in future docs or release work. | CR-M2-F1; learning trigger from user review. | Review-resolution validation and later M2 clean review. |

## Tests Added Or Changed

The primary test surface is `scripts/test-adapter-distribution.py`:

- `T1`: proves `v0.1.1` release verification validates public output and omits `build-skills.py --check` as required release evidence.
- `T2` and `T3`: prove `.codex/skills/` may exist locally when ignored/untracked but is not built or structurally validated for release readiness.
- `T4` and `T6`: prove tracked public adapter output remains current and structurally valid.
- `T5` and `T11`: prove adapter docs, release notes, and contributor guidance describe the transition boundaries.
- `T8`: proves downloadable archives are optional and metadata is required only when archives are present.
- `T9`: proves token-cost metadata uses canonical skills and public Codex adapter output, not `.codex/skills/`.

`scripts/test-skill-validator.py` was changed in M3 because full validation found stale docs assertions from the previous generated-output rule shape. The updated test proves contributor surfaces use the public Codex adapter local setup wording and reject obsolete `.codex/skills/` direct-regeneration phrases.

The test levels are appropriate because the risks are release-contract drift, documentation drift, structured metadata drift, and generated adapter drift rather than application runtime behavior.

## Validation Evidence Available Before Final Verify

Milestone and review validation has passed for:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml`
- `python scripts/validate-release.py --version v0.1.1`
- `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.1`
- `bash scripts/release-verify.sh v0.1.1`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check --`

Hosted CI status is not known from this local workflow stage. Final `verify` has not run yet.

## Review Resolution Summary

Material review findings: 1.

- `CR-M2-F1`: accepted and resolved. Contributor and governance docs were simplified to describe the active public-adapter local setup path instead of preserving obsolete `.codex/skills/` defensive wording.

Review resolution is tracked in `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-resolution.md`.

No open material findings remain. M1, M2, and M3 code-review records are closed with no remaining implementation milestones.

## Alternatives Rejected

- Publishing `v0.1.1` with `.codex/skills/` generation as required release evidence was rejected because it preserves a privileged internal Codex path instead of proving the public Codex adapter path.
- Removing tracked public adapter skill copies from `dist/adapters/` in this release was rejected because `v0.1.0` users still install from repository-tree adapter package roots and downloadable archive migration is not ready.
- Making downloadable adapter archives a required part of `v0.1.1` was rejected because it would combine two migrations in one release and increase release risk.
- Repeating defensive `.codex/skills/` warning wording in contributor docs was rejected after CR-M2-F1; the active guidance now says what to do.

## Scope Control

The change did not:

- remove tracked public adapter skill copies under `dist/adapters/**/skills`;
- remove support for Codex, Claude Code, or opencode;
- require downloadable adapter archives for `v0.1.1`;
- change shipped skill behavior or skill wording;
- introduce a package manager, registry, or installer;
- publish, tag, merge, or deploy a release;
- rewrite Git history.

No generated public adapter packages changed during M3 because drift checks showed they were already current.

## Risks And Follow-Ups

Remaining risks:

- Final `verify` has not run yet.
- PR handoff has not been prepared.
- Hosted CI status is unknown.
- Public release publication remains outside this implementation plan.

Follow-ups:

- Run final `verify`.
- Prepare PR handoff after verification passes.
- Handle downloadable adapter archives in a later accepted migration before removing tracked public adapter skill copies from `dist/adapters/`.

## Readiness

M1-M3 are implemented and reviewed. This explanation records the change rationale and supports handoff to `verify`; it does not claim final verification, PR readiness, or release publication.
