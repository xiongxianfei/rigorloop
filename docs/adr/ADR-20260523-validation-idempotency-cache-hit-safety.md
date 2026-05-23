# ADR-20260523-validation-idempotency-cache-hit-safety: Validation Cache Hits for Unchanged Explicit-Path Lifecycle Inputs

## Status

accepted

## Context

RigorLoop validation is intentionally conservative because validators protect artifact lifecycle, review evidence, change metadata, and workflow readiness. Recent script-output improvements made validation easier to inspect but did not reduce repeated work. Contributors can still rerun the same validator command after unrelated or tiny edits even when the validator's complete input surface has not changed since a prior passing run.

Skipping validators based on edit intent is risky because a wrong classification can hide defects. The approved first slice therefore starts with validation idempotency for one bounded command family: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

The architecture needs a durable decision because this change introduces local cache state, formal cache-hit evidence, validator implementation and policy manifests, closeout evidence-kind rules, and measurement evidence that gates any later edit-scoped validation work.

## Decision

Introduce a validation cache-hit architecture for unchanged explicit-path lifecycle validation inputs.

The first cacheable validator command family is `validate-artifact-lifecycle.py --mode explicit-paths`. A cache hit may reuse only a previous passing result when the normalized command, complete input-surface hash, validator implementation manifest hash, and policy/config manifest hash all match. Any uncertainty, malformed key, missing manifest, changed input, changed implementation, changed policy, unsupported validator, failed prior result, branch/worktree/change-local mismatch, or closeout gate causes the validator to run.

Local execution cache state is untracked, branch-local, worktree-local, and change-local. It may speed repeated local commands but is not lifecycle evidence and is not portable across branches, worktrees, machines, remote caches, shared caches, or CI jobs.

Formal workflow cache-hit evidence lives in `docs/changes/<change-id>/validation-cache-evidence.yaml`. That evidence records why a prior pass still applies, but it is not a new validator pass. Stage and milestone closeout require actual-run evidence in compact `schema_version: 2` change metadata. `cache-hit-inner-loop` may support inner-loop evidence but cannot satisfy closeout. `validate-artifact-lifecycle.py` owns primary closeout rejection for cache-only closeout evidence; `validate-change-metadata.py` owns consistency checks for invalid `change.yaml` evidence references.

Workstream A measurement evidence lives in `docs/changes/<change-id>/validation-cache-measurement.yaml`. It records eligible commands, cache hits, cache misses, disabled cache evaluations, actual runs, estimated time saved, remaining validation cost, closeout actual-run evidence, and whether a follow-on Workstream B proposal is justified. Workstream B edit-scoped validation remains out of scope until that measurement is reviewed and a separate proposal or spec amendment authorizes it.

## Alternatives considered

### Do nothing

Rejected because repeated identical validation remains costly and increases pressure for unsafe ad hoc shortcuts.

### Agent-declared edit-scoped validation

Rejected because self-declared edit classes can be wrong and can skip validators that should have run.

### Diff-derived edit-scoped validation first

Rejected for the first slice because classification mistakes can hide real defects. It may be reconsidered only after Workstream A measurement.

### Cache every validator immediately

Rejected because each validator needs a deterministic input-surface contract and implementation manifest. Starting with one explicit-path lifecycle command keeps the proof surface bounded.

### Tracked cache as the execution source

Rejected because tracked cache state can become noisy or stale. The local execution cache is untracked; tracked change-local evidence records formal cache-hit claims when workflow evidence cites them.

## Consequences

- Validation cache behavior is part of the validation architecture, not a presentation-only optimization.
- Implementation needs deterministic command normalization, repository-relative path normalization, input-surface hashing, implementation manifests, and policy/config manifests.
- Cache-hit evidence becomes a structured change-local evidence class that must avoid secrets, usernames, hostnames, credentials, machine-local absolute paths, and environment dumps.
- Closeout validators must distinguish `actual-run-pass` from `cache-hit-inner-loop` and reject cache-only closeout.
- CI and stage-closeout validation must continue to run actual required closeout bundles in the first slice.
- Workstream A measurement evidence becomes the gate for deciding whether a riskier edit-scoped validation proposal is worthwhile.
- Rollback is simple: disable cache reads and force validators to run. Tracked cache-hit evidence may remain historical inner-loop evidence but cannot be promoted into closeout pass evidence.

## Follow-up

- Update the canonical architecture package to record validation cache state, formal evidence, closeout enforcement, measurement, and Workstream B gating.
- Create architecture-review evidence for this ADR and canonical package update.
- Create the execution plan after architecture-review approves the design.
