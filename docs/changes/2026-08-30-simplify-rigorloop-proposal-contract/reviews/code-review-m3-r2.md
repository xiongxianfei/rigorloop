# Code Review M3 R2: Publication Parity Rereview

Review ID: code-review-m3-r2
Stage: code-review
Round: r2
Reviewer: Codex independent code-review context with fresh-assumption reset
Review date: 2026-08-30
Target: corrected complete M3 state through commit `7491345b`
Reviewed milestone: M3
Reviewed artifact: original implementation `788d3ae5`, Delivery correction and approval `3c4aff53` and `004b711d`, implementation correction `2acecb1c`, resolution `49ea6080`, and rereview routing `7491345b`
Review status: changes-requested
Status: changes-requested
Material findings: SPC-M3-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m3-r2.md` and matching change-local review evidence
- Open blockers: none; one focused evidence-attribution correction is required
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SPC-M3-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-log.md`
- Review resolution: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3
- Required review-resolution: yes
- Finding IDs: SPC-M3-CR2
- Verify readiness: not-claimed

## Actual-diff summary

The corrected M3 implementation retains only two behavior changes: the local skill-build test compares every generated file for `proposal` and `proposal-review` with canonical source, and the adapter-distribution test builds temporary archives and clean-installs both packages across Codex, Claude, and opencode. The corrected Delivery R3 package separates current temporary projection proof in CMD-07 from immutable historical release proof in CMD-08.

`SPC-M3-CR1` is resolved. The published `v0.4.1` report, bundled metadata, release-index digest, and package expectation are byte-identical to their pre-M3 state. Recorded-source validation passes against source `a9f1220040acd590f50ff0ed2d50f72d0990bcf0`. The complete build and adapter suites pass, including missing, stale, escaped-resource, archive-security, clean-install, and no-generated-archive checks. No generated skill body, repository-local installed copy, archive, or compressed package output is committed.

One evidence line remains stale: the corrected M3 evidence names Delivery Review R2 as the approval for the plan, but the command split it reports was introduced after R2 and is authorized by Delivery Review R3.

## Finding SPC-M3-CR2

Finding ID: SPC-M3-CR2
Severity: minor
Location: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m3-publication-parity.md:20`
Evidence: The M3 evidence says the plan is “approved in `delivery-review-r2`,” while the plan and test specification were changed in commit `3c4aff53` to replace CMD-08, and `delivery-review-r3` is the exact approval recorded in `change.yaml` and `reviews/delivery-review-r3.md`. The evidence itself relies on that R3-only split when it states that CMD-07 owns current temporary parity and CMD-08 owns recorded-source historical validation.
Required outcome: The M3 evidence must identify `delivery-review-r3` as the exact approved Delivery package authorizing the corrected M3 proof.
Safe resolution path: Change only the stale review ID in the M3 evidence from `delivery-review-r2` to `delivery-review-r3`, record the accepted disposition, run review/change-metadata validation and `git diff --check`, then request a focused M3 R3 rereview of that evidence correction.
needs-decision rationale: none; this is a safely actionable evidence-attribution correction owned by implementation/review-resolution.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | SPC-R17/SPC-R18, BND-COMPOSE-001, BND-RECOVERY-001, and INT-003 are directly covered by current temporary projection and immutable recorded-source proof. |
| Test coverage | pass | The new tests select both proposal-stage packages and every supported adapter; the 8-test build suite and 152-test adapter suite include missing, stale, mixed, escaped, security, and committed-output regressions. |
| Edge cases | pass | Current versus historical identity, three adapter roots, opencode command aliases, missing/stale resources, and clean-install materialization have direct proof. |
| Error handling | pass | Existing validators fail on missing archives, missing or stale mapped resources, unsafe paths, invalid selections, and recorded-source mismatches. |
| Architecture boundaries | pass | `skills/` remains canonical; current archives and install roots are temporary; historical release validation rebuilds from its recorded source. |
| Compatibility | pass | All four reviewed `v0.4.1` metadata/expectation surfaces match their pre-M3 bytes, and recorded-source validation passes. |
| Security/privacy | pass | Existing archive traversal, resource containment, and release security checks pass; no new network authority, secret, permission, or logging behavior is introduced. |
| Derived artifact currency | pass | Canonical proposal-stage resources equal generated temporary packages, and all supported temporary archive/install projections validate without tracked generated bodies. |
| Unrelated changes | pass | The complete M3 behavior diff is limited to two focused tests; remaining tracked changes are required evidence, Delivery correction, review, resolution, and routing records. |
| Validation evidence | concern | The commands and results are current and pass, but the evidence attributes them to superseded Delivery Review R2 instead of the exact R3 package. |

## Validation and direct proof

- `git diff --exit-code 8581b3ad -- docs/reports/adapter-artifacts/releases/v0.4.1.yaml packages/rigorloop/dist/metadata/adapter-artifacts-v0.4.1.json packages/rigorloop/dist/metadata/releases.json packages/rigorloop/test/cli.test.js`: passed; all four historical surfaces match their pre-M3 state.
- `python scripts/test-build-skills.py`: passed, 8 tests.
- `python scripts/build-skills.py --check`: passed using temporary generated output.
- `python scripts/test-adapter-distribution.py`: passed, 152 tests.
- `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto`: passed for recorded source `a9f1220040acd590f50ff0ed2d50f72d0990bcf0` and all supported adapter archives.
- Complete M3 changed-path inspection found no tracked generated skill bodies, repository-local installed copies, `.zip`, or `.tar.gz` output.

This isolated rereview does not close M3 or advance final closeout. `SPC-M3-CR2` requires review-resolution, the one-line evidence correction, and focused independent rereview.
