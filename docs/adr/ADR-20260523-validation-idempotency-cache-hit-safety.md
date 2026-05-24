# ADR-20260523-validation-idempotency-cache-hit-safety: Validation Cache Hits for Unchanged Explicit-Path Lifecycle Inputs

## Status

accepted

## Context

RigorLoop validation is intentionally conservative because validators protect artifact lifecycle, review evidence, change metadata, and workflow readiness. Recent script-output improvements made validation easier to inspect but did not reduce repeated work. Contributors can still rerun the same validator command after unrelated or tiny edits even when the validator's complete input surface has not changed since a prior passing run.

Skipping validators based on edit intent is risky because a wrong classification can hide defects. The approved first slice therefore starts with validation idempotency for one bounded command family: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

The first observed adoption problem was not cache correctness. The cache was available through opt-in flags, while contributors and agents continued to use the direct explicit-path lifecycle command they already knew. That made cache use dependent on every caller remembering extra context. The approved helper amendment fixes that adoption surface without expanding cache eligibility.

The architecture needs a durable decision because this change introduces local cache state, formal cache-hit evidence, validator implementation and policy manifests, closeout evidence-kind rules, and measurement evidence that gates any later edit-scoped validation work.

## Decision

Introduce a validation cache-hit architecture for unchanged explicit-path lifecycle validation inputs, with a named inner-loop helper mode for adoption.

The first cacheable validator command family is the explicit-path lifecycle command family. It has two command surfaces in this slice:

- direct actual-run lifecycle validation: `validate-artifact-lifecycle.py --mode explicit-paths`;
- cache-aware inner-loop helper validation: `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`.

The helper mode is a user-facing inner-loop command surface, not a separate cacheable validator family. For cache-key computation, prior passing event matching, and input-surface identity, the helper normalizes to the canonical direct `--mode explicit-paths` argv while formal helper cache-hit evidence records both the displayed helper argv and the canonical cache argv. A helper cache hit may reuse a prior direct actual run or a prior helper invocation that fell back to actual validation, but formal helper evidence must trace to an `actual-run-pass`.

A cache hit may reuse only a previous passing result when the normalized canonical command, complete input-surface hash, validator implementation manifest hash, and policy/config manifest hash all match. Any uncertainty, malformed key, missing manifest, changed input, changed implementation, changed policy, unsupported validator, failed prior result, unresolved prior actual run, branch/worktree/change-local mismatch, or closeout gate causes the validator to run.

Local execution cache state is untracked, branch-local, worktree-local, and change-local. It may speed repeated local commands but is not lifecycle evidence and is not portable across branches, worktrees, machines, remote caches, shared caches, or CI jobs.

Formal workflow cache-hit evidence lives in `docs/changes/<change-id>/validation-cache-evidence.yaml`. Helper cache-hit evidence is written or merged only when a safe change root or safe evidence path is supplied or inferable; ad hoc helper use outside that context may print cache status without writing formal evidence. That evidence records why a prior pass still applies, but it is not a new validator pass. Stage and milestone closeout require actual-run evidence in compact `schema_version: 2` change metadata. `cache-hit-inner-loop` may support inner-loop evidence but cannot satisfy closeout. `validate-artifact-lifecycle.py` owns primary closeout rejection for cache-only closeout evidence; `validate-change-metadata.py` owns consistency checks for invalid `change.yaml` evidence references.

Workstream A measurement evidence lives in `docs/changes/<change-id>/validation-cache-measurement.yaml`. It records eligible commands, helper invocations, cache hits, cache misses, disabled cache evaluations, helper actual-run fallbacks, actual runs, closeout actual runs, estimated time saved, remaining validation cost, cache-hit rate, and whether a follow-on Workstream B proposal is justified. Helper cache hits remain separate from closeout actual runs. Workstream B edit-scoped validation remains out of scope until that measurement is reviewed and a separate proposal or spec amendment authorizes it.

## Alternatives considered

### Do nothing

Rejected because repeated identical validation remains costly and increases pressure for unsafe ad hoc shortcuts.

### Agent-declared edit-scoped validation

Rejected because self-declared edit classes can be wrong and can skip validators that should have run.

### Diff-derived edit-scoped validation first

Rejected for the first slice because classification mistakes can hide real defects. It may be reconsidered only after Workstream A measurement.

### Cache every validator immediately

Rejected because each validator needs a deterministic input-surface contract and implementation manifest. Starting with one explicit-path lifecycle command keeps the proof surface bounded.

### Make direct explicit-path lifecycle validation cache-aware by default

Rejected for this adoption slice because direct `--mode explicit-paths` is also the closeout, verify, branch-readiness, PR-readiness, and CI command shape. Making that command cache-aware by default would blur actual-run evidence with inner-loop cache evidence.

### Add a separate wrapper script for the helper

Rejected for the first helper slice. A separate script would create a stronger physical command boundary, but the approved spec chooses one new lifecycle validator mode and pairs it with closeout rejection for `explicit-paths-inner-loop` proof commands.

### Tracked cache as the execution source

Rejected because tracked cache state can become noisy or stale. The local execution cache is untracked; tracked change-local evidence records formal cache-hit claims when workflow evidence cites them.

## Consequences

- Validation cache behavior is part of the validation architecture, not a presentation-only optimization.
- Cache adoption is now part of the command architecture: the helper supplies approved cache context for inner-loop use without requiring callers to remember long cache flag sets.
- Implementation needs deterministic command normalization, repository-relative path normalization, input-surface hashing, implementation manifests, and policy/config manifests.
- Implementation must keep displayed helper argv distinct from canonical direct cache argv in formal evidence.
- Cache-hit evidence becomes a structured change-local evidence class that must avoid secrets, usernames, hostnames, credentials, machine-local absolute paths, and environment dumps.
- Closeout validators must distinguish `actual-run-pass` from `cache-hit-inner-loop` and reject cache-only closeout.
- CI, verify, branch-readiness, PR-readiness, and milestone closeout must continue to use actual-run direct validation in the first slice.
- Workstream A measurement evidence becomes the gate for deciding whether a riskier edit-scoped validation proposal or broader cache eligibility proposal is worthwhile.
- Rollback is simple: disable cache reads and force validators to run. Tracked cache-hit evidence may remain historical inner-loop evidence but cannot be promoted into closeout pass evidence.

## Follow-up

- Canonical architecture package update for the helper mode: recorded in `docs/architecture/system/architecture.md`.
- Create architecture-review evidence for this ADR and canonical package update.
- Create the execution plan after architecture-review approves the design.
