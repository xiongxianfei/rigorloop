# CLI observability and token-efficient results

## Owning change record

`docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md`

## Goal and context

RigorLoop must retain a bounded, privacy-safe machine-local history of CLI execution while keeping routine human and agent results concise. Logging is diagnostic and must remain independent of governed lifecycle truth, semantic command behavior, transaction correctness, and exit status.

The first compatibility slice adds default local logging, log discovery and exact invocation lookup, and opt-in concise and detailed projections. Existing default human output and existing JSON contracts remain unchanged throughout v0.4.x. Concise defaults may be adopted only at the declared v0.5.0 compatibility boundary after the measurement and semantic-preservation gates in this specification pass.

## Glossary

| Term | Meaning |
| --- | --- |
| Invocation | One CLI process execution that reaches minimum logger initialization. |
| Invocation ID | A random 16-character lowercase hexadecimal identifier shared by one invocation's start and completion events. |
| Semantic result | The command outcome, repository mutation, exit class, and continuation facts produced independently of logging. |
| Console event | A diagnostic rendered to stderr when its severity meets the console threshold. |
| File event | One versioned JSON object appended as one JSON Lines record to the local log. |
| Concise projection | A result containing the closed continuation-critical field set and omitting unrelated detail. |
| Detailed projection | The complete supported result representation for the command family. |
| Minimum logger initialization | The point after safe configuration and invocation-ID creation but before command dispatch and request parsing. |

## Examples first

Example E1: successful lifecycle status is recorded without console noise
Given default logging configuration and a valid governed change
When a caller runs lifecycle status
Then stdout retains the v0.4.x default result, stderr is empty, and the local log contains correlated `invocation-start` and `invocation-complete` info events.

Example E2: changes-requested settlement remains actionable in concise JSON
Given a registered changes-requested review with open findings
When a caller requests `settle-artifact` with the concise JSON projection
Then stdout identifies the operation, status, change, resulting lifecycle revision, state change, next operation, finding IDs, and invocation ID without returning the complete artifact inventory.

Example E3: expected governance rejection is quiet but searchable
Given an approved review whose material finding remains open
When settlement is rejected with `RL_UNRESOLVED_MATERIAL_FINDING`
Then the semantic exit code is unchanged, stderr remains empty at the default console threshold, and the completion event is recorded at warning with the stable code and finding IDs.

Example E4: logging failure does not change lifecycle behavior
Given the log directory cannot be written safely
When a lifecycle mutation otherwise succeeds
Then the repository mutation and semantic exit code are unchanged, stderr contains one bounded `RL_LOG_UNAVAILABLE` diagnostic, and a new projection reports degraded observability without claiming a file record exists.

Example E5: exact lookup never reruns an operation
Given invocation `a1b2c3d4e5f60718` is present in a retained log
When a caller runs `rigorloop logs show a1b2c3d4e5f60718 --format json`
Then the command returns only the allowlisted retained events for that invocation and performs no governed mutation.

Example E6: rotation remains inside the resolved directory
Given the active log would exceed its size limit
When another event is appended
Then rotation retains only the configured archive count, never follows a symlink or deletes outside the resolved log directory, and either records the event safely or reports degraded observability without changing the semantic result.

Example E7: concise defaults fail the adoption gate
Given the six v1 profiles achieve only a 25% unweighted median reduction against the recorded v0.4.x baseline
When release readiness for v0.5.0 is evaluated
Then concise projections remain opt-in and existing defaults remain unchanged.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Every CLI invocation that reaches minimum logger initialization MUST attempt exactly one `invocation-start` event and exactly one terminal `invocation-complete` event; process interruption MAY leave only the start event. |
| R2 | The CLI MUST classify each invocation into exactly one closed command family: `lifecycle`, `repository-setup`, `introspection`, `log-inspection`, or `invalid-input`; an unclassified new public command MUST fail conformance before release. |
| R3 | File event severity MUST be exactly `debug`, `info`, `warning`, or `error`; the default file threshold MUST be `info` and the default console threshold MUST be `error`. |
| R4 | Successful and ordinary blocked operations MUST produce no console event at the default threshold; blocked or expected policy rejection MUST be recorded at `warning`, and unexpected internal, unsafe recovery, or logging failures MUST be `error`. |
| R5 | Every file event MUST use log schema version `1` and the common fields `schema_version`, `event`, `timestamp`, `invocation_id`, `severity`, `command_family`, `command`, `cli_version`, and `sequence`; completion events MUST additionally include `status`, `exit_code`, and `duration_ms`. |
| R6 | Invocation IDs MUST match `^[0-9a-f]{16}$`, MUST be generated independently for every process invocation, and MUST NOT be derived from request, repository, artifact, environment, or user data. |
| R7 | Event extensions MUST be allowlisted by command family. Lifecycle extensions MAY include normalized operation, change ID, stage, prior/resulting lifecycle revisions, state-changed boolean, stable diagnostic codes, finding IDs, and milestone IDs. Other families MUST NOT inherit lifecycle-only fields. |
| R8 | Logs MUST NOT contain raw argv, raw requests, artifact contents, request hashes or fingerprints, credentials, secrets, arbitrary environment values, Git remote URLs, usernames, hostnames, stack traces at info or warning, or machine-local absolute repository paths. |
| R9 | String event fields MUST reject or normalize newline and control characters, and each encoded event MUST be no larger than 16 KiB. An oversized event MUST be replaced by a bounded error event that contains no truncated sensitive value. |
| R10 | The default log directory MUST be outside the repository in the platform user-state location: `$XDG_STATE_HOME/rigorloop/logs` or `~/.local/state/rigorloop/logs` on Linux, `~/Library/Logs/RigorLoop` on macOS, and `%LOCALAPPDATA%\\RigorLoop\\Logs` on Windows. |
| R11 | A `RIGORLOOP_LOG_DIR` override MUST resolve to an absolute directory and becomes the containment root for the five owned log names and rotation lock. The root and every existing component from the nearest existing ancestor to that root MUST NOT be a symlink; owned operations MUST remain beneath the resolved root, and events MUST NOT record its absolute path. |
| R12 | Newly created log directories and files MUST use the most restrictive permissions available to the current user; on POSIX the target modes MUST be `0700` for directories and `0600` for files. The CLI MUST NOT broaden, narrow, or otherwise repair permissions on a pre-existing entry. Broader access on a pre-existing root or owned file MUST produce degraded observability with `RL_LOG_UNSAFE_PATH`. |
| R13 | The active log file MUST rotate before an append that would exceed 5 MiB, MUST retain at most four archives plus the active file, and MUST never delete or rename a path outside the resolved log directory. |
| R14 | Append and rotation MUST preserve complete JSON Lines records under supported concurrent writers. Lock acquisition MUST use at most 10 attempts and 1,000 milliseconds total per event. Exhaustion or a stale lock MUST degrade observability rather than block longer, remove an unowned lock, or corrupt an event. |
| R15 | Logging availability, rotation, lookup, or configuration failure MUST NOT change semantic command behavior, repository bytes, transaction recovery, or semantic exit code. Unless the caller explicitly selected console level `off`, a logging failure MUST emit exactly one non-recursive bounded `RL_LOG_UNAVAILABLE` stderr diagnostic per invocation; `off` MUST suppress it. A new structured projection MUST still report `observability: degraded`. |
| R16 | File logging MUST be enabled by default and MAY be disabled per invocation with `--no-file-log` or `RIGORLOOP_FILE_LOG=off`; disabling logging MUST NOT alter stdout or the semantic exit code. |
| R17 | `--file-log-level` and `RIGORLOOP_FILE_LOG_LEVEL` MUST accept only the four severity values; `--console-log-level` and `RIGORLOOP_CONSOLE_LOG_LEVEL` MUST accept those values plus `off`. CLI options MUST override environment configuration. Unknown values MUST fail closed before dispatch without recording raw input. |
| R18 | `rigorloop logs path` MUST return the resolved log directory in human or JSON form without creating governed state; failure MUST use a stable diagnostic and MUST NOT expose unrelated environment values. |
| R19 | `rigorloop logs show <invocation-id>` MUST validate the exact ID grammar, search only the active file and retained archives, return events only for that ID, and distinguish `RL_LOG_NOT_FOUND`, `RL_LOG_UNAVAILABLE`, and `RL_LOG_CORRUPT_ENTRY`. `RL_LOG_NOT_FOUND` covers both IDs never recorded and IDs no longer retained; the first release MUST NOT claim which case occurred. |
| R20 | Log inspection MUST be read-only, MUST NOT rerun or reconstruct the original command, MUST NOT recursively include its own diagnostic events in the lookup result, and MUST preserve corrupt unrelated lines as warnings without returning their raw content. |
| R21 | During v0.4.x, existing default human output, `--json`, and lifecycle `--format json` schemas and whitespace-independent semantics MUST remain compatible. |
| R22 | The compatibility slice MUST add `--format concise-human`, `--format concise-json`, and `--format detailed-json` to the common renderer. Existing `--json` MUST remain an alias for the existing detailed JSON contract through v0.4.x. |
| R23 | Concise JSON MUST use result schema version `2`, identify `projection: concise`, use compact JSON encoding, omit null and empty optional fields, and include only applicable fields from the closed common set: `schema_version`, `projection`, `invocation_id`, `command`, `operation`, `status`, `exit_code`, `change_id`, `lifecycle_revision`, `state_changed`, `next_operation`, `codes`, `finding_ids`, `milestone_ids`, and `observability`. |
| R24 | Every concise-human terminal result MUST contain at most two non-empty lines and MUST include the operation or command, outcome, relevant identity, stable code when present, safe next operation when deterministically known, and invocation ID. Help text, shell completion, version text, and explicit detailed or log-event-list projections are not concise-human terminal results. |
| R25 | A concise result MUST contain every fact required to select the next safe operation without log lookup. Complete artifact inventories, supporting paths, repeated explanations, stack traces, and empty collections MUST be omitted. |
| R26 | Detailed JSON MUST preserve the current complete result semantics and remain available as `--format detailed-json` throughout v0.5.x; removing it before v0.6.0 requires a separate approved compatibility decision. |
| R27 | Concise and detailed projections of one internal result MUST agree on every shared semantic fact, state mutation, stable code, and exit status. No result may be duplicated as a console event. |
| R28 | New projections MUST include `observability: recorded`, `degraded`, or `disabled`; this field is diagnostic only and MUST NOT be interpreted as semantic command status or lifecycle evidence. Existing v0.4.x projections need not add it. |
| R29 | `packages/rigorloop/test/fixtures/observability/token-profiles-v1.json` MUST own exactly six named profiles: `status`, `context`, `mutation-success`, `mutation-blocked`, `validation-failure`, and `unexpected-error`. `docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json` MUST record the same fixtures against existing v0.4.x output. Each measurement MUST count normalized agent-facing UTF-8 bytes from stdout and stderr plus every lookup or detailed projection required to complete the task. |
| R30 | Concise defaults MAY replace existing defaults no earlier than v0.5.0 and only when the unweighted median of the six per-profile percentage reductions from the R29 baseline is at least 30%, no profile's complete-interaction bytes grow by more than 10%, every required field in the concise applicability matrix remains present, and `status`, `context`, `mutation-success`, and `mutation-blocked` require no lookup. Missing, renamed, added, or changed fixtures create a new benchmark version and baseline rather than silently altering v1. Otherwise concise projections MUST remain opt-in. |
| R31 | The repository-owned wrapper `scripts/validate-governed-lifecycle-cli.py` MUST preserve each child lifecycle command's semantic exit classification and MUST consume structured stdout without printing a successful child's stdout a second time. Other Python CLI callers in tests or measurement tooling are not production wrappers in this release. Hosted CI retention and forwarding are outside this specification. |
| R32 | A fresh repository checkout MUST reconstruct governed lifecycle state without logs, and no log event, log configuration, lookup result, or observability status may authorize or settle a governed operation. |
| R33 | Event timestamps MUST be UTC RFC3339 with millisecond precision; duration MUST use a monotonic source and MUST be a non-negative integer number of milliseconds. Timestamp or duration failure MUST degrade only the affected diagnostic event. |
| R34 | Logging work on the ordinary non-rotation path MUST be bounded to directory validation plus two event appends; lookup MUST scan only the active file and four retained archives. No daemon, database, network request, or unbounded directory traversal is permitted. |

## Inputs and outputs

### Configuration inputs

| Input | Values | Default | Ownership |
| --- | --- | --- | --- |
| `--file-log-level` / `RIGORLOOP_FILE_LOG_LEVEL` | `debug`, `info`, `warning`, `error` | `info` | Diagnostic file sink only |
| `--console-log-level` / `RIGORLOOP_CONSOLE_LOG_LEVEL` | `debug`, `info`, `warning`, `error`, `off` | `error` | Diagnostic stderr sink only |
| `--no-file-log` / `RIGORLOOP_FILE_LOG` | flag / `on`, `off` | `on` | Diagnostic file sink only |
| `RIGORLOOP_LOG_DIR` | safe absolute directory | platform default | Diagnostic file sink only |
| `--format` | existing formats plus `concise-human`, `concise-json`, `detailed-json` | existing v0.4.x default | Result renderer only |

### Log events

The active file is `rigorloop.jsonl`; archives are `rigorloop.1.jsonl` through `rigorloop.4.jsonl`. Sequence is `1` for start and `2` for completion. A start event has `event: invocation-start`; a completion event has `event: invocation-complete`.

Unknown fields in log schema version 1 are rejected by repository conformance fixtures. Readers may skip a whole event with a newer unsupported schema version and report it as unavailable; they must not partially interpret it.

### Result channels

- Semantic human or JSON results use stdout.
- Console events meeting the threshold use stderr.
- File events use the local JSON Lines sink.
- Logging diagnostics never replace or wrap the semantic exit status.

### Concise JSON field applicability

The table is exhaustive for result schema version 2. “Required when” means the field is omitted in every other case; an applicable empty collection is also omitted.

| Field | Required when |
| --- | --- |
| `schema_version`, `projection`, `invocation_id`, `command`, `status`, `exit_code`, `observability` | Every concise JSON terminal result. |
| `operation` | The dispatched command has a named subcommand or lifecycle operation. |
| `change_id` | Exactly one governed change was selected for the result. |
| `lifecycle_revision` | The result read or attempted to mutate a selected governed change and a current revision is safely available. |
| `state_changed` | A governed mutating operation reached transition evaluation; it is `true` only when repository lifecycle bytes changed. |
| `next_operation` | The transition engine returns exactly one deterministically permitted corrective or continuation operation. |
| `codes` | One or more stable warning, blocker, or error codes apply. |
| `finding_ids` | One or more findings cause or explain the result. |
| `milestone_ids` | One or more milestones cause, explain, or are changed by the result. |

The detailed and concise renderers consume the same internal result. A field omitted by this matrix is not permission to discard that fact from the detailed projection.

## State and invariants

- Git-tracked artifacts remain the only durable governed lifecycle truth.
- An invocation ID correlates events but grants no authority.
- One invocation has at most one start and one completion event in the active retained set.
- Rotation owns only the five named files and its bounded lock inside the validated directory.
- Result projection is a pure representation of one internal semantic result.
- Logging failure is non-semantic and cannot roll back or approve a command.
- Existing detailed results remain sufficient without access to local logs.

## Error and boundary behavior

| Code | Condition | Semantic effect | Diagnostic behavior |
| --- | --- | --- | --- |
| `RL_LOG_UNAVAILABLE` | Directory, permission, append, lock, rotation, or disk failure | None | One bounded stderr error; new projections report `degraded`. |
| `RL_LOG_NOT_FOUND` | A valid invocation ID is absent from all five retained log files | Lookup command fails | No guessed history, expiry claim, result reconstruction, or rerun. |
| `RL_LOG_CORRUPT_ENTRY` | A retained line is invalid JSON or violates schema | Lookup warns or fails if the requested event is affected | Raw corrupt bytes are not returned. |
| `RL_LOG_UNSAFE_PATH` | Override or existing path escapes, contains a symlink, or violates containment | Logging degrades; `logs path` fails | No fallback to repository or current directory. |
| `RL_INVALID_LOG_LEVEL` | A threshold value is outside the closed vocabulary | Command fails before dispatch | Only normalized code and safely recognized command family may be logged. |

Failures before minimum logger initialization are not file-observable. They may produce one bounded stderr diagnostic when the process can render safely, but no requirement permits raw argv or environment capture.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R2, R6, R7, R8, R9, R11, R15, R17, R18, R19, R20 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R1, R13, R14, R15, R16, R18, R19, R20, R28, R32 | BND-STATE-001 | - |
| identity-authority | applicable | R6, R7, R8, R11, R15, R18, R19, R20, R28, R32 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R5, R15, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R1, R13, R14, R15, R19, R33 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R9, R13, R14, R15, R19, R20, R32, R33 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | BND-COMPAT-001 | - |
| external-environment | applicable | R8, R10, R11, R12, R13, R14, R15, R16, R21, R22, R27, R31, R34 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R2, R6, R7, R8, R9, R11, R15, R17, R18, R19, R20 | known/unknown family; valid/invalid ID; valid/unknown level; safe/unsafe string | Closed vocabularies fail before family-specific interpretation; private input is never persisted. | Valid inputs proceed; invalid inputs return stable codes without raw capture. | R2 |
| BND-STATE-001 | state-lifecycle | R1, R13, R14, R15, R16, R18, R19, R20, R28, R32 | enabled/disabled/degraded; retained/missing/corrupt; start-only/complete | Diagnostic state never becomes lifecycle state or authority. | Operations preserve semantic results; lookup reports only a provable retained-state partition. | R15 |
| BND-AUTH-001 | identity-authority | R6, R7, R8, R11, R15, R18, R19, R20, R28, R32 | random invocation ID; exact lookup ID; semantic repository identity; prohibited private identity | Correlation identities do not authorize operations and contain no derived request identity. | Exact IDs retrieve allowlisted diagnostics only; authority crossings fail. | R32 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R5, R15, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | stdout/stderr/file; human/concise JSON/detailed JSON; direct/wrapper | One semantic result owns stdout and exit status; sinks and projectors cannot duplicate or alter it. | Shared facts agree; console threshold and wrapper paths preserve single emission. | R27 |
| BND-TEMPORAL-001 | temporal-retry | R1, R13, R14, R15, R19, R33 | concurrent append; competing rotation; stale lock; interruption; repeated lookup | Events remain complete and bounded; interruption may omit only completion. | Safe append/rotation succeeds or observability degrades without blocking indefinitely. | R14 |
| BND-RECOVERY-001 | failure-recovery | R9, R13, R14, R15, R19, R20, R32, R33 | permission denied; disk full; corrupt line; oversized event; clock failure | Recovery never changes repository bytes or returns unsafe raw content. | One bounded diagnostic, safe lookup outcome, or skipped event; semantic result remains authoritative. | R15 |
| BND-COMPAT-001 | compatibility-migration | R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31 | v0.4.x existing defaults; opt-in projections; v0.5.0 adoption pass/fail; v0.6.0 removal decision | Existing schemas remain stable during their window; adoption needs measured proof. | Gates pass and defaults may change, or fail and opt-in behavior remains. | R30 |
| BND-ENV-001 | external-environment | R8, R10, R11, R12, R13, R14, R15, R16, R21, R22, R27, R31, R34 | Linux/macOS/Windows; safe/unsafe override; direct/wrapper; writable/unwritable filesystem | Logs stay outside the repository, under user control, with bounded resources and no network. | Supported environment records safely; unsafe or unavailable environment degrades only diagnostics. | R10 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R8, R11, R15 | BND-INPUT-001, BND-AUTH-001, BND-ENV-001 | An unsafe override contains private path data while logging fails. | Reject the path without recording it and preserve the semantic command result. |
| INT-002 | R13, R14, R15 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | Two writers rotate while one append fails or a lock becomes stale. | No partial JSON line or external deletion occurs; affected invocations report degraded observability. |
| INT-003 | R21, R22, R27, R31 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | A wrapper consumes concise JSON while legacy consumers still expect detailed JSON. | Explicit formats remain deterministic, exit codes match, and no wrapper duplicates stdout. |
| INT-004 | R19, R20, R32 | BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001 | Lookup encounters an exact event plus corrupt unrelated retained lines. | Return only validated exact-ID events with a bounded warning and no reconstruction or authority claim. |
| INT-005 | R29, R30 | BND-COMPOSE-001, BND-COMPAT-001 | Concision saves initial bytes but forces extra lookup for the next action. | Count the lookup in the profile; adoption fails if one-pass continuation or byte gates fail. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R1, R3, R4, R5, R21 | BND-COMPOSE-001 | - | - |
| E2 | regression | R23, R25, R27 | BND-COMPOSE-001, BND-COMPAT-001 | proposal-revision-deadlock | - |
| E3 | illustration | R3, R4, R5 | BND-COMPOSE-001 | - | - |
| E4 | illustration | R15, R28, R32 | BND-STATE-001 | - | - |
| E5 | illustration | R18, R19, R20 | BND-STATE-001 | - | - |
| E6 | illustration | R13, R14, R15 | BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | - | - |
| E7 | illustration | R29, R30 | BND-COMPAT-001 | - | - |

## Compatibility and migration

The v0.4.x slice is additive. Existing human defaults and JSON aliases remain unchanged, while explicit concise and detailed formats are added. Log schema version 1 is independent of result schema versions. No repository migration is required because logs and configuration remain machine-local.

At v0.5.0, changing defaults requires all R30 gates and a release-visible compatibility note. `detailed-json` remains available through v0.5.x. Existing logs remain readable by schema-version-aware lookup, but logs are disposable diagnostics and require no durable migration. Rollback disables the file sink and restores existing default projections independently.

## Observability

This feature is itself the observability contract. Validation must prove event shape, severity, thresholds, single emission, correlation, lookup outcomes, rotation bounds, degraded behavior, and privacy. No hosted telemetry, metric backend, or CI retention is implied.

## Security and privacy

The event model is allowlist-only. Values outside an explicitly admitted semantic field are never serialized and are not made safe merely by hashing or truncation. Directory containment and symlink refusal occur before file creation or rotation. Log inspection never returns raw corrupt lines. Test fixtures must use synthetic secrets and paths and must prove absence from stdout, stderr, active logs, archives, and lookup results.

Invocation IDs are correlation labels, not authentication tokens. The first release assumes the local user can read their own logs and does not defend against a malicious user with unrestricted filesystem authority.

## Accessibility and UX

No graphical interface is introduced. Human output must preserve meaning without color, keep codes and next actions in text, and remain understandable when stderr is captured separately. The two-line budget applies to ordinary concise outcomes, not to help text or explicit detailed output.

## Performance expectations

The ordinary path is bounded by R34 and the 16 KiB event limit. Rotation and lookup operate over five fixed names rather than an unbounded directory scan. Performance tests should report append and lookup timings but must not use environment-sensitive wall-clock thresholds as the sole correctness gate.

## Edge cases

EC1. A process terminates after start append: the start event remains valid and lookup reports no invented completion.

EC2. The event would cross 16 KiB: a bounded error event replaces it without including a substring of the rejected value.

EC3. The log directory is a symlink or contains a symlink component: logging degrades with `RL_LOG_UNSAFE_PATH`; no fallback file is created.

EC4. The disk becomes full during rotation: named files outside the resolved directory are untouched and the semantic command result is preserved.

EC5. A valid ID was removed by rotation: lookup returns `RL_LOG_NOT_FOUND` and does not claim whether the ID never existed or is no longer retained.

EC6. `--console-log-level off` and file logging remain enabled: stderr is quiet and searchable file events remain.

EC7. `--no-file-log` and console threshold error are combined: no file is created, ordinary success is quiet, and new projections report disabled observability.

EC8. An unknown command reaches initialization: it records the invalid-input family with a stable parser code and no raw token beyond a safely normalized recognized command name.

EC9. Logger initialization itself fails: no file-observability claim is made and one safe stderr diagnostic is permitted.

EC10. A newer log schema appears in an archive: the reader reports the unsupported event without partially interpreting it.

EC11. A detailed projection is requested while logging is unavailable: complete semantic detail remains available and the exit code is unchanged.

EC12. A new command is added without an event family: conformance validation fails before release.

## Non-goals

- Hosted CI retention, forwarding, telemetry, aggregation, search, or tailing.
- A repository execution ledger or use of logs as review, approval, settlement, or verification evidence.
- A daemon, database, control plane, remote service, or network dependency.
- Automatic default adoption before the compatibility and measurement gates pass.
- Removal of the detailed projection in this change.
- Recording raw or derived request identity.
- Changing lifecycle operations, state transitions, workflow routing, or transaction semantics.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every command family and invalid-input partition has start/completion, threshold, schema, and privacy proof. |
| AC2 | Default file info and console error behavior is deterministic across success, blocked, invalid, and internal-error outcomes. |
| AC3 | Active plus four archives never exceeds five owned log files, records remain complete under concurrency, and unsafe paths never mutate. |
| AC4 | Logging enabled, disabled, degraded, rotated, or corrupt does not change semantic stdout, repository diff, or exit code. |
| AC5 | Exact path discovery and lookup distinguish found, missing, unavailable, and corrupt outcomes without guessed history or rerun. |
| AC6 | Existing v0.4.x output contracts pass unchanged; explicit concise and detailed projections agree on shared facts. |
| AC7 | Concise output preserves the complete continuation-critical set and meets the human and machine shape contracts. |
| AC8 | Synthetic secret, request, environment, control-character, and absolute-path fixtures are absent from every output and retained log surface. |
| AC9 | Representative complete-interaction measurements enforce the 30% median, 10% per-profile, and one-pass continuation gates before any default change. |
| AC10 | Direct, agent, and local wrapper paths preserve one semantic result and do not duplicate successful output. |
| AC11 | A fresh checkout reconstructs lifecycle state without local logs, and no observability field authorizes a transition. |

## Open questions

None. Architecture owns the internal component decomposition and locking mechanism but may not change these observable outcomes, limits, compatibility windows, or authority boundaries.

## Next artifacts

- Independent specification review.
- Architecture assessment and architecture/ADR work because machine-local persistence, cross-process rotation, and shared result projection alter long-lived component boundaries.
- Execution plan and test specification after architecture settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for spec-review.
