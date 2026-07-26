# Boundary-First Proof Modeling for Published Lifecycle Skills

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Change ID: 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
- Start date: 2026-07-25
- Last updated: 2026-07-26
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved boundary-model v1 contract so examples remain useful
without becoming the completeness model.
The implementation must move omitted-boundary detection before code review,
preserve the behavior of eight published lifecycle skills, and establish one
portable, computed capability baseline before progressive-disclosure work
resumes.

## Source artifacts

- Proposal: `docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md`
- Specs: `specs/rigorloop-workflow.md` R28-R28z and `specs/skill-contract.md` R56-R56q
- Spec review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r2.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260725-boundary-first-proof-modeling.md`
- Architecture review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r2.md`
- Test specs: `specs/rigorloop-workflow.test.md` R28-R28z and `specs/skill-contract.test.md` R56-R56q

## Context and orientation

The approved specs remain normative.
`scripts/boundary_proof_model.py` will be their immutable typed projection and
pure aggregate evaluator.
`scripts/validate-boundary-proof.py` will be the sole capability-report writer.
The first release governs exactly:

```text
spec
spec-review
test-spec
test-spec-review
implement
code-review
verify
workflow
```

Each skill will map a byte-identical
`references/boundary-proof-model.md` resource copied from
`templates/shared/boundary-proof-model.md`.
Existing adapter generation and resource-integrity validation must carry that
resource through generated, packed, and installed outputs.

## Non-goals

- Do not add a lifecycle stage or a universal per-change boundary artifact.
- Do not update the other six lifecycle skills in this slice.
- Do not let executable constants override approved spec semantics.
- Do not make structural validators judge semantic adequacy.
- Do not resume capability-preserving progressive disclosure.
- Do not activate a release or perform publication, PR, or deployment actions.

## Requirements covered

| Requirement set | Implementation milestone |
| --- | --- |
| R28-R28e, R28k, R28p-R28w | M1 typed projection and structural validation |
| R28x-R28y, R56m, R56o-R56p | M1 fixtures, aggregate evaluation, and report serialization |
| R56-R56e, R56j-R56k | M2 authoring and proof-planning skills |
| R28f-R28j, R56f-R56i, R56l | M3 implementation, review, verify, and workflow skills |
| R28l-R28o, R28z, R56n, R56q | M4 selector, adapter parity, baseline, activation, and rollback proof |

## Current Handoff Summary

- Current milestone: M1. Typed model, validator, fixtures, and report core
- Current milestone state: resolution-needed
- Latest review evidence: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r4.md
- Review status: approved; stage=architecture-review; round=r4
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: plan revision
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — review-state=open; open-count=7; open-findings=BFP-M1-CR1,BFP-M1-CR2,BFP-M1-CR3,BFP-M1-CR4,BFP-M1-CR5,BFP-M1-CR6,BFP-M1-CR7

## Milestones

### M1. Typed model, validator, fixtures, and report core

- Milestone state: resolution-needed
- Goal: Establish the closed executable projection and fail-closed proof engine before changing published skill behavior.
- Requirements: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p
- Files/components likely touched:
  - `scripts/boundary_proof_model.py`
  - `scripts/validate-boundary-proof.py`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/`
- Dependencies:
  - Approved specs and accepted ADR
  - Active matching test specs
- Tests to add/update:
  - Closed-value, exact-field, ID-grammar, uniqueness, reference, version, and scope regressions
  - All eight frozen incident IDs and one compact simple-change fixture
  - Pass, fail, not-run, stale, asserted, duplicate, orphan, and aggregate-result cases
- Implementation steps:
  - Write failing tests for the typed record schemas and unknown-value behavior.
  - Implement immutable enums/dataclasses, parsers, and pure aggregation.
  - Implement structural validation and exclusive report serialization.
  - Add positive, negative, incident, and overhead fixtures.
- Validation commands:
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py --help`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: The engine rejects incomplete or unknown boundary records and computes, but does not assert, the canonical capability result.
- Commit message: `M1: add boundary proof model and validator core`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Parser code could become a second normative contract or accept unknown values through fall-through.
- Rollback/recovery:
  - Revert the new isolated scripts and fixtures; no published skill or release surface depends on them before M2-M4.

### M2. Authoring and proof-planning skill projection

- Milestone state: planned
- Goal: Make boundary classification and proof mapping explicit in the four upstream public skills while keeping stable detail loadable on demand.
- Requirements: R56-R56e, R56j-R56k; R28-R28g
- Files/components likely touched:
  - `templates/shared/boundary-proof-model.md`
  - `skills/spec/`
  - `skills/spec-review/`
  - `skills/test-spec/`
  - `skills/test-spec-review/`
  - `tests/fixtures/skills/boundary-proof/`
- Dependencies:
  - M1 closed
- Tests to add/update:
  - Resource-map, raw-byte-copy, trigger, stop, claim, and handoff tests
  - Example-only spec and test-spec rejection fixtures
  - Behavior-preservation fixtures for all four skills
- Implementation steps:
  - Write the reviewed shared reference from the approved record grammar.
  - Map identical skill-local copies in the four skill packages.
  - Add compact stage-owned instructions without moving normative behavior into the reference.
  - Prove semantic responsibilities and prior behavior remain visible.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
- Expected observable result: The four upstream skills require complete boundary and proof maps while loading detailed stable structure only when applicable.
- Commit message: `M2: project boundary proof into authoring skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Shared reference use could hide stage-specific stop or claim boundaries.
- Rollback/recovery:
  - Revert the four skill edits and mapped copies as one unit while retaining the isolated M1 engine.

### M3. Implementation, review, verification, and routing projection

- Milestone state: planned
- Goal: Carry boundary proof through implementation, independent review, final verification, and workflow routing.
- Requirements: R28f-R28j; R56f-R56i, R56l
- Files/components likely touched:
  - `skills/implement/`
  - `skills/code-review/`
  - `skills/verify/`
  - `skills/workflow/`
  - `tests/fixtures/skills/boundary-proof/`
- Dependencies:
  - M1 and M2 closed
- Tests to add/update:
  - Proof-before-change, sibling-remediation, public-path composition, stale-evidence, and pause behavior
  - Behavior-preservation fixtures for the remaining four skills
  - Cross-stage version and handoff parity
- Implementation steps:
  - Add mapped copies of the shared reference.
  - Add stage-local triggers, sibling analysis, independence, verification, and pause rules.
  - Extend fixtures to prove examples cannot substitute for boundary coverage.
  - Confirm workflow routing adds no new stage or automatic authority.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
- Expected observable result: The full eight-skill chain preserves prior capabilities and stops on missing, stale, partial, or example-only boundary evidence.
- Commit message: `M3: enforce boundary proof across delivery skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Workflow guidance could accidentally claim authority or duplicate reviewer judgment.
- Rollback/recovery:
  - Revert M3 skill projections together; keep M1-M2 inactive and do not claim a complete baseline.

### M4. Selection, adapter parity, capability baseline, and activation proof

- Milestone state: planned
- Goal: Make the complete boundary capability selectable, portable, measurable, and release-safe without activating or publishing it.
- Requirements: R28l-R28o, R28z; R56n, R56q
- Files/components likely touched:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - adapter generation and validation tests
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
  - release validation tests and fixtures
- Dependencies:
  - M1-M3 closed
- Tests to add/update:
  - Exact routing for the six boundary check IDs
  - Canonical/generated/packed/installed raw-byte parity
  - Report provenance, required-order aggregation, hash mismatch, partial activation, and rollback
  - No-new-universal-artifact and simple-fixture overhead assertions
- Implementation steps:
  - Register exact affected paths and checks in the selector.
  - Extend existing generation and resource-integrity proof for all supported adapters.
  - Generate the canonical capability-baseline report from actual evidence.
  - Add release-note activation validation without writing an activation marker in this non-release change.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
- Expected observable result: A passing, provenance-bound R28y report proves the eight-skill implementation checks across canonical and distributed surfaces. It does not by itself satisfy the later R28o review-resolution and verification predicate, and release activation remains a later release action.
- Commit message: `M4: prove portable boundary capability baseline`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Adapter or report evidence could be stale, asserted, or coupled to a working-tree-only path.
- Rollback/recovery:
  - Remove selector and activation checks, regenerate adapters from the last known good canonical skills, and retain the report only as failed historical evidence.

## Validation plan

- `python scripts/test-boundary-proof.py`: focused typed-model, parser, fixture, and aggregate proof.
- `python scripts/validate-skills.py`: canonical skill structure and mapped-resource contract.
- `python scripts/test-skill-validator.py`: public-skill regressions, including unknown values.
- `python scripts/build-skills.py --check`: generated local mirror parity.
- `python scripts/test-select-validation.py`: exact changed-path and check-ID routing.
- `python scripts/test-adapter-distribution.py`: generated, packed, and installed adapter parity.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`: active generated adapter archive and resource parity.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: formal-review closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml`: lifecycle metadata consistency.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md --path specs/rigorloop-workflow.md --path specs/skill-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260725-boundary-first-proof-modeling.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md`: exact touched lifecycle artifact state.
- `bash scripts/ci.sh --mode explicit ...`: selected integration proof after focused suites.
- `git diff --check`: whitespace and patch integrity.

The matching test specs must replace the ellipsis above with exact paths before
implementation authorization is requested.

## Risks and recovery

- Risk: Structural checks may be mistaken for semantic completeness.
  - Recovery: Keep semantic applicability and proof adequacy in formal reviews and reject any validator claim beyond exact structure and aggregation.
- Risk: Eight copied references may drift.
  - Recovery: Treat the shared template as copy source and require raw-byte equality across every canonical and distributed copy.
- Risk: The first slice could expand to all lifecycle skills.
  - Recovery: Fail review when a changed skill is outside the closed eight-skill list unless a separate approved slice exists.
- Risk: Capability reporting could become a new universal artifact.
  - Recovery: Keep the report path fixed to this initiative and reject generic scaffolding or schema registration.
- Risk: Release activation could be claimed from branch-local evidence.
  - Recovery: Validate activation only in tracked release notes against an actual release tag and report byte identity.

## Dependencies

- Plan-review approval before test-spec authoring.
- Matching test-spec amendments and clean test-spec review before implementation.
- M1 before any published-skill dependency on the model.
- M2 before M3 so downstream skills consume a stable upstream record contract.
- M1-M3 before M4 computes capability outcomes.
- M4 writes the R28y report from implementation evidence; its code review then closes the implementation milestone without recursively rewriting the report to cite its own review.
- R28o remains unsatisfied until all milestone reviews and the final holistic code review are clean, review resolution is closed, explain-change is current, and final verification passes.
- Separate implementation authorization before M1.
- Separate verification authorization only after implementation closeout and final review evidence exist.

## Progress

- 2026-07-25: Plan created after spec-review R2 and architecture-review R2 approval.
- 2026-07-25: Plan-review R2 approved the corrected four-milestone sequence.
- 2026-07-25: Matching workflow and skill-contract test specs were amended with v1 proof maps, fixtures, commands, and milestone gates.
- 2026-07-26: M1 added the immutable typed model, deterministic validator CLI, frozen incident registry, compact simple-change fixture, and synthetic capability aggregation proof.
- 2026-07-26: M1 code-review R1 recorded seven findings; BFP-M1-CR4, BFP-M1-CR6, and BFP-M1-CR7 require owner decisions before correction.
- 2026-07-26: The user authorized the recommended contract-first resolution; the workflow and skill specs now define identity-bound evidence, boundary-state incident replay, and computed simple-change traces pending spec-review R3.
- 2026-07-26: Spec-review R3 requested exact incident rules, trace formulas, and operation-bound evidence receipts before M1 correction.
- 2026-07-26: The R4 candidate freezes incident derivation, operation-bound evidence receipts, a closed stage-event grammar, and deterministic simple-change metrics.
- 2026-07-26: Spec-review R4 retained the R3 findings and required fresh operation recomputation plus phase-appropriate workflow proof.
- 2026-07-26: The R5 candidate replaces caller-authored receipts with fresh closed-registry execution, makes incident triggers unique, and phases real skill behavior after M1's synthetic engine proof.
- 2026-07-26: Spec-review R5 resolved incident derivation and retained only snapshot/trace closure and operation-registry projection.
- 2026-07-26: The R6 candidate closes the operation-to-report registry, input/output provenance, preservation and adapter manifests, behavior-output capture, snapshot/event cardinality, structural/result consistency, and reproducible artifact-inventory formulas.
- 2026-07-26: Spec-review R6 retained BFP-SR3-2 and BFP-SR3-3 for oracle/input/output separation, complete workspace inventory, historical and typed-result identity, aggregate observation projection, marker-absence selection, and frozen fixture paths.
- 2026-07-26: The R7 candidate makes candidates oracle-only, closes stage input cardinality and terminal branches, inventories the behavior artifact tree with a closed classifier, materializes historical evidence, identity-binds typed results and dependencies, and losslessly projects aggregate observations.
- 2026-07-26: Spec-review R7 retained BFP-SR3-2 and BFP-SR3-3 for oracle-label independence, exact normalized assertions, complete formal-review output bundles, pre-run HEAD authority, canonical manifest paths, and normalized result identities.
- 2026-07-26: The R8 candidate makes scenario labels comparison-only, closes normalized oracle records, bundles complete formal review evidence, derives simple-run HEAD and pre-M2 preservation baselines separately, freezes support-manifest paths and schemas, and normalizes typed-result identities.
- 2026-07-26: Spec-review R8 retained only review-event evidence-union, portable immutable-run publication, and filesystem-versus-typed selector separation gaps.
- 2026-07-26: The R9 candidate defines authoring and review evidence sets separately, counts complete review bundles, publishes immutable runs through one atomically replaced pointer, and separates filesystem input references from typed-result dependencies.
- 2026-07-26: Spec-review R9 resolved BFP-SR3-2 and BFP-SR3-3 and opened BFP-SR9-1 because generation and validation still reran nondeterministic skill invocations and stale pointer reuse was not input-bound.
- 2026-07-26: The R10 candidate separates one-shot behavior generation from deterministic recorded-run validation, binds immutable evidence to an exact current input set, and reconciles prepared publication without repeating skills or accepting stale pointers.
- 2026-07-26: Spec-review R10 retained BFP-SR9-1 only for immutable prior-pointer history and complete behavior-harness/orchestration implementation identity.
- 2026-07-26: The R11 candidate stores the prior pointer as immutable inline history and binds every behavior-affecting workflow, harness, capture, serialization, evaluation, contract, and runtime input through one closed implementation manifest.
- 2026-07-26: Spec-review R11 retained BFP-SR9-1 because the manual component list omitted transitive workflow imports, governing instructions, and exact environment derivation.
- 2026-07-26: The R12 candidate replaces the manual component list with a validated transitive import/resource/instruction closure, runs against an allowlisted read view, and derives normalized non-secret execution-environment fields from authoritative runtime sources.
- 2026-07-26: Spec-review R12 retained BFP-SR9-1 because that transitive closure omitted participating resources and runtime instructions and could not deterministically model dynamic imports or the observable runtime boundary.
- 2026-07-26: The R13 candidate replaces the open-ended transitive closure with a standalone hermetic behavior harness, a closed two-module import policy, complete five-skill resource-map binding, applicable instruction discovery, and an observable runtime/model/tool invocation profile.
- 2026-07-26: Spec-review R13 approved the revised contract with no new findings and resolved BFP-SR9-1; architecture amendment is required before test-spec revision or implementation.
- 2026-07-26: The architecture R3 candidate assigns the standalone harness, five-skill package assembly, isolated child runtime, observable invocation attestation, transient access enforcement, and prepared-receipt immutable publication to explicit components and updates the ADR and C4 views.
- 2026-07-26: Architecture-review R3 requested the exact R28y publication order, trusted parent/runtime enforcement with opaque control-plane authentication, and durable ADR rationale for the hermetic design.
- 2026-07-26: The R4 candidate corrects publication to validated run installation, fsynced receipt, atomic pointer replacement, parent fsync, and receipt cleanup; assigns confinement to parent-attested runtime sandboxing; keeps credentials in a private runtime-only channel; and records rejected alternatives and operating costs.
- 2026-07-26: Architecture-review R4 approved the hermetic child-runtime boundary, exact publication recovery, ADR tradeoffs, and C4 views; plan revision must start with runtime feasibility proof.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-25 | Use four implementation milestones ordered engine, upstream skills, downstream skills, distribution evidence. | Each slice has an independently reviewable contract and a safe rollback boundary. | One large milestone; skill edits before the proof engine; adapter work before canonical behavior settles. |
| 2026-07-25 | Keep release activation validation in M4 but perform no activation or publication. | The spec requires activation semantics, while external release actions remain outside this change and automation authority. | Omitting activation tests; writing a premature activation marker. |
| 2026-07-26 | Use frozen dataclasses plus pure mapping validators and JSON fixture inputs for M1. | The executable projection remains dependency-free, immutable, deterministic, and separate from Markdown serialization or semantic review. | A second YAML registry; validator-owned semantic scoring; mutable global records. |

## Surprises and discoveries

- The unified automation state adapter writes `run.pause_reason`, while the
  change-metadata schema currently accepts `run.stop_reason`. The run was
  normalized through the sole state writer. This pre-existing harness mismatch
  is outside the boundary-proof implementation scope and requires a focused
  workflow-automation bugfix before the next release.
- M1 aligned-surface audit: selector registration, public skills, shared
  references, adapters, release notes, and the canonical capability report are
  intentionally unaffected because M2-M4 own those surfaces.

## Validation notes

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-07-25-boundary-first-proof-modeling.md` passed after R1 corrections, with unrelated existing workflow-spec lifecycle-language warnings.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml` passed after R1 corrections.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` passed after R1 recording.
- `python scripts/test-boundary-proof.py` passed 12 tests covering closed values, exact fields, version parity, traceability, fixtures, aggregation, evidence, and sole-writer serialization.
- `python scripts/validate-boundary-proof.py --help` passed.
- `python -m py_compile scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` passed.
- `python scripts/test-artifact-lifecycle-validator.py` passed 156 tests.

## Outcome and retrospective

- Pending implementation, milestone reviews, the R28y capability report, final holistic code review, closed review resolution, explain-change, and final verification.
- Progressive-disclosure proposal review remains paused until the complete R28o predicate passes; a passing report alone is insufficient.

## Readiness

- See `Current Handoff Summary`.
- Readiness is not implementation completion or final closeout.
