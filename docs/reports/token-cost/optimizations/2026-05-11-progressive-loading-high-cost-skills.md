# Progressive Loading High-Cost Skills Optimization

## Status

Post-optimization static and dynamic retest recorded; PR #43 open

## Baseline

Baseline evidence comes from the `v0.1.1` token-friendliness report and the M2 pre-edit static measurement.

Changed skills:

- `workflow`
- `implement`
- `code-review`

## Workflow Detail Migration Table

| Removed or summarized topic | New owner surface | Rationale |
|---|---|---|
| Review-resolution details | `docs/workflows.md`, `specs/rigorloop-workflow.md`, and owning review guidance | The public workflow skill should route to review-resolution, not duplicate detailed disposition policy. |
| Lifecycle-managed artifact table | `docs/workflows.md` and `specs/rigorloop-workflow.md` | Contributor-facing workflow guidance owns full artifact-state tables. |
| Detailed validation layering | `docs/workflows.md`, validation selector tooling, test specs, release specs, and verify guidance | Stage-specific proof selection belongs to validation owners. |
| Detailed default artifact path lists | `docs/workflows.md`, plan examples, and contributor guidance | Public skill text should route from state without requiring long repository path lists. |
| Bugfix and support-stage detail | Owning stage skills and `docs/workflows.md` | Specialized behavior belongs to the stage that owns it. |

No workflow safety topic was removed without a new owner surface or a no-longer-needed rationale.

## Static Skill Size

| Skill | Before estimated tokens | After estimated tokens | Notes |
|---|---:|---:|---|
| `workflow` | 6,674 | 4,857 | Long-form routing detail summarized into public skill and owned in `docs/workflows.md`; still above 4,000 because milestone, review-resolution, and claim-boundary safety anchors remain in the public router. |
| `implement` | 3,542 | 3,963 | Quick guide and handoff inspection budget added to reduce runtime state discovery. |
| `code-review` | 4,726 | 4,671 | Quick guide added and repeated/template prose compressed while preserving protected review contracts. |

Total static estimate changed from 54,294 to 52,843 tokens across 23 skills.

## Dynamic Benchmark Comparison

M4 reran the full required benchmark suite because the runner does not expose a targeted prompt filter. The run used regenerated public Codex skill output from `dist/adapters/codex/.agents/skills/`.

Command:

```bash
python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-progressive-loading-m4
```

| Benchmark | Before input tokens | After input tokens | Before largest output | After largest output | Before full-skill reads | After full-skill reads | Before broad searches | After broad searches | Result quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `workflow-route` | 34,853 | 53,855 | 4,071 | 3,234 | 1 | 1 | 0 | 0 | pass |
| `implement-handoff` | 92,262 | 91,698 | 20,738 | 3,098 | 1 | 1 | 2 | 4 | pass |
| `code-review-small` | 72,313 | 113,726 | 3,177 | 2,850 | 1 | 1 | 0 | 3 | pass |
| `verify-final-pack` | 76,400 | 73,524 | 3,515 | 3,515 | 1 | 1 | 0 | 1 | pass |

Manual M4 result-quality review found no targeted benchmark result-quality regression from `pass` to `fail`. The run outputs stayed within the requested no-edit behavior and output shape for these prompts.

## Requested Retest

After PR handoff, a fresh requested retest reran static measurement and the full dynamic suite on the optimized branch. The dynamic run again used regenerated public Codex skill output from `dist/adapters/codex/.agents/skills/`.

Commands:

```bash
python scripts/measure-skill-tokens.py
python scripts/run-token-cost-benchmarks.py --suite benchmarks/token-cost/manifest.yaml --release v0.1.1 --tool codex --output-dir /tmp/rigorloop-token-progressive-loading-requested-test
```

Static retest result:

| Skill | Before estimated tokens | Retest estimated tokens | Delta |
|---|---:|---:|---:|
| `workflow` | 6,674 | 4,857 | -1,817 |
| `implement` | 3,542 | 3,963 | +421 |
| `code-review` | 4,726 | 4,671 | -55 |
| Total, 23 skills | 54,294 | 52,843 | -1,451 |

Dynamic targeted retest comparison:

| Benchmark | Before input tokens | Retest input tokens | Input delta | Before largest output | Retest largest output | Largest-output delta | Before full-skill reads | Retest full-skill reads | Before broad searches | Retest broad searches | Retest verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `workflow-route` | 34,853 | 53,801 | +18,948 | 4,071 | 3,234 | -837 | 1 | 1 | 0 | 0 | warning |
| `implement-handoff` | 92,262 | 91,577 | -685 | 20,738 | 3,098 | -17,640 | 1 | 1 | 2 | 2 | warning |
| `code-review-small` | 72,313 | 89,577 | +17,264 | 3,177 | 2,850 | -327 | 1 | 1 | 0 | 1 | warning |
| `verify-final-pack` | 76,400 | 94,624 | +18,224 | 3,515 | 3,515 | 0 | 1 | 1 | 0 | 1 | warning |

Dynamic full-suite retest results:

| Benchmark | Retest input tokens | Retest largest output | Retest full-skill reads | Retest broad searches | Retest verdict |
|---|---:|---:|---:|---:|---|
| `workflow-route` | 53,801 | 3,234 | 1 | 0 | warning |
| `proposal-short` | 69,178 | 2,018 | 1 | 0 | warning |
| `plan-handoff` | 90,596 | 2,512 | 1 | 1 | warning |
| `implement-handoff` | 91,577 | 3,098 | 1 | 2 | warning |
| `code-review-small` | 89,577 | 2,850 | 1 | 1 | warning |
| `explain-change-summary` | 93,617 | 1,840 | 1 | 2 | warning |
| `verify-final-pack` | 94,624 | 3,515 | 1 | 1 | warning |
| `pr-handoff` | 94,966 | 2,289 | 1 | 1 | warning |
| `architecture-no-impact` | 33,412 | 2,557 | 1 | 0 | warning |
| `learn-no-durable-lesson` | 33,845 | 3,097 | 1 | 0 | warning |

Targeted largest-command-output total changed from 31,501 estimated tokens before optimization to 12,697 in the requested retest. The largest single targeted command output remains `verify-final-pack` at 3,515 estimated tokens; the measured top offender `implement-handoff` remains substantially reduced at 3,098 estimated tokens.

## Command Output And Reads

- Largest command output before: `implement-handoff`, 20,738 estimated tokens.
- Largest command output after, targeted set: `verify-final-pack`, 3,515 estimated tokens.
- Largest command output after, full required suite: `verify-final-pack`, 3,515 estimated tokens.
- Full-skill read count before: all ten required transition runs read active public skill files.
- Full-skill read count after: all ten required transition runs still read active public skill files.
- Targeted full-skill read count before/after: 4 before, 4 after.
- Targeted broad-search count before/after: 2 before, 8 after.

## Remaining Warnings

`workflow` remains above the 4,000 warning target because the public router still carries safety-critical milestone, review-resolution, autoprogression, claim-boundary, and stop-condition anchors required by existing static validators. It moved below the 5,000 high-warning level.

`code-review` remains above the 4,000 warning target because independent-review posture, mixed-evidence handling, material findings, detailed review records, milestone-aware handoff, stop conditions, and result format remain protected public contracts.

## Dynamic Result Interpretation

The optimization materially reduced command-output amplification for the measured top offender: `implement-handoff` largest command output fell from 20,738 to 3,098 estimated tokens.

The optimization did not eliminate whole-skill-style reads. The requested retest still observed one full-file-style read in every required run, which suggests the remaining read pattern is driven by benchmark prompt/tool behavior rather than static skill text alone.

The broad-search signal remained mixed. In the requested retest, `implement-handoff` returned to the baseline broad-search count of 2, while `code-review-small` and `verify-final-pack` each recorded one broad-search signal. This remains a follow-up measurement target.

`workflow` remains above the 4,000 warning target but below the high-warning threshold, with safety-critical routing and milestone handoff guidance retained. `code-review` remains above the target range because protected independent-review, mixed-evidence, material-finding, detailed-record, milestone-aware handoff, stop-condition, and result-format guidance remains public.
