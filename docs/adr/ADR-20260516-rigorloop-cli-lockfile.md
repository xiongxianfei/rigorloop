# ADR-20260516-rigorloop-cli-lockfile: RigorLoop CLI Durable Lockfile Boundary

## Status

accepted

## Context

The first RigorLoop CLI slice intentionally emitted only planned lockfile content. That kept `rigorloop.lock` from becoming durable project state before the repository had an approved contract for what the lockfile owns, how hashes are computed, and when the file may be updated.

The approved lockfile spec now defines a strict `schema_version: 1` document shape, generated adapter entries, `rigorloop-tree-hash-v1`, network and local archive source semantics, drift behavior, and unknown-field blocking. The architecture decision is how the CLI package owns lockfile creation and update without weakening the existing source-of-truth boundary between canonical repository content, release artifacts, generated adapter output, and downstream project state.

## Decision

Allow the `@xiongxianfei/rigorloop` CLI package to write durable `rigorloop.lock` only for the approved first lockfile-writing surface:

```text
rigorloop init --adapter codex
rigorloop init --adapter codex --from-archive <path>
```

The lockfile records verified generated Codex adapter output state in a downstream project. It does not become canonical workflow content, canonical skill content, canonical adapter metadata, or release evidence.

The CLI owns lockfile serialization, validation, drift comparison, and write ordering for this surface:

- parse and validate an existing lockfile before mutating generated output;
- block unknown top-level sections, unknown fields, unsupported schemas, unsupported adapters, unsupported source values, and unsupported tree hash algorithms;
- verify the Codex archive and installed `.agents/skills` tree before writing an entry that claims installation success;
- compute `rigorloop-tree-hash-v1` from the installed generated output tree;
- write deterministic UTF-8/LF YAML with sorted adapter entries;
- record `source: release-archive` for network downloads and `source: local-archive` for `--from-archive` installs;
- record only the local archive basename for local installs, never absolute local paths;
- update only the CLI-owned package version, manifest hash, and matching Codex adapter entry in supported lockfiles;
- refuse drifted or unsupported existing state before destructive replacement unless a later spec defines repair or migration behavior.

Partial-failure ordering is conservative. The CLI must not write or update `rigorloop.lock` until adapter archive verification, extraction safety checks, generated-output mutation, and installed-tree verification have succeeded. If lockfile writing fails after adapter installation, the command reports the lockfile failure explicitly and must not claim that durable lockfile state was recorded.

## Alternatives considered

### Keep `rigorloop.lock` as planned output only

Rejected for the lockfile-enabled slice because the approved spec authorizes durable lockfile writes after verification. Keeping planned-only output would leave projects without drift detection or reproducible generated-output state.

### Treat local archive installs as `source: release-archive`

Rejected because the lockfile should record the install delivery mode. Both delivery modes use bundled official metadata as the trust root, but they are operationally different and should remain observable.

### Preserve unknown fields in the first lockfile schema

Rejected for the first slice because preserving unknown YAML byte-for-byte would add migration complexity and create false confidence. Unknown lockfile shape blocks before mutation until a later migration or preservation spec defines otherwise.

### Let `--force` replace lockfiles

Rejected because forced lockfile replacement would make durable generated-output state easy to erase without an approved recovery or repair contract.

## Consequences

- The CLI package becomes the sole writer of first-slice `rigorloop.lock` state.
- Lockfile support adds a parser/serializer and validation boundary to the CLI package, but does not move canonical workflow, skills, schemas, or release metadata into downstream projects.
- Existing first-slice projects without `rigorloop.lock` remain valid; the first successful lockfile-enabled Codex init may create the file.
- Supported lockfiles are deterministic and reviewable as text.
- Unknown or future lockfile shapes block instead of being silently rewritten.
- Drift checks protect generated adapter output before destructive replacement.
- Failed archive verification, tree-hash verification, mutation safety checks, or manifest validation must not update the lockfile.
- A later spec is required for lockfile migration, repair, status, validate integration, non-Codex adapters, or generated workflow output entries.

## Follow-up

- Update the canonical architecture package to record the lockfile ownership, runtime flow, deployment boundary, quality requirements, and risks.
- Create architecture-review evidence for this ADR and canonical package update.
- Create the lockfile test spec only after architecture-review approves the design.
