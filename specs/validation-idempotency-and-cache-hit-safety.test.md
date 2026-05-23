# Validation Idempotency and Cache-Hit Safety Test Spec

## Status

active

## Related spec and plan

- Spec: [Validation Idempotency and Cache-Hit Safety](validation-idempotency-and-cache-hit-safety.md), approved.
- Plan: [Validation Idempotency and Cache-Hit Safety Plan](../docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md), active.
- Architecture: [System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260523-validation-idempotency-cache-hit-safety](../docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md), accepted.
- Spec reviews: `spec-review-r2` approved the revised spec with no material findings.
- Architecture review: `architecture-review-r1` approved the architecture and ADR with no material findings.
- Plan review: `plan-review-r1` approved the plan with no material findings.

## Testing strategy

- Unit tests exercise deterministic command normalization, repository-relative path normalization, content hashing, missing-file markers, implementation manifests, policy/config manifests, local cache-key matching, evidence-file parsing, measurement validation, and unsafe-value detection.
- Integration tests execute repository-owned CLIs: `scripts/validate-artifact-lifecycle.py`, `scripts/validate-change-metadata.py`, `scripts/select-validation.py`, and `scripts/ci.sh`.
- End-to-end proof is milestone-scoped selected CI over changed files plus final branch-local changed-path proof through `bash scripts/ci.sh --mode local`.
- Smoke tests use repeated explicit-path lifecycle validator commands to prove first run executes, repeated unchanged run can cache-hit, and changed or uncertain conditions fall back to actual validation.
- Manual verification is limited to reviewing behavior-preservation and measurement evidence after implementation; all safety-critical cache and closeout rules require automated tests.
- Contract tests assert validator semantics, selected checks, exit behavior, cache evidence shape, compact metadata evidence-kind semantics, selector routing, and Workstream B non-implementation.
- Migration tests prove existing legacy metadata remains valid unless it attempts to claim cache-hit or closeout semantics through unsupported new fields.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1, R2, R3 | VIC-T001, VIC-T011 | unit, integration | First-slice cache eligibility is limited to lifecycle explicit-path mode. |
| R4, R5 | VIC-T009, VIC-T012, VIC-T013 | unit, integration | Only previous `pass` entries are reusable. |
| R6, R7, R78, R79, R80, R81, R82, R83, R84, R85, R86 | VIC-T002, VIC-T003, VIC-T004, VIC-T012 | unit | Normalized command and command hash contract. |
| R8, R12, R13, R14, R15, R97, R98, R99, R100 | VIC-T005, VIC-T006, VIC-T007, VIC-T012, VIC-T014 | unit, integration | Input-surface hash includes normalized ordered paths, content hashes, missing markers, and duplicate/order behavior. |
| R9, R16, R18, R19, R20, R21, R22, R23, R24, R25, R26 | VIC-T008, VIC-T012, VIC-T015, VIC-T016 | unit, integration | Deterministic implementation manifest and invalidation. |
| R10, R17, R27, R28, R29, R30, R31 | VIC-T009, VIC-T012, VIC-T017 | unit, integration | Policy/config manifest and invalidation. |
| R11 | VIC-T012, VIC-T014, VIC-T015, VIC-T016, VIC-T017, VIC-T018 | integration | Unknown, missing, malformed, unsupported, or changed components run the validator. |
| R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48 | VIC-T019, VIC-T020, VIC-T021, VIC-T022 | unit, integration, security | Formal cache-hit evidence shape, required fields, pointers, and unsafe-value rejection. |
| R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59 | VIC-T023, VIC-T024, VIC-T025, VIC-T026, VIC-T027 | integration, migration | Cache hits are not new passes and cannot satisfy closeout. |
| R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71, R72 | VIC-T010, VIC-T012, VIC-T018, VIC-T022 | unit, security | Local cache lifetime, portability, TTL, deletion, and tracked evidence boundaries. |
| R73, R74 | VIC-T028, VIC-T029 | integration, contract | Actual validator execution preserves behavior, checks, exit codes, and failure detection. |
| R75, R117, R118, R119, R120, R121, R122, R123, R124, R125, R126, R127, R128, R129, R130 | VIC-T030, VIC-T031 | unit, integration, security | Measurement evidence location, shape, counts, enums, rationale, closeout skips, and unsafe values. |
| R76, R77 | VIC-T032, VIC-T036 | contract, manual | Workstream B is not implemented and remains blocked until separate authorization. |
| R87, R88, R89, R90, R91, R92, R93, R94, R95, R96 | VIC-T004, VIC-T007 | unit | Repository-relative path normalization and unsafe path rejection. |
| R101, R102, R103, R104, R105, R106, R107, R108, R109, R110, R111, R112, R116 | VIC-T023, VIC-T024, VIC-T025, VIC-T026 | unit, integration | Compact evidence-kind fields, result pairings, closeout eligibility, and safe refs. |
| R113, R114, R115 | VIC-T027 | migration | Legacy metadata compatibility and rejection of unsupported cache-hit semantics. |
| AC1, AC2, AC3, AC4, AC5, AC6, AC7 | VIC-T012, VIC-T014, VIC-T015, VIC-T016, VIC-T017, VIC-T018 | integration | Core cache hit and invalidation criteria. |
| AC8, AC9, AC10 | VIC-T019, VIC-T020, VIC-T021, VIC-T022 | unit, integration, security | Formal evidence and local-cache non-authority. |
| AC11, AC12, AC13, AC14 | VIC-T023, VIC-T024, VIC-T025, VIC-T026 | integration | Closeout actual-run enforcement. |
| AC15 | VIC-T010, VIC-T018 | unit, integration | Local cache boundary mismatches. |
| AC16 | VIC-T028, VIC-T029 | integration, contract | Actual-run behavior preservation. |
| AC17, AC29, AC30, AC31 | VIC-T030, VIC-T031 | unit, integration | Measurement evidence. |
| AC18, AC32 | VIC-T032, VIC-T036 | contract, manual | Workstream B remains blocked. |
| AC19, AC20, AC21, AC22, AC23 | VIC-T002, VIC-T003, VIC-T004, VIC-T005, VIC-T006, VIC-T007 | unit | Command/path normalization acceptance criteria. |
| AC24, AC25, AC26, AC27, AC28 | VIC-T023, VIC-T024, VIC-T025, VIC-T026, VIC-T027 | unit, integration, migration | Metadata evidence-kind contract. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | VIC-T012, VIC-T019 | Repeated unchanged explicit-path command can cache-hit and record inner-loop evidence. |
| E2 | VIC-T014 | Changed input file invalidates cache and runs validator. |
| E3 | VIC-T015, VIC-T016 | Changed helper or implementation manifest invalidates cache. |
| E4 | VIC-T013 | Failed prior result is not reusable. |
| E5 | VIC-T019, VIC-T020 | Formal cache-hit evidence is reviewable and complete. |
| E6 | VIC-T023, VIC-T026 | Cache-only closeout fails. |
| E7 | VIC-T024 | Inner-loop cache hit plus actual-run closeout is valid. |
| E8 | VIC-T010, VIC-T018 | Local cache is not portable across branch/worktree/CI boundaries. |
| E9 | VIC-T032, VIC-T036 | Workstream B remains gated by measurement and separate approval. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1, EC2, EC3 | VIC-T011, VIC-T012, VIC-T013 | Unknown command, missing pass, and non-pass prior result run validator. |
| EC4, EC5, EC6, EC7, EC8 | VIC-T012, VIC-T014, VIC-T015, VIC-T016, VIC-T017 | Cache key mismatches and manifest errors run validator. |
| EC9, EC10, EC21, EC22, EC24 | VIC-T006, VIC-T017 | Missing-file markers participate in input and policy identity. |
| EC11, EC12, EC13, EC14, EC25, EC26 | VIC-T020, VIC-T021, VIC-T022 | Cache evidence unsafe values, invalid prior events, closeout flag, and unsupported validators fail. |
| EC15, EC28 | VIC-T023, VIC-T024, VIC-T026 | Closeout requires `actual-run-pass`; cache evidence can only support. |
| EC16, EC17, EC18, EC27 | VIC-T010, VIC-T018 | Local cache branch/worktree/change/TTL mismatches are ineligible. |
| EC19, EC20, EC29, EC30, EC31, EC32 | VIC-T003, VIC-T004, VIC-T005, VIC-T007 | Path order, duplicates, relative normalization, unsafe paths, globs, and environment tokens. |
| EC23 | VIC-T008, VIC-T015 | Conditional repository-local helpers must be included or caching disabled. |
| EC33, EC34, EC35 | VIC-T025, VIC-T027 | Invalid evidence-kind/result pairings and legacy field misuse fail. |
| EC36, EC37 | VIC-T030, VIC-T031 | Measurement count and recommendation failures. |

## Test cases

### VIC-T001. Cacheable command family is restricted to lifecycle explicit paths

- Covers: R1, R2, R3, AC1
- Level: unit
- Fixture/setup: Command-family helper inputs for lifecycle explicit-paths, lifecycle local/pr/push modes, metadata validator, review validator, and arbitrary commands.
- Steps: Evaluate cache eligibility for each command family.
- Expected result: Only `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` is cache-eligible.
- Failure proves: Unsupported validators or modes can be cache-skipped by this first slice.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T002. Normalized argv and command hash are deterministic

- Covers: R6, R7, R78, R79, R80, R81, R82, R83, R84, R85, R86, AC19
- Level: unit
- Fixture/setup: Commands represented as argv lists and POSIX shell strings with quoting, spaces, glob-looking tokens, and environment-looking tokens.
- Steps: Normalize command inputs and compute command hashes repeatedly.
- Expected result: Equivalent argv input hashes identically; argument order is preserved; shell expansion, glob expansion, environment expansion, command substitution, and working-directory expansion do not occur.
- Failure proves: Cache keys can vary nondeterministically or depend on local shell behavior.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T003. Explicit path order affects first-slice command keys

- Covers: R14, R83, R98, R100, AC20, AC22, EC19
- Level: unit
- Fixture/setup: Two explicit-path commands with the same normalized path set in different orders.
- Steps: Normalize both commands and compute command hashes/cache keys.
- Expected result: Normalized paths preserve user-supplied order and produce different command hashes/cache keys.
- Failure proves: The first slice is making unproven path-set equivalence assumptions.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T004. Repository-relative path normalization accepts safe variants

- Covers: R87, R88, R89, R91, R96, R97, AC20, EC29
- Level: unit
- Fixture/setup: Safe path values such as `./docs/plan.md`, `docs/./plan.md`, and case-sensitive path variants.
- Steps: Normalize path values.
- Expected result: Leading `./` and `.` segments collapse, `/` separators are used, and case is preserved exactly.
- Failure proves: Input-surface identity can drift across harmless path spelling differences or lose case-sensitive meaning.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T005. Duplicate explicit paths disable cache eligibility

- Covers: R99, AC21, EC20
- Level: unit
- Fixture/setup: Explicit-path command containing the same normalized `--path` value twice.
- Steps: Evaluate cache eligibility.
- Expected result: Invocation is not cache-eligible and returns a stable cache-disabled reason.
- Failure proves: Duplicate path semantics can enter the cache key without an approved contract.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T006. Input-surface hash uses content hashes and missing-file markers

- Covers: R8, R12, R13, R15, EC9, EC21, EC22
- Level: unit
- Fixture/setup: Temporary repo fixture with present explicit paths, changed contents, missing paths, and repeated missing paths.
- Steps: Compute input-surface manifests and hashes across unchanged, changed, and missing states.
- Expected result: Unchanged content hashes match; changed contents change the hash; missing-file markers are stable when still missing and differ from present files.
- Failure proves: Cache hits can ignore actual input state.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T007. Unsafe path values are rejected before cache lookup

- Covers: R90, R92, R93, R94, R95, AC23, EC30, EC31, EC32
- Level: unit
- Fixture/setup: Absolute POSIX paths, absolute Windows paths, `~/...`, repository-escaping `../...`, URLs, hostname-like values, credential-bearing URLs, `$HOME/foo`, and glob-like path tokens.
- Steps: Normalize each value as a path argument.
- Expected result: Unsafe values are rejected before cache lookup; glob/env values are not expanded.
- Failure proves: Cache evidence or keys can capture machine-local or secret-bearing values.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T008. Implementation manifest is deterministic and complete

- Covers: R9, R16, R18, R19, R20, R21, R22, R23, R24, R25, R26, EC23
- Level: unit
- Fixture/setup: Validator entrypoint plus repository-local helper modules, standard-library imports, third-party import names, and manifest-generation helper.
- Steps: Generate the implementation manifest, hash it, and run invalid cases where imports cannot be resolved deterministically.
- Expected result: Manifest includes entrypoint, resolved repository-local imports/helpers, and manifest-generation logic; excludes standard-library and third-party source; unresolved manifest disables caching.
- Failure proves: Validator code changes can reuse stale cache entries.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T009. Policy/config manifest is deterministic

- Covers: R10, R17, R27, R28, R29, R30, R31
- Level: unit
- Fixture/setup: Policy files `CONSTITUTION.md`, `docs/workflows.md`, `specs/plan-index-lifecycle-ownership.md`, explicit lifecycle-related specs, and missing optional files.
- Steps: Generate policy/config manifests and hashes for present, changed, and missing-file states.
- Expected result: Required files and explicit lifecycle specs participate in the hash; declared missing optional files use missing-file markers.
- Failure proves: Policy or spec changes can reuse stale cache entries.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T010. Local execution cache is branch, worktree, and change local

- Covers: R60, R61, R62, R63, R64, R65, R66, R67, R68, R70, R71, R72, AC15, EC16, EC17, EC18, EC27, E8
- Level: unit
- Fixture/setup: Local cache records with matching and mismatching branch, worktree identity, change ID, remote/shared/CI context markers, TTL values, and deleted records.
- Steps: Evaluate local cache entry eligibility.
- Expected result: Only matching branch/worktree/change-local entries can be considered; remote/shared/CI entries are ineligible; TTL can expire but never validate a mismatched key; deletion forces a run.
- Failure proves: Local cache can become portable or authoritative outside its allowed context.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T011. Unsupported commands and modes run normally

- Covers: R1, R2, R3, R11, EC1
- Level: integration
- Fixture/setup: CLI invocations for unsupported lifecycle modes and other validators.
- Steps: Run representative commands through CLI paths or integration helpers.
- Expected result: Unsupported commands do not read cache entries and continue normal execution behavior.
- Failure proves: First-slice cache support leaks to unsupported validation surfaces.
- Automation location: `scripts/test-artifact-lifecycle-validator.py`; targeted CLI smoke in `scripts/test-validation-cache.py`.

### VIC-T012. Repeated identical passing lifecycle validation can cache-hit

- Covers: R4, R6, R7, R8, R9, R10, R11, R73, AC1, E1
- Level: integration
- Fixture/setup: Temporary repo/change fixture with eligible explicit-path lifecycle command and clean local cache directory.
- Steps: Run the validator once, then run the same command again with identical key components.
- Expected result: First run executes and passes; second run may emit bounded `[CACHE HIT]` and exits successfully without changing validator semantics.
- Failure proves: The core idempotency behavior does not work for the only supported first-slice command.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T013. Failed or non-passing prior results are never reused

- Covers: R4, R5, AC7, EC2, EC3, E4
- Level: integration
- Fixture/setup: Local cache records or prior events with `fail`, `blocked`, `skipped`, `not-run`, missing, and unknown results.
- Steps: Request the same eligible validator command.
- Expected result: Validator runs; no cache hit converts a non-pass into a pass.
- Failure proves: Cache can hide a prior validation failure or incomplete run.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T014. Changed explicit input invalidates cache

- Covers: R8, R11, AC2, EC5, E2
- Level: integration
- Fixture/setup: Eligible prior pass and an explicit input file modified afterward.
- Steps: Run the same command after modifying the file.
- Expected result: Input-surface hash changes, cache is missed, and the validator actually runs.
- Failure proves: Cache can skip after validator-readable input changed.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T015. Changed validator entrypoint or manifest generator invalidates cache

- Covers: R9, R11, R18, R19, R23, R26, AC3, AC6, EC6, EC8, E3
- Level: integration
- Fixture/setup: Eligible prior pass, then changed validator entrypoint, manifest generator, or unresolved implementation manifest.
- Steps: Run the same command after implementation-manifest change or manifest-generation failure.
- Expected result: Implementation manifest hash changes or caching is disabled, and validator runs.
- Failure proves: Validator implementation changes can reuse old pass evidence.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T016. Changed repository-local helper invalidates cache

- Covers: R9, R11, R20, AC4, E3
- Level: integration
- Fixture/setup: Eligible prior pass and a changed repository-local helper module included in the import graph.
- Steps: Run the same command after helper change.
- Expected result: Implementation manifest hash changes and validator runs.
- Failure proves: Helper changes can fail to invalidate cache.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T017. Changed policy/config/spec invalidates cache

- Covers: R10, R11, R27, R28, R29, R30, R31, AC5, EC7, EC10, EC24
- Level: integration
- Fixture/setup: Eligible prior pass and modified or missing declared policy/config/spec files.
- Steps: Run the same command after policy/config manifest change.
- Expected result: Policy/config hash changes and validator runs.
- Failure proves: Governing policy changes can reuse old pass evidence.
- Automation location: `scripts/test-validation-cache.py`.

### VIC-T018. Local cache boundary mismatch runs validator

- Covers: R60, R61, R62, R63, R64, R65, R66, R67, R69, AC9, AC15, EC16, EC27, E8
- Level: integration
- Fixture/setup: Prior pass cache entries created under different branch, worktree, change ID, machine/shared/remote/CI marker, or tracked evidence containing worktree path.
- Steps: Request the eligible command in a mismatched context.
- Expected result: Local cache entry is ineligible and validator runs; tracked evidence rejects local absolute path exposure.
- Failure proves: Cache state can cross the first-slice portability boundary.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T019. Formal cache-hit evidence has required shape

- Covers: R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R46, E1, E5, AC8, AC9
- Level: integration
- Fixture/setup: Formal workflow cache-hit evidence file under `docs/changes/<change-id>/validation-cache-evidence.yaml`.
- Steps: Generate or validate a cache-hit record.
- Expected result: Record includes schema version, change ID, stable ID, validator ID, normalized command argv, prior passing event, command/input/implementation/policy hashes, `result_reused: pass`, allowed reason, `scope: inner-loop`, and `closeout_evidence: false`.
- Failure proves: Skipped validation cannot be reviewed from tracked evidence.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-change-metadata-validator.py` if evidence validation is delegated there.

### VIC-T020. Cache-hit evidence references a real prior pass

- Covers: R39, R49, EC13, EC25, E5
- Level: integration
- Fixture/setup: Cache evidence pointing to valid passing, failing, missing, and unresolved prior events.
- Steps: Validate evidence files and references.
- Expected result: Valid prior passing reference passes; failing, missing, or unresolved prior event references fail.
- Failure proves: Cache-hit evidence can claim unsupported prior validation.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-change-metadata-validator.py`.

### VIC-T021. Cache-hit evidence rejects unsupported validator and closeout flag

- Covers: R37, R44, R50, EC14, EC26
- Level: integration
- Fixture/setup: Evidence entries for unsupported validators and entries with `closeout_evidence: true`.
- Steps: Validate evidence files.
- Expected result: Unsupported validators and closeout evidence claims fail in the first slice.
- Failure proves: First-slice evidence can escape the approved command family or closeout boundary.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-change-metadata-validator.py`.

### VIC-T022. Tracked cache-hit evidence rejects unsafe values

- Covers: R45, R46, R68, R69, AC10, EC11, EC12
- Level: unit, security
- Fixture/setup: Evidence records containing absolute paths, worktree paths, usernames, hostnames, credentials, tokens, secret-like values, private environment dumps, and safe repository-relative paths.
- Steps: Validate evidence records.
- Expected result: Unsafe values fail with stable diagnostics; repository-relative safe paths pass.
- Failure proves: Formal evidence can leak local or sensitive data.
- Automation location: `scripts/test-validation-cache.py`; `scripts/test-change-metadata-validator.py`.

### VIC-T023. Compact evidence-kind result pairings are enforced

- Covers: R101, R102, R103, R104, R105, R106, R107, R108, AC24, AC25, EC33, EC34
- Level: unit, integration
- Fixture/setup: Compact `schema_version: 2` metadata fixtures with each valid and invalid `evidence_kind`/`result` pairing.
- Steps: Run change metadata validator on fixtures.
- Expected result: Valid pairings pass; `actual-run-fail` with `pass`, `blocked` with `pass`, and other invalid combinations fail.
- Failure proves: Metadata can mislabel evidence state.
- Automation location: `scripts/test-change-metadata-validator.py`; `tests/fixtures/change-metadata/**`.

### VIC-T024. Inner-loop cache hit plus actual-run closeout is valid

- Covers: R50, R52, R53, R59, R110, AC12, E7, EC28
- Level: integration
- Fixture/setup: Compact metadata with an inner-loop `cache-hit-inner-loop` event and a closeout `actual-run-pass` event covering the required bundle.
- Steps: Run change metadata and artifact lifecycle validators.
- Expected result: Inner-loop cache hit is accepted as supporting evidence and closeout passes only because actual-run evidence exists.
- Failure proves: Supporting cache evidence and closeout pass semantics are not safely separated.
- Automation location: `scripts/test-change-metadata-validator.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T025. Evidence references are safe and resolved

- Covers: R111, R112, AC28
- Level: unit, integration
- Fixture/setup: Compact metadata with repository-relative evidence refs, absolute paths, home paths, URLs, hostnames, credential-bearing refs, and missing anchors.
- Steps: Run metadata validation on each fixture.
- Expected result: Safe tracked refs with existing anchors pass; unsafe or unresolved refs fail.
- Failure proves: `change.yaml` can point reviewers to unsafe or nonexistent evidence.
- Automation location: `scripts/test-change-metadata-validator.py`.

### VIC-T026. Cache-only closeout fails in lifecycle and metadata validation

- Covers: R51, R56, R57, R58, R109, R116, AC11, AC13, AC14, AC26, E6, EC15
- Level: integration
- Fixture/setup: Compact closeout event claiming `result: pass` with only `evidence_kind: cache-hit-inner-loop`.
- Steps: Run `validate-change-metadata.py` and `validate-artifact-lifecycle.py` over fixtures.
- Expected result: Both ownership surfaces reject cache-only closeout or promotion of cache hits into closeout pass claims.
- Failure proves: Stage or milestone closeout can be satisfied without actual validation execution.
- Automation location: `scripts/test-change-metadata-validator.py`; `scripts/test-artifact-lifecycle-validator.py`.

### VIC-T027. Legacy metadata remains compatible but cannot claim cache semantics

- Covers: R113, R114, R115, AC27, EC35
- Level: migration
- Fixture/setup: Existing valid legacy fixtures plus legacy entries attempting to use `evidence_kind` or `evidence_ref`.
- Steps: Run change metadata validator.
- Expected result: Existing valid legacy metadata passes; legacy cache-hit or closeout evidence claims fail with stable diagnostics.
- Failure proves: Migration either breaks valid old records or allows unsupported semantics.
- Automation location: `scripts/test-change-metadata-validator.py`.

### VIC-T028. Actual validator pass behavior is preserved

- Covers: R73, R74, AC16
- Level: integration, contract
- Fixture/setup: Baseline passing explicit-path lifecycle fixture and equivalent post-cache command with cache disabled or forced actual run.
- Steps: Compare selected checks, output status, and exit code before and after cache support when actual execution occurs.
- Expected result: Passing actual run behavior remains unchanged except for allowed cache-disabled bookkeeping that does not alter validator semantics.
- Failure proves: Cache support changed what the validator checks or how it reports actual pass behavior.
- Automation location: `scripts/test-artifact-lifecycle-validator.py`; `docs/changes/.../behavior-preservation.md`.

### VIC-T029. Actual validator fail behavior is preserved

- Covers: R73, R74, AC16
- Level: integration, contract
- Fixture/setup: Baseline failing explicit-path lifecycle fixture and equivalent post-cache command with cache disabled or forced actual run.
- Steps: Run failing fixture before and after cache support.
- Expected result: Exit code, failure detection, and diagnostic identity remain equivalent for actual validator execution.
- Failure proves: Cache support hides or changes real validation failures.
- Automation location: `scripts/test-artifact-lifecycle-validator.py`; `docs/changes/.../behavior-preservation.md`.

### VIC-T030. Measurement evidence validates required fields and counts

- Covers: R75, R117, R118, R119, R120, R121, R122, R123, R124, R125, R126, R127, R128, R129, AC17, AC29, AC30, AC31, EC36, EC37
- Level: unit, integration
- Fixture/setup: `validation-cache-measurement.yaml` valid fixture and invalid fixtures with missing fields, negative counts, inconsistent counts, invalid recommendation state, missing follow-up rationale, and `closeout_cache_skips > 0`.
- Steps: Validate measurement fixtures.
- Expected result: Valid measurement passes; invalid counts, enum values, missing rationale, and closeout skips fail.
- Failure proves: Workstream A measurement cannot be trusted as a follow-on gate.
- Automation location: `scripts/test-change-metadata-validator.py` or `scripts/test-validation-cache.py`, depending on implementation ownership.

### VIC-T031. Measurement evidence rejects unsafe values

- Covers: R130, AC31
- Level: unit, security
- Fixture/setup: Measurement fixtures containing secret-like values, usernames, hostnames, credentials, environment dumps, absolute local paths, and safe repository-relative fields.
- Steps: Validate measurement files.
- Expected result: Unsafe values fail; safe repository-relative evidence passes.
- Failure proves: Measurement artifacts can leak local or sensitive data.
- Automation location: `scripts/test-change-metadata-validator.py` or `scripts/test-validation-cache.py`.

### VIC-T032. Workstream B remains unimplemented

- Covers: R76, R77, AC18, AC32, E9
- Level: contract
- Fixture/setup: Changed-path selector and validation runner surfaces after implementation.
- Steps: Inspect tests and run selector/CI commands that might otherwise narrow validators by edit class.
- Expected result: No runtime behavior selects fewer validators based on changed-path or edit-class narrowing under this spec.
- Failure proves: Riskier Workstream B behavior shipped without measurement review and separate authorization.
- Automation location: `scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit ...`; manual review of implementation diff.

### VIC-T033. New cache evidence files route through selected validation

- Covers: R32, R75, AC8, AC17
- Level: integration
- Fixture/setup: Changed paths `docs/changes/<change-id>/validation-cache-evidence.yaml` and `docs/changes/<change-id>/validation-cache-measurement.yaml`.
- Steps: Run `python scripts/select-validation.py --mode explicit --path <evidence> --path <measurement>` and selected CI explicit mode.
- Expected result: Paths route through bounded selected checks and do not emit `manual-routing-required`.
- Failure proves: New deterministic evidence files can reach verify with unresolved selector debt.
- Automation location: `scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit ...`.

### VIC-T034. Branch-local changed-path proof includes cache evidence files

- Covers: R75, AC17
- Level: smoke
- Fixture/setup: This branch after cache evidence and measurement files exist.
- Steps: Run `python scripts/select-validation.py --mode local` and `bash scripts/ci.sh --mode local`.
- Expected result: Actual changed paths, including new evidence files, route through selected checks before verify.
- Failure proves: Explicit fixtures are being mistaken for actual branch proof.
- Automation location: `python scripts/select-validation.py --mode local`; `bash scripts/ci.sh --mode local`.

### VIC-T035. Behavior-preservation evidence points to cache evidence when formal hits exist

- Covers: R47, R48
- Level: manual, contract
- Fixture/setup: `behavior-preservation.md` created during implementation and optional formal cache-hit evidence.
- Steps: Review behavior-preservation evidence and run lifecycle validation over it.
- Expected result: Behavior-preservation may summarize cache hits but points to `validation-cache-evidence.yaml` when formal evidence exists and does not replace it.
- Failure proves: Narrative evidence can become the structured cache authority.
- Automation location: Manual review in code-review; `scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

### VIC-T036. Final implementation closeout proves Workstream A only

- Covers: R73, R74, R75, R76, R77, AC16, AC17, AC18, AC32, E9
- Level: smoke, manual
- Fixture/setup: Completed implementation branch after M1 through M4 and code-review.
- Steps: Run final local selected CI, lifecycle validation, metadata validation, review-artifact validation, behavior-preservation review, and measurement review.
- Expected result: Workstream A cache behavior and measurement are present; Workstream B remains absent; actual-run closeout evidence remains required.
- Failure proves: Final branch state exceeds the approved scope or lacks required proof.
- Automation location: `bash scripts/ci.sh --mode local`; `verify`; manual code-review/verify inspection.

## Fixtures and data

- `tests/fixtures/validation-cache/` for command normalization, path normalization, cache key, manifest, local cache, formal evidence, and measurement fixtures.
- `tests/fixtures/change-metadata/` additions for compact evidence-kind, evidence-ref, cache-only closeout, legacy compatibility, and measurement fixtures.
- `tests/fixtures/artifact-lifecycle/` additions for cache-only closeout and behavior-preservation fixtures when direct lifecycle fixtures are clearer than metadata-only fixtures.
- Temporary repository fixtures created by tests may be used for branch/worktree/change-local cache behavior and implementation manifest import graphs.
- `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/behavior-preservation.md` records actual-run pass/fail behavior preservation during implementation.
- `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/validation-cache-measurement.yaml` records Workstream A measurement after implementation.
- `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/validation-cache-evidence.yaml` is created only if formal workflow cache-hit evidence is produced during implementation.

## Mocking/stubbing policy

- Unit tests may use temporary files, synthetic cache records, and temporary repository roots to isolate hashing and local-cache behavior.
- Tests must not mock away actual command/path normalization rules, hash inputs, unsafe-value validation, or evidence-kind semantics.
- Integration tests must execute repository-owned scripts through subprocess where exit codes, output, selector routing, and validator behavior are the contract.
- Remote/shared cache, CI cache reuse, and cross-machine reuse are non-goals; tests should simulate those contexts only enough to prove first-slice rejection.

## Migration or compatibility tests

- Existing valid legacy change metadata fixtures continue to pass.
- Existing compact metadata fixtures continue to pass unless they use invalid new evidence-kind fields.
- Legacy metadata attempting to use `evidence_kind` or `evidence_ref` to claim cache-hit or closeout semantics fails.
- Existing validators outside `validate-artifact-lifecycle.py --mode explicit-paths` continue to run normally and are not cache-skipped.
- Rollback behavior is manually reviewed: disabling cache reads must force validators to run while leaving historical cache-hit evidence as non-closeout inner-loop evidence.

## Observability verification

- Cache-hit output includes bounded human-readable status such as `[CACHE HIT]`, validator ID, prior pass reference or local cache identity, short key/hash, and unchanged-input reason.
- Formal cache-hit evidence is inspectable from `validation-cache-evidence.yaml`.
- Measurement evidence is inspectable from `validation-cache-measurement.yaml`.
- Failure diagnostics for unsafe evidence, invalid evidence-kind pairings, unresolved evidence refs, and cache-only closeout are stable enough for fixture assertions.

## Security/privacy verification

- Tracked cache-hit evidence rejects secrets, credentials, tokens, usernames, hostnames, private environment dumps, worktree absolute paths, and machine-local paths.
- Tracked measurement evidence rejects secrets, usernames, hostnames, credentials, environment dumps, and machine-local absolute paths.
- Local worktree identity may appear only in untracked local cache state and must never be copied into tracked evidence.
- Command normalization does not expand shell, glob, environment, command substitution, or working-directory-dependent expressions.

## Performance checks

- Unit tests should assert deterministic hash behavior, not specific wall-clock performance.
- Measurement evidence records eligible commands, cache hits, cache misses, disabled evaluations, actual runs, estimated time saved, remaining validation seconds, cache-hit rate, closeout actual runs, and Workstream B recommendation.
- Final verify reviews the measurement file for plausibility, but the first slice does not set a required minimum speedup threshold.

## Manual QA checklist

- Review the implementation diff to confirm Workstream B changed-path/edit-class narrowing was not added.
- Review behavior-preservation evidence for actual-run pass/fail behavior.
- Review `validation-cache-measurement.yaml` to confirm `closeout_cache_skips: 0`.
- Confirm no tracked cache evidence contains local machine details.
- Confirm closeout evidence uses actual-run validation, not cache-hit-only evidence.

## What not to test and why

- Do not test edit-scoped validation, mixed-edit union selection, or diff-derived edit classes; they are Workstream B and out of scope.
- Do not test remote/shared/cross-branch cache reuse as a supported behavior; first-slice tests prove rejection only.
- Do not test caching for `validate-change-metadata.py`, `validate-review-artifacts.py`, skill validation, release validation, or selector checks; first-slice cache eligibility is lifecycle explicit-path only.
- Do not require historical change records to add cache evidence or measurement files.
- Do not assert exact wall-clock speedup; measurement records observed value and remaining cost.

## Uncovered gaps

None. The approved spec and plan provide enough contract detail for implementation.

## Next artifacts

```text
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof-planning surface for implementation. Ready for M1 implementation after the active plan handoff is updated to `implement M1`.
