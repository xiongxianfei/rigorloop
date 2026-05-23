# Release Process Contract Explain Change

## Status

Explain-change recorded for M4 implementation handoff. Final `verify`, PR readiness, and npm publication readiness are not claimed here.

## Summary

This change defines and implements the first slice of a standing RigorLoop release-process contract. Routine publishes remain operations on already-reviewed work, while release-process changes still require the normal lifecycle.

The implementation adds release evidence authoring surfaces, selector routing for flat release evidence files, lightweight lifecycle/checklist validation for release evidence, non-publishing release-gate rehearsal output, dry-run rehearsal evidence, and lifecycle closeout records.

No npm package was published. No registry state, dist-tag, release tag, or public artifact was changed by this implementation.

## Problem

RigorLoop already had lifecycle discipline for deciding what to build and existing release-specific validation for historical npm releases. What was missing was a durable standing process for packaging, publishing, verifying, and recording an already-merged release candidate.

Without a standing contract, each release could be reconstructed from maintainer memory or prior PRs. That creates release safety risks around stale generated output, missing package preview, skipped registry verification, unclear version decisions, secret-bearing evidence, and over-applying proposal/spec/plan ceremony to every routine publish.

## Decision Trail

The accepted proposal selected the rule:

```text
Contract the release process once.
Execute routine publishes many times.
```

Spec review found one material contradiction, `REL-SR1`: the spec required the full release gate before publish while also allowing emergency evidence to record deferred gates. The spec now makes the default gate hard for routine releases and defines a narrow emergency-deferral contract under `REL-R14a` and `REL-R63`, with non-deferrable safety requirements.

Architecture review accepted the first-slice boundary: add evidence/template/routing/checklist/rehearsal support without introducing a broad release CLI, staged publishing, or real npm publication.

Plan review approved four implementation milestones:

- M1: release evidence README, index, and template/checklist.
- M2: flat release evidence routing and lightweight lifecycle/checklist fixtures.
- M3: release gate dry-run contract output and non-publishing rehearsal evidence.
- M4: lifecycle closeout and final validation preparation.

M2 code review found `CR-M2-1`: `docs/releases/v<version>.md` selected only `release.validate`, bypassing the lifecycle checklist added in M2. The fix routes flat release evidence to `artifact_lifecycle.validate` while preserving existing release-directory metadata routing.

## Diff Rationale By Area

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `docs/proposals/2026-05-23-release-process-contract.md` | Records the accepted release-process direction, npm publication policy, routine-publish boundary, failure handling, and first-slice scope. | Establishes the decision that release process is contracted once and routine publishes execute it without new lifecycle ceremony. | Proposal reviews R1/R2 approved. |
| `specs/release-process-contract.md` | Defines the standing requirements for process boundary, version/dist-tag decisions, release gate, evidence, npm policy, registry verification, recovery, emergency deferrals, and non-deferrable requirements. | Converts the proposal into a normative, testable contract. | Spec review R2 approved after `REL-SR1` resolution. |
| `specs/release-process-contract.test.md` | Maps requirements to release evidence fixtures, selector tests, lifecycle/checklist validation, dry-run release-gate proof, and closeout validation. | Makes the standing contract executable without publishing a package. | Test spec approved by the user before implementation. |
| `docs/architecture/system/architecture.md` and `docs/adr/ADR-20260523-release-process-contract.md` | Record the architecture/ADR boundary for standing release evidence, existing release metadata, lifecycle validation, and release-gate rehearsal. | Keeps the first slice within existing workflow/validation components and avoids premature release automation. | Architecture review R1 approved. |
| `docs/releases/README.md` | Explains `docs/releases/v<version>.md`, its relation to existing `docs/releases/<version>/` records, secret suppression, emergency deferrals, and plan-index boundaries. | Gives maintainers contributor-facing guidance for future release evidence. | M1 code-review clean-with-notes. |
| `docs/releases/index.md` | Initializes the release evidence index. | Provides the optional index shape selected by the spec without backfilling historical releases. | M1 code-review clean-with-notes. |
| `templates/release-evidence.md` | Adds the release evidence template/checklist for result, version decision, routine boundary, preflight gate, package contents, publish event, registry verification, recovery, follow-up, and safety review. | Creates a stable evidence authoring surface for routine publish records. | M1 validation and review. |
| `scripts/validation_selection.py` | Detects flat release evidence files under `docs/releases/v<version>.md` and selects `artifact_lifecycle.validate`; preserves directory-style `docs/releases/<version>/release.yaml` routing. | Ensures the new evidence class cannot bypass the checklist validator. | `CR-M2-1` resolution and selector tests. |
| `scripts/test-select-validation.py` | Adds selector regressions for flat release evidence, release guidance files, and existing release-directory metadata. | Proves deterministic routing and avoids `manual-routing-required` or version inference failures. | `python scripts/test-select-validation.py`. |
| `scripts/artifact_lifecycle_validation.py` | Adds lightweight release-evidence checklist validation for required sections, routine gate failures, emergency deferrals, non-deferrable registry verification, and forbidden secret/private-machine markers. | Implements first-slice validation through lifecycle validation rather than a new dedicated validator. | `python scripts/test-artifact-lifecycle-validator.py`. |
| `scripts/test-artifact-lifecycle-validator.py` | Adds positive and negative release-evidence fixtures for the checklist. | Proves missing gate evidence, invalid emergency deferrals, deferred registry verification, and unsafe evidence are rejected. | M2 validation and re-review. |
| `scripts/release-verify.sh` | Prints a standing release-process gate rehearsal summary before release checks, including generated-output currency, package preview/packed smoke, publish path, registry verification, and dry-run no-publish behavior. | Makes the approved standing gate visible during dry-run rehearsal without changing package contents or publishing. | `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`. |
| `scripts/validate-release-ci.py` | Builds historical adapter release archives from the source commit recorded in adapter artifact metadata before validating current release metadata. | Keeps `v0.1.5` release validation executable after later repository source changes, without rewriting historical checksums. | `python scripts/validate-release-ci.py --version v0.1.5`. |
| `scripts/test-adapter-distribution.py` | Adds regressions for release-gate dry-run output and recorded-source release CI validation. | Proves the M3 gate and historical-source behavior directly. | `python scripts/test-adapter-distribution.py`. |
| `docs/changes/2026-05-23-release-process-contract/release-process-dry-run.md` | Records the dry-run rehearsal as not a release and confirms no package, tag, dist-tag, registry state, release evidence record, or public artifact changed. | Provides durable implementation evidence without pretending the process implementation is itself a release. | M3 code-review clean-with-notes. |
| `docs/plans/2026-05-23-release-process-contract.md`, `docs/plan.md`, `change.yaml`, review records, and review logs | Track milestone state, validation evidence, review results, and remaining downstream gates. | Keeps lifecycle state synchronized and reviewable. | Review-artifact and lifecycle validation. |

## Tests Added Or Changed

- `scripts/test-select-validation.py`
  - Flat release evidence path selects `artifact_lifecycle.validate`.
  - Release README/index guidance routes without a version requirement.
  - Existing release-directory metadata routing remains under `release.validate`.
- `scripts/test-artifact-lifecycle-validator.py`
  - Routine release evidence passes only with required sections and gate entries.
  - Missing package preview and incomplete gates fail.
  - Emergency deferrals require owner, rationale, impact, risk, follow-up, and deadline.
  - Registry verification remains non-deferrable.
  - Secret-bearing and private-machine evidence fails.
- `scripts/test-adapter-distribution.py`
  - `release-verify.sh v0.1.5` dry-run names the standing release gate and does not publish.
  - `validate-release-ci.py --version v0.1.5` validates from recorded release source without checksum mismatch.

## Validation Evidence Available Before Final Verify

Implementation and reviews recorded these passing checks:

- `python scripts/test-select-validation.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`
- `python scripts/select-validation.py --mode explicit --path docs/releases/README.md --path docs/releases/index.md`
- `python scripts/select-validation.py --mode explicit --path docs/releases/v0.1.5/release.yaml`
- `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5`
- `python scripts/validate-release-ci.py --version v0.1.5`
- `python scripts/test-adapter-distribution.py`
- `python scripts/test-npm-package-publication.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-release-process-contract`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-23-release-process-contract/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check -- ...`

The M4 handoff validation reruns the closeout, metadata, lifecycle, and selected CI checks named by the plan. Final `verify` remains a downstream stage and must make its own readiness judgment.

## Review Resolution Summary

Detailed review records live under `docs/changes/2026-05-23-release-process-contract/reviews/`.

Material findings resolved:

- `REL-SR1`: accepted and resolved by defining the emergency full-gate exception in the requirements body, adding `REL-R14a`, aligning `REL-R63`, and clarifying non-deferrable release requirements.
- `CR-M2-1`: accepted and resolved by routing `docs/releases/v<version>.md` to `artifact_lifecycle.validate` and updating selector tests to assert that route directly.

Clean review events with no material findings were recorded for proposal-review R1/R2, spec-review R2, architecture-review R1, plan-review R1, code-review M1 R1, code-review M2 R2, and code-review M3 R1.

## Alternatives Rejected

- Require proposal/spec/plan for every routine publish: rejected because routine publish is an operation on already-decided work.
- Keep releases ad hoc: rejected because release quality would depend on maintainer memory.
- Fully automate release immediately: rejected as too broad for the first slice and risky around real npm publication.
- Add a dedicated release-evidence validator immediately: deferred until evidence shape stabilizes.
- Require staged publishing in the first process: deferred until trusted publishing works reliably.
- Backfill historical releases into `docs/releases/v<version>.md`: rejected for this slice; historical release records remain valid in their existing shape.

## Scope Control

This implementation preserves the first-slice non-goals:

- no npm publication;
- no GitHub trusted publishing workflow configuration;
- no staged publishing;
- no release CLI/scaffolding;
- no package behavior, CLI behavior, skill behavior, adapter layout, or lockfile semantic change;
- no historical release evidence backfill;
- no stored tokens, OTPs, credentials, private environment dumps, hostnames, usernames, or machine-local path dependencies in release evidence.

## Risks And Follow-Ups

Remaining risks:

- The release evidence checklist is intentionally lightweight and may need a dedicated validator after real release evidence stabilizes.
- Trusted publishing remains preferred but not configured by this first slice.
- Live registry verification is named by the contract but not executed by this implementation because no package is published.

Follow-up proposals identified by the proposal/spec remain appropriate:

- GitHub Actions trusted publishing workflow.
- Staged publishing after trusted publishing works reliably.
- Dedicated release-evidence validator.
- Release CLI/scaffolding.
- Changelog/release-notes generation.
- Backport and LTS release policy.

## Current Readiness

M1 through M4 are closed after clean code review. Final `verify` passed on the committed branch state, including PR-mode selected CI, broad smoke, release-gate dry-run rehearsal, release CI validation for `v0.1.5`, selector regression, lifecycle regression, review-artifact closeout, and change metadata validation.

PR #89 is open for hosted CI and human review. This artifact does not claim that a package was published, that hosted CI passed, or that the change is a real npm release.
