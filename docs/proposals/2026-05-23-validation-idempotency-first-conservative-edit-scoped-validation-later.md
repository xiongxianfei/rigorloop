# Validation Idempotency and Cache-Hit Safety

## Status

accepted

## Problem

Recent output and evidence improvements made validation easier to inspect, but they did not reduce repeated validation work. Contributors still rerun the same validators after tiny lifecycle or evidence edits, even when the validator input surface has not changed since the last passing run.

The tempting fix is "after a small edit, run fewer validators." That is risky. Unlike output compaction, this change affects which validation runs, so a wrong classification can hide a real defect.

The safer first optimization is idempotency/caching:

```text
If a validator's complete input surface is byte-identical to its last passing
run under the same validator implementation and policy key, re-running it adds
cost but no new information.
```

Caching is safer than edit-scoped narrowing because it does not require guessing whether an edit could have affected a validator. It only skips work when the relevant inputs are unchanged.

This proposal separates two ideas:

| Workstream | Purpose | Risk |
| --- | --- | --- |
| A: validation idempotency/cache hits | Skip rerunning validators whose input surfaces are unchanged since the last passing run. | Lower; safe by construction if the input surface is complete. |
| B: edit-scoped validation | Use diff-derived edit classes to run a subset of validators during inner-loop edits. | Higher; misclassification can skip a needed check. |

The proposal leads with Workstream A. Workstream B is explicitly gated on measurement after A.

## Goals

- Reduce redundant validator reruns without weakening defect detection.
- Lead with idempotency/caching before edit-scoped validation.
- Define a validator input-surface hash contract.
- Allow cache hits only for previous passing results.
- Include validator implementation identity, command arguments, policy/config, and relevant input files in the cache key.
- Default to running the validator on any uncertainty.
- Preserve full validation at lifecycle and stage closeout.
- Measure remaining validation cost after caching before deciding whether edit-scoped narrowing is worth the risk.
- Keep validation semantics, selected checks, exit codes, failure detection, and required evidence unchanged.

## Non-goals

- Do not replace stage-closeout full-bundle validation.
- Do not skip validation because an agent or contributor says an edit is "prose-only."
- Do not use self-declared edit labels as authority.
- Do not reduce mixed-edit validation below the union of all affected classes.
- Do not cache failed validator results as successful.
- Do not reuse a cache entry after validator code, command arguments, policy, config, or input files change.
- Do not change what any validator checks.
- Do not change validator exit semantics.
- Do not hide failures, blockers, stale readiness, or review-record drift.
- Do not make caching mandatory for every validator in the first slice.
- Do not proceed to edit-scoped narrowing until caching impact is measured.

## Vision fit

fits the current vision

RigorLoop's validation model exists to make artifact-driven work safe to inspect, review, and advance. This proposal improves efficiency only where validation evidence is provably identical to a prior passing run.

The proposal is falsified if any of these occur:

```text
- a real defect ships because a validator was skipped;
- a cache hit is accepted when any input surface changed;
- a validator implementation change reuses an old cache result;
- a stage closes without full-bundle validation evidence;
- a mixed edit runs less than the union of its triggered checks;
- reduced validation passes something full validation would have failed;
- cache metadata is not reviewable enough to explain why a validator did not run.
```

The governing principle:

```text
Validation scope may be reduced only when the reduction cannot skip a check
that the edit or changed input could have broken.

On uncertainty, run more.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Lead with caching/idempotency | in scope | Recommended direction, Workstream A |
| Avoid unsafe validator skipping | in scope | Non-goals, Vision fit |
| Treat scope narrowing as riskier | in scope | Workstream B |
| Derive edit classification from actual diff | deferred follow-up | Workstream B |
| Use union of checks for mixed edits | deferred follow-up | Workstream B |
| Enforce full bundle at closeout | in scope | Stage-closeout gate |
| Measure before expanding optimization | in scope | Measurement gate |
| Preserve validation behavior | in scope | Behavior-preservation proof |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Workstream A validation idempotency/cache hits | core to this proposal | It is the recommended policy direction and the only first-slice optimization. |
| Cache key and input-surface contract | first-slice candidate | Cache safety depends on stable command, implementation, policy, and input identity. |
| Cache-hit evidence | first-slice candidate | Skipped validation needs reviewable evidence explaining why the prior pass still applies. |
| Stage-closeout full-bundle preservation | same-slice dependency | Inner-loop optimization must not replace lifecycle completion proof. |
| Measurement after Workstream A | same-slice dependency | Workstream B should be decided from observed remaining cost, not assumed benefit. |
| Workstream B diff-derived edit-scoped validation | separate proposal | Scope narrowing has different safety risks and should wait for Workstream A measurements. |
| Shared or remote validation cache | deferable follow-up | First-slice value should be proven locally before widening persistence or sharing. |
| Full validator fleet caching | separate implementation slice | Each cacheable validator needs a deterministic input-surface contract. |
| Stage-closeout cache eligibility | separate proposal | The recommended first-slice rule is to run closeout bundles rather than cache-skip them. |

## Context

The remaining validation-efficiency slice is different in kind from output/routing work because it changes whether a validator runs. Compacting output cannot cause a real failure to go undetected, but skipping a validator can.

Recent slices optimized how validation evidence is presented, routed, or queried. This proposal optimizes validation execution itself, so the design is conservative by default.

## Options considered

### Option 1: Do nothing

Keep rerunning full validation bundles during inner-loop edits.

Pros:

- Safest behavior.
- No validator cache complexity.
- No risk of stale cache use.

Cons:

- Repeated identical validation costs remain.
- Contributors spend time rechecking unchanged inputs.
- Pressure grows to use unsafe ad hoc shortcuts.

### Option 2: Agent-declared edit-scoped validation

Let the agent say "this was a prose-only edit" and run a smaller validator subset.

Pros:

- Simple.
- Potentially large speedup.

Cons:

- Unsafe; self-declared edit classes can be wrong.
- A readiness or status line can be mislabeled as prose.
- Mixed edits can be under-validated.
- Prior review history shows self-declared categories are a recurring failure mode.

Rejected.

### Option 3: Diff-derived edit-scoped validation first

Compute edit classes from the actual diff and run only the owning validator subset.

Pros:

- Better than self-declaration.
- Can reduce work after small edits.
- Can be testable with fixtures.

Cons:

- Still risky.
- Requires a complete edit-class mapping.
- Mixed edits need union checks.
- Misclassification can hide a defect.
- Requires strong full-bundle closeout gates.

Deferred until after caching measurement.

### Option 4: Idempotency/cache hits first

Skip validator reruns only when the validator input surface is byte-identical to the last passing run under the same command, validator implementation, and policy key.

Pros:

- Safer by construction.
- Does not require classifying edit intent.
- Catches the repeated unchanged-input case.
- Easy to invalidate on input or implementation change.
- Can coexist with full-bundle closeout gates.

Cons:

- Requires defining complete input surfaces.
- Requires cache metadata and cache-hit evidence.
- Does not skip validators whose input surface changed, even if the change is harmless.

Recommended first.

### Option 5: Idempotency first, then gated edit-scoped validation if still worth it

Implement caching first, measure remaining cost, then decide whether to add diff-derived scope narrowing.

Pros:

- Captures safer optimization first.
- Keeps risky narrowing optional and evidence-gated.
- Separates proof surfaces.
- Preserves conservative-by-default behavior.

Cons:

- More lifecycle overhead than a single broad change.
- May require two implementation waves.

Recommended overall direction.

## Recommended direction

Choose Option 5, with Workstream A implemented first.

```text
Workstream A:
  validation idempotency/cache hits for unchanged validator input surfaces

Measurement gate:
  quantify remaining repeated validation cost after Workstream A

Workstream B:
  optional diff-derived edit-scoped validation, only if still justified
```

Do not start Workstream B until Workstream A has shipped, measured cache-hit value, and shown that remaining validation cost justifies the added risk.

The first implementing spec covers validation idempotency/cache hits only. Edit-scoped validation is follow-on design context and should not be implemented until Workstream A measurement is reviewed and a separate owner decision authorizes a follow-on proposal or spec amendment.

Priority order:

```text
1. preserve defect-detection parity with full validation
2. preserve stage-closeout full-bundle gates
3. implement safe idempotency/cache hits for unchanged inputs
4. measure remaining validation cost
5. consider edit-scoped validation only after caching evidence
```

## Workstream A: Validation Idempotency/Cache Hits

A validator may be skipped by cache only when all of these are true:

```text
- the previous result was pass;
- the validator command is identical;
- validator implementation identity is identical;
- validator policy/config identity is identical;
- the complete input surface hash is identical;
- the cache entry is not expired or invalidated;
- the current stage is not a required full-bundle closeout gate.
```

If any element is unknown, missing, changed, or unsupported:

```text
run the validator
```

A cache key should include:

| Component | Meaning |
| --- | --- |
| Validator ID | Stable name, for example `artifact-lifecycle`, `change-metadata`, or `review-artifacts`. |
| Command argv | Exact command and arguments after normalization. |
| Validator implementation hash | Hash from the deterministic validator implementation manifest. |
| Policy/config hash | Relevant spec version, config file, registry, or schema hash. |
| Input surface hash | Hash of all files and values the validator reads for the command. |
| Environment policy key | Only if the validator depends on meaningful environment variables. |
| Repository version context | Commit or tree hash when useful; this should not replace explicit input hashes. |

Cache keys should not include secrets, hostnames, machine-local paths, usernames, or credentials.

Each cacheable validator should declare its input surface. Examples:

| Validator | Input surface examples |
| --- | --- |
| `validate-change-metadata.py <change.yaml>` | `change.yaml`, referenced review log/resolution when counts are validated, relevant schema and semantics code. |
| `validate-artifact-lifecycle.py --mode explicit-paths ...` | Every explicit path, lifecycle validation code, lifecycle policy/config. |
| `validate-review-artifacts.py --mode closeout <change-root>` | Review records, review log, review resolution, parser code, closeout policy. |
| `validate-skills.py skills/<skill>/SKILL.md` | Skill file, referenced skill-local assets if validator checks them, skill validation code/policy. |

Input-surface rules:

```text
- If the input surface cannot be declared deterministically, the validator is
  not cacheable in Workstream A.
- If a validator discovers additional inputs dynamically, those discovered
  inputs are recorded before the result is cacheable.
- Missing files are part of the input surface state.
- File content hashes, not timestamps, determine identity.
```

A passing validation cache record should contain:

```yaml
validator_cache_entry:
  validator_id: artifact-lifecycle
  command: python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
  result: pass
  input_surface_hash: sha256:<hash>
  validator_implementation_hash: sha256:<hash>
  policy_hash: sha256:<hash>
  created_at: <timestamp or commit-local event>
  evidence:
    prior_validation_event: <stage or validation ID>
    input_surface_manifest: <path or inline summary>
```

## Cache storage decision

First-slice cache storage has two layers:

1. Local execution cache:
   - may be untracked;
   - may be deleted at any time;
   - accelerates repeated local commands;
   - is not itself lifecycle evidence.
2. Change-local cache-hit evidence:
   - required whenever a cache hit is cited in formal workflow validation;
   - lives at `docs/changes/<change-id>/validation-cache-evidence.yaml`;
   - records validator ID, normalized command, input-surface hash, implementation hash, policy hash, prior passing event, and cache-hit reason;
   - must not contain secrets, hostnames, credentials, usernames, machine-local absolute paths, or private environment dumps.

A cache hit is evidence that a prior pass still applies. It is not a new passing validator run. Untracked local cache state is never the sole evidence for a skipped validator in a formal workflow claim.

Recommended first-slice evidence shape:

```yaml
schema_version: 1
change_id: <change-id>
cache_hits:
  - id: cache-hit-001
    validator_id: artifact-lifecycle
    command:
      argv:
        - python
        - scripts/validate-artifact-lifecycle.py
        - --mode
        - explicit-paths
    prior_passing_event:
      stage: code-review-m3-r1
      evidence: docs/changes/<change-id>/change.yaml#validation-events
    cache_key:
      input_surface_hash: sha256:<hash>
      validator_implementation_hash: sha256:<hash>
      policy_hash: sha256:<hash>
      command_hash: sha256:<hash>
    result_reused: pass
    allowed_reason: input surface, validator implementation, policy, and command unchanged since prior passing event
    scope: inner-loop
    closeout_evidence: false
```

`behavior-preservation.md` may summarize cache hits, but it should point to `validation-cache-evidence.yaml` rather than becoming the authoritative structured cache-hit evidence surface.

When a validator is skipped due to cache, record a bounded cache-hit line:

```text
[CACHE HIT] artifact-lifecycle: input surface unchanged since code-review-m3-r1; prior result pass; key sha256:<short>
```

For formal lifecycle evidence, include:

```text
- validator ID;
- command;
- cache key or short hash;
- prior passing validation event;
- input surface hash;
- reason cache hit is allowed;
- full-bundle closeout still required when applicable.
```

A cache hit is not a new passing validation result. It is evidence that a previous pass still applies.

## First validator decision

The first cacheable validator is:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

Only explicit-path invocations are cache-eligible in the first slice.

The cacheable input surface is:

- normalized command argv;
- ordered explicit path list;
- content hash or missing-file marker for each explicit path;
- validator implementation manifest;
- lifecycle policy/config/spec hash.

`validate-change-metadata.py` is deferred until a later slice because compact metadata, path variables, review-artifact counts, and referenced artifacts make its input surface more dynamic.

## Validator implementation manifest

For first-slice cache eligibility, implementation identity is computed from a deterministic manifest. The manifest is generated, not hand-maintained.

The manifest includes:

- the validator entrypoint file;
- all resolved repository-local imports and helper modules imported directly or transitively by the validator;
- shared semantics/parser modules used by the validator;
- validator-owned schema/config/policy files.
- manifest-generation logic identity.

For the first cacheable validator, the manifest includes four groups:

1. Entrypoint:
   - `scripts/validate-artifact-lifecycle.py`.
2. Repository-local imports and helper modules:
   - every repository-local `.py` file resolved from the validator import graph;
   - no standard-library modules;
   - no third-party package source files.
3. Governing lifecycle policy/spec/config files:
   - `CONSTITUTION.md`;
   - `docs/workflows.md`;
   - `specs/plan-index-lifecycle-ownership.md`;
   - any lifecycle-related spec explicitly referenced by the validator or active plan.
4. Manifest-generation logic identity:
   - the repository file that owns cache/manifest computation, such as `scripts/validation_cache.py`.

Missing optional policy files are recorded as explicit missing-file markers. Missing-file state is part of the manifest identity.

If the implementation cannot determine this manifest deterministically, the validator is not cache-eligible.

A manually maintained version stamp may be recorded as additional evidence, but it does not replace source-file and policy/config hashes in the first slice.

## Stage-closeout Gate

Focused cache hits are allowed only inside a stage or milestone. They should not replace a required stage-closeout full-bundle run.

Recommended first-slice rule:

```text
Do not cache-skip stage-closeout full bundles.
```

This keeps Workstream A safe and easy to reason about.

## Closeout enforcement

A stage or milestone closeout validation record must include actual validator execution evidence for the required full bundle.

A cache-hit entry may appear as supporting inner-loop evidence, but it does not satisfy closeout by itself.

Primary rejection owner:

```text
scripts/validate-artifact-lifecycle.py
```

Secondary consistency owner:

```text
scripts/validate-change-metadata.py
```

`validate-artifact-lifecycle.py` owns lifecycle closeout validity and rejects a milestone or stage closeout whose required full-bundle evidence is represented only by cache hits. `validate-change-metadata.py` rejects invalid formal evidence references in `change.yaml`, such as a closeout validation event claiming `pass` while pointing only to cache-hit evidence.

Accepted closeout evidence values:

```text
actual-run-pass
actual-run-fail
blocked
```

Cache evidence value:

```text
cache-hit-inner-loop
```

`cache-hit-inner-loop` is not a closeout pass value.

Example invalid closeout:

```yaml
validation_events:
  - stage: code-review-m3-closeout
    lifecycle_stage: code-review
    result: pass
    evidence_kind: cache-hit-inner-loop
    evidence_ref: validation-cache-evidence.yaml#cache-hit-001
```

Expected result:

```text
validation fails: closeout requires actual-run-pass evidence
```

Example valid inner-loop cache hit plus closeout run:

```yaml
validation_events:
  - stage: code-review-m3-inner-loop
    lifecycle_stage: code-review
    result: pass
    evidence_kind: cache-hit-inner-loop
    evidence_ref: validation-cache-evidence.yaml#cache-hit-001

  - stage: code-review-m3-closeout
    lifecycle_stage: code-review
    result: pass
    evidence_kind: actual-run-pass
    command: python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

Expected result:

```text
valid
```

## Local cache lifetime

First-slice validation cache is branch-local, worktree-local, and change-local.

The local cache accelerates repeated commands in one repository working context. It is not portable evidence and should not be copied across branches, worktrees, machines, CI jobs, remote stores, or shared caches.

A local cache entry may be considered only when all of these match:

```text
- repository root identity;
- current Git branch name;
- current worktree path identity, stored as a non-exported local key only;
- change ID, when running in a workflow-managed change;
- normalized validator command;
- validator implementation manifest hash;
- policy/config manifest hash;
- complete input-surface hash;
- previous result was pass.
```

Formal evidence must not expose local machine details. Worktree absolute paths may be stored only in the untracked local cache when needed for local invalidation; they must not appear in tracked evidence.

Cache entries may be deleted at any time. A time TTL can expire otherwise-valid entries, but TTL does not make an entry valid; hash/key equality and prior passing result are the correctness boundary.

## Measurement Gate After Workstream A

Before Workstream B is authorized, record:

```text
- total validation commands during representative milestone loops;
- number of cache hits;
- time saved by cache hits;
- validators still rerun despite unchanged practical relevance;
- remaining cases where edit-scoped narrowing might help;
- defects caught by full closeout despite inner-loop cache hits.
```

If caching removes most redundant cost, Workstream B should be deferred or rejected.

## Workstream B: Guarded Edit-Scoped Validation

Workstream B is not part of the first implementation slice unless approved later.

If pursued, edit classes should be computed from:

```text
- changed paths;
- changed content;
- structured diff patterns;
- parser-owned lifecycle/status fields where relevant.
```

They should not be based on an agent's claimed intent.

Forbidden:

```text
agent says "prose-only" -> skip lifecycle validation
```

Required:

```text
diff shows which files and fields changed -> derive classes -> run union checks
```

Each edit class maps to a set of validators. Example sketch:

| Edit class | Trigger | Required validators |
| --- | --- | --- |
| Change metadata edit | `docs/changes/*/change.yaml` changed | Change metadata validator; lifecycle if paths/status are affected. |
| Review artifact edit | `review-log.md`, `review-resolution.md`, `reviews/*.md` changed | Review-artifact validator; lifecycle validator. |
| Plan lifecycle edit | `docs/plan.md` or active plan handoff/status changed | Artifact lifecycle or plan-index validator. |
| Skill edit | `skills/**/SKILL.md` or skill asset changed | Skill validator; generated output checks when required. |
| Validator code edit | `scripts/validate-*.py`, shared semantics modules | Affected validator tests; full relevant validation bundle. |

Mixed edits use:

```text
union of all triggered validators
```

If classification is unknown, ambiguous, unsupported, or conflicts with another signal:

```text
run full relevant bundle
```

For representative edit fixtures, reduced validation should catch every defect that full validation catches. If any reduced-scope fixture passes while full-scope validation fails, Workstream B is unsafe and should not ship.

## Expected behavior changes

After Workstream A:

- Repeated validator commands with unchanged input surfaces can be skipped by cache.
- Cache hits are visible and reviewable.
- Full closeout validation still runs.
- Validator behavior and failure detection do not change.
- Validation runtime decreases for repeated unchanged surfaces.

After possible Workstream B:

- Inner-loop edits may run a smaller validator subset only when diff-derived classification is complete and conservative.
- Mixed edits run union validators.
- Uncertain edits run full validation.

## Architecture impact

| Surface | Impact |
| --- | --- |
| Validation runners | May consult cache manifests before executing eligible validators. |
| Validator scripts | Need declared input-surface manifests or helper APIs. |
| Change metadata/evidence | May record cache-hit evidence or cache manifest references. |
| Selector/CI wrapper | May expose cache-hit status while preserving failure behavior. |
| Test specs | Need cache-key, invalidation, and closeout-gate tests. |
| Existing validators | No semantic change to what they validate. |
| Workflow skills | May need guidance that cache hits are inner-loop optimization, not closeout approval. |

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `VIC-001` | Validator cache key includes command, implementation hash, policy hash, and input surface hash. |
| `VIC-002` | Cache hit occurs only after a previous pass. |
| `VIC-003` | Failed validator results are not reused as passes. |
| `VIC-004` | Changed input file invalidates cache. |
| `VIC-005` | Changed validator code invalidates cache. |
| `VIC-006` | Changed validator policy/config invalidates cache. |
| `VIC-007` | Missing or undeclared input surface disables caching. |
| `VIC-008` | Cache-hit evidence names prior passing validation event and input hash. |
| `VIC-009` | Stage-closeout full bundle still runs and is not replaced by cache hits. |
| `VIC-010` | Cache manifest contains no secrets, hostnames, machine-local paths, or credentials. |
| `VIC-011` | Measurement report records cache-hit rate and time saved. |
| `VIC-012` | Workstream B is blocked unless Workstream A measurement is recorded. |
| `VIC-013` | Formal workflow cache hits are reviewable from change-local evidence. |
| `VIC-014` | Untracked local cache state is never the sole evidence for a skipped validator. |
| `VIC-015` | A milestone closeout record with only cache-hit evidence fails validation. |
| `VIC-016` | A milestone closeout record with actual full-bundle pass evidence can include cache-hit evidence as supporting context. |
| `VIC-017` | Changing the validator entrypoint invalidates the cache. |
| `VIC-018` | Changing a helper module invalidates the cache. |
| `VIC-019` | Changing a policy/config/spec file invalidates the cache. |
| `VIC-020` | An unresolved implementation manifest disables caching. |
| `VIC-021` | `validate-artifact-lifecycle.py` rejects cache-only closeout evidence. |
| `VIC-022` | `validate-change-metadata.py` rejects `change.yaml` closeout references that promote cache hits into pass evidence. |
| `VIC-023` | Local cache reuse is blocked across branch, worktree, change ID, remote/shared cache, and CI-job boundaries. |

Suggested validation commands for the eventual plan:

```bash
python scripts/test-validation-cache.py
python scripts/test-select-validation.py
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check --
```

Use repository-owned command names once the spec and test spec name the implementation surface.

## Behavior-preservation proof

The downstream change should create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| Validator pass behavior | Baseline command output | Post-cache command output | unchanged |
| Validator fail behavior | Failing fixture | Post-cache failing fixture | unchanged |
| Input changed | Previous pass plus changed file | Cache invalidated and validator runs | preserved |
| Validator code changed | Previous pass plus validator edit | Cache invalidated and validator runs | preserved |
| Failed prior result | Failed validation event | No cache pass accepted | preserved |
| Stage closeout | Full bundle before | Full bundle after | preserved |
| Cache evidence | None | Cache-hit record | reviewable and bounded |

For any Workstream B pilot:

| Surface | Baseline proof | Reduced proof | Required result |
| --- | --- | --- | --- |
| Metadata defect fixture | Full validation fails | Reduced validation fails | parity |
| Review-log drift fixture | Full validation fails | Reduced validation fails | parity |
| Plan state drift fixture | Full validation fails | Reduced validation fails | parity |
| Mixed edit fixture | Full validation runs union | Reduced validation runs union | parity |

## Proof route

This proposal requires a first-slice spec for validation idempotency/cache hits only.

Workstream B, edit-scoped validation, is not part of the first implementing spec or test spec. It may be described as a follow-on safety model, but it must not be implementable until Workstream A measurement is reviewed and an explicit owner decision authorizes a separate follow-on proposal or spec amendment.

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Write spec for validation idempotency and cache-hit safety.
3. Write test spec for cache keys, invalidation, and closeout gates.
4. Implement cache key and input-surface manifest for `validate-artifact-lifecycle.py --mode explicit-paths`.
5. Record cache-hit evidence.
6. Measure cache-hit rate and time saved.
7. Decide whether to expand to more validators.
8. Decide separately whether Workstream B is justified.
9. Only after measurement, consider diff-derived edit-scoped validation.

Rollback:

- Disable cache reads and force validators to run.
- Keep cache records as historical evidence if harmless.
- Revert cache manifest parsing if it creates ambiguity.
- Do not change validator semantics during rollback.
- Do not remove full-bundle closeout gates.
- Do not convert cached passes into durable stage-closeout evidence after rollback.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Incomplete input surface causes stale cache hit. | Cache only validators with declared deterministic input surfaces; default to run. |
| Validator code changes but cache still hits. | Include validator implementation hash. |
| Policy/config changes but cache still hits. | Include policy/config hash. |
| Failed result is reused. | Cache only passing results. |
| Cache hit is mistaken for closeout validation. | Stage-closeout full-bundle gate remains mandatory. |
| Agent self-declares edit class. | Workstream B requires diff-derived classification only. |
| Mixed edit under-validates. | Use the union of triggered validators. |
| Scope narrowing hides a defect. | Use defect-detection parity fixtures; defer Workstream B until after Workstream A measurement. |
| Cache metadata leaks environment info. | Store repository-relative paths and hashes only; reject secrets and machine-local paths. |
| Cache complexity exceeds benefit. | Use the measurement gate; stop after Workstream A if savings are low. |

## First-slice boundary

First implementation slice:

```text
Workstream A only
validate-artifact-lifecycle.py --mode explicit-paths only
cache-key computation
input-surface manifest
cache-hit evidence
cache invalidation tests
stage-closeout full-bundle preservation tests
measurement report
```

Out of scope for first slice:

```text
edit-scoped validation
self-declared edit classes
full validator fleet caching
historical cache migration
remote/shared cache
cache persistence across machines
workflow closeout replacement
changed-path selector semantics changes
```

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-VIC-001` | Cache hits are allowed only for previous passing validator results. |
| `AC-VIC-002` | Cache key includes command, validator implementation identity, policy/config identity, and complete input-surface hash. |
| `AC-VIC-003` | Any changed input-surface file invalidates the cache. |
| `AC-VIC-004` | Any changed validator implementation invalidates the cache. |
| `AC-VIC-005` | Any changed policy/config input invalidates the cache. |
| `AC-VIC-006` | Validators without deterministic input-surface manifests are not cache-eligible. |
| `AC-VIC-007` | Cache-hit evidence records prior passing event, validator ID, command, and input-surface hash. |
| `AC-VIC-008` | Cache-hit evidence contains no secrets, hostnames, credentials, machine-local paths, or private environment dumps. |
| `AC-VIC-009` | Stage-closeout full-bundle validation still runs in the first slice. |
| `AC-VIC-010` | Validator pass/fail behavior is unchanged when the validator actually runs. |
| `AC-VIC-011` | Measurement report records cache-hit count, cache-miss count, and time saved. |
| `AC-VIC-012` | Workstream B does not begin until Workstream A measurement is reviewed. |
| `AC-VIC-013` | First-slice cache eligibility applies only to `validate-artifact-lifecycle.py --mode explicit-paths`. |
| `AC-VIC-014` | Formal workflow cache hits are reviewable from change-local evidence. |
| `AC-VIC-015` | Untracked local cache state is never the sole evidence for a skipped validator. |
| `AC-VIC-016` | Implementation identity uses a deterministic source/policy manifest; manual version stamps may supplement but not replace source and policy hashes. |
| `AC-VIC-017` | A milestone closeout record with only cache-hit evidence fails validation. |
| `AC-VIC-018` | A milestone closeout record with actual full-bundle pass evidence can include cache-hit evidence as supporting context. |
| `AC-VIC-019` | Formal cache-hit evidence is recorded in `docs/changes/<change-id>/validation-cache-evidence.yaml`. |
| `AC-VIC-020` | The implementation manifest includes the validator entrypoint, all resolved repository-local imports/helpers, governing lifecycle policy/spec/config files, and the manifest generator identity. |
| `AC-VIC-021` | `validate-artifact-lifecycle.py` owns cache-only closeout rejection, with `validate-change-metadata.py` owning consistency checks for `change.yaml` evidence references. |
| `AC-VIC-022` | Local cache entries are branch-local, worktree-local, and change-local only, with no cross-branch, cross-worktree, remote, shared, or CI cache reuse in the first slice. |

## Follow-on gate

If Workstream B is later proposed, it should satisfy these follow-on gates before implementation:

| ID | Criterion |
| --- | --- |
| `FG-VIC-001` | Workstream A measurement has been recorded and reviewed. |
| `FG-VIC-002` | An explicit owner decision authorizes a separate follow-on proposal or spec amendment. |
| `FG-VIC-003` | Edit classes are derived from actual diffs, not agent declarations. |
| `FG-VIC-004` | Mixed edits run the union of all triggered validators. |
| `FG-VIC-005` | Reduced validation catches every defect caught by the full-bundle fixtures. |

## Open questions

None for first-slice proposal readiness.

The first-slice spec should still define exact YAML field names, manifest-generation implementation details, and fixture names before implementation.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-23 | Lead with validation idempotency/caching. | Safer than edit-scoped narrowing because unchanged inputs make skip safety provable. | Start with edit-scoped validation. |
| 2026-05-23 | Treat edit-scoped validation as guarded follow-up. | Misclassification can hide real defects. | Implement both in one first slice. |
| 2026-05-23 | Require full-bundle closeout gate. | Focused validation is an inner-loop optimization, not lifecycle completion proof. | Let cache hits replace closeout. |
| 2026-05-23 | Derive any future edit class from actual diff. | Self-declared categories are unsafe. | Trust agent-declared prose-only labels. |
| 2026-05-23 | Use union checks for future mixed edits. | Mixed edits can break multiple surfaces. | Choose a primary edit class. |
| 2026-05-23 | Measure after caching before Workstream B. | Caching may remove enough wasted cost to make riskier narrowing unnecessary. | Commit to scope narrowing before data. |
| 2026-05-23 | Limit the first implementing spec to validation idempotency/cache hits. | Keeps Workstream B from becoming implementable before measurement. | Specify cache hits and edit-scoped validation together. |
| 2026-05-23 | Use local untracked cache plus change-local formal cache-hit evidence. | Separates execution speed from reviewable lifecycle evidence. | Treat untracked cache state as sufficient formal evidence. |
| 2026-05-23 | Start with `validate-artifact-lifecycle.py --mode explicit-paths`. | Its input surface is easier to bound than dynamic metadata validation. | Start with `validate-change-metadata.py`. |
| 2026-05-23 | Require deterministic implementation manifests. | Manual stamps can miss helper or policy changes. | Use a version stamp as the first-slice identity fallback. |
| 2026-05-23 | Make closeout full-bundle evidence mechanically checkable. | Cache hits are inner-loop evidence, not closeout passes. | Rely on prose guidance only. |
| 2026-05-23 | Use `validation-cache-evidence.yaml` for formal cache-hit evidence. | Structured cache-hit claims need machine-checkable reviewable data. | Use `behavior-preservation.md` as the authoritative evidence surface. |
| 2026-05-23 | Make `validate-artifact-lifecycle.py` the primary cache-only closeout rejection owner. | Lifecycle closeout validity belongs with lifecycle validation. | Leave closeout rejection owner unspecified. |
| 2026-05-23 | Make local cache branch-local, worktree-local, and change-local only. | Prevents first-slice cache reuse across contexts that are harder to reason about. | Cross-branch, cross-worktree, remote, shared, or CI cache reuse. |

## Next artifacts

```text
proposal-review
spec: validation idempotency and cache-hit safety
spec-review
test-spec
plan
plan-review
implementation milestones
code-review
explain-change
verify
pr
```

Potential later proposals, if justified by Workstream A evidence:

- Diff-derived edit-scoped validation.
- Shared validation input-surface manifests across all validators.
- Remote or cross-branch validation cache.
- Validator cache visualization in change metadata or query helper.
- Full-bundle closeout cache eligibility.

## Follow-on artifacts

- `specs/validation-idempotency-and-cache-hit-safety.md`

## Readiness

Accepted after `proposal-review-r2`; downstream spec created at `specs/validation-idempotency-and-cache-hit-safety.md`.

## Core invariant

```text
Caching is allowed only when validation inputs are unchanged and the previous
result was a pass.

Validation scope narrowing is not the first slice. If it is ever added, it must
be diff-derived, union-safe for mixed edits, conservative on uncertainty, and
proven to catch every defect the full bundle would catch.

Focused validation may speed the inner loop, but it does not replace the
stage-closeout full-bundle gate.
```
