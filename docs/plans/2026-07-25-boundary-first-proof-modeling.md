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
- Spec review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r13.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260725-boundary-first-proof-modeling.md`
- Architecture review: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r4.md`
- Test specs: `specs/rigorloop-workflow.test.md` R28-R28z and `specs/skill-contract.test.md` R56-R56q; revision required after plan-review R3

## Context and orientation

The approved specs remain normative.
`scripts/boundary_proof_model.py` will be their immutable typed projection and
pure aggregate evaluator.
`scripts/boundary_proof_behavior.py` will be the standalone hermetic behavior
harness and immutable-run publisher; it is not a workflow-automation engine.
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
| R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p | M1 runtime feasibility plus typed projection, structural validation, fixtures, trace, and report correction |
| R28y, R56p | M2 standalone hermetic behavior harness and immutable publication/recovery |
| R56-R56e, R56j-R56k | M3 authoring and proof-planning skills plus canonical upstream behavior run |
| R28f-R28j, R56f-R56i, R56l | M4 implementation, review, verify, and workflow skills |
| R28l-R28o, R28z, R56n, R56q | M5 selector, adapter parity, baseline, activation, and rollback proof |

## Current Handoff Summary

- Current milestone: M1. Runtime feasibility and deterministic core correction
- Current milestone state: resolution-needed
- Latest review evidence: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/plan-review-r3.md
- Review status: changes-requested; stage=plan-review; round=r3
- Remaining in-scope implementation milestones: M1, M2, M3, M4, M5
- Next stage: plan revision
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: lifecycle-gates-open, implementation-milestones-open, review-findings-open, explain-change-pending, verify-pending, pr-handoff-pending — review-state=open; open-count=9; open-findings=BFP-M1-CR1,BFP-M1-CR2,BFP-M1-CR3,BFP-M1-CR4,BFP-M1-CR5,BFP-M1-CR6,BFP-M1-CR7,BFP-PL4,BFP-PL5

## Milestones

### M1. Runtime feasibility and deterministic core correction

- Milestone state: resolution-needed
- Goal: Prove that the selected runtime can enforce the approved hermetic profile, then close every M1 code-review finding in the deterministic model, fixtures, trace, and report engine before building the full behavior harness.
- Requirements: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p
- Files/components likely touched:
  - `scripts/boundary_proof_behavior.py`
  - `scripts/boundary_proof_model.py`
  - `scripts/validate-boundary-proof.py`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/`
  - `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/validation-m1.md`
- Dependencies:
  - Approved R13 specs, accepted R4 architecture/ADR, and revised active test specs
- Tests to add/update:
  - Runtime supported/unsupported version, missing profile attestation, wrong effective sandbox, unavailable or unsafe model metadata, credential leakage, and secret-free evidence cases
  - Stable and unique regression/discovery IDs plus exact requirement ownership for each proof reference
  - Exact eight-row incident ID, seeded-omission, and gate registry mutation cases
  - Complete marker/scope presence and parity matrix, including fully markerless grandfathering and contradictory partial state
  - Missing, unsafe, non-regular, stale, substituted, and wrong-kind evidence references plus exact not-run blockers
  - Canonical byte serialization across semantically equivalent mapping permutations
  - Eight executable boundary-state incident fixtures with detected stage, diagnostic, code-review escape, and sibling-bypass results
  - Synthetic four-stage simple-change trace with derived applicable-only proof map, artifact count, false blocking, and correction cycles
- Implementation steps:
  - First implement a read-only `check-environment` path that resolves the exact Codex executable, records bounded version and executable identity, obtains runtime-owned model metadata, verifies the effective runtime-native sandbox/profile from parent-observed evidence, and proves that the private runtime home is outside child-readable roots.
  - Run the real feasibility check and record only non-secret bounded results. If any required enforcement or credential-isolation property is unavailable, stop M1 and route back to architecture; do not emulate or weaken the profile.
  - Add failing tests for BFP-M1-CR1 through BFP-M1-CR7 before correcting production behavior.
  - Enforce the complete closed ID/ownership, incident registry, marker parity, evidence identity/blocker, canonical serialization, incident replay, and synthetic trace contracts.
  - Keep M1 behavior proof synthetic: do not invoke lifecycle skills or claim published-skill preservation.
- Validation commands:
  - `python scripts/boundary_proof_behavior.py check-environment --json`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py --help`
  - `python -m py_compile scripts/boundary_proof_behavior.py scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
- Expected observable result: Runtime feasibility is proven without exposing credentials; every R1 adversarial probe fails closed; the deterministic engine computes synthetic results without asserting published behavior.
- Commit message: `M1: close boundary core findings and prove runtime feasibility`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Current Codex runtime may not expose verifiable effective-profile or credential-isolation evidence.
  - Parser correction could still compress multi-property requirements or accept unknown values through fall-through.
- Rollback/recovery:
  - If feasibility fails, retain the failed non-secret evidence, stop, and revise architecture rather than adding a weaker fallback.
  - Revert the M1 script/fixture correction as one unit; no published skill depends on it before M3.

### M2. Standalone hermetic behavior harness

- Milestone state: planned
- Goal: Implement one standalone, identity-bound workflow behavior invocation and deterministic immutable-run validation/recovery without importing the workflow-automation engine.
- Requirements: R28y, R56p
- Files/components likely touched:
  - `scripts/boundary_proof_behavior.py`
  - `scripts/boundary_proof_model.py`
  - `scripts/validate-boundary-proof.py`
  - `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/behavior/`
- Dependencies:
  - M1 closed
- Tests to add/update:
  - Sole allowed repository import plus relative, wildcard, third-party, other local, and dynamic-import rejections
  - Complete five-skill resource-map set; missing, extra, stale, escaping, non-regular, and unmapped resource contrasts
  - Root and nested applicable/inapplicable `AGENTS.md` discovery
  - Harness prompt identity from module constant plus scenario identity
  - Runtime executable/version/model/instruction/tool/Python identity mismatch, unavailable, and unsafe cases
  - Caller-supplied instruction, unexpected tool, connector, subagent, network, and unmanifested read rejection
  - Validation under a different validator environment without profile replacement
  - Crash points before run install, after run install, after receipt fsync, after pointer replace, after parent fsync, and before receipt removal
  - Later commits with unchanged referenced bytes versus changed referenced bytes
- Implementation steps:
  - Freeze the two-module AST import policy and exact manifest/input-set schemas.
  - Assemble the five skill packages, applicable instructions, contracts, scenario, and candidates into a fresh isolated workspace.
  - Launch the identified runtime through the M1-proven sandbox and private runtime home; capture only bounded parent-observed attestation and typed event output.
  - Build and validate the sibling temporary run; install the immutable run; fsync the receipt; replace/fsync the pointer; fsync the parent; reconcile; remove the receipt.
  - Implement validation-only reuse that never invokes a lifecycle skill and never substitutes validation-time environment data.
  - Exercise the full pipeline with controlled fixture packages; do not yet publish the canonical four-stage behavior result.
- Validation commands:
  - `python scripts/boundary_proof_behavior.py check-environment --json`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py --help`
  - `python -m py_compile scripts/boundary_proof_behavior.py scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py`
- Expected observable result: Controlled fixture runs publish and recover one input-bound immutable run; deterministic validation detects every stale or substituted input without reinvocation.
- Commit message: `M2: add hermetic boundary behavior harness`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Nondeterministic runtime output or crash recovery could make tests flaky or repeat work.
  - Sandbox attestation could be accidentally treated as child self-report.
- Rollback/recovery:
  - Remove M2 run evidence and revert the standalone harness flow while retaining the proven M1 preflight and deterministic engine.

### M3. Authoring and proof-planning skill projection

- Milestone state: planned
- Goal: Make boundary classification and proof mapping explicit in the four upstream public skills and generate the first canonical simple-change behavior run.
- Requirements: R56-R56e, R56j-R56k; R28-R28g, R28y
- Files/components likely touched:
  - `skills/workflow/`
  - `templates/shared/boundary-proof-model.md`
  - `skills/spec/`
  - `skills/spec-review/`
  - `skills/test-spec/`
  - `skills/test-spec-review/`
  - `tests/fixtures/skills/boundary-proof/`
  - change-local immutable simple-change behavior evidence
- Dependencies:
  - M1 and M2 closed
- Tests to add/update:
  - Resource-map, raw-byte-copy, trigger, stop, claim, handoff, complete review-bundle, and isolation tests
  - Example-only spec/test-spec rejection and valid compact simple-change cases
  - Behavior-preservation fixtures for all four stage skills and workflow orchestration
  - Canonical generation followed by validation-only reuse
- Implementation steps:
  - Write the reviewed shared reference from the approved record grammar.
  - Map identical skill-local copies in the five participating skill packages.
  - Add compact stage-owned instructions without moving normative behavior into the reference.
  - Generate the real `spec -> spec-review -> test-spec -> test-spec-review` run through one `workflow` invocation.
  - Validate the current pointer, trace, bundles, metrics, input identities, and zero unmanifested inputs without reinvoking skills.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/boundary_proof_behavior.py generate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --scenario tests/fixtures/boundary-proof/simple-change/scenario.json`
  - `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`
- Expected observable result: The upstream skills require complete boundary/proof maps, preserve their stage claims, and produce one current immutable simple-change run with zero false blocking and no new universal artifact.
- Commit message: `M3: project and prove upstream boundary behavior`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Shared reference use could hide stage-specific stop or claim boundaries.
  - The workflow skill could become a second normative owner or broaden automatic authority.
- Rollback/recovery:
  - Revert the five package edits and canonical pointer together; retain historical immutable failed runs only as non-current evidence.

### M4. Implementation, review, verification, and routing projection

- Milestone state: planned
- Goal: Carry boundary proof through implementation, independent review, final verification, and workflow routing while preserving prior behavior.
- Requirements: R28f-R28j; R56f-R56i, R56l
- Files/components likely touched:
  - `skills/implement/`
  - `skills/code-review/`
  - `skills/verify/`
  - `skills/workflow/`
  - `tests/fixtures/skills/boundary-proof/`
  - change-local preservation manifests and snapshots
- Dependencies:
  - M1-M3 closed
- Tests to add/update:
  - Proof-before-change, sibling-remediation, public-path composition, stale-evidence, and pause behavior
  - Behavior, claim-boundary, review-recording, isolation, and handoff preservation for all eight skills
  - Cross-stage version, scope, and handoff parity
- Implementation steps:
  - Add mapped copies of the shared reference to the remaining skills.
  - Add stage-local proof, sibling analysis, independence, verification, and pause rules.
  - Materialize before snapshots from the frozen pre-M3 baseline and current after artifacts.
  - Evaluate all five preservation categories without rerunning the upstream simple-change workflow.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-boundary-proof.py`
- Expected observable result: The full eight-skill chain preserves behavior and stops on missing, stale, partial, or example-only boundary evidence.
- Commit message: `M4: enforce boundary proof across delivery skills`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Workflow guidance could claim authority or duplicate reviewer judgment.
  - Historical snapshot materialization could cite stale Git bytes instead of current evidence.
- Rollback/recovery:
  - Revert M4 skill projections and after evidence together; retain M1-M3 without claiming the complete baseline.

### M5. Selection, adapter parity, capability baseline, and activation proof

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
  - M1-M4 closed
- Tests to add/update:
  - Exact routing for the six boundary check IDs
  - Canonical/generated/packed/installed raw-byte parity
  - Report provenance, required-order aggregation, hash mismatch, partial activation, and rollback
  - No-new-universal-artifact and simple-fixture overhead assertions
- Implementation steps:
  - Register exact affected paths and checks in the selector.
  - Extend existing generation and resource-integrity proof for all supported adapters.
  - Generate the canonical capability-baseline report from current immutable and preservation evidence.
  - Add release-note activation validation without writing an activation marker in this non-release change.
- Validation commands:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-adapter-distribution.py`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/test-boundary-proof.py`
  - `python scripts/validate-boundary-proof.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md`
- Expected observable result: A passing, provenance-bound R28y report proves the eight-skill implementation checks across canonical and distributed surfaces. It does not by itself satisfy R28o, and release activation remains a later release action.
- Commit message: `M5: prove portable boundary capability baseline`
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
- `python scripts/boundary_proof_behavior.py check-environment --json`: live, non-secret runtime sandbox/profile and credential-isolation feasibility proof.
- `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: deterministic current immutable-run validation without lifecycle reinvocation.
- `python scripts/validate-skills.py`: canonical skill structure and mapped-resource contract.
- `python scripts/test-skill-validator.py`: public-skill regressions, including unknown values.
- `python scripts/build-skills.py --check`: generated local mirror parity.
- `python scripts/test-select-validation.py`: exact changed-path and check-ID routing.
- `python scripts/test-adapter-distribution.py`: generated, packed, and installed adapter parity.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`: active generated adapter archive and resource parity.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills`: formal-review closeout.
- `python scripts/validate-change-metadata.py docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml`: lifecycle metadata consistency.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills.md --path specs/rigorloop-workflow.md --path specs/skill-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260725-boundary-first-proof-modeling.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md`: exact touched lifecycle artifact state.
- `bash scripts/ci.sh --mode explicit --path scripts/boundary_proof_behavior.py --path scripts/boundary_proof_model.py --path scripts/validate-boundary-proof.py --path scripts/test-boundary-proof.py --path tests/fixtures/boundary-proof/incident-registry.json --path tests/fixtures/boundary-proof/simple-change.json --path templates/shared/boundary-proof-model.md --path skills/spec/SKILL.md --path skills/spec-review/SKILL.md --path skills/test-spec/SKILL.md --path skills/test-spec-review/SKILL.md --path skills/implement/SKILL.md --path skills/code-review/SKILL.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md`: selected integration proof after focused suites.
- `git diff --check`: whitespace and patch integrity.

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
- Risk: The selected runtime cannot prove its effective sandbox or isolate credentials from child tools.
  - Recovery: Stop at M1 with `environment-unavailable`, record bounded evidence in `validation-m1.md`, and route to architecture revision; do not add an unreviewed weaker execution mode.
- Risk: Nondeterministic generation could be mistaken for deterministic validation.
  - Recovery: Keep generation and validation commands separate; validation never invokes lifecycle skills and a stale input identity requires a new explicit generation.

## Dependencies

- Plan-review approval before test-spec authoring.
- Matching test-spec amendments and clean test-spec review before implementation.
- M1 runtime feasibility and deterministic correction before full harness work.
- M2 harness and recovery proof before any canonical published-skill behavior generation.
- M3 before M4 so downstream skills consume a stable upstream record contract and current immutable run.
- M1-M4 before M5 computes capability outcomes.
- M5 writes the R28y report from implementation evidence; its code review then closes the implementation milestone without recursively rewriting the report to cite its own review.
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
- 2026-07-26: The plan R3 candidate replaces the stale four-milestone sequence with five reviewed boundaries: runtime feasibility and core correction, standalone harness and recovery, upstream behavior generation, downstream preservation, and portable capability aggregation.
- 2026-07-26: Plan-review R3 requested restoration of normative R28y M1-M4 ownership and exact production, validation, promotion, baseline, and recovery commands.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-25 | Use four implementation milestones ordered engine, upstream skills, downstream skills, distribution evidence. | This was the approved initial sequence before the R13 hermetic behavior contract. | One large milestone; skill edits before the proof engine; adapter work before canonical behavior settles. |
| 2026-07-25 | Keep release activation validation in the final baseline milestone but perform no activation or publication. | The spec requires activation semantics, while external release actions remain outside this change and automation authority. | Omitting activation tests; writing a premature activation marker. |
| 2026-07-26 | Use frozen dataclasses plus pure mapping validators and JSON fixture inputs for M1. | The executable projection remains dependency-free, immutable, deterministic, and separate from Markdown serialization or semantic review. | A second YAML registry; validator-owned semantic scoring; mutable global records. |
| 2026-07-26 | Revise to five milestones: feasibility/core, harness, upstream behavior, downstream preservation, and distribution baseline. | The accepted R13/R4 design adds a high-risk runtime boundary and recoverable publication flow that need an independent review before public skill mutation. | Hide the harness inside upstream skill work; build the full harness before proving runtime support; keep stale four-milestone mapping. |

## Surprises and discoveries

- The unified automation state adapter writes `run.pause_reason`, while the
  change-metadata schema currently accepts `run.stop_reason`. The run was
  normalized through the sole state writer. This pre-existing harness mismatch
  is outside the boundary-proof implementation scope and requires a focused
  workflow-automation bugfix before the next release.
- M1 aligned-surface audit: selector registration, public skills, shared
  references, adapters, release notes, and the canonical capability report are
  intentionally unaffected because M3-M5 own those surfaces.

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
