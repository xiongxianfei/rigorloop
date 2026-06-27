# Broad-Smoke Parallelism Preservation

## Status

M2 opt-in preservation evidence.

## Scope

M1 recorded the canonical broad-smoke child inventory, reconciled classification
freshness, and recorded sequential timing before execution behavior changes.
M2 adds first-slice opt-in parallel execution only when broad-smoke receives an
explicit `--jobs` value greater than `1`.

Omitted `--jobs` and `--jobs 1` remain strict sequential compatibility paths.
The opt-in path validates classification freshness before launching children,
runs only high-confidence eligible children in parallel windows, keeps
sequential-only children sequential, captures child output separately, and
aggregates output and failures in canonical child order.

## Preservation Matrix

| Surface | Baseline | M2 proof | Result |
| --- | --- | --- | --- |
| Child set | `scripts/ci.sh` `run_broad_smoke` child inventory | sequential `run_check` inventory remains in `run_broad_smoke`; opt-in scheduler uses the same child IDs and commands in the same canonical slots | preserved |
| Child commands | `run_check` command lines in `scripts/ci.sh` | classification validation fails on command mismatch; opt-in scheduler invokes the same command vectors | preserved |
| Canonical order | order of `run_check` invocations | aggregation walks result slots `1..12` and prints grouped output/failures in canonical order | preserved |
| Required/optional status | all current `run_check` children required | classification requires `required: true`; opt-in mode aggregates all executed required child results before choosing the canonical first failure exit code | preserved |
| Exit behavior | sequential broad-smoke exits according to child failures | omitted `--jobs` and `--jobs 1` use the existing sequential path; opt-in mode exits `0` only when all required children pass and nonzero when any required child or scheduler preflight fails | preserved |
| Failure diagnostics | `run_check` prints label, command, captured output, and rerun command | opt-in mode prints child ID, label, command, exit code, duration, execution phase, captured output, and rerun command for each failure | preserved |
| Output order | sequential command order | opt-in mode captures output per child and aggregates in canonical order, not completion order | preserved |
| `--verbose` | successful child output printed in sequence | opt-in mode prints successful child output grouped by child in canonical order with no interleaving | preserved |
| `--jobs 1` | selected worker option parsed, broad-smoke still sequential | explicit `--jobs 1` and omitted `--jobs` do not enter the opt-in scheduler | preserved |
| Final verify | actual broad-smoke execution evidence | M2 changes local scheduling only and does not alter final verify ownership, hosted CI claims, branch readiness, or PR readiness | preserved |
| Cache boundary | no validation-result cache proof | M2 does not add validation-result caching, remote/shared caching, persistent workers, or validator composition | preserved |

## M2 Opt-In Evidence

- Opt-in trigger: `--jobs` must be explicitly provided and greater than `1`.
- Sequential rollback: omitted `--jobs` and `--jobs 1`.
- Classification preflight: `python scripts/validate-broad-smoke-classification.py --classification <artifact>` runs before opt-in children launch.
- Eligible children: only classification entries with `result.eligible_for_parallelism: true` are considered for parallel scheduling.
- Sequential-only children: low-confidence, explicit ineligible, resource-heavy, dynamic, or ordering-dependent children remain sequential.
- Output capture: each opt-in child writes status, command, duration, phase, and captured output into a per-child result directory before aggregation.
- Failure policy: first-slice opt-in mode runs all required broad-smoke children and reports all failures in canonical order.

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

## Validation Evidence

- `python scripts/test-select-validation.py -k broad_smoke` covers sequential compatibility, opt-in overlap, missing-classification preflight failure, deterministic verbose grouping, and all-failures aggregation.
- `python scripts/test-select-validation.py -k jobs` covers existing bounded worker behavior.
- M2 must still run real `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped --jobs 1` before handoff to prove the rollback path on real commands.
