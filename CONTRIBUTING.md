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
[Validation](docs/design/engineering/validation.md) owns source-formatting and proof requirements.

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

Use `bash scripts/ci.sh --mode local` for checks selected from the working-tree changes, or `--mode explicit --path PATH` for a bounded surface. PR CI uses the same selector with `--mode pr --base SHA --head SHA`; unclassified paths or failed preflight checks block execution. PR validation checks current record stores at the exact head revision; archival stores are excluded without running retired validators. Main CI retains the full direct gate suite, and release validation retains its existing policy.

Documentation is classified by its role: skills, model contracts, records and executable examples still select their owning checks. A Markdown extension alone does not grant an exemption. Selected checks report durations; full main gates report progress and duration per gate. The unified Validation change retires cache-only and historical-classification checks under its exact source map; surviving required cases and failure detection remain protected.

Current validation routing and execution are owned by [Validation](docs/design/engineering/validation.md). The catalog supplies trusted commands and dependencies to one bounded executor. All repository-owned Python unittest and native Node test populations support independent case execution within the shared worker budget. Use `--jobs N` to bound concurrency; `--jobs 1` retains the same case coverage. Direct suite commands remain available for reproduction. Validators without test cases retain their declared command constraints. Equivalent requests for the same canonical check execute once per invocation; distinct scopes and release configurations retain their own checks. Current validation executes checks and does not reuse a validation-result cache.
