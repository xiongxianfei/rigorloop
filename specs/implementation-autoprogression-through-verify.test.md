# Implementation Autoprogression Through Verify Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/workflow-stage-autoprogression.md`
- Workflow spec: `specs/rigorloop-workflow.md`
- Review finding contract: `specs/review-finding-resolution-contract.md`
- Plan: `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`
- Proposal: `docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md`
- Spec-review: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/spec-review-r1.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`
- Architecture-review: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/architecture-review-r1.md`
- Plan-review: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/plan-review-r1.md`

## Testing strategy

- Use unit and fixture-backed integration tests for parser-owned contracts: change metadata profile policy, review-finding fields, review artifact validation, workflow-state synchronization, and lifecycle validation.
- Use routing fixtures for profile activation, phase refusal, test-spec settlement, milestone order, correction-loop convergence, stop conditions, and idempotent resume.
- Use contract/manual review for canonical skill guidance where no executable orchestrator exists yet; pair those checks with generated-output and adapter validation after canonical skill edits.
- Use targeted repository validators first, then selected broad smoke only when changed-path selection or the implementation plan requires it.
- Keep Phase C behavior behind fixture-proven refusal unless the persisted phase is `C` and promotion evidence is linked. The first implementation slice must prove Phase C cannot run accidentally.
- Treat final PR opening, deployment, publication, verify-failure repair, project-wide defaults, background execution, and independent `test-spec-review` as explicit exclusions.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `workflow-stage-autoprogression` R2am-R2ar; `rigorloop-workflow` R7ea-R7ev; proposal `AC-ITV-001`, `AC-ITV-002`, `AC-ITV-025`, `ITV-001`-`ITV-005`, `ITV-032`, `ITV-037` | T1, T2, T14 | unit, integration, contract | Closed profile values, independent authorization, durable persistence, cancellation, unknown values, dirty state, and profile-off behavior |
| `workflow-stage-autoprogression` R2as-R2ax; `rigorloop-workflow` R7eu-R7ew; proposal `AC-ITV-024`, `ITV-004`, `ITV-005`, `ITV-036` | T2, T3, T14 | integration, contract | Activation preconditions, phase persistence, phase A/B/C boundaries, promotion evidence, and refusal outside phase |
| `workflow-stage-autoprogression` R2ay-R2bb; `rigorloop-workflow` R7ex; proposal `AC-ITV-003`, `ITV-006`-`ITV-008`, `ITV-038` | T3, T4, T14 | integration, contract | Test-spec authoring, deterministic settlement, complete coverage, no gaps, input identity recording, and stale-identity pause |
| `workflow-stage-autoprogression` R2bc-R2bd; `rigorloop-workflow` R7ey; proposal `AC-ITV-004`, `ITV-009`, `ITV-010`, `ITV-022` | T5, T6, T14 | integration, manual | Ordered milestones, independent review rounds, context-reset evidence, and review-before-close |
| `workflow-stage-autoprogression` R2be-R2bl; `review-finding-resolution-contract` R1e-R1l; proposal `AC-ITV-005`-`AC-ITV-008`, `ITV-011`-`ITV-014` | T7, T8, T9, T14 | unit, integration, contract | `auto_fix_class`, closed values, closed mechanical kinds, declared-safe recipes, owner-decision pauses, and production-code proof |
| `workflow-stage-autoprogression` R2bm-R2bu; `rigorloop-workflow` R7faa-R7fab; `review-finding-resolution-contract` R11; proposal `AC-ITV-009`-`AC-ITV-014`, `ITV-015`-`ITV-021`, `ITV-025`, `ITV-034`, `ITV-039` | T9, T10, T11, T14 | unit, integration, contract | Round cap, shrinking sets, no-new-findings, path locality, scope-budget stops, governing-artifact stops, command boundaries, CI deny-list, and audit reconstruction |
| `workflow-stage-autoprogression` R2bv-R2bz; `rigorloop-workflow` R7fac-R7fad; proposal `AC-ITV-015`-`AC-ITV-020`, `ITV-023`-`ITV-031`, `ITV-036` | T12, T13, T14 | integration, smoke, manual | Final full review, explain-change, fresh verify, cache limits, verify failure pause, post-verify edit replay, completed profile, and stop-before-PR |
| Architecture and ADR implementation-profile policy boundary | T2, T6, T10, T12, T13, T14 | contract, manual | Ensures implementation uses existing workflow/review/validation surfaces and does not add services, schedulers, hosted PR actors, or release mechanisms |
| Plan M1-M5 implementation sequencing | T1-T15 | unit, integration, smoke, manual | Maps tests to the approved plan milestones and final proof obligations |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `workflow-stage-autoprogression` E21 | T2 | Activation after clean planning and separate authorization |
| `workflow-stage-autoprogression` E22 | T3, T4 | Test-spec settlement before implementation |
| `workflow-stage-autoprogression` E23 | T8, T10 | Mechanical finding correction and fresh review |
| `workflow-stage-autoprogression` E24 | T7 | Missing classification defaults to `none` and pauses |
| `workflow-stage-autoprogression` E25 | T10 | New finding after correction pauses |
| `workflow-stage-autoprogression` E26 | T12 | Phase B stops before `explain-change` |
| `workflow-stage-autoprogression` E27 | T13 | Phase C verifies and stops before PR |
| `rigorloop-workflow` E21 | T13 | Clean Phase C reports `pr` next without opening PR |
| `review-finding-resolution-contract` E15 | T7 | Unclassified finding pause |
| `review-finding-resolution-contract` E16 | T8 | Mechanical finding fields |
| `review-finding-resolution-contract` E17 | T9 | Declared-safe production-code proof |

## Edge case coverage

- `EC32`: implementation profile armed before clean planning pauses before test-spec: T2
- `EC33`: Phase A is audit-only and does not execute implementation: T2
- `EC34`: Phase B stops before `explain-change`: T12
- `EC35`: test-spec settlement input identity changes before first milestone review: T4
- `EC36`: missing `auto_fix_class` behaves as `none`: T7
- `EC37`: declared-safe recipe touches forbidden or governing paths: T9, T10
- `EC38`: correction round introduces new finding class: T10
- `EC39`: Phase C verify reports PR next but does not invoke PR: T13
- Dirty worktree or unrelated changed files block activation unless explicitly excluded: T2
- Cancellation prevents future automatic transitions: T1
- Resumption does not duplicate closed milestones or clean reviews: T5
- CI maintenance pauses when CI files are not enumerated or deny-list checks fail: T11
- Static repository check confirms no `test-spec-review` skill is introduced: T15

## Test cases

### T1. Implementation profile metadata schema is closed and independent

- Covers: `R2am`-`R2ar`, `R7ea`-`R7ev`, `AC-ITV-001`, `AC-ITV-002`, `AC-ITV-025`, `ITV-001`-`ITV-003`, `ITV-032`, `ITV-037`
- Level: unit
- Fixture/setup: Change metadata fixtures with profile `off`, valid authoring profile, valid implementation profile, malformed implementation profile, missing phase, unsupported phase, shared authorization record, cancellation, and forbidden live-state fields.
- Steps: Run the change metadata validator over each fixture.
- Expected result: Valid implementation-profile records pass only when authorization is independent, phase is closed to `A|B|C`, required fields are present, and live-state fields remain forbidden. Unknown profiles and malformed policy fail closed.
- Failure proves: Implementation authorization could be implied, malformed, or allowed to own live workflow state.
- Automation location: `scripts/test-change-metadata-validator.py` and `tests/fixtures/change-metadata/implementation-autoprogression-*`.

### T2. Activation gate and phase evaluator refuse unsafe starts

- Covers: `R2as`-`R2ax`, `R7eu`-`R7ew`, E21, `EC32`, `EC33`, `AC-ITV-024`, `ITV-004`, `ITV-005`, `ITV-036`
- Level: integration
- Fixture/setup: Workflow route fixtures for clean planning, missing plan-review, unsynchronized plan, unordered milestones, incomplete test-spec inputs, unrelated dirty state, missing commands, open governing findings, phase A, phase B, phase C without promotion evidence, and phase C with promotion evidence.
- Steps: Run the workflow transition evaluator or fixture harness over each state.
- Expected result: Activation starts only after clean planning and durable implementation-profile authorization. Phase A records audit decisions only, Phase B refuses closeout transitions, and Phase C refuses without linked promotion evidence.
- Failure proves: The profile can start without authority or execute behavior outside its persisted phase.
- Automation location: Workflow route fixture tests added during M2.

### T3. Test-spec settlement requires complete synchronized coverage

- Covers: `R2ay`, `R2az`, `R7ex`, E22, `AC-ITV-003`, `ITV-006`, `ITV-007`, `ITV-008`
- Level: integration
- Fixture/setup: Test-spec artifacts with active status, draft status, missing requirement coverage, missing acceptance coverage, missing negative or boundary cases, uncovered gaps, `needs-decision`, missing validation commands, upstream contradiction, structural validation failure, and clean settlement.
- Steps: Run the settlement validator or fixture evaluator.
- Expected result: Only the clean active/settled test spec with complete mapping, no gaps, no `needs-decision`, named commands, no contradictions, structural validation, and state synchronization settles.
- Failure proves: Implementation could begin from an incomplete or contradictory proof contract.
- Automation location: Test-spec settlement fixture tests added during M2.

### T4. Settlement input identities are rechecked by first milestone review

- Covers: `R2ba`, `R2bb`, `R7ex`, `EC35`, `ITV-038`
- Level: integration
- Fixture/setup: Settlement evidence with recorded spec, architecture/ADR, plan, and test-spec identities; paired first-code-review fixtures with matching and mismatching identities.
- Steps: Run the first milestone review precondition check.
- Expected result: Matching identities allow review to proceed; any changed input identity pauses before relying on settlement.
- Failure proves: Stale settlement could authorize implementation after governing inputs changed.
- Automation location: Workflow or review precondition fixture tests added during M2.

### T5. Milestones run in approved order and resume idempotently

- Covers: `R2bc`, `R2bd`, `R7ey`, `AC-ITV-004`, `AC-ITV-021`, `ITV-009`, `ITV-010`, `ITV-033`
- Level: integration
- Fixture/setup: Plan-state fixtures with ordered milestones, skipped M1, closed M1/open M2, duplicate resume after clean review, and final milestone state.
- Steps: Run workflow-state synchronization and route evaluation.
- Expected result: The evaluator runs only the next approved open milestone, does not skip ahead, does not rerun closed milestones or clean reviews unless inputs changed, and requires review before closure.
- Failure proves: Autoprogression could duplicate or reorder implementation work.
- Automation location: Workflow-state fixture tests added during M2.

### T6. Code-review rounds record independent context evidence

- Covers: `R2bd`, review independence architecture, `AC-ITV-014`, `ITV-010`, `ITV-022`
- Level: manual
- Fixture/setup: `skills/code-review/SKILL.md`, generated adapter output, review receipt templates, and sample review records.
- Steps: Inspect canonical and generated code-review guidance plus sample records.
- Expected result: Each review round is a fresh invocation over actual diff, governing artifacts, validation evidence, prior findings when applicable, context-reset mode, and reviewed commit/diff identity.
- Failure proves: Implementation and review could collapse into self-approval.
- Automation location: Manual contract review plus generated-output validation during M4.

### T7. Missing or `none` auto-fix classification pauses

- Covers: `R2be`-`R2bg`, `R1e`-`R1g`, E24, E15, `EC36`, `AC-ITV-005`, `AC-ITV-006`, `ITV-011`, `ITV-014`
- Level: unit
- Fixture/setup: Review finding fixtures with omitted `auto_fix_class`, explicit `none`, owner decision, compatibility alternative, unbounded paths, and nondeterministic validation.
- Steps: Run review artifact validation and correction eligibility evaluation.
- Expected result: Missing classification and every `none` condition pause the profile with open finding evidence.
- Failure proves: The orchestrator could infer or auto-fix findings without reviewer authority.
- Automation location: `scripts/validate-review-artifacts.py` fixtures and correction eligibility tests added during M3.

### T8. Mechanical findings require closed kind and deterministic authority

- Covers: `R2bh`-`R2bj`, `R1h`, `R1i`, E23, E16, `AC-ITV-007`, `ITV-012`
- Level: unit
- Fixture/setup: Mechanical finding fixtures for every allowed kind plus unsupported kind, missing affected paths, missing deterministic authority, and missing required validation.
- Steps: Run review artifact validation and correction eligibility evaluation.
- Expected result: Only allowed kinds with affected paths, deterministic authority, and required validation are eligible.
- Failure proves: Mechanical auto-fix scope could expand beyond deterministic recipes.
- Automation location: Review artifact validator tests added during M3.

### T9. Declared-safe findings require complete deterministic recipes

- Covers: `R2bk`, `R2bl`, `R1j`-`R1l`, E17, `EC37`, `AC-ITV-008`, `AC-ITV-009`, `ITV-013`, `ITV-015`, `ITV-017`
- Level: unit
- Fixture/setup: Declared-safe finding fixtures with complete recipe, missing recipe field, forbidden path, governing-artifact edit need, owner decision, new dependency, new component, production-code change without behavior proof, and production-code change citing existing test-spec mapping.
- Steps: Run review artifact validation and correction eligibility evaluation.
- Expected result: Only complete deterministic recipes without owner decisions, governing edits, or new scope are eligible; production-code changes require changed-behavior test proof or cited existing mapping.
- Failure proves: Declared-safe could become an unbounded reviewer escape hatch.
- Automation location: Review artifact validator tests added during M3.

### T10. Correction loops are bounded, shrinking, path-local, and auditable

- Covers: `R2bm`-`R2bt`, `R7faa`, `R7fab`, `AC-ITV-010`-`AC-ITV-013`, `ITV-016`, `ITV-018`-`ITV-021`, `ITV-034`, E25, `EC38`
- Level: integration
- Fixture/setup: Correction-loop fixtures for shrinking set, same-size set, increased set, new finding ID, new finding class, fourth round for one milestone, unauthorized path, generated-output derived path, approved workflow projection, governing artifact edit, unapproved command, and audit evidence.
- Steps: Run correction-loop guardrail evaluator over before/after finding sets, diff paths, commands, and audit records.
- Expected result: Only shrinking, no-new-finding, path-local, approved-command rounds within the per-milestone cap proceed; every automatic correction records reconstructable evidence.
- Failure proves: The profile could chase new work, oscillate, exceed caps, or apply unauditable fixes.
- Automation location: Workflow/review-resolution fixture tests added during M3 and M5.

### T11. Conditional CI maintenance is explicitly scoped and deny-list checked

- Covers: `R2bu`, `ITV-025`, `ITV-039`
- Level: integration
- Fixture/setup: Plan/test-spec fixtures that enumerate CI files, omit CI files, include credential references, include deploy target changes, include hosted-runner privilege changes, and include secrets references.
- Steps: Run CI-maintenance eligibility or workflow route fixtures.
- Expected result: Automatic CI maintenance proceeds only when CI files are explicitly enumerated and deny-list checks pass; otherwise the profile pauses.
- Failure proves: CI maintenance could mutate credential, deploy, runner, or secret behavior without explicit authority.
- Automation location: CI-maintenance route fixtures added during M3 or M4.

### T12. Phase B stops after final clean code review

- Covers: `R2bv`, `R7fac`, E26, `EC34`, `AC-ITV-015`, `ITV-023`, `ITV-024`, `ITV-036`
- Level: integration
- Fixture/setup: Final milestone fixtures with all findings closed, final full review clean, persisted phase `B`, and persisted phase `C`.
- Steps: Run workflow route evaluation after final clean review.
- Expected result: Phase B reports phase-boundary completion and refuses `explain-change`; Phase C may continue only when promotion evidence exists.
- Failure proves: Phase C behavior could run under Phase B configuration.
- Automation location: Workflow route fixtures added during M4.

### T13. Phase C uses fresh verify evidence and stops before PR

- Covers: `R2bw`-`R2bz`, `R7fac`, `R7fad`, E27, `rigorloop-workflow` E21, `EC39`, `AC-ITV-016`-`AC-ITV-020`, `ITV-026`-`ITV-031`
- Level: integration
- Fixture/setup: Phase C fixtures with clean final review, current explain-change, fresh verify pass, verify cache-only sensitive checks, informational cache hit after baseline, verify failure, post-verify edit, and successful PR-boundary state.
- Steps: Run verify/closeout route evaluation and change-metadata evidence validation.
- Expected result: Sensitive and correctness-bearing final checks require fresh actual runs; verify failure pauses without repair; post-verify edits require review/explanation/verify replay; successful verify completes the profile, computes branch readiness from recorded evidence, reports PR next, and does not invoke PR.
- Failure proves: Verification could rely on stale evidence, auto-repair failures, or cross the external PR boundary.
- Automation location: Verify and workflow fixtures added during M4.

### T14. Cross-surface behavior-preservation matrix proves first-slice coverage

- Covers: proposal `ITV-001`-`ITV-039`, `AC-ITV-001`-`AC-ITV-025`, profile-off compatibility, architecture boundary, and audit reconstruction
- Level: manual
- Fixture/setup: Completed M1-M4 validation output, generated output validation, review records, and `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/behavior-preservation.md`.
- Steps: Build and review the behavior-preservation matrix against the proposal's expected behavior changes and falsification list.
- Expected result: Every acceptance criterion and test check is covered by automated tests, manual review, or explicit deferred follow-up with owner and rationale. Profile-off behavior remains unchanged.
- Failure proves: The implementation could satisfy local tests while missing a proposal-level safety invariant.
- Automation location: Manual review plus artifact lifecycle validation during M5.

### T15. No independent test-spec-review stage is introduced

- Covers: `ITV-007`, non-goal for `test-spec-review`
- Level: smoke
- Fixture/setup: Repository tree after skill/spec updates.
- Steps: Check that no `skills/test-spec-review/SKILL.md`, `.agents/skills/test-spec-review/SKILL.md`, lifecycle stage enum, or workflow stage row introduces `test-spec-review`.
- Expected result: Test-spec settlement exists as a deterministic gate, but no formal `test-spec-review` skill or stage is added.
- Failure proves: The implementation changed workflow topology beyond the approved proposal.
- Automation location: Static repository check added during M5.

## Fixtures and data

- Change metadata fixtures under `tests/fixtures/change-metadata/implementation-autoprogression-*`.
- Review artifact fixtures under `tests/fixtures/review-artifacts/implementation-autoprogression-*`.
- Workflow route and correction-loop fixtures under the existing workflow or artifact-lifecycle fixture layout selected during implementation.
- Test-spec settlement fixtures with complete, incomplete, stale, contradictory, and structurally invalid test specs.
- Behavior-preservation evidence at `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/behavior-preservation.md`.

## Mocking/stubbing policy

- Prefer parser and fixture tests over mocks for metadata, review records, lifecycle state, and workflow routes.
- Stub command execution only where the test is about command authorization or route selection, not validator semantics.
- Do not mock generated-output validation; regenerate or validate generated artifacts through repository-owned scripts.
- Do not mock final verify freshness in Phase C fixtures; represent freshness with explicit actual-run or cache evidence records.

## Migration or compatibility tests

- Existing change records without implementation-profile policy remain `off`.
- Existing authoring-profile records remain valid and do not authorize implementation.
- Existing review findings without `auto_fix_class` remain parseable but behave as `none` only when implementation-profile correction eligibility is evaluated.
- Existing plan and review workflows remain unchanged when the implementation profile is `off`.
- Public adapter/generated skill validation proves generated guidance remains distributable after canonical skill updates.

## Observability verification

- Automatic transition audit records include profile authorization, activation baseline, phase, milestone, review round, finding IDs, classifications, recipes, affected paths, actual paths changed, before/after unresolved finding sets, commands, validation results, review-context reset evidence, commit or diff identity, and completion or pause result.
- Verify audit records include evidence inputs, source revision, working-tree state, validation freshness, commands, outputs or transcript references, and completion result.
- Completion records state that verify completed, PR was not opened, and human authorization is required for PR.

## Security/privacy verification

- Profile policy and audit records must not contain secrets, credentials, private keys, raw environment dumps, private hostnames, usernames, or machine-local absolute paths.
- Automatic commands cannot be credentialed, destructive, deployment, publication, branch-push, hosted PR, or remote-notification commands.
- CI maintenance fixtures deny-list credentials, deploy targets, hosted-runner privilege changes, and secrets references unless explicit human authorization pauses and redirects the workflow.
- PR opening, publication, deployment, package release, and remote review request remain outside the profile.

## Performance checks

- No broad performance benchmark is required for first-slice workflow guidance and validator changes.
- Validator and fixture additions should keep targeted test output bounded and actionable.
- If generated-output or adapter validation becomes materially slower, record the impact in validation notes and keep broad smoke for final closeout rather than inner-loop proof.

## Manual QA checklist

- Confirm canonical skill text preserves user-facing clarity for `auto-through: verify`, phase boundaries, pause reasons, and PR boundary language.
- Confirm generated adapter guidance matches canonical skills after regeneration.
- Confirm behavior-preservation evidence can reconstruct why each automatic correction would have been allowed or paused.
- Confirm first-time exposure wording describes "verify-bounded implementation autoprogression" and later references can use the shorter profile name.

## What not to test and why

- Do not test hosted PR creation, package publication, deployment, branch push, or remote notification because they are explicit non-goals.
- Do not test automatic verify-failure repair because it is a permanent non-goal for this profile and requires explicit user direction.
- Do not test project-wide defaults because change-local opt-in is the approved first slice.
- Do not test a new `test-spec-review` stage beyond the static absence check because the approved design uses deterministic settlement.
- Do not build a background worker or asynchronous execution harness because execution remains interactive workflow-managed behavior.

## Uncovered gaps

- None for the first implementation slice. Phase C execution remains guarded until Phase B promotion evidence exists; the tests above prove refusal and boundary behavior before enablement.

## Next artifacts

- Implement M1 after this active test spec is recorded.
- Code-review after each implementation milestone.
- Explain-change after all implementation milestones and required review-resolution close.
- Verify before PR handoff.

## Follow-on artifacts

- None yet.

## Readiness

- Active proof surface for implementing M1 through M5 in `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md`.
- The active plan `Current Handoff Summary` owns the next workflow action.
