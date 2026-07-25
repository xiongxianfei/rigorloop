# Single Bounded Review-Fix Workflow Automation Test Specification

## Status

active

## Related spec and plan

- Spec: [Single Bounded Review-Fix Workflow Automation](single-bounded-review-fix-workflow-automation.md)
- Plan: [Single Bounded Review-Fix Workflow Automation Plan](../docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md)
- Architecture: [RigorLoop Canonical System Architecture](../docs/architecture/system/architecture.md)
- ADR: [ADR-20260721 Single Bounded Review-Fix Workflow Automation Mechanism](../docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md)

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | `specs/single-bounded-review-fix-workflow-automation.md` | approved; spec-review R5 approved | SHA-256 `59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070` |
| Spec review | `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r5.md` | approved | SHA-256 `b5f2c146a37b71cd9c616bc49caffcc3d99beb0adfe629fbacd45e99c40e27a2` |
| Architecture | `docs/architecture/system/architecture.md` | approved; architecture-review R3 approved | SHA-256 `3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8` |
| Architecture review | `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/architecture-review-r3.md` | approved | SHA-256 `0eee15e80d7a6936d3bfd562ddb1eaa442dddf790111a7584211a5de80cb6493` |
| ADR | `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md` | accepted | SHA-256 `72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538` |
| Execution plan | `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` | active; plan-review R2 approved; test-spec revision awaiting rereview | SHA-256 `2d3ed1ce7d6bccdeb729482d72eff2cd62a5c70f529b5a4b4b4050f1f5e0a326` |
| Plan review | `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/plan-review-r2.md` | approved | SHA-256 `823197aca7c83296c879de2e65db3c41c8e09a6dbfcfaf0380506a3f8f09fc40` |
| Test-spec review | `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r3.md` | changes-requested; BRF-TSR1 through BRF-TSR3 resolved; BRF-TSR4 completed pending R4 | SHA-256 `c2cc4959b320972dc8c753c31ff0a616a94c2c5130aea3d7e4c6ed43a5b2d555` |

Implementation and the first milestone code review must recheck these identities.
A substantive upstream change makes this test spec stale and returns the initiative to the owning upstream review gate.

## Testing strategy

- Unit tests prove closed vocabularies, legal transitions, immutable stage policies, target binding, authorization and capability predicates, receipt reconciliation, migration projection, and status formatting.
- Integration tests compose the command adapter, canonical-position resolver, stage-policy registry, authority evaluator, sole state writer, lifecycle parsers, review evidence, and stage-owned completion evidence.
- End-to-end tests use a temporary repository fixture to traverse proposal review through final verify, including pauses and resumes, without opening a PR or performing any external action.
- Smoke tests prove the atomic public cutover, canonical skill generation, adapter generation and validation, selected CI, and repository broad smoke.
- Contract tests compare the immutable Python registry and exact cross-spec disposition ledger to the approved spec rather than maintaining a second hand-authored policy source.
- Migration tests prove dual-read/single-write behavior, one-way mutating migration, indefinite terminal reads, cancellation, and mixed-writer rejection.
- Manual proof is limited to review-independence inspection, C4/write-boundary inspection, and confirmation that no external side effects or secrets are introduced.
- Determinism proof fixes time, IDs, locale, timezone, environment, temporary roots, and execution order so transactional and migration evidence is reproducible.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| BRF-R001, BRF-R002, BRF-R003, BRF-R003a, BRF-R003b, BRF-R003c, BRF-R003d | T1, T24, T25 | integration | One writable mechanism and one normative owner; ordinary lifecycle continuation creates no automation state. |
| BRF-R004, BRF-R005, BRF-R006 | T20, T22, T25 | integration | Current commands, compatibility adapters, and read-only status converge on unified state. |
| BRF-R007, BRF-R007a, BRF-R007b, BRF-R007c | T16 | integration | Cancellation reconciles first and has deterministic idempotent results. |
| BRF-R008, BRF-R008a, BRF-R008b, BRF-R008c, BRF-R008d, BRF-R008e, BRF-R008f, BRF-R008g, BRF-R008h, BRF-R008i, BRF-R008j | T2 | unit | Separate closed vocabularies, legal transitions, pause ownership, and capability consumption. |
| BRF-R009, BRF-R010, BRF-R011, BRF-R012, BRF-R013, BRF-R014, BRF-R015 | T4, T5, T9 | integration | Structured targets bind occurrence without widening consent or skipping gates. |
| BRF-R016, BRF-R017 | T26 | integration | Conditional architecture handling is deterministic. |
| BRF-R017a, BRF-R017b, BRF-R017c, BRF-R017d, BRF-R017e, BRF-R017f | T4, T5 | integration | Closed occurrence matrix and exact repeated-stage diagnostics. |
| BRF-R018, BRF-R019, BRF-R020, BRF-R021, BRF-R022, BRF-R023 | T6 | integration | Pre-plan derivation and post-plan ownership handoff do not create a second cursor. |
| BRF-R024, BRF-R025, BRF-R026, BRF-R027, BRF-R028, BRF-R029, BRF-R030, BRF-R031 | T7, T18 | integration | Parent consent is bounded, non-executable, risk-scoped, and excludes external actions. |
| BRF-R032, BRF-R033, BRF-R034, BRF-R035, BRF-R036, BRF-R037, BRF-R038, BRF-R039, BRF-R040, BRF-R041, BRF-R042, BRF-R043 | T8 | integration | Effective capabilities bind valid parents and complete stage-relative bases. |
| BRF-R043a, BRF-R043b, BRF-R043c, BRF-R043d, BRF-R043e | T9 | integration | Verify target and verification consent are independent. |
| BRF-R044, BRF-R045, BRF-R046 | T8, T15 | integration | Material basis or scope change invalidates rather than mutates authority. |
| BRF-R047, BRF-R048, BRF-R049, BRF-R050, BRF-R051, BRF-R052, BRF-R053, BRF-R054, BRF-R055, BRF-R056, BRF-R057, BRF-R058, BRF-R059 | T10 | integration | Occurrence, gate, routing, scope, and all review outcomes are exhaustive. |
| BRF-R060, BRF-R061, BRF-R062 | T11, T12 | integration | Reviews stay independent; proposal correction remains driver-owned and bounded. |
| BRF-R063, BRF-R064, BRF-R065, BRF-R066, BRF-R067 | T11, T13, T18 | integration | Implementation correction is reviewer-owned; stale review and verify failure pause. |
| BRF-R068, BRF-R069, BRF-R070, BRF-R071, BRF-R072 | T14, T29, T30 | integration | Prepared receipts precede mutation, bind exact executable authority, and remain deterministic at the state and composed-engine boundaries. |
| BRF-R073, BRF-R074, BRF-R075, BRF-R076, BRF-R077 | T15, T29, T30 | integration | Evidence-first resume is exhaustive, fail-closed, and order-independent at both executable boundaries. |
| BRF-R078, BRF-R079, BRF-R080 | T3, T12 | contract | Complete policies coordinate but do not replace stage owners; internal stages stay non-public. |
| BRF-R081, BRF-R082, BRF-R083, BRF-R084 | T17 | integration | Implementation and milestone review completion remain distinct and ordered. |
| BRF-R085, BRF-R086 | T18 | e2e | Final closeout evidence is required and successful verify stops before PR. |
| BRF-R087, BRF-R088, BRF-R089, BRF-R090 | T12, T18, T27 | integration | Direct review and bugfix isolation remain; recording remains mandatory; external actions are prohibited. |
| BRF-R091, BRF-R092, BRF-R093, BRF-R094, BRF-R095, BRF-R096, BRF-R097, BRF-R098 | T19, T29, T30 | migration | Migration is readable, one-way, auditable, deterministic, and never restores retired writers. |
| BRF-R098a, BRF-R098b, BRF-R098c, BRF-R098d | T20 | migration | Legacy command adapters remain supported and write only unified state. |
| BRF-R098e, BRF-R098f, BRF-R098g, BRF-R098h, BRF-R098i | T21 | contract | Exact dispositions, selector uniqueness, closed affected set, and status settlement are validated. |
| BRF-R099, BRF-R100 | T22, T30 | integration | Result and resume evidence are complete, tracked, and reproducible without hidden process state. |
| BRF-R101, BRF-R102 | T2, T3, T21 | contract | Unknown-value rejection precedes consistency checks and has direct regressions. |
| BRF-AC001 through BRF-AC009 | T1, T4, T6, T7, T8 | integration | Unified state, target, position, parent, and capability acceptance proof. |
| BRF-AC010 through BRF-AC014 | T10, T11 | integration | Proposal review bootstrap, separated capabilities, outcomes, and no-spin behavior. |
| BRF-AC015 through BRF-AC017 | T14, T15, T29, T30, T5 | integration | Write-ahead recovery, deterministic composition, and stable repeated targets. |
| BRF-AC018 through BRF-AC022 | T17, T13, T11, T18, T12, T27 | integration | Ordered review, correction ownership, final verify, isolation, and external prohibition. |
| BRF-AC023 through BRF-AC026 | T19, T2, T22, T20 | migration | Migration, fail-closed vocabularies, status, and compatibility adapters. |
| AC-BRF-SR1-1 through AC-BRF-SR1-5 | T4, T5 | integration | Stage/occurrence binding contract. |
| AC-BRF-SR2-1 through AC-BRF-SR2-6 | T2, T16 | integration | Durable state and cancellation contract. |
| AC-BRF-SR3-1 through AC-BRF-SR3-5 | T9 | integration | Verification authorization timing contract. |
| AC-BRF-SR4-1 through AC-BRF-SR4-6 | T20 | migration | Legacy alias contract. |
| AC-BRF-SR5-1 through AC-BRF-SR5-5 | T21 | contract | Cross-spec disposition contract. |
| AC-BRF-SR6-1 through AC-BRF-SR6-4 | T21 | contract | Selector registry and approval-settlement contract. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 proposal review before approval | T8, T10 | Proposal-review basis has no circular prior-review requirement and permits review evidence only. |
| E2 later target pauses at risk boundary | T7, T9, T28 | Final target persists while missing later authority pauses. |
| E3 bounded proposal correction | T11 | Eligible fixes invalidate old gate evidence and require rereview. |
| E4 inconclusive review pauses | T10 | No rerun occurs without material evidence change. |
| E5 milestone target remains bound | T5, T17 | `code-review@M2` never becomes M3. |
| E6 interrupted transition reconciles | T14, T15, T29, T30 | Completion evidence is reconciled without duplicate work and remains deterministic at both executable boundaries. |
| E7 active legacy state migrates once | T19 | Explicit mutating resume writes one migration receipt. |
| E8 direct review remains isolated | T12 | Formal evidence is recorded without run creation or advancement. |
| E9 repeated target binds before persistence | T5 | Current plan and milestone identities are persisted first. |
| E10 cancellation has one durable result | T16 | Run, parents, capabilities, and receipts settle deterministically. |
| E11 verify target precedes verification consent | T9 | No future-contingent verification authorization is stored. |
| E12 legacy verify alias uses unified writer | T20 | Compatibility mapping writes no retired profile state. |

## Edge case coverage

| Edge cases | Covered by | Expected proof |
| --- | --- | --- |
| EC1-EC5 | T7, T8 | Stage-relative basis, parent class, revocation propagation, and scope expansion fail safely. |
| EC6-EC8 | T10, T11 | Exact review target, inconclusive no-spin, and stale approval behavior. |
| EC9, EC15-EC18 | T4, T5 | Repeated target binding, invalid pairs, missing plan, and no rebinding. |
| EC10 | T15 | Partial files are not completion evidence. |
| EC11, EC12, EC22, EC23 | T19, T20 | Mixed writers fail; status is read-only; legacy off migrates and cancels. |
| EC13 | T26 | Explicit architecture-review returns target-not-applicable. |
| EC14, EC21 | T9, T18 | Early target persists; verify failure pauses without repair. |
| EC19, EC20 | T2, T16 | Terminal resume fails; cancellation reconciles an in-flight receipt. |
| EC24-EC26 | T21 | Missing, duplicate, contradictory, and absent selectors follow the closed registry contract. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-workflow-automation-policy.py` | planned-for-implementation | automation policy tests | M1 | M1 code-review | blocks M1 | zero tests blocks M1 | active plan validation notes | local read/test only |
| CMD2 | `python scripts/test-validate-workflow-automation.py -k vocabulary` | planned-for-implementation | automation validator tests | M1 | M1 code-review | blocks M1 | zero selected tests blocks M1 | active plan validation notes | local read/test only |
| CMD3 | `python scripts/test-change-metadata-validator.py -k workflow_automation` | existing/configured | change metadata tests | M1 | M1 code-review | blocks M1 | zero selected tests blocks M1 | active plan validation notes | temporary fixtures only |
| CMD4 | `python scripts/test-change-metadata-validator.py` | existing/configured | change metadata tests | M1 | M1 code-review | blocks milestone and later cutover | zero tests blocks milestone | active plan validation notes | temporary fixtures only |
| CMD5 | `python scripts/validate-change-metadata.py docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml` | existing/configured | change metadata validator | M1 | every metadata handoff | blocks handoff | not applicable | change metadata validation ledger | read-only validation |
| CMD6 | `python scripts/test-workflow-automation-state.py` | planned-for-implementation | automation state tests | M2 | M2 code-review | blocks M2 | zero tests blocks M2 | active plan validation notes | temporary files only |
| CMD7 | `python scripts/test-validate-workflow-automation.py -k receipt` | planned-for-implementation | automation validator tests | M2 | M2 code-review | blocks M2 | zero selected tests blocks M2 | active plan validation notes | local read/test only |
| CMD8 | `python scripts/test-validate-workflow-automation.py -k migration` | planned-for-implementation | automation validator tests | M2 | M2 code-review | blocks M2 | zero selected tests blocks M2 | active plan validation notes | temporary fixtures only |
| CMD9 | `python scripts/test-query-change-record.py` | existing/configured | change-record query tests | M2 | M2 code-review | blocks M2 | zero tests blocks M2 | active plan validation notes | read-only queries and temporary fixtures |
| CMD10 | `python scripts/test-workflow-automation.py -k target` | planned-for-implementation | automation engine tests | M3 | M3 code-review | blocks M3 | zero selected tests blocks M3 | active plan validation notes | non-public temporary harness |
| CMD11 | `python scripts/test-workflow-automation.py -k position` | planned-for-implementation | automation engine tests | M3 | M3 code-review | blocks M3 | zero selected tests blocks M3 | active plan validation notes | non-public temporary harness |
| CMD12 | `python scripts/test-workflow-automation.py -k capability` | planned-for-implementation | automation engine tests | M3 | M3 code-review | blocks M3 | zero selected tests blocks M3 | active plan validation notes | non-public temporary harness |
| CMD13 | `python scripts/test-artifact-lifecycle-validator.py -k automation` | existing/configured | lifecycle validator tests | M3 | M3 code-review | blocks M3 | zero selected tests blocks M3 | active plan validation notes | temporary fixtures only |
| CMD14 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | lifecycle validator tests | M3 | M3 code-review | blocks milestone and later cutover | zero tests blocks milestone | active plan validation notes | temporary fixtures only |
| CMD15 | `python scripts/test-workflow-automation.py -k proposal_review` | planned-for-implementation | automation engine tests | M4 | M4 code-review | blocks M4 | zero selected tests blocks M4 | active plan validation notes | non-public temporary harness |
| CMD16 | `python scripts/test-workflow-automation.py -k proposal_correction` | planned-for-implementation | automation engine tests | M4 | M4 code-review | blocks M4 | zero selected tests blocks M4 | active plan validation notes | non-public temporary harness |
| CMD17 | `python scripts/test-workflow-automation.py -k authoring` | planned-for-implementation | automation engine tests | M4 | M4 code-review | blocks M4 | zero selected tests blocks M4 | active plan validation notes | non-public temporary harness |
| CMD18 | `python scripts/test-workflow-automation.py -k non_public` | planned-for-implementation | automation engine tests | M4 | M4 code-review | blocks M4 and every later public-boundary handoff; rerun before M5 code-review | zero selected tests blocks milestone | active plan validation notes | proves harness is unreachable publicly |
| CMD19 | `python scripts/test-review-artifact-validator.py` | existing/configured | review evidence tests | M4 | M4 code-review | blocks milestone and cutover | zero tests blocks milestone | active plan validation notes | temporary fixtures only |
| CMD20 | `python scripts/test-skill-validator.py` | existing/configured | skill contract tests | M4 | M4 code-review | blocks milestone and cutover | zero tests blocks milestone | active plan validation notes | canonical skill reads only |
| CMD21 | `python scripts/test-workflow-automation.py -k implementation` | planned-for-implementation | automation engine tests | M5 | M5 code-review | blocks M5 | zero selected tests blocks M5 | active plan validation notes | non-public temporary harness |
| CMD22 | `python scripts/test-workflow-automation.py -k correction` | planned-for-implementation | automation engine tests | M5 | M5 code-review | blocks M5 | zero selected tests blocks M5 | active plan validation notes | non-public temporary harness |
| CMD23 | `python scripts/test-workflow-automation.py -k milestone` | planned-for-implementation | automation engine tests | M5 | M5 code-review | blocks M5 | zero selected tests blocks M5 | active plan validation notes | non-public temporary harness |
| CMD24 | `python scripts/test-workflow-automation.py -k verify` | planned-for-implementation | automation engine tests | M5 | M5 code-review | blocks M5 | zero selected tests blocks M5 | active plan validation notes | no PR, network, credentials, or external mutation |
| CMD25 | `python scripts/test-workflow-automation.py` | planned-for-implementation | automation engine tests | M6 | M6 code-review | blocks cutover | zero tests blocks cutover | active plan validation notes | temporary repository; external actions disabled |
| CMD26 | `python scripts/test-validate-workflow-automation.py` | planned-for-implementation | automation validator tests | M6 | M6 code-review | blocks cutover | zero tests blocks cutover | active plan validation notes | local read/test only |
| CMD27 | `python scripts/validate-skills.py` | existing/configured | skill validator | M6 | M6 code-review | blocks cutover | not applicable | active plan validation notes | canonical skill reads only |
| CMD28 | `python scripts/build-skills.py --check` | existing/configured | skill generator | M6 | M6 code-review | blocks cutover | not applicable | active plan validation notes | check mode; no tracked writes |
| CMD29 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution tests | M6 | M6 code-review | blocks cutover | zero tests blocks cutover | active plan validation notes | temporary output only |
| CMD30 | `adapter_version="$(awk '$1 == "version:" {print $2; exit}' dist/adapters/manifest.yaml)" && test -n "$adapter_version" && adapter_output="$(mktemp -d)" && trap 'rm -rf "$adapter_output"' EXIT && python scripts/build-adapters.py --version "$adapter_version" --output-dir "$adapter_output" && python scripts/validate-adapters.py --root "$adapter_output" --version "$adapter_version"` | existing/configured | adapter build and validation | M6 | M6 code-review | blocks cutover | not applicable | active plan validation notes | manifest-derived generated temporary output only; no publication/network |
| CMD31 | `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path schemas/change.schema.json --path scripts/workflow_automation.py --path scripts/workflow_automation_policy.py --path scripts/workflow_automation_state.py --path scripts/validate_workflow_automation.py` | existing/configured | selected CI wrapper | M6 | M6 code-review | blocks cutover | any selected test command with zero tests blocks its owning proof | active plan validation notes | local selected checks only |
| CMD32 | `bash scripts/ci.sh --mode broad-smoke` | existing/configured | repository broad smoke | M6 | M6 code-review and final verify | blocks cutover and final readiness | any test suite unexpectedly collecting zero tests blocks | active plan and verify evidence | local repository validation; no publication |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1-T4, T7, T8 | none | CMD1-CMD5 | test output and active plan validation notes | M1 code-review | No writer or public routing is enabled. |
| M2 | T14-T16, T19, T23, T29 | none | CMD4-CMD9 | test output and active plan validation notes | M2 code-review | State replacement, reconciliation, and deterministic repetition use fresh temporary repositories. |
| M3 | T4-T9, T14 | none | CMD10-CMD14 | test output and active plan validation notes | M3 code-review | Only one stage is coordinated through the non-public engine. |
| M4 | T10-T12, T24, T26 | MP1 | CMD14-CMD20 | test output, skill diff, and active plan validation notes | M4 code-review | Public commands and aliases remain unchanged. |
| M5 | T13, T17, T18, T24 | MP1, MP2 | CMD14, CMD18-CMD24 | test output, skill diff, and active plan validation notes | M5 code-review | Final holistic review remains distinct; PR boundary is not crossed. |
| M6 | T1, T12, T16, T18-T23, T25-T28, T30 | MP1-MP3 | CMD4, CMD14, CMD19, CMD20, CMD25-CMD32 | test output, generated temporary adapter evidence, plan validation notes, and final review evidence | M6 code-review; CMD32 again before final verify | Public activation and legacy-writer removal occur atomically and repeatably. Earlier focused cases may run as regression coverage, but they are not separate M6 proof obligations unless listed here. |

### Progressive milestone activation

Commands and assertions listed for a later activation are planned but not required at an earlier gate.
A milestone depends only on the commands in its milestone row and the activation entry below; omitted later-owned commands do not block the earlier milestone.

| Test ID | Earlier activation | Later activation | Explicit deferral |
| --- | --- | --- | --- |
| T1 | M1: CMD3-CMD4 prove schema exclusivity, duplicate-run rejection, and no automation write from ordinary lifecycle continuation. | M6: CMD25-CMD26 prove the same invariant through the publicly composed engine and validator. | Public routing and composed-engine assertions are planned for M6 and are not required at M1. |
| T4 | M1: CMD1 proves the closed stage/occurrence policy matrix. | M3: CMD10 proves command target resolution and pre-persistence rejection. | Engine target resolution is planned for M3 and is not required at M1. |
| T7 | M1: CMD2 proves parent record shape, vocabulary, and non-executable status. | M3: CMD12 proves derivation, cross-risk rejection, and direct-execution refusal. | Capability derivation behavior is planned for M3 and is not required at M1. |
| T8 | M1: CMD2 proves capability record shape and stage-relative required fields. | M3: CMD12 proves live derivation, subset scope, invalidation, and conflict handling. | Engine derivation and invalidation behavior is planned for M3 and is not required at M1. |
| T9 | M3: CMD12 proves verify-target persistence without future-contingent authority. | M5: CMD24 proves the live verification-boundary pause and invocation prohibition. | Verification-stage invocation behavior is planned for M5 and is not required at M3. |
| T12 | M4: CMD18-CMD20 prove authoring-review independence, direct-invocation isolation, and non-public support stages. | M6: CMD20 and CMD27 recheck the final composed public skill surface and formal-review isolation. | Final public-surface inspection is planned for M6 and is not required at M4. |
| T14 | M2: CMD6-CMD7 prove prepared-receipt ordering and persistence. | M3: CMD12 proves the receipt-to-capability-to-parent authority chain during engine coordination. | Coordinator authority-chain proof is planned for M3 and is not required at M2. |
| T16 | M2: CMD6-CMD7 prove durable cancellation settlement and prepared-receipt reconciliation. | M6: CMD25 proves public `off` orchestration and idempotent composed behavior. | Public command orchestration is planned for M6 and is not required at M2. |
| T18 | M5: CMD24 proves verification gates, failure pause, and no repair or PR action. | M6: CMD25 proves final composed closeout through successful verify. | Full public composition is planned for M6 and is not required at M5. |
| T19 | M2: CMD8-CMD9 prove read-only projection, one-way state migration, and mixed-writer rejection. | M6: CMD25-CMD26 prove migration through the final engine and validator. | Composed migration routing is planned for M6 and is not required at M2. |
| T22 | M2: CMD9 proves read-only query fields and state-hash stability. | M6: CMD25 proves final public result, help, diagnostic, and resume output. | Public engine output is planned for M6 and is not required at M2. |
| T23 | M2: CMD6 proves atomic replacement, drift detection, and sole-writer behavior. | M6: CMD26 plus MP3 prove final caller coverage and architecture/write-boundary conformance. | Final executable-call-graph inspection is planned for M6 and is not required at M2. |
| T24 | M4: CMD18 and CMD20 prove authoring-stage integration remains non-public. | M5: CMD18 and CMD20 rerun the boundary after implementation-stage integration. | M5 rerun is not required for M4 closeout. |
| T26 | M4: CMD17 proves required, not-required, and ambiguous architecture routing through the non-public authoring harness. | M6: CMD25 proves the same conditional routing through the final publicly composed engine. | Public-route composition is planned for M6 and is not required at M4. |
| T27 | M6: CMD20, CMD27, and CMD32 prove the final security and external-action boundary. | Final verify: rerun CMD32 and recheck MP2 evidence. | Final-verify recheck is not required for M6 code-review closeout. |

Manual proof contracts:

### MP1. Formal review independence and isolated recording

- Automation rationale: Static tests prove required markers and routes, but a reviewer must inspect the composed skill and fixture diff to confirm that authoring and review responsibilities remain semantically independent.
- Owner: milestone code reviewer.
- Owning stage: code-review.
- Required environment: Local tracked worktree at the M4, M5, or M6 review boundary; canonical `skills/`; affected review fixtures; review records; no network or external credentials.
- Exact steps: Inspect every affected formal-review skill and its invocation path; compare the reviewed artifact identity before and after the review pass; confirm review evidence is written; invoke or inspect the isolated-review fixture; confirm no automation run is created or advanced.
- Evidence artifact: The corresponding M4, M5, or M6 code-review record plus the active plan `Validation notes`.
- Pass condition: Every reviewed artifact is unchanged during its review pass, formal evidence is durable, and isolated review creates or advances no automation run.
- Failure condition: Any same-pass target edit, missing formal evidence, or isolated-review run creation/advancement.
- Required gate: M4, M5, and M6 code-review whenever those milestones change a formal-review surface.

### MP2. Verification and external-action containment

- Automation rationale: Fail-on-call doubles cover executable paths, while a reviewer must inspect the final composed skill and command surface for undeclared indirect PR, credential, network, or external mutation routes.
- Owner: M5/M6 milestone code reviewer; final verify rechecks the recorded proof.
- Owning stage: code-review, with verify recheck.
- Required environment: Local tracked worktree at M5 or M6 closeout; final workflow/verify skill text; executable automation modules; no credentials, network access, or external service setup.
- Exact steps: Trace success and failure exits from explain-change and verify; inspect imported/called command surfaces; confirm fail-on-call tests cover PR, push, publication, release, deployment, merge, destructive Git, credentials, network, and external mutation; confirm successful verify reports only `pr` as next.
- Evidence artifact: The M5/M6 code-review record, active plan `Validation notes`, and final verify evidence.
- Pass condition: No external action or credential path is reachable and verify success stops before PR invocation.
- Failure condition: Any direct or indirect external mutation, credential access, or automatic PR invocation is reachable.
- Required gate: M5 and M6 code-review, then final verify recheck.

### MP3. Sole state writer and generated-output ownership

- Automation rationale: Integration tests observe known callers, while final diff inspection is required to detect an unregistered direct YAML writer or hand-edited generated adapter surface outside the instrumented paths.
- Owner: M6 milestone code reviewer.
- Owning stage: code-review.
- Required environment: Local tracked final M6 diff; accepted architecture and ADR; canonical scripts; `dist/adapters/README.md`; `dist/adapters/manifest.yaml`; generated temporary adapter output; no publication or network access.
- Exact steps: Inspect every `workflow.automation` write call in the final diff; confirm each routes through `scripts/workflow_automation_state.py`; compare the final C4 ownership with the implementation; inspect tracked adapter changes; confirm generated adapter bodies are absent from authored diffs and CMD30 uses temporary output.
- Evidence artifact: The M6 code-review record, active plan `Validation notes`, and CMD30 temporary-output validation evidence.
- Pass condition: The state adapter is the only durable writer, C4 ownership matches, and generated adapter bodies were not hand-edited.
- Failure condition: Any direct writer bypass, ownership mismatch, or authored generated adapter body appears.
- Required gate: M6 code-review.

## Test cases

### T1. Unified mechanism and normative ownership are exclusive

- Covers: BRF-R001-BRF-R003d, BRF-AC001, AC-BRF-SR6-3
- Level: integration
- Command IDs: CMD3, CMD4, CMD25, CMD26
- Fixture/setup: Change records containing unified-only, legacy-only, lifecycle-continuation-only, duplicate active run, and forbidden new legacy-write shapes.
- Steps: Validate each record; invoke ordinary lifecycle continuation without an automation command; inspect written state.
- Expected result: New automation writes only one `bounded-review-fix` run under `workflow.automation`; duplicate active runs and new retired-profile writes fail; ordinary continuation writes no automation state.
- Failure proves: More than one writable mechanism or normative execution owner survives.
- Evidence artifact: Active plan validation notes.
- Automation location: `scripts/test-change-metadata-validator.py`, planned `scripts/test-workflow-automation.py`.
- Required by milestone: M1 and M6.

### T2. Closed durable vocabularies reject unknown values before consistency

- Covers: BRF-R008-BRF-R008j, BRF-R101, BRF-R102, BRF-AC024, AC-BRF-SR2-1 through AC-BRF-SR2-3, AC-BRF-SR2-6
- Level: unit
- Command IDs: CMD1-CMD4
- Fixture/setup: One valid and one unknown-value fixture for every closed enum, plus every legal and representative illegal state transition.
- Steps: Run structural validation before cross-field validation; attempt terminal resume and capability reuse.
- Expected result: Unknown values produce explicit vocabulary errors first; only legal transitions pass; only run status may pause; consumed capabilities and terminal runs cannot resume.
- Failure proves: Malformed durable state can bypass fail-closed validation.
- Evidence artifact: Active plan validation notes.
- Automation location: planned policy and validator test modules.
- Required by milestone: M1.

### T3. Immutable stage-policy registry is complete and spec-conformant

- Covers: BRF-R079, BRF-R080, BRF-R101, BRF-R102
- Level: unit
- Command IDs: CMD1, CMD2, CMD26
- Fixture/setup: Approved public/internal stage inventory and mutations removing a field, duplicating a stage, adding an unknown stage, widening mutation scope, or changing occurrence.
- Steps: Compare every frozen policy's sixteen fields to the approved contract projection.
- Expected result: Every automatable stage has exactly one complete immutable policy; drift fails before execution.
- Failure proves: Planning or implementation has invented a second policy contract.
- Evidence artifact: Active plan validation notes.
- Automation location: planned `scripts/test-workflow-automation-policy.py`.
- Required by milestone: M1.

### T4. Public targets use one compatible occurrence and completion predicate

- Covers: BRF-R009-BRF-R012, BRF-R017a, BRF-R017e, AC-BRF-SR1-1, AC-BRF-SR1-5
- Level: unit
- Command IDs: CMD1, CMD10
- Fixture/setup: Every public stage with its valid occurrence and every invalid stage/occurrence pairing.
- Steps: Resolve each target before persistence and inject invalid singleton, milestone, and final pairs.
- Expected result: Singleton, milestone, and final mappings match the closed matrix; invalid pairs fail before run or authorization persistence.
- Failure proves: Target semantics can be inferred or rebound inconsistently.
- Evidence artifact: Active plan validation notes.
- Automation location: planned policy and engine tests.
- Required by milestone: M1 and M3.

### T5. Repeated targets bind one current milestone and never rebind

- Covers: BRF-R013, BRF-R017b-BRF-R017f, BRF-AC002, BRF-AC017, AC-BRF-SR1-2 through AC-BRF-SR1-4, EC9, EC15-EC18
- Level: integration
- Command IDs: CMD10, CMD13, CMD14
- Fixture/setup: Plans with unique M2, no plan, missing milestone, terminal milestone, out-of-scope milestone, two plausible milestones, and a persisted `code-review@M2` after M3 becomes current.
- Steps: Request implement/code-review and resume the persisted target after plan advancement.
- Expected result: Valid requests persist milestone and plan identity; all ambiguous cases fail with the exact diagnostic; resume remains bound to M2.
- Failure proves: Repeated targets can drift across milestone occurrences.
- Evidence artifact: Active plan validation notes.
- Automation location: planned engine tests and lifecycle fixtures.
- Required by milestone: M3.

### T6. Canonical position hands off from evidence to the active plan

- Covers: BRF-R018-BRF-R023, BRF-AC003
- Level: integration
- Command IDs: CMD11, CMD13, CMD14
- Fixture/setup: Pre-plan artifacts/reviews with unique, stale, ambiguous, and contradictory positions; valid and invalid active plan summaries.
- Steps: Resolve pre-plan position, create and validate a plan, then introduce automation-observed identity drift.
- Expected result: Evidence owns pre-plan derivation, the valid plan summary owns live state immediately after handoff, no cursor is persisted, and ambiguity/drift pauses.
- Failure proves: Automation has become a competing workflow-state owner.
- Evidence artifact: Active plan validation notes.
- Automation location: planned engine tests and lifecycle state-sync fixtures.
- Required by milestone: M3.

### T7. Parent authorization is bounded consent and never executable authority

- Covers: BRF-R024-BRF-R031, BRF-AC004, BRF-AC005, BRF-AC009
- Level: unit
- Command IDs: CMD2, CMD12
- Fixture/setup: Complete authoring, implementation, and verification parents plus missing-field, revoked, cross-risk, external-action, and parent-only execution cases.
- Steps: Validate records, derive allowed/disallowed children, and attempt direct execution.
- Expected result: Parents record complete maximum scope, never execute, never imply another risk class, prohibit external actions, and propagate revocation/invalidation.
- Failure proves: A maximum consent envelope can be mistaken for executable authority.
- Evidence artifact: Active plan validation notes.
- Automation location: planned validator and engine tests.
- Required by milestone: M1 and M3.

### T8. Effective capabilities bind complete stage-relative bases and subset scope

- Covers: BRF-R032-BRF-R045, BRF-AC006-BRF-AC008, BRF-AC010, BRF-AC011, EC1-EC5
- Level: unit
- Command IDs: CMD2, CMD12
- Fixture/setup: Valid basis fixture per capability kind and variants with missing parent/review/input, stale identity, changed occurrence, expanded root/category/budget, and conflicting authority.
- Steps: Derive each capability and mutate one basis/scope dimension at a time.
- Expected result: Proposal review succeeds without a prior review identity; later capabilities require their reviews; invalid or expanded bases pause/fail and require a new capability rather than mutation.
- Failure proves: Executable authority is free-floating, circular, stale, or wider than consent.
- Evidence artifact: Active plan validation notes.
- Automation location: planned validator and engine tests.
- Required by milestone: M1 and M3.

### T9. Verify target never acts as future-contingent verification consent

- Covers: BRF-R014, BRF-R043a-BRF-R043e, BRF-AC020, AC-BRF-SR3-1 through AC-BRF-SR3-5, EC21
- Level: integration
- Command IDs: CMD12, CMD24
- Fixture/setup: Pre-implementation, partial-closeout, complete-closeout, and both-bases-valid repository states.
- Steps: Persist final verify target; request verification authority at each state; reach the boundary without authority.
- Expected result: Target persists early; authorization remains absent until every concrete basis exists; the run pauses with the exact reason and does not invoke explain-change or verify.
- Failure proves: Destination selection has become deferred blanket authority.
- Evidence artifact: Active plan validation notes.
- Automation location: planned engine tests.
- Required by milestone: M3 and M5.

### T10. Proposal-review occurrence, gate, and routing are exhaustive

- Covers: BRF-R047-BRF-R059, BRF-AC012-BRF-AC014, E1, E4, EC6-EC8
- Level: integration
- Command IDs: CMD15, CMD19
- Fixture/setup: Exact and later targets for approved, changes-requested, blocked, inconclusive, and unknown outcomes; unchanged-evidence rereview attempt.
- Steps: Invoke review against the exact proposal identity and inspect review result, gate, route, scope, and retry behavior.
- Expected result: All four known outcomes record occurrences; only approved satisfies the gate; exact target stops after occurrence; blocked/inconclusive pause; unknown fails; unchanged inconclusive does not spin.
- Failure proves: Review completion is being conflated with approval.
- Evidence artifact: Formal review fixtures and active plan validation notes.
- Automation location: planned engine tests and review validator tests.
- Required by milestone: M4.

### T11. Proposal correction is deterministic, bounded, and forces rereview

- Covers: BRF-R054, BRF-R062, BRF-R065, BRF-R066, BRF-AC019, E3
- Level: integration
- Command IDs: CMD16, CMD19
- Fixture/setup: Eligible accepted findings, owner-decision findings, exhausted budget, changed finding class, non-shrinking set, expanded scope, and stale evidence.
- Steps: Derive correction capability, apply eligible fixes, update proposal identity, and attempt downstream continuation on the old review.
- Expected result: Only driver-owned eligible corrections run; all guardrails pause; mutation preserves history, stales the gate, and requires a new review capability.
- Failure proves: Proposal correction can overreach or reuse stale approval.
- Evidence artifact: Review-resolution fixtures and active plan validation notes.
- Automation location: planned engine and review validator tests.
- Required by milestone: M4.

### T12. Reviews and direct skill invocations remain independent and isolated

- Covers: BRF-R060, BRF-R061, BRF-R078, BRF-R080, BRF-R087-BRF-R089, BRF-AC021, E8
- Level: integration
- Command IDs: CMD18-CMD20, CMD27
- Fixture/setup: Direct proposal-review/code-review requests, workflow-managed review requests, and bugfix invocation.
- Steps: Compare state and diffs before/after each invocation contract; inspect review evidence and public reachability.
- Expected result: Review is a distinct recorded pass that cannot edit its target; direct and bugfix requests do not create/advance a run; internal support stages are not public targets.
- Failure proves: Automation collapses reviewer independence or broadens isolated commands.
- Evidence artifact: MP1 and formal review fixtures.
- Automation location: skill/review tests and manual skill diff inspection.
- Required by milestone: M4 and M6.

### T13. Implementation correction remains reviewer-owned and convergent

- Covers: BRF-R063-BRF-R065, BRF-AC019
- Level: integration
- Command IDs: CMD22, CMD19
- Fixture/setup: Findings with eligible classes/recipes, missing class, new ID/class, non-shrinking set, exhausted budget, expanded scope, stale evidence, and missing validation.
- Steps: Evaluate each correction loop and compare unresolved sets across cycles.
- Expected result: Only reviewer-classified eligible recipes execute; missing class is none; every divergence condition pauses.
- Failure proves: The engine has invented a universal or driver-owned implementation repair policy.
- Evidence artifact: Review-resolution fixtures and active plan validation notes.
- Automation location: planned engine and review validator tests.
- Required by milestone: M5.

### T14. Every mutation is preceded by one capability-bound prepared receipt

- Covers: BRF-R068-BRF-R072, BRF-AC015
- Level: integration
- Command IDs: CMD6, CMD7, CMD12
- Fixture/setup: Instrumented state adapter and stage invoker with valid, parent-only, mismatched-capability, and concurrent-transition cases.
- Steps: Attempt a transition and capture write/invocation ordering; inspect the receipt authority chain.
- Expected result: Prepared receipt is durable before invocation, records every required field and `effective_capability_id`, and one in-flight transition is enforced.
- Failure proves: Mutation can start without recoverable write-ahead evidence or exact authority.
- Evidence artifact: State test event trace and active plan validation notes.
- Automation location: planned state and engine tests.
- Required by milestone: M2 and M3.

### T15. Interrupted transitions reconcile evidence before retry

- Covers: BRF-R073-BRF-R077, BRF-AC016, E6, EC10
- Level: integration
- Command IDs: CMD6, CMD7
- Fixture/setup: Prepared receipts with valid completion, absent completion under each retry policy, partial output, changed output identity, invalidated capability, completed/canonical mismatch, unknown state/version, and multiple in-flight receipts.
- Steps: Resume each fixture and record whether stage invocation occurs.
- Expected result: Valid completion reconciles without rerun; only idempotent retry may rerun absent evidence; all other unsafe states pause or fail closed exactly as specified.
- Failure proves: Resume can duplicate work, accept partial output, or silently rebind authority.
- Evidence artifact: Reconciliation test trace and active plan validation notes.
- Automation location: planned state and validator tests.
- Required by milestone: M2.

### T16. Cancellation reconciles first and settles one durable terminal result

- Covers: BRF-R007-BRF-R007c, AC-BRF-SR2-4, AC-BRF-SR2-5, E10, EC20
- Level: integration
- Command IDs: CMD6, CMD7, CMD25
- Fixture/setup: Active run with/without prepared transition, cancelled run, completed run, and no active run.
- Steps: Invoke off repeatedly and inspect run, parents, capabilities, receipts, and outputs.
- Expected result: Prepared work reconciles first; active run becomes cancelled; parents revoke and capabilities invalidate; evidence remains; repeated/no-active/completed results are idempotent and non-mutating.
- Failure proves: Cancellation can abandon unknown work or leave executable authority active.
- Evidence artifact: State fixtures and active plan validation notes.
- Automation location: planned state and engine tests.
- Required by milestone: M2 and M6.

### T17. Implementation and milestone review execute in plan order

- Covers: BRF-R081-BRF-R084, BRF-AC018, E5
- Level: integration
- Command IDs: CMD21, CMD23, CMD19
- Fixture/setup: Three-milestone plan with validation success/failure, approved/changes-requested review, open/closed resolution, and out-of-order attempts.
- Steps: Execute implement and code-review transitions across M1-M3.
- Expected result: Implement reaches review-requested only after validation and implies no approval; code-review closes only its bound milestone after approval/resolution; later milestones cannot start early.
- Failure proves: Milestones can skip validation, review, resolution, or plan order.
- Evidence artifact: Active-plan fixture history and validation notes.
- Automation location: planned engine, lifecycle, and review tests.
- Required by milestone: M5.

### T18. Final verification requires holistic closeout and stops before PR

- Covers: BRF-R067, BRF-R085, BRF-R086, BRF-R090, BRF-AC020, BRF-AC022, EC14
- Level: e2e
- Command IDs: CMD24, CMD25
- Fixture/setup: Closed milestones with missing/clean final review, stale/current explanation, verification success/failure, and an external-action trap.
- Steps: Attempt final verification at each gate and inspect resulting state and next action.
- Expected result: Missing evidence pauses; failure pauses without repair; success reports PR next but never invokes PR or another external action.
- Failure proves: Verify can bypass final review, repair implementation, or cross the external-action boundary.
- Evidence artifact: End-to-end trace, MP2, and active plan validation notes.
- Automation location: planned engine end-to-end tests.
- Required by milestone: M5 and M6.

### T19. Legacy state is dual-read, single-write, and migrates once

- Covers: BRF-R091-BRF-R098, BRF-AC023, E7, EC11, EC12
- Level: integration
- Command IDs: CMD8, CMD9, CMD25, CMD26
- Fixture/setup: Terminal and active records for each legacy mechanism, status-only read, first/repeated mutating resume, mixed writable state, and rollback mode.
- Steps: Read status, resume with/without explicit mutation authority, repeat resume, and activate rollback.
- Expected result: Reads are side-effect free; first authorized mutation writes one unified run/receipt and freezes legacy state; mixed writers fail; rollback preserves evidence and returns to explicit stages without retired writes.
- Failure proves: Migration rewrites history, duplicates runs, or preserves parallel writers.
- Evidence artifact: Migration fixtures and active plan validation notes.
- Automation location: planned state, engine, and validator tests.
- Required by milestone: M2 and M6.

### T20. Legacy command adapters preserve meaning without legacy writes

- Covers: BRF-R005, BRF-R098a-BRF-R098d, BRF-AC026, AC-BRF-SR4-1 through AC-BRF-SR4-6, E12, EC22, EC23
- Level: integration
- Command IDs: CMD8, CMD25, CMD26
- Fixture/setup: plan-review and verify aliases, status, off, unknown alias, and early/complete authority bases.
- Steps: Normalize each command, persist resulting state, and compare legacy records byte-for-byte.
- Expected result: Plan-review maps to singleton authoring only; verify maps to final target with only basis-valid authority; status reads; off uses unified migration/cancellation; unknown forms diagnose; no adapter writes legacy state.
- Failure proves: Compatibility preserves a retired engine or future-contingent authority.
- Evidence artifact: Adapter mapping fixtures and active plan validation notes.
- Automation location: planned engine and validator tests.
- Required by milestone: M6.

### T21. Cross-spec disposition registry is exact, closed, and contradiction-free

- Covers: BRF-R003a-BRF-R003c, BRF-R098e-BRF-R098i, AC-BRF-SR5-1 through AC-BRF-SR6-4, EC24-EC26
- Level: unit
- Command IDs: CMD2, CMD26
- Fixture/setup: Canonical ledger plus missing, duplicate, unknown, open-range, retired-exclusive-subject, superseded-current-citation, notice-drift, duplicate-source-selector, and absent-selector variants.
- Steps: Run selector uniqueness before disposition consistency and compare amendment notices/status settlement.
- Expected result: Every affected selector has exactly one disposition; duplicates fail first; absence implies nothing; review-fix is superseded and retained specs own only their explicit boundaries.
- Failure proves: Multiple specs can silently remain live automation authorities.
- Evidence artifact: Validator fixtures and active plan validation notes.
- Automation location: planned automation validator tests.
- Required by milestone: M6.

### T22. Status and run results are complete, tracked, and read-only

- Covers: BRF-R006, BRF-R099, BRF-R100, BRF-AC025
- Level: integration
- Command IDs: CMD9, CMD25
- Fixture/setup: Active, paused, prepared, completed, migrated, and review-outcome runs with tracked identities.
- Steps: Query status/result and compare state hashes before/after.
- Expected result: Output and public help distinguish target, current authority, canonical position, transition, gate, decision, artifact, stop reason, and next action; unknown and ambiguous diagnostics identify the exact rejected field or repeated-stage binding problem; status writes nothing; resume uses tracked evidence only.
- Failure proves: Operators need hidden chat state or status mutates the run.
- Evidence artifact: Query snapshots with behavioral field assertions and active plan validation notes.
- Automation location: change-record query and planned engine tests.
- Required by milestone: M2 and M6.

### T23. The state adapter is the sole atomic automation-state writer

- Covers: Architecture write boundary; BRF-R002, BRF-R068, BRF-R100
- Level: integration
- Command IDs: CMD6, CMD26
- Fixture/setup: Change files with unrelated fields, simulated write interruption, concurrent identity drift, and instrumented callers.
- Steps: Apply complete-file updates, interrupt before replace, change input identity, and scan executable callers for direct automation-state writes.
- Expected result: Unrelated valid metadata survives; interrupted temp writes do not truncate canonical YAML; drift blocks replacement; only the state adapter mutates the subsection.
- Failure proves: The architecture's recoverable single-write boundary is not real.
- Evidence artifact: State test trace and MP3.
- Automation location: planned state tests and architecture conformance inspection.
- Required by milestone: M2 and M6.

### T24. M1-M5 integration remains unreachable from public commands

- Covers: Plan public activation boundary; BRF-R080, BRF-R087, BRF-R098a
- Level: integration
- Command IDs: CMD18, CMD20
- Fixture/setup: Repository state at each pre-cutover milestone and every current/legacy public command.
- Steps: Attempt to route public commands into each non-public harness.
- Expected result: Internal tests can exercise the engine, but public skills and aliases retain prior behavior until M6.
- Failure proves: A partially implemented mechanism is publicly reachable.
- Evidence artifact: Non-public routing tests and active plan validation notes.
- Automation location: planned engine tests and skill validator tests.
- Required by milestone: M4 and M5.

### T25. M6 activates unified routing and disables legacy writers atomically

- Covers: BRF-R001-BRF-R005, BRF-R091, BRF-R098a, BRF-AC001, BRF-AC026
- Level: smoke
- Command IDs: CMD25-CMD32
- Fixture/setup: Final canonical skills, schemas, scripts, legacy records, adapter manifest, and generated temporary adapter output.
- Steps: Run full engine/validator suites, inspect all public command routes, generate/validate adapters, run selected CI and broad smoke.
- Expected result: Every public route uses unified writes, every legacy writer is disabled in the same slice, generated guidance is current, and no partial-activation state exists.
- Failure proves: Cutover can expose split-brain automation behavior.
- Evidence artifact: M6 validation notes and temporary adapter validation output.
- Automation location: full repository validation and adapter suites.
- Required by milestone: M6.

### T26. Conditional architecture routing is deterministic

- Covers: BRF-R016, BRF-R017, EC13
- Level: integration
- Command IDs: CMD17, CMD25
- Fixture/setup: Architecture-required, not-required, and ambiguous assessments with explicit architecture, explicit architecture-review, and later targets.
- Steps: Resolve each route and inspect receipt/result.
- Expected result: Later target records not-applicable and continues; explicit conditional target stops target-not-applicable; ambiguity pauses for owner decision.
- Failure proves: Conditional stages can be silently skipped or invented.
- Evidence artifact: Authoring route fixtures and active plan validation notes.
- Automation location: planned engine tests.
- Required by milestone: M4 and M6.

### T27. Security and privacy boundaries exclude external authority and secrets

- Covers: BRF-R029, BRF-R090, BRF-AC022
- Level: manual
- Command IDs: CMD20, CMD27, CMD32
- Fixture/setup: Final diff, skill contracts, state schema, result formatting, and test doubles that fail on external calls.
- Steps: Inspect state fields and command surfaces; run validators; confirm no credential fields, raw environment output, network/publication path, destructive Git, or external mutation is reachable.
- Expected result: External actions remain prohibited and persisted/reporting evidence contains no secrets or machine-local data.
- Failure proves: The workflow mechanism crosses its approved security boundary.
- Evidence artifact: MP2 and final validation notes.
- Automation location: manual diff inspection plus repository validators.
- Required by milestone: M6 and final verify.

### T28. Full workflow traverses proposal review through verify with bounded pauses

- Covers: BRF-AC001-BRF-AC026, E1-E12
- Level: e2e
- Command IDs: CMD25, CMD26, CMD32
- Fixture/setup: Temporary repository with approved artifacts, two implementation milestones, review outcomes, correction budgets, interrupted receipt, legacy input, separate risk authorizations, and external-action trap.
- Steps: Run clean, correction, interruption, cancellation, migration, missing-authority, and final-success scenarios.
- Expected result: The engine advances only with current effective capabilities, preserves stage evidence and plan ownership, reconciles safely, and stops after fresh verify with PR merely reported as next.
- Failure proves: The component contracts do not compose into the single bounded mechanism.
- Evidence artifact: M6 end-to-end trace and broad-smoke evidence.
- Automation location: planned full engine suite in a temporary repository.
- Required by milestone: M6.

### T29. State, receipt, and migration proof is deterministic and order-independent

- Covers: BRF-R068-BRF-R077, BRF-R094, BRF-AC015, BRF-AC016, E6
- Level: integration
- Command IDs: CMD6, CMD7, CMD8
- Fixture/setup: Fixed-clock state, receipt, and migration fixtures using explicit IDs/keys, sanitized environment, fresh temporary roots, and two declared execution orders.
- Steps: Run the M2 transactional and migration subset twice with identical inputs; rerun it in reverse declared order; compare normalized receipts, transition keys, migration records, canonical files, and teardown results.
- Expected result: Both identical runs and the reordered run produce the same normalized state evidence and outcomes and leave no shared state or temporary roots.
- Failure proves: Time, randomness, environment, fixture order, or leaked process state can change workflow evidence or behavior.
- Evidence artifact: Determinism comparison output and active plan validation notes.
- Automation location: Planned state, receipt-validator, and migration-validator suites using the deterministic fixture contract.
- Required by milestone: M2.

### T30. Composed automation proof is deterministic and order-independent

- Covers: BRF-R068-BRF-R077, BRF-R094, BRF-R100, BRF-AC015, BRF-AC016, E6
- Level: e2e
- Command IDs: CMD25
- Fixture/setup: Fixed-clock full-engine, status, receipt-resume, and legacy-migration fixtures using explicit IDs/keys, a sanitized environment, fresh temporary repositories, two declared execution orders, and external-action traps.
- Steps: Run the composed transaction, interruption, migration, status, and final-success scenarios twice with identical inputs; rerun them in reverse declared order; compare normalized receipts, transition keys, migration records, status output, canonical files, teardown results, and external-action trap counts.
- Expected result: Identical and reordered composed runs produce the same normalized evidence and outcomes, leave no shared state or temporary roots, and make no external call.
- Failure proves: Engine composition introduces time, randomness, environment, order, or process-state dependence that focused M2 proof cannot detect.
- Evidence artifact: Full-engine determinism comparison output and active plan validation notes.
- Automation location: Planned full engine suite using the deterministic fixture contract.
- Required by milestone: M6.

## Fixtures and data

- Add focused fixtures under `tests/fixtures/workflow-automation/` grouped as `policy/`, `state/`, `targets/`, `reviews/`, `plans/`, `migration/`, and `integration/`.
- Reuse existing artifact-lifecycle, review-artifact, change-metadata, skill, and adapter fixture builders instead of copying their parsers or review semantics.
- Store minimal synthetic tracked artifacts with stable IDs and relative paths; do not store machine-local paths, branch names, credentials, tokens, or raw environment values.
- Use temporary repository copies for mutation, interruption, cancellation, and end-to-end cases.
- Represent output completion with stage-native evidence, not path existence alone.
- Keep the exact affected-selector registry and expected stage-policy projection in test code derived from the approved spec; do not add another editable YAML/JSON policy file.

### Deterministic fixture contract

- Clock: Use an injected fake UTC clock beginning at `2026-07-21T00:00:00Z`; tests explicitly advance it when ordering matters and never read the host wall clock.
- IDs and keys: Supply run, authorization, capability, transition, review, milestone, and migration IDs explicitly. Compute transition keys only from normalized fixture inputs; random UUID generation is prohibited in proof fixtures.
- Environment: Run with `TZ=UTC`, `LC_ALL=C`, and an explicit allowlist containing only variables required by the Python process and temporary repository. Remove workflow, CI, credential, proxy, and user-specific variables.
- Randomness: Do not use randomness unless a case directly tests it. Any unavoidable randomized helper uses a recorded fixed seed and emits that seed on failure.
- Filesystem: Allocate a fresh temporary root per case, avoid shared mutable fixture files, reject symlink escape, and assert teardown removes temporary output and leaves source fixtures byte-identical.
- Process isolation: Reset injected clocks, ID providers, caches, registries, environment overrides, and fail-on-call counters after every case.
- Order proof: T29 runs the M2 state/receipt/migration subset twice with identical inputs and once in reverse declared order. T30 independently repeats and reverses the M6 composed-engine scenarios. Normalized evidence and outcomes must match at each boundary.

## Mocking/stubbing policy

- Stub only process boundaries needed to observe stage invocation order and to prohibit external actions.
- Use real state serialization, schema validation, lifecycle parsing, review validation, plan synchronization, and temporary filesystem replacement behavior.
- Do not mock completion evidence when an existing stage-owned validator can produce it.
- Formal review fixtures may provide predetermined review records, but the engine must consume them through the real review-evidence parser.
- Inject clock and ID providers at test seams; do not globally monkeypatch host time or process-wide randomness when a component-local dependency can be supplied.
- External PR, network, credential, publication, deployment, merge, and destructive Git functions must be replaced by fail-on-call test doubles; no live external system is contacted.

## Migration or compatibility tests

- T19 proves terminal legacy reads, read-only status projection, first mutating migration, migration idempotency, mixed-writer rejection, audit-based removal precondition, and rollback without retired writers.
- T20 proves every supported legacy command mapping and forbids future-contingent verification authority.
- T21 proves exact cross-spec precedence and approval settlement.
- T25 proves canonical and generated public adapters expose the same unified semantics at atomic cutover.
- Compatibility aliases remain mandatory; removal behavior is intentionally excluded until a separate approved change exists.

## Observability verification

- T14 and T15 assert transition IDs, deterministic keys, bound capability IDs, input/output identities, canonical-sync status, and reconciliation result.
- T16 asserts cancellation reason and authority invalidation while preserving prior evidence.
- T22 asserts the complete status/result field contract and read-only behavior.
- T28 records stage outcomes, review/gate state, fixes, decisions, artifacts, stop reason, and next action for each end-to-end scenario.

## Security/privacy verification

- T7 and T27 prove `external_actions: prohibited` is not a grantable class.
- T18 and T28 use fail-on-call traps for PR, push, publication, release, deploy, merge, destructive Git, credentials, network, and external mutation.
- Fixtures and outputs are scanned through existing repository validators for secrets, absolute machine-local paths, and raw environment details.
- Status and receipts expose stable artifact identities and bounded reasons, not artifact contents or credentials.

## Performance checks

- No throughput or latency benchmark is required because the mechanism is synchronous, change-local, and not a service or background worker.
- M2 state tests must prove one complete-file replacement per logical update and no unbounded retry loop.
- T10 proves unchanged inconclusive evidence does not spin; T15 proves retry behavior is policy-bounded.
- CMD32 remains required because the active plan explicitly sets `broad_smoke_required: true` for the final cutover.

## Manual QA checklist

- Execute MP1 exactly at every applicable M4-M6 code-review gate and record its evidence artifact.
- Execute MP2 at M5/M6 code-review and recheck its recorded evidence during final verify.
- Execute MP3 at M6 code-review after the complete public-cutover diff and CMD30 evidence exist.
- T22 owns automated public help/status distinction and exact unknown/ambiguous diagnostic assertions; no separate untracked manual check remains.

## What not to test and why

- Do not test alias removal; the approved contract requires aliases throughout this migration window and removal needs a separate approved compatibility change.
- Do not test background, asynchronous, hosted, or cross-repository scheduling; the accepted architecture defines an in-interaction repository component only.
- Do not test automatic PR, push, publication, release, deployment, merge, destructive Git, credentials, or external mutation except to prove they are unreachable.
- Do not test a second YAML/JSON policy registry or separate automation state file because both are prohibited.
- Do not use snapshot-only assertions for behavioral contracts; field-level and transition assertions are required.
- Do not claim hosted CI passed from local commands; hosted evidence belongs to later verify/PR stages if observed.

## Uncovered gaps

None blocking.

The exact internal Python class/function decomposition and fixture serialization may be selected during implementation, but they must preserve the approved module ownership, closed contracts, stage-native evidence, stable IDs, and command surfaces recorded here.

## Next artifacts

- Formal `test-spec-review` R4 of this revised active proof map.
- M1 implementation only after test-spec-review approves this artifact with no unresolved material findings.
- Independent `code-review` after each of M1-M6.
- Final holistic review, `explain-change`, fresh `verify`, and PR handoff only after every milestone is closed.

## Follow-on artifacts

- [Test-spec-review R1](../docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r1.md) requested `BRF-TSR1` through `BRF-TSR3`; this revision incorporates all three findings pending rereview.
- [Test-spec-review R2](../docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r2.md) confirmed the R1 findings resolved and requested explicit milestone-local activation through `BRF-TSR4`; this revision incorporates that finding pending R3.
- [Test-spec-review R3](../docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/test-spec-review-r3.md) confirmed the split determinism proof and kept `BRF-TSR4` open for the missing T26 M4/M6 activation; this revision incorporates that final mapping pending R4.

## Readiness

This test specification is active and ready for `test-spec-review` R4.
It does not authorize implementation.
M1 remains blocked until a clean formal test-spec-review is recorded and lifecycle state is synchronized.
