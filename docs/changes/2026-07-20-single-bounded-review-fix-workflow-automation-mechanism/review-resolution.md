# Review Resolution: Single Bounded Review-Fix Workflow Automation Mechanism

## Summary

Closeout status: open

Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3
Review closeout: test-spec-review-r4
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m1-r4
Review closeout: code-review-m1-r5
Review closeout: code-review-m1-r6
Review closeout: code-review-m1-r7
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2
Review closeout: code-review-m3-r3
Review closeout: code-review-m3-r4
Review closeout: code-review-m3-r5
Review closeout: code-review-m3-r6
Review closeout: code-review-m3-r7
Review closeout: code-review-m3-r8
Review closeout: code-review-m3-r9
Review closeout: code-review-m4-r1
Review closeout: code-review-m4-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `architecture-review-r1`, `architecture-review-r2`, `architecture-review-r3`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `test-spec-review-r3`, `test-spec-review-r4`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m1-r4`, `code-review-m1-r5`, `code-review-m1-r6`, `code-review-m1-r7`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`, `code-review-m3-r1`, `code-review-m3-r2`, `code-review-m3-r3`, `code-review-m3-r4`, `code-review-m3-r5`, `code-review-m3-r6`, `code-review-m3-r7`, `code-review-m3-r8`, `code-review-m3-r9`, `code-review-m4-r1`, `code-review-m4-r2`
- Findings resolved: 57
- Unresolved findings: 2
- Current result: Code-review M4 R2 classified `BRF-M4-CR1` and `BRF-M4-CR2` as failed remediations and opened `BRF-M4-CR3` and `BRF-M4-CR4`. M4 remains resolution-needed; M5 is blocked.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| BRF-PR1 | accepted | resolved | Defined pre-plan derivation and the plan-creation ownership handoff; R2 confirmed resolution. |
| BRF-PR2 | accepted | resolved | Bound grants to concrete reviewed identities, scope, and invalidation rules; R2 confirmed resolution. |
| BRF-PR3 | accepted | resolved | Added write-ahead transition receipts and deterministic recovery; R2 confirmed resolution. |
| BRF-PR4 | accepted | resolved | Bound repeated targets to milestone occurrences and completion predicates; R2 confirmed resolution. |
| BRF-PR5 | accepted | resolved | Added a review-only effective authoring capability bound to the exact proposal identity and a separately based post-proposal capability; R3 confirmed resolution. |
| BRF-PR6 | accepted | resolved | Replaced the ambiguous grant invariant with distinct bounded parent authorization and effective capability contracts; R4 confirmed resolution. |
| BRF-PR7 | accepted | resolved | Separated review occurrence from clean-gate satisfaction and defined all four closed outcome routes; R4 confirmed resolution. |
| BRF-SR1 | accepted | resolved | Added deterministic stage-to-occurrence compatibility and repeated-target binding; spec-review R2 confirmed resolution. |
| BRF-SR2 | accepted | resolved | Added closed durable state, capability-kind, and transition vocabularies; spec-review R2 confirmed resolution. |
| BRF-SR3 | accepted | resolved | Added non-contingent verification-authorization timing; spec-review R2 confirmed resolution. |
| BRF-SR4 | accepted | resolved | Added mandatory migration-window command adapters and exact legacy-command mappings; spec-review R2 confirmed resolution. |
| BRF-SR5 | accepted | resolved | Replaced implicit preservation with a closed affected-selector registry and explicit contract ownership; spec-review R4 confirmed resolution. |
| BRF-SR6 | accepted | resolved | Made source selectors unique, updated intended references, and added uniqueness-before-consistency proof; spec-review R4 confirmed resolution. |
| BRF-AR1 | accepted | resolved | Completed the typed stage-policy projection against every field required by `BRF-R079`; R3 confirmed resolution. |
| BRF-AR2 | accepted | resolved | Selected one executable code boundary and one canonical first-version persistence surface and aligned the C4 roles; R3 confirmed resolution. |
| BRF-AR3 | accepted | resolved | Bound prepared receipts to effective capability IDs instead of an ambiguous grant identity; R3 confirmed resolution. |
| BRF-PL1 | accepted | resolved | Replaced obsolete or incomplete adapter commands and required executed selected-CI plus broad-smoke final-cutover proof; R2 confirmed resolution. |
| BRF-PL2 | accepted | resolved | Split stage integration and made one final milestone own atomic public activation; R2 confirmed resolution. |
| BRF-TSR1 | accepted | resolved | Added complete MP1-MP3 contracts and moved remaining checks into T22 automation; R2 confirmed resolution. |
| BRF-TSR2 | accepted | resolved | Replaced CMD30 with a pipe-free executable command and normalized CMD18's first required milestone; R2 confirmed resolution. |
| BRF-TSR3 | accepted | resolved | Added deterministic fixture controls and repeat/order-independence case T29; R2 confirmed resolution. |
| BRF-TSR4 | accepted | resolved | T29/T30 remain split and T26 has an explicit M4/M6 activation and deferral mapping; R4 confirmed resolution. |
| BRF-M1-CR1 | accepted | resolved | Capability occurrence validation now derives from the immutable registry for public and internal stages and requires milestone identity. |
| BRF-M1-CR2 | accepted | resolved | Stage basis and invalidation records now require concrete values and closed trigger/action behavior. |
| BRF-M1-CR3 | accepted | resolved | Receipts now validate the requested structural run/change/policy/capability bindings; R2 records distinct semantic gaps separately. |
| BRF-M1-CR4 | accepted | resolved | The requested matrix expansion is present; R2 records incorrect contrast semantics and remaining gaps separately. |
| BRF-M1-CR5 | accepted | resolved | Receipt destinations now match the run while capability operations are independently bounded by the run and parent targets; evidence values are concrete. |
| BRF-M1-CR6 | accepted | resolved | Contrast tests now cover later destinations, operation bounds, complete parent targets, and placeholder evidence. |
| BRF-M1-CR7 | accepted | resolved | Parent maximum targets now reuse the complete structured-target validator. |
| BRF-M1-CR8 | accepted | resolved | Canonical predecessor and graph reachability now come from the immutable typed stage-policy projection; validator-local rank/frontier policy was removed. |
| BRF-M1-CR9 | accepted | resolved | Recursive evidence validation now rejects stripped-empty strings, non-finite numbers, cycles, and excessive nesting while accepting finite values. |
| BRF-M1-CR10 | accepted | resolved | Exact-target frontier checks replaced cyclic reachability; R5 classified the broader predicate-enforcement remediation as failed and records the remaining defect separately in `BRF-M1-CR11`. |
| BRF-M1-CR11 | accepted | resolved | One typed evaluator now enforces target frontier, guard evidence, and occurrence constraints; structural helpers cannot authorize execution. |
| BRF-M1-CR12 | accepted | resolved | The next-milestone edge admits repeated targets only when their persisted occurrence equals the identity-bound next milestone. |
| BRF-M2-CR1 | accepted | resolved | Recovery resolves the exact persisted receipt by transition ID and rejects absent, mismatched, or non-unique prepared bindings. |
| BRF-M2-CR2 | accepted | resolved | Recovery derives retry behavior from the immutable stage policy; required receipt projections must match and are transition-key-bound. |
| BRF-M2-CR3 | accepted | resolved | T29 now repeats and reverses fresh-root transition/migration scenarios and compares receipts, keys, migration evidence, canonical bytes, and teardown. |
| BRF-M2-CR4 | accepted | resolved | Unified status queries use the canonical validated read boundary and return stable read-only errors for malformed state. |
| BRF-M2-CR5 | accepted | resolved | Canonical validation owns deterministic key computation; read, recovery, cancellation, and query reject stale prepared or completed receipts. |
| BRF-M2-CR6 | accepted | resolved | All retry families now use complete persisted states that pass canonical read before decision evaluation, with mismatch rejection per family. |
| BRF-M3-CR1 | accepted | resolved | Coordination now derives canonical position, binds complete observed identities to basis and receipt inputs, and rejects unknown, missing, stale, or contradictory evidence before invocation. |
| BRF-M3-CR2 | accepted | resolved | One policy projection now supplies target completion for binding, resume, and durable validation; every public-stage tamper fails closed. |
| BRF-M3-CR3 | accepted | resolved | Proposal and implementation correction capabilities now require current positive budget scope and identity within the parent maximum. |
| BRF-M3-CR4 | accepted | resolved | Typed stage completion and canonical synchronization results are validated before completion; unsafe outcomes pause without consuming authority. |
| BRF-M3-CR5 | accepted | resolved | Implementation-correction basis now requires the concrete correction-budget identity and must match bounded scope exactly. |
| BRF-M3-CR6 | accepted | resolved | Added policy-derived postconditions, repository path/hash checks, and durable synchronization fields; R3 records the remaining semantic and recovery gap separately as `BRF-M3-CR7`. |
| BRF-M3-CR7 | accepted | resolved | Added parser-valid review and occurrence checks; R4 records the remaining canonical-path and canonical-identity gap separately as `BRF-M3-CR8`. |
| BRF-M3-CR8 | accepted | resolved | Canonical completion paths reject symlinks and bind log identity; R5 records the remaining repository-root binding gap separately as `BRF-M3-CR9`. |
| BRF-M3-CR9 | accepted | resolved | The state store now owns one immutable canonical repository root and rejects foreign-root coordination or finalization before mutation. |
| BRF-M3-CR10 | accepted | resolved | Lifecycle state sync now requires `review-findings-open` exactly when structured formal review evidence has open accepted findings. |
| BRF-M3-CR11 | accepted | resolved | Canonical construction now derives the exact lexical repository root, rejects symlinked metadata paths and ancestor roots, and exposes no finalizer root override. |
| BRF-M3-CR12 | accepted | resolved | Live open-review detail now carries an exact count/ID projection and forbids independent finding claims in its remainder. |
| BRF-M3-CR13 | accepted | resolved | Canonical construction now checks every absolute lexical component through `change.yaml` before resolution, including ancestors above the derived root. |
| BRF-M3-CR14 | accepted | resolved | The review-state remainder now rejects every additional structured field as well as independent finding claims and IDs. |
| BRF-M3-CR15 | accepted | resolved | Replaced the prefix-plus-remainder parser and denylist with exact equality against one generated open/closed formal review-state projection. |
| BRF-M4-CR1 | accepted | resolved | Connected the non-public authoring route to prepared receipts, capability consumption, canonical synchronization, and parser-backed completion for every M4 stage. |
| BRF-M4-CR2 | accepted | resolved | Replaced caller authority booleans with capability-derived correction authority and bound review, finding, classification, budget, path, and proposal mutation evidence. |
| BRF-M4-CR3 | needs-decision | open | Completed non-review recovery requires irrelevant review-log evidence, all-stage proof remains registry-only, and post-verification routing rereads unbound paths. |
| BRF-M4-CR4 | needs-decision | open | Correction still trusts caller dictionaries, accepts invalid budget state, and omits independent post-mutation convergence plus fresh-review authority. |

## Common Resolution Metadata

- Owner: proposal owner
- Owning stage: proposal
- Validation target: Proposal-review closeout and proposal lifecycle normalization before specification
- Validation evidence: Focused validation passed and proposal-review R4 approved with no material findings

## Finding Details

### code-review-m4-r2

#### BRF-M4-CR3 - Non-review authoring completion is not durably recoverable

Finding ID: BRF-M4-CR3
Disposition: needs-decision
Status: open
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Confirm the recorded stage-generic recovery and verifier-normalized routing correction.
Rationale: A completed authored-artifact receipt cannot resume because recovery requires a formal-review log identity that its valid proof cannot contain.
Required outcome: Every M4 stage must have stage-appropriate completion and completed-recovery proof that compares the originally persisted identities without requiring irrelevant review-log evidence, and route selection must use verifier-normalized proof or recheck the exact identity.
Chosen action: Pending user acceptance of the safe resolution.
Safe resolution path: Make completed recovery compare the complete normalized identity map generically, condition review-log checks on formal-review proof, route from verified proof or rehash before parsing, and add positive recovery plus drift contrasts for every M4 stage family.
Validation target: Stage-semantic completion/recovery matrix, CMD14-CMD20, full engine/state/validator suites, broad smoke when selected, and code-review M4 R3.
Validation evidence: R2 source-level proof shows non-review proof lacks `-log` while completed recovery requires it; the registry equality and representative spec transaction do not exercise recovery.

#### BRF-M4-CR4 - Correction authority and convergence remain caller-substitutable

Finding ID: BRF-M4-CR4
Disposition: needs-decision
Status: open
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Confirm the recorded repository-backed authority and post-mutation convergence correction.
Rationale: Hashing caller dictionaries against opaque identities does not derive current review-resolution evidence, and preflight returns before the post-mutation obligations that the composed coordinator never re-evaluates.
Required outcome: Correction authority and convergence must come from current repository-backed review, resolution, classifier, budget, and proposal evidence; invalid budgets must pause; post-mutation proof must establish strict shrinkage, validation, identity change, preserved history, stale gate, and fresh proposal-review authority.
Chosen action: Pending user acceptance of the safe resolution.
Safe resolution path: Parse capability-bound review/resolution paths through repository parsers, recompute persisted structured identities, validate the exact closed budget, split preflight from independent post-mutation evaluation, persist stale-gate/history proof, and derive fresh review authority before rereview routing.
Validation target: Forged caller, stale persisted budget, empty/extra/over-limit budget, false shrinkage/validation, unchanged identity, old-review reuse, and fresh-capability tests; CMD14-CMD20; broad smoke when selected; code-review M4 R3.
Validation evidence: R2 directly reproduced empty-budget correction routing, preflight authorization with false deterministic validation and unchanged identities, and persisted budget content drift accepted without identity recomputation.

### code-review-m4-r1

#### BRF-M4-CR1 - Authoring integration is not connected to the transactional engine

Finding ID: BRF-M4-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's implementation request accepted the recorded safe resolution.
Rationale: Pure decisions called only by tests cannot establish stage invocation, prepared-receipt ordering, stage-native completion, canonical synchronization, or durable resume behavior.
Required outcome: Provide one explicitly non-public receipt-backed path through every M4 stage to `test-spec-review`, using exact effective capabilities and stage-native evidence without exposing public or legacy entry.
Chosen action: Implement the non-public transition harness through the existing coordinator and state writer, add stage-native completion verifiers for every M4 stage, and replace helper-only positives with transactional temporary-repository proof.
Safe resolution path: Add stage-specific completion verification, compose it through `coordinate_one_stage`, and replace helper-only positives with temporary-repository transition fixtures covering receipt, invocation, synchronization, exact target, conditional applicability, and isolation behavior.
Validation target: CMD14-CMD20, direct state/receipt integration contrasts for every M4 stage, MP1, selector routing, broad smoke when selected, and code-review M4 R2.
Validation evidence: Receipt-backed spec and proposal-correction integration tests pass; all eleven M4 authoring stages have closed verifier registration; the full 33-test engine, 49-test state/recovery, 52-test automation-validator, CMD14-CMD20, Python compilation, diff checks, and repository broad smoke pass.

#### BRF-M4-CR2 - Proposal correction trusts unbound caller assertions

Finding ID: BRF-M4-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's implementation request accepted the recorded safe resolution.
Rationale: Correction authority and convergence cannot be established from caller assertions, and an optional reviewed-classification map cannot detect every new or changed finding class.
Required outcome: Resolve correction authority, finding/classification state, budget identity, path scope, validation evidence, and proposal identities from the exact current persisted capability and repository evidence; omission or drift must pause or fail closed.
Chosen action: Resolve correction from the canonical capability and repository-backed review/correction evidence, require classification history and budget identity, verify the resulting proposal identity, and force fresh proposal review authority.
Safe resolution path: Replace boolean/string inputs with a canonical capability ID and repository-backed review-resolution/proposal evidence, require old and current classification identities, bind the budget identity, record mutation under a prepared receipt, invalidate the old review, and derive a fresh proposal-review capability.
Validation target: Add omission, forged authority, changed classification, stale budget, forged validation/identity, and old-review continuation regressions; rerun CMD14-CMD20, broad smoke when selected, and code-review M4 R2.
Validation evidence: The correction-capability resolver rejects forged finding sets and stale basis identities; classification history is mandatory; exhausted budget, changed class, stale review, expanded path/scope, non-shrinking findings, and missing deterministic validation pause; receipt-backed correction proves a changed proposal identity and consumes the exact capability before rereview routing. CMD14-CMD20 and repository broad smoke pass.

### code-review-m3-r9

No material findings; no additional review resolution is required.

### code-review-m3-r8

#### BRF-M3-CR15 - Review-state remainder remains an open vocabulary

Finding ID: BRF-M3-CR15
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's implementation request accepted the review's safe resolution.
Rationale: Restricted key matching and selected prose tokens cannot prove that an unrestricted authoritative remainder contains no equivalent review-state assertion.
Required outcome: The complete live review-state detail must use one closed representation for both open and closed formal state, with no unrestricted remainder.
Chosen action: Require the entire live detail after the em dash to equal `review-state=<open|closed>; open-count=<n>; open-findings=<none|sorted IDs>`, remove all remainder scanners, preserve terminal history, and add exact open/closed plus alternate-key/plain-prose regressions.
Safe resolution path: Make the text after the em dash exactly `review-state=<open|closed>; open-count=<n>; open-findings=<none|sorted IDs>`; require it in both states, remove the remainder scanners, update active-plan and fixture defaults, and add exact open/closed plus alternate-key/prose negative regressions.
Validation target: Focused state-sync contrasts, full lifecycle regressions, artifact validation, broad smoke when selected, and code-review M3 R9.
Validation evidence: The proof-first contrasts failed before correction. After correction, focused open/closed contrasts, the complete 156-test lifecycle suite, M3 state/engine/validator/review-parser/compile suites, selected artifact checks, and the 11-check repository broad smoke pass.

### code-review-m3-r7

#### BRF-M3-CR13 - Earlier lexical ancestor symlink still rebinds canonical ownership

Finding ID: BRF-M3-CR13
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's implementation request accepted the existing safe resolution.
Rationale: Checking only the derived root and its descendants permits a symlink earlier in the absolute metadata path to disappear during resolution and change the repository owner.
Required outcome: Canonical metadata construction must reject any symlink in the lexical canonical path chain that can redirect repository identity before read or root binding.
Chosen action: Walked the absolute lexical path from its anchor through `change.yaml`, rejecting any symlink before calling `resolve()`, while retaining exact explicit-root and change-directory identity checks.
Safe resolution path: Validate components from the absolute path anchor through `change.yaml` without following symlinks, or use an equivalent no-follow descriptor boundary; add an earlier-ancestor symlink regression and preserve normal canonical paths.
Validation target: State/recovery tests, direct ancestor-chain contrasts, CMD10-CMD14, broad smoke when selected, and code-review M3 R8.
Validation evidence: The proof-first earlier-ancestor symlink test failed before production correction and now passes. All 48 state/recovery tests, 23 engine tests, CMD10-CMD14, Python compilation, and the 11-check broad-smoke boundary pass.

#### BRF-M3-CR14 - Review-state remainder permits a second contradictory state claim

Finding ID: BRF-M3-CR14
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's implementation request accepted the reserved structured review-state namespace.
Rationale: Screening only `finding(s)` and uppercase finding IDs does not prevent a second `review-state`, `open-count`, or alternate open-state key from contradicting the validated projection.
Required outcome: Live bounded detail must contain exactly one authoritative review-state projection and no second structured or equivalent review-state claim in its remainder.
Chosen action: Reserved all structured `key=value` fields to the single leading projection and rejected any additional structured field, finding word, or finding-shaped ID in the remainder.
Safe resolution path: Reserve and reject review-state keys outside the leading projection while keeping the remainder explicitly non-authoritative; add full-validator second-projection and zero-open/unstructured-state regressions.
Validation target: Focused state-sync contrasts, full lifecycle regressions, artifact validation, broad smoke when selected, and code-review M3 R8.
Validation evidence: Both proof-first full-validator reproductions failed before production correction and now pass. All 154 lifecycle tests, 52 automation-validator tests, 103 review-parser tests, Python compilation, and the 11-check broad-smoke boundary pass.

### code-review-m3-r2

#### BRF-M3-CR5 - Implementation-correction budget identity is not bound to its basis

Finding ID: BRF-M3-CR5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the user's request to apply the deterministic safe resolution.
Rationale: Implementation-correction basis omits correction-budget identity, so derivation and durable validation accept any non-empty scope identity when the optional basis field is absent.
Required outcome: Require a concrete correction-budget identity in every correction capability basis and exact equality with its bounded scope identity.
Chosen action: Added `correction_budget_identity` to the implementation-correction basis contract, made basis/scope equality unconditional for both correction kinds, and added missing, mismatched, and matching derivation and durable-validation contrasts.
Safe resolution path: Add the identity to implementation-correction basis requirements, compare it unconditionally for both correction kinds, and add derivation plus durable-validation contrasts for missing, arbitrary, changed, and matching identities.
Validation target: CMD12, full automation-validator regressions, direct unbound-identity rejection, and code-review M3 R3.
Validation evidence: The proof-first missing-basis test failed before the correction. CMD12, all 18 engine tests, all 52 automation-validator tests, all 30 state-writer tests, all 149 lifecycle tests, all 53 metadata tests, Python compilation, diff checks, and the final 12-check broad-smoke suite now pass; missing or mismatched identities fail closed.

#### BRF-M3-CR6 - Typed callback claims still substitute for stage completion and canonical reread

Finding ID: BRF-M3-CR6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the user's request to apply the deterministic safe resolution.
Rationale: Callback-returned mappings are trusted as completion and synchronization without inspecting a stage-owned artifact or independently rereading canonical state; completed durable receipts also require only synchronized status.
Required outcome: Establish completion from repository-owned stage evidence, synchronize through the canonical owner, reread it independently, and durably validate the proof before consuming authority.
Chosen action: Removed caller-selected postconditions; the coordinator now derives them from immutable stage policy, requires typed repository-relative artifact references within capability scope, rereads and hashes those artifacts after invocation and synchronization, and persists exact synchronization evidence plus engine-derived observed identities. R3 records the remaining semantic verification and recovery gap as `BRF-M3-CR7`.
Safe resolution path: Separate invocation from evidence inspection, derive postconditions from policy, inspect real stage evidence after invocation, synchronize and reread canonical state through its owner, require completed receipt sync evidence/identities, and add fake/no-artifact/no-write/stale-reread/valid-fixture contrasts.
Validation target: CMD12-CMD14, full engine/state/validator regressions, direct no-artifact and evidence-free completed-receipt rejection, and code-review M3 R3.
Validation evidence: Proof-first tests failed before `ArtifactEvidence` existed. The corrected contrasts reject absent artifacts, stale identities, failed synchronization, caller-defined postconditions, and evidence-free completed receipts; the valid file-backed fixture completes and consumes capability authority. R3 found the narrower remaining semantic-verification and recovery defect recorded in `BRF-M3-CR7`.

### code-review-m3-r3

#### BRF-M3-CR7 - Path labels substitute for stage-native completion and recovery proof

Finding ID: BRF-M3-CR7
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the user's request to apply the deterministic safe resolution.
Rationale: Path and SHA-256 checks establish artifact identity but not the stage-owned semantic completion predicate. The synchronization callback can echo the same evidence mapping, while recovery and cancellation accept caller-supplied evidence without locating or parsing any artifact.
Required outcome: Completion and recovery must use stage-native semantic evidence and an independent canonical-owner reread before a receipt becomes completed or a capability becomes consumed.
Chosen action: Exposed bounded formal-review record and review-log parsers from the repository review validator, added a fail-closed proposal-review completion verifier in the state/reconciliation boundary, bound the parsed review target to the receipt proposal identity, required a matching canonical review-log occurrence, enforced the verifier before state-writer completion, and reused it for prepared/completed recovery and cancellation. Unsupported later-stage verifiers remain fail-closed until their owning M4/M5 integration milestones.
Safe resolution path: Add one policy-owned evidence verifier/reader contract per stage that reuses existing review, lifecycle, plan, and verification parsers. Route coordinator completion, prepared-receipt recovery, and cancellation through it; independently re-resolve canonical state after synchronization; and add arbitrary-bytes, malformed-review, identity/outcome mismatch, no-write, stale-reread, nonexistent-recovery, and valid parser-produced fixtures.
Validation target: CMD12-CMD14, full engine/state/validator regressions, direct semantic-artifact and recovery contrasts, and code-review M3 R4.
Validation evidence: Proof-first tests reproduced arbitrary review bytes and nonexistent recovery evidence completing or consuming authority before the fix. After the correction, CMD10-CMD14 pass; 14 capability tests, 33 state/recovery tests, 52 durable validator tests, and 103 review-parser tests pass. Direct contrasts reject arbitrary or malformed review evidence, unknown outcomes, wrong reviewed-artifact identity, missing canonical-log synchronization, nonexistent recovery artifacts, and disappeared completed-receipt canonical evidence; the parser-produced valid review fixture completes and consumes authority exactly once. The required broad-smoke suite passed all 11 checks in 436 seconds.

### code-review-m3-r4

#### BRF-M3-CR8 - Canonical review-log path and identity are not authority-bound

Finding ID: BRF-M3-CR8
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the deterministic safe resolution was accepted.
Rationale: The formal review artifact is path- and hash-bound, but the canonical review log is followed without repository containment and its identity is absent from completed receipt evidence.
Required outcome: Canonical review-log evidence must remain inside its repository-owned location, and its independently observed identity must be persisted and compared before normal completion, prepared/completed recovery, cancellation, or capability consumption.
Chosen action: Added one repository-file resolver that rejects absolute paths, traversal, missing files, and every symlinked path component for reviewed artifacts, review targets, and canonical logs. The shared stage-native verifier now returns normalized completion proof with independently observed review-record and review-log identities. Finalization and cancellation persist only that proof, and completed recovery compares the current log identity with the receipt before continuing.
Safe resolution path: Resolve every canonical-owner path through one containment checker; reject absolute paths, traversal, and symlink escape; return engine-derived normalized canonical identities from the shared verifier; persist the review-log identity; and make recovery/cancellation consume only that verified normalized proof. Add external/in-repository symlink, canonical-log identity drift, mismatched occurrence, missing log, and valid parser-produced fixtures.
Validation target: CMD12-CMD14, full engine/state/validator regressions, direct canonical-path and canonical-identity contrasts, and code-review M3 R5.
Validation evidence: Proof-first tests reproduced five unsafe outcomes before the correction: external and in-repository log symlinks reconciled, canonical-log drift continued, cancellation consumed authority from an external log, and caller-selected log identity was persisted. After the correction, CMD10-CMD14 pass; all 22 engine, 40 state/recovery, 52 automation-validator, and 103 review-parser tests pass. The new contrasts reject both symlink forms without consuming authority, reject mismatched canonical occurrences, pause on canonical-log drift, persist verifier-derived identities in normal completion and cancellation, and continue with unchanged valid proof. All five selector-chosen focused checks pass, and the final required repository broad-smoke suite passed all 11 checks in 445 seconds. Awaiting code-review M3 R5.

### code-review-m3-r5

#### BRF-M3-CR9 - Completion evidence root is not bound to canonical state

Finding ID: BRF-M3-CR9
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's request accepted the deterministic safe resolution.
Rationale: Path-level containment is enforced relative to a root, but the caller can choose a root unrelated to the state store's metadata and consume authority from copied evidence there.
Required outcome: Completion, recovery, and cancellation evidence must resolve only against the repository that canonically owns the persisted change metadata.
Chosen action: Bound each state store to one immutable canonical repository root, inferred that root from canonical change paths, validated the change-directory identity, rejected coordinator/root mismatch before invocation, and rejected finalization/root mismatch before any durable mutation.
Safe resolution path: Bind and validate one repository root at state-store construction, reject coordinator/root mismatch before invocation, remove per-finalization trust-root override, use the bound root across recovery/cancellation, and add a two-repository negative regression.
Validation target: CMD12-CMD14, full engine/state/validator regressions, direct cross-repository contrasts, and code-review M3 R6.
Validation evidence: Proof-first cross-repository tests failed before the correction. The direct coordinator and finalization contrasts now reject Repository B while preserving Store A byte-for-byte with its capability active and receipt prepared. All 23 engine tests and 43 state/recovery tests pass; canonical-layout tests also prove repository-root inference and change-directory identity rejection. Repository broad smoke passed all 11 checks in 443 seconds.

#### BRF-M3-CR10 - Authoritative handoff reason contradicts resolved review state

Finding ID: BRF-M3-CR10
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's request accepted deterministic handoff synchronization.
Rationale: The active plan owns post-plan workflow state but its handoff reason said one R4 finding remained open while every review evidence surface recorded zero open findings.
Required outcome: Current Handoff Summary, review resolution, review log, change metadata, and plan index must agree at every handoff.
Chosen action: Added a bidirectional lifecycle state-sync rule: open accepted material findings require `review-findings-open`, while a zero-open formal review summary forbids that reason code. Synchronized the active plan, plan index, review log, review resolution, and change metadata for the M3 R6 handoff.
Safe resolution path: Synchronize the plan from the actual R5 state, add a semantic state-sync regression for reason tokens and open-finding prose, and rerun lifecycle validation before rereview.
Validation target: lifecycle state-sync selection, full lifecycle regressions, review/metadata validation, and code-review M3 R6.
Validation evidence: Both proof-first semantic drift fixtures passed incorrectly before the correction and now fail with explicit `review-findings-open` diagnostics. The valid resolution-needed control and all 151 lifecycle regressions pass. Review, metadata, guide, and lifecycle artifact validation are rerun for final handoff.

### code-review-m3-r6

#### BRF-M3-CR11 - Canonical store construction permits root rebinding

Finding ID: BRF-M3-CR11
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's request accepted the deterministic safe resolution.
Rationale: Post-construction root comparison is insufficient when construction itself can bind the store to an arbitrary ancestor or to a foreign metadata symlink target.
Required outcome: Canonical metadata must bind to exactly its lexical repository root and matching change directory before any read or mutation.
Chosen action: Preserved the lexical metadata path through canonical-layout validation, rejected symlinks from repository root through `change.yaml`, required explicit-root equality with the derived canonical root, enforced lexical directory/change-ID binding, and removed the finalizer's repository-root parameter.
Safe resolution path: Validate the lexical canonical metadata path and every component before resolving, reject symlinks, derive the exact repository root from the canonical layout, require explicit-root equality, enforce change-directory identity, and add constructor-level adversarial regressions.
Validation target: Full state/engine regressions, direct ancestor/common-root and metadata-symlink contrasts, CMD10-CMD14, and code-review M3 R7.
Validation evidence: Proof-first ancestor-root and metadata file/directory symlink tests failed before correction and now pass alongside valid inferred/explicit root and mismatched-ID controls. All 47 state/recovery tests and 23 engine tests pass; repository broad smoke passed all 11 checks in 400 seconds.

#### BRF-M3-CR12 - Authoritative reason detail can contradict review state

Finding ID: BRF-M3-CR12
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: None; the user's request accepted the bounded machine-checkable projection.
Rationale: The new validator checks only reason codes before the em dash, while the same authoritative field's detail can assert the opposite open-finding state.
Required outcome: Both the structured reason code and bounded detail must agree deterministically with formal open-finding evidence.
Chosen action: Added an exact `review-state`, `open-count`, and sorted `open-findings` prefix for live open-review detail, validates it against formal review evidence, and rejects independent finding words or IDs in the remaining detail. Closed state rejects unstructured finding claims without changing unrelated or historical prose.
Safe resolution path: Define and validate an exact review-state clause containing current open count or IDs, or prohibit review-state claims outside that clause; add open-evidence/closed-detail and closed-evidence/open-detail regressions without scanning historical prose.
Validation target: Focused lifecycle state-sync contrasts, full lifecycle regressions, artifact lifecycle validation, and code-review M3 R7.
Validation evidence: Proof-first wrong-count, wrong-ID, missing-projection, open-evidence/closed-prose, and closed-evidence/open-prose contrasts failed before correction and now pass. The valid exact projection passes, all 153 lifecycle regressions pass, and repository broad smoke passed all 11 checks in 400 seconds.

### code-review-m3-r1

#### BRF-M3-CR1 - Canonical evidence is not bound to stage invocation

Finding ID: BRF-M3-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: The resolver accepts unknown or missing evidence relationships, while the coordinator accepts caller-supplied predecessor and input identities that may disagree with capability basis and still invokes the stage.
Required outcome: Resolve and bind complete current canonical evidence, transition evidence, and stage-required receipt inputs before capability or receipt persistence.
Chosen action: Connect canonical resolution to one-stage coordination, compare complete observed identities with capability basis and receipt inputs, and reject unknown, missing, stale, or contradictory evidence before callback invocation.
Safe resolution path: Introduce a typed canonical evaluation input, reject identity-set disappearance and mismatch, validate closed review/transition evidence, and add callback-not-invoked contrasts.
Validation target: CMD11-CMD14, direct identity/transition/outcome regressions, and code-review M3 R2.
Validation evidence: CMD11-CMD14 pass; direct unknown, missing, stale, contradictory, and callback-not-invoked contrasts pass. Awaiting code-review M3 R2.

#### BRF-M3-CR2 - Target completion predicates are not policy-bound

Finding ID: BRF-M3-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: A non-empty but attacker-chosen completion mapping passes resume and durable validation, allowing target stop semantics to drift from the approved policy.
Required outcome: Bind every target completion predicate exactly to the immutable stage-policy projection.
Chosen action: Centralize expected completion projection and enforce exact equality in binding, resume, and durable target validation.
Safe resolution path: Reuse one policy-derived helper across engine and validator and add one-field target-completion mutation tests for every public stage.
Validation target: CMD10, full automation-validator regressions, direct completion-tamper contrasts, and code-review M3 R2.
Validation evidence: CMD10 and all 50 automation-validator tests pass; every public target rejects one-field completion tampering. Awaiting code-review M3 R2.

#### BRF-M3-CR3 - Correction budget is absent from effective capability evaluation

Finding ID: BRF-M3-CR3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: A parent with zero remaining correction cycles and findings can derive an active correction capability because derivation neither receives nor compares current budget scope.
Required outcome: Correction capabilities must bind current budget state within the parent maximum and reject exhaustion, expansion, or identity mismatch.
Chosen action: Add typed correction-budget state to capability derivation and persist or bind the deterministic constraint needed for evaluation.
Safe resolution path: Compare requested/current limits to the parent, require current budget identity, and add proposal- and implementation-correction budget matrices.
Validation target: CMD12, expanded/exhausted/changed-budget direct regressions, and code-review M3 R2.
Validation evidence: CMD12 passes proposal- and implementation-correction matrices for valid, exhausted, expanded, dimension-mismatched, and stale-identity budgets. Awaiting code-review M3 R2.

#### BRF-M3-CR4 - Coordinator fabricates completed canonical synchronization

Finding ID: BRF-M3-CR4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: Any non-empty callback output is finalized as completed and synchronized without checking stage-owned evidence, expected postcondition, or canonical state.
Required outcome: Finalize completion only after typed stage-owned evidence satisfies the postcondition and canonical synchronization is performed and re-read successfully.
Chosen action: Separate output evidence from canonical-sync evidence, validate both, and leave unsafe outcomes paused or failed without consuming the capability.
Safe resolution path: Return a typed stage result, validate policy completion evidence and postcondition, perform canonical synchronization through the owning boundary, and add failure-ordering contrasts.
Validation target: CMD12-CMD14, arbitrary-output/postcondition/sync failure regressions, and code-review M3 R2.
Validation evidence: CMD12-CMD14 pass; arbitrary output, mismatched postcondition, and failed synchronization contrasts pause without capability consumption. Awaiting code-review M3 R2.

### code-review-m2-r3

No material findings; no additional review resolution is required.

### code-review-m2-r2

#### BRF-M2-CR5 - Persisted transition-key integrity is not validated

Finding ID: BRF-M2-CR5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the approved deterministic receipt contract; no owner choice remained.
Rationale: The correction adds retry policy to transition-key computation, but canonical read and recovery accept a non-empty stale key after immutable receipt inputs change.
Required outcome: Every persisted prepared or completed receipt must have a transition key equal to the deterministic key computed from its immutable operation inputs before read, projection, or recovery can succeed.
Chosen action: Enforce transition-key integrity at the canonical state-validation boundary and add prepared/completed read, query, and recovery regressions.
Safe resolution path: Centralize dependency-safe key computation, reject mismatches with a stable contract error, and prove stale keys cannot reach status or recovery.
Validation target: CMD6-CMD7, query stale-key regression, and code-review M2 R3.
Validation evidence: Proof-first prepared/completed read, direct recovery, cancellation, and query tests failed before implementation. Deterministic key computation now lives in the canonical validator and is re-exported by the state adapter; all stale-key paths fail closed. The final targeted run passed 30 state tests, 18 receipt-selected validator tests, 49 full validator tests, and 19 query tests.

#### BRF-M2-CR6 - Retry-family proof uses invalid automation states

Finding ID: BRF-M2-CR6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by approved T15 and stage-policy contracts; no owner choice remained.
Rationale: Two retry-family cases bypass canonical validation with incomplete parent, basis, predecessor, and milestone state, so T15's all-family proof is not credible.
Required outcome: Exercise idempotent, reconcile-only, and manual recovery with complete validator-valid persisted automation states.
Chosen action: Replace stage-name mutation fixtures with stage-appropriate complete states that pass canonical read before recovery is evaluated.
Safe resolution path: Reuse stage-specific fixture builders, persist/read through `WorkflowAutomationStateStore`, assert validation success, then test all three decisions and mismatch rejection.
Validation target: CMD6-CMD7 and code-review M2 R3.
Validation evidence: The replacement fixtures construct complete architecture-assessment, proposal-review, and implement@M2 states with stage-appropriate parent scope, basis, predecessor evidence, occurrence, and transition keys. Each state passes `WorkflowAutomationStateStore.read()` before recovery; expected retry, pause, and manual-recovery decisions plus per-family policy mismatch rejection pass in the 30-test state suite.

### code-review-m2-r1

#### BRF-M2-CR1 - Recovery is not bound to the persisted prepared receipt

Finding ID: BRF-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the approved write-ahead receipt contract; no owner choice remained.
Rationale: Resume authority must come from the durable write-ahead record, but the evaluator currently accepts a separate caller-supplied receipt and can retry when no receipt is persisted.
Required outcome: Resolve and evaluate exactly the unique persisted prepared receipt by transition identity; reject absence, substitution, mismatch, or duplication before retry or reconciliation.
Chosen action: Change recovery to resolve the receipt from canonical automation state and add direct persisted-versus-supplied identity contrasts.
Safe resolution path: Accept a transition ID, retrieve the canonical receipt, bind its mapping key and immutable identity, and fail closed before evaluating policy or evidence when the binding is not exact.
Validation target: CMD6-CMD7, direct unpersisted/mismatched receipt regressions, and code-review M2 R2.
Validation evidence: Proof-first recovery tests failed when the evaluator still accepted a caller-supplied object. After correction, unpersisted and substituted IDs fail closed and all 27 state/recovery tests pass.

#### BRF-M2-CR2 - Retry authority is controlled by receipt data instead of stage policy

Finding ID: BRF-M2-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the immutable stage-policy ownership contract; no owner choice remained.
Rationale: The approved immutable registry owns retry policy; a mutable receipt value cannot widen a reconcile-only or manual stage into idempotent retry.
Required outcome: Derive retry behavior from the effective capability's immutable stage policy and reject any persisted projection that disagrees.
Chosen action: Make stage policy authoritative, validate any receipt projection against it, and bind a retained projection into the transition key.
Safe resolution path: Resolve capability stage to `STAGE_POLICY_BY_STAGE`, use its retry policy for recovery, reject mismatch/missing required projection, and add all-family contrasts.
Validation target: CMD6-CMD7, direct policy-mismatch/key-binding regressions, and code-review M2 R2.
Validation evidence: Proof-first transition-key and recovery tests exposed mutable retry authority. After correction, all three retry families derive from `STAGE_POLICY_BY_STAGE`, mismatched or missing projections fail validation, the projection changes the key, 27 state tests pass, and 17 receipt-selected validator tests pass.

#### BRF-M2-CR3 - T29 deterministic proof is incomplete

Finding ID: BRF-M2-CR3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by approved T29; no owner choice remained.
Rationale: Dictionary-order and duplicate migration checks do not prove the approved transactional subset is repeatable and order-independent across canonical files and fresh roots.
Required outcome: Execute T29's complete fixed-input repeated and reverse-order scenario and compare normalized receipt, key, migration, canonical-file, and teardown evidence.
Chosen action: Add a deterministic fresh-root scenario runner and explicit normal/repeated/reverse comparisons.
Safe resolution path: Keep M2 scope to state/receipt/migration operations, inject fixed IDs and time, sanitize inputs, compare canonical outputs, and assert no shared temporary state remains.
Validation target: CMD6-CMD8 and code-review M2 R2.
Validation evidence: The new T29 runner uses fresh temporary roots and fixed inputs, executes transition and migration scenarios twice in normal order and once in reverse order, compares normalized receipts, keys, migration records, and canonical file bytes, and proves temporary-root and temporary-file cleanup. All 27 state tests plus the 17 receipt and 3 migration validator selections pass.

#### BRF-M2-CR4 - Status bypasses canonical automation validation

Finding ID: BRF-M2-CR4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the approved canonical read-boundary contract; no owner choice remained.
Rationale: Operator status must not report unknown or malformed durable automation state as successful current state.
Required outcome: Validate the unified automation subsection before projection and return a stable read-only error diagnostic on invalid state.
Chosen action: Route unified query status through the canonical validated read boundary and add malformed-state byte-stability regressions.
Safe resolution path: Reuse `validate_workflow_automation` or `WorkflowAutomationStateStore.status`, convert failures to the query error envelope, and cover unknown run/receipt/policy/migration values.
Validation target: CMD8-CMD9, direct unknown-status regression, and code-review M2 R2.
Validation evidence: Proof-first query regression returned success for an unknown run status before correction. Unified queries now use `WorkflowAutomationStateStore.read`; unknown run, policy, receipt, and migration values return `invalid-automation-state`, preserve source bytes, and all 18 query tests pass.

### code-review-m1-r7

No material findings; no additional review resolution is required.

### code-review-m1-r6

#### BRF-M1-CR12 - Stage-only target frontiers reject valid later milestone targets

Finding ID: BRF-M1-CR12
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: Resolved by the approved structured-target contract; no owner choice remained.
Rationale: R6 directly reproduced a complete next-milestone transition that succeeds only for final target `verify` and fails for structured targets `implement@M2` and `code-review@M2`.
Required outcome: Repeated-stage target permission must use target occurrence identity so valid work can advance to a bound later milestone without allowing continuation after an already-reached occurrence.
Chosen action: Expanded the next-milestone edge to the repeated-stage frontier and required `implement` and `code-review` targets to bind the same milestone ID as the evaluated next milestone.
Safe resolution path: Make the repeated-stage frontier occurrence-aware, add positive M1-to-M2 transitions toward `implement@M2` and `code-review@M2`, and retain negative exact-M1 stopping and no-rebinding contrasts.
Validation target: Targeted repeated-target predicate tests, the full M1 command set, broad smoke, and code-review M1 R7.
Validation evidence: Proof-first policy and complete-state tests failed for both repeated targets before implementation. After correction, 15 policy tests, 42 automation-validator tests, 5 vocabulary tests, 4 focused metadata tests, all 52 metadata tests, Python compilation, and 12 broad-smoke checks in 299 seconds pass. Exact stale-M1 and missing-target-identity contrasts remain rejected.

### test-spec-review-r1

#### BRF-TSR1 - Manual proof contracts are incomplete

Finding ID: BRF-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Replace MP1-MP3 and the unnumbered manual checks with complete owned manual-proof contracts or automated mappings.
Rationale: Milestone closeout cannot rely on one-line confirmations that omit environment, evidence, and explicit pass/fail conditions.
Required outcome: Every milestone-required manual proof has a stable ID, automation rationale, exact steps, environment, evidence artifact, pass condition, failure condition, owner, and gate.
Safe resolution path: Add structured manual-proof records, bind their milestone/stage ownership, and map the two unnumbered checks to stable manual or automated IDs.
Validation target: Revised test spec and `test-spec-review-r2`.
Validation evidence: The revised test spec records structured MP1-MP3 contracts with rationale, owner, stage, environment, exact steps, evidence, pass/fail conditions, and gates. T22 owns the two former unnumbered checks. Test-spec-review R2 confirmed resolution.

#### BRF-TSR2 - Required M6 command is not executable as stored

Finding ID: BRF-TSR2
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Replace the escaped-pipe CMD30 representation with a directly executable equivalent and normalize CMD18's first required milestone.
Rationale: A canonical proof command must be runnable from its tracked representation, and the first-required field must identify one gate.
Required outcome: CMD30 remains manifest-derived, temporary-output-only, and directly executable; CMD18 identifies M4 as its first required milestone.
Safe resolution path: Use a no-pipe version lookup or a repository-owned wrapper while preserving the approved adapter proof semantics.
Validation target: Revised test spec and `test-spec-review-r2`.
Validation evidence: CMD30 uses a manifest-derived `awk` first-match expression with non-empty validation and no Markdown pipe; CMD18 identifies M4 code-review as its first gate and records M5 reuse. Test-spec-review R2 confirmed resolution.

#### BRF-TSR3 - Deterministic fixture controls are undefined

Finding ID: BRF-TSR3
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Define deterministic time, ID, environment, randomness, temporary-root, teardown, and execution-order controls.
Rationale: Transaction, migration, status, and recovery proof depends on nondeterministic inputs that the current fixture policy does not constrain.
Required outcome: Relevant tests run against fixed inputs, fresh isolated state, and repeat/reordered execution without hidden environment dependence.
Safe resolution path: Add an injected fixed UTC clock, stable IDs/keys, fixed locale/timezone, sanitized environment, seeded or prohibited randomness, fresh temporary roots, teardown assertions, and repeat/order-independence proof.
Validation target: Revised test spec and `test-spec-review-r2`.
Validation evidence: The revised fixture contract fixes UTC time, IDs/keys, locale, timezone, environment, randomness, temporary roots, teardown, and process state. T29 repeats and reverses transactional/migration execution and compares normalized evidence. Test-spec-review R2 confirmed resolution.

### test-spec-review-r2

#### BRF-TSR4 - Multi-milestone proof activation is ambiguous

Finding ID: BRF-TSR4
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Chosen action: Make assertion and command activation explicit for every test case required by more than one milestone, splitting T29 into independently executable M2 and M6 proof cases unless an equally explicit activation map is clearer.
Rationale: A milestone gate must be executable without inferring which parts of a shared test case remain unavailable until a later component and command exist.
Required outcome: Every multi-milestone test case identifies the exact assertions and command IDs active at each milestone; M2 determinism proof is independent of the M6 full-engine command and evidence.
Safe resolution path: Audit all progressive cases; add per-milestone activation records; split T29 into state-level M2 determinism and M6 full-engine order-independence; update coverage, test counts, milestone rows, fixture order proof, and command mappings; then rerun test-spec-review.
Validation target: Revised test spec and `test-spec-review-r3`.
Validation evidence: The revised test spec separates T29/T30 across M2/M6 and maps all 15 progressive cases. T26 explicitly uses M4/CMD17 for the non-public authoring harness and M6/CMD25 for final public composition, with later proof deferred at M4. Test-spec-review R4 confirmed resolution.

### test-spec-review-r3

No new material findings.
`BRF-TSR4` remains open because T26 has contradictory case-level and M6 milestone ownership and no progressive activation row.

### test-spec-review-r4

No material findings.
R4 approved the active test specification and confirmed `BRF-TSR1` through `BRF-TSR4` resolved.
Implementation handoff is allowed; the isolated review does not automatically start implementation.

### plan-review-r1

#### BRF-PL1 - Final-cutover validation commands

Finding ID: BRF-PL1
Disposition: accepted
Status: resolved
Owner: plan owner
Owning stage: plan
Chosen action: Replace M5's bare adapter checks with versioned generated release-output proof and execute selector-selected checks through the repository CI wrapper.
Rationale: The current adapter command is missing a required argument, the tracked-tree check conflicts with the active release-archive contract, and selection alone does not execute the required checks.
Required outcome: Every final-cutover validation command is runnable and proves the active generated-adapter and selected-check contracts.
Validation target: Revised plan and `plan-review-r2`.
Validation evidence: The revised plan uses manifest-versioned temporary adapter generation and validation, executes selected checks through `scripts/ci.sh`, requires broad smoke, and reserves public activation for M6. `bash scripts/ci.sh --mode explicit ...` passed all six selected checks, including `broad_smoke.repo` in 377.30 seconds; plan-review R2 confirmed resolution.

#### BRF-PL2 - Public activation and milestone boundary

Finding ID: BRF-PL2
Disposition: accepted
Status: resolved
Owner: plan owner
Owning stage: plan
Chosen action: Separate authoring/review integration from implementation/verification integration and reserve public command activation, compatibility aliases, and retired-writer removal for one final cutover milestone.
Rationale: Overlapping workflow-skill ownership can expose a partially migrated engine and makes the largest stage-integration milestone difficult to review or recover independently.
Required outcome: Earlier integration milestones remain non-public and non-routable, and one final milestone atomically activates the unified public mechanism after prerequisite proof.
Validation target: Revised plan and `plan-review-r2`.
Validation evidence: The revised plan splits authoring integration into M4 and implementation/verification integration into M5, keeps M1-M5 behind a non-public harness, and makes M6 the sole public activation and legacy-writer cutover. `bash scripts/ci.sh --mode explicit ...` passed all six selected checks, including `broad_smoke.repo` in 377.30 seconds; plan-review R2 confirmed resolution.

### plan-review-r2

No material findings. Plan-review R2 confirmed `BRF-PL1` and `BRF-PL2` resolved and approved the execution plan.

### proposal-review-r1

#### BRF-PR1 - Canonical workflow-position resolution

Finding ID: BRF-PR1
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Chosen action: Add two canonical position epochs, evidence-derived pre-plan routing, active-plan ownership after validated plan creation, a recorded ownership handoff, and fail-closed ambiguity handling.
Rationale: Automation cannot resume deterministically unless canonical position exists before the plan without becoming automation-owned state.
Validation target: Revised proposal and proposal-review R2.
Validation evidence: The revised proposal records two canonical-position epochs, fail-closed ambiguity behavior, and a receipt-recorded plan ownership handoff. Focused lifecycle, metadata, review-artifact, and diff validation passed. Proposal-review R2 confirmed this finding resolved.

#### BRF-PR2 - Identity-bound grants

Finding ID: BRF-PR2
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Chosen action: Replace status-only grants with identity-bound grant envelopes, grant-specific basis and scope, deterministic invalidation, and a closed non-grantable external-action value.
Rationale: Durable authority must become stale when its reviewed basis or mutation scope changes.
Validation target: Revised proposal and proposal-review R2.
Validation evidence: The revised proposal records stable grant IDs, policy versions, reviewed basis identities, milestone/path/mutation/command scope, invalidation triggers, separate implementation and verification grants, and non-grantable external actions. Focused validation passed. Proposal-review R2 confirmed this finding resolved.

#### BRF-PR3 - Recoverable transition protocol

Finding ID: BRF-PR3
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Chosen action: Define write-ahead prepared receipts, deterministic transition keys, closed receipt states, stage retry policies, reconciliation before retry, and one in-flight transition per change.
Rationale: Multi-artifact lifecycle writes are not atomic, so post-hoc receipts cannot prove safe recovery.
Validation target: Revised proposal and proposal-review R2.
Validation evidence: The revised proposal records prepared receipts, deterministic transition keys, closed receipt statuses, retry policies, evidence-first reconciliation, and one in-flight transition. Focused validation passed. Proposal-review R2 confirmed this finding resolved.

#### BRF-PR4 - Structured repeated-stage targets

Finding ID: BRF-PR4
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Chosen action: Replace the stage-only target with stage, occurrence, and completion identity; bind repeated targets to milestone IDs; distinguish milestone-local review from final holistic review.
Rationale: A stage-only target can silently rebind after resume and cannot prove which repeated occurrence completed.
Validation target: Revised proposal and proposal-review R2.
Validation evidence: The revised proposal records structured target envelopes, milestone occurrence binding, exact `implement@M<n>` and `code-review@M<n>` completion, final verify completion, and conditional architecture behavior. Focused validation passed. Proposal-review R2 confirmed this finding resolved.

### proposal-review-r2

#### BRF-PR5 - Proposal-review target has circular grant basis

Finding ID: BRF-PR5
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Decision owner: proposal owner
Decision needed: None; the proposal owner selected the review-only effective capability and bounded parent-authorization model.
Chosen action: Keep `proposal-review` as a public singleton target. Materialize a review-only effective authoring capability against the exact proposal identity, separate review from correction, invalidate gate use of prior review after proposal mutation, and materialize post-proposal authoring capability only after clean review evidence exists within a bounded parent authoring authorization.
Rationale: The prior authoring grant required a clean proposal gate while the public target set included the proposal review needed to create that gate. Separate identity-bound effective capabilities preserve the single mechanism, reviewer independence, and non-circular authorization.
Required outcome: Define a deterministic authorization basis for `proposal-review` that cannot authorize continuation to `spec` or later until a clean proposal gate and a separately identity-bound post-proposal authoring grant exist.
Validation target: Revise the proposal and run proposal-review R3.
Validation evidence: The proposal now defines proposal-review, proposal-correction, and post-proposal effective authoring capabilities; binds review to an exact proposal identity and review-evidence-only mutation scope; permits post-proposal derivation only within bounded parent authoring authority after a clean gate; and prohibits derivation across risk classes. Proposal-review R3 confirmed the non-circular direction resolved.

### proposal-review-r3

#### BRF-PR6 - Common grant invariant contradicts pre-review capability

Finding ID: BRF-PR6
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Decision owner: proposal owner
Decision needed: None; the proposal owner selected distinct durable parent authorization and effective capability record types.
Chosen action: Define parent authorization as non-executable maximum user consent with stable identity, policy, change, target, capability, scope, budget, revocation, and invalidation fields. Define effective capability as the only executable authority, bound to its parent identity, stage occurrence, stage-appropriate basis, actual subset scope, derivation state, and invalidation behavior. Make review identities conditional on the stage-policy basis.
Rationale: A proposal-review capability cannot both precede proposal approval and satisfy a universal reviewed-basis requirement. The parent authorization is the source for derived authority and therefore also needs explicit durable identity, scope, revocation, and invalidation semantics.
Required outcome: Define one consistent two-level authorization contract covering bounded parent authorization and effective stage capability without requiring review evidence where the stage exists to create it.
Validation target: Revise the proposal and run proposal-review R4.
Validation evidence: The proposal now uses distinct record types, a stage-appropriate capability invariant, conditional review identities, exhaustive derivation checks, parent and child invalidation propagation, revised acceptance criteria `AC-BRF-033` and `AC-BRF-046` through `AC-BRF-050`, and focused test checks `UWA-033` through `UWA-038`. Focused validation passed and proposal-review R4 confirmed resolution.

#### BRF-PR7 - Inconclusive proposal-review outcome has no target behavior

Finding ID: BRF-PR7
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal
Decision owner: proposal owner
Decision needed: None; the proposal owner selected separate occurrence, outcome, clean-gate, and routing facts.
Chosen action: Record all four closed proposal-review outcomes against the exact proposal identity, allow only `approved` to satisfy the clean gate, route `changes-requested` to bounded correction only with valid capability and budget, pause on `blocked` and `inconclusive`, and fail closed on unknown outcomes. Prevent inconclusive rereview without material evidence change.
Rationale: `inconclusive` is a valid closed proposal-review outcome, so unknown-value failure does not define its target, pause, or continuation behavior.
Required outcome: Define deterministic behavior for all four proposal-review outcomes while permitting only `approved` to satisfy the clean proposal gate.
Validation target: Revise the proposal and run proposal-review R4.
Validation evidence: The proposal now defines a review-result receipt, closed clean-gate and routing vocabularies, an exhaustive exact-target and later-target matrix, correction and no-spin behavior, acceptance criteria `AC-BRF-051` through `AC-BRF-058`, and focused checks `UWA-039` through `UWA-041`. Focused validation passed and proposal-review R4 confirmed resolution.

### proposal-review-r4

No material findings.

### spec-review-r1

Review closeout: open

#### BRF-SR1 - Repeated target binding

Finding ID: BRF-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add a closed stage-to-occurrence matrix and bind bare `implement` and `code-review` commands to the unique current in-scope plan milestone before persistence.
Rationale: A repeated-stage target is not deterministic if the command supplies no occurrence and the spec permits non-milestone occurrence kinds.
Required outcome: Every public target resolves to exactly one valid occurrence and completion predicate before authorization or run state is persisted.
Safe resolution path: Require milestone occurrences for `implement` and `code-review`, singleton occurrences for singleton stages, and final occurrence for `verify`; pause on a missing or ambiguous current milestone; add invalid-pair and resume-no-rebind coverage.
Validation target: Revised spec and `spec-review-r2`.
Validation evidence: The revised spec defines one occurrence kind and completion predicate per public stage, binds repeated targets to the active plan's unique milestone before persistence, rejects ambiguous or incompatible bindings, and preserves persisted occurrences on resume. Focused validation is recorded below; spec-review R2 remains required.

#### BRF-SR2 - Closed durable state and capability vocabularies

Finding ID: BRF-SR2
Disposition: accepted
Status: resolved-pending-rereview
Owner: spec author
Owning stage: spec
Chosen action: Define distinct closed status sets, capability kinds, legal transitions, resumability, terminality, and one deterministic `off` transition.
Rationale: Unknown-value rejection is not implementable when the valid run, parent, capability, and capability-kind sets are absent.
Required outcome: Validators and the transition engine can exhaustively distinguish valid values, invalid values, and illegal transitions for every durable automation record.
Safe resolution path: Add normative vocabulary and transition tables, bind every stage policy to one capability kind, define cancellation propagation, and require unknown-value and illegal-transition regressions.
Validation target: Revised spec and `spec-review-r2`.
Validation evidence: The revised spec defines separate closed run, parent-authorization, capability-status, and capability-kind vocabularies; exhaustive legal transitions; run-owned pause; single-use capabilities; and deterministic cancellation propagation. Focused validation is recorded below; spec-review R2 remains required.

#### BRF-SR3 - Verification authorization timing

Finding ID: BRF-SR3
Disposition: accepted
Status: resolved-pending-rereview
Owner: spec author
Owning stage: spec
Chosen action: Prohibit future-contingent verification parent authorization while allowing an eventual final `verify` target to exist before verification authority.
Rationale: Capability-basis checks alone do not preserve the accepted proposal's separate authorization-timing decision.
Required outcome: Verification parent authorization and effective capability exist only after their concrete closeout, review, promotion, explanation, and branch-state bases are independently valid.
Safe resolution path: Add the timing requirement, pause at the verification boundary without current authority, and cover early target, early authorization rejection, and valid late authorization cases.
Validation target: Revised spec and `spec-review-r2`.
Validation evidence: The revised spec permits an early final verify target while forbidding verification authorization until implementation closeout, final review, promotion, explanation, branch-state, and verification inputs are concrete. It requires a boundary pause when authority is absent. Focused validation is recorded below; spec-review R2 remains required.

#### BRF-SR4 - Legacy command adapter mapping

Finding ID: BRF-SR4
Disposition: accepted
Status: resolved-pending-rereview
Owner: spec author
Owning stage: spec
Chosen action: Make legacy command adapters mandatory during the migration window and map each supported alias to a structured target and currently valid risk-class authorization boundary.
Rationale: Optional aliases contradict the accepted proposal's compatibility goal and leave old-client behavior undefined.
Required outcome: `auto-through: plan-review`, `auto-through: verify`, status, and off have deterministic unified behavior without legacy writes or premature verification authority.
Safe resolution path: Add an alias mapping table, define later-boundary pauses, define removal only through a later compatibility decision, and add equivalence fixtures.
Validation target: Revised spec and `spec-review-r2`.
Validation evidence: The revised spec makes legacy adapters mandatory throughout migration, maps plan-review, verify, status, off, and unknown forms exhaustively, preserves read-only status, and requires unified-only writes. Focused validation is recorded below; spec-review R2 remains required.

#### BRF-SR5 - Cross-spec supersession boundary

Finding ID: BRF-SR5
Disposition: accepted
Status: resolved-pending-rereview
Owner: spec author
Owning stage: spec
Chosen action: Replace open-ended supersession phrases with exact requirement and acceptance mappings or amend the affected approved specs in the same revision.
Rationale: Same-rank approved specs still name retired profiles as the exclusive continuation mechanism outside the listed superseded ranges.
Required outcome: Every affected legacy requirement is explicitly superseded, preserved unchanged, or preserved with its subject rebound to the unified mechanism.
Safe resolution path: Reconcile `workflow-stage-autoprogression` `R2b`, `R2g`, `R2w` through `R2al`, related inputs/outputs and acceptance criteria, and equivalent references in the other governing specs; add a static contradiction check.
Validation target: Revised spec and `spec-review-r2`.
Validation evidence: The revised spec adds exact dispositions for affected requirements and stable selectors for affected inputs, outputs, state, errors, compatibility, observability, security, examples, and acceptance surfaces. The four legacy specs carry conditional unified-amendment notices and matching selectors. Focused validation is recorded below; spec-review R2 remains required.

### spec-review-r2

Review closeout: open

#### BRF-SR6 - Cross-spec source selectors are not uniquely enumerable

Finding ID: BRF-SR6
Disposition: accepted
Status: resolved-pending-rereview
Owner: spec author
Owning stage: spec
Chosen action: Give each duplicate source requirement a unique stable identifier, remove open-ended default precedence, enumerate every applicable disposition explicitly, and add selector uniqueness to the static validation contract.
Rationale: Exact precedence cannot be validated when two source requirements share one ID or when omission implicitly means preservation.
Required outcome: Every covered source selector is unique and receives exactly one explicit disposition that a static check can prove complete.
Safe resolution path: Rename one `R2ba` occurrence using a repository-valid stable ID, update references, replace the unlisted default with an exact inventory or statically closed affected-selector registry, and extend `BRF-R098e` plus proof coverage.
Validation target: Revised spec and `spec-review-r3`.
Validation evidence: The ordinary lifecycle-continuation requirement now uses unique ID `R2b1`; the later test-spec-settlement requirement retains `R2ba`; intended test-spec and plan references were updated. The unified spec now defines a closed affected-selector registry, rejects duplicate source selectors before disposition consistency, forbids implicit dispositions, and assigns sole persisted-automation ownership to the unified spec. Focused validation is recorded below; spec-review R4 remains required.

### spec-review-r3

Review closeout: inconclusive

No new material findings were recorded. The reviewed spec and affected legacy workflow identities were unchanged from spec-review R2, so the existing `BRF-SR5` and `BRF-SR6` resolutions remain open and no approval decision was possible.

### spec-review-r4

Review closeout: closed

No material findings. Spec-review R4 confirmed `BRF-SR5` and `BRF-SR6` resolved through unique source selectors, a closed affected-selector registry, sole persisted-automation ownership, and deterministic supersession settlement.

### spec-review-r5

Review closeout: closed

No material findings. Spec-review R5 confirmed the unified spec's `approved` state and the retired review-fix spec's `superseded_by` settlement implement the R4-approved contract without substantive behavior changes.

### architecture-review-r1

Review closeout: open

#### BRF-AR1 - Stage-policy projection is incomplete

Finding ID: BRF-AR1
Disposition: accepted
Status: resolved-pending-rereview
Owner: architecture author
Owning stage: architecture
Chosen action: Enumerate the complete `BRF-R079` stage-policy field set in the canonical architecture and ADR while retaining the approved specification as normative owner.
Rationale: Routing, capability, mutation, evidence, next-stage, and stop semantics cannot be left for the plan or implementation to infer.
Required outcome: The executable registry projection covers predecessor, applicability, authorization class, capability kind, owning skill, mutation category, input identities, completion evidence, retry, next-stage calculation, correction, and stop behavior for every automatable stage.
Safe resolution path: Revise the registry responsibility and ADR decision with exact spec terms and require exhaustive typed-registry conformance proof.
Validation target: Revised architecture package and `architecture-review-r3`.
Validation evidence: The canonical architecture and proposed ADR enumerate the complete immutable sixteen-field projection, retain approved specifications as normative owner, prohibit a second hand-authored registry, and require exhaustive fail-closed conformance proof. Focused validation passed and architecture-review R3 confirmed resolution.

#### BRF-AR2 - Executable and persistence ownership is ambiguous

Finding ID: BRF-AR2
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Select one physical owner for orchestration, typed policy/evaluation/validation, and one canonical first-version `workflow.automation` persistence surface; align prose and C4 roles to that split.
Rationale: The current package assigns code and state across overlapping `skills/`, `scripts/`, automation, and change-local-evidence containers, so planning would need to make an architecture decision.
Required outcome: The architecture names the code-module boundary, state file/section, schema ownership, and dependency direction without duplicate ownership.
Safe resolution path: Keep workflow command orchestration in the workflow skill, typed executable machinery in named Python modules under `scripts/`, and canonical state in `docs/changes/<change-id>/change.yaml#workflow.automation`, or explicitly define an alternative single change-local file and schema.
Validation target: Revised architecture prose, container/component diagrams, ADR, and `architecture-review-r3`.
Validation evidence: The package assigns public semantics to `skills/workflow/SKILL.md`, executable responsibilities to four named Python modules, the sole write boundary to `scripts/workflow_automation_state.py`, and durable state to `change.yaml#workflow.automation`. The diagrams separate code from state and use component/container roles consistently. Focused validation passed and architecture-review R3 confirmed resolution.

#### BRF-AR3 - Receipt uses obsolete grant identity

Finding ID: BRF-AR3
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Replace `grant identity` with the exact `effective capability ID` required by `BRF-R069` and audit the architecture for equivalent ambiguity.
Rationale: Only an effective capability is executable authority; a parent authorization is a maximum consent envelope.
Required outcome: Prepared receipts bind the exact effective capability used for the transition and cannot imply direct execution from a parent authorization.
Safe resolution path: Correct runtime step 10 and keep the capability-to-parent linkage as the only path to parent authorization evidence.
Validation target: Revised architecture package and `architecture-review-r3`.
Validation evidence: Runtime and ADR text bind prepared receipts and resume to the original `effective_capability_id`, reach the non-executable parent only through `parent_authorization_id`, and pause instead of silently rebinding invalidated authority. Focused validation passed and architecture-review R3 confirmed resolution.

### architecture-review-r2

Review closeout: inconclusive

No new material findings were recorded. The canonical architecture, container diagram, workflow-automation component diagram, and proposed ADR still contain the R1 evidence. The owner-provided resolution decisions have not yet been incorporated into those tracked architecture surfaces, so `BRF-AR1`, `BRF-AR2`, and `BRF-AR3` remain open and no approval decision is possible.

### architecture-review-r3

Review closeout: closed

No material findings. Architecture-review R3 confirmed `BRF-AR1` through `BRF-AR3` resolved, approved the substantive architecture package, and identified coordinated architecture/ADR lifecycle normalization as the remaining pre-plan action.

## Shared Validation Evidence

| Validation area | Result | Notes |
| --- | --- | --- |
| Proposal revision | pass | `BRF-PR1` through `BRF-PR7` are incorporated in the revised proposal. |
| Change metadata | pass | `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` passed. |
| Review artifacts | pass | Structure and closeout validation passed for the R1/R2/R3/R4 review evidence pack. |
| Artifact lifecycle | pass | Explicit-path lifecycle validation passed for the proposal and R1/R2/R3/R4 review evidence pack. |
| Diff whitespace | pass | `git diff --check` passed. |
| Formal rereview R2 | changes-requested | R2 closed `BRF-PR1` through `BRF-PR4` and opened `BRF-PR5`. |
| Formal rereview R3 | changes-requested | R3 confirmed `BRF-PR5` resolved and opened `BRF-PR6` and `BRF-PR7`. |
| Formal rereview R4 | approved | R4 confirmed `BRF-PR1` through `BRF-PR7` resolved with no material findings. |
| Formal spec-review R1 | changes-requested | R1 opened `BRF-SR1` through `BRF-SR5`; the spec remains draft and is not ready for architecture or test-spec reliance. |
| Spec revision for R1 findings | pass | `BRF-SR1` through `BRF-SR5` are incorporated; findings remain open in the review ledger until spec-review R2. |
| Revised spec review-artifact validation | pass | Structure validation passed with 5 reviews, 12 findings, and 5 findings still open pending R2. |
| Revised spec artifact lifecycle | pass with baseline warning | Six lifecycle artifacts passed; `specs/rigorloop-workflow.md` retained its existing merge-dependent-language warning for reviewer attention. |
| Revised spec change metadata | pass | Change metadata validation and all 48 validator regressions passed. |
| Revised spec diff whitespace | pass | `git diff --check` passed. |
| Formal spec-review R2 | changes-requested | R2 closed `BRF-SR1` through `BRF-SR4`; `BRF-SR5` remains open and `BRF-SR6` records the exact-selector defect. |
| Formal spec-review R3 | inconclusive | The spec and affected legacy workflow identities were unchanged from R2, so no approval or new finding was recorded. |
| Spec-review R3 recording validation | pass | Review structure passed with 7 reviews and 13 material findings; change metadata and staged diff checks passed. |
| Consolidation revision selector audit | pass | All requirement selectors are unique across the four affected source specs; `R2b1` and `R2ba` now identify different intended contracts. |
| Consolidation revision focused checks | pass | Review artifacts, ten lifecycle artifacts, 48 metadata regressions, change metadata, and staged diff checks passed; only existing merge-language warnings remain. |
| Formal spec-review R4 | approved | R4 confirmed all six spec-review findings resolved with no material findings. |
| Spec lifecycle settlement | pass | The unified spec is `approved`; the retired review-fix spec is `superseded` and identifies the unified spec as its replacement. |
| Final spec closeout validation | pass | Review closeout, lifecycle, change metadata, and staged diff validation passed; only existing merge-language warnings remain. |
| Formal spec-review R5 | approved | R5 confirmed the settled lifecycle metadata without reopening the approved contract. |
| Spec-review R5 recording validation | pass | Review structure and closeout passed with 9 reviews and 13 findings; lifecycle and metadata validation plus staged diff checks passed. |
| Formal architecture-review R1 | changes-requested | R1 opened `BRF-AR1` through `BRF-AR3`; architecture is not ready for planning. |
| Architecture-review R1 recording validation | pass with baseline warning | Review structure passed with 10 reviews, 16 findings, and 3 open findings; metadata and staged diff checks passed; lifecycle validation retained the existing merge-language warning. |
| Formal architecture-review R2 | inconclusive | No architecture input changed after R1; all three R1 findings remain open. |
| Architecture-review R2 recording validation | pass with baseline warning | Review structure passed with 11 reviews, 16 findings, and 3 unresolved findings; metadata and staged diff checks passed; lifecycle validation retained the existing merge-language warning. |
| Architecture revision for R1 findings | pass with baseline warning | `BRF-AR1` through `BRF-AR3` and the ADR lifecycle observation are incorporated. The repository selected four focused checks with no broad smoke; review structure, four lifecycle artifacts, 48 metadata regressions, change metadata, and diff checks passed. Lifecycle validation retained the existing merge-language warning. Architecture-review R3 remains required. |
| Formal architecture-review R3 | approved | R3 closed `BRF-AR1` through `BRF-AR3` with no new material findings; lifecycle status normalization remains before plan reliance. |
| Architecture-review R3 recording validation | pass with baseline warning | Review structure and closeout passed with 12 reviews and 16 findings; metadata and staged diff checks passed; lifecycle validation retained the existing merge-language warning. |
| Formal test-spec-review R1 | changes-requested | R1 opened `BRF-TSR1` through `BRF-TSR3`; implementation handoff is not allowed. |
| Test-spec-review R1 recording validation | pass | Review structure passed with 15 reviews, 21 findings, and 3 open findings; metadata and scoped diff checks passed. |
| Formal test-spec-review R2 | changes-requested | R2 confirmed `BRF-TSR1` through `BRF-TSR3` resolved and opened `BRF-TSR4`; implementation handoff remains not allowed. |
| Test-spec-review R2 recording validation | pass | Review structure passed with 16 reviews, 22 findings, and 1 open finding; metadata and scoped diff checks passed. |
| `BRF-TSR4` test-spec revision | pass pending rereview | Static authoring checks confirmed 30 tests, 32 commands, 14 explicit progressive activation entries, separate M2/M6 determinism cases, current plan identity, valid review structure and change metadata, and a clean scoped diff. |
| Formal test-spec-review R3 | changes-requested | R3 confirmed the split determinism proof but kept `BRF-TSR4` open because T26 lacks its M4/M6 activation mapping; no new finding ID was needed. |
| Test-spec-review R3 recording validation | pass | Review structure passed with 17 reviews, 22 findings, and 1 open finding; metadata and scoped diff checks passed. |
| Final `BRF-TSR4` test-spec revision | pass pending rereview | T26 now binds M4/CMD17 and M6/CMD25 with explicit deferral; static authoring checks cover 30 tests, 32 commands, and all 15 progressive entries. |
| Formal test-spec-review R4 | approved | R4 confirmed all four test-spec findings resolved with no new material findings and allowed M1 implementation handoff. |
| Test-spec-review R4 recording validation | pass | Review structure and closeout passed with 18 reviews and 22 resolved findings; metadata and scoped diff checks passed. |
| Formal code-review M1 R1 | changes-requested | R1 opened `BRF-M1-CR1` through `BRF-M1-CR4`; M1 is resolution-needed and M2 remains blocked. |
| Code-review M1 R1 recording validation | pass with baseline warning | Review structure passed with 19 reviews and 26 findings, metadata and guide checks passed, lifecycle validation retained the existing lifecycle-language warning, and diff checks passed. |
| Code-review M1 R1 resolution implementation | pass pending rereview | The policy and state validators now enforce the four required outcomes; 9 policy tests, 5 selected vocabulary tests, 25 validator tests, 4 focused metadata tests, 52 metadata regressions, and 11 broad-smoke checks pass. |

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has a chosen action.
- [x] Proposal revision validation evidence is recorded.
- [x] Proposal-review R2 is recorded.
- [x] `BRF-PR5` owner decision and proposal-revision evidence are recorded.
- [x] Proposal-review R3 is recorded.
- [x] `BRF-PR6` and `BRF-PR7` owner decisions and proposal-revision evidence are recorded.
- [x] Proposal-review R4 is recorded.
- [x] Spec-review R1 is recorded with dispositions for `BRF-SR1` through `BRF-SR5`.
- [ ] Spec revision validation evidence is recorded.
- [x] Spec-review R2 closes `BRF-SR1` through `BRF-SR4`.
- [x] Spec revision closes `BRF-SR5` and `BRF-SR6`.
- [x] Spec-review R4 approves the exact-selector and ownership contract.
- [x] `BRF-AR1` through `BRF-AR3` are incorporated in the architecture package.
- [x] A changed architecture package is ready for architecture-review R3.
- [x] Architecture-review R3 approves the revised package.
- [ ] No review-log findings remain open.
- [ ] Closeout status is closed with final dispositions and validation evidence.

### code-review-m1-r1

#### BRF-M1-CR1 - Effective-capability occurrence validation

Finding ID: BRF-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: The validator must enforce the approved occurrence rule for every capability stage, including internal and milestone-bound stages.
Required outcome: Use the immutable policy projection for all capability occurrence checks and require exact milestone occurrence identity where applicable.
Chosen action: Replaced the partial occurrence map with immutable-policy lookup, validated all internal occurrences, and required milestone identity for milestone capabilities.
Safe resolution path: Derive capability occurrence validation from `STAGE_POLICIES` and add internal and repeated-stage negative tests.
Validation target: Add internal-stage wrong-occurrence, missing-milestone, and changed-occurrence regressions; rerun the M1 command set and code-review.
Validation evidence: Policy tests pass 9 cases; validator tests directly reject wrong internal occurrence and missing milestone identity; all M1 commands and the 11-check broad smoke pass.

#### BRF-M1-CR2 - Concrete basis and invalidation validation

Finding ID: BRF-M1-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: Key presence does not establish a concrete authority basis or deterministic invalidation behavior.
Required outcome: Validate stage-relative basis values and closed, non-empty parent/capability invalidation rules.
Chosen action: Added stage-relative concrete identity validation, non-empty scope/budget checks, and closed parent/capability invalidation trigger and action validation.
Safe resolution path: Add stage-relative concrete-value validation and closed invalidation rules with direct negative tests.
Validation target: Add null, empty, wrong-type, and unknown-invalidation-action regressions for all parent classes and capability kinds; rerun the M1 command set and code-review.
Validation evidence: Validator tests reject null basis identities, empty invalidation objects, unknown triggers/actions, cross-risk parent kinds, and validate complete records for all six capability kinds; all M1 commands and broad smoke pass.

#### BRF-M1-CR3 - Complete receipt binding validation

Finding ID: BRF-M1-CR3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: Prepared receipts are the durable mutation boundary and cannot remain structurally valid when their target or authority binding is inconsistent.
Required outcome: Validate receipt target structure and run/change/policy/effective-capability/evidence consistency.
Chosen action: Composed structured target validation into receipts and added run, change, policy, active capability, stage occurrence, input identity, postcondition, outputs, and canonical-sync validation.
Safe resolution path: Reuse structured target validation and cross-check every receipt identity and evidence shape against its run and effective capability.
Validation target: Add incompatible-target, wrong-ID, stale-capability, and empty-evidence regressions; rerun the M1 command set and code-review.
Validation evidence: Receipt regressions reject incompatible targets, mismatched IDs, inactive or mismatched capabilities, and empty/wrong evidence shapes; the full validator suite and broad smoke pass.

#### BRF-M1-CR4 - Exhaustive negative proof matrix

Finding ID: BRF-M1-CR4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: The approved test specification and repository governance require direct fail-closed proof for every new closed vocabulary and named mutation family.
Required outcome: Complete the table-driven policy, vocabulary, authorization, capability, and receipt negative proof matrix.
Chosen action: Expanded table-driven unknown-value, incomplete-policy, occurrence, parent, capability, and receipt proof while preserving the planned vocabulary selector.
Safe resolution path: Expand table-driven unknown-value, incomplete-policy, and stage-relative authority fixtures while preserving the planned test selector.
Validation target: Add explicitly named unknown-value and incomplete-record tests while preserving the planned vocabulary selector; rerun the M1 command set and code-review.
Validation evidence: 9 policy tests, 5 selected vocabulary tests, 25 full validator tests, 4 focused metadata tests, 52 metadata regressions, and 11 broad-smoke checks pass.

### code-review-m1-r2

#### BRF-M1-CR5 - Receipt operation, target, and concrete evidence semantics

Finding ID: BRF-M1-CR5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R2 reproduced a valid later destination rejected by direct capability/target equality and placeholder postcondition/output evidence accepted as recoverable evidence.
Required outcome: Separate the run destination from the concrete capability-bound operation and require concrete receipt evidence.
Chosen action: Removed destination/capability equality, required receipt target equality with the run destination, bounded capability operations by both run and parent targets, and added recursive concrete postcondition/output validation.
Safe resolution path: Validate policy reachability and capability-bound operation independently of the destination; reject null/empty postcondition and output evidence while preserving empty prepared outputs.
Validation target: Targeted regressions, full M1 command set, and code-review M1 R3.
Validation evidence: Proof-first contrast tests failed before implementation and now pass; 30 validator tests, 9 policy tests, 52 metadata tests, and 11 broad-smoke checks pass.

#### BRF-M1-CR6 - Corrected negative proof matrix

Finding ID: BRF-M1-CR6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R2 demonstrated that passing positive and negative fixtures encode contract-invalid semantics.
Required outcome: Correct parent, receipt-operation, destination, and concrete-evidence contrast fixtures.
Chosen action: Replaced the misleading stage-equality test and reduced parent positives with contract-valid destination/operation, target-completeness, and concrete-evidence contrast fixtures.
Safe resolution path: Replace invalid positives and misleading negatives with contract-derived table cases.
Validation target: Full policy, validator, metadata, and broad-smoke proof followed by code-review M1 R3.
Validation evidence: The full 30-test validator suite includes direct positive and negative coverage for every reproduced R2 case and passes.

#### BRF-M1-CR7 - Structured parent maximum target

Finding ID: BRF-M1-CR7
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: A repeated-stage parent authorization can currently be persisted without the occurrence identity required before authorization persistence.
Required outcome: Validate parent maximum targets as complete structured targets, including milestone and plan identity where repeated.
Chosen action: Reused `_validate_target` for parent maximum targets and required milestone, plan, binding-time, and completion identity for repeated targets.
Safe resolution path: Reuse structured-target validation and add complete parent positives plus missing-field negatives.
Validation target: Targeted parent regressions, full M1 command set, and code-review M1 R3.
Validation evidence: Four missing-field parent-target cases fail as required; complete authoring, implementation, and verification parent/capability fixtures pass.

### code-review-m1-r3

#### BRF-M1-CR8 - Canonical transition reachability and policy ownership

Finding ID: BRF-M1-CR8
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R3 reproduced arbitrary and backward from-positions and demonstrated that mutable validator-local reachability tables change validation behavior.
Required outcome: One immutable executable policy projection must validate canonical predecessor, operation, and destination reachability.
Chosen action: Added typed workflow positions and immutable predecessor/successor relations to the policy projection; receipt validation now rejects unknown or invalid predecessor transitions and uses graph reachability for target bounds.
Safe resolution path: Move typed read-only transition relations into the policy projection and add unknown, backward, conditional, correction, repeated-stage, drift, and mutation regressions.
Validation target: Targeted transition-policy proof, full M1 command set, broad smoke, and code-review M1 R4.
Validation evidence: Proof-first tests failed before implementation. After correction, 11 policy tests, 35 automation-validator tests, 4 focused metadata tests, all 52 metadata regressions, and 12 broad-smoke checks pass.

#### BRF-M1-CR9 - Durable concrete evidence values

Finding ID: BRF-M1-CR9
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R3 reproduced whitespace-only and NaN postconditions passing the concrete-evidence validator.
Required outcome: Nested evidence values must be meaningful, finite, serializable, and deterministic.
Chosen action: Strengthened recursive concrete-value and identity validation to require stripped non-empty strings, finite numbers, non-empty containers, acyclic structures, and bounded nesting.
Safe resolution path: Reject stripped-empty strings and non-finite numbers recursively while retaining valid finite values and identity strings.
Validation target: Targeted evidence regressions, full M1 command set, broad smoke, and code-review M1 R4.
Validation evidence: Whitespace, NaN, positive/negative infinity, nested invalid values, and cyclic evidence regressions pass; finite integer and float evidence remains accepted. The full M1 and 12-check broad-smoke suites pass.

### code-review-m1-r4

#### BRF-M1-CR10 - Exact target boundary under cyclic transitions

Finding ID: BRF-M1-CR10
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R4 directly reproduced complete code-review and proposal-correction receipts that occur after their exact targets but pass because generic graph search can cycle back to the target stage name.
Required outcome: Transition validation must preserve the exact structured target as a stopping boundary across correction loops and repeated milestone stages.
Chosen action: Replaced generic graph reachability with immutable target-aware transition rules projected into each stage policy. Receipt validation now evaluates the exact predecessor, concrete operation, and persisted target; correction and repeated-stage cycle edges declare explicit later-target frontiers and occurrence constraints.
Safe resolution path: Replace unqualified reachability with immutable branch- and occurrence-aware transition rules evaluated from the receipt predecessor, concrete operation, and structured target; fail closed when required context is absent.
Validation target: Add complete exact-target negative fixtures, retain valid conditional/correction/repeated paths, run the full M1 command set and broad smoke, then rerun code-review M1.
Validation evidence: Both proof-first complete-state regressions failed before the correction and now pass. Valid immediate review and later-target proposal-correction paths remain accepted by policy tests. The final validation passed 13 policy tests, 37 automation-validator tests, 5 selected vocabulary tests, 4 focused metadata tests, all 52 metadata tests, metadata validation, Python compilation, diff checks, and 12 repository broad-smoke checks in 216 seconds.

### code-review-m1-r5

#### BRF-M1-CR11 - Transition predicates are recorded but never enforced

Finding ID: BRF-M1-CR11
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Rationale: R5 directly reproduced complete architecture-skip and next-milestone receipts that validate without the evidence required by their declared guard and occurrence constraint.
Required outcome: Every selected transition rule must enforce its guard and occurrence constraint against concrete identity-bound evidence and fail closed when required context is absent, mismatched, or ambiguous.
Chosen action: Added an immutable `TransitionContext` and typed `TransitionEvaluation`, centralized all guard and occurrence enforcement in `evaluate_transition`, and renamed the remaining boolean helpers to make their non-authorizing structural purpose explicit. Receipt validation now supplies concrete input evidence, plan identity, and source/destination milestone identities to the evaluator.
Safe resolution path: Add typed predicate-evaluation inputs, require identity-bound branch and source-occurrence evidence, evaluate the selected rule before accepting the transition, and add complete positive and negative fixtures for architecture applicability and milestone ordering.
Validation target: Targeted proof-first predicate-context tests, the full M1 command set, broad smoke, and code-review M1 R6.
Validation evidence: Proof-first policy tests initially failed because the typed evaluator did not exist, and both complete-state validator regressions reproduced zero-error acceptance. After correction, all eight guarded paths have positive and missing-evidence contrasts; proposal correction, architecture applicability, identity-bound same-milestone review, unique next-milestone progression, wrong occurrence, and absent context are covered directly. The final validation passed 15 policy tests, 41 automation-validator tests, 5 selected vocabulary tests, 4 focused metadata tests, all 52 metadata tests, metadata validation, Python compilation, diff checks, and 12 repository broad-smoke checks in the final 231-second run.
