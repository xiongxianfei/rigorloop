# Behavior Preservation

Change ID: `2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper`

## Scope

This record covers M5 repository-local guidance and behavior-preservation evidence for the cache-aware inner-loop lifecycle validation helper.

Published skills are intentionally unchanged in this slice. They remain user-facing, portable guidance and do not expose RigorLoop-internal validator commands, selector mechanics, generated-output paths, or repository maintenance details.

## Repository-Local Command Guidance

Repository-local maintainers should keep inner-loop lifecycle validation and closeout lifecycle validation as distinct command kinds:

| Purpose | Command kind | Cache allowed | Evidence kind |
| --- | --- | --- | --- |
| Repeated inner-loop lifecycle check | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path <path>...` | yes | `cache-hit-inner-loop` or actual-run fallback |
| Milestone closeout lifecycle check | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...` | no | `actual-run-pass` or `actual-run-fail` |
| Verify, PR readiness, CI, release, or branch readiness | governing direct actual-run validation command | no | actual-run evidence |

Cache-hit evidence is inner-loop evidence only. It does not replace closeout, verify, branch-readiness, PR-readiness, CI, release, external-state, or selected-routing proof.

## Preservation Matrix

| Surface | Baseline proof | M5 proof | Preservation result |
| --- | --- | --- | --- |
| Direct lifecycle actual run | Direct `--mode explicit-paths` lifecycle validation was the closeout path before this helper. | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md` | unchanged actual-run closeout path |
| Inner-loop helper cache miss | M2 recorded helper cache-miss fallback behavior. | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml --path docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/behavior-preservation.md --path specs/validation-idempotency-and-cache-hit-safety.md` | safe fallback to actual validation |
| Inner-loop helper cache hit | M2 helper cache-hit tests prove unchanged canonical identity can reuse a prior pass. | `python scripts/test-validation-cache.py` and `python scripts/test-artifact-lifecycle-validator.py` cover helper cache-hit identity, output, and evidence behavior. | cache hit remains inner-loop only |
| Closeout validation | M3 recorded closeout rejection for helper proof commands and cache-only closeout. | `python scripts/test-artifact-lifecycle-validator.py` covers helper closeout rejection and direct actual-run closeout compatibility. | actual-run closeout requirement preserved |
| Failure detection | Direct lifecycle validation failed invalid lifecycle artifacts before this helper. | `python scripts/test-artifact-lifecycle-validator.py` continues to exercise lifecycle failure fixtures and helper fallback behavior. | failure detection unchanged |
| Cache evidence | M2 records formal helper cache-hit evidence only when a safe change root or evidence path exists. | `validation-cache-evidence.yaml` remains optional and is not created by M5 because no formal cache hit is cited as workflow proof. | evidence boundary preserved |
| Selector and CI routing | Selector and CI proof used direct actual-run validation before this helper. | `python scripts/test-select-validation.py` and M4 selector proof keep cache evidence files routed without making CI use the helper. | routing remains actual-run where required |
| Measurement | M4 recorded helper invocation, fallback, closeout actual run, and `defer` expansion recommendation. | `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/validation-cache-measurement.yaml` remains the measurement source. | expansion remains measurement-gated |
| Published skill boundary | Published skills should not expose repository-internal helper commands. | `rg -n "explicit-paths-inner-loop|validate-artifact-lifecycle.py|validation-cache-evidence.yaml|validation-cache-measurement.yaml|validation_selection.py|scripts/select-validation.py" skills` returned no matches. | no internal command leak |
| Generated adapter output | Published skill source was not changed in M5. | No canonical skill file changed, so generated adapter output is unaffected. | generated surfaces unaffected |

## Workstream B Boundary

Workstream B edit-scoped validation remains unimplemented. The first-slice helper makes unchanged-input lifecycle rechecks easier to use; it does not authorize edit-scoped validation, broader validator caching, CI caching, closeout caching, or generated-output/external-state caching.

## M5 Result

The repository-local guidance now shows the two command kinds for maintainers, behavior-preservation evidence is recorded, and published skills remain free of internal RigorLoop command details.
