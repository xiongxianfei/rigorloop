# Adapter Packaging Proof: Plan Assets

## Scope

This record covers M3 adapter packaging proof for the assets-first `plan` pilot.

## Commands

- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_archives_include_packaged_skill_assets AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m3-adapters`
- `python scripts/validate-adapters.py --root /tmp/rigorloop-m3-adapters --version v0.1.5`

## Result

All commands passed.

## Archive Asset Inventory

| Adapter | Archive | Asset entries present |
| --- | --- | --- |
| codex | `/tmp/rigorloop-m3-adapters/rigorloop-adapter-codex-v0.1.5.zip` | `.agents/skills/plan/assets/current-handoff-summary.md`, `.agents/skills/plan/assets/decision-log-row.md`, `.agents/skills/plan/assets/milestone.md`, `.agents/skills/plan/assets/plan-skeleton.md` |
| claude | `/tmp/rigorloop-m3-adapters/rigorloop-adapter-claude-v0.1.5.zip` | `.claude/skills/plan/assets/current-handoff-summary.md`, `.claude/skills/plan/assets/decision-log-row.md`, `.claude/skills/plan/assets/milestone.md`, `.claude/skills/plan/assets/plan-skeleton.md` |
| opencode | `/tmp/rigorloop-m3-adapters/rigorloop-adapter-opencode-v0.1.5.zip` | `.opencode/skills/plan/assets/current-handoff-summary.md`, `.opencode/skills/plan/assets/decision-log-row.md`, `.opencode/skills/plan/assets/milestone.md`, `.opencode/skills/plan/assets/plan-skeleton.md` |

## Boundary

- Generated adapter archives were built from canonical `skills/`.
- No generated adapter skill body or asset was hand-edited.
- Adapter install roots, lockfile behavior, and CLI behavior were not changed.
