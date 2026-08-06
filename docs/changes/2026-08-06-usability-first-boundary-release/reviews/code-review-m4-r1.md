# Usability-First Boundary-First v0.4.0 Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: 5e6a4ce88ab4e99442e9e75177193646c9164229..cfd7ef0e with cumulative initiative d215c045..cfd7ef0e
Reviewed artifact: commit cfd7ef0e
Reviewed milestone: M4 and final holistic candidate
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-m4-implementation
Reviewer context ID: m4-r1-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: exact-reviewed-baseline-provenance; frozen-inventory-authority; checked-revision-activation; cumulative-selector-integration; routine-release-evidence
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; specs/release-process-contract.md; specs/release-process-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@cfd7ef0e#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@cfd7ef0e#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@cfd7ef0e#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@cfd7ef0e#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@cfd7ef0e#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@cfd7ef0e#sha256:0d40990afa7fca98282552bfc08086840c169a18943139f3994d5e52e3a8b8f1; range:5e6a4ce88ab4e99442e9e75177193646c9164229..cfd7ef0e.diff@cfd7ef0e#sha256:8d04895faa71056843cfd4080b18d7f1548242576fd55d9c9c8f3f1fb578dd4c; range:d215c045..cfd7ef0e.diff@cfd7ef0e#sha256:faa3dc4eb65ca4bd8aca314bf015d11808b67d49852ce984db367bd8b593025d
Prompt template version: code-review-v1
Initial packet hash: sha256:8d04895faa71056843cfd4080b18d7f1548242576fd55d9c9c8f3f1fb578dd4c
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: exact active snapshot; frozen historical compatibility; current-file validation; rollback selection; cumulative routine-release integration
Highest-impact failure modes: wrong reviewed baseline; incomplete or differently sorted inventory; recurring history dependency; false public claim; selector regression; rollback substitution; archive-source identity conflation
Changed boundaries: BND-STATE-001; BND-AUTH-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-COMPAT-001; BND-ENV-001; INT-002; INT-003
Evidence expected: independent baseline and inventory proof; no-history active validation; independently valid pending fixtures; exact rollback identities; selector integration; release preparation/preflight; selected CI and full standing-gate evidence; no external mutation
Areas requiring direct inspection: activation tuple; M3 review provenance; Git tree inventory; proof-model readiness; pending fixtures; selector fixtures; rollback metadata; release evidence; archive-source separation
Areas intentionally out of scope: live tag creation; push; publication; merge; public closeout; explain-change; verify; PR readiness
Risk classes considered: requirement-fidelity=applicable; checked-revision-activation=applicable; compatibility-and-selector-integration=applicable; release-identity-and-authority=applicable; package-supply-chain=applicable; recovery-and-rollback=applicable; privacy=applicable; live-publication=not-applicable:forbidden-lifecycle-action; external-mutation=not-applicable:forbidden-lifecycle-action
Falsifiable review questions: Is the baseline exactly the pending source reviewed by M3 R7? Does an independent Git-tree reconstruction equal the frozen 78-item tuple? Can normal active validation run without history, tag, remote, network, or derivation? Does active state preserve every ordinary selector and routine release path?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m4-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: specs/boundary-first-activation.yaml; specs/boundary-first-proof-model.md; scripts/test-boundary-first-validation.py; scripts/test-select-validation.py; docs/releases/v0.4.0.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*; specs/
Requirement-fidelity matched category triggers: spec-derived validators; workflow routing contracts; closed enums; generated-output or package parity validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > cumulative diff > validator assertions > validation evidence > prior findings
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-M4-CR1-001
Material findings: UBR-M4-CR1-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-M4-CR1-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M4-CR1-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-m4-r1`
- Reviewed milestone: M4 and final holistic candidate
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4
- Required review-resolution: yes
- Finding IDs: UBR-M4-CR1-001
- Verify readiness: not-claimed

## Finding UBR-M4-CR1-001

Finding ID: UBR-M4-CR1-001
Severity: major
Location: `scripts/test-select-validation.py:3783`; active compatibility authority in `specs/boundary-first-activation.yaml`
Evidence: `python scripts/test-select-validation.py` reports 1 failure and 146 passes. `ValidationSelectionTests.test_ci_wrapper_executes_selector_selected_path_and_root_checks` still uses `specs/test-layering-and-change-scoped-validation.md`, which is now in the frozen 78-path grandfathered inventory. Its exact CI-wrapper reproduction invokes `python scripts/validate-boundary-first.py --check --path specs/test-layering-and-change-scoped-validation.md`, correctly returns `BFR-GRANDFATHERED-REVIEW`, and contradicts the fixture's expected successful wrapper result.
Required outcome: The cumulative selector suite passes under the active snapshot while preserving the rule that a substantively changed grandfathered spec requires semantic spec-review classification.
Safe resolution path: Retarget the CI-wrapper execution fixture to a current adopting feature spec outside the frozen inventory, or otherwise make the fixture supply the required review classification without weakening active historical-spec enforcement; then rerun the focused reproduction and all 147 selector tests.
needs-decision rationale: none
auto_fix_class: declared-safe

## Exact activation and provenance evidence

- `grandfathering_baseline_revision` is `ca2630e4a0a4bc82c330b51f0480eb97e047ec3f`.
- `git rev-parse 5e6a4ce88ab4e99442e9e75177193646c9164229^` returns that exact identity, so the frozen baseline is the exact source reviewed by clean M3 R7 rather than its later review-evidence commit.
- Independent Git plumbing inspected the baseline commit and every eligible top-level `specs/*.md` blob without importing or calling `derive_grandfathered_specs`. The independently reconstructed inventory has 78 unique paths, is raw-UTF-8 sorted, and exactly equals the active record with no missing or extra path.
- The active tuple is exactly `active`, release intent `v0.4.0`, rollback `v0.3.6`, the full reviewed baseline, and the 78-item frozen inventory. The proof-model status and readiness agree and explicitly deny tag, publication, and public-availability claims.
- The 59 non-authoring boundary tests pass, including no-history active validation with Git subprocess and derivation seams forced to fail, independently constructed pending fixtures, exact rollback selection, privacy suppression, and active output claim separation. The three derivation-unit tests were intentionally not invoked because M4's one-time authoring call had already occurred; independent Git inspection replaced that review proof.

## Prior-finding reconciliation

- M1's semantic-oracle and closed-vocabulary findings remain resolved: the 285 skill tests and 28 reference tests pass, with canonical skill and generated-skill validation current.
- M2's private-path, literal-object, ambient-Git, rollback, and malformed-state findings remain resolved: active validation is current-file-only, v0.3.6 selects the exact three recorded archives, and the no-history fixture executes without Git or derivation.
- M3's preparation, dist-tag, tag-identity, standing-record, complete-evidence, state-matrix, and emergency-deferral findings remain resolved: preparation and preflight pass, 102 release-transaction tests and 168 lifecycle tests pass, recorded-source release validation succeeds, and archive-source commit `c7b0babe6e8c91655c2b98f4092197eef5fabc69` remains distinct from both the activation baseline and future trusted tag authority.
- No `v0.4.0` tag exists, and review execution performed no tag, push, publication, registry write, merge, network release check, or public-success claim.

## Release evidence challenge

- `python scripts/prepare-release.py v0.4.0 --check` — pass; no changes.
- `python scripts/release-preflight.py v0.4.0 --skip-remote` — pass with the pre-existing report-only v0.3.4 literal warning.
- `python scripts/validate-release.py --recorded-source-auto --version v0.4.0` — pass; all three archives rebuilt and metadata validated against the separate recorded source commit.
- `python scripts/test-release-transaction.py` — pass, 102 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — pass, 168 tests.
- `python scripts/test-adapter-distribution.py` — pass, 149 tests.
- `python scripts/test-npm-package-publication.py` — pass, 6 tests.
- The implementation receipt records actual passing executions of release-selected CI and `release-verify.sh` on the active snapshot. The reviewer challenged their selector description, component suites, archive reconstruction, recorded-source release validation, preparation, and preflight rather than rerunning the two umbrella commands after the cumulative selector finding stopped clean closeout.

## Checklist coverage

- Spec alignment: blocked only by UBR-M4-CR1-001; active historical enforcement is correct, but the cumulative selector proof did not migrate with it.
- Test coverage: blocked; one selector integration fixture is stale after the active snapshot.
- Edge cases: pass for wrong tuples, missing history, absent tag, unavailable baseline, malformed state, inventory order/uniqueness, and rollback divergence.
- Error handling: pass; active selector failure is bounded and identifies the required semantic review.
- Architecture boundaries: pass; no writer, public CLI, transition ledger, custom publisher, or recurring history authority was introduced.
- Compatibility: blocked only by the stale selector test; the frozen inventory and prospective-adoption rule themselves are exact.
- Security/privacy: pass; diagnostics and evidence remain repository-relative and private-value bounded.
- Derived artifact currency: pass; skills, packages, archives, and preparation output are current.
- Unrelated changes: pass; M4 is scoped to the activation tuple, proof-model state, fixtures, release evidence, and lifecycle evidence.
- Validation evidence: blocked; the cumulative selector suite is red despite the focused activation and release-owned gates passing.

## Final holistic assessment

The reviewer inspected the complete initiative range `d215c045..cfd7ef0e`, the governing proposal/spec/test-spec/architecture/ADR/plan, all M1-M3 material finding dispositions, M4's exact diff, generated and release identities, and cumulative validation selection. The exact activation and release authority is sound, but a final holistic approval cannot be issued while UBR-M4-CR1-001 leaves a cumulative suite red. Explain-change and verify remain blocked until review-resolution corrects the fixture and an independent M4 R2 rereview closes the finding.

## Handoff

M4 remains open in `resolution-needed`. Resolve UBR-M4-CR1-001 without weakening grandfathered-spec semantic-review enforcement, rerun the focused CI-wrapper reproduction and the full selector suite, then request independent M4 R2. Final holistic approval, explain-change, and verify remain pending.
