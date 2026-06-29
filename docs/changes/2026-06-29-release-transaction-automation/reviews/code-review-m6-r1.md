# Code Review M6 R1

Review ID: code-review-m6-r1
Stage: code-review
Round: M6 R1
Reviewer: Codex code-review skill
Target: M6 commit `47877c73`
Reviewed artifact: M6 implementation diff `47877c73`
Reviewed milestone: M6. Published evidence closeout and behavior preservation
Status: changes-requested
Review status: changes-requested
Review date: 2026-06-29
Recording status: recorded
Material findings: CR-RTA-M6-F1
Immediate next stage: review-resolution

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m6-r1.md, docs/changes/2026-06-29-release-transaction-automation/review-log.md, docs/changes/2026-06-29-release-transaction-automation/review-resolution.md, docs/plans/2026-06-29-release-transaction-automation.md, docs/plan.md, docs/changes/2026-06-29-release-transaction-automation/change.yaml
- Open blockers: none
- Next stage: review-resolution M6
- Review status: changes-requested
- Material findings: CR-RTA-M6-F1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-29-release-transaction-automation/reviews/code-review-m6-r1.md
- Review log: docs/changes/2026-06-29-release-transaction-automation/review-log.md
- Review resolution: docs/changes/2026-06-29-release-transaction-automation/review-resolution.md#code-review-m6-r1
- Reviewed milestone: M6. Published evidence closeout and behavior preservation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6 resolution needed
- Required review-resolution: yes
- Finding IDs: CR-RTA-M6-F1
- Verify readiness: not-claimed

## Review Inputs

- Diff range: `HEAD^..HEAD` at `47877c73`.
- Review surface: `scripts/close-release-publication.py`, `scripts/release_transaction.py`, `scripts/validate-release.py`, `scripts/test-release-transaction.py`, behavior-preservation evidence, active plan M6 state, and change metadata.
- Governing spec: `specs/release-transaction-automation.md` requirements `R31` through `R38`, plus `R43` and `R44`.
- Test spec: `specs/release-transaction-automation.test.md` `RTA-T020`, `RTA-T021`, and `RTA-T023`.
- Active plan milestone: `docs/plans/2026-06-29-release-transaction-automation.md` M6.
- Validation evidence inspected: M6 plan and change metadata entries for focused release transaction tests, `close-release-publication.py --help`, Python compilation, release-verify dry-run, selector-selected adapter/release regression, behavior-preservation artifact lifecycle validation, and whitespace validation.

## Diff Summary

M6 adds `scripts/close-release-publication.py`, closeout helpers in `scripts/release_transaction.py`, published evidence validation wired into `scripts/validate-release.py`, closeout and published-validation tests, and behavior-preservation evidence. The command reads a release profile plus a local public-evidence YAML file, validates required fields and target rows, and writes published `npm-publication.md` evidence.

## Findings

### CR-RTA-M6-F1: Closeout accepts manually supplied public evidence instead of collecting required public metadata and fresh public smoke

Finding ID: CR-RTA-M6-F1
Severity: major
Status: open
Location: `scripts/release_transaction.py:499`
Evidence: The M6 spec requires published evidence closeout to read public GitHub release asset metadata and npm registry metadata before marking evidence published at `specs/release-transaction-automation.md:129`, and to run fresh public `npx` smoke for `version`, `init codex`, `init claude`, and `init opencode` before marking post-publication target smoke as passed at `specs/release-transaction-automation.md:131`. The active plan states the M6 goal is to generate closeout from GitHub/npm/npx data at `docs/plans/2026-06-29-release-transaction-automation.md:258` and says fresh public smoke remains required at `docs/plans/2026-06-29-release-transaction-automation.md:272`. The implementation path in `close_release_publication` only chooses `public_evidence` or `docs/releases/<tag>/public-evidence.yaml`, reads that local file, validates its fields, and writes published evidence at `scripts/release_transaction.py:499` through `scripts/release_transaction.py:541`. There is no subprocess call to `npx`, no npm registry lookup, and no GitHub release asset lookup in `scripts/close-release-publication.py` or `scripts/release_transaction.py`. The tests likewise create a local fixture file with already-filled `version_command`, asset URLs, npm metadata, and target smoke rows in `scripts/test-release-transaction.py:1119` through `scripts/test-release-transaction.py:1190`, then call closeout with that fixture. That proves field-shape validation, but it does not prove the closeout command performs the required public collection or fresh smoke.
Required outcome: `close-release-publication.py <tag>` must collect or execute the required public evidence itself, with fixture/stub injection for tests. It must not mark evidence published solely because a manually authored local evidence file asserts GitHub/npm/npx results.
Safe resolution path: Add closeout-owned provider functions or injectable command/network runners for GitHub release asset metadata, npm registry metadata, npm tarball identity/integrity, and public `npx` smoke. In production/default mode, the closeout command should call those providers and fail clearly when evidence is unavailable. In tests, stub those providers to avoid network and live `npx` execution while proving the command path requests GitHub assets, npm metadata, version smoke, and every target init smoke before writing published evidence. Keep `--public-evidence` only as an explicit fixture/import mode if the spec is revised to allow it, or make it a test-only/private path that cannot satisfy routine closeout without provider proof.
needs-decision rationale: none

## Checklist Coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | `R32` and `R33` require closeout to read public metadata and run fresh public `npx` smoke. The implementation validates a local evidence file instead. |
| Test coverage | block | Tests prove generated evidence shape and validator rejection paths, but no command-path proof shows GitHub/npm collection or fresh public smoke execution/stub invocation. |
| Edge cases | concern | Missing public evidence and malformed command/hash shapes are covered, but the highest-risk edge case, stale or fabricated local public evidence being accepted as published proof, is not prevented. |
| Error handling | concern | Missing evidence fails without writes, but unavailable GitHub/npm/npx state is not independently detected because those sources are not queried. |
| Architecture boundaries | pass | The implementation keeps release transaction logic in shared helpers and uses `validate-release.py` for validation. |
| Compatibility | concern | Historical evidence is preserved and the full release gate command set is unchanged, but the published closeout proof boundary is weaker than the accepted release transaction contract. |
| Security/privacy | pass | No secrets or credentials are introduced. No live network or public smoke is run, which is safe for tests but incomplete for the release contract. |
| Derived artifact currency | pass | Behavior-preservation evidence and change metadata were updated. Generated published evidence is deterministic from the fixture input. |
| Unrelated changes | pass | The diff is scoped to M6 closeout, published validation, tests, behavior-preservation evidence, and lifecycle metadata. |
| Validation evidence | concern | Recorded validation is relevant for shape validation, but it cannot prove `R32`/`R33` because the command never attempts those operations. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

Selector validation still has known manual-routing limitations for release transaction scripts. M6 remains open until the closeout command owns public evidence collection or the governing spec/test spec is explicitly changed.

## Validation

- Reviewed implementation evidence: `python scripts/test-release-transaction.py` passed with 74 tests.
- Reviewed implementation evidence: `python scripts/close-release-publication.py --help` passed.
- Reviewed implementation evidence: Python compilation passed.
- Reviewed implementation evidence: release-verify dry-run passed.
- Reviewed implementation evidence: selected adapter/release regression and behavior-preservation artifact lifecycle validation passed.

## Recommended Next Stage

Enter `review-resolution M6`, implement closeout-owned public metadata and public smoke collection with fixture-safe provider stubs, rerun M6 validation, and return M6 to code review.
