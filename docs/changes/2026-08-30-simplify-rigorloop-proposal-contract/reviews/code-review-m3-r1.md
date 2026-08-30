# Code Review M3 R1: Publication Parity

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: M3 implementation commit `788d3ae56dbd3394feeeea6c4bc334df7edeeebf`
Reviewed milestone: M3
Reviewed artifact: commit `788d3ae56dbd3394feeeea6c4bc334df7edeeebf`; workflow handoff commit `647a0e0f` used only as state context
Review status: blocked
Status: blocked
Material findings: SPC-M3-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: blocked
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m3-r1.md` and `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Open blockers: The approved Delivery command targets the already-published `v0.4.1` release as a current candidate, and the implementation makes it pass by replacing immutable published-release identities with current-branch archive identities.
- Next stage: blocked pending delivery-package correction, then review-resolution and M3 implementation correction
- Review status: blocked
- Material findings: SPC-M3-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md` required before correction closeout
- Reviewed milestone: M3
- Milestone closeout: blocked
- Remaining implementation milestones: M3
- Required review-resolution: yes
- Finding IDs: SPC-M3-CR1
- Verify readiness: not-claimed

## Actual-diff summary

The M3 implementation adds direct selection of both proposal-stage packages in local build and supported Codex, Claude, and opencode archive/install parity tests. Those focused tests pass, existing missing and stale resource checks remain present, no generated skill bodies, installed copies, archives, or compressed package outputs are committed, and the implementation evidence truthfully limits its readiness claims.

The same commit also replaces the tracked `v0.4.1` adapter checksums, tree identities, file counts, release-index digest, and package expectation with archives generated from the current branch. That release was published on 2026-08-12 and its durable publication evidence records the original three archive checksums and 75-file installed projections. The changed metadata therefore no longer describes the assets available at its own `v0.4.1` URLs or the recorded release source.

## Finding SPC-M3-CR1

Finding ID: SPC-M3-CR1
Severity: blocker
Location: `docs/reports/adapter-artifacts/releases/v0.4.1.yaml:3-28`; `packages/rigorloop/dist/metadata/adapter-artifacts-v0.4.1.json:3-75`; `packages/rigorloop/dist/metadata/releases.json`; `packages/rigorloop/test/cli.test.js:571-575`; `specs/simplified-proposal-contract.test.md:94`
Evidence: The changed report still binds `v0.4.1` to recorded source commit `a9f1220040acd590f50ff0ed2d50f72d0990bcf0`, but replaces its published archive checksums with current-branch values. `docs/releases/v0.4.1/npm-publication.md` records `Status: published`, the public archive URLs, original checksums `78c67a...`, `bf9ebd...`, and `33e4bf...`, and 75-file installed projections. Running `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto` against this commit fails all three archive checksum comparisons and marks `validation.adapter_artifact_metadata` inconsistent. The package test now asserts the replacement 90-file projection, so it passes by accepting metadata that cannot describe the published package/release pair.
Required outcome: Preserve the published `v0.4.1` report, bundled metadata, release-index digest, and package mapping expectation as historical release evidence, while proving the current proposal/proposal-review projections with temporary current-branch output or a distinct future release-candidate identity.
Safe resolution path: Route CMD-08 and the M3 release-proof wording back to Delivery ownership because `bash scripts/release-verify.sh v0.4.1` treats the historical tag as a current candidate and cannot pass for current canonical sources without rewriting published identities. Replace it with proof that preserves `v0.4.1` through the recorded-source profile and validates current generated archives under a non-published candidate identity or existing temporary-output path. Then revert the five historical metadata/expectation changes, update the M3 evidence to describe the corrected proof, rerun CMD-06/CMD-07 and the corrected release command, resolve this finding, and rereview M3.
needs-decision rationale: The exact approved Delivery package mandates CMD-08 against `v0.4.1`; implementation cannot both satisfy that command as currently defined and preserve the governing immutable historical release evidence. Test-spec and plan ownership must correct the proof target before implementation can close safely.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | SPC-R17 requires coherent supported release surfaces, while the updated `v0.4.1` metadata contradicts its published evidence. SPC-R18 keeps generated archives derived rather than authored truth; the focused temporary projections satisfy that part. |
| Test coverage | concern | The new exact-package and three-adapter tests select both changed skills and pass, but the changed package assertion encodes the incorrect historical projection and the required command omits recorded-source validation. |
| Edge cases | block | The current-canonical versus already-published-version boundary changes the meaning of the archive URLs and checksums. |
| Error handling | pass | Existing missing, stale, escaped, and mixed resource tests remain present, and the recorded-source validator fails with exact checksum diagnostics. |
| Architecture boundaries | block | Canonical resources are correctly generated from `skills/`, but current output is projected into a historical release identity instead of a temporary or new release-candidate boundary. |
| Compatibility | block | Public `v0.4.1` evidence and the package-bundled `v0.4.1` metadata now disagree on every archive identity and installed file count. |
| Security/privacy | pass | No credential, permission, network-authority, logging, or private-data behavior changed; existing archive security validation remains in the selected adapter suite. |
| Derived artifact currency | block | Current temporary projections are coherent, but the tracked historical release projection is stale relative to its actual published assets because it was replaced with a different tree. |
| Unrelated changes | concern | Refreshing published `v0.4.1` identities exceeds the M3 requirement to validate temporary derived output and violates historical-release preservation. No generated bodies or archives were committed. |
| Validation evidence | block | The two focused M3 tests pass, but direct recorded-source validation fails with three checksum mismatches and an inconsistent release validation field. A local current-source `release-verify` pass does not establish published-version integrity. |

## Validation and direct proof

- `python scripts/test-build-skills.py BuildSkillsTests.test_proposal_stage_packages_preserve_canonical_resources`: passed, 1 test.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_proposal_stage_packages_pass_supported_archive_install_parity`: passed, 1 test across Codex, Claude, and opencode clean-install paths.
- `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto`: failed as direct negative proof, reporting all three original-versus-replacement archive checksum mismatches and `validation.adapter_artifact_metadata: expected fail, found pass`.
- `git diff --check 788d3ae5^ 788d3ae5`: passed.
- Changed-path inspection found no committed generated skill bodies, repository-local installed copies, `.zip`, or `.tar.gz` outputs.

This review is isolated and does not close M3 or advance final closeout. SPC-M3-CR1 requires upstream Delivery correction, explicit review-resolution disposition, bounded implementation correction, and an independent M3 rereview.
