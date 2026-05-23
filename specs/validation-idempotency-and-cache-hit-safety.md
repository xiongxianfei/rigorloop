# Validation Idempotency and Cache-Hit Safety

## Status

approved

## Related proposal

- [Validation Idempotency and Cache-Hit Safety](../docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md), accepted.

## Goal and context

RigorLoop validation should avoid rerunning a validator when doing so would add no new information: the same validator command already passed, and the command, implementation identity, policy/config identity, and complete input surface are unchanged.

This spec defines the first-slice contract for validation idempotency and cache-hit safety. The slice applies only to `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`. It does not implement edit-scoped validation, changed-path narrowing, remote/shared cache, or cache-skip closeout bundles.

The core safety rule is:

```text
A cache hit may reuse only a previous pass for the same validator command when
the complete input surface, validator implementation identity, and policy/config
identity are unchanged.

On uncertainty, run the validator.
```

## Glossary

- `validator`: A repository-owned command that checks artifacts, metadata, code, or release state.
- `cacheable validator`: A validator command family with a deterministic input-surface contract and deterministic implementation manifest.
- `cache hit`: A decision to reuse a previous passing validator result because the current cache key matches.
- `local execution cache`: Untracked cache state used only to speed repeated local commands.
- `formal cache-hit evidence`: Tracked change-local evidence showing why a skipped validator's prior pass still applies.
- `input surface`: The complete set of files, missing-file states, command arguments, and relevant values read by a cacheable validator for a specific invocation.
- `input-surface hash`: A SHA-256 digest over the normalized input-surface manifest.
- `implementation manifest`: A deterministic list of repository files and states that define the validator implementation identity.
- `policy/config manifest`: A deterministic list of governing policy, spec, schema, or config files and missing-file markers used by the validator.
- `actual-run-pass`: Closeout evidence kind meaning the required validation command actually ran and passed.
- `actual-run-fail`: Closeout evidence kind meaning the required validation command actually ran and failed.
- `blocked`: Closeout evidence kind meaning required validation could not run and records why.
- `cache-hit-inner-loop`: Evidence kind meaning a prior pass was reused for inner-loop proof only.

## Examples first

Example E1: unchanged explicit-path lifecycle command uses a cache hit
Given `validate-artifact-lifecycle.py --mode explicit-paths` previously passed for the same normalized command
And every explicit path has the same content hash or missing-file marker
And the implementation manifest hash and policy/config hash are unchanged
When the same command is run again inside an inner-loop stage
Then the runner may record a `cache-hit-inner-loop` result that references the prior passing event.

Example E2: changed input file invalidates cache
Given a previous lifecycle explicit-path command passed
When any explicit path's content hash changes
Then the cache key no longer matches
And the validator runs instead of reusing the prior pass.

Example E3: changed helper module invalidates cache
Given a previous lifecycle explicit-path command passed
When any repository-local helper module in the implementation manifest changes
Then the implementation manifest hash changes
And the validator runs instead of reusing the prior pass.

Example E4: failed prior result is not reusable
Given the matching command and input surface previously failed
When the same validator command is requested again
Then the cache must not convert that failure into a pass
And the validator runs.

Example E5: formal cache-hit evidence is reviewable
Given an inner-loop validation event uses a cache hit
When reviewers inspect `docs/changes/<change-id>/validation-cache-evidence.yaml`
Then they can see the validator ID, normalized command, prior passing event, command hash, input-surface hash, implementation hash, policy hash, reused result, scope, and closeout flag.

Example E6: cache-only closeout fails
Given a milestone closeout validation event claims `result: pass`
And its evidence kind is `cache-hit-inner-loop`
When lifecycle validation checks the closeout record
Then validation fails because closeout requires `actual-run-pass` evidence in the first slice.

Example E7: valid inner-loop cache hit plus closeout run
Given an inner-loop event records `cache-hit-inner-loop`
And the same milestone later records closeout evidence with `actual-run-pass`
When lifecycle validation checks the records
Then the cache hit is allowed as supporting evidence
And the closeout pass remains valid because the required bundle actually ran.

Example E8: local cache is not portable evidence
Given a local execution cache exists in one worktree and branch
When a contributor switches branch, changes worktree, runs in CI, or copies cache state elsewhere
Then the first-slice cache must not reuse that local entry.

Example E9: Workstream B remains gated
Given Workstream A measurement has not been recorded and reviewed
When a contributor wants to run fewer validators based on changed-path classes
Then this spec does not authorize that behavior.

## Requirements

R1. The first slice MUST apply cache eligibility only to `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

R2. Validators outside R1 MUST run normally and MUST NOT be cache-skipped by this spec.

R3. `validate-artifact-lifecycle.py` modes other than `explicit-paths` MUST NOT be cache-eligible in the first slice.

R4. A cache hit MUST be allowed only when the previous result was `pass`.

R5. Failed, blocked, skipped, not-run, missing, or unknown prior results MUST NOT be reused as passing results.

R6. A cache hit MUST require the same normalized validator command.

R7. A cache hit MUST require the same command hash.

R8. A cache hit MUST require the same complete input-surface hash.

R9. A cache hit MUST require the same validator implementation manifest hash.

R10. A cache hit MUST require the same policy/config manifest hash.

R11. If any cache-key component is unknown, missing, malformed, unsupported, or changed, the validator MUST run.

R12. Cache identity MUST use content hashes and explicit missing-file markers rather than timestamps.

R13. The explicit-path input surface MUST include the normalized command argv.

R14. The explicit-path input surface MUST include the ordered explicit `--path` list after normalization.

R15. The explicit-path input surface MUST include a content hash or missing-file marker for every explicit path.

R16. The explicit-path input surface MUST include the validator implementation manifest hash.

R17. The explicit-path input surface MUST include the policy/config manifest hash.

R18. The implementation manifest MUST be generated deterministically.

R19. The implementation manifest MUST include `scripts/validate-artifact-lifecycle.py`.

R20. The implementation manifest MUST include every resolved repository-local Python file imported directly or transitively by the validator command family.

R21. The implementation manifest MUST NOT include standard-library module source files.

R22. The implementation manifest MUST NOT include third-party package source files.

R23. The implementation manifest MUST include the repository file that owns cache or manifest-generation logic.

R24. A manually maintained version stamp MAY be recorded as additional evidence.

R25. A manually maintained version stamp MUST NOT replace source-file and policy/config hashes in the first slice.

R26. If the implementation manifest cannot be generated deterministically, the validator MUST run and caching MUST be disabled for that invocation.

R27. The policy/config manifest MUST include `CONSTITUTION.md`.

R28. The policy/config manifest MUST include `docs/workflows.md`.

R29. The policy/config manifest MUST include `specs/plan-index-lifecycle-ownership.md`.

R30. The policy/config manifest MUST include any lifecycle-related spec explicitly referenced by the validator or active plan for the invocation.

R31. Optional policy/config files that are absent MUST be represented with explicit missing-file markers when they are part of the declared manifest.

R32. Formal cache-hit evidence MUST be recorded in `docs/changes/<change-id>/validation-cache-evidence.yaml` whenever a cache hit is cited in formal workflow validation.

R33. The untracked local execution cache MUST NOT be the sole evidence for a skipped validator in formal workflow claims.

R34. `validation-cache-evidence.yaml` MUST include `schema_version`.

R35. `validation-cache-evidence.yaml` MUST include `change_id`.

R36. Each cache-hit record MUST include a stable cache-hit ID.

R37. Each cache-hit record MUST include `validator_id`.

R38. Each cache-hit record MUST include normalized command argv.

R39. Each cache-hit record MUST include prior passing event stage and evidence reference.

R40. Each cache-hit record MUST include command hash, input-surface hash, validator implementation hash, and policy hash.

R41. Each cache-hit record MUST include `result_reused: pass`.

R42. Each cache-hit record MUST include an allowed reason.

R43. Each cache-hit record MUST include `scope: inner-loop`.

R44. Each cache-hit record MUST include `closeout_evidence: false`.

R45. A cache-hit record MUST NOT contain secrets, credentials, tokens, usernames, hostnames, private environment dumps, or absolute local paths.

R46. A cache-hit record MUST use repository-relative paths when paths are recorded.

R47. `behavior-preservation.md` MAY summarize cache hits, but it MUST point to `validation-cache-evidence.yaml` when formal cache-hit evidence exists.

R48. `behavior-preservation.md` MUST NOT replace `validation-cache-evidence.yaml` as the authoritative structured cache-hit evidence surface.

R49. A cache hit MUST be represented as evidence that a prior pass still applies, not as a new validator pass.

R50. `cache-hit-inner-loop` MUST be allowed only as inner-loop or supporting evidence in the first slice.

R51. `cache-hit-inner-loop` MUST NOT satisfy stage or milestone closeout validation.

R52. Stage or milestone closeout evidence MUST use one of `actual-run-pass`, `actual-run-fail`, or `blocked`.

R53. `actual-run-pass` MAY satisfy first-slice closeout evidence.

R54. `actual-run-fail` MUST record a failed closeout attempt and MUST NOT satisfy closeout readiness.

R55. `blocked` MUST record why closeout validation could not run and MUST NOT satisfy closeout readiness.

R56. `validate-artifact-lifecycle.py` MUST be the primary validator owner for rejecting cache-only closeout evidence.

R57. `validate-change-metadata.py` MUST reject `change.yaml` evidence references that promote a cache hit into a closeout pass.

R58. A closeout record with only `cache-hit-inner-loop` evidence MUST fail validation.

R59. A closeout record with `actual-run-pass` MAY include cache-hit evidence as supporting context.

R60. The local execution cache MUST be branch-local.

R61. The local execution cache MUST be worktree-local.

R62. The local execution cache MUST be change-local when a change ID is known.

R63. The local execution cache MUST NOT be reused across branches.

R64. The local execution cache MUST NOT be reused across worktrees.

R65. The local execution cache MUST NOT be reused across machines.

R66. The local execution cache MUST NOT be reused through remote or shared cache storage.

R67. The local execution cache MUST NOT be reused across CI jobs in the first slice.

R68. Worktree absolute path identity MAY be stored in the untracked local execution cache only for local invalidation.

R69. Worktree absolute path identity MUST NOT appear in tracked cache-hit evidence.

R70. A cache entry MAY expire by TTL.

R71. TTL MUST NOT make an otherwise-invalid cache entry valid.

R72. Cache entries MAY be deleted at any time without affecting lifecycle evidence validity.

R73. Actual validator execution MUST preserve existing pass/fail behavior, selected checks, exit codes, and failure detection.

R74. Cache support MUST NOT change what `validate-artifact-lifecycle.py --mode explicit-paths` checks when it actually runs.

R75. The first slice MUST record measurement after implementation, including cache-hit count, cache-miss count, total eligible commands, estimated time saved, and remaining validation cost.

R76. Workstream B edit-scoped validation MUST NOT begin under this spec.

R77. Reduced validation based on changed-path or edit-class selection MUST NOT be implemented until Workstream A measurement is reviewed and a separate proposal or spec amendment authorizes it.

R78. Validation cache keys MUST use a deterministic normalized command representation.

R79. The normalized command MUST be an ordered argv vector.

R80. If a command is already recorded as an argv list, that list MUST be the source of truth for command normalization.

R81. If a command is recorded as a string, validators MUST parse it with POSIX `shlex` rules for cache-key construction.

R82. Validators MUST NOT perform shell execution, glob expansion, environment-variable expansion, command substitution, or working-directory-dependent expansion while normalizing commands.

R83. The normalized argv vector MUST preserve argument order.

R84. The command hash MUST be SHA-256 over the canonical JSON encoding of the normalized argv vector.

R85. Canonical JSON encoding for command hashes MUST use UTF-8, sorted object keys where objects appear, and no insignificant whitespace.

R86. Canonical JSON command-hash input MUST NOT include machine-local absolute paths.

R87. Path values in normalized commands MUST be normalized to repository-relative POSIX paths.

R88. Repository-relative path normalization MUST remove leading `./`.

R89. Repository-relative path normalization MUST collapse `.` path segments.

R90. Repository-relative path normalization MUST reject `..` segments that escape the repository root.

R91. Repository-relative path normalization MUST use `/` separators.

R92. Repository-relative path normalization MUST reject absolute POSIX paths.

R93. Repository-relative path normalization MUST reject absolute Windows paths.

R94. Repository-relative path normalization MUST reject home paths such as `~/...`.

R95. Repository-relative path normalization MUST reject URLs, hostnames, credentials, and machine-local path values.

R96. Repository-relative path normalization MUST preserve path case exactly.

R97. For `validate-artifact-lifecycle.py --mode explicit-paths`, explicit paths MUST be the values supplied through `--path`.

R98. The normalized explicit path list MUST preserve user-supplied order after repository-relative path normalization.

R99. Duplicate explicit paths MUST make the invocation ineligible for caching in the first slice.

R100. Two commands with the same normalized explicit path set in a different order MUST produce different command hashes and different first-slice cache keys.

R101. First-slice formal cache-hit and closeout evidence references MUST be supported only in compact `schema_version: 2` `validation_events`.

R102. Compact validation events MAY include `evidence_kind`.

R103. Compact validation events MAY include `evidence_ref`.

R104. `evidence_kind` MUST use one of `actual-run-pass`, `actual-run-fail`, `blocked`, or `cache-hit-inner-loop`.

R105. `evidence_kind: actual-run-pass` MUST pair only with `result: pass`.

R106. `evidence_kind: actual-run-fail` MUST pair only with `result: fail`.

R107. `evidence_kind: blocked` MUST pair only with `result: blocked`.

R108. `evidence_kind: cache-hit-inner-loop` MUST pair only with `result: pass`.

R109. A compact validation event with `result: pass` and `evidence_kind: cache-hit-inner-loop` MUST NOT satisfy stage-closeout or milestone-closeout full-bundle requirements.

R110. A compact validation event with `result: pass` and `evidence_kind: actual-run-pass` MAY satisfy closeout when it covers the required closeout bundle.

R111. `evidence_ref`, when present, MUST be a repository-relative reference to a tracked evidence surface.

R112. Validators MUST reject `evidence_ref` values that are absolute paths, home paths, URLs, hostnames, credential-bearing references, or unresolved anchors.

R113. Legacy validation metadata MUST remain valid for existing validation evidence.

R114. Legacy validation entries MUST NOT use `evidence_kind` or `evidence_ref` to claim cache-hit or closeout semantics.

R115. If a legacy entry attempts to claim cache-hit closeout evidence, validators MUST reject it with a stable diagnostic.

R116. A closeout bundle MUST be satisfied only by compact validation event evidence with `result: pass` and `evidence_kind: actual-run-pass`.

R117. Workstream A measurement evidence MUST be recorded at `docs/changes/<change-id>/validation-cache-measurement.yaml`.

R118. `validation-cache-measurement.yaml` MUST include `schema_version`.

R119. `validation-cache-measurement.yaml` MUST include `change_id`.

R120. `validation-cache-measurement.yaml` MUST include `measurement_window`.

R121. `validation-cache-measurement.yaml` MUST include summary counts for `eligible_commands`, `cache_hits`, `cache_misses`, `cache_disabled`, `actual_runs`, `estimated_seconds_saved`, `remaining_validation_seconds`, and `cache_hit_rate`.

R122. `validation-cache-measurement.yaml` MUST include per-validator measurement entries.

R123. `validation-cache-measurement.yaml` MUST include closeout measurement fields `full_bundle_actual_runs` and `closeout_cache_skips`.

R124. `closeout_cache_skips` MUST be `0` in the first slice.

R125. `validation-cache-measurement.yaml` MUST include `workstream_b_recommendation.state`.

R126. `workstream_b_recommendation.state` MUST be one of `defer`, `propose-follow-up`, or `reject-for-now`.

R127. `workstream_b_recommendation.rationale` MUST be present and non-empty when `state` is `propose-follow-up`.

R128. Measurement counts MUST be non-negative.

R129. Measurement evidence MUST reject impossible count relationships, including `cache_hits + cache_misses + cache_disabled` disagreeing with `eligible_commands`.

R130. Measurement evidence MUST NOT include secrets, usernames, hostnames, absolute machine-local paths, credentials, or environment dumps.

## Command and explicit-path normalization

Validation cache keys use a deterministic normalized command representation.

The normalized command is an ordered argv vector. If the command is already recorded as an argv list, that list is the source of truth. If the command is recorded as a string, validators parse it with POSIX `shlex` rules for cache-key construction only. Validators do not perform shell execution, glob expansion, environment-variable expansion, command substitution, or working-directory-dependent expansion while normalizing the command.

The command hash is:

```text
sha256(JSON canonical encoding of the normalized argv vector)
```

The canonical JSON encoding uses UTF-8, sorted object keys where objects appear, no insignificant whitespace, and no machine-local absolute paths.

Arguments that are path values are normalized to repository-relative POSIX paths:

- remove leading `./`;
- collapse `.` path segments;
- reject `..` segments that escape the repository root;
- use `/` separators;
- reject absolute POSIX paths;
- reject absolute Windows paths;
- reject home paths such as `~/...`;
- reject URLs, hostnames, credentials, and machine-local paths;
- preserve case exactly.

For `validate-artifact-lifecycle.py --mode explicit-paths`, explicit paths are the values supplied through `--path`. The normalized explicit path list preserves the user-supplied order after repository-relative path normalization.

Duplicate explicit paths are invalid for cache eligibility in the first slice.

Two commands with the same normalized path set in a different order produce different command hashes and different cache keys. The first slice prioritizes deterministic replay over semantic path-set equivalence. Later work may introduce canonical path-set hashing if the validator proves order is irrelevant.

## Change metadata evidence-kind contract

First-slice formal cache-hit and closeout evidence references are supported only in compact `schema_version: 2` metadata.

A compact validation event may include:

```yaml
stage: <event id>
lifecycle_stage: <lifecycle stage>
result: <pass | fail | blocked | skipped | not-run>
evidence_kind: <actual-run-pass | actual-run-fail | blocked | cache-hit-inner-loop>
evidence_ref: <optional repository-relative evidence reference>
```

Evidence-kind semantics:

| `evidence_kind` | Allowed `result` | Closeout eligible? | Meaning |
| --- | --- | ---: | --- |
| `actual-run-pass` | `pass` | yes | Required validator or bundle actually ran and passed. |
| `actual-run-fail` | `fail` | no | Required validator or bundle actually ran and failed. |
| `blocked` | `blocked` | no | Validator or bundle could not run because a precondition was missing. |
| `cache-hit-inner-loop` | `pass` | no | Prior passing result still applies to unchanged inputs; inner-loop evidence only. |

A validation event with `result: pass` and `evidence_kind: cache-hit-inner-loop` does not satisfy stage-closeout or milestone-closeout full-bundle requirements.

A validation event with `result: pass` and `evidence_kind: actual-run-pass` may satisfy closeout when it covers the required closeout bundle.

`evidence_ref`, when present, is a repository-relative reference to a tracked evidence surface such as:

```text
docs/changes/<change-id>/validation-cache-evidence.yaml#<cache-hit-id>
```

Validators reject cache-hit evidence references that are absolute paths, home paths, URLs, hostnames, credential-bearing references, or unresolved anchors.

Legacy metadata remains valid for existing validation evidence. Legacy validation entries do not support `evidence_kind` or `evidence_ref` for cache-hit or closeout semantics. If a legacy entry attempts to claim cache-hit closeout evidence, validators reject it with a stable diagnostic and instruct the author to use compact `schema_version: 2` validation events or record an actual closeout run.

## Closeout evidence rule

Stage and milestone closeout require actual-run evidence in the first slice.

A closeout bundle is satisfied only by a compact validation event with:

```yaml
result: pass
evidence_kind: actual-run-pass
```

A cache hit may appear as supporting inner-loop evidence, but it is not a closeout pass.

## Workstream A measurement evidence

After Workstream A implementation, the change records measurement evidence at:

```text
docs/changes/<change-id>/validation-cache-measurement.yaml
```

This file records whether validation idempotency produced enough value to justify considering later edit-scoped validation.

The measurement file includes:

```yaml
schema_version: 1
change_id: <change-id>
measurement_window:
  start_stage: <stage>
  end_stage: <stage>
  description: <what workflow interval was measured>
summary:
  eligible_commands: <integer>
  cache_hits: <integer>
  cache_misses: <integer>
  cache_disabled: <integer>
  actual_runs: <integer>
  estimated_seconds_saved: <number>
  remaining_validation_seconds: <number>
  cache_hit_rate: <number between 0 and 1>
validators:
  - validator_id: <id>
    eligible_commands: <integer>
    cache_hits: <integer>
    cache_misses: <integer>
    actual_runs: <integer>
    estimated_seconds_saved: <number>
    still_rerun_reason: <none | input-changed | implementation-changed | policy-changed | closeout-gate | unsupported-surface | other>
closeout:
  full_bundle_actual_runs: <integer>
  closeout_cache_skips: 0
workstream_b_recommendation:
  state: <defer | propose-follow-up | reject-for-now>
  rationale: <bounded rationale>
```

Measurement rules:

- `eligible_commands` counts commands for which first-slice cache eligibility was evaluated.
- `cache_hits` counts validators skipped because all cache-hit conditions matched.
- `cache_misses` counts eligible validators that ran because any cache key component changed.
- `cache_disabled` counts validators that were not cache-eligible because their input surface or implementation manifest was unsupported.
- `actual_runs` counts validators that actually executed.
- `closeout_cache_skips` is `0` in the first slice.
- `workstream_b_recommendation.state` is one of `defer`, `propose-follow-up`, or `reject-for-now`.
- Measurement evidence does not include secrets, usernames, hostnames, absolute machine-local paths, credentials, or environment dumps.

## Inputs and outputs

Inputs:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...`
- explicit repository-relative paths supplied through repeated `--path` arguments;
- tracked files referenced by those explicit paths;
- validator implementation files from the implementation manifest;
- lifecycle policy/config/spec files from the policy/config manifest;
- optional untracked local execution cache state;
- change ID when running in a workflow-managed change.

Outputs:

- normal validator output and exit code when the validator runs;
- bounded cache-hit output when a cache hit is used, such as `[CACHE HIT] artifact-lifecycle: ...`;
- optional untracked local execution cache updates;
- tracked `docs/changes/<change-id>/validation-cache-evidence.yaml` entries for formal cache-hit claims;
- tracked `docs/changes/<change-id>/validation-cache-measurement.yaml` after Workstream A implementation;
- validation failures when cache identity, evidence shape, or closeout evidence is unsafe.

## State and invariants

- A cache hit is valid only while the full cache key matches a prior passing result.
- A cache hit is not a new validator pass.
- Formal workflow evidence is tracked and reviewable; local cache state is not formal evidence.
- Closeout validation in the first slice requires actual-run evidence.
- Missing files are part of input, implementation, and policy identity when declared.
- On uncertainty, the validator runs.

## Error and boundary behavior

EC1. Unknown validator command family: caching is disabled and the validator runs.

EC2. Missing prior pass: caching is disabled and the validator runs.

EC3. Prior result is not `pass`: caching is disabled and the validator runs.

EC4. Command hash mismatch: caching is disabled and the validator runs.

EC5. Input-surface hash mismatch: caching is disabled and the validator runs.

EC6. Implementation manifest hash mismatch: caching is disabled and the validator runs.

EC7. Policy/config hash mismatch: caching is disabled and the validator runs.

EC8. Manifest-generation error: caching is disabled and the validator runs.

EC9. Missing file in an explicit path: the missing-file marker participates in the input-surface hash.

EC10. Missing optional policy file: the missing-file marker participates in the policy/config manifest hash when that file is declared.

EC11. Cache evidence contains an absolute local path: validation fails.

EC12. Cache evidence contains a secret-like value, hostname, username, credential, or environment dump: validation fails.

EC13. Cache-hit evidence references a prior event that is not passing: validation fails.

EC14. Cache-hit evidence claims `closeout_evidence: true`: validation fails in the first slice.

EC15. Closeout evidence uses only `cache-hit-inner-loop`: validation fails.

EC16. Local cache exists but branch, worktree, or change ID changed: cache entry is ineligible.

EC17. Local cache entry is expired by TTL: cache entry is ineligible.

EC18. TTL is current but any key component mismatches: cache entry is ineligible.

## Compatibility and migration

Existing validators continue to run normally when no eligible cache entry exists.

Existing change metadata remains valid unless it claims formal cache-hit evidence or closeout evidence using the new first-slice fields. First-slice cache-hit and closeout evidence references are supported only in compact `schema_version: 2` `validation_events`; legacy metadata cannot claim cache-hit closeout semantics. This spec does not require existing changes to add `validation-cache-evidence.yaml`.

Rollback is to disable cache reads and force validators to run. Tracked cache-hit evidence may remain as historical inner-loop evidence, but it must not be converted into closeout pass evidence.

## Observability

The system MUST make cache hits visible in command output or validation evidence. A cache hit line SHOULD include validator ID, prior passing event, short key or hash, and a reason that unchanged inputs allow reuse.

Formal workflow cache hits MUST be inspectable from `validation-cache-evidence.yaml`.

Measurement evidence after Workstream A MUST be inspectable from `docs/changes/<change-id>/validation-cache-measurement.yaml` and record eligible commands, cache hits, cache misses, disabled cache evaluations, actual runs, estimated time saved, remaining validation cost, closeout actual-run evidence, and Workstream B recommendation state.

## Security and privacy

Tracked cache-hit evidence MUST NOT contain secrets, credentials, tokens, usernames, hostnames, private environment dumps, worktree absolute paths, or machine-local paths.

Tracked cache-hit evidence MUST use repository-relative paths.

The local execution cache MAY contain non-exported local worktree identity only when needed for invalidation and MUST remain untracked.

## Accessibility and UX

No UI accessibility requirements apply. Command output should remain bounded and readable by humans, with cache-hit status visible enough that reviewers can tell a validator did not actually rerun.

## Performance expectations

Cache-key computation SHOULD be cheaper than rerunning the eligible validator for repeated unchanged input surfaces.

The first slice MUST measure cache-hit count, cache-miss count, disabled cache evaluations, actual runs, eligible command count, estimated time saved, remaining validation cost, closeout actual-run evidence, and Workstream B recommendation state before proposing broader cache coverage or edit-scoped validation.

## Edge cases

EC19. The same explicit paths are provided in a different order: the commands produce different command hashes and different first-slice cache keys.

EC20. Duplicate explicit paths are provided: the invocation is not cache-eligible in the first slice.

EC21. A path exists during the prior pass but is missing now: the input-surface hash changes and the validator runs.

EC22. A path is missing during both the prior pass and current run: the missing-file marker can match if every other key component matches.

EC23. A helper module is imported conditionally: if it can affect validator behavior, it must be included in the deterministic implementation manifest or caching is disabled.

EC24. A lifecycle policy/spec file is absent in a project where it is optional: the missing-file marker is part of the policy/config identity.

EC25. A cache-hit evidence file records a prior passing event that cannot be found: validation fails.

EC26. A cache hit is recorded for an unsupported validator: validation fails.

EC27. A cache hit is recorded after a branch switch using local cache state: validation fails or the entry is ignored and the validator runs.

EC28. A closeout record includes both `cache-hit-inner-loop` and `actual-run-pass`: validation may pass only because of `actual-run-pass`.

EC29. `./docs/plan.md` and `docs/plan.md` are supplied as explicit paths: both normalize to `docs/plan.md`.

EC30. An explicit path is an absolute POSIX path, absolute Windows path, home path, URL, hostname, credential-bearing value, or repository-escaping path: cache eligibility is rejected before cache lookup.

EC31. A command string contains a glob such as `docs/*.md`: command normalization does not expand the glob; the literal value is either treated literally or rejected if unsupported as a path value.

EC32. A command string contains an environment token such as `$HOME/foo`: command normalization does not expand the token and rejects it as unsafe if it is path-like.

EC33. Compact metadata records `evidence_kind: actual-run-fail` with `result: pass`: validation fails.

EC34. Compact metadata records `evidence_kind: blocked` with `result: pass`: validation fails.

EC35. Legacy validation metadata attempts to use `evidence_kind` or `evidence_ref`: validation fails with a stable diagnostic.

EC36. Measurement evidence has negative counts, impossible count relationships, invalid Workstream B recommendation state, or `closeout_cache_skips > 0`: validation fails.

EC37. Measurement evidence recommends Workstream B follow-up without a bounded rationale: validation fails.

## Non-goals

- Do not implement edit-scoped validation.
- Do not implement changed-path validator narrowing.
- Do not cache validators other than `validate-artifact-lifecycle.py --mode explicit-paths` in the first slice.
- Do not cache-skip stage or milestone closeout full bundles.
- Do not add remote, shared, cross-branch, cross-worktree, or CI cache reuse.
- Do not change what any validator checks.
- Do not change validator exit semantics when the validator actually runs.
- Do not reuse failed validator results as passes.
- Do not use agent-declared edit labels as validation authority.
- Do not make caching mandatory for every validator.

## Acceptance criteria

AC1. `validate-artifact-lifecycle.py --mode explicit-paths` can produce a cache hit only after a previous pass with identical command, implementation manifest hash, policy/config hash, and input-surface hash.

AC2. A changed explicit input path invalidates the cache and runs the validator.

AC3. A changed validator entrypoint invalidates the cache and runs the validator.

AC4. A changed repository-local helper module invalidates the cache and runs the validator.

AC5. A changed policy/config/spec file invalidates the cache and runs the validator.

AC6. An unresolved implementation manifest disables caching and runs the validator.

AC7. A failed prior result is never reused as a passing cache hit.

AC8. Formal cache-hit evidence is recorded in `docs/changes/<change-id>/validation-cache-evidence.yaml`.

AC9. Untracked local cache state is never the sole evidence for a skipped validator.

AC10. Cache-hit evidence containing secrets, credentials, hostnames, usernames, absolute local paths, or private environment dumps fails validation.

AC11. A closeout record backed only by `cache-hit-inner-loop` fails validation.

AC12. A closeout record with `actual-run-pass` may include cache-hit evidence as supporting context.

AC13. `validate-artifact-lifecycle.py` owns lifecycle closeout rejection for cache-only closeout evidence.

AC14. `validate-change-metadata.py` rejects `change.yaml` evidence references that promote cache hits into closeout passes.

AC15. Local cache reuse is blocked across branch, worktree, machine, shared-cache, remote-cache, and CI-job boundaries.

AC16. Actual validator execution preserves selected checks, pass/fail behavior, exit codes, and failure detection.

AC17. Workstream A measurement records cache-hit count, cache-miss count, total eligible commands, estimated time saved, and remaining validation cost.

AC18. Workstream B remains unimplemented unless later measurement review and a separate approved proposal or spec amendment authorize it.

AC19. The spec defines normalized command argv as an ordered vector and defines the command hash over canonical JSON.

AC20. Explicit `--path` values for lifecycle validation preserve user-supplied order after repository-relative normalization.

AC21. Duplicate explicit paths are rejected for first-slice cache eligibility.

AC22. Commands with the same paths in different order produce different first-slice cache keys.

AC23. Unsafe paths, absolute paths, home paths, escaping paths, URLs, hostnames, and credential-bearing path values are rejected before cache eligibility.

AC24. First-slice cache-hit and closeout evidence references are supported only in compact `schema_version: 2` `validation_events`.

AC25. The spec defines `evidence_kind`, allowed values, allowed result pairings, and closeout eligibility.

AC26. `cache-hit-inner-loop` cannot satisfy closeout full-bundle validation.

AC27. Legacy validation metadata remains valid but cannot claim cache-hit closeout semantics.

AC28. `evidence_ref` is repository-relative, safe, and validator-checkable.

AC29. Workstream A measurement evidence lives at `docs/changes/<change-id>/validation-cache-measurement.yaml`.

AC30. Measurement evidence records eligible commands, cache hits, cache misses, disabled cache evaluations, actual runs, estimated time saved, remaining validation cost, closeout actual-run evidence, and Workstream B recommendation.

AC31. Measurement evidence rejects impossible counts, unsafe values, and `closeout_cache_skips > 0`.

AC32. Workstream B cannot proceed unless measurement evidence records a reviewed recommendation to propose follow-up work.

## Open questions

None for first-slice architecture.

The test spec should choose exact fixture names and concrete command invocations.

## Next artifacts

```text
architecture
architecture-review
plan
plan-review
test-spec
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Approved for downstream architecture. Workstream B remains blocked until Workstream A measurement is reviewed and a separate proposal or spec amendment authorizes it.
