# Broad-Smoke Parallelism Preservation

## Status

M1 baseline preservation draft.

## Scope

M1 records the canonical broad-smoke child inventory, reconciles classification
freshness, and records sequential timing before execution behavior changes.
Broad-smoke execution remains sequential in this slice.

## Preservation Matrix

| Surface | Baseline | M1 proof | Result |
| --- | --- | --- | --- |
| Child set | `scripts/ci.sh` `run_broad_smoke` child inventory | `scripts/validate-broad-smoke-classification.py` reconciles classification against `run_broad_smoke` | preserved |
| Child commands | `run_check` command lines in `scripts/ci.sh` | classification validation fails on command mismatch | preserved |
| Canonical order | order of `run_check` invocations | classification validation fails on order mismatch | preserved |
| Required/optional status | all current `run_check` children required | classification requires `required: true` for each current child | preserved |
| Exit behavior | sequential broad-smoke exits according to child failures | M1 does not change `run_broad_smoke` execution | preserved |
| Failure diagnostics | `run_check` prints label, command, captured output, and rerun command | M1 does not change `run_check` | preserved |
| Output order | sequential command order | M1 does not introduce parallel aggregation | preserved |
| `--verbose` | successful child output printed in sequence | M1 does not change verbose behavior | preserved |
| `--jobs 1` | selected worker option parsed, broad-smoke still sequential | M1 does not consume `--jobs` for broad-smoke parallel scheduling | preserved |
| Final verify | actual broad-smoke execution evidence | M1 does not change final verify ownership | preserved |
| Cache boundary | no validation-result cache proof | M1 does not add caching | preserved |

## Classification Reconciliation

- Current classification artifact: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-child-classification.yaml`
- Validator: `python scripts/validate-broad-smoke-classification.py`
- Freshness check: child ID, label, command, order, required status, confidence, side-effect contradictions, and eligibility consistency.

## Timing Evidence

- Baseline artifact: `docs/changes/2026-06-27-broad-smoke-safe-parallelism/broad-smoke-parallelism-baseline.yaml`
- Status: one measured local sequential baseline run recorded in M1.
- Total measured child time: `374061ms`.
- Slowest children: `broad_smoke.adapters.regression` at `173108ms`,
  `broad_smoke.artifact_lifecycle.scoped` at `149434ms`,
  `broad_smoke.artifact_lifecycle.regression` at `13909ms`.
- Limitation: one local WSL2 run is recorded because full sequential child
  timing took about 374s; M3 must use paired same-machine runs before making a
  before/after runtime claim.
