# PR Full-Gate Correction Code Review R3

Review ID: code-review-pr-full-gate-r3
Stage: code-review
Round: 3
Reviewer: Codex independent contract-first code-review peer
Target: f0b1b6fc..e193e1f7
Reviewed artifact: commit e193e1f755ea7571f2cbc19a919ab184065414a9
Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-pr-full-gate-correction-r3
Reviewer context ID: pr-full-gate-r3-fresh-contract-first-reviewer
Context separation mechanism: separate-agent-contract-first-rereview
Author context excluded: true
Risk tier: high
Risk-tier triggers: spec-derived-validator-authority; closed-vocabulary-fail-closed; release-selector-regression-safety; historical-package-compatibility; post-verify-pr-correction
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: CONSTITUTION.md; schemas/change.schema.json; specs/boundary-first-proof-model.md; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; spec-review-r5; test-spec-review-r4; specs/target-native-init.md; specs/target-native-init.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@e193e1f7#sha256:5727760223fbeb9a50a8eb7c440820ca3eeaf09a0940f7bae095c7b13309d900; schemas/change.schema.json@e193e1f7#sha256:fa3d07dd253a4816f9e143f6b9243767da248613f91c57ddb8508b35c0f67db6; specs/boundary-first-proof-model.md@e193e1f7#sha256:f4a4ce4860981af14484c4d4f15edc362cf269806d2fe7f052db5bfff11ed159; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md@e193e1f7#sha256:46865935c04fa404a38b34c96f7c19f5934a6b9eee672081f22b3cfc2ff64ba4; specs/usability-first-boundary-release.md@e193e1f7#sha256:5045edf83c5e71531445f524b88c4098f28fc115bf6ba8277335c178058bf6cd; specs/usability-first-boundary-release.test.md@e193e1f7#sha256:4669a662b16d87e236ecb0387135431e7ae706f05b6532a4d51529b60745b833; specs/target-native-init.md@e193e1f7#sha256:0b27d8c6df0eac7edd8ede0c480bc2822e989bc0f6c6e4e0c82f59446e3f86e0; specs/target-native-init.test.md@e193e1f7#sha256:32a6b10f3c1a19fcfb128fa948cbb2fcf2fcac5fc50a4c08021aa36d9e0c4c0a; docs/architecture/system/architecture.md@e193e1f7#sha256:e093f7e58b50a8851765c1a5c8edba701f43f0cc9b1e466a8e2d334a6c7e7dfc; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@e193e1f7#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@e193e1f7#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@e193e1f7#sha256:eeae232b336cae1f4443951446aae09fb056bf2cb4701ecf157ef1f95f81a7c1; scripts/boundary_first_validation.py@e193e1f7#sha256:a5f9299327f974dcf29a0e5396092760ab95470c454fc6a7154fbc05f4e99376; scripts/test-boundary-first-validation.py@e193e1f7#sha256:1d65ebd6bb3bf6d966d895a49673c904ac590e37ba6f0364012b3903218f92d7; scripts/validation_selection.py@e193e1f7#sha256:6ac7831ec8f4baa51f717bb78d1860591cd7720ccd58d60ce529b5ab0520396a; scripts/test-select-validation.py@e193e1f7#sha256:89e45952a75b8269553b82b11a427034d887a6d9d194d91f1f306fd6161274ad; packages/rigorloop/test/cli.test.js@e193e1f7#sha256:4717358d9f590d6b807bc6f71d3b5e8a611004c0d42017f6b253d27528bc1bd5; range:f0b1b6fc..e193e1f7.diff@e193e1f7#sha256:b978353c9ddaf01a79c241ac5a3fde02f3ed606f26cc6c7c51ed9d636057ad2a
Prompt template version: code-review-v1
Initial packet hash: sha256:b978353c9ddaf01a79c241ac5a3fde02f3ed606f26cc6c7c51ed9d636057ad2a
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: lifecycle-selected boundary marker placement; lifecycle authority parsing; release-profile routing; current package identity; historical opencode compatibility proof
Highest-impact failure modes: stage-owned status bypass; unknown lifecycle authority downgraded to legacy; semantic YAML value misclassified; malformed profile version fabrication; current metadata replacing historical proof
Changed boundaries: cross-file lifecycle authority; exact marker placement; YAML scalar identity; profile path-to-version extraction; current-versus-historical fixture identity
Evidence expected: governing clauses and schema; cumulative diff; reciprocal and vocabulary probes; focused T24; profile negative; historical package tests; prior-finding reconciliation
Areas requiring direct inspection: authority parser and both marker branches; T24 fixtures; lifecycle schema; profile namespace branch; fixture identity helpers; review evidence
Areas intentionally out of scope: broad smoke; hosted CI; PR opening; push; tag; publication; merge; public closeout
Risk classes considered: requirement-fidelity; spec-derived-validation; closed-vocabulary-validation; fail-closed-release-routing; package-supply-chain; compatibility-and-migration; lifecycle-closeout; live-publication=not-applicable:forbidden; external-mutation=not-applicable:forbidden
Falsifiable review questions: Does exact authority select placement? Do present unknown values fail rather than become legacy? Does YAML quoting preserve semantic authority? Do profile and historical fixture corrections remain safe?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-full-gate-r3.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/test-boundary-first-validation.py; scripts/validation_selection.py; scripts/test-select-validation.py; packages/rigorloop/test/cli.test.js; schemas/change.schema.json; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*; specs/; docs/changes/**/reviews/; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: spec-derived validators; artifact lifecycle validators; workflow routing contracts; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > lifecycle schema and stage-owned scope > approved test proof > cumulative diff > direct probes > focused regressions > author evidence > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: UBR-PRFG-CR3-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed; M1-M4 remain closed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: UBR-PRFG-CR3-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-PRFG-CR3-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-full-gate-r3.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-pr-full-gate-r3`
- Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: UBR-PRFG-CR3-001
- Verify readiness: not-claimed

## Finding UBR-PRFG-CR3-001

Finding ID: UBR-PRFG-CR3-001
Severity: major
Location: `scripts/boundary_first_validation.py:363`; `scripts/test-boundary-first-validation.py:336`; `schemas/change.schema.json:20`; `CONSTITUTION.md`
Evidence: `_stage_owned_marker_authority` extracts the top-level value with a text regex, rejects only duplicate matches, and returns non-stage-owned for every single value other than the literal unquoted text. The change schema defines the only present vocabulary value as `stage-owned-change-local-v1`, while absence represents historical pre-adoption state. Direct paired probes show `lifecycle_contract: future-contract-v2` plus the status marker returns no issue, so an unknown authority silently receives legacy behavior. They also show YAML-equivalent `lifecycle_contract: "stage-owned-change-local-v1"` rejects the owner form and accepts the status form, even though the repository change-metadata parser accepts that quoted scalar. The added test encodes `lifecycle_contract: legacy` as a successful non-stage-owned status fixture and has no `unknown_value` regression. This violates the repository rule that closed vocabularies fail before consistency checks and lets presentation syntax change lifecycle authority.
Required outcome: Parse or otherwise classify the top-level lifecycle scalar semantically, distinguish absence from a present value, recognize the exact stage-owned value regardless of valid YAML quoting, and return a bounded authority error for every present unknown, malformed, duplicate, or unreadable value. Historical absence must retain the status form. Add direct `unknown_value` and quoted exact-value regressions.
Safe resolution path: Replace the regex truthiness comparison with a bounded repository-owned YAML scalar seam or an equivalent exact parser that produces three states: absent historical, exact stage-owned, or invalid authority. Keep path containment and symlink checks, use the invalid state for unknown/malformed/duplicate values, revise the existing T24 fixture from invented `legacy` to absent historical authority, and rerun the targeted T24 test plus the 64-test boundary suite and path-aware feature/test-spec validation. Do not edit the approved spec, selector, CLI/package fixtures, release metadata, architecture, ADR, or plan.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior finding reconciliation

- `UBR-PRFG-CR2-001`: resolved. Exact unquoted stage-owned authority is now evaluated before marker-branch acceptance; the owner form passes, the status form fails, absent historical authority retains status, and the direct before-pointer case fails.
- `UBR-PRFG-CR1-001`: resolved through the approved UBR-R021 contract plus the R3 reciprocal probe and focused T24 test.
- `UBR-PRFG-CR1-002`: remains resolved. The targeted malformed-profile test passes all three fail-closed paths without selecting release validation.
- `UBR-PRFG-CR1-003`: remains resolved. Five bounded historical/current skills-only cases pass with v0.3.3 identities where compatibility is claimed and v0.4.0 for the unmarked current negative.
- `UBR-PRFG-CR3-001`: new finding. It concerns closed lifecycle vocabulary and YAML semantic identity, not the canonical reciprocal bypass fixed from R2.

## Confirmed corrections

- The canonical R2 bypass is closed: stage-owned owner placement succeeds, stage-owned status placement fails, absent historical status placement succeeds, and before/outside/duplicate placements fail with bounded codes.
- Profile selection remains exclusive for `docs/releases/profiles/`; the targeted canonical/three-malformed regression passes.
- Current and historical CLI fixture identity remains separated; the five skills-only/older-opencode tests pass without command-alias overclaim or unexpected mutation.
- The correction remains within the approved validator, test, selector, package-fixture, and evidence boundaries; no architecture or release-flow change is present.

## Validation evidence challenged

- Reciprocal and vocabulary probe: canonical stage owner `[]`; canonical stage status `BFR-MARKER-PLACEMENT`; absent historical status `[]`; unknown status `[]`; unknown owner `BFR-MARKER-AUTHORITY`; quoted exact stage owner `BFR-MARKER-AUTHORITY`; quoted exact stage status `[]`; before/outside/duplicate return their bounded placement/count codes. The unknown and quoted results reproduce `UBR-PRFG-CR3-001`.
- `python scripts/test-boundary-first-validation.py BoundaryFirstStructuralTests.test_stage_owned_marker_requires_matching_lifecycle_contract` — pass, 1 targeted test.
- `python scripts/test-boundary-first-validation.py` — pass, 64 tests.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_malformed_release_profile_paths_require_release_version` — pass, 1 targeted test.
- `node --test --test-name-pattern='skills-only|older opencode' packages/rigorloop/test/cli.test.js` — pass, 5 tests.
- `python scripts/validate-boundary-first.py --check --path specs/usability-first-boundary-release.md --path specs/usability-first-boundary-release.test.md` — pass with active v0.4.0 and rollback v0.3.6.
- Quoted and unknown temporary change-record probes both pass the current metadata command; this confirms no sibling metadata gate compensates for the authority misclassification. The pre-existing general schema-enum enforcement omission is not broadened into this scoped finding.
- `git diff --check f0b1b6fc..e193e1f7` — pass.
- Broad smoke, complete selector/CLI suites, hosted CI, PR mutation, tagging, publication, and merge were not run and are not claimed.

## Checklist coverage

- Spec alignment: blocked by `UBR-PRFG-CR3-001`; canonical UBR-R021 placement is correct, but lifecycle identity is textual rather than semantic and unknown values fail open.
- Test coverage: blocked for unknown-value and quoted exact-scalar authority; canonical reciprocal, before-pointer, outside, duplicate, malformed-profile, and historical package cases have direct proof.
- Edge cases: blocked for closed vocabulary and YAML-equivalent presentation; named T24 placement cases pass.
- Error handling: blocked because present unknown authority becomes legacy status success; missing files, owner mismatch, and placement failures remain bounded.
- Architecture boundaries: pass. The change stays in the approved boundary-validator seam and adds no dependency or ownership change.
- Compatibility: blocked because valid quoted stage authority is treated as legacy; historical absence, v0.3.3 skills-only compatibility, and v0.4.0 current behavior remain intact.
- Security/privacy: pass. Repository containment and symlink checks remain present; diagnostics are repository-relative.
- Derived artifact currency: pass for the inspected current/historical identities; no generated output was edited by the latest correction.
- Unrelated changes: pass. The implementation correction is scoped to the R2 authority path, tests, state registration, and evidence.
- Validation evidence: blocked. All selected tests pass, but the independent vocabulary/YAML probes reproduce a material authority divergence absent from the suite.

## Handoff

Stop at review-resolution. Resolve `UBR-PRFG-CR3-001` within the boundary authority parser and T24 tests, preserve the resolved marker, profile, and historical-package behavior, then request a fresh formal cumulative rereview. Code-review records evidence only; workflow must consume this result and update change-local unresolved-count, artifact registration, latest review, and routing state.
