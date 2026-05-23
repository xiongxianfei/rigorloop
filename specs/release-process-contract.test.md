# Release Process Contract Test Spec

## Status

active

## Related spec and plan

- Spec: [Release Process Contract](release-process-contract.md), approved.
- Plan: [Release Process Contract Execution Plan](../docs/plans/2026-05-23-release-process-contract.md), active and approved by `plan-review-r1`.
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260523 Release Process Contract](../docs/adr/ADR-20260523-release-process-contract.md), accepted.
- Change metadata: [change.yaml](../docs/changes/2026-05-23-release-process-contract/change.yaml).
- Review records:
  - `docs/changes/2026-05-23-release-process-contract/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-23-release-process-contract/reviews/architecture-review-r1.md`
  - `docs/changes/2026-05-23-release-process-contract/reviews/plan-review-r1.md`

## Testing strategy

This test spec proves a standing release-process contract without publishing a package. The implementation proof is split across release evidence structure, selector routing, lightweight checklist validation, release-gate rehearsal, and final lifecycle coherence.

- Unit tests cover release evidence/checklist parsing, required field presence, release classification, version/dist-tag decisions, emergency deferral shape, non-deferrable requirements, and forbidden secret/machine-local markers.
- Integration tests cover `docs/releases/v<version>.md` selector routing, preservation of existing `docs/releases/<version>/release.yaml` routing, artifact lifecycle validation, release validation wrappers, package publication regression tests, adapter distribution tests, and change metadata validation.
- Smoke tests run release validation in dry-run or non-publishing modes such as `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5` and `python scripts/validate-release-ci.py --version v0.1.5`.
- Manual verification is limited to reviewing the dry-run rehearsal evidence and confirming it does not claim a real release or publish event.
- Contract tests assert that routine publish evidence does not replace upstream lifecycle review, does not update `docs/plan.md` unless the release is tied to an active lifecycle plan, and does not allow emergency deferrals to hide failed or non-deferrable checks.
- Migration tests preserve historical `docs/releases/<version>/release.yaml`, release notes, npm publication evidence, and release-specific specs. Historical releases are not backfilled into `docs/releases/v<version>.md`.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| REL-R1 through REL-R6 | TREL-001, TREL-002, TREL-003 | contract, integration | Process boundary, routine/no-new-decision claim, breaking release upstream approval, and lifecycle-managed process changes. |
| REL-R7 through REL-R13 | TREL-004 | unit, contract | No-op publish block and version/dist-tag classification. |
| REL-R14, REL-R14a | TREL-005, TREL-006, TREL-007 | unit, integration | Full gate, emergency exception, deferral record, and failed-gate visibility. |
| REL-R15 through REL-R27 | TREL-005, TREL-010, TREL-011 | integration, smoke | Pre-publish gate, generated-output checks, package preview, packed install smoke, evidence path, and automation evidence visibility. |
| REL-R28 through REL-R31 | TREL-003, TREL-008, TREL-009, TREL-016 | integration, contract | Version-scoped evidence path, change-record link, plan-index boundary, release index behavior. |
| REL-R32 through REL-R38 | TREL-003, TREL-005, TREL-012, TREL-013 | unit, integration | Required evidence fields, version rationale, gate results, package contents, publish event, registry verification, recovery notes. |
| REL-R39 | TREL-014 | unit, security | Secret and private machine-state suppression. |
| REL-R40 through REL-R41 | TREL-008, TREL-009 | integration, contract | First-slice lifecycle/checklist validation and no premature dedicated validator. |
| REL-R42 through REL-R50 | TREL-011, TREL-012 | contract, integration | Trusted publishing preference, manual fallback reason, provenance mode, dist-tags, staged publishing deferred. |
| REL-R51 through REL-R56 | TREL-012, TREL-007 | integration, smoke | Registry verification, dist-tag, integrity, fresh install smoke, CLI/npx smoke, emergency smoke deferral. |
| REL-R57 through REL-R62 | TREL-013 | unit, contract | Failed-before/during/after states, uncertain publish verification, fix-forward/deprecate, no overwrite. |
| REL-R63 through REL-R64 | TREL-006, TREL-007 | unit, integration | Emergency deferral evidence and registry verification remains mandatory. |
| REL-R65 through REL-R72 | TREL-007, TREL-014 | unit, security | Non-deferrable requirements and fresh install smoke deferral shape. |
| AC-REL-001 through AC-REL-014 | TREL-001 through TREL-017 | contract, integration, smoke, manual | Acceptance criteria covered by grouped release evidence, routing, gate, recovery, security, and lifecycle tests. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 routine stable publish uses standing process | TREL-001, TREL-003, TREL-005, TREL-012 | Routine evidence records process, gate, package preview, registry verification, and install smoke. |
| E2 release-process change requires lifecycle treatment | TREL-002 | Release-process changes cannot be routine publish evidence. |
| E3 generated output drift blocks publish | TREL-010, TREL-011 | Gate requires generated-output checks and fails on drift. |
| E4 manual fallback keeps the full gate | TREL-011, TREL-012, TREL-014 | Manual fallback reason is recorded and does not relax evidence or secret suppression. |
| E5 bad package content after publish fixes forward | TREL-013 | Published package content uses fix-forward/deprecate/dist-tag correction, not overwrite. |
| E6 release evidence stays out of the plan index | TREL-016 | Routine release evidence updates release surfaces, not `docs/plan.md`, unless tied to active lifecycle plan. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 breaking change already completed lifecycle | TREL-001, TREL-004 | Publish may be routine but evidence records major decision and upstream approval. |
| EC2 npm version already exists before publish | TREL-004, TREL-013 | Publish stops and records duplicate/recovery/no-op state. |
| EC3 trusted publishing unavailable during first rollout | TREL-011, TREL-012 | Manual fallback preserves full gate and records reason. |
| EC4 registry integrity metadata temporarily unavailable | TREL-012, TREL-013 | Evidence records failed-after-publish until follow-up verification or approved rationale. |
| EC5 adapter archives are release-output | TREL-010, TREL-011 | Evidence records generated-output boundary and validates temporary or release-output artifacts. |
| EC6 release tied to active lifecycle plan | TREL-016, TREL-017 | Plan surfaces update only when lifecycle plan owns the release. |
| EC7 emergency release | TREL-006, TREL-007 | Deferrals require owner approval and preserve registry verification/secret suppression. |
| EC8 routine release missing package preview | TREL-005 | Routine release blocks; emergency rules do not apply. |
| EC9 valid emergency fresh install smoke deferral | TREL-006, TREL-007 | Deferral can pass only with owner, impact, risk, follow-up, deadline, and registry verification. |
| EC10 registry verification deferred | TREL-007 | Validation fails because registry verification is non-deferrable. |
| EC11 deferral lacks owner or validation impact | TREL-006 | Validation fails and publish cannot proceed under emergency exception. |

## Test cases

### TREL-001. Routine publish evidence records no-new-decision boundary

- Covers: REL-R1, REL-R2, REL-R5, REL-R6, E1, EC1, AC-REL-001, AC-REL-002
- Level: contract
- Fixture/setup: Valid routine release evidence fixture based on `templates/release-evidence.md` with release type, no-new-decision claim, source commit, and upstream approval reference for a major release fixture.
- Steps: Validate the fixture through the release-evidence checklist or lifecycle structural checks.
- Expected result: Routine evidence passes only when release type and no-new-decision claim are explicit; breaking publish fixture passes only when upstream approval is recorded.
- Failure proves: Routine publish evidence can silently replace upstream lifecycle review.
- Automation location: `scripts/test-artifact-lifecycle-validator.py` or release checklist tests added in M2.

### TREL-002. Release-process and package-surface changes cannot be routine

- Covers: REL-R1, REL-R3, REL-R4, E2, AC-REL-003
- Level: contract
- Fixture/setup: Invalid evidence fixtures that mark changed gate, auth/provenance policy, package name/scope, adapter target, install root, evidence location, or publish mechanics as routine.
- Steps: Run the checklist validation against each invalid fixture.
- Expected result: Each fixture fails with a diagnostic that the change requires lifecycle treatment before publish.
- Failure proves: A routine publish can smuggle release-process or package-surface decisions.
- Automation location: `scripts/test-artifact-lifecycle-validator.py` or release checklist tests.

### TREL-003. Release evidence template has required sections and fields

- Covers: REL-R28 through REL-R38, E1, AC-REL-004, AC-REL-010, AC-REL-012
- Level: unit, contract
- Fixture/setup: `templates/release-evidence.md`, valid fixture, and fixtures missing required sections.
- Steps: Assert the template and valid fixture include result, version decision, preflight gate, package contents, publish event, registry verification, recovery/rollback notes, and follow-up sections.
- Expected result: Complete evidence passes; missing required sections or fields fail.
- Failure proves: Release evidence cannot reconstruct version, source, package, gate, publish event, registry result, smoke result, and recovery.
- Automation location: `scripts/test-artifact-lifecycle-validator.py` or release checklist tests.

### TREL-004. Version, release type, dist-tag, and no-op publish rules are enforced

- Covers: REL-R7 through REL-R13, EC1, EC2, AC-REL-004
- Level: unit
- Fixture/setup: Version-decision fixtures for patch, minor, major, prerelease, stable, no-op, and duplicate npm version states.
- Steps: Run checklist validation against valid and invalid version-decision fixtures.
- Expected result: Patch/minor/major/prerelease/stable decisions pass only with matching rationale and dist-tag; no-op and duplicate-version fixtures block publish.
- Failure proves: Maintainers can improvise version or dist-tag decisions.
- Automation location: release checklist tests.

### TREL-005. Routine full-gate checklist blocks missing gate evidence

- Covers: REL-R14 through REL-R18, REL-R21 through REL-R27, EC8, AC-REL-005, AC-REL-007
- Level: integration
- Fixture/setup: Routine release evidence fixtures with complete gate, missing package preview, missing packed install smoke, missing evidence path, unresolved blocker, and hidden automation evidence.
- Steps: Validate fixtures through lifecycle/checklist validation.
- Expected result: Complete routine gate passes; each missing required gate item fails before publish.
- Failure proves: Routine releases can publish without the full gate.
- Automation location: `scripts/test-artifact-lifecycle-validator.py` or release checklist tests.

### TREL-006. Emergency deferral record shape is complete and visible

- Covers: REL-R14, REL-R14a, REL-R63, EC7, EC9, EC11, AC-REL-005
- Level: unit, integration
- Fixture/setup: Valid emergency fixture plus invalid fixtures missing approving owner, emergency rationale, deferred item, reason, validation impact, accepted risk, follow-up, or deadline.
- Steps: Run checklist validation against emergency fixtures.
- Expected result: Valid emergency deferral passes with emergency-with-deferred-gate status; incomplete deferrals fail.
- Failure proves: Emergency deferral can become a vague skip-gate label.
- Automation location: release checklist tests.

### TREL-007. Non-deferrable emergency requirements fail closed

- Covers: REL-R64 through REL-R72, EC9, EC10, AC-REL-005, AC-REL-009, AC-REL-011
- Level: unit, security
- Fixture/setup: Emergency fixtures attempting to defer release evidence creation, secret suppression, source/version recording, package name/dist-tag, publish path, registry verification, recovery/follow-up, and fresh install smoke with and without required deferral metadata.
- Steps: Validate each fixture.
- Expected result: Non-deferrable items always fail when deferred; fresh install smoke may be deferred only with required owner/reason/impact/follow-up metadata while registry verification remains present.
- Failure proves: Emergency mode can bypass safety-critical release requirements.
- Automation location: release checklist tests.

### TREL-008. `docs/releases/v<version>.md` routes deterministically

- Covers: REL-R28, REL-R40, REL-R41, AC-REL-010
- Level: integration
- Fixture/setup: Selector fixture path `docs/releases/v1.2.3.md` or equivalent non-real version evidence path.
- Steps: Run `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`.
- Expected result: Path is classified as release evidence, selects the intended release validation/checklist route, and does not emit `manual-routing-required` or `release-version-required`.
- Failure proves: The new evidence class will become late verify routing debt.
- Automation location: `scripts/test-select-validation.py`.

### TREL-009. Existing release-directory routing remains compatible

- Covers: REL-R40, REL-R41, compatibility claims, AC-REL-010
- Level: migration, integration
- Fixture/setup: Existing paths such as `docs/releases/v0.1.5/release.yaml`, `docs/releases/v0.1.5/release-notes.md`, and `docs/releases/v0.1.5/npm-publication.md`.
- Steps: Run selector and release validation fixtures for existing release-directory paths.
- Expected result: Existing release metadata routing and validation still work; no historical backfill is required.
- Failure proves: The standing process breaks prior release-specific evidence.
- Automation location: `scripts/test-select-validation.py`; `python scripts/validate-release-ci.py --version v0.1.5`.

### TREL-010. Generated-output currency checks are required

- Covers: REL-R18 through REL-R20, E3, EC5, AC-REL-006
- Level: integration
- Fixture/setup: Release gate dry-run or checklist fixture that names `skills.drift`, `adapters.drift`, `scripts/build-skills.py --check`, `scripts/build-adapters.py --check`, adapter archive validation, or current equivalents.
- Steps: Validate complete and missing generated-output proof fixtures; run existing generated-output regression checks when gate scripts change.
- Expected result: Evidence passes only when generated-output currency is proven by repository-owned checks.
- Failure proves: Release evidence can assert generated-output freshness from memory.
- Automation location: release checklist tests; `python scripts/test-adapter-distribution.py`; `python scripts/test-select-validation.py`.

### TREL-011. Release gate dry-run invokes existing release checks without publishing

- Covers: REL-R15 through REL-R27, REL-R42 through REL-R50, E3, E4, EC3, EC5, AC-REL-006 through AC-REL-008
- Level: smoke, integration
- Fixture/setup: Existing `v0.1.5` release metadata and `RELEASE_VERIFY_DRY_RUN=1`.
- Steps: Run `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`.
- Expected result: Output names required gate checks, package/npm checks for npm releases, generated-output checks, release validation, and no real publish command.
- Failure proves: The release gate cannot be rehearsed safely or omits required standing checks.
- Automation location: `scripts/release-verify.sh`; optional assertions in `scripts/test-adapter-distribution.py` or release gate tests.

### TREL-012. Registry verification and publish-path evidence are recorded

- Covers: REL-R36, REL-R37, REL-R42 through REL-R56, E4, EC3, EC4, AC-REL-008, AC-REL-009
- Level: integration
- Fixture/setup: Evidence fixtures for trusted publishing, manual fallback, valid provenance, missing manual fallback reason, missing registry version, missing dist-tag, missing integrity, and missing CLI/npx smoke.
- Steps: Validate fixtures through the release evidence checklist.
- Expected result: Publish path and provenance mode are recorded without secrets; registry verification fields are present; manual fallback includes reason; integrity failures mark failed-after-publish until follow-up.
- Failure proves: Publication can be assumed from local output or unaudited auth path.
- Automation location: release checklist tests.

### TREL-013. Failure and recovery states are distinct

- Covers: REL-R38, REL-R57 through REL-R62, E5, EC2, EC4, AC-REL-012, AC-REL-013
- Level: unit, contract
- Fixture/setup: Evidence fixtures for failed-before-publish, failed-during-publish, uncertain publish outcome, failed-after-publish, duplicate version, bad package content, fix-forward, dist-tag correction, deprecation, and attempted overwrite.
- Steps: Validate each fixture and negative variant.
- Expected result: Each failure phase has distinct status and recovery notes; uncertain publish outcome requires registry check before retry; overwrite is rejected.
- Failure proves: Bad or uncertain npm publishes can be retried unsafely or hidden behind generic failure notes.
- Automation location: release checklist tests.

### TREL-014. Release evidence rejects secrets and private machine state

- Covers: REL-R39, REL-R45, REL-R66, security/privacy requirements, E4, AC-REL-011
- Level: unit, security
- Fixture/setup: Evidence fixtures containing token-like values, OTP labels, credential fields, private key markers, environment dumps, hostnames, usernames, home-directory paths, and machine-local temp paths.
- Steps: Run checklist validation against forbidden-content fixtures.
- Expected result: Forbidden evidence fails with stable diagnostics; valid command-family summaries pass.
- Failure proves: Durable release evidence can leak credentials or private machine details.
- Automation location: release checklist tests.

### TREL-015. Release evidence template and docs remain contributor-readable

- Covers: contributor UX, observability, performance expectations
- Level: manual
- Fixture/setup: `docs/releases/README.md`, `docs/releases/index.md`, and `templates/release-evidence.md`.
- Steps: Manually review headings, tables, and summaries after M1.
- Expected result: Maintainers can inspect release state without reading full logs; large logs are referenced or summarized.
- Failure proves: The release evidence shape is too vague or too log-heavy to serve as durable proof.
- Automation location: manual checklist in M1 code review.

### TREL-016. Routine release evidence does not update `docs/plan.md`

- Covers: REL-R29 through REL-R31, E6, EC6, AC-REL-014
- Level: contract, migration
- Fixture/setup: Routine release evidence fixture with no active lifecycle plan and release tied to active lifecycle plan fixture.
- Steps: Validate checklist expectations and review changed paths in dry-run/rehearsal evidence.
- Expected result: Routine release updates `docs/releases/v<version>.md` and release index when required; `docs/plan.md` is updated only when an active lifecycle plan owns the release.
- Failure proves: Routine publishes become lifecycle-plan events by default.
- Automation location: release checklist tests; manual review of dry-run evidence.

### TREL-017. Lifecycle closeout artifacts remain synchronized

- Covers: AC-REL-001 through AC-REL-014, plan closeout requirements
- Level: integration
- Fixture/setup: Final change metadata, plan body, plan index, review artifacts, and lifecycle artifacts.
- Steps: Run final metadata, review-artifact, lifecycle, and PR-mode validation commands from the plan.
- Expected result: Plan body, `docs/plan.md`, change metadata, review records, and validation evidence agree before PR handoff.
- Failure proves: The implementation can pass local tests while lifecycle state is stale or contradictory.
- Automation location: `python scripts/validate-review-artifacts.py --mode closeout ...`; `python scripts/validate-change-metadata.py ...`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `bash scripts/ci.sh --mode pr --base <base-sha> --head <head-sha>`.

## Fixtures and data

- Positive routine release evidence fixture derived from `templates/release-evidence.md`.
- Positive emergency deferral fixture with fresh install smoke deferred and registry verification present.
- Negative emergency fixtures for missing owner, missing validation impact, deferred registry verification, deferred release evidence, and deferred secret suppression.
- Version decision fixtures for patch, minor, major, prerelease, stable, no-op, duplicate version, and breaking release with upstream approval.
- Failure-state fixtures for failed-before-publish, failed-during-publish, uncertain outcome, failed-after-publish, fix-forward, dist-tag correction, deprecation, and overwrite attempt.
- Selector path fixtures for `docs/releases/v1.2.3.md` and existing `docs/releases/v0.1.5/release.yaml`.
- Existing release metadata under `docs/releases/v0.1.5/` and existing npm package publication tests.

## Mocking/stubbing policy

- Do not contact npm or publish packages in automated tests.
- Stub registry verification as evidence fixtures for checklist tests.
- Use `RELEASE_VERIFY_DRY_RUN=1` for release gate rehearsal.
- Use existing local release metadata and generated adapter/package tests for integration proof.
- Networked npm registry checks are manual release-operation evidence for future real publishes, not this implementation slice.

## Migration or compatibility tests

- Preserve selector routing for `docs/releases/<version>/release.yaml`, `release-notes.md`, and `npm-publication.md`.
- Preserve `scripts/validate-release.py`, `scripts/validate-release-ci.py`, and `scripts/release-verify.sh` behavior for existing supported releases unless a planned milestone explicitly changes release-gate output.
- Historical release records are valid historical evidence and are not bulk-migrated.
- Release-specific specs may remain stricter and must not be weakened by the standing process.

## Observability verification

- Release evidence fixtures must reconstruct release type, version, source commit, package, dist-tag, gate result, generated-output proof, package preview, publish event, registry result, smoke result, recovery notes, and follow-up.
- Checklist validation must preserve failed, deferred-with-owner-risk, failed-after-publish, and emergency-with-deferred-gate statuses.
- Dry-run evidence must state that no package was published.

## Security/privacy verification

- Automated forbidden-content tests cover token, OTP, credential, private key, private environment dump, hostname, username, home-directory path, and machine-local temp path markers.
- Manual review confirms dry-run evidence contains command families and bounded public facts only.
- Package preview evidence treats secret-bearing files as blockers through existing npm package publication tests.

## Performance checks

- No hard runtime budget is introduced.
- Release gate tests may be slower than inner-loop checks; use focused unit/checklist tests first and full release dry-run only for M3 and final verification.
- Large command logs should be summarized in evidence rather than embedded.

## Manual QA checklist

- Confirm `docs/releases/README.md`, `docs/releases/index.md`, and `templates/release-evidence.md` are readable and do not duplicate historical release YAML as a competing source.
- Confirm `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md`, if created, says no package was published.
- Confirm no release evidence, dry-run evidence, or fixtures contain real credentials, OTPs, usernames, hostnames, or machine-local paths.

## What not to test and why

- Do not perform real npm publication; this implementation defines and rehearses the process.
- Do not require npm credentials, maintainer 2FA, trusted publisher admin access, or live registry writes.
- Do not test staged publishing; it is out of scope until trusted publishing works reliably.
- Do not build a release CLI; broad automation is a follow-on proposal.
- Do not backfill historical releases into `docs/releases/v<version>.md`.
- Do not assert current npm documentation behavior from tests; external npm policy is captured in proposal/spec context and should be rechecked during future release-process policy changes.

## Uncovered gaps

None. Requirements that depend on real npm publication are covered by evidence fixtures, dry-run rehearsal, and future manual release-operation evidence rather than live publish tests.

## Next artifacts

```text
implement M1
code-review M1
review-resolution if triggered
implement M2
code-review M2
review-resolution if triggered
implement M3
code-review M3
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

This proof surface is active for the M1 implementation stage. No implementation, verification, PR readiness, or publish readiness is claimed.
