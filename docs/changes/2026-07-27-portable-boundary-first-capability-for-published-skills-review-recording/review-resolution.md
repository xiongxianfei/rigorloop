# Review Resolution: Portable Boundary-First Capability for Published Skills

## Summary

Closeout status: open

Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2
Review closeout: code-review-m3-r3
Review closeout: code-review-m3-r4
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r1
Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m1-r4

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `test-spec-review-r1`, `test-spec-review-r2`
- Findings resolved: 33
- Unresolved findings: 2
- Final result: R4 confirms PBF-M3-CR15 resolved; PBF-M3-CR14 remains partially resolved and PBF-M3-CR16 is open pending renewed correction authority and an upstream trust-owner decision.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PBF-M3-CR16 | needs-decision | needs-decision | Bind accepted proof-map identities to the trusted pre-transition rollback evidence. |
| PBF-M3-CR14 | needs-decision | needs-decision | Current-state recomputation cannot prove pre-transition rollback membership. |
| PBF-M3-CR15 | accepted | resolved | Fixed activation and proof-model inputs are contained before reads. |
| PBF-M3-CR9 | accepted | resolved | Immutable activation history survives later marked adoption and rollback. |
| PBF-M3-CR10 | accepted | resolved | Explicit and derived feature/proof paths are contained before reads. |
| PBF-M3-CR11 | accepted | resolved | Valid aligned separators pass while malformed cells fail. |
| PBF-M3-CR12 | accepted | resolved | Deleted proof maps and orphaned test specs fail when counterparts survive. |
| PBF-M3-CR13 | accepted | resolved | Symlinked historical inventory roots, candidates, and entries fail before reads. |
| PBF-M3-CR1 | accepted | resolved | Markdown parsing is fence-aware, the marker is Status-owned, and separators are exact. |
| PBF-M3-CR2 | accepted | resolved | Malformed records are bounded and proof references and gap IDs fail in vocabulary validation. |
| PBF-M3-CR3 | accepted | resolved | Every governed projection is compared directly with canonical bytes. |
| PBF-M3-CR4 | accepted | resolved | Feature and test-spec paths share one activation-marker gate. |
| PBF-M3-CR5 | accepted | resolved | Active and rolled-back historical inventory membership is exact. |
| PBF-M3-CR6 | accepted | resolved | Absolute, traversal, non-spec, and symlink-escaping changed paths are rejected. |
| PBF-M3-CR7 | accepted | resolved | Serialized offending values use deterministic redacted identities. |
| PBF-M3-CR8 | accepted | resolved | Coordinator commit 197d150b makes CMD8 reproducible from committed state. |
| PBF-M2-CR1 | accepted | resolved | Structured ten-stage packets and negative mutations now prove exact semantic owners, outcomes, handoffs, and closed coverage. |
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

### code-review-m3-r4

R4 partially resolves PBF-M3-CR14 and updates its original disposition below.

#### PBF-M3-CR16 - Rollback inventory omits accepted proof maps

Finding ID: PBF-M3-CR16
Disposition: needs-decision
Status: needs-decision
Owner: user and architecture/spec owner
Decision owner: user and architecture/spec owner
Decision needed: Choose whether proof identities share the feature inventory or use a separate closed inventory, then authorize another correction cycle.
Owning stage: review-resolution M3
Chosen action: Include proof-map identities in the same trusted pre-transition evidence model selected for PBF-M3-CR14.
Rationale: PBF-R057 preserves boundary records and proof maps; feature-only identity is incomplete.
Validation target: missing, stale, symlinked, and mismatched preserved proof maps, CMD6, CMD7, and code-review M3 R5.
Validation evidence: R4 shows activation passes with an exact preserved feature and missing proof map.

### code-review-m3-r3

#### PBF-M3-CR14 - Rollback trusts self-declared current lifecycle status

Finding ID: PBF-M3-CR14
Disposition: needs-decision
Status: needs-decision
Owner: user and architecture/spec owner
Decision owner: user and architecture/spec owner
Decision needed: Choose the trusted pre-transition evidence owner and authorize another correction cycle.
Owning stage: review-resolution M3
Chosen action: Select and bind a trusted pre-transition evidence owner before another correction begins.
Rationale: Current rolled-back files and a recomputable digest cannot prove that membership existed before the transition.
Validation target: add-new plus recomputed-inventory rejection, CMD6, CMD7, and code-review M3 R5.
Validation evidence: The unchanged-inventory regression passes, but R4 shows a new post-rollback approved marker passes after current path/hash insertion and digest recomputation.

#### PBF-M3-CR15 - Fixed authoritative inputs may follow external symlinks

Finding ID: PBF-M3-CR15
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Apply repository containment and no-symlink checks to the fixed activation and proof-model paths before reads.
Rationale: Repository-local authority cannot be delegated through an external symlink.
Validation target: CMD6, CMD7, direct symlink attacks, and code-review M3 R4.
Validation evidence: CMD6 rejects outside symlinks for both fixed inputs and for changed-spec activation lookup; CMD7 passes.

### code-review-m3-r2

#### PBF-M3-CR9 - Activation-time history conflicts with later adoption and rollback preservation

Finding ID: PBF-M3-CR9
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Preserve immutable activation membership and identities while validating later marked current artifacts independently and retaining accepted marked artifacts through rollback.
Rationale: Prospective adoption must not rewrite or invalidate activation-time history.
Validation target: CMD6, CMD7, and code-review M3 R3.
Validation evidence: CMD6 passes 44 tests, including later adoption and rollback preservation; CMD7 passes.

#### PBF-M3-CR10 - Derived companion paths bypass containment

Finding ID: PBF-M3-CR10
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Apply one contained no-symlink resolver to explicit and derived feature/proof paths.
Rationale: A safe selected path must not authorize reads through an unsafe companion.
Validation target: CMD6, direct symlink attacks, and code-review M3 R3.
Validation evidence: CMD6 rejects explicit and derived companion symlink escapes before reads.

#### PBF-M3-CR11 - Valid aligned Markdown separators are rejected

Finding ID: PBF-M3-CR11
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Accept CommonMark alignment separator cells with at least three hyphens while retaining exact width.
Rationale: The contract closes semantic columns, not harmless Markdown alignment.
Validation target: CMD6 and code-review M3 R3.
Validation evidence: CMD6 accepts left-, right-, and center-aligned CommonMark separators and retains malformed-separator failures.

#### PBF-M3-CR12 - Deleted adopting test specs bypass validation

Finding ID: PBF-M3-CR12
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Evaluate surviving counterparts before treating an absent selected path as irrelevant.
Rationale: Deletion is a changed surface and cannot silently remove required proof.
Validation target: CMD6, CMD8, and code-review M3 R3.
Validation evidence: CMD6 rejects deleted adopting proofs and orphaned tests while permitting paired deletion; CMD8 passes 134 tests.

#### PBF-M3-CR13 - Historical inventory paths may follow symlinks outside the repository

Finding ID: PBF-M3-CR13
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Reject symlinked specs roots, eligibility candidates, and recorded historical paths before reading bytes.
Rationale: Activation evidence must depend only on repository-owned regular files.
Validation target: CMD6, CMD7, and code-review M3 R3.
Validation evidence: CMD6 rejects symlinked historical entries and the `specs/` inventory root before reads; CMD7 passes.

### code-review-m3-r1

#### PBF-M3-CR1 - Markdown structure is not context-safe

Finding ID: PBF-M3-CR1
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Add fence-aware parsing, exact Status marker placement, table-separator validation, corrected fixtures, and adversarial regressions.
Rationale: Closed structural validation must reject quoted examples and malformed serialization without claiming semantic completeness.
Validation target: CMD6, CMD7, CMD8, and code-review M3 R2.
Validation evidence: Fence, Status placement, duplicate marker, and malformed-separator regressions pass in CMD6.

#### PBF-M3-CR2 - Malformed rows and identifiers bypass bounded vocabulary handling

Finding ID: PBF-M3-CR2
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Short-circuit malformed governing records, harden feature extraction, and validate proof references and gap IDs in the vocabulary phase.
Rationale: Invalid input must produce deterministic diagnostics, never a traceback or later misleading consistency error.
Validation target: CMD6, CMD7, and code-review M3 R2.
Validation evidence: Malformed governing rows return bounded issues; malformed proof lists and gap IDs fail before consistency in CMD6.

#### PBF-M3-CR3 - Aggregate projection identity can bless mixed bytes

Finding ID: PBF-M3-CR3
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Require each governed projection hash to equal the canonical raw-byte hash before validating the aggregate digest.
Rationale: An internally consistent mixed inventory is still a mixed-version activation baseline.
Validation target: CMD6, CMD7, and code-review M3 R2.
Validation evidence: A divergent projection with a recomputed aggregate still fails `BFR-PROJECTION-DIVERGENT`.

#### PBF-M3-CR4 - Test-spec validation bypasses inactive marker enforcement

Finding ID: PBF-M3-CR4
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Apply one feature activation-marker gate before either feature or test-spec validation.
Rationale: Selector routing must not change contract enforcement for the same governing feature.
Validation target: CMD6, CMD8, and code-review M3 R2.
Validation evidence: Pending marked feature and test-spec paths both fail `BFR-MARKER-INACTIVE`.

#### PBF-M3-CR5 - Active grandfathered inventory membership is not validated

Finding ID: PBF-M3-CR5
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Enumerate lifecycle-eligible top-level feature specs and compare exact active or rolled-back membership.
Rationale: Inventory membership is structural; substantive-revision classification remains with spec-review.
Validation target: CMD6, CMD7, and code-review M3 R2.
Validation evidence: Active omitted historical membership fails `BFR-GRANDFATHERED-MEMBERSHIP`.

#### PBF-M3-CR6 - Changed paths can escape the repository

Finding ID: PBF-M3-CR6
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Enforce lexical and resolved repository containment and the top-level feature/test-spec path grammar before reads.
Rationale: Validation must not read arbitrary caller-selected filesystem paths.
Validation target: CMD6, direct CLI adversarial cases, and code-review M3 R2.
Validation evidence: Absolute, traversal, non-spec, and outside-symlink paths fail before reads.

#### PBF-M3-CR7 - Diagnostics expose offending private payloads

Finding ID: PBF-M3-CR7
Disposition: accepted
Status: resolved
Owner: M3 implement
Owning stage: review-resolution M3
Chosen action: Replace offending values with deterministic redacted identities and test credential/private-payload omission.
Rationale: Stable diagnostics do not require echoing the invalid payload.
Validation target: CMD6, CMD7, and code-review M3 R2.
Validation evidence: Credential-like payload text is absent from serialized JSON and replaced by a stable SHA-256 identity.

#### PBF-M3-CR8 - Recorded selector evidence is not reproducible

Finding ID: PBF-M3-CR8
Disposition: accepted
Status: resolved
Owner: authorized workflow-coordinator bugfix, then M3 implement
Owning stage: review-resolution M3
Chosen action: Complete the separately authorized coordinator correction as an isolated commit, then rerun CMD8 from committed repository state.
Rationale: M3 evidence cannot depend on hidden worktree changes, and the user already authorized the owning bugfix.
Validation target: coordinator regression, full CMD8, and code-review M3 R2.
Validation evidence: Commit `197d150b`; coordinator suites pass 76, 60, and 68 tests, and full CMD8 passes 134 tests.

### code-review-m2-r2

Review closeout: code-review-m2-r2

No material findings.
R2 independently confirms PBF-M2-CR1 resolved and closes M2.

### code-review-m2-r1

#### PBF-M2-CR1 - Semantic behavior fixtures do not exercise the approved contract

Finding ID: PBF-M2-CR1
Disposition: accepted
Status: resolved
Owner: M2 implement
Owning stage: review-resolution M2
Chosen action: Replace phrase-only fixture cases with an exact ten-skill packet matrix carrying structured input, semantic owner, expected outcome, and expected handoff; add negative mutation proof.
Rationale: T10 and T16 require stage behavior and handoff proof, not only published-text substring checks.
Validation target: CMD3, CMD4, CMD5, focused lifecycle tests, and same-stage code-review M2 R2.
Validation evidence: Four focused lifecycle tests, all 263 skill-validator tests, canonical skill validation, generated build checking, and scoped diff checking pass.

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

### code-review-m1-r4

Review closeout: code-review-m1-r4

No material findings.
R4 independently confirms PBF-M1-CR1 through PBF-M1-CR4 resolved and closes M1.
