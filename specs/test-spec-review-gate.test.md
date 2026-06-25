# Test-Spec-Review Gate Test Spec

## Status

active

## Related spec and plan

- Spec: [Test-Spec-Review Gate](test-spec-review-gate.md), approved.
- Proposal: [Independent Test-Spec-Review Gate for Proof-Map Adequacy](../docs/proposals/2026-06-25-independent-test-spec-review-gate.md), accepted.
- Architecture: [Independent Test-Spec-Review Gate Architecture](../docs/architecture/2026-06-25-independent-test-spec-review-gate.md), approved.
- ADR: [ADR-20260625 Independent Test-Spec-Review Gate](../docs/adr/ADR-20260625-independent-test-spec-review-gate.md), accepted.
- Plan: [Independent Test-Spec-Review Gate Plan](../docs/plans/2026-06-25-independent-test-spec-review-gate.md), active after clean `plan-review-r2`.
- Spec-review: [spec-review-r1](../docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/spec-review-r1.md), approved.
- Architecture-review: [architecture-review-r1](../docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/architecture-review-r1.md), approved.
- Plan-review: [plan-review-r2](../docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/plan-review-r2.md), approved.

## Testing strategy

- Use contract and lifecycle tests in `specs/rigorloop-workflow.test.md`, `scripts/test-artifact-lifecycle-validator.py`, and `scripts/lifecycle_state_sync.py` for workflow order, implementation eligibility, stale review routing, and plan-state synchronization.
- Use review-artifact validator tests in `scripts/test-review-artifact-validator.py` and `scripts/validate-review-artifacts.py` for review status, immediate-next-stage, implementation-handoff, formal record placement, clean-review receipts, material findings, and review-resolution behavior.
- Use skill validator and skill packaging tests in `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/test-build-skills.py`, `scripts/build-skills.py --check`, `scripts/build-adapters.py`, and `scripts/validate-adapters.py` for canonical skill shape, assets, routing text, generated package inclusion, and no hand-edited adapter output.
- Use fixture-backed integration tests for complete proof maps, missing requirement coverage, happy-path-only failure behavior, vague manual proof, nonexistent commands, upstream contradictions, and post-approval substantive edits.
- Use manual contract review only for nuanced prose boundaries that are not safely reducible to string assertions, such as whether review dimensions stay proof-map-focused and whether `code-review` and `verify` remain meaningful downstream backstops.
- Do not execute final validation commands as part of `test-spec-review`; tests only prove command classification, bounded optional command checks, and later-stage ownership.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T10 | integration, contract | Workflow stage order and contributor-facing chain show `test-spec-review` before `implement`. |
| R2 | T2, T9, T15 | integration | Implementation blocks missing, stale, non-approved, or open-finding review evidence. |
| R3 | T1, T10 | integration, contract | Test-spec status vocabulary remains `active`; review approval is external. |
| R4 | T4 | integration | Formal approval is recorded in a separate review artifact and review log. |
| R5 | T3 | unit, integration | Review status enum is closed. |
| R6 | T3 | unit, integration | Implementation-handoff enum is closed. |
| R7 | T3 | unit, integration | Status-to-handoff mapping is deterministic. |
| R8 | T3, T6 | unit, integration | Immediate-next-stage enum is closed and routing-specific. |
| R9 | T3 | unit, integration | `implement` next stage is valid only for approved reviews. |
| R10 | T5, T7, T8 | integration | Test-spec proof-map defects produce `changes-requested`. |
| R11 | T6 | integration | Upstream contradictions produce `blocked` and upstream routing. |
| R12 | T6 | integration | Inconclusive reviews name evidence gap and smallest needed evidence. |
| R13 | T7, T12, T14 | integration, manual | Traceability covers requirements, examples, edge cases, architecture, milestones, commands, fixtures, and evidence. |
| R14 | T7 | integration | Happy-path-only proof fails when failure behavior is required. |
| R15 | T7 | integration | Vague manual proof fails; complete manual proof fields pass. |
| R16 | T8 | integration | Commands are classified as existing, planned, manual-only, or external/release-owned. |
| R17 | T8 | integration, manual | Optional review-time command execution is bounded to no-side-effect checks. |
| R18 | T14 | integration, manual | Fixtures and data are deterministic, isolated, safe, representative, and cleaned up. |
| R19 | T9 | integration | Substantive post-approval test-spec edits stale approval. |
| R20 | T9 | integration | Non-substantive typo, heading, link, or list-order edits do not automatically stale approval. |
| R21 | T6, T9 | integration | Upstream revision routing blocks implementation until proof map is revised or confirmed current. |
| R22 | T4 | integration | Formal review records live under `docs/changes/<change-id>/reviews/` and update `review-log.md`. |
| R23 | T4, T5 | integration | Clean reviews do not require empty `review-resolution.md`; material/blocking outcomes require disposition. |
| R24 | T10, T12 | contract, manual | Skill output avoids implementation, code-review, validation, branch, PR, and final-closeout claims. |
| R25 | T10 | contract, integration | `test-spec` routes formal workflow output to `test-spec-review`. |
| R26 | T2, T10 | contract, integration | `implement` requires active test spec plus approved current recorded review. |
| R27 | T3 | unit, integration | Unknown review values fail closed before consistency checks. |
| R28 | T11 | smoke, integration | Generated and installed packages include the new skill and assets through normal generation. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 complete proof map is approved | T7 | Complete fixture maps requirements, examples, edge cases, milestones, commands, fixtures, and evidence to approved handoff. |
| E2 missing failure proof blocks implementation | T7 | Happy-path-only fixture for failure-bearing requirement returns non-approval. |
| E3 upstream ambiguity routes upstream | T6 | Contradictory spec/plan fixture routes to owning upstream revision stage. |
| E4 isolated advisory review does not authorize implementation | T13 | Advisory review fixture is clean but does not satisfy formal implementation eligibility. |
| E5 low-risk command check stays bounded | T8 | Help-text/dry-run-only fixture passes; side-effecting, network, secret, or fixture-setup command checks fail. |

## Edge case coverage

- EC1 happy-path-only proof with required failure behavior: T7.
- EC2 nonexistent or ownerless validation command: T8.
- EC3 vague manual proof: T7.
- EC4 typo-only edit after approval: T9.
- EC5 plan revision after review: T9.
- EC6 isolated advisory approval: T13.
- Unknown review status, immediate-next-stage, or implementation-handoff value: T3.
- Approved review with `Implementation handoff: not-allowed`: T3.
- `changes-requested` with `Implementation handoff: allowed`: T3.
- `approved` with `Immediate next stage: test-spec revision`: T3.
- Clean review with empty `review-resolution.md`: T4.
- Material finding without evidence, required outcome, or safe resolution path: T5.
- Manual proof with complete required fields but automation rationale: T7.
- Planned command with owner and milestone but not yet implemented: T8.
- Substantive fixture or validation-command edit after approval: T9.
- Generated adapter manifest missing `test-spec-review`: T11.

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| M1 Workflow and contract baseline | T1, T2, T3, T4, T5, T6, T9, T12 | Workflow order, status separation, enums, routing, review placement, staleness, and behavior preservation. |
| M2 Canonical skill and review assets | T7, T8, T10, T13, T14 | Skill/assets, proof dimensions, manual proof, command boundaries, isolated behavior, and fixture/data guidance. |
| M3 Validators, fixtures, generated package proof, and representative evidence | T3, T4, T6, T7, T8, T9, T11, T15 | Validator fixtures, stale-review fixtures, generated adapter proof, representative review outcomes, and lifecycle validation. |

## Test cases

### T1. Workflow chain inserts test-spec-review and preserves active test-spec state

- Covers: R1, R3, AC-TSR-001, AC-TSR-002
- Level: integration
- Fixture/setup: `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/workflows.md`, and lifecycle fixtures for standard workflow chains.
- Steps:
  - Add or update assertions that the standard workflow chain contains `plan-review -> test-spec -> test-spec-review -> implement`.
  - Assert the test-spec lifecycle row keeps `active` as the durable current state and does not add `approved` or `changes-requested`.
  - Assert contributor-facing workflow guidance reflects the same order.
- Expected result: Workflow and lifecycle guidance place the new gate between test-spec and implement, while test specs remain `active`.
- Failure proves: Implementation can still begin merely because a test spec exists or test-spec approval is conflated with artifact status.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-skill-validator.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

### T2. Implement blocks without approved current test-spec-review evidence

- Covers: R2, R26, AC-TSR-006, AC-TSR-007
- Level: integration
- Fixture/setup: Implementation-readiness fixtures with active test spec, missing review, stale review, `changes-requested`, `blocked`, `inconclusive`, open findings, and approved review.
- Steps:
  - Assert `implement` handoff is unavailable when review evidence is missing, stale, non-approved, has `Implementation handoff: not-allowed`, or has open material findings.
  - Assert implementation handoff is available only when active test spec and latest applicable approved review evidence are present and current.
- Expected result: Only approved, current, recorded, open-finding-free review evidence allows implementation eligibility.
- Failure proves: The new gate can be bypassed.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-skill-validator.py`.

### T3. Review result enums and routing combinations fail closed

- Covers: R5, R6, R7, R8, R9, R27, AC-TSR-003, AC-TSR-004
- Level: unit
- Fixture/setup: Review-artifact fixtures for all valid statuses and invalid unknown values.
- Steps:
  - Add tests for allowed `Review status`, `Implementation handoff`, and `Immediate next stage` values.
  - Add unknown-value tests with `unknown_value` or `not_in_vocabulary` in the test name.
  - Assert invalid status/handoff/stage combinations fail before downstream routing, including `changes-requested` with `allowed`, non-approved with `allowed`, and approved with revision stages.
- Expected result: Closed vocabularies and consistency mappings are enforced fail-closed.
- Failure proves: Validators can silently accept unsupported lifecycle routing.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/validate-review-artifacts.py --mode structure <fixture-root>`.

### T4. Formal review records use change-pack placement

- Covers: R4, R22, R23, AC-TSR-012, AC-TSR-013
- Level: integration
- Fixture/setup: Change-pack fixtures under `tests/fixtures/review-artifacts/` with clean and material `test-spec-review` records.
- Steps:
  - Assert formal `test-spec-review-r<n>.md` records under `docs/changes/<change-id>/reviews/` validate and are referenced from `review-log.md`.
  - Assert clean review records do not require an empty `review-resolution.md`.
  - Assert material or blocking outcomes require review-resolution disposition entries.
- Expected result: Formal review evidence is durable, indexed, and resolution behavior is conditional on findings or blockers.
- Failure proves: Review approval can become chat-only or resolution artifacts can become empty ceremony.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/validate-review-artifacts.py --mode structure <change-pack>`.

### T5. Material findings identify proof-map defects with actionable resolution

- Covers: R10, R23, AC-TSR-011
- Level: integration
- Fixture/setup: `changes-requested` review records with material findings for missing coverage, vague manual proof, and invalid command ownership.
- Steps:
  - Assert each finding includes Finding ID, severity, location, evidence, required outcome, and safe resolution path or `needs-decision` rationale.
  - Assert missing finding fields fail validation.
  - Assert `review-resolution.md` uses allowed dispositions and closes only with required evidence.
- Expected result: Material proof-map defects are recorded before fixes and have actionable resolution paths.
- Failure proves: Review findings can become vague or unactionable.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/validate-review-artifacts.py --mode closeout <change-pack>`.

### T6. Blocked and inconclusive reviews route to upstream or evidence production

- Covers: R8, R11, R12, R21, EC5
- Level: integration
- Fixture/setup: Review fixtures for contradictory spec/plan mappings, missing required architecture review, missing command ownership evidence, and missing target revision identity.
- Steps:
  - Assert upstream contradictions return `blocked` with `Immediate next stage: spec revision`, `architecture revision`, or `plan revision`.
  - Assert missing evidence returns `inconclusive`, `Immediate next stage: none`, and names the smallest evidence needed to make review conclusive.
  - Assert implementation handoff remains unavailable until upstream artifacts settle and a later review confirms the proof map.
- Expected result: Review does not invent semantics for upstream gaps and does not authorize implementation without required evidence.
- Failure proves: The gate can silently repair or ignore upstream ambiguity.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`.

### T7. Proof adequacy fixtures cover complete, missing, happy-path-only, and vague-manual cases

- Covers: R10, R13, R14, R15, E1, E2, EC1, EC3, AC-TSR-005, AC-TSR-006
- Level: integration
- Fixture/setup: Representative active test specs for complete proof map, missing requirement, missing negative case, vague manual proof, and complete manual proof.
- Steps:
  - Validate the complete proof-map fixture as `approved` and `Implementation handoff: allowed`.
  - Validate missing requirement coverage, happy-path-only failure proof, and vague manual proof as non-approved.
  - Assert complete manual proof includes stable ID, automation rationale, exact steps, environment, evidence artifact, pass condition, failure condition, and owning stage.
- Expected result: Adequate proof maps pass; incomplete proof maps fail before implementation.
- Failure proves: The review can approve a proof map that does not prove the approved contract.
- Automation location: `python scripts/test-review-artifact-validator.py`; representative fixtures under `tests/fixtures/review-artifacts/test-spec-review/`.

### T8. Validation command classification and bounded command checks are enforced

- Covers: R16, R17, E5, EC2
- Level: integration
- Fixture/setup: Test-spec fixtures referencing existing configured commands, planned commands with owner/milestone, manual-only checks, external/release-owned commands, nonexistent commands, and side-effecting command checks.
- Steps:
  - Assert every referenced command is classified as existing, planned, manual-only, or external/release-owned.
  - Assert planned commands name an owner and milestone.
  - Assert optional review-time checks are limited to resolvability, help-text, or dry-run with no fixture setup, side effects, secrets, or network dependence.
  - Assert nonexistent ownerless commands produce non-approval.
- Expected result: Command proof is reviewable without becoming final validation execution.
- Failure proves: The review can approve invented commands or blur into verify.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`.

### T9. Stale-review detection distinguishes substantive and non-substantive edits

- Covers: R19, R20, R21, EC4, EC5, AC-TSR-007
- Level: integration
- Fixture/setup: Approved review fixture plus post-review test-spec edits affecting mappings, commands, fixtures, manual procedures, milestone mapping, automation levels, pass/fail criteria, and non-goal treatment; separate typo, heading, link, and list-reordering edits.
- Steps:
  - Assert substantive edits stale the approval and block implementation handoff.
  - Assert non-substantive edits do not automatically stale approval when proof obligations are confirmed unchanged.
  - Assert upstream plan revision blocks handoff until the proof map is revised or confirmed current by later review.
- Expected result: Implementation relies only on review evidence for the proof map it actually consumes.
- Failure proves: Review approval can outlive the test spec it reviewed.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-review-artifact-validator.py`.

### T10. Canonical skills expose correct routing and claim boundaries

- Covers: R1, R3, R24, R25, R26, AC-TSR-001, AC-TSR-002, AC-TSR-015
- Level: contract
- Fixture/setup: `skills/test-spec-review/SKILL.md`, `skills/test-spec/SKILL.md`, `skills/implement/SKILL.md`, `skills/workflow/SKILL.md`, and `specs/skill-contract.md` when changed.
- Steps:
  - Assert `test-spec-review` skill frontmatter, workflow role, upstream/downstream boundaries, result skeleton, and asset references are normalized.
  - Assert `test-spec` formal workflow downstream routes to `test-spec-review`.
  - Assert `implement` requires active test spec plus approved current recorded review evidence.
  - Assert `test-spec-review` does not claim implementation, code-review, validation success, branch readiness, PR readiness, or final closeout.
- Expected result: Published skill guidance routes the workflow through the new gate without weakening adjacent stages.
- Failure proves: Contributors can follow shipped skills and skip or overclaim the new review gate.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T11. Generated adapter packages include test-spec-review and assets

- Covers: R28, AC-TSR-008
- Level: smoke
- Fixture/setup: Canonical `skills/test-spec-review/`, `dist/adapters/manifest.yaml`, and temporary adapter output directory.
- Steps:
  - Build adapters using the version from `dist/adapters/manifest.yaml`.
  - Validate generated Codex, Claude, and opencode packages include `test-spec-review` and mapped assets.
  - Assert generated public adapter output is not hand-edited in tracked source.
- Expected result: Public package consumers receive the same new skill and assets as canonical source.
- Failure proves: The gate exists only in repository-local source and not in supported public installations.
- Automation location: `python scripts/build-adapters.py --version <manifest-version> --output-dir <tmpdir>`; `python scripts/validate-adapters.py --root <tmpdir> --version <manifest-version>`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`.

### T12. Downstream code-review and verify remain required backstops

- Covers: R13, R24, AC-TSR-009
- Level: manual
- Fixture/setup: Updated workflow/spec/skill surfaces and behavior-preservation evidence under the change pack.
- Steps:
  - Review changed workflow and skill text for any claim that `test-spec-review` replaces `code-review` or `verify`.
  - Confirm behavior-preservation evidence records `code-review` and `verify` as preserved downstream responsibilities.
- Expected result: The new gate approves planned proof only; implemented proof and final evidence remain downstream.
- Failure proves: The new gate weakens later review or final verification.
- Automation location: Manual contract review recorded in `docs/changes/2026-06-25-independent-test-spec-review-gate/behavior-preservation.md`.

### T13. Isolated advisory review stays isolated

- Covers: R4, R22, E4, EC6, AC-TSR-014
- Level: integration
- Fixture/setup: Advisory review fixture without formal workflow-managed change-pack recording and formal review fixture with recording.
- Steps:
  - Assert advisory `approved` output does not satisfy formal implementation eligibility.
  - Assert formal review evidence under the change pack is required before workflow-managed handoff is allowed.
- Expected result: Manual review remains useful without creating false lifecycle approval.
- Failure proves: Isolated review can accidentally authorize implementation.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-review-artifact-validator.py`.

### T14. Fixture and data guidance is deterministic, isolated, and safe

- Covers: R13, R18
- Level: integration
- Fixture/setup: Complete and invalid proof-map fixtures with declared fixtures, cleanup, data-safety, network/time/randomness boundaries, and representative cases.
- Steps:
  - Assert complete fixtures declare deterministic setup, isolation, cleanup, and safe representative data.
  - Assert external mutable state, uncontrolled time/randomness, unsafe data, or missing cleanup produces non-approval when relevant.
- Expected result: Review can reject proof maps that would produce nondeterministic or unsafe evidence.
- Failure proves: Implementation can rely on unstable or unsafe proof surfaces.
- Automation location: `python scripts/test-review-artifact-validator.py`; manual review of representative fixture design when semantic validation is not practical.

### T15. Lifecycle validation recognizes test-spec-review implementation eligibility

- Covers: R2, R19, R27
- Level: integration
- Fixture/setup: Full change-pack fixtures including active test spec, review record, review log, plan handoff, and change metadata.
- Steps:
  - Assert lifecycle validation accepts a synchronized approved-current review path.
  - Assert missing, stale, unknown-valued, or inconsistent review evidence blocks lifecycle handoff before implementation.
  - Assert unknown vocabulary errors are explicit.
- Expected result: Repository lifecycle validation protects the new gate at workflow handoff time.
- Failure proves: Individual review records validate but workflow routing can still bypass the gate.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

## Fixtures and data

- Review-artifact fixtures should live under `tests/fixtures/review-artifacts/test-spec-review/` or the nearest existing review-artifact fixture convention used by `scripts/test-review-artifact-validator.py`.
- Lifecycle fixtures should live beside existing lifecycle-state fixtures in `scripts/test-artifact-lifecycle-validator.py` unless the test helper is split into fixture files during implementation.
- Command fixtures must use repository-local no-network commands and must not require secrets or external services.
- Adapter proof must use a temporary output directory and the manifest version from `dist/adapters/manifest.yaml`.
- Proof-map fixtures must use synthetic requirements, examples, commands, and data. Do not include sensitive or machine-local data.

## Mocking/stubbing policy

- Prefer filesystem-backed temporary fixtures over mocks for review records, plan state, change metadata, test specs, and generated adapter packages.
- Mock subprocess or command execution only when proving that disallowed review-time command checks are not invoked; do not mock validator parsing that can run directly.
- Do not mock generated package contents when adapter build and validation commands can run against a temporary directory.

## Migration or compatibility tests

- Historical test specs are not retroactively migrated in the first slice.
- Compatibility proof must show existing workflow stages, direct isolated skill invocations, `code-review`, and `verify` still behave as downstream backstops.
- Rollback proof must show `test-spec -> implement` can be restored by reverting routing and generated package inclusion while preserving historical review records.

## Observability verification

- Review outputs must expose target, review status, material findings, recording status, review record, review log, review-resolution status, open blockers, immediate next stage, implementation handoff, and stop condition.
- Failure records must identify the requirement, example, edge case, command, fixture, milestone, or upstream artifact that made proof inadequate or unreviewable.
- Validator failures should include explicit unknown-value or inconsistent-combination messages.

## Security/privacy verification

- `test-spec-review` fixtures and manual proof records must avoid secrets, credentials, private network access, and sensitive operational data.
- Optional review-time command checks must prohibit network dependence, side effects, fixture setup, and secret access.
- Generated package proof must not require publishing, registry access, or live adapter installation.

## Performance checks

- Review validation should start from bounded evidence and fixture-level checks.
- Expensive adapter proof is required when canonical skill packaging changes, but ordinary contributors do not need all supported tools installed locally.
- No numeric quality score, semantic proof-map scorer, or broad model-based evaluation is required.

## Manual QA checklist

- Confirm `test-spec-review` review dimensions remain proof-map-focused and do not reapprove product direction.
- Confirm `code-review` and `verify` language remains meaningful and required.
- Confirm published skill wording avoids repository-maintainer-only implementation details.
- Confirm behavior-preservation evidence records unchanged downstream responsibilities.

## What not to test and why

- Do not test historical migration of old test specs; the approved first slice is forward-only.
- Do not execute final product validation commands during `test-spec-review`; that belongs to implementation, CI, code-review, or verify.
- Do not test numeric proof scoring; the spec explicitly keeps reviewer judgment.
- Do not require a different model or vendor; review independence policy is broader than this gate.
- Do not hand-edit or inspect generated public adapter bodies as source; build and validate generated packages from canonical sources.

## Uncovered gaps

None. Requirements R1-R28, examples E1-E5, edge cases EC1-EC6, architecture boundaries, and plan milestones M1-M3 have planned proof.

## Next artifacts

```text
implement M1
code-review M1
review-resolution, when triggered
implement M2
code-review M2
review-resolution, when triggered
implement M3
code-review M3
review-resolution, when triggered
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action. This test spec does not claim implementation, code-review, verification, branch readiness, or PR readiness.
