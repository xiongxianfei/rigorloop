# Single Authored Skill Source First Slice Change Explanation

## Summary

This change makes `skills/` the only authored skill source in day-to-day Git state for the first migration slice.

The implementation changes local Codex mirror validation to use generated temporary output, removes tracked `.codex/skills/**`, keeps public adapter skill copies under `dist/adapters/**/skills` tracked for compatibility, adds tracked adapter install guidance, and prevents token-cost public-surface benchmarks from using the repository-local `.codex/skills/` mirror.

## Problem

RigorLoop had multiple tracked copies of the same skill bodies:

- canonical authored skills under `skills/`;
- repository-local Codex mirror output under `.codex/skills/`;
- public adapter skill copies under `dist/adapters/**/skills`.

That made reviews noisy, let generated output look like authored source, and risked token-cost reports measuring the local Codex mirror instead of public adapter output. The accepted first slice removes only the local Codex mirror from tracked Git state and preserves public adapter repository-tree install compatibility.

## Decision Trail

The proposal chose a staged migration: remove `.codex/skills/` first, keep public `dist/adapters/**/skills` tracked until release artifact packaging and install docs are ready, and validate generated output from canonical `skills/`.

The approved spec requirements implemented by this slice include:

- `R1`-`R8`: `skills/` is the only authored skill source and `.codex/skills/` is generated local output.
- `R10`-`R17`: local Codex mirror generation and validation must work without tracked mirror files.
- `R18`-`R23`: adapter manifest and README are tracked support metadata, not generated skill bodies.
- `R43`, `R49`: public adapter skill copies and drift checks remain active during the compatibility window.
- `R61`-`R66`: token-cost public-surface benchmarks must not use `.codex/skills/`.
- `R67`-`R73`: contributor docs explain generated surfaces and do not present generated copies as authored source.

The architecture and ADR record the same boundary: `.codex/skills/` is generated local runtime output; `dist/adapters/manifest.yaml` and `dist/adapters/README.md` are tracked support surfaces; adapter archives are future release assets, not committed files by default.

The plan executed three milestones:

- M1: local mirror temp-output generation.
- M2: untrack local Codex mirror and update contributor guidance.
- M3: preserve public adapters and add benchmark source guardrails.

All three milestone code reviews closed cleanly with no material findings. No `review-resolution.md` was required.

## Diff Rationale By Area

| Area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `.codex/skills/**` | Removed tracked local Codex mirror files. | Generated local mirror output should not be authored repository content. | `R3`, `R4`, M2 | `test -z "$(git ls-files .codex/skills)"` |
| `.gitignore` | Added `.codex/skills/`. | Prevent regenerated local mirror output from re-entering tracked Git state. | `R7`, M2 | `git check-ignore .codex/skills/proposal/SKILL.md` |
| `scripts/build-skills.py` | Added explicit output-directory support and changed `--check` to validate temporary generated output. | Validation should prove generation works without requiring tracked `.codex/skills/`. | `R10`-`R17`, M1 | `python scripts/test-build-skills.py`; `python scripts/build-skills.py --check` |
| `scripts/skill_validation.py` | Reused validation behavior for generated temp output. | Generated mirror output still needs structural validation. | `R13`, `R16` | `tmpdir=... build-skills.py --output-dir ... && validate-skills.py ...` |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Added selector coverage for skill generation regression and ignore-policy changes. | Changes to generator or ignore policy need focused local-mirror proof. | Plan M1/M2 validation routing | `python scripts/test-select-validation.py` |
| `README.md`, `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md` | Clarified `skills/` source of truth, generated local mirror behavior, public adapter compatibility, and benchmark source guardrails. | Contributor guidance must match the new generated-output boundary. | `R67`-`R73` | `python scripts/test-skill-validator.py`; README validation |
| `dist/adapters/README.md` | Added tracked adapter package guidance. | Users need repository-tree install guidance now and release-asset migration guidance later. | `R20`-`R23`, M3 | `test_public_adapter_readme_documents_metadata_and_install_transition` |
| `scripts/adapter_distribution.py` | Allowed `dist/adapters/README.md` as support metadata during drift/sync. | Adapter drift checks should stay active for generated adapter output without deleting tracked support metadata. | `R18`, `R20`, `R49` | `python scripts/test-adapter-distribution.py`; `build-adapters.py --check` |
| `scripts/validate-token-cost-report.py` | Rejected `.codex/skills/` with an explicit public-source error. | Dynamic public-surface benchmarks must use public adapter output, not local runtime output. | `R62`, `R66` | `test_comparison_portability_and_runner_rules_are_enforced` |
| `scripts/test-adapter-distribution.py` | Added assertions for tracked public adapter skill copies, metadata-only manifest, adapter README, and no generated archives. | M3 named edge cases needed direct proof. | `T11`, `T12`, `T13` | `python scripts/test-adapter-distribution.py` |
| `scripts/test-token-cost-report-validation.py` | Added negative `.codex/skills/` and positive public adapter source checks. | Token-cost source behavior needed direct proof. | `T9` | `python scripts/test-token-cost-report-validation.py` |
| `docs/changes/.../change.yaml`, `docs/plans/...`, `docs/plan.md` | Recorded milestone status, validation evidence, and review handoffs. | The active plan owns current workflow state. | Repository workflow contract | Change metadata and lifecycle validation |

## Tests Added Or Changed

- `scripts/test-build-skills.py`: proves explicit temp output generation, `--check` temp-output validation, generated-output structural validation, and independence from tracked `.codex/skills/`.
- `scripts/test-select-validation.py`: proves generator and ignore-policy changes select the required focused validation.
- `scripts/test-skill-validator.py`: proves contributor docs preserve the generated-output boundary.
- `scripts/test-token-cost-report-validation.py`: proves `.codex/skills/` fails as a public benchmark source and `dist/adapters/codex/.agents/skills/` remains valid while public adapter copies are tracked.
- `scripts/test-adapter-distribution.py`: proves public adapter skill copies remain tracked, adapter manifest stays metadata-only, `dist/adapters/README.md` documents install and migration paths, and generated adapter archives are not committed.

These are unit and contract-level tests because the change is mostly repository packaging, validation routing, and source-boundary behavior. Full release artifact publishing is intentionally out of scope for this slice.

## Validation Evidence Available Before Final Verify

Recorded validation includes:

- `python scripts/test-build-skills.py`
- `python scripts/test-select-validation.py`
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `tmpdir="$(mktemp -d)" && python scripts/build-skills.py --output-dir "$tmpdir/skills" && python scripts/validate-skills.py "$tmpdir/skills"`
- `test -z "$(git ls-files .codex/skills)"`
- `git check-ignore .codex/skills/proposal/SKILL.md`
- `python scripts/build-skills.py`
- `test -n "$(git ls-files 'dist/adapters/*/.*/skills/*/SKILL.md')"`
- `python scripts/test-token-cost-report-validation.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-token-cost-report.py tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml`
- `! git ls-files | rg '(^|/)rigorloop-adapter-.*\.(zip|tar\.gz)$'`
- `python scripts/validate-readme.py README.md`
- `python scripts/validate-readme.py README.md --vision-markers`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-single-authored-skill-source-first-slice/change.yaml`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `python -m py_compile ...`
- `git diff --check ...`

Lifecycle validation passed with existing lifecycle-language warnings in `docs/plan.md` and `docs/workflows.md`; those warnings predate this closeout and require reviewer attention but did not block the scoped validation.

Hosted CI status is not claimed here. Final `verify` has not run yet.

## Review Resolution Summary

No material findings were recorded in M1, M2, or M3 code reviews. Detailed review records and `review-resolution.md` were not required.

Review outcomes:

- M1 code-review: clean-with-notes; no material findings.
- M2 code-review: clean-with-notes; no material findings.
- M3 code-review: clean-with-notes; no material findings.

## Alternatives Rejected

- Untracking public adapter skill copies in this slice was rejected because users may still install adapters by copying `dist/adapters/` from GitHub.
- Committing generated adapter archives was rejected because archives should be release assets with tracked metadata and checksums, not day-to-day Git churn.
- Keeping `.codex/skills/` tracked was rejected because it preserves a duplicate local runtime mirror as apparent authored content.
- Treating `build-skills.py --check` as tracked-file equality after untracking was rejected because it would fail whenever `.codex/skills/` is absent by design.

## Scope Control

This change does not change skill behavior or wording. It does not remove adapter support for Codex, Claude Code, or opencode. It does not remove or untrack public adapter skill copies. It does not add release artifact metadata for adapter archives, because no release artifact is published in this first slice. It does not rewrite Git history.

## Risks And Follow-Ups

Remaining risk is mostly release-process risk: public adapter skill copies still need a later release-artifact migration plan before they can be untracked safely.

Follow-up work remains:

- final `verify`;
- PR handoff;
- later release artifact packaging and metadata work;
- later public adapter cleanup after the compatibility window.

## Current Handoff

The active plan has all implementation milestones closed after clean code review. This explanation completes the rationale surface for the current branch state. The next lifecycle stage is `verify`; final closeout and PR readiness are not claimed by this artifact.
