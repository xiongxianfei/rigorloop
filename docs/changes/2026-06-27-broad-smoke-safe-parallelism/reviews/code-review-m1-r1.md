# Code Review M1 R1: Broad-Smoke Inventory and Baseline

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Inventory, Classification Freshness, and Timing Baseline
Reviewed artifact: commit `5408529db4b0a41630e2fadc4516bf63ea9faebb`
Reviewed commit: `5408529db4b0a41630e2fadc4516bf63ea9faebb`
Review date: 2026-06-27
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CR-M1-1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-M1-1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m1-r1
- Reviewed milestone: M1. Inventory, Classification Freshness, and Timing Baseline
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: CR-M1-1
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `5408529db4b0a41630e2fadc4516bf63ea9faebb`
- Governing spec: `specs/broad-smoke-safe-parallelism.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`
- Active plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- Test-spec review: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/test-spec-review-r1.md`
- M1 implementation files: `scripts/validate-broad-smoke-classification.py`, `scripts/test-select-validation.py`, `scripts/validation_selection.py`
- M1 evidence artifacts: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Diff Summary

M1 adds a reusable broad-smoke classification validator, change-local child
classification metadata, sequential per-child timing evidence, preservation
evidence, selector routing for the new deterministic evidence files, and
regression tests for inventory reconciliation, stale command detection,
contradictory side-effect metadata, baseline shape, and selector routing.

M1 does not change `scripts/ci.sh` broad-smoke execution scheduling, enable
parallel execution, change child commands, add caching, add validator
composition, or change final verify semantics.

## Findings

## Finding CR-M1-1

Finding ID: CR-M1-1
Severity: major
Location: `scripts/validate-broad-smoke-classification.py:12`; `scripts/test-select-validation.py:21`
Evidence: The new validator and test file import `yaml`, but a repository search shows no existing `import yaml` use outside this M1 diff and no project dependency manifest declaring PyYAML for ordinary contributor validation. The new script is now part of selected-CI routing, so an environment without PyYAML would fail before exercising the broad-smoke classification checks.
Required outcome: M1 validation must not rely on an undeclared third-party YAML parser. The classification validator and tests must use repository-supported dependencies or standard-library parsing while preserving classification freshness and baseline-shape coverage.
Safe resolution path: Convert the change-local classification and baseline artifacts to JSON-compatible YAML and parse them with the Python standard-library `json` module, or add an approved dependency declaration and validation proof for PyYAML. The smaller safe fix is to remove the PyYAML dependency and keep the existing validator/test semantics.
needs-decision rationale: none
auto_fix_class: mechanical
auto_fix_scope: `scripts/validate-broad-smoke-classification.py`, `scripts/test-select-validation.py`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`, validation evidence and lifecycle state surfaces.
auto_fix_validation: `python scripts/validate-broad-smoke-classification.py`; `python scripts/test-select-validation.py -k broad_smoke`; `python scripts/test-select-validation.py -k registered_change_evidence`; selected explicit CI for M1 paths.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | M1 covers inventory, classification freshness, timing baseline, and preservation evidence, but the undeclared parser dependency weakens the validation surface. |
| Test coverage | pass | Tests cover passing reconciliation, stale command failure, contradictory metadata failure, baseline artifact shape, and selector routing. |
| Edge cases | pass | Missing/stale/contradictory classification paths have direct proof through validator tests. |
| Error handling | concern | Classification validation fails closed, but an undeclared import failure would happen before controlled diagnostics. |
| Architecture boundaries | pass | No persistent worker, cache, composition framework, new protocol, or broad-smoke scheduling change is introduced in M1. |
| Compatibility | concern | Ordinary repository validation should not require a new undeclared third-party dependency. |
| Security/privacy | pass | The baseline avoids committing the machine-local adapter temp path and records only local environment timing context. |
| Derived artifact currency | pass | No generated outputs are edited. |
| Unrelated changes | pass | The diff is scoped to M1 lifecycle artifacts, classification validation, selector routing, and tests. |
| Validation evidence | pass | M1 validation evidence includes the classification validator, broad-smoke tests, selected CI, and `--jobs 1` broad-smoke wrapper run. |

## Handoff

M1 requires review-resolution for `CR-M1-1` before it can close or hand off to M2 implementation. This review does not claim branch readiness, PR readiness, final verification, or hosted CI status.
