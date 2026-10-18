# Minimal repository tests

## Purpose / big picture

The maintainer selected one direct command and four small test groups after merging PR #211. Reduce routine regression breadth and remove its custom execution infrastructure. Preserve final independent review/Verify and critical protection against false completion, state loss and unsafe installation. This is an explicit reduction of automated assurance; it does not retire supported product behavior or claim equivalent coverage.

## Current Handoff Summary

Owning Change: `2026-10-18-minimal-tests`. Use its CLI context for mutable progress and evidence.

## Source artifacts

System TEST-SR-07–10, 15, 17 and 21–23 govern protection and its disposition. Validation owns repository execution and the reduced allocation. CLI/Records, Installation, Packaging and Release retain product contracts. Existing tests supply independently specified assertions; their presence alone does not require retaining the old suite.

## Scope and selected design

Run four groups directly through native Node/Python runners: workflow, storage/recovery, real package installation, and skill/resource integrity. Keep existing release qualification entrypoints and actual candidate/publication observations; run a small release-boundary regression group with release qualification. No bespoke selector, per-case worker scheduler, Node adapter, result-envelope writer, browser automation toolchain or exact-phrase regression suite remains.

The direct entrypoint is `bash scripts/ci.sh`, with no path/mode/worker/report options. PR and main use identical essential tests. Product generators and runtime validators remain available. On-demand model/browser generation and semantic review replace routine exhaustive schema/diagram/browser/prose regressions; they are not equivalent automatic protection. Release candidate checks stay in release tooling, not implicit CI candidate preparation.

## Milestones

1. Select the reduced proof and amend current validation/coverage consumers. Preserve stable IDs and explicitly mark removed case realizations and residual risk; historical evidence remains historical.
2. Consolidate useful existing assertions, simplify the runner and CI, remove superseded tests, exclusive fixtures and execution machinery. Reconcile release callers and model test references in the same change.
3. Run all retained tests, check representative defective candidates, inspect imports/links/workflow permissions and regenerate affected outputs. Obtain independent whole-change review, then distinct final Verify.

## Verification allocation

| Group | Required observation | Existing source of assertions |
| --- | --- | --- |
| Workflow | Owner-selected bases complete only with independent review and distinct Verify; unresolved findings and stale support block success | operational-review and operational-reliance tests |
| Storage | Public CLI persists across processes; invalid/stale requests preserve state; backup/restore preserves records and payloads; interrupted recovery remains fenced | operational-store, operational-update and operational-maintenance tests |
| Installation | Actual tarball installs and initializes both targets; conflicts and unsafe paths preserve user data; archive inventory matches authored skills | npm publication and installer replacement tests |
| Skill integrity | Required skills and mapped local resources exist; a missing resource fails | skill resource/metadata tests and existing validator |
| Release boundary | Actual prepared artifacts retain identity checks and public smoke; authority/tag mismatch and publication failure cannot report success | Release validators and selected release regression cases |

## Removal and residual risk

Remove documentation phrase assertions, redundant policy permutations, legacy compatibility fixture suites, model/schema/browser regression populations and custom execution tests. Remaining supported legacy import, detailed browser behavior, command rendering, exhaustive malformed-input combinations and rare concurrency/recovery interleavings lose continuous regression protection. Changes in those areas require explicit affected proof or manual assessment, and must not cite this minimal suite as complete coverage. Retain known corruption, rollback, self-approval, unsafe-path and publication-authority checks. Preserve release fixtures that actual production release tooling still consumes.

Detailed test catalogs remain scenario intent. Removed executable references become explicit unimplemented proof gaps; no replacement test is linked unless its assertions prove that scenario. Validation completeness means the selected essential suite ran, not that every product requirement is automatically tested.

## Validation plan

- `bash scripts/ci.sh`: execute the four essential groups with real temporary stores, archives and filesystem boundaries.
- `python3 tests/engineering/release/test-release-transaction.py`: retained release-boundary checks.
- `python3 scripts/validate-boundary-first.py --check`: inspect affected current model structure and references.
- Existing projection/generation check commands for affected canonical inputs.
- Temporary faulty runtime copies: remove final approval guard and make rejected update mutate state; corresponding essential assertions must fail. Do not modify the working implementation for this experiment.
- `git diff --check`, native syntax/import checks and source-consumer audit.

## Risks and recovery

Test removal reduces detection breadth. The user selected this tradeoff; critical retained assertions and independent review bound the claim. Recover removed sources from base `d7761c8c9c34f0f3a4bb3a74504190e0ceafed53` if needed. Revert tests, runner, contracts and consumers together; no runtime storage migration or customer-record change is involved. No release, merge or publication is authorized by this plan.

## Final review checkpoint

Review the full removal scope, retained assertions, source dependencies, CI and release wiring, coverage limitations and actual results. Reassess corrections in the same whole-change gate. Final Verify is separate.
