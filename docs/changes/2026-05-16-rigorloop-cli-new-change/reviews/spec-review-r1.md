# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/rigorloop-cli-new-change.md
Reviewed artifact: specs/rigorloop-cli-new-change.md
Review date: 2026-05-16
Recording status: recorded
Status: changes-requested

## Scope

Reviewed the draft `rigorloop new-change` CLI contract against the accepted scaffolding CLI proposal, the approved first-slice CLI command contract, the approved lockfile boundary, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, and `schemas/change.schema.json`.

The review focused on whether the spec is precise enough for architecture, test-spec, and implementation without guessing. No implementation code was reviewed.

## Dimension Results

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | block | Public option value domains for `--type` and `--risk` are not defined. |
| Normative language | concern | Most requirements are testable, but minimal-profile warning behavior is only `SHOULD` while acceptance requires it, and placeholder lifecycle language needs a stricter contract. |
| Completeness | concern | Normal, dry-run, path conflict, and no-overwrite cases are covered, but partial-write failure handling and placeholder lifecycle semantics are incomplete. |
| Testability | block | Tests cannot assert accepted or rejected `--type`/`--risk` values without inventing rules. |
| Examples | pass | Examples are concrete and match the intended command surface. |
| Compatibility | concern | The spec preserves existing change roots and lockfile behavior, but the standard profile may create a durable-looking `explain_change` artifact before durable reasoning exists. |
| Observability | pass | Human and JSON outputs, warnings, actions, artifacts, and stable exit classes are covered. |
| Security/privacy | concern | Path traversal and secret leakage are covered; symlink and partial-write outcomes should be made explicit during revision. |
| Non-goals | pass | Exclusions for `status`, `validate`, workflow YAML, lockfile writes, adapters, and PR readiness are explicit. |
| Acceptance criteria | concern | AC2 requires a minimal-profile warning, but the corresponding requirement is only a `SHOULD`. |

## Findings

### SR1-F1: Public option value domains are underdefined

Finding ID: SR1-F1

Severity: blocking

Location: `specs/rigorloop-cli-new-change.md:130`, `specs/rigorloop-cli-new-change.md:134`, `specs/rigorloop-cli-new-change.md:193`

Evidence: `R5` says `--type <classification>` sets the `classification` field, and `R7` says `--risk <risk>` sets the `risk` field. The spec defines defaults in `R6` and `R8`, but it never defines allowed values, allowed characters, length limits, case normalization, or error behavior for invalid values. `R37` only says values must be escaped or quoted so YAML shape is not corrupted. Because `--type` and `--risk` are public command options and persisted into `change.yaml`, test-spec and implementation would have to invent whether values such as `High`, `security review`, `../x`, `""`, `medium/high`, or `workflow-governance-spec` are valid.

Required outcome: The spec must define first-slice value domains and invalid-value behavior for `--type` and `--risk`.

Safe resolution path: Add explicit requirements such as:

```md
`--type` MUST accept only lowercase classification tokens matching `[a-z][a-z0-9-]*`.
`--risk` MUST accept only `low`, `medium`, or `high`.
Invalid `--type` MUST return status `error`, exit code `4`, and error code `invalid-classification`.
Invalid `--risk` MUST return status `error`, exit code `4`, and error code `invalid-risk`.
```

If the intended model is free-form classification, define that instead with exact character and length rules, but do not leave it to implementation.

### SR1-F2: Standard-profile `explain-change.md` placeholder conflicts with durable reasoning semantics

Finding ID: SR1-F2

Severity: major

Location: `specs/rigorloop-cli-new-change.md:168`, `specs/rigorloop-cli-new-change.md:207`, `specs/rigorloop-cli-new-change.md:227`, `specs/rigorloop-workflow.md:684`, `specs/rigorloop-workflow.md:793`

Evidence: The workflow contract says the ordinary baseline non-trivial pack is `change.yaml` plus durable Markdown reasoning, and `change.yaml` `artifacts` records paths to durable Markdown artifacts that exist for the change. The draft spec makes the standard profile create `explain-change.md` as a draft placeholder and records it under `artifacts.explain_change`, while also saying the placeholder must not claim the `explain-change` stage has completed. That leaves an ambiguous public contract: downstream tools may treat `artifacts.explain_change` as durable rationale, while the placeholder says it is not final rationale.

Required outcome: The spec must decide how scaffolded placeholders interact with the workflow's durable reasoning and artifact mapping contract.

Safe resolution path: Choose one first-slice rule:

- simplest: standard profile creates only `change.yaml`, and a later spec adds optional `--with-explain-change-template`; or
- keep the placeholder but require a machine-checkable placeholder marker, require `artifacts.explain_change` to be omitted until the real explain-change stage replaces the placeholder, and require JSON `artifacts` to mark the placeholder as `draft`; or
- explicitly amend the workflow-facing contract in this spec so `artifacts.explain_change` may point at a draft scaffold, and define how `status`, `validate`, `verify`, and users distinguish draft placeholders from completed rationale.

Do not leave `artifacts.explain_change` looking final while the file content says it is not final.

### SR1-F3: Partial mutation failure behavior is incomplete

Finding ID: SR1-F3

Severity: major

Location: `specs/rigorloop-cli-new-change.md:245`, `specs/rigorloop-cli-new-change.md:273`, `specs/rigorloop-cli-new-change.md:378`

Evidence: `R46` and `R56` require a pre-mutation write plan and blocker handling before writes, but the command writes multiple directories and files. The error table says permission failure during mutation exits `1` unless classified as a mutation conflict, but the spec does not define what happens if directory creation succeeds and `change.yaml` or `explain-change.md` write fails afterward. It also does not define whether the command attempts rollback, leaves partial directories, reports partial writes in JSON `actions`, or guarantees file-write ordering.

Required outcome: The spec must define observable behavior for partial write failures after mutation begins.

Safe resolution path: Add a partial-failure contract such as:

```md
The command MUST write files only after all planned directories are created.
If a write fails after earlier mutations, the command MUST return status `error`, exit code `1`, include completed and failed actions in JSON, and name any filesystem paths that may have been created.
The command MUST NOT claim artifact-pack creation success unless all planned files are written.
The command MAY leave successfully created directories in place, but if it does, it MUST report them as done.
```

If atomic rollback is required instead, specify the rollback behavior and failure reporting explicitly.

## Requirement Notes

- `R1` through `R12`: mostly pass, except value domains for public options are incomplete.
- `R13` through `R19`: pass for change-id and path traversal boundaries.
- `R20` through `R26`: concern; the default standard placeholder needs a clearer lifecycle contract.
- `R27` through `R37`: block until `classification` and `risk` value domains are specified.
- `R38` through `R43`: concern; placeholder content is constrained, but its durable artifact status is ambiguous.
- `R44` through `R56`: concern; preflight mutation safety is good, but partial mutation failure behavior is incomplete.
- `R57` through `R70`: concern only for `R64`, which should be a `MUST` if AC2 remains as written.
- `R71` through `R76`: pass for no-overclaim and missing-manifest behavior.

## Recommendation

Changes requested.

No automatic downstream handoff is performed because this was a direct `spec-review` request.

Immediate next repository stage: spec.

Eventual test-spec readiness: not-ready.

Stop condition: revise `specs/rigorloop-cli-new-change.md` to resolve `SR1-F1`, `SR1-F2`, and `SR1-F3`, then rerun `spec-review`.
