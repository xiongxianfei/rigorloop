# Explain Change: Stop Tracking Generated Public Adapter Skill Bodies for v0.1.3

## Summary

This change completes the adapter install migration that `v0.1.2` prepared. `skills/` remains the only authored skill source, tracked generated adapter package bodies under `dist/adapters/<adapter>/` are retired, and public adapter installation for `v0.1.3` moves to generated release archives.

The implementation also updates validation so adapter correctness is proved from generated temporary or release-output packages, not tracked generated package trees. Release evidence, token-cost evidence, root guidance, and lifecycle review records were updated so the new source layout is explicit and reviewable.

## Problem

The accepted proposal identified that `v0.1.2` intentionally kept tracked generated public adapter skill bodies during the compatibility window while introducing downloadable adapter archives. After that release shipped, those tracked generated trees became duplicated generated output:

```text
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

Keeping them tracked made generated skill text look like source, increased review noise, and left the single-authored-source migration incomplete.

## Decision Trail

The proposal selected the `v0.1.3` release slice instead of redoing PR #51 or bundling unrelated deferred work. The compatibility-window precondition was satisfied by the stable `v0.1.2` archive-introduction release.

The governing spec requires:

- `R0`-`R2`: scope this migration to `v0.1.3+` while preserving `v0.1.2` historical evidence.
- `R3`-`R7`: keep `skills/` as authored source and preserve adapter support and workflow behavior.
- `R8`-`R15d`: leave only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` tracked under `dist/adapters/`.
- `R16`-`R32`: make adapter install guidance and root contributor guidance point to release archives or the install-contract surface.
- `R33`-`R41g`: replace tracked-package drift validation with generated-output and archive validation.
- `R42`-`R51`: record `v0.1.3` release evidence, metadata, checksums, release notes, smoke evidence, and final release gate.
- `R52`-`R57`: record token-cost evidence using canonical `skills/` and generated public adapter output, not `.codex/skills/`.
- `R58`-`R61`: keep deferred work out of scope.
- `R62`-`R68`: test the supersession and validation replacement contract.

The architecture/ADR decision is the archive-install model: tracked source contains canonical skills and adapter support metadata; generated adapter packages are release artifacts and temporary validation output.

The plan split the work into four milestones:

- M1: validation model migration and regression tests.
- M2: repository tree untracking and root guidance alignment.
- M3: `v0.1.3` release evidence and token-cost reports.
- M4: final local release verification and lifecycle handoff.

## Diff Rationale By Area

| Area | Files | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- | --- |
| Validation model | `scripts/adapter_distribution.py`, `scripts/release-verify.sh`, `scripts/ci.sh`, `scripts/validation_selection.py`, related tests | Release and adapter checks now generate or validate release-output archives for `v0.1.3` instead of requiring tracked adapter package trees. | Satisfies `R33`-`R41g` and review finding `CR-M1-1`. | Spec validation replacement, M1 plan | `test_release_verify_script_supports_v0_1_3_archive_only_gate`, `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3`, full `bash scripts/release-verify.sh v0.1.3` |
| Adapter support surface | `dist/adapters/README.md`, `dist/adapters/manifest.yaml`, removed tracked generated package fragments | Retained README and manifest while removing generated skills, generated instruction entrypoints, and generated opencode command wrappers from tracked source. | Completes single authored source and prevents partial installable packages under `dist/adapters/`. | `R8`-`R15d` | `git ls-files 'dist/adapters/**'`, `test_public_adapter_support_surface_only_tracks_readme_and_manifest` |
| Root/user guidance | `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md`, `dist/adapters/README.md` | Replaced active repository-tree adapter install guidance with archive/install-contract guidance and version-qualified compatibility-window history. | Resolves proposal-review `PAU-R1`; prevents users from following retired install paths. | `R16`-`R32` | `test_root_guidance_points_to_adapter_install_contract_surface`, selector checks for affected guidance paths |
| Release evidence | `docs/releases/v0.1.3/release-notes.md`, `docs/releases/v0.1.3/release.yaml`, `docs/reports/adapter-artifacts/releases/v0.1.3.yaml` | Added release notes, release metadata, smoke evidence, adapter artifact metadata, checksums, and archive install contract for `v0.1.3`. | Makes the release publishable and auditable under the archive-install model. | `R42`-`R51` | `validate-release.py --version v0.1.3 ...`, `bash scripts/release-verify.sh v0.1.3` |
| Token-cost evidence | `docs/reports/token-cost/releases/v0.1.3.md`, `.yaml`, `docs/reports/token-cost/runs/v0.1.3/`, runner/validator tests | Recorded static canonical skill cost and dynamic benchmark evidence using generated public Codex adapter output. Added rejection of `.codex/skills/` and retired tracked adapter source for `v0.1.3`. | Keeps benchmark source aligned with public adapter output and the single-authored-source model. | `R52`-`R57` | `validate-token-cost-report.py`, token-cost runner/report tests, dry-run benchmark evidence |
| Lifecycle evidence | proposal/spec/architecture/ADR/plan/test-spec/review artifacts/change metadata | Recorded proposal/spec review resolutions, milestone reviews, validation notes, and current handoff state. | Keeps workflow state traceable across the release migration. | Workflow contract, plan milestones | `validate-review-artifacts.py`, `validate-change-metadata.py`, `validate-artifact-lifecycle.py` |

## Tests Added Or Changed

The test spec mapped requirements to `T1`-`T17`. Implementation updated repository-owned validation around those cases rather than relying on manual inspection:

- Cross-spec/version behavior: tests prove `v0.1.3` supersedes tracked-package expectations without invalidating `v0.1.2`.
- Tracked surface: tests prove only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked under `dist/adapters/`.
- Generated-output validation: tests prove adapter packages and archives validate from temporary/release output without tracked package bodies.
- Release gate: tests prove `release-verify.sh v0.1.3` builds or uses release output, passes `--release-output-dir` and `--release-commit`, and avoids retired tracked package checks.
- Release metadata: tests prove checksum and `release.source_commit` validation, including negative source-commit mismatch coverage.
- Guidance: tests prove root guidance points to `dist/adapters/README.md` and no longer presents retired tracked adapter skill-body paths as active install guidance.
- Token-cost: tests prove public adapter skill-source handling and rejection of `.codex/skills/` for dynamic public-surface evidence.

No new behavior tests were added in M4 because M4 was an evidence-only release verification milestone.

## Validation Evidence Before Final Verify

Key validation already recorded:

- `python scripts/validate-skills.py` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/test-adapter-distribution.py` passed with 92 tests.
- `python scripts/build-adapters.py --version v0.1.3 --output-dir /tmp/rigorloop-v013-release-output` passed.
- `python scripts/validate-adapters.py --root /tmp/rigorloop-v013-release-output --version v0.1.3` passed.
- `python scripts/run-token-cost-benchmarks.py --release v0.1.3 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir docs/reports/token-cost/runs/v0.1.3 --skill-source /tmp/rigorloop-v013-codex/.agents/skills --dry-run` passed.
- `python scripts/measure-skill-tokens.py` passed with warning-only high-cost findings for `workflow` and `code-review`.
- `python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.3.yaml` passed.
- `python scripts/validate-release.py --version v0.1.3 --release-output-dir /tmp/rigorloop-v013-release-output --release-commit 0f3fe12c8d03d9cb64d9315acc25ac1045c745a8` passed.
- `bash scripts/release-verify.sh v0.1.3` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the lifecycle surfaces used in M4 and review.
- `git diff --check --` passed.

The adapter distribution suite emits an expected negative-fixture token-cost validation message during release verification, but the suite completes `OK` and the release verifier passes.

## Review Resolution Summary

Review resolution is tracked in `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/review-resolution.md`.

Material findings closed:

- `PAU-R1`: accepted. Added root guidance alignment to the proposal before spec work.
- `SGPA-SR1`: accepted. Added explicit relationship/supersession language to the spec.
- `CR-M1-1`: accepted. Updated `release-verify.sh` to support the `v0.1.3` archive-only release gate and added regression coverage.
- `CR-M3-1`: accepted. Updated `docs/releases/v0.1.3/release.yaml` to record maintainer-confirmed manual smoke evidence for extracted Codex, Claude Code, and opencode `v0.1.3` archives.

Clean reviews:

- `proposal-review-r2`
- `spec-review-r2`
- `architecture-review-r1`
- `plan-review-r1`
- `code-review-m1-r2`
- `code-review-m2-r1`
- `code-review-m3-r2`
- `code-review-m4-r1`

The review-resolution closeout status is closed.

## Alternatives Rejected

- Keep tracking `dist/adapters/**/skills`: rejected because it preserves duplicated generated diffs and leaves generated output looking like source after archive distribution is available.
- Remove adapter support: rejected by non-goals and `R5`; Codex, Claude Code, and opencode support remain active.
- Treat this as a main-branch-only cleanup without release evidence: rejected by the accepted proposal, which scoped this as a `v0.1.3` release slice.
- Keep partial generated package fragments tracked: rejected because it would create a misleading half-installable repository tree; generated entrypoints and opencode command wrappers are package output too.
- Use `.codex/skills/` as token-cost public benchmark source: rejected because `.codex/skills/` is local runtime state, not public adapter output.
- Combine this with skill-validator fixture migration or high-cost skill optimization: rejected by non-goals `R58`-`R60`.

## Scope Control

Preserved non-goals:

- No adapter support was removed.
- Workflow stage order was not changed.
- Git history was not rewritten.
- Generated adapter output was not hand-edited as source.
- The skill-validator proof pack was not moved.
- Broad progressive-loading or high-cost public skill optimization was not included.
- No new token-cost threshold gate was added.
- `v0.1.2` historical release evidence remains valid.

## Risks And Follow-Ups

- Release publication is not done yet. Tagging, GitHub release creation, and archive attachment remain downstream release work after verify and PR handoff.
- Token-cost runtime evidence uses the approved dry-run path because live local Codex execution stalled. This is recorded in the `v0.1.3` token-cost report.
- Static token-cost warnings remain for `workflow` and `code-review`; they are warning-only follow-up work, not blockers for this release slice.
- The untracked learn session `docs/learn/sessions/2026-05-13-release-version-gate.md` remains outside this change unless the later workflow chooses to include it.

## Current Readiness

All implementation milestones M1-M4 are closed after code-review. This explanation records the durable change rationale. The next workflow stage is `verify`; this artifact does not claim final verification, PR readiness, hosted CI status, or release publication.
