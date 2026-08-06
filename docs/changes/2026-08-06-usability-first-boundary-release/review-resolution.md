# Review Resolution: Usability-First Boundary-First v0.4.0 Release

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: code-review-m1-r2

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`
- Findings resolved: 14
- Unresolved findings: 0
- Current result: All M2 R1 findings are resolved and ready for code-review M2 R2.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| UBR-M2-CR1-001 | accepted | resolved | Activation-record diagnostics are repository-relative and private-root CLI regressions pass. |
| UBR-M2-CR1-002 | accepted | resolved | Replacement refs and lazy fetch are disabled for every derivation Git read. |
| UBR-M2-CR1-003 | accepted | resolved | Rollback proof and validation bind to tracked immutable v0.3.6 metadata. |
| UBR-M2-CR1-004 | accepted | resolved | Non-string activation states return structured closed-vocabulary issues. |
| UBR-M1-CR1-001 | accepted | resolved | Each stable usability case is bound to independent required and forbidden semantics outside fixture-owned output. |
| UBR-M1-CR1-002 | accepted | resolved | Closed-vocabulary types are validated before membership and malformed values produce bounded errors. |
| UBR-SR1-001 | accepted | resolved | Exact activation fields and compatibility dispositions are present; R2 records the narrower snapshot/transition residual as UBR-SR2-001. |
| UBR-SR1-002 | accepted | resolved | The journeys now have concrete semantic oracles; R2 records the newly observed fixture-identity ambiguity as UBR-SR2-002. |
| UBR-SR1-003 | accepted | resolved | UBR-R013 owns the exact cleanup inventory and preserves ordinary validation and release steps. |
| UBR-SR2-001 | accepted | resolved | Pending and active are independently valid checked-revision snapshots, and activation preparation receives the reviewed baseline explicitly. |
| UBR-SR2-002 | accepted | resolved | The semantic journeys use existing RigorLoop validator, loader, cleanup, and release surfaces. |
| UBR-AR1-001 | accepted | resolved | The canonical package and ADR now define the exact internal callable, input, output, failure, no-write, one-time-use, and normal-validation separation contract. |
| UBR-PR1-001 | accepted | resolved | M3 now executes the release-selected CI bundle and the separate standing full gate before code review and baseline selection; M4 reruns them after activation. |
| UBR-TSR1-001 | accepted | resolved | T23 and its M2 evidence now align with CMD06; M1 retains direct UBR-R005 proof through T4. |

## Common Resolution Metadata

- Owner: spec author
- Owning stage: spec
- Validation target: revised specification plus rerun `spec-review`
- Validation evidence: spec revision R3 authoring checks and approved spec-review R3

## Finding Details

### code-review-m2-r1

#### UBR-M2-CR1-001 - Activation parse diagnostics expose the absolute root

Finding ID: UBR-M2-CR1-001
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Use the repository-relative activation path in every parse/shape issue and add sentinel-root structured and CLI regressions.
Rationale: UBR-R017 forbids machine-local paths in validation evidence.
Validation target: code-review-m2-r2
Validation evidence: Missing, malformed, and wrong-shape CLI cases report `specs/boundary-first-activation.yaml` and suppress the private sentinel root; the 61-test suite passes.
Safe resolution path: Mechanical path substitution plus negative output assertions.
Auto-fix class: mechanical

#### UBR-M2-CR1-002 - Replacement refs can substitute the derivation baseline

Finding ID: UBR-M2-CR1-002
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Disable Git replacement objects and lazy fetch for every derivation object read and prove stable output under a replacement ref.
Rationale: The explicit full commit identity must bind the real local object graph and the helper must not acquire or write objects.
Validation target: code-review-m2-r2
Validation evidence: A real replacement ref leaves the baseline inventory at `specs/alpha.md`, every Git call asserts both guard variables, and the 61-test suite passes.
Safe resolution path: Shared derivation-only Git environment plus replacement-ref and environment regressions.
Auto-fix class: declared-safe

#### UBR-M2-CR1-003 - Rollback fixture does not use tracked v0.3.6 evidence

Finding ID: UBR-M2-CR1-003
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Copy tracked version-specific metadata for the positive case and reject v0.3.5 identities relabeled as v0.3.6.
Rationale: T12 requires the exact immutable rollback authority, not a structurally valid surrogate.
Validation target: code-review-m2-r2
Validation evidence: Positive selection matches parsed tracked v0.3.6 hashes and relabeled v0.3.5 identities fail; the 61-test suite passes.
Safe resolution path: Fixture-only correction and substitution regression.
Auto-fix class: mechanical

#### UBR-M2-CR1-004 - Malformed activation state raises TypeError

Finding ID: UBR-M2-CR1-004
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Chosen action: Type-check state before membership and regress list, object, and CLI malformed values.
Rationale: Closed vocabularies must fail closed before consistency checks.
Validation target: code-review-m2-r2
Validation evidence: Unknown string, list, and object values return `BFR-UNKNOWN-ACTIVATION-STATE` through direct and CLI validation; the 61-test suite passes.
Safe resolution path: String guard plus direct malformed-value tests.
Auto-fix class: mechanical

### code-review-m1-r1

#### UBR-M1-CR1-001 - Usability journey fixture is its own semantic oracle

Finding ID: UBR-M1-CR1-001
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Add independent per-case stage, artifact, required-topic, forbidden-topic, and depth-relation expectations plus coordinated-drift regression mutations.
Rationale: Stable journey IDs must preserve the approved E1-E3 semantic oracle; fixture metadata cannot author both the behavior and its expected proof result.
Validation target: code-review-m1-r2
Validation evidence: Contract-owned E1/E2 partition and stage/artifact expectations plus coordinated-drift mutations pass in the full 285-test skill-validator suite; the complete M1 command set passes.
Safe resolution path: Keep the semantic fixture concise, but validate it against contract-owned expectations outside the mutable case rows and prove required deletion, forbidden admission, stage reassignment, and coordinated expected-output edits fail.
Auto-fix class: declared-safe

#### UBR-M1-CR1-002 - Malformed vocabulary values escape as exceptions

Finding ID: UBR-M1-CR1-002
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Add string guards before closed-vocabulary membership or semantic evaluation and regress non-string JSON values for stage, trigger, and artifact fields.
Rationale: A validation fixture must fail closed with an explicit bounded error; malformed values must not escape as interpreter exceptions.
Validation target: code-review-m1-r2
Validation evidence: Array, object, and null vocabulary mutations return validation errors without exceptions; the focused tests and full 285-test skill-validator suite pass.
Safe resolution path: Guard the three fields mechanically, skip dependent evaluation for malformed rows, and add list, object, boolean, numeric, and null mutations.
Auto-fix class: mechanical

### code-review-m1-r2

Review result: clean-with-notes
Material findings: none
Resolution required: no
Validation evidence: The independent rereview reconciled both R1 findings as resolved, accepted the contract-owned semantic oracle and fail-closed type guards, and found no new material findings.

### proposal-review-r1

Review result: approved
Material findings: none
Resolution required: no

### spec-review-r1

#### UBR-SR1-001 - Tree-local activation transition is incomplete

Finding ID: UBR-SR1-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define the complete local activation transition and exact standing-contract disposition without restoring tag-era publication choreography.
Rationale: Architecture and tests need one unambiguous owner for retained manifest and grandfathering semantics.
Validation target: UBR-R006 through UBR-R008, UBR-R019, BND-STATE-001, BND-COMPAT-001, and later spec-review.
Validation evidence: Spec revision R2 added the exact active tuple, frozen inventory, and standing-contract disposition table. Spec-review R2 confirmed those corrections and recorded the narrower no-history transition residual as UBR-SR2-001.

#### UBR-SR1-002 - Concise journeys have no independent semantic oracle

Finding ID: UBR-SR1-002
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add three small concrete journey contracts with required inclusions, exclusions, and stage-owned outcomes.
Rationale: Representative semantic proof must distinguish concise correctness from both omission and exhaustive output without brittle prose metrics.
Validation target: E1 through E3, UBR-R001 through UBR-R003, UBR-R018, AC-UBR-001, AC-UBR-002, AC-UBR-011, and later spec-review.
Validation evidence: Spec revision R2 added concrete inclusion and exclusion oracles in E1 through E3 and AC-UBR-001/002. Spec-review R2 confirmed the semantic oracle and recorded the separate user-facing fixture-identity issue as UBR-SR2-002.

#### UBR-SR1-003 - Exact helper retirement lacks stable requirement ownership

Finding ID: UBR-SR1-003
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Give the exact helper and candidate-only selector retirement inventory a stable requirement ID and direct acceptance mapping.
Rationale: The proposal requires removal, while the current stable requirement only prevents ordinary execution and can leave misleading dormant surfaces.
Validation target: UBR-R013, the exact compatibility inventory, EC9, AC-UBR-008, and later spec-review.
Validation evidence: Spec-review R2 confirmed that UBR-R013 owns the closed eight-surface cleanup table and UBR-R012 preserves the original routine release mechanism.

### spec-review-r2

#### UBR-SR2-001 - Declarative snapshots retain an unobservable transition rule

Finding ID: UBR-SR2-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Remove local transition-state claims, keep pending and active as coherent snapshots, and make the reviewed baseline revision an explicit activation-preparation input.
Rationale: A thin tree-local validator cannot prove history after the specification deliberately removes transition-history authority.
Validation target: UBR-R006, UBR-R007, State and invariants, BND-STATE-001, AC-UBR-004, and later spec-review.
Validation evidence: Spec revision R3 removed the unobservable transition rule, made the baseline an explicit activation-preparation input, and passed focused validation. Spec-review R3 approved the resulting snapshot-only contract.

#### UBR-SR2-002 - Synthetic journey interfaces look like shipped commands

Finding ID: UBR-SR2-002
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Use existing RigorLoop surfaces for the three journeys or label fixture-only interfaces before any command-like token.
Rationale: Concrete semantic fixtures should not create user confusion about the product interface.
Validation target: glossary, E1 through E3, AC-UBR-001, AC-UBR-002, and later spec-review.
Validation evidence: Spec revision R3 replaced the synthetic interfaces with existing RigorLoop validator, loader, cleanup, and release surfaces. Spec-review R3 approved the journeys and acceptance criteria.

### spec-review-r3

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review approved all ten review dimensions, reconciled both R2 findings as resolved, and found no new material findings.

### architecture-review-r1

#### UBR-AR1-001 - Baseline inventory derivation has no exact interface

Finding ID: UBR-AR1-001
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Define one exact repository-owned, read-only authoring interface that accepts the full reviewed baseline revision and returns the deterministic sorted eligible-spec inventory without writing state or participating in normal `--check` validation.
Rationale: The approved spec requires an explicit baseline input and repeatable one-time derivation, while the current architecture only names a conceptual helper and rejects a preparation CLI. Planning must not invent the surviving interface or accidentally retain history dependence in checked-revision validation.
Validation target: Revised ADR decision and matching canonical Building Block, Runtime, and Crosscutting statements, followed by architecture-review R2.
Validation evidence: The revised canonical Building Block, Runtime, Crosscutting, quality, risk, and component-diagram surfaces plus ADR-20260806 name the exact callable contract. Architecture-review R2 independently approved the correction with no new material findings.
Safe resolution path: Prefer a pure function in the existing boundary-first validation module with a documented one-time repository invocation; if direct maintainer usability requires a command, permit only a read-only derivation command and keep activation writing out of scope.

### architecture-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review reconciled UBR-AR1-001 as resolved, approved all 13 review dimensions, confirmed arc42/C4/ADR sufficiency, and found no new material findings.

### plan-review-r1

#### UBR-PR1-001 - M3 selects but does not execute its release proof

Finding ID: UBR-PR1-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Add exact executable release-selected CI and standing full-gate commands to M3 before code-review handoff and selection of the reviewed pending baseline; preserve M4's active-state reruns.
Rationale: M3 owns the complete pending release payload and must independently prove package parity and routine-release preservation before M4 freezes its source state. Selector output alone is routing evidence, not execution evidence.
Validation target: Revised M3 validation commands, proof timing, and expected-result wording followed by plan-review R2.
Validation evidence: Plan revision R2 adds both executable gates and distinguishes pending-baseline proof from the active-state rerun. Plan-review R2 approved the sequencing and found no material findings.
Safe resolution path: Add `bash scripts/ci.sh --mode release --release-version v0.4.0` and add `bash scripts/release-verify.sh v0.4.0` unless the former demonstrably invokes the latter; run after M3 supports `v0.4.0` and before baseline selection.

### plan-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review confirmed that M3 executes both release gates before its pending revision becomes M4's baseline, M4 reruns them only after the activation state change, all boundary obligations close independently, and no new scope or mechanism was introduced.

### test-spec-review-r1

#### UBR-TSR1-001 - M1 proof depends on an M2-owned command

Finding ID: UBR-TSR1-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Keep T4 as M1's direct UBR-R005 proof and move T23 plus AC-UBR-012's fail-closed proof-map mutation coverage to M2.
Rationale: CMD06 and the boundary-validator regression suite are owned by M2 in the approved plan, so M1 cannot depend on them for code-review closeout.
Validation target: Revised T23 required milestone, M1 and M2 proof rows, and test-spec-review R2.
Validation evidence: Test-spec revision R2 moves T23 from M1 to M2, updates its evidence path, and preserves T4 under M1. Test-spec-review R2 approved the corrected proof timing with no material findings.
Safe resolution path: Remove T23 from M1, add it to M2, and change T23's required milestone to M2. Preserve T4 under M1 and do not move CMD06 or change plan sequencing.

### test-spec-review-r2

Review result: approved
Material findings: none
Resolution required: no
Validation evidence: The independent review confirmed that every milestone now closes with owner-aligned commands, all requirements and boundary obligations retain direct proof, and no new scope or mechanism was introduced.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Initial review recording | pass | Review record and open dispositions were recorded before lifecycle settlement. |
| R2 reconciliation | pass | Three R1 findings were reconciled, and the two narrower R2 findings are resolved by revision and review R3. |
| R3 authoring validation | pass | Boundary structure, boundary validator tests, change-metadata tests, metadata, review structure, and whitespace validation pass. |
| R3 review settlement | pass | Spec-review R3 approved the revised contract with no material findings. |
| Architecture review R1 recording | pass | The detailed review, log entry, open disposition, and exact architecture and ADR lifecycle settlements are recorded. |
| Architecture revision R2 | pass | The internal derivation function now has exact ownership, input, output, ordering, bounded failure, no-write, one-time-use, and normal-validation separation semantics. |
| Architecture review R2 settlement | pass | R2 approved the canonical architecture and ADR with no open material findings. |
| Plan review R1 recording | pass | The detailed review, log entry, accepted open disposition, and exact plan lifecycle settlement are recorded before any revision. |
| Plan revision R2 | pass | M3 now executes release-mode CI and the standing full gate before review and baseline selection; authoring validation passed. |
| Plan review R2 settlement | pass | R2 approved the revised plan with no material findings and closed UBR-PR1-001. |
| Test-spec review R1 recording | pass | The detailed review, log entry, accepted open disposition, and exact proof-timing gap are recorded before revision. |
| Test-spec revision R2 | pass | T23, CMD06, and M2 evidence now share one milestone boundary; authoring validation passed. |
| Test-spec review R2 settlement | pass | R2 approved all review dimensions with no material findings and closed UBR-TSR1-001. |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale or is not applicable.
- [x] Every deferred finding has follow-up or is not applicable.
- [x] Every `needs-decision` finding is resolved or is not applicable.
- [x] Validation evidence is recorded.
- [x] Closeout status is correct.
