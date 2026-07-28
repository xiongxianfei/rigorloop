# Review Resolution: Portable Boundary-First Capability for Published Skills

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 18
- Unresolved findings: 0
- Final result: PBF-M1-CR4 is resolved under the user-authorized additional correction cycle; M1 awaits code-review R4.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PBC-PR1 | accepted | resolved | R3 confirmed the ten-skill scope, proposal-stage exclusion, and governed-resource consumer rule. |
| PBC-PR2 | accepted | resolved | R3 confirmed bounded independent semantic-review evidence and claim limits. |
| PBC-PR3 | accepted | resolved | R3 confirmed the corrected lifecycle sequence. |
| PBF-PR1 | accepted | resolved | R3 confirmed the first-version vocabulary and record relationships. |
| PBF-PR2 | accepted | resolved | R3 confirmed planning and exact semantic-review responsibilities. |
| PBF-PR3 | accepted | resolved | R3 confirmed the READ reference and deterministic projection model. |
| PBF-PR4 | accepted | resolved | R3 confirmed activation, grandfathering, and rollback. |
| PBF-SR1 | accepted | resolved | V1 grammar is closed and undefined extensions and imports are prohibited. |
| PBF-SR2 | accepted | resolved | Durable activation-baseline evidence and semantic revision ownership are defined. |
| PBF-SR3 | accepted | resolved | Covered proof rows and blocking gap rows are distinct. |
| PBF-AR1 | accepted | resolved | The proof-model spec owns activation state and grandfathering is accepted-only. |
| PBF-AR2 | accepted | resolved | One shared helper defines reproducible projection and inventory digests. |
| PBF-TSR1 | accepted | resolved | Acceptance criteria, exact edge cases, and supplemental normative surfaces have stable direct proof. |
| PBF-TSR2 | accepted | resolved | M4 and final-verify broad-smoke invocations have separate stage owners and gates. |
| PBF-M1-CR1 | accepted | resolved | Parent-directory symlink escape is rejected before outside reads or writes. |
| PBF-M1-CR2 | accepted | resolved | Symlinked unexpected consumers fail closed without traversal. |
| PBF-M1-CR3 | accepted | resolved | Symlink regression outside fixtures use managed cleanup. |
| PBF-M1-CR4 | accepted | resolved | Unexpected-consumer symlink proof covers write-mode non-mutation and combined errors. |

## Finding Details

### proposal-review-r1

#### PBC-PR1 - Governed-skill and packaged-resource scope is contradictory

Finding ID: PBC-PR1
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Chosen action: Govern ten lifecycle skills, begin normative boundary authoring at `spec`, exclude proposal stages from first-version authoring, and package the reference with each governed skill.
Rationale: The broader PBF-PR2 decision added planning while preserving an explicit pre-spec boundary and an exact resource-consumer rule.
Validation target: A revised proposal with one explicit governed-skill list and one unambiguous resource-consumer rule.
Validation evidence: Proposal-review R3 confirmed `First-version portable contract`, `Goals`, `Scope budget`, `Architecture Impact`, and `Acceptance Criteria` use the same ten-skill scope and governed-resource rule.

### proposal-review-r2

#### PBF-PR1 - Core boundary contract is deferred past proposal review

Finding ID: PBF-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Chosen action: Add a closed first-version dimension vocabulary, applicability states, boundary-record relationships, proof-record relationships, and example classifications.
Rationale: These choices determine user burden and cross-stage compatibility, so the proposal must select them before specification.
Validation target: Revised `First-version portable contract`, acceptance criteria, decision log, and open-question sections.
Validation evidence: Proposal-review R3 confirmed the revised contract defines eight dimensions, two applicability states, feature-spec boundary records, test-spec proof records, and example classifications.

#### PBF-PR2 - Governed path omits planning and leaves semantic-review ownership generic

Finding ID: PBF-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Chosen action: Expand the governed set to ten skills and assign exact authoring, review, implementation, and verification responsibilities.
Rationale: Planning owns milestone isolation, sequencing, rollback units, dependencies, and proof timing; semantic approval must remain with named review stages.
Validation target: Revised scope budget, governed-skill matrix, testing strategy, architecture impact, rollout, and acceptance criteria.
Validation evidence: Proposal-review R3 confirmed the governed-skill matrix covers ten skills, including `plan` and `plan-review`, with distinct semantic judgments.

#### PBF-PR3 - Shared reference source and packaging model are unsettled

Finding ID: PBF-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Chosen action: Select a versioned `READ` reference with one canonical source, deterministic skill-local projections, and byte parity through installed adapters.
Rationale: The resource class and projection model are part of the published-skill contract, while architecture may still select the exact canonical path.
Validation target: Revised first-version contract, architecture impact, testing strategy, rollout, and acceptance criteria.
Validation evidence: Proposal-review R3 confirmed `Shared reference`, `Architecture Impact`, `Testing and Verification Strategy`, and `AC-PBF-006` through `AC-PBF-008` define the versioned READ resource and parity chain.

#### PBF-PR4 - Activation and compatibility semantics are deferred

Finding ID: PBF-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal revision
Chosen action: Add `boundary_contract: boundary-first-v1`, substantive-revision triggers, in-flight opt-in, no-partial-activation gates, grandfathering, and rollback preservation.
Rationale: Activation changes public workflow expectations and historical compatibility, so the proposal must select the policy before specification.
Validation target: Revised rollout and rollback, expected behavior, acceptance criteria, decision log, and open-question sections.
Validation evidence: Proposal-review R3 confirmed `Activation`, `Expected Behavior Changes`, `Rollout and Rollback`, the decision log, and `AC-PBF-011` through `AC-PBF-012` define prospective atomic activation and grandfathering.

#### PBC-PR2 - Semantic-review proof is undefined within the proposal's validation limits

Finding ID: PBC-PR2
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Chosen action: Add bounded independent review exercises with named fixture inputs, expected findings, durable evidence, and explicit non-generalization.
Rationale: This preserves semantic-review proof without making a validator or runtime certification claim.
Validation target: A revised testing strategy that names the proof surface, reviewer independence, pass/fail evidence, and claim boundary.
Validation evidence: Proposal-review R3 confirmed `Testing and Verification Strategy` distinguishes deterministic fixtures from bounded independent review exercises and limits their claims to reviewed cases.

#### PBC-PR3 - Next-artifact order conflicts with the governing lifecycle

Finding ID: PBC-PR3
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Chosen action: Order downstream work as spec, spec-review, architecture, architecture-review, plan, plan-review, test-spec, test-spec-review, then implementation.
Rationale: The governing lifecycle already fixes the required ordering for this compatibility-sensitive architecture change.
Validation target: A revised `Next Artifacts` sequence aligned with the governing lifecycle and its required review gates.
Validation evidence: Proposal-review R3 confirmed `Next Artifacts` lists every required artifact and adjacent review gate in governing order.

### proposal-review-r3

Review closeout: proposal-review-r3

No material findings.
R3 confirms all seven prior findings resolved.

### spec-review-r1

#### PBF-SR1 - The v1 record grammar is not closed

Finding ID: PBF-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Prohibit v1 extensions and cross-feature imports, add exact prefix mapping, and define sentinel and multi-ID serialization.
Rationale: Deterministic validators and downstream skills must not invent missing grammar.
Validation target: Revised PBF-R008 through PBF-R040 and matching edge cases.
Validation evidence: Spec-review R2 confirmed closed prefixes, sentinels, ID lists, extension prohibition, and import prohibition.

#### PBF-SR2 - Activation lacks a durable grandfathering baseline

Finding ID: PBF-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Require a durable activation record and assign semantic substantive-revision classification to spec-review.
Rationale: Prospective compatibility cannot depend on chat history or validator inference.
Validation target: Revised activation, compatibility, observability, and acceptance criteria.
Validation evidence: Spec-review R2 confirmed the durable activation record, baseline identities, and split structural-versus-semantic ownership.

#### PBF-SR3 - Proof gaps can be mistaken for proof coverage

Finding ID: PBF-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Add a closed proof coverage state and blocking gap-row semantics.
Rationale: Missing proof must route upstream and cannot satisfy implementation eligibility.
Validation target: Revised proof-map requirements and edge cases.
Validation evidence: Spec-review R2 confirmed `covered` and `gap` rows, exact field rules, and the implementation block.

### spec-review-r2

Review closeout: spec-review-r2

No material findings.
R2 confirms PBF-SR1 through PBF-SR3 resolved and approves the contract
amendment for architecture.

### architecture-review-r1

#### PBF-AR1 - Activation ownership and grandfathering eligibility are ambiguous

Finding ID: PBF-AR1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Chosen action: Keep activation state authoritative in the proof-model spec, make YAML state a checked projection, grandfather only accepted or approved historical specs, and block unresolved in-flight specs unless they opt in.
Rationale: Compatibility must not create two state owners or let a preactivation draft bypass the new contract.
Validation target: Revised ADR, canonical runtime and crosscutting sections, risk handling, and architecture-review R2.
Validation evidence: Architecture-review R2 confirmed authoritative state ownership, YAML parity, accepted-only grandfathering, and in-flight handling.

#### PBF-AR2 - Projection and inventory identities are not reproducible

Finding ID: PBF-AR2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture revision
Chosen action: Define sorted POSIX-path and raw-byte-hash record serialization with one shared digest helper.
Rationale: Generator and validator identities must be deterministic across supported environments.
Validation target: Revised ADR, canonical crosscutting section, and architecture-review R2.
Validation evidence: Architecture-review R2 confirmed the exact shared digest serialization and scope.

### architecture-review-r2

Review closeout: architecture-review-r2

No material findings.
R2 confirms PBF-AR1 and PBF-AR2 resolved and approves planning reliance.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Proposal review R1 | pass | Review artifacts and change metadata pass repository structural validation. |
| Proposal revision | pass | All seven recorded findings map to explicit revised proposal sections. |
| Proposal review R3 | pass | Independent rereview found no material finding and confirmed all seven prior findings resolved. |
| Spec review R1 | changes-requested | Three material contract gaps are accepted for revision. |
| Spec review R2 | pass | Independent rereview confirmed all three spec findings resolved. |
| Architecture review R1 | changes-requested | Two material design clarifications are accepted for revision. |
| Architecture review R2 | pass | Independent rereview confirmed both architecture findings resolved. |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale; no findings are rejected.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale; no findings are deferred.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [x] Validation evidence is recorded for PBF-SR1 through PBF-SR3.
- [x] Validation evidence is recorded for PBF-AR1 and PBF-AR2.
- [x] Closeout status is correct.
### plan-review-r1

Review closeout: plan-review-r1

No material findings.
R1 approves the four-milestone trust-boundary decomposition for test-spec
authoring. Implementation authority remains separate.

### test-spec-review-r1

#### PBF-TSR1 - Normative and acceptance-criterion traceability is incomplete

Finding ID: PBF-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Add stable acceptance-criterion and supplemental normative-coverage mappings, refining existing tests or adding one focused test where direct proof is absent.
Rationale: Every normative contract obligation must have direct, executable proof before implementation begins.
Validation target: Revised coverage maps and stable test cases for diagnostics, redacted evidence, published Markdown readability, and the ordinary-authoring portability boundary.
Validation evidence: Test spec identity `sha256:c7666cb2205e150cf8e43487087ab4cd3401b532d87d93d51832a211926a71c1` maps all fourteen acceptance criteria, all sixteen named edge cases including EC10a, and supplemental normative observability, privacy, accessibility, and portability surfaces to stable tests and commands; test-spec-review R2 remains the approval gate.

#### PBF-TSR2 - Broad-smoke ownership conflicts with its first required gate

Finding ID: PBF-TSR2
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Split M4 and final-verify broad-smoke records so each invocation has the stage owner that performs its first required gate.
Rationale: A later verify-only authority cannot satisfy an implementation milestone's pre-code-review proof requirement.
Validation target: Revised command ledger, M4 proof row, and performance text with distinct implementation and verify command IDs.
Validation evidence: CMD13 now assigns the pre-code-review M4 broad-smoke run to `implement`, while CMD16 independently assigns the final rerun to `verify`; both name their first required gate and failure behavior.

### test-spec-review-r2

Review closeout: test-spec-review-r2

No material findings.
R2 confirms PBF-TSR1 and PBF-TSR2 resolved and approves implementation handoff
for M1 under separate implementation authority.

### code-review-m1-r1

#### PBF-M1-CR1 - Projection paths can escape the repository through symlinked parents

Finding ID: PBF-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution M1
Chosen action: Add source-parent and destination-parent symlink-escape regressions, then apply one repository-contained path-component guard before projection filesystem operations.
Rationale: The correction is fully determined by the approved security boundary and remains inside M1 implementation scope.
Validation target: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
Validation evidence: Commit `0b198866`; `python scripts/test-boundary-first-reference.py` passed nine tests including source-parent and destination-parent escape cases; `python scripts/project-boundary-first-reference.py --check` passed all ten consumers.

### code-review-m1-r2

#### PBF-M1-CR2 - Symlinked unexpected consumers evade closed-inventory validation

Finding ID: PBF-M1-CR2
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution M1
Chosen action: Add both unexpected-consumer symlink regressions and reject the encountered symlink topology without traversal.
Rationale: Closed consumer membership and symlink-escape rejection are explicit approved requirements.
Validation target: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
Validation evidence: Commit `ffa692c0`; both ungoverned symlink topologies now produce `BFR-UNEXPECTED-CONSUMER-SYMLINK`; the ten-test suite and live ten-consumer projection check pass.

#### PBF-M1-CR3 - Symlink regressions leak their outside fixtures

Finding ID: PBF-M1-CR3
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution M1
Chosen action: Allocate each outside fixture with its own registered `TemporaryDirectory` cleanup.
Rationale: The correction is deterministic test-fixture hygiene and does not alter product behavior or the approved contract.
Validation target: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
Validation evidence: Commit `ffa692c0`; outside fixtures now use registered `TemporaryDirectory` cleanup, and the legacy sibling-directory count remained unchanged across the ten-test run.

### code-review-m1-r3

#### PBF-M1-CR4 - Unexpected-consumer symlink proof omits write mode and combined errors

Finding ID: PBF-M1-CR4
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution M1
Chosen action: Extend the focused regression over check/write and add immutable outside-sentinel plus combined-error assertions.
Rationale: The user authorized one additional correction cycle for this deterministic test-only change.
Validation target: `python scripts/test-boundary-first-reference.py`; `python scripts/project-boundary-first-reference.py --check`
Validation evidence: Commit `877a697f`; `python scripts/test-boundary-first-reference.py` passed ten tests covering both topology and mode pairs, exact combined errors, and outside sentinel preservation; live ten-consumer projection check passed.
