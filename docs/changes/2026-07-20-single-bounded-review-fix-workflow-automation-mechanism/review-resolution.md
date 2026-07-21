# Review Resolution: Single Bounded Review-Fix Workflow Automation Mechanism

## Summary

Closeout status: closed

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

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `spec-review-r4`, `spec-review-r5`, `architecture-review-r1`, `architecture-review-r2`, `architecture-review-r3`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `test-spec-review-r3`, `test-spec-review-r4`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m1-r4`, `code-review-m1-r5`
- Findings resolved: 33
- Unresolved findings: 0
- Current result: `BRF-M1-CR11` is resolved with one typed fail-closed transition evaluator, complete guard and occurrence contrasts, the full M1 command set, and repository broad smoke. M1 is ready for fresh code review; M2 remains blocked pending approval.

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

## Common Resolution Metadata

- Owner: proposal owner
- Owning stage: proposal
- Validation target: Proposal-review closeout and proposal lifecycle normalization before specification
- Validation evidence: Focused validation passed and proposal-review R4 approved with no material findings

## Finding Details

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
- [x] No review-log findings remain open.
- [x] Closeout status is closed with final dispositions and validation evidence.

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
