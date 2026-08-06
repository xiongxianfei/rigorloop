# PR Full-Gate Correction Code Review R1

Review ID: code-review-pr-full-gate-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: a78f1908c7656aeb5e1b6d8931fff38ba745b0a0..841ebc9ca8ecc526f1b67fb847629bba0ee5c1a3
Reviewed artifact: commit 841ebc9ca8ecc526f1b67fb847629bba0ee5c1a3
Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: root-pr-full-gate-correction
Reviewer context ID: pr-full-gate-r1-fresh-independent-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: high
Risk-tier triggers: spec-derived-validator-authority; release-selector-fail-closed-routing; historical-package-compatibility; canonical-architecture-ownership; post-verify-pr-correction
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: CONSTITUTION.md; specs/boundary-first-proof-model.md; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md; specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; specs/target-native-init.md; specs/target-native-init.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@841ebc9c#sha256:5727760223fbeb9a50a8eb7c440820ca3eeaf09a0940f7bae095c7b13309d900; specs/boundary-first-proof-model.md@841ebc9c#sha256:f4a4ce4860981af14484c4d4f15edc362cf269806d2fe7f052db5bfff11ed159; specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md@841ebc9c#sha256:46865935c04fa404a38b34c96f7c19f5934a6b9eee672081f22b3cfc2ff64ba4; specs/usability-first-boundary-release.md@841ebc9c#sha256:1518d7d18f409def99ef4dd4c688754fde8a030c609c5a9fb549a0183ef587d7; specs/usability-first-boundary-release.test.md@841ebc9c#sha256:993839ee82239baa63d41d929dec61ea26db4bed3239e3baf52e3e45755f432f; specs/target-native-init.md@841ebc9c#sha256:0b27d8c6df0eac7edd8ede0c480bc2822e989bc0f6c6e4e0c82f59446e3f86e0; specs/target-native-init.test.md@841ebc9c#sha256:32a6b10f3c1a19fcfb128fa948cbb2fcf2fcac5fc50a4c08021aa36d9e0c4c0a; docs/architecture/system/architecture.md@841ebc9c#sha256:e093f7e58b50a8851765c1a5c8edba701f43f0cc9b1e466a8e2d334a6c7e7dfc; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@841ebc9c#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@841ebc9c#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@841ebc9c#sha256:c040695afa79e39d51ea279ab19a14fed51193ea1616c3be82d1473f4c0e0622; docs/changes/2026-08-06-usability-first-boundary-release/evidence/pr-readiness-full-gate-fixes.md@841ebc9c#sha256:c8586e2fec9b736007b127c833fc4ea470d9d00f55c89fb45a6d334404a86e8f; scripts/boundary_first_validation.py@841ebc9c#sha256:5f4a364e572f0c90ba5d9bb2c90830697a3a0d4c78df143fa76f6505e97eb6e4; scripts/validation_selection.py@841ebc9c#sha256:0b50b42ffa7484e7a1a6f5b9ecbe2787cfbeb429fde1d191669f768a5af264b4; packages/rigorloop/test/cli.test.js@841ebc9c#sha256:425dcb76f052883cd902f03a23c8bc8863c3a54f918456f4bac1050b9b0db9a1; range:a78f1908c7656aeb5e1b6d8931fff38ba745b0a0..841ebc9ca8ecc526f1b67fb847629bba0ee5c1a3.diff@841ebc9c#sha256:956d01b8c4638967996e43f1f45e588a5561a5841f24a9fe5d2ab6091cbccfe5
Prompt template version: code-review-v1
Initial packet hash: sha256:956d01b8c4638967996e43f1f45e588a5561a5841f24a9fe5d2ab6091cbccfe5
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: boundary-record adoption and placement; release-version selection; architecture ownership; v0.4.0 CLI fixtures; older opencode compatibility proof; final lifecycle routing
Highest-impact failure modes: a green validator diverges from its standing spec; malformed release profiles receive unrelated validation; current v0.4.0 is falsely modeled as skills-only compatible; duplicate artifact ownership; green but semantically weakened proof
Changed boundaries: spec-derived marker placement; exact bootstrap exemption; feature/proof normalization; release profile path parsing; architecture registry ownership; current and historical package fixtures
Evidence expected: exact correction diff; standing and current requirements; canonical and malformed profile probes; package metadata across v0.3.0-v0.4.0; direct architecture ownership query; focused and complete regressions; lifecycle validation
Areas requiring direct inspection: marker and bootstrap call path; normalized examples and proof maps; profile special-case and fallback; architecture owner records; CLI fixture helpers and all skills-only cases; change-local evidence and routing
Areas intentionally out of scope: broad smoke rerun; hosted CI; PR opening; push; tag; publication; merge; public closeout
Risk classes considered: requirement-fidelity=applicable; spec-derived-validation=applicable; release-routing=applicable; compatibility=applicable; package-supply-chain=applicable; architecture-ownership=applicable; lifecycle-closeout=applicable; live-publication=not-applicable:forbidden; external-mutation=not-applicable:forbidden
Falsifiable review questions: Does the stage-owned marker form have normative authority and retain the legacy form? Do malformed profile names block? Does the v0.4.0 refresh retain a genuinely historical skills-only fixture?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-full-gate-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/boundary_first_validation.py; scripts/test-boundary-first-validation.py; scripts/validation_selection.py; scripts/test-select-validation.py; packages/rigorloop/test/cli.test.js; four normalized release specs; canonical architecture ownership and change-local state
Requirement-fidelity matched path triggers: scripts/*validator*; scripts/validate-*; specs/; docs/changes/**/reviews/; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: spec-derived validators; artifact lifecycle validators; workflow routing contracts; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > stage-owned override scope > current feature/test spec > architecture/ADR/plan > correction diff > regressions > direct probes > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: UBR-PRFG-CR1-001; UBR-PRFG-CR1-002; UBR-PRFG-CR1-003
Material findings: UBR-PRFG-CR1-001, UBR-PRFG-CR1-002, UBR-PRFG-CR1-003
Immediate next stage: review-resolution
Automatic downstream handoff: review-resolution
Milestone closeout: resolution-needed; M1-M4 remain closed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and change-local routing state
- Open blockers: UBR-PRFG-CR1-001, UBR-PRFG-CR1-002, UBR-PRFG-CR1-003
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-PRFG-CR1-001, UBR-PRFG-CR1-002, UBR-PRFG-CR1-003
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-full-gate-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-pr-full-gate-r1`
- Reviewed milestone: post-verify PR full-gate correction; M1-M4 remain closed
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: UBR-PRFG-CR1-001, UBR-PRFG-CR1-002, UBR-PRFG-CR1-003
- Verify readiness: not-claimed

## Finding UBR-PRFG-CR1-001

Finding ID: UBR-PRFG-CR1-001
Severity: major
Location: `scripts/boundary_first_validation.py:305`; `specs/boundary-first-proof-model.md:140`; `specs/usability-first-boundary-release.md:176`
Evidence: `_marker_issues` now accepts the marker after a normalized owning-change pointer, and the two changed feature specs rely on that form. The standing authoritative PBF-R002 still requires the marker in `## Status` after a lifecycle value. The current compatibility table replaces only named activation subjects and leaves PBF-R002 authoritative. Stage-owned SLA-R013/R014 explains why mutable lifecycle status belongs in `change.yaml`, but it neither amends the boundary contract nor makes the new marker location part of its closed replacement table. The focused positive regression therefore proves implementation behavior that no approved feature contract currently authorizes.
Required outcome: Establish one explicit normative rule for stage-owned marker placement and align the validator, legacy compatibility test, adopting specs, and proof-model test spec with it. Preserve exactly-one placement and rejection before the owner pointer or outside governed metadata.
Safe resolution path: Route the placement rule to the owning spec stage, amend the standing proof-model contract and test spec (or an explicitly higher-priority replacement table) to allow the normalized owner-pointer form for governed artifacts while retaining the legacy status form, obtain the required spec review, then rerun structural and changed-path regressions.
needs-decision rationale: none
auto_fix_class: requires-upstream-spec

## Finding UBR-PRFG-CR1-002

Finding ID: UBR-PRFG-CR1-002
Severity: major
Location: `scripts/validation_selection.py:2639`; `scripts/test-select-validation.py:2184`
Evidence: The canonical `docs/releases/profiles/v0.4.0.yaml` case now correctly selects `--version v0.4.0`, but the profile namespace is not isolated from the general release-directory fallback. Direct explicit-mode probes report status `ok` and no blocker while selecting `--version profiles` for `docs/releases/profiles/not-a-version.yaml` and `docs/releases/profiles/v0.4.0.yml`; `docs/releases/profiles/v.yaml` selects `--version v`. The existing release-path negative tests establish `release-version-required` as the fail-closed result when a version cannot be inferred, but the new regression tests only the canonical positive.
Required outcome: Profile-path extraction accepts the exact supported versioned profile shape and otherwise blocks with `release-version-required`; no malformed or near-match profile path may become `profiles`, `v`, or another fabricated release version.
Safe resolution path: Make `docs/releases/profiles/` an exclusive parser branch, validate the filename against the repository's supported release-tag grammar, add canonical and malformed near-match regressions, and rerun the complete selector suite plus direct v0.4.0 release validation.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-PRFG-CR1-003

Finding ID: UBR-PRFG-CR1-003
Severity: major
Location: `packages/rigorloop/test/cli.test.js:2806`; `packages/rigorloop/test/cli.test.js:2844`; `packages/rigorloop/test/cli.test.js:2863`; `packages/rigorloop/test/cli.test.js:2920`; `specs/target-native-init.test.md:225`
Evidence: The package refresh globally changed every skills-only compatibility fixture from v0.3.4 to current v0.4.0. The v0.4.0 opencode metadata declares both skills and commands plus command aliases and has no `skills_only_compatibility`; the actual bundled skills-only range is v0.3.0 through v0.3.3. TTNI-INST-003 explicitly requires an older official opencode skills-only fixture. All 117 tests pass only because the helper fabricates v0.4.0 metadata with a skills-only marker, so the suite no longer proves the historical compatibility contract and instead models an impossible current release.
Required outcome: Keep v0.4.0 as the current package/metadata fixture while independently exercising an actual older official skills-only release identity and its trusted compatibility marker, warnings, root shape, and mutation boundaries.
Safe resolution path: Parameterize the fixture release identity, use a bundled historical skills-only version such as v0.3.3 for TTNI-INST-003 and its related negative/dry-run cases, retain v0.4.0 assertions for current package behavior, and rerun all 117 CLI tests plus npm publication tests.
needs-decision rationale: none
auto_fix_class: declared-safe

## Confirmed corrections

- Canonical boundary validation passes all 64 regressions and the four changed adopting feature/test specs. The bootstrap exemption is exact by path; the public CLI still validates the fixed authoritative activation and proof-model inputs before changed paths, so missing or symlinked bootstrap authority remains fail-closed.
- The normalized boundary scopes, `## Proof map` headings, and narrowed historical example ownership rows satisfy the closed structural rule that every cited requirement is governed by every cited boundary. The historical example prose and test coverage are unchanged; the record no longer overclaims cross-boundary ownership.
- `docs/architecture/system/architecture.md` points to the established July lifecycle change, that change is the sole primary architecture registry owner, and the current release change no longer registers a second architecture artifact.
- The canonical profile path selects v0.4.0 and recorded-source release validation passes; UBR-PRFG-CR1-002 is limited to malformed/near-match fail-closed routing.
- Current v0.4.0 package identity, bundled metadata filename, Codex tree hash, and 63-file count are correct, and all 117 CLI tests pass; UBR-PRFG-CR1-003 concerns the lost historical compatibility proof, not current package identity.

## Validation evidence challenged

- `python scripts/test-boundary-first-validation.py` — pass, 64 tests.
- Changed-spec `python scripts/validate-boundary-first.py --check` — pass for the four adopting release spec/test paths, with active v0.4.0 and exact v0.3.6 rollback output.
- `python scripts/test-select-validation.py` — pass, 149 tests in 61.37 seconds.
- Direct malformed profile probes — reproduce UBR-PRFG-CR1-002 with selector status `ok`, no blocking result, and fabricated versions `profiles` or `v`.
- `python scripts/validate-release.py --recorded-source-auto --version v0.4.0` — pass from recorded source `c7b0babe6e8c91655c2b98f4092197eef5fabc69`.
- Exact correction-range lifecycle validation — pass for 13 artifacts with three pre-existing merge-language warnings.
- `npm test --prefix packages/rigorloop` — pass, 117 tests; metadata inspection independently shows current v0.4.0 commands and historical v0.3.0-v0.3.3 skills-only identities.
- `python scripts/test-npm-package-publication.py` — pass, 6 tests.
- Exact correction-range PR selection — status `ok`; focused boundary, lifecycle, selector, CLI, metadata, documentation, and npm-publication checks selected with no selector blocker.
- Broad smoke was not rerun, as explicitly prohibited. The recorded first PR run's 17 passing checks, including broad smoke, were treated as prior evidence only.

## Checklist coverage

- Spec alignment: blocked by UBR-PRFG-CR1-001; canonical behavior works but the new marker location lacks contract authority.
- Test coverage: blocked by UBR-PRFG-CR1-002 and UBR-PRFG-CR1-003; canonical cases pass while malformed profile and genuine historical compatibility cases are absent.
- Edge cases: blocked for malformed profile filenames and old skills-only release identity; marker before-pointer, outside-section, duplicate, and legacy status cases remain fail-closed.
- Error handling: blocked for malformed profiles because selector status is `ok` rather than `release-version-required`; boundary and lifecycle diagnostics remain bounded.
- Architecture boundaries: pass; the canonical architecture has one primary owner and the release ADR remains registered separately.
- Compatibility: blocked only by the replaced older skills-only package proof and unauthorized marker-form contract change; rollback v0.3.6 and legacy status-form validation remain current.
- Security/privacy: pass; direct diagnostics remain repository-relative and no credentials or external mutation were involved.
- Derived artifact currency: pass for current v0.4.0 package metadata and release archive reconstruction; historical metadata was inspected read-only.
- Unrelated changes: pass; correction content is limited to the four failed gate families and their lifecycle evidence.
- Validation evidence: blocked because green canonical suites do not exercise the three material authority boundaries.

## Handoff

Stop at review-resolution. Route UBR-PRFG-CR1-001 to the owning specification stage before implementation; resolve UBR-PRFG-CR1-002 and UBR-PRFG-CR1-003 without weakening canonical v0.4.0 proof, then request a fresh independent PR full-gate correction rereview. Explain-change, verify, PR handoff, and all external release actions remain blocked.
