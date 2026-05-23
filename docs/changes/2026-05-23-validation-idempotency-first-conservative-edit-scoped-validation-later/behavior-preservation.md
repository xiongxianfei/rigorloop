# Validation Cache Behavior Preservation

## Status

active

## Scope

This artifact records behavior-preservation proof for M2 of validation idempotency and cache-hit safety.

M2 adds opt-in local cache lookup for:

```text
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

The underlying lifecycle validator still performs the same checks whenever it actually runs. Cache support is not enabled for other modes, closeout context, CI, or unsupported validator commands.

## M2 preservation matrix

| Surface | Baseline proof | M2 proof | Preservation result |
| --- | --- | --- | --- |
| Actual pass behavior | Existing explicit-path lifecycle validator tests | `test_cli_cache_hits_on_second_identical_explicit_path_run` first run returns normal `validated ... explicit-paths mode` output before any cache hit | unchanged actual-run pass behavior |
| Actual fail behavior | Existing artifact lifecycle failing fixtures | M2 does not change `artifact_lifecycle_validation.validate_repository`; cache integration is confined to the CLI wrapper and only stores records after a pass | unchanged actual-run failure detection |
| Cache hit behavior | none before M2 | Second identical opt-in explicit-path CLI run emits bounded `[CACHE HIT] artifact-lifecycle` output and exits successfully | prior pass reused only after matching cache identity |
| Changed input | M1 content-hash input-surface tests | M2 cache identity recomputes the complete input-surface hash before lookup | cache miss and actual run required |
| Validator/helper changed | M1 strict implementation-manifest tests | `test_cache_lookup_misses_after_helper_or_policy_change` proves helper changes miss local cache | cache miss and actual run required |
| Policy changed | M1 policy manifest tests | `test_cache_lookup_misses_after_helper_or_policy_change` proves policy changes miss local cache | cache miss and actual run required |
| Failed prior result | M1 local-cache eligibility test | `test_local_cache_store_reuses_only_matching_prior_pass` proves failed records are not cache hits | failed prior result is not reused |
| Formal cache-hit evidence | none before M2 | `test_formal_cache_hit_evidence_file_has_required_shape` writes `validation-cache-evidence.yaml` shape without local worktree details | structured and reviewable when requested |
| Closeout behavior | stage closeout required actual validation before M2 | M2 cache lookup is disabled when `--validation-cache-context closeout` is used | cache hits remain inner-loop only |

## Formal cache-hit evidence

M2 provides the writer for:

```text
docs/changes/<change-id>/validation-cache-evidence.yaml
```

This change does not cite a formal cache hit as lifecycle evidence. The M2 tests exercise the evidence writer in a temporary fixture so no durable workflow cache-hit claim is recorded for this change.
