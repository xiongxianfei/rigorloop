# Adapter Init and Proxy Fetch Guidance

## Frame

- Trigger: explicit maintainer invocation asking for best practices to support Claude Code/opencode and solve Node `fetch` proxy failures.
- Trigger type: maintainer request / contributor observation.
- Scope:
  - Current `rigorloop init --adapter codex` CLI behavior.
  - Existing public adapter archive support for Codex, Claude Code, and opencode.
  - Network archive download behavior through Node `fetch`.
  - Best-practice routing for future CLI support and proxy-aware download reliability.
- Evidence reviewed:
  - `README.md` CLI and adapter package sections.
  - `packages/rigorloop/dist/bin/rigorloop.js` adapter constants, usage text, `fetchBytes`, archive-download error handling, and adapter gate.
  - `specs/rigorloop-cli-package-and-codex-init.md` first-slice Codex-only CLI contract.
  - `specs/rigorloop-cli-lockfile.test.md` lockfile, mocked-network, local-archive, unsupported-adapter, and trust-boundary expectations.
  - `docs/learn/README.md`.
  - `docs/learn/sessions/2026-05-16-v015-publication-time-retrospective.md`.
  - Node.js Enterprise Network Configuration: `https://nodejs.org/learn/http/enterprise-network-configuration`.
  - Undici `EnvHttpProxyAgent` documentation: `https://github.com/nodejs/undici/blob/main/docs/docs/api/EnvHttpProxyAgent.md`.
  - Undici `ProxyAgent` documentation: `https://github.com/nodejs/undici/blob/main/docs/docs/api/ProxyAgent.md`.
- Explicit exclusions:
  - This session does not approve a CLI behavior change.
  - This session does not update specs, architecture, code, release metadata, adapter archives, or tests.
  - This session does not claim Claude Code/opencode init support exists today.
  - This session does not create authoritative proxy policy.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-16-v015-publication-time-retrospective.md`, especially the observation that package versions, bundled adapter metadata, release assets, and real install smoke must stay coherent.

## Observe

### O1: Adapter distribution support and CLI init support are currently different surfaces

The repository documents generated adapter archives for Codex, Claude Code, and opencode. The same README maps them to `.agents/skills/`, `.claude/skills/`, and `.opencode/skills/`, and documents opencode command aliases.

The CLI command surface is narrower. `packages/rigorloop/dist/bin/rigorloop.js` hard-codes `ADAPTER = "codex"` and `INSTALL_ROOT = ".agents/skills"`, prints help for `rigorloop init --adapter codex`, and rejects any other adapter in `handleInit`.

### O2: Existing specs intentionally block non-Codex adapter state in the current slice

The approved first-slice CLI spec says the broader proposal remains product direction but does not define non-Codex adapters. It also requires unsupported adapters to be rejected.

The lockfile test spec reinforces that boundary: unsupported adapter entries such as `claude` block before mutation, and inventing multi-adapter semantics without a spec is explicitly called out as a failure mode.

### O3: Multi-adapter init needs a contract-first slice, not a constants-only patch

Supporting `rigorloop init --adapter claude` and `rigorloop init --adapter opencode` changes public command syntax, install roots, archive selection, metadata lookup, lockfile shape/compatibility, overwrite safety, JSON action names, and validation evidence.

opencode also has a second generated surface: command aliases under `.opencode/commands/` in addition to portable skills under `.opencode/skills/`. Treating opencode as only a different skill install root would miss that observable behavior.

### O4: Local archive mode is the current reliable fallback for network differences

The lockfile test spec already requires local archive installs to record `source: local-archive`, keep the official package-compatible release tag, verify against trusted bundled metadata, and avoid machine-local path leakage.

This makes `--from-archive` the right user-facing fallback when GitHub is reachable by `curl` but Node `fetch` fails because of proxy or TLS differences.

### O5: Proxy-aware network install needs Node-version-aware handling

The current CLI uses bare `fetch()` for archive download and collapses any thrown error to `Official Codex adapter archive is unavailable.`

Node's current enterprise network guidance says `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` are used by `fetch()` only when `NODE_USE_ENV_PROXY` or `--use-env-proxy` is enabled on supported Node versions. The same guide says global `http`/`https` agents do not affect `fetch()`.

Undici provides programmatic proxy support. `EnvHttpProxyAgent` reads proxy environment variables and can be registered with `setGlobalDispatcher`; `ProxyAgent` can be used as a dispatcher for explicit proxy URLs and can also be registered globally.

### O6: Network tests should stay hermetic, but proxy behavior needs focused coverage

The existing test spec says network archive behavior remains fixture-backed and must not depend on live GitHub availability. That remains correct.

If proxy-aware behavior is added, tests should exercise dispatcher/proxy configuration through a controlled local or mocked fetch path, not by depending on a real external proxy or GitHub.

## Classify

| Observation | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record | local README and CLI evidence | This clarifies current state without requiring a behavior change. |
| O2 | observation | observation | session record | approved spec and test-spec evidence | This records why non-Codex init cannot be added as an incidental code tweak. |
| O3 | direction | pending confirmation | proposal/spec for multi-adapter init; likely architecture/test-spec before implementation | pending contributor confirmation | The requested behavior is a public CLI expansion across multiple contract surfaces. |
| O4 | durable-lesson candidate | pending confirmation | possible topic entry or CLI troubleshooting docs | pending contributor confirmation | Local archive fallback is already supported and reusable, but durable topic capture needs confirmation. |
| O5 | artifact-update candidate | pending confirmation | CLI spec/update and implementation plan for proxy-aware fetch diagnostics/support | pending contributor confirmation | Proxy behavior affects runtime reliability and user diagnostics; authoritative behavior belongs in specs/code/docs. |
| O6 | process-follow-up candidate | pending confirmation | targeted tests for proxy handling while preserving hermetic network tests | pending contributor confirmation | Test strategy is actionable but should be owned by the eventual implementation plan. |

## Route

- Session record created: `docs/learn/sessions/2026-05-18-adapter-init-and-proxy-fetch.md`.
- No topic file updated because contributor confirmation is pending.
- No authoritative artifact updated in this learn session.
- Candidate follow-ups pending contributor confirmation:
  - Open a proposal/spec slice for `rigorloop init --adapter claude|opencode`.
  - Add proxy-aware download behavior or documented runtime flags for Node `fetch`.
  - Improve `--debug` output so archive download failures expose the underlying fetch error category without leaking credentials.
  - Add hermetic proxy/download tests that do not depend on live GitHub or a real external proxy.

## Practical Best Practices

For Claude Code/opencode support:

1. Treat it as a new public CLI slice. Start with proposal/spec/test-spec before code because it changes command syntax, metadata, lockfile compatibility, output JSON, install roots, and mutation safety.
2. Model adapters through a small descriptor table rather than scattered constants:
   - `codex`: archive `rigorloop-adapter-codex-<version>.zip`, install root `.agents/skills/`.
   - `claude`: archive `rigorloop-adapter-claude-<version>.zip`, install root `.claude/skills/`.
   - `opencode`: archive `rigorloop-adapter-opencode-<version>.zip`, install root `.opencode/skills/`, plus `.opencode/commands/` aliases.
3. Keep package-bundled metadata as the trust root. Do not allow user-supplied metadata to define official archive URLs, checksums, install roots, or tree hashes.
4. Extend `rigorloop.lock` deliberately for multi-adapter state. Decide whether a project can install multiple adapters simultaneously, whether rerunning one adapter preserves other supported adapters, and how unsupported future adapter entries are handled.
5. Preserve generated-output safety: refuse path traversal, symlinks, wrong install roots, mismatched archive/tree hashes, and overwrites of non-generated user files.
6. Keep live GitHub out of automated tests. Use fixture archives and mocked fetch/dispatcher behavior, then reserve real public archive smoke for release verification.

For proxy-aware fetch:

1. Support the no-code runtime path first where available:
   - Node versions that support it can use `NODE_USE_ENV_PROXY=1` or `node --use-env-proxy` with `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`.
2. Add programmatic support if the CLI must work across Node versions that do not reliably honor proxy env vars for `fetch()`:
   - Use Undici `EnvHttpProxyAgent` with `setGlobalDispatcher()` to honor environment variables.
   - Use `ProxyAgent` when an explicit proxy URL option is introduced.
3. Respect `NO_PROXY`; do not force all traffic through a proxy.
4. Redact proxy credentials from diagnostics. `--debug` should identify error class and target host, not print credential-bearing proxy URLs.
5. Keep `--from-archive` as the deterministic fallback for restricted networks. It should remain verified against bundled metadata and should record only the archive basename in lockfile state.

## Validation

No validation commands were run for this learn session beyond bounded evidence reads and external documentation lookup. The session adds only this Markdown record.
