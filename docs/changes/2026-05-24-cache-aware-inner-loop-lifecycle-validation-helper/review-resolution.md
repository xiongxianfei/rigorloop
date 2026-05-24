# Cache-Aware Inner-Loop Lifecycle Validation Helper Review Resolution

## Scope

This record tracks formal lifecycle review findings for the cache-aware inner-loop lifecycle validation helper change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

#### VIC-IH-SR1

Finding ID: VIC-IH-SR1
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec
Required outcome: Define the cache identity normalization relationship between `explicit-paths-inner-loop` and direct `explicit-paths` so implementers know which previous passing event the helper may reuse.
Safe resolution path: Revise the spec to state whether the helper's cache identity normalizes the helper mode to the canonical direct `explicit-paths` command, or whether it keys on the literal helper mode. If it normalizes to direct `explicit-paths`, define the exact canonical argv used for command hash, prior passing event matching, and evidence recording. If it keys on the helper mode, update the adoption rationale and examples so they do not imply reuse of prior direct actual-run passes.
Rationale: The proposal's adoption value depends on the helper reusing safe prior explicit-path lifecycle passes without callers remembering cache flags, but the current spec only says the helper evaluates the same command-family identity.
Chosen action: Defined canonical direct-command cache identity for the helper. The spec now states that `--mode explicit-paths-inner-loop` is a user-facing helper mode and normalizes to canonical direct `--mode explicit-paths` argv for cache-key computation, prior passing event matching, and input-surface identity. Formal helper cache-hit evidence records both `displayed_command_argv` and `canonical_cache_argv`, and formal helper evidence must trace to a prior `actual-run-pass`.
Stop state: closed
Validation target: Rerun spec-review and lifecycle validation after the spec defines helper command normalization and prior-pass matching.
Validation evidence: Spec-review R2 approved the revised helper normalization contract with no material findings. Focused artifact validation is recorded in `change.yaml`.

#### VIC-IH-SR2

Finding ID: VIC-IH-SR2
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec
Required outcome: Remove the normative conflict between the updated helper eligibility requirements and the unchanged non-goal excluding validators other than direct `explicit-paths`.
Safe resolution path: Revise the non-goal to exclude validators outside the explicit-path lifecycle command family while naming `explicit-paths-inner-loop` as the only allowed helper mode, or otherwise make the non-goal use the same eligibility language as R1 and R3.
Rationale: Downstream readers should not have to decide whether the helper is an allowed cache-aware path or excluded by the non-goal.
Chosen action: Rewrote the conflicting non-goal to define the first-slice cache-eligible surface as the explicit-path lifecycle command family, consisting only of direct `--mode explicit-paths` and helper `--mode explicit-paths-inner-loop`. The spec now explicitly excludes metadata validation, review-artifact validation, selected CI, broad smoke, npm tests, release checks, GitHub metadata, external-state proof, generated-output verification, and any unlisted validator or command family.
Stop state: closed
Validation target: Rerun spec-review and lifecycle validation after the eligibility and non-goal language agree.
Validation evidence: Spec-review R2 approved the revised eligibility and non-goal language with no material findings. Focused artifact validation is recorded in `change.yaml`.

#### VIC-IH-SR3

Finding ID: VIC-IH-SR3
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec
Required outcome: Make the measurement schema internally consistent for helper-specific fields and count relationships.
Safe resolution path: Update R121 and related measurement requirements so the required summary field list includes `helper_invocations`, `actual_run_fallbacks`, and `closeout_actual_runs`, or explicitly place those fields elsewhere. Add count consistency rules for helper fields, such as `actual_run_fallbacks <= helper_invocations`, helper cache hits plus fallbacks not exceeding helper invocations, and closeout actual runs remaining separate from helper cache hits.
Rationale: The spec example and AC45 require helper measurement fields, but R121's MUST field list omits them and R129's impossible-count rule covers only the original fields.
Chosen action: Updated the Workstream A measurement schema so helper-specific fields are normative. The required summary fields now include `helper_invocations`, `actual_run_fallbacks`, and `closeout_actual_runs`; validator entries include helper fields; and the spec defines consistency rules separating helper cache hits, helper actual-run fallbacks, and closeout actual runs.
Stop state: closed
Validation target: Rerun spec-review and lifecycle validation after the measurement schema and acceptance criteria agree.
Validation evidence: Spec-review R2 approved the revised measurement schema and count rules with no material findings. Focused artifact validation is recorded in `change.yaml`.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

No material findings.
