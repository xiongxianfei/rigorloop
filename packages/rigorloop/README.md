# @xiongxianfei/rigorloop

RigorLoop CLI for repository-local AI-assisted software delivery.

This package exposes the `rigorloop` binary for approved CLI workflows such as target initialization and change metadata scaffolding. Release archives remain verified GitHub release artifacts; they are not bundled into the npm package. npm is the CLI delivery channel, not the canonical source for workflow rules, skills, schemas, templates, or adapter archives.

## Quick Start

Run directly with `npx`; no install step is required:

```bash
npx @xiongxianfei/rigorloop@latest --help
npx @xiongxianfei/rigorloop@latest version
npx @xiongxianfei/rigorloop@latest init codex
npx @xiongxianfei/rigorloop@latest init claude
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

For reading reports in the terminal, omit `--format json` or use `--format text`:

```bash
rigorloop review show design-review --root /path/to/project --change example
rigorloop verify show --root /path/to/project --change example
```

Text output displays labeled YAML fields with multiline bodies as indented literal blocks, preserving paragraphs, lists and code blocks. It includes the same selected information, identities and scope as JSON. Use `--format json` for automation; JSON strings retain their required newline escapes. Display formatting does not rewrite stored records.

New stored JSON records use two-space indentation. Later targeted edits preserve readable indentation in multiline files while leaving untouched fields and records unchanged. Existing compact records retain their formatting; historical files are not bulk-reformatted. JSON still escapes newlines inside string fields, and machine output remains compact.

A targeted write has `schema_version: 1`, `interface: targeted-recording-v1`, the observed `contract`, `change_id`, `expected_revision`, `reads: [{path, identity}]`, and `operation: {op, target, values}`. Batch replaces operation with operations. Use the read result's exact record_contract and revision, and subject inspection's identities; the CLI does not substitute newly observed content for the actor's decision basis. Each command's --help gives its exact selectors and fields. The CLI constructs registry entries and serialized bytes and preserves omitted fields, neighbors and narrative. Newly created supporting records require explicit applicability; actor judgments and dispositions are never inferred.

Use `change create` only with explicit new-change authority, an absent root and contract rigorloop-records-v3. New records are change.json, reviews/<id>.json, evidence.json, material-decisions.json and success-only verify-report.json. Retired stored formats are unsupported runtime input and reject without fallback or mutation. Historical records remain unchanged archival evidence. V2 and v3 have packaged schemas/templates; targeted transport has its own targeted-recording-v1.schema.json. Templates illustrate stored shapes, not normal full-file write requests or approval. Create docs/changes/ before creating an absent change root.

Normal writes validate and optionally support --dry-run; preview reserves nothing. Results are compact and storage-only. Saved/unchanged/valid/inspected use exit 0, rejected 2, conflict 3, busy 4 and recovery-required 5. Reread and reassess conflicts instead of retry-merging. Observation summaries disclose omitted detail; observations show retrieves bounded detail with revision and observation-identity checks. Diagnostic volume cannot prevent an otherwise valid correction. A saved judgment, failed check or completion claim does not justify downstream reliance.

V3 Review and Verify store `summary`, `assessment_scope`, `rationale` and `limitations`; Verify also stores `changes`. Reasons, limitations and changes are arrays of complete strings. Judgment, findings, actors, subjects and evidence retain their existing authoritative fields. Review/Verify v3 records do not store `body`; material decisions still do. The optional closed `verification_basis` belongs only to a Git/PR readiness assessment.

Use `review show ID --fields summary,rationale,limitations` or `verify show --fields changes,limitations` with the normal root/change/format selectors. Omitting `--fields` returns the full selected record. Explicit selection returns exact requested values with identity, applicability, revision, omissions and absent optional fields; `complete: true` describes retrieval, not a complete assessment read. Human output renders the same decoded values.

`review set ID` and `verify set` accept a nonempty subset of explanation fields through the normal request envelope. They replace whole fields, preserve omitted bytes, and reject stale revisions. They cannot change judgment, actors, subjects, findings or verification basis. Use complete assessment operations for reassessment and finding operations for explicit corrections. V3 findings preserve only ID immutability; v2 findings and all blockers retain immutable origins. Saving never approves, restores applicability or runs verification.

Primary requests remain schema 1. Results are schema 3 for the recognized new set commands, even for errors before store access; retained commands select schema 3 only after validated v3 selection, otherwise schema 2. Preserve the returned operation and dispatch by schema_version, status and operation. A schema-3 error does not prove that a v3 store exists. Advanced requests remain schema 2 and advanced results schema 1.

Advanced `record-store inspect|check|record|recover` remains for diagnostics, complete explicit restoration and persistence maintenance. New stores require v3; existing v2 stores retain read/write/recovery support without migration. The independently versioned advanced result schema 1 and targeted-recording-v1 transport remain supported. Advanced replacements contain exact complete bytes under the selected stored version, while primary writes construct bytes. Both share containment, conflict and recovery protections. For interrupted storage use `record-store recover --root PATH --change ID --transaction ID --expected-recovery DIGEST --action restore|complete --format json` with one explicit action. Do not edit records with external tools during save/recovery; the documented limitation for external edits after the final identity check is unchanged.

The retired new-change, compact and lifecycle command families reject before request processing or side effects. Use v3 `change create` with explicit authority for new work. Recovery classifies the journal's recorded format selector and saved before/candidate/write/read basis; supported consistent v2/v3 transactions recover, including initial creation with no current manifest. Retired, unknown, inconsistent or ambiguous bases stop before restore/complete writes and preserve evidence. Journal selector 1 selects retired v1; the advanced result's schema 1 is independent. Never change a discriminator to simulate recovery or rollback.

### Other command families

```bash
rigorloop --help
rigorloop version
rigorloop init codex|claude [--force] [--from-archive <path>] [--dry-run] [--json]
rigorloop workflow-context [--change <id>] [--format human|json]
rigorloop logs path [--format human|json]
rigorloop logs show <invocation-id> [--format human|json]
```

`workflow-context` returns factual schema-2 discovery, never eligibility, an authoritative next stage or implicit change selection. It classifies current v2/v3 manifests, malformed or ambiguous current stores, and unrelated YAML-only archives without running legacy validators. Explicit targets avoid unrelated enumeration. Limits are inclusive: 1,024 directories, 64 candidates and an 8 MiB response budget. Exceeding a bound reports incomplete scope and limit-exceeded without silent truncation. An optional root `rigorloop.workflow.yaml` may override supported artifact locations; retired record-slot overrides, unsafe paths and invalid configuration fail closed. Use primary context/show for complete selected current-record content.

## Local CLI logs and concise results

RigorLoop records privacy-bounded local JSON Lines diagnostics by default and prints console diagnostics at `error` level by default. Routine success is therefore quiet on stderr. Logs rotate at 5 MiB and retain `rigorloop.jsonl` plus four archives in the platform user-state directory; use `rigorloop logs path` to locate it and `rigorloop logs show <invocation-id>` for exact lookup.

For historical commands, use `--no-file-log` or `RIGORLOOP_FILE_LOG=off` to disable file logging. Set `--file-log-level debug|info|warning|error` and `--console-log-level debug|info|warning|error|off` for one invocation; the matching environment variables are `RIGORLOOP_FILE_LOG_LEVEL` and `RIGORLOOP_CONSOLE_LOG_LEVEL`. `RIGORLOOP_LOG_DIR` accepts only an absolute, non-symlinked safe directory. Primary recording commands and the advanced `record-store` namespace must be the first argument; they reject these flags, ignore this logging environment and emit only their model-defined results.

Existing v0.4.x output defaults and `--json` remain unchanged. Agents can opt into compact results with `--format concise-json` or `--format concise-human`; complete results remain available with `--format detailed-json`. Local logs are diagnostics only and never authorize lifecycle transitions.

## Target Init

Use `rigorloop init codex|claude` to install verified skills into `.agents/skills/` or `.claude/skills/`. Package-bundled trusted metadata identifies the official archive. `--from-archive <path>` uses the same trusted metadata and verification for a local copy; it does not accept a substitute trust root.

Installation checks every candidate skill destination after archive verification. Any existing skill directory or declared file is a conflict, even if empty or identical. It lists the conflicts and installs nothing. Shared parent directories and unrelated skills are preserved.

The installer currently requires Linux with accessible `/proc/self/fd` directory descriptors and a filesystem supporting hard links. If those safety primitives are unavailable, installation stops without replacing existing skills. This requirement applies to fresh installation as well as force replacement.

Use `--force` to replace existing destination skills completely. Local changes and obsolete files within replaced skill directories leave the active installation. Originals remain at reported private paths outside skill discovery for separate inspection and cleanup. Symlinks, unsafe paths and intervening changes still stop installation. Partial failure reports what completed, what failed and what remains untouched; retry performs verification again and existing destinations still require explicit `--force`.

```bash
rigorloop init codex --dry-run --json
rigorloop init claude --from-archive ./rigorloop-adapter-claude-<version>.zip --json
rigorloop init codex --force
```

Dry-run reports preliminary destination checks and unperformed archive verification without downloading, extracting or writing. Installation does not read or write `rigorloop.yaml` or `rigorloop.lock`; their presence and contents do not affect installation. `--write-state` and `--adapter` are retired, and OpenCode is unsupported, including pinned and local-archive requests through this CLI.

Network failures report bounded diagnostics without proxy credentials. Configure Node's `NODE_USE_ENV_PROXY` or `--use-env-proxy` support when needed, or download the matching official archive and use `--from-archive`.

## New change recording

Use `rigorloop change create --help` for the targeted request shape, then submit the explicit v3-contract request with `--root PATH --input - --format json`. Add `--dry-run` for an optional preview. Creation requires explicit authority and an absent root; it grants no proposal, Design, review, Verify or PR judgment. The removed `new-change` scaffold is unsupported.

## Version Guidance

Use `@latest` for manual exploration. Use an explicit version such as `@0.3.5` for CI, onboarding docs, and repeatable agent setup.

## Source of Truth

npm is the CLI delivery channel. The canonical workflow sources, skills, specs, schemas, and release records live in the GitHub repository:

```text
https://github.com/xiongxianfei/rigorloop
```

## Upgrading retired authoring skills

The current package contains `design` and `route`; `spec`, `architecture` and `workflow` are retired. Candidates or installed inventories containing retired entries stop with exact-path diagnostics. `--force` replaces only current candidate skills and cannot delete unrelated retired entries. Inspect and preserve old content separately before reconciling those entries; the installer provides no migration or state-repair procedure. Historical release archives retain their original inventories.
