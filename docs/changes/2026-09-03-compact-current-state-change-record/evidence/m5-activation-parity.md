# M5 implementation evidence: coherent compact activation

Milestone: M5
Subject path: `docs/plans/2026-09-03-compact-current-state-change-record.md`
Subject identity: `sha256:0c18ba75e3139f28415889279a453f2769b963dc37dd5d96da565fda2da7f67e`
Validation result: passed

## Result

- Skill: implement
- Status: M5 implementation complete and ready for Code Review
- Activation: `compact-current-state-v1` reader and prospective writer are active only when the canonical and packaged exact component matrices agree
- Supported adapters: Claude, Codex, and opencode candidate archives validate against the same canonical skill and resource set
- Compatibility: legacy records remain readable by their registered readers, reject compact writes and migration, and remain unchanged during compact projection and rollback checks
- External boundary: no release, publication, push, pull request, merge, network-backed correctness check, or other external mutation was performed
- Claim limitations: this evidence does not claim Code Review acceptance, final Verify, publication, release, or pull-request readiness

## Test-first and integrated evidence

Activation tests first required one exact closed matrix and proved that mixed, incomplete, unknown, and withheld matrices fail closed. The active matrix covers adapters, canonical guidance, CLI, documentation, fixtures, both validators, schemas, skills, and templates. Writer rollback preserves compact readers and recovery while rejecting new compact mutation.

The prospective writer now creates the exact empty compact coordinator with a valid whole-set lifecycle revision. The operation suite covers each lifecycle edge, stable review replacement, first and subsequent typed milestone selection, correction route and explicit return, rereview and exact settlement, finding and decision non-loss, evidence update and invalidation, milestone closure, final Code Review, and successful Verify. CLI transport tests prove argument, standard-input, and temporary-file requests have identical semantics and do not enter the authoritative set. Recovery tests cover interruption and exact restore without Git, PR, network, process, or log dependencies.

Equal-current-state projection proof compares one lean fixture with a fixture containing 250 disposable request records and 250 superseded review files. Their `skill-context` projections are equal, and the serialized result remains below 16 KiB. Only authoritative current paths are selected.

The standing vision and public positioning were revised as a substantive non-material clarification. RigorLoop remains a rigorous software engineering workflow for AI coding agents; Git, CI, pull requests, hosting, and repository-local storage are compatibility surfaces rather than product identity or correctness dependencies. The exact vision operation is recorded in `m5-vision-positioning-manifest.md`.

## Required validation results

- `npm test --prefix packages/rigorloop` — passed, 461 tests total: 459 passed and 2 intentional historical skips.
- `python scripts/test-lifecycle-cli-conformance.py` — passed, 6 invalid and 10 protected fixtures.
- `python scripts/test-governed-lifecycle-cli-validator.py` — passed, 19 tests.
- `python scripts/test-adapter-distribution.py` — passed, 157 tests.
- `python scripts/build-adapters.py --check` — passed for untracked archive-only candidate version `v0.5.1`.
- `python scripts/test-select-validation.py` — passed, 155 tests.
- `python scripts/validate-npm-package.py` — passed.
- `bash scripts/ci.sh --mode broad-smoke` — passed, 11 integrated checks in 485 seconds.

## Supplemental validation results

- Focused compact activation, CLI, and legacy migration tests — passed, 11 tests.
- Focused adapter verbose-check regression — passed.
- `python scripts/validate-documentation-prose.py --mode audit` — passed with zero errors and warnings.
- Markdown readability validation for the revised vision, README, positioning rationale, and standing architecture — passed with advisory warnings only.
- `git diff --check` — passed as a local whitespace diagnostic; compact correctness does not consume Git state.

## Deterministic candidate metadata

- Canonical activation: `specs/compact-current-state-activation.yaml`.
- Packaged activation: `packages/rigorloop/dist/metadata/compact-current-state-activation.json`.
- Activation schema: `schemas/compact-current-state-activation.schema.json`.
- Candidate adapter support metadata: `dist/adapters/manifest.yaml` at `v0.5.1`.
- Candidate archive identities and sizes: `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json`.
- Bundled metadata trust identity: `packages/rigorloop/dist/metadata/releases.json`.

The activation files agree on every required component and adapter. Deterministic archive regeneration matches the recorded candidate hashes. Generated public adapter skill bodies remain untracked release archives, so current drift validation builds and validates temporary candidates rather than requiring retired repository-tree output.

## Recovery and rollback

Changing the activation state from `active` to `withheld` disables prospective writers without removing compact readers or explicit transaction recovery. Existing compact records therefore remain readable and recoverable. Mixed-version matrices fail before writing. Legacy changes never acquire compact writer authority, and no migration writer exists.
