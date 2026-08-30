# Code Review M4 R1: Final Holistic Review

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: complete branch diff from `origin/main` through commit `c3238d0382bccacf7f3ab000261847ef3821f4a8`
Reviewed milestone: M4
Reviewed artifact: branch diff `origin/main...c3238d0382bccacf7f3ab000261847ef3821f4a8`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M4-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m4-r1.md`, `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`, `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`, and the review projection in `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`
- Open blockers: review closeout validation incorrectly treats Markdown source order as review chronology, so seven superseded blocking reviews fail final closeout.
- Next stage: review-resolution, then a bounded validator correction and independent final holistic rereview
- Review status: changes-requested
- Material findings: SPC-M4-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`
- Reviewed milestone: M4
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: SPC-M4-CR1
- Verify readiness: not-claimed

## Actual-diff summary

The complete branch diff consistently simplifies proposal authoring and review across the canonical proposal and proposal-review skills, templates, governance references, validators, tests, and supported adapter generation paths. Current proposal-stage packages are selected directly from canonical resources and proven through temporary build, archive, and clean-install paths for Codex, Claude, and opencode. Missing and stale resources retain deterministic failure behavior. No generated skill bodies, installed copies, or release archives are committed.

The M1-M3 implementation and all accepted corrections are coherent across milestones. The CLI prerequisite retry fix permits an unchanged independent rereview after a blocked review while rejecting altered prior evidence. The published `v0.4.1` report, bundled metadata, release index, and package expectation remain byte-identical to `origin/main`, and recorded-source validation passes. The full package test command passes with 298 passing tests, two intentional skips, and no failures.

The implementation behavior is ready, but final review-evidence closeout is not: the closeout validator reports seven already-superseded review outcomes as open because it searches only entries physically below each blocking entry. The canonical log intentionally keeps clean receipts above detailed findings, so Markdown layout is mistaken for review chronology.

## Finding SPC-M4-CR1

Finding ID: SPC-M4-CR1
Severity: major
Location: `scripts/review_artifact_validation.py:3894-3900`; `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md:5-145`
Evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-30-simplify-rigorloop-proposal-contract` reports seven failures for `design-review-r1`, `delivery-review-r1`, `code-review-m2-r1` through `code-review-m2-r4`, and `code-review-m3-r1`. Each has a higher-round nonblocking rereview for the same review occurrence recorded in the clean-receipt or package-review section, and every material finding has a resolved disposition. `_validate_blocking_review_closeout` nevertheless passes only `log_entries[index + 1:]` to `_has_later_nonblocking_review`, making physical source order an undeclared chronology rule. The helper also compares stage alone, so simply removing the slice would incorrectly let an earlier milestone's higher-numbered code review close a later milestone's R1.
Required outcome: Final closeout must recognize a higher-round nonblocking rereview for the same stable review occurrence regardless of where the canonical review-log section places that entry, while continuing to reject blocking reviews that have neither a later round for that occurrence nor an explicit closeout.
Safe resolution path: Compare review entries by stable occurrence identity (for example, the review ID without its final `-rN` suffix), stage, and numeric round across all log sections instead of using source position or stage alone. Add canonical-order positive coverage and negative cases for no higher round and a higher round belonging to a different implementation milestone, then rerun review-artifact tests, structure and closeout validation, change-metadata validation, and diff checks before final holistic rereview.
needs-decision rationale: The correction is bounded and does not require a product choice, but it changes repository validator behavior and therefore requires implementation ownership rather than review-only editing.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The complete branch implements the approved simplified proposal contract and preserves downstream Design and Delivery authority. |
| Test coverage | concern | All approved implementation commands pass, but no regression covers canonical clean-receipt placement above an earlier detailed blocking review or prevents cross-milestone round matching. |
| Edge cases | block | SPC-M4-CR1 prevents a fully resolved multi-round review history from reaching closeout. |
| Error handling | concern | The validator fails closed, but reports semantically resolved reviews as unresolved because it uses source position. |
| Architecture boundaries | pass | Canonical authored resources remain under `skills/`; package bodies and archives remain generated output. |
| Compatibility | pass | Untouched settled proposal history remains valid, current selected paths use the simplified contract, and historical `v0.4.1` evidence is preserved. |
| Security/privacy | pass | No new credential, permission, network-authority, private-data, or logging behavior was introduced. |
| Derived artifact currency | pass | Temporary current packages match canonical proposal-stage resources across all supported adapters; tracked historical release metadata remains immutable. |
| Unrelated changes | pass | The CLI retry prerequisite is explicitly within final holistic scope; no unrelated generated output or refactor was found. |
| Validation evidence | block | Approved CMD-01 through CMD-12 pass under their specified modes, including CMD-10, but direct closeout-mode evidence validation fails as described in SPC-M4-CR1. |

## Validation and direct proof

- `python scripts/test-skill-validator.py`: passed, 361 tests.
- `python scripts/validate-skill.py skills/proposal && python scripts/validate-skill.py skills/proposal-review`: passed.
- `python scripts/test-artifact-lifecycle.py`: passed, 158 tests.
- `python scripts/test-review-artifacts.py`: passed, 107 tests.
- Explicit-path artifact lifecycle validation from CMD-05: passed.
- `python scripts/test-build-skills.py && python scripts/build-skills.py --check`: passed, 8 tests and a clean build check.
- `python scripts/test-adapter-distribution.py`: passed, 152 tests, including current proposal/proposal-review archive and clean-install parity across all supported adapters.
- `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto`: passed for recorded source `a9f1220040acd590f50ff0ed2d50f72d0990bcf0`.
- `python scripts/validate-docs.py --all`: completed with the documented pre-existing prose baseline; no reported issue is on a changed line.
- `npm test --prefix packages/rigorloop`: passed, 300 total tests, 298 passed, 2 intentionally skipped, 0 failed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`: passed before this review recording.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-30-simplify-rigorloop-proposal-contract`: passed before this review recording.
- `python scripts/validate-skill-boundaries.py`: passed.
- `git diff --exit-code origin/main -- docs/reports/adapter-artifacts/releases/v0.4.1.yaml packages/rigorloop/dist/metadata/adapter-artifacts-v0.4.1.json packages/rigorloop/dist/metadata/releases.json packages/rigorloop/test/cli.test.js`: passed; all four historical surfaces match their pre-branch values.
- Changed-path inspection found no committed generated skill bodies, repository-local installed copies, `.zip`, or `.tar.gz` outputs.
- `git diff --check origin/main...c3238d03`: passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-30-simplify-rigorloop-proposal-contract`: failed with seven false unresolved-review findings, providing the direct evidence for SPC-M4-CR1.

This review records the final holistic finding only. It does not close M4, change lifecycle routing, write explanation or verification evidence, or prepare a pull request.
