# Legacy Architecture Lifecycle Normalization Explain Change

## Summary

This change closes the follow-on legacy architecture lifecycle normalization required by the C4, arc42, and ADR architecture package method. It inventories every current `docs/architecture/` file, compares the eight pre-canonical Markdown architecture records, merges accepted current content into `docs/architecture/system/architecture.md`, archives the legacy records as historical evidence, and records final closeout evidence.

The change remains review-based. It does not add required arc42 section validation, C4 diagram validation, ADR-presence validation, package-shape validation, dependencies, or command behavior changes.

## Problem

The architecture package method introduced one canonical architecture package under `docs/architecture/system/`, but older approved architecture documents still existed at the top of `docs/architecture/`. Without a follow-on normalization artifact, contributors could mistake those change-specific snapshots for current architecture truth, or durable current details could remain stranded in historical files.

The approved plan required normalization in order: inventory first, domain comparison second, canonical merge-back third, legacy lifecycle disposition fourth, and final closeout proof last.

## Decision Trail

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Spec: `specs/architecture-package-method.md`
- Requirement set for this follow-on: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R72`, `R73`-`R75`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- Change-local architecture delta: `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- ADR context: `docs/adr/ADR-20260428-architecture-package-method.md`
- Test spec: `specs/legacy-architecture-lifecycle-normalization.test.md`
- Plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test / evidence |
| --- | --- | --- | --- | --- |
| `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md` | Keeps the full inventory, classification table, domain sequencing, M5 validation notes, final outcome, and `done` state | Make the migration artifact itself prove that every current architecture file was inventoried and every changed legacy record reached a final lifecycle state | spec `R63`-`R66`, plan M1-M5 | `T10`, `T11`, inventory proof, lifecycle validation |
| `docs/plan.md` | Moves the plan from Active to Done | Keep the plan index synchronized with the plan body after M5 closeout | workflow lifecycle rules, plan M5 | `T11`, artifact lifecycle validation |
| `docs/architecture/system/architecture.md` | Removes stale "normalization pending" wording and states that top-level legacy records are archived historical evidence | The canonical package must be current after closeout and must not imply M4 or M5 is still pending | plan M5, `T10` | stale-string assertion, lifecycle validation |
| `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md` | Records M5 evidence, final readiness, and historical-only status for the change-local delta | Preserve reviewable merge-back and disposition evidence without letting the delta compete with the canonical package | spec `R37`-`R39`, `R63`-`R66` | `T10`, `T11` |
| `docs/architecture/*.md` legacy records | Archives all eight top-level legacy Markdown architecture records with canonical package pointers and closeout notes | Preserve historical rationale while stopping legacy snapshots from acting as current architecture sources | plan M4, spec `R63`-`R66` | `T7`, `T8`, M5 legacy lifecycle validation |
| `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml` | Records final changed files, T10/T11/T12 coverage, M5 validation commands, and review handoff state | Keep traceability and validation evidence machine-readable for final review and PR handoff | `T11` | change metadata validation |
| `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-*` | Preserves CR1-F1, CR2-F1, CR3-F1, and the clean M5 code-review record | Keep material review findings durable and closed with evidence | review-resolution contract | review artifact validation |

## Tests And Proof

- `T1` through `T4` proved change-local routing, inventory, domain comparison, and selector non-enforcement.
- `T5` and `T6` proved canonical merge-back and stale canonical wording cleanup.
- `T7` and `T8` proved final lifecycle disposition and historical-body preservation for legacy records.
- `T9` covered publishability and readable, repository-relative artifacts.
- `T10` is the M5 final closeout proof for inventory, canonical freshness, every changed legacy document, lifecycle validation, selector output, and CI wrapper execution.
- `T11` proves the plan body, plan index, change metadata, and this explanation agree.
- `T12` proves the follow-on did not add forbidden enforcement automation or reopen the completed architecture-method rollout scope.

## Review Resolution Summary

The change had three material code-review findings before M5:

- `CR1-F1`: accepted by adding `canonical_artifacts.architecture_package` to `change.yaml`.
- `CR2-F1`: accepted by adding the proposal artifact reference to `change.yaml`.
- `CR3-F1`: accepted by updating only the stale readiness paragraph in the touched change-local architecture delta.

All three findings are closed in `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-resolution.md`. The M5 code-review record is `clean-with-notes` and adds no required-change findings.

## Validation Evidence

M5 validation ran the approved plan commands:

- `find docs/architecture -type f | sort`
- `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing-from-plan %s\n' "$path"; done < <(find docs/architecture -type f | sort)`
- `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
- `python scripts/select-validation.py --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/architecture/system/architecture.md`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
- `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path docs/architecture/system/architecture.md`
- `bash scripts/ci.sh --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md`
- `python -c 'from pathlib import Path; bt=chr(96); text=Path("docs/architecture/system/architecture.md").read_text(); stale=[p for p in ("docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md", "M3 "+bt+"code-review"+bt, "M3 "+bt+"verify"+bt, "M4 skill and generated-output update", "M5 legacy architecture normalization follow-on artifact before final completion claims", "diagrams and change-local architecture deltas remain manual-routed review evidence in the first adoption slice") if p in text]; assert not stale, stale'`
- `rg -n "Status|superseded|archived|canonical architecture|docs/architecture/system/architecture.md" docs/architecture/*.md`
- `git diff --check -- .`

Post-review verify also reran the all-touched selector and CI wrapper checks:

- `python scripts/select-validation.py --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-log.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-resolution.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/reviews/code-review-r4.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/architecture/system/architecture.md --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- `bash scripts/ci.sh --mode explicit --path docs/plan.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-log.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/review-resolution.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/reviews/code-review-r4.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/architecture/system/architecture.md --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization`
- `find docs/architecture -type f | sort`
- `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing-from-plan %s\n' "$path"; done < <(find docs/architecture -type f | sort)`
- `python -c 'from pathlib import Path; bt=chr(96); text=Path("docs/architecture/system/architecture.md").read_text(); stale=[p for p in ("docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md", "M3 "+bt+"code-review"+bt, "M3 "+bt+"verify"+bt, "M4 skill and generated-output update", "M5 legacy architecture normalization follow-on artifact before final completion claims", "diagrams and change-local architecture deltas remain manual-routed review evidence in the first adoption slice") if p in text]; assert not stale, stale'`
- `rg -n "Status|superseded|archived|canonical architecture|docs/architecture/system/architecture.md" docs/architecture/*.md`
- `git diff --check HEAD~6..HEAD -- .`

The M5 and verify selector output did not select `broad_smoke.repo`, so broad smoke was not part of the pass gate.

## Scope Control

- No historical body content in the archived legacy architecture records was rewritten to match the current canonical package.
- No C4 diagram source changed because no actor, external system, container, or deployment boundary changed.
- No ADR was added because the follow-on documented and normalized existing architecture truth without introducing or revising a durable decision.
- No validator, dependency, selected-check coverage, command output behavior, or command exit behavior changed.
- The change-local architecture delta remains historical evidence only after merge-back.

## Risks And Follow-Ups

- Hosted CI has not been observed for the M5 commit from this environment.
- Future architecture-significant work should update `docs/architecture/system/architecture.md` directly or use a change-local delta only as temporary working evidence before merge-back.
- Future package-shape enforcement still requires a later approved contract; this follow-on intentionally stays review-based.

## Readiness

- `implement`, `code-review`, `verify`, and `explain-change` are complete for M5 final closeout.
- The next repository stage is `pr`.
