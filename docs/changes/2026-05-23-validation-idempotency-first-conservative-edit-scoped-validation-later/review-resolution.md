# Validation Idempotency First Review Resolution

## Scope

This record closes formal lifecycle review findings for the validation idempotency and cache-hit safety proposal revision.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

## Resolution Entries

### proposal-review-r1

#### VIC-PR1

Finding ID: VIC-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Narrowed the first implementing spec to validation idempotency/cache hits only, changed the next spec name to `validation idempotency and cache-hit safety`, added a `Proof route` section, and moved Workstream B checks into a follow-on gate.
Rationale: The proposal's safety depends on caching first and edit-scoped validation only after measurement and explicit authorization.
Validation target: Proposal keeps Workstream B out of the first implementing spec and test spec.
Validation evidence: Proposal sections `Recommended direction`, `Proof route`, `Acceptance criteria`, `Follow-on gate`, and `Next artifacts`.

#### VIC-PR2

Finding ID: VIC-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Cache storage decision`, separating untracked local execution cache from required change-local cache-hit evidence for formal workflow claims.
Rationale: Local cache state can speed repeated commands, but formal skipped-validation claims need reviewable change-local evidence.
Validation target: Proposal decides the first-slice cache authority model.
Validation evidence: Proposal section `Cache storage decision` and acceptance criteria `AC-VIC-014` through `AC-VIC-015`.

#### VIC-PR3

Finding ID: VIC-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `First validator decision`, locking first-slice cache eligibility to `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` and deferring `validate-change-metadata.py`.
Rationale: Explicit-path lifecycle validation has a more bounded input surface than metadata validation with dynamic references and counts.
Validation target: Proposal names exactly one first cacheable validator and its input surface.
Validation evidence: Proposal sections `First validator decision`, `First-slice boundary`, and `Acceptance criteria`.

#### VIC-PR4

Finding ID: VIC-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replaced version-stamp fallback language with deterministic implementation manifest requirements covering entrypoint, repository-local imports, shared semantics/parser modules, and policy/config/spec files.
Rationale: A manually maintained stamp can miss helper or policy changes and create stale cache hits.
Validation target: Proposal requires deterministic implementation identity for first-slice cache eligibility.
Validation evidence: Proposal sections `Workstream A: Validation Idempotency/Cache Hits`, `Validator implementation manifest`, `Testing and verification strategy`, and `Acceptance criteria`.

#### VIC-PR5

Finding ID: VIC-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Closeout enforcement`, defining actual-run closeout evidence values, `cache-hit-inner-loop` as non-closeout evidence, and acceptance criteria for rejecting closeout records backed only by cache hits.
Rationale: Closeout safety should be mechanically checkable rather than dependent on contributor memory.
Validation target: Proposal defines the closeout enforcement surface.
Validation evidence: Proposal sections `Stage-closeout Gate`, `Closeout enforcement`, `Testing and verification strategy`, and `Acceptance criteria`.

Validation evidence:

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed with 1 review, 5 findings, 1 log entry, and 5 resolution entries.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r1.md` passed.
- `git diff --check -- docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later` passed.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/reviews/proposal-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.

### proposal-review-r2

No material findings.

### spec-review-r1

#### VIC-SR1

Finding ID: VIC-SR1
Disposition: accepted
Status: resolved after spec revision
Owner: spec author
Owning stage: spec
Required outcome: Define normalized argv, path order behavior, duplicate path behavior, and command-hash fixture expectations.
Chosen action: Defined deterministic command and explicit-path normalization. Cache keys now use an ordered normalized argv vector. Explicit `--path` values are normalized to repository-relative POSIX paths while preserving user-supplied order. Duplicate explicit paths are rejected for first-slice cache eligibility. Commands with the same explicit paths in different order produce distinct first-slice cache keys.
Rationale: Preserving argv and path order avoids hidden equivalence assumptions while keeping the first slice deterministic.
Validation target: Spec requirements and acceptance criteria cover command/path normalization without relying on test-spec inference.
Validation evidence: Spec sections `Requirements`, `Command and explicit-path normalization`, `Edge cases`, and `Acceptance criteria`.

#### VIC-SR2

Finding ID: VIC-SR2
Disposition: accepted
Status: resolved after spec revision
Owner: spec author
Owning stage: spec
Required outcome: Define whether the new evidence fields live in compact `schema_version: 2` validation events, legacy metadata, or another named surface, and define how `result` interacts with each evidence kind.
Chosen action: Anchored first-slice cache and closeout evidence to compact `schema_version: 2` `validation_events`. Added the `evidence_kind` contract with `actual-run-pass`, `actual-run-fail`, `blocked`, and `cache-hit-inner-loop`, including allowed result pairings and closeout eligibility. Legacy validation metadata remains valid but cannot claim cache-hit closeout evidence.
Rationale: Closeout and cache-hit evidence need a concrete metadata contract so validators can reject cache-only closeout claims mechanically.
Validation target: Spec requirements and acceptance criteria cover valid and invalid metadata fixtures for cache-only closeout rejection.
Validation evidence: Spec sections `Requirements`, `Change metadata evidence-kind contract`, `Closeout evidence rule`, `Compatibility and migration`, `Edge cases`, and `Acceptance criteria`.

#### VIC-SR3

Finding ID: VIC-SR3
Disposition: accepted
Status: resolved after spec revision
Owner: spec author
Owning stage: spec
Required outcome: Define a durable measurement evidence surface and minimum required fields before test-spec.
Chosen action: Defined Workstream A measurement evidence at `docs/changes/<change-id>/validation-cache-measurement.yaml` with required fields for eligible commands, cache hits, cache misses, disabled cache evaluations, actual runs, estimated time saved, remaining validation cost, closeout actual-run evidence, and Workstream B recommendation state.
Rationale: The feature spec owns durable workflow-gate evidence location and minimum shape; the test spec should operationalize fixtures and commands against that contract.
Validation target: Spec requirements and acceptance criteria cover measurement evidence shape and location.
Validation evidence: Spec sections `Requirements`, `Workstream A measurement evidence`, `Inputs and outputs`, `Observability`, `Performance expectations`, `Edge cases`, and `Acceptance criteria`.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

#### VIC-CR-M1-R1-F1

Finding ID: VIC-CR-M1-R1-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement M1 review-resolution
Required outcome: The cache identity layer must expose unresolved implementation-manifest state as cache-ineligible, and M1 tests must directly prove the named unresolved-manifest edge case from `VIC-T008` / spec `R26`.
Chosen action: Updated `scripts/validation_cache.py` so implementation-manifest construction fails closed with stable `CacheIdentityError.code` values for missing validator entrypoints, unresolved repository-local imports, unparseable repository-local helpers, and unresolved manifest-generator identity. Added direct tests in `scripts/test-validation-cache.py` for missing entrypoint, unresolved `scripts.*` helper import, unparseable repository-local helper, and continued standard-library/third-party exclusion.
Rationale: A stale or incomplete implementation manifest can make a future cache hit unsafe. M1 is the helper layer that later cache execution will rely on, so unresolved manifest inputs need direct proof before lifecycle cache integration proceeds.
Validation target: Focused unresolved-manifest regression coverage and M1 validation set pass before rerunning code-review.
Validation evidence: `python scripts/test-validation-cache.py` passed with 13 tests; `python scripts/test-artifact-lifecycle-validator.py` passed with 61 tests; `python scripts/test-select-validation.py` passed with 94 tests; `python scripts/validate-change-metadata.py docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml` passed; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-log.md --path docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md --path docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md --path docs/plan.md` passed; `bash scripts/ci.sh --mode explicit --path scripts/validation_cache.py --path scripts/test-validation-cache.py` passed selected `validation_cache.regression`; `git diff --check --` passed.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

#### VIC-CR-M2-R1-F1

Finding ID: VIC-CR-M2-R1-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement M2 review-resolution
Required outcome: Local cache hit eligibility must fail closed when the stored cache key is missing or differs from the current computed key, and when the stored validator ID is missing, malformed, unsupported, or different from the first-slice validator ID.
Chosen action: Updated local cache records and contexts to require `cache_key`, `validator_id`, and `command_family`; local cache eligibility now rejects missing, malformed, or mismatched cache keys, unsupported or mismatched validator IDs, and mismatched command families before comparing component hashes.
Rationale: Spec `R11` requires actual validation when any cache-key component is unknown, missing, malformed, unsupported, or changed; accepting records without stored cache key or validator identity can allow unsafe cache skips.
Validation target: Missing or malformed local cache identity fields produce cache misses, while valid matching records still produce cache hits.
Validation evidence: `python scripts/test-validation-cache.py` passed with 20 tests; `python scripts/test-artifact-lifecycle-validator.py` passed with 62 tests; `python scripts/test-select-validation.py` passed with 94 tests; selected CI passed `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, and `validation_cache.regression`; `git diff --check --` passed.

#### VIC-CR-M2-R1-F2

Finding ID: VIC-CR-M2-R1-F2
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement M2 review-resolution
Required outcome: Writing a cache-hit evidence record must preserve existing cache-hit records unless the same stable cache-hit ID is intentionally replaced.
Chosen action: Updated formal cache-hit evidence writing to load and validate an existing `schema_version: 1` evidence file, preserve unrelated `cache_hits`, replace only a matching stable ID, append new IDs, and fail closed on malformed files or duplicate existing IDs.
Rationale: Formal workflow cache-hit evidence is the reviewable trail for skipped validators; overwriting the file can erase earlier formal cache-hit claims.
Validation target: Multiple formal cache-hit evidence records remain reviewable across sequential writes, same-ID replacement is bounded to the matching record, and malformed existing formal evidence fails closed.
Validation evidence: `python scripts/test-validation-cache.py` passed with 20 tests; `python scripts/test-artifact-lifecycle-validator.py` passed with 62 tests; `python scripts/test-select-validation.py` passed with 94 tests; selected CI passed `review_artifacts.validate`, `artifact_lifecycle.regression`, `artifact_lifecycle.validate`, and `validation_cache.regression`; `git diff --check --` passed.

### code-review-m2-r2

No material findings.
