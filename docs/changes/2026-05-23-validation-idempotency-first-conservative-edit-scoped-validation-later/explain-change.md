# Explain Change: Validation Idempotency and Cache-Hit Safety

## Summary

This change adds the first Workstream A slice of validation idempotency for RigorLoop:

- deterministic cache identity primitives for explicit-path lifecycle validation;
- opt-in local cache hits for `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`;
- formal cache-hit evidence writing;
- compact metadata enforcement that prevents cache hits from satisfying closeout;
- Workstream A measurement evidence and selector routing for cache evidence files.

The change intentionally does not implement Workstream B edit-scoped validation or changed-path validator narrowing.

## Problem

Contributors rerun the same validators after small lifecycle or evidence edits even when a validator's complete input surface has not changed since the last passing run. The risky shortcut would be to classify edits as "small" and run fewer validators. The accepted direction is safer: skip only when the validator command, implementation identity, policy/config identity, and complete input surface are unchanged from a prior passing result.

## Decision Trail

| Decision point | Outcome | Source |
| --- | --- | --- |
| Proposal | Lead with validation idempotency/cache hits; defer edit-scoped validation. | `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md` |
| First-slice scope | Cache eligibility applies only to explicit-path lifecycle validation. | `specs/validation-idempotency-and-cache-hit-safety.md` R1-R3 |
| Cache safety rule | On missing, malformed, unsupported, changed, or unknown cache identity, run the validator. | Spec R4-R12 |
| Input and implementation identity | Hash normalized command, ordered paths, content or missing markers, deterministic implementation manifest, and policy manifest. | Spec R13-R31, R78-R100 |
| Evidence model | Local execution cache is not lifecycle evidence; formal cache-hit claims use change-local evidence. | Spec R32-R48, architecture/ADR |
| Closeout safety | `cache-hit-inner-loop` is supporting evidence only; closeout requires actual-run evidence. | Spec R49-R59, R101-R116 |
| Measurement gate | Record Workstream A measurement before any Workstream B follow-up. | Spec R75-R77, R117-R130 |
| Plan milestones | M1 cache identity, M2 lifecycle integration, M3 closeout metadata, M4 measurement/routing. | `docs/plans/2026-05-23-validation-idempotency-cache-hit-safety.md` |

Material review findings were resolved before downstream use:

- Proposal review R1: `VIC-PR1` through `VIC-PR5` accepted and closed.
- Spec review R1: `VIC-SR1` through `VIC-SR3` accepted and closed.
- Code review M1 R1: `VIC-CR-M1-R1-F1` accepted and closed.
- Code review M2 R1: `VIC-CR-M2-R1-F1` and `VIC-CR-M2-R1-F2` accepted and closed.

See `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md`.

## Diff Rationale by Area

| Area | Files | Why changed | Requirement/test link |
| --- | --- | --- | --- |
| Cache identity primitives | `scripts/validation_cache.py`, `scripts/test-validation-cache.py` | Added normalized command hashing, explicit-path input-surface hashing, deterministic implementation and policy manifests, local cache context, strict cache-key matching, and formal evidence writing. | R1-R31, R60-R72, R78-R100; VIC-T001 through VIC-T014 |
| Lifecycle cache integration | `scripts/validate-artifact-lifecycle.py`, `.gitignore` | Added opt-in local cache lookup/write for explicit-path lifecycle validation and ignored local untracked cache state. Closeout and unsupported modes still run normally. | R1-R12, R49-R59, R73-R74; VIC-T015, VIC-T028, VIC-T029 |
| Lifecycle safety checks | `scripts/artifact_lifecycle_validation.py`, `scripts/test-artifact-lifecycle-validator.py` | Added compact change metadata scanning so closeout records backed only by `cache-hit-inner-loop` fail lifecycle validation. | R49-R59, R101-R116; VIC-T026 |
| Change metadata evidence contract | `scripts/validate-change-metadata.py`, `scripts/test-change-metadata-validator.py`, compact metadata fixtures | Added `evidence_kind`/`evidence_ref` validation, legacy field rejection for cache evidence semantics, cache-only closeout rejection, and measurement file validation. | R101-R130, AC24-AC31; VIC-T023 through VIC-T031 |
| Selector routing | `scripts/validation_selection.py`, `scripts/test-select-validation.py` | Registered validation cache helper paths and change-local cache evidence files so selected validation does not fall back to manual routing. | R32, R75-R77; VIC-T032 through VIC-T034 |
| Measurement and preservation evidence | `validation-cache-measurement.yaml`, `behavior-preservation.md` | Recorded Workstream A measurement and documented pass/fail preservation, cache safety, closeout safety, and Workstream B deferral. | R47-R48, R75, R117-R130; VIC-T034, VIC-T035 |
| Lifecycle artifacts | Proposal, spec, architecture, ADR, test spec, plan, review records, change metadata | Recorded the formal workflow trail, review findings, dispositions, validation evidence, and current handoff state. | Workflow contract and plan milestones M0-M4 |

## Tests Added or Changed

| Test surface | What it proves |
| --- | --- |
| `scripts/test-validation-cache.py` | Cache identity includes command, input surface, implementation, policy, local cache context, previous pass-only behavior, strict local cache record identity, and formal evidence merging. |
| `scripts/test-artifact-lifecycle-validator.py` | Explicit-path cache integration preserves actual validator behavior and rejects cache-only closeout through lifecycle validation. |
| `scripts/test-change-metadata-validator.py` | Compact evidence-kind/result pairings, evidence refs, legacy compatibility, cache-only closeout rejection, measurement shape, count consistency, unsafe values, and Workstream B recommendation enum. |
| `scripts/test-select-validation.py` | Validation cache helper paths and change-local cache evidence files route through selected checks without manual-routing debt. |
| `tests/fixtures/change-metadata/**` | Positive and negative compact metadata and measurement examples used by validator regression tests. |

The test level is intentionally mixed: cache identity is unit-tested, CLI behavior is integration-tested, metadata contracts are fixture-tested, and selector routing is contract-tested because routing output is part of the workflow contract.

## Validation Evidence Before Final Verify

Available validation evidence recorded in the active plan includes:

- `python scripts/test-validation-cache.py`
- `python scripts/test-change-metadata-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-select-validation.py`
- `python scripts/select-validation.py --mode local`
- `bash scripts/ci.sh --mode local`
- `python scripts/validate-change-metadata.py .../change.yaml .../validation-cache-measurement.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout ...`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check --`

Code-review M1 R2, M2 R2, M3 R1, and M4 R1 all closed with no material findings after review-resolution where needed.

Final `verify` has not run yet.

## Review Resolution Summary

Review-resolution status is closed.

| Review stage | Material findings | Disposition |
| --- | ---: | --- |
| Proposal review R1 | 5 | accepted and resolved |
| Spec review R1 | 3 | accepted and resolved |
| Code review M1 R1 | 1 | accepted and resolved |
| Code review M2 R1 | 2 | accepted and resolved |
| Proposal review R2, spec review R2, architecture review R1, plan review R1, code-review M1 R2, M2 R2, M3 R1, M4 R1 | 0 | no material findings |

Durable record: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/review-resolution.md`.

## Alternatives Rejected

- Agent-declared "prose-only" validation narrowing was rejected because self-declared edit classes can be wrong.
- Diff-derived edit-scoped validation was deferred because misclassification can hide a real defect.
- Remote, shared, cross-branch, cross-worktree, and CI cache reuse were rejected for the first slice.
- Stage-closeout cache skipping was rejected for the first slice; closeout requires actual-run evidence.
- Caching other validators was deferred until each validator has a deterministic input-surface contract.

## Scope Control

This change preserves the first-slice non-goals:

- no Workstream B implementation;
- no edit-class validator narrowing;
- no cache-skip closeout bundles;
- no reuse of failed, blocked, skipped, not-run, missing, malformed, unsupported, or unknown cache records as passes;
- no semantic change to what lifecycle validation checks when it actually runs;
- no formal lifecycle reliance on untracked local cache state.

## Risks and Follow-ups

- Workstream A measurement is review evidence, not authorization for Workstream B. Any edit-scoped validation follow-up still needs separate proposal/spec authorization.
- Measurement numbers are bounded local observations, not a performance guarantee.
- More validators can become cache-eligible only after deterministic input-surface contracts are specified and tested.
- Final verify remains required before PR handoff.

## Current Readiness

All implementation milestones M1 through M4 are closed after code review. The next lifecycle stage is `verify` after this explain-change artifact is recorded and validated. Branch readiness, PR readiness, and final verification are not claimed here.
