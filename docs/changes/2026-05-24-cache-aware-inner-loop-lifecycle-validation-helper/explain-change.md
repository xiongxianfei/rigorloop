# Explain Change

Change ID: `2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`

## Why This Changed

The validation cache already existed for the explicit-path lifecycle validator, but normal inner-loop command habits still used direct actual-run validation. The change adds an explicit inner-loop lifecycle helper mode so repeated lifecycle checks can use the approved cache path without requiring callers to remember the long cache flag set.

The core boundary remains unchanged: helper cache hits are inner-loop evidence only. Closeout, verify, PR readiness, CI, release, and branch-readiness proof still require actual-run validation.

## Implementation Summary

M1 added the `explicit-paths-inner-loop` command-family identity surface. The helper mode normalizes cache identity to canonical direct `explicit-paths` argv while preserving displayed helper argv for evidence.

M2 exposed helper runtime behavior in `validate-artifact-lifecycle.py`. Helper invocations use the existing explicit-path lifecycle cache context by default, fall back to actual validation on misses or unsafe/unknown state, and write formal cache-hit evidence only when a safe change root or explicit evidence path exists.

M3 enforced the closeout boundary. Compact change metadata and lifecycle validation reject helper-mode proof commands and cache-only closeout evidence unless separate direct actual-run closeout evidence satisfies the bundle.

M4 updated measurement validation and evidence. `validation-cache-measurement.yaml` now records helper invocations, cache hits, misses, disabled cache evaluations, actual-run fallbacks, actual runs, closeout actual runs, savings, remaining validation cost, and a Workstream B recommendation that defaults to `defer`.

M5 recorded repository-local guidance and behavior preservation. The two-command table lives in change-local evidence, not published skill text, and published skills remain free of repository-internal helper commands or selector mechanics.

## Safety Boundaries Preserved

- Cache eligibility remains limited to the explicit-path lifecycle command family.
- Direct `--mode explicit-paths` validation remains actual-run closeout evidence.
- `--mode explicit-paths-inner-loop` is helper-only and cannot satisfy closeout as sole proof.
- CI does not use the helper in this slice.
- Selector, routing, external-state, npm, release, generated-output, review-artifact, and change-metadata validation were not made cache-eligible.
- Workstream B edit-scoped validation remains unimplemented.

## Evidence

- `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md` records behavior preservation and the repository-local command split.
- `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml` records first-slice helper measurement and defers eligibility expansion.
- Code-review records for M1 through M5 are recorded under `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/`.
- The active plan records validation commands and current lifecycle state.

## Result

The safe cached inner-loop path is now easy to use through a named helper mode, while actual-run closeout proof remains structurally separate and required.
