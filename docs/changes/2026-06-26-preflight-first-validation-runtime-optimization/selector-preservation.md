# Selector Preservation

## Scope

- Milestone: M2. Selector Preservation and Missing-Route Blockers
- Baseline commit before M2 edits: `ee73f074fc26fcef0e6b1e91734de742ffd600bb`
- Worktree state during proof: dirty; M2 selector tests, selector diagnostics, plan state, and this evidence artifact are being edited.
- Source profile: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-regression-profile.md`

## Selected-check identity

Baseline identity from M1 profile:

- `selector.regression`

M2 selector surface identity:

Command:

```bash
python scripts/select-validation.py --mode explicit \
  --path scripts/validation_selection.py \
  --path scripts/test-select-validation.py \
  --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md \
  --json
```

Observed selected checks:

- `artifact_lifecycle.validate`
- `selector.regression`

Identity result:

- `selector.regression` remains selected for selector code changes.
- `artifact_lifecycle.validate` is additionally selected because this M2 preservation evidence is a registered lifecycle evidence artifact.
- All selected checks retain `cache_status: not-applicable`.
- No selected-check coverage is removed.

## Failure-sensitivity proof

Negative fixtures:

- `python scripts/test-select-validation.py -k unregistered_change_evidence` passed 3 tests.
- The unregistered change-local evidence fixture still returns `status: blocked`.
- The blocker still uses `code: manual-routing-required`.
- The blocker now records `path_class: unregistered-change-evidence`, `affected_class: change-local evidence`, `verify_readiness: blocked`, and corrective guidance to register selector routing or record a complete owner-approved deferral.

Diagnostic broad-smoke boundary:

- `python scripts/test-select-validation.py -k diagnostic_broad_smoke` passed 1 test.
- Explicit diagnostic broad-smoke keeps `broad_smoke_required: true` and selects `broad_smoke.repo`.
- The selected-validation result remains `blocked` while the missing-route blocker is present.

Positive fixture:

- `python scripts/test-select-validation.py -k selector_preservation_surface` passed 1 test.
- The M2 selector surface remains classified, has no blocking results, and selects the expected focused checks.

Full selector regression:

- `/usr/bin/time -p python scripts/test-select-validation.py` passed 105 tests.
- Suite-reported duration was `153.67s`; `/usr/bin/time` reported `real 146.03`, `user 5.44`, `sys 24.35`.

Selected-wrapper proof:

- `/usr/bin/time -p bash scripts/ci.sh --mode explicit --timeout 300 --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/selector-preservation.md` passed.
- `artifact_lifecycle.validate` passed in `0.18s`.
- `selector.regression` passed in `142.54s`.
- Focused phase timing was `142.72s`.

## Runtime decision

Safe reduction identified: no.

No-safe-reduction rationale:

M2 strengthens selector preservation and missing-route diagnostics, but it does not optimize `selector.regression` runtime. The M1 profile shows `selector.regression` dominates selected-CI runtime and can exceed 180 seconds under the wrapper. The M2 wrapper proof passed within `300s`, but the direct and wrapper runs still show selector regression as the dominant cost. M2 did not isolate a behavior-preserving runtime reduction that can be accepted without broader selector proof work.

Follow-up decision:

Keep the timeout behavior recorded in M1. Future optimization must preserve selected-check identity, failure sensitivity, missing-route diagnostics, and cache/final-verify boundaries before claiming a runtime improvement.
