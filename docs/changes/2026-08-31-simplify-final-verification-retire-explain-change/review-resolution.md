# Review Resolution: Simplify Final Verification and Retire Explain Change

## Summary

Closeout status: closed

Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m3-r1
Review closeout: code-review-m3-r2
Review closeout: code-review-m3-r3
Review closeout: code-review-m4-r1
Review closeout: code-review-m4-r2
Review closeout: delivery-review-r2
Review closeout: delivery-review-r3

- Reviews covered: `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m2-r3`, `code-review-m3-r1`, `code-review-m3-r2`, `code-review-m3-r3`, `code-review-m4-r1`, `code-review-m4-r2`, `delivery-review-r2`, `delivery-review-r3`
- Findings resolved: 16
- Unresolved findings: 0
- Current result: Code Review M4 R2 independently confirmed FV-M4-CR1 and FV-M4-CR2 resolved; the corrected M4 implementation is clean. Lifecycle milestone settlement remains blocked by withheld package authority rather than an implementation-review finding.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| FV-M1-CR1 | accepted | resolved | Governed, v1 or legacy, and v2 inventories now use parsed semantic lifecycle contracts and fail closed on unknown or unreadable metadata. |
| FV-M1-CR2 | accepted | resolved | Node, Python, and public-wrapper tests directly reject duplicate and unsorted final-verification manifest entries. |
| FV-M2-CR1 | accepted | resolved | Every proved-surface reference is now closed, unique, and mapped before applicability consistency. |
| FV-M2-CR2 | accepted | resolved | Execution labels now require kind-specific command, hosted, prior-evidence, or cache proof. |
| FV-M2-CR3 | accepted | resolved | Current evidence now requires one exact parsed report plus its matching hash- and subject-bound lifecycle registration. |
| FV-M2-CR4 | accepted | resolved | JavaScript and Python now share identical cardinality and non-empty explanation behavior, backed by direct conformance fixtures. |
| FV-M2-CR5 | accepted | resolved | Successful readiness now requires canonical repository, branch, revision, digest, safe-ID, review-ID, and plan-path identities. |
| FV-M2-CR6 | accepted | resolved | JavaScript and Python now require arrays for all three collections on every outcome and share malformed-collection diagnostics. |
| FV-M2-CR7 | accepted | resolved | Both runtimes and the exported applicability evaluators reject non-boolean evidence facts before semantic interpretation. |
| FV-M3-CR1 | accepted | resolved | V3 accepts only the S-R review-recorded tail; legacy S-R-E remains required only by v1/v2. |
| FV-M3-CR2 | accepted | resolved | Public v3 owner routing is executable through exact review boundaries and v1/v2 reject verification-only reasons. |
| FV-M3-CR3 | accepted | resolved | R3 confirmed every R2 counterexample fails through public transaction and authority probes. |
| FV-M4-CR1 | accepted | resolved | Verify and current handoffs are v3-only; historical v1/v2 records grant no current progression authority. |
| FV-M4-CR2 | accepted | resolved | The shared parsed-YAML mapper rejects duplicate governed keys at every depth before selecting the registered primary plan or any nested authority value. |
| FV-DLR2-01 | accepted | resolved | The plan now binds Design Review R2 consistently at every current upstream authority point. |
| FV-DLR2-02 | accepted | resolved | M5 is non-authoritative with one exact exception; M6 binds and proves the immutable v2 closeout snapshot; activation follows only after M6. |

## Finding Details

### code-review-m1-r1

#### FV-M1-CR1

Finding ID: FV-M1-CR1
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; apply the bounded correction required by the approved contract.
Chosen action: replace raw lifecycle-contract substring discovery with parsed semantic classification for governed records and the frozen v2 inventory.
Rationale: valid YAML representation must not change lifecycle identity, and comments or unrelated text must not select a contract.
Required outcome: wrapper inventory, Node runtime, and Python classifiers agree for quoted, ordinary, unknown, absent, commented, listed, and unlisted contract states.
Safe resolution path: reuse the safe YAML loader and shared classifier, add public wrapper regressions, rerun all M1 commands, and return the corrected M1 diff to Code Review.
Follow-up: Code Review M1 R2 after implementation correction.
Validation target: FV-R5, FV-R6, TG-01, TG-03, BND-COMPAT-001, INT-004.
Validation evidence: Code Review M1 R2 inspected `311b2f3b..17067726`; quoted v2 and v3, misleading-comment, unknown-contract, and public inventory regressions pass. Reviewer probes also proved unrelated scalar text does not select a contract, malformed metadata fails explicitly, and quoted v1 plus unversioned inventory remains valid. The 71-test Node suite, 87-test change-metadata suite, 167-test artifact-lifecycle suite, and 16-test governed-wrapper suite passed.

#### FV-M1-CR2

Finding ID: FV-M1-CR2
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; add the direct proof already allocated by M1.
Chosen action: add duplicate and raw-UTF-8 ordering regressions for the final-verification activation manifest at helper and public boundaries.
Rationale: passing older-manifest ordering tests does not directly prove the newly introduced manifest validator.
Required outcome: duplicate and unsorted new-manifest entries fail directly in Node and Python, and malformed active inventory cannot pass the public wrapper.
Safe resolution path: add named regressions, retain unknown-value-first behavior, rerun all M1 commands, and return the corrected M1 diff to Code Review.
Follow-up: Code Review M1 R2 after implementation correction.
Validation target: TG-02, FV-R5, FV-R6, FV-R38, BND-COMPAT-001.
Validation evidence: Code Review M1 R2 confirmed direct duplicate, raw-UTF-8-unsorted, and unknown-value-first final-manifest tests in Node and Python, plus duplicate and ordering failures at the public wrapper boundary. The complete planned M1 command set passed.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

#### FV-M2-CR1

Finding ID: FV-M2-CR1
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; apply the bounded correction required by the approved evidence-map contract.
Chosen action: validated every proved-surface reference against the closed impact vocabulary and the classified impact map before freshness or decision consistency.
Rationale: freshness can determine execution but cannot authorize an unclassified evidence surface.
Required outcome: unknown, duplicate, or unmapped proved surfaces fail closed and valid multi-surface evidence remains conservative.
Safe resolution path: add identical JavaScript/Python validation and shared regressions, rerun every M2 command, and return M2 for rereview.
Follow-up: Code Review M2 R2.
Validation target: FV-R10, FV-R11, FV-R14, FV-R18, FV-R22, FV-R38, TG-06, TG-07.
Validation evidence: Node and Python regressions reject unknown, duplicate, and unmapped proved surfaces; the exported evaluators also fail closed before freshness. The focused 7-test Node and 16-test Python protocol suites and all five planned M2 commands passed.

#### FV-M2-CR2

Finding ID: FV-M2-CR2
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; implement the already-approved exact command and observed-result contract.
Chosen action: added execution-kind-specific proof identities for evidence and always-current entries.
Rationale: an execution label alone does not prove that a command ran or hosted evidence was observed.
Required outcome: successful reports bind exact command or observation proof, while cache hits and configured-only commands cannot establish a pass.
Safe resolution path: close entry shapes, update resources/skeleton, add direct negative and successful round-trip tests, and rerun M2 validation.
Follow-up: Code Review M2 R2.
Validation target: FV-R20, FV-R21, FV-R22, FV-R26, TG-08.
Validation evidence: exact entry shapes now bind `actual-run` to argv/path/digest proof, `hosted-observation` to provider/run/check/subject/path/digest proof, `reused-pass` to prior evidence identity, `cache-hit` to a cache key, and `not-run` to null proof. Focused negative and success tests plus all planned M2 commands passed.

#### FV-M2-CR3

Finding ID: FV-M2-CR3
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; close the exact report and lifecycle-registration boundary approved by Design.
Chosen action: required and bound both tail members and exact parsed report content, aligned with the actual lifecycle registration schema.
Rationale: an allow-list over supplied paths cannot detect a missing report or registration and cannot grant readiness after partial persistence.
Required outcome: only one complete report plus its matching content registration is current; every partial, mismatched, duplicated, trailing, or drifted state is non-authoritative.
Safe resolution path: replace the subset predicate with exact tail-state validation and add direct write/read-back/registration/replay/drift tests before M3 integration.
Follow-up: Code Review M2 R2.
Validation target: FV-R31-FV-R34, TG-09, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001.
Validation evidence: exact-tail tests reject empty, partial, duplicate, extra-path, malformed, trailing-content, digest-drift, subject-drift, authority-drift, and selector-drift states. Only the report and `change.yaml#lifecycle_cli.validations.verify-result` registration can be current, and the registration is bound to the parsed report digest and verified subject revision. Focused suites and all planned M2 commands passed.

#### FV-M2-CR4

Finding ID: FV-M2-CR4
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; restore the required cross-language conformance contract.
Chosen action: aligned exact always-current cardinality and successful explanation non-empty rules through a direct cross-language fixture matrix.
Rationale: the runtime and repository validator must not disagree about whether the same report grants readiness.
Required outcome: JavaScript and Python return identical outcomes for duplicate checks, whitespace strings, empty list members, malformed collections, and every closed vocabulary.
Safe resolution path: add one shared fixture matrix and mirror error ordering and content validation in both implementations.
Follow-up: Code Review M2 R2.
Validation target: FV-R19, FV-R27, FV-R38, TG-09, BND-STATE-001.
Validation evidence: Python invokes the packaged Node validator against the same payload matrix and compares the complete ordered error arrays. Duplicate always-current entries, whitespace-only explanation strings, empty list members, unknown proved surfaces, malformed basis identities, and missing proof now agree. Both focused suites and all planned M2 commands passed.

#### FV-M2-CR5

Finding ID: FV-M2-CR5
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; enforce existing canonical identity types and formats.
Chosen action: validated each normalized basis member with its repository identity, revision, digest, safe-ID, review-ID, or repository-relative plan-path contract.
Rationale: a non-empty scalar is not necessarily an exact immutable identity.
Required outcome: malformed or unresolved basis values cannot support success, while exact current identities continue to round-trip identically.
Safe resolution path: reuse existing validators, add shared invalid-format fixtures, and rerun M2 validation.
Follow-up: Code Review M2 R2.
Validation target: FV-R8, FV-R26, FV-R31, FV-R33, TG-05, BND-AUTH-001, INT-003.
Validation evidence: shared regressions reject malformed repository and remote identities, branch identities, revisions, digests, safe IDs, review IDs, delivery-plan paths, unresolved strings, and numeric placeholders before readiness. Valid canonical identities continue to round-trip in both runtimes. Focused suites and all planned M2 commands passed.

### code-review-m2-r2

#### FV-M2-CR6

Finding ID: FV-M2-CR6
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; restore the approved single normalized result contract.
Chosen action: made JavaScript and Python enforce identical array shapes and diagnostics for impact, evidence, and always-current collections on every outcome.
Rationale: the same report bytes cannot be authoritative in one runtime and malformed in the other.
Required outcome: null, scalar, mapping, empty-success, and valid empty-non-success partitions have identical acceptance and ordered errors in both runtimes.
Safe resolution path: add explicit JavaScript collection-shape checks, align error order, extend the shared conformance matrix, rerun all M2 commands, and return for Code Review M2 R3.
Follow-up: Code Review M2 R3 after bounded implementation correction.
Validation target: FV-R26, FV-R28, FV-R34, TG-09, BND-STATE-001.
Validation evidence: shared conformance cases cover null, string, mapping, and numeric collection values for all three fields. Both runtimes reject them with the same ordered errors, preserve valid empty non-success collections, and reject empty successful collections. The 9-test Node and 18-test Python focused suites plus all five planned M2 commands passed.

#### FV-M2-CR7

Finding ID: FV-M2-CR7
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; enforce the staged evidence entry's existing boolean facts.
Chosen action: required JSON booleans for authority, identity, environment, conflict, new-obligation, and cache-hit fields before decision consistency.
Rationale: incidental strict-comparison fall-through cannot normalize malformed evidence facts or support branch-ready.
Required outcome: only true/false values are accepted; strings, numbers, null, objects, and lists fail in both runtimes before a successful result is considered.
Safe resolution path: add explicit type validation and a shared boolean conformance matrix, retain conservative decision precedence, rerun all M2 commands, and return for Code Review M2 R3.
Follow-up: Code Review M2 R3 after bounded implementation correction.
Validation target: FV-R14-FV-R17, FV-R21, FV-R26, TG-07-TG-09, BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001.
Validation evidence: both validators reject strings, numbers, null, mappings, and lists for all six evidence facts, while accepting actual true/false values. The exported applicability evaluators also reject malformed applicability booleans directly. The cache-separation fixture now supplies structurally valid boolean facts and still proves cache hits cannot satisfy required execution. Focused suites and all five planned M2 commands passed.

### code-review-m2-r3

No material findings.

### code-review-m3-r1

#### FV-M3-CR1

Finding ID: FV-M3-CR1
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Decision owner: M3 implementer
Decision needed: none; enforce the approved v3 S-R-V boundary.
Chosen action: reject every v3 pre-Verify state containing an explanation recording or handoff revision while retaining the legacy complete-tail requirement for v1/v2.
Rationale: removing the stage graph edge is insufficient if readiness still consumes its durable evidence commit.
Required outcome: v3 accepts exactly S-R before Verify; S-R-E fails for v3 and remains required for v1/v2.
Safe resolution path: tighten the contract-keyed tail guard and add direct object plus repository-backed compatibility tests.
Follow-up: Code Review M3 R2 after implementation correction.
Validation target: FV-R1, FV-R2, FV-R28, FV-R31-FV-R34, TG-10, TG-12, BND-STATE-001, BND-TEMPORAL-001, INT-003.
Validation evidence: `python scripts/test-workflow-code-state.py` passed 19 tests. The direct guard proves v3 S-R succeeds, v3 S-R-E fails, and the identical S-R-E state remains required by v1/v2. `python scripts/test-workflow-automation.py` passed 78 tests, including repository-backed v3 readiness without explanation input.

#### FV-M3-CR2

Finding ID: FV-M3-CR2
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Decision owner: M3 implementer
Decision needed: none under the approved owner map; route to Design only if external-evidence acquisition cannot be represented without a new lifecycle decision.
Chosen action: compose the closed owner classifier with an executable contract-keyed Workflow correction transaction and rereview return boundary.
Rationale: an unused lookup table identifies ownership but does not route a failed Verify attempt or enforce no-repair authority.
Required outcome: all seven finding kinds route to exactly one non-Verify owner; wrong, unknown, and Verify-owned routes fail without mutation; corrections return through required review and Verify.
Safe resolution path: integrate routing and add public/request-path matrices while preserving v1/v2 correction behavior.
Follow-up: Code Review M3 R2 after implementation correction.
Validation target: FV-R23-FV-R25, FV-R30, TG-11, TG-12, BND-AUTH-001, BND-RECOVERY-001, INT-002.
Validation evidence: Code Review M3 R3 reran the 89-pass/2-skip lifecycle suite and every planned M3 command. Public matrices confirmed all seven exact route-and-return outcomes, legacy rejection, blocker clearing, and invalid-owner no-mutation behavior; active-route probes rejected non-routed and mismatched v3 artifact revisions.

### code-review-m3-r2

#### FV-M3-CR3

Finding ID: FV-M3-CR3
Disposition: accepted
Status: resolved
Owner: M3 implementer
Owning stage: review-resolution
Decision owner: M3 implementer
Decision needed: none; complete the already approved correction, rereview, and compatibility boundaries.
Chosen action: keep FV-M3-CR2 open and correct both the artifact-owner rereview escape and v2 verification-reason leakage.
Rationale: R2 independently reproduced both outcomes after the claimed CR2 correction and therefore classifies the remediation as failed.
Required outcome: public v3 correction transactions reach every exact owner and cannot re-enter Verify before required consolidated review; v1/v2 reject verification-only correction semantics; invalid routes never mutate state.
Safe resolution path: key correction vocabularies and return behavior by lifecycle contract and source, then add public route-and-return matrices for all owners and legacy rejection cases.
Follow-up: Code Review M3 R3 after bounded implementation correction.
Validation target: FV-R23-FV-R25, FV-R30, TG-11, TG-12, BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001, INT-002.
Validation evidence: Code Review M3 R3 directly confirmed v1/v2 rejection without mutation, all seven public v3 owner returns, consolidated review stops, cleared Verify blocker, invalid-owner no-mutation, unchanged legacy suites, and exact active-route-only artifact revision authority.

### code-review-m3-r3

No material findings.

### code-review-m4-r1

#### FV-M4-CR1

Finding ID: FV-M4-CR1
Disposition: accepted
Status: resolved
Owner: M4 implementer
Owning stage: review-resolution
Decision owner: M4 implementer
Decision needed: none; the user selected the newest-contract-only rule and Design Review R2 approved it.
Chosen action: make Verify and every current handoff v3-only, with historical v1/v2 records readable but non-executable; prove the same semantics in all staged candidates.
Rationale: one current contract avoids both the impossible candidate dependency and a permanent compatibility checker. The implementing change's v2 closeout is bound separately to an immutable reviewed snapshot.
Required outcome: current Verify accepts no standalone explanation input, creates no explanation on failure, creates the final explanation only on success, and no current skill route grants v1/v2 progression.
Safe resolution path: update canonical Verify and workflow clauses, add semantic canonical and three-adapter candidate regressions, rerun all M4 commands, and return for Code Review M4 R2.
Follow-up: Code Review M4 R2 after bounded implementation correction.
Validation target: FV-R1-FV-R3, FV-R24, FV-R27, FV-R28, FV-R35-FV-R38, TG-15, TG-16, TG-18, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001, INT-002, INT-004.
Validation evidence: Code Review M4 R2 inspected the complete corrected M4 diff, confirmed canonical and all three generated candidate semantics, and reran 386 skill tests, 156 adapter tests, canonical skill validation for 21 skills, 8 build tests, and generated-skill drift checking.

#### FV-M4-CR2

Finding ID: FV-M4-CR2
Disposition: accepted
Status: resolved
Owner: M4 implementer
Owning stage: review-resolution
Decision owner: M4 implementer
Decision needed: none; make existing safe parsing fail closed at every mapping depth.
Chosen action: reject recursive duplicate mapping keys before any lifecycle or registered-plan authority is selected.
Rationale: last-wins parsing lets ambiguous nested metadata choose a different plan, kind, role, or path.
Required outcome: duplicate `artifact_states`, `plan`, `kind`, `role`, or `path` keys fail for both v2 and v3 regardless of ordering, while valid metadata and active v2 behavior remain unchanged.
Safe resolution path: correct the shared parser or boundary parser, add direct reversal fixtures at every nested authority level, rerun all M4 commands, and return for Code Review M4 R2.
Follow-up: Code Review M4 R2 after bounded implementation correction.
Validation target: TG-17, BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001.
Validation evidence: Code Review M4 R2 confirmed the shared parsed-YAML mapper rejects duplicates before assignment at every recursive depth, the boundary validator has no separate raw-text duplicate scan, direct probes reject all five authority key families, and 69 boundary plus 107 metadata-validator tests pass.

### code-review-m4-r2

No material findings.

### delivery-review-r2

#### FV-DLR2-01

Finding ID: FV-DLR2-01
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: plan author
Decision needed: none; update the plan's exact approved Design authority.
Chosen action: replace current `design-review-r1` authority references with `design-review-r2` and return the new plan revision for Delivery Review.
Rationale: R1 approved superseded compatibility machinery and cannot authorize the revised sole-current-v3 plan.
Required outcome: every current upstream Design reference in the plan and Delivery package matches settled `design-review-r2`.
Safe resolution path: revise only plan-owned authority references, record the plan revision through the lifecycle CLI after Design settlement, and request Delivery Review R3.
Follow-up: Delivery Review R3.
Validation target: package upstream identity and requirement-to-delivery authority trace.
Validation evidence: Delivery Review R3 found only `design-review-r2` at current authority points and confirmed the registered plan hash `5bdf89552ab9a0f88988c62f5d9ae57dae8e12a184d18bb678fc73254fa81514`.

#### FV-DLR2-02

Finding ID: FV-DLR2-02
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: plan author
Decision needed: none; allocate the already-approved closeout-before-activation boundary without circular prerequisites.
Chosen action: treat M5 as non-authoritative candidate assembly, bind M6 to one immutable trusted v2 tool/package and direct closeout proof, and defer the universal completion/activation record until after M6.
Rationale: the current M5 completion dependency includes this still-open change, while M6 depends on M5 and lacks an executable identity for the removed v2 runtime.
Required outcome: M5 can start without claiming this change complete; M6 can provably close the exact v2 record after source retirement; public activation occurs only after zero nonterminal pre-v3 changes are revalidated.
Safe resolution path: revise dependencies, TGs, evidence expectations, commands, tool identities, integrity checks, and recovery boundaries, then request Delivery Review R3.
Follow-up: Delivery Review R3.
Validation target: FV-R7, FV-AC12, BND-AUTH-001, BND-RECOVERY-001, BND-COMPAT-001, TG-23, TG-26, TG-FINAL-03.
Validation evidence: Delivery Review R3 reproduced the bound archive, explain-change skill, Verify skill, and CLI hashes; confirmed the sole M5 exception and absence of activation evidence; and confirmed M6 extracted mutation plus dual read-back and post-M6 zero-nonterminal activation allocation.

### delivery-review-r3

No material findings.
