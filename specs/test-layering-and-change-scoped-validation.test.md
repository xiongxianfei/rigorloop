# Test Layering and Change-Scoped Validation Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/test-layering-and-change-scoped-validation.md`
- Plan: `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`
- Proposal: `docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md`
- Architecture: `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- Spec-review findings: resolved in the approved spec after SR2 updates.
- Architecture-review findings: resolved by `architecture-review-r2`.
- Plan-review findings: `PR1-F1` resolved by routing expected blocked selector and wrapper proof through `python scripts/test-select-validation.py`; `plan-review-r2` approved the plan.
- Change-local review resolution: `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md`

## Testing strategy

- Unit tests exercise selector request validation, path normalization, path classification, affected-root derivation, check-catalog data, command placeholder substitution, broad-smoke trigger records, and JSON rendering.
- Integration tests exercise `scripts/select-validation.py` CLI modes and `scripts/ci.sh` wrapper behavior using small temporary repositories, fixture changed paths, and stub selected commands where needed.
- Contract tests inspect workflow docs, stage skills, generated skill mirrors, and generated adapter packages to prove targeted-proof, broad-smoke, and manual-proof guidance stays aligned after canonical skill changes.
- Regression tests for selector and wrapper behavior live primarily in `python scripts/test-select-validation.py`, including expected blocked-path cases that should exit nonzero at the CLI level but pass when asserted by the test harness.
- Existing repository validators remain proof executors. Selector tests must assert selected check IDs and command strings, not revalidate skills, adapters, releases, review artifacts, or lifecycle artifacts themselves.
- Non-smoke validation must use only repository files, the Python standard library, Bash, and Git. It must not require network access, secrets, hosted CI, or installed Codex, Claude Code, or OpenCode tools.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R2c` | `T14`, `T18` | Layered validation, targeted proof, broad smoke, and release-only manual smoke guidance. |
| `R3`-`R3j` | `T2`, `T3`, `T4` | Standalone selector command, source-of-truth boundary, CLI forms, required flags, JSON stdout, and exit codes. |
| `R4`-`R4f` | `T2`, `T5`, `T10`, `T12` | Validation modes, changed-path sources, and mode-specific breadth without duplicate selection logic. |
| `R5`-`R5t` | `T1`, `T3`, `T4`, `T11`, `T12` | JSON fields, selected-check shape, status enum, catalog IDs, command templates, placeholder substitution, and wrapper fallback handling. |
| `R6`-`R7a` | `T6`, `T9` | First-slice category coverage and repository-governance scope boundary. |
| `R8`-`R8c` | `T7` | Canonical skill path selection and generated-output checks. |
| `R9`-`R9b` | `T7`, `T8`, `T16` | Generated adapter and adapter-generation selection plus generated-output drift proof. |
| `R10`-`R10d` | `T8` | Review artifact roots, change metadata checks, affected roots, and multi-file change metadata validation. |
| `R11`-`R11a` | `T8` | Lifecycle artifact selection for proposals, specs, test specs, architecture docs, ADRs, and plans. |
| `R12`-`R12a` | `T8`, `T9` | Release metadata selection and release version inference/blocking. |
| `R13`-`R13b` | `T9`, `T17` | Workflow, governance, template, schema, selector, generation, validation, and release script routing. |
| `R14`-`R15b` | `T4`, `T9` | Non-fail-open behavior, unclassified-path blocking, fallback reservation, and unknown-path targeted-proof safety. |
| `R16`-`R16d` | `T12`, `T13` | `scripts/ci.sh` wrapper consumption, non-broad-smoke default behavior, fallback handling, and non-recursive broad smoke. |
| `R17`-`R17g` | `T10`, `T14`, `T18` | Source-attributed broad-smoke triggers and planned versus ordinary change handoff behavior. |
| `R18`-`R20` | `T14`, `T18` | Targeted proof before review handoff and broad smoke before final planned-initiative verification. |
| `R21`-`R21n` | `T15` | Durable manual proof fields, allowed results, manual-by-design wording, and closeout blocking behavior. |
| `R22`-`R26` | `T3`, `T12`, `T17` | Structured-output tests, stable check-ID examples, small fixtures, duplicate-test discipline, golden-file boundary, and actionable failures. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T7` | Skill change selects skill and adapter-related generated-output checks. |
| `E2` | `T8` | Review artifact change selects the change root and `review_artifacts.validate`. |
| `E3` | `T8` | `change.yaml` change selects change metadata checks and affected root. |
| `E4` | `T4`, `T9` | Unknown paths block with `unclassified-path` in v1. |
| `E5` | `T12`, `T14` | Wrapper execution does not imply broad smoke for every PR. |
| `E6` | `T10`, `T18` | Planned initiative broad smoke is required before final handoff. |
| `E7` | `T15` | Manual proof records include required structured fields and `manual by design`. |
| `E8` | `T8`, `T10`, `T12` | Release mode selects release validation and release-required breadth. |
| `E9` | `T3`, `T12` | Selector output exposes check IDs, roots, status, rationale, and blocking results. |
| `E10` | `T10`, `T14` | Broad smoke requires an authoritative trigger, not subjective risk alone. |

## Edge case coverage

- EC1, classified and unclassified paths together: `T4`, `T9`, `T12`
- EC2, generated adapter output without generator code: `T7`, `T8`, `T16`
- EC3, canonical skills plus generated `.codex/skills/`: `T7`, `T16`
- EC4, release notes with no inferable version: `T8`, `T9`
- EC5, `AGENTS.md` without workflow specs: `T9`, `T14`
- EC6, only `docs/changes/<change-id>/explain-change.md`: `T8`, `T9`
- EC7, selector code itself: `T9`, `T17`
- EC8, malformed or incomplete selector output: `T3`, `T12`
- EC9, selected command unavailable: `T12`
- EC10, manual proof `blocked` or `not-run`: `T15`
- EC11, PR and local mode same path with different breadth: `T2`, `T10`, `T12`
- EC12, main mode from a push range: `T2`, `T10`
- EC13, release mode from a tag context: `T2`, `T8`, `T10`
- EC14, contract category directory absent: `T6`, `T9`

## Test cases

### T1. Check catalog defines stable IDs and executable command templates

- Covers: `R5o`, `R5p`, `R5s`, `R5t`
- Level: unit
- Fixture/setup:
  - `scripts/validation_selection.py`
  - v1 catalog data
- Steps:
  - Load the selector catalog.
  - Assert every v1 check ID from the spec exists exactly once.
  - Assert each catalog entry has a category and command template matching the spec.
  - Assert command templates with placeholders declare required context values.
- Expected result:
  - The catalog exposes exactly the stable v1 check IDs and command templates.
- Failure proves:
  - Selector output and wrapper execution can drift from the published check contract.
- Automation location:
  - `python scripts/test-select-validation.py`

### T2. Selector CLI validates modes and mode-specific inputs

- Covers: `R3`, `R3d`-`R3i`, `R4`-`R4f`, `EC11`, `EC12`, `EC13`
- Level: integration
- Fixture/setup:
  - temporary Git repository with committed and changed fixture paths
  - `scripts/select-validation.py`
- Steps:
  - Run `local` and `explicit` mode with repeatable `--path` arguments.
  - Run `pr` and `main` mode with `--base` and `--head` commit refs.
  - Run `release` mode with `--release-version`.
  - Omit required flags for each mode and capture the result.
  - Pass `--broad-smoke` where supported.
- Expected result:
  - Valid mode invocations return JSON with the requested mode.
  - Missing required mode inputs return `status: "error"` and exit code `4`.
  - PR, main, release, local, and explicit modes all use the same selector module.
- Failure proves:
  - The selector CLI cannot serve as one reusable interface for local, PR, main, release, and explicit validation.
- Automation location:
  - `python scripts/test-select-validation.py`

### T3. Selector JSON shape is parseable and complete

- Covers: `R3j`, `R5`-`R5n`, `R5q`, `R22`, `R22a`, `R26`, `E9`, `EC8`
- Level: unit, integration
- Fixture/setup:
  - representative classified path fixture
  - malformed output fixture for wrapper tests
- Steps:
  - Run the selector for a classified path.
  - Parse stdout as JSON without prose stripping.
  - Assert required top-level fields exist.
  - Assert `classified_paths` entries include `path` and `category`.
  - Assert every selected check includes `id`, `command`, and `reason`.
  - Assert path-scoped and root-scoped checks include `paths` or `affected_roots` when needed.
  - Assert status values and exit codes match `ok`, `blocked`, `fallback`, and `error`.
- Expected result:
  - Selector output is JSON-only machine output with enough structured data for tests and wrappers.
- Failure proves:
  - Consumers would need brittle prose greps or hidden assumptions to execute selected checks.
- Automation location:
  - `python scripts/test-select-validation.py`

### T4. Expected blocked selector cases are asserted through regression tests

- Covers: `R5i`, `R5q`, `R14`-`R15b`, `E4`, `EC1`
- Level: integration
- Fixture/setup:
  - changed path `experimental/runtime/example.txt`
  - mixed changed paths including one classified path and one unclassified path
- Steps:
  - Run the selector through the test harness for an unclassified path.
  - Assert the CLI exits `2` while the harness test itself passes.
  - Assert JSON contains `status: "blocked"`, the path in `unclassified_paths`, and an `unclassified-path` blocking result.
  - Assert no empty targeted-proof result is returned for unknown paths.
  - Assert mixed classified and unclassified inputs still block automatic execution.
  - Assert `fallback` is reserved and not selected in v1 because no fallback set exists.
- Expected result:
  - Unknown paths never fail open, and the expected nonzero CLI behavior is proven by a passing regression test.
- Failure proves:
  - Contributors can receive empty or misleading targeted proof for unsupported changed paths.
- Automation location:
  - `python scripts/test-select-validation.py`

### T5. Changed-path discovery and path normalization are deterministic

- Covers: `R4a`-`R4c`, inputs and outputs, error and boundary behavior
- Level: unit, integration
- Fixture/setup:
  - temporary Git repository with tracked changes and untracked files
  - relative, redundant, and outside-repository path inputs
- Steps:
  - Derive local changed paths from tracked worktree changes.
  - Include untracked authored artifacts in local mode when no explicit paths are supplied.
  - Normalize explicit paths to repository-relative POSIX paths.
  - Reject or block path traversal and outside-repository paths.
  - Return a blocking result for an empty changed path set without valid release context.
- Expected result:
  - The selector has stable repository-relative path inputs and does not silently ignore untracked authored artifacts.
- Failure proves:
  - Local validation can under-select checks or leak machine-local path assumptions.
- Automation location:
  - `python scripts/test-select-validation.py`

### T6. First-slice categories classify governed surfaces or block explicitly

- Covers: `R6`-`R7a`, `EC14`
- Level: unit
- Fixture/setup:
  - one representative path for each first-slice category
  - absent optional directories such as `templates/**` or `schemas/**` when not present
- Steps:
  - Classify paths under `skills/**`, `dist/adapters/**`, `docs/changes/**`, `specs/**`, `docs/workflows.md`, `AGENTS.md`, `CONSTITUTION.md`, `templates/**`, `schemas/**`, and `scripts/**`.
  - Assert repository-governance and artifact-centric categories are recognized.
  - Assert arbitrary runtime or application paths block rather than expanding scope.
  - Assert optional absent category directories do not require synthetic repository paths.
- Expected result:
  - First-slice routing is explicit for governed surfaces and conservative for unsupported paths.
- Failure proves:
  - The selector has either skipped a governed category or broadened beyond the approved scope.
- Automation location:
  - `python scripts/test-select-validation.py`

### T7. Skill and adapter changes select generated-output proof

- Covers: `R8`-`R9b`, `E1`, `EC2`, `EC3`
- Level: unit, integration
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `.codex/skills/code-review/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/code-review/SKILL.md`
  - adapter generator and validator script paths
- Steps:
  - Select validation for canonical skill changes.
  - Assert `skills.validate`, `skills.regression`, and `skills.drift` are selected.
  - Assert adapter drift or validation is selected when public adapter output can be affected.
  - Select validation for generated `.codex/skills/**` and generated `dist/adapters/**` paths.
  - Select validation for adapter generator, validator, and template changes.
- Expected result:
  - Canonical and generated skill/adapter changes select the required validation and drift checks.
- Failure proves:
  - Generated output can become stale without targeted proof.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `python scripts/test-adapter-distribution.py`

### T8. Change-local, lifecycle, and release paths select scoped validators

- Covers: `R10`-`R12a`, `E2`, `E3`, `E8`, `EC4`, `EC6`, `EC13`
- Level: unit, integration
- Fixture/setup:
  - `docs/changes/2026-04-25-example/review-resolution.md`
  - `docs/changes/2026-04-25-example/reviews/code-review-r1.md`
  - multiple `docs/changes/<change-id>/change.yaml` files
  - lifecycle artifact paths under `docs/proposals/`, `specs/`, `docs/architecture/`, `docs/adr/`, and `docs/plans/`
  - release metadata and release-notes paths under `docs/releases/<version>/`
- Steps:
  - Assert review artifacts select `review_artifacts.validate` scoped to the change root.
  - Assert one or more `change.yaml` paths select `change_metadata.validate`, `change_metadata.regression`, and the correct affected roots.
  - Assert `change_metadata.validate` command receives all changed metadata files in one invocation.
  - Assert lifecycle-managed artifacts select `artifact_lifecycle.validate` scoped to touched paths.
  - Assert release metadata or release notes select `release.validate` for the inferred version.
  - Assert ambiguous release paths block or require manual routing.
  - Assert unsupported files under `docs/changes/<change-id>/` block rather than being ignored.
- Expected result:
  - Existing validators remain selected with the narrowest safe roots or paths.
- Failure proves:
  - Change-local, lifecycle, or release artifacts can bypass their existing proof surfaces.
- Automation location:
  - `python scripts/test-select-validation.py`

### T9. Workflow, governance, scripts, templates, schemas, and selector changes route safely

- Covers: `R6e`-`R6i`, `R13`-`R13b`, `R14c`, `R15b`, `E4`, `EC5`, `EC7`, `EC14`
- Level: unit
- Fixture/setup:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `templates/example.md` when templates exist
  - `schemas/example.schema.json` when schemas exist
  - selector, validation, generation, and release script paths
- Steps:
  - Assert selector implementation and selector test changes select `selector.regression`.
  - Assert validation scripts select a matching regression check when one exists in the catalog.
  - Assert workflow, governance, templates, and schemas either select deterministic contract checks or block with manual routing.
  - Assert unclassified routing is represented in structured output.
- Expected result:
  - Governance and validation-routing changes do not return empty proof and do not pretend unsupported surfaces are covered.
- Failure proves:
  - High-impact workflow or validation changes can be merged without targeted proof.
- Automation location:
  - `python scripts/test-select-validation.py`

### T10. Broad-smoke triggers preserve source attribution

- Covers: `R3i`, `R17`-`R17g`, `E6`, `E10`, `EC11`, `EC12`, `EC13`
- Level: unit, integration
- Fixture/setup:
  - selector mode inputs for `main` and `release`
  - explicit `--broad-smoke`
  - fixture active plan with `broad_smoke_required: true`
  - fixture test spec with broad-smoke validation requirement
  - fixture review-resolution requiring broad smoke
  - fixture release metadata requiring smoke
- Steps:
  - Run selector requests for each authoritative trigger source.
  - Assert output includes `broad_smoke_required: true`.
  - Assert optional `broad_smoke.required` matches the compatibility boolean.
  - Assert `broad_smoke.sources` names the source type and path or value.
  - Assert unrelated active artifacts are not discovered by whole-repo scanning unless supplied as context paths.
  - Assert subjective risk without a recorded source does not trigger broad smoke.
  - Assert a recorded source cannot be ignored by subjective judgment.
- Expected result:
  - Broad-smoke requirements remain tied to authoritative, observable sources.
- Failure proves:
  - Broad smoke can become either unexplained overhead or silently skipped handoff proof.
- Automation location:
  - `python scripts/test-select-validation.py`

### T11. Placeholder substitution produces safe selected commands

- Covers: `R5p`, `R5t`, security and privacy design
- Level: unit
- Fixture/setup:
  - catalog entries with `<adapter-version>`, `<version>`, `<change-root>`, `<change-yaml>`, and `<path>` placeholders
  - invalid context missing a required placeholder value
- Steps:
  - Build selected check command strings from catalog entries and selector context.
  - Assert placeholder values come from selector inputs, inferred affected roots, or repository defaults.
  - Assert missing placeholder values produce `status: "error"` before executable selected checks are emitted.
  - Assert command strings remain catalog-derived and do not require arbitrary JSON command execution through `eval`.
- Expected result:
  - Selected commands are reproducible, scoped, and safe for the wrapper to execute from trusted catalog data.
- Failure proves:
  - The wrapper could run stale, malformed, or user-controlled command text.
- Automation location:
  - `python scripts/test-select-validation.py`

### T12. CI wrapper consumes selector output and executes selected checks

- Covers: `R3b`, `R3c`, `R5r`, `R16`-`R16c`, `R22`-`R26`, `E5`, `E9`, `EC8`, `EC9`
- Level: integration
- Fixture/setup:
  - `scripts/ci.sh`
  - selector fixture output for `ok`, `blocked`, `fallback`, malformed JSON, missing command, and failing selected command
  - stub selected-check commands in a temporary executable path where needed
- Steps:
  - Run wrapper modes that forward selector inputs.
  - Assert wrapper validates selector JSON before executing checks.
  - Assert `ok` output executes selected checks in deterministic catalog order.
  - Assert selected root-scoped and path-scoped commands receive substituted paths.
  - Assert `blocked` output fails without running partial selected checks.
  - Assert `fallback` is reported and fails in v1 because no fallback set is defined.
  - Assert malformed JSON, missing commands, and failing selected commands produce actionable nonzero wrapper failures.
  - Assert wrapper logs mode, check ID or blocking result, affected path/root, rationale, and actual commands when available.
- Expected result:
  - `scripts/ci.sh` is a wrapper around selector-selected proof, not a second path selector or silent broad smoke alias.
- Failure proves:
  - Local and hosted CI can diverge from the selector contract.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode explicit --path <fixture-path>`

### T13. Broad-smoke wrapper mode is non-recursive

- Covers: `R16b`, `R16d`, broad-smoke flow
- Level: integration, smoke
- Fixture/setup:
  - `scripts/ci.sh`
  - broad-smoke mode fixture or repository broad-smoke command list
- Steps:
  - Run `bash scripts/ci.sh --mode broad-smoke`.
  - Assert broad-smoke mode executes the repository broad-smoke list directly.
  - Assert it does not invoke selector logic in a way that selects `broad_smoke.repo` recursively.
  - Assert normal selector modes that select `broad_smoke.repo` delegate to the same non-recursive broad-smoke function.
- Expected result:
  - Broad smoke remains available for final handoff, main, and release contexts without recursive self-selection.
- Failure proves:
  - A broad-smoke trigger can loop or skip the repository-wide proof set.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `bash scripts/ci.sh --mode broad-smoke`

### T14. Workflow guidance distinguishes targeted proof from broad smoke

- Covers: `R1`-`R2c`, `R17a`-`R20`, `R22b`, `E5`, `E6`, `E10`
- Level: contract
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Inspect workflow docs and affected stage skills.
  - Assert targeted proof is the default first proof step for non-trivial changes.
  - Assert broad smoke is required for planned initiatives before final handoff.
  - Assert ordinary non-trivial changes require broad smoke only when an authoritative trigger exists.
  - Assert release-only manual smoke remains release-specific or tool-behavior-specific.
  - Assert examples use stable check IDs and do not replace check IDs with prose categories.
- Expected result:
  - Contributors and agents see the same layered validation contract across workflow surfaces.
- Failure proves:
  - Stage guidance can over-run broad smoke too early or skip it when required.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - targeted contract assertions may live in `python scripts/test-select-validation.py` if selector wording checks are centralized there

### T15. Manual proof records and closeout behavior are contract-tested

- Covers: `R21`-`R21n`, `E7`, `EC10`
- Level: contract
- Fixture/setup:
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - fixture `docs/changes/<change-id>/verify-report.md`
  - fixture `docs/releases/<version>/release.yaml`
- Steps:
  - Assert normal-change manual proof guidance stores durable records in `verify-report.md`.
  - Assert release smoke proof guidance stores release proof in release metadata.
  - Assert required fields are check ID, result, why manual, performer, evidence, date, rationale when needed, owner when needed, and follow-up when needed.
  - Assert `manual by design` is required for intentionally non-automatable checks.
  - Assert guidance rejects replacing a manual proof with only `not tested`.
  - Assert `pass` is valid final proof.
  - Assert `fail` blocks `verify`, final `explain-change` closeout, and `pr`.
  - Assert `blocked` and `not-run` block handoff unless explicitly allowed by a governing contract with rationale, owner, and follow-up.
- Expected result:
  - Manual proof has a durable structured record and clear final-handoff behavior.
- Failure proves:
  - Manual checks can be treated as vague notes instead of governed evidence.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T16. Generated skill and adapter outputs stay synchronized after guidance changes

- Covers: `R8c`, `R9`-`R9b`, generated-output impact from the plan, `EC2`, `EC3`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
  - `dist/adapters/manifest.yaml`
- Steps:
  - Update canonical workflow-facing skills as required by implementation.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
- Expected result:
  - Canonical skills, generated Codex skill mirrors, public adapter packages, and manifest stay in sync.
- Failure proves:
  - Public adapter output can lag canonical workflow guidance.
- Automation location:
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T17. Selector tests use structured fixtures and avoid duplicate or prose-only assertions

- Covers: `R22`-`R25`, `R13a`, `R13b`
- Level: contract
- Fixture/setup:
  - `scripts/test-select-validation.py`
  - `tests/fixtures/validation-selection/` if fixture files are added
- Steps:
  - Assert selector tests parse JSON and inspect fields rather than grepping implementation text.
  - Assert literal text assertions are used only for contract literals such as stable check IDs, status values, or blocking-result codes.
  - Assert fixture paths are small and single-purpose for each changed-surface category.
  - Assert repeated invariants have one primary contract test and only distinct-risk alignment tests.
  - Assert no large golden file is used except for stable generated outputs or canonical record formats.
- Expected result:
  - The selector regression suite is fast, maintainable, and behavior-oriented.
- Failure proves:
  - Test maintenance costs can grow without improving contract confidence.
- Automation location:
  - `python scripts/test-select-validation.py`

### T18. Final validation proves targeted proof plus planned broad smoke

- Covers: `R1`-`R2c`, `R17a`, `R18`, `R19`, acceptance criteria
- Level: smoke
- Fixture/setup:
  - completed M1-M3 implementation
  - active plan with `broad_smoke_required: true`
  - change metadata and review-resolution closeout records
- Steps:
  - Run selector-targeted proof for final changed surfaces.
  - Run `bash scripts/ci.sh --mode explicit --path scripts/select-validation.py --path scripts/validation_selection.py --path scripts/ci.sh`.
  - Run `bash scripts/ci.sh --mode broad-smoke`.
  - Run review artifact closeout validation.
  - Run change metadata validation.
  - Run artifact lifecycle validation over proposal, spec, test spec, architecture, plan, and change metadata.
  - Run `git diff --check -- .`.
- Expected result:
  - The branch has targeted proof, broad-smoke proof for the planned initiative, and synchronized lifecycle state before `code-review`, `verify`, `explain-change`, and `pr`.
- Failure proves:
  - The change optimized local proof order but did not preserve final confidence gates.
- Automation location:
  - M4 validation commands in `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`

## Fixtures and data

- Selector fixture paths should be small literal path sets, with one fixture per first-slice category where possible.
- Git-mode tests should create temporary repositories using `git init`, local fixture commits, and explicit base/head refs.
- Wrapper tests may use stub selected commands in temporary directories to avoid running the full repository check set for every failure-path assertion.
- Release mode fixtures should use minimal `docs/releases/<version>/release.yaml` and release-notes paths.
- Manual proof fixtures should use minimal `verify-report.md` tables and release metadata rows.
- Existing fixtures under `tests/fixtures/adapters/`, `tests/fixtures/artifact-lifecycle/`, and `tests/fixtures/review-artifacts/` should be reused when the selector only needs representative paths.

## Mocking/stubbing policy

- Do not mock selector classification or catalog functions in selector unit tests.
- It is acceptable to stub selected-check command execution in wrapper tests when the test proves wrapper behavior rather than validator behavior.
- Git behavior should be tested with temporary repositories instead of string-only mocks where mode behavior depends on real Git ranges or untracked files.
- Do not require hosted CI, network services, installed agent tools, or external smoke environments for non-smoke tests.

## Migration or compatibility tests

- Existing direct validation commands must remain usable after selector adoption.
- Existing `bash scripts/ci.sh` users must receive actionable mode guidance and command output after wrapper migration.
- Hosted CI must remain a thin wrapper around repository-owned scripts and must not embed a second path-selection implementation in workflow YAML.
- Generated `.codex/skills/` and public adapter output must remain deterministic and reproducible from canonical sources.

## Observability verification

- Selector JSON must include mode, status, changed paths, classified paths, unclassified paths, selected checks, affected roots, broad-smoke state, blocking results, and rationale.
- Wrapper output must name the selector mode and each command actually run.
- Blocking and failure outputs must identify the relevant mode, check ID or blocking result, affected path or root, and rationale when available.
- Broad-smoke output must preserve trigger source records when broad smoke is required.

## Security/privacy verification

- Selector output and wrapper logs must not expose secrets, tokens, private keys, or machine-local sensitive paths.
- Path normalization tests must reject outside-repository path traversal.
- Wrapper tests must prove command execution comes from trusted catalog data and does not use arbitrary JSON command text through `eval`.
- Manual proof records must not require committing private credentials, private UI output, or private hosted-service data.
- Targeted-proof selection must not weaken release validation, security checks, generated-output drift checks, or manual release smoke gates.

## Performance checks

- Selector unit and fixture tests should complete quickly enough to run before review handoff.
- Selector execution must select checks without running the selected validators.
- Wrapper broad-smoke tests may run the broader repository set only in M4 or explicit broad-smoke validation, not inside every selector unit test.
- No dependency graph inference or repository-wide artifact scanning should be added in the first implementation slice.

## Manual QA checklist

- No manual QA is required for selector and wrapper non-smoke validation.
- Release-only manual smoke remains outside this implementation unless a release contract or later handoff explicitly requires it.
- If a required manual check is introduced during implementation, record it in `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/verify-report.md` with the fields from `T15`.

## What not to test

- Do not test installed Codex, Claude Code, or OpenCode behavior for this selector implementation.
- Do not build a dependency graph for arbitrary app/runtime code.
- Do not duplicate existing validator behavior inside selector tests; assert selected check IDs and scopes instead.
- Do not add a conservative fallback execution suite in v1 because fallback behavior is explicitly deferred until a later approved spec defines the fallback set.
- Do not use broad golden files for selector output unless the output becomes a stable generated record format.

## Uncovered gaps

- None for the approved v1 scope.
- A future conservative fallback implementation will require a new spec, architecture update, and test spec because the fallback check set is intentionally undefined in this change.

## Next artifacts

- `implement` for M1 after this active test spec is accepted as the proof plan.
- `code-review` after implementation milestones record targeted proof.
- `verify` after targeted proof and planned broad smoke are complete.

## Follow-on artifacts

- None yet.

## Readiness

This active test spec is the current proof-planning surface for `specs/test-layering-and-change-scoped-validation.md` and `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`.

Immediate next repository stage: `implement`.

Implementation must begin test-first with `python scripts/test-select-validation.py` covering selector and wrapper behavior before production selector or wrapper code is relied on.
