# Review Resolution: Activate Boundary-First v1 in RigorLoop v0.4.0

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: proposal-review-r4
Review closeout: spec-review-r2
Review closeout: architecture-review-activation-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: plan-review-r3
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3
Review closeout: code-review-m1-r1
Review closeout: test-spec-review-r4
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: spec-review-r3
Review closeout: spec-review-r4
Review closeout: spec-review-r5
Review closeout: architecture-review-activation-r2
Review closeout: architecture-review-activation-r3
Review closeout: plan-review-r4
Review closeout: test-spec-review-r5
Review closeout: test-spec-review-r6
Review closeout: test-spec-review-r7

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `proposal-review-r4`, `spec-review-r2`, `architecture-review-activation-r1`, `plan-review-r1`, `plan-review-r2`, `plan-review-r3`, `test-spec-review-r1`, `test-spec-review-r2`, `test-spec-review-r3`, `code-review-m1-r1`, `test-spec-review-r4`, `code-review-m1-r2`, `code-review-m1-r3`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `architecture-review-activation-r2`, `architecture-review-activation-r3`, `plan-review-r4`, `test-spec-review-r5`, `test-spec-review-r6`, `test-spec-review-r7`
- Findings resolved: 30
- Unresolved findings: 5
- Final result: Test-spec R7 approves the R/C/H proof map; existing M1 identity, proof, invocation-shape, and privacy findings remain for implementation and code-review R4.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| BFA-PR1-001 | accepted | resolved | Added pre-tag candidate validation while preserving strict tag-context activation proof. |
| BFA-PR2-001 | accepted | resolved | Separated final reviewed branch head from the activation transition tag target and required tagged-tree self-containment. |
| BFA-SR1-001 | accepted | resolved | Separated remote publication base P from transition parent/grandfathering baseline B. |
| BFA-SR1-002 | accepted | resolved | Replaced patch v0.3.7 with contract-compliant minor v0.4.0 through proposal revision. |
| BFA-SR1-003 | accepted | resolved | Invalid unpublished transition histories require a fresh replacement branch and rereview. |
| BFA-SR1-004 | accepted | resolved | Completed formal boundary ownership for identity, self-containment, strict composition, drift, and replacement. |
| BFA-SR3-001 | accepted | resolved | Defined phase-correct publication readiness after local tag creation with explicit persisted and fresh authorities. |
| BFA-SR3-002 | accepted | resolved | Added BFA-R017 ownership to the identity applicability and E4 traceability records. |
| BFA-SR4-001 | accepted | resolved | Aligned E3, BND-COMPOSE-001, and INT-004 with the three pre-publication gates. |
| BFA-AR2-001 | accepted | resolved | Aligned the focused component view and canonical decision summary with candidate P/B/T/R, evidence C, and readiness-bound H. |
| BFA-TSR5-001 | accepted | resolved | Completed the originally identified candidate, readiness, and T16 producer chains. |
| BFA-TSR5-002 | accepted | resolved | Added direct readiness/publication privacy sentinel partitions and MP1 scans. |
| BFA-TSR6-001 | accepted | resolved | Added CMD17/CMD18 to remaining hybrid rows that claim their evidence. |
| BFA-TSR6-002 | accepted | resolved | Assigned T12 fixture privacy proof to M2 evidence/milestone and completed the summary. |
| BFA-PLAN-R1-001 | accepted | resolved | Final M3 workflow closeout head is B and T is its immediate child. |
| BFA-PLAN-R1-002 | accepted | resolved | Separated candidate, strict-H, and detached-T proof phases. |
| BFA-PLAN-R1-003 | accepted | resolved | Mapped release and public-closeout boundary proof owners. |
| BFA-PLAN-R1-004 | accepted | resolved | Replaced placeholder commands with executable rules and corrected CLI syntax. |
| BFA-PLAN-R2-001 | accepted | resolved | Designated B only after M3 review and closeout evidence settles. |
| BFA-PLAN-R2-002 | accepted | resolved | Corrected release validation and added failure-safe executable shell. |
| BFA-TSR1-001 | accepted | resolved | Replaced invalid proof levels with admitted execution levels. |
| BFA-TSR1-002 | accepted | resolved | Added phase-correct lifecycle-readiness regression and evidence. |
| BFA-TSR1-003 | accepted | resolved | Linked atomic, tag-workflow, and public paths to direct commands and evidence. |
| BFA-TSR1-004 | accepted | resolved | Made MP1 and MP2 executable and auditable. |
| BFA-TSR2-001 | accepted | resolved | Linked MP1 and producing commands directly from PRF-006 and PRF-008. |
| BFA-M1-CR1-001 | accepted | resolved | Reject every supplied candidate value except exact v0.4.0. |
| BFA-M1-CR1-002 | accepted | resolved | Inspect every direct post-T first-parent commit so a revert cannot hide drift. |
| BFA-M1-CR1-003 | accepted | resolved | Composed canonical settlement with phase-correct tagged readiness. |
| BFA-M1-CR1-004 | accepted | resolved | Emit available failure context and corrective action. |
| BFA-M1-CR1-005 | accepted | resolved | Completed direct M1 proof and all eight sibling failure paths. |
| BFA-M1-CR1-006 | accepted | resolved | Require all applicable directory descendants to be tracked. |
| BFA-M1-CR1-007 | accepted | resolved | Replaced open evidence/review subtrees with closed lifecycle ownership. |
| BFA-M1-CR1-008 | accepted | resolved | Bound diagnostics against short and runtime private sentinels. |
| BFA-M1-R2-001 | accepted | resolved | Inspect merged side-branch commits so change-and-revert ancestry cannot hide drift. |
| BFA-M1-R3-001 | accepted | resolved | Separated candidate-producing R, evidence commit C, and publication head H. |
| BFA-M1-R4-001 | accepted | resolved | Replaced candidate-mode rerun with phase-correct tagged readiness. |
| BFA-M1-R4-002 | accepted | resolved | Aligned closed receipt validation with accepted abbreviated identities. |
| BFA-M1-R4-003 | accepted | resolved | Redact short PIN, API-key, and auth-code environment values. |
| BFA-M1-R5-001 | accepted | resolved | Bound revision validation to each packet inventory entry. |
| BFA-M1-R5-002 | accepted | resolved | Accept lexical numeric abbreviated base/head revisions. |
| BFA-M1-R6-001 | accepted | resolved | Rejected duplicate inventory sections and mapping keys. |
| BFA-M1-R7-001 | accepted | resolved | Normalized parser-equivalent duplicate top-level keys. |
| BFA-M1-R7-002 | accepted | resolved | Required unique packet inventory paths. |

## Finding Details

### proposal-review-r1

#### BFA-PR1-001 - Pre-tag PR and strict activation validation are circular

Finding ID: BFA-PR1-001
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the proposal to define a candidate-validation bridge and strict release-owned tag validation.
Rationale: This preserves reviewed PR readiness, immutable tag authority, the existing rollback rule, and the user's stable-release objective without publishing before review.
Validation target: proposal-review-r2
Validation evidence: Proposal-review R2 confirms explicit candidate and strict tag-context phases resolve the circular gate.

### proposal-review-r2

#### BFA-PR2-001 - Reviewed branch head and activation tag target are conflated

Finding ID: BFA-PR2-001
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the proposal to publish `main` at the final reviewed head and `v0.3.7` at the earlier reviewed transition commit, with tagged-tree release self-containment.
Rationale: The activation tag contract binds the pending-to-active transition, while durable lifecycle evidence can validly follow that transition on the same first-parent branch.
Validation target: proposal-review-r3
Validation evidence: Proposal-review R3 confirms the two-identity first-parent model, tagged-tree self-containment, candidate/strict authority split, compare-and-swap, and atomic publication are coherent.

### spec-review-r1

#### BFA-SR1-001 - Publication base and grandfathering baseline are conflated

Finding ID: BFA-SR1-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Introduce publication base P and preserve B as T's first parent.
Rationale: Candidate preparation can occur between the remote fork point and activation transition.
Validation target: spec-review-r2
Validation evidence: Spec-review R2 approves the `P ... B -> T ... H` identity chain and confirms compare-and-swap uses P while the activation manifest retains B.

#### BFA-SR1-002 - Patch version violates release classification

Finding ID: BFA-SR1-002
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the release target to stable minor v0.4.0 and retain v0.3.6 rollback.
Rationale: REL-R9 and REL-R10 classify new backward-compatible public skill behavior as a minor release.
Validation target: proposal-review-r4 then spec-review-r2
Validation evidence: Proposal-review R4 approves stable minor v0.4.0 under REL-R10 and confirms v0.3.6 rollback plus prior sequencing remain intact.

#### BFA-SR1-003 - Invalid transition recovery lacks a legal history

Finding ID: BFA-SR1-003
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define replacement-branch regeneration from the authorized publication base.
Rationale: Appending another transition violates uniqueness and force-pushing would rewrite reviewed history.
Validation target: spec-review-r2
Validation evidence: Spec-review R2 confirms BFA-R035, E7, EC8, AC-BFA-015, and INT-007 define a legal replacement history without force-push.

#### BFA-SR1-004 - Formal boundary ownership is incomplete

Finding ID: BFA-SR1-004
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Extend exact boundary and interaction ownership for the missing requirements and hazards.
Rationale: Downstream proof must consume requirement-owned semantic rows rather than infer them.
Validation target: spec-review-r2
Validation evidence: Spec-review R2 confirms self-containment, strict composition, changed-path rejection, and replacement recovery have explicit boundary and interaction ownership.

### plan-review-r1

#### BFA-PLAN-R1-001 - M3 lacks a realizable B to T commit sequence

Finding ID: BFA-PLAN-R1-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Split the release work into a committed pre-transition payload baseline B and a narrow transition commit T.
Rationale: The approved identity chain requires B and T to be separately realizable and reviewable commits.
Validation target: plan-review-r2
Validation evidence: Plan-review R3 confirms the final M3 workflow closeout head is B and M4 creates immediate-child T with no intervening commit.

#### BFA-PLAN-R1-002 - Candidate proof is conflated with strict tagged-tree proof

Finding ID: BFA-PLAN-R1-002
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Separate candidate validation at H from release-owned local-tag validation at H and detached-T release verification.
Rationale: Candidate proof cannot establish the strict tag-context contract that exists only after the local release tag is created.
Validation target: plan-review-r2
Validation evidence: Plan-review R2 confirms candidate-H, strict-H, and detached-T proof now have separate owners and ordered phases.

#### BFA-PLAN-R1-003 - Boundary ownership omits release and public closeout proof

Finding ID: BFA-PLAN-R1-003
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Map implementation, candidate, strict release, atomic publication, and post-publication closeout to distinct proof owners.
Rationale: State, recovery, environment, and publication outcomes cross multiple phases and need explicit ownership.
Validation target: plan-review-r2
Validation evidence: Plan-review R2 confirms implementation, candidate, strict release, atomic publication, and public closeout are mapped independently.

### plan-review-r2

#### BFA-PLAN-R2-001 - B is designated before M3 can close

Finding ID: BFA-PLAN-R2-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Treat the payload commit as preparation and designate the final M3 closeout head as B only after review, resolution, and validation settle.
Rationale: T must be the immediate child of B while M4 may begin only after M3 is fully closed.
Validation target: plan-review-r3
Validation evidence: Plan-review R3 confirms M3 review and resolution settle before the final workflow closeout/routing commit becomes B.

#### BFA-PLAN-R2-002 - Release-checkpoint commands are not fully executable

Finding ID: BFA-PLAN-R2-002
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Correct `validate-release.py` to use `--version` and replace the prose recipe with a literal failure-safe shell block.
Rationale: Release operators need executable commands that cannot continue to publication after a failed strict or tagged-tree gate.
Validation target: plan-review-r3
Validation evidence: Plan-review R3 confirms the corrected CLI, Bash syntax, pre-publication cleanup, publication gating, and post-attempt evidence preservation.

#### BFA-PLAN-R1-004 - Broader validation commands are placeholders

Finding ID: BFA-PLAN-R1-004
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Replace placeholder commands with executable command rules for candidate H, strict H, detached T, bare-remote publication, and closeout.
Rationale: Implementation and release handoffs must be reproducible without inventing commands downstream.
Validation target: plan-review-r2
Validation evidence: Plan-review R3 confirms literal selector, candidate-H, strict-H, detached-T, bare-remote, and closeout command coverage.

## Test-Spec Review Findings

### test-spec-review-r1

#### BFA-TSR1-001 - Invalid proof-level vocabulary

Finding ID: BFA-TSR1-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Replace `migration` proof levels with the admitted level matching actual execution while retaining compatibility semantics in prose.
Rationale: Proof-level vocabulary is closed and structural validity must match semantic execution.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R2 confirms every proof row uses an admitted integration or end-to-end level.

#### BFA-TSR1-002 - Lifecycle readiness proof is circular and mistimed

Finding ID: BFA-TSR1-002
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add a planned missing-evidence regression command, schedule current-state readiness at M4 and release checkpoint, and use phase-owned evidence.
Rationale: A preimplementation review receipt cannot prove publication-time lifecycle settlement.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R2 confirms M1 missing-evidence fixtures, M4 candidate proof, and release-checkpoint preflight provide phase-correct evidence.

#### BFA-TSR1-003 - Public sibling paths lack direct command and evidence links

Finding ID: BFA-TSR1-003
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add automated tag-workflow composition proof and map actual atomic, tag-workflow, and closeout commands to distinct evidence.
Rationale: Helper or selector proof cannot substitute for the real public path.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R3 confirms actual atomic, tag-workflow, and public paths have direct command, procedure, and distinct evidence links.

#### BFA-TSR1-004 - Manual procedures are not independently auditable

Finding ID: BFA-TSR1-004
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add explicit owner, stage, rationale, environment, commands, evidence, pass/failure, cleanup, and forbidden-action fields to MP1 and MP2.
Rationale: Irreversible external proof requires exact bounded procedures and durable evidence.
Validation target: test-spec-review-r2
Validation evidence: Test-spec-review R2 confirms MP1 and MP2 define owner, stage, rationale, environment, commands, evidence, pass/failure, recovery, and forbidden actions.

### test-spec-review-r2

#### BFA-TSR2-001 - Actual atomic evidence lacks producing procedure links

Finding ID: BFA-TSR2-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add T11, MP1, checkpoint commands, and checkpoint evidence to PRF-006, and add CMD17 plus MP1 to PRF-008.
Rationale: Each hybrid proof row must cite the command and procedure that directly produce its claimed external evidence.
Validation target: test-spec-review-r3
Validation evidence: Test-spec-review R3 confirms PRF-006 and PRF-008 cite MP1 and every command producing their claimed external evidence.

### code-review-m1-r1

#### BFA-M1-CR1-001 - Empty candidate value falls through to strict mode

Finding ID: BFA-M1-CR1-001
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Dispatch on option presence and add empty-value CLI regressions.
Rationale: Candidate vocabulary is closed and malformed candidate input cannot become strict success.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirms empty candidate values remain in candidate mode and reject while missing `--check` remains a parser error.

#### BFA-M1-CR1-002 - Reverted post-transition payload drift is accepted

Finding ID: BFA-M1-CR1-002
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Inspect every T-to-H first-parent commit and report the union of forbidden paths.
Rationale: Endpoint equality does not prove that unpublished candidate history remained valid.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirms direct first-parent change/revert, rename, deletion, and multi-path histories are resolved; merged ancestry is tracked separately as BFA-M1-R2-001.

#### BFA-M1-CR1-003 - Publication readiness treats file presence as settlement

Finding ID: BFA-M1-CR1-003
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Compose canonical lifecycle validators and require candidate verification evidence.
Rationale: Placeholder files cannot authorize external publication.
Validation target: code-review-m1-r2
Validation evidence: R2 correction now compares the complete persisted result to fresh authority and requires its evidence commit to be the immediate child of the recorded producing head; forged-identity and canonical-authority regressions pass, pending R3 confirmation.

#### BFA-M1-CR1-004 - Candidate failure output lacks bounded context and corrective action

Finding ID: BFA-M1-CR1-004
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Return and serialize bounded available candidate context plus stable corrective actions.
Rationale: Operators need actionable, privacy-safe failure evidence at the authority boundary.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirms available P/B/T/H, rollback, tag state, invariant details, and corrective actions are present; remaining privacy bounds are tracked under BFA-M1-CR1-008.

#### BFA-M1-CR1-005 - M1 direct proof is materially incomplete

Finding ID: BFA-M1-CR1-005
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Add the missing T4, T5, T6, T12, and T16 partitions and correct evidence claims; route normative test-spec text changes to its owner if required.
Rationale: Passing partial tests cannot substitute for the approved direct proof map.
Validation target: code-review-m1-r2
Validation evidence: R2 correction adds security/CI selection, one injected selected-command failure per sibling owner, merged drift, forged evidence, and invocation-shape partitions; CMD1 and CMD6 pass, pending R3 confirmation.

#### BFA-M1-CR1-006 - Directory preflight hides mixed tracked and untracked contents

Finding ID: BFA-M1-CR1-006
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Require every applicable existing directory descendant to be tracked and add boundary fixtures.
Rationale: One tracked child cannot authorize an otherwise mixed directory surface.
Validation target: code-review-m1-r2
Validation evidence: Code-review M1 R2 confirms fully tracked, mixed, empty, only-untracked, and top-level symlink directory behavior is resolved.

#### BFA-M1-CR1-007 - Lifecycle subtree allowlist admits arbitrary payload

Finding ID: BFA-M1-CR1-007
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Use a closed lifecycle evidence path/shape policy and reject packages, generated output, and arbitrary descendants.
Rationale: Directory placement alone does not confer lifecycle ownership.
Validation target: code-review-m1-r2
Validation evidence: R2 correction closes the invocation grammar and requires matching identity, stage, manifest owner, and workflow evidence reference; unknown, malformed, unowned, and valid cases pass, pending R3 confirmation.

#### BFA-M1-CR1-008 - Drift diagnostics disclose private path sentinels

Finding ID: BFA-M1-CR1-008
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Bound path identities and add every required privacy sentinel to failure-output tests.
Rationale: Changed-path evidence must remain useful without disclosing prohibited private values.
Validation target: code-review-m1-r2
Validation evidence: R2 correction hashes paths containing actual runtime identity or private environment values and bounds invalid candidate/rollback scalars; direct CLI regressions pass, pending R3 confirmation.

### code-review-m1-r2

#### BFA-M1-R2-001 - Merged side-branch history bypasses drift detection

Finding ID: BFA-M1-R2-001
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Traverse every commit newly reachable in T..H and union forbidden parent-relative paths across merge ancestry.
Rationale: First-parent-only enumeration can hide a forbidden side-branch change and revert even though both commits remain in reviewed history.
Validation target: code-review-m1-r3
Validation evidence: Code-review M1 R3 confirms complete T..H traversal rejects merged side-branch change/revert history.

### code-review-m1-r3

#### BFA-M1-R3-001 - Final evidence-bearing H is self-referential

Finding ID: BFA-M1-R3-001
Disposition: accepted
Status: resolved
Owner: spec and architecture authors
Owning stage: spec then architecture
Decision owner: spec and architecture authors
Decision needed: Choose the realizable identity model for candidate-producing head, evidence commit, final publication head, and publisher target.
Chosen action: Decide and specify a distinct candidate-producing identity and final evidence-bearing publication head, then align plan, test spec, and implementation.
Rationale: A tracked evidence file cannot contain the Git identity of its own containing commit; the implementation cannot safely guess a new identity model.
Validation target: spec-review, architecture-review, plan-review, test-spec-review, then code-review-m1-r4
Validation evidence: Spec-review R5, architecture-review R3, plan-review R4,
test-spec-review R7, and code-review M1 R4 confirm the realizable R/C/H model.

### code-review-m1-r4

#### BFA-M1-R4-001 - Readiness reruns pre-tag candidate mode

Finding ID: BFA-M1-R4-001
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Implement phase-correct stored R/C and live-H readiness without
calling candidate mode, then prove success after local tag creation.
Rationale: BFA-R018 explicitly separates pre-tag candidate validation from
post-tag publication readiness.
Validation target: code-review-m1-r5
Validation evidence: pending correction and R5

### code-review-m1-r5

#### BFA-M1-R5-001 - Cross-section revision substitution

Finding ID: BFA-M1-R5-001
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Lexically bind every inventory revision to its own packet block.
Rationale: File-wide counts cannot prove per-entry validity.
Validation target: code-review-m1-r6
Validation evidence: pending correction and R6

### code-review-m1-r6

#### BFA-M1-R6-001 - Duplicate inventory ambiguity

Finding ID: BFA-M1-R6-001
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Require unique top-level fields, one inventory section, and exact
full consumption of packet triples without duplicate keys.
Rationale: Closed lifecycle evidence cannot rely on last-value-wins YAML parsing.
Validation target: code-review-m1-r7
Validation evidence: pending correction and R7

### code-review-m1-r7

#### BFA-M1-R7-001 - Spaced duplicate keys

Finding ID: BFA-M1-R7-001
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Normalize top-level key syntax before duplicate detection.
Rationale: Lexical validation must match parser key equivalence.
Validation target: code-review-m1-r8
Validation evidence: pending correction and R8

#### BFA-M1-R7-002 - Duplicate packet paths

Finding ID: BFA-M1-R7-002
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Require unique lexical and parsed packet paths.
Rationale: One reviewed artifact path cannot carry contradictory identities.
Validation target: code-review-m1-r8
Validation evidence: pending correction and R8

#### BFA-M1-R5-002 - Numeric abbreviated revisions rejected

Finding ID: BFA-M1-R5-002
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Validate top-level base/head revisions from their exact lexical fields.
Rationale: YAML numeric coercion must not invalidate a canonical Git abbreviation.
Validation target: code-review-m1-r6
Validation evidence: pending correction and R6

#### BFA-M1-R4-002 - Closed receipt validation rejects accepted manifests

Finding ID: BFA-M1-R4-002
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Admit canonical abbreviated revisions and test representative
accepted receipts for every allowed review family while retaining closed fields.
Rationale: A release gate must accept its own settled lifecycle evidence.
Validation target: code-review-m1-r5
Validation evidence: pending correction and R5

#### BFA-M1-R4-003 - Short PIN/auth values escape redaction

Finding ID: BFA-M1-R4-003
Disposition: accepted
Status: open
Owner: M1 implementer
Owning stage: review-resolution
Chosen action: Expand sensitive environment-name coverage and add short PIN,
API-key, and auth-code diagnostics regressions.
Rationale: Value length cannot determine whether authentication material is private.
Validation target: code-review-m1-r5
Validation evidence: pending correction and R5

### spec-review-r3

#### BFA-SR3-001 - Post-tag revalidation authority is contradictory and underspecified

Finding ID: BFA-SR3-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define a named publication-readiness phase that validates stored
R/C provenance, derives live H, recomputes release authorities, and uses
phase-correct local and remote tag requirements.
Rationale: Pre-tag candidate mode cannot be rerun after its forbidden local tag
has intentionally been created.
Validation target: spec-review-r4
Validation evidence: Spec-review R4 confirms the distinct publication-readiness phase is normative, but E3, BND-COMPOSE-001, and INT-004 still require composition alignment.

#### BFA-SR3-002 - R/C/H behavior is incompletely owned by the boundary record

Finding ID: BFA-SR3-002
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Map BFA-R017 to identity applicability and E4, retaining its
existing BND-AUTH-001 and INT-002 ownership.
Rationale: The formal record must trace the new provenance behavior consistently.
Validation target: spec-review-r4
Validation evidence: Spec-review R4 confirms identity applicability and E4 now consistently own BFA-R017 provenance.

### spec-review-r4

#### BFA-SR4-001 - Publication-readiness composition descriptions remain inconsistent

Finding ID: BFA-SR4-001
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Align E3, BND-COMPOSE-001, and INT-004 with strict validation
and publication readiness at H plus full release verification at T.
Rationale: The formal composition record must match the normative phase contract.
Validation target: spec-review-r5
Validation evidence: Spec-review R5 approves E3, BND-COMPOSE-001, and INT-004 alignment with R018 and R019.

### architecture-review-activation-r2

#### BFA-AR2-001 - Canonical component view exposes superseded authority model

Finding ID: BFA-AR2-001
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Update the focused diagram and canonical decision summary to
show candidate P/B/T/R, immediate R-to-C provenance, publication-readiness H,
and exact H handoff to the atomic publisher.
Rationale: One canonical package cannot expose two incompatible authority models.
Validation target: architecture-review-activation-r3
Validation evidence: Architecture-review R3 approves the diagram, exact-H authority edge, decision summary, and no-new-state-owner design.

### test-spec-review-r5

#### BFA-TSR5-001 - Proof rows omit direct producing commands and evidence

Finding ID: BFA-TSR5-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add actual candidate, readiness, and selector commands plus
their stage-owned evidence to every amended proof row.
Rationale: A proof row must cite the command and evidence that directly produce each claim.
Validation target: test-spec-review-r6
Validation evidence: Test-spec R6 confirms CMD13 and T16 producer chains were added; residual atomic/public rows are tracked separately as BFA-TSR6-001.

#### BFA-TSR5-002 - Readiness and publication serializers lack privacy-negative proof

Finding ID: BFA-TSR5-002
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Inject private sentinels through M2 readiness and evidence
serialization, assert all output/evidence suppresses them, and map R034 to T12/MP1.
Rationale: Candidate redaction cannot prove a separate serializer boundary.
Validation target: test-spec-review-r6
Validation evidence: Test-spec R6 confirms direct M2 sentinel and MP1 scan partitions; residual M2 evidence ownership is tracked as BFA-TSR6-002.

### test-spec-review-r6

#### BFA-TSR6-001 - Hybrid proof rows omit atomic and public evidence producers

Finding ID: BFA-TSR6-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add CMD17 and CMD18 to PRF-004 and PRF-012.
Rationale: Rows claiming atomic and public evidence must cite their producers.
Validation target: test-spec-review-r7
Validation evidence: Test-spec-review R7 confirms CMD17/CMD18 producer closure.

#### BFA-TSR6-002 - T12 privacy proof lacks M2 evidence and milestone ownership

Finding ID: BFA-TSR6-002
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Add M2 implementation evidence and milestone ownership to T12,
include T12 in the M2 proof map, and cite T12/MP1 in the privacy summary.
Rationale: Fixture serializer proof and actual release evidence require distinct owners.
Validation target: test-spec-review-r7
Validation evidence: Test-spec-review R7 confirms M2 fixture and MP1 actual privacy ownership.

## Clean review receipts

### code-review-m1-r8

Status: approved
Material findings: none
Resolution required: closes all remaining M1 receipt-authority findings
Evidence: reviews/code-review-m1-r8.md

### test-spec-review-r7

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-TSR6-001 and BFA-TSR6-002 closure
Evidence: reviews/test-spec-review-r7.md

### plan-review-r4

Status: approved
Material findings: none
Resolution required: no new findings; approves P/B/T/R/C/H sequencing and same-invocation exact-H publication intent
Evidence: reviews/plan-review-r4.md

### architecture-review-activation-r3

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-AR2-001 closure and architecture settlement
Evidence: reviews/architecture-review-activation-r3.md

### spec-review-r5

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-SR4-001 closure and approves the corrected R/C/H publication-readiness contract
Evidence: reviews/spec-review-r5.md

### test-spec-review-r4

Status: approved
Material findings: none
Resolution required: no new findings; approves the CMD4 selector-surface amendment made for BFA-M1-CR1-005
Evidence: reviews/test-spec-review-r4.md

### test-spec-review-r3

Status: approved
Material findings: none
Resolution required: no new findings; confirms all test-spec-review R1 and R2 findings are closed
Evidence: reviews/test-spec-review-r3.md

### proposal-review-r3

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-PR1-001 and BFA-PR2-001 closure
Evidence: reviews/proposal-review-r3.md

### proposal-review-r4

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-SR1-002 closure
Evidence: reviews/proposal-review-r4.md

### spec-review-r2

Status: approved
Material findings: none
Resolution required: no new findings; confirms BFA-SR1-001, BFA-SR1-003, and BFA-SR1-004 closure
Evidence: reviews/spec-review-r2.md

### architecture-review-activation-r1

Status: approved
Material findings: none
Resolution required: no new findings; canonical architecture and activation-publication ADR are approved
Evidence: reviews/architecture-review-activation-r1.md

### plan-review-r3

Status: approved
Material findings: none
Resolution required: no new findings; confirms all plan-review R1 and R2 findings are closed
Evidence: reviews/plan-review-r3.md

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Every rejected finding has rationale.
- [x] Every deferred finding has follow-up or explicit no-follow-up rationale.
- [x] Every `needs-decision` finding is resolved or blocks closeout.
- [x] Validation evidence is recorded for the open M1 findings.
- [x] Closeout status is correct.
