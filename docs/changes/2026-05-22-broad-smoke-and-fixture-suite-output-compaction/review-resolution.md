# Broad-Smoke and Fixture-Suite Output Compaction Review Resolution

## Scope

This record closes formal lifecycle review findings for the broad-smoke and fixture-suite output compaction proposal revision.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2
Review closeout: code-review-m4-r1
Review closeout: code-review-m4-r2

## Resolution Entries

### proposal-review-r1

#### BSO-PR1

Finding ID: BSO-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added a `Proof route` section requiring a focused test-spec amendment, defining when a spec amendment is required, and blocking implementation until the plan names an approved route.
Rationale: Broad-smoke `run_check` capture is a new output layer beyond the first accepted script-output slice, so planning needs an explicit proof route.
Validation target: Proposal defines the proof route before downstream planning.
Validation evidence: Proposal section `Proof route`.

#### BSO-PR2

Finding ID: BSO-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added an `Acceptance criteria` section with `AC-BSO-*` criteria for audit, broad-smoke capture, failure and verbose output, selected command preservation, first producer output, ordinary-validation coverage, selected-CI regression, and unchanged out-of-scope surfaces.
Rationale: Plan-review and code-review need explicit closure criteria rather than inferring them from goals and testing strategy.
Validation target: Proposal includes explicit acceptance criteria for the slice.
Validation evidence: Proposal section `Acceptance criteria`.

#### BSO-PR3

Finding ID: BSO-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `First producer decision` and `Producer verbosity decision`, locking the default first producer to `scripts/test-change-metadata-validator.py` unless a recorded approved audit exception replaces it, and requiring the plan to explicitly include or exclude `--quiet`.
Rationale: The producer target and verbosity modes affect test-spec, implementation, and code-review scope.
Validation target: Proposal settles the first producer and verbosity decision boundary.
Validation evidence: Proposal sections `First producer decision` and `Producer verbosity decision`.

#### BSO-PR4

Finding ID: BSO-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Behavior-preservation proof` and `Ordinary-validation guard`, requiring ordered command/test identity proof with SHA-256 hashes and ordinary validation coverage for output-contract tests.
Rationale: Prior script-output work showed count-only or separately run output-contract proof can miss selected-test drift or exclude required tests from ordinary validation.
Validation target: Proposal requires stable identity proof and ordinary-validation coverage.
Validation evidence: Proposal sections `Behavior-preservation proof` and `Ordinary-validation guard`.

Validation evidence:

- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction` passed with 1 review, 4 findings, 1 log entry, and 4 resolution entries.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r1.md` passed.
- `git diff --check -- docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction` passed.
- `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r1.md` passed selected `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, and `change_metadata.validate`.

### proposal-review-r2

No material findings.

### spec-review-r1

#### SRO-BSO-SR1

Finding ID: SRO-BSO-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. Preserve existing unittest-compatible `--quiet`/`-q` behavior while keeping custom compact quiet formatting out of scope for this slice.
Chosen action: Revised R60, added R60a through R60c, revised error/boundary behavior, replaced EC21, added EC21a, revised Non-goals, and added AC31 through AC36.
Rationale: Current `python scripts/test-change-metadata-validator.py --quiet` exits `0`, so the draft spec cannot safely state that the flag is unsupported.
Required outcome: Revise the spec so R60, EC21, Non-goals, and acceptance criteria match the selected compatibility contract.
Safe resolution path: Either define producer quiet success/failure requirements for this slice, or preserve existing unittest `--quiet`/`-q` behavior as compatibility and state only that custom quiet formatting is out of scope.
Validation target: Revised spec no longer contradicts current producer `--quiet` behavior.
Validation evidence: `python scripts/test-change-metadata-validator.py --quiet` and `python scripts/test-change-metadata-validator.py -q` both exit `0`, write no stdout, and write the normal unittest quiet success summary to stderr. Final structural validation is recorded after spec-review R2.

### spec-review-r2

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

#### BSO-M2-CR1

Finding ID: BSO-M2-CR1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Decision owner: implementer
Decision needed: Resolved by implementation.
Stop state: resolved; return M2 to code-review.
Required outcome: The M2 guard checks every `scripts/ci.sh` orchestration mode that runs validation producers, or explicitly recognizes an approved documented exception.
Safe resolution path: Add a structural helper that enumerates repository-owned orchestration paths in `scripts/ci.sh` that can run validation producers and asserts each uses the expected capture policy or an approved spec/test-spec exception. Extend the negative fixture so it introduces a validation-producing mode/path outside `run_check()` that streams child output directly and prove the guard fails with that mode/path identified.
Validation target: R51, R52, and TSRO-020 are fully covered by ordinary validation.

Chosen action: Broadened the `scripts/test-select-validation.py` wrapper-mode consistency guard from a helper-only `run_check()` assertion into a two-layer guard.

The guard now:
- keeps the helper-level assertion that `run_check()` captures child output with `"$@" 2>&1`, prints `Captured output:`, supports `verbose`, and does not stream a bare `"$@"`;
- verifies `scripts/ci.sh` mode dispatch routes selected-CI modes through the documented selected-CI policy and broad-smoke through `run_broad_smoke`;
- documents the selected-CI policy exception with reason, spec reference, and test-spec reference;
- scans repository-owned `run_*` orchestration functions for validation producer calls;
- allows producer command array construction but rejects direct validation producer execution outside `run_check`;
- rejects direct bare `"$@"` streaming outside `run_check`;
- names the offending mode/path in diagnostics.

Added negative fixture coverage for:
- a new `run_new_validation_mode()` that runs `python scripts/test-change-metadata-validator.py` directly outside `run_check`;
- a new `run_direct_streaming_mode()` that streams `"$@"` directly outside `run_check`.

Rationale: The original M2 guard proved only that the helper captured output. It did not enforce the wrapper-mode invariant that every validation-producing orchestration mode must use capture-on-success/show-on-failure-or-verbose behavior or carry a documented exception.

Validation evidence: `python scripts/test-select-validation.py --verbose -k broad_smoke_wrapper_mode_consistency_guard_is_enforced` passed.
- `python scripts/test-select-validation.py --verbose -k broad_smoke` passed 8 tests.
- `python scripts/test-select-validation.py` passed 77 tests.

### code-review-m2-r2

No material findings.

### code-review-m3-r1

#### BSO-M3-CR1

Finding ID: BSO-M3-CR1
Disposition: accepted
Status: resolved after evidence update
Owner: implementer
Owning stage: review-resolution
Decision owner: implementer
Decision needed: Resolved by evidence update.
Stop state: resolved; return M3 to code-review.
Required outcome: The recorded producer selected-test identity extraction method must replay after the M3 dataclass runner change and continue to prove unchanged ordered identifiers and SHA-256 hash.
Safe resolution path: Add `sys.modules[spec.name] = module` before `spec.loader.exec_module(module)` in the recorded extraction method, rerun the extraction and `sha256sum`, confirm the post-M3 hash remains `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`, and record validation evidence.
Validation target: R62 and TSRO-024.
Chosen action: Updated the audit and behavior-preservation proof route to register the loaded producer module in `sys.modules` before executing it, then replayed the selected-test identity extraction.
Rationale: M3 added a dataclass declaration before the test class, so the import-based proof must register the module before `exec_module()` to remain replayable.

Resolution: Updated `script-output-layer-audit.md` and `behavior-preservation.md` to use one replayable import-based extraction method. The documented method now registers the loaded module in `sys.modules` before `spec.loader.exec_module(module)`, preserving compatibility with the M3 dataclass declaration in `scripts/test-change-metadata-validator.py`.

Validation evidence: Replayed the documented extraction successfully. Result: count `18`; SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`.

#### BSO-M3-CR2

Finding ID: BSO-M3-CR2
Disposition: accepted
Status: resolved after metadata update
Owner: implementer
Owning stage: review-resolution
Decision owner: implementer
Decision needed: Resolved by metadata update.
Stop state: resolved; return M3 to code-review.
Required outcome: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` must list `scripts/test-change-metadata-validator.py`.
Safe resolution path: Add `scripts/test-change-metadata-validator.py` to `changed_files`, keep the M3 review record path listed, and rerun change metadata and lifecycle validation.
Validation target: change-local metadata accuracy for the M3 implementation surface.
Chosen action: Added `scripts/test-change-metadata-validator.py` to the `changed_files` list in `change.yaml`.
Rationale: M3 changes the targeted producer file directly, so the change-local file inventory must include that primary implementation surface.

Resolution: Added `scripts/test-change-metadata-validator.py` to the `changed_files` list in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`.

Validation evidence: `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` passed after the metadata update.

Review-resolution validation:

- Producer selected-test identity extraction replay passed with count `18` and SHA-256 `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`.
- `python scripts/test-change-metadata-validator.py` passed.
- `python scripts/test-change-metadata-validator.py --verbose` passed.
- `python scripts/test-change-metadata-validator.py --quiet` passed.
- `python scripts/test-select-validation.py` passed.
- `bash scripts/ci.sh --mode explicit --path scripts/ci.sh --path scripts/test-select-validation.py --path scripts/test-change-metadata-validator.py` passed selected `change_metadata.regression` and `selector.regression`.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md --path docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/behavior-preservation.md --path docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md --path docs/plan.md` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction` passed.
- `git diff --check --` passed.

### code-review-m3-r2

No material findings.

### code-review-m4-r1

#### BSO-M4-CR1

Finding ID: BSO-M4-CR1
Disposition: accepted
Status: resolved after lifecycle-state synchronization
Owner: implementer
Owning stage: review-resolution
Decision owner: implementer
Decision needed: Resolved by lifecycle state synchronization.
Stop state: resolved; return M4 to code-review.
Required outcome: The active plan must have a consistent M4 state across its Current Handoff Summary and M4 milestone body before M4 can close or downstream final closeout can begin.
Safe resolution path: Update the M4 milestone body to the current lifecycle state used by the handoff. Because code-review M4 R1 found a material issue, keep M4 in `resolution-needed` until the finding is fixed and re-reviewed. After a clean M4 re-review, synchronize `docs/plan.md`, the active plan, and `change.yaml` to close M4 and hand off to final closeout.
Rationale: M4 is the milestone that owns preservation evidence and lifecycle synchronization, so an internally stale M4 milestone state blocks a reliable handoff to final closeout even though the runtime proof evidence is otherwise present.
Chosen action: Synchronized the active plan so the Current Handoff Summary and M4 milestone body both record M4 as `resolution-needed`, and synchronized the plan index and change metadata with the M4 review-resolution state.
Resolution: The M4 milestone body no longer says `planned`; it now records `Milestone state: resolution-needed`. M4 is not marked closed. No runtime output behavior, selected command identity evidence, selected-test identity evidence, broad-smoke behavior, selected-CI behavior, generated artifacts, skills, adapters, or JSON behavior changed.
Validation target: planned-initiative lifecycle state synchronization for M4.
Validation evidence: Review-resolution validation is recorded in `change.yaml`; final structure, metadata, artifact lifecycle, and patch hygiene validation passed after the lifecycle state synchronization.

### code-review-m4-r2

No material findings.
