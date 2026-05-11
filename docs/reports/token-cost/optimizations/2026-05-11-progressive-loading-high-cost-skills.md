# Progressive Loading High-Cost Skills Optimization

## Status

M2 static evidence recorded; dynamic benchmark comparison pending M4

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

Targeted dynamic benchmark evidence is scheduled for the dynamic benchmark milestone after regenerated public skill output exists.

| Benchmark | Before | After | Result quality |
|---|---|---|---|
| `workflow-route` | v0.1.1 baseline | pending M4 | pending M4 |
| `implement-handoff` | v0.1.1 baseline | pending M4 | pending M4 |
| `code-review-small` | v0.1.1 baseline | pending M4 | pending M4 |
| `verify-final-pack` | v0.1.1 baseline | pending M4 | pending M4 |

## Command Output And Reads

- Largest command output before: `implement-handoff`, 20,738 estimated tokens.
- Largest command output after: pending M4.
- Full-skill read count before: all ten required transition runs read active public skill files.
- Full-skill read count after: pending M4.

## Remaining Warnings

`workflow` remains above the 4,000 warning target because the public router still carries safety-critical milestone, review-resolution, autoprogression, claim-boundary, and stop-condition anchors required by existing static validators. It moved below the 5,000 high-warning level.

`code-review` remains above the 4,000 warning target because independent-review posture, mixed-evidence handling, material findings, detailed review records, milestone-aware handoff, stop conditions, and result format remain protected public contracts.

Dynamic benchmark warnings will be explained after M4 compares regenerated public skill output.
