# Artifact status lifecycle ownership test spec

## Status

- active

## Related spec and plan

- Spec: `specs/artifact-status-lifecycle-ownership.md`
- Related proposal: `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
- Architecture: `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
- ADR: `docs/adr/ADR-20260419-repository-source-layout.md`
- Plan: `docs/plans/2026-04-20-artifact-status-lifecycle-ownership.md`
- Related validator and guidance surfaces:
  - `scripts/artifact_lifecycle_contracts.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/`
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `specs/feature-template.md`
  - `specs/feature-template.test.md`
  - canonical `skills/`
  - generated `.codex/skills/`

## Testing strategy

- Use fixture-driven integration tests for the new lifecycle validator because the main behavior is deterministic parsing, classification, and structural rule enforcement over tracked repo artifacts.
- Use explicit-path and explicit CI-diff command shapes as the required proof surface. Treat `--mode local` as optional proof only when the working tree has no unrelated changes.
- Use manual contract review for workflow docs, templates, skills, and approved example surfaces because contributor-facing guidance is part of the shipped behavior.
- Use `bash scripts/ci.sh` as the smoke proof that the validator and its fixture suite are wired into the repository-owned CI wrapper.
- Prefer real repository files and real fixture trees over mocks or snapshots. Use substring assertions for validation findings instead of brittle full-output matching.
- Treat migration checks as both structural and manual: structural scans confirm statuses and closeout markers, while manual review confirms settled-current versus historical wording remains truthful.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R2`, `R3`, `R3a`, `R3b`, `R3c` | `T1`, `T2`, `T12` | manual, integration | Workflow summary, in-scope coverage, and delegated detailed guidance remain explicit |
| `R4`, `R5`, `R5a`, `R5b`, `R5c`, `R6`, `R6a` | `T2`, `T3`, `T4`, `T13` | manual, integration | Durable status vocabulary and transitional-state cleanup across artifact classes |
| `R7`, `R7a`, `R7b`, `R7c`, `R7d`, `R7e`, `R9`, `R9a`, `R9b`, `R9c`, `R9d`, `R9e`, `R9f` | `T2`, `T5`, `T13` | manual, integration | Settlement-versus-closeout rules, readiness wording, and follow-on handling |
| `R8`, `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e` | `T2`, `T6`, `T13` | manual, integration | Transition ownership, superseded-versus-archived behavior, and replacement pointers |
| `R11`, `R11a`, `R11b`, `R11c`, `R11d`, `R11e`, `R12` | `T8`, `T9`, `T10`, `T13`, `T14` | integration, manual | Related-scope resolution, block-versus-warning classification, and stale-state detection |
| `R13`, `R13a`, `R13aa`, `R13b`, `R13c` | `T3`, `T4`, `T5`, `T6`, `T7`, `T10`, `T11` | integration, smoke | Minimal executable enforcement, fixture coverage, objective-only validator scope, and CI path |
| `R14`, `R14a`, `R14b` | `T1`, `T2`, `T12` | manual, integration | Canonical guidance update and generated-boundary handling |
| `R15`, `R15a`, `R15b` | `T13`, `T14` | integration, manual | Relied-on migration and warning-only treatment for unrelated baseline debt |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T5`, `T13` | Accepted proposal remains settled current guidance without forced terminal closeout |
| `E2` | `T5`, `T13` | Approved spec remains current guidance rather than archived history |
| `E3` | `T6`, `T13` | Superseded architecture docs must identify replacements |
| `E4` | `T8`, `T9`, `T10` | Verify uses pre-PR handoff surfaces before PR text exists |
| `E5` | `T9`, `T14` | Unrelated stale baseline artifacts warn instead of block |
| `E6` | `T4`, `T5`, `T13` | Test specs move from active proof surface to archived history |

## Edge case coverage

- `EC1`: accepted proposals may remain current direction rather than archive-only history: `T5`, `T13`
- `EC2`: approved specs and architecture docs may remain current guidance without immediate closeout: `T5`, `T13`
- `EC3`: test specs may remain `active` during live implementation or review work: `T4`, `T5`
- `EC4`: artifacts may be `archived` without direct replacements: `T6`
- `EC5`: explicitly replaced artifacts must be `superseded`, not merely `archived`: `T6`, `T13`
- `EC6`: unrelated stale baseline artifacts warn without blocking unless the current change relies on them: `T9`, `T14`
- `EC7`: draft PR-body references join scope only when draft PR text exists: `T8`, `T10`
- `EC8`: settled current artifacts may omit `Follow-on artifacts` until actual downstream artifacts exist: `T5`
- `EC9`: premature `Follow-on artifacts` sections must say `None yet`: `T5`

## Test cases

### T1. Workflow summary and root guidance expose the artifact lifecycle model

- Covers: `R1`, `R1a`, `R2`, `R3`, `R3a`, `R3b`, `R3c`, `R14`, `R14a`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
- Steps:
  - Review the updated workflow and governance docs.
  - Confirm the workflow summary table includes the required columns and rows for proposal, spec, architecture, test spec, and ADR lifecycle ownership.
  - Confirm artifact-local status remains the source of truth and that change-local artifacts are not promoted to authoritative lifecycle state.
  - Confirm contributor-facing docs make the settlement-versus-closeout split discoverable.
- Expected result:
  - A contributor can identify the repository-wide artifact lifecycle model without reading chat history.
- Failure proves:
  - The feature still depends on implicit or contradictory workflow guidance.
- Automation location:
  - Manual review during M2.

### T2. Canonical templates, skills, and approved examples teach the per-artifact contract

- Covers: `R4`, `R5`, `R5a`, `R5b`, `R5c`, `R7`-`R10e`, `R14`, `R14a`, `R14b`
- Level: manual, integration
- Fixture/setup:
  - `specs/feature-template.md`
  - `specs/feature-template.test.md`
  - canonical skills under `skills/`
  - generated `.codex/skills/`
  - approved proposal and architecture examples for this feature
- Steps:
  - Review canonical templates and targeted skills for proposal, spec, test-spec, architecture, verify, and workflow behavior.
  - Confirm they teach allowed statuses, main transitions, closeout expectations, and verify handling per class.
  - Confirm examples remain aligned but non-normative, and generated `.codex/skills/` remains derived rather than authoritative.
- Expected result:
  - Human guidance surfaces teach the same lifecycle contract the validator enforces.
- Failure proves:
  - Contributors could follow canonical guidance and still violate the executable rules, or generated output could be mistaken for source.
- Automation location:
  - Manual review plus `python scripts/build-skills.py --check` during M2.

### T3. Valid fixtures pass for each in-scope artifact class

- Covers: `R2`, `R4`-`R10e`, `R13`, `R13a`, `R13b`
- Level: integration
- Fixture/setup:
  - valid fixtures under `tests/fixtures/artifact-lifecycle/` for:
    - proposal
    - top-level spec
    - test spec
    - architecture doc
    - ADR
- Steps:
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <valid fixture or representative file>` for at least one valid artifact per class.
- Expected result:
  - Valid artifacts pass with zero blocking findings.
- Failure proves:
  - The validator rejects spec-compliant artifact shapes or class-specific rule registration is wrong.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T4. Invalid status vocabulary and transitional-state misuse fail clearly

- Covers: `R4`, `R5`, `R5a`, `R5b`, `R5c`, `R6`, `R6a`, `R12`
- Level: integration
- Fixture/setup:
  - invalid fixtures under `tests/fixtures/artifact-lifecycle/` for:
    - proposal or spec using `reviewed`
    - test spec using long-lived `complete`
    - architecture or spec using an unknown status
    - ADR using a non-ADR status
- Steps:
  - Run the fixture suite.
  - Confirm failures identify invalid status vocabulary or forbidden transitional-state usage.
- Expected result:
  - The validator rejects stale or unsupported status models with actionable errors.
- Failure proves:
  - The contract still tolerates the exact metadata drift this feature is intended to stop.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T5. Settlement, closeout, follow-on, and readiness rules are enforced objectively

- Covers: `R7`, `R7a`, `R7b`, `R7c`, `R7d`, `R7e`, `R9`, `R9a`, `R9b`, `R9c`, `R9d`, `R9e`, `R9f`, `R12`, `E1`, `E2`, `E6`, `EC1`, `EC2`, `EC3`, `EC8`, `EC9`
- Level: integration
- Fixture/setup:
  - fixtures for:
    - accepted or approved settled-current artifacts with truthful readiness and no premature terminal closeout
    - terminal artifacts missing required closeout surfaces
    - premature `Follow-on artifacts` sections that are empty instead of `None yet`
    - settled artifacts with stale pre-review or pre-implementation readiness wording
- Steps:
  - Run the fixture suite and narrow explicit-path validation over representative files.
  - Confirm settled-current fixtures pass without forced terminal closeout.
  - Confirm terminal-state and readiness-drift fixtures fail.
- Expected result:
  - The validator preserves the settlement-versus-closeout split while rejecting objective contradictions.
- Failure proves:
  - Implementation would either over-close current guidance or miss stale metadata that later stages rely on.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T6. Superseded and archived artifacts are distinguished correctly

- Covers: `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `E3`, `EC4`, `EC5`
- Level: integration
- Fixture/setup:
  - fixtures for:
    - superseded artifacts with valid replacement pointers
    - superseded artifacts missing `superseded_by`
    - archived artifacts without replacements
    - artifacts incorrectly marked `archived` when they were explicitly replaced
- Steps:
  - Run the fixture suite.
  - Confirm replacement-pointer rules and archived-versus-superseded distinctions behave as specified.
- Expected result:
  - Replacement chains are explicit, and archive-only history does not masquerade as supersession.
- Failure proves:
  - Replacement semantics remain ambiguous and authoritative lineage could be lost.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T7. Identifier, naming, placeholder, and generated-boundary checks stay within v0.1 scope

- Covers: `R13aa`, `R13b`, `R13c`, `R14b`
- Level: integration
- Fixture/setup:
  - fixtures for:
    - invalid proposal filename stem
    - invalid top-level spec stem
    - invalid ADR filename stem
    - placeholder text
    - duplicate identifiers where class contracts require uniqueness
    - generated output path used as authored source
- Steps:
  - Run the fixture suite.
  - Confirm identifier and naming checks apply only to classes with explicit contracts.
  - Confirm generated-source misuse fails clearly.
- Expected result:
  - The validator enforces only objective, class-scoped structural rules and preserves the canonical-versus-generated boundary.
- Failure proves:
  - v0.1 enforcement scope drifted into arbitrary metadata requirements or weak source-boundary handling.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T8. Related-scope expansion includes the required pre-PR and draft-PR surfaces

- Covers: `R11`, `R11c`, `R11d`, `R11e`, `E4`, `EC7`
- Level: integration
- Fixture/setup:
  - scope fixtures or targeted repo fixtures involving:
    - `docs/changes/<change-id>/change.yaml`
    - an explain-change artifact
    - the active plan
    - optional draft PR-body input
- Steps:
  - Run targeted validator checks that exercise scope expansion through each supported surface.
  - Confirm pre-PR mode works without draft PR text.
  - Confirm draft PR-body references join scope only when explicit draft PR text is supplied.
- Expected result:
  - Related-scope expansion follows the approved pre-PR and draft-PR rules deterministically.
- Failure proves:
  - Verify scope could silently miss authoritative references or block on non-existent PR text.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T9. Related artifacts block while unrelated stale baseline artifacts warn

- Covers: `R11`, `R11a`, `R11b`, `R12`, `E5`, `EC6`
- Level: integration
- Fixture/setup:
  - fixtures or controlled repo cases containing:
    - stale touched artifact
    - stale referenced artifact
    - stale authoritative artifact for the changed area
    - unrelated stale baseline artifact
- Steps:
  - Run validator scenarios that classify both related and unrelated stale artifacts.
  - Confirm related stale artifacts produce blocking findings.
  - Confirm unrelated stale baseline artifacts produce warnings only.
- Expected result:
  - The validator enforces the block-versus-warning contract without turning baseline debt into a blanket blocker.
- Failure proves:
  - Verify classification is wrong and either misses blocking drift or blocks unrelated work.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`

### T10. CLI mode contracts are deterministic and fail clearly on missing inputs

- Covers: `R11c`, `R11d`, `R11e`, `R13`, `R13a`
- Level: integration
- Fixture/setup:
  - `scripts/validate-artifact-lifecycle.py`
  - representative explicit-path targets
- Steps:
  - Run:
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <repo-path>`
    - `python scripts/validate-artifact-lifecycle.py --mode pr-ci --base <sha> --head <sha>`
    - `python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before <sha> --after <sha>`
  - Confirm missing `--path`, `--base`/`--head`, or `--before`/`--after` inputs fail with clear input errors.
  - Confirm `--mode local` is treated as optional proof and is not the milestone-required path when unrelated worktree changes exist.
- Expected result:
  - All validator modes are explicit, deterministic, and safe to use in local and hosted flows.
- Failure proves:
  - Scope selection still depends on guessing or ambiguous environment state.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py` plus direct CLI checks during M1 and M3.

### T11. The repository-owned CI wrapper runs the lifecycle validator and fixture suite

- Covers: `R13`, `R13a`, `R13b`
- Level: smoke
- Fixture/setup:
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
- Steps:
  - Review `scripts/ci.sh` and `.github/workflows/ci.yml`.
  - Run `bash scripts/ci.sh`.
  - Confirm the CI wrapper prints and runs the lifecycle validator path and its fixture tests alongside existing checks.
- Expected result:
  - Hosted CI remains a thin wrapper over repo-owned validation commands and includes the new first-enforcement stack.
- Failure proves:
  - The feature would claim executable enforcement without actually wiring it into the repository validation path.
- Automation location:
  - `bash scripts/ci.sh`

### T12. Workflow docs, templates, canonical skills, and generated output stay aligned

- Covers: `R1`-`R3c`, `R14`, `R14a`, `R14b`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `specs/feature-template.md`
  - `specs/feature-template.test.md`
  - canonical `skills/`
  - generated `.codex/skills/`
- Steps:
  - Review the updated human guidance surfaces.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Confirm generated output mirrors canonical guidance and that no surface still teaches the stale lifecycle model.
- Expected result:
  - Contributors and runtime adapters see one coherent lifecycle contract.
- Failure proves:
  - The feature leaves discoverability drift between docs, templates, canonical skills, and generated compatibility output.
- Automation location:
  - M2 validation plus targeted manual review.

### T13. Migration normalizes relied-on touched artifacts without over-closing current guidance

- Covers: `R6a`, `R7`-`R10e`, `R12`, `R15`, `R15a`, `E1`, `E2`, `E3`, `E6`, `EC1`, `EC2`, `EC4`, `EC5`, `EC8`, `EC9`
- Level: integration, manual
- Fixture/setup:
  - touched authoritative artifacts for this feature:
    - `docs/proposals/2026-04-20-artifact-status-lifecycle-ownership.md`
    - `specs/artifact-status-lifecycle-ownership.md`
    - `docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md`
  - historical relied-on test specs:
    - `specs/rigorloop-workflow.test.md`
    - `specs/constitution-governance-surface.test.md`
    - `specs/plan-index-lifecycle-ownership.test.md`
- Steps:
  - Run explicit-path validation over the touched relied-on artifacts.
  - Review the touched artifacts’ status, readiness, and closeout wording manually.
  - Confirm settled current artifacts remain current guidance where appropriate.
  - Confirm historical test specs no longer rely on `complete`.
- Expected result:
  - The repository stops relying on stale state for touched authoritative artifacts without rewriting settled current guidance as archive-only history.
- Failure proves:
  - Migration either missed known stale state or over-corrected current guidance into terminal closeout.
- Automation location:
  - M4 validation plus manual artifact review.

### T14. Unrelated stale baseline debt stays visible but non-blocking

- Covers: `R11a`, `R11b`, `R15b`, `E5`, `EC6`
- Level: manual, integration
- Fixture/setup:
  - validator output from a repo state that still contains unrelated stale baseline artifacts, if any
  - plan and validation-note records for this feature
- Steps:
  - Run the lifecycle validator on the changed-area scope.
  - Confirm any unrelated stale baseline artifacts are reported as warnings rather than blockers.
  - Confirm the current change does not begin relying on any artifact still classified as unrelated stale debt.
- Expected result:
  - Baseline debt remains visible without blocking unrelated adoption work.
- Failure proves:
  - The repository will either ignore stale debt entirely or over-block unrelated changes.
- Automation location:
  - M4 validation and verify-stage artifact review.

## Fixtures and data

- Add focused fixtures under `tests/fixtures/artifact-lifecycle/` for:
  - valid per-class artifacts
  - invalid status vocabulary and transitional-state misuse
  - closeout and readiness contradictions
  - superseded-versus-archived cases
  - identifier and naming violations
  - generated-source misuse
  - related-scope inputs from `change.yaml`, explain-change, active plan, and optional draft PR body
- Reuse real repository artifacts for manual migration review instead of synthetic stand-ins when verifying touched authoritative files.

## Mocking/stubbing policy

- Do not mock artifact parsing or rule evaluation in the primary proof surface.
- Prefer subprocess-driven CLI tests and real fixture trees.
- If helper-level unit tests are added later, keep them secondary to end-to-end validator fixture tests.
- Assert key substrings, severity, and blocker-versus-warning classification rather than full exact output formatting unless output shape becomes an explicit contract.

## Migration or compatibility tests

- Verify historical test specs formerly marked `complete` are reclassified to truthful lifecycle states.
- Verify settled current artifacts keep truthful readiness without forced terminal closeout.
- Verify superseded artifacts identify replacements when replacements exist.
- Verify unrelated stale baseline artifacts remain warning-only unless the current change relies on them.

## Observability verification

- Validator output should identify mode, scope source, artifact path, artifact class, seen status, violated rule, and blocker-versus-warning classification.
- `verify` evidence should record which related artifacts were checked and which stale artifacts were warnings only.
- CI output should continue to print the exact validator commands being run.

## Security/privacy verification

- Validate that the lifecycle validator uses only local repository files and explicit caller inputs.
- Validate that no network calls, GitHub API reads, or secrets are required for the fixture suite or base CI path.
- Validate that generated output is not accepted as authoritative source content.

## Performance checks

- The validator should remain a bounded file scan over explicit scope plus optional baseline classification.
- Smoke proof is sufficient for v0.1:
  - explicit-path runs complete promptly on small target sets
  - `bash scripts/ci.sh` remains practical for normal contributor use
- No benchmark harness is required in this change unless the implementation introduces unexpected repository-wide scanning cost.

## Manual QA checklist

- Confirm the workflow summary matrix in `specs/rigorloop-workflow.md` matches the approved spec exactly enough for contributors to apply it without chat history.
- Confirm proposal, spec, test-spec, architecture, and ADR guidance all use the new durable status model.
- Confirm touched authoritative artifacts for this feature are tracked and no longer rely on stale readiness or status wording.
- Confirm unrelated untracked proposal drafts remain out of scope and excluded from required milestone validation.
- Confirm generated `.codex/skills/` output is regenerated from canonical `skills/` rather than hand-edited.

## What not to test

- Do not add subjective prose-quality scoring for artifact writing in v0.1.
- Do not test GitHub-hosted PR creation or remote PR-body retrieval; the approved design is file-based and local-input-driven.
- Do not build a repository-wide full-history audit in this change; test the changed area plus warning-only baseline handling instead.
- Do not duplicate existing skill-structure validator coverage beyond proving the new lifecycle surfaces integrate with it.

## Uncovered gaps

- No blocking spec or architecture gaps remain for implementation.
- Exact fixture directory names and helper function names are implementation details and do not need separate spec changes unless they alter the observable validator contract.
