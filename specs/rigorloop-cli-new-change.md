# RigorLoop CLI New Change

## Status

approved

## Related proposal

- [RigorLoop Scaffolding CLI and Machine-Readable Workflow](../docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md)
- Follow-up: `FU-005` in [follow-ups](../docs/follow-ups.md)
- Builds on: [RigorLoop CLI Package and Codex Init](rigorloop-cli-package-and-codex-init.md)
- Builds on: [RigorLoop CLI Lockfile](rigorloop-cli-lockfile.md)

## Goal and context

This spec defines the first implementable `rigorloop new-change` command contract for the existing `@xiongxianfei/rigorloop` package and `rigorloop` binary.

The command helps users create a change-local artifact pack under `docs/changes/<change-id>/` without needing to memorize repository paths or the first-release `change.yaml` shape. It is a scaffolding command only. It creates draft traceability artifacts; it does not accept proposals, complete reviews, verify branches, open PRs, or claim workflow readiness.

This spec intentionally does not define `rigorloop status`, `rigorloop validate`, workflow YAML canonicality, npm publication hardening, non-Codex adapters, lockfile migration, or generated workflow documentation.

## Glossary

- `change id`: the repository-local identifier used as the final path segment under `docs/changes/`.
- `change root`: the directory `docs/changes/<change-id>/`.
- `change metadata`: the YAML file `docs/changes/<change-id>/change.yaml`.
- `artifact pack`: the change root plus files scaffolded by `new-change`.
- `standard profile`: the default profile for ordinary non-trivial work; it creates `change.yaml` and uses normal success output.
- `minimal profile`: a smaller profile for intentionally lightweight or early work; it creates `change.yaml` and reports a durable-reasoning warning.

## Examples first

### Example E1: standard scaffold creates change metadata

Given a project has no `docs/changes/adapter-install-cli/`
When the user runs:

```bash
rigorloop new-change adapter-install-cli --title "Adapter install CLI" --type workflow
```

Then the command creates:

```text
docs/changes/adapter-install-cli/change.yaml
```

And `change.yaml` includes the required first-release fields
And the command does not claim that durable reasoning, review, verification, or PR readiness is complete.

### Example E2: minimal scaffold creates only change metadata

Given a project has no `docs/changes/docs-typo/`
When the user runs:

```bash
rigorloop new-change docs-typo --title "Fix docs typo" --type docs --profile minimal
```

Then the command creates only:

```text
docs/changes/docs-typo/change.yaml
```

And the command reports a warning that ordinary non-trivial workflow closeout still needs durable Markdown reasoning when applicable.

### Example E3: dry-run JSON reports every planned mutation

Given `docs/changes/new-feature/` does not exist
When the user runs:

```bash
rigorloop new-change new-feature --title "New feature" --dry-run --json
```

Then stdout contains JSON only
And `actions` reports planned creation of `docs`, `docs/changes`, `docs/changes/new-feature`, and `change.yaml`
And no files or directories are created.

### Example E4: existing change metadata is not overwritten

Given `docs/changes/new-feature/change.yaml` already exists
When the user runs:

```bash
rigorloop new-change new-feature --title "New feature"
```

Then the command blocks before mutation
And exits with code `5`
And reports the existing `change.yaml` path.

### Example E5: invalid change id is rejected before path planning

Given the user runs:

```bash
rigorloop new-change ../outside --title "Outside"
```

Then the command exits with code `4`
And reports invalid usage
And no filesystem paths are created.

## Requirements

### Command surface

R1. The command surface added by this spec MUST be:

```text
rigorloop new-change <change-id>
rigorloop new-change <change-id> --title <title>
rigorloop new-change <change-id> --type <classification>
rigorloop new-change <change-id> --risk <risk>
rigorloop new-change <change-id> --profile standard|minimal
rigorloop new-change <change-id> --dry-run
rigorloop new-change <change-id> --json
```

R2. `new-change` MUST run through the existing `rigorloop` binary in the existing `@xiongxianfei/rigorloop` package.

R3. `new-change` MUST require a positional `<change-id>`.

R4. `new-change` MUST require `--title <title>` in this first slice.

R5. `--type <classification>` MUST set the `classification` field in `change.yaml`.

R5a. `--type <classification>` MUST accept only lowercase classification tokens matching:

```text
[a-z][a-z0-9-]{0,63}
```

R5b. `--type` MUST reject empty values, uppercase values, whitespace, path separators, path traversal, URL-encoded path separators, and control characters.

R5c. Invalid `--type` values MUST return status `error`, exit code `4`, and error code `invalid-classification`.

R6. If `--type` is omitted, the command MUST use `classification: default`.

R7. `--risk <risk>` MUST set the `risk` field in `change.yaml`.

R7a. `--risk <risk>` MUST accept only `low`, `medium`, or `high`.

R7b. Invalid `--risk` values MUST return status `error`, exit code `4`, and error code `invalid-risk`.

R8. If `--risk` is omitted, the command MUST use `risk: medium`.

R9. First-slice supported profiles MUST be `standard` and `minimal`.

R10. If `--profile` is omitted, the command MUST use `standard`.

R11. Unknown options, missing option values, missing `<change-id>`, or missing `--title` MUST exit with code `4`.

R12. `rigorloop --help` MUST include `new-change` only after the command is implemented.

### Change id and path rules

R13. `<change-id>` MUST be a single repository-relative path segment.

R14. `<change-id>` MUST match this shape:

```text
[a-z0-9](?:[a-z0-9-]*[a-z0-9])?
```

R15. A one-character alphanumeric `<change-id>` MAY be accepted.

R16. `<change-id>` MUST NOT contain `.`, `/`, `\`, `:`, a leading dash, whitespace, control characters, URL encoding, or path traversal.

R17. The target change root MUST be `docs/changes/<change-id>/`.

R18. The command MUST NOT create or write outside the target change root except for missing parent directories `docs/` and `docs/changes/`.

R19. Invalid change ids MUST be rejected before filesystem mutation with status `error`, exit code `4`, and error code `invalid-change-id`.

### Generated artifact pack

R20. The standard profile MUST create `docs/changes/<change-id>/change.yaml`.

R21. The standard profile MUST NOT create `docs/changes/<change-id>/explain-change.md` in this first slice.

R22. The minimal profile MUST create `docs/changes/<change-id>/change.yaml`.

R23. The minimal profile MUST NOT create `explain-change.md`.

R24. The command MUST NOT create review records, review logs, review-resolution files, verify reports, proposal files, spec files, plan files, architecture files, ADRs, or PR-body files in this first slice.

R25. The command MUST NOT create or update `rigorloop.yaml` or `rigorloop.lock`.

R26. The command MUST NOT install adapters or perform network access.

### `change.yaml` shape

R27. Generated `change.yaml` MUST be YAML.

R28. Generated `change.yaml` MUST be UTF-8 text with LF line endings.

R29. Generated `change.yaml` MUST use deterministic field order.

R30. Generated `change.yaml` MUST include these top-level fields:

```yaml
change_id: "<change-id>"
title: "<title>"
classification: "<classification>"
risk: "<risk>"
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  status: pending
  unresolved_items: 0
```

R31. For the standard profile, `artifacts` MUST be empty unless a later approved spec adds explicit artifact creation options.

R32. For the minimal profile, `artifacts` MUST be empty unless a later approved spec adds explicit artifact options.

R33. Generated metadata MUST satisfy the first-release `change.yaml` schema shape used by `schemas/change.schema.json`.

R34. Generated metadata MUST NOT claim implementation completion, review completion, verification completion, PR readiness, proposal acceptance, spec approval, architecture approval, plan approval, or workflow completion.

R35. Generated metadata MAY contain empty arrays for `requirements`, `tests`, `validation`, and `changed_files` because `new-change` scaffolds the pack before those facts are known.

R36. Generated metadata MUST NOT include machine-local absolute paths, usernames, hostnames, temp directories, tokens, environment variable values, or command stderr.

R37. The command MUST escape or quote YAML scalar values so title, classification, and risk cannot corrupt the generated YAML shape.

### Deferred artifact templates

R38. The first slice MUST NOT create durable Markdown placeholder files.

R39. A later approved spec MAY add optional artifact template flags such as `--with-explain-change-template`.

R40. Any later placeholder or template spec MUST define placeholder markers, lifecycle semantics, validator behavior, replacement behavior, and artifact mapping rules before implementation.

R41. `new-change` MUST NOT record artifact paths in `change.yaml` for files it does not create.

R42. `new-change` MUST NOT record `artifacts.explain_change` in this first slice.

R43. The absence of `explain-change.md` after `new-change` MUST NOT weaken the workflow requirement that ordinary non-trivial closeout needs durable Markdown reasoning when applicable.

### Write plan and mutation safety

R44. `new-change` MUST default to non-destructive behavior.

R45. `--dry-run` MUST perform no file writes, directory creation, deletion, or modification.

R46. Before mutating, `new-change` MUST compute a write plan that identifies every file and directory it intends to create, skip, or block.

R47. The write plan MUST include parent directories that would be created, including `docs`, `docs/changes`, and `docs/changes/<change-id>`.

R48. The deterministic action order MUST be:

```text
docs
docs/changes
docs/changes/<change-id>
docs/changes/<change-id>/change.yaml
```

R49. The first-slice write plan MUST NOT include an `explain-change.md` action.

R50. Existing directories needed by the plan MUST be reported as existing or skipped rather than hidden.

R51. If an expected directory path exists as a file or other non-directory entry, the command MUST block with exit code `5`.

R51a. If any planned directory path is a symlink, the command MUST block before mutation with status `blocked`, exit code `5`, and blocker code `path-not-directory`.

R51b. The command MUST NOT follow symlinks for planned write paths in this first slice.

R52. If a planned file already exists, the command MUST block with exit code `5`.

R53. `new-change` MUST NOT overwrite existing files in this first slice.

R54. `new-change` MUST NOT delete files or directories in this first slice.

R55. `--force` MUST NOT be supported for `new-change` in this first slice.

R56. A blocked mutation MUST happen before any filesystem writes.

R56a. The command MUST preflight all planned paths before mutation.

R56b. The command MUST create directories before writing files.

R56c. The command MUST write files in deterministic action order.

R56d. If a write fails after earlier mutations, the command MUST return status `error`.

R56e. If a write fails after earlier mutations, the command MUST exit with code `1` unless the failure is classified before writing as a mutation conflict.

R56f. If a write fails after earlier mutations, JSON `actions` MUST mark completed mutations as `done`.

R56g. If a write fails after earlier mutations, JSON `actions` MUST mark the failed path as `failed`.

R56h. If a write fails after earlier mutations, JSON output MUST include an `errors[]` entry naming the failed path.

R56i. If a write fails after earlier mutations, the command MUST NOT claim artifact-pack creation success.

R56j. The command MAY leave already-created directories in place after partial failure, but it MUST report them.

R56k. The first slice does not guarantee atomic rollback.

### JSON and exit contract

R57. `new-change --json` MUST reuse the stable CLI JSON envelope:

```json
{
  "schema_version": 1,
  "command": "new-change",
  "package": {
    "name": "@xiongxianfei/rigorloop",
    "version": "0.1.3"
  },
  "cwd": "/path/to/project",
  "status": "success",
  "summary": "",
  "actions": [],
  "artifacts": [],
  "blockers": [],
  "warnings": [],
  "errors": [],
  "diagnostics": {}
}
```

R58. `new-change --json` MUST print JSON only to stdout.

R59. JSON `status` MUST be one of `success`, `warning`, `blocked`, or `error`.

R60. Exit codes MUST use the existing CLI mapping:

| Exit code | Meaning |
|---|---|
| `0` | success or warning |
| `2` | blocked |
| `3` | validation failed |
| `4` | invalid usage or invalid config |
| `5` | mutation conflict or overwrite refused |
| `1` | internal or unexpected error |

R61. Invalid command usage MUST return status `error`, exit code `4`, and an `errors[]` entry.

R62. Mutation conflicts and overwrite refusals MUST return status `blocked`, exit code `5`, and a `blockers[]` entry.

R63. Successful standard-profile creation MUST return status `success`.

R64. Successful minimal-profile creation MUST return status `warning` with warning code `durable-reasoning-not-scaffolded`.

R65. JSON `actions` entries MUST use stable fields `type`, `path`, `status`, and `reason`.

R66. JSON `artifacts` entries MUST use stable fields `path`, `kind`, and `status`.

R67. JSON `blockers`, `warnings`, and `errors` entries MUST use stable fields `code`, `message`, `path` when path-specific, and `next_action` when useful.

R68. JSON output MUST include a `change` object with `change_id`, `root`, `metadata_path`, and `profile`.

R69. In human mode, stdout MUST contain a concise human summary and MUST NOT print JSON fragments as routine output.

R70. `--quiet`, `--debug`, `--no-color`, and `NO_COLOR` behavior MUST match the existing CLI contract.

### State and invariants

R71. `new-change` creates draft artifact locations; it MUST NOT advance lifecycle stage state.

R72. File existence after `new-change` MUST NOT imply that any downstream lifecycle stage is complete.

R73. The command MUST be idempotent only in the sense that rerunning against existing generated paths blocks safely; it MUST NOT silently treat existing metadata as success.

R74. The command MUST NOT inspect Git remotes, branch names, hosted CI, or PR state.

R75. The command MUST NOT require `rigorloop.yaml` to exist.

R76. If `rigorloop.yaml` is missing, the command MAY warn but MUST NOT block solely for that reason.

## Inputs and outputs

### Inputs

- Positional `<change-id>`.
- Required `--title <title>`.
- Optional `--type <classification>`.
- Optional `--risk <risk>`.
- Optional `--profile standard|minimal`.
- Optional `--dry-run`.
- Optional `--json`.
- Existing global output flags `--quiet`, `--debug`, and `--no-color`.

### Outputs

- `docs/changes/<change-id>/change.yaml`.
- Human output or JSON output using the stable CLI envelope.
- No lockfile writes.
- No network output.

## Error and boundary behavior

1. Missing `<change-id>` returns `error`, exit `4`, code `missing-change-id`.
2. Missing `--title` returns `error`, exit `4`, code `missing-title`.
3. Invalid `<change-id>` returns `error`, exit `4`, code `invalid-change-id`.
4. Unsupported profile returns `error`, exit `4`, code `unsupported-profile`.
5. Invalid `--type` returns `error`, exit `4`, code `invalid-classification`.
6. Invalid `--risk` returns `error`, exit `4`, code `invalid-risk`.
7. Existing `change.yaml` returns `blocked`, exit `5`, code `path-exists`.
8. Directory path occupied by a file returns `blocked`, exit `5`, code `path-not-directory`.
9. Symlink at any planned directory path returns `blocked`, exit `5`, code `path-not-directory`.
10. Permission failure during mutation returns `error`, exit `1` unless the implementation can classify it as an expected mutation conflict before writing.
11. YAML serialization failure returns `error`, exit `1`.
12. Schema-shape generation failure discovered before writing returns `error`, exit `4`.
13. Partial write failure after earlier mutations returns `error`, exit `1`, and reports completed and failed actions.

## Compatibility and migration

- This spec extends the first CLI package command surface; it supersedes the earlier first-slice help limitation only for the now-specified `new-change` command.
- Existing projects without `rigorloop.yaml` remain compatible.
- Existing projects with `docs/changes/` remain compatible as long as the selected change id path is unused.
- Existing change roots are not migrated or rewritten.
- No existing `rigorloop.lock` behavior changes.
- No public npm publication is authorized by this spec.

## Observability

- Human output must name the created or planned change root.
- JSON output must include planned or completed actions for every filesystem path affected by the command.
- JSON output must include warning details for minimal profile durable-reasoning omissions.
- Debug output may include parser and write-plan details but must not include secrets or environment dumps.
- The command does not emit metrics, traces, or audit events in this slice.

## Security and privacy

- The command must reject path traversal and absolute or multi-segment change ids.
- The command must not perform network access.
- The command must not include secrets, environment variables, usernames, hostnames, or temp directories in generated artifacts.
- The command must not follow symlinks to write outside the intended change root.
- The command must not create files outside the repository-relative `docs/changes/<change-id>/` tree except missing parent directories.

## Accessibility and UX

- Human output must be concise and actionable.
- Error messages must name the invalid option or conflicting path.
- JSON mode must be stable for agents and CI.
- `--profile minimal` must be available for users who intentionally want only the metadata scaffold, but it must not weaken downstream workflow closeout requirements.

## Performance expectations

- The command must complete using local filesystem inspection only.
- Runtime should be proportional to the number of scaffolded paths, not to repository size.
- The command must not run full repository validation.

## Edge cases

1. `docs/` is absent: plan and create it unless dry-run.
2. `docs/` exists as a file: block with exit `5`.
3. `docs/changes/` is absent: plan and create it unless dry-run.
4. `docs/changes/` exists as a file: block with exit `5`.
5. Change root exists but is empty: create planned files if they do not already exist.
6. Change root exists with unrelated files: create planned files only if no planned file conflicts.
7. `change.yaml` exists: block with exit `5`.
8. Existing `explain-change.md`: do not touch it; still block if `change.yaml` conflicts.
9. Symlink at `docs`, `docs/changes`, or the change root: block with exit `5`.
10. Title contains quotes or colon characters: generate valid YAML.
11. `--json --quiet` is supplied: JSON output remains present and stable.
12. `--dry-run` with existing conflicts: report blocked plan and write nothing.
13. Directory creation succeeds but file write fails: report completed directory actions, failed file action, and no artifact-pack success.

## Non-goals

- No implementation of `status`, `validate`, workflow YAML, workflow rendering, or frozen checks.
- No creation of proposals, specs, plans, architecture docs, ADRs, review records, review logs, review resolutions, verify reports, or PR bodies.
- No lifecycle status advancement or readiness claim.
- No change metadata validation command execution.
- No lockfile creation or update.
- No adapter install behavior.
- No project-wide scans beyond the planned path checks.
- No generated docs or diagrams.
- No public npm publication or release hardening.

## Acceptance criteria

- AC1. `rigorloop new-change <id> --title <title>` creates a valid standard artifact pack with `change.yaml` only.
- AC2. `--profile minimal` creates only `change.yaml` and reports the durable-reasoning warning.
- AC3. `--dry-run --json` reports every planned directory and file action without writing anything.
- AC4. Existing planned files block with exit `5` before mutation.
- AC5. Invalid change ids and missing titles exit `4`.
- AC6. Generated `change.yaml` passes the repository change metadata schema validation.
- AC7. Generated files use deterministic UTF-8/LF content.
- AC8. The command does not create `rigorloop.lock`, install adapters, or perform network access.
- AC9. The command does not claim proposal acceptance, review completion, verification, or PR readiness.
- AC10. `docs/follow-ups.md` continues to track later command surfaces separately.
- AC11. Invalid `--type` and `--risk` values exit `4` with field-specific error codes.
- AC12. Partial write failures report completed and failed actions without claiming success.
- AC13. Planned directory symlinks block before mutation.

## Open questions

None.

## Next artifacts

- Implement M1 from `docs/plans/2026-05-16-rigorloop-cli-new-change.md`.

## Follow-on artifacts

- Spec-review: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r1.md`
- Spec-review rerun: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/spec-review-r2.md`
- Architecture-review: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md`
- Plan: `docs/plans/2026-05-16-rigorloop-cli-new-change.md`
- Plan-review: `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/plan-review-r1.md`
- Test spec: `specs/rigorloop-cli-new-change.test.md`

## Readiness

Approved by `spec-review-r2`; downstream architecture-review and plan-review are complete, and the active test spec is ready to guide M1 implementation.
