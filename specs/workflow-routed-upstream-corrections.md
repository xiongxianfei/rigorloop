<!-- Template: spec-skeleton-v1; Skill: spec; Template status: normative -->

# Workflow-Routed Upstream Corrections

## Owning change record

`docs/changes/2026-08-25-workflow-routed-upstream-corrections/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-25-workflow-routed-upstream-corrections.md`

## Goal and context

RigorLoop must provide a governed path from a downstream-discovered defect to revision and rereview of an already settled upstream artifact. Workflow remains the semantic route owner. The lifecycle CLI validates and atomically records the supplied route, admits only the exact destination owner's revision, preserves downstream state, and validates the return.

The same release prevents cross-change artifact-path collisions and supplies a narrow recovery operation for an existing duplicate architecture or ADR registration. Direct lifecycle editing, generic reopening, and arbitrary removal remain unsupported.

## Glossary

| Term | Meaning |
| --- | --- |
| Correction route | Durable workflow-owned coordination that suspends one downstream position while one exact upstream artifact is revised and rereviewed. |
| Source snapshot | The current stage, next stage, lifecycle state, blocker, milestone identity and state, and finding IDs preserved when a correction route starts. |
| Destination artifact | The exact settled proposal, spec, architecture, plan, test spec, or ADR selected by workflow for correction. |
| Return | Restoration of the preserved source snapshot after the destination revision has a current approving review. |
| Canonical owner | The one governed change identified by the artifact's own owning-change pointer and exact normalized artifact entry. |
| Duplicate registration | An artifact entry in a different change for the canonical owner's normalized path. |

## Examples first

Example E1: proof gap routes to test-spec without closing code-review findings
Given M1 is in review resolution with an open code-review finding that identifies a proof-contract gap
When workflow requests a correction route to the settled primary test spec
Then the CLI records the preserved M1 state, routes to test-spec, keeps the finding open, and makes revision available only for that test spec.

Example E2: unrelated open findings do not block destination settlement
Given an active correction route to test-spec and unrelated open code-review findings
When a new test-spec review approves the exact revised test spec with no findings for that review occurrence
Then settlement succeeds for the test spec while the unrelated code-review findings remain open.

Example E3: correction return restores the suspended downstream position
Given the routed destination has a newer registered revision and a current approving review
When workflow requests correction return with the exact route ID and lifecycle revision
Then the CLI restores the recorded downstream stage, blocker, milestone state, and next stage without closing findings or advancing the milestone.

Example E4: duplicate shared architecture registration is withdrawn safely
Given one change registers a canonical architecture path whose document points to another exact governed owner
When workflow requests guarded withdrawal with exact owner and evidence
Then only the duplicate registration and its derived CLI registrations are withdrawn, a durable withdrawal receipt remains, and the architecture file and historical review evidence are unchanged.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | The CLI MUST expose mutating operations `route-correction`, `return-correction`, and `withdraw-artifact-registration` through the existing lifecycle command family. |
| R2 | Every new operation MUST use the existing request envelope, exact change selection, expected lifecycle revision, atomic replacement, post-validation, idempotent retry, and stable result contract. |
| R3 | `route-correction` MUST be authorized only for `stage_authority: workflow`; workflow MUST supply the route and the CLI MUST NOT select a destination. |
| R4 | A route request MUST include exact source stage, destination stage, destination artifact ID, reason, evidence path, preserved finding IDs, and return stage; it MUST include the active milestone ID when one exists. |
| R5 | Route reasons MUST be exactly `upstream-contract-gap`, `upstream-proof-gap`, `upstream-ownership-gap`, `upstream-planning-gap`, or `upstream-stale-input`; unknown reasons MUST fail before consistency checks. |
| R6 | Destination stages MUST be exactly `proposal`, `spec`, `architecture`, `plan`, or `test-spec`, and the destination stage MUST match the destination artifact kind and authoring authority. An ADR correction uses destination stage `architecture`. |
| R7 | The destination artifact MUST exist, be currently settled, have current registered identity, and precede the source stage in the canonical workflow. Forward, lateral, unknown, ambiguous, stale, or already-active routes MUST be rejected. |
| R8 | Route evidence MUST be a contained regular repository file that names the change, source stage, destination artifact, reason, finding IDs, return stage, and current lifecycle revision. |
| R9 | Starting a route MUST move the source workflow blocker into the immutable source snapshot, preserve the rest of the complete source snapshot, and MUST NOT change artifact settlement, review outcomes, finding dispositions, milestone state, semantic artifacts, or evidence files. The suspended source blocker MUST NOT remain an active fatal blocker during the route. |
| R10 | Starting a route MUST set current workflow routing to the destination authoring stage, set the current workflow blocker to null, and persist one active correction-route record sufficient for fresh-checkout reconstruction. Status MUST expose that route as coordination state rather than reclassifying it as a blocker. |
| R11 | While a route is active, `record-artifact-revision` MUST be admitted only for the exact destination artifact and its owning authoring authority, even when the source snapshot contains a blocker or unrelated findings remain open; every other settled-artifact revision MUST remain blocked. No other operation gains permission merely because the current blocker is null. |
| R12 | The routed revision MUST still require exact prior identity and authoring evidence, derive `review-required`, invalidate prior destination review/validation registrations, and leave the correction route active. |
| R13 | Review recording and settlement during a correction MUST scope material findings to the exact review occurrence and target artifact. Open findings from another artifact or review occurrence MUST remain visible but MUST NOT block an otherwise valid destination settlement. |
| R14 | `return-correction` MUST be authorized only for workflow and require the exact active route ID, expected lifecycle revision, and return evidence path. The evidence MUST bind the change ID, route ID, expected lifecycle revision, destination artifact ID, path, and current SHA-256 plus the approving review ID, round, stage authority, outcome, evidence path, and evidence SHA-256. |
| R15 | Return MUST require that the destination artifact identity differs from the route's captured prior identity and has an approving review for that exact revised identity registered after the route started. The required review authority MUST be derived from the destination artifact kind: `proposal-review`, `spec-review`, `architecture-review` for architecture or ADR, `plan-review`, or `test-spec-review`. The registered review facts MUST exactly match the return evidence. |
| R16 | Return MUST restore the preserved source stage, next stage, lifecycle state, blocker, active milestone identity, and milestone state exactly; it MUST NOT settle, resolve, close, advance, or reclassify them. |
| R17 | A route retry with identical durable facts against current state MUST return `already-recorded`; a conflicting active route or stale envelope MUST fail without mutation. |
| R18 | New artifact registration MUST reject a normalized path already registered by another supported governed change with `RL_ARTIFACT_PATH_OWNED` before mutation. |
| R19 | Cross-change collision discovery MUST examine repository-contained supported `docs/changes/*/change.yaml` records only, normalize paths identically to lifecycle registration, and fail closed on unreadable, ambiguous, escaped, or conflicting ownership. |
| R20 | `withdraw-artifact-registration` MUST be authorized only for workflow and in the first release MUST support only artifact kinds `architecture` and `adr`. |
| R21 | Withdrawal MUST require exact artifact ID, artifact path, canonical owner change ID, reason `duplicate-registration`, and a contained evidence path that binds those facts and the current lifecycle revision. |
| R22 | Withdrawal MUST succeed only when the selected artifact's own owning-change pointer identifies the supplied canonical owner, that owner has exactly one matching normalized artifact entry, and the selected change is a different duplicate owner. |
| R23 | Withdrawal MUST refuse the current active artifact, an active correction destination, a uniquely owned path, a missing canonical owner, multiple canonical owners, wrong kind, wrong path, stale revision, or unknown reason with `RL_WITHDRAWAL_UNSAFE`. |
| R24 | Withdrawal MUST remove only the selected change's artifact entry and its matching derived CLI artifact, review, validation, and finding-resolution registrations. It MUST NOT delete or modify the semantic artifact, review records, review log, review resolution, authoring evidence, or canonical owner's state. |
| R25 | Withdrawal MUST persist a deterministic receipt containing the withdrawn artifact ID, kind, normalized path, content identity, canonical owner, evidence identity, request `prior_lifecycle_revision`, and status. The receipt MUST not contain a self-referential resulting revision and MUST not count as an active artifact owner; the common operation result alone reports `resulting_lifecycle_revision`. |
| R26 | Context requested for a non-current authoring stage MUST return `RL_WORKFLOW_ROUTE_REQUIRED` when a legal workflow route is deterministically available and MUST name current stage, requested stage, route owner, blocking finding IDs, and `available_after_workflow_route`. |
| R27 | `permitted_operations` MUST contain only operations executable immediately. Deferred or owner-dependent guidance MUST be represented separately and MUST never contradict the immediate set. |
| R28 | Human output MUST remain bounded and actionable; JSON MUST expose equivalent codes, stages, artifact IDs, route ID, finding IDs, immediate operations, deferred operation, and evidence paths without absolute machine paths. |
| R29 | The operations MUST preserve Git-contained truth, portable skill independence, and the existing separation of semantic judgment, recording, settlement, routing, and continuation. |
| R30 | Unknown new operation fields, route reasons, destination stages, withdrawal kinds, withdrawal reasons, receipt statuses, and route statuses MUST fail closed before consistency logic. |
| R31 | Existing request/result schema version 1 remains readable. The architecture MUST choose either an additive compatible stored representation or an explicit migration; older clients MUST fail closed for new mutations without corrupting existing state. |
| R32 | CI validation MUST detect an active route with missing evidence, mismatched source snapshot, stale destination identity, illegal return, or contradictory workflow routing, and MUST ignore valid withdrawal receipts when counting active owners. |

## Inputs and outputs

`route-correction` request fields are the common lifecycle envelope plus `source_stage`, `destination_stage`, `destination_artifact_id`, `reason`, `evidence_path`, `finding_ids`, `return_stage`, and optional `milestone_id`. `return_stage` must equal the current source stage in the first release.

`return-correction` request fields are the common envelope plus `route_id`, `evidence_path`, and `stage_authority: workflow`. The referenced evidence contains the closed fields required by R14; callers do not duplicate or override those review facts in request fields.

`withdraw-artifact-registration` request fields are the common envelope plus `artifact_id`, `artifact_path`, `canonical_owner_change_id`, `reason: duplicate-registration`, `evidence_path`, and `stage_authority: workflow`.

Successful route output includes the route ID, source snapshot summary, destination, reason, evidence, and resulting lifecycle revision. Successful return includes the restored routing summary. Successful withdrawal includes the withdrawn registration and canonical owner but omits full artifact inventories in concise output.

## State and invariants

- At most one correction route is active per change.
- A correction route is coordination state, not approval, a workflow blocker, or finding resolution.
- The active workflow blocker is null during correction; the original blocker exists only in the immutable source snapshot until exact return restores it.
- Open findings remain attached to their original review occurrence throughout the route.
- Only the routed artifact owner may revise the destination.
- Destination review settlement considers findings from that exact review occurrence, not unrelated global findings.
- Return restores rather than recalculates the source snapshot.
- A withdrawal receipt is durable history but not active artifact ownership.
- No new operation changes semantic Markdown.

## Error and boundary behavior

| Code | Meaning |
| --- | --- |
| `RL_WORKFLOW_ROUTE_REQUIRED` | The requested authoring stage is not current and workflow must record a legal correction route first. |
| `RL_CORRECTION_ROUTE_INVALID` | The route source, destination, reason, evidence, finding set, snapshot, or return is unsupported or contradictory. |
| `RL_ARTIFACT_PATH_OWNED` | Another governed change already owns the normalized artifact path. |
| `RL_WITHDRAWAL_UNSAFE` | Exact canonical ownership and safe duplicate withdrawal cannot be proven. |

Existing `RL_INVALID_REQUEST`, `RL_AUTHORITY_BOUNDARY`, `RL_STALE_OPERATION`, `RL_STALE_EVIDENCE`, `RL_UNRESOLVED_MATERIAL_FINDING`, and `RL_POST_VALIDATION_FAILED` behavior remains applicable.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R3, R4, R5, R6, R7, R8, R14, R18, R19, R20, R21, R22, R23, R30 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R7, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R32 | BND-STATE-001 | - |
| identity-authority | applicable | R3, R6, R7, R8, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R29 | BND-AUTH-001 | - |
| composition-path | applicable | R11, R12, R13, R18, R19, R26, R27, R28, R29, R31, R32 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R2, R15, R16, R17, R23, R25 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R2, R17, R18, R19, R20, R21, R22, R23, R24, R25, R30, R31, R32 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R18, R19, R25, R26, R27, R30, R31, R32 | BND-COMPAT-001 | - |
| external-environment | applicable | R8, R18, R19, R21, R22, R23, R24, R25, R28, R29 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R3, R4, R5, R6, R7, R8, R14, R18, R19, R20, R21, R22, R23, R30 | valid, missing, unknown, malformed, mismatched, additional | Closed request vocabularies fail before consistency checks. | Valid input proceeds; every other partition rejects without mutation. | R30 |
| BND-STATE-001 | state-lifecycle | R7, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R32 | no route, legal route, active route, revised, reviewed, returnable, returned, unique owner, duplicate owner, ambiguous owner, withdrawn, replay, contradictory | One active route suspends one exact source snapshot while current routing has no fatal source blocker; only a provable duplicate can leave active ownership. | Legal route, return, and exact duplicate withdrawal commit once; illegal routes, contradictory state, and unsafe ownership refuse without mutation. | R10 |
| BND-AUTH-001 | identity-authority | R3, R6, R7, R8, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R29 | workflow route, destination authoring, destination review, workflow return, canonical owner, duplicate owner, wrong owner, active dependency | Each actor mutates only its owned operation, exact target, and exact review occurrence; canonical ownership is proved from repository evidence and never reassigned implicitly. | Correct operation and exact duplicate withdrawal proceed; crossing authority, mismatching identity, or ambiguous ownership fails. | R3 |
| BND-COMPOSE-001 | composition-path | R11, R12, R13, R18, R19, R26, R27, R28, R29, R31, R32 | workflow, CLI, authoring skill, review skill, validator, human, JSON | All consumers share immediate permission and exact route facts without duplicating route logic. | Equivalent decisions and diagnostics appear across paths. | R27 |
| BND-TEMPORAL-001 | temporal-retry | R2, R15, R16, R17, R23, R25 | current, stale, identical replay, conflicting replay, interrupted replacement | Expected revision precedes every mutation and durable facts are never duplicated or self-referential. | Current commits; identical current replay is idempotent; stale or conflicting replay blocks. | R17 |
| BND-RECOVERY-001 | failure-recovery | R2, R17, R18, R19, R20, R21, R22, R23, R24, R25, R30, R31, R32 | validation failure, partial replace, post-validation failure, unsafe withdrawal | Rejected operations preserve prior bytes and semantic artifacts. | Existing atomic recovery applies; unsafe recovery produces a stable refusal. | R2 |
| BND-COMPAT-001 | compatibility-migration | R18, R19, R25, R26, R27, R30, R31, R32 | old CLI, compatible current CLI, new route state, withdrawal receipt, rollback | Unsupported clients never rewrite unknown coordination state. | Compatible clients operate; older or mixed clients fail closed with guidance. | R31 |
| BND-ENV-001 | external-environment | R8, R18, R19, R21, R22, R23, R24, R25, R28, R29 | fresh checkout, contained files, symlink escape, unreadable record, no hidden state | All authority and recovery evidence is repository-contained and path-safe. | Fresh checkout reconstructs state; unsafe filesystem evidence blocks. | R29 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R15, R16, R17 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | A destination artifact changes or is reviewed while downstream findings remain open. | Only the exact routed revision and its scoped review can enable return; downstream findings remain open and source state restores exactly. |
| INT-002 | R18, R19, R21, R22, R23, R24, R25 | BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001, BND-ENV-001 | A branch contains a duplicate shared architecture registration. | New duplicates are prevented; an existing exact duplicate withdraws atomically without changing semantic or canonical-owner files. |
| INT-003 | R26, R27, R31 | BND-COMPOSE-001, BND-COMPAT-001 | A skill or older CLI sees a blocked upstream operation. | Immediate and deferred operations remain distinct; unsupported clients fail closed rather than recommending direct edits. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | regression | R9, R10, R11, R12 | BND-STATE-001 | REG-UPSTREAM-ROUTE-DEADLOCK | - |
| E2 | regression | R11, R12, R13 | BND-STATE-001, BND-AUTH-001 | REG-GLOBAL-FINDING-SETTLEMENT | - |
| E3 | illustration | R15, R16, R17 | BND-STATE-001, BND-TEMPORAL-001 | - | - |
| E4 | regression | R18, R19, R21, R22, R23, R24, R25 | BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001 | REG-DUPLICATE-ARCHITECTURE-OWNER | - |

## Compatibility and migration

Existing schema-version-1 changes without correction or withdrawal records remain readable and writable for existing operations. New fields are additive only if architecture proves older supported CLIs preserve or reject them safely; otherwise the implementation must introduce an explicit supported schema migration before enabling the new operations.

Published workflow and authoring skills must not request the new operations until their declared CLI compatibility includes this release. Rollback must preserve route and withdrawal records as readable blocked evidence and must never instruct direct field editing.

## Observability

Status and context expose active route ID, source stage, destination artifact, reason, return stage, preserved milestone, finding IDs, and readiness without dumping full artifact inventories in concise output. Withdrawal output names the artifact ID, normalized repository path, canonical owner, receipt status, and resulting revision. File logs follow the separate CLI observability contract and never become lifecycle evidence.

## Security and privacy

Requests and evidence paths are repository-relative, contained, regular files with no symlink traversal. Diagnostics omit absolute paths and raw file content. `stage_authority` remains a structural claim rather than authenticated identity; Git permissions, protected branches, and trusted CI remain the adversarial boundary.

## Accessibility and UX

No graphical interface is introduced. Human diagnostics must be understandable without color and lead with the current stage, requested stage, blocking reason, and owning next action. JSON must expose the same facts through stable fields.

## Performance expectations

Cross-change ownership discovery may scan supported change records but must not scan generated archives, Git history, network resources, or unrelated file contents. Repository fixtures should establish a bounded regression budget; correctness and fail-closed ownership take priority over caching.

## Edge cases

EC1. Workflow routes to the current or a downstream stage: reject `RL_CORRECTION_ROUTE_INVALID`.

EC2. A second route is requested while one is active: identical current facts return `already-recorded`; all conflicts reject.

EC3. The route cites findings not present in the current durable review evidence: reject without mutation.

EC4. The destination artifact changes before route commit: reject stale operation or evidence.

EC5. The destination revision is recorded but no new review settles it: return remains blocked.

EC6. Unrelated code-review findings remain open while test-spec review is clean: test-spec settlement succeeds and unrelated findings remain open.

EC7. A withdrawal targets a proposal, spec, plan, or test spec: reject as unsupported in the first release.

EC8. The artifact pointer and canonical owner's entry disagree: reject `RL_WITHDRAWAL_UNSAFE`.

EC9. Withdrawal succeeds and is retried with refreshed equivalent facts: return `already-recorded` using the receipt.

EC10. Post-validation detects route or receipt inconsistency: restore prior bytes under the existing recovery protocol.

EC11. Return evidence omits or mismatches any route, artifact, review-occurrence, authority, outcome, evidence-identity, or expected-revision fact: reject `RL_CORRECTION_ROUTE_INVALID` without mutation.

## Non-goals

- Automatic route selection or autonomous workflow execution.
- Arbitrary artifact deregistration, stage assignment, status setting, finding closure, or milestone advancement.
- Semantic review, artifact editing, PR operations, release, deployment, or merge.
- Deleting historical review or authoring evidence.
- Defending against a malicious maintainer with unrestricted Git and filesystem authority.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every route, return, and withdrawal request field has valid, missing, unknown, malformed, stale, wrong-authority, and conflicting fixtures. |
| AC2 | A routed upstream artifact can be revised and settled while the suspended source blocker and unrelated downstream findings remain preserved but non-fatal to that exact operation, and return restores the exact source snapshot including its blocker. |
| AC3 | No route operation closes findings, settles artifacts, advances milestones, or chooses a destination. |
| AC4 | New cross-change collisions are rejected and one existing duplicate architecture registration is withdrawn without semantic-file changes. |
| AC5 | Atomicity and fault-injection tests prove prior bytes survive every rejected or interrupted new operation. |
| AC6 | Human and JSON status distinguish immediate from post-route operations and expose equivalent actionable facts. |
| AC7 | A fresh checkout reproduces active route, return readiness, withdrawal history, and canonical ownership without hidden state. |
| AC8 | Existing lifecycle operations and portable skill use remain compatible, and older unsupported clients fail closed. |
| AC9 | CI validation rejects contradictory routes and ambiguous ownership while not counting withdrawal receipts as active owners. |

## Open questions

None. Architecture must choose the additive-versus-migrated stored representation while preserving R31's observable compatibility outcome.

## Next artifacts

- Independent spec review.
- Architecture assessment and architecture/ADR authoring because the change modifies public operation, persistence, repository discovery, transaction, and authority boundaries.
- Execution plan after approved architecture.
- Traceable test specification after plan review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`; not approved, architecture-ready, plan-ready, implementation-ready, verified, or PR-ready.
