# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as
target initialization and change metadata scaffolding. Release archives remain
verified GitHub release artifacts; they are not bundled into the npm package.
npm is the CLI delivery channel, not the canonical source for workflow rules,
skills, schemas, templates, or adapter archives.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@latest init claude
npx @xiongxianfei/rigorloop@latest init opencode
```

Use a pinned version when you want reproducible setup:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex
```

Install as a project-local development dependency:

```bash
npm install --save-dev @xiongxianfei/rigorloop
npx rigorloop --help
npx rigorloop init codex
```

Install globally only if you want a machine-wide `rigorloop` command:

```bash
npm install --global @xiongxianfei/rigorloop
rigorloop --help
rigorloop init codex
```

## Commands

### Explicit workflow recording

The coordinated local candidate provides the RigorLoop Record Format through targeted commands. Workflow owns actor decisions; Record Format owns stored representation; CLI owns construction, encoding and recoverable persistence. Projects must explicitly adopt the matching models and skills. Installation alone does not activate a project or customer, and this candidate does not claim a released version.

```sh
rigorloop status --root /path/to/project --change example --format json
rigorloop context --root /path/to/project --change example --input - --format json
rigorloop subject inspect --root /path/to/project --path docs/design/example.md --content full --format json
rigorloop work set work-1 --root /path/to/project --change example --input - --format json
rigorloop batch --root /path/to/project --change example --input - --format json
rigorloop verify show --root /path/to/project --change example --format json
rigorloop decisions show --root /path/to/project --change example --format json
```

Context input is `{ "schema_version": 1, "select": [{ "kind": "work", "where": { "ids": ["work-1"] } }] }`. Full selected fields are the default; scope reports omissions, missing content and continuation. Expand the selection when the engineering decision needs more basis. Status reports recorded activity and counts, never an authoritative next stage.

A targeted write has `schema_version: 1`, `interface: targeted-recording-v1`, the observed `contract`, `change_id`, `expected_revision`, `reads: [{path, identity}]`, and `operation: {op, target, values}`. Batch replaces operation with operations. Use the read result's exact record_contract and revision, and subject inspection's identities; the CLI does not substitute newly observed content for the actor's decision basis. Each command's --help gives its exact selectors and fields. The CLI constructs registry entries and serialized bytes and preserves omitted fields, neighbors and narrative. Newly created supporting records require explicit applicability; actor judgments and dispositions are never inferred.

Use `change create` only with explicit new-change authority, an absent root and contract rigorloop-records-v2. New records are change.json, reviews/<id>.json, evidence.json, material-decisions.json and success-only verify-report.json. Retired stored formats are unsupported runtime input and reject without fallback or mutation. Historical records remain unchanged archival evidence. V2 has packaged schemas/templates; targeted transport has its own targeted-recording-v1.schema.json. Templates illustrate stored shapes, not normal full-file write requests or approval. Create docs/changes/ before creating an absent change root.

Normal writes validate and optionally support --dry-run; preview reserves nothing. Results are compact and storage-only. Saved/unchanged/valid/inspected use exit 0, rejected 2, conflict 3, busy 4 and recovery-required 5. Reread and reassess conflicts instead of retry-merging. Observation summaries disclose omitted detail; observations show retrieves bounded detail with revision and observation-identity checks. Diagnostic volume cannot prevent an otherwise valid correction. A saved judgment, failed check or completion claim does not justify downstream reliance.

Advanced `record-store inspect|check|record|recover` remains for diagnostics, complete explicit restoration and persistence maintenance. Only v2 is accepted by advanced and primary recording. The independently versioned advanced result schema 1 and targeted-recording-v1 transport remain supported. Advanced replacements contain exact complete bytes under the selected stored version, while primary writes construct bytes. Both share containment, conflict and recovery protections. For interrupted storage use `record-store recover --root PATH --change ID --transaction ID --expected-recovery DIGEST --action restore|complete --format json` with one explicit action. Do not edit records with external tools during save/recovery; the documented limitation for external edits after the final identity check is unchanged.

The retired new-change, compact and lifecycle command families reject before request processing or side effects. Use v2 `change create` with explicit authority for new work. Recovery classifies the journal's recorded format selector and saved before/candidate/write/read basis; supported consistent v2 transactions recover, including initial creation with no current manifest. Retired, unknown, inconsistent or ambiguous bases stop before restore/complete writes and preserve evidence. Journal selector 1 selects retired v1; the advanced result's schema 1 is independent. Never change a discriminator to simulate recovery or rollback.

### Other command families

```bash
rigorloop --help
rigorloop version
rigorloop init codex|claude|opencode [--write-state] [--from-archive <path>] [--dry-run] [--json]
rigorloop workflow-context [--change <id>] [--format human|json]
rigorloop logs path [--format human|json]
rigorloop logs show <invocation-id> [--format human|json]
```

Registered historical lifecycle mutations use request files and their existing operations. Existing version-1 coordination remains readable under that contract. Compact operations instead accept transient arguments, standard input, or disposable request files; successful requests are not governed artifacts. The CLI validates expected revision, exact identities, semantic operation shape, and resulting consistency, but it does not grant caller permission.

`workflow-context` returns factual schema-2 discovery, never eligibility, an authoritative next stage or implicit change selection. It classifies current v2 manifests, malformed or ambiguous current stores, and unrelated YAML-only archives without running legacy validators. Explicit targets avoid unrelated enumeration. Limits are inclusive: 1,024 directories, 64 candidates and an 8 MiB response budget. Exceeding a bound reports incomplete scope and limit-exceeded without silent truncation. An optional root `rigorloop.workflow.yaml` may override supported artifact locations; retired record-slot overrides, unsafe paths and invalid configuration fail closed. Use primary context/show for complete selected current-record content.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs path` to locate it and `rigorloop logs show <invocation-id>` for exact lookup.

For historical commands, use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory. Primary recording commands and the advanced `record-store` namespace must be the first argument; they reject these flags, ignore this logging environment and emit only their model-defined results.

Existing v0.4.x output defaults and `--json` remain unchanged. Agents can opt into compact results with `--format concise-json` or `--format concise-human`; complete results remain available with `--format detailed-json`. Local logs are diagnostics only and never authorize lifecycle transitions.

## Target Init

Version 0.5.1 is an unpublished candidate. Its bundled metadata describes route-only candidate archives and makes no claim that those archives or the npm package are publicly available yet. For an exact lockfile-managed install, rerun `init` with `--write-state` to replace `workflow` with `route`; unmanaged or drifted installs remain blocked with state-specific recovery guidance. Legacy persistent automation store adapters are unsupported; no v2 automation mapping is implied.

After v0.5.1 is published, initialize target support from its verified official release archive:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex --json
npx @xiongxianfei/rigorloop@0.5.1 init claude --json
npx @xiongxianfei/rigorloop@0.5.1 init opencode --json
```

Preview the write plan without mutating files:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init opencode --dry-run --json
```

Use `--from-archive` with a matching generated candidate during local validation, or with the official archive after publication:

```bash
npx @xiongxianfei/rigorloop@0.5.1 init codex --from-archive ./rigorloop-adapter-codex-v0.5.1.zip --json
npx @xiongxianfei/rigorloop@0.5.1 init claude --from-archive ./rigorloop-adapter-claude-v0.5.1.zip --json
npx @xiongxianfei/rigorloop@0.5.1 init opencode --from-archive ./rigorloop-adapter-opencode-v0.5.1.zip --json
```

Default init installs verified target support without writing `rigorloop.yaml` or `rigorloop.lock`. Use `--write-state` when you want RigorLoop-managed project state files. The command verifies the selected archive before extraction and verifies the installed tree before reporting success. Runtime roots are target-specific:

```text
codex:   .agents/skills
claude:  .claude/skills
opencode: .opencode/skills and .opencode/commands when command aliases are declared
```

Network installs use Node `fetch()`. If download fails in a proxied environment, JSON output reports bounded diagnostics such as target name, release version, trusted archive URL, detected proxy environment variable names, Node env-proxy status, and failure class. It does not print proxy credentials or raw proxy values. On Node versions that support env-proxy, enable it with `NODE_USE_ENV_PROXY=1`, `NODE_OPTIONS=--use-env-proxy`, or `node --use-env-proxy`; otherwise use the `--from-archive` fallback.

## New change recording

Use `rigorloop change create --help` for the targeted request shape, then submit the explicit v2 request with `--root PATH --input - --format json`. Add `--dry-run` for an optional preview. Creation requires explicit authority and an absent root; it grants no proposal, Design, review, Verify or PR judgment. The removed `new-change` scaffold is unsupported.

## Version Guidance

Use `@latest` for manual exploration. Use an explicit version such as `@0.3.5` for CI, onboarding docs, and repeatable agent setup.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, specs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```

## Upgrading retired authoring skills

The unified authoring candidate supplies `design` and withdraws `spec` and `architecture`, including OpenCode command aliases. Use a CLI and verified adapter archive from the same coherent candidate or adopting release. This source change does not publish that release. Ordinary init rejects old or mixed entries before writing; a candidate containing retired entries also rejects. Previously released archives retain their own inventory.

For a managed target, **do not remove the old directories first**: that changes the installed-tree hash and correctly triggers drift protection. The installation owner’s bounded authority is [TNI-DES-01–06](../../specs/target-native-init.md#scoped-design-amendment-managed-authoring-replacement).

1. Stop local writers and inspect `rigorloop.yaml`, `rigorloop.lock` and the selected target’s complete recorded roots. Codex selects `.agents/skills`; Claude selects `.claude/skills`; OpenCode selects both `.opencode/skills` and `.opencode/commands`. Custom, overlapping, missing or unsafe roots need owner reconciliation. Inspect other managed targets too: writing shared state retains their safety checks.
2. Make a separate backup outside the project and installation roots of **every complete selected root and both state files**, preserving bytes and permissions. Record a state file’s absence explicitly. Verify that the backup is readable and complete. Preserve local additions or modifications separately; a backup does not authorize overwriting them. Keep the untouched original installation in place for eligibility checks.
3. With explicit authority to replace those complete generated roots and update their state entry, run the following command with the selected target and matching archive. A dry run reports intent and state checks; it does not read or approve archive contents. The actual run verifies candidate trust and inventory and rechecks original hashes before replacement.

```bash
rigorloop init codex --from-archive /absolute/path/to/rigorloop-adapter-codex-v0.5.1.zip --write-state --dry-run --format json
rigorloop init codex --from-archive /absolute/path/to/rigorloop-adapter-codex-v0.5.1.zip --write-state --format json
```

Use `claude` or `opencode` with its matching archive for those targets. The version here identifies the local candidate; select the actual coherent release when one is separately published. `--write-state` is narrowly authorized replacement, not a drift override. Modified old entries, unrecorded additions, manual pre-deletion, mixed ownership and conflicting state block before mutation. Restore the recorded original basis from a known backup only after preserving and reconciling local changes; never delete the lockfile or refresh hashes merely to bypass this check.

4. Inspect the result: `design` exists, retired skills and OpenCode aliases are absent, both selected OpenCode roots agree, installed counts/hashes match the new selected lock entry, and other targets and unrelated content are unchanged. Repeating the same successful command is idempotent. Keep the separate backup and every path reported by the retained-backup diagnostic until that comparison and inspection for late writes are complete.
5. On a caught failure, the CLI either restores the exact original roots/state or reports incomplete recovery and retained paths. A process interruption can leave a partial pair. Preserve that partial content and any independent changes in another backup before recovery. Under the installation owner’s explicit recovery authority, restore **the complete original selected roots and both original state files as one coherent basis**, including original absence; do not overlay old files on a partial new tree. Inspect and move partial selected content aside before restoring. If another actor changed shared state or other targets, preserve those changes and have their owner reconcile them before restoration; do not overwrite them with the old shared files. Then rerun the same authorized command. Private recovery evidence requires a coherent original or verified candidate basis before retry can proceed; it cannot bless a partial installation.

The CLI retains private `.rigorloop-authoring-*` recovery evidence and detached original/rollback paths outside selected roots. Do not remove these to bypass recovery. Once a coherent pair and any late writes have been inspected, the operator may explicitly remove the reported retained paths and backup; the installer does not automatically delete them. Unrelated files and other targets are outside that cleanup authority.

For a genuinely unmanaged installation with neither state file implicating the target, inspect and separately back up the retired skill directories and applicable command aliases, explicitly remove only those entries, then retry ordinary init. Remaining unrelated content and generated-file conflicts retain their ordinary protections. A managed or ambiguous target cannot use this manual cleanup path to escape the recorded basis.
