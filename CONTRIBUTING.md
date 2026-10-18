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
[System](design/architecture/composition.md#living-test-design-composition) owns shared test-design and proof-quality rules. [Validation](design/support/validation.md) owns source-format checks and validation execution.

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

Run `bash scripts/ci.sh` for the complete essential suite. PR and main CI use the same command; mode, path, worker and report options are retired. Install package dependencies with `npm ci --prefix packages/rigorloop` first. Native Node and Python runners provide discovery, failures and summaries.

The suite covers workflow completion guards, real record persistence/recovery, packed installation/archive integrity and skill resources. [Validation](design/support/validation.md) defines the selected coverage and reduced-assurance areas. No full-product coverage claim follows from a passing essential suite. Changes outside it need explicit affected proof or concrete manual/review evidence. Product generators and validators remain available for that work.

Release qualification runs its own small boundary suite and actual artifact/public checks. Use `python3 tests/engineering/release/test-release-transaction.py` for the local release regressions; it uses controlled public-service fixtures and performs no real publication.

Tests own private mutable fixtures and cleanup. Reuse existing assertions and follow [shared test-design rules](design/support/test-design/rules.md). Current source groups and executable commands are listed in [Validation](design/support/validation.md#test-sources-groups-and-fixtures); the [system test design](design/support/test-design/system-test-design.md) defines stable scenarios and expected observations. Logs and review evidence belong to operational records, not source documents.
