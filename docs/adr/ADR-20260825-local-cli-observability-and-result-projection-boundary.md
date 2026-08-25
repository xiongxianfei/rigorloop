# ADR-20260825: Local CLI Observability and Result Projection Boundary

## Owning change record

`docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

## Context

The `rigorloop` binary has several command families and historically renders results inside individual handlers. Governed lifecycle commands already return a structured semantic result, while init, scaffolding, and top-level paths retain older output shapes. Users and agents need short actionable output, but operators also need a searchable history when the console is intentionally quiet.

The approved specification requires default machine-local JSON Lines logging, exact invocation correlation, safe bounded rotation, default console severity `error`, opt-in concise and detailed projections, unchanged v0.4.x defaults, and a measured v0.5.0 adoption gate. Logs cannot become lifecycle evidence or change command semantics. Raw arguments, requests, environment values, artifact contents, machine paths, and other private data are forbidden from persisted events.

These requirements create durable boundaries for command orchestration, local persistence, concurrency, result projection, compatibility, and privacy. They belong in one package-level decision rather than separate per-command logging implementations.

## Decision

Introduce one invocation controller around command dispatch. It creates a random invocation ID after safe logging configuration, classifies the command family without persisting raw input, starts a monotonic duration, emits the start event, invokes the existing semantic handler, renders exactly one semantic result, emits the completion event, and maps the semantic exit result. Logging failures are captured as diagnostic state and never thrown through the semantic handler.

Split the package-local implementation into five responsibilities:

1. Logging configuration resolves platform defaults, strict environment and CLI overrides, thresholds, and `off` without exposing raw invalid values.
2. An allowlist event builder converts normalized command and result facts into schema-versioned events, validates closed fields and size, and has no access to raw argv, request bodies, arbitrary environment data, artifact contents, or stack traces at info or warning.
3. A synchronous local sink validates the selected root, modes, and owned names; serializes append and rotation with a fixed exclusive-create lock; and writes complete one-line records before returning. Synchronous I/O is chosen so terminal events are not lost to an unawaited process exit.
4. One internal command-result representation separates semantic facts from presentation. Compatibility, concise-human, concise-JSON, and detailed-JSON renderers are pure projections of that result.
5. Read-only log commands resolve the selected directory and scan only the active file plus four archives. Exact lookup never invokes the original command and never interprets absent random IDs as proven expiry.

The file sink owns `rigorloop.jsonl`, `rigorloop.1.jsonl` through `rigorloop.4.jsonl`, and `.rigorloop-log.lock` beneath the selected root. Every append acquires the lock for at most 10 attempts and 1,000 milliseconds total. Under the lock, the sink revalidates owned paths with non-following filesystem inspection, rotates before an append that would cross 5 MiB, renames archives from highest to lowest, and appends one encoded record. It never steals a lock based on age. Contention, unsafe paths, permissions, disk failure, or malformed owned state degrade observability and preserve the semantic result.

The selected absolute log directory is the containment root. Linux uses `$XDG_STATE_HOME/rigorloop/logs` or `~/.local/state/rigorloop/logs`, macOS uses `~/Library/Logs/RigorLoop`, and Windows uses `%LOCALAPPDATA%\RigorLoop\Logs`. An explicit override replaces that root; the root and existing path components may not be symlinks. New POSIX directories and files use `0700` and `0600`; existing permissions are inspected but never repaired implicitly.

The invocation controller attempts start and completion independently. A process interruption may leave only start. File events default to info; stderr events default to error. Expected policy rejection maps to warning in the file and stays quiet on the default console. Unless console output is explicitly `off`, one guarded emergency path may write a bounded logging-unavailable diagnostic directly to stderr. That path cannot call the logger recursively.

Existing v0.4.x renderers remain compatibility adapters and retain their schemas and ordinary formatting. New concise and detailed renderers consume the shared result model but do not change existing aliases. A future default switch is a release decision gated by the versioned six-profile fixture and v0.4.x baseline; the implementation cannot infer adoption merely because the new renderer exists.

Use Node built-ins for cryptographic randomness, paths, clocks, synchronous filesystem operations, and JSON encoding. Add no logging framework, daemon, database, network client, telemetry exporter, or background worker. The existing pinned `yaml` dependency remains unrelated to diagnostics.

## Alternatives considered

- Log inside each command handler: rejected because field allowlists, severity, correlation, and failure isolation would drift across command families.
- Print info events to the console and rely on shell redirection: rejected because routine output would remain noisy and history would depend on user setup.
- Use an asynchronous logging library: rejected because it expands dependencies and shutdown coordination for two small bounded events per invocation.
- Use operating-system log services: rejected because behavior, retention, access, and portability would vary and exact local lookup would require platform adapters.
- Store an SQLite index or append-only repository ledger: rejected because the first adds a database and the second could be mistaken for governed truth. Five bounded files are sufficient diagnostics.
- Persist an index to distinguish expired IDs: rejected because random absent IDs cannot be proven expired without another retention and privacy contract.
- Replace v0.4.x defaults immediately: rejected because output is a compatibility surface and token savings require measured complete-interaction proof.

## Consequences

- Every command passes through one observable invocation boundary, while semantic handlers remain independently testable without filesystem logging.
- Logging adds two bounded synchronous append attempts to the ordinary path. This favors terminal-event reliability and simple shutdown over maximum throughput; CLI invocation volume makes the tradeoff acceptable.
- Cross-process safety depends on one local lock per event. Contention may lose diagnostics after the fixed bound but cannot delay or alter semantic command completion beyond that bound.
- Privacy is fail-closed at the event builder and path boundary. Debug events may add only separately allowlisted fields; debug does not authorize raw requests, argv, environment dumps, or private paths.
- The result-model extraction touches multiple handlers and requires compatibility fixtures proving byte or whitespace-independent stability for every existing output mode.
- Local logs are disposable, user-scoped diagnostics. A fresh checkout, lifecycle validation, review, settlement, and CI correctness never depend on them.
- A v0.5.0 default change remains blocked until the versioned profile corpus, baseline, semantic field matrix, and complete-interaction thresholds pass.

## Follow-up

- Architecture review of this ADR and the matching canonical update.
- Execution planning must isolate result-model compatibility, logging primitives, command integration, lookup, and adoption measurement into reviewable milestones.
- A later proposal is required for hosted forwarding, telemetry, an expiry index, detailed-output retirement, or a default switch that fails the approved adoption gate.
