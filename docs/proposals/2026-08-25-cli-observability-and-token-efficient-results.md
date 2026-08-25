# Local CLI Observability and Token-Efficient Results

## Owning change record

This proposal is owned by [change.yaml](../changes/2026-08-25-cli-observability-token-efficient-results/change.yaml). It is a separate follow-up and does not modify or extend the lifecycle state of `2026-08-24-governed-lifecycle-cli` or PR #155. The earlier recording-only root preserves proposal-review-r1 evidence but does not own this proposal's lifecycle.

## Problem

The governed lifecycle CLI can report the operation and result of its current invocation, but it does not retain a searchable machine-local execution history. Successful child output is commonly captured by wrappers, so later inspection cannot reliably answer which lifecycle command ran, which change and revision it targeted, or why it completed, blocked, or failed.

At the same time, returning complete artifact inventories and detailed diagnostics on every invocation increases agent context consumption. Printing more diagnostic detail to solve observability would make the token problem worse and would mix user-facing results with operational evidence.

RigorLoop needs two deliberately separate surfaces: concise results containing only facts required to understand or continue an operation, and bounded machine-local logs containing searchable execution evidence.

## Goals

- Record a structured machine-local log by default for every CLI invocation that reaches minimum logger initialization, including privacy-bounded invalid input, without changing governed repository state.
- Support the closed severity levels `debug`, `info`, `warning`, and `error`, with a default file threshold of `info` and console threshold of `error`.
- Rotate logs within a bounded storage budget and make their location discoverable.
- Correlate command start and completion, including interrupted invocations, through a short invocation identifier.
- Keep default human and machine results useful, deterministic, and materially smaller than detailed diagnostic output.
- Let callers retrieve the recorded allowlisted diagnostics for an invocation without rerunning a mutation, while retaining an explicit detailed result projection when complete operation output is required at execution time.
- Preserve exit codes, transaction behavior, repository diffs, and Git-contained lifecycle truth independently of logging availability.

## Non-goals

- Treat logs as governed lifecycle truth, approval evidence, or an authorization boundary.
- Write logs, logging configuration, or execution history into the repository or `change.yaml`.
- Introduce hosted telemetry, remote collection, a daemon, a database, or a control plane.
- Record request bodies, artifact contents, secrets, credentials, arbitrary environment values, absolute repository paths, or raw command arguments.
- Infer semantic approval, perform workflow routing, invoke agents, or change lifecycle operations.
- Build a general log analytics product. Initial discovery and lookup should remain narrow.
- Remove information required to identify a blocker, preserve authority, or safely perform the next operation merely to meet a size target.

## Vision fit

fits the current vision

The direction improves inspectability and agent ergonomics while keeping Git-tracked artifacts authoritative and avoiding a hosted runtime. Machine-local logs diagnose execution; durable engineering decisions and evidence remain reviewable repository artifacts.

## Context

The governed lifecycle CLI already separates semantic operations from lifecycle field mutation and returns stable human and JSON results. The current specification requires a broad machine envelope and equivalent human facts, while operation-specific context is intended to contain only facts needed by the requested stage.

The accepted design direction adds a third concern that should not be conflated with either result representation:

```text
stdout   concise operation result
stderr   console messages at the configured threshold
log file structured machine-local execution history
```

The user selected default recording, rotation, four severity levels, an `error` console default, and token-friendly standard output. This proposal refines those choices into a product boundary without specifying implementation tasks.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Observe which lifecycle CLI command executed | in scope | Goals, Recommended Direction, Expected Behavior Changes |
| Keep execution records in logs rather than governed repository artifacts | in scope | Non-goals, Recommended Direction |
| Record logs by default and rotate them | in scope | Goals, Recommended Direction, Rollout and Rollback |
| Support debug, info, warning, and error levels | in scope | Goals, Expected Behavior Changes |
| Print only errors at the default console threshold | in scope | Recommended Direction, Expected Behavior Changes |
| Keep stdout useful and short for agents | in scope | Problem, Recommended Direction, Testing and Verification Strategy |
| Retrieve fuller diagnostics only when needed | in scope | Recommended Direction, Expected Behavior Changes |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Structured machine-local JSON Lines logging | core to this proposal | It provides the searchable execution history requested by the user. |
| Severity classification and independent file/console thresholds | core to this proposal | Default recording and quiet console behavior require separate controls. |
| Size-bounded rotation and retention | same-slice dependency | Default recording is unsafe without a bounded disk policy. |
| Concise default human and JSON results | core to this proposal | Token reduction is a primary user outcome, not incidental formatting. |
| Detailed on-demand result projection | same-slice dependency | Concise defaults must not make complete diagnostics unavailable. |
| Invocation correlation, log-path discovery, and single-invocation lookup | same-slice dependency | Concise defaults cannot promise safe detail recovery without a deterministic read-only retrieval path. |
| CI retention or forwarding of CLI log events | separate proposal | The first release promises machine-local observability only. [FU-011](../follow-ups.md#open-follow-ups) reserves ownership for a future proposal without approving that work; this proposal requires only a forward-compatible local schema. |
| Agent token baseline and post-change measurement | same-slice dependency | Measurement is an adoption gate for concise defaults, not a post-release justification. |
| Hosted telemetry or centralized aggregation | out of scope | It conflicts with the local, Git-first product boundary and is unnecessary for command observability. |
| Repository-tracked execution ledger | rejected option | It would mix diagnostic history with governed durable truth and create high-churn diffs. |

## Options Considered

### O1: Print complete diagnostics to stdout or stderr

This makes execution immediately visible and requires no persistent sink. It increases agent tokens, creates noisy CI output, conflates results with diagnostics, and still loses history after output capture. Reject.

### O2: Record rotating machine-local logs and return concise results

Every invocation writes structured start and completion events to a bounded per-user log directory. Standard output contains only continuation-critical facts, console logging defaults to errors, and detailed results or invocation lookup remain explicit. This preserves local observability without changing governed truth and directly addresses token consumption. Select.

### O3: Store an execution ledger in the repository

Git would make history durable and reviewable, but routine reads and rejected operations would create repository churn, branch conflicts, privacy concerns, and a misleading second lifecycle authority. Reject.

### O4: Send logs to a hosted telemetry service

Central collection could improve fleet-wide search and retention. It introduces networking, authentication, privacy, availability, hosting, and organizational governance beyond the local CLI's intended boundary. Reject.

## Recommended Direction

Choose O2: add an internal observability pipeline with three independent outputs.

```text
lifecycle execution
      |
      +-- result projector --> concise stdout
      |
      +-- console sink -----> stderr at error by default
      |
      +-- file sink --------> rotating JSON Lines at info by default
```

The file sink records command start and completion using a versioned log schema and short invocation ID. Start records identify the normalized semantic command, operation, change, stage when applicable, dry-run state, and CLI version. Completion records identify status, exit code, prior and resulting lifecycle revisions, stable diagnostic codes, relevant finding or milestone IDs, and duration. The first release records no request digest or other persistent request fingerprint.

Every supported public command uses a small common event envelope. Command-family extensions add only allowlisted fields that have defined meaning for that family.

| Command family | Initial commands | Default event treatment |
| --- | --- | --- |
| Lifecycle | `lifecycle status`, `context`, `validate`, and governed operations | Common envelope plus allowlisted change, operation, stage, revision, blocker, finding, and milestone fields. |
| Repository setup | `init` and `new-change` | Common envelope plus non-sensitive target and outcome fields; no raw arguments or absolute paths. |
| Introspection | `version` and help | Common envelope only. |
| Log inspection | log-path discovery and single-invocation lookup | Common envelope plus the validated lookup target ID; lookup remains read-only and does not recursively expand its own event. |
| Invalid input | malformed arguments, unknown commands or operations, and incomplete requests that reach minimum logger initialization | Common envelope plus a safely normalized command token when recognized and a stable parser or request error code; never raw arguments or request fields. |

A new public command cannot ship until it is assigned to exactly one command family with an allowlisted event shape and privacy tests. Unknown command families fail conformance rather than silently inheriting lifecycle fields.

Minimum logger initialization occurs after the process has resolved a safe logging configuration and invocation ID but before command-family dispatch or request parsing. Invocations reaching that boundary receive best-effort start and completion events even when dispatch or parsing fails. Failures before that boundary, including process startup failure, unsafe log-directory resolution, or inability to initialize the logger, are explicitly unobservable in the file and receive only the bounded non-semantic console failure described below. This is the complete applicability boundary; the implementation must not recover observability by recording raw `argv` or request data.

The logger never records raw request data, artifact content, raw `argv`, arbitrary environment values, credentials, Git remote URLs, or absolute repository paths. Repository-relative semantic paths should appear only when necessary and explicitly admitted by the log schema.

File and console thresholds are independent. The default file threshold is `info`, so successful command start and completion are searchable. The default console threshold is `error`, so expected governance rejections remain in the file as `warning` without consuming terminal or agent context. Unexpected internal failures, unsafe recovery conditions, and logging failures are `error`. Debug events cover bounded parser, discovery, and invariant-evaluation detail and are opt-in.

Concise results retain operation, outcome, change or target identity when needed, the lifecycle revision required for continuation, stable blocker or error codes, relevant finding or milestone IDs, whether state changed, the deterministically known next operation, and the invocation reference. Complete inventories, supporting paths, expanded explanations, and full blocker sets move behind an explicit detailed projection.

Human success should normally fit within two short lines. Blocked and error output should lead with the operation, stable code, relevant identity, safe next action, and invocation reference. Machine results should use compact JSON encoding and omit facts irrelevant to the requested operation while retaining a versioned schema and deterministic field meanings. Size objectives are expressed as character and field budgets rather than a model-specific tokenizer contract.

Compatibility changes occur in two stages. A v0.4.x compatibility release preserves the current default human result and current `--format json` result schema. It adds an explicit concise human projection, `--format concise-json`, and `--format detailed-json` as the durable detailed alias. The concise machine projection uses a new result-schema version and identifies `projection: concise`; the existing detailed envelope retains its current schema during the transition. If compatibility and measurement gates pass, v0.5.0 may make concise human output and concise JSON the defaults. At that boundary, `--format json` maps to the versioned concise schema while `--format detailed-json` remains supported throughout v0.5.x and can be removed no earlier than v0.6.0 through a separate compatibility decision. Output channels retain one owner: semantic results use stdout, console log events meeting the threshold use stderr, and no result is duplicated as a console event.

A narrow read-only discovery surface is a same-slice dependency of concise-default adoption. It exposes the resolved log directory and retrieves the recorded allowlisted events and diagnostics for one validated invocation ID across the bounded current and rotated set. Lookup distinguishes not found, expired, unavailable, and corrupt-entry outcomes; it never claims to reconstruct fields that were not admitted to the log schema and never reruns the original operation. Callers that require the complete detailed result select that projection when executing the original command. Search, aggregation, and tailing beyond those operations remain external-tool responsibilities for the first release.

Logging is diagnostic, not transactional authority. Lifecycle execution remains correct when logging is unavailable. A logging failure produces one bounded console error without recursive logging, never causes a partial lifecycle mutation, and never changes the semantic operation result or exit code. The downstream specification should decide whether an inability to write the initial start event is merely degraded observability or is reported through a separate non-semantic process status.

## Expected Behavior Changes

- Every CLI invocation reaching minimum logger initialization attempts to append one common structured start event and one completion event to a machine-local log by default, with only its command family's allowlisted extension fields; safely recognized invalid input uses the `invalid-input` family.
- Failures before minimum logger initialization are not claimed as file-observable and produce no fallback capture of raw arguments or request data.
- An interrupted invocation may have a start event without a completion event and remains searchable by invocation ID.
- Successful and blocked operations produce no console log at the default `error` threshold.
- Blocked operations are recorded at `warning`; unexpected internal or recovery failures are recorded at `error`.
- The compatibility release keeps current default output and adds explicit concise human and machine projections.
- A declared breaking release may adopt concise defaults only after the compatibility and measurement gates pass; the detailed projection remains available through its announced window.
- Concise results expose a short log reference so humans and agents can inspect detail without rerunning a mutation.
- Read-only log-path discovery and exact single-invocation lookup ship before concise output can become the default.
- Logs rotate within a bounded size and retained-file count in a platform-appropriate per-user state directory outside the repository.
- Logging configuration comes from CLI options or narrowly named environment configuration, never governed lifecycle state.
- Existing exit codes, lifecycle revisions, atomic mutation behavior, and repository diffs do not depend on log success.

## Architecture Impact

Architecture assessment is required. The proposal introduces machine-local persistence, cross-process append and rotation behavior, a public output-projection boundary, a versioned log schema, privacy controls, and local wrapper integration.

Downstream architecture should decide:

- the platform-specific state-directory resolver and safe override rules;
- whether the standard Node runtime is sufficient for bounded rotation or a reviewed dependency is justified;
- append atomicity, rotation locking, stale-lock handling, and behavior across Windows, macOS, and Linux;
- file and directory permissions, symlink refusal, path containment, and disk-full behavior;
- event correlation, timestamp and duration sources, event-size limits, and crash semantics;
- the exact boundary among the internal lifecycle result, concise and detailed projectors, console sink, and file sink;
- how local Python wrappers preserve semantic results without printing successful child output wholesale, while the local event schema remains forward-compatible for a separately proposed CI retention design;
- compatibility treatment for consumers of the current broad JSON envelope and pretty-printed encoding.

Machine-local logs cannot become necessary to reconstruct effective lifecycle state. A fresh checkout remains sufficient for governed status, while logs provide only execution diagnostics for the machine on which commands ran.

## Testing and Verification Strategy

Use contract tests for every severity, threshold, result projection, log event, and failure boundary. Logging disabled by configuration, default info recording, default error console output, explicit debug recording, warning-only file output, and error propagation should each have direct fixtures.

Output tests should compare stdout and exit codes with logging available, unavailable, rotated, and disabled. Concise results must retain all continuation-critical facts and omit complete inventories, repeated explanations, empty structures, absolute paths, and stack traces. Detailed results must remain semantically equivalent to concise results while adding diagnostics. JSON should remain parseable and stable without relying on whitespace.

Rotation tests should cover the size boundary, retained-file count, concurrent writers, a competing rotation, a stale rotation lock, permission denial, disk exhaustion, unsafe symlinks, path escape, and interruption between start and completion. Security fixtures should include representative secrets, credential-bearing URLs, absolute paths, raw requests, request equality probes, low-entropy request values, newlines, and control characters and prove they do not appear in logs or concise output. Invalid-input fixtures should cover unknown commands, malformed arguments, incomplete requests, dispatch failures, and failures before minimum logger initialization without capturing raw arguments.

First-release integration tests should prove that direct human invocation, agent invocation, and local Python validation wrappers preserve the same semantic result without printing successful child output wholesale. Hosted-runner retention and forwarding are not first-release claims; [FU-011](../follow-ups.md#open-follow-ups) owns the separate proposal for that contract, privacy proof, and delivery decision.

Measure representative `status`, `context`, successful mutation, blocked mutation, validation failure, and unexpected-error interactions against the current merged CLI before changing defaults. Normalized agent-facing bytes are the deterministic primary measure; a documented tokenizer estimate is secondary evidence. The measure includes every follow-up log lookup needed to complete the task so the design cannot claim savings by forcing repeated commands.

Concise-default adoption requires at least a 30% reduction in median agent-facing bytes across the representative profiles, no profile regression greater than 10%, and complete preservation of the operation-specific continuation-critical field set. An ordinary success or expected blocked result must not require lookup to determine the next safe action. If any gate fails, concise projections remain opt-in and the current defaults remain unchanged.

## Rollout and Rollback

Roll out in compatibility-aware slices:

1. Specify severity semantics, log schema, redaction, storage defaults, rotation, output projections, lookup behavior, and compatibility guarantees.
2. Implement the internal logger and rotating file sink while preserving existing stdout projection; observe logging reliability before changing result defaults.
3. Add concise and detailed result projectors, invocation references, log-path discovery, and exact single-invocation lookup after parity tests pass.
4. Measure complete representative interactions and retain concise output as opt-in unless every adoption gate passes.
5. Change defaults only at the declared compatibility boundary; adjust only presentation budgets, not semantic facts or lifecycle authority.
6. Leave hosted CI retention and forwarding untouched; evaluate them only through the separate proposal reserved by [FU-011](../follow-ups.md#open-follow-ups).

Before concise output becomes default, rollback disables the new projection and file sink independently. After adoption, a compatibility release can restore the prior detailed default while retaining readable log files. Rotation never deletes files outside the resolved log directory, and rollback never treats log history as lifecycle evidence requiring migration.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Default logging leaks sensitive data | Use an allowlisted event schema, prohibit raw requests and environment values, sanitize strings, test redaction, and create private directories and files. |
| Persistent request fingerprints leak equality or guessed low-entropy values | Record no request digest or derived request fingerprint in the first release; correlate events only with the random invocation ID and explicitly allowlisted semantic identity fields. |
| Logs consume unbounded disk | Rotate by size, retain a fixed archive count, bound event size, and fail safely when storage is unavailable. |
| Concurrent CLI processes corrupt or lose records | Use one-event append writes, a bounded rotation protocol, concurrency tests, and explicit degraded-observability behavior. |
| Logging failure changes lifecycle behavior | Keep logging outside the transaction authority, preserve semantic results and exit codes, and emit one non-recursive console error. |
| Concise output omits a fact needed for safe continuation | Define a closed continuation-critical field set per operation and test concise/detailed semantic equivalence. |
| Token savings are achieved by forcing repeated lookups | Measure complete task interactions, including detailed output or log retrieval, and retain blocker IDs and corrective operations by default. |
| Existing JSON consumers break | Version the projection contract, provide a compatibility transition, and test old and new forms before changing defaults. |
| Console and result errors appear twice | Define one rendering owner per mode and test single-emission behavior. |
| Logs are mistaken for durable audit evidence | Document their diagnostic-only status and keep lifecycle reconstruction independent of them. |
| A logging dependency enlarges the supply-chain boundary | Prefer standard runtime capabilities; justify and pin any dependency through architecture and package-policy review. |

## Open Questions

1. What exact concise field set applies to each read-only and mutating operation?
2. What default character and field budgets satisfy the adoption gates while preserving one-pass corrective action?
3. What platform-specific directory and permission behavior is supported?
4. What size, archive count, and event-size limits are appropriate defaults?
5. What bounded cross-process rotation protocol is sufficiently portable without a new dependency?
6. Should logging failure produce only a console error or also a separate non-semantic status field?
7. Which documented tokenizer estimate should supplement normalized bytes without becoming the normative compatibility measure?

## Decision Log

| Decision | Outcome | Rationale |
| --- | --- | --- |
| Relationship to governed lifecycle CLI | Separate follow-up proposal | PR #155 is already verified; default logging and projection changes should not silently expand its settled first-release scope. |
| Durable authority | Logs are machine-local diagnostics only | Git-tracked artifacts remain the sole durable lifecycle truth. |
| Default file recording | Enabled at `info` | Successful operations must be searchable without opt-in. |
| Default console threshold | `error` | Routine success and expected governance blocks should not consume agent context. |
| Severity vocabulary | `debug`, `info`, `warning`, `error` | The user selected four understandable operational levels. |
| Rotation | Bounded size and retained-file count | Default persistence requires a predictable disk ceiling. |
| Result strategy | Concise opt-in first, then default only after compatibility and measurement gates | Agents need next-action facts without an unsupported compatibility break. |
| Correlation | Short invocation ID and log reference | Concise output can point to diagnostics without copying them. |
| Token measurement | Measure complete interactions | Retrieval costs must be counted so savings are not artificial. |
| Command applicability | Every invocation reaching minimum logger initialization uses a common envelope and exactly one allowlisted family, including `invalid-input`; earlier startup failures are explicitly unobservable | The guarantee covers dispatch and parser failures without raw argument capture and does not make an impossible process-start claim. |
| Request correlation | No request digest or derived request fingerprint in the first release | Invocation IDs and allowlisted semantic identities provide correlation without persistent request-equality leakage. |
| Lookup dependency | Log-path discovery and exact single-invocation lookup ship before concise defaults | Detail remains available without rerunning mutations. |
| Compatibility | v0.4.x adds opt-in projections; v0.5.0 may change defaults only after gates pass | Existing JSON consumers receive a defined transition and durable detailed form. |
| Detailed retention | `detailed-json` remains through v0.5.x and cannot be removed before a separate v0.6.0 decision | Diagnostic access and migration time remain explicit. |
| Token adoption gate | 30% median byte reduction, no profile regression above 10%, and no semantic loss | The primary user-value claim is falsifiable before defaults change. |
| CI retention | Separate proposal reserved by FU-011 | The first release claims machine-local observability and only keeps its local schema forward-compatible; hosted retention and forwarding require an independent scope, privacy contract, and decision. |

## Next Artifacts

- Independent governed proposal rereview focused on CLIOBS-PR6 through CLIOBS-PR8 without weakening privacy, compatibility, token value, default persistence, or rotation portability.
- Feature specification defining severity, event schemas, concise and detailed result contracts, redaction, storage, rotation, failure behavior, lookup, compatibility, and acceptance criteria.
- Architecture assessment and likely ADR covering machine-local persistence, cross-process rotation, result projection, component ownership, and local wrapper result parity; hosted CI forwarding remains outside this proposal.
- Test specification and execution plan after proposal, spec, and architecture settlement.

## Follow-on Artifacts

- [Proposal review r1](../changes/2026-08-25-cli-observability-token-efficient-results-review-recording/reviews/proposal-review-r1.md) recorded the command-scope, compatibility, lookup, token-value, and lifecycle-pointer findings addressed by this revision.
- [Proposal review r1 for the owning change](../changes/2026-08-25-cli-observability-token-efficient-results/reviews/proposal-review-r1.md) records CLIOBS-PR6 through CLIOBS-PR8 addressed by this revision.
- [FU-011](../follow-ups.md#open-follow-ups) owns the separate future proposal boundary for hosted CI log retention and forwarding.
