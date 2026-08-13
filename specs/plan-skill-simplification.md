# Plan Skill Simplification Specification

## Owning change record

`docs/changes/2026-08-12-plan-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-12-plan-skill-simplification.md`

## Goal and context

This specification defines a shorter published `plan` skill package while preserving plan quality and correcting live milestone-state ownership. It also amends the stage-owned lifecycle contract so clean plan-review evidence precedes one-time plan-owned `planned_work` initialization and the same review then retries settlement without repeating judgment.

## Glossary

- `portable planning`: plan authoring without a governed RigorLoop change record.
- `stable artifact identity`: artifact ID, kind `plan`, role `primary`, and normalized plan path.
- `reviewed revision identity`: review ID, round, review record path, reviewed artifact path, and reviewed repository revision or commit.
- `initialization-required`: clean current plan-review evidence exists for a `review-required` plan, but initial `planned_work` is absent.
- `settlement-retry-required`: matching initial `planned_work` exists for a clean-reviewed `review-required` plan, but the review settlement has not moved the plan to `active`.

## Examples first

### Example E1: portable planning loads only the common procedure

Given no valid governed change context and no boundary-first trigger, when `plan` authors a plan, then it loads `SKILL.md`, copies applicable structural assets, writes no `change.yaml`, and makes no governed lifecycle claim.

### Example E2: a new governed plan reaches review without live work state

Given an exact governed change with plan-authoring authority and no primary plan, when `plan` creates the canonical plan, then it registers the stable artifact identity, moves only that plan entry through authoring to `review-required`, and leaves `planned_work` absent.

### Example E3: clean review requests initialization before settlement

Given a `review-required` primary plan without `planned_work`, when `plan-review` records a clean review for the exact current revision, then the plan remains `review-required`, the result reports `initialization-required`, and workflow does not route to implementation.

### Example E4: workflow completes the two-phase transaction

Given current clean review evidence and no open resolution, when workflow invokes `initialize-approved-plan`, then `plan` creates only missing initial `planned_work`; workflow invokes the identical plan-review settlement retry; plan-review reuses the recorded judgment and moves only the plan entry to `active`.

### Example E5: stale review cannot initialize live work

Given the plan changed after the recorded clean review, when initialization is attempted, then initialization stops, `planned_work` remains absent, the plan remains `review-required`, and downstream routing stays blocked.

### Example E6: historical plan state is not current authority

Given an active old-format plan contains `Milestone state` but its governed change has complete `planned_work`, when current state is read, then stable intent comes from the plan and all current milestone state comes from `change.yaml`.

## Requirements

### Package and resource ownership

PSIM-R001. The published `plan` package MUST contain one universal `SKILL.md`, `references/governed-plan-authoring.md`, the existing `references/boundary-first-method-v1.md`, and exactly the existing three structural assets.

PSIM-R002. `SKILL.md` MUST remain sufficient for portable plan classification, upstream readiness, plan quality, traceability, milestone decomposition, validation, recovery, universal stops, claims, resource triggers, and handoff.

PSIM-R003. The governed reference MUST own only governed change inspection, the three closed plan operations, stable artifact registration, authoring transitions, one-time initialization, and their retry and failure procedure. Loading it MUST NOT grant authority.

PSIM-R004. The boundary reference MUST retain its existing checked activation contract. Missing or unreadable triggered procedure MUST stop dependent work without reconstruction from memory.

PSIM-R005. Assets MUST own labels and structure only. They MUST NOT define state, authority, settlement, status, or routing policy.

### Invocation and authority

PSIM-R006. Governed planning MUST classify exactly one operation: `create-primary-plan`, `revise-primary-plan`, or `initialize-approved-plan`.

PSIM-R007. `create-primary-plan` MUST require one governed change, settled prerequisites, plan-authoring authority, a deterministic intended normalized path, and absence of a conflicting plan file or entry; it MUST NOT require a pre-existing plan identity.

PSIM-R008. `revise-primary-plan` MUST require exactly one current matching stable artifact identity and canonical plan file. File-entry asymmetry, multiple primary candidates, or identity mismatch MUST stop before mutation.

PSIM-R009. `initialize-approved-plan` MUST require the exact current stable artifact identity, current clean plan-review evidence for the reviewed revision, no later edit or contradictory review, no open plan-review resolution, valid stable milestone definitions, and absent `planned_work`.

PSIM-R010. Manual and workflow-managed execution MUST use the same plan-owned write boundary. Only workflow-managed authority may coordinate downstream calls and routing.

### Identity and settlement transaction

PSIM-R011. Stable artifact identity MUST be the tuple of artifact ID, kind, role, and normalized path. The change MUST NOT add a governed-document hash or `content_identity` field.

PSIM-R012. Reviewed revision identity MUST use the durable review ID, round, review record path, reviewed artifact path, and reviewed repository revision or commit.

PSIM-R013. Clean plan-review MUST record durable evidence before initialization and MUST leave the plan `review-required` while `planned_work` is absent.

PSIM-R014. A clean review with missing `planned_work` MUST report `initialization-required`. An isolated review MUST stop after reporting it; workflow-managed execution MAY coordinate initialization.

PSIM-R015. Initialization MUST derive the complete initial `planned_work` exactly once from the exact reviewed ordered milestone definitions and MUST write no other artifact or workflow field.

PSIM-R016. Repeating initialization with the identical artifact and review basis MUST be an idempotent no-op. Existing mismatched `planned_work` MUST stop and MUST NOT be replaced, repaired, or updated by `plan`.

PSIM-R017. After matching initialization, workflow MUST coordinate an identical plan-review settlement retry. Plan-review MUST reuse the recorded judgment and MUST NOT rerun semantic review.

PSIM-R018. Only the settlement retry MAY move the exact plan entry from `review-required` to `active`. Workflow MUST NOT route beyond plan-review until initialization and settlement both succeed.

PSIM-R019. Legal current-state combinations MUST be exactly those below:

| Plan state | Current clean review | `planned_work` | Result |
| --- | ---: | ---: | --- |
| `authoring`, `revision-required`, or `blocked` | no | absent | no live execution state |
| `review-required` | no | absent | review pending |
| `review-required` | yes | absent | initialization required |
| `review-required` | yes | matching | settlement retry required |
| `active` | yes and settled | matching | downstream routing permitted |

PSIM-R020. Every other combination MUST fail closed. Initialization failure MUST preserve clean review evidence, leave the plan `review-required`, record the blocker in stage-owned evidence, and prohibit downstream routing.

### Plan content and live state

PSIM-R021. New or substantively revised plan bodies MUST contain stable execution intent and MUST NOT contain mutable milestone state, command outcomes, validation progress, blockers, review status, or closeout progress.

PSIM-R022. The milestone asset MUST retain milestone ID and kind, goal, requirement and architecture links, affected components, dependencies, tests and proof, implementation steps, validation commands, expected result, completion criteria, required evidence, review handoff, risks, rollback or recovery, and optional commit boundary.

PSIM-R023. For governed `stage-owned-change-local-v1` changes, `change.yaml#workflow_state.planned_work` MUST be the sole current milestone-state authority. Historical embedded plan state MUST never override or repair it.

PSIM-R024. A plan baseline becomes settled only after matching initialization and review settlement. Later changes to milestone ID, order, kind, completion criteria, or required evidence MUST route to an explicitly governed replan or migration and MUST NOT mutate existing `planned_work` through ordinary plan authoring.

### Compatibility and migration

PSIM-R025. Migration MUST be read-old/write-new: readers MAY accept compatible historical plan structures, but writers MUST emit only the stable-intent structure.

PSIM-R026. Historical terminal plans MUST remain unchanged. Portable plans MUST remain readable documentation without implying governed state.

PSIM-R027. An active old-format governed plan with complete matching `planned_work` MUST use plan content only for stable intent and `change.yaml` for current state. Missing or conflicting authoritative state MUST block and route to explicit workflow-owned migration.

PSIM-R028. No reverse synchronization or compatibility adapter MAY recreate mutable state in plan bodies or infer current `planned_work` from historical plan prose.

### Simplification and proof

PSIM-R029. Every behaviorally significant existing rule MUST have exactly one disposition and destination, and every literal dependency MUST be separately classified as normative, parser/package, incidental test, obsolete, or historical fixture.

PSIM-R030. Acceptance MUST measure canonical LF-normalized UTF-8 bytes and Unicode whitespace-separated words for `PL0`, `PL0B`, `PL1`, and `PL1B`, count each loaded procedure once, and report assets and total package size separately.

PSIM-R031. Both `PL0` and `PL1` procedural words and bytes MUST decrease from baseline, every duplicate cluster MUST have one loaded owner, and boundary variants MUST have no unexplained growth. No fixed percentage may override semantic preservation.

PSIM-R032. Acceptance MUST use deterministic structural, static contract, migration, package-parity, and independent semantic-review proof. It MUST NOT execute a target-agent runtime or introduce a permanent simplicity, tokenizer, transcript, or prose-quality validator.

PSIM-R033. Canonical, generated, archived, and clean-installed packages MUST preserve all mapped resources and required byte parity. Mixed versions MUST fail closed.

### Architecture ownership

PSIM-R034. This change MUST update canonical architecture and add a narrow successor ADR defining the evidence-initialization-settlement transaction, legal temporary states, identity, recovery, and ownership.

PSIM-R035. The owning `change.yaml` MUST own mutable architecture-assessment status and artifact pointers; architecture artifacts MUST own stable design rationale.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: PSIM-R001, PSIM-R002, PSIM-R003, PSIM-R004, PSIM-R005, PSIM-R006, PSIM-R007, PSIM-R008, PSIM-R009, PSIM-R010, PSIM-R011, PSIM-R012, PSIM-R013, PSIM-R014, PSIM-R015, PSIM-R016, PSIM-R017, PSIM-R018, PSIM-R019, PSIM-R020, PSIM-R021, PSIM-R022, PSIM-R023, PSIM-R024, PSIM-R025, PSIM-R026, PSIM-R027, PSIM-R028, PSIM-R029, PSIM-R030, PSIM-R031, PSIM-R032, PSIM-R033, PSIM-R034, PSIM-R035

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | PSIM-R006, PSIM-R007, PSIM-R008, PSIM-R009 | BND-INPUT-001 | - |
| state-lifecycle | applicable | PSIM-R013, PSIM-R014, PSIM-R015, PSIM-R017, PSIM-R018, PSIM-R019, PSIM-R020 | BND-STATE-001 | - |
| identity-authority | applicable | PSIM-R003, PSIM-R006, PSIM-R009, PSIM-R010, PSIM-R011, PSIM-R012 | BND-AUTH-001 | - |
| composition-path | applicable | PSIM-R001, PSIM-R002, PSIM-R003, PSIM-R004, PSIM-R005 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | PSIM-R013, PSIM-R015, PSIM-R016, PSIM-R017, PSIM-R018 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | PSIM-R004, PSIM-R008, PSIM-R009, PSIM-R016, PSIM-R020, PSIM-R027 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | PSIM-R021, PSIM-R023, PSIM-R024, PSIM-R025, PSIM-R026, PSIM-R027, PSIM-R028 | BND-COMPAT-001 | - |
| external-environment | not-applicable | - | - | The contract adds no network, service, platform, credential, deployment, or external-system behavior. |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | PSIM-R006, PSIM-R007, PSIM-R008, PSIM-R009 | create; revise; initialize; unknown; ambiguous | Exactly one legal operation is selected from authoritative evidence. | Valid operation proceeds; unknown, conflicting, or ambiguous input stops. | PSIM-R006 |
| BND-STATE-001 | state-lifecycle | PSIM-R013, PSIM-R014, PSIM-R015, PSIM-R017, PSIM-R018, PSIM-R019, PSIM-R020 | authoring; review pending; initialization required; settlement retry required; active | Only enumerated plan/review/planned-work combinations are legal. | Legal transitions proceed in order; every other combination fails closed. | PSIM-R019 |
| BND-AUTH-001 | identity-authority | PSIM-R003, PSIM-R006, PSIM-R009, PSIM-R010, PSIM-R011, PSIM-R012 | stable artifact; reviewed revision; plan owner; review owner; workflow coordinator | Loading never grants authority and identity uses no document hash. | Current matching authority permits its bounded write; stale or mismatched authority stops. | PSIM-R011 |
| BND-COMPOSE-001 | composition-path | PSIM-R001, PSIM-R002, PSIM-R003, PSIM-R004, PSIM-R005 | portable; governed; boundary-triggered; structural output | Each rule and structure has one owner and triggered resources load once. | Correct assembly proceeds; missing or contradictory package resources stop dependent work. | PSIM-R001 |
| BND-TEMPORAL-001 | temporal-retry | PSIM-R013, PSIM-R015, PSIM-R016, PSIM-R017, PSIM-R018 | evidence; initialize; retry settlement; duplicate retry; interruption | Evidence precedes initialization and settlement follows initialization. | Identical retry reconciles; reordering, drift, or conflict stops. | PSIM-R017 |
| BND-RECOVERY-001 | failure-recovery | PSIM-R004, PSIM-R008, PSIM-R009, PSIM-R016, PSIM-R020, PSIM-R027 | missing resource; stale review; partial initialization; conflicting state; active legacy gap | Failure preserves authoritative evidence and never invents or repairs another owner's state. | Stop with blocker; explicit owner retry or migration resumes safely. | PSIM-R020 |
| BND-COMPAT-001 | compatibility-migration | PSIM-R021, PSIM-R023, PSIM-R024, PSIM-R025, PSIM-R026, PSIM-R027, PSIM-R028 | new format; historical terminal; active old complete; active old incomplete; rollback | Writers emit stable intent only and current state has one owner. | Compatible old data reads; incomplete or conflicting live state blocks migration. | PSIM-R025 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | PSIM-R009, PSIM-R013, PSIM-R015, PSIM-R017, PSIM-R020 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | Review evidence becomes stale between judgment and initialization. | Initialization stops before write and settlement remains incomplete. |
| INT-002 | PSIM-R004, PSIM-R003, PSIM-R020 | BND-COMPOSE-001, BND-RECOVERY-001 | A required governed procedure is missing during a state-changing call. | The call stops without reconstructing procedure or partially mutating state. |
| INT-003 | PSIM-R023, PSIM-R025, PSIM-R027, PSIM-R028 | BND-STATE-001, BND-COMPAT-001, BND-RECOVERY-001 | Historical plan state conflicts with live change-local state. | `change.yaml` remains authoritative; incomplete or conflicting live state routes to explicit migration. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | PSIM-R001, PSIM-R002, PSIM-R010 | BND-COMPOSE-001 | - | - |
| E2 | illustration | PSIM-R007, PSIM-R011, PSIM-R013 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001 | - | - |
| E3 | illustration | PSIM-R013, PSIM-R014, PSIM-R019 | BND-STATE-001, BND-TEMPORAL-001 | - | - |
| E4 | illustration | PSIM-R015, PSIM-R017, PSIM-R018 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | - | - |
| E5 | illustration | PSIM-R009, PSIM-R020 | BND-AUTH-001, BND-RECOVERY-001 | - | - |
| E6 | illustration | PSIM-R023, PSIM-R025, PSIM-R027 | BND-COMPAT-001 | - | - |

## Inputs and outputs

Inputs are the accepted proposal, current skill package, exact governed change and review evidence when applicable, current lifecycle spec and architecture, historical/current plan fixtures, parsers, validators, and package resources. Outputs are the revised published skill package, amended lifecycle contracts, architecture and ADR artifacts, migrated consumers, deterministic proof, and change-local preservation and measurement evidence.

## State and invariants

`change.yaml` remains the sole mutable lifecycle and milestone-state owner. Plan owns only initial derivation, plan-review owns judgment and settlement, and workflow owns coordination, routing, and every later transition. Clean evidence is not settlement; initialized state is not active until settlement retry succeeds.

## Error and boundary behavior

Unknown operations, invalid state combinations, stale identities, missing resources, conflicting package versions, failed writes, and ambiguous migration cases fail closed before dependent claims. A failed initialization preserves review evidence and reports an actionable blocker without routing onward.

## Compatibility and migration

The migration is prospective and read-old/write-new. New writers remove mutable plan state; readers retain compatible historical support. Active legacy changes require complete authoritative `planned_work` or explicit workflow-owned migration. Rollback is atomic across contracts, architecture, canonical package, validators, parsers, fixtures, and generated packages.

## Observability

Review records, authoring evidence, `change.yaml`, workflow automation evidence, migration fixtures, rule/literal ledgers, profile measurements, and validation commands provide durable observability. No new telemetry service is introduced.

## Security and privacy

No new secrets, credentials, network calls, personal data, or external mutation are introduced. Existing filesystem, destructive-action, and external-action boundaries remain unchanged.

## Accessibility and UX

No visual interface is changed. User-facing Markdown must remain concise, structurally navigable, and keep complete sentences intact in source.

## Performance expectations

Portable and governed procedural words and UTF-8 bytes must decrease. Validation runtime has no new normative limit, and no target-agent runtime enters acceptance.

## Edge cases

EC1. A plan file without an entry, an entry without a file, or multiple primary candidates stops creation or revision.

EC2. Clean review evidence exists but the plan changed before initialization; initialization stops as stale.

EC3. Initialization succeeds and settlement is interrupted; an identical retry settles without reviewing again.

EC4. `planned_work` already matches the same reviewed basis; initialization is a no-op and settlement may retry.

EC5. Existing `planned_work` differs from the reviewed plan; plan never replaces it and workflow routes to replan or migration.

EC6. A triggered reference is unreadable; portable unrelated work may continue only when that trigger is false.

EC7. A historical terminal plan contains old state fields; it remains unchanged and readable as history.

EC8. An active old plan has no complete `planned_work`; current state is not inferred from prose.

## Non-goals

- No generic planning engine, scheduler, state store, new public skill, fourth asset, target-agent journey, or permanent simplicity validator.
- No automatic mutation of existing `planned_work`, automatic replan, PR action, release action, or external system action.
- No optimization of adjacent skills beyond directly required contract and consumer alignment.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-PSIM-001 | All three operations and every legal/illegal state combination have deterministic fixtures. |
| AC-PSIM-002 | Stable and reviewed identities are proven without a content hash. |
| AC-PSIM-003 | Clean evidence, initialization, and settlement retry preserve owner boundaries and block early routing. |
| AC-PSIM-004 | New plan output contains stable intent and no mutable progress or state fields. |
| AC-PSIM-005 | Read-old/write-new fixtures cover historical, active complete, active incomplete, conflict, and rollback cases. |
| AC-PSIM-006 | Rule and literal inventories account for every significant behavior and compatibility dependency. |
| AC-PSIM-007 | Both portable and governed loaded profiles decrease, with assets and total package reported separately. |
| AC-PSIM-008 | Architecture and successor ADR are approved before planning. |
| AC-PSIM-009 | Existing validation families prove canonical, generated, archived, and installed package parity. |
| AC-PSIM-010 | No target-agent runtime or permanent simplicity validator is used for acceptance. |

## Open questions

None.

## Next artifacts

- Independent `spec-review`.
- Canonical architecture update, successor ADR, and `architecture-review` because architecture is required.
- Execution plan and `plan-review`.
- Test specification and `test-spec-review`.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This specification does not claim architecture, planning, implementation, verification, or PR readiness.
