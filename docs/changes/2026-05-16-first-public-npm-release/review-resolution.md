# First Public npm Release Review Resolution

## Scope

This record tracks formal review closeout for the first public npm release proposal and spec.

Closeout status: closed

Review closeout: code-review-r8

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `architecture-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`, `code-review-r6`, `code-review-r7`, `code-review-r8`
- Findings resolved: 6
- Unresolved findings: 0
- Final result: `code-review-r8` found no material findings for the scoped M6a repository-local readiness proof; M6a remains open for verify, PR handoff, implementation PR merge, and tag authorization.

## Finding Details

### proposal-review-r1

No material findings; no resolution action required.

### spec-review-r1

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| SR1-F1 | accepted | resolved | First-publication bootstrap conflicts with release workflow ownership. |
| SR1-F2 | accepted | resolved | Acceptance can pass without proving the real Codex adapter install path. |

#### SR1-F1 - First-publication bootstrap conflicts with release workflow ownership

Finding ID: SR1-F1
Disposition: accepted
Status: resolved by spec-review-r2
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. The spec now defines mutually exclusive `trusted-publishing` and `bootstrap` modes.
Chosen action: Added publication-mode requirements to `specs/rigorloop-npm-publication.md`. Trusted-publishing mode uses `.github/workflows/release.yml` and npm OIDC. Bootstrap mode is limited to `@xiongxianfei/rigorloop@0.1.4`, allows manual `npm publish <tarball>` only for the exact recorded packed tarball, requires release verification/package-content validation/packed-package smoke, and forbids `release.yml` from also publishing the same version.
Rationale: The first public package needs one testable publication contract. Release readiness can remain workflow-owned while the first package claim uses a narrow manual bootstrap only if required.

Required outcome: Revise the spec to define mutually exclusive trusted-publishing and bootstrap publication modes, including exactly which path publishes `@xiongxianfei/rigorloop@0.1.4` and how the published tarball identity is proven.

Safe resolution path: Add a "Publication modes" section. Trusted-publishing mode should let `.github/workflows/release.yml` run release verification, package-content validation, packed-package smoke, and `npm publish` through OIDC. Bootstrap mode should be limited to `0.1.4`, require the same release readiness checks, and allow maintainer manual publication only for the exact packed tarball whose filename, SHA-256, source commit, and smoke result are recorded. The spec should also say whether the release workflow publish job is enabled for `v0.1.4` or only future trusted-publishing releases after bootstrap.

Validation target: Revised `specs/rigorloop-npm-publication.md` defines one testable publication path for first publish and explicit evidence fields for bootstrap tarball identity.

#### SR1-F2 - Publication acceptance does not prove the real Codex adapter install path

Finding ID: SR1-F2
Disposition: accepted
Status: resolved by spec-review-r2
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. The spec now requires actual install proof before FU-010 closeout, and before publication when official release assets are externally observable.
Chosen action: Added real Codex adapter install proof requirements to `specs/rigorloop-npm-publication.md`. The spec now requires actual non-dry-run `init --adapter codex --json` smoke from the packed or published package, verification of the official archive URL, checksum, size when available, safe extraction, installed tree hash, generated files, and explicit ordering-gap evidence when npm publication precedes externally observable GitHub release assets.
Rationale: The primary public user flow is not dry-run. Publication evidence must prove that the official Codex adapter archive named by bundled metadata exists, is reachable, verifies, extracts safely, and produces the expected installed tree.

Required outcome: Revise the spec so FU-010 cannot close while the primary public `init --adapter codex` path remains unproven.

Safe resolution path: Require verification that the official `v0.1.4` Codex adapter archive named by bundled metadata is available at the official GitHub release URL and verifies successfully. Before FU-010 closes, run an actual `init --adapter codex --json` from the packed or published package in a temporary project, not only dry-run. If npm publication happens before GitHub release assets are externally observable, publication evidence should record the temporary ordering gap and FU-010 should remain open until the actual install smoke passes.

Validation target: Revised `specs/rigorloop-npm-publication.md` requires actual packed or published package `init --adapter codex --json` verification against the official `v0.1.4` Codex release archive before FU-010 closeout.

### spec-review-r2

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| SR2-F1 | accepted | resolved | Acceptance criterion AC8 conflicts with bootstrap publication mode. |

#### SR2-F1 - Acceptance criterion conflicts with bootstrap publication mode

Finding ID: SR2-F1
Disposition: accepted
Status: resolved by spec-review-r3
Owner: spec author
Owning stage: spec
Decision owner: spec author
Decision needed: Resolved by spec revision. AC8 is now mode-aware.
Chosen action: Replaced unconditional AC8 with mode-aware acceptance criteria. In trusted-publishing mode, evidence proves `.github/workflows/release.yml` owns npm publication, uses the approved release trigger, and rejects unsupported tags. In bootstrap mode, evidence proves `.github/workflows/release.yml` did not publish `@xiongxianfei/rigorloop@0.1.4`, and complete bootstrap tarball identity evidence is required. Added R36e and R36f to distinguish release readiness ownership from npm publish execution ownership in bootstrap mode.
Stop state: Spec approval is blocked until AC8 is revised and spec-review reruns.

Required outcome: Revise the acceptance criteria so `release.yml` ownership is required only in trusted-publishing mode, while bootstrap mode requires evidence that `release.yml` did not also publish `@xiongxianfei/rigorloop@0.1.4`.

Safe resolution path: Replace AC8 with mode-aware wording such as: "Publication evidence proves exactly one publication mode. In trusted-publishing mode, `.github/workflows/release.yml` owns npm publication and rejects unsupported tags. In bootstrap mode, `.github/workflows/release.yml` does not also publish `@xiongxianfei/rigorloop@0.1.4`, and bootstrap tarball identity evidence is complete."

Rationale: R36d requires `.github/workflows/release.yml` not to publish `0.1.4` in bootstrap mode, but AC8 still unconditionally says the workflow owns npm publication. Acceptance criteria must not contradict the normative publication modes.

Validation target: Revised acceptance criteria are mode-aware and no longer conflict with R36 through R40 and R53 through R61d.

### spec-review-r3

No material findings; no resolution action required. This review approved the revised npm publication spec and confirmed SR1-F1, SR1-F2, and SR2-F1 are closed.

### architecture-review-r1

No material findings; no resolution action required. This review approved the canonical architecture update, C4 diagram updates, and `docs/adr/ADR-20260516-rigorloop-npm-publication.md`.

### plan-review-r1

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| PR1-F1 | accepted | resolved by plan-review-r2 | Publication execution and repository closeout sequencing is underdefined. |

#### PR1-F1 - Publication execution and repository closeout sequencing is underdefined

Finding ID: PR1-F1
Disposition: accepted
Status: resolved by plan-review-r2
Owner: plan author
Owning stage: plan
Decision owner: plan author
Decision needed: No owner decision needed. The plan needs a clearer execution/evidence boundary.
Chosen action: Split the final lifecycle closeout into `M6a Pre-Publication PR And Merge Readiness` and `M6b Publication Execution And Evidence Closeout`. Added an explicit release execution boundary ordering implementation PR merge before tag creation, tag before publication, publication before final evidence, and FU-010 closeout only after tracked validated evidence.
Rationale: The plan must distinguish the repository implementation PR/merge boundary from the external publication event and post-publication evidence update. Release workflow changes must be merged before tag publication can run, while final npm publication evidence and FU-010 closeout can only be recorded after publication and real install proof.

Required outcome: Revise the plan to explicitly model the release execution boundary and repository evidence update path.

Safe resolution path: Split M6 into pre-publication PR/merge readiness and post-publication evidence closeout, or keep M6 but add explicit ordered gates: implementation PR merged before tag; tag created from the merged commit; selected publication mode runs from that tag or exact verified tarball; post-publication evidence is committed through a named repository update path; FU-010 closes only after that evidence update passes validation.

Validation target: Revised plan names the implementation PR/merge boundary, release tag precondition, selected publication execution, post-publication evidence update path, and validation commands for the evidence update. Plan-review must rerun cleanly before test-spec.

Validation evidence: `plan-review-r2` confirmed that the revised plan splits final closeout into `M6a Pre-Publication PR And Merge Readiness` and `M6b Publication Execution And Evidence Closeout`, adds the ordered release execution boundary, and names the post-publication evidence PR path. No material findings remain.

### plan-review-r2

No material findings; no resolution action required. This review approved the revised execution plan and confirmed `PR1-F1` is closed.

### code-review-r1

No material findings; no resolution action required. This review closed M1 Package Metadata And Runtime Tarball Contract and handed off to M2 implementation.

### code-review-r2

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| CR2-F1 | accepted | resolved | Root-level forbidden archive and secret-like files are not rejected. |

#### CR2-F1 - Root-level forbidden archive and secret-like files are not rejected

Finding ID: CR2-F1
Disposition: accepted
Status: resolved by M2 fix
Owner: implementation
Owning stage: implement
Decision owner: implementation
Decision needed: No owner decision needed. The issue is a fixable implementation and test coverage gap within M2 scope.
Chosen action: Add direct tests for root-level and nested forbidden paths and update package tarball path matching so recursive forbidden patterns reject files at package root as well as in subdirectories.
Required outcome: Package-content validation must reject forbidden tarball paths at package root and nested paths, including adapter/archive/secrets patterns required by R22-R26 and TNP-003/TNP-021.
Safe resolution path: Add direct tests for root-level and nested forbidden paths such as `package/rigorloop-adapter-codex-v0.1.4.zip`, `package/archive.tgz`, `package/.env`, `package/secret.pem`, and `package/secret.key`. Update `is_forbidden_path` to implement the spec's intended recursive semantics explicitly, for example by checking exact forbidden prefixes and suffixes in addition to path-glob patterns, or by adding root-level patterns like `package/*.zip`, `package/*.tgz`, `package/*.pem`, `package/*.key`, and `package/*.env`.
Rationale: R22-R26 require package-content validation to block forbidden tarball contents before publication. Python `fnmatch` does not treat `**` as matching zero or more directories, so the current validator misses root-level forbidden paths.
Validation target: `python scripts/test-npm-package-publication.py`, `python scripts/test-select-validation.py`, selected CI, and diff check pass after the validator rejects both root-level and nested forbidden tarball paths.
Validation evidence: Added root-level and nested forbidden-path tests in `scripts/test-npm-package-publication.py`; updated `scripts/npm_package_validation.py` to normalize tarball paths and reject forbidden file classes by package-relative meaning. `python scripts/test-npm-package-publication.py` passes after the fix.

### code-review-r3

No material findings; no resolution action required. This review confirmed `CR2-F1` is fixed, closed M2 Package-Content Validation And Packed-Package Smoke, and handed off to M3 implementation.

### code-review-r4

No material findings; no resolution action required. This review closed M3 Release Verification And v0.1.4 Release Evidence and handed off to M4 implementation.

### code-review-r5

| Finding | Disposition | Status | Summary |
| --- | --- | --- | --- |
| CR5-F1 | accepted | fixed pending code-review rerun | Bootstrap tarball SHA mismatch is not validated. |

#### CR5-F1 - Bootstrap tarball SHA mismatch is not validated

Finding ID: CR5-F1
Disposition: accepted
Status: fixed pending code-review rerun
Owner: implementation
Owning stage: implement
Decision owner: implementation
Decision needed: No owner decision needed. The issue is a fixable validation and test coverage gap within M4 scope.
Chosen action: Add deterministic mismatched-tarball-SHA coverage and update release evidence validation to compare the recorded bootstrap tarball SHA-256 to the actual packed tarball bytes when the tarball is available to the validator.
Required outcome: Bootstrap evidence validation must reject a mismatched tarball SHA-256, not only missing or malformed SHA text, before M4 can close.
Safe resolution path: Add a fixture that creates or points to a packed tarball file and records a different `tarball.sha256` in `npm-publication.md`. Update validation so, when a bootstrap tarball is available to the release/evidence validator, it computes the SHA-256 over the exact tarball named by evidence and fails when it differs. Keep pending-publication scaffold behavior intact.
Rationale: R61c requires bootstrap publication to block when the tarball SHA-256 differs from recorded evidence, and TNP-011 requires a mismatched-SHA negative fixture. The current implementation checks only whether the recorded SHA is 64 lowercase hex characters.
Validation target: M4 focused tests include a mismatched tarball SHA negative fixture, `python scripts/test-adapter-distribution.py` passes, `bash scripts/release-verify.sh v0.1.4` passes, selected CI passes, and code-review reruns cleanly.
Validation evidence: Added matching, mismatched, missing-file, and malformed-SHA bootstrap tarball tests in `scripts/test-adapter-distribution.py`; added `--npm-tarball-root` support to `scripts/validate-release.py`; updated release evidence validation in `scripts/adapter_distribution.py` to compute SHA-256 over the named tarball when a tarball root is supplied. Focused CR5-F1 tests, the full adapter distribution suite, `bash scripts/release-verify.sh v0.1.4`, selected CI, and lifecycle validation pass after the fix. M4 still requires code-review rerun before closeout.

### code-review-r6

No material findings; no resolution action required. This review confirmed `CR5-F1` is fixed, closed M4 Release Workflow And Publication Mode Gates, and handed off to M5 implementation.

### code-review-r7

No material findings; no resolution action required. This review closed M5 Documentation, Follow-Up State, And Final Local Readiness and handed off to M6a Pre-Publication PR And Merge Readiness.

### code-review-r8

No material findings; no resolution action required. This review confirmed the M6a repository-local readiness proof and kept M6a open for verify, PR handoff, implementation PR merge, and tag authorization.
