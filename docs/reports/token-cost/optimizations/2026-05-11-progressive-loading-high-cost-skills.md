# Progressive Loading High-Cost Skills Optimization

## Status

M4 dynamic benchmark evidence recorded; code-review M4 pending

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

The optimization did not eliminate whole-skill-style reads. All required runs still read active public skill files, which suggests the remaining read pattern is driven by benchmark prompt/tool behavior rather than static skill text alone.

The broad-search signal did not improve in this run. `implement-handoff` still recorded broad searches, and `code-review-small` gained broad-search signals. This remains a follow-up measurement target; it is not a result-quality regression because the reviewed benchmark outputs still satisfied the prompt shape and ownership boundaries.

`workflow` remains above the 4,000 warning target but below the high-warning threshold, with safety-critical routing and milestone handoff guidance retained. `code-review` remains above the target range because protected independent-review, mixed-evidence, material-finding, detailed-record, milestone-aware handoff, stop-condition, and result-format guidance remains public.
