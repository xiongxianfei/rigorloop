# Explain Change: Test Layering and Change-Scoped Validation

## Summary

This change adds a repository-owned validation selector and makes `scripts/ci.sh` execute selector-selected checks. It lets contributors run targeted proof first, preserves broad smoke for planned or otherwise triggered handoff contexts, and keeps manual proof as durable verification evidence instead of selector state.

The implementation keeps existing validators as proof executors. The new selector owns routing, stable check IDs, affected roots, broad-smoke source attribution, and safe blocking for unclassified paths.

## Problem

RigorLoop had strong validation coverage but no shared, parseable way to choose the cheapest valid proof for a changed surface. Contributors and agents often had to run broad checks early, which slowed iteration without improving first-failure diagnosis.

The approved proposal chose layered validation and change-scoped selection rather than fewer tests.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Add layered validation and a standalone selector: one selector, many modes. |
| Spec | Define JSON selector output, stable check IDs, first-slice path categories, wrapper behavior, unclassified-path blocking, broad-smoke triggers, and manual-proof semantics. |
| Architecture | Put selector logic in `scripts/validation_selection.py`, keep `scripts/select-validation.py` thin, keep `scripts/ci.sh` as wrapper, and do not execute arbitrary selector JSON commands. |
| Plan | Implement M1 selector core, M2 wrapper consumption, M3 workflow/generation alignment, and M4 integration closeout. |
| Review resolution | Accepted 7 material findings across architecture, plan, and code review; all have final actions and validation evidence in `review-resolution.md`. |

Primary requirement groups: `R1`-`R2c`, `R3`-`R5t`, `R6`-`R15b`, `R16`-`R17g`, `R18`-`R21n`, and `R22`-`R26`.

## Diff Rationale by Area

| Area | Files | Why they changed | Evidence |
| --- | --- | --- | --- |
| Selector implementation | `scripts/validation_selection.py`, `scripts/select-validation.py` | Adds the shared selection engine and thin JSON CLI required by the spec. It classifies first-slice paths, emits stable selected checks, maps statuses to exit codes, and blocks unknown paths in v1. | `python scripts/test-select-validation.py` |
| CI wrapper | `scripts/ci.sh`, `.github/workflows/ci.yml` | Moves normal routing to selector output while preserving non-recursive `--mode broad-smoke`; hosted CI passes PR/main ranges through the wrapper. | `bash scripts/ci.sh --mode explicit ...`, `bash scripts/ci.sh --mode broad-smoke` |
| Selector tests | `scripts/test-select-validation.py` | Adds table-driven and fixture-style coverage for catalog IDs, modes, path categories, unclassified blocking, PR/main ranges, release inference, wrapper failures, trusted command enforcement, and guidance alignment. | 25 passing selector/wrapper tests |
| Workflow contract and guidance | `specs/test-layering-and-change-scoped-validation.md`, `specs/test-layering-and-change-scoped-validation.test.md`, `specs/rigorloop-workflow.md`, `docs/workflows.md` | Records the contributor-visible contract for targeted proof, broad smoke, manual proof, selector modes, and stable check IDs. | Lifecycle validation and guidance alignment test |
| Stage skills | `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/workflow/SKILL.md` | Aligns implement, review, verify, and workflow guidance with selector-selected targeted proof, triggered broad smoke, and manual-proof closeout ownership. | `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py` |
| Generated outputs | `.codex/skills/**`, `dist/adapters/**` | Regenerated from canonical skills so Codex, Claude, and OpenCode adapter packages carry the updated workflow guidance without hand edits. | `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1` |
| Change artifacts | `docs/changes/...`, `docs/plans/...`, `docs/plan.md`, architecture/proposal docs | Preserve the approved lifecycle, review records, review resolution, implementation progress, validation evidence, verification notes, and this explanation. | Review artifact, change metadata, and lifecycle validators |

## Tests Added or Changed

- `scripts/test-select-validation.py` is the new selector/wrapper regression surface. It covers the v1 check catalog, JSON shape, exit codes, explicit/local/pr/main/release modes, affected roots, release-version inference, first-slice categories, unclassified-path blocking, wrapper command execution, malformed selector output, selected-command failures, unavailable commands, trusted catalog command enforcement, and workflow guidance alignment.
- A follow-up PR-CI regression covers deterministic routing for `.github/workflows/ci.yml`, `docs/workflows.md`, `docs/plan.md`, and change-local `explain-change.md`, so hosted PR mode does not stop on manual routing for those governed surfaces.
- The M3 guidance alignment test intentionally checks contract-level wording for selector-selected targeted proof, broad-smoke triggers, stable check IDs, `verify-report.md`, release metadata, and manual-proof ownership.
- Adapter and skill tests were not expanded for selector behavior; they remain proof executors and drift checks for generated outputs.

## Verification Evidence

Key commands run and recorded in the plan/change metadata:

- `python scripts/test-select-validation.py`
- `bash scripts/ci.sh --mode explicit --path .github/workflows/ci.yml --path docs/workflows.md --path docs/plan.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md --path scripts/validation_selection.py --path scripts/test-select-validation.py`
- `bash scripts/ci.sh --mode explicit --path scripts/select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh`
- `bash scripts/ci.sh --mode explicit --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-log.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/reviews/code-review-r6.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`
- `bash scripts/ci.sh --mode broad-smoke`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-25-test-layering-and-change-scoped-validation`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `git diff --check -- .`

Verification initially found that `docs/plan.md` and several PR-handoff governance surfaces were not deterministically routed. Hosted PR CI confirmed that gap, and the selector now maps those surfaces to `artifact_lifecycle.validate` or `selector.regression`.

Hosted CI was not observed in this local workflow.

## Review Resolution Summary

- Accepted 7 material findings.
- Rejected 0 findings.
- Deferred 0 findings.
- Partially accepted 0 findings.
- Needs-decision 0 findings remain.
- Review-resolution: `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md`

## Alternatives Rejected

- Fewer tests: rejected because the project needs trustworthy automation and generated-output safety.
- Broad-smoke-first workflow: rejected because it preserves confidence but keeps slow feedback as the first debugging loop.
- Conservative fallback in v1: rejected because no exact fallback check set was approved; v1 blocks unclassified paths instead.
- Hand-editing generated skills/adapters: rejected because generated outputs must remain reproducible from canonical skills.
- Creating `verify-report.md` for this change: rejected because no required manual proof was used; automated proof and lifecycle records were sufficient.

## Scope Control

This change does not add dependency-graph test selection, app/runtime-code routing, semantic review-quality automation, or new manual adapter smoke requirements. It does not reduce broad smoke or release validation; it makes the order and trigger sources explicit.

## Risks and Follow-ups

- A future approved change can define a real conservative fallback set for selector status `fallback`.
- If contributors repeatedly hit manual routing for governance files, add explicit selector mappings with tests rather than weakening unclassified-path blocking.
