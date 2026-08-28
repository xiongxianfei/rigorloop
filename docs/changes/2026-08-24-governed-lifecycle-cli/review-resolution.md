# Review Resolution: Governed Lifecycle CLI

## Summary

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-deadlock-r1
Review closeout: code-review-deadlock-r3
Review closeout: code-review-deadlock-r4

- Reviews covered: `spec-review-r1`, `architecture-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-deadlock-r1`, `code-review-deadlock-r3`, `code-review-deadlock-r4`, `code-review-deadlock-r5`, `code-review-deadlock-r6`
- Findings resolved: 12
- Unresolved findings: 0
- Second review required: yes
- Second review satisfied: yes
- Second-review agreement: clean on exact packet `sha256:cbe4dbd0498986725451767552f2d7b198ed2fbc462c13197ee53c2f210126b2`
- Second-review evidence: `reviews/code-review-deadlock-r5.md`; `reviews/code-review-deadlock-r6.md`
- Current result: R5 and R6 independently agree that the exact frozen packet resolves CR1, CR2, and CR3. The elevated-risk correction review gate is closed; final verification remains not claimed.

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RLCLI-SR1 | accepted | resolved | Added the normative evidence-invalidation matrix and architecture constraint. |
| RLCLI-SR2 | accepted | resolved | Defined recovery-bundle, restoration, blocking, and repair outcomes. |
| RLCLI-SR3 | accepted | resolved | Separated stale-envelope failure from current-revision already-recorded success. |
| RLCLI-AR1 | accepted | resolved | Reconciled canonical hash-policy statements with activated freshness identity. |
| RLCLI-AR2 | accepted | resolved | Selected pinned `yaml`, closed input domain, and deterministic serialization. |
| RLCLI-AR3 | accepted | resolved | Defined fixed lock/recovery paths, phases, ordering, refusal, and repair. |
| RLCLI-CR-M1-1 | accepted | resolved | Enforced complete operation-specific request contracts and closed values. |
| RLCLI-CR-M1-2 | accepted | resolved | Added and proved the closed version-one provenance exclusion set. |
| RLCLI-CR-M1-3 | accepted | resolved | Admitted and validated only the documented request-provenance vocabulary. |
| RLCLI-DEADLOCK-CR1 | accepted | resolved | Completion and workflow-selected start now preserve routing authority and synchronize active automation atomically. |
| RLCLI-DEADLOCK-CR2 | accepted | resolved | Supplied and projected replay now share evidence-complete identity, and duplicate canonical table or prose occurrences reject unchanged. |
| RLCLI-DEADLOCK-CR3 | accepted | resolved | Start and completion now fail closed on inconsistent remaining work and completion accepts only `review-requested`. |

### code-review-deadlock-r1

#### RLCLI-DEADLOCK-CR1

Finding ID: RLCLI-DEADLOCK-CR1
Disposition: accepted
Rationale: The approved correction keeps continuation selection in workflow while allowing the CLI to validate and atomically apply only a closed workflow-selected `start-milestone` projection.
Status: resolved
Owner: governed-lifecycle CLI spec owner and workflow contract owner
Owning stage: spec
Decision owner: governed-lifecycle CLI spec owner and workflow contract owner
Decision needed: none; the spec owner selected workflow-owned continuation with closed CLI application of `start-milestone`.
Final action: Revised and approved R16/R31, architecture, and T09; removed routing from `complete-milestone`; added eligibility output; made `start-milestone` synchronize `workflow_state` and active automation routing atomically; added contradiction and no-routing regressions.
Stop state: resolved by independent L1 review of the exact corrected packet.
Required outcome: One non-contradictory routing authority model with coherent lifecycle projections and direct proof.
Follow-up: final verification.
Validation target: `packages/rigorloop/test/lifecycle-milestone.test.js`; current reviewed spec, test-spec, and architecture identities.
Validation evidence: `reviews/spec-review-r5.md`; `reviews/test-spec-review-r5.md`; `reviews/architecture-review-r5.md`; `evidence/deadlock-completion-replay-correction-r1.md`; `reviews/code-review-deadlock-r3.md`; `reviews/code-review-deadlock-r4.md`

#### RLCLI-DEADLOCK-CR2

Finding ID: RLCLI-DEADLOCK-CR2
Disposition: accepted
Rationale: Exact replay is valid only while all evidence that authorized the original completion remains identity-equal; checking only the milestone proof and receipt permits stale canonical-log or packet facts to pass.
Status: resolved
Owner: implement
Owning stage: implement
Decision owner: none
Decision needed: none
Final action: Replaced projected status-only completion with exact review-record reconstruction and the same normalized fingerprint used by supplied reviews; canonical lookup now requires exactly one prose or table occurrence.
Stop state: resolved by independent L1 R5 and R6 clean agreement at packet `sha256:cbe4dbd0498986725451767552f2d7b198ed2fbc462c13197ee53c2f210126b2`; elevated-risk second review is satisfied.
Required outcome: Review-log-only drift and non-proof packet-only drift reject without lifecycle mutation; an identity-equal replay remains `already-recorded`.
Follow-up: final verification.
Validation target: `packages/rigorloop/test/lifecycle-milestone.test.js`
Validation evidence: `evidence/deadlock-completion-replay-correction-r1.md`; `reviews/code-review-deadlock-r4.md`; `reviews/code-review-deadlock-r5.md`; `reviews/code-review-deadlock-r6.md`; both independent reviews passed C05 16/16; R6 selected probes passed 4/4; duplicate table and direct duplicate-prose probes rejected with byte-identical lifecycle state

### code-review-deadlock-r4

#### RLCLI-DEADLOCK-CR3

Finding ID: RLCLI-DEADLOCK-CR3
Disposition: accepted
Rationale: R16 and the stage-owned lifecycle contract require exact current-milestone, remaining-work, review-state, and legal-transition enforcement before workflow mutation.
Status: resolved
Owner: implement
Owning stage: implement
Decision owner: none
Decision needed: none while enforcing the current approved contract
Required outcome: `start-milestone` rejects inconsistent remaining implementation IDs, and `complete-milestone` cannot skip the required `review-requested` source state; every rejection preserves lifecycle bytes.
Safe resolution path: add shared fail-closed milestone-prestate validation plus public-CLI regressions, rerun C05 and lifecycle tests, then submit a new exact packet for independent rereview.
Final action: Added exact remaining-implementation projection validation before mutation and restricted completion to the legal `review-requested -> closed` transition, with public-CLI byte-unchanged regressions.
Stop state: resolved by independent L1 R5 and R6 clean agreement at packet `sha256:cbe4dbd0498986725451767552f2d7b198ed2fbc462c13197ee53c2f210126b2`; elevated-risk second review is satisfied.
Follow-up: final verification
Validation target: `packages/rigorloop/dist/lib/lifecycle-operations.js`; `packages/rigorloop/test/lifecycle-milestone.test.js`
Validation evidence: `reviews/code-review-deadlock-r4.md`; `reviews/code-review-deadlock-r5.md`; `reviews/code-review-deadlock-r6.md`; both independent reviews passed C05 16/16, including inconsistent-remaining-work and illegal-source-transition byte-unchanged regressions; R6 selected probes passed 4/4

### code-review-m1-r2

#### RLCLI-CR-M1-3

Finding ID: RLCLI-CR-M1-3
Disposition: accepted
Rationale: Every approved request shape must be representable while unknown provenance continues to fail closed.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Admitted only `actor` and `recorded_at`, validated non-empty actor and calendrically valid RFC 3339 timestamp values, and added accepted, malformed, and unknown-field regressions.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`
Validation evidence: `evidence/m1-correction-r2.md`; formal rereview pending

### code-review-m1-r1

#### RLCLI-CR-M1-1

Finding ID: RLCLI-CR-M1-1
Disposition: accepted
Rationale: Incomplete requests must fail before transition consistency or mutation.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Added closed per-operation required fields and validators for identifiers, paths, review authority, migration source version, repair conditions, and repair acknowledgment.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`
Validation evidence: `evidence/m1-correction-r1.md`; formal rereview pending

#### RLCLI-CR-M1-2

Finding ID: RLCLI-CR-M1-2
Disposition: accepted
Rationale: The versioned lifecycle identity contract must exclude only documented provenance.
Status: resolved
Owner: implement
Owning stage: implement
Final action: Added the version-one `actor` and `recorded_at` exclusion set to code and the shared fixture, with regressions proving excluded provenance is stable and workflow state remains identity-relevant.
Validation target: `packages/rigorloop/test/lifecycle-contract.test.js`; shared conformance fixture
Validation evidence: `evidence/m1-correction-r1.md`; formal rereview pending

### spec-review-r1

#### RLCLI-SR1

Finding ID: RLCLI-SR1
Disposition: accepted
Rationale: Evidence freshness is a product contract and cannot be delegated to architecture.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Added the closed first-release evidence-invalidation matrix and made architecture subordinate to its outcomes.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`

### architecture-review-r1

#### RLCLI-AR1

Finding ID: RLCLI-AR1
Disposition: accepted
Rationale: Current canonical architecture must not contain both hash-based freshness and an unconditional no-hash rule.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Qualified every legacy no-hash statement and made ADR-20260824 the scoped successor for activated freshness identities.
Validation target: canonical architecture at `sha256:911aafdbec7f124d92705dd0364183c7a4a805f8963a359553e17d343d2b3c95`
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-AR2

Finding ID: RLCLI-AR2
Disposition: accepted
Rationale: YAML parsing is a security, compatibility, dependency, and deterministic-output architecture choice.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Selected the pinned `yaml` dependency, rejected unsafe YAML constructs, and defined normalized schema-ordered UTF-8/LF serialization.
Validation target: revised architecture and ADR identities from architecture-review r2
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-AR3

Finding ID: RLCLI-AR3
Disposition: accepted
Rationale: Same-worktree serialization and recovery must have one fault-injectable protocol before planning.
Status: resolved
Owner: architecture
Owning stage: architecture
Final action: Fixed sibling paths, exclusive-create semantics, modes, phases, recovery ordering, refusal behavior, cleanup, and orphan-lock repair.
Validation target: revised architecture and ADR identities from architecture-review r2
Validation evidence: `evidence/architecture-revision-r1.md`; `reviews/architecture-review-r2.md`

#### RLCLI-SR2

Finding ID: RLCLI-SR2
Disposition: accepted
Rationale: Atomicity and recovery require one observable outcome across crashes and post-validation failure.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Added a verified recovery bundle, automatic restore, recovery-blocked state, and named reconciliation repair contract.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`

#### RLCLI-SR3

Finding ID: RLCLI-SR3
Disposition: accepted
Rationale: The stale-revision invariant and idempotent result must be simultaneously testable.
Status: resolved
Owner: spec
Owning stage: spec
Final action: Preserved fail-closed stale revisions and defined current-revision equivalent operations as already recorded only when durable facts are identical.
Validation target: `specs/governed-lifecycle-cli.md` at `sha256:f7d9984c6913f5326cce231874f57673835c25ed1d4c94a03bdf4437eba8e405`
Validation evidence: `evidence/spec-revision-r1.md`; `reviews/spec-review-r2.md`
