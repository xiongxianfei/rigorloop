# Verify Report: Stop Tracking Generated Public Adapter Skill Bodies for v0.1.3

## Scope

This report verifies the reviewed M1-M4 implementation for the `v0.1.3` adapter skill-body untracking release slice.

It does not publish the release, create the Git tag, attach GitHub release assets, open a PR, or claim hosted CI status.

## Verdict

Branch-ready for PR handoff.

The implementation, tests, release evidence, token-cost reports, review records, lifecycle artifacts, and durable explanation agree. No verification blockers remain for the tracked change pack.

One unrelated untracked file remains outside this change: `docs/learn/sessions/2026-05-13-release-version-gate.md`.

## Traceability

| Requirement group | Test IDs / proof | Files changed | Evidence | Status |
| --- | --- | --- | --- | --- |
| `R0`-`R7`: version scope, compatibility window, source ownership, adapter support | `T1`, `T2`, release metadata tests, review records | proposal, spec, release notes, root guidance | `v0.1.2` remains historical compatibility evidence; `v0.1.3` release notes and metadata validate | pass |
| `R8`-`R15d`: tracked adapter surface retirement | `T3`, `T5`, `T16` | `dist/adapters/README.md`, `dist/adapters/manifest.yaml`, removed generated package fragments | `git ls-files 'dist/adapters/**'` shows only README and manifest; release validation rejects tracked package fragments | pass |
| `R16`-`R32`: install contract and root guidance alignment | `T7`, `T8`, `T15` | `dist/adapters/README.md`, `CONSTITUTION.md`, `AGENTS.md`, `README.md`, `docs/workflows.md` | adapter README/root-guidance tests passed; selector checks for guidance surfaces passed | pass |
| `R33`-`R41g`: generated-output/archive validation replaces tracked tree checks | `T4`, `T6`, `T9`, `T16` | `scripts/adapter_distribution.py`, `scripts/release-verify.sh`, `scripts/ci.sh`, validation tests | `release-verify.sh v0.1.3` builds release archives and validates release metadata with `--release-output-dir` | pass |
| `R42`-`R51`: release evidence, metadata, notes, smoke, final release gate | `T9`, `T10`, `T11`, `T12`, `T16` | `docs/releases/v0.1.3/*`, `docs/reports/adapter-artifacts/releases/v0.1.3.yaml` | `validate-release.py` passed through the release verifier; smoke rows record maintainer manual archive smoke | pass |
| `R52`-`R57`: token-cost evidence | `T13`, `T14`, `T16` | token-cost reports, run evidence, runner/validator tests | token-cost report validates; dynamic public source uses generated public Codex adapter output, not `.codex/skills/` | pass |
| `R58`-`R61`: non-goals | `T17`, review diff checks | no skill-validator move, no broad skill optimization, no new threshold gate | explain-change and code-review records confirm deferred scope stayed out | pass |
| `R62`-`R68`: test-spec coverage and supersession validation | test spec, adapter distribution suite | spec/test-spec, validator tests | adapter distribution suite passed 92 tests during release verification | pass |

## Verification Dimensions

| Dimension | Result | Evidence |
| --- | --- | --- |
| Spec coverage | pass | `explain-change.md` maps each diff area to approved requirements; no extra behavior was found during final diff/lifecycle inspection. |
| Requirement satisfaction | pass | All `MUST` groups have automated, release-gate, or allowed maintainer smoke evidence. |
| Test coverage | pass | The test spec `T1`-`T17` are covered by adapter distribution, skill, token-cost, release, selector, lifecycle, and review-artifact validations. |
| Test validity | pass | Negative coverage includes tracked package fragments, missing/malformed archives, source-commit mismatch, invalid token-cost source, and stale root guidance. |
| Architecture coherence | pass | The archive-install model is respected: `skills/` is authored source, generated adapters are release output, and `dist/adapters/` tracks only README and manifest. |
| Artifact lifecycle state | pass | `docs/plan.md`, the plan body, change metadata, review log/resolution, explain-change, and release evidence are synchronized. |
| Plan completion | pass | M1-M4 are closed after code-review; explain-change is recorded; verify is the current stage before PR. |
| Validation evidence | pass | Fresh final release verification, review-artifact closeout, change metadata, lifecycle validation, and `git diff --check --` passed. |
| Drift detection | pass | Canonical skill drift check ran in release verification; tracked adapter support surface is limited to README and manifest; generated archives are temporary output only. |
| Risk closure | pass | Compatibility window is version-qualified, rollback/release risks are documented, smoke evidence is recorded, and publication remains a downstream release step. |
| Release readiness | pass | Local `v0.1.3` release gate passed. Hosted CI, GitHub tag creation, release asset upload, and publication are not claimed. |

## Commands

| Command | Result | Notes |
| --- | --- | --- |
| `bash scripts/release-verify.sh v0.1.3` | pass | Validated canonical skills, 73 skill regression tests, generated Codex skill drift, 92 adapter distribution tests, built temporary `v0.1.3` archives, and validated release metadata against `release.source_commit` `0f3fe12c8d03d9cb64d9315acc25ac1045c745a8`. |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies` | pass | 12 reviews, 4 findings, 12 log entries, 4 resolution entries. |
| `python scripts/validate-change-metadata.py docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml` | pass | Change metadata is valid. |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md --path specs/stop-tracking-generated-public-adapter-skill-bodies.md --path specs/stop-tracking-generated-public-adapter-skill-bodies.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md --path docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md --path docs/plan.md --path docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml --path docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/explain-change.md` | pass | Validated the authoritative lifecycle set before writing this report. |
| `git diff --check --` | pass | No whitespace or patch-format issues. |
| `git ls-files 'dist/adapters/**' && git ls-files 'dist/adapters/**/skills/**'` | pass | Output lists only `dist/adapters/README.md` and `dist/adapters/manifest.yaml`; no tracked adapter skill bodies. |

The release verifier prints `token-cost report validation failed: dynamic_runtime.runs: missing required benchmark architecture-review` as expected negative-fixture output from the adapter distribution suite. The suite completed `OK` and the release verifier passed.

## CI Status

Hosted CI was not observed in this verification stage.

Local CI/release readiness is covered by repository-owned validation:

- `.github/workflows/ci.yml` runs `bash scripts/ci.sh` for PR and push events.
- `.github/workflows/release.yml` runs `bash scripts/release-verify.sh "$GITHUB_REF_NAME"` on version tags and uploads `release-output/*` assets through `gh release create`.
- The local `v0.1.3` release gate passed.

## Drift And Lifecycle Assessment

- `docs/plan.md` and the active plan agree: M1-M4 are closed, explain-change is recorded, verify is running, and PR/release publication remain.
- `review-resolution.md` has `Closeout status: closed`; no `needs-decision` disposition remains.
- `review-log.md` has no open findings.
- `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml` lists the governing artifacts, review records, explain-change, and validation evidence.
- `dist/adapters/` tracks only `README.md` and `manifest.yaml`.
- Generated adapter archives are created in temporary release output and are not tracked in Git.

## Remaining Risks

- GitHub release publication and release asset attachment remain downstream release work.
- Hosted CI has not been observed.
- Token-cost runtime evidence uses the approved dry-run path because live local Codex execution stalled.
- Static token-cost warnings for `workflow` and `code-review` remain warning-only follow-up work.
- The unrelated untracked learn session `docs/learn/sessions/2026-05-13-release-version-gate.md` remains outside this change pack.

## Handoff

`verify` passes. The tracked change pack is branch-ready for `pr`.
