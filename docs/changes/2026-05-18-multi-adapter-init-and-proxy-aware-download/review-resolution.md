# Review Resolution: Multi-Adapter Init and Proxy-Aware Adapter Download

## Scope

This record tracks material finding closeout for proposal review and spec review of the multi-adapter init and proxy-aware adapter download change.

Closeout status: closed

Review closeout: proposal-review
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: spec-review-r3
Review closeout: plan-review-r1

- Reviews covered: `proposal-review`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `spec-review-r3`, `plan-review-r1`
- Findings resolved: 9
- Unresolved findings: 0
- Final result: `FID-01`, `FID-02`, `FID-03`, `FID-04`, and `FID-05` are accepted and resolved in the proposal. `SR1-F1`, `SR1-F2`, `SR1-F3`, and `SR1-F4` are accepted and closed by `spec-review-r2`.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| FID-01 | accepted | resolved | The proposal now chooses `schema_version: 2` for multi-root adapter support and preserves backward-compatible parsing for existing Codex single-root entries. |
| FID-02 | accepted | resolved | The proposal now requires declared opencode command aliases for new archives and permits older archives without alias metadata to install with a warning. |
| FID-03 | accepted | resolved | The proposal now chooses Node built-in env-proxy support and diagnostics for the first slice, with Undici dispatcher support deferred. |
| FID-04 | accepted | resolved | The proposal now lists safe proxy facts and prohibits reporting credentials, full proxy URLs, private hostnames, tokens, or raw environment values. |
| FID-05 | accepted | resolved | The proposal now keeps Codex on the existing single-root `installed_root` lockfile field while multi-root adapters use `installed_roots` and `root_hashes`. |
| SR1-F1 | accepted | resolved | Spec now allows compatible older opencode archives to install skills only with warning code `opencode-command-aliases-not-declared` and records only installed roots. |
| SR1-F2 | accepted | resolved | Spec now defines `rigorloop.yaml` single-root and multi-root shapes plus merge and conflict behavior. |
| SR1-F3 | accepted | resolved | Spec now defines trusted metadata fields for single-root adapters, multi-root adapters, and opencode command aliases. |
| SR1-F4 | accepted | resolved | Spec now defines bounded proxy diagnostic fields and allowed values. |

## Common Resolution Metadata

- Owner: proposal author
- Owning stage: proposal
- Validation target: targeted readback of proposal decisions and review closeout artifacts.
- Validation evidence: Targeted readback and formal `spec-review-r2` confirmed the proposal and spec record all accepted decisions, `review-log.md` lists no open findings, and this resolution is closed.

## Finding Details

### proposal-review

Finding closeout for `proposal-review`.

### FID-01 - Lockfile schema version bump

Finding ID: FID-01
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add a resolved proposal-review decision selecting `schema_version: 2` for multi-root adapter support, preserve backward-compatible parsing for existing `schema_version: 1` Codex entries, and require CLI/validation logic to handle mixed single-root and multi-root entries concurrently.
Rationale: Multi-root lockfile fields change durable compatibility state and should not be silently interpreted by older schema assumptions.
Validation target: Confirm the proposal's lockfile section and decision log state the chosen schema strategy.
Validation evidence: Targeted readback confirmed the proposal records `schema_version: 2`, backward-compatible parsing for existing Codex single-root entries, existing `installed_root`, and multi-root `installed_roots` plus `root_hashes`.

### FID-02 - Opencode command aliases

Finding ID: FID-02
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add opencode alias enforcement rules: new archives must include aliases when metadata declares them, missing declared aliases are validation failures, and older archives lacking alias metadata may install with a warning.
Rationale: opencode command aliases are a runtime surface; silent partial installs would be misleading, while older archive compatibility should not be broken without a versioned reason.
Validation target: Confirm the proposal's opencode section records new-archive enforcement and old-archive warning behavior.
Validation evidence: Targeted readback confirmed the proposal records required declared opencode aliases for new archives, validation failure for missing declared aliases, and warning behavior for older archives without alias metadata.

### FID-03 - Proxy support implementation

Finding ID: FID-03
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Choose Node built-in env-proxy support and diagnostics for the first implementation slice, and defer programmatic Undici proxy dispatcher support unless a later spec justifies it.
Rationale: The first slice should reduce proxy confusion without adding unnecessary runtime dependency or dispatcher complexity.
Validation target: Confirm the proposal's resolved decisions and decision log record the first-slice proxy scope.
Validation evidence: Targeted readback confirmed the proposal records Node built-in env-proxy support for the first slice and defers programmatic Undici dispatcher support.

### FID-04 - Safe proxy reporting

Finding ID: FID-04
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Define safe proxy facts: adapter name, release version, detected proxy environment variable names, Node env-proxy support status, download failure class, trusted public archive URL, and `--from-archive` fallback guidance. Keep the prohibition on reporting credentials, full proxy URLs, private hostnames, tokens, or raw environment variable values.
Rationale: Diagnostics should help users recover without leaking sensitive enterprise network data.
Validation target: Confirm the proxy diagnostics section records allowed and forbidden diagnostic facts.
Validation evidence: Targeted readback confirmed the proposal records safe proxy facts, including detected proxy environment variable names, Node env-proxy support status, download failure class, trusted public archive URL, and fallback guidance.

### FID-05 - Codex lockfile single-root handling

Finding ID: FID-05
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Keep Codex entries using the existing `installed_root` lockfile field while multi-root adapters use `installed_roots` and `root_hashes`.
Rationale: Codex remains a single-root `.agents/skills` adapter, so normalizing it to multi-root shape in this slice would add churn without user value.
Validation target: Confirm the proposal's lockfile section and decision log record mixed single-root and multi-root handling.
Validation evidence: Targeted readback confirmed the proposal records Codex on existing `installed_root` and multi-root adapters on `installed_roots` and `root_hashes`.

### proposal-review-r2

No material findings. No disposition entries required.

### proposal-review-r3

No material findings. No disposition entries required.

### spec-review-r1

Finding closeout for `spec-review-r1`.

### SR1-F1 - opencode older-archive behavior conflicts with required multi-root lockfile shape

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: resolved by spec author
Decision needed: None; owner chose skills-only compatibility for accepted older opencode release ranges.
Chosen action: Revise the spec so older opencode archives without `command_aliases.opencode` may install `.opencode/skills` only when the bundled trusted metadata lists the release as compatible with skills-only opencode installation. The CLI must omit `.opencode/commands`, emit warning code `opencode-command-aliases-not-declared`, and record only `skills` in `rigorloop.yaml` and `rigorloop.lock`.
Rationale: This preserves compatibility for older verified opencode archives without silently claiming command aliases that were not declared or installed.
Required outcome: Define whether `.opencode/commands` is required, optional, or omitted for older opencode archives, and define the exact `rigorloop.yaml` and `rigorloop.lock` shape for that case.
Safe resolution path: Add explicit requirements that descriptor roots are possible roots while trusted metadata determines required roots. For older opencode archives without command-alias metadata, either block installation or allow skills-only installation with `installed_roots.skills` and `root_hashes.skills` only, omit `commands`, emit a stable warning code, and ensure `rigorloop.yaml` does not record `.opencode/commands`.
Needs-decision rationale: Resolved by owner decision and closed by `spec-review-r2`.
Validation target: Revise `specs/multi-adapter-init-and-proxy-aware-download.md` and rerun spec-review.
Validation evidence: Spec requirements `MAI-R14a`, `MAI-R21e`, `MAI-R21f`, `MAI-R44`, `MAI-R46a` through `MAI-R46c`, `MAI-R51c`, `MAI-R51e`, `MAI-R64a`, and `MAI-R64b` record the accepted skills-only older opencode behavior. Formal `spec-review-r2` approved the revised spec and closed this finding.

### SR1-F2 - `rigorloop.yaml` merge and conflict behavior is underspecified

Finding ID: SR1-F2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: resolved by spec author
Decision needed: None; owner chose single-root `install_root` and multi-root `install_roots` manifest shape.
Chosen action: Revise the spec so single-root adapters use `install_root`, multi-root adapters use `install_roots` keyed by root role, skills-only opencode records only installed roots, existing valid unrelated adapter entries are preserved, and malformed or conflicting manifest state blocks before mutation.
Rationale: The manifest shape should mirror adapter root cardinality while keeping existing valid project configuration stable and making unsafe merge cases explicit.
Required outcome: Define a testable manifest shape and update policy for adding or reinstalling adapters.
Safe resolution path: Add a `rigorloop.yaml` schema example and requirements for single-root entries using `install_root`, multi-root entries using `install_roots`, updating only the selected adapter entry after verification, preserving unrelated valid adapter entries, and blocking on duplicate selected adapter entries, malformed adapters, unsupported manifest schema, or unknown manifest fields that cannot be safely preserved.
Needs-decision rationale: Resolved by owner decision and closed by `spec-review-r2`.
Validation target: Revise `specs/multi-adapter-init-and-proxy-aware-download.md` and rerun spec-review.
Validation evidence: Spec requirements `MAI-R49` through `MAI-R51i` define the manifest shape, examples, and conflict behavior. Formal `spec-review-r2` approved the revised spec and closed this finding.

### SR1-F3 - Trusted metadata shape is too vague for multi-root verification

Finding ID: SR1-F3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: resolved by spec author
Decision needed: None; owner chose explicit metadata fields for single-root adapters, multi-root adapters, and opencode command aliases.
Chosen action: Revise the spec so trusted metadata includes single-root `install_root`, `tree_sha256`, and `file_count`; multi-root `install_roots` and `root_hashes`; opencode `command_aliases.opencode` count and exact paths when declared; and treats absence of `command_aliases.opencode` as the only older skills-only signal within accepted release ranges.
Rationale: The CLI needs a precise metadata contract to verify generated output, distinguish single-root from multi-root archives, and avoid guessing older opencode behavior.
Required outcome: Define the minimum trusted metadata contract needed by the CLI for all supported adapters.
Safe resolution path: Add normative metadata fields for single-root adapters (`install_root`, `tree_sha256`, `file_count`), multi-root adapters (`install_roots`, `root_hashes` keyed by root role), and opencode command aliases (`command_aliases` section with count and exact paths when aliases are declared). Define absence of `command_aliases.opencode` as the only older-archive signal and only for release ranges the spec allows.
Needs-decision rationale: Resolved by owner decision and closed by `spec-review-r2`.
Validation target: Revise `specs/multi-adapter-init-and-proxy-aware-download.md` and rerun spec-review.
Validation evidence: Spec requirements `MAI-R20` through `MAI-R21f` define the trusted metadata shape and old-archive compatibility boundary. Formal `spec-review-r2` approved the revised spec and closed this finding.

### SR1-F4 - Proxy diagnostic fields are not precise enough for tests

Finding ID: SR1-F4
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Decision owner: resolved by spec author
Decision needed: None; owner chose bounded proxy diagnostic fields and deferred Undici dispatcher support.
Chosen action: Revise the spec so first-slice proxy behavior uses Node built-in env-proxy support only when supported and enabled, leaves programmatic Undici dispatcher support out of scope, and exposes stable diagnostic fields for detected proxy variable names, Node env-proxy status, download failure class, and trusted archive URL.
Rationale: Bounded diagnostics make proxy failures testable and actionable while avoiding sensitive enterprise network disclosure and extra dispatcher complexity in this slice.
Required outcome: Define stable proxy diagnostic fields and allowed values.
Safe resolution path: Add explicit diagnostic values such as `proxy_env_vars_detected` names only from `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`; `node_env_proxy_status: enabled | disabled | unsupported | unknown`; `download_failure_class: dns | tls | timeout | http-status | proxy | network | unknown`; and `archive_url` as the trusted public archive URL only.
Needs-decision rationale: Resolved by owner decision and closed by `spec-review-r2`.
Validation target: Revise `specs/multi-adapter-init-and-proxy-aware-download.md` and rerun spec-review.
Validation evidence: Spec requirements `MAI-R77` through `MAI-R85` define first-slice proxy scope, bounded diagnostic field names, allowed values, and privacy limits. Formal `spec-review-r2` approved the revised spec and closed this finding.

### spec-review-r2

No material findings. Clean formal review approved the revised spec and closed `SR1-F1`, `SR1-F2`, `SR1-F3`, and `SR1-F4`.

### architecture-review-r1

No material findings. Clean formal review approved the canonical architecture update and ADR with no required canonical updates, ADR updates, or architecture blockers before planning.

### spec-review-r3

No material findings. Clean formal review rechecked the approved spec after architecture-review and found no contract blockers before planning.

### plan-review-r1

No material findings. Clean formal review approved the active execution plan for test-spec handoff with no required plan edits.

### code-review-m1-r1

No material findings. Clean formal review closed M1 and handed off to implementation M2. No review-resolution work is required for this review.

## Closeout Checklist

- [x] Every material finding has a disposition.
- [x] Every accepted finding has action and rationale.
- [x] Validation evidence is recorded for each resolved finding.
- [x] `review-log.md` lists no open findings.
- [x] Closeout status is correct.
