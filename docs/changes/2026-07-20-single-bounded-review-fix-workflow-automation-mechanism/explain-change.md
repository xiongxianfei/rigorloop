# Single Bounded Review-Fix Workflow Automation Change Explanation

## Summary

This change replaces three independently writable workflow-automation profiles with one target-driven `bounded-review-fix` mechanism.

The public command surface now normalizes current and legacy commands into one structured target, while execution remains bounded by separate authoring, implementation, and verification authority.
The implementation preserves formal review independence, stage-specific correction ownership, active-plan live-state ownership, evidence-first recovery, and the hard stop before PR or other external actions.

This explanation covers the reviewed branch range `52bdcbb329897225c22a593b8e04541409e2d315..b4f08b56`.
The later commit `105e6d09` records the clean final holistic rereview and does not change the reviewed runtime behavior.

## Problem

The repository had three automation mechanisms with overlapping lifecycle responsibilities:

- `authoring-through-plan-review`;
- proposal-side `bounded-review-fix`;
- `implementation-through-verify`.

They had evolved separate state, authorization, continuation, recovery, and reporting rules.
A shared command name alone would not remove that duplication because the underlying writable state machines could still disagree.

The required outcome was one mechanism whose target states where the user wants to stop, whose authority states what may execute now, and whose durable evidence allows safe pause, resume, correction, cancellation, and migration.

## Decision trail

| Decision level | Selected decision | Durable source |
| --- | --- | --- |
| Exploration and option comparison | Select O2: expand `bounded-review-fix` into the one target-driven engine. Reject keeping three engines, a dispatcher-only facade, an immediate general workflow DSL, and blanket proposal-to-verify authority. | [Proposal](../../proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md) |
| Mechanism contract | New automation writes only `workflow.automation` with `mechanism: bounded-review-fix`; legacy profiles remain compatibility inputs. | `BRF-R001`-`BRF-R008j`, `BRF-R091`-`BRF-R098i` in the [approved spec](../../../specs/single-bounded-review-fix-workflow-automation.md) |
| Target and position | Persist a structured stage plus occurrence; bind repeated stages to one milestone; derive pre-plan position from artifacts and use the active plan after plan creation. | `BRF-R009`-`BRF-R023` |
| Authority | Separate non-executable parent authorization from stage-bound effective capability; keep authoring, implementation, and verification risk classes independent. | `BRF-R024`-`BRF-R046` |
| Review and correction | Treat proposal review as a first-class target, separate review occurrence from clean-gate approval, preserve driver-owned proposal correction and reviewer-owned implementation correction. | `BRF-R047`-`BRF-R067` |
| Recovery | Persist a capability-bound prepared receipt before mutation, reconcile evidence before retry, and fail closed on contradictory or ambiguous state. | `BRF-R068`-`BRF-R077` |
| Stage execution | Project every stage into one complete immutable policy, preserve stage-owning skills, require final holistic review and fresh verification, and stop before external actions. | `BRF-R078`-`BRF-R090` |
| Architecture | Keep specifications normative; put public semantics in `skills/workflow/SKILL.md`, executable behavior in named Python modules, and canonical state only in `change.yaml#workflow.automation`. | [Architecture](../../architecture/system/architecture.md), [ADR](../../adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md) |
| Delivery sequence | Implement schema/policy, state/recovery, routing/authority, authoring, implementation/verification, then atomic public cutover. | M1-M6 in the [active plan](../../plans/2026-07-21-single-bounded-review-fix-workflow-automation.md) |

The approved specification is the sole normative automation contract.
The older workflow and review specs retain only explicitly preserved lifecycle, review-resolution, and compatibility responsibilities through the exact cross-spec disposition ledger.

## Diff rationale by area

| File or area | Change | Why | Requirement, design, or milestone | Test or evidence |
| --- | --- | --- | --- | --- |
| `schemas/change.schema.json`, `scripts/validate-change-metadata.py`, metadata regressions | Add the unified run, target, parent authorization, effective capability, receipt, migration, and closed-state shapes; reject unknown and mixed writable state. | Durable state must be singular, typed, and fail closed before execution. | `BRF-R001`-`BRF-R008j`, `BRF-R024`-`BRF-R046`; M1 | T1, T2, T7, T8 |
| `scripts/workflow_automation_policy.py` and its tests | Add frozen enums, complete sixteen-field stage policies, transition graphs, applicability, completion, retry, correction, and stop rules. | The executable projection must not invent or omit normative policy. | `BRF-R079`-`BRF-R080`; ADR policy projection; M1 | T3, T4, T26 |
| `scripts/workflow_automation_state.py` and its tests | Add the sole atomic state writer, compare-and-swap updates, prepared receipts, reconciliation, cancellation, and one-way migration. | Interrupted execution and concurrent or stale writes require one recoverable write boundary. | `BRF-R068`-`BRF-R077`, `BRF-R091`-`BRF-R098`; M2 | T14-T16, T19, T23, T29 |
| `scripts/workflow_automation.py` and its tests | Add command normalization, target binding, canonical-position resolution, capability derivation, stage coordination, proposal correction, milestone loops, legacy adapters, status, and public activation. | All automation paths need one evaluator without taking ownership from stage artifacts or the plan. | `BRF-R003`-`BRF-R067`, `BRF-R078`-`BRF-R100`; M3-M6 | T4-T13, T17-T22, T24-T30 |
| `scripts/workflow_code_state.py` and its tests | Derive a Git-backed target ref, merge base, exact reviewed commit, and complete changed-file set; reject target drift, unreviewed commits, dirty files, and unsafe exclusions. | Verification authority must bind to the exact reviewed code state rather than caller assertions. | `BRF-R043a`-`BRF-R043e`, `BRF-R085`-`BRF-R086`; architecture trust boundary; M5 | T9, T18, T28 |
| `scripts/validate_workflow_automation.py` and its tests | Validate every closed vocabulary and cross-record invariant, including occurrence, authority, receipt, policy, migration, and exact cross-spec dispositions. | Invalid durable state must fail before consistency or mutation logic can accept it. | `BRF-R008`-`BRF-R008j`, `BRF-R098e`-`BRF-R102`; M1-M6 | T2-T5, T7-T8, T14-T16, T19-T23 |
| Lifecycle, review, query, and state-sync scripts and tests | Teach existing repository tools to query and validate unified automation evidence without making it the live workflow cursor or review-verdict owner. | The new evidence must compose with existing canonical lifecycle and review ownership. | `BRF-R018`-`BRF-R023`, `BRF-R060`-`BRF-R061`, `BRF-R099`-`BRF-R100`; M2-M6 | T6, T10, T12, T22 |
| `scripts/validation_selection.py` and selector tests | Classify every automation source/test path and select engine, policy, state, code-state, and validator regressions as one complete category. | Automation changes must not bypass a required proof suite. | M6 integration proof; final finding `BRF-FH-CR1` | T25, direct ten-path classification, 133 selector regressions |
| `skills/workflow/SKILL.md`, affected lifecycle skills, `docs/workflows.md`, and `README.md` | Publish one `workflow auto: <stage>` model, keep legacy aliases as adapters, preserve direct-skill isolation, and document authorization pauses and the external-action boundary. | User-facing behavior must match the unified engine and stage ownership contracts. | `BRF-R002`-`BRF-R005`, `BRF-R078`, `BRF-R087`-`BRF-R100`; M4-M6 | T12, T20, T22, T25, T27-T28 |
| Unified and amended specifications | Make the new spec canonical, supersede the old writable review-fix contract, and classify every affected legacy selector exactly once. | One mechanism requires one normative automation owner without erasing preserved review and lifecycle rules. | `BRF-R003a`-`BRF-R003d`, `BRF-R098e`-`BRF-R098i` | T1, T21 |
| Architecture, diagrams, and ADRs | Separate public orchestration, executable tooling, and persisted evidence; supersede the three mechanism-specific ADRs. | Code ownership, state ownership, and authority flow must be unambiguous before implementation. | Architecture decisions and ADR-20260721 | Architecture reviews R1-R3; T23 |
| Active and predecessor plans | Deliver the cutover through six reviewable milestones and preserve supersession context. | The migration could not safely activate partially. | M1-M6 | Milestone review records and proof gates |
| Change-local proposal, reviews, review resolution, and metadata | Record the complete decision, review, correction, and validation history. | A high-risk workflow migration needs durable traceability without making chat the source of truth. | Repository lifecycle contract | 68 formal reviews; 104 resolved findings |

No unrelated feature or service was added.
The large line count is dominated by the new engine and tests plus the durable review trail accumulated across proposal, specification, architecture, planning, test-specification, and six implementation milestones.

## Tests added or changed

The [test specification](../../../specs/single-bounded-review-fix-workflow-automation.test.md) defines 30 traceable cases:

| Test family | Test IDs | What it proves | Test level rationale |
| --- | --- | --- | --- |
| State and policy closure | T1-T4, T7-T8 | One writable mechanism, closed vocabularies, complete immutable policies, compatible occurrences, and bounded executable authority. | Unit tests isolate malformed records and policy drift before orchestration. |
| Target and position | T5-T6, T9 | Repeated targets bind once, plan ownership is respected, and a verify target is not future verification consent. | Integration tests need artifacts, plan state, and persisted targets together. |
| Review and correction | T10-T13 | Review outcomes are exhaustive, clean gates are distinct, direct reviews remain isolated, and correction ownership stays stage-specific. | Integration tests exercise review records, capabilities, budgets, and routing. |
| Transaction safety | T14-T16, T23, T29-T30 | Mutation follows a prepared receipt, recovery is evidence-first, cancellation reconciles, the writer is atomic, and reruns are deterministic. | Integration and end-to-end tests cover file persistence and composed interruption paths. |
| Implementation and verification | T17-T18, T28 | Milestones execute in plan order, final holistic closeout gates verification, and success stops before PR. | End-to-end coverage is required because several stage-owned artifacts interact. |
| Migration and compatibility | T19-T21 | Legacy state is dual-read/single-write, aliases preserve meaning, and cross-spec precedence is exact. | Integration and unit tests combine legacy fixtures with static contract validation. |
| Reporting, activation, and conditional routing | T22, T24-T26 | Status is read-only and complete, pre-cutover code stays non-public, M6 activates atomically, and conditional architecture routing is deterministic. | Integration plus smoke tests cover public visibility and cutover boundaries. |
| Security boundary | T27 | External actions and secret-bearing or machine-local evidence remain excluded. | Bounded manual inspection complements schema and behavioral tests. |

Production changes were generally preceded by focused failing regressions recorded in the active plan.
Each milestone then ran its focused suite, affected repository validators, selected CI checks, and the required broad smoke before review closure.

## Validation evidence available before final verify

The following evidence was produced during implementation and the final holistic review:

| Validation | Result |
| --- | --- |
| `python scripts/test-workflow-automation.py` | 73 engine tests passed |
| `python scripts/test-workflow-automation-state.py` | 60 state and recovery tests passed |
| `python scripts/test-workflow-code-state.py` | 12 Git code-state tests passed |
| `python scripts/test-validate-workflow-automation.py` | 68 automation-validator tests passed |
| `python scripts/test-workflow-automation-policy.py` | Complete policy projection suite passed in milestone proof |
| `python scripts/test-select-validation.py` | 133 selector regressions passed |
| `python scripts/test-skill-validator.py` | 259 skill-contract regressions passed in M6 proof |
| `python scripts/test-artifact-lifecycle-validator.py` | 156 lifecycle regressions passed in M6 proof |
| `python scripts/test-review-artifact-validator.py` | 104 review-artifact regressions passed in M6 proof |
| `python scripts/test-change-metadata-validator.py` | 53 metadata regressions passed in M6 proof |
| `python scripts/test-query-change-record.py` | 22 query regressions passed in M6 proof |
| `python scripts/test-adapter-distribution.py` | 131 adapter-distribution regressions passed in M6 proof |
| Explicit selector audit over all ten automation source/test paths | Every path selected exactly the same five automation checks with no registration debt |
| `bash scripts/ci.sh --mode explicit --path scripts/workflow_code_state.py --path scripts/test-workflow-code-state.py` | Five workflow-automation checks passed |
| `bash scripts/ci.sh --mode broad-smoke` | Twelve checks passed in 242 seconds after the final code-state routing fix |
| Selected CI for this explanation, change metadata, active plan, and plan index | Lifecycle, 53 metadata regressions, metadata validation, guide-system, documentation-prose audit, and broad smoke passed; broad smoke took 417.19 seconds |

Lifecycle, metadata, review-structure, review-closeout, guide-system, compilation, and whitespace validation also passed at the final review handoff.
Lifecycle validation retained one pre-existing non-blocking merge-language warning in `review-resolution.md`.

This is pre-verify evidence, not a final verification result.
Hosted CI has not been observed from this environment, and final `verify` has not run.

## Review resolution summary

The [review-resolution record](review-resolution.md) is closed:

- 68 formal reviews are recorded across proposal, specification, architecture, plan, test specification, six implementation milestones, and final holistic review;
- all 104 material findings have disposition `accepted` and status `resolved`;
- no open finding or `needs-decision` disposition remains;
- final holistic code-review R2 is `clean-with-notes`.

The reviews materially tightened canonical-position derivation, structured target identity, parent/capability separation, review outcome routing, write-ahead recovery, Git-backed final-code identity, migration behavior, and selected-CI completeness.
They did not reopen the accepted single-mechanism direction.

## Alternatives rejected

- Keep the three writable mechanisms.
  This preserved duplicated state and inconsistent resume behavior.
- Put a shared dispatcher in front of the existing engines.
  This standardized syntax but not authority, persistence, or recovery.
- Build a fully declarative workflow graph immediately.
  This introduced a second policy language before the common stage model had stabilized.
- Treat one early request as continuous proposal-to-verify authority.
  This collapsed destination into consent and crossed authoring, implementation, and verification risk boundaries.
- Remove legacy aliases immediately.
  This would break active historical workflows; the accepted migration keeps them as read-only adapters until a separately approved removal.

## Scope control

- PR creation, push, publication, release, deployment, merge, and destructive Git operations remain outside automatic authority.
- The mechanism does not replace stage-owning skills, formal review records, the active plan, or verification evidence.
- `workflow.automation` records observed identities and transition evidence; it is not a second `next_stage` cursor.
- Historical legacy records remain readable and are not rewritten merely by status inspection.
- The first version uses an immutable Python policy projection rather than adding a second hand-authored YAML or JSON registry.
- No new service, database, background worker, network dependency, or deployment surface was introduced.
- Compatibility removal, new external-action authority, and a general workflow DSL require separate approved changes.

## Risks and follow-ups

- Final `verify` must still establish current branch, artifact, test, and release-readiness coherence after this explanation is added.
- Hosted CI remains unobserved and must not be inferred from local validation.
- The migration window stays open until a repository audit proves that no active legacy state remains; alias removal requires its own compatibility change.
- Stage-policy additions must update the approved specification, immutable projection, conformance tests, and selector coverage together.
- Recovery and verification depend on exact artifact and Git identities; ambiguous or stale evidence is intentionally a pause, not an automatic repair.
- The existing non-blocking lifecycle merge-language warning should be cleaned up separately if it becomes touched or starts obscuring new diagnostics.

## Readiness

The implementation and all required code reviews are complete, review resolution is closed, and this durable explanation is now present.
The active plan remains `active`; its next stage is `verify`.

This direct `explain-change` invocation is isolated, so final verification was not run and PR readiness is not claimed.
