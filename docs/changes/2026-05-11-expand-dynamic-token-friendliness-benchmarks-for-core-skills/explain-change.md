# Explain Change

## Summary

This change expands the token-cost benchmark suite from `skill-token-runtime-v1` to the M1 slice of `skill-token-runtime-v2`.

M1 adds the required core benchmark fixtures for `plan`, `explain-change`, and `pr`, keeps the v1 `architecture` and `learn` prompts as transition carryover benchmarks, and records the optional extended benchmark set in the manifest without implementing optional prompt fixtures yet.

## Changed surfaces

- `benchmarks/token-cost/manifest.yaml`: declares `skill-token-runtime-v2`, v1 comparison metadata, required core benchmarks, transition carryover benchmarks, optional extended benchmark names, and the flat executable prompt list used by the current runner.
- `benchmarks/token-cost/prompts/plan-handoff.md`: adds the required core plan handoff prompt.
- `benchmarks/token-cost/prompts/explain-change-summary.md`: adds the required core explain-change summary prompt.
- `benchmarks/token-cost/prompts/pr-handoff.md`: adds the required core PR handoff prompt.
- `benchmarks/token-cost/prompts/workflow-route.md`: changes the existing prompt to use the same explicit `Output only:` shape enforced by the M1 prompt test.
- `scripts/test-token-cost-measurement.py`: updates the manifest and prompt fixture contract test to enforce v2 suite identity, required core groups, transition carryover, optional extended declarations, prompt existence, no-edit instructions, and bounded output.

## Validation

- `python scripts/test-token-cost-measurement.py BenchmarkFixtureTests.test_manifest_lists_v2_prompt_groups_and_fixtures`
- `python scripts/test-token-cost-measurement.py`
- `python scripts/run-token-cost-benchmarks.py --dry-run --suite benchmarks/token-cost/manifest.yaml --release test --tool codex`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- `git diff --check -- benchmarks/token-cost scripts/test-token-cost-measurement.py docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills`

## Notes

The dry-run command wrote synthetic output under `docs/reports/token-cost/runs/test/`; those generated validation files were removed after the command completed so they are not committed as release evidence.
