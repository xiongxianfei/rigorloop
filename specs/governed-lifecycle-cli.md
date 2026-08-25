# Governed Lifecycle CLI

## Owning change record

`docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Governed Lifecycle CLI for RigorLoop](../docs/proposals/2026-08-24-governed-lifecycle-cli.md), Proposal ID `RL-PROP-CLI-001`, accepted.

## Goal and context

The first release makes the existing local `rigorloop` executable the canonical interpreter and guarded mutation boundary for supported governed lifecycle state. Callers request closed semantic operations; the CLI validates current repository evidence and derives the permitted `change.yaml` result. Stage and review skills retain semantic judgment and artifact authoring but stop encoding lifecycle field-editing procedure.

The repository remains the durable source of truth. The CLI neither stores required state outside the repository nor routes or executes lifecycle stages.

## Glossary

- **Governed change**: a change record using `lifecycle_contract: stage-owned-change-local-v1`.
- **Recorded state**: lifecycle values serialized in the governed change record.
- **Effective state**: the CLI's interpretation after applying evidence identity, freshness, blockers, and compatibility rules.
- **Semantic artifact**: a proposal, spec, architecture record, plan, test spec, review, resolution, explanation, or verification artifact authored by its owning stage.
- **Registration**: validating an existing semantic artifact or evidence file and recording its identity or reference in the governed change record.
- **Settlement**: the lifecycle transition derived from a recorded review outcome for the matching artifact.
- **Lifecycle revision**: a deterministic identity of the exact governed state used as the optimistic-concurrency basis for an operation.

## Examples first

Example E1: unresolved finding blocks settlement
Given a current specification review with material finding `F-12` still open
When a caller requests `settle-artifact` for that specification
Then the command exits blocked, reports `RL_UNRESOLVED_MATERIAL_FINDING`, identifies `F-12`, and leaves every tracked file byte-unchanged.

Example E2: stale review cannot settle a revised artifact
Given a recorded approved review for specification identity `sha256:A` and the current specification identity is `sha256:B`
When a caller requests `settle-artifact`
Then the command exits blocked with `RL_STALE_EVIDENCE` and does not reuse the approval.

Example E3: skill uses concise lifecycle procedure
Given a governed `spec-review` invocation
When the review skill requests `context spec-review --format json`
Then the response identifies the exact change, spec, review round, allowed review-record path, blockers, lifecycle revision, and permitted recording operation without requiring the skill to calculate settlement fields.

Example E4: portable skill remains independent
Given a repository without a governed change record
When a portable skill authors an isolated artifact without requesting a governed transition
Then no lifecycle CLI state or `change.yaml` is required.

Example E5: authored revision is registered without a field setter
Given an authorized governed spec skill has written a revised specification and its bound authoring evidence
When it requests `record-artifact-revision` with the exact artifact, evidence, prior identity, and current lifecycle revision
Then the CLI verifies those bytes, invalidates evidence for the replaced identity, derives `review-required`, changes only the matching artifact entry, and leaves workflow routing unchanged.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | The CLI MUST treat Git-trackable repository artifacts as the complete durable input required to reconstruct governed status at a supported commit. |
| R2 | The CLI MUST support governed lifecycle commands under `rigorloop lifecycle` and MUST reject lifecycle mutation for records that do not declare the supported lifecycle contract. |
| R3 | The first release MUST expose the read-only commands `status`, `context <stage>`, and `validate`, plus the mutating operations `record-artifact-revision`, `record-review`, `record-validation`, `record-finding-resolution`, `settle-artifact`, `start-milestone`, `complete-milestone`, `migrate`, and `repair`. |
| R4 | Mutating commands MUST accept a versioned JSON request through `--request <repository-relative-path>` and MUST reject unknown request schema versions, operation names, fields, and closed-vocabulary values before mutation. |
| R5 | The public interface MUST NOT expose a command or request field that assigns arbitrary lifecycle fields or caller-selected target states. |
| R6 | Every command MUST support human output by default and `--format json`; both formats MUST derive from the same interpreted result. |
| R7 | JSON results MUST include `schema_version`, `command`, `operation`, `status`, `change_id`, `lifecycle_revision`, `effective_state`, `blockers`, `permitted_operations`, `artifacts`, `warnings`, and `errors`. |
| R8 | Errors MUST include a stable `code`, summary, blocking invariant, relevant identities, and a corrective operation only when deterministically known. |
| R9 | `status` MUST distinguish recorded state, evidence state, and effective state and report current stage, active artifact or milestone, blockers, unresolved findings, stale evidence, permitted operations, and supporting repository paths. |
| R10 | `context <stage>` MUST return only the validated facts needed by that stage: exact change, operation, target artifact, settled upstream inputs, review round when applicable, authorized output path, blockers, lifecycle revision, and permitted registration operation. |
| R11 | If exactly one active governed change exists, read-only commands MAY select it implicitly; otherwise the caller MUST provide `--change <change-id>`, and zero or multiple candidates MUST produce a non-mutating diagnostic. |
| R11a | `record-artifact-revision` MUST validate an existing stage-authored artifact and authoring-evidence file, exact artifact ID, kind, role, path, stage authority, and prior identity for revisions; it MUST create or revise only the matching artifact entry, invalidate registrations tied to the replaced identity, and derive `review-required` without changing workflow routing or accepting a target state. |
| R12 | `record-review` MUST validate an existing review record, review-log entry, review round, outcome, reviewed artifact identity, and finding set before registering it; it MUST NOT make or alter the semantic judgment. |
| R13 | `record-validation` MUST validate an existing evidence artifact and exact subject identity before registration; command success or test exit status alone MUST NOT imply approval, settlement, or readiness. |
| R14 | `record-finding-resolution` MUST validate an existing resolution entry, allowed disposition, finding identity, owner, required evidence, and review-log consistency before registration. |
| R15 | `settle-artifact` MUST derive the target lifecycle state from the matching current review outcome and MUST reject missing, stale, contradictory, unresolved, wrong-round, wrong-artifact, or unauthorized evidence. |
| R16 | `start-milestone` and `complete-milestone` MUST enforce the active plan identity, unique current milestone, predecessor ordering, milestone kind, required proof, review state, and remaining-milestone projection. |
| R17 | A material change to an artifact or governed input MUST apply the first-release evidence-invalidation matrix in this spec; architecture MAY define the mechanism but MUST NOT change the matrix outcomes. Stale evidence MUST remain inspectable but MUST NOT authorize settlement. |
| R18 | Every mutating request MUST include the lifecycle revision returned by prior status or context, and a mismatch MUST fail with `RL_STALE_OPERATION` before mutation. |
| R19 | First-release semantic recording and transition operations MUST mutate only the exact governed `change.yaml`; referenced semantic artifacts MUST already exist and remain owned by their stage skills. |
| R20 | Mutation MUST validate the complete pre-state, compute and validate a deterministic candidate, persist a same-directory recovery bundle containing the prior bytes and transaction identity, durably replace `change.yaml`, verify the persisted result, remove the recovery bundle, and report success only after those steps pass. |
| R21 | Rejection or interruption before replacement MUST leave `change.yaml` byte-unchanged. Failure after replacement MUST automatically restore and verify the prior bytes when possible; if restoration cannot be verified, the recovery bundle MUST remain and every lifecycle command except `validate` and the named `reconcile-interrupted-replace` repair MUST fail with `RL_POST_VALIDATION_FAILED`. Startup and validation MUST detect and deterministically reconcile or report that condition without treating the candidate as settled. |
| R22 | A request whose expected lifecycle revision is not current MUST fail under R18 even when an equivalent earlier operation completed. An equivalent operation submitted against the current revision MUST return explicit `already-recorded` success when all requested durable facts are present and identical, without duplicating evidence, review rounds, findings, or transitions; conflicting facts MUST fail. |
| R23 | `validate` MUST check schema compatibility, artifact identity, lifecycle combinations, evidence references and freshness, review and resolution consistency, milestone projections, lifecycle revision consistency, and detectable unsupported manual mutations. |
| R24 | `migrate` MUST support only explicitly enumerated source schema versions and deterministic transformations; for an existing supported artifact it MUST seed the current path, kind, role, content identity, authoring authority, and available authoring-evidence identity so the first later revision has a registered prior identity; unsupported or ambiguous legacy state MUST fail without mutation. |
| R25 | `repair` MUST accept only named recoverable condition codes, show its exact planned mutation in dry-run output, require the current lifecycle revision, and refuse unknown corruption or arbitrary field edits. |
| R26 | The CLI MUST reject unsupported repository schema or CLI/repository compatibility combinations with `RL_UNSUPPORTED_SCHEMA` or `RL_INCOMPATIBLE_VERSION` and actionable version guidance. |
| R27 | Machine-readable output, error codes, request schemas, lifecycle revision calculation, and resulting diffs MUST be deterministic for identical supported inputs except documented timestamp or actor provenance fields. |
| R28 | Governed canonical skills and supported workflow automation MUST use CLI status, context, registration, and settlement operations rather than directly mutating lifecycle fields after enforcement is activated. |
| R29 | Skills MUST retain semantic criteria, artifact responsibilities, authority boundaries, stop behavior, and portable-mode guidance; migration MUST NOT remove semantic review or engineering guidance merely to reduce size. |
| R30 | Mandatory enforcement MUST remain disabled until supported skills and adapters are migrated, conformance and recovery proof passes, version compatibility is documented, and CI can invoke `rigorloop lifecycle validate` non-interactively. |
| R31 | The first release MUST NOT perform workflow routing, invoke agents, author semantic artifacts, infer semantic approval, open or modify pull requests, push, merge, deploy, or access hosted control planes. |
| R32 | The CLI MUST avoid printing secrets, raw environment values, credentials, private request payloads, or machine-local absolute paths in human or JSON diagnostics. |
| R33 | A fresh checkout at the same supported commit MUST reproduce the same effective state and permitted operations without a prior process, conversation, daemon, or uncommitted cache. |
| R34 | Representative governed skill profiles MUST demonstrate the measured token objective or record an owner-approved revised threshold before mandatory enforcement; measurement MUST separate mechanical instructions, semantic guidance, and returned CLI context. |

## Inputs and outputs

Common command inputs are repository root discovery, optional `--change`, `--format human|json`, and optional `--dry-run` for mutating commands. Mutation requests contain `schema_version`, `operation`, `change_id`, `expected_lifecycle_revision`, operation-specific artifact IDs and repository-relative evidence paths, and optional documented provenance. `record-artifact-revision` additionally contains `artifact_kind`, `artifact_role`, `artifact_path`, `stage_authority`, and optional `prior_artifact_sha256`; omission of the prior identity means creation and is valid only when the entry and path are non-conflicting.

Repository-relative paths must be normalized, remain inside the repository, identify regular files, and reject symlink traversal. Request files are inputs only and are not durable evidence unless separately registered by an allowed operation.

Exit codes extend the existing CLI contract: `0` success or idempotent already-recorded result, `2` structurally blocked operation, `3` repository validation failure, `4` invalid usage/request/schema, `5` stale revision or mutation conflict, and `1` internal failure.

## State and invariants

- `change.yaml` remains the sole mutable governed lifecycle snapshot.
- Semantic Markdown remains stage-owned and is never rewritten by lifecycle commands.
- A review or evidence identity always names exact bytes using the configured supported digest algorithm.
- One lifecycle revision represents the complete mutation-relevant governed snapshot and referenced identity set.
- Recording does not imply settlement; settlement does not imply workflow continuation; structural permission does not imply semantic truth.
- Workflow routing fields change only through workflow-owned operations, even when another CLI operation proves a transition structurally eligible.
- Unknown closed-vocabulary values fail before consistency checks.

### First-release evidence-invalidation matrix

The CLI compares registered identities and declared dependency edges; it does not infer semantic dependency from filenames or prose. In every row, recorded historical evidence remains readable. Invalidation changes effective state and permitted operations; it does not silently rewrite the semantic evidence artifact.

| Changed subject | Dependent evidence | Effective result | Settlement or milestone effect | Required corrective operation |
| --- | --- | --- | --- | --- |
| Reviewed artifact bytes or registered identity | Review outcome, findings, and finding resolutions for the prior identity | `stale` | Prior settlement is ineffective; the artifact returns to review-required effective state | Register the revision and record a new review round |
| Validation subject bytes or registered identity | Validation evidence for the prior identity | `stale` | Any settlement or milestone completion requiring that proof is blocked | Record validation evidence for the current identity |
| Registered upstream artifact identity on an explicit dependency edge | Downstream review and validation evidence whose recorded dependency set contains the prior identity | `stale` | Dependent downstream settlement is ineffective | Revise or reaffirm the downstream artifact, then rereview and revalidate as required |
| Active plan identity or governed milestone definition | Milestone evidence and completion for the prior plan identity | `stale` | No later milestone may start; affected completion is ineffective | Settle the current plan identity and repeat affected milestone proof and review |
| Registered review record, review-log entry, or resolution bytes | Registration and settlement derived from the prior evidence identity | `stale` or `contradictory` | Settlement is ineffective; contradictory evidence blocks all settlement operations | Correct the stage-owned evidence, then register and settle it again |
| Provenance-only field explicitly excluded by the versioned identity schema | None | `current` | No effect | None |

An implementation or architecture revision that adds an invalidation class or changes any result in this table requires a specification revision. Architecture must define the exact dependency serialization, digest inputs, and efficient evaluation of these outcomes.

### Interrupted-replacement recovery

The recovery bundle is transient same-directory transaction state, not governed truth. It contains the prior `change.yaml` bytes, prior and candidate identities, and a closed transaction phase; it must not contain semantic judgments or secrets. A clean checkout needs no bundle to reconstruct status.

On startup, the CLI compares `change.yaml` with the bundle identities. A verified prior file removes an abandoned pre-replacement bundle. A verified candidate is post-validated: success completes the transaction, while failure restores and verifies the prior bytes. Any unknown identity combination or failed restoration remains recovery-blocked and admits only `validate` or `repair` with condition `reconcile-interrupted-replace`; repair may restore only the bundle's verified prior bytes and must refuse every other mutation.

## Error and boundary behavior

The initial stable error set includes:

| Code | Meaning |
| --- | --- |
| `RL_CHANGE_NOT_FOUND` | No requested governed change exists. |
| `RL_AMBIGUOUS_CHANGE` | Implicit selection found multiple active governed changes. |
| `RL_UNSUPPORTED_SCHEMA` | Repository schema is not supported. |
| `RL_INCOMPATIBLE_VERSION` | CLI, schema, skill, or adapter compatibility is unsupported. |
| `RL_INVALID_REQUEST` | Request schema, operation, field, path, or closed value is invalid. |
| `RL_OPERATION_NOT_PERMITTED` | Current effective state does not admit the operation. |
| `RL_STALE_OPERATION` | Expected lifecycle revision does not match current state. |
| `RL_STALE_EVIDENCE` | Evidence identity does not match its current subject. |
| `RL_UNRESOLVED_MATERIAL_FINDING` | A material finding remains open. |
| `RL_MILESTONE_ORDER` | Milestone selection or predecessor ordering is invalid. |
| `RL_AUTHORITY_BOUNDARY` | The operation would cross its documented mutation authority. |
| `RL_POST_VALIDATION_FAILED` | Candidate state failed validation and was not committed or requires documented recovery. |
| `RL_REPAIR_UNSAFE` | The condition is unknown or unsafe for a named repair. |

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R3, R4, R5, R6, R7, R8, R11, R24, R25, R26 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R9, R15, R16, R17, R18, R22, R23, R24, R25, R30 | BND-STATE-001, BND-STATE-002 | - |
| identity-authority | applicable | R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R28, R29, R30, R31 | BND-AUTH-001, BND-AUTH-002 | - |
| composition-path | applicable | R6, R10, R19, R23, R28, R29, R30, R31 | BND-COMPOSE-001, BND-COMPOSE-002 | - |
| temporal-retry | applicable | R17, R18, R20, R21, R22, R27 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R20, R21, R22, R23, R24, R25 | BND-RECOVERY-001, BND-RECOVERY-002 | - |
| compatibility-migration | applicable | R24, R26, R27, R28, R29, R30, R33, R34 | BND-COMPAT-001 | - |
| external-environment | applicable | R1, R20, R31, R32, R33 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R3, R4, R5, R6, R7, R8, R11, R24, R25, R26 | valid, missing, unknown, malformed, ambiguous, unsupported | Unknown values never fall through to consistency logic. | Valid input is interpreted; every other partition fails before mutation with a stable code. | R4 |
| BND-STATE-001 | state-lifecycle | R9, R15, R16, R17, R18, R22, R23, R24, R25, R30 | recorded-current, recorded-stale, blocked, unsettled, settled, invalid | Effective state derives from current evidence rather than raw status alone. | Current state permits closed operations; stale or invalid state blocks with evidence. | R9 |
| BND-STATE-002 | state-lifecycle | R9, R15, R16, R17, R18, R22, R23, R24, R25, R30 | predecessor-incomplete, eligible, active, proof-incomplete, review-incomplete, complete | A later milestone never starts before its required predecessor and proof close. | Eligible transitions succeed once; invalid ordering blocks; repeat is idempotent. | R16 |
| BND-AUTH-001 | identity-authority | R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R28, R29, R30, R31 | exact subject, wrong subject, stale subject, wrong round, unresolved finding | Evidence can authorize only the exact subject revision and review occurrence it records. | Exact current evidence may register or settle; mismatches block. | R15 |
| BND-AUTH-002 | identity-authority | R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R28, R29, R30, R31 | stage artifact authoring, lifecycle registration, settlement, routing | Each operation mutates only its owned surface; CLI never acquires semantic or routing authority implicitly. | Boundary-respecting operations proceed; authority crossings fail. | R19 |
| BND-COMPOSE-001 | composition-path | R6, R10, R19, R23, R28, R29, R30, R31 | human, JSON, local, CI | Every path uses one interpreter and stable result model. | Equivalent facts and exit status are observed across representations. | R6 |
| BND-COMPOSE-002 | composition-path | R6, R10, R19, R23, R28, R29, R30, R31 | governed skill, workflow, human, portable skill | Governed mutation uses the CLI; portable semantic work remains independent. | Governed callers share enforcement; portable callers are not forced into lifecycle state. | R28 |
| BND-TEMPORAL-001 | temporal-retry | R17, R18, R20, R21, R22, R27 | current request, stale request, interrupted pre-replace, completed replay, conflicting replay | Revision comparison precedes mutation and completed evidence is never duplicated. | Current request commits; stale/conflicting requests block; identical replay is idempotent. | R18 |
| BND-RECOVERY-001 | failure-recovery | R20, R21, R22, R23, R24, R25 | validation failure, write failure, interruption, post-validation failure | No rejected pre-replacement operation changes committed state. | Safe failure leaves bytes unchanged; detectable recovery condition produces explicit diagnostics. | R20 |
| BND-RECOVERY-002 | failure-recovery | R20, R21, R22, R23, R24, R25 | named recoverable condition, unknown corruption, unsafe repair | Repair vocabulary is closed and has no arbitrary setter. | Named repair produces deterministic plan/result; unknown state refuses. | R25 |
| BND-COMPAT-001 | compatibility-migration | R24, R26, R27, R28, R29, R30, R33, R34 | supported current, supported legacy, unsupported newer, unsupported older, mixed versions | Mutation occurs only for declared compatible combinations. | Supported state runs or migrates; unsupported or mixed state blocks with guidance. | R26 |
| BND-ENV-001 | external-environment | R1, R20, R31, R32, R33 | fresh checkout, writable local filesystem, read-only filesystem, symlink/path escape, hidden-state absence | Durable truth remains repository-contained and paths remain inside the repository. | Supported local checkout reconstructs state; unsafe filesystem conditions block without leakage. | R33 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R15, R17, R18 | BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001 | Artifact changes after context and review were calculated. | Both stale lifecycle revision and stale evidence are detected before settlement; neither old approval nor old context is reused. |
| INT-002 | R19, R20, R21 | BND-AUTH-002, BND-RECOVERY-001, BND-ENV-001 | A mutating operation is interrupted or cannot safely replace the state file. | Semantic artifacts remain untouched, committed state is unchanged, and recovery diagnostics name the safe next action. |
| INT-003 | R24, R25, R26, R27, R28, R29, R30 | BND-COMPAT-001, BND-COMPOSE-002, BND-RECOVERY-002 | Skills migrate before a compatible CLI or repair path exists. | Mandatory enforcement remains disabled and CI reports compatibility blockers rather than encouraging direct edits. |
| INT-004 | R6, R7, R8, R9, R10, R32 | BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001 | Human and JSON diagnostics diverge or expose environment-sensitive data. | Both formats report equivalent bounded facts and suppress secrets and absolute local paths. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R15 | BND-STATE-001, BND-AUTH-001 | - | - |
| E2 | illustration | R17, R18 | BND-AUTH-001, BND-TEMPORAL-001 | - | - |
| E3 | illustration | R10, R28, R29 | BND-AUTH-002, BND-COMPOSE-002 | - | - |
| E4 | illustration | R28, R29, R30, R31 | BND-COMPOSE-002 | - | - |

## Compatibility and migration

The first release is additive and enforcement defaults off. Existing supported repositories remain readable through `status` and `validate`. A repository is writable only when its schema declares a supported migration or current version. Migration writes a deterministic current snapshot, registers the exact current identities of supported existing artifacts without changing their settlement state, and preserves historical semantic artifacts.

Canonical skills and adapters migrate only after the CLI contract is shipped and validated. Mixed deployments fail closed for mutation while retaining read-only diagnostics. Rollback before enforcement restores the existing validated direct-edit process; rollback after enforcement requires a compatibility release and never instructs users to perform undocumented status edits.

## Observability

Every command reports selected change, operation, effective state, lifecycle revision, result status, blockers, evidence paths, and permitted next operations. Mutating success additionally reports the prior and resulting lifecycle revisions and the exact changed repository path. Diagnostics are deterministic and bounded; verbose expansion may add rule identifiers and evidence details without changing status or exit code.

## Security and privacy

The CLI is an integrity boundary against accidental or ordinary stale mutation, not a cryptographic security perimeter. It validates repository-relative paths, rejects symlink escape, avoids shell evaluation of request values, and suppresses secrets, raw environment values, credentials, private hostnames, and absolute local paths. Strong adversarial authorization remains the responsibility of Git permissions, protected branches, trusted CI, and organizational controls.

## Accessibility and UX

No graphical interface is introduced. Human output must be readable without color, preserve meaning when color is disabled, use concise headings and stable error codes, and provide a deterministic corrective operation when known. JSON provides equivalent non-visual machine access.

## Performance expectations

Read-only status and context should avoid invoking unrelated language toolchains or network access. Validation may scale with the governed evidence set but must not scan generated archives or unrelated changes unless their identities are dependencies. Performance thresholds will be established from repository fixtures before enforcement; correctness and deterministic freshness checks take precedence over speculative caching.

## Edge cases

EC1. No governed changes exist: return `RL_CHANGE_NOT_FOUND` without creating state.

EC2. Multiple active changes exist and `--change` is absent: return `RL_AMBIGUOUS_CHANGE` with candidate IDs.

EC3. The request file is outside the repository, a symlink, malformed JSON, or contains unknown fields: return `RL_INVALID_REQUEST` before mutation.

EC4. Evidence exists but its current bytes differ from the registered identity: expose it as stale and block reliance.

EC5. Two callers use the same lifecycle revision: exactly one changed operation may commit; the other receives `RL_STALE_OPERATION`.

EC6. A caller retries its original old-revision envelope after commit: return `RL_STALE_OPERATION`. If it refreshes context and submits equivalent durable facts against the current revision, return `already-recorded` without a duplicate transition; conflicting facts fail.

EC7. Persisted-result verification or post-validation fails: do not report success, automatically restore and verify the prior bytes, and emit `RL_POST_VALIDATION_FAILED`. If restoration cannot be verified, preserve the recovery bundle, block other lifecycle commands, and permit only validation or `reconcile-interrupted-replace` repair.

EC8. A later CLI sees a newer schema or unknown repair condition: preserve state and fail closed.

EC9. A workflow asks the CLI to continue after settlement: the CLI may report structural eligibility but does not invoke or select the next stage.

EC10. A portable skill runs in a repository containing unrelated governed changes: it remains isolated unless an exact governed mutation is requested.

## Non-goals

- Semantic review, code generation, agent invocation, workflow orchestration, or automatic lifecycle progression.
- Pull-request, push, merge, release, deployment, hosted control-plane, or cryptographic authorization behavior.
- Cross-repository or distributed transactions.
- Multi-file mutation of semantic artifacts in the first release.
- Arbitrary lifecycle field editing or general-purpose workflow configuration.
- Replacing readable Git-tracked state with an event database, daemon, or required cache.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every supported operation has valid, invalid-predecessor, unknown-value, stale-revision, and idempotent-retry fixtures. |
| AC2 | Unresolved findings, stale evidence, wrong identities, wrong rounds, out-of-order milestones, unsupported schemas, and unsafe repairs are rejected before mutation. |
| AC3 | Fault injection before replacement preserves the prior `change.yaml` bytes, and recovery-condition fixtures produce deterministic diagnostics. |
| AC4 | Identical fixtures and requests produce identical lifecycle diffs and JSON results except documented provenance. |
| AC5 | Human and JSON output agree on state, blockers, identities, permitted operations, and exit status. |
| AC6 | A fresh checkout reconstructs the same effective state without hidden state. |
| AC7 | Canonical governed skills and generated Codex, Claude Code, and opencode packages use the CLI for lifecycle operations and retain semantic guidance. |
| AC8 | CI invokes non-interactive lifecycle validation and rejects inconsistent or unsupported governed state. |
| AC9 | Token reports separately measure removed mechanics, retained semantic guidance, returned CLI context, and total representative profile cost. |
| AC10 | Mandatory enforcement remains off until migration, compatibility, conformance, recovery, adapter, CI, and measurement gates are recorded as passed or explicitly owner-resolved. |

## Open questions

- The architecture must choose the internal shared lifecycle-engine boundary and how Node CLI code and Python validation converge without competing authorities.
- The architecture must define the digest inputs for lifecycle revision and the precise durable replace/recovery mechanism.
- The specification may be amended before implementation if measured token baselines require replacing the provisional 30% objective with a justified threshold.

## Next artifacts

- Independent spec review.
- Architecture assessment, followed by architecture authoring and review because the accepted proposal and this contract change cross-component authority, persistence, compatibility, and transaction boundaries.
- Execution plan after approved architecture.
- Traceable test specification after plan review.

## Follow-on artifacts

None yet

## Readiness

Ready for `spec-review`; not approved, architecture-ready, plan-ready, implementation-ready, verified, or PR-ready.
