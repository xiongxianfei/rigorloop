# Test Layering and Change-Scoped Validation

## Status

- approved

## Related proposal

- [Test Layering and Change-Scoped Validation](../docs/proposals/2026-04-25-test-layering-and-change-scoped-validation.md)

## Goal and context

This spec defines the contributor-visible validation contract for layered proof, change-scoped validation selection, `scripts/ci.sh` wrapper behavior, and structured manual proof records.

RigorLoop uses many validation surfaces because it optimizes for reviewability, traceability, generated-output correctness, and release safety. This contract does not reduce required proof. It defines how contributors and agents select the cheapest valid proof first, when broad smoke is required, and how repository-owned automation must avoid silently skipping required validation.

The core rule is:

```text
One selector, many modes.
```

The selector is the source of truth for validation routing. `scripts/ci.sh` is the wrapper that executes selected validation. The wrapper is not synonymous with broad smoke.

## Glossary

- `validation selector`: the repository-owned command that maps changed paths and mode to selected validation checks.
- `check catalog`: the versioned repository contract that maps stable check IDs to executable validation commands.
- `check ID`: a stable identifier for one validation check, such as `skills.validate`.
- `selected check`: one repository-owned validation command selected by the validation selector.
- `affected root`: the smallest repository path or change root a selected check is scoped to, such as `docs/changes/<change-id>/`.
- `targeted proof`: the selected checks that directly prove changed surfaces and governing dependencies before review handoff.
- `broad smoke`: broader validation intended to catch cross-surface drift before final handoff, push-to-main, or release.
- `release validation`: release-specific checks for release metadata, generated adapter packages, release notes, smoke matrix rules, and security checks.
- `validation mode`: the selector context that determines required breadth, such as `local`, `pr`, `main`, or `release`.
- `unclassified path`: a changed path that the selector cannot map to a supported first-slice category.
- `conservative fallback validation set`: a repository-defined safe check set used when path classification is uncertain and the selector chooses not to block.
- `manual proof`: durable evidence for a check that cannot reasonably be automated.
- `manual by design`: an explicit marker that a proof surface is intentionally manual rather than accidentally untested.
- `wrapper`: an orchestration command that invokes selected validation checks but does not itself define validation breadth.
- `first-slice category`: a path category supported by the initial selector contract.
- `selector status`: the top-level selector result status: `ok`, `blocked`, `fallback`, or `error`.

## Examples first

### Example E1: skill change selects skill and generated-output checks

Given a contributor changes `skills/code-review/SKILL.md`
When `python scripts/select-validation.py --mode local` evaluates the changed path
Then the selected check IDs include `skills.validate`, `skills.regression`, and `skills.drift`
And the selected check IDs include `adapters.drift` or `adapters.validate` when public adapter output can be affected.

### Example E2: review artifact change selects one changed root

Given a contributor changes `docs/changes/2026-04-25-example/review-resolution.md`
When the selector evaluates the changed path
Then the output includes `docs/changes/2026-04-25-example/` as an affected review artifact root
And the selected check IDs include `review_artifacts.validate`.

### Example E3: change metadata change selects change-local checks

Given a contributor changes `docs/changes/2026-04-25-example/change.yaml`
When the selector evaluates the changed path
Then the output includes `docs/changes/2026-04-25-example/` as an affected root
And the selected check IDs include `change_metadata.validate` and `change_metadata.regression`.

### Example E4: unknown path does not fail open

Given a contributor changes `experimental/runtime/example.txt`
And that path is not classified by the first-slice selector
When the selector evaluates the changed path
Then the selector returns an explicit `unclassified-path` blocking result requiring manual routing
Or it selects the repository-defined conservative fallback validation set.

### Example E5: wrapper is not broad smoke

Given an ordinary non-trivial documentation change has classified changed paths
When `scripts/ci.sh` runs in PR mode
Then it executes the selector-selected PR checks
And it does not imply broad-smoke mode unless policy, risk, handoff, main, or release context requires that mode.

### Example E6: planned initiative requires broad smoke before final handoff

Given a planned initiative records targeted proof during implementation
When `verify` evaluates final handoff readiness
Then broad smoke evidence is required before the planned initiative can be branch-ready.

### Example E7: manual proof is structured

Given a release smoke check requires live tool UI interaction
When the check is recorded as manual proof
Then the record includes a check ID, result, manual rationale, performer, evidence location, and date
And the rationale says `manual by design`.

### Example E8: release mode selects release validation

Given a maintainer validates a release tag
When `scripts/ci.sh` or release automation runs release mode
Then the selected check IDs include `release.validate`
And broad-smoke or release-specific check IDs are selected according to the release contract.

### Example E9: selector output is structured

Given changed paths include `specs/review-finding-resolution-contract.md`
When the selector runs
Then JSON output identifies selected check IDs, affected roots, mode, status, rationale, and whether any result blocks automatic execution.

### Example E10: broad smoke requires an authoritative trigger

Given an ordinary non-trivial change has targeted proof
When no selector mode, CLI flag, active plan, test spec, review-resolution, or release metadata requires broad smoke
Then broad-smoke mode is not required merely because a contributor subjectively believes the change has some risk.

## Requirements

R1. The repository MUST define layered validation using these layers:
- fast structural tests;
- contract tests;
- change-scoped integration tests;
- broad smoke;
- release-only manual smoke.

R2. The workflow MUST distinguish targeted proof from broad smoke.

R2a. Targeted proof MUST be the default first proof step for non-trivial changes.

R2b. Broad smoke MUST NOT be treated as the default first proof step for every local edit.

R2c. Release-only manual smoke MUST remain reserved for release readiness or tool behavior that repository-owned structural checks cannot prove.

R3. The repository MUST provide a standalone validation selector command:

```text
python scripts/select-validation.py
```

R3a. The selector command MUST be the source of truth for validation selection logic.

R3b. `scripts/ci.sh` MUST consume selector output rather than owning separate path-selection logic after selector adoption.

R3c. Hosted CI and local CI MUST use the same selector logic.

R3d. The selector CLI MUST support these invocation forms:

```text
python scripts/select-validation.py --mode local --path <path>...
python scripts/select-validation.py --mode explicit --path <path>... [--broad-smoke]
python scripts/select-validation.py --mode pr --base <sha> --head <sha>
python scripts/select-validation.py --mode main --base <sha> --head <sha>
python scripts/select-validation.py --mode release --release-version <version>
```

R3e. `--mode` MUST be required for every selector invocation.

R3f. `--path` MUST be repeatable and MUST be supported for `local` and `explicit` mode.

R3g. `--base` and `--head` MUST be required for `pr` and `main` modes.

R3h. `--release-version` MUST be required for `release` mode.

R3i. `--broad-smoke` MUST be supported as an explicit broad-smoke override for modes where the flag is meaningful.

R3j. Selector stdout MUST be JSON machine output by default. If `--json` is supported, it MUST preserve the same JSON shape.

R4. The selector MUST support at least these validation modes:
- `local`;
- `explicit`;
- `pr`;
- `main`;
- `release`.

R4a. Mode-specific behavior MUST change validation breadth without creating separate selection logic.

R4b. Explicit mode MUST use the provided `--path` values as the changed path set.

R4c. Local mode MUST use provided `--path` values when present and MAY derive changed paths from the local Git worktree when paths are not provided.

R4d. PR mode MUST select targeted proof plus required PR-scope checks.

R4e. Main mode MUST select broader smoke plus required main-branch checks.

R4f. Release mode MUST select release validation and any release-required smoke or metadata checks.

R5. The selector output MUST be JSON that tests and wrappers can consume without grepping prose.

R5a. Selector output MUST include the selected validation checks.

R5b. Selector output MUST include affected roots when a check is root-scoped.

R5c. Selector output MUST include the validation mode.

R5d. Selector output MUST include rationale for why each check was selected.

R5e. Selector output MUST identify blocking results, including unclassified changed paths.

R5f. Selector JSON MUST contain these top-level fields:
- `mode`;
- `status`;
- `changed_paths`;
- `classified_paths`;
- `unclassified_paths`;
- `selected_checks`;
- `affected_roots`;
- `broad_smoke_required`;
- `blocking_results`;
- `rationale`.

R5g. `status` MUST use exactly one of:
- `ok`;
- `blocked`;
- `fallback`;
- `error`.

R5h. `ok` means selection completed without blocking results.

R5i. `blocked` means the selector cannot safely select validation and manual routing is required.

R5j. `fallback` means classification was incomplete and the repository-defined conservative fallback validation set was selected.

R5k. `error` means the invocation was invalid or an internal selector failure occurred.

R5l. Each `classified_paths` entry MUST include `path` and `category`.

R5m. Each `selected_checks` entry MUST include `id`, `command`, and `reason`.

R5n. Each `selected_checks` entry MAY include `paths` or `affected_roots` when the check is path-scoped or root-scoped.

R5o. Each selected check `id` MUST come from the v1 check catalog.

R5p. Each selected check `command` MUST match the command defined for that check ID in the v1 check catalog, after documented placeholder substitution.

R5q. Selector exit codes MUST be:
- `0` for `ok`;
- `2` for `blocked`;
- `3` for `fallback`;
- `4` for `error`.

R5r. `scripts/ci.sh` MUST handle selector exit code `3` as fallback-selected, report the fallback state, and then either execute the selected fallback checks or fail with a clear message when fallback execution is not supported.

R5s. The v1 check catalog MUST include these stable check IDs:

```yaml
checks:
  skills.validate:
    command: python scripts/validate-skills.py
    category: skills

  skills.regression:
    command: python scripts/test-skill-validator.py
    category: skills

  skills.drift:
    command: python scripts/build-skills.py --check
    category: skills

  adapters.regression:
    command: python scripts/test-adapter-distribution.py
    category: adapters

  adapters.drift:
    command: python scripts/build-adapters.py --version <adapter-version> --check
    category: adapters

  adapters.validate:
    command: python scripts/validate-adapters.py --version <adapter-version>
    category: adapters

  review_artifacts.regression:
    command: python scripts/test-review-artifact-validator.py
    category: review-artifacts

  review_artifacts.validate:
    command: python scripts/validate-review-artifacts.py <change-root>...
    category: review-artifacts

  artifact_lifecycle.regression:
    command: python scripts/test-artifact-lifecycle-validator.py
    category: lifecycle

  artifact_lifecycle.validate:
    command: python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...
    category: lifecycle

  change_metadata.regression:
    command: python scripts/test-change-metadata-validator.py
    category: change-metadata

  change_metadata.validate:
    command: python scripts/validate-change-metadata.py <change-yaml>...
    category: change-metadata

  release.validate:
    command: python scripts/validate-release.py --version <version>
    category: release

  selector.regression:
    command: python scripts/test-select-validation.py
    category: selector

  broad_smoke.repo:
    command: bash scripts/ci.sh --mode broad-smoke
    category: broad-smoke
```

R5t. Placeholder values such as `<adapter-version>`, `<version>`, `<change-root>`, `<change-yaml>`, and `<path>` MUST be supplied from selector inputs, inferred affected roots, or repository defaults before a wrapper executes a command.

R6. The selector MUST support the first-slice categories:
- skills;
- generated adapters;
- review artifacts;
- lifecycle artifacts;
- release metadata;
- workflow specs;
- workflow summaries;
- templates;
- schemas;
- validation, generation, selector, and release scripts.

R6a. The first-slice path set MUST include `skills/**`.

R6b. The first-slice path set MUST include `dist/adapters/**`.

R6c. The first-slice path set MUST include `docs/changes/**`.

R6d. The first-slice path set MUST include `specs/**`.

R6e. The first-slice path set MUST include `docs/workflows.md`.

R6f. The first-slice path set MUST include `AGENTS.md` and `CONSTITUTION.md` when touched or explicitly declared affected.

R6g. The first-slice path set MUST include `templates/**` when that path exists.

R6h. The first-slice path set MUST include `schemas/**` when that path exists.

R6i. The first-slice path set MUST include validation, generation, selector, and release scripts under `scripts/**`.

R7. The first selector slice MUST remain repository-governance and artifact-centric.

R7a. The selector MUST NOT broaden to arbitrary app or runtime code unless a later approved spec extends the category contract.

R8. A skill change under `skills/**` MUST select `skills.validate`.

R8a. A skill change under `skills/**` MUST select `skills.regression`.

R8b. A skill change under `skills/**` MUST select `skills.drift`.

R8c. A skill change under `skills/**` MUST select `adapters.drift` or `adapters.validate` when public adapter output can be affected.

R9. A generated adapter or adapter-generation change MUST select `adapters.regression`.

R9a. A generated adapter or adapter-generation change MUST select `adapters.drift`.

R9b. A generated adapter or adapter-generation change MUST select `adapters.validate`.

R10. A review artifact change under `docs/changes/<change-id>/` that touches `reviews/`, `review-log.md`, or `review-resolution.md` MUST select `review_artifacts.validate` scoped to that change root.

R10a. A change-local metadata change matching `docs/changes/<change-id>/change.yaml` MUST select `change_metadata.validate`.

R10b. A change-local metadata change matching `docs/changes/<change-id>/change.yaml` MUST select `change_metadata.regression`.

R10c. For `docs/changes/<change-id>/change.yaml`, the affected root MUST be `docs/changes/<change-id>/`.

R10d. `change_metadata.validate` MUST support validating multiple changed `change.yaml` files in one command invocation.

R11. A lifecycle-managed artifact change MUST select `artifact_lifecycle.validate` for the touched paths.

R11a. Lifecycle-managed artifact paths include proposals, specs, test specs, architecture documents, ADRs, and plan files governed by the repository lifecycle contract.

R12. A release metadata or release notes change MUST select `release.validate` for the affected version when the version can be inferred.

R12a. When the affected release version cannot be inferred, the selector MUST return a blocking result requiring manual routing or select a conservative fallback validation set.

R13. A workflow summary, governance, template, schema, validation script, generation script, selector script, or release script change MUST select checks that prove the changed validation routing or contract surface.

R13a. A change to selector implementation or selector tests MUST select `selector.regression` and broad enough wrapper proof to show selector output remains consumable.

R13b. A change to a validation script MUST select the matching regression check when one exists in the v1 check catalog.

R14. The selector MUST NOT fail open.

R14a. If any changed path is unclassified, the selector MUST either return an explicit `unclassified-path` blocking result requiring manual routing or select a repository-defined conservative fallback validation set.

R14b. The selector MUST never return empty targeted proof for unknown changed paths.

R14c. The selector MUST make the chosen unclassified-path handling visible in structured output.

R15. The conservative fallback validation set MUST be repository-defined and deterministic.

R15a. The fallback set MUST be broad enough to avoid silently skipping validation for the unclassified changed paths.

R15b. If the repository cannot define a safe fallback for a mode, the selector MUST block with `unclassified-path` instead of guessing.

R16. `scripts/ci.sh` MUST remain a wrapper for selected validation.

R16a. `scripts/ci.sh` MUST NOT be treated as synonymous with broad smoke.

R16b. The wrapper MAY execute targeted proof, broad-smoke mode, or release validation.

R16c. The wrapper alone MUST NOT imply that broad-smoke validation is required for every PR.

R16d. When executing `broad_smoke.repo`, the wrapper MUST avoid recursive self-selection and MUST execute broad-smoke validation through a non-recursive broad-smoke mode.

R17. Broad-smoke mode MUST be required when planned, policy, risk, handoff, main, or release context triggers it.

R17a. Planned initiatives MUST record both targeted proof and broad smoke before final handoff.

R17b. Ordinary non-trivial changes MUST record targeted proof and MUST add broad smoke only when repository policy, risk, or handoff context triggers it.

R17c. Broad-smoke requirement MUST come from one or more authoritative trigger sources.

R17d. Allowed authoritative broad-smoke trigger sources are:
- selector mode `main`;
- selector mode `release`;
- explicit selector input `--broad-smoke`;
- active execution plan field `broad_smoke_required: true`;
- test-spec validation requirement;
- review-resolution requirement;
- release metadata requirement.

R17e. When broad smoke is triggered by an authored artifact, that artifact SHOULD record `broad_smoke_required: true` and a human-readable `broad_smoke_reason`.

R17f. Unrecorded subjective risk MUST NOT silently require broad-smoke mode.

R17g. Unrecorded subjective risk MUST NOT remove broad-smoke mode when an authoritative trigger requires it.

R18. Before `code-review` or review handoff, non-trivial changes MUST have targeted proof evidence or an explicit blocker explaining why targeted proof could not run.

R19. Before final `verify` branch-ready for a planned initiative, broad smoke evidence MUST exist.

R20. Before final `verify` branch-ready for an ordinary non-trivial change, broad smoke evidence MUST exist only when triggered by repository policy, risk, handoff context, main mode, or release mode.

R21. Manual proof MUST be recorded as durable structured evidence.

R21a. Manual proof records MUST include a check ID.

R21b. Manual proof records MUST include a result value of `pass`, `fail`, `blocked`, or `not-run`.

R21c. Manual proof records MUST include why the check is manual.

R21d. Manual proof records MUST include the performer.

R21e. Manual proof records MUST include the evidence location.

R21f. Manual proof records MUST include the date.

R21g. A check that is intentionally not automatable MUST be labeled `manual by design`.

R21h. A check MUST NOT be represented only as `not tested` when it is intentionally manual.

R21i. Manual proof result `pass` is valid final proof for the named manual check.

R21j. Manual proof result `fail` MUST block `verify`, final `explain-change` closeout, and `pr`.

R21k. Manual proof result `blocked` MUST block handoff unless the governing stage or release contract explicitly allows blocked manual proof.

R21l. Manual proof result `not-run` MUST NOT count as final proof unless the governing stage or release contract explicitly allows `not-run`.

R21m. A manual proof record with result `blocked` or `not-run` that is temporarily allowed by a governing contract MUST include rationale, owner, and follow-up.

R21n. A manual proof record with result `fail` SHOULD include a failure reason when that reason is available.

R22. Selector tests MUST prove behavior through structured output or fixture execution rather than grepping implementation text.

R22a. Tests MAY assert literal text only when that literal text is itself part of the contract.

R22b. Examples MUST use stable selected-check IDs from the v1 check catalog instead of prose descriptions of check categories.

R23. Validation tests SHOULD use small, single-purpose fixtures for changed-path categories.

R24. Duplicate validation of the same invariant SHOULD be minimized.

R24a. A normative contract invariant SHOULD have one primary contract test plus alignment tests only where the additional layer covers a distinct risk.

R25. Golden-file tests SHOULD be reserved for stable generated outputs and canonical record formats.

R26. Selector and wrapper failures MUST identify the mode, selected check or blocking result, affected path or root, and rationale when that information is available.

## Inputs and outputs

### Inputs

- Changed paths from local Git diff, explicit path arguments, PR diff, push-to-main range, or release context.
- Selector mode: `local`, `explicit`, `pr`, `main`, or `release`.
- Repeatable `--path` values for `local` and `explicit` mode.
- `--base` and `--head` commit references for `pr` and `main` mode.
- `--release-version` for release mode.
- Optional `--broad-smoke` explicit override.
- Optional explicit affected roots or release version when automatic inference is insufficient.
- Repository-owned validation command catalog.
- Repository-defined conservative fallback validation set.

### Outputs

- Structured selector output containing mode, selected checks, affected roots, rationale, and blocking results.
- JSON selector status using `ok`, `blocked`, `fallback`, or `error`.
- Exit status indicating whether selected validation can proceed automatically.
- Wrapper execution output from `scripts/ci.sh` naming commands actually run.
- Manual proof records when a check is manual by design or externally blocked, including required closeout fields.

## State and invariants

- The selector is the source of truth for validation routing.
- `scripts/ci.sh` is an execution wrapper and does not redefine validation breadth.
- Targeted proof remains required for non-trivial changes before review handoff.
- Broad smoke remains a triggered gate, not a universal first step.
- Unknown paths must not produce empty targeted proof.
- Release validation remains stricter than ordinary local or PR validation.
- Repository-owned validation commands remain authoritative over hosted workflow glue.

## Error and boundary behavior

- If changed paths are empty and no explicit mode context provides a range, the selector MUST return a blocking result requiring an explicit path or range.
- If required mode-specific CLI inputs are missing, the selector MUST return `status: "error"` and exit code `4`.
- If a release version is required but cannot be inferred, the selector MUST block or use a conservative fallback that includes release validation only when a safe target can be determined.
- If selector output is malformed, `scripts/ci.sh` MUST fail instead of running an implicit default.
- If selector output has `status: "blocked"`, `scripts/ci.sh` MUST fail unless an explicit manual-routing workflow handles the blocking result.
- If selector output has `status: "fallback"`, `scripts/ci.sh` MUST report fallback mode before executing fallback checks.
- If a selected validation command is unavailable, the wrapper MUST fail and identify the unavailable command.
- If any selected check fails, the wrapper MUST fail and preserve the failing command output.
- If manual proof is required but missing, `verify` MUST treat the proof as incomplete.
- If required manual proof has result `fail`, `verify` MUST fail final closeout.
- If required manual proof has result `blocked` or `not-run`, `verify` MUST keep handoff open unless the governing contract explicitly allows that state and the record contains rationale, owner, and follow-up.
- If unclassified changed paths are present with classified paths, the selector MUST still surface the unclassified paths and MUST NOT proceed with only the classified targeted proof unless the conservative fallback is selected.

## Compatibility and migration

- Existing explicit validation commands remain valid.
- Existing contributors MAY continue to run specific repository-owned validation commands directly when a plan, test spec, or review asks for them.
- `scripts/ci.sh` remains the stable wrapper command, but its internal selection should migrate to selector output.
- Hosted CI should continue to use repository-owned scripts rather than embedding validation logic directly in workflow YAML.
- The first implementation may preserve current broad checks while adding selector output, but it must not claim change-scoped optimization until `scripts/ci.sh` consumes the selector.
- Rollback is to direct explicit validation commands and the previous wrapper behavior while selector rules are repaired.

## Observability

- Selector output MUST show why each check was selected.
- Selector output MUST be valid JSON for machine consumers.
- Wrapper output MUST name each command actually run.
- Blocking selector results MUST be visible to contributors without requiring debug flags.
- Manual proof records MUST link or point to durable evidence.
- Hosted CI logs MUST show the selector mode and selected checks.

## Security and privacy

- Selector output and wrapper logs MUST NOT expose secrets, credentials, tokens, private keys, or machine-local sensitive paths.
- Manual proof evidence MUST NOT require committing private credentials or private tool output.
- Release validation and security checks MUST NOT be weakened by targeted-proof selection.
- Unknown or unclassified paths MUST NOT bypass validation.

## Accessibility and UX

No user interface is involved. Contributor-facing command output should remain readable, explicit, and actionable.

## Performance expectations

- Local targeted selection SHOULD complete quickly enough to be used before review handoff.
- Selector execution SHOULD avoid running validation commands itself; it should select checks and let wrappers or contributors execute them.
- The selector SHOULD avoid dependency graph inference in the first slice unless a later approved spec requires it.

## Edge cases

EC1. A change includes both classified and unclassified paths.

EC2. A change touches generated adapter output but not generator code.

EC3. A change touches canonical skills and generated `.codex/skills/` output.

EC4. A change touches release notes but the version cannot be inferred from the path.

EC5. A change touches `AGENTS.md` but not workflow specs.

EC6. A change touches only `docs/changes/<change-id>/explain-change.md` and no review artifacts.

EC7. A change touches selector code itself.

EC8. Selector output is malformed or missing required fields.

EC9. A selected command is unavailable in the contributor environment.

EC10. A manual proof check is `blocked` or `not-run`.

EC11. PR mode and local mode classify the same changed path but select different breadth.

EC12. Main mode runs after a merge commit with a push range instead of a working tree diff.

EC13. Release mode runs from a tag context.

EC14. A path category exists in the contract but the directory is absent from the repository.

## Non-goals

- Reducing required proof for non-trivial changes.
- Replacing full CI, release checks, generated-output drift checks, or manual adapter smoke.
- Creating a general-purpose dependency graph for arbitrary application code.
- Selecting tests for app/runtime code that this repository does not currently contain.
- Replacing human review.
- Requiring every documentation expectation to be machine-enforced in the first implementation slice.
- Requiring ordinary contributors to install Claude Code, OpenCode, or Codex for non-smoke validation.

## Acceptance criteria

- A standalone selector command exists and emits structured selected checks.
- `scripts/ci.sh` consumes selector output instead of owning independent path-selection behavior.
- Selector fixtures cover skills, generated adapters, review artifacts, change metadata, lifecycle artifacts, release metadata, workflow specs, workflow summaries, `AGENTS.md`, `CONSTITUTION.md`, templates, schemas, validation scripts, and unclassified paths.
- Selector fixtures include changed `docs/changes/<change-id>/change.yaml` paths and prove `change_metadata.validate`, `change_metadata.regression`, and the correct affected root are returned.
- Unclassified paths cannot produce empty targeted proof.
- PR, main, and release modes use the same selector logic with mode-specific breadth.
- Selector output uses the required JSON fields, status enum, selected-check fields, and exit codes.
- Selected checks use stable v1 check IDs from the catalog.
- Broad-smoke mode is triggered only by authoritative recorded sources.
- Manual proof records have the required structured fields.
- Manual proof closeout behavior blocks handoff for `fail`, and for `blocked` or `not-run` unless a governing contract explicitly allows them.
- Workflow docs and affected stage skills distinguish targeted proof from broad smoke without implying broad smoke for every PR.
- Validation evidence can show the commands actually run.

## Open questions

None.

## Next artifacts

- `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`.
- `plan-review`.
- `specs/test-layering-and-change-scoped-validation.test.md`.
- Implementation after plan-review and test-spec.

## Follow-on artifacts

- `spec-review`: approved after SR2 updates; no material findings remain open.
- `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- `architecture-review`: approved by `architecture-review-r2`.
- `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`
- `plan-review`: approved by `plan-review-r2`.
- `specs/test-layering-and-change-scoped-validation.test.md`

## Readiness

Approved by `spec-review`; architecture approved by `architecture-review-r2`; execution plan approved by `plan-review-r2`; matching test spec is active.

Immediate next repository stage: `implement`.
