# Contributing

Thanks for contributing.

## Before opening a pull request

1. Read `AGENTS.md`.
2. Check whether the task needs an owning Design and execution plan.
3. Keep the change small and reviewable.
4. Run the relevant verification and list the commands in the PR.
5. Update docs or examples when behavior changes.

## Markdown Source Lines

For review-critical Markdown, break source lines where meaning breaks, not where an editor column counter wraps.
Keep complete sentences, list items, commands, and lifecycle chains intact when practical; use bullets or other Markdown structure when prose becomes dense.
[System](docs/design/system.md#living-test-design-composition) owns shared test-design and proof-quality rules. [Validation](docs/design/engineering/validation.md) owns source-format checks and validation execution.

Before handing off changed covered prose, run:

```bash
python scripts/validate-documentation-prose.py --mode enforce --path README.md --path VISION.md
```

## Pull request expectations

- One focused change per PR.
- Explain why the change exists.
- State what was verified.
- Call out assumptions, scope limits, and follow-up work.

## Good first contributions

- docs clarifications
- small bug fixes with regression coverage
- test improvements
- build and tooling cleanup with clear scope

## Validation scope

Repository tests live in `tests/skill/` and `tests/engineering/{validation,packaging,release}/`; package tests stay in `packages/rigorloop/test/`. Supported operational commands remain at the `scripts/` root. Reusable implementation belongs in `scripts/lib/{validation,packaging,release}/`, using explicit package imports; authored operational inputs belong in `scripts/resources/`. Keep command arguments and exit behavior stable when moving internal code; update subprocess readers and copied test repositories together. Follow [Validation’s test organization](docs/design/engineering/validation.md#test-sources-groups-and-fixtures) for behavior groups, shared fixtures and evidence selection. Start from the [shared test-design rules](docs/design/test-design/rules.md), with [script structure](docs/design/test-design/rules.md#test-script-structure) and [worked examples](docs/design/test-design/rules.md#worked-authoring-examples) for scenarios and reusable setup; [test-design navigation](docs/design/test-design/README.md) locates model-owned coverage.

Use `bash scripts/ci.sh --mode local` for checks selected from the working-tree changes, or `--mode explicit --path PATH` for a bounded surface. PR CI uses the same selector with `--mode pr --base SHA --head SHA`; unclassified paths or failed preflight checks block execution. PR validation checks current record stores at the exact head revision; archival stores are excluded without running retired validators. Main CI retains the full direct gate suite, and release validation retains its existing policy.

Documentation is classified by its role: skills, model contracts, records and executable examples still select their owning checks. A Markdown extension alone does not grant an exemption. Selected checks report durations; full main gates report progress and duration per gate. The unified Validation change retires cache-only and historical-classification checks under its exact source map; surviving required cases and failure detection remain protected.

Current validation routing and execution are owned by [Validation](docs/design/engineering/validation.md). The catalog supplies trusted commands and dependencies to one bounded executor. All repository-owned Python unittest and native Node test populations support independent case execution within the shared worker budget. Use `--jobs N` to bound concurrency; `--jobs 1` retains the same case coverage. Direct suite commands remain available for reproduction. Validators without test cases retain their declared command constraints. Equivalent requests for the same canonical check execute once per invocation; distinct scopes and release configurations retain their own checks. Current validation executes checks and does not reuse a validation-result cache.

Add `--durations N` to show the slowest dispatched workers, or `--durations 0` to show all. Each row identifies a native case or a non-case check, its actual status and its rerun command. Unstarted work is unmeasured and excluded from ranking. Set `RIGORLOOP_VALIDATION_RESULT_JSON` to collect the compatible JSON envelope in any validation mode; `RIGORLOOP_BROAD_SMOKE_RESULT_JSON` remains a broad-smoke-only alias. If both are set for broad-smoke, they must resolve to the same destination.

```bash
validation_report_dir=$(mktemp -d)
RIGORLOOP_VALIDATION_RESULT_JSON="$validation_report_dir/results.json" \
  bash scripts/ci.sh --mode explicit --path scripts/ci.sh --durations 10
```

The report parent must already exist. Choose a private report path outside source files, selected inputs and worker outputs. The invocation reserves that destination until finalization, atomically replaces it and removes only its own temporary files. A concurrent writer rejects before checks launch. Children do not inherit the parent destination; prepared release validation hands back a private report while the parent retains ownership.

Worker elapsed time includes launch, interpreter/import, fixtures, execution and owned-process cleanup; it excludes queue wait and discovery. Execution wall time includes discovery and scheduling through cleanup, and excludes selection, preflight and report formatting/I/O. Summed worker durations are occupied worker time, not CPU usage or a speedup estimate. Reports preserve failed and unstarted results and declare incomplete collection; zero duration with `started: false` is an unmeasured placeholder. Compare only equivalent scopes, worker budgets and source/environment conditions, retaining exact changed-subject identities for dirty trees. See [execution-cost reporting](docs/design/engineering/validation.md#execution-cost-reporting) for the full measurement and failure contract.
