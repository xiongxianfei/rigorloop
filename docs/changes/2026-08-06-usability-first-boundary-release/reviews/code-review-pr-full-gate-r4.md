# PR Full-Gate Correction Code Review R4

Review ID: code-review-pr-full-gate-r4
Stage: code-review
Round: 4
Reviewer: Codex independent contract-first code-review peer
Target: f0b1b6fc..ed41f631
Reviewed artifact: commit ed41f6319b8ab074193cb01eef07cf0c86f8dc88
Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-pr-full-gate-correction-r4
Reviewer context ID: pr-full-gate-r4-fresh-contract-first-reviewer
Context separation mechanism: separate-agent-contract-first-rereview
Author context excluded: true
Risk tier: high
Risk-tier triggers: spec-derived-validator-authority; closed-vocabulary-fail-closed; yaml-semantic-authority; release-selector-regression-safety; historical-package-compatibility; post-verify-pr-correction
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: CONSTITUTION.md; schemas/change.schema.json; specs/boundary-first-proof-model.md; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; spec-review-r5; test-spec-review-r4; specs/target-native-init.md; specs/target-native-init.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@ed41f631#sha256:5727760223fbeb9a50a8eb7c440820ca3eeaf09a0940f7bae095c7b13309d900; schemas/change.schema.json@ed41f631#sha256:fa3d07dd253a4816f9e143f6b9243767da248613f91c57ddb8508b35c0f67db6; specs/boundary-first-proof-model.md@ed41f631#sha256:f4a4ce4860981af14484c4d4f15edc362cf269806d2fe7f052db5bfff11ed159; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md@ed41f631#sha256:46865935c04fa404a38b34c96f7c19f5934a6b9eee672081f22b3cfc2ff64ba4; specs/usability-first-boundary-release.md@ed41f631#sha256:5045edf83c5e71531445f524b88c4098f28fc115bf6ba8277335c178058bf6cd; specs/usability-first-boundary-release.test.md@ed41f631#sha256:4669a662b16d87e236ecb0387135431e7ae706f05b6532a4d51529b60745b833; specs/target-native-init.md@ed41f631#sha256:0b27d8c6df0eac7edd8ede0c480bc2822e989bc0f6c6e4e0c82f59446e3f86e0; specs/target-native-init.test.md@ed41f631#sha256:32a6b10f3c1a19fcfb128fa948cbb2fcf2fcac5fc50a4c08021aa36d9e0c4c0a; docs/architecture/system/architecture.md@ed41f631#sha256:e093f7e58b50a8851765c1a5c8edba701f43f0cc9b1e466a8e2d334a6c7e7dfc; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@ed41f631#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@ed41f631#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@ed41f631#sha256:5d68a048fc7eee7640cf77beedb67e5d5e9f2ea6fe9e143123f8c803af61001e; docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r5.md@ed41f631#sha256:904d296ab93fea31184ff27623bad2b1d6ad134096059c96d9f342a5cff51bb5; docs/changes/2026-08-06-usability-first-boundary-release/reviews/test-spec-review-r4.md@ed41f631#sha256:c1cca214201fab7be241ab40f11d8992b81b9be6e797215485e6f97e30493aa4; docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-full-gate-r3.md@ed41f631#sha256:6aa730d8b1e98f01beb628eae4c914850a087dfc5739b801c64dff2411469623; docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-full-gate-r3.yaml@ed41f631#sha256:f50c3533792c3cc61f1d2a502093f5caab4687984110a8261e6963729f138e4c; docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md@ed41f631#sha256:cf46d153ffbf3558de78d724cc8c73a2b6316c4b5b51ab6ed46fb6e0168a384f; docs/changes/2026-08-06-usability-first-boundary-release/evidence/pr-full-gate-review-resolution.md@ed41f631#sha256:9ef6d650d81ce7b039292f26feb4fbcb30ec26b488c08c2e22cecdd61d7dff72; scripts/boundary_first_validation.py@ed41f631#sha256:852a5a8fc643074f41d28afd64ddf6b537464639b3ce63cc8ea40ae772e57b48; scripts/test-boundary-first-validation.py@ed41f631#sha256:89e08de25fc6117d1a7143f0c4d870cd8f4d294fe0fc203fbfe11a6ac4a05237; scripts/validation_selection.py@ed41f631#sha256:6ac7831ec8f4baa51f717bb78d1860591cd7720ccd58d60ce529b5ab0520396a; scripts/test-select-validation.py@ed41f631#sha256:89e45952a75b8269553b82b11a427034d887a6d9d194d91f1f306fd6161274ad; packages/rigorloop/test/cli.test.js@ed41f631#sha256:4717358d9f590d6b807bc6f71d3b5e8a611004c0d42017f6b253d27528bc1bd5; range:f0b1b6fc..ed41f631.diff@ed41f631#sha256:9edb6f6ed7ee2823169e125098f4baddea6b645cb17458aea5669f09b34709b5
Prompt template version: code-review-v1
Initial packet hash: sha256:9edb6f6ed7ee2823169e125098f4baddea6b645cb17458aea5669f09b34709b5
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: lifecycle-selected boundary marker placement; lifecycle authority parsing; release-profile routing; current package identity; historical opencode compatibility proof
Highest-impact failure modes: YAML-equivalent authority ignored as absent; duplicate lifecycle key evading detection; stage-owned status bypass; malformed profile version fabrication; current metadata replacing historical proof
Changed boundaries: cross-file lifecycle authority; exact marker placement; YAML scalar and key identity; profile path-to-version extraction; current-versus-historical fixture identity
Evidence expected: governing clauses and schema; cumulative diff; reciprocal, vocabulary, malformed, duplicate, and semantic-key probes; focused T24; profile negative; historical package tests; prior-finding reconciliation
Areas requiring direct inspection: authority parser and both marker branches; repository YAML tokenizer/parser; T24 fixtures; lifecycle schema; profile namespace branch; fixture identity helpers; review evidence
Areas intentionally out of scope: broad smoke; hosted CI; PR opening; push; tag; publication; merge; public closeout
Risk classes considered: requirement-fidelity; spec-derived-validation; closed-vocabulary-validation; fail-closed-release-routing; package-supply-chain; compatibility-and-migration; lifecycle-closeout; live-publication=not-applicable:forbidden; external-mutation=not-applicable:forbidden
Falsifiable review questions: Do exact quoted/unquoted authorities select owner placement? Does absence alone retain status? Do unknown/malformed/duplicate authorities fail before placement? Does repository-accepted key spacing preserve authority? Do profile and historical fixture corrections remain safe?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-full-gate-r4.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/test-boundary-first-validation.py; scripts/validation_selection.py; scripts/test-select-validation.py; packages/rigorloop/test/cli.test.js; schemas/change.schema.json; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*; specs/; docs/changes/**/reviews/; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: spec-derived validators; artifact lifecycle validators; workflow routing contracts; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > lifecycle schema and repository YAML semantics > approved test proof > cumulative diff > direct probes > focused regressions > author evidence > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: UBR-PRFG-CR4-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed; M1-M4 remain closed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: UBR-PRFG-CR3-001, UBR-PRFG-CR4-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-PRFG-CR4-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-full-gate-r4.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-pr-full-gate-r4`
- Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: UBR-PRFG-CR4-001
- Verify readiness: not-claimed

## Finding UBR-PRFG-CR4-001

Finding ID: UBR-PRFG-CR4-001
Severity: major
Location: `scripts/boundary_first_validation.py:363`; `scripts/validate-change-metadata.py:270`; `scripts/validate-change-metadata.py:299`; `scripts/test-boundary-first-validation.py:270`
Evidence: `_stage_owned_marker_authority` recognizes lifecycle entries only with `^lifecycle_contract:`, while the repository change-metadata parser splits at `:` and strips the mapping key. Consequently, `lifecycle_contract : stage-owned-change-local-v1` is the same top-level semantic key/value to the repository parser but is absent to the boundary authority parser: direct probes reject owner placement and accept status placement. `lifecycle_contract : future-contract-v2` likewise accepts status placement instead of returning `BFR-UNKNOWN-LIFECYCLE-CONTRACT`. A mixed-spelling duplicate containing one canonical and one spaced key accepts owner placement rather than returning the duplicate authority error. The correction therefore remains presentation-sensitive and does not reject every present unknown or duplicate authority before marker consistency.
Required outcome: Classify top-level lifecycle entries with the repository's mapping-key semantics while preserving occurrence count before mapping overwrite; recognize the exact stage-owned scalar across supported quoting and key spacing, retain historical behavior only when the semantic key is absent, and return a bounded authority error for every semantic duplicate, unknown, or malformed entry before marker placement.
Safe resolution path: Replace the exact-key regex seam with a bounded tokenizer/parser seam that observes top-level mapping entries, normalizes the key like `split_mapping_entry`, preserves all lifecycle occurrences, and parses each scalar with the repository-owned scalar rules or an equivalent shared helper. Add direct regressions for `lifecycle_contract :` exact, unknown, malformed, and mixed-spelling duplicate forms. Preserve the resolved profile selector and current/historical package fixtures; do not edit the approved spec, architecture, ADR, plan, release metadata, or workflow state.
needs-decision rationale: none
auto_fix_class: declared-safe

## Prior finding reconciliation

- `UBR-PRFG-CR3-001`: partially corrected but remains open. Exact unquoted, double-quoted, and single-quoted stage-owned values select owner placement; canonical unknown and malformed values return `BFR-UNKNOWN-LIFECYCLE-CONTRACT`; canonical duplicates return `BFR-MARKER-AUTHORITY`; absent authority retains status. Repository-accepted key spacing still inverts or bypasses those classifications, recorded as `UBR-PRFG-CR4-001`.
- `UBR-PRFG-CR2-001`: remains resolved for canonical and quoted exact authority. Owner placement passes, status placement fails, and before/outside/duplicate marker placement returns bounded placement/count codes.
- `UBR-PRFG-CR1-001`: remains resolved through the approved UBR-R021 contract and canonical reciprocal proof.
- `UBR-PRFG-CR1-002`: remains resolved. Canonical profile selection passes and all three malformed profile names block without selecting release validation.
- `UBR-PRFG-CR1-003`: remains resolved. Five focused skills-only/older-opencode cases retain v0.3.3 identity for historical claims and v0.4.0 for the current unmarked negative.

## Confirmed corrections

- Exact unquoted, double-quoted, and single-quoted stage-owned values select owner placement; status placement is rejected.
- Absent lifecycle authority retains the historical status form and rejects owner placement.
- Canonically spelled unknown and malformed authority returns `BFR-UNKNOWN-LIFECYCLE-CONTRACT` before placement; canonically spelled duplicates return `BFR-MARKER-AUTHORITY`.
- Before-pointer, outside-section, and duplicate marker placement return bounded placement/count codes.
- The profile namespace remains exclusive, and malformed profile filenames do not fabricate a release version.
- Current v0.4.0 and historical v0.3.3 fixture identities remain separated with no command-alias overclaim or unexpected mutation.

## Validation evidence challenged

- Direct canonical matrix: exact unquoted owner passes/status returns `BFR-MARKER-PLACEMENT`; exact double- and single-quoted owner forms pass; absent owner returns `BFR-MARKER-AUTHORITY` while absent status passes; canonical unknown and malformed forms return `BFR-UNKNOWN-LIFECYCLE-CONTRACT`; canonical duplicates return `BFR-MARKER-AUTHORITY`; before/outside/duplicate markers return bounded placement/count codes.
- Semantic-key probe: the repository parser reads `lifecycle_contract : stage-owned-change-local-v1` as the exact lifecycle key/value, but boundary validation rejects owner and accepts status. A spaced unknown value accepts status, and a mixed-spelling duplicate accepts owner. These results reproduce `UBR-PRFG-CR4-001`.
- `python scripts/test-boundary-first-validation.py BoundaryFirstStructuralTests.test_stage_owned_marker_requires_matching_lifecycle_contract BoundaryFirstStructuralTests.test_unknown_value_lifecycle_contract_fails_before_marker_consistency` — pass, 2 targeted tests.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_release_profile_path_uses_profile_filename_as_version ValidationSelectionTests.test_malformed_release_profile_paths_require_release_version` — pass, 2 targeted tests.
- `node --test --test-name-pattern='skills-only|older opencode' packages/rigorloop/test/cli.test.js` — pass, 5 tests.
- `python scripts/validate-boundary-first.py --check --path specs/usability-first-boundary-release.md --path specs/usability-first-boundary-release.test.md` — pass with active v0.4.0 and rollback v0.3.6.
- `git diff --check f0b1b6fc..ed41f631` — pass.
- Broad smoke, complete boundary/selector/CLI suites, hosted CI, PR mutation, tagging, publication, and merge were not run and are not claimed.

## Checklist coverage

- Spec alignment: blocked by `UBR-PRFG-CR4-001`; canonical UBR-R021 cases align, but lifecycle authority is not semantic across repository-accepted key serialization.
- Test coverage: blocked for semantic-key exact/unknown/malformed/duplicate cases; canonical reciprocal, value-quoting, unknown, profile, and historical package cases have direct proof.
- Edge cases: blocked for mixed-spelling duplicate and spaced-key authority; named marker placement and canonical malformed/duplicate cases pass.
- Error handling: blocked because a present spaced-key unknown authority becomes historical status success; canonical missing, malformed, unknown, duplicate, and placement failures remain bounded.
- Architecture boundaries: pass. The correction stays in the approved validator/test/selector/package seams and adds no dependency or ownership change.
- Compatibility: blocked only for repository-accepted key presentation; historical absence, quoted exact values, malformed profiles, and v0.3.3 skills-only compatibility remain correct.
- Security/privacy: pass. Repository containment and symlink checks remain present, and diagnostics are repository-relative.
- Derived artifact currency: pass for inspected current/historical fixture identities; no generated output changed in the CR3 correction.
- Unrelated changes: pass. The cumulative correction remains within the approved validator, tests, selector, package fixtures, state registration, and evidence surfaces.
- Validation evidence: blocked. Selected tests pass, but the semantic-key probes reproduce a material authority bypass absent from the suite.

## Handoff

Stop at review-resolution. Resolve `UBR-PRFG-CR4-001` together with the still-open semantic portion of `UBR-PRFG-CR3-001`, preserve the canonical marker, profile, and historical-package behavior, then request a fresh formal cumulative rereview. Code-review records evidence only; workflow must consume this result and update change-local unresolved count, artifact registration, latest review, and routing state.
