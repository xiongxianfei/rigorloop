# RigorLoop CLI Lockfile Review Resolution

## Scope

This record tracks material finding closeout for the RigorLoop CLI durable lockfile contract.

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5

- Reviews covered: `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `architecture-review-r1`, `plan-review-r1`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`, `code-review-r5`
- Findings resolved: 4
- Unresolved findings: 0
- Final result: `SR1-F1`, `SR2-F1`, `CR1-F1`, and `CR3-F1` are resolved. `code-review-r2` approved M1 with no material findings. `code-review-r4` approved M2 with no material findings after the `CR3-F1` fix. `code-review-r5` approved M3 with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SR1-F1 | accepted | resolved | The spec now defines a complete `schema_version: 1` lockfile shape and strict unknown-field policy. |
| SR2-F1 | accepted | resolved | The spec now allows durable lockfile writes for local archive installs with `source: local-archive`. |
| CR1-F1 | accepted | resolved | M1 parser now detects unknown nested mapping fields; code-review-r2 approved the fix. |
| CR3-F1 | accepted | resolved | M2 now verifies the installed Codex adapter tree against trusted metadata before lockfile writes and rejects extra, modified, or partial installed trees. |

## Common Resolution Metadata

- Owner: spec author
- Owning stage: spec
- Validation target: revise `specs/rigorloop-cli-lockfile.md`, rerun `spec-review`, then run review artifact, change metadata, artifact lifecycle, and selected CI validation.
- Validation evidence: pending

## Finding Details

### spec-review-r1

#### SR1-F1 - Durable lockfile document shape is incomplete

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add a complete normative `rigorloop.lock` YAML schema with top-level `schema_version`, `rigorloop`, `manifest`, and `generated.adapters[]` sections. Define every required field, add a full valid example, and choose a first-slice unknown-field policy that blocks on unknown or unsupported lockfile shape.
Rationale: `rigorloop.lock` is durable compatibility state. Architecture, tests, and implementation must not invent public structure.
Validation target: Update the test spec with positive full-fixture coverage, missing-field failures, unsupported-schema blocking, and unknown-field blocking.
Validation evidence: `specs/rigorloop-cli-lockfile.md` now defines the complete top-level lockfile shape, generated adapter entry fields, and strict first-slice unknown-field policy. Same-stage `spec-review-r2` confirmed this closes `SR1-F1`.

### spec-review-r2

#### SR2-F1 - Local archive lockfile source semantics conflict

Finding ID: SR2-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Allow durable lockfile writes for local archive installs and add `source: local-archive` as a first-slice allowed value alongside `source: release-archive`. Define `source` as the install delivery mode, not the metadata trust root. Local archive mode records the local archive basename, official release tag, archive SHA-256, install root, tree hash algorithm, tree hash, and file count without recording absolute local paths.
Rationale: `--from-archive` is a supported first-slice install path. If it installs generated adapter output, the lockfile should record that durable state consistently instead of blocking or pretending the delivery mode was network download.
Validation target: Update the test spec to cover network lockfile entries, local archive lockfile entries, unsupported source values, no absolute local path recording, and no lockfile mutation after failed archive verification.
Validation evidence: `specs/rigorloop-cli-lockfile.md` now defines `source` as the install delivery mode, allows `release-archive` and `local-archive`, and defines local archive lockfile fields. Same-stage `spec-review-r3` approved the revised spec.

### spec-review-r3

No material findings; no resolution entry required. The same-stage spec-review rerun approved the revised spec and closed `SR2-F1`.

### architecture-review-r1

No material findings; no resolution entry required. Architecture-review approved the canonical architecture package update and ADR for the durable lockfile boundary.

### plan-review-r1

No material findings; no resolution entry required. Plan-review approved the lockfile execution plan and cleared the path to test-spec.

### code-review-r1

#### CR1-F1 - Unknown nested mapping fields are silently accepted

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution
Chosen action: Fix M1 parser handling for unknown nested mapping fields and add regression coverage.
Rationale: The lockfile spec requires first-slice CLIs to block on unknown fields instead of silently accepting or preserving future shape.
Required outcome: Unknown nested mapping fields inside known lockfile sections and adapter entries must block as `unsupported-lockfile-shape` before mutation.
Safe resolution path: Update the strict parser to detect any indented unknown field key, including mapping keys without scalar values, and add unit/integration tests for unknown mapping keys inside `rigorloop` and `generated.adapters[]`.
Validation target: Rerun `npm test --prefix packages/rigorloop`, selected CI for the lockfile paths, and code-review.
Validation evidence: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-005|TLF-006|TLF-007'` and `npm test --prefix packages/rigorloop` passed after adding parser and CLI integration coverage for unknown nested mapping keys. Same-stage `code-review-r2` approved the fix with no material findings.

### code-review-r2

No material findings; no resolution entry required. Code-review approved M1 and closed `CR1-F1`.

### code-review-r3

#### CR3-F1 - Installed tree hash can include unrelated pre-existing files

Finding ID: CR3-F1
Disposition: accepted
Status: resolved
Owner: implementation
Owning stage: review-resolution
Chosen action: Fix M2 lockfile creation/update so the installed-tree hash recorded in `rigorloop.lock` represents only verified Codex generated adapter output, or so any installed-root tree mismatch against trusted metadata fails before lockfile write.
Rationale: The lockfile records durable generated-output state. It must not silently claim unrelated pre-existing files under `.agents/skills` as verified Codex adapter output.
Required outcome: Successful M2 init must not write or update `rigorloop.lock` when post-extraction installed-tree verification fails.
Safe resolution path: After extraction, compute the installed tree using the verified adapter file set or compare the installed root to the trusted expected tree and return `tree-hash-mismatch` with validation-failed exit code `3` before lockfile write on extra or modified files. Add regression coverage for a pre-existing extra file under `.agents/skills` and prove `rigorloop.lock` stays absent or unchanged.
Validation target: Rerun `npm test --prefix packages/rigorloop`, selected CI for the lockfile paths, and code-review.
Validation evidence: Focused CR3-F1 tests and `npm test --prefix packages/rigorloop` passed after adding installed-tree mismatch handling. The regression coverage proves extra, modified, and partial pre-existing installed trees return `installed-tree-mismatch` with exit code `3`, exact existing adapter trees can create a lockfile with the trusted metadata tree, and existing lockfiles remain unchanged on installed-tree mismatch.

### code-review-r4

No material findings; no resolution entry required. Code-review approved M2 and closed `CR3-F1`.

### code-review-r5

No material findings; no resolution entry required. Code-review approved M3 and closed the final implementation milestone.

## Closeout Checklist

- [x] Every material finding has a final disposition.
- [x] Every accepted finding has action and rationale.
- [x] Validation evidence is recorded for each resolved finding.
- [x] `review-log.md` lists no open findings.
- [x] Closeout status is correct.
