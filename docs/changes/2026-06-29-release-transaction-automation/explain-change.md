# Explain Change: Release Transaction Automation and Evidence Generation

## Summary

This change introduces the first reviewed slice of release transaction automation. It adds a release profile contract, release-surface ownership and literal-audit proof, release preparation, release preflight, timing evidence validation, published closeout evidence collection, and focused tests that keep the full release gate intact.

The purpose is to reduce routine release rework caused by duplicated version state and manually shaped evidence, without weakening GitHub release, npm publication, archive integrity, or public `npx` smoke requirements.

## Problem

The release retrospective found that routine releases were expensive because release state was hand-synchronized across package metadata, release docs, shell/Python/JavaScript validation expectations, adapter metadata, tests, and publication evidence.

The accepted direction treats a release as a typed transaction: one release profile drives generated release surfaces, validator-compatible pending and published evidence, cheap preflight, full release verification, public closeout, and timing evidence.

## Decision Trail

| Stage | Decision | Artifact |
| --- | --- | --- |
| Proposal | Use the release profile, generators, preflight, closeout, and timing direction. | `docs/proposals/2026-06-29-release-transaction-automation.md` |
| Proposal review | Make profile location, generated-surface ownership, and preflight/full-gate boundary explicit before spec. | `docs/changes/2026-06-29-release-transaction-automation/reviews/proposal-review-r1.md` |
| Spec | Define release profile ownership, routine/special release boundaries, generated surfaces, preflight, full gate, closeout, timing, and historical compatibility. | `specs/release-transaction-automation.md` |
| Architecture | Record the release profile as durable release evidence under `docs/releases/profiles/<tag>.yaml`, not script-owned state. | `docs/adr/ADR-20260629-release-transaction-profile.md` |
| Plan | Split implementation into M1 through M6: profile, ownership/audit, prepare-release, preflight, timing/parity, closeout. | `docs/plans/2026-06-29-release-transaction-automation.md` |
| Test spec | Add proof-contract details, fixture layout, command ownership, direct negative tests, and release command boundaries. | `specs/release-transaction-automation.test.md` |
| Reviews | Resolve 10 material findings: 2 test-spec-review findings and 8 code-review findings across M1-M6. | `docs/changes/2026-06-29-release-transaction-automation/review-resolution.md` |
| Verify / CI maintenance | Verify found selector routing could not cover the new release transaction script and fixture family. CI maintenance added deterministic routing through `release_transaction.regression`. | `docs/changes/2026-06-29-release-transaction-automation/verify-report.md` |

Key requirement groups implemented include profile source of truth (`R1`-`R6`), generated-surface ownership and pending evidence (`R7`-`R17`), release preflight (`R18`-`R27`), full gate parity and timing (`R28`-`R30`, `R39`-`R42`), public closeout (`R31`-`R38`), and historical compatibility / behavior preservation (`R43`-`R44`).

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `scripts/release_transaction.py` | Added release profile loading/validation, surface inventory and literal-audit validation, generated-region helpers, prepare-release planning, pending evidence validation, preflight, timing validation, workflow parity, public closeout providers, and published evidence validation. | Centralizes release transaction logic behind typed helpers instead of scattering version and evidence rules across scripts. | Spec `R1`-`R44`; ADR profile decision; plan M1-M6. | `python scripts/test-release-transaction.py` |
| `scripts/prepare-release.py` | Added CLI wrapper for profile-backed release preparation and check mode. | Gives maintainers a single command to generate routine pending release surfaces without publishing. | Spec `R12`-`R17`; plan M3. | Prepare-release tests and `python scripts/prepare-release.py --help` |
| `scripts/release-preflight.py` | Added CLI wrapper for cheap deterministic release-state checks, including default Git changed-file discovery. | Catches profile drift, metadata drift, unauthorized literals, local inputs, pending evidence shape, release-output dirtiness, and tag conflicts before the full gate. | Spec `R18`-`R27`; plan M4; `CR-RTA-M4-F1`, `CR-RTA-M4-F2`. | Preflight tests and `python scripts/release-preflight.py --help` |
| `scripts/close-release-publication.py` | Added closeout CLI and fixture-mode guard. | Makes routine closeout collect public GitHub/npm metadata and fresh public `npx` smoke through providers before writing published evidence. | Spec `R31`-`R38`; plan M6; `CR-RTA-M6-F1`. | Closeout provider tests and `python scripts/close-release-publication.py --help` |
| `scripts/validate-release.py` | Wired release transaction timing and published evidence validation into the existing release validation command. | Ensures the full gate inherits timing and published-evidence failures when a profile requires them. | Spec `R28`-`R30`, `R39`-`R42`; `CR-RTA-M5-F1`. | Command-level validate-release timing and published-evidence tests |
| `scripts/release-verify.sh` | Preserved `validate-release.py` as the release validation path and added dry-run/parity support used by tests. | Keeps `release-verify.sh <tag>` the authoritative full local gate while enabling fixture-safe proof. | Spec `R28`-`R30`; test spec `RTA-T016`, `RTA-T017`. | `RELEASE_VERIFY_DRY_RUN=1 ... bash scripts/release-verify.sh v0.3.5` |
| `scripts/validation_selection.py`, `scripts/test-select-validation.py` | Added `release_transaction.regression`, classified release transaction scripts and fixtures as `release-transaction`, and added selector regression coverage. | Removes the verify blocker where `bash scripts/ci.sh --mode explicit --path ...` stopped on `manual-routing-required` and `unclassified-path` for the new release transaction family. | Verify report `RTA-VERIFY-B1`; CI-maintenance handoff. | `python scripts/test-select-validation.py`; targeted selector run; full `bash scripts/ci.sh --mode explicit --path ...` |
| `scripts/test-release-transaction.py` | Added the focused release transaction test suite covering M1-M6. | Provides direct proof for profile schema, surface ownership, literal audit, prepare-release, preflight, timing, release gate parity, closeout, and published evidence. | Test spec `RTA-T001` through `RTA-T025`; `TRTA-*` proof contracts. | Focused release transaction test runs recorded in the plan and `change.yaml` |
| `tests/fixtures/release-transaction/**` | Added valid and invalid profile, surface-inventory, and literal-audit fixtures. | Makes required positive and negative proof cases explicit and reviewable. | Test spec fixture layout and M1/M2 review findings. | Fixture-backed unit and integration tests |
| `docs/changes/2026-06-29-release-transaction-automation/release-surface-inventory.yaml` | Added the release surface ownership inventory. | Records generated, human-authored/profile-checked, and historical immutable release surfaces. | Spec generated-surface ownership; `CR-RTA-M2-F2`. | Inventory validation tests |
| `docs/changes/2026-06-29-release-transaction-automation/release-literal-audit-baseline.yaml` | Added baseline literal-audit evidence. | Separates generated-current, profile-owned, historical, baseline-drift, and unauthorized literals. | Test spec literal-audit baseline contract. | Literal-audit validation tests |
| `docs/changes/2026-06-29-release-transaction-automation/behavior-preservation.md` | Added behavior-preservation proof. | Shows full gate, GitHub/npm evidence, public smoke, adapter metadata, historical fixtures, and timing behavior are preserved or strengthened. | Spec `RTA-T024`; plan M6. | Lifecycle validation |
| `docs/learn/sessions/2026-06-29-release-time-root-cause.md`, `docs/learn/sessions/2026-06-29-release-automation-review-findings.md` | Recorded release-time and review-finding retrospectives from explicit `$learn` requests. | Captures why release automation was proposed and why review findings clustered around proof/command-boundary gaps. | Learn sessions requested during this initiative. | Included as intentional change-pack context; no topic routing performed. |
| `docs/proposals/**`, `specs/**`, `docs/architecture/system/architecture.md`, `docs/adr/**`, `docs/plans/**`, `docs/plan.md` | Added or updated lifecycle source artifacts and state. | Records the accepted direction, contract, architecture decision, implementation plan, and current handoff state. | Workflow contract and plan policy. | Artifact lifecycle validation |
| `docs/changes/**/reviews`, `review-log.md`, `review-resolution.md`, `change.yaml` | Recorded proposal/spec/architecture/plan/test-spec/code review evidence and finding resolutions. | Keeps material findings traceable and closed before explanation/verify. | Review-recording rules. | Review artifact validation and closeout checks |

## Tests Added Or Changed

The primary test owner is `scripts/test-release-transaction.py`.

| Test area | What it proves | Why this level is appropriate |
| --- | --- | --- |
| Release profile tests | Valid routine profiles load; profile paths resolve under `docs/releases/profiles`; malformed, missing-field, unknown-kind, unknown-target, special-release-without-rationale, and version mismatch cases fail closed. | The release profile is the source of truth, so schema and vocabulary errors must fail before downstream generation. |
| Surface inventory tests | Release surfaces are classified, unknown/missing classifications fail, manual overrides need rationale, and the change-local inventory loads. | Ownership rules prevent generated/human/historical surfaces from drifting. |
| Literal audit tests | Baseline drift, unknown/missing classifications, unauthorized changed literals, historical rationale, and generated-current owner requirements are enforced. | Current-version literal drift was a core release-cost root cause. |
| Prepare-release tests | Generated pending artifacts are idempotent, check mode reports changes, pending evidence validates, no external publication happens, and CLI check mode works. | Generation must be deterministic and non-publishing. |
| Pending evidence negative tests | Published result in pending evidence, `npx -y`, missing/duplicate/unknown targets, and table/YAML mismatch fail. | `CR-RTA-M3-F1` showed global fragment checks were too weak; target-bound validation is required. |
| Preflight tests | Clean fixture is side-effect-light; CLI works; non-Git roots fail without explicit changed files; missing/malformed/incomplete profiles, missing local inputs, package drift, metadata drift, invalid pending evidence, dirty release-output, unauthorized literals, local tags, remote tag conflicts, and unreachable remote diagnostics are covered. | Preflight owns cheap deterministic release-state failures before the full gate. |
| Gate parity and timing tests | Release verify dry-run preserves full checks, release workflow delegates to `release-verify.sh`, timing skeletons are generated, timing evidence validates, missing/malformed timing fails when profile-required, and duration over target is warning-only. | Timing must be enforced through the release command path without turning first-slice duration targets into hard failures. |
| Closeout and published evidence tests | Closeout waits when public evidence is unavailable, requests GitHub/npm/version smoke/target smoke provider calls, rejects manual evidence in default mode, handles provider failures, uses provider values, validates command/hash/file-count shapes, and leaves historical evidence untouched. | Published release evidence is a supply-chain trust boundary; fixture shape alone is not enough. |
| Selector routing tests | Release transaction scripts and fixtures classify as `release-transaction` and select `release_transaction.regression` without manual-routing or unclassified-path blockers. | This directly resolves the verify blocker for repo-owned CI wrapper coverage of the new script and fixture family. |

## Validation Evidence Available Before Final Verify

Validation evidence is recorded in `docs/changes/2026-06-29-release-transaction-automation/change.yaml` and the active plan. Key commands include:

- `python scripts/test-release-transaction.py`
- `python scripts/prepare-release.py --help`
- `python scripts/release-preflight.py --help`
- `python scripts/close-release-publication.py --help`
- `python scripts/validate-release.py --help`
- `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py scripts/validate-release.py scripts/close-release-publication.py`
- `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=/tmp/rigorloop-release-output RELEASE_COMMIT=fixture-commit bash scripts/release-verify.sh v0.3.5`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files AdapterDistributionTests.test_validate_adapters_cli_rejects_retired_repository_output AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-29-release-transaction-automation/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-29-release-transaction-automation/`
- `git diff --check --`

Earlier selector validation reported manual routing for new release transaction scripts and fixture directories. That became a verify blocker, so CI maintenance added deterministic `release_transaction.regression` routing for the script and fixture family.

Post-CI-maintenance validation evidence includes:

- `python scripts/test-select-validation.py` passed with 124 tests.
- `python scripts/select-validation.py --mode explicit --path scripts/release_transaction.py --path scripts/test-release-transaction.py --path scripts/prepare-release.py --path scripts/release-preflight.py --path scripts/close-release-publication.py --path tests/fixtures/release-transaction/profiles/valid-routine-v0.3.5.yaml --path tests/fixtures/release-transaction/literal-audit/valid-baseline.yaml --path tests/fixtures/release-transaction/surface-inventory/valid-inventory.yaml` passed and selected `release_transaction.regression`.
- `bash scripts/ci.sh --mode explicit --path ...` passed over the final changed release automation path set and selected `release_transaction.regression`.

Final `verify` must rerun after this refreshed explanation.

## Review Resolution Summary

Review resolution is closed in `docs/changes/2026-06-29-release-transaction-automation/review-resolution.md`.

Counts:

- Material findings: 10
- Accepted and resolved: 10
- Open findings: 0
- `needs-decision`: 0

Findings resolved:

- `RTA-TSR1`, `RTA-TSR2`: test-spec proof-contract and command ownership details.
- `CR-RTA-M1-F1`: missing profile and required-field coverage.
- `CR-RTA-M2-F1`, `CR-RTA-M2-F2`: missing classification proof and prior profile snapshot inventory.
- `CR-RTA-M3-F1`: structured target-bound pending evidence validation.
- `CR-RTA-M4-F1`, `CR-RTA-M4-F2`: default Git changed-file discovery and named preflight negative tests.
- `CR-RTA-M5-F1`: timing validation wired into `validate-release.py`.
- `CR-RTA-M6-F1`: closeout owns public GitHub/npm metadata and fresh public smoke collection.
- `RTA-VERIFY-B1`: selector routing for the new release transaction scripts and fixtures is resolved by `release_transaction.regression`.

All M1-M6 second code-review rounds are clean.

## Alternatives Rejected

- Parallelizing the release gate first was rejected because it would not remove version-state drift or evidence-shape loops.
- Preflight-only and evidence-template-only approaches were rejected as useful but incomplete.
- Script-owned release profile state was rejected because release profiles are durable release evidence and belong under `docs/releases/profiles/<tag>.yaml`.
- Historical release migration was kept out of scope to avoid rewriting published evidence.
- Hard timing budgets were deferred; timing duration over target is warning-only in this first slice.
- Manual public-evidence files were rejected as sufficient routine closeout proof after `CR-RTA-M6-F1`; they remain allowed only in explicit fixture/import mode.

## Scope Control

This change does not publish a release, create live GitHub releases, run live npm publication in tests, remove the full release gate, remove public smoke, rewrite historical release evidence, or make every historical release conform retroactively.

`release-verify.sh <tag>` remains the authoritative full local release gate. `release-preflight.py` is a cheap deterministic gate, not a substitute for full release verification.

## Risks And Follow-Ups

- Final `verify` still needs to rerun after this refreshed explanation.
- The previous selector-routing blocker is resolved, but verify has not yet recomputed branch readiness after the CI-maintenance diff.
- The release-time and review-finding learn sessions are included as change-pack context; they did not route topic or workflow-policy updates.
- Real production closeout depends on public GitHub/npm availability and public `npx` smoke; tests use provider stubs by design.
- Future releases should collect timing evidence across multiple releases before proposing hard duration budgets or release-gate parallelism.
