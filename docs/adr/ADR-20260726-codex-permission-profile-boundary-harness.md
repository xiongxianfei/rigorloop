# ADR-20260726: Codex Permission-Profile Boundary Harness

## Status

accepted

## Context

The accepted boundary-first architecture requires a child runtime whose tools
can access only the isolated scenario workspace, cannot use network,
connectors, or subagents, cannot read control-plane credentials, and report
their actual model and runtime profile before behavior output is accepted.

The first M2 preflight proved that `codex exec --json` is not a sufficient
adapter. Its JSONL start event omits model and effective-profile metadata, and
advertised CLI options cannot prove enforcement. The preflight therefore
stopped with `effective-profile-attestation-unavailable` before any published
skill mutation.

Codex CLI 0.138.0 and later supports named permission profiles. The app-server
protocol's `thread/start` response includes model, provider, CLI version,
active permission profile, runtime workspace roots, instruction sources, and
working directory. The separate `codex sandbox` surface can apply the same
profile to deterministic parent-owned allow and deny probes.

## Decision

Use Codex app-server over stdio as the first-version child-runtime protocol.

The harness:

1. resolves the Codex launcher and runtime package, records stable raw-byte and
   filesystem identities before and after every probe and invocation, and
   rejects versions before 0.138.0;
2. creates a fresh mode-restricted `CODEX_HOME` containing only the exact
   generated configuration and the minimum copied authentication material;
3. configures one named permission profile without any legacy `sandbox_mode`:
   `:root` is denied; `:minimal` and the identified runtime package are
   readable; the isolated workspace roots are writable; command network is
   disabled;
4. disables apps, browser/computer tools, subagents, web search, plugins, and
   unmanifested MCP servers and gives spawned commands only an explicit
   minimal environment;
5. generates the experimental app-server schema with the exact executable,
   binds the path-sorted raw-byte schema-bundle identity, and requires the
   exact protocol methods and non-null fields used by the harness;
6. initializes app-server with `capabilities.experimentalApi: true`, then
   obtains runtime-owned `config/read`, `configRequirements/read`, fully
   paginated `experimentalFeature/list`, `app/list`, `plugin/list`,
   `mcpServerStatus/list`, and `skills/list` evidence;
7. requires an exact capability inventory: apps, plugins, MCP servers,
   browser/computer/image/search tools, goals, realtime/remote capabilities,
   and subagent tools are absent, and skills equal the five manifest-bound
   packages;
8. runs deterministic positive and negative probes through
   `codex sandbox --include-managed-config`, binding generated configuration
   and applicable managed-configuration identities on both execution paths;
9. starts one ephemeral thread with `dynamicTools: []`, `environments: []`,
   and only the manifested skill capability roots, and accepts lifecycle
   output only when
   `thread/start` reports the exact active
   profile, runtime workspace roots, instruction sources, working directory,
   CLI version, model, and provider expected by the parent;
10. injects a transient control-plane canary and requires an exact
    spawned-command environment-name allowlist plus argv/stdin, private-path,
    and process-metadata denial proof;
11. records only bounded typed attestation and stable diagnostics. It discards
   raw probe and protocol logs and never serializes credentials, private paths,
   or configuration values.

The required parent probes are:

- manifested workspace read succeeds;
- behavior-output write succeeds;
- unmanifested source read fails;
- private authentication path read fails;
- child network connection fails.
- spawned-command environment names equal the closed allowlist;
- the transient canary and credential-shaped variables are absent from command
  environment, argv, stdin, readable paths, and process metadata.

The app-server response, runtime-owned effective configuration and capability
inventories, exact experimental schema, applicable managed requirements, and
direct probes are complementary. No one source is sufficient alone. Help
text, parent configuration assertions, child narration, and access history
never satisfy the gate.

The exact permitted model-visible built-in tool set is:

- sandboxed command execution backed only by `shell_tool`, `unified_exec`, and
  `shell_snapshot`;
- sandboxed file-change/apply-patch events confined to the isolated workspace.

All dynamic tools, apps, plugins, MCP/connectors, subagents, goals,
browser/computer/image/search tools, realtime/remote capabilities, and external
environments are prohibited.

The harness owns one closed version/schema-bound classification for every
fully paginated `experimentalFeature/list` row. Each row is classified as a
permitted built-in tool, permitted non-tool runtime behavior, or
must-be-disabled tool-bearing behavior. Missing required rows, unknown rows,
unknown mappings, or an enabled prohibited row return
`environment-unavailable` before `turn/start`.

The complete generated protocol vocabulary is also identity-bound. Every item
variant is classified as permitted side effect, non-side-effect protocol
traffic, or prohibited capability event. A prohibited variant may exist in
the schema because protocol support is not effective enablement; pre-turn
configuration, feature, and inventory evidence must prove its capability
disabled, and any observed prohibited event during the accepted turn fails
closed. Only sandboxed command execution and isolated-workspace file change
are permitted side effects.

## Alternatives considered

- Keep `codex exec --json`: rejected because it does not report the selected
  model or active permission-profile provenance.
- Treat named-profile configuration as attestation: rejected because intended
  policy is not effective enforcement.
- Use only `codex sandbox` probes: rejected because they do not report the
  lifecycle thread's model, instructions, roots, or active profile.
- Use an external container or namespace wrapper: deferred because the native
  permission profile and app-server protocol already expose a smaller
  supported boundary; an external wrapper would add image, mount, proxy, and
  credential-broker inputs.
- Weaken the proof to fixture-only or child self-report: rejected because it
  would no longer prove the published skill workflow under the accepted
  contract.

## Consequences

- M2 can resume only after architecture review accepts this interface and the
  revised preflight proves it on the current runtime.
- The harness must implement a bounded JSON-RPC client using only the Python
  standard library and `boundary_proof_model`.
- App-server protocol fields and the permission-profile shape become
  identity-bound implementation inputs and receive missing, extra, stale, and
  mismatch tests.
- Beta permission-profile protocol drift fails closed with
  `environment-unavailable`; it never falls back to legacy sandbox modes.
- Experimental API negotiation and the exact generated schema are
  identity-bound inputs; missing, null, additional, defaulted-away, or
  incompatible fields fail before a turn.
- Authentication remains runtime control-plane state. Direct auth-path denial
  plus canary, exact environment-name, argv/stdin, and process-metadata proofs
  are mandatory before model output is accepted.
- The architecture still uses one standalone child invocation and does not
  import workflow automation or create a second workflow engine.

## Acceptance conditions

This ADR may become accepted only after architecture review confirms:

- the app-server response fields satisfy runtime-owned metadata requirements;
- direct probes establish the effective filesystem and network boundary;
- connector, subagent, plugin, browser, and MCP closure is deterministic;
- runtime-owned effective config and capability inventories are exact;
- the fully paginated feature inventory maps exhaustively to the exact allowed
  built-in tool set before the turn;
- experimental protocol negotiation and schema identity fail closed on drift;
- managed requirements and generated profile bytes are bound across app-server
  and sandbox-probe execution;
- credential material stays outside child-readable roots and evidence;
- unsupported or drifting runtimes fail closed before skill mutation.

## Relationship

This ADR refines the child-runtime adapter selected by
`ADR-20260725-boundary-first-proof-modeling`. It does not supersede the
boundary model, evidence, publication, or activation decisions in that ADR.
