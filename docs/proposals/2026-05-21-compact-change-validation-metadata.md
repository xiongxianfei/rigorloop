# Compact Change Validation Metadata

## Status

accepted

## Problem

RigorLoop change metadata currently stores validation evidence in a verbose transcript-like shape. A non-trivial `change.yaml` can accumulate dozens of entries that repeat long commands, long change IDs, near-identical lifecycle paths, and prose-encoded pass results. The common reader has to scan a large list to recover a small amount of information: which validation bundles ran, whether they passed, what stages were validated, and whether anything remains blocked.

This is the same class of problem as noisy script output, but the storage medium is different. Terminal output is transient and can be suppressed. `change.yaml` is durable evidence, so the goal is not to hide validation evidence. The goal is to store it in a shape where the common read is cheap and the full detail remains recoverable.

The current shape has three recurring problems:

| Problem | Effect |
| --- | --- |
| Long change IDs repeated in every command path | Large byte cost and poor scanability. |
| Same validation commands repeated after many stages | The artifact scales with validation reruns rather than information value. |
| Pass results encoded as long prose-like strings | Counts and state are hard to parse and easy to drift. |

Because `validate-change-metadata.py` may depend on the current shape, this cannot be solved by hand-editing a single `change.yaml`. It is a change-metadata contract update and should proceed through proposal, review, spec, test-spec, plan, implementation, review, and verification.

## Goals

- Define a compact validation-evidence model for `change.yaml`.
- Preserve durable audit value while reducing common-read verbosity.
- Store validation bundles once and reference them by stable ID.
- Store change-local paths through reusable variables instead of repeating the full change ID.
- Replace prose-encoded pass strings with structured result fields and counts.
- Allow stage-level validation evidence to summarize repeated standard bundles.
- Preserve access to deep validation transcripts when forensic detail is needed.
- Maintain backward compatibility with existing verbose `change.yaml` files.
- Update validators to read both legacy and compact forms during migration.
- Prevent validation-summary compression from changing selected checks, command exit behavior, failure detection, or required validation evidence.

## Non-goals

- Do not remove validation evidence.
- Do not weaken lifecycle, metadata, review-artifact, whitespace, generated-output, or selected-CI validation requirements.
- Do not hide failures or unresolved blockers behind summary fields.
- Do not change what commands are selected by validation selectors.
- Do not change the semantics of review records, review logs, review-resolution, or artifact lifecycle validation.
- Do not require immediate migration of every historical `change.yaml`.
- Do not make external CI logs the only source of validation proof.
- Do not optimize for byte count at the cost of auditability.
- Do not change artifact locations outside the change-metadata validation surface unless the spec later shows that a location change is needed.

## Vision fit

fits the current vision

RigorLoop's vision depends on durable artifacts that let reviewers reconstruct what happened without chat history. Compact validation metadata supports that vision by making the common evidence surface easier to inspect while preserving the ability to recover full validation details.

The proposal is falsified if the compact shape causes any of these outcomes:

```text
- a reviewer cannot reconstruct which validation bundles ran;
- a reviewer cannot tell which stages were validated;
- a failed or blocked validation is summarized as pass;
- selected validation checks change because of metadata compression;
- deep validation detail becomes unrecoverable when needed;
- validators accept ambiguous or incomplete validation evidence;
- old valid change metadata becomes invalid without a migration path.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Reduce noisy `change.yaml` validation evidence | in scope | Problem, Goals |
| Keep durable audit trail | in scope | Goals, Validation transcript policy |
| Define validation bundles once | in scope | Recommended direction |
| Use path variables for repeated change IDs | in scope | Path variable model |
| Structure result counts instead of prose strings | in scope | Structured counts |
| Move full transcript out of common metadata | in scope | Validation transcript policy |
| Preserve validator compatibility | in scope | Compatibility and migration |
| Treat this as schema work, not a freehand edit | in scope | Problem, Rollout and rollback |
| Avoid weakening selected validation checks or failure detection | in scope | Goals, Non-goals, Risks and mitigations |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact validation section shape | core to this proposal | This is the central contract decision. |
| Path variable model | core to this proposal | It addresses repeated change IDs and reconstructable paths. |
| Validation bundle model | core to this proposal | It addresses repeated command definitions. |
| Structured stage results and counts | core to this proposal | It replaces prose-encoded pass strings with queryable fields. |
| Legacy validator compatibility | same-slice dependency | Compatibility is required for safe adoption. |
| Compact valid and invalid fixtures | first-slice candidate | Fixtures prove the schema and validator behavior. |
| Optional transcript references | first-slice candidate | The summary/transcript split is useful, but the exact transcript format can remain minimal. |
| Bulk migration of historical `change.yaml` files | separate proposal | Mass migration has separate risk and review cost. |
| Standard `change.validation-log.yaml` transcript format | separate proposal | The first slice can validate references without standardizing every transcript field. |
| CLI scaffolding that writes compact metadata | deferable follow-up | Scaffolding is useful after the compact shape is approved. |
| Review-artifact count cross-checking | same-slice dependency | Structured counts become durable evidence, so the validator should bind them to review-artifact parser output instead of allowing drift. |

## Context

Existing `change.yaml` validation entries can become a durable version of a noisy terminal log: dozens of near-identical validation records, repeated long commands, repeated change IDs, and verbose pass strings. Recent script-output optimization work uses a related principle:

```text
Output volume should scale with the information the reader needs,
not the amount of work performed.
```

For durable metadata, the corresponding shape is:

```text
common read:
  compact summary, bundles, stage results, final counts, blockers

deep read:
  reconstructable commands, expanded paths, optional transcript file
```

## Options Considered

### Option 1: Keep the current verbose validation list

Pros:

- No schema work.
- Existing validators continue unchanged.
- Full commands are always visible inline.

Cons:

- `change.yaml` continues to grow with reruns.
- Common inspection remains expensive.
- Repeated command and path strings obscure actual state.
- Result strings remain hard to parse.

### Option 2: Suppress validation detail entirely

Pros:

- Smallest metadata.
- Easy to read.

Cons:

- Loses durable audit value.
- Reviewers cannot reconstruct what ran.
- Violates RigorLoop's evidence-first model.

### Option 3: Keep current shape but shorten result strings

Pros:

- Small improvement.
- Lower migration risk than a schema change.

Cons:

- Does not address repeated commands or repeated change IDs.
- Still scales with reruns rather than information value.
- Does not create a structured validation model.

### Option 4: Add compact validation bundles and structured stage results

Pros:

- Stores command bundles once.
- Stores paths through reusable variables.
- Keeps per-stage pass/fail evidence.
- Makes counts machine-readable.
- Preserves auditability through reconstructable commands and optional transcript files.
- Allows backward-compatible schema migration.

Cons:

- Requires schema, test-spec, and validator work.
- Requires migration or dual-read support.
- Requires care to avoid hiding failures.

### Option 5: Split all validation logs into a separate file and keep only final status in `change.yaml`

Pros:

- Smallest common `change.yaml`.
- Deep transcript is retained elsewhere.

Cons:

- Too aggressive for the first slice.
- Reviewers may lose stage-level summary in the common artifact.
- Requires stronger artifact-linking and lifecycle validation.

## Recommended Direction

Choose Option 4, with optional transcript splitting from Option 5 as a controlled extension.

Define a compact validation-evidence shape that:

```text
- declares path variables once;
- declares validation bundles once;
- records stage-level validation events with bundle references;
- stores structured result and count fields;
- stores final validation summary;
- optionally links to a separate full transcript file.
```

Use explicit `schema_version: 2` for compact validation metadata. The dual-read validator needs to distinguish legacy and compact files during migration; branching on a declared version is deterministic, while detecting shape by field presence is heuristic and fails on ambiguous mid-migration files.

## Proposed Compact Shape

Tentative `change.yaml` direction:

```yaml
schema_version: 2

change:
  id: 2026-05-21-review-skill-family-consistency-parser-owned-finding-shape

path_vars:
  change_id: 2026-05-21-review-skill-family-consistency-parser-owned-finding-shape
  slug: review-skill-family-consistency-parser-owned-finding-shape
  change_root: docs/changes/{change_id}
  proposal: docs/proposals/{change_id}.md
  spec: specs/{slug}.md
  test_spec: specs/{slug}.test.md
  plan: docs/plans/{change_id}.md

validation_bundles:
  lifecycle:
    command: python scripts/validate-artifact-lifecycle.py --mode explicit-paths
  metadata:
    command: python scripts/validate-change-metadata.py {change_root}/change.yaml
  reviews:
    command: python scripts/validate-review-artifacts.py --mode closeout {change_root}
  whitespace:
    command: git diff --check --

validation_events:
  - stage: proposal-review-r1
    bundles: [lifecycle, metadata, reviews, whitespace]
    paths_added:
      lifecycle:
        - docs/proposals/{change_id}.md
    result: pass
    counts:
      reviews: 1
      findings: 0
      log_entries: 1
      resolution_entries: 0
    evidence:
      transcript: null

  - stage: spec-review-r1
    bundles: [lifecycle, metadata, reviews, whitespace]
    paths_added:
      lifecycle:
        - specs/{slug}.md
        - docs/changes/{change_id}/review-log.md
        - docs/changes/{change_id}/reviews/spec-review-r1.md
    result: pass
    counts:
      reviews: 2
      findings: 1
      log_entries: 2
      resolution_entries: 1
    evidence:
      transcript: null

validation_summary:
  all_passed: true
  stages_validated:
    - proposal-review-r1
    - spec-review-r1
  final_counts:
    reviews: 2
    findings: 1
    log_entries: 2
    resolution_entries: 1
  open_validation_blockers: []
```

## Validation Bundle Model

A validation bundle is a named command family.

| Field | Required? | Meaning |
| --- | ---: | --- |
| `command` | yes | Base command or command template. |
| `description` | optional | Human-readable purpose. |
| `expands_with` | conditional | Path or stage data used to reconstruct full command when the bundle expands from event data. |
| `required_for` | optional | Stages or conditions where bundle is expected. |

Example:

```yaml
validation_bundles:
  lifecycle:
    command: python scripts/validate-artifact-lifecycle.py --mode explicit-paths
    expands_with: validation_events[].paths_added.lifecycle
    required_for: formal lifecycle artifact changes
```

For path-expanding bundles, exact command reconstruction should be pinned rather than best-effort. The spec should require each validation event to record `paths_added` for a bundle whenever that bundle's resolved path set changes from the prior event. The resolved path set at any event is the ordered accumulation of that bundle's `paths_added` entries up to and including the event. If the path set does not change, the event can omit `paths_added` for that bundle. This keeps the common form compact while letting a reviewer reconstruct the exact command and path set that ran at each stage.

## Stage Event Model

Each validation event records one stage-level validation result.

| Field | Required? | Meaning |
| --- | ---: | --- |
| `stage` | yes | Lifecycle stage or milestone validation point. |
| `bundles` | yes | Bundles run at that point. |
| `result` | yes | Structured result. |
| `counts` | conditional | Review, log, and finding counts when relevant. |
| `paths_added` | conditional | Stage-local path deltas keyed by bundle ID when a referenced bundle's path set changed. |
| `failures` | required when result is not `pass` | Bounded failure details. |
| `evidence.transcript` | optional | Link to deep transcript file. |

Proposed event result enum:

```text
pass
fail
blocked
skipped
not-run
```

Interpretation:

```text
- `pass` means all referenced bundles succeeded.
- `fail` means one or more bundles ran and failed.
- `blocked` means validation could not run due to a missing precondition.
- `skipped` needs an explicit reason and owner decision.
- `not-run` is reserved for planned-but-not-yet-executed stages.
```

Every bundle ID referenced by `validation_events[].bundles` should resolve to a definition in `validation_bundles`. Events for path-expanding bundles should provide enough event-local or accumulated path data to reconstruct the exact expanded command.

## Structured Counts

Replace strings such as:

```text
pass_reviews_5_findings_2_log_entries_5_resolution_entries_2_after_code_review_m1_recording
```

with structured fields:

```yaml
stage: code-review-m1-recording
result: pass
counts:
  reviews: 5
  findings: 2
  log_entries: 5
  resolution_entries: 2
```

The compact form should not encode data in prose strings when it can be represented as fields.

Structured counts that mirror review artifacts should be treated as checked evidence, not merely copied summary. The validator should compare stored counts such as `reviews`, `findings`, `log_entries`, and `resolution_entries` against the review-artifact parser when the relevant artifacts exist, or report a clear blocked/precondition state when the cross-check cannot run.

## Path Variable Model

Use path variables to avoid repeating long change IDs, while preserving the repository's distinction between point-in-time event records and durable contracts.

Example:

```yaml
path_vars:
  change_id: 2026-05-21-review-skill-family-consistency-parser-owned-finding-shape
  slug: review-skill-family-consistency-parser-owned-finding-shape
  change_root: docs/changes/{change_id}
  proposal: docs/proposals/{change_id}.md
  spec: specs/{slug}.md
  test_spec: specs/{slug}.test.md
  plan: docs/plans/{change_id}.md
  reviews_root: {change_root}/reviews
  review_log: {change_root}/review-log.md
  review_resolution: {change_root}/review-resolution.md
```

`change_id` is the dated event identifier, shaped as `<YYYY-MM-DD>-<slug>`. `slug` is the durable contract identifier derived by removing the leading `<YYYY-MM-DD>-` prefix from `change_id`. Dated artifacts such as proposals, plans, and change-local directories should use `change_id` because they record a point-in-time change event. Durable contracts such as specs and test specs should use `slug` because one canonical contract path can be amended by multiple dated changes over time.

This distinction is intentional. If two changes amend the same behavior contract, for example `2026-05-21-foo` and `2026-07-10-foo-revisited`, they can share the same durable spec path when they are both updating `specs/foo.md`. The dated proposal, plan, and change directory remain separate event records, while the undated spec remains the single contract. A compact metadata model should respect that split instead of generating dated spec fragments such as `specs/2026-05-21-foo.md`.

Rules for the future spec:

```text
- path variables expand deterministically;
- validators derive `slug` from `change_id` by stripping the leading date prefix;
- expanded paths remain repository-relative;
- dated event artifacts use `change_id`;
- durable contract artifacts use `slug`;
- spec paths resolve under `specs/{slug}.md`;
- test-spec paths resolve under `specs/{slug}.test.md`;
- a spec or test-spec path using the full dated `change_id` fails validation;
- every resolved path exists once its artifact class's first-exists lifecycle stage has been reached;
- no per-path `optional` or `not_yet_created` flag can suppress a stage-required existence check;
- variables do not hide machine-local paths, usernames, hostnames, or secrets;
- validators reject recursive, unresolved, or ambiguous variables.
```

The spec or artifact-location guide should document each lifecycle artifact class, whether it is dated or undated, its naming rule, and the reason for that rule. That keeps the convention from living only as filename folklore and gives path-variable authors a contract to follow.

## Validation Transcript Policy

`change.yaml` should contain the common-read summary.

A separate transcript file may store full command and rerun detail:

```text
docs/changes/<change-id>/change.validation-log.yaml
```

Recommended split:

| File | Purpose | Read frequency |
| --- | --- | --- |
| `change.yaml` | Common summary, bundles, stages, results, final counts, blockers | frequent |
| `change.validation-log.yaml` | Full expanded commands, stdout/stderr summaries, rerun transcript, timestamps | rare |

Transcript files should be optional in the first slice. The first slice owns the transcript reference contract, not the transcript file's internal schema. When present, `change.yaml` can reference one through:

```yaml
validation_events:
  - stage: code-review-m1
    evidence:
      transcript: change.validation-log.yaml#code-review-m1
```

The transcript should not become the only proof of validation. The common summary should remain sufficient for normal review.

The first-slice acceptance criteria should include a non-load-bearing transcript check: a reviewer should be able to reach the normal validation verdict from `change.yaml` alone without opening `change.validation-log.yaml`. Transcript files can provide forensic detail, but the compact common summary should retain bundle IDs, reconstructed commands, stage results, counts, blockers, and failure details needed for ordinary review.

First-slice transcript-reference rules:

```text
- `evidence.transcript` is optional;
- when present, it uses a well-formed repo-relative file reference with optional `#anchor`;
- when present, the referenced file exists;
- the transcript file's internal field schema is deferred to a separate proposal.
```

## Compatibility and Migration

Support both shapes during migration, but reject mixed shapes within a single file:

| Shape | Status |
| --- | --- |
| Legacy verbose validation list | still accepted |
| Compact bundle/event shape | new preferred shape |
| Mixed legacy and compact in one change | rejected as ambiguous |

Recommended migration rule:

```text
Existing change.yaml files remain valid.
New change.yaml files SHOULD use compact validation metadata after the compact contract lands.
Validators support legacy files until a separate migration proposal retires them.
One `change.yaml` is either wholly legacy, with `schema_version` absent or legacy, or wholly compact with `schema_version: 2`.
The repository may contain legacy and compact files at the same time.
A file containing both legacy validation entries and compact `validation_events` is rejected.
```

First implementation should:

```text
- add compact validation metadata support;
- keep legacy support;
- avoid migrating all historical files;
- optionally migrate one active change as fixture or proof.
```

## Expected Behavior Changes

- New or migrated `change.yaml` files become shorter and easier to scan.
- Common readers see validation state by stage and bundle instead of repeated full commands.
- Full commands remain reconstructable from bundle definitions, variables, paths, and optional transcript references.
- Validators accept both legacy and compact formats during migration.
- Structured results become easier to query and test.
- No validation requirement is weakened.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `schemas/change.schema.json` or equivalent | Add compact validation metadata shape if this repository has a formal schema surface for `change.yaml`. |
| `scripts/validate-change-metadata.py` | Add compact parsing and validation while preserving legacy support. |
| Artifact-location guidance or change-metadata spec | Document dated event-record paths versus undated durable-contract paths. |
| `docs/changes/*/change.yaml` | New files may use compact validation metadata after the contract lands. |
| `docs/changes/*/change.validation-log.yaml` | Optional new forensic transcript file if included in the first slice. |
| Lifecycle validation | May need to understand transcript references if included. |
| Review artifacts | No direct change. |
| Skill files | No direct change expected. |
| Adapter output | No change expected. |
| CLI behavior | No change unless future scaffolding writes compact metadata. |

## Testing and Verification Strategy

The spec and test spec should convert these checks into concrete tests and fixture names:

| Check ID | What is verified |
| --- | --- |
| `CVM-001` | Legacy verbose validation entries still validate. |
| `CVM-002` | Compact validation bundles validate. |
| `CVM-003` | Path variables expand deterministically. |
| `CVM-004` | Unresolved or recursive variables fail. |
| `CVM-005` | Stage events reference existing bundles. |
| `CVM-006` | Stage event result uses an allowed enum value. |
| `CVM-007` | `fail` and `blocked` events require failure or blocker details. |
| `CVM-008` | Structured counts validate as integers. |
| `CVM-009` | Summary `all_passed: true` is rejected if any event is not `pass`. |
| `CVM-010` | Optional transcript reference resolves when present. |
| `CVM-011` | Machine-local paths, credentials, hostnames, and secret-like values are rejected. |
| `CVM-012` | Compact metadata is at least 30% smaller on the common-read surface of a representative high-rerun fixture after reconstruction is proven. |
| `CVM-013` | Expanded reconstructed commands match legacy fixture commands where expected. |
| `CVM-014` | Mixed legacy/compact validation metadata in one `change.yaml` is rejected, while legacy and compact files may coexist across the repository. |
| `CVM-015` | Path-expanding bundle commands reconstruct the exact accumulated path set for each validation event. |
| `CVM-016` | Stored `validation_summary` agrees with values derived from `validation_events`. |
| `CVM-017` | Stored review-artifact counts agree with review-artifact parser output when the referenced artifacts exist. |
| `CVM-018` | `change.yaml` alone is sufficient for normal review verdicts when transcript references are present. |
| `CVM-019` | `slug` is derived from `change_id` by removing the leading date prefix. |
| `CVM-020` | Spec and test-spec variables resolve to undated durable contract paths under `specs/{slug}.md` and `specs/{slug}.test.md`. |
| `CVM-021` | A compact file fails when a resolved path does not exist after that artifact's first-exists lifecycle stage has been reached. |
| `CVM-022` | Path-variable interpolation accepts `{var}` only, rejects `${var}` and other forms, and defines an escape for literal braces. |
| `CVM-023` | Compactness is measured on the `change.yaml` common-read surface of a representative high-rerun fixture. |

Suggested validation commands, with final names to be confirmed by the test spec:

```bash
python scripts/validate-change-metadata.py tests/fixtures/change-metadata/legacy-valid/change.yaml
python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-valid/change.yaml
python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-unresolved-var/change.yaml
python scripts/validate-change-metadata.py tests/fixtures/change-metadata/compact-invalid-summary-conflict/change.yaml
python scripts/test-change-metadata-validator.py
git diff --check --
```

## Rollout and Rollback

Rollout:

1. Approve the proposal.
2. Write or amend the spec for compact `change.yaml` validation metadata.
3. Write or amend the matching test spec.
4. Implement validator support for compact and legacy shapes.
5. Add fixtures for compact valid and invalid examples.
6. Optionally migrate one active change metadata file as a proof fixture.
7. Run code review.
8. Explain the change and verify.
9. Use compact shape for new changes after approval.

Rollback:

1. Revert validator changes.
2. Keep legacy verbose validation format accepted.
3. If an active change was migrated, convert it back to legacy verbose format or leave it only if the reverted validator still accepts it.
4. Keep deep transcript artifacts until all references are removed.
5. Do not invalidate historical change metadata.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Summary hides failed validation. | Reject `all_passed: true` if any event is fail, blocked, skipped without accepted reason, or not-run after the required stage. |
| Summary fields drift from validation events. | Treat `validation_summary` as validator-derived and validator-checked; reject stored summaries that disagree with `validation_events`. |
| Full command reconstruction becomes impossible. | Bundle definitions, path variables, and per-bundle accumulated `paths_added` should be sufficient to reconstruct the exact command and path set for each event. |
| Migration breaks old changes. | Keep legacy shape valid during migration. |
| Validators become too complex. | Start with bundle/event shape only; defer full transcript semantics if needed. |
| Path variables hide secrets or machine-local paths. | Reject absolute paths, home paths, hostnames, credentials, and unresolved variables. |
| Path variables produce dated spec fragments or dead links. | Derive `slug` from `change_id`, require durable contract variables to use `slug`, and check resolved paths against the filesystem after the artifact's first-exists lifecycle stage has been reached. |
| Structured counts drift from review artifacts. | Cross-check counts against review-log and review-resolution where available, either in the first slice or a named follow-up. |
| Mixed legacy/compact format becomes ambiguous. | Reject mixed formats within one `change.yaml`; allow incremental migration only across files. |
| Compactness removes useful per-stage details. | Keep `paths_added`, failure details, and transcript references available. |
| Per-path not-yet-created flags weaken existence checks. | Derive existence requirements from lifecycle stage and artifact first-exists stage; no path may opt out of a stage-required existence check. |
| Size reduction becomes a goal that erodes evidence. | Treat reconstruction preservation as the dominant gate and the 30% reduction as a secondary floor on a representative high-rerun fixture. |

## First-Slice Boundary

First implementation slice:

```text
- compact validation section in the change metadata contract;
- validate-change-metadata.py support for compact validation bundles/events;
- legacy-shape compatibility;
- dated event-record and undated durable-contract path variable rules;
- filesystem existence checks for resolved path variables, derived from lifecycle stage and artifact first-exists stage;
- fixtures for compact valid and invalid metadata;
- one representative compact fixture or active change proof;
- test-spec coverage for compact validation metadata behavior;
- review-artifact count cross-checking for structured counts when referenced artifacts exist.
```

Out of scope for the first slice:

```text
- bulk migration of historical change.yaml files;
- CI artifact retention policy;
- full transcript standardization;
- CLI scaffolding that writes compact metadata;
- changes to review-record format;
- changes to artifact lifecycle rules;
- changes to validation command selection.
```

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-CVM-001` | Legacy verbose validation metadata still validates. |
| `AC-CVM-002` | Compact bundle/event metadata validates. |
| `AC-CVM-003` | Path variables expand deterministically and safely. |
| `AC-CVM-004` | Structured results replace prose-encoded pass strings in compact fixtures. |
| `AC-CVM-005` | `all_passed: true` is rejected when any event is not `pass`. |
| `AC-CVM-006` | Failure/blocker details are required for failed or blocked events. |
| `AC-CVM-007` | Optional transcript references validate when present. |
| `AC-CVM-008` | Full validation commands are reconstructable from bundles, variables, and event data in compact fixtures. |
| `AC-CVM-009` | Compact fixture is materially smaller than equivalent legacy fixture while preserving evidence. |
| `AC-CVM-010` | No validation selection, command exit behavior, or failure detection semantics change. |
| `AC-CVM-011` | Mixed legacy/compact validation metadata in one `change.yaml` is rejected. |
| `AC-CVM-012` | No historical change metadata is invalidated by this proposal. |
| `AC-CVM-013` | Path-expanding bundles preserve exact per-stage path sets through deterministic accumulation or an equivalent unambiguous model. |
| `AC-CVM-014` | Stored validation summary fields are rejected when they disagree with `validation_events`. |
| `AC-CVM-015` | `change.yaml` remains sufficient for normal validation review even when transcript references are present. |
| `AC-CVM-016` | Structured review counts are cross-checked against review-artifact parser output when the referenced artifacts exist. |
| `AC-CVM-017` | Path variables distinguish dated event artifacts from undated durable contracts using `change_id` and `slug`. |
| `AC-CVM-018` | Spec and test-spec variables resolve to canonical undated paths, and dated spec paths such as `specs/{change_id}.md` fail validation. |
| `AC-CVM-019` | Resolved path variables are checked against the filesystem once the artifact's first-exists lifecycle stage has been reached. |
| `AC-CVM-020` | Path-variable interpolation uses `{var}` exclusively, rejects `${var}` and other alternate forms, and defines an escape for literal braces. |
| `AC-CVM-021` | The representative high-rerun compact fixture is at least 30% smaller on the `change.yaml` common-read surface, after proving full reconstruction of legacy evidence. |

## Open Questions

None. The six prior spec-input questions are resolved in the recommendation and decision log.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | Treat noisy validation metadata as a schema problem. | The validator parses `change.yaml`, so hand-editing one file would break the contract. | Freehand compacting of one change file. |
| 2026-05-21 | Preserve durable evidence while reducing common-read volume. | Validation metadata is audit evidence, not transient terminal output. | Suppress detail entirely. |
| 2026-05-21 | Use bundles and path variables. | Repeated commands and repeated change IDs are the largest avoidable cost. | Shorten prose result strings only. |
| 2026-05-21 | Keep legacy compatibility. | Historical change files must remain valid. | Immediate forced migration. |
| 2026-05-21 | Defer bulk migration. | Validator support should land before migration. | Bulk-edit historical metadata in the first slice. |
| 2026-05-21 | Pin path-expanding bundle reconstruction through per-bundle accumulated path deltas. | Bundle names alone do not prove the exact historical command or path set that ran at a stage. | Optional or best-effort `paths_added`; full transcript as the only proof. |
| 2026-05-21 | Treat `validation_summary` as validator-derived and validator-checked. | Stored summary fields are useful for common reading but can drift from `validation_events`. | Unchecked duplicated summary data; dropping all summary fields from `change.yaml`. |
| 2026-05-21 | Use explicit `schema_version: 2` for compact validation metadata. | Version branching makes compact-vs-legacy detection deterministic for the dual-read validator; field-presence detection is heuristic and fragile during migration. | Additive compact shape under the current schema version. |
| 2026-05-21 | Include review-artifact count cross-checking in the first slice when referenced artifacts exist. | Structured counts become durable evidence and should be bound to parser output. | Treat copied counts as unchecked prose-equivalent summary. |
| 2026-05-21 | Use separate `change_id` and `slug` variables for path expansion. | Proposals, plans, and change directories are dated event records, while specs and test specs are undated durable contracts that can be amended by multiple changes. | A single `{change_id}` variable for all artifact classes; dated spec paths. |
| 2026-05-21 | Validate resolved path variables against the filesystem. | Dead derived paths such as `specs/{change_id}.md` should fail at metadata validation time. | Let reviewers discover dead links manually. |
| 2026-05-21 | Reject mixed legacy and compact validation metadata within one `change.yaml`. | A hybrid shape creates a third validator surface and precedence rules can silently ignore conflicting evidence. | Bounded in-file transition form; precedence between legacy and compact evidence. |
| 2026-05-21 | Contract transcript references in the first slice, not transcript internals. | Reference syntax and target existence are needed to avoid dead links, while transcript field standardization is a separate broader contract. | No reference validation; full transcript schema in the first slice. |
| 2026-05-21 | Use `{var}` as the only path-variable interpolation syntax for the first slice. | A closed syntax is easier to validate and avoids `${var}` shell/env-var confusion. | Multiple interpolation syntaxes; `${var}` support. |
| 2026-05-21 | Derive path existence requirements from lifecycle stage, not per-path opt-out flags. | A per-path not-yet-created flag lets missing required artifacts excuse themselves; stage ownership keeps existence checks authoritative. | Per-path `optional` or `not_yet_created` flags. |
| 2026-05-21 | Use a 30% common-read size-reduction floor under a reconstruction-preservation gate. | Compactness should prove reduced noise without allowing evidence loss; the metric applies to a representative high-rerun fixture. | Whole-file size-only measurement; no threshold; threshold without reconstruction gate. |

## Next Artifacts

```text
proposal-review
spec: compact change validation metadata
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Potential follow-up proposals after this proposal settles:

- Bulk migration of existing `change.yaml` validation metadata.
- Standard `change.validation-log.yaml` transcript format.
- CLI scaffolding that writes compact validation metadata automatically.
- Applying the same summary/transcript split to other durable evidence surfaces.

## Follow-on Artifacts

None yet

## Readiness

Proposal review approved. Ready for `spec`.

Core invariant:

```text
Compact validation metadata must make the common read cheaper without weakening
the audit trail.

The standard validation bundle can be summarized by stage only when commands are
reconstructable, failures remain explicit, structured counts remain verifiable,
and legacy verbose evidence remains accepted during migration.
```
