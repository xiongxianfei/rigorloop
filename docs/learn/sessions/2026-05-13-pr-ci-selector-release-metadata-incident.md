# Learn Session: PR CI Selector and Release Metadata Incident

## Frame

- Trigger: maintainer explicitly invoked `$learn` after asking why the CI bug took so long, what the root cause was, and what lessons it holds.
- Trigger type: explicit maintainer request / failed CI incident retrospective.
- Scope: PR #51 CI failures and remediation for the public adapter artifact migration `v0.1.2` branch.
- Session path: `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md`
- Evidence in scope:
  - Hosted CI run `25810860553`, which blocked before selected checks because `verify-report.md` and `docs/reports/adapter-artifacts/releases/v0.1.2.yaml` were not deterministically classified.
  - Hosted CI run `25812063916`, which failed after selector unblocking because `release.validate` lacked generated release output and full adapter regression exceeded the selected-check timeout locally.
  - Hosted CI run `25812546063`, which failed because selected broad smoke still used dirty-worktree diff-scoped review-root validation in the hosted PR checkout.
  - Hosted CI run `25812923256`, which passed after the final CI shape fix.
  - Plan decision log and validation notes in `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`.
  - Change metadata validation notes in `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`.
  - Remediation commit `8681ee8` (`Fix PR selector routing for release metadata`).
  - CI and selector changes in `scripts/validation_selection.py`, `scripts/ci.sh`, `scripts/validate-release-ci.py`, and `scripts/test-select-validation.py`.
- Explicit exclusions:
  - This session does not claim PR review, release publication, or final lifecycle closeout.
  - This session does not create new authoritative CI, release, or workflow policy.
  - This session does not update curated topic guidance without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-05-11-progressive-loading-high-cost-skills.md`

## Observe

### O1: The delay came from a chain of hidden CI-contract gaps, not one broken line

The first hosted failure was a selector classification bug. After fixing that, the same PR exposed follow-on contract mismatches that had been hidden behind the selector block:

- selected adapter regression used the full adapter test suite, which is larger than the selected-check 60-second timeout budget;
- selected release validation used `python scripts/validate-release.py --version v0.1.2`, but `v0.1.2` archive validation requires generated release output and the accepted `release.source_commit`;
- selected broad smoke delegated to the legacy dirty-worktree broad-smoke shape, which could validate unrelated retained examples in the hosted PR checkout.

Evidence:

- `change.yaml` records `failed_selector_block_verify_report_and_adapter_artifact_metadata`.
- After selector unblocking, local PR-mode CI recorded `fail_after_selector_unblocked_adapter_regression_timeout_and_release_validate_missing_release_output`.
- Hosted run `25812063916` then failed in nested broad smoke, and hosted run `25812546063` showed the selected `broad_smoke.repo` command still ran `bash scripts/ci.sh --mode broad-smoke` without a PR-safe diff-scoped shape.
- Hosted run `25812923256` passed after `broad_smoke.repo` selected `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped`.

### O2: The root cause was incomplete modeling of new release artifacts as first-class CI surfaces

The `v0.1.2` work introduced adapter artifact metadata and archive-backed release validation, but the selector and CI catalog still mostly reflected older assumptions:

- release files could be validated from tracked repository state alone;
- adapter regression could be represented by the full distribution test suite as a selected check;
- broad smoke could safely infer changed roots from the working tree at execution time;
- all change-local lifecycle artifacts were already enumerated.

That model was no longer true once `docs/reports/adapter-artifacts/releases/v0.1.2.yaml`, generated release archives, and change-local `verify-report.md` became part of PR validation.

Evidence:

- `scripts/validation_selection.py` now has explicit routing for `adapter-artifact-metadata` and `verify-report.md`.
- `scripts/validate-release-ci.py` now generates temporary archives and validates `v0.1.2` with the metadata `source_commit`.
- `scripts/ci.sh` now supports `--skip-diff-scoped` for selected broad smoke.

### O3: Local reproduction was necessary but initially insufficient

The first local reproduction proved the selector block was gone, but it also revealed additional failures that were not part of the original hosted log. After those were fixed locally, hosted CI still failed because the hosted checkout's dirty-worktree behavior differed from the clean local checkout.

Evidence:

- Local `bash scripts/ci.sh --mode pr --base 318641d2c42dcf05931c162e1d6b83628b3f2778 --head HEAD` passed before pushing `4c0fda6`.
- Hosted run `25812546063` failed because selected broad smoke still used dirty-worktree review-root discovery.
- The final local PR-mode command passed only after the selected broad-smoke command used `--skip-diff-scoped`; hosted run `25812923256` then passed.

### O4: Existing learn evidence already captures one adjacent pattern

The prior learn session `2026-05-11-progressive-loading-high-cost-skills.md` observed that reproducing hosted CI may require the exact PR base commit. This incident is adjacent but different: the base commit was available and local PR-mode reproduction ran, but hosted state still differed because nested broad smoke used dirty-worktree detection rather than the selector's explicit PR diff.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | pending confirmation | Candidate process-follow-up: use a small "CI contract shape" checklist for new artifact classes before PR handoff | Pending contributor confirmation | This is evidence-bound and reusable, but it should not become durable process guidance until the maintainer confirms the lesson or routes a follow-up. |
| O2 | durable-lesson | pending confirmation | Candidate topic: CI/release validation; possible future spec or workflow update if behavior should become policy | Pending contributor confirmation | The root cause is systemic: new release artifact classes require selector classification, selected-check command shape, timeout fit, and hosted-checkout behavior to be modeled together. |
| O3 | process-follow-up | pending confirmation | Candidate follow-up: add a regression that selected `broad_smoke.repo` uses PR-safe scope rather than dirty-worktree scope | Pending contributor confirmation | The final fix is implemented, but durable prevention would be stronger with an explicit regression for selected broad-smoke command shape and hosted-style dirty checkout. |
| O4 | observation | observation | Session record only | Evidence from prior learn session | The adjacent prior lesson remains useful context but does not fully cover this incident. |

## Route

- Created session record: `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md`.
- No topic file was updated.
- No authoritative artifact was updated from this learn session.
- Candidate durable guidance, pending contributor confirmation: when a change introduces a new artifact class or generated-release validation path, treat CI support as a contract slice with four parts: path classification, selected command shape, runtime budget, and hosted-checkout behavior.
- Candidate process follow-up, pending contributor confirmation: add a focused regression that proves selected `broad_smoke.repo` uses `--skip-diff-scoped` and does not validate unrelated dirty-worktree review roots.

## Direct Answer

Why it took time:

- The original failure was only the first blocking layer. Once fixed, CI progressed far enough to reveal additional incompatible assumptions.
- The bug crossed selector routing, release validation, adapter regression runtime, broad-smoke delegation, and hosted checkout behavior.
- Local and hosted runs were not identical until selected broad smoke stopped relying on dirty-worktree diff detection.

Root cause:

- `v0.1.2` added first-class adapter artifact metadata and archive-backed release validation, but CI still treated release validation and broad smoke like older tracked-repository-only checks.
- The selector knew too little about the new paths, and the selected check catalog had commands that were either too broad for the timeout or missing generated release context.

Lessons:

- New artifact classes need selector routing and CI command shape designed together.
- Selected checks must fit the selected-check timeout budget; full suites belong in broad smoke or explicit verification when they are too slow.
- Release validation that depends on generated artifacts needs a CI wrapper or equivalent reproducible setup, not a tracked-file-only command.
- Nested broad smoke in PR CI should use explicit PR-safe scope, not dirty-worktree inference.

## Validation Evidence

Commands run during the remediation before this learn session:

```bash
python scripts/test-select-validation.py
python scripts/validate-release-ci.py --version v0.1.2
python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files AdapterDistributionTests.test_validate_adapters_cli_accepts_repository_output AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata
bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped
bash scripts/ci.sh --mode pr --base 318641d2c42dcf05931c162e1d6b83628b3f2778 --head HEAD
gh pr checks 51 --watch
```

Result:

- Hosted PR CI passed in run `25812923256` after commit `8681ee8`.

## Follow-Ups

- Pending maintainer confirmation before topic updates or new follow-up work.
- No follow-up has been created by this session.
