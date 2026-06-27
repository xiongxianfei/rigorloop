# Code Review M1 R2: Broad-Smoke Inventory and Baseline

Review ID: code-review-m1-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M1. Inventory, Classification Freshness, and Timing Baseline
Reviewed artifact: commit `e75c8542e026b3a7f75ac25dd4281235162d3a0f`
Reviewed commit: `e75c8542e026b3a7f75ac25dd4281235162d3a0f`
Review date: 2026-06-27
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r2.md
- Open blockers: none
- Next stage: implement
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r2.md
- Review log: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-log.md
- Review resolution: docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m1-r2
- Reviewed milestone: M1. Inventory, Classification Freshness, and Timing Baseline
- Milestone closeout: closed
- Remaining implementation milestones: M2, M3
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review Inputs

- Diff/review surface: commit `e75c8542e026b3a7f75ac25dd4281235162d3a0f`
- Prior review: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/reviews/code-review-m1-r1.md`
- Review resolution: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/review-resolution.md#code-review-m1-r1`
- Governing spec: `specs/broad-smoke-safe-parallelism.md`
- Test spec: `specs/broad-smoke-safe-parallelism.test.md`
- Active plan: `docs/plans/2026-06-27-broad-smoke-safe-parallelism.md`
- M1 implementation files: `scripts/validate-broad-smoke-classification.py`, `scripts/test-select-validation.py`, `scripts/validation_selection.py`
- M1 evidence artifacts: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`, `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-preservation.md`

## Diff Summary

The R2 review surface resolves `CR-M1-1` by removing the undeclared PyYAML dependency from the M1 validation path. The broad-smoke classification validator now uses the Python standard-library `json` module, and the change-local classification and baseline artifacts are JSON-compatible YAML files. The related regression tests also use standard-library JSON loading and mutation writes.

No `scripts/ci.sh` broad-smoke scheduling behavior changes are introduced in M1. Broad-smoke remains sequential until the M2 opt-in scheduling milestone.

## Findings

No material findings.

## No-Finding Rationale

The previous material finding is resolved: the new M1 validator no longer imports an undeclared third-party package, the tests no longer rely on PyYAML, and the classification/baseline artifacts remain machine-validated. The M1 scope still satisfies the approved contract by recording canonical child inventory, classification freshness validation, per-child timing evidence, selector routing, and preservation evidence before any scheduling behavior change.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M1 covers inventory, command identity, classification freshness, and baseline evidence without enabling parallel execution before M2. |
| Test coverage | pass | `scripts/test-select-validation.py` covers valid reconciliation, stale command failure, contradictory side-effect failure, baseline shape, and selector routing for the M1 surfaces. |
| Edge cases | pass | Stale command identity and contradictory parallel-safe metadata have direct regression tests. |
| Error handling | pass | `scripts/validate-broad-smoke-classification.py` fails closed with explicit classification errors for inventory mismatch, stale fields, invalid confidence, unsafe parallel candidates, and missing captured diagnostics. |
| Architecture boundaries | pass | M1 adds a repository-owned validation script and evidence artifacts only; it does not introduce cache, persistent workers, composition, new protocols, or scheduling changes. |
| Compatibility | pass | The R2 fix removes the undeclared PyYAML dependency and keeps the validation path on Python standard-library parsing. |
| Security/privacy | pass | The evidence artifacts record local timing/environment context and command metadata only; no credentials or sensitive outputs are introduced. |
| Derived artifact currency | pass | The classification and baseline artifacts parse under the validator/test path after conversion to JSON-compatible YAML. |
| Unrelated changes | pass | The reviewed diff is limited to the M1 dependency fix, review-resolution state, and lifecycle metadata. |
| Validation evidence | pass | Recorded evidence includes the classification validator, broad-smoke test subset, registered evidence tests, grep proof for removed YAML imports, and selected CI after `CR-M1-1` resolution. |

## Handoff

M1 is closed. The approved auto-through workflow may proceed to M2 implementation. This review does not claim branch readiness, PR readiness, final verification, or hosted CI status.
