# PR Full-Gate Correction Code Review R2

Review ID: code-review-pr-full-gate-r2
Stage: code-review
Round: 2
Reviewer: Codex independent contract-first code-review peer
Target: f0b1b6fc..5f1448a4
Reviewed artifact: commit 5f1448a4a610371aff2364da496086c11d9a075e
Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-pr-full-gate-correction-r2
Reviewer context ID: pr-full-gate-r2-fresh-contract-first-reviewer
Context separation mechanism: separate-agent-contract-first-rereview
Author context excluded: true
Risk tier: high
Risk-tier triggers: spec-derived-validator-authority; release-selector-fail-closed-routing; historical-package-compatibility; post-verify-pr-correction
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: CONSTITUTION.md; specs/boundary-first-proof-model.md; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; spec-review-r5; test-spec-review-r4; specs/target-native-init.md; specs/target-native-init.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@5f1448a4#sha256:5727760223fbeb9a50a8eb7c440820ca3eeaf09a0940f7bae095c7b13309d900; specs/boundary-first-proof-model.md@5f1448a4#sha256:f4a4ce4860981af14484c4d4f15edc362cf269806d2fe7f052db5bfff11ed159; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md@5f1448a4#sha256:46865935c04fa404a38b34c96f7c19f5934a6b9eee672081f22b3cfc2ff64ba4; specs/usability-first-boundary-release.md@5f1448a4#sha256:5045edf83c5e71531445f524b88c4098f28fc115bf6ba8277335c178058bf6cd; specs/usability-first-boundary-release.test.md@5f1448a4#sha256:4669a662b16d87e236ecb0387135431e7ae706f05b6532a4d51529b60745b833; specs/target-native-init.md@5f1448a4#sha256:0b27d8c6df0eac7edd8ede0c480bc2822e989bc0f6c6e4e0c82f59446e3f86e0; specs/target-native-init.test.md@5f1448a4#sha256:32a6b10f3c1a19fcfb128fa948cbb2fcf2fcac5fc50a4c08021aa36d9e0c4c0a; docs/architecture/system/architecture.md@5f1448a4#sha256:e093f7e58b50a8851765c1a5c8edba701f43f0cc9b1e466a8e2d334a6c7e7dfc; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@5f1448a4#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@5f1448a4#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@5f1448a4#sha256:1e45eed4efc00f94410c9a5da5dba397971047a3ac63df4cfeae3ada45bdd319; docs/changes/2026-08-06-usability-first-boundary-release/reviews/spec-review-r5.md@5f1448a4#sha256:904d296ab93fea31184ff27623bad2b1d6ad134096059c96d9f342a5cff51bb5; docs/changes/2026-08-06-usability-first-boundary-release/reviews/test-spec-review-r4.md@5f1448a4#sha256:c1cca214201fab7be241ab40f11d8992b81b9be6e797215485e6f97e30493aa4; scripts/boundary_first_validation.py@5f1448a4#sha256:de5311385b95dce7c50c61d61a11a103f2c2617c6a9168d865ca49ea6fa7c9fd; scripts/test-boundary-first-validation.py@5f1448a4#sha256:af638e59807137f26f412b710a754b212e9a45a8ddf42a3e57c23cf037f5a330; scripts/validation_selection.py@5f1448a4#sha256:6ac7831ec8f4baa51f717bb78d1860591cd7720ccd58d60ce529b5ab0520396a; scripts/test-select-validation.py@5f1448a4#sha256:89e45952a75b8269553b82b11a427034d887a6d9d194d91f1f306fd6161274ad; packages/rigorloop/test/cli.test.js@5f1448a4#sha256:4717358d9f590d6b807bc6f71d3b5e8a611004c0d42017f6b253d27528bc1bd5; range:f0b1b6fc..5f1448a4.diff@5f1448a4#sha256:d2d67f9c344f948a52dffa9538fcbf957a3a099789ddaeff6ed6c5659edc69a0
Prompt template version: code-review-v1
Initial packet hash: sha256:d2d67f9c344f948a52dffa9538fcbf957a3a099789ddaeff6ed6c5659edc69a0
Manifest owner: workflow-orchestrator
Forbidden initial context excluded: true
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: lifecycle-selected boundary marker placement; release-profile routing; current package identity; historical opencode compatibility proof
Highest-impact failure modes: a stage-owned artifact passes through the legacy marker form; malformed profiles receive fabricated versions; current metadata replaces historical compatibility proof; green tests omit a named authority partition
Changed boundaries: cross-file lifecycle authority; exact marker placement; profile path-to-version extraction; current-versus-historical package fixture identity
Evidence expected: governing clauses; cumulative diff; reciprocal marker probes; canonical and malformed profile tests; historical metadata; focused regressions; resolution reconciliation
Areas requiring direct inspection: both marker branches and root threading; path-aware T24 tests; profile namespace branch; fixture helpers and skills-only cases; current review evidence
Areas intentionally out of scope: broad smoke; hosted CI; PR opening; push; tag; publication; merge; public closeout
Risk classes considered: requirement-fidelity; spec-derived-validation; fail-closed-release-routing; package-supply-chain; compatibility-and-migration; lifecycle-closeout; live-publication=not-applicable:forbidden; external-mutation=not-applicable:forbidden
Falsifiable review questions: Does lifecycle authority select placement in both directions? Do malformed profiles block? Are current and historical package fixtures independently truthful?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-full-gate-r2.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/test-boundary-first-validation.py; scripts/validation_selection.py; scripts/test-select-validation.py; packages/rigorloop/test/cli.test.js; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*; specs/; docs/changes/**/reviews/; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: spec-derived validators; artifact lifecycle validators; workflow routing contracts; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > stage-owned override scope > approved spec-review and test-spec-review > cumulative diff > direct probes > regressions > author evidence > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: UBR-PRFG-CR2-001
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed; M1-M4 remain closed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: UBR-PRFG-CR1-001, UBR-PRFG-CR2-001
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-PRFG-CR2-001
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-full-gate-r2.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-pr-full-gate-r2`
- Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: UBR-PRFG-CR2-001
- Verify readiness: not-claimed

## Finding UBR-PRFG-CR2-001

Finding ID: UBR-PRFG-CR2-001
Severity: major
Location: `scripts/boundary_first_validation.py:380`; `scripts/test-boundary-first-validation.py:248`; `specs/usability-first-boundary-release.md:127`; `specs/usability-first-boundary-release.test.md:466`
Evidence: UBR-R021 makes the referenced `lifecycle_contract` select the valid marker form: stage-owned feature specs must use the owner-pointer form, while only non-stage-owned specs retain `## Status`. `_marker_issues` resolves lifecycle authority only after it has already selected the owner-marker branch. Its status-marker branch never resolves a normalized owning change pointer. A direct paired-fixture probe therefore reports no issues for both the authorized owner form and an unauthorized status form pointing to the same `stage-owned-change-local-v1` record. The 64-test suite remains green because T24 covers owner-form matching, missing, and different authority plus generic outside/duplicate checks, but it does not exercise a stage-owned record with the legacy status marker or its named before-pointer mutation.
Required outcome: Make referenced lifecycle authority select the permitted placement before accepting either branch. A stage-owned record plus a status marker must fail, a genuinely non-stage-owned status form must continue to pass, and T24 must directly cover the reciprocal authority case and every named before-pointer, outside-section, and duplicate mutation.
Safe resolution path: Extract the normalized owner pointer independently of marker placement, resolve its repository-contained lifecycle contract once, apply the stage-owned owner-form rule or retained non-stage-owned status-form rule, add table-driven paired fixtures for both positive forms and all named negatives, then rerun the boundary suite and path-aware feature/test-spec validation. Do not change the approved spec, release selector, CLI implementation, release metadata, or package output.
needs-decision rationale: none
auto_fix_class: declared-safe

## R1 reconciliation

- `UBR-PRFG-CR1-001`: failed remediation; the owner-form branch now authenticates its change record, but the reciprocal stage-owned status form still passes. It remains open through `UBR-PRFG-CR2-001`.
- `UBR-PRFG-CR1-002`: resolved. The profile namespace is exclusive, accepts exact stable semantic-version YAML names, and the canonical plus three malformed cases prove `release-version-required` fail-closed behavior.
- `UBR-PRFG-CR1-003`: resolved. The current package defaults remain v0.4.0, while the positive, human-warning, unexpected-root, and dry-run skills-only cases use the actual historical v0.3.3 package/tag/metadata identity and explicit compatibility marker.

## Confirmed corrections

- `scripts/validation_selection.py:2642` through `scripts/validation_selection.py:2653` prevents malformed profile paths from reaching the general release-directory fallback. The 150-test selector suite and targeted malformed-path test pass.
- `packages/rigorloop/test/cli.test.js:31` through `packages/rigorloop/test/cli.test.js:37` keeps current and historical identities distinct; the four historical cases bind v0.3.3 consistently through archive, package, release index, and bundled metadata. All 117 CLI tests and six npm publication tests pass.
- Owner-form authority now rejects missing and different lifecycle records and threads repository root authority through feature/proof validation. Before-pointer, outside-section, and duplicate direct probes fail with bounded marker issues. This is partial progress only because authority does not govern the status branch.
- The cumulative correction remains scoped to its approved specs, test spec, validator, selector, package fixtures, and review evidence. Architecture, ADR, plan intent, release behavior, generated packages, and public interfaces are unchanged.

## Validation evidence challenged

- Reciprocal paired-fixture probe: `stage_owner []`, `stage_status []`, `legacy_status []`, `before_owner [BFR-MARKER-PLACEMENT]`, `outside_owner [BFR-MARKER-PLACEMENT]`, `duplicate [BFR-MARKER-COUNT]`; the second result reproduces `UBR-PRFG-CR2-001`.
- `python scripts/test-boundary-first-validation.py` — pass, 64 tests.
- `python scripts/test-select-validation.py` — pass, 150 tests in 59.88 seconds.
- `npm test --prefix packages/rigorloop` — pass, 117 tests.
- `python scripts/test-npm-package-publication.py` — pass, 6 tests.
- `python scripts/validate-boundary-first.py --check --path specs/usability-first-boundary-release.md --path specs/usability-first-boundary-release.test.md` — pass with active v0.4.0 and rollback v0.3.6 identities.
- `git diff --check f0b1b6fc..5f1448a4` — pass.
- Broad smoke, hosted CI, release publication, tagging, pushing, and PR mutation were not run and are not claimed.

## Checklist coverage

- Spec alignment: blocked. The reciprocal status branch violates UBR-R021 even though owner-form authority is now authenticated.
- Test coverage: blocked. The approved T24 matrix lacks the stage-owned-status negative and direct before-pointer regression; the release and historical package correction tests are adequate.
- Edge cases: blocked only for lifecycle-selected placement. Malformed profile names and historical skills-only identity are directly covered.
- Error handling: pass for missing/different owner authority, malformed profiles, package warnings, and mutation boundaries; the unauthorized status form incorrectly produces no error.
- Architecture boundaries: pass. The correction reuses the approved validator, selector, and fixture seams without new ownership or dependencies.
- Compatibility: blocked by accepting the wrong legacy form for a stage-owned artifact. Genuine legacy status form and v0.3.3 skills-only behavior remain accepted.
- Security/privacy: pass. Authority paths are repository-contained and symlink-aware; diagnostics disclose only repository-relative identities.
- Derived artifact currency: pass for inspected current/historical metadata identities; no derived output was edited or claimed by this review.
- Unrelated changes: pass. The cumulative range stays within the approved correction and its governing/evidence artifacts.
- Validation evidence: blocked. Green suites do not exercise the reproduced reciprocal lifecycle-authority failure.

## Handoff

Stop at review-resolution. Correct `UBR-PRFG-CR2-001` in the existing boundary validator and T24 regression seam, preserve the resolved selector and package-fixture corrections, then request a fresh formal PR full-gate rereview. Code-review records evidence only; workflow must consume this result and update change-local milestone, unresolved-count, artifact-registration, and routing state.
